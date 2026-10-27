"""Load one employer's file: payroll register, application, business description and supporting logs.

Only the payroll register, the application and an audit period statement are required. Every other record is optional
and is used when present. Files nothing reads are reported, so a reviewer can see what the first pass did not use.
"""

import csv
import datetime
import re
from decimal import Decimal
from pathlib import Path

CENT = Decimal("0.01")
PERIOD = re.compile(r"Audit period ([A-Z][a-z]+ \d{1,2}, \d{4}) to ([A-Z][a-z]+ \d{1,2}, \d{4})")
SPLIT_ROW = re.compile(r"^\|\s*([A-Z]-\d{3})\s*\|\s*(\d+)\s*\|\s*([\d,]+\.\d{2})\s*\|", re.M)


def money(value):
    value = str(value).strip().replace(",", "")
    return Decimal(value or "0").quantize(CENT)


def day(value):
    return datetime.date.fromisoformat(value.strip())


class RecordError(ValueError):
    pass


class EmployerFile:
    """Read-only view of one employer folder that remembers which files were read."""

    def __init__(self, folder):
        self.folder = Path(folder)
        if not self.folder.is_dir():
            raise RecordError(f"employer folder not found: {self.folder}")
        self.slug = self.folder.name
        self.files = sorted(p.name for p in self.folder.iterdir() if p.is_file() and not p.name.startswith("."))
        self.read = set()

    def find(self, *patterns):
        for pattern in patterns:
            hits = sorted(self.folder.glob(pattern))
            if hits:
                return hits[0].name
        return None

    def text(self, name):
        self.read.add(name)
        return (self.folder / name).read_text(encoding="utf-8")

    def rows(self, name, required):
        self.read.add(name)
        with open(self.folder / name, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            missing = set(required) - set(reader.fieldnames or [])
            if missing:
                raise RecordError(f"{name} is missing column(s): {', '.join(sorted(missing))}")
            return [{k: (v or "").strip() for k, v in row.items()} for row in reader]

    def unread(self):
        return [f for f in self.files if f not in self.read]


def load(folder):
    ef = EmployerFile(folder)
    rec = {"file": ef}

    name = ef.find("payroll-register.csv", "*payroll-register*.csv")
    if not name:
        raise RecordError(f"{ef.slug}: no payroll register (payroll-register.csv) in the employer file")
    rec["register_file"] = name
    rec["register"] = []
    for r in ef.rows(name, ["employee_id", "name", "position", "wages_paid"]):
        rec["register"].append({
            "id": r["employee_id"], "name": r["name"], "position": r["position"], "wages": money(r["wages_paid"]),
            "travel_days": int(r["travel_days"]) if r.get("travel_days") else None,
            "travel_allowance": money(r["travel_allowance_paid"]) if r.get("travel_allowance_paid") else None,
        })
    rec["has_travel_columns"] = any(e["travel_allowance"] is not None for e in rec["register"])

    name = ef.find("application.md", "*application*.md")
    if not name:
        raise RecordError(f"{ef.slug}: no application (application.md) with the employer's own payroll split")
    text = ef.text(name)
    rec["application_file"] = name
    rec["application_id"] = (re.search(r"Application (APP-[\w-]+)", text) or [None, None])[1]
    rec["signed_by"] = (re.search(r"signed by ([^.\n]+)", text) or [None, None])[1]
    rec["employer_name"] = (re.search(r"^#\s*([^:\n]+)", text, re.M) or [None, ef.slug])[1].strip()
    rec["employer_split"] = {code: {"employees": int(n), "payroll": money(amt)} for code, n, amt in SPLIT_ROW.findall(text)}
    if not rec["employer_split"]:
        raise RecordError(f"{ef.slug}: could not read the employer's payroll split table in {name}")
    note = re.search(r'Employer\'s note:\s*"(.*?)"', text, re.S)
    rec["employer_note"] = " ".join(note.group(1).split()) if note else None

    # The business description defines the audit period (house practice, interview 3). Other statements are compared.
    desc = ef.find("business-description.md", "*description*.md")
    stated = {}
    for name in dict.fromkeys([desc] + [n for n in ef.files if n.endswith(".md")] + [rec["register_file"]]):
        m = name and PERIOD.search((ef.folder / name).read_text(encoding="utf-8"))
        if m:
            ef.read.add(name)
            stated[name] = tuple(datetime.datetime.strptime(s, "%B %d, %Y").date() for s in m.groups())
    if not stated:
        raise RecordError(f"{ef.slug}: no 'Audit period <date> to <date>' statement found in the employer file")
    rec["period_file"] = desc if desc in stated else next(iter(stated))
    rec["period"] = stated[rec["period_file"]]
    rec["period_issues"] = []
    if rec["period_file"] != desc:
        rec["period_issues"].append(f"the business description does not state the audit period; "
                                    f"{rec['period_file']} does")
    for name, p in stated.items():
        if p != rec["period"]:
            rec["period_issues"].append(f"{name} states {p[0].isoformat()} to {p[1].isoformat()}")

    for name in [n for n in ef.files if n.endswith(".md") and "note" in n]:
        rec["field_notes_file"] = name
        ef.read.add(name)
    if desc:
        ef.read.add(desc)
        rec["description_file"] = desc

    optional = {
        "timesheets": (("*timesheet*.csv",), ["date", "employee_id", "work_type", "hours"]),
        "signins": (("*sign*in*.csv",), ["date", "employee_id", "site"]),
        "route_log": (("route-log*.csv", "*route*.csv"), ["date", "driver_id", "ride_along_id"]),
        "weekly_payroll": (("weekly-payroll*.csv",), ["week_start", "week_end", "employee_id", "gross_pay"]),
        "sub_payments": (("subcontractor-payments*.csv", "*subcontract*.csv"), ["date", "subcontractor", "work", "amount_paid"]),
        "certificates": (("insurance-certificates*.csv", "*certificate*.csv"), ["subcontractor", "certificate_no", "coverage_from", "coverage_to"]),
    }
    rec["receipts_file"] = ef.find("*receipts*.csv")
    for key, (patterns, cols) in optional.items():
        name = ef.find(*patterns)
        rec[key + "_file"] = name
        rec[key] = ef.rows(name, cols) if name else []
    return rec
