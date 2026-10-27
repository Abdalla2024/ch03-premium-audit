# Premium audit first pass: class codes and payroll allocation

Prepared by the class-code-assistant Skill as a **first pass for review by Nadia Brennan, Senior Premium Auditor**. It is not audit work until she has reviewed it (house practice HP-11). It classifies and allocates payroll only; it does not set rates or quote premium.

- Classification rules: Linden Shore Mutual classification guide excerpt, edition of July 2025, sha256 `89480f691737`, read from https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view.
- Employer files read from https://drive.google.com/drive/folders/1pt8gzX8HDuaAq6g8ZFeQ66zbVIYdlN_n at 2026-10-27T04:14:59+00:00.
- Three kinds of statement are kept apart:
  - **Confirmed rules** (`HP-n`) are what Nadia Brennan stated in interviews 1 and 2, listed with timestamps in `skills/class-code-assistant/references/house-practice.md`, together with the guide (`CG-nn`).
  - **Facts** cite the employer record they come from.
  - **Open items** are unresolved judgements. Each one gives the proposed handling, why, and the Skill's reading (`R-n`) where one was needed. Each is on the employer's question list for confirmation, and Nadia reviews the proposal (HP-10).
- **Questionable records** are used as written and sent to the employer to confirm (HP-15).

## Which two employers to call first

Nadia left the choice to the analyst, with reasons (HP-12). The order ranks employers by the payroll the first pass places in a code above what the employer reported there: payroll moved in from another code, plus payroll added. It is in dollars of payroll, not premium. A larger figure means the employer's own split, and so the figures underwriting would otherwise quote from, is further from the records. Ties go to the employer with more open items.

| Order | Employer | Payroll placed differently | Net change | Employer reported | First pass | Open items | Employer questions |
|---|---|---|---|---|---|---|---|
| 1 | Bay Crest Exteriors | 319,158.10 | 0.00 | 541,498.05 | 541,498.05 | 0 | 22 |
| 2 | Larkspur Lane Bistro | 114,293.80 | 0.00 | 340,725.35 | 340,725.35 | 0 | 6 |
| 3 | Severn Homebuilders | 112,101.48 | +52,260.78 | 461,879.70 | 514,140.48 | 1 | 9 |
| 4 | Patuxent Electric | 66,250.00 | -51,750.00 | 467,930.45 | 416,180.45 | 1 | 11 |
| 5 | Annapolis Courier | 22,808.75 | 0.00 | 284,515.40 | 284,515.40 | 0 | 8 |
| 6 | Harbor Point Legal | 0.00 | 0.00 | 425,148.16 | 425,148.16 | 1 | 4 |

1. **Bay Crest Exteriors**: 319,158.10 of payroll is placed differently from the employer's split. The largest drivers are Teresa Lindqvist: reclassified (68,430.90 under R-310); Luis Carrillo: reclassified (54,880.40 under R-310); Brian Tull: reclassified (52,115.75 under R-310). Open items for the employer: none.
2. **Larkspur Lane Bistro**: 114,293.80 of payroll is placed differently from the employer's split. The largest drivers are Hannah Pryor: caterer receipts test (46,725.55 under F-710); Ivan Petrov: caterer receipts test (38,190.40 under F-710); Clara Bose: caterer receipts test (29,377.85 under F-710). Open items for the employer: none.

Close call for second place: Severn Homebuilders (112,101.48) is within 5% of Larkspur Lane Bistro (114,293.80). Of the 112,101.48, 52,260.78 is added only because certificates are missing from the file and could change if the employer produces them. Nadia may prefer that call.

## Summary

| Employer | Employer's split | Decision rests on |
|---|---|---|
| Annapolis Courier | Not accepted | payroll-register.csv, route-log.csv, field-notes.md, weekly-payroll.csv |
| Bay Crest Exteriors | Not accepted | payroll-register.csv, field-notes.md, crew-timesheets.csv, site-signin-log.csv |
| Harbor Point Legal | Accepted | payroll-register.csv, field-notes.md, site-signin-log.csv |
| Larkspur Lane Bistro | Not accepted | payroll-register.csv, field-notes.md, gross-receipts.csv |
| Patuxent Electric | Not accepted | payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md |
| Severn Homebuilders | Not accepted | payroll-register.csv, business-description.md, field-notes.md, site-signin-log.csv, subcontractor-payments.csv, insurance-certificates.csv |

## Annapolis Courier

Application APP-AC-0529, signed by Gloria Rhee. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, payroll-register.csv, route-log.csv, weekly-payroll.csv.

Employer's note on the application: "Our dispatchers work the phones. Lena rides along about two days a week to train new stops, so at most two fifths of her time is on the road."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, route-log.csv, field-notes.md, weekly-payroll.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 130,629.20 | 107,820.45 | -22,808.75 |
| T-610 | CG-31 | 153,886.20 | 176,694.95 | +22,808.75 |
| **Total** | | **284,515.40** | **284,515.40** | **0.00** |

Confirmed rules that decided or changed something here: HP-2, HP-15. Governing code (field code carrying the most payroll, HP-4): T-610.

Reconciliation:

| Step | Amount (USD) |
|---|---|
| Payroll register wages | 284,515.40 |
| First-pass total (equals the sum of the codes CSV) | 284,515.40 |

### Where and why the first pass differs from the employer's split

