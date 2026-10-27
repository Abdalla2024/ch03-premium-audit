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
| `python3 -m unittest discover -s tests` | 13 tests OK. They cover the guide parser, owner flat amount, allowance cap and zero-day allowance, the 60% uninsured subcontractor share with certificate dates and name mismatch, the five-day clerical threshold, the threshold with no applicable code, an unmapped site raising an error, the no-split rule, the whole-week route split, unknown-code rejection, question coverage, the CSV format and split inference. All use a synthetic employer. |
| `python3 skills/class-code-assistant/scripts/validate.py` | 165/165 checks pass. It checks CSV header, cents and zero rows, `rationale_ref` against the guide, CSV totals against the report, a section per employer in both files, every adjustment named in that employer's questions, a stated accept/not-accept decision, no rate or premium figures, no employer names or IDs in the Skill code, and an unchanged interview export. |
| `run.py --all` (fresh fetch) and `--employer larkspur-lane-bistro --local .cache/sources` | Same CSV for that employer either way. |
| Error paths | A missing worksheet, an unfilled scaffold and a missing guide each stop with a clear `error:` and exit 1. |
| Hand check | Patuxent Electric E-510 (306,024.85 + 63,700.00 + 3 × 720.00 + 390.00 = 372,274.85), Severn Homebuilders subcontractor additions (60% of 41,155.65 = 24,693.39 H-420; 60% of 31,645.65 = 18,987.39 R-310) and the Bay Crest Exteriors totals were recomputed by hand from the source files and match. |

Not verified. Each of these is an open item in the report:

- The readings of house practice (A1 to A6 in `references/house-practice.md`) have not been confirmed by the auditor.
- The code given to a clerical person who passes the five-day test (Teresa Lindqvist, Dana Whitcomb) is the Skill's
  proposal.
- The call-first ranking rule is the Skill's own; the auditor has not said how she prioritises calls.
- The employer-level comparison relies on an inferred per-person reading of each application. That reading is unique for
  all six employers, but it is still an inference.
- The Drive fetcher depends on Google's public folder-view page; if its markup changes, fetching fails loudly and
  `--local` still works.

## First-pass decisions on the employers' own splits

| Employer | Employer's split | Rests on |
|---|---|---|
| Harbor Point Legal | Accepted | payroll register; field notes (all office work). Tomas Reyes's six condominium sign-ins are an open item. |
| Larkspur Lane Bistro | Accepted | payroll register; field notes (catering crew does off-site events, CG-42). The crew's restaurant shifts have no time record: open item. |
| Bay Crest Exteriors | Not accepted | crew timesheets (eight crew members on roofing, siding and gutters, not office work); site sign-in log (estimator, 9 site days) |
| Patuxent Electric | Not accepted | business description (owner not excluded); field notes and site sign-in log (owner does field work); register travel columns (allowance above 47.00 per day) |
| Severn Homebuilders | Not accepted | site sign-in log (office manager, 11 site days); subcontractor payments against insurance certificates (Tidewater Drywall has none; Kent Island's lapsed 2026-01-31) |
| Annapolis Courier | Not accepted | route log and weekly payroll (both dispatchers rode along; whole weeks moved to T-610) |
