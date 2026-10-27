"""Apply the classification guide and the audit team's house practice to one employer's records.

The worksheet (written per employer by the analyst running the Skill) supplies the judgments the records cannot make on
their own: the code that describes each person's actual duties, which code each type of crew work, job site and
subcontracted trade falls under, and owner status. Everything that is arithmetic or a stated house rule is applied here,
from the records, the same way for every employer.
"""

import datetime
import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from .records import CENT, day, money

FIXED_HOLIDAYS = {(1, 1): "New Year's Day", (7, 4): "Independence Day", (12, 25): "Christmas Day"}


class WorksheetError(ValueError):
    pass


@dataclass
class Line:
    code: str
    amount: Decimal
    basis: str


@dataclass
class Person:
    id: str
    name: str
    position: str
    wages: Decimal
    lines: list = field(default_factory=list)
    records: list = field(default_factory=list)
    employer_code: str | None = None
    evidence: str = ""  # plain statement of the time records, worded for the employer question list

    @property
    def primary_code(self):
        return max(self.lines, key=lambda l: l.amount).code


@dataclass
class Adjustment:
    about: str
    kind: str
    amount: Decimal
    code: str
    detail: str
    records: list
    rule: str


@dataclass
class OpenItem:
    about: str
    proposal: str
    why: str
    records: list
    rule: str = "HP-10"


@dataclass
class Result:
    rec: dict
    ws: dict
    people: list = field(default_factory=list)
    sub_lines: list = field(default_factory=list)
    adjustments: list = field(default_factory=list)
    open_items: list = field(default_factory=list)
    questions: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    totals: dict = field(default_factory=dict)
    inference: str = ""

    @property
    def employer_split(self):
        return {c: v["payroll"] for c, v in self.rec["employer_split"].items()}

    def differences(self):
        codes = sorted(set(self.totals) | set(self.employer_split))
        return {c: self.totals.get(c, Decimal("0.00")) - self.employer_split.get(c, Decimal("0.00")) for c in codes}

    @property
    def accepts_employer_split(self):
        return all(d == 0 for d in self.differences().values()) and not any(
            p.employer_code and {l.code for l in p.lines} != {p.employer_code} for p in self.people)


def _uniq(items):
    return list(dict.fromkeys(i for i in items if i))


def fmt(amount):
    return f"{amount:,.2f}"


def infer_employer_codes(register, split):
    """Find the one assignment of register employees to the employer's codes that reproduces its split.

    Returns (mapping or None, explanation). The application gives only a head count and payroll per code, so a
    per-person reading of the employer's split is an inference and is labelled as one.
    """
    codes = list(split)
    if len(codes) ** len(register) > 3_000_000:
        return None, "too many employees to infer the employer's per-person split from its totals"
    hits = []
    for combo in itertools.product(codes, repeat=len(register)):
        counts, sums = Counter(combo), defaultdict(Decimal)
        if any(counts[c] != split[c]["employees"] for c in codes):
            continue
        for code, e in zip(combo, register):
            sums[code] += e["wages"]
        if all(sums[c] == split[c]["payroll"] for c in codes):
            hits.append(dict(zip((e["id"] for e in register), combo)))
            if len(hits) > 1:
                return None, "more than one way to read the employer's split per person; it is compared by code only"
    if not hits:
        return None, ("no assignment of register wages reproduces the employer's split exactly; "
                      "it is compared by code only")
    return hits[0], ("the employer's per-person codes are inferred: exactly one assignment of the register's wages "
                     "reproduces its reported head count and payroll for every code")


