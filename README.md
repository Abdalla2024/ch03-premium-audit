# Class Code and Premium Audit Assistant

A reusable Agent Skill that does the first pass of a Linden Shore Mutual premium audit on any employer file. It
suggests the company's class codes, allocates payroll to them with the guide paragraph and supporting records for each
decision, and drafts the questions the auditor should put to the employer. It classifies and allocates payroll only; it
does not set rates or quote premium.

## Interview rule

**Interview rule.** You conduct the stakeholder interview yourself, and the questions are yours. Do not connect a coding
agent or any other AI to the interview to run, script, or automate it. The interview transcript is assessed together
with the code; a project whose interview was run by an agent is not scored.

- This is a real-case Challenge, closer to client work. The course rule is to plan for at most 3 conversations with the stakeholder, so prepare before each conversation and ask completely.
- The employer files and the company's classification rules are not in this repository. Ask Nadia Brennan, the
  premium auditor you interview, where they are, and read them from there during each run.
- No implementation or runtime is supplied; choose and document the dependencies your Skill needs.
- Export your interview as the original Markdown, save one final complete file per session under `interviews/`, and
  commit it with your code. Do not rewrite the export.

## Layout

| Path | What it is |
|---|---|
| `interviews/` | Original interview exports, unchanged |
| `skills/class-code-assistant/SKILL.md` | The Skill: inputs, steps, outputs, error behaviour |
| `skills/class-code-assistant/references/` | House practice from the interview, its parameters, source locations, worksheet guide |
| `skills/class-code-assistant/scripts/` | Fetcher, engine (`cca/`), runner and validator |
| `deliverables/worksheets/<slug>.json` | The analyst's per-employer judgments (duty codes, work and site mappings, facts, open items) |
| `deliverables/codes/<slug>.csv`, `audit-report.md`, `audit-questions.md` | The required outputs |
| `tests/` | Rule tests on a synthetic employer |

## Setup

Python 3.10 or later; standard library only, so there is nothing to install. The runner downloads the classification
guide and the employer files from the Google Drive locations Nadia Brennan gave in interview 1
(`skills/class-code-assistant/references/sources.json`) into `.cache/sources/` on every run. The cache is git-ignored.
The links are view-only shares, so no credentials are used or stored.

## Run

```sh
# all six employers: fetches sources, writes deliverables/codes/*.csv, audit-report.md, audit-questions.md
python3 skills/class-code-assistant/scripts/run.py --all

# one employer: writes deliverables/codes/<slug>.csv and deliverables/runs/<slug>-audit-{report,questions}.md
python3 skills/class-code-assistant/scripts/run.py --employer severn-homebuilders
```

Add `--local <dir>` to run from a local copy laid out as `<dir>/classification-guide.md` and
`<dir>/employers/<slug>/`, instead of fetching.

### A new employer

1. Put the employer's folder (payroll register, application, business description, field notes, any timesheets, sign-in
   or route logs, and any subcontractor payments or certificates) at the source location, or in a local copy.
2. `python3 skills/class-code-assistant/scripts/run.py --init-worksheet <slug>` writes
   `deliverables/worksheets/<slug>.json`, listing every decision the records need.
3. Fill it in from the records, following `skills/class-code-assistant/references/worksheet.md`.
4. `python3 skills/class-code-assistant/scripts/run.py --employer <slug>`, then run the checks below.

## Verification

Commands run on the committed revision, with their results:

| Command | Result |
|---|---|
| `python3 -m unittest discover -s tests` | 14 tests OK, all on a synthetic employer. They cover the guide parser; the owner flat amount; the allowance cap and an allowance with no travel days; a certificate that must cover the whole audit period, plus a name mismatch; the five-day sign-in test moving pay to the governing code, including a holiday sign-in used as written; the threshold at an employer with no field code; the no-split rule counted in days, not hours; the route split needing two ride days in a week; the 40% caterer receipts test at 39.99% and 40.00%; reconciliation; unknown-code rejection; question coverage; the CSV format; and the split pairing. |
| `python3 skills/class-code-assistant/scripts/validate.py` | 270/270 checks pass. It checks CSV header, cents, zero rows and `rationale_ref` against the guide; CSV totals against the report and the reconciliation total; every cited record file exists in that employer's folder; every cited `CG-nn` is in the guide and every `HP-n` or `R-n` is in `house-practice.md`; every adjustment and open item is on that employer's question list; no rate or premium figures; no employer names or IDs in the Skill code; and both interview exports are committed and untouched since their first commit. It was also run against a deliberately broken copy: a changed CSV cent, an unknown rule label and a non-existent record are each reported and the exit status is 1. |
| `run.py --all` (fresh fetch from the Drive sources) and `--employer severn-homebuilders --local .cache/sources` | Same CSV for that employer either way. |
| Error paths | An unfilled worksheet and a missing guide each stop with a clear `error:` and exit 1. |
| Hand check | Annapolis T-610: 153,886.20 + 22,808.75 (Lena Ortiz's 25 weeks with two or more ride days) = 176,694.95. Severn R-310: 60% of 45,945.65 (all three Kent Island payments) = 27,567.39. Severn H-420: 284,670.30 + 59,840.70 + 60% of 41,155.65 = 369,204.39. Larkspur: off-site catering 362,410.85 of 1,647,026.05 receipts = 22.00%, so all 340,725.35 is F-710. Patuxent E-510: 306,024.85 + 63,700.00 + 3 × 720.00 + 390.00 = 372,274.85. All recomputed by hand from the source files and matched. |

Not verified. Each item that affects an allocation is an open item in the report:

- The Skill's readings R2 (most timesheet days decide a crew member's single code), R3, R4 (which payroll decides the
  governing code), R6 (allowance with no travel days) and R14 (receipt months that partly overlap the period) are not
  confirmed by the auditor. On these six files, only R2 and R6 change an allocation.
- Whether the July 2025 guide edition applies to the whole audit period. Nadia knows only the guide she has.
- The 'Employer's code' column pairs people with the application's totals. The application names no one, so this is
  used only to explain differences, never to classify.
- The Drive fetcher depends on Google's public folder-view page; if its markup changes, fetching fails loudly and
  `--local` still works.

## First-pass decisions on the employers' own splits

| Employer | Employer's split | Rests on |
|---|---|---|
| Harbor Point Legal | Accepted | payroll register and field notes (all office work). Tomas Reyes has 6 sign-in days, but the firm has no field code to move him to: open item. |
| Larkspur Lane Bistro | Not accepted | gross-receipts.csv: off-site catering is 22.00% of receipts, below the 40% test (HP-14), so the catering crew is F-710, not F-720 |
| Bay Crest Exteriors | Not accepted | crew timesheets (eight crew members on roofing, siding and gutters, counted in days); site sign-in log (estimator, 9 days, so the governing code R-310) |
| Patuxent Electric | Not accepted | business description (owner not excluded); field notes and site sign-in log (owner does field work, so the flat 63,700.00 under E-510); register travel columns (allowance above 47.00 per day) |
| Severn Homebuilders | Not accepted | site sign-in log (office manager, 11 days, so the governing code H-420); certificates (Tidewater Drywall has none; Kent Island's ends 2026-01-31, before the period ends, so all three of its payments are added) |
| Annapolis Courier | Not accepted | route log and weekly payroll (Lena Ortiz's 25 weeks with two or more ride days go to T-610; Paul Haskins's two single-day weeks stay C-110) |
