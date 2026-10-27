"""Write the deliverables: one codes CSV per employer, the audit report and the employer question list."""

import csv
from decimal import Decimal

from .rules import fmt

ZERO = Decimal("0.00")


def write_codes_csv(path, result, guide):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["class_code", "payroll_allocated", "rationale_ref"])
        for code, amount in result.totals.items():
            if amount:
                w.writerow([code, f"{amount:.2f}", guide.ref_for(code)])


def change(result):
    """Sum of absolute per-code differences from the employer's own split, in payroll dollars (no rates involved)."""
    return sum((abs(d) for d in result.differences().values()), ZERO)


def call_order(results):
    return sorted(results, key=lambda r: (-change(r), -len(r.open_items), r.rec["employer_name"]))


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def _signed(d):
    return f"+{fmt(d)}" if d > 0 else fmt(d)


def _drivers(result, n=3):
    big = sorted(result.adjustments, key=lambda a: -abs(a.amount))[:n]
    return "; ".join(f"{a.about}: {a.kind.lower()} ({fmt(a.amount)} under {a.code})" for a in big)


def report(results, guide, run):
    out = ["# Premium audit first pass: class codes and payroll allocation", ""]
    out += [
        "Prepared by the class-code-assistant Skill as a **first pass for review by Nadia Brennan, Senior Premium "
        "Auditor**. It is not audit work until she has reviewed it (house practice HP-11). It classifies and "
        "allocates payroll only; it does not set rates or quote premium.",
        "",
        f"- Classification rules: Linden Shore Mutual classification guide excerpt, edition of {guide.edition}, "
        f"sha256 `{run['guide_sha256'][:12]}`, read from {run['guide_source']}.",
        f"- Employer files read from {run['employer_source']} at {run['fetched_at']}.",
        "- House practice: the audit team's unwritten rules from interview 1, labelled HP-1 to HP-12 in "
        "`skills/class-code-assistant/references/house-practice.md`. Readings A1 to A6 in the same file are this "
        "Skill's interpretations; every place one changes an allocation is listed as an open item.",
        "- **Facts** below are cited to the employer record they come from. **Open items** are proposals for gray "
        "areas: each says how the first pass treated the case and why, and needs Nadia's confirmation.",
        "",
        "## Which two employers to call first",
        "",
        "The order ranks employers by how much payroll the records move away from the employer's own split. That is "
        "the sum of the absolute differences per code, in dollars of payroll, not premium. Ties go to the employer "
        "with more open items. The two at the top have the most payroll resting on records the employer still has to "
        "confirm.",
        "",
        "| Order | Employer | Payroll moved vs employer split | Employer reported | First pass | Open items | Employer questions |",
        "|---|---|---|---|---|---|---|",
    ]
    ordered = call_order(results)
    for i, r in enumerate(ordered, 1):
        out.append(f"| {i} | {r.rec['employer_name']} | {fmt(change(r))} | {fmt(sum(r.employer_split.values(), ZERO))} "
                   f"| {fmt(sum(r.totals.values(), ZERO))} | {len(r.open_items)} | {len(r.questions)} |")
    out.append("")
    for i, r in enumerate(ordered[:2], 1):
        out.append(f"{i}. **{r.rec['employer_name']}**: {fmt(change(r))} of payroll moves. The largest drivers are "
                   f"{_drivers(r)}. {len(r.open_items)} open item(s) depend on the employer's confirmation.")
    out += ["", "## Summary", "", "| Employer | Employer's split | Decision rests on |", "|---|---|---|"]
    for r in results:
        out.append(f"| {r.rec['employer_name']} | {'Accepted' if r.accepts_employer_split else 'Not accepted'} | "
                   f"{_cell(_decision_records(r))} |")
    for r in results:
        out += [""] + _employer_section(r, guide)
    return "\n".join(out).rstrip() + "\n"


def _decision_records(r):
    recs = []
    for p in r.people:
        recs += p.records
    for a in r.adjustments:
        recs += a.records
    return ", ".join(dict.fromkeys(x.split(" (")[0] for x in recs))