def allocate(guide, hp, rec, ws):
    res = Result(rec, ws)
    clerical = hp["clerical_code"]
    threshold = int(hp["clerical_job_site_day_threshold"])
    owner_flat = money(hp["owner_field_work_flat_payroll"])
    sub_share = Decimal(hp["uninsured_subcontractor_payroll_share"])
    allowance_cap = money(hp["out_of_town_daily_allowance_exclusion"])
    start, end = rec["period"]
    in_period = lambda d: start <= d <= end  # noqa: E731
    reg_file = rec["register_file"]

    def code_ok(code, where):
        if not code:
            raise WorksheetError(f"{where} is not filled in; decide it from the records (see SKILL.md, step 3)")
        try:
            guide.ref_for(code)
        except ValueError as exc:
            raise WorksheetError(f"{where}: {exc}") from None
        return code

    ws_people = ws.get("employees", {})
    missing = [e["id"] for e in rec["register"] if e["id"] not in ws_people]
    extra = [i for i in ws_people if i not in {e["id"] for e in rec["register"]}]
    if missing or extra:
        raise WorksheetError(f"worksheet employees do not match {reg_file}: missing {missing or 'none'}, "
                             f"not on register {extra or 'none'}")

    def out_of_period(rows, key, file):
        n = sum(1 for r in rows if r.get(key) and not in_period(day(r[key])))
        if n:
            res.notes.append(f"{n} row(s) in {file} fall outside the audit period and were not used.")

    # Index the supporting records, audit period only.
    timesheets = defaultdict(list)
    for r in rec["timesheets"]:
        if in_period(day(r["date"])):
            timesheets[r["employee_id"]].append(r)
    out_of_period(rec["timesheets"], "date", rec["timesheets_file"])

    site_days = defaultdict(lambda: defaultdict(set))
    for r in rec["signins"]:
        if r["employee_id"] and in_period(day(r["date"])):
            site_days[r["employee_id"]][day(r["date"])].add(r["site"])
    others = [r for r in rec["signins"] if not r["employee_id"]]
    if others:
        res.notes.append(f"{len(others)} sign-in row(s) in {rec['signins_file']} have no employee ID "
                         f"({', '.join(sorted({r.get('name', '?') for r in others}))}); they are not employees and were not used.")
    out_of_period(rec["signins"], "date", rec["signins_file"])

    ride_days = defaultdict(set)
    for r in rec["route_log"]:
        if r["ride_along_id"] and in_period(day(r["date"])):
            ride_days[r["ride_along_id"]].add(day(r["date"]))
    out_of_period(rec["route_log"], "date", rec["route_log_file"])

    weekly = defaultdict(list)
    for r in rec["weekly_payroll"]:
        weekly[r["employee_id"]].append((day(r["week_start"]), day(r["week_end"]), money(r["gross_pay"])))

    work_codes = ws.get("work_type_codes", {})
    site_codes = ws.get("site_codes", {})
    route_code = ws.get("route_code") and code_ok(ws["route_code"], "route_code")
    if ride_days and not route_code:
        raise WorksheetError(f"{rec['route_log_file']} records ride-alongs, but worksheet route_code is not filled in")
    split_people, ride_people = [], []

    for e in rec["register"]:
        w = ws_people[e["id"]]
        duty = code_ok(w.get("duty_code") or "", f"employees.{e['id']}.duty_code")
        p = Person(e["id"], e["name"], e["position"], e["wages"], records=[reg_file] + w.get("records", []))
        owner = ws.get("owners", {}).get(e["id"])

        if owner and owner.get("included") and owner.get("field_work"):
            code = code_ok(owner.get("field_code") or duty, f"owners.{e['id']}.field_code")
            p.records = _uniq(p.records + owner.get("records", []))
            p.lines = [Line(code, owner_flat, f"Included owner who does field work ({owner['basis']}). Counted at the "
                                              f"flat {fmt(owner_flat)} (HP-3) under the code for the work done (CG-05).")]
            res.adjustments.append(Adjustment(
                e["name"], "Owner counted at flat amount", owner_flat, code,
                f"{reg_file} shows wages of {fmt(e['wages'])}. House practice counts an owner who does any field work at "
                f"{fmt(owner_flat)}, under {code}, the code for the work done.", _uniq(p.records), "HP-3, CG-05"))
            res.people.append(p)
            continue

        final, basis = duty, w["basis"]
        hours = timesheets.get(e["id"])
        if hours:
            by_code, by_type = defaultdict(Decimal), defaultdict(Decimal)
            for r in hours:
                if r["work_type"] not in work_codes:
                    raise WorksheetError(f"work type {r['work_type']!r} in {rec['timesheets_file']} has no entry in "
                                         f"worksheet work_type_codes")
                code = code_ok(work_codes[r["work_type"]], f"work_type_codes.{r['work_type']}")
                by_code[code] += Decimal(r["hours"])
                by_type[r["work_type"]] += Decimal(r["hours"])
            ranked = sorted(by_code.items(), key=lambda kv: -kv[1])
            leaders = [c for c, h in ranked if h == ranked[0][1]]
            final = duty if duty in leaders else leaders[0]
            mix = ", ".join(f"{t} {h:g} h" for t, h in sorted(by_type.items(), key=lambda kv: -kv[1]))
            basis = (f"Crew timesheets: {mix}. The whole of the pay goes to {final}, the code with the most recorded "
                     f"hours (HP-2: one person's pay is not split; reading A2).")
            p.records.append(rec["timesheets_file"])
            p.evidence = f"{rec['timesheets_file']} records {mix} for {e['name']}."
            if len(by_code) > 1:
                split_people.append((p, dict(by_code), final))
            if len(leaders) > 1:
                res.open_items.append(OpenItem(
                    e["name"], f"Report all of {e['name']}'s pay under {final}.",
                    f"The timesheets show equal hours under {', '.join(leaders)}, and house practice does not say how "
                    f"to break a tie.", [rec["timesheets_file"]]))
        elif duty == clerical and site_days.get(e["id"]):
            days = site_days[e["id"]]
            p.records.append(rec["signins_file"])
            dates = ", ".join(d.isoformat() for d in sorted(days))
            p.evidence = (f"{rec['signins_file']} records {e['name']} at a job site on {len(days)} day(s): " + "; ".join(
                f"{d.isoformat()} {', '.join(sorted(days[d]))}" for d in sorted(days)) + ".")
            for d in sorted(days):
                if (d.month, d.day) in FIXED_HOLIDAYS:
                    res.open_items.append(OpenItem(
                        f"{e['name']}: sign-in on {d.isoformat()}",
                        "Count the day as recorded, because the records decide (HP-7).",
                        f"{rec['signins_file']} records {e['name']} at {', '.join(sorted(days[d]))} on "
                        f"{FIXED_HOLIDAYS[(d.month, d.day)]}. This may be a recording error.", [rec["signins_file"]]))
            if len(days) < threshold:
                basis += (f" {rec['signins_file']} shows {len(days)} job-site day(s) ({dates}), fewer than "
                          f"{threshold}, so the person stays {clerical} (HP-4).")
            else:
                unmapped = sorted({s for sites in days.values() for s in sites if s not in site_codes})
                if unmapped:
                    raise WorksheetError(f"site(s) {unmapped} in {rec['signins_file']} have no entry in worksheet "
                                         f"site_codes (use null when no code in the guide describes the work there)")
                code_days = Counter()
                for sites in days.values():
                    for c in {site_codes[s] for s in sites} - {None}:
                        code_days[c] += 1
                chosen = w.get("field_code")
                ranked = code_days.most_common()
                if not chosen and ranked:
                    leaders = [c for c, n in ranked if n == ranked[0][1]]
                    chosen = leaders[0] if len(leaders) == 1 else None
                    if len(leaders) > 1:
                        res.open_items.append(OpenItem(
                            e["name"], f"Keep {e['name']} under {clerical} until the employer confirms the work at the sites.",
                            f"The sites visited split evenly between {', '.join(leaders)}.", [rec["signins_file"]]))
                site_mix = ", ".join(f"{c} {n} day(s)" for c, n in ranked) or "no code in the guide describes the site work"
                if chosen:
                    final = code_ok(chosen, f"employees.{e['id']}.field_code")
                    basis = (f"{w['basis']} {rec['signins_file']} shows {len(days)} job-site days ({dates}), so the "
                             f"person is not clerical (HP-4: {threshold} or more days). Days by site code: {site_mix}. "
                             f"The person is reported under {final} (reading A3).")
                    res.open_items.append(OpenItem(
                        e["name"], f"Report all {fmt(e['wages'])} of {e['name']}'s pay under {final} instead of {clerical}.",
                        f"{len(days)} job-site days is at or above the {threshold}-day threshold (HP-4). House practice "
                        f"does not say which code replaces {clerical}. {final} is the code of the work at the sites "
                        f"visited ({site_mix}).", [rec["signins_file"]] + w.get("records", [])))
                else:
                    basis += (f" {rec['signins_file']} shows {len(days)} job-site days ({dates}), but no code in the "
                              f"guide describes the work at those sites, so the person stays {clerical}.")
                    res.open_items.append(OpenItem(
                        e["name"], f"Keep {e['name']} under {clerical}.",
                        f"{len(days)} job-site days meets the {threshold}-day threshold (HP-4), but no code in the guide "
                        f"describes the work at the sites ({', '.join(sorted({s for v in days.values() for s in v}))}). "
                        f"House practice does not say what happens then.", [rec["signins_file"]] + w.get("records", [])))
        p.lines = [Line(final, e["wages"], basis)]

        rides = ride_days.get(e["id"])
        if route_code and rides and final != route_code:
            weeks = sorted(weekly.get(e["id"], []))
            p.records += [rec["route_log_file"]]
            if not weeks:
                res.open_items.append(OpenItem(
                    e["name"], f"Leave all of {e['name']}'s pay under {final}.",
                    f"The route log shows {len(rides)} ride-along days, but there is no weekly pay record, so the "
                    f"pay cannot be split by whole weeks (HP-2).", [rec["route_log_file"]]))
            else:
                p.records.append(rec["weekly_payroll_file"])
                ride_weeks = [(s, t, g) for s, t, g in weeks if any(s <= d <= t for d in rides)]
                moved = sum((g for _, _, g in ride_weeks), Decimal("0.00"))
                weekly_total = sum((g for _, _, g in weeks), Decimal("0.00"))
                if weekly_total != e["wages"]:
                    res.open_items.append(OpenItem(
                        e["name"], f"Use {reg_file} for the total and {rec['weekly_payroll_file']} for the week split.",
                        f"The weekly pay totals {fmt(weekly_total)} but {reg_file} shows {fmt(e['wages'])}.",
                        [reg_file, rec["weekly_payroll_file"]]))
                p.lines = [
                    Line(route_code, moved, f"{rec['route_log_file']} shows {len(rides)} ride-along days in "
                                            f"{len(ride_weeks)} pay weeks. Those whole weeks' pay goes to {route_code} "
                                            f"(HP-2, reading A1)."),
                    Line(final, e["wages"] - moved, f"{basis} The other {len(weeks) - len(ride_weeks)} pay weeks stay "
                                                    f"under {final}."),
                ]
                ride_people.append((p, rides, ride_weeks, weeks, moved))
                res.adjustments.append(Adjustment(
                    e["name"], "Whole-week route split", moved, route_code,
                    f"{len(rides)} ride-along days ({min(rides).isoformat()} to {max(rides).isoformat()}) fall in "
                    f"{len(ride_weeks)} of {len(weeks)} pay weeks. Those weeks' gross pay of {fmt(moved)} moves from "
                    f"{final} to {route_code}.", [rec["route_log_file"], rec["weekly_payroll_file"]], "HP-2"))

        if e["travel_allowance"]:
            tdays = e["travel_days"] or 0
            excluded = min(e["travel_allowance"], allowance_cap * tdays)
            excess = e["travel_allowance"] - excluded
            p.records.append(f"{reg_file} (travel_days, travel_allowance_paid)")
            if excess:
                p.lines.append(Line(final, excess, f"Out-of-town allowance above {fmt(allowance_cap)} per day: "
                                                   f"{fmt(e['travel_allowance'])} paid for {tdays} travel days, "
                                                   f"{fmt(excluded)} excluded (HP-6)."))
                res.adjustments.append(Adjustment(
                    e["name"], "Travel allowance above the daily exclusion", excess, final,
                    f"{fmt(e['travel_allowance'])} paid for {tdays} recorded travel days. Up to {fmt(allowance_cap)} "
                    f"per day ({fmt(excluded)}) is left out; the remaining {fmt(excess)} is payroll.",
                    [f"{reg_file} (travel_days, travel_allowance_paid)"], "HP-6"))
            if tdays == 0:
                res.open_items.append(OpenItem(
                    e["name"], f"Count all {fmt(e['travel_allowance'])} of the allowance as payroll under {final}.",
                    f"{reg_file} records a travel allowance but no travel days. House practice excludes up to "
                    f"{fmt(allowance_cap)} per travel day, so with no recorded days nothing is excluded (reading A6).",
                    [reg_file]))
        p.records = _uniq(p.records)
        res.people.append(p)

    _subcontractors(res, rec, ws, code_ok, sub_share, in_period)

    if split_people:
        rows = "; ".join(f"{p.name}: " + ", ".join(f"{c} {h:g} h" for c, h in sorted(bc.items(), key=lambda kv: -kv[1]))
                         + f" -> {f}" for p, bc, f in split_people)
        res.open_items.append(OpenItem(
            "Crew members with more than one type of work",
            "Report each person's whole pay under the code with the most recorded hours.",
            f"CG-07 allows a division when time records are kept, but house practice is that one person's pay is not "
            f"split, except for route ride-alongs (HP-2). House practice does not say which single code to use. "
            f"Hours by code: {rows}.", [rec["timesheets_file"]]))
    if ride_people:
        res.open_items.append(OpenItem(
            "Reading of 'split the pay by whole weeks'",
            "Any pay week with at least one ride-along day goes wholly to the route code (reading A1).",
            "A narrower reading, counting only weeks spent wholly on the road, would move less payroll. "
            + "; ".join(f"{p.name}: {len(r)} ride days in {len(rw)} of {len(wk)} weeks, {fmt(m)} moved"
                        for p, r, rw, wk, m in ride_people) + ".",
            [rec["route_log_file"], rec["weekly_payroll_file"]]))

    for item in ws.get("open_items", []):
        target = next((o for o in res.open_items if o.about == item.get("merge_with")), None)
        if target:  # the analyst's context for an item the rules already raised
            target.proposal = item.get("proposal", target.proposal)
            target.why += " " + item["why"]
            target.records = _uniq(target.records + item.get("records", []))
        else:
            res.open_items.append(OpenItem(item["about"], item["proposal"], item["why"], item.get("records", []),
                                           item.get("rule", "HP-10")))

    totals = defaultdict(Decimal)
    for line in [l for p in res.people for l in p.lines] + res.sub_lines:
        totals[line.code] += line.amount
    res.totals = {c: v.quantize(CENT) for c, v in sorted(totals.items()) if v}

    mapping, res.inference = infer_employer_codes(rec["register"], rec["employer_split"])
    for p in res.people:
        p.employer_code = (mapping or {}).get(p.id)
        if p.employer_code and p.primary_code != p.employer_code and not any(a.about == p.name for a in res.adjustments):
            res.adjustments.append(Adjustment(
                p.name, "Reclassified", p.wages, p.primary_code,
                f"The employer reported {p.name} ({p.position}) under {p.employer_code}. The records put the "
                f"{fmt(p.wages)} under {p.primary_code}: {p.lines[0].basis}", p.records, "HP-1, HP-7"))
        for a in res.adjustments:
            if a.about == p.name and a.kind != "Reclassified" and p.employer_code and p.employer_code != a.code:
                a.detail += f" The employer reported {p.name} under {p.employer_code}."

    _questions(res, rec, ws)
    return res


