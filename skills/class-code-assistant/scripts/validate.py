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

    for f in failures:
        print(f"FAIL {f}")
    print(f"{checks - len(failures)}/{checks} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
