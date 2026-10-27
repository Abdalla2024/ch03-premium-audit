"""Rule tests on a synthetic employer. Nothing here comes from the six real employer files."""

import atexit
import csv
import json
import shutil
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "class-code-assistant" / "scripts"))

from cca import records, render  # noqa: E402
from cca.guide import Guide  # noqa: E402
from cca.rules import WorksheetError, allocate, infer_employer_codes  # noqa: E402

HP = json.loads((ROOT / "skills/class-code-assistant/references/house_practice.json").read_text())

GUIDE = """# Test guide

Edition of March 2030.

**CG-01. Premium basis.** Not used.

**CG-04. C-110 Clerical office employees.** Office work.

**CG-30. Z-100 Field work.** Work at sites.

**CG-31. Z-200 Other field work.** Different work at sites.

**CG-32. T-610 Courier drivers.** Driving routes.
"""


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


class Employer:
    """Build a throwaway employer folder."""

    def __init__(self, register, split, travel=False):
        tmp = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, tmp, True)
        self.dir = Path(tmp) / "test-co"
        self.dir.mkdir()
        rows = "\n".join(f"| {c} | {n} | {a} |" for c, (n, a) in split.items())
        (self.dir / "application.md").write_text(
            f"# Test Co: payroll\n\nApplication APP-T-1, signed by Pat Doe.\n\n| Code | Employees | Payroll |\n|---|---|---|\n{rows}\n")
        (self.dir / "business-description.md").write_text("# Test Co\n\nAudit period January 1, 2030 to December 31, 2030.\n")
        header = ["employee_id", "name", "position", "wages_paid"] + (["travel_days", "travel_allowance_paid"] if travel else [])
        write_csv(self.dir / "payroll-register.csv", header, register)

    def csv(self, name, header, rows):
        write_csv(self.dir / name, header, rows)
        return self

    def run(self, ws):
        return allocate(Guide(GUIDE), HP, records.load(self.dir), ws)


def person(code, **kw):
    return {"duty_code": code, "basis": "test duties", "records": [], **kw}


class GuideTests(unittest.TestCase):
    def test_paragraph_refs_and_edition(self):
        g = Guide(GUIDE)
        self.assertEqual(g.edition, "March 2030")
        self.assertEqual(g.ref_for("Z-100"), "CG-30")
        self.assertEqual(g.ref_for("C-110"), "CG-04")
        with self.assertRaises(ValueError):
            g.ref_for("Q-999")


