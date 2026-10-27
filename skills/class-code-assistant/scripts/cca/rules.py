"""Apply the classification guide and the audit team's confirmed house practice to one employer's records.

The worksheet (written per employer by the analyst running the Skill) supplies the judgments the records cannot make on
their own: the code that describes each person's actual duties, which code each type of crew work and subcontracted
trade falls under, owner status, and which receipts columns are off-site catering. Everything that is arithmetic or a
confirmed house rule (references/house-practice.md, HP-n) is applied here, from the records, the same way for every
employer. Where a rule leaves a detail open, the Skill's reading (R-n) is applied and raised as an open item.
"""

import datetime
import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from .records import CENT, day, money

FIXED_HOLIDAYS = {(1, 1): "New Year's Day", (7, 4): "Independence Day", (12, 25): "Christmas Day"}  # reading R15
ZERO = Decimal("0.00")


def _holiday(d):
    return FIXED_HOLIDAYS.get((d.month, d.day))


def _crew_code(by_code, duty, hp, employer_codes):
    """One code for a crew member's whole pay from timesheet days (HP-2, HP-13). Returns (code, basis, tied codes, rule).

    At a contractor that does both roofing and siding, 15 or more roof days puts the worker under the roof code and fewer
    under the siding code (HP-16). Any other mix of work has no stated test: the code with the most days (reading R2)."""
    roof, siding = hp["roof_code"], hp["siding_code"]
    if {roof, siding} <= employer_codes and set(by_code) <= {roof, siding}:
        need, n = int(hp["roof_days_for_roof_code"]), len(by_code.get(roof, ()))
        code = roof if n >= need else siding
        edge = (f" This is exactly at the line: one roof day fewer would put the whole pay under {siding}." if n == need
                else f" This is one day short of the line: one more roof day would put the whole pay under {roof}."
                if n == need - 1 else "")
        return code, (f"{n} roof day(s) in the audit period ({'at or above' if n >= need else 'below'} {need}).{edge} At a "
                      f"contractor that does both roofing and siding, a field worker with {need} or more roof days goes "
                      f"entirely under {roof} and one with fewer entirely under {siding}; one worker's pay is never split "
                      f"(HP-16)."), [], "HP-16"
    days = {c: len(d) for c, d in by_code.items()}
    top = max(days.values())
    leaders = [c for c, n in sorted(days.items(), key=lambda kv: -kv[1]) if n == top]
    code = duty if duty in leaders else leaders[0]
    return code, (f"One person's pay is not split (HP-2) and tests are in days (HP-13); the whole pay goes to {code}, "
                  f"the code with the most recorded days (reading R2)."), leaders, "R2"


@dataclass
class Questionable:
    """A record used as written and sent to the employer to confirm (HP-15), with whether the decision rests on it."""
    about: str
    record: str
    detail: str
    effect: str
    decisive: Decimal | None = None  # payroll whose code would change without the record


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
    question: str = ""  # the employer question that would settle it (HP-10: open item for the employer to confirm)