def _subcontractors(res, rec, ws, code_ok, share, in_period):
    if not rec["sub_payments"]:
        return
    certs = defaultdict(list)
    for c in rec["certificates"]:
        certs[c["subcontractor"]].append((c["certificate_no"], day(c["coverage_from"]), day(c["coverage_to"])))
    matches = ws.get("subcontractor_certificate_matches", {})
    work_codes = ws.get("subcontract_work_codes", {})
    files = _uniq([rec["sub_payments_file"], rec["certificates_file"]])
    by_sub = defaultdict(list)
    for pay in rec["sub_payments"]:
        if in_period(day(pay["date"])):
            by_sub[pay["subcontractor"]].append(pay)
        else:
            res.notes.append(f"{pay['subcontractor']} invoice {pay.get('invoice', '?')} ({pay['date']}, "
                             f"{fmt(money(pay['amount_paid']))}) in {rec['sub_payments_file']} falls outside the audit "
                             f"period and was not used.")

    for sub, pays in by_sub.items():
        cert_name = sub if sub in certs else matches.get(sub)
        if cert_name and cert_name != sub:
            res.open_items.append(OpenItem(
                sub, f"Treat the certificate issued to '{cert_name}' as {sub}'s.",
                f"{rec['sub_payments_file']} pays '{sub}', but the certificate in {rec['certificates_file']} is issued "
                f"to '{cert_name}'. The names are close but not the same.", files))
        insured, uninsured = [], []
        for pay in pays:
            d = day(pay["date"])
            cover = [c for c in certs.get(cert_name, []) if c[1] <= d <= c[2]]
            (insured if cover else uninsured).append((pay, cover))
        for pay, _ in uninsured:
            work = pay["work"]
            if work not in work_codes:
                raise WorksheetError(f"subcontracted work {work!r} has no entry in worksheet subcontract_work_codes")
            code = code_ok(work_codes[work], f"subcontract_work_codes.{work}")
            paid = money(pay["amount_paid"])
            added = (paid * share).quantize(CENT, rounding=ROUND_HALF_UP)
            held = certs.get(cert_name, [])
            why = ("no certificate of insurance for this subcontractor is in the file" if not held else
                   "the certificate in the file (" + "; ".join(f"{n}, {f.isoformat()} to {t.isoformat()}" for n, f, t in held)
                   + f") does not cover the payment date {pay['date']}")
            res.sub_lines.append(Line(code, added, f"{share:.0%} of {fmt(paid)} paid to uninsured subcontractor {sub} "
                                                   f"(invoice {pay.get('invoice', '?')}, {pay['date']}, {work}) (HP-5, CG-06)."))
            res.adjustments.append(Adjustment(
                f"{sub}, invoice {pay.get('invoice', '?')}", "Uninsured subcontractor payment added", added, code,
                f"{fmt(paid)} paid on {pay['date']} for {work}. Because {why}, {share:.0%} ({fmt(added)}) is added to "
                f"payroll under {code}, the code for the work.", files, "HP-5, CG-06"))
        res.notes.append(f"{sub}: {len(insured)} payment(s) covered by a certificate in the file, "
                         f"{len(uninsured)} not covered.")
        res.questions.append((sub, _sub_question(sub, cert_name, insured, uninsured, rec)))


