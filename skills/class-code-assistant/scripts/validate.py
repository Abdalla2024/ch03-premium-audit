"""Check the deliverables against the assignment's format rules. Exit status 1 on any failure.

Checks: the six codes CSVs (exact header, cents, no zero rows, rationale_ref as printed in the guide); CSV totals match
the report's allocation tables; one report and one question section per employer; every adjustment in the report is
named in that employer's questions; no employer names or IDs are hard-coded in the Skill's code; interview exports
are unchanged since they were committed.
"""

import argparse
import csv
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cca.guide import Guide  # noqa: E402

HEADER = ["class_code", "payroll_allocated", "rationale_ref"]
CENTS = re.compile(r"^\d+\.\d{2}$")


def sections(text):
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="deliverables", type=Path)
    ap.add_argument("--guide", default=".cache/sources/classification-guide.md", type=Path)
    ap.add_argument("--employers", default=".cache/sources/employers", type=Path)
    args = ap.parse_args(argv)
    failures, checks = [], 0

    def check(ok, message):
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(message)

    guide = Guide(args.guide.read_text())
    house_practice = (Path(__file__).resolve().parent.parent / "references" / "house-practice.md").read_text()
    slugs = sorted(p.name for p in args.employers.iterdir() if p.is_dir())
    report = (args.out / "audit-report.md").read_text()
    questions = (args.out / "audit-questions.md").read_text()
    rep_sections, q_sections = sections(report), sections(questions)
    names = {}

    for slug in slugs:
        app = (args.employers / slug / "application.md").read_text()
        name = re.search(r"^#\s*([^:\n]+)", app, re.M).group(1).strip()
        names[slug] = name
        path = args.out / "codes" / f"{slug}.csv"
        check(path.exists(), f"{path} is missing")
        if not path.exists():
            continue
        with open(path, newline="") as f:
            rows = list(csv.reader(f))
        check(rows and rows[0] == HEADER, f"{path}: header must be exactly {','.join(HEADER)}")
        body = rows[1:]
        check(len({r[0] for r in body}) == len(body), f"{path}: a class code appears more than once")
        totals = {}
        for r in body:
            check(len(r) == 3, f"{path}: row {r} does not have 3 columns")
            code, amount, ref = r
            check(CENTS.match(amount) is not None, f"{path}: {amount!r} is not dollars to the cent without separators")
            check(Decimal(amount) > 0, f"{path}: {code} has zero payroll")
            check(guide.code_ref.get(code) == ref, f"{path}: {code} rationale_ref {ref!r} is not the guide paragraph "
                                                   f"{guide.code_ref.get(code)!r}")
            totals[code] = Decimal(amount)

        sec = rep_sections.get(name)
        check(sec is not None, f"audit-report.md has no section '## {name}'")
        check(name in q_sections, f"audit-questions.md has no section '## {name}'")
        if sec is None:
            continue
        table = {m[0]: Decimal(m[2].replace(",", "")) for m in
                 re.findall(r"^\| ([A-Z]-\d{3}) \| (CG-\d+) \| [\d,.]+ \| ([\d,.]+) \|", sec, re.M)}
        table = {c: v for c, v in table.items() if v}
        check(table == totals, f"{name}: CSV totals {totals} differ from the report's allocation table {table}")
        adj = re.search(r"### Adjustments\n\n(.*?)\n\n", sec, re.S)
        qtext = q_sections.get(name, "")
        for row in (adj.group(1).splitlines()[2:] if adj else []):
            about = row.split(" | ")[1].split(", invoice")[0]
            check(about in qtext, f"{name}: adjustment about {about!r} has no question naming it")
        check("Employer's split: accepted" in sec or "Employer's split: not accepted" in sec,
              f"{name}: the report does not state whether the employer's split is accepted")

        recon = re.search(r"\| First-pass total \(equals the sum of the codes CSV\) \| ([\d,.]+) \|", sec)
        check(recon is not None and Decimal(recon.group(1).replace(",", "")) == sum(totals.values(), Decimal(0)),
              f"{name}: reconciliation total missing or differs from the CSV total {sum(totals.values(), Decimal(0))}")

        folder = {p.name for p in (args.employers / slug).iterdir()}
        for cited in sorted(set(re.findall(r"\b([a-z][a-z0-9-]*\.(?:csv|md))\b", sec))):
            check(cited in folder, f"{name}: cites record {cited}, which is not in the employer file")
        for ref in sorted(set(re.findall(r"\bCG-\d+\b", sec))):
            check(ref in guide.paragraphs, f"{name}: cites {ref}, which is not a paragraph in the guide")
        for ref in sorted(set(re.findall(r"\b(HP-\d+|R\d+)\b", sec))):
            check(re.search(rf"\b{ref}\b", house_practice) is not None,
                  f"{name}: cites {ref}, which is not defined in house-practice.md")

        items = re.search(r"### Open items: unresolved judgements\n\n.*?\n\n(.*?)\n\n", sec, re.S)
        check(items is not None, f"{name}: no open items section")
        for row in (items.group(1).splitlines()[2:] if items and items.group(1).startswith("|") else []):
            about = row.split(" | ")[1]
            check(f"**{about}.**" in qtext or about in qtext, f"{name}: open item {about!r} is not on the question list")

    check(re.search(r"\brate[sd]? (of|at) \d|premium (of|is) \$?\d", report, re.I) is None,
          "audit-report.md appears to state a rate or premium figure")

    skill_code = "\n".join(p.read_text() for p in Path(__file__).resolve().parent.parent.rglob("*") if p.suffix in {".py", ".json", ".md"})
    for slug, name in names.items():
        check(slug not in skill_code and name not in skill_code, f"the Skill's code or references mention {name}")
    for slug in slugs:
        with open(args.employers / slug / "payroll-register.csv", newline="") as f:
            for r in csv.DictReader(f):
                check(r["employee_id"] not in skill_code and r["name"] not in skill_code,
                      f"the Skill's code or references mention {r['employee_id']} {r['name']}")

    changed = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "interviews"], capture_output=True, text=True)
    check(changed.returncode == 0 and not changed.stdout.strip(), f"interview exports changed since commit: {changed.stdout}")
    tracked = set(subprocess.run(["git", "ls-files", "interviews"], capture_output=True, text=True).stdout.split())
    on_disk = {f"interviews/{p.name}" for p in Path("interviews").glob("*.md")}
    check(on_disk and on_disk <= tracked, f"interview exports not committed: {sorted(on_disk - tracked)}")
    for f in sorted(tracked):
        history = subprocess.run(["git", "log", "--format=%h", "--", f], capture_output=True, text=True).stdout.split()
        check(len(history) == 1, f"{f} was changed after it was first committed ({len(history)} commits touch it)")

    for f in failures:
        print(f"FAIL {f}")
    print(f"{checks - len(failures)}/{checks} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