@dataclass
class Result:
    rec: dict
    ws: dict
    people: list = field(default_factory=list)
    sub_lines: list = field(default_factory=list)
    adjustments: list = field(default_factory=list)
    open_items: list = field(default_factory=list)
    questionable: list = field(default_factory=list)  # Questionable: used as written, sent to the employer (HP-15)
    questions: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    applied: list = field(default_factory=list)  # confirmed rules (HP-n) that changed or decided something
    totals: dict = field(default_factory=dict)
    governing_code: str | None = None
    reconciliation: list = field(default_factory=list)
    inference: str = ""

    @property
    def employer_split(self):
        return {c: v["payroll"] for c, v in self.rec["employer_split"].items()}

    def differences(self):
        codes = sorted(set(self.totals) | set(self.employer_split))
        return {c: self.totals.get(c, ZERO) - self.employer_split.get(c, ZERO) for c in codes}

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

    The application gives only a head count and payroll per code. The pairing is used only to explain where the first
    pass differs from the employer; it never decides a classification (HP-1: not by application estimates).
    """
    codes = list(split)
    if len(codes) ** len(register) > 3_000_000:
        return None, "too many employees to pair the employer's split with people; it is compared by code only"
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
                return None, "more than one pairing of people fits the employer's split; it is compared by code only"
    if not hits:
        return None, "no pairing of register wages reproduces the employer's split exactly; it is compared by code only"
    return hits[0], ("the application names no people; exactly one pairing of register wages reproduces its head count "
                     "and payroll for every code, so 'Employer's code' shows that pairing. It explains differences "
                     "only and decided no classification (HP-1)")


def allocate(guide, hp, rec, ws):
    res = Result(rec, ws)
    clerical = hp["clerical_code"]
    threshold = int(hp["clerical_job_site_day_threshold"])
    min_ride = int(hp["route_split_min_ride_days_per_week"])
    owner_flat = money(hp["owner_flat_payroll"])
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

    def applied(rule):
        if rule not in res.applied:
            res.applied.append(rule)

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
    route_code = ws.get("route_code") and code_ok(ws["route_code"], "route_code")
    if ride_days and not route_code:
        raise WorksheetError(f"{rec['route_log_file']} records ride-alongs, but worksheet route_code is not filled in")
    split_people, pending, owners = [], [], []

    # Pass 1: each person's own code from duties and time records.
    for e in rec["register"]:
        w = ws_people[e["id"]]
        duty = code_ok(w.get("duty_code") or "", f"employees.{e['id']}.duty_code")
        p = Person(e["id"], e["name"], e["position"], e["wages"], records=[reg_file] + w.get("records", []))
        owner = ws.get("owners", {}).get(e["id"])

        if owner and owner.get("included"):
            p.records = _uniq(p.records + owner.get("records", []))
            if owner.get("field_work"):
                code = code_ok(owner.get("field_code") or duty, f"owners.{e['id']}.field_code")
                p.lines = [Line(code, owner_flat, f"Working owner who does field work ({owner['basis']}). Counted at the "
                                                  f"flat {fmt(owner_flat)}, regardless of actual wages, under the "
                                                  f"employer's trade code {code} (HP-3).")]
                res.adjustments.append(Adjustment(
                    e["name"], "Owner counted at flat amount", owner_flat, code,
                    f"{reg_file} shows wages of {fmt(e['wages'])}. A working owner who does any field work is counted "
                    f"at {fmt(owner_flat)} regardless of actual wages, under the employer's trade code {code} "
                    f"(difference {fmt(owner_flat - e['wages'])}).", _uniq(p.records), "HP-3"))
                owners.append(p)
                applied("HP-3")
            else:
                p.lines = [Line(clerical, owner_flat, f"Owner who never works in the field ({owner['basis']}). Counted "
                                                      f"at the flat {fmt(owner_flat)} under {clerical} (HP-3).")]
                res.adjustments.append(Adjustment(
                    e["name"], "Owner counted at flat amount", owner_flat, clerical,
                    f"{reg_file} shows wages of {fmt(e['wages'])}. An owner who never works in the field is counted at "
                    f"the same flat {fmt(owner_flat)} under {clerical} (difference {fmt(owner_flat - e['wages'])}).",
                    _uniq(p.records), "HP-3"))
                applied("HP-3")
            res.people.append(p)
            continue

        final, basis = duty, w["basis"]
        rows = timesheets.get(e["id"])
        if rows:
            by_code, by_type = defaultdict(set), defaultdict(set)
            for r in rows:
                if r["work_type"] not in work_codes:
                    raise WorksheetError(f"work type {r['work_type']!r} in {rec['timesheets_file']} has no entry in "
                                         f"worksheet work_type_codes")
                code = code_ok(work_codes[r["work_type"]], f"work_type_codes.{r['work_type']}")
                by_code[code].add(day(r["date"]))
                by_type[r["work_type"]].add(day(r["date"]))
            final, why, leaders, rule = _crew_code(by_code, duty, hp, set(work_codes.values()))
            mix = ", ".join(f"{t} {len(d)} days" for t, d in sorted(by_type.items(), key=lambda kv: -len(kv[1])))
            basis = f"{rec['timesheets_file']}: {mix}. {why}"
            p.records.append(rec["timesheets_file"])
            p.evidence = f"{rec['timesheets_file']} records {mix} for {e['name']}."
            applied("HP-13")
            if rule == "HP-16":
                applied("HP-16")
                n, need = len(by_code.get(hp["roof_code"], ())), int(hp["roof_days_for_roof_code"])
                if n in (need, need - 1):
                    p.evidence += (f" That is {n} roof days, {'exactly at' if n == need else 'one day short of'} the "
                                   f"{need}-day line between {hp['roof_code']} and {hp['siding_code']}, so each roof day "
                                   f"matters.")
            elif len(by_code) > 1:
                split_people.append((p, {c: len(d) for c, d in by_code.items()}, final))
            if len(leaders) > 1:
                res.open_items.append(OpenItem(
                    e["name"], f"Report all of {e['name']}'s pay under {final}.",
                    f"The timesheets show equal days under {', '.join(leaders)}. Nadia has no rule for an exact tie "
                    f"(interview 3).", [rec["timesheets_file"]], "HP-10, R2",
                    f"{e['name']} ({rec['timesheets_file']}): {p.evidence} Please confirm which work {e['name']} "
                    f"mainly did during the audit period."))
            hol = {d for ds in by_code.values() for d in ds if _holiday(d)}
            if hol:
                alt = _crew_code({c: ds - hol for c, ds in by_code.items() if ds - hol}, duty, hp,
                                 set(work_codes.values()))[0] if any(ds - hol for ds in by_code.values()) else None
                them = "it" if len(hol) == 1 else "them"
                effect = (f"Decisive: without {them} the whole {fmt(e['wages'])} would go under {alt}, not {final}."
                          if alt and alt != final else f"Not decisive: without {them} the code is still {final}.")
                res.questionable.append(Questionable(
                    e["name"], rec["timesheets_file"],
                    f"{rec['timesheets_file']} records {e['name']} working on "
                    + ", ".join(f"{d.isoformat()} ({_holiday(d)}, {', '.join(sorted(t for t, ds in by_type.items() if d in ds))})"
                                for d in sorted(hol)),
                    effect, e["wages"] if alt and alt != final else None))
        elif duty == clerical and site_days.get(e["id"]):
            days = site_days[e["id"]]
            p.records.append(rec["signins_file"])
            dates = ", ".join(d.isoformat() for d in sorted(days))
            p.evidence = (f"{rec['signins_file']} records {e['name']} at a job site on {len(days)} day(s): " + "; ".join(
                f"{d.isoformat()} {', '.join(sorted(days[d]))}" for d in sorted(days)) + ".")
            hol = [d for d in sorted(days) if _holiday(d)]
            if hol:
                left = len(days) - len(hol)
                decisive = len(days) >= threshold > left
                effect = (f"Decisive: without {'it' if len(hol) == 1 else 'them'} {e['name']} has {left} job-site days, "
                          f"fewer than {threshold}, and would stay {clerical}." if decisive else
                          f"Not decisive: without {'it' if len(hol) == 1 else 'them'} {e['name']} still has {left} "
                          f"job-site days, {'five or more' if left >= threshold else f'and stays {clerical} either way'}.")
                res.questionable.append(Questionable(
                    e["name"], rec["signins_file"],
                    f"{rec['signins_file']} records {e['name']} at " + "; ".join(
                        f"{', '.join(sorted(days[d]))} on {d.isoformat()} ({_holiday(d)})" for d in hol),
                    effect, e["wages"] if decisive else None))
            if len(days) < threshold:
                basis += (f" {rec['signins_file']} shows {len(days)} job-site day(s) in the audit period ({dates}), "
                          f"fewer than {threshold}, so the person stays {clerical} (HP-4).")
                applied("HP-4")
            else:
                pending.append((p, w, days, dates))
        p.lines = [Line(final, e["wages"], basis)]

        rides = ride_days.get(e["id"])
        if route_code and rides and final != route_code:
            weeks = sorted(weekly.get(e["id"], []))
            p.records += [rec["route_log_file"]]
            if not weeks:
                res.open_items.append(OpenItem(
                    e["name"], f"Leave all of {e['name']}'s pay under {final}.",
                    f"{rec['route_log_file']} shows {len(rides)} ride-along days, but there is no weekly pay record, so "
                    f"the whole-week test (HP-2) cannot be applied.", [rec["route_log_file"]], "HP-2, HP-10",
                    f"{e['name']} ({rec['route_log_file']}): please send {e['name']}'s weekly gross pay for the audit "
                    f"period, Monday to Sunday."))
            else:
                p.records.append(rec["weekly_payroll_file"])
                per_week = [(s, t, g, sum(1 for d in rides if s <= d <= t)) for s, t, g in weeks]
                hist = Counter(n for *_, n in per_week)
                moved_weeks = [w_ for w_ in per_week if w_[3] >= min_ride]
                moved = sum((g for _, _, g, _ in moved_weeks), ZERO)
                weekly_total = sum((g for _, _, g in weeks), ZERO)
                if weekly_total != e["wages"]:
                    res.open_items.append(OpenItem(
                        e["name"], f"Use {reg_file} for the total and {rec['weekly_payroll_file']} for the week split.",
                        f"The weekly pay totals {fmt(weekly_total)} but {reg_file} shows {fmt(e['wages'])}.",
                        [reg_file, rec["weekly_payroll_file"]], "HP-10",
                        f"{e['name']} ({reg_file}, {rec['weekly_payroll_file']}): the weekly pay totals "
                        f"{fmt(weekly_total)} but the register shows {fmt(e['wages'])}; please send the reconciliation."))
                split_text = (f"{len(rides)} ride-along days in the audit period. Pay weeks by ride days: "
                              + ", ".join(f"{n} day(s) {hist[n]} week(s)" for n in sorted(hist)) + ".")
                applied("HP-2")
                if moved:
                    p.lines = [
                        Line(route_code, moved, f"{rec['route_log_file']}: {split_text} The {len(moved_weeks)} weeks "
                                                f"with {min_ride} or more ride days are driver payroll under "
                                                f"{route_code} (HP-2)."),
                        Line(final, e["wages"] - moved, f"{basis} The other {len(weeks) - len(moved_weeks)} pay weeks "
                                                        f"(no ride day or only one) stay under {final} (HP-2)."),
                    ]
                    res.adjustments.append(Adjustment(
                        e["name"], "Whole-week route split", moved, route_code,
                        f"{split_text} {len(moved_weeks)} pay weeks have {min_ride} or more ride days; their gross pay "
                        f"of {fmt(moved)} moves from {final} to {route_code}: "
                        + ", ".join(f"{s.isoformat()} ({n} days, {fmt(g)})" for s, _, g, n in moved_weeks) + ".",
                        [rec["route_log_file"], rec["weekly_payroll_file"]], "HP-2"))
                else:
                    p.lines[0].basis += (f" {rec['route_log_file']}: {split_text} No pay week has {min_ride} or more "
                                         f"ride days, so all pay stays under {final} (HP-2).")
                p.evidence = (f"{rec['route_log_file']} records {e['name']} as a ride-along on {len(rides)} day(s): "
                              + ", ".join(d.isoformat() for d in sorted(rides)) + ".")
                for s, t, g, n in per_week:
                    hol = [d for d in sorted(rides) if s <= d <= t and _holiday(d)]
                    if not hol:
                        continue
                    decisive = n >= min_ride > n - len(hol)
                    effect = (f"Decisive: the pay week of {s.isoformat()} has {n} ride days including it; without it the "
                              f"week has {n - len(hol)} and its {fmt(g)} would stay under {final}, not {route_code}."
                              if decisive else
                              f"Not decisive: the pay week of {s.isoformat()} has {n} ride day(s) "
                              + (f"and {n - len(hol)} without it, so its {fmt(g)} stays under {route_code}."
                                 if n - len(hol) >= min_ride else f"and its {fmt(g)} stays under {final} either way."))
                    res.questionable.append(Questionable(
                        e["name"], rec["route_log_file"],
                        f"{rec['route_log_file']} records {e['name']} as a ride-along on "
                        + ", ".join(f"{d.isoformat()} ({_holiday(d)})" for d in hol), effect, g if decisive else None))

        _travel(res, hp, e, p, reg_file, rec["register"])
        p.records = _uniq(p.records)
        res.people.append(p)

    _caterer_test(res, hp, rec, ws, code_ok)

    # Governing code (HP-4): the field code carrying the most payroll, before any clerical move (reading R4).
    field_pay = defaultdict(Decimal)
    for p in res.people:
        for l in p.lines:
            if l.code != clerical:
                field_pay[l.code] += l.amount
    res.governing_code = max(field_pay, key=field_pay.get) if field_pay else None
    gov_mix = ", ".join(f"{c} {fmt(v)}" for c, v in sorted(field_pay.items(), key=lambda kv: -kv[1])) or "none"

    for p, w, days, dates in pending:
        applied("HP-4")
        if res.governing_code:
            for l in p.lines:
                if l.code == clerical:
                    l.code = res.governing_code
            p.lines[0].basis = (f"{w['basis']} {rec['signins_file']} shows {len(days)} job-site days in the audit "
                                f"period ({dates}): five or more, so the whole payroll moves to the employer's governing "
                                f"code {res.governing_code}, the field code carrying the most payroll ({gov_mix}) (HP-4).")
        else:
            p.lines[0].basis += (f" {rec['signins_file']} shows {len(days)} job-site days ({dates}), five or more, but "
                                 f"the employer has no field code, so there is no governing code to move to.")
            res.open_items.append(OpenItem(
                p.name, f"Keep {p.name} under {clerical}.",
                f"{len(days)} job-site days meets the five-day test (HP-4), and the rule moves the whole payroll to the "
                f"field code carrying the most payroll. This employer has no payroll under any field code, so the rule "
                f"has nothing to move to. Nadia has no practice for this: the rule was set up for contractors' office "
                f"staff, and she asked for it to be marked as an open item for confirmation (interview 3). The days at "
                f"{', '.join(sorted({s for v in days.values() for s in v}))} stay in the count as written (HP-4).",
                [rec["signins_file"]] + w.get("records", []), "HP-4, HP-10",
                f"{p.name} ({rec['signins_file']}): {p.evidence} Please describe what {p.name} did at each visit, and "
                f"whether any of it was physical work outside the office."))

    for p in owners:
        if res.governing_code and p.lines[0].code != res.governing_code:
            res.open_items.append(OpenItem(
                p.name, f"Keep the owner's flat amount under {p.lines[0].code}.",
                f"House practice counts a working owner under the employer's trade code. The worksheet names "
                f"{p.lines[0].code}, but the field code carrying the most payroll is {res.governing_code}.",
                p.records, "HP-3, R3",
                f"{p.name} ({', '.join(p.records)}): please describe the field work {p.name} did during the audit period."))

    _subcontractors(res, hp, rec, ws, code_ok, in_period)

    if pending and res.governing_code and res.sub_lines:
        with_subs = defaultdict(Decimal, field_pay)
        for l in res.sub_lines:
            with_subs[l.code] += l.amount
        alt = max(with_subs, key=with_subs.get)
        if alt != res.governing_code:
            res.open_items.append(OpenItem(
                "Governing code", f"Use {res.governing_code}, from employees' payroll only.",
                f"Counting subcontractor additions would make {alt} the governing code. Nadia has no rule on whether "
                f"subcontractor payroll counts in that comparison (interview 3; reading R4).",
                [rec["sub_payments_file"]], "HP-4, R4"))

    if split_people:
        rows = "; ".join(f"{p.name}: " + ", ".join(f"{c} {n} days" for c, n in sorted(bc.items(), key=lambda kv: -kv[1]))
                         + f", reported under {f}" for p, bc, f in split_people)
        res.open_items.append(OpenItem(
            "Crew members with more than one type of work",
            "Report each person's whole pay under the code with the most recorded days.",
            f"Confirmed: one person's pay is not split except for route ride-alongs (HP-2), tests use days, not "
            f"hours (HP-13), and a roofing-and-siding contractor uses the roof-day test (HP-16). Not stated: the test "
            f"for any other mix of work. The most-days choice is this Skill's reading (R2). Days by code: {rows}.",
            [rec["timesheets_file"]], "HP-10, R2"))

    if rec.get("period_issues"):
        res.open_items.append(OpenItem(
            "Audit period", f"Use {start.isoformat()} to {end.isoformat()} from {rec['period_file']}.",
            "The audit period in the business description defines the timeframe, and a missing or differing statement "
            "goes on the question list (HP-17). Here " + "; ".join(rec["period_issues"]) + ".",
            [rec["period_file"]], "HP-17",
            f"Audit period: please confirm the audit period. The first pass uses {start.isoformat()} to {end.isoformat()} "
            f"({rec['period_file']}), but " + "; ".join(rec["period_issues"]) + "."))

    if any(q.decisive for q in res.questionable):
        applied("HP-15")

    for item in ws.get("open_items", []):
        target = next((o for o in res.open_items if o.about == item.get("merge_with")), None)
        if target:  # the analyst's context for an item the rules already raised
            target.proposal = item.get("proposal", target.proposal)
            target.why += " " + item["why"]
            target.records = _uniq(target.records + item.get("records", []))
            target.question = item.get("employer_question", target.question)
        else:
            res.open_items.append(OpenItem(item["about"], item["proposal"], item["why"], item.get("records", []),
                                           item.get("rule", "HP-10"), item.get("employer_question", "")))

    totals = defaultdict(Decimal)
    for line in [l for p in res.people for l in p.lines] + res.sub_lines:
        totals[line.code] += line.amount
    res.totals = {c: v.quantize(CENT) for c, v in sorted(totals.items()) if v}
    _reconcile(res, rec)

    mapping, res.inference = infer_employer_codes(rec["register"], rec["employer_split"])
    for p in res.people:
        p.employer_code = (mapping or {}).get(p.id)
        if p.employer_code and p.primary_code != p.employer_code and not any(a.about == p.name for a in res.adjustments):
            res.adjustments.append(Adjustment(
                p.name, "Reclassified", p.wages, p.primary_code,
                f"The records put {p.name}'s {fmt(p.wages)} under {p.primary_code}: {p.lines[0].basis} (Employer's "
                f"split pairs {p.name} with {p.employer_code}.)", p.records, "HP-1, HP-7"))
        for a in res.adjustments:
            if a.about == p.name and a.kind != "Reclassified" and p.employer_code and p.employer_code != a.code:
                a.detail += f" (Employer's split pairs {p.name} with {p.employer_code}.)"

    _questions(res, rec, ws)
    return res


def _travel(res, hp, e, p, reg_file, register):
    if not e["travel_allowance"]:
        return
    cap = money(hp["out_of_town_daily_allowance_exclusion"])
    code = p.lines[-1].code
    tdays = e["travel_days"] or 0
    excluded = min(e["travel_allowance"], cap * tdays)
    excess = e["travel_allowance"] - excluded
    src = f"{reg_file} (travel_days, travel_allowance_paid)"
    p.records.append(src)
    if "HP-6" not in res.applied:
        res.applied.append("HP-6")
    if excess:
        p.lines.append(Line(code, excess, f"Daily allowance above {fmt(cap)} per day: {fmt(e['travel_allowance'])} paid "
                                          f"for {tdays} travel days, {fmt(excluded)} left out (HP-6)."))
        res.adjustments.append(Adjustment(
            e["name"], "Travel allowance above the daily exclusion", excess, code,
            f"{fmt(e['travel_allowance'])} paid for {tdays} recorded travel days. Up to {fmt(cap)} per day "
            f"({fmt(excluded)}) is left out; the remaining {fmt(excess)} is payroll under {code}.", [src],
            "HP-6" if tdays else "HP-6, R6"))
    if tdays == 0:
        paid = e["travel_allowance"]
        rates = defaultdict(list)
        for r in register:
            if r["travel_days"]:
                rates[(r["travel_allowance"] / r["travel_days"]).quantize(CENT)].append(r["name"])
        fits = [x for x in rates if x and (paid / x) == (paid / x).to_integral_value()]
        if len(fits) == 1:
            rate = fits[0]
            n = int(paid / rate)
            out = min(paid, cap * n)
            paid_at = "; ".join(f"{', '.join(names)} {fmt(x)} per day" for x, names in sorted(rates.items(), key=lambda kv: -kv[0]))
            proposal = (f" Proposed handling for Nadia to confirm: the register's daily rates are {paid_at}. "
                        f"{fmt(paid)} is exactly {n} days at {fmt(rate)} and not a whole number of days at any other rate, "
                        f"so it looks like {n} out-of-town days that were not entered. If the employer confirms {n} travel days, "
                        f"{fmt(out)} ({n} x {fmt(cap)}) is left out and {fmt(paid - out)} is payroll under {code}. If it "
                        f"was a documented expense reimbursement, none of it is payroll (CG-03).")
        else:
            proposal = (f" Proposed handling for Nadia to confirm: apply HP-6 to the travel days the employer confirms; "
                        f"if it was a documented expense reimbursement, none of it is payroll (CG-03).")
        res.open_items.append(OpenItem(
            e["name"], f"Allocated as practice stands: all {fmt(paid)} of the allowance is payroll under {code}."
                       + proposal,
            f"{reg_file} records an allowance but no travel days. Nadia has no practice for this and asked for it to be "
            f"allocated under her practice and the guide as they stand, with a written proposal for her to confirm "
            f"(interviews 2 and 3). HP-6 leaves out up to {fmt(cap)} per travel day, so with no recorded day nothing "
            f"qualifies, and the amount is payroll (reading R6).", [reg_file], "HP-6, R6, CG-03"))


def _caterer_test(res, hp, rec, ws, code_ok):
    """HP-14: the caterer code applies only if off-site catering is 40% or more of the employer's gross receipts."""
    caterer, restaurant = hp["caterer_code"], hp["restaurant_code"]
    crew = [p for p in res.people if any(l.code == caterer for l in p.lines)]
    if not crew:
        return
    cfg = ws.get("receipts") or {}
    name = cfg.get("file") or rec.get("receipts_file")
    names = ", ".join(p.name for p in crew)
    if not name or not cfg.get("offsite_columns") or not cfg.get("other_columns"):
        res.open_items.append(OpenItem(
            f"Caterer receipts test ({names})", f"Keep {names} under {caterer} until the receipts test can be run.",
            f"{caterer} applies only if off-site catering is {Decimal(hp['caterer_min_offsite_receipts_share']):.0%} or "
            f"more of gross receipts (HP-14), and the file has no receipts record mapped in the worksheet.", [],
            "HP-14, HP-10", f"{names}: please send monthly gross receipts for the audit period, split between off-site "
                            f"catering and everything else."))
        return
    rows = rec["file"].rows(name, ["month"] + cfg["offsite_columns"] + cfg["other_columns"])
    start, end = rec["period"]
    used, partial = [], []
    for r in rows:
        first = datetime.date.fromisoformat(r["month"] + "-01")
        last = (first.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        if first <= end and last >= start:
            used.append(r)
            if first < start or last > end:
                partial.append(r["month"])
    offsite = sum((money(r[c]) for r in used for c in cfg["offsite_columns"]), ZERO)
    total = offsite + sum((money(r[c]) for r in used for c in cfg["other_columns"]), ZERO)
    share = offsite / total if total else Decimal(0)
    need = Decimal(hp["caterer_min_offsite_receipts_share"])
    months = f"{used[0]['month']} to {used[-1]['month']}" if used else "none"
    text = (f"{name}, {months}: off-site catering {fmt(offsite)} of {fmt(total)} gross receipts = {share:.2%} "
            f"(test: {need:.0%} or more for {caterer}, HP-14).")
    if partial:
        whole = [r for r in used if r["month"] not in partial]
        off_w = sum((money(r[c]) for r in whole for c in cfg["offsite_columns"]), ZERO)
        tot_w = off_w + sum((money(r[c]) for r in whole for c in cfg["other_columns"]), ZERO)
        share_w = off_w / tot_w if tot_w else Decimal(0)
        what = (f"Leaving {'it' if len(partial) == 1 else 'them'} out gives {share_w:.2%}, on the same side of the test, "
                f"so it does not change the allocation." if (share_w >= need) == (share >= need) else
                f"Leaving {'it' if len(partial) == 1 else 'them'} out gives {share_w:.2%}, which changes the result.")
        res.notes.append(f"{name}: month(s) {', '.join(partial)} only partly overlap the audit period "
                         f"{start.isoformat()} to {end.isoformat()} and were counted whole (reading R14; Nadia has no "
                         f"rule for this, interview 3). {what}")
        if (share_w >= need) != (share >= need):
            res.open_items.append(OpenItem(
                f"Receipts months {', '.join(partial)}", f"Count months {', '.join(partial)} whole ({share:.2%}).",
                f"Counting them whole gives {share:.2%}; leaving them out gives {share_w:.2%}, on the other side of the "
                f"{need:.0%} test (HP-14). Nadia has no rule for months that cross the audit period boundary (reading R14).",
                [name], "HP-14, R14",
                f"{name}: please send receipts for {', '.join(partial)} split by date, so the part inside the audit "
                f"period {start.isoformat()} to {end.isoformat()} can be used."))
    res.applied.append("HP-14")
    res.notes.append(f"Caterer receipts test: {text}")
    for p in crew:
        p.records = _uniq(p.records + [name])
        if share < need:
            moved = sum((l.amount for l in p.lines if l.code == caterer), ZERO)
            for l in p.lines:
                if l.code == caterer:
                    l.code = restaurant
            p.lines[0].basis += f" {text} Below the test, so the catering crew stays under {restaurant}."
            res.adjustments.append(Adjustment(
                p.name, "Caterer receipts test", moved, restaurant,
                f"{p.name} works on the catering crew. {text} Below {need:.0%}, so {fmt(moved)} goes under {restaurant}, "
                f"not {caterer}.", [name] + [r for r in p.records if r != name], "HP-14"))
        else:
            p.lines[0].basis += f" {text} At or above the test, so {caterer} applies."
    code_ok(restaurant, "house_practice.restaurant_code")


def _subcontractors(res, hp, rec, ws, code_ok, in_period):
    if not rec["sub_payments"]:
        return
    share = Decimal(hp["uninsured_subcontractor_payroll_share"])
    start, end = rec["period"]
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
    res.applied.append("HP-5")
    period = f"{start.isoformat()} to {end.isoformat()}"
    for sub, pays in by_sub.items():
        cert_name = sub if sub in certs else matches.get(sub)
        held = certs.get(cert_name, [])
        whole = [c for c in held if c[1] <= start and c[2] >= end]
        if cert_name and cert_name != sub:
            effect = ("This decides whether the payments are insured." if whole else
                      "It does not change the allocation: that certificate does not cover the whole audit period, and a "
                      "certificate that lapses partway through counts as no certificate (HP-5), so the payments are "
                      "added whichever business it belongs to. The name matters only if the employer sends a further "
                      "certificate in that name.")
            res.open_items.append(OpenItem(
                sub, f"Treat the certificate issued to '{cert_name}' as {sub}'s, for the record only.",
                f"{rec['sub_payments_file']} pays '{sub}', but the certificate in {rec['certificates_file']} is issued to "
                f"'{cert_name}'. Nadia has no practice for a name that differs (interview 2). {effect}", files, "HP-10",
                f"{sub} ({', '.join(files)}): please confirm whether '{sub}' and '{cert_name}' are the same business, "
                f"with its legal name and federal tax ID."))
        listing = ", ".join(f"{p.get('invoice', '?')} ({p['date']}, {fmt(money(p['amount_paid']))})" for p in pays)
        lead = f"{sub} ({', '.join(files)})"
        if whole:
            res.notes.append(f"{sub}: certificate {whole[0][0]} covers the whole audit period ({period}); "
                             f"{len(pays)} payment(s) not added to payroll (HP-5).")
            res.questions.append((sub, f"{lead}: please confirm that certificate {whole[0][0]} covered {sub}'s own "
                                       f"workers for the whole audit period {period}, including invoices {listing}."))
            continue
        why = ("no certificate of insurance for this subcontractor is in the file" if not held else
               "the certificate in the file (" + "; ".join(f"{n}, {f.isoformat()} to {t.isoformat()}" for n, f, t in held)
               + f") does not cover the whole audit period {period}, and a certificate that lapses partway through "
                 f"counts as no certificate, also for payments made while it was in force")
        for pay in pays:
            work = pay["work"]
            if work not in work_codes:
                raise WorksheetError(f"subcontracted work {work!r} has no entry in worksheet subcontract_work_codes")
            code = code_ok(work_codes[work], f"subcontract_work_codes.{work}")
            paid = money(pay["amount_paid"])
            added = (paid * share).quantize(CENT, rounding=ROUND_HALF_UP)
            res.sub_lines.append(Line(code, added, f"{share:.0%} of {fmt(paid)} paid to uninsured subcontractor {sub} "
                                                   f"(invoice {pay.get('invoice', '?')}, {pay['date']}, {work}) (HP-5, CG-06)."))
            res.adjustments.append(Adjustment(
                f"{sub}, invoice {pay.get('invoice', '?')}", "Uninsured subcontractor payment added", added, code,
                f"{fmt(paid)} paid on {pay['date']} for {work}. Because {why}, {share:.0%} ({fmt(added)}) is added to "
                f"payroll under {code}, the code for the work.", files, "HP-5, CG-06"))
        res.notes.append(f"{sub}: {why}; all {len(pays)} payment(s) added at {share:.0%} (HP-5).")
        res.questions.append((sub, f"{lead}: {why}. Please send a workers' compensation certificate covering {sub}'s "
                                   f"own workers for the whole audit period {period}. Without one, {share:.0%} of "
                                   f"invoices {listing} stays in payroll."))


def _reconcile(res, rec):
    """Register wages plus every adjustment that adds or removes payroll must equal the allocated total."""
    register = sum((e["wages"] for e in rec["register"]), ZERO)
    steps = [("Payroll register wages", register)]
    for a in res.adjustments:
        if a.kind == "Owner counted at flat amount":
            p = next(p for p in res.people if p.name == a.about)
            steps.append((f"{a.about}: flat {fmt(a.amount)} replaces register wages {fmt(p.wages)}", a.amount - p.wages))
        elif a.kind in ("Travel allowance above the daily exclusion", "Uninsured subcontractor payment added"):
            steps.append((f"{a.about}: {a.kind.lower()}", a.amount))
    total = sum((v for _, v in steps), ZERO)
    allocated = sum(res.totals.values(), ZERO)
    if total != allocated:
        raise AssertionError(f"reconciliation failed: register plus adjustments {total} != allocated {allocated}")
    res.reconciliation = steps + [("First-pass total (equals the sum of the codes CSV)", allocated)]


def _questions(res, rec, ws):
    """Every adjustment, every record a decision rests on, every questionable record and every open item gets at least
    one employer question (HP-9, HP-10, HP-15)."""
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
            q(a.about, f"{a.about} ({', '.join(p.records)}): please confirm that {a.about} has not filed an election "
                       f"of exclusion, did field work during the audit period, and was paid the {fmt(p.wages)} shown in "
                       f"{reg}.")
        elif a.kind == "Whole-week route split":
            q(a.about, f"{a.about} ({rec['route_log_file']}, {rec['weekly_payroll_file']}): {p.evidence} Please confirm "
                       f"these ride-along days and the weekly gross pay in the weeks with two or more of them "
                       f"(total {fmt(a.amount)}).")
        elif a.kind == "Travel allowance above the daily exclusion":
            row = next(e for e in rec["register"] if e["name"] == a.about)
            if row["travel_days"]:
                q(a.about, f"{a.about} ({reg}, travel columns): please confirm the {row['travel_days']} out-of-town "
                           f"travel days and the {fmt(row['travel_allowance'])} daily allowance paid, with the trip dates "
                           f"and job.")
            else:
                q(a.about, f"{a.about} ({reg}, travel columns): the register shows a {fmt(row['travel_allowance'])} "
                           f"travel allowance but no travel days. Please say what the payment was for and, if it was "
                           f"for out-of-town work, send the dates and job.")
        elif a.kind == "Caterer receipts test":
            q(a.about, f"{a.about} ({', '.join(a.records)}): please confirm the monthly split of gross receipts between "
                       f"off-site catering and the restaurant for the audit period, and that {a.about} worked on the "
                       f"catering crew.")
        elif a.kind == "Reclassified":
            recs = ", ".join(r for r in p.records if r != reg)
            q(a.about, f"{a.about} ({recs or reg}): {p.evidence or 'The records in the file describe other work.'} "
                       f"Please confirm {a.about}'s actual duties during the audit period and that these records are "
                       f"complete.")

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

    for x in res.questionable:
        stake = f" The code of {fmt(x.decisive)} of payroll depends on this record." if x.decisive else ""
        q(x.about, f"{x.about} ({x.record}): {x.detail}. The first pass uses the record as written.{stake} Please "
                   f"confirm it or send the corrected record.")

    if res.people:
        listing = "; ".join(f"{p.name}, {p.position}, {fmt(p.wages)} (first pass: "
                            + ", ".join(f"{fmt(l.amount)} {l.code}" for l in p.lines) + ")" for p in res.people)
        q("Payroll register", f"{reg}: please confirm that these wages are complete for the audit period "
                              f"{rec['period'][0].isoformat()} to {rec['period'][1].isoformat()}, and that each "
                              f"person's work matches the code given: {listing}.")

    res.questions += sub_qs
    for c in ws.get("confirmations", []):
        q(c["about"], c["question"])
    for o in res.open_items:
        q(o.about, o.question or f"{o.about} ({', '.join(o.records) or 'records in the file'}): the first pass "
                                 f"proposes: {o.proposal} Please confirm, or send the record that shows otherwise.")
