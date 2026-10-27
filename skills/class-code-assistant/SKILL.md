---
name: class-code-assistant
description: First-pass premium audit for Linden Shore Mutual workers' compensation new business. It reads an employer's payroll register, application, business description, field notes and time records, then assigns company class codes. It allocates payroll to each code, citing the classification guide paragraph and the supporting records, and drafts employer-specific audit questions. Use it when a premium auditor asks to check, classify or allocate an employer's payroll, or to run the first pass on an employer file. It never sets rates or quotes premium.
---

# Class code assistant

This Skill does the first pass that Nadia Brennan, Senior Premium Auditor, reviews before underwriting quotes an
employer. It classifies people and allocates payroll. It does **not** set rates, compute premium or quote.

## Ground rules

- **Use only the company's own rules.** The authoritative rules are the Linden Shore Mutual classification guide
  excerpt (paragraphs `CG-nn`), read from the location in `references/sources.json` on every run. Public
  classification manuals, such as NCCI or state manuals, do not apply and give wrong answers. Never use them.
- **Apply house practice as the auditor stated it.** `references/house-practice.md` keeps three lists apart:
  confirmed rules from interviews 1 to 3 (HP-1 to HP-17), stated gaps where the auditor has no rule, and the Skill's
  own readings (R2, R3, R4, R6, R14, R15), which are always raised as open items where they matter. The numbers are in `references/house_practice.json`.
- **Classify by actual duties, not titles (HP-1).** The records in the file decide, not the employer's application
  (HP-7).
- **Gray areas: propose, explain and flag, never invent.** When neither the guide nor house practice covers a case,
  propose a treatment, write down why, and add an open item that goes on the employer's question list and
  that the auditor reviews (HP-10). Never present a proposal as company
  rule.
- **Keep facts apart from assumptions.** Every fact cites the employer record it comes from. Every assumption is an
  open item.

## Inputs

Per employer, one folder named by its slug (for example `acme-roofing`) holding:

