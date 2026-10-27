"""Rule tests on a synthetic employer. Nothing here comes from the six real employer files."""

import atexit
import csv
import datetime
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

**CG-11. R-310 Roofing.** Roofs.

**CG-12. R-320 Siding and gutters.** Siding.

**CG-30. Z-100 Field work.** Work at sites.

**CG-31. Z-200 Other field work.** Different work at sites.

**CG-32. T-610 Courier drivers.** Driving routes.

**CG-41. F-710 Restaurants.** Meals.

**CG-42. F-720 Off-site caterers.** Events.
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

    def test_certificate_must_cover_whole_audit_period(self):
        # HP-5 (interview 2): a certificate counts only if it covers the whole audit period.
        e = (Employer([["E1", "A", "Crew", "1000.00"]], {"Z-100": (1, "1000.00")})
             .csv("subcontractor-payments.csv", ["date", "subcontractor", "work", "invoice", "amount_paid"],
                  [["2030-02-01", "Acme", "framing", "I1", "1000.00"],
                   ["2030-08-01", "Acme", "framing", "I2", "333.33"],
                   ["2030-03-01", "Nocert", "roofing", "I3", "100.00"],
                   ["2030-04-01", "Fullco", "roofing", "I4", "500.00"],
                   ["2029-12-31", "Nocert", "roofing", "I0", "999.00"]])
             .csv("insurance-certificates.csv", ["subcontractor", "certificate_no", "coverage_from", "coverage_to"],
                  [["Acme Ltd", "C1", "2030-01-01", "2030-06-30"], ["Fullco", "C2", "2029-12-01", "2031-01-31"]]))
        r = e.run({"employees": {"E1": person("Z-100")},
                   "subcontract_work_codes": {"framing": "Z-100", "roofing": "Z-200"},
                   "subcontractor_certificate_matches": {"Acme": "Acme Ltd"}})
        # Acme's certificate covers the payment date of I1 but not the whole period: both payments added (600 + 200).
        self.assertEqual(r.totals["Z-100"], Decimal("1800.00"))
        self.assertEqual(r.totals["Z-200"], Decimal("60.00"))  # Nocert only; Fullco is covered for the whole period
        self.assertTrue(any("does not change the allocation" in o.why for o in r.open_items))
        self.assertTrue(any("outside the audit period" in n for n in r.notes))

    def test_clerical_five_days_moves_to_governing_code(self):
        # HP-4 (interview 2): whole payroll moves to the field code carrying the most payroll.
        signins = [[f"2030-03-0{d}", "E1", "A", "North lot"] for d in range(1, 5)]
        signins += [[f"2030-04-0{d}", "E2", "B", "North lot"] for d in range(1, 5)] + [["2030-12-25", "E2", "B", "North lot"]]
        e = (Employer([["E1", "A", "Clerk", "100.00"], ["E2", "B", "Clerk", "200.00"],
                       ["E3", "C", "Crew", "300.00"], ["E4", "D", "Crew", "250.00"]], {"C-110": (4, "850.00")})
             .csv("site-signin-log.csv", ["date", "employee_id", "name", "site"], signins))
        r = e.run({"employees": {"E1": person("C-110"), "E2": person("C-110"),
                                 "E3": person("Z-200"), "E4": person("Z-100")}})
        self.assertEqual(r.governing_code, "Z-200")
        self.assertEqual(r.totals, {"C-110": Decimal("100.00"), "Z-100": Decimal("250.00"), "Z-200": Decimal("500.00")})
        # HP-15: the holiday sign-in is used as written and sent to the employer, not dropped.
        self.assertEqual(len(r.questionable), 1)
        self.assertTrue(any("2030-12-25" in t for _, t in r.questions))

    def test_threshold_met_but_no_field_code_keeps_clerical_as_open_item(self):
        signins = [[f"2030-04-0{d}", "E1", "A", "Client office"] for d in range(1, 7)]
        e = (Employer([["E1", "A", "Clerk", "100.00"]], {"C-110": (1, "100.00")})
             .csv("site-signin-log.csv", ["date", "employee_id", "name", "site"], signins))
        r = e.run({"employees": {"E1": person("C-110")}})
        self.assertEqual(r.totals, {"C-110": Decimal("100.00")})
        self.assertIsNone(r.governing_code)
        self.assertEqual(len(r.open_items), 1)
        self.assertTrue(any(about == "A" for about, _ in r.questions))

    def test_no_split_whole_pay_to_most_days_not_hours(self):
        # HP-13: days, not hours. alpha has more hours (3 x 10), beta more days (4 x 2).
        ts = [[f"2030-01-0{d}", "E1", "A", "J1", "alpha", "10"] for d in (2, 3, 4)]
        ts += [[f"2030-01-1{d}", "E1", "A", "J2", "beta", "2"] for d in (2, 3, 4, 5)]
        e = (Employer([["E1", "A", "Crew", "500.00"]], {"Z-100": (1, "500.00")})
             .csv("crew-timesheets.csv", ["date", "employee_id", "name", "job_id", "work_type", "hours"], ts))
        r = e.run({"employees": {"E1": person("Z-100")}, "work_type_codes": {"alpha": "Z-100", "beta": "Z-200"}})
        self.assertEqual(r.totals, {"Z-200": Decimal("500.00")})
        self.assertEqual(r.adjustments[0].kind, "Reclassified")

    def test_route_split_needs_two_ride_days_in_the_pay_week(self):
        # HP-2 (interview 2): two or more ride days in a Monday-Sunday week moves that week; one day does not.
        routes = [["2030-01-02", "R1", "D1", "E1", "5"], ["2030-01-16", "R1", "D1", "E1", "5"],
                  ["2030-01-17", "R1", "D1", "E1", "5"], ["2030-01-09", "R1", "D1", "", "5"]]
        weekly = [["2030-01-01", "2030-01-07", "E1", "100.00"], ["2030-01-08", "2030-01-14", "E1", "110.00"],
                  ["2030-01-15", "2030-01-21", "E1", "120.00"]]
        e = (Employer([["E1", "A", "Dispatcher", "330.00"]], {"C-110": (1, "330.00")})
             .csv("route-log.csv", ["date", "route_id", "driver_id", "ride_along_id", "stops"], routes)
             .csv("weekly-payroll.csv", ["week_start", "week_end", "employee_id", "gross_pay"], weekly))
        r = e.run({"employees": {"E1": person("C-110")}, "route_code": "T-610"})
        self.assertEqual(r.totals, {"C-110": Decimal("210.00"), "T-610": Decimal("120.00")})

    def test_caterer_code_needs_40_percent_offsite_receipts(self):
        # HP-14: F-720 only if off-site catering is 40% or more of gross receipts.
        ws = {"employees": {"E1": person("F-720"), "E2": person("F-710")},
              "receipts": {"file": "gross-receipts.csv", "offsite_columns": ["offsite"], "other_columns": ["dine_in"]}}
        for offsite, expected in (("39.99", {"F-710": Decimal("300.00")}),
                                  ("40.00", {"F-710": Decimal("200.00"), "F-720": Decimal("100.00")})):
            e = (Employer([["E1", "A", "Event Cook", "100.00"], ["E2", "B", "Cook", "200.00"]],
                          {"F-710": (1, "200.00"), "F-720": (1, "100.00")})
                 .csv("gross-receipts.csv", ["month", "dine_in", "offsite"], [["2030-01", f"{100 - Decimal(offsite)}", offsite]]))
            self.assertEqual(e.run(ws).totals, expected, offsite)

    def test_roof_siding_contractor_uses_15_roof_days(self):
        # HP-16 (interview 3): 15 or more roof days -> whole pay R-310; fewer -> whole pay R-320. Not most days.
        def ts(emp, roof, siding, start=1):
            days = [datetime.date(2030, 1, 1) + datetime.timedelta(d) for d in range(start, start + roof + siding)]
            return [[d.isoformat(), emp, emp, "J", "roofing" if i < roof else "siding", "8"] for i, d in enumerate(days)]
        rows = ts("E1", 15, 100) + ts("E2", 14, 3) + ts("E3", 20, 0)
        e = (Employer([["E1", "E1", "Siding", "100.00"], ["E2", "E2", "Roofer", "200.00"], ["E3", "E3", "Roofer", "300.00"]],
                      {"R-310": (3, "600.00")})
             .csv("crew-timesheets.csv", ["date", "employee_id", "name", "job_id", "work_type", "hours"], rows))
        r = e.run({"employees": {i: person("R-310") for i in ("E1", "E2", "E3")},
                   "work_type_codes": {"roofing": "R-310", "siding": "R-320"}})
        self.assertEqual(r.totals, {"R-310": Decimal("400.00"), "R-320": Decimal("200.00")})
        self.assertIn("HP-16", r.applied)
        self.assertFalse(any("most recorded days" in o.proposal for o in r.open_items))

    def test_holiday_entries_flagged_and_hp15_only_when_decisive(self):
        # HP-15 (interviews 2 and 3): holiday entries in timesheets, route logs and sign-ins are used as written and
        # flagged; HP-15 is listed as deciding something only when the allocation rests on the entry.
        roof = [d.isoformat() for d in (datetime.date(2030, 12, 10) + datetime.timedelta(i) for i in range(14))]
        rows = [[d, "E1", "A", "J", "roofing", "8"] for d in roof + ["2030-12-25"]]
        rows += [["2030-11-0" + str(i), "E1", "A", "J", "siding", "8"] for i in range(1, 6)]
        e = (Employer([["E1", "A", "Roofer", "500.00"]], {"R-310": (1, "500.00")})
             .csv("crew-timesheets.csv", ["date", "employee_id", "name", "job_id", "work_type", "hours"], rows))
        r = e.run({"employees": {"E1": person("R-310")}, "work_type_codes": {"roofing": "R-310", "siding": "R-320"}})
        self.assertEqual(r.totals, {"R-310": Decimal("500.00")})  # 15 roof days counted as written
        self.assertEqual(r.questionable[0].decisive, Decimal("500.00"))
        self.assertIn("HP-15", r.applied)
        self.assertTrue(any("2030-12-25" in t and "depends on this record" in t for _, t in r.questions))

        signins = [[f"2030-03-0{d}", "E1", "A", "North lot"] for d in range(1, 7)] + [["2030-12-25", "E1", "A", "North lot"]]
        e = (Employer([["E1", "A", "Clerk", "100.00"], ["E2", "B", "Crew", "300.00"]], {"C-110": (2, "400.00")})
             .csv("site-signin-log.csv", ["date", "employee_id", "name", "site"], signins))
        r = e.run({"employees": {"E1": person("C-110"), "E2": person("Z-100")}})
        self.assertIsNone(r.questionable[0].decisive)  # six days remain without the holiday
        self.assertNotIn("HP-15", r.applied)

    def test_holiday_ride_that_makes_the_week_is_decisive(self):
        routes = [["2030-12-24", "R1", "D1", "E1", "5"], ["2030-12-25", "R1", "D1", "E1", "5"]]
        weekly = [["2030-12-23", "2030-12-29", "E1", "100.00"], ["2030-12-30", "2031-01-05", "E1", "50.00"]]
        e = (Employer([["E1", "A", "Dispatcher", "150.00"]], {"C-110": (1, "150.00")})
             .csv("route-log.csv", ["date", "route_id", "driver_id", "ride_along_id", "stops"], routes)
             .csv("weekly-payroll.csv", ["week_start", "week_end", "employee_id", "gross_pay"], weekly))
        r = e.run({"employees": {"E1": person("C-110")}, "route_code": "T-610"})
        self.assertEqual(r.totals, {"C-110": Decimal("50.00"), "T-610": Decimal("100.00")})
        self.assertEqual(r.questionable[0].decisive, Decimal("100.00"))

    def test_owner_without_field_work_flat_amount_under_clerical(self):
        # HP-3 (interview 3): the same flat figure, under C-110.
        e = Employer([["E1", "Owner", "Owner", "120000.00"]], {"C-110": (1, "120000.00")})
        r = e.run({"employees": {"E1": person("C-110")},
                   "owners": {"E1": {"included": True, "field_work": False, "basis": "office only"}}})
        self.assertEqual(r.totals, {"C-110": Decimal("63700.00")})
        self.assertEqual(r.open_items, [])

    def test_allowance_without_days_proposal_uses_the_only_fitting_rate(self):
        e = Employer([["E1", "A", "Tech", "1000.00", "10", "650.00"], ["E2", "B", "Tech", "1000.00", "4", "188.00"],
                      ["E3", "C", "Tech", "1000.00", "0", "390.00"]], {"Z-100": (3, "3000.00")}, travel=True)
        r = e.run({"employees": {i: person("Z-100") for i in ("E1", "E2", "E3")}})
        item = next(o for o in r.open_items if o.about == "C")
        self.assertIn("all 390.00 of the allowance is payroll", item.proposal)  # allocated as practice stands
        self.assertIn("exactly 6 days at 65.00", item.proposal)
        self.assertIn("282.00 (6 x 47.00) is left out and 108.00 is payroll", item.proposal)

    def test_audit_period_from_business_description_and_conflict_is_open_item(self):
        e = Employer([["E1", "A", "Clerk", "100.00"]], {"C-110": (1, "100.00")})
        (e.dir / "field-notes.md").write_text("Notes. Audit period February 1, 2030 to December 31, 2030.\n")
        r = e.run({"employees": {"E1": person("C-110")}})
        self.assertEqual(r.rec["period"], (datetime.date(2030, 1, 1), datetime.date(2030, 12, 31)))
        self.assertEqual(r.rec["period_file"], "business-description.md")
        self.assertTrue(any(o.about == "Audit period" for o in r.open_items))
        self.assertTrue(any(about == "Audit period" for about, _ in r.questions))

    def test_allocation_reconciles_to_register_plus_adjustments(self):
        e = Employer([["E1", "Owner", "Owner", "1000.00", "0", "0.00"], ["E2", "B", "Tech", "10.00", "2", "100.00"]],
                     {"C-110": (2, "1010.00")}, travel=True)
        r = e.run({"employees": {"E1": person("Z-100"), "E2": person("Z-100")},
                   "owners": {"E1": {"included": True, "field_work": True, "field_code": "Z-100", "basis": "x"}}})
        self.assertEqual(r.reconciliation[-1][1], sum(r.totals.values()))
        self.assertEqual(r.totals, {"Z-100": Decimal("63700.00") + Decimal("10.00") + Decimal("6.00")})

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