- **C-110** -22,808.75: out: Lena Ortiz (47,442.20 reported here, now 22,808.75 T-610, 24,633.45 C-110).
- **T-610** +22,808.75: in: Lena Ortiz (whole-week route split, 22,808.75).
- How the employer's split was compared: the application names no people; exactly one pairing of register wages reproduces its head count and payroll for every code, so 'Employer's code' shows that pairing. It explains differences only and decided no classification (HP-1).

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Lena Ortiz | Whole-week route split | 22,808.75 | T-610 | 60 ride-along days in the audit period. Pay weeks by ride days: 0 day(s) 21 week(s), 1 day(s) 6 week(s), 2 day(s) 21 week(s), 3 day(s) 4 week(s). 25 pay weeks have 2 or more ride days; their gross pay of 22,808.75 moves from C-110 to T-610: 2025-07-07 (2 days, 912.35), 2025-07-28 (2 days, 912.35), 2025-08-18 (3 days, 912.35), 2025-08-25 (2 days, 912.35), 2025-09-01 (2 days, 912.35), 2025-09-08 (2 days, 912.35), 2025-09-15 (2 days, 912.35), 2025-09-29 (3 days, 912.35), 2025-10-06 (2 days, 912.35), 2025-10-13 (2 days, 912.35), 2025-10-27 (2 days, 912.35), 2025-11-03 (2 days, 912.35), 2025-11-10 (2 days, 912.35), 2025-11-17 (2 days, 912.35), 2025-11-24 (3 days, 912.35), 2025-12-22 (2 days, 912.35), 2025-12-29 (2 days, 912.35), 2026-01-19 (2 days, 912.35), 2026-02-02 (3 days, 912.35), 2026-02-16 (2 days, 912.35), 2026-03-02 (2 days, 912.35), 2026-04-20 (2 days, 912.35), 2026-04-27 (2 days, 912.35), 2026-06-01 (2 days, 912.35), 2026-06-08 (2 days, 912.35). (Employer's split pairs Lena Ortiz with C-110.) | route-log.csv, weekly-payroll.csv | HP-2 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code (paired from application totals) | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| AC-E01 | Derek Nolan | Driver | 52,956.80 | T-610 | 52,956.80 T-610 | Van driver: route-log.csv lists AC-E01 as the driver of route AR-1 on every route day in the audit period. Drivers of vans delivering parcels and documents are CG-31. | payroll-register.csv, route-log.csv |
| AC-E02 | Maria Santos | Driver | 51,311.00 | T-610 | 51,311.00 T-610 | Van driver: route-log.csv lists AC-E02 as the driver of route AR-2 on every route day in the audit period (CG-31). | payroll-register.csv, route-log.csv |
| AC-E03 | Felix Grant | Driver | 49,618.40 | T-610 | 49,618.40 T-610 | Van driver: route-log.csv lists AC-E03 as the driver of route AR-3 on every route day in the audit period (CG-31). | payroll-register.csv, route-log.csv |
| AC-E04 | Lena Ortiz | Dispatcher | 47,442.20 | C-110 | 22,808.75 T-610<br>24,633.45 C-110 | route-log.csv: 60 ride-along days in the audit period. Pay weeks by ride days: 0 day(s) 21 week(s), 1 day(s) 6 week(s), 2 day(s) 21 week(s), 3 day(s) 4 week(s). The 25 weeks with 2 or more ride days are driver payroll under T-610 (HP-2).<br>Dispatcher in the dispatch office (field-notes.md, 2026-07-20). Dispatching by telephone or radio is CG-04. The other 27 pay weeks (no ride day or only one) stay under C-110 (HP-2). | payroll-register.csv, field-notes.md, route-log.csv, weekly-payroll.csv |
| AC-E05 | Paul Haskins | Dispatcher | 46,675.20 | C-110 | 46,675.20 C-110 | Dispatcher, seen on the radio during the visit (field-notes.md, 2026-07-20). Dispatching by telephone or radio is CG-04. route-log.csv: 2 ride-along days in the audit period. Pay weeks by ride days: 0 day(s) 50 week(s), 1 day(s) 2 week(s). No pay week has 2 or more ride days, so all pay stays under C-110 (HP-2). | payroll-register.csv, field-notes.md, route-log.csv, weekly-payroll.csv |
| AC-E06 | Irene Voss | Bookkeeper | 36,511.80 | C-110 | 36,511.80 C-110 | Bookkeeping is CG-04. The only evidence of duties is the register title; no record shows other work. | payroll-register.csv |

### Documented facts relied on

- Three van routes run six days a week; six employees, paid weekly (business-description.md)
- The owner, Gloria Rhee, has filed an election of exclusion and is not on the payroll register (business-description.md)
- The route log lists every route day with its driver and anyone riding along; pay weeks run Monday to Sunday (field-notes.md)
- On 2026-07-20, after the audit period ended, dispatcher Lena Ortiz left with the AR-2 van and came back at noon (field-notes.md)
- Weekly gross pay per employee sums to the register's wages_paid for every employee (weekly-payroll.csv, payroll-register.csv)

### Questionable records (used as written, HP-15)

Holiday entries are used as written and sent to the employer to confirm (HP-15). Each line says whether the allocation rests on the entry.

- route-log.csv records Lena Ortiz as a ride-along on 2025-12-25 (Christmas Day). Decisive: the pay week of 2025-12-22 has 2 ride days including it; without it the week has 1 and its 912.35 would stay under C-110, not T-610.
- route-log.csv records Lena Ortiz as a ride-along on 2026-01-01 (New Year's Day). Decisive: the pay week of 2025-12-29 has 2 ride days including it; without it the week has 1 and its 912.35 would stay under C-110, not T-610.

### Open items: unresolved judgements

Status of each: open. The proposed handling is applied in the figures above, the employer is asked to confirm it (see the question list), and Nadia Brennan reviews the proposal (HP-10, HP-11).

None.


## Bay Crest Exteriors

Application APP-BCE-0217, signed by Philip Crestwood. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, crew-timesheets.csv, field-notes.md, payroll-register.csv, site-signin-log.csv.

Employer's note on the application: "Most of our people coordinate jobs, order material and handle customers. Three are on the roofs."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, field-notes.md, crew-timesheets.csv, site-signin-log.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 363,970.45 | 44,812.35 | -319,158.10 |
| R-310 | CG-11 | 177,527.60 | 450,480.60 | +272,953.00 |
| R-320 | CG-12 | 0.00 | 46,205.10 | +46,205.10 |
| **Total** | | **541,498.05** | **541,498.05** | **0.00** |

Confirmed rules that decided or changed something here: HP-4, HP-13, HP-16. Governing code (field code carrying the most payroll, HP-4): R-310.

Reconciliation:

| Step | Amount (USD) |
|---|---|
| Payroll register wages | 541,498.05 |
| First-pass total (equals the sum of the codes CSV) | 541,498.05 |

### Where and why the first pass differs from the employer's split

- **C-110** -319,158.10: out: Luis Carrillo (54,880.40 reported here, now 54,880.40 R-310); Brian Tull (52,115.75 reported here, now 52,115.75 R-310); Owen Petrakis (49,607.30 reported here, now 49,607.30 R-310); Rafael Duarte (47,918.65 reported here, now 47,918.65 R-310); Jamal Whitfield (46,205.10 reported here, now 46,205.10 R-320); Teresa Lindqvist (68,430.90 reported here, now 68,430.90 R-310).
- **R-310** +272,953.00: in: Luis Carrillo (reclassified, 54,880.40); Brian Tull (reclassified, 52,115.75); Owen Petrakis (reclassified, 49,607.30); Rafael Duarte (reclassified, 47,918.65); Teresa Lindqvist (reclassified, 68,430.90).
- **R-320** +46,205.10: in: Jamal Whitfield (reclassified, 46,205.10).
- How the employer's split was compared: the application names no people; exactly one pairing of register wages reproduces its head count and payroll for every code, so 'Employer's code' shows that pairing. It explains differences only and decided no classification (HP-1).

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Luis Carrillo | Reclassified | 54,880.40 | R-310 | The records put Luis Carrillo's 54,880.40 under R-310: crew-timesheets.csv: roofing 164 days, siding 40 days, gutters 12 days. 164 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). (Employer's split pairs Luis Carrillo with C-110.) | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 2 | Brian Tull | Reclassified | 52,115.75 | R-310 | The records put Brian Tull's 52,115.75 under R-310: crew-timesheets.csv: roofing 152 days, siding 56 days, gutters 4 days. 152 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). (Employer's split pairs Brian Tull with C-110.) | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 3 | Owen Petrakis | Reclassified | 49,607.30 | R-310 | The records put Owen Petrakis's 49,607.30 under R-310: crew-timesheets.csv: siding 100 days, roofing 97 days, gutters 18 days. 97 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). (Employer's split pairs Owen Petrakis with C-110.) | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 4 | Rafael Duarte | Reclassified | 47,918.65 | R-310 | The records put Rafael Duarte's 47,918.65 under R-310: crew-timesheets.csv: siding 162 days, gutters 34 days, roofing 15 days. 15 roof day(s) in the audit period (at or above 15). This is exactly at the line: one roof day fewer would put the whole pay under R-320. At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). (Employer's split pairs Rafael Duarte with C-110.) | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 5 | Jamal Whitfield | Reclassified | 46,205.10 | R-320 | The records put Jamal Whitfield's 46,205.10 under R-320: crew-timesheets.csv: siding 171 days, gutters 34 days, roofing 9 days. 9 roof day(s) in the audit period (below 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). (Employer's split pairs Jamal Whitfield with C-110.) | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 6 | Teresa Lindqvist | Reclassified | 68,430.90 | R-310 | The records put Teresa Lindqvist's 68,430.90 under R-310: Estimator. Estimating at a desk is CG-04, but on the visit day she was measuring a house for a quote (field-notes.md, 2026-07-15), and office staff sign the site sign-in sheet when they visit a job. site-signin-log.csv shows 9 job-site days in the audit period (2025-07-24, 2025-09-02, 2025-11-17, 2025-11-26, 2025-12-25, 2026-03-04, 2026-05-26, 2026-06-03, 2026-07-01): five or more, so the whole payroll moves to the employer's governing code R-310, the field code carrying the most payroll (R-310 382,049.70, R-320 46,205.10) (HP-4). (Employer's split pairs Teresa Lindqvist with C-110.) | payroll-register.csv, field-notes.md, site-signin-log.csv | HP-1, HP-7 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code (paired from application totals) | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| BC-E01 | Darnell Price | Roof Foreman | 61,240.55 | R-310 | 61,240.55 R-310 | crew-timesheets.csv: roofing 188 days, siding 28 days, gutters 6 days. 188 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, field-notes.md, crew-timesheets.csv |
| BC-E02 | Kevin Moraes | Roofer | 58,976.20 | R-310 | 58,976.20 R-310 | crew-timesheets.csv: roofing 176 days, siding 35 days, gutters 6 days. 176 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E03 | Sam Okonjo | Roofer | 57,310.85 | R-310 | 57,310.85 R-310 | crew-timesheets.csv: roofing 201 days, siding 16 days, gutters 2 days. 201 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E04 | Luis Carrillo | Roofer | 54,880.40 | C-110 | 54,880.40 R-310 | crew-timesheets.csv: roofing 164 days, siding 40 days, gutters 12 days. 164 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E05 | Brian Tull | Roofer | 52,115.75 | C-110 | 52,115.75 R-310 | crew-timesheets.csv: roofing 152 days, siding 56 days, gutters 4 days. 152 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E06 | Owen Petrakis | Roofer | 49,607.30 | C-110 | 49,607.30 R-310 | crew-timesheets.csv: siding 100 days, roofing 97 days, gutters 18 days. 97 roof day(s) in the audit period (at or above 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E07 | Rafael Duarte | Siding Installer | 47,918.65 | C-110 | 47,918.65 R-310 | crew-timesheets.csv: siding 162 days, gutters 34 days, roofing 15 days. 15 roof day(s) in the audit period (at or above 15). This is exactly at the line: one roof day fewer would put the whole pay under R-320. At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E08 | Jamal Whitfield | Siding Installer | 46,205.10 | C-110 | 46,205.10 R-320 | crew-timesheets.csv: siding 171 days, gutters 34 days, roofing 9 days. 9 roof day(s) in the audit period (below 15). At a contractor that does both roofing and siding, a field worker with 15 or more roof days goes entirely under R-310 and one with fewer entirely under R-320; one worker's pay is never split (HP-16). | payroll-register.csv, crew-timesheets.csv |
| BC-E09 | Teresa Lindqvist | Estimator | 68,430.90 | C-110 | 68,430.90 R-310 | Estimator. Estimating at a desk is CG-04, but on the visit day she was measuring a house for a quote (field-notes.md, 2026-07-15), and office staff sign the site sign-in sheet when they visit a job. site-signin-log.csv shows 9 job-site days in the audit period (2025-07-24, 2025-09-02, 2025-11-17, 2025-11-26, 2025-12-25, 2026-03-04, 2026-05-26, 2026-06-03, 2026-07-01): five or more, so the whole payroll moves to the employer's governing code R-310, the field code carrying the most payroll (R-310 382,049.70, R-320 46,205.10) (HP-4). | payroll-register.csv, field-notes.md, site-signin-log.csv |
| BC-E10 | Nora Beckett | Bookkeeper | 44,812.35 | C-110 | 44,812.35 C-110 | Bookkeeper who works in the office (field-notes.md); bookkeeping is CG-04. No site sign-ins or timesheets for her. | payroll-register.csv, field-notes.md |

### Documented facts relied on

- Bay Crest replaces roofs and installs siding and gutters; ten employees; no subcontractors in the period (business-description.md)
- The owner, Philip Crestwood, has filed an election of exclusion and is not on the payroll register (business-description.md)
- On the visit day eight people were out on two jobs (one roof, one siding) and the estimator was measuring a house for a quote (field-notes.md)
- Crew time is recorded on the crew timesheets by job and type of work; office staff sign the site sign-in sheet when they visit a job (field-notes.md)
- crew-timesheets.csv has entries for BC-E01 to BC-E08 only, all 8-hour days (crew-timesheets.csv)

### Questionable records (used as written, HP-15)

Holiday entries are used as written and sent to the employer to confirm (HP-15). Each line says whether the allocation rests on the entry.

- crew-timesheets.csv records Darnell Price working on 2025-12-25 (Christmas Day, roofing). Not decisive: without it the code is still R-310.
- crew-timesheets.csv records Kevin Moraes working on 2025-12-25 (Christmas Day, roofing), 2026-01-01 (New Year's Day, roofing). Not decisive: without them the code is still R-310.
- crew-timesheets.csv records Sam Okonjo working on 2025-12-25 (Christmas Day, roofing), 2026-01-01 (New Year's Day, roofing). Not decisive: without them the code is still R-310.
- crew-timesheets.csv records Luis Carrillo working on 2025-12-25 (Christmas Day, siding), 2026-01-01 (New Year's Day, roofing). Not decisive: without them the code is still R-310.
- crew-timesheets.csv records Brian Tull working on 2026-01-01 (New Year's Day, siding). Not decisive: without it the code is still R-310.
- crew-timesheets.csv records Owen Petrakis working on 2025-12-25 (Christmas Day, roofing), 2026-01-01 (New Year's Day, roofing). Not decisive: without them the code is still R-310.
- crew-timesheets.csv records Rafael Duarte working on 2026-01-01 (New Year's Day, siding). Not decisive: without it the code is still R-310.
- crew-timesheets.csv records Jamal Whitfield working on 2025-12-25 (Christmas Day, roofing). Not decisive: without it the code is still R-320.
- site-signin-log.csv records Teresa Lindqvist at Arnold re-roof on 2025-12-25 (Christmas Day). Not decisive: without it Teresa Lindqvist still has 8 job-site days, five or more.

### Open items: unresolved judgements

Status of each: open. The proposed handling is applied in the figures above, the employer is asked to confirm it (see the question list), and Nadia Brennan reviews the proposal (HP-10, HP-11).

None.

### Notes on the records

- 1 sign-in row(s) in site-signin-log.csv have no employee ID (County inspector); they are not employees and were not used.


## Harbor Point Legal

Application APP-HPL-0102, signed by Catherine Harbor. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, payroll-register.csv, site-signin-log.csv.

Employer's note on the application: "All of our staff work in the office."

**Employer's split: accepted.** The records give the same codes and payroll, to the cent, as the employer reported. The decision rests on payroll-register.csv, field-notes.md, site-signin-log.csv. Open items below still need confirmation.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 425,148.16 | 425,148.16 | 0.00 |
| **Total** | | **425,148.16** | **425,148.16** | **0.00** |

Confirmed rules that decided or changed something here: HP-4. Governing code (field code carrying the most payroll, HP-4): none, no field code.

Reconciliation:

| Step | Amount (USD) |
|---|---|
| Payroll register wages | 425,148.16 |
| First-pass total (equals the sum of the codes CSV) | 425,148.16 |

### Where and why the first pass differs from the employer's split

No difference. No adjustment was needed.

### Employee by employee

| ID | Name | Position | Register wages | Employer's code (paired from application totals) | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| HP-E01 | Marcus Adeyemi | Associate Attorney | 128,400.00 | C-110 | 128,400.00 C-110 | Attorney: professional staff who work in the office are CG-04. Court and closings are not job sites, and no one does physical work outside the office (field-notes.md, 2026-07-14). | payroll-register.csv, field-notes.md |
| HP-E02 | Julia Fenwick | Associate Attorney | 121,750.00 | C-110 | 121,750.00 C-110 | Attorney: professional staff who work in the office are CG-04 (field-notes.md, 2026-07-14). | payroll-register.csv, field-notes.md |
| HP-E03 | Tomas Reyes | Paralegal | 64,212.48 | C-110 | 64,212.48 C-110 | Paralegal: professional office staff, CG-04. Field notes say no one on staff does physical work outside the office. site-signin-log.csv shows 6 job-site days (2025-09-16, 2025-10-22, 2025-12-09, 2026-01-28, 2026-03-04, 2026-04-15), five or more, but the employer has no field code, so there is no governing code to move to. | payroll-register.csv, field-notes.md, site-signin-log.csv |
| HP-E04 | Ellen Short | Legal Secretary | 51,880.16 | C-110 | 51,880.16 C-110 | Legal secretary: correspondence in the office is CG-04 (field-notes.md). | payroll-register.csv, field-notes.md |
| HP-E05 | Gwen Talbot | Office Manager | 58,905.52 | C-110 | 58,905.52 C-110 | Office manager in the office suite: CG-04 (field-notes.md). | payroll-register.csv, field-notes.md |

### Documented facts relied on

- Five-employee law office in Annapolis; no other locations, no subcontractors (business-description.md)
- The founding partner, Catherine Harbor, has filed an election of exclusion and is not on the payroll register (business-description.md)
- Attorneys appear in court and meet clients at closings, neither of which is a job site; no one on staff does physical work outside the office; no travel pay (field-notes.md)
- The payroll register agrees with the general ledger (field-notes.md)
- site-signin-log.csv records Tomas Reyes at Sallowmere Court Condominiums on six dates (site-signin-log.csv)

### Open items: unresolved judgements

Status of each: open. The proposed handling is applied in the figures above, the employer is asked to confirm it (see the question list), and Nadia Brennan reviews the proposal (HP-10, HP-11).

| # | About | Proposed handling | Why | Records | Rule / reading |
|---|---|---|---|---|---|
| 1 | Tomas Reyes | Keep all 64,212.48 of Tomas Reyes's pay under C-110. | 6 job-site days meets the five-day test (HP-4), and the rule moves the whole payroll to the field code carrying the most payroll. This employer has no payroll under any field code, so the rule has nothing to move to. Nadia has no practice for this: the rule was set up for contractors' office staff, and she asked for it to be marked as an open item for confirmation (interview 3). The days at Sallowmere Court Condominiums stay in the count as written (HP-4). Nadia confirmed that days are counted where the sign-in log shows a job-site location, and that a questionable activity stays in the count and is flagged for the employer (interview 3), so the six days count. Every code in the guide that describes field work is for a trade this firm does not carry, and the field notes say the attorneys meet clients at closings, that closings are not job sites, and that no one on staff does physical work outside the office. Why a law office keeps a site sign-in log is not explained in the file. | site-signin-log.csv, field-notes.md | HP-4, HP-10 |


## Larkspur Lane Bistro

Application APP-LL-0611, signed by Rosa Delacroix. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, gross-receipts.csv, payroll-register.csv.

Employer's note on the application: "Our catering crew works events away from the restaurant, so they go under the caterer code."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, field-notes.md, gross-receipts.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| F-710 | CG-41 | 226,431.55 | 340,725.35 | +114,293.80 |
| F-720 | CG-42 | 114,293.80 | 0.00 | -114,293.80 |
| **Total** | | **340,725.35** | **340,725.35** | **0.00** |

Confirmed rules that decided or changed something here: HP-14. Governing code (field code carrying the most payroll, HP-4): F-710.

Reconciliation:

| Step | Amount (USD) |
|---|---|
| Payroll register wages | 340,725.35 |
| First-pass total (equals the sum of the codes CSV) | 340,725.35 |

### Where and why the first pass differs from the employer's split

- **F-710** +114,293.80: in: Hannah Pryor (caterer receipts test, 46,725.55); Ivan Petrov (caterer receipts test, 38,190.40); Clara Bose (caterer receipts test, 29,377.85).
- **F-720** -114,293.80: out: Hannah Pryor (46,725.55 reported here, now 46,725.55 F-710); Ivan Petrov (38,190.40 reported here, now 38,190.40 F-710); Clara Bose (29,377.85 reported here, now 29,377.85 F-710).
- How the employer's split was compared: the application names no people; exactly one pairing of register wages reproduces its head count and payroll for every code, so 'Employer's code' shows that pairing. It explains differences only and decided no classification (HP-1).

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Hannah Pryor | Caterer receipts test | 46,725.55 | F-710 | Hannah Pryor works on the catering crew. gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14). Below 40%, so 46,725.55 goes under F-710, not F-720. (Employer's split pairs Hannah Pryor with F-720.) | gross-receipts.csv, payroll-register.csv, field-notes.md | HP-14 |
| 2 | Ivan Petrov | Caterer receipts test | 38,190.40 | F-710 | Ivan Petrov works on the catering crew. gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14). Below 40%, so 38,190.40 goes under F-710, not F-720. (Employer's split pairs Ivan Petrov with F-720.) | gross-receipts.csv, payroll-register.csv, field-notes.md | HP-14 |
| 3 | Clara Bose | Caterer receipts test | 29,377.85 | F-710 | Clara Bose works on the catering crew. gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14). Below 40%, so 29,377.85 goes under F-710, not F-720. (Employer's split pairs Clara Bose with F-720.) | gross-receipts.csv, payroll-register.csv, field-notes.md | HP-14 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code (paired from application totals) | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| LL-E01 | Anton Varga | Sous Chef | 52,310.45 | F-710 | 52,310.45 F-710 | Restaurant kitchen staff (CG-41). The field notes describe the restaurant kitchen and dining room; no record puts him on the catering crew. | payroll-register.csv, field-notes.md |
| LL-E02 | Bea Lindell | Line Cook | 41,872.30 | F-710 | 41,872.30 F-710 | Restaurant kitchen staff (CG-41). | payroll-register.csv, field-notes.md |
| LL-E03 | Omar Haddad | Line Cook | 39,640.15 | F-710 | 39,640.15 F-710 | Restaurant kitchen staff (CG-41). | payroll-register.csv, field-notes.md |
| LL-E04 | Sophie Tran | Server | 33,215.80 | F-710 | 33,215.80 F-710 | Restaurant server (CG-41). | payroll-register.csv, field-notes.md |
| LL-E05 | Will Garner | Server | 31,904.65 | F-710 | 31,904.65 F-710 | Restaurant server (CG-41). | payroll-register.csv, field-notes.md |
| LL-E06 | Jose Melendez | Dishwasher | 27,488.20 | F-710 | 27,488.20 F-710 | Restaurant dishwasher (CG-41). | payroll-register.csv, field-notes.md |
| LL-E07 | Hannah Pryor | Catering Lead | 46,725.55 | F-720 | 46,725.55 F-710 | Catering lead: prepares event food in the restaurant kitchen and serves it at the venue (field-notes.md, 2026-07-21). CG-42 covers the catering crew of an employer that also runs a restaurant. gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14). Below the test, so the catering crew stays under F-710. | payroll-register.csv, field-notes.md, gross-receipts.csv |
| LL-E08 | Ivan Petrov | Event Cook | 38,190.40 | F-720 | 38,190.40 F-710 | Catering crew member (field-notes.md): CG-42. gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14). Below the test, so the catering crew stays under F-710. | payroll-register.csv, field-notes.md, gross-receipts.csv |
| LL-E09 | Clara Bose | Event Server | 29,377.85 | F-720 | 29,377.85 F-710 | Catering crew member (field-notes.md): CG-42. gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14). Below the test, so the catering crew stays under F-710. | payroll-register.csv, field-notes.md, gross-receipts.csv |

### Documented facts relied on

- 70-seat restaurant that also caters weddings and office events at customers' venues with a small catering crew; nine employees; books kept by an outside accountant (business-description.md)
- The owner, Rosa Delacroix, has filed an election of exclusion and is not on the payroll register (business-description.md)
- The catering lead and her two crew members prepare event food in the restaurant kitchen and serve it at the venue; on quiet weeks they work restaurant shifts (field-notes.md)
- The owner's sales summary splits monthly receipts between the dining room and off-site catering (field-notes.md, gross-receipts.csv)

### Open items: unresolved judgements

Status of each: open. The proposed handling is applied in the figures above, the employer is asked to confirm it (see the question list), and Nadia Brennan reviews the proposal (HP-10, HP-11).

None.

### Notes on the records

- gross-receipts.csv: month(s) 2025-07 only partly overlap the audit period 2025-07-07 to 2026-07-05 and were counted whole (reading R14; Nadia has no rule for this, interview 3). Leaving it out gives 21.97%, on the same side of the test, so it does not change the allocation.
- Caterer receipts test: gross-receipts.csv, 2025-07 to 2026-06: off-site catering 362,410.85 of 1,647,026.05 gross receipts = 22.00% (test: 40% or more for F-720, HP-14).


## Patuxent Electric

Application APP-PE-0388, signed by Raymond Dunmore. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, payroll-register.csv, site-signin-log.csv.

Employer's note on the application: "My own salary is management and goes under the office code. Travel pay for out-of-town jobs is an expense, not wages, so it is left out."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 161,905.60 | 43,905.60 | -118,000.00 |
| E-510 | CG-21 | 306,024.85 | 372,274.85 | +66,250.00 |
| **Total** | | **467,930.45** | **416,180.45** | **-51,750.00** |

Confirmed rules that decided or changed something here: HP-3, HP-6. Governing code (field code carrying the most payroll, HP-4): E-510.

Reconciliation:

| Step | Amount (USD) |
|---|---|
| Payroll register wages | 467,930.45 |
| Raymond Dunmore: flat 63,700.00 replaces register wages 118,000.00 | -54,300.00 |
| Curtis Bell: travel allowance above the daily exclusion | +720.00 |
| Hector Ruiz: travel allowance above the daily exclusion | +720.00 |
| Aaron Weiss: travel allowance above the daily exclusion | +720.00 |
| Kyle Brandt: travel allowance above the daily exclusion | +390.00 |
| First-pass total (equals the sum of the codes CSV) | 416,180.45 |

### Where and why the first pass differs from the employer's split

- **C-110** -118,000.00: out: Raymond Dunmore (118,000.00 reported here, now 63,700.00 E-510).
- **E-510** +66,250.00: in: Raymond Dunmore (owner counted at flat amount, 63,700.00); Curtis Bell (travel allowance above the daily exclusion, 720.00); Hector Ruiz (travel allowance above the daily exclusion, 720.00); Aaron Weiss (travel allowance above the daily exclusion, 720.00); Kyle Brandt (travel allowance above the daily exclusion, 390.00).
- How the employer's split was compared: the application names no people; exactly one pairing of register wages reproduces its head count and payroll for every code, so 'Employer's code' shows that pairing. It explains differences only and decided no classification (HP-1).

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Raymond Dunmore | Owner counted at flat amount | 63,700.00 | E-510 | payroll-register.csv shows wages of 118,000.00. A working owner who does any field work is counted at 63,700.00 regardless of actual wages, under the employer's trade code E-510 (difference -54,300.00). (Employer's split pairs Raymond Dunmore with C-110.) | payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md | HP-3 |
| 2 | Curtis Bell | Travel allowance above the daily exclusion | 720.00 | E-510 | 2,600.00 paid for 40 recorded travel days. Up to 47.00 per day (1,880.00) is left out; the remaining 720.00 is payroll under E-510. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |
| 3 | Hector Ruiz | Travel allowance above the daily exclusion | 720.00 | E-510 | 2,600.00 paid for 40 recorded travel days. Up to 47.00 per day (1,880.00) is left out; the remaining 720.00 is payroll under E-510. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |
| 4 | Aaron Weiss | Travel allowance above the daily exclusion | 720.00 | E-510 | 2,600.00 paid for 40 recorded travel days. Up to 47.00 per day (1,880.00) is left out; the remaining 720.00 is payroll under E-510. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |
| 5 | Kyle Brandt | Travel allowance above the daily exclusion | 390.00 | E-510 | 390.00 paid for 0 recorded travel days. Up to 47.00 per day (0.00) is left out; the remaining 390.00 is payroll under E-510. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6, R6 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code (paired from application totals) | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| PE-E01 | Raymond Dunmore | Owner, Master Electrician | 118,000.00 | C-110 | 63,700.00 E-510 | Working owner who does field work (has not filed an election of exclusion (business-description.md); leads a crew on site most days and pulls wire (field-notes.md); site-signin-log.csv shows sign-ins on 214 days: 160 at Solomons, Lexington Park and Huntingtown, and 54 at Prince Frederick, the town where the shop and office are (field-notes.md)). Counted at the flat 63,700.00, regardless of actual wages, under the employer's trade code E-510 (HP-3). | payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md |
| PE-E02 | Curtis Bell | Journeyman Electrician | 72,410.35 | E-510 | 72,410.35 E-510<br>720.00 E-510 | Electrician on residential, light commercial and out-of-town wiring jobs (business-description.md, field-notes.md): CG-21.<br>Daily allowance above 47.00 per day: 2,600.00 paid for 40 travel days, 1,880.00 left out (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E03 | Hector Ruiz | Journeyman Electrician | 69,855.90 | E-510 | 69,855.90 E-510<br>720.00 E-510 | Electrician (business-description.md, field-notes.md): CG-21.<br>Daily allowance above 47.00 per day: 2,600.00 paid for 40 travel days, 1,880.00 left out (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E04 | Aaron Weiss | Journeyman Electrician | 64,120.65 | E-510 | 64,120.65 E-510<br>720.00 E-510 | Electrician (business-description.md, field-notes.md): CG-21.<br>Daily allowance above 47.00 per day: 2,600.00 paid for 40 travel days, 1,880.00 left out (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E05 | Tyrone Banks | Electrician | 58,377.20 | E-510 | 58,377.20 E-510 | Electrician (business-description.md, field-notes.md): CG-21. | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E06 | Kyle Brandt | Apprentice Electrician | 41,260.75 | E-510 | 41,260.75 E-510<br>390.00 E-510 | Apprentice electrician on the wiring crew (business-description.md): CG-21.<br>Daily allowance above 47.00 per day: 390.00 paid for 0 travel days, 0.00 left out (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E07 | Linda Marsh | Office Administrator | 43,905.60 | C-110 | 43,905.60 C-110 | Runs the office and never goes to jobs (field-notes.md, 2026-07-17); no entries in site-signin-log.csv. CG-04. | payroll-register.csv, field-notes.md |

### Documented facts relied on

- Seven people on the payroll register, including the owner, Raymond Dunmore, who has not filed an election of exclusion; no subcontractors in the period (business-description.md)
- The owner leads a crew on site most days and pulls wire himself; the office administrator never goes to jobs (field-notes.md)
- site-signin-log.csv has sign-ins on 214 days, all for Raymond Dunmore: Solomons 60, Lexington Park 52, Huntingtown 48, Prince Frederick 54. The shop and office are in Prince Frederick (field-notes.md), so those 54 may not all be job sites; the 160 elsewhere and the field notes are enough to show field work (site-signin-log.csv)
- Electricians on the Hagerstown job were paid a flat amount per day away on top of wages, in its own register column (field-notes.md, payroll-register.csv)

### Open items: unresolved judgements

Status of each: open. The proposed handling is applied in the figures above, the employer is asked to confirm it (see the question list), and Nadia Brennan reviews the proposal (HP-10, HP-11).

| # | About | Proposed handling | Why | Records | Rule / reading |
|---|---|---|---|---|---|
| 1 | Kyle Brandt | Allocated as practice stands: all 390.00 of the allowance is payroll under E-510. Proposed handling for Nadia to confirm: the register's daily rates are Curtis Bell, Hector Ruiz, Aaron Weiss 65.00 per day; Tyrone Banks 47.00 per day. 390.00 is exactly 6 days at 65.00 and not a whole number of days at any other rate, so it looks like 6 out-of-town days that were not entered. If the employer confirms 6 travel days, 282.00 (6 x 47.00) is left out and 108.00 is payroll under E-510. If it was a documented expense reimbursement, none of it is payroll (CG-03). | payroll-register.csv records an allowance but no travel days. Nadia has no practice for this and asked for it to be allocated under her practice and the guide as they stand, with a written proposal for her to confirm (interviews 2 and 3). HP-6 leaves out up to 47.00 per travel day, so with no recorded day nothing qualifies, and the amount is payroll (reading R6). | payroll-register.csv | HP-6, R6, CG-03 |


## Severn Homebuilders

Application APP-SH-0417, signed by Martin Severn. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, insurance-certificates.csv, payroll-register.csv, site-signin-log.csv, subcontractor-payments.csv.

Employer's note on the application: "Three office staff. All of our subcontractors carry their own insurance."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, business-description.md, field-notes.md, site-signin-log.csv, subcontractor-payments.csv, insurance-certificates.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 177,209.40 | 117,368.70 | -59,840.70 |
| H-420 | CG-15 | 284,670.30 | 369,204.39 | +84,534.09 |
| R-310 | CG-11 | 0.00 | 27,567.39 | +27,567.39 |
| **Total** | | **461,879.70** | **514,140.48** | **+52,260.78** |

Confirmed rules that decided or changed something here: HP-4, HP-5. Governing code (field code carrying the most payroll, HP-4): H-420.

Reconciliation:

| Step | Amount (USD) |
|---|---|
| Payroll register wages | 461,879.70 |
| Kent Island Roofing, invoice SV-KEN-01: uninsured subcontractor payment added | +8,580.00 |
| Kent Island Roofing, invoice SV-KEN-02: uninsured subcontractor payment added | +11,928.27 |
| Kent Island Roofing, invoice SV-KEN-03: uninsured subcontractor payment added | +7,059.12 |
| Tidewater Drywall, invoice SV-TID-01: uninsured subcontractor payment added | +10,944.33 |
| Tidewater Drywall, invoice SV-TID-02: uninsured subcontractor payment added | +13,749.06 |
| First-pass total (equals the sum of the codes CSV) | 514,140.48 |

### Where and why the first pass differs from the employer's split

- **C-110** -59,840.70: out: Dana Whitcomb (59,840.70 reported here, now 59,840.70 H-420).
- **H-420** +84,534.09: in: Tidewater Drywall, invoice SV-TID-01 (uninsured subcontractor payment added, 10,944.33); Tidewater Drywall, invoice SV-TID-02 (uninsured subcontractor payment added, 13,749.06); Dana Whitcomb (reclassified, 59,840.70).
- **R-310** +27,567.39: in: Kent Island Roofing, invoice SV-KEN-01 (uninsured subcontractor payment added, 8,580.00); Kent Island Roofing, invoice SV-KEN-02 (uninsured subcontractor payment added, 11,928.27); Kent Island Roofing, invoice SV-KEN-03 (uninsured subcontractor payment added, 7,059.12).
- How the employer's split was compared: the application names no people; exactly one pairing of register wages reproduces its head count and payroll for every code, so 'Employer's code' shows that pairing. It explains differences only and decided no classification (HP-1).

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Kent Island Roofing, invoice SV-KEN-01 | Uninsured subcontractor payment added | 8,580.00 | R-310 | 14,300.00 paid on 2025-09-12 for roofing. Because the certificate in the file (MD-WC-517736, 2025-04-01 to 2026-01-31) does not cover the whole audit period 2025-07-07 to 2026-07-05, and a certificate that lapses partway through counts as no certificate, also for payments made while it was in force, 60% (8,580.00) is added to payroll under R-310, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 2 | Kent Island Roofing, invoice SV-KEN-02 | Uninsured subcontractor payment added | 11,928.27 | R-310 | 19,880.45 paid on 2026-03-20 for roofing. Because the certificate in the file (MD-WC-517736, 2025-04-01 to 2026-01-31) does not cover the whole audit period 2025-07-07 to 2026-07-05, and a certificate that lapses partway through counts as no certificate, also for payments made while it was in force, 60% (11,928.27) is added to payroll under R-310, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 3 | Kent Island Roofing, invoice SV-KEN-03 | Uninsured subcontractor payment added | 7,059.12 | R-310 | 11,765.20 paid on 2026-05-08 for roofing. Because the certificate in the file (MD-WC-517736, 2025-04-01 to 2026-01-31) does not cover the whole audit period 2025-07-07 to 2026-07-05, and a certificate that lapses partway through counts as no certificate, also for payments made while it was in force, 60% (7,059.12) is added to payroll under R-310, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 4 | Tidewater Drywall, invoice SV-TID-01 | Uninsured subcontractor payment added | 10,944.33 | H-420 | 18,240.55 paid on 2025-10-03 for drywall. Because no certificate of insurance for this subcontractor is in the file, 60% (10,944.33) is added to payroll under H-420, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 5 | Tidewater Drywall, invoice SV-TID-02 | Uninsured subcontractor payment added | 13,749.06 | H-420 | 22,915.10 paid on 2026-02-27 for drywall. Because no certificate of insurance for this subcontractor is in the file, 60% (13,749.06) is added to payroll under H-420, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 6 | Dana Whitcomb | Reclassified | 59,840.70 | H-420 | The records put Dana Whitcomb's 59,840.70 under H-420: Office manager who drives material and paperwork out to the sites and meets inspectors there (field-notes.md, 2026-07-16). site-signin-log.csv shows 11 job-site days in the audit period (2025-09-17, 2025-09-19, 2025-10-02, 2025-10-17, 2025-11-14, 2026-01-08, 2026-01-14, 2026-01-16, 2026-03-04, 2026-06-16, 2026-06-23): five or more, so the whole payroll moves to the employer's governing code H-420, the field code carrying the most payroll (H-420 284,670.30) (HP-4). (Employer's split pairs Dana Whitcomb with C-110.) | payroll-register.csv, field-notes.md, site-signin-log.csv | HP-1, HP-7 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code (paired from application totals) | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| SH-E01 | Garrett Holm | Lead Carpenter | 66,315.40 | H-420 | 66,315.40 H-420 | Own crew doing framing, drywall, finish carpentry and site labor on single-family houses (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E02 | Victor Amadi | Carpenter | 62,780.15 | H-420 | 62,780.15 H-420 | Crew carpenter on house construction (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E03 | Peter Kowal | Carpenter | 58,442.60 | H-420 | 58,442.60 H-420 | Crew carpenter on house construction (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E04 | Andre Sutton | Laborer | 49,905.85 | H-420 | 49,905.85 H-420 | General labor at the building site (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E05 | Colin Rusk | Laborer | 47,226.30 | H-420 | 47,226.30 H-420 | General labor at the building site (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E06 | Marissa Gale | Estimator | 71,250.45 | C-110 | 71,250.45 C-110 | Estimator who visits a site now and then to measure (field-notes.md, 2026-07-16). Estimating at a desk is CG-04. site-signin-log.csv shows 4 job-site day(s) in the audit period (2025-07-24, 2026-01-16, 2026-03-24, 2026-04-21), fewer than 5, so the person stays C-110 (HP-4). | payroll-register.csv, field-notes.md, site-signin-log.csv |
| SH-E07 | Dana Whitcomb | Office Manager | 59,840.70 | C-110 | 59,840.70 H-420 | Office manager who drives material and paperwork out to the sites and meets inspectors there (field-notes.md, 2026-07-16). site-signin-log.csv shows 11 job-site days in the audit period (2025-09-17, 2025-09-19, 2025-10-02, 2025-10-17, 2025-11-14, 2026-01-08, 2026-01-14, 2026-01-16, 2026-03-04, 2026-06-16, 2026-06-23): five or more, so the whole payroll moves to the employer's governing code H-420, the field code carrying the most payroll (H-420 284,670.30) (HP-4). | payroll-register.csv, field-notes.md, site-signin-log.csv |
| SH-E08 | Helen Ostrow | Bookkeeper | 46,118.25 | C-110 | 46,118.25 C-110 | Bookkeeper who stays in the office (field-notes.md): CG-04. | payroll-register.csv, field-notes.md |

Subcontractor payroll added:

- 8,580.00 R-310: 60% of 14,300.00 paid to uninsured subcontractor Kent Island Roofing (invoice SV-KEN-01, 2025-09-12, roofing) (HP-5, CG-06).
- 11,928.27 R-310: 60% of 19,880.45 paid to uninsured subcontractor Kent Island Roofing (invoice SV-KEN-02, 2026-03-20, roofing) (HP-5, CG-06).
- 7,059.12 R-310: 60% of 11,765.20 paid to uninsured subcontractor Kent Island Roofing (invoice SV-KEN-03, 2026-05-08, roofing) (HP-5, CG-06).
- 10,944.33 H-420: 60% of 18,240.55 paid to uninsured subcontractor Tidewater Drywall (invoice SV-TID-01, 2025-10-03, drywall) (HP-5, CG-06).
- 13,749.06 H-420: 60% of 22,915.10 paid to uninsured subcontractor Tidewater Drywall (invoice SV-TID-02, 2026-02-27, drywall) (HP-5, CG-06).

### Documented facts relied on

- Severn builds single-family houses with its own crew for framing, drywall, finish carpentry and site labor, and uses subcontractors for some trades; eight employees (business-description.md)
- The owner, Martin Severn, has filed an election of exclusion and is not on the payroll register (business-description.md)
- Three houses were under construction; the office manager drives material and paperwork out to the sites and meets inspectors; the estimator visits a site now and then; the bookkeeper stays in the office (field-notes.md)
- Three subcontractors were paid in the period (framing, drywall, roofing); the certificates collected are the ones the owner could find (field-notes.md)
- The file holds certificates for Tenbury Ridge Framing Co. (MD-WC-448201, 2025-06-01 to 2026-12-31) and Kent Island Roofing & Siding LLC (MD-WC-517736, 2025-04-01 to 2026-01-31); none for Tidewater Drywall (insurance-certificates.csv)

### Open items: unresolved judgements

Status of each: open. The proposed handling is applied in the figures above, the employer is asked to confirm it (see the question list), and Nadia Brennan reviews the proposal (HP-10, HP-11).

| # | About | Proposed handling | Why | Records | Rule / reading |
|---|---|---|---|---|---|
| 1 | Kent Island Roofing | Treat the certificate issued to 'Kent Island Roofing & Siding LLC' as Kent Island Roofing's, for the record only. | subcontractor-payments.csv pays 'Kent Island Roofing', but the certificate in insurance-certificates.csv is issued to 'Kent Island Roofing & Siding LLC'. Nadia has no practice for a name that differs (interview 2). It does not change the allocation: that certificate does not cover the whole audit period, and a certificate that lapses partway through counts as no certificate (HP-5), so the payments are added whichever business it belongs to. The name matters only if the employer sends a further certificate in that name. | subcontractor-payments.csv, insurance-certificates.csv | HP-10 |

### Notes on the records

- 1 sign-in row(s) in site-signin-log.csv have no employee ID (County inspector); they are not employees and were not used.
- Tenbury Ridge Framing Co.: certificate MD-WC-448201 covers the whole audit period (2025-07-07 to 2026-07-05); 3 payment(s) not added to payroll (HP-5).
- Kent Island Roofing: the certificate in the file (MD-WC-517736, 2025-04-01 to 2026-01-31) does not cover the whole audit period 2025-07-07 to 2026-07-05, and a certificate that lapses partway through counts as no certificate, also for payments made while it was in force; all 3 payment(s) added at 60% (HP-5).
- Tidewater Drywall: no certificate of insurance for this subcontractor is in the file; all 2 payment(s) added at 60% (HP-5).