def _employer_section(r, guide):
    rec, ws = r.rec, r.ws
    start, end = rec["period"]
    out = [f"## {rec['employer_name']}", ""]
    out += [
        f"Application {rec['application_id']}, signed by {rec['signed_by']}. Audit period {start.isoformat()} to "
        f"{end.isoformat()} ({rec['period_file']}). Files read: {', '.join(sorted(rec['file'].read))}.",
        "",
    ]
    if rec["employer_note"]:
        out += [f"Employer's note on the application: \"{rec['employer_note']}\"", ""]
    if r.accepts_employer_split:
        out += [f"**Employer's split: accepted.** The records give the same codes and payroll, to the cent, as the "
                f"employer reported. The decision rests on {_decision_records(r)}. Open items below still need "
                f"confirmation.", ""]
    else:
        out += [f"**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The "
                f"decision rests on {_decision_records(r)}. Each difference is on this employer's question list.", ""]

    out += ["### Allocation", "", "| Class code | Guide paragraph | Employer reported | First pass | Difference |",
            "|---|---|---|---|---|"]
    for code, d in r.differences().items():
        out.append(f"| {code} | {guide.ref_for(code)} | {fmt(r.employer_split.get(code, ZERO))} | "
                   f"{fmt(r.totals.get(code, ZERO))} | {_signed(d) if d else '0.00'} |")
    tot_e, tot_f = sum(r.employer_split.values(), ZERO), sum(r.totals.values(), ZERO)
    out += [f"| **Total** | | **{fmt(tot_e)}** | **{fmt(tot_f)}** | **{_signed(tot_f - tot_e) if tot_f != tot_e else '0.00'}** |", ""]

    out += ["### Where and why the first pass differs from the employer's split", ""]
    if not r.adjustments:
        out += ["No difference. No adjustment was needed.", ""]
    else:
        for code, d in r.differences().items():
            if d:
                why = [a for a in r.adjustments if a.code == code] or []
                out.append(f"- **{code}** {_signed(d)}: " + ("; ".join(f"{a.about} ({a.kind.lower()}, {fmt(a.amount)})" for a in why)
                                                          or "payroll moved to other codes; see the adjustments below") + ".")
        out.append(f"- How the employer's split was compared: {r.inference}.")
        out.append("")
        out += ["### Adjustments", "", "| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |",
                "|---|---|---|---|---|---|---|---|"]
        for i, a in enumerate(r.adjustments, 1):
            out.append(f"| {i} | {_cell(a.about)} | {a.kind} | {fmt(a.amount)} | {a.code} | {_cell(a.detail)} | "
                       f"{_cell(', '.join(a.records))} | {a.rule} |")
        out.append("")

    out += ["### Employee by employee", "",
            "| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |",
            "|---|---|---|---|---|---|---|---|"]
    for p in r.people:
        alloc = "<br>".join(f"{fmt(l.amount)} {l.code}" for l in p.lines)
        basis = "<br>".join(_cell(l.basis) for l in p.lines)
        out.append(f"| {p.id} | {p.name} | {p.position} | {fmt(p.wages)} | {p.employer_code or 'n/a'} | {alloc} | "
                   f"{basis} | {_cell(', '.join(p.records))} |")
    if r.sub_lines:
        out += ["", "Subcontractor payroll added:", ""] + [f"- {fmt(l.amount)} {l.code}: {l.basis}" for l in r.sub_lines]
    out.append("")

    if ws.get("facts"):
        out += ["### Documented facts relied on", ""]
        out += [f"- {f['fact']} ({f['record']})" for f in ws["facts"]] + [""]

    out += ["### Open items for Nadia Brennan to confirm", ""]
    if r.open_items:
        out += ["| # | About | Proposed handling | Why | Records |", "|---|---|---|---|---|"]
        for i, o in enumerate(r.open_items, 1):
            out.append(f"| {i} | {_cell(o.about)} | {_cell(o.proposal)} | {_cell(o.why)} | {_cell(', '.join(o.records))} |")
    else:
        out.append("None.")
    out.append("")

    notes = list(r.notes)
    for name in rec["file"].unread():
        reason = ws.get("unused_records", {}).get(name, "not needed by any rule applied")
        notes.append(f"{name} was not used for the allocation: {reason}")
    if notes:
        out += ["### Notes on the records", ""] + [f"- {n}" for n in notes] + [""]
    return out


def questions(results):
    out = ["# Audit questions for employers", "",
           "One section per employer. Each question names the employee, subcontractor or record it is about, and the "
           "document that would confirm it. Every adjustment in the audit report, and every record a decision rests "
           "on, has at least one question (house practice HP-9). These are drafts for Nadia Brennan to review before "
           "they go to the employer.", ""]
    for r in results:
        out += [f"## {r.rec['employer_name']}", ""]
        for i, (about, text) in enumerate(r.questions, 1):
            out.append(f"{i}. **{about}.** {text}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"
