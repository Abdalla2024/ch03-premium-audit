"""Run the class-code-assistant first pass on one employer, several, or all of them.

Examples (from the repository root):

    python3 skills/class-code-assistant/scripts/run.py --all
    python3 skills/class-code-assistant/scripts/run.py --employer patuxent-electric
    python3 skills/class-code-assistant/scripts/run.py --local path/to/sources --employer new-employer
    python3 skills/class-code-assistant/scripts/run.py --init-worksheet new-employer
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cca import records, render  # noqa: E402
from cca.guide import Guide  # noqa: E402
from cca.rules import WorksheetError, allocate  # noqa: E402
from fetch_sources import fetch  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
REFS = SKILL_DIR / "references"


def load_sources(args):
    sources = json.loads((REFS / "sources.json").read_text())
    root = Path(args.local) if args.local else Path(args.cache)
    if not args.local:
        fetch(root, sources, None if args.all else args.employer)
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"fetched_at": "local copy", "files": {}}
    guide_path = root / "classification-guide.md"
    if not guide_path.exists():
        raise SystemExit(f"error: no classification guide at {guide_path}; the authoritative rules are required")
    guide_bytes = guide_path.read_bytes()
    run = {
        "fetched_at": manifest["fetched_at"],
        "guide_sha256": hashlib.sha256(guide_bytes).hexdigest(),
        "guide_source": sources["classification_guide"] if not args.local else str(guide_path),
        "employer_source": sources["employer_files"] if not args.local else str(root / "employers"),
    }
    return root, Guide(guide_bytes.decode("utf-8")), run


def init_worksheet(rec, path):
    """Scaffold a worksheet listing every judgment the analyst must make for this employer, with nothing filled in."""
    ws = {
        "employer": rec["employer_name"],
        "employees": {e["id"]: {"name": e["name"], "position": e["position"], "duty_code": None,
                                "basis": "TODO: the employee's actual duties and the record that shows them",
                                "records": []} for e in rec["register"]},
        "owners": {},
        "work_type_codes": {t: None for t in sorted({r["work_type"] for r in rec["timesheets"]})},
        "site_codes": {s: None for s in sorted({r["site"] for r in rec["signins"] if r["employee_id"]})},
        "route_code": None if rec["route_log"] else "n/a",
        "subcontract_work_codes": {w: None for w in sorted({r["work"] for r in rec["sub_payments"]})},
        "subcontractor_certificate_matches": {},
        "facts": [],
        "confirmations": [],
        "open_items": [],
        "unused_records": {},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"error: {path} already exists; not overwriting it")
    path.write_text(json.dumps(ws, indent=2) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Class code and payroll allocation first pass (Linden Shore Mutual).")
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--all", action="store_true", help="every employer folder at the source location")
    who.add_argument("--employer", action="append", help="employer folder slug (repeatable)")
    who.add_argument("--init-worksheet", metavar="SLUG", help="scaffold deliverables/worksheets/SLUG.json and stop")
    ap.add_argument("--local", help="read a local copy (classification-guide.md + employers/<slug>/) instead of fetching")
    ap.add_argument("--cache", default=".cache/sources", help="where fetched sources are written (default .cache/sources)")
    ap.add_argument("--worksheets", default="deliverables/worksheets", type=Path)
    ap.add_argument("--out", default="deliverables", type=Path)
    args = ap.parse_args(argv)
    if args.init_worksheet:
        args.employer = [args.init_worksheet]

    root, guide, run = load_sources(args)
    slugs = sorted(p.name for p in (root / "employers").iterdir() if p.is_dir()) if args.all else args.employer
    hp = json.loads((REFS / "house_practice.json").read_text())

    if args.init_worksheet:
        path = args.worksheets / f"{args.init_worksheet}.json"
        init_worksheet(records.load(root / "employers" / args.init_worksheet), path)
        print(f"wrote {path}: fill in every null and TODO from the employer's records, then run --employer {args.init_worksheet}")
        return 0

    results = []
    for slug in slugs:
        ws_path = args.worksheets / f"{slug}.json"
        if not ws_path.exists():
            raise SystemExit(f"error: no worksheet for {slug} at {ws_path}. Run --init-worksheet {slug}, then fill it "
                             f"in from the records (see SKILL.md, step 3).")
        try:
            result = allocate(guide, hp, records.load(root / "employers" / slug), json.loads(ws_path.read_text()))
        except (records.RecordError, WorksheetError) as exc:
            raise SystemExit(f"error: {slug}: {exc}")
        render.write_codes_csv(args.out / "codes" / f"{slug}.csv", result, guide)
        results.append(result)
        print(f"{slug}: " + ", ".join(f"{c} {v:.2f}" for c, v in result.totals.items())
              + f" | adjustments {len(result.adjustments)}, open items {len(result.open_items)}, "
                f"questions {len(result.questions)}, employer split {'accepted' if result.accepts_employer_split else 'not accepted'}")

    if args.all:
        report_path, questions_path = args.out / "audit-report.md", args.out / "audit-questions.md"
    else:
        report_path = args.out / "runs" / f"{'+'.join(slugs)}-audit-report.md"
        questions_path = args.out / "runs" / f"{'+'.join(slugs)}-audit-questions.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render.report(results, guide, run))
    questions_path.write_text(render.questions(results))
    (args.out / "run-manifest.json").write_text(json.dumps({
        **run, "employers": {r.rec["file"].slug: {k: f"{v:.2f}" for k, v in r.totals.items()} for r in results},
        "report": str(report_path), "questions": str(questions_path)}, indent=2) + "\n") if args.all else None
    print(f"wrote {report_path} and {questions_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
