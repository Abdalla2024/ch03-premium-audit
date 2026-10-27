# Employer worksheet (`deliverables/worksheets/<slug>.json`)

The worksheet holds the judgments that need a reader: what each person actually does, and which guide code describes a
type of work. The engine does everything else from the records: the thresholds, splits, flat amounts, caps,
subcontractor shares and comparison with the employer. Start from `run.py --init-worksheet <slug>`.

Every code must be one the guide describes. Every judgment cites the record it rests on. If a record does not settle a
judgment, make the best-supported proposal and add an `open_items` entry; do not leave it implied.

| Field | Content |
|---|---|
| `employees.<id>.duty_code` | The code describing the person's **actual** duties from the file (HP-1). For crew with timesheets, give the expected code; the timesheets then decide by days (HP-13, R2). For office staff, give `C-110`; the engine applies the five-day sign-in test and moves the person to the governing code (HP-4). For a catering crew member, give the caterer code; the engine applies the 40% receipts test (HP-14). |
| `employees.<id>.basis` | One or two sentences: what the person does, the record and date that show it, and the guide paragraph. Say so when the only evidence is a job title. |
| `employees.<id>.records` | Files the basis rests on. The payroll register is added automatically. |
| `owners.<id or name>` | `included` (no election of exclusion), `field_work`, `field_code` (the employer's trade code, HP-3), `basis`, `records`. Excluded owners are listed for the record only. |
| `work_type_codes` | Timesheet `work_type` to code. |
| `route_code` | Code for driver payroll in route ride-along weeks, when a route log exists (T-610, HP-2). |
| `receipts` | `{file, offsite_columns, other_columns}`: the gross receipts record and which columns are off-site catering, for the HP-14 test. |
| `subcontract_work_codes` | Subcontracted `work` to code. |
| `subcontractor_certificate_matches` | Payee name to certificate name, when they differ. Always raised as an open item. |
| `facts` | `{fact, record}` statements the report lists as documented. |
| `confirmations` | `{about, question}` employer questions for records relied on that the engine does not know about, such as an owner's exclusion election. Name the person or record and the document needed. |
| `open_items` | `{about, proposal, why, records, employer_question?, merge_with?}`. `merge_with` adds context to an item the engine raises for the same person. |
| `unused_records` | File name to the reason it was not used. |