class RuleTests(unittest.TestCase):
    def test_owner_with_field_work_counted_at_flat_amount(self):
        e = Employer([["E1", "Owner", "Owner", "120000.00"]], {"C-110": (1, "120000.00")})
        r = e.run({"employees": {"E1": person("C-110")},
                   "owners": {"E1": {"included": True, "field_work": True, "field_code": "Z-100", "basis": "on site"}}})
        self.assertEqual(r.totals, {"Z-100": Decimal("63700.00")})
        self.assertFalse(r.accepts_employer_split)

    def test_travel_allowance_cap_and_zero_days(self):
        e = Employer([["E1", "A", "Tech", "1000.00", "10", "600.00"],
                      ["E2", "B", "Tech", "1000.00", "10", "470.00"],
                      ["E3", "C", "Tech", "1000.00", "0", "50.00"]],
                     {"Z-100": (3, "3000.00")}, travel=True)
        r = e.run({"employees": {i: person("Z-100") for i in ("E1", "E2", "E3")}})
        # E1: 600 - 10*47 = 130 payroll; E2: exactly at cap, 0; E3: no travel days, all 50 is payroll.
        self.assertEqual(r.totals["Z-100"], Decimal("3180.00"))
        self.assertEqual(sorted(a.amount for a in r.adjustments), [Decimal("50.00"), Decimal("130.00")])
        self.assertTrue(any("no travel days" in o.why for o in r.open_items))

    def test_uninsured_subcontractor_60_percent_by_certificate_dates(self):
        e = (Employer([["E1", "A", "Crew", "1000.00"]], {"Z-100": (1, "1000.00")})
             .csv("subcontractor-payments.csv", ["date", "subcontractor", "work", "invoice", "amount_paid"],
                  [["2030-02-01", "Acme", "framing", "I1", "1000.00"],
                   ["2030-08-01", "Acme", "framing", "I2", "333.33"],
                   ["2030-03-01", "Nocert", "roofing", "I3", "100.00"],
                   ["2029-12-31", "Nocert", "roofing", "I0", "999.00"]])
             .csv("insurance-certificates.csv", ["subcontractor", "certificate_no", "coverage_from", "coverage_to"],
                  [["Acme Ltd", "C1", "2030-01-01", "2030-06-30"]]))
        r = e.run({"employees": {"E1": person("Z-100")},
                   "subcontract_work_codes": {"framing": "Z-100", "roofing": "Z-200"},
                   "subcontractor_certificate_matches": {"Acme": "Acme Ltd"}})
        self.assertEqual(r.totals["Z-100"], Decimal("1200.00"))  # 1000 + 60% of 333.33 = 200.00 (199.998 rounded)
        self.assertEqual(r.totals["Z-200"], Decimal("60.00"))
        self.assertTrue(any("not the same" in o.why for o in r.open_items))
        self.assertTrue(any("outside the audit period" in n for n in r.notes))

    def test_clerical_site_day_threshold(self):
        signins = [[f"2030-03-0{d}", "E1", "A", "North lot"] for d in range(1, 5)]
        signins += [[f"2030-04-0{d}", "E2", "B", "North lot"] for d in range(1, 6)]
        e = (Employer([["E1", "A", "Clerk", "100.00"], ["E2", "B", "Clerk", "200.00"]], {"C-110": (2, "300.00")})
             .csv("site-signin-log.csv", ["date", "employee_id", "name", "site"], signins))
        r = e.run({"employees": {"E1": person("C-110"), "E2": person("C-110")}, "site_codes": {"North lot": "Z-100"}})
        self.assertEqual(r.totals, {"C-110": Decimal("100.00"), "Z-100": Decimal("200.00")})
        self.assertTrue(any(o.about == "B" for o in r.open_items))

    def test_threshold_met_but_no_code_keeps_clerical_as_open_item(self):
        signins = [[f"2030-04-0{d}", "E1", "A", "Client office"] for d in range(1, 7)]
        e = (Employer([["E1", "A", "Clerk", "100.00"]], {"C-110": (1, "100.00")})
             .csv("site-signin-log.csv", ["date", "employee_id", "name", "site"], signins))
        r = e.run({"employees": {"E1": person("C-110")}, "site_codes": {"Client office": None}})
        self.assertEqual(r.totals, {"C-110": Decimal("100.00")})
        self.assertTrue(r.accepts_employer_split)
        self.assertEqual(len(r.open_items), 1)

    def test_unmapped_site_is_an_error_not_a_guess(self):
        signins = [[f"2030-04-0{d}", "E1", "A", "Mystery"] for d in range(1, 7)]
        e = (Employer([["E1", "A", "Clerk", "100.00"]], {"C-110": (1, "100.00")})
             .csv("site-signin-log.csv", ["date", "employee_id", "name", "site"], signins))
        with self.assertRaises(WorksheetError):
            e.run({"employees": {"E1": person("C-110")}, "site_codes": {}})

    def test_no_split_whole_pay_to_most_hours(self):
        ts = [["2030-01-02", "E1", "A", "J1", "alpha", "8"]] * 3 + [["2030-01-03", "E1", "A", "J2", "beta", "8"]] * 4
        e = (Employer([["E1", "A", "Crew", "500.00"]], {"Z-100": (1, "500.00")})
             .csv("crew-timesheets.csv", ["date", "employee_id", "name", "job_id", "work_type", "hours"], ts))
        r = e.run({"employees": {"E1": person("Z-100")}, "work_type_codes": {"alpha": "Z-100", "beta": "Z-200"}})
        self.assertEqual(r.totals, {"Z-200": Decimal("500.00")})
        self.assertEqual(r.adjustments[0].kind, "Reclassified")

    def test_whole_week_route_split(self):
        routes = [["2030-01-02", "R1", "D1", "E1", "5"], ["2030-01-16", "R1", "D1", "E1", "5"],
                  ["2030-01-17", "R1", "D1", "E1", "5"], ["2030-01-09", "R1", "D1", "", "5"]]
        weekly = [["2030-01-01", "2030-01-07", "E1", "100.00"], ["2030-01-08", "2030-01-14", "E1", "110.00"],
                  ["2030-01-15", "2030-01-21", "E1", "120.00"]]
        e = (Employer([["E1", "A", "Dispatcher", "330.00"]], {"C-110": (1, "330.00")})
             .csv("route-log.csv", ["date", "route_id", "driver_id", "ride_along_id", "stops"], routes)
             .csv("weekly-payroll.csv", ["week_start", "week_end", "employee_id", "gross_pay"], weekly))
        r = e.run({"employees": {"E1": person("C-110")}, "route_code": "T-610"})
        self.assertEqual(r.totals, {"C-110": Decimal("110.00"), "T-610": Decimal("220.00")})

    def test_unknown_code_in_worksheet_is_rejected(self):
        e = Employer([["E1", "A", "Clerk", "100.00"]], {"C-110": (1, "100.00")})
        with self.assertRaises(WorksheetError):
            e.run({"employees": {"E1": person("Q-999")}})

    def test_every_adjustment_has_a_question_naming_it(self):
        e = Employer([["E1", "Owner", "Owner", "1.00"], ["E2", "Zed", "Tech", "10.00", "1", "100.00"]],
                     {"C-110": (2, "11.00")}, travel=True)
        r = e.run({"employees": {"E1": person("C-110"), "E2": person("Z-100")},
                   "owners": {"E1": {"included": True, "field_work": True, "field_code": "Z-100", "basis": "x"}}})
        for a in r.adjustments:
            self.assertTrue(any(a.about in about or a.about in text for about, text in r.questions), a.about)


class OutputTests(unittest.TestCase):
    def test_csv_format(self):
        e = Employer([["E1", "A", "Clerk", "1234.50"], ["E2", "B", "Crew", "0.00"]], {"C-110": (2, "1234.50")})
        r = e.run({"employees": {"E1": person("C-110"), "E2": person("Z-100")}})
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.csv"
            render.write_codes_csv(path, r, Guide(GUIDE))
            self.assertEqual(path.read_text(), "class_code,payroll_allocated,rationale_ref\nC-110,1234.50,CG-04\n")

    def test_employer_split_inference(self):
        reg = [{"id": "a", "wages": Decimal("1")}, {"id": "b", "wages": Decimal("2")}, {"id": "c", "wages": Decimal("3")}]
        mapping, _ = infer_employer_codes(reg, {"X": {"employees": 1, "payroll": Decimal("2")},
                                                "Y": {"employees": 2, "payroll": Decimal("4")}})
        self.assertEqual(mapping, {"a": "Y", "b": "X", "c": "Y"})
        mapping, why = infer_employer_codes(reg, {"X": {"employees": 3, "payroll": Decimal("7")}})
        self.assertIsNone(mapping)


if __name__ == "__main__":
    unittest.main()