| File | Required | Used for |
|---|---|---|
| `payroll-register.csv` (`employee_id,name,position,wages_paid`, optional `travel_days,travel_allowance_paid`) | yes | wages per person; out-of-town allowance |
| `application.md` (table of code, employees, payroll; employer's note) | yes | the employer's own split, for comparison |
| a `.md` stating `Audit period <Month D, YYYY> to <Month D, YYYY>`: the business description defines it (HP-17) | yes | audit period filter; a missing or differing statement elsewhere is an open item |
| `field-notes.md`, `business-description.md` | no | duties, owner status, subcontractors |
| `*timesheet*.csv` (`date,employee_id,work_type,hours`) | no | crew work by type, counted in days (HP-2, HP-13): at a roofing-and-siding contractor, 15 or more roof days means R-310, fewer R-320 (HP-16); other mixes R2 |
| `*sign*in*.csv` (`date,employee_id,site`) | no | clerical job-site days; five or more moves the whole pay to the governing code (HP-4) |
| `route-log.csv` (`date,driver_id,ride_along_id`) + `weekly-payroll.csv` (`week_start,week_end,employee_id,gross_pay`) | no | route split: pay weeks with two or more ride days go to T-610 (HP-2) |
| `subcontractor-payments.csv` (`date,subcontractor,work,invoice,amount_paid`) + `insurance-certificates.csv` (`subcontractor,certificate_no,coverage_from,coverage_to`) | no | uninsured subcontractors; a certificate must cover the whole audit period (HP-5) |
| `*receipts*.csv` (`month` + receipts columns named in the worksheet) | no | caterer test: F-720 only if off-site catering is 40% or more of gross receipts (HP-14) |

Other files are listed in the report as not used. Give the reason in the worksheet's `unused_records`.

Plus one **worksheet** per employer, `deliverables/worksheets/<slug>.json`, holding the analyst's judgments (step 3).

## How to run

From the repository root, with Python 3.10 or later and no other dependencies:

1. **Fetch and scaffold.** Run `python3 skills/class-code-assistant/scripts/run.py --init-worksheet <slug>`. This
   downloads the guide and employer files into `.cache/sources/` and writes an empty worksheet listing every person,
   work type, subcontracted trade and receipts column that needs a decision.
2. **Read everything.** Read the guide (`.cache/sources/classification-guide.md`) and every file in
   `.cache/sources/employers/<slug>/`. Note which statements are documented, and where the employer's application
   disagrees with its own records.
3. **Fill in the worksheet** following `references/worksheet.md`. For each person, record the code that describes
   what they actually do, a `basis` citing the record, and the `records` relied on. Map each timesheet work type, job
   subcontracted trade to a guide code, and name the off-site catering receipts columns. Record owners,
   documented facts, confirmations to ask the employer for, and open items for gray areas. Do **not** do arithmetic
   here; the engine applies the house rules.
4. **Run.** Use `python3 skills/class-code-assistant/scripts/run.py --employer <slug>` for one employer, or `--all`
   for every employer folder at the source. Add `--local <dir>` to use a local copy laid out as
   `<dir>/classification-guide.md` and `<dir>/employers/<slug>/`, instead of fetching.
5. **Check.** Run `python3 -m unittest discover -s tests` and
   `python3 skills/class-code-assistant/scripts/validate.py`. Then read the report section and the questions as the
   auditor would, and fix the worksheet, not the outputs, if anything is wrong.
6. **Hand over** to the auditor for review (HP-11). The output is a first pass, not audit work.

## Outputs

| Path | Content |
|---|---|
| `deliverables/codes/<slug>.csv` | Exactly `class_code,payroll_allocated,rationale_ref`. One row per code carrying payroll, dollars to the cent, `rationale_ref` = the guide paragraph describing the code |
| `deliverables/audit-report.md` (`--all`) or `deliverables/runs/<slug>-audit-report.md` | Call-first order with reasons. Per employer: whether the employer's split is accepted and the records that decision rests on, the allocation against the employer's split, where and why they differ, every adjustment with person or payment, amount and records, an employee-by-employee basis, documented facts, open items, and notes on unused records |
| `deliverables/audit-questions.md` (or `deliverables/runs/<slug>-audit-questions.md`) | Per employer, questions naming the person, subcontractor or record, and the document needed. Every adjustment, record relied on, questionable record and open item is covered (HP-9, HP-10, HP-15) |
| `deliverables/run-manifest.json` (`--all`) | Fetch time, guide sha256 and totals per employer, for traceability |

## Error behaviour

The run stops with `error: ...` and a non-zero exit, writing nothing for that employer, when:

- the guide, the payroll register, the application split or the audit period statement is missing or unreadable;
- a CSV lacks a required column;
- the worksheet is missing, does not list exactly the register's employees, leaves a decision unfilled, or names a
  class code the guide does not describe;
- a timesheet work type, a subcontracted trade or the route code has no worksheet mapping. The engine
  will not guess one.

Conditions the records can't settle become open items and do not stop the run: a tie in timesheet days, a
certificate name mismatch, an allowance with no travel days, weekly pay that does not sum to the register, a sign-in on
a holiday in a sign-in log, route log or crew timesheet (used as written, sent to the employer, and marked decisive or
not, HP-15), an audit period missing from the business description or stated differently elsewhere (HP-17), a five-day
threshold met at an employer with no
field code, or a caterer with no receipts record.

## Supporting files

- `references/house-practice.md`: the audit team's unwritten rules from the three interviews, with timestamps, plus the
  stated gaps and the Skill's readings.
- `references/house_practice.json`: the numeric parameters (flat owner amount, day threshold, subcontractor share,
  allowance cap).
- `references/sources.json`: where the guide and employer files are kept.
- `references/worksheet.md`: the worksheet fields and how to fill them.
- `scripts/fetch_sources.py`: downloads the sources; standard library only, no credentials.
- `scripts/run.py`: the command-line entry point. `scripts/cca/` holds the guide parser, record loader, rule engine
  and renderer.
- `scripts/validate.py`: checks the deliverables against the required formats.