def _sub_question(sub, cert_name, insured, uninsured, rec):
    parts = []
    if insured:
        nos = sorted({c[0] for _, cov in insured for c in cov})
        parts.append(f"confirm that certificate {', '.join(nos)} covered {sub}'s own workers on the dates of invoices "
                     + ", ".join(f"{p.get('invoice', '?')} ({p['date']}, {fmt(money(p['amount_paid']))})" for p, _ in insured))
    if uninsured:
        parts.append("send a workers' compensation certificate covering the dates of invoices "
                     + ", ".join(f"{p.get('invoice', '?')} ({p['date']}, {fmt(money(p['amount_paid']))})" for p, _ in uninsured)
                     + "; without one, 60% of each payment stays in payroll")
    lead = f"{sub} ({rec['sub_payments_file']}" + (f", {rec['certificates_file']}" if rec["certificates_file"] else "") + ")"
    return f"{lead}: please " + ", and ".join(parts) + "."


def _questions(res, rec, ws):
    """Every adjustment, and every record a decision rests on, gets at least one employer question (HP-9)."""
    reg = rec["register_file"]
    adjusted = {a.about for a in res.adjustments}
    sub_qs = list(res.questions)
    res.questions = []
    q = lambda about, text: res.questions.append((about, text))  # noqa: E731

    for a in res.adjustments:
        if a.kind == "Uninsured subcontractor payment added":
            continue
        p = next((p for p in res.people if p.name == a.about), None)
        if a.kind == "Owner counted at flat amount":
            q(a.about, f"{a.about} ({', '.join(p.records)}): please confirm that {a.about} is an included owner "
                       f"(no election of exclusion on file) who did field work during the audit period, and the "
                       f"{fmt(p.wages)} of wages shown in {reg}.")
        elif a.kind == "Whole-week route split":
            q(a.about, f"{a.about} ({rec['route_log_file']}, {rec['weekly_payroll_file']}): please confirm that "
                       f"{a.about} rode along on the route days the route log records, and the weekly gross pay "
                       f"in those weeks (total {fmt(a.amount)}).")
        elif a.kind == "Travel allowance above the daily exclusion":
            row = next(e for e in rec["register"] if e["name"] == a.about)
            if row["travel_days"]:
                q(a.about, f"{a.about} ({reg}, travel columns): please confirm the {row['travel_days']} out-of-town "
                           f"travel days and the {fmt(row['travel_allowance'])} allowance paid, with the trip dates and job.")
            else:
                q(a.about, f"{a.about} ({reg}, travel columns): the register shows a {fmt(row['travel_allowance'])} "
                           f"travel allowance but no travel days. Please say what the payment was for and, if it was "
                           f"for out-of-town work, send the dates and job.")
        elif a.kind == "Reclassified":
            recs = ", ".join(r for r in p.records if r != reg)
            q(a.about, f"{a.about} ({recs or reg}): the application reports {a.about} ({p.position}) under "
                       f"{p.employer_code}. {p.evidence or 'The records describe other work.'} Please confirm "
                       f"{a.about}'s actual duties during the audit period and that these records are complete.")

    for p in res.people:
        if p.name in adjusted:
            continue
        if p.evidence:
            q(p.name, f"{p.name} ({', '.join(r for r in p.records if r != reg)}): {p.evidence} Please confirm that "
                      f"these records are complete and correct for the audit period.")
        travel = next((e for e in rec["register"] if e["id"] == p.id and e["travel_allowance"]), None)
        if travel:
            q(p.name, f"{p.name} ({reg}, travel columns): please confirm the {travel['travel_days']} travel days and the "
                      f"{fmt(travel['travel_allowance'])} allowance paid.")

    if res.people:
        listing = "; ".join(f"{p.name}, {p.position}, {fmt(p.wages)} (first pass: "
                            + ", ".join(f"{fmt(l.amount)} {l.code}" for l in p.lines) + ")" for p in res.people)
        q("Payroll register", f"{reg}: please confirm that these wages are complete for the audit period "
                              f"{rec['period'][0].isoformat()} to {rec['period'][1].isoformat()}, and that each "
                              f"person's work matches the code given: {listing}.")

    res.questions += sub_qs
    for c in ws.get("confirmations", []):
        q(c["about"], c["question"])
    for item in ws.get("open_items", []):
        if item.get("employer_question"):
            q(item["about"], item["employer_question"])
