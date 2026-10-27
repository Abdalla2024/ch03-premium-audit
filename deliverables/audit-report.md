# Premium audit first pass: class codes and payroll allocation

Prepared by the class-code-assistant Skill as a **first pass for review by Nadia Brennan, Senior Premium Auditor**. It is not audit work until she has reviewed it (house practice HP-11). It classifies and allocates payroll only; it does not set rates or quote premium.

- Classification rules: Linden Shore Mutual classification guide excerpt, edition of July 2025, sha256 `89480f691737`, read from https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view.
- Employer files read from https://drive.google.com/drive/folders/1pt8gzX8HDuaAq6g8ZFeQ66zbVIYdlN_n at 2026-10-27T01:34:45+00:00.
- House practice: the audit team's unwritten rules from interview 1, labelled HP-1 to HP-12 in `skills/class-code-assistant/references/house-practice.md`. Readings A1 to A6 in the same file are this Skill's interpretations; every place one changes an allocation is listed as an open item.
- **Facts** below are cited to the employer record they come from. **Open items** are proposals for gray areas: each says how the first pass treated the case and why, and needs Nadia's confirmation.

## Which two employers to call first

The order ranks employers by how far the first pass is from the employer's own split. The measure is the sum of the absolute per-code differences, in dollars of payroll (not premium); payroll moved from one code to another counts once out and once in. Ties go to the employer with more open items. This ranking rule is the Skill's own proposal: the auditor has not said how she wants calls prioritised (open item).

| Order | Employer | Sum of per-code differences | Employer reported | First pass | Open items | Employer questions |
|---|---|---|---|---|---|---|
| 1 | Bay Crest Exteriors | 638,316.20 | 541,498.05 | 541,498.05 | 5 | 14 |
| 2 | Patuxent Electric | 184,250.00 | 467,930.45 | 416,180.45 | 2 | 9 |
| 3 | Severn Homebuilders | 163,362.18 | 461,879.70 | 505,560.48 | 3 | 8 |
| 4 | Annapolis Courier | 60,156.10 | 284,515.40 | 284,515.40 | 2 | 6 |
| 5 | Larkspur Lane Bistro | 0.00 | 340,725.35 | 340,725.35 | 2 | 4 |
| 6 | Harbor Point Legal | 0.00 | 425,148.16 | 425,148.16 | 1 | 4 |

1. **Bay Crest Exteriors**: per-code differences total 638,316.20 (net 0.00). The largest drivers are Teresa Lindqvist: reclassified (68,430.90 under R-310); Luis Carrillo: reclassified (54,880.40 under R-310); Brian Tull: reclassified (52,115.75 under R-310). 5 open item(s) depend on the employer's confirmation.
2. **Patuxent Electric**: per-code differences total 184,250.00 (net -51,750.00). The largest drivers are Raymond Dunmore: owner counted at flat amount (63,700.00 under E-510); Curtis Bell: travel allowance above the daily exclusion (720.00 under E-510); Hector Ruiz: travel allowance above the daily exclusion (720.00 under E-510). 2 open item(s) depend on the employer's confirmation.

## Summary

| Employer | Employer's split | Decision rests on |
|---|---|---|
| Annapolis Courier | Not accepted | payroll-register.csv, route-log.csv, field-notes.md, weekly-payroll.csv |
| Bay Crest Exteriors | Not accepted | payroll-register.csv, field-notes.md, crew-timesheets.csv, site-signin-log.csv |
| Harbor Point Legal | Accepted | payroll-register.csv, field-notes.md, site-signin-log.csv |
| Larkspur Lane Bistro | Accepted | payroll-register.csv, field-notes.md |
| Patuxent Electric | Not accepted | payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md |
| Severn Homebuilders | Not accepted | payroll-register.csv, business-description.md, field-notes.md, site-signin-log.csv, subcontractor-payments.csv, insurance-certificates.csv |

## Annapolis Courier

Application APP-AC-0529, signed by Gloria Rhee. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, payroll-register.csv, route-log.csv, weekly-payroll.csv.

Employer's note on the application: "Our dispatchers work the phones. Lena rides along about two days a week to train new stops, so at most two fifths of her time is on the road."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, route-log.csv, field-notes.md, weekly-payroll.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 130,629.20 | 100,551.15 | -30,078.05 |
| T-610 | CG-31 | 153,886.20 | 183,964.25 | +30,078.05 |
| **Total** | | **284,515.40** | **284,515.40** | **0.00** |

### Where and why the first pass differs from the employer's split

- **C-110** -30,078.05: out: Lena Ortiz (47,442.20 reported here, now 28,282.85 T-610, 19,159.35 C-110); Paul Haskins (46,675.20 reported here, now 1,795.20 T-610, 44,880.00 C-110).
- **T-610** +30,078.05: in: Lena Ortiz (whole-week route split, 28,282.85); Paul Haskins (whole-week route split, 1,795.20).
- How the employer's split was compared: the employer's per-person codes are inferred: exactly one assignment of the register's wages reproduces its reported head count and payroll for every code.

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Lena Ortiz | Whole-week route split | 28,282.85 | T-610 | 60 ride-along days (2025-07-10 to 2026-06-12) fall in 31 of 52 pay weeks. Those weeks' gross pay of 28,282.85 moves from C-110 to T-610. The employer reported Lena Ortiz under C-110. | route-log.csv, weekly-payroll.csv | HP-2 |
| 2 | Paul Haskins | Whole-week route split | 1,795.20 | T-610 | 2 ride-along days (2025-12-03 to 2026-03-26) fall in 2 of 52 pay weeks. Those weeks' gross pay of 1,795.20 moves from C-110 to T-610. The employer reported Paul Haskins under C-110. | route-log.csv, weekly-payroll.csv | HP-2 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| AC-E01 | Derek Nolan | Driver | 52,956.80 | T-610 | 52,956.80 T-610 | Van driver: route-log.csv lists AC-E01 as the driver of route AR-1 on every route day in the audit period. Drivers of vans delivering parcels and documents are CG-31. | payroll-register.csv, route-log.csv |
| AC-E02 | Maria Santos | Driver | 51,311.00 | T-610 | 51,311.00 T-610 | Van driver: route-log.csv lists AC-E02 as the driver of route AR-2 on every route day in the audit period (CG-31). | payroll-register.csv, route-log.csv |
| AC-E03 | Felix Grant | Driver | 49,618.40 | T-610 | 49,618.40 T-610 | Van driver: route-log.csv lists AC-E03 as the driver of route AR-3 on every route day in the audit period (CG-31). | payroll-register.csv, route-log.csv |
| AC-E04 | Lena Ortiz | Dispatcher | 47,442.20 | C-110 | 28,282.85 T-610<br>19,159.35 C-110 | route-log.csv shows 60 ride-along days in 31 pay weeks. Those whole weeks' pay goes to T-610 (HP-2, reading A1).<br>Dispatcher in the dispatch office (field-notes.md, 2026-07-20). Dispatching by telephone or radio is CG-04. The other 21 pay weeks stay under C-110. | payroll-register.csv, field-notes.md, route-log.csv, weekly-payroll.csv |
| AC-E05 | Paul Haskins | Dispatcher | 46,675.20 | C-110 | 1,795.20 T-610<br>44,880.00 C-110 | route-log.csv shows 2 ride-along days in 2 pay weeks. Those whole weeks' pay goes to T-610 (HP-2, reading A1).<br>Dispatcher, seen on the radio during the visit (field-notes.md, 2026-07-20). Dispatching by telephone or radio is CG-04. The other 50 pay weeks stay under C-110. | payroll-register.csv, field-notes.md, route-log.csv, weekly-payroll.csv |
| AC-E06 | Irene Voss | Bookkeeper | 36,511.80 | C-110 | 36,511.80 C-110 | Bookkeeping is CG-04. The only evidence of duties is the register title; no record shows other work. | payroll-register.csv |

### Documented facts relied on

- Three van routes run six days a week; six employees, paid weekly (business-description.md)
- The owner, Gloria Rhee, has filed an election of exclusion and is not on the payroll register (business-description.md)
- The route log lists every route day with its driver and anyone riding along; pay weeks run Monday to Sunday (field-notes.md)
- On 2026-07-20, after the audit period ended, dispatcher Lena Ortiz left with the AR-2 van and came back at noon (field-notes.md)
- Weekly gross pay per employee sums to the register's wages_paid for every employee (weekly-payroll.csv, payroll-register.csv)

### Open items for Nadia Brennan to confirm

| # | About | Proposed handling | Why | Records |
|---|---|---|---|---|
| 1 | Reading of 'split the pay by whole weeks' | Any pay week with at least one ride-along day goes wholly to the route code (reading A1). | A narrower reading, counting only weeks spent wholly on the road, would move less payroll. Lena Ortiz: 60 ride days in 31 of 52 weeks, 28,282.85 moved; Paul Haskins: 2 ride days in 2 of 52 weeks, 1,795.20 moved. | route-log.csv, weekly-payroll.csv |
| 2 | Employer's statement about dispatcher ride-alongs | Use the route log, not the application's note, for the ride-along weeks. | The application says the dispatchers work the phones and that Lena 'rides along about two days a week ... at most two fifths of her time'. route-log.csv records 60 ride-along days for Lena Ortiz and 2 for Paul Haskins in the audit period, so the note understates Paul's road time and does not match Lena's pattern. The records decide (HP-7). | application.md, route-log.csv |


## Bay Crest Exteriors

Application APP-BCE-0217, signed by Philip Crestwood. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, crew-timesheets.csv, field-notes.md, payroll-register.csv, site-signin-log.csv.

Employer's note on the application: "Most of our people coordinate jobs, order material and handle customers. Three are on the roofs."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, field-notes.md, crew-timesheets.csv, site-signin-log.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 363,970.45 | 44,812.35 | -319,158.10 |
| R-310 | CG-11 | 177,527.60 | 352,954.65 | +175,427.05 |
| R-320 | CG-12 | 0.00 | 143,731.05 | +143,731.05 |
| **Total** | | **541,498.05** | **541,498.05** | **0.00** |

### Where and why the first pass differs from the employer's split

- **C-110** -319,158.10: out: Luis Carrillo (54,880.40 reported here, now 54,880.40 R-310); Brian Tull (52,115.75 reported here, now 52,115.75 R-310); Owen Petrakis (49,607.30 reported here, now 49,607.30 R-320); Rafael Duarte (47,918.65 reported here, now 47,918.65 R-320); Jamal Whitfield (46,205.10 reported here, now 46,205.10 R-320); Teresa Lindqvist (68,430.90 reported here, now 68,430.90 R-310).
- **R-310** +175,427.05: in: Luis Carrillo (reclassified, 54,880.40); Brian Tull (reclassified, 52,115.75); Teresa Lindqvist (reclassified, 68,430.90).
- **R-320** +143,731.05: in: Owen Petrakis (reclassified, 49,607.30); Rafael Duarte (reclassified, 47,918.65); Jamal Whitfield (reclassified, 46,205.10).
- How the employer's split was compared: the employer's per-person codes are inferred: exactly one assignment of the register's wages reproduces its reported head count and payroll for every code.

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Luis Carrillo | Reclassified | 54,880.40 | R-310 | The employer reported Luis Carrillo (Roofer) under C-110. The records put the 54,880.40 under R-310: Crew timesheets: roofing 1312.0 h, siding 320.0 h, gutters 96.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 2 | Brian Tull | Reclassified | 52,115.75 | R-310 | The employer reported Brian Tull (Roofer) under C-110. The records put the 52,115.75 under R-310: Crew timesheets: roofing 1216.0 h, siding 448.0 h, gutters 32.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 3 | Owen Petrakis | Reclassified | 49,607.30 | R-320 | The employer reported Owen Petrakis (Roofer) under C-110. The records put the 49,607.30 under R-320: Crew timesheets: siding 800.0 h, roofing 776.0 h, gutters 144.0 h. The whole of the pay goes to R-320, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 4 | Rafael Duarte | Reclassified | 47,918.65 | R-320 | The employer reported Rafael Duarte (Siding Installer) under C-110. The records put the 47,918.65 under R-320: Crew timesheets: siding 1296.0 h, gutters 272.0 h, roofing 120.0 h. The whole of the pay goes to R-320, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 5 | Jamal Whitfield | Reclassified | 46,205.10 | R-320 | The employer reported Jamal Whitfield (Siding Installer) under C-110. The records put the 46,205.10 under R-320: Crew timesheets: siding 1368.0 h, gutters 272.0 h, roofing 72.0 h. The whole of the pay goes to R-320, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv | HP-1, HP-7 |
| 6 | Teresa Lindqvist | Reclassified | 68,430.90 | R-310 | The employer reported Teresa Lindqvist (Estimator) under C-110. The records put the 68,430.90 under R-310: Estimator. Estimating at a desk is CG-04, but on the visit day she was measuring a house for a quote (field-notes.md, 2026-07-15), and office staff sign the site sign-in sheet when they visit a job. site-signin-log.csv shows 9 job-site days (2025-07-24, 2025-09-02, 2025-11-17, 2025-11-26, 2025-12-25, 2026-03-04, 2026-05-26, 2026-06-03, 2026-07-01), so the person is not clerical (HP-4: 5 or more days). Days by site code: R-310 5 day(s), R-320 4 day(s). The person is reported under R-310 (reading A3). | payroll-register.csv, field-notes.md, site-signin-log.csv | HP-1, HP-7 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| BC-E01 | Darnell Price | Roof Foreman | 61,240.55 | R-310 | 61,240.55 R-310 | Crew timesheets: roofing 1504.0 h, siding 224.0 h, gutters 48.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, field-notes.md, crew-timesheets.csv |
| BC-E02 | Kevin Moraes | Roofer | 58,976.20 | R-310 | 58,976.20 R-310 | Crew timesheets: roofing 1408.0 h, siding 280.0 h, gutters 48.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E03 | Sam Okonjo | Roofer | 57,310.85 | R-310 | 57,310.85 R-310 | Crew timesheets: roofing 1608.0 h, siding 128.0 h, gutters 16.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E04 | Luis Carrillo | Roofer | 54,880.40 | C-110 | 54,880.40 R-310 | Crew timesheets: roofing 1312.0 h, siding 320.0 h, gutters 96.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E05 | Brian Tull | Roofer | 52,115.75 | C-110 | 52,115.75 R-310 | Crew timesheets: roofing 1216.0 h, siding 448.0 h, gutters 32.0 h. The whole of the pay goes to R-310, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E06 | Owen Petrakis | Roofer | 49,607.30 | C-110 | 49,607.30 R-320 | Crew timesheets: siding 800.0 h, roofing 776.0 h, gutters 144.0 h. The whole of the pay goes to R-320, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E07 | Rafael Duarte | Siding Installer | 47,918.65 | C-110 | 47,918.65 R-320 | Crew timesheets: siding 1296.0 h, gutters 272.0 h, roofing 120.0 h. The whole of the pay goes to R-320, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E08 | Jamal Whitfield | Siding Installer | 46,205.10 | C-110 | 46,205.10 R-320 | Crew timesheets: siding 1368.0 h, gutters 272.0 h, roofing 72.0 h. The whole of the pay goes to R-320, the code with the most recorded hours (HP-2: one person's pay is not split; reading A2). | payroll-register.csv, crew-timesheets.csv |
| BC-E09 | Teresa Lindqvist | Estimator | 68,430.90 | C-110 | 68,430.90 R-310 | Estimator. Estimating at a desk is CG-04, but on the visit day she was measuring a house for a quote (field-notes.md, 2026-07-15), and office staff sign the site sign-in sheet when they visit a job. site-signin-log.csv shows 9 job-site days (2025-07-24, 2025-09-02, 2025-11-17, 2025-11-26, 2025-12-25, 2026-03-04, 2026-05-26, 2026-06-03, 2026-07-01), so the person is not clerical (HP-4: 5 or more days). Days by site code: R-310 5 day(s), R-320 4 day(s). The person is reported under R-310 (reading A3). | payroll-register.csv, field-notes.md, site-signin-log.csv |
| BC-E10 | Nora Beckett | Bookkeeper | 44,812.35 | C-110 | 44,812.35 C-110 | Bookkeeper who works in the office (field-notes.md); bookkeeping is CG-04. No site sign-ins or timesheets for her. | payroll-register.csv, field-notes.md |

### Documented facts relied on

- Bay Crest replaces roofs and installs siding and gutters; ten employees; no subcontractors in the period (business-description.md)
- The owner, Philip Crestwood, has filed an election of exclusion and is not on the payroll register (business-description.md)
- On the visit day eight people were out on two jobs (one roof, one siding) and the estimator was measuring a house for a quote (field-notes.md)
- Crew time is recorded on the crew timesheets by job and type of work; office staff sign the site sign-in sheet when they visit a job (field-notes.md)
- crew-timesheets.csv has entries for BC-E01 to BC-E08 only, all 8-hour days (crew-timesheets.csv)

### Open items for Nadia Brennan to confirm

| # | About | Proposed handling | Why | Records |
|---|---|---|---|---|
| 1 | Teresa Lindqvist: sign-in on 2025-12-25 | Count the day as recorded, because the records decide (HP-7). | site-signin-log.csv records Teresa Lindqvist at Arnold re-roof on Christmas Day. This may be a recording error. | site-signin-log.csv |
| 2 | Teresa Lindqvist | Report all 68,430.90 of Teresa Lindqvist's pay under R-310 instead of C-110. | 9 job-site days is at or above the 5-day threshold (HP-4). House practice does not say which code replaces C-110. R-310 is the code of the work at the sites visited (R-310 5 day(s), R-320 4 day(s)). | site-signin-log.csv, field-notes.md |
| 3 | Crew members with more than one type of work | Report each person's whole pay under the code with the most recorded hours. | CG-07 allows a division when time records are kept, but house practice is that one person's pay is not split, except for route ride-alongs (HP-2). House practice does not say which single code to use. Hours by code: Darnell Price: R-310 1504.0 h, R-320 272.0 h -> R-310; Kevin Moraes: R-310 1408.0 h, R-320 328.0 h -> R-310; Sam Okonjo: R-310 1608.0 h, R-320 144.0 h -> R-310; Luis Carrillo: R-310 1312.0 h, R-320 416.0 h -> R-310; Brian Tull: R-310 1216.0 h, R-320 480.0 h -> R-310; Owen Petrakis: R-320 944.0 h, R-310 776.0 h -> R-320; Rafael Duarte: R-320 1568.0 h, R-310 120.0 h -> R-320; Jamal Whitfield: R-320 1640.0 h, R-310 72.0 h -> R-320. | crew-timesheets.csv |
| 4 | Employer's split leans to the clerical code | Allocate from crew-timesheets.csv and site-signin-log.csv, not from the application. | The application puts 7 of 10 employees under C-110 and says most people coordinate jobs. The timesheets record eight crew members working roofing, siding and gutters every working day, and the field notes saw eight people out on two jobs. The records decide (HP-7). | application.md, crew-timesheets.csv, field-notes.md |
| 5 | Teresa Lindqvist: site work types read from site names | Treat 're-roof' sites as R-310 work and 'siding' sites as R-320 work. | site-signin-log.csv gives only site names. The work done at each site is read from the name; no record links the sign-in sites to timesheet job IDs. Her code depends on this: 5 re-roof days against 4 siding days, and one of the re-roof days is 2025-12-25. | site-signin-log.csv |

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

### Where and why the first pass differs from the employer's split

No difference. No adjustment was needed.

### Employee by employee

| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| HP-E01 | Marcus Adeyemi | Associate Attorney | 128,400.00 | C-110 | 128,400.00 C-110 | Attorney: professional staff who work in the office are CG-04. Court and closings are not job sites, and no one does physical work outside the office (field-notes.md, 2026-07-14). | payroll-register.csv, field-notes.md |
| HP-E02 | Julia Fenwick | Associate Attorney | 121,750.00 | C-110 | 121,750.00 C-110 | Attorney: professional staff who work in the office are CG-04 (field-notes.md, 2026-07-14). | payroll-register.csv, field-notes.md |
| HP-E03 | Tomas Reyes | Paralegal | 64,212.48 | C-110 | 64,212.48 C-110 | Paralegal: professional office staff, CG-04. Field notes say no one on staff does physical work outside the office. site-signin-log.csv shows 6 job-site days (2025-09-16, 2025-10-22, 2025-12-09, 2026-01-28, 2026-03-04, 2026-04-15), but no code in the guide describes the work at those sites, so the person stays C-110. | payroll-register.csv, field-notes.md, site-signin-log.csv |
| HP-E04 | Ellen Short | Legal Secretary | 51,880.16 | C-110 | 51,880.16 C-110 | Legal secretary: correspondence in the office is CG-04 (field-notes.md). | payroll-register.csv, field-notes.md |
| HP-E05 | Gwen Talbot | Office Manager | 58,905.52 | C-110 | 58,905.52 C-110 | Office manager in the office suite: CG-04 (field-notes.md). | payroll-register.csv, field-notes.md |

### Documented facts relied on

- Five-employee law office in Annapolis; no other locations, no subcontractors (business-description.md)
- The founding partner, Catherine Harbor, has filed an election of exclusion and is not on the payroll register (business-description.md)
- Attorneys appear in court and meet clients at closings, neither of which is a job site; no one on staff does physical work outside the office; no travel pay (field-notes.md)
- The payroll register agrees with the general ledger (field-notes.md)
- site-signin-log.csv records Tomas Reyes at Sallowmere Court Condominiums on six dates (site-signin-log.csv)

### Open items for Nadia Brennan to confirm

| # | About | Proposed handling | Why | Records |
|---|---|---|---|---|
| 1 | Tomas Reyes | Keep Tomas Reyes under C-110. The visits look like client or closing work, not field work. | 6 job-site days meets the 5-day threshold (HP-4), but no code in the guide describes the work at the sites (Sallowmere Court Condominiums). House practice does not say what happens then. The field notes say no one does physical work outside the office and that closings are not job sites, so the sign-ins may not be 'job site' days in the sense of HP-4. Why a law office has a site sign-in log at all is not explained. | site-signin-log.csv, field-notes.md |


## Larkspur Lane Bistro

Application APP-LL-0611, signed by Rosa Delacroix. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, payroll-register.csv.

Employer's note on the application: "Our catering crew works events away from the restaurant, so they go under the caterer code."

**Employer's split: accepted.** The records give the same codes and payroll, to the cent, as the employer reported. The decision rests on payroll-register.csv, field-notes.md. Open items below still need confirmation.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| F-710 | CG-41 | 226,431.55 | 226,431.55 | 0.00 |
| F-720 | CG-42 | 114,293.80 | 114,293.80 | 0.00 |
| **Total** | | **340,725.35** | **340,725.35** | **0.00** |

### Where and why the first pass differs from the employer's split

No difference. No adjustment was needed.

### Employee by employee

| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| LL-E01 | Anton Varga | Sous Chef | 52,310.45 | F-710 | 52,310.45 F-710 | Restaurant kitchen staff (CG-41). The field notes describe the restaurant kitchen and dining room; no record puts him on the catering crew. | payroll-register.csv, field-notes.md |
| LL-E02 | Bea Lindell | Line Cook | 41,872.30 | F-710 | 41,872.30 F-710 | Restaurant kitchen staff (CG-41). | payroll-register.csv, field-notes.md |
| LL-E03 | Omar Haddad | Line Cook | 39,640.15 | F-710 | 39,640.15 F-710 | Restaurant kitchen staff (CG-41). | payroll-register.csv, field-notes.md |
| LL-E04 | Sophie Tran | Server | 33,215.80 | F-710 | 33,215.80 F-710 | Restaurant server (CG-41). | payroll-register.csv, field-notes.md |
| LL-E05 | Will Garner | Server | 31,904.65 | F-710 | 31,904.65 F-710 | Restaurant server (CG-41). | payroll-register.csv, field-notes.md |
| LL-E06 | Jose Melendez | Dishwasher | 27,488.20 | F-710 | 27,488.20 F-710 | Restaurant dishwasher (CG-41). | payroll-register.csv, field-notes.md |
| LL-E07 | Hannah Pryor | Catering Lead | 46,725.55 | F-720 | 46,725.55 F-720 | Catering lead: prepares event food in the restaurant kitchen and serves it at the venue (field-notes.md, 2026-07-21). CG-42 covers the catering crew of an employer that also runs a restaurant. | payroll-register.csv, field-notes.md |
| LL-E08 | Ivan Petrov | Event Cook | 38,190.40 | F-720 | 38,190.40 F-720 | Catering crew member (field-notes.md): CG-42. | payroll-register.csv, field-notes.md |
| LL-E09 | Clara Bose | Event Server | 29,377.85 | F-720 | 29,377.85 F-720 | Catering crew member (field-notes.md): CG-42. | payroll-register.csv, field-notes.md |

### Documented facts relied on

- 70-seat restaurant that also caters weddings and office events at customers' venues with a small catering crew; nine employees; books kept by an outside accountant (business-description.md)
- The owner, Rosa Delacroix, has filed an election of exclusion and is not on the payroll register (business-description.md)
- The catering lead and her two crew members prepare event food in the restaurant kitchen and serve it at the venue; on quiet weeks they work restaurant shifts (field-notes.md)
- The owner's sales summary splits monthly receipts between the dining room and off-site catering (field-notes.md, gross-receipts.csv)

### Open items for Nadia Brennan to confirm

| # | About | Proposed handling | Why | Records |
|---|---|---|---|---|
| 1 | Catering crew restaurant shifts (Hannah Pryor, Ivan Petrov, Clara Bose) | Keep each catering crew member's whole pay under F-720, as the employer reported. | The field notes say the catering crew works restaurant shifts on quiet weeks, but the file has no time record showing how many. House practice does not split one person's pay between codes, except for route ride-alongs (HP-2), and their main work is catering (CG-42). If their records showed mostly restaurant shifts, the code would change. | field-notes.md, payroll-register.csv |
| 2 | Gross receipts not used to split payroll | Do not allocate payroll from gross-receipts.csv. | Premium is based on payroll (CG-01, CG-03). Receipts are sales, and house practice gives no rule for using them to divide payroll. The receipts are noted only as context: off-site catering is about 22% of receipts. | gross-receipts.csv |

### Notes on the records

- gross-receipts.csv was not used for the allocation: receipts are sales, not payroll (CG-01, CG-03); see the open item on gross receipts.


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

### Where and why the first pass differs from the employer's split

- **C-110** -118,000.00: out: Raymond Dunmore (118,000.00 reported here, now 63,700.00 E-510).
- **E-510** +66,250.00: in: Raymond Dunmore (owner counted at flat amount, 63,700.00); Curtis Bell (travel allowance above the daily exclusion, 720.00); Hector Ruiz (travel allowance above the daily exclusion, 720.00); Aaron Weiss (travel allowance above the daily exclusion, 720.00); Kyle Brandt (travel allowance above the daily exclusion, 390.00).
- How the employer's split was compared: the employer's per-person codes are inferred: exactly one assignment of the register's wages reproduces its reported head count and payroll for every code.

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Raymond Dunmore | Owner counted at flat amount | 63,700.00 | E-510 | payroll-register.csv shows wages of 118,000.00. House practice counts an owner who does any field work at 63,700.00, under E-510, the code for the work done. The employer reported Raymond Dunmore under C-110. | payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md | HP-3, CG-05 |
| 2 | Curtis Bell | Travel allowance above the daily exclusion | 720.00 | E-510 | 2,600.00 paid for 40 recorded travel days. Up to 47.00 per day (1,880.00) is left out; the remaining 720.00 is payroll. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |
| 3 | Hector Ruiz | Travel allowance above the daily exclusion | 720.00 | E-510 | 2,600.00 paid for 40 recorded travel days. Up to 47.00 per day (1,880.00) is left out; the remaining 720.00 is payroll. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |
| 4 | Aaron Weiss | Travel allowance above the daily exclusion | 720.00 | E-510 | 2,600.00 paid for 40 recorded travel days. Up to 47.00 per day (1,880.00) is left out; the remaining 720.00 is payroll. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |
| 5 | Kyle Brandt | Travel allowance above the daily exclusion | 390.00 | E-510 | 390.00 paid for 0 recorded travel days. Up to 47.00 per day (0.00) is left out; the remaining 390.00 is payroll. | payroll-register.csv (travel_days, travel_allowance_paid) | HP-6 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| PE-E01 | Raymond Dunmore | Owner, Master Electrician | 118,000.00 | C-110 | 63,700.00 E-510 | Included owner who does field work (has not filed an election of exclusion (business-description.md); leads a crew on site most days and pulls wire (field-notes.md); signed in at job sites on 214 days (site-signin-log.csv)). Counted at the flat 63,700.00 (HP-3) under the code for the work done (CG-05). | payroll-register.csv, field-notes.md, site-signin-log.csv, business-description.md |
| PE-E02 | Curtis Bell | Journeyman Electrician | 72,410.35 | E-510 | 72,410.35 E-510<br>720.00 E-510 | Electrician on residential, light commercial and out-of-town wiring jobs (business-description.md, field-notes.md): CG-21.<br>Out-of-town allowance above 47.00 per day: 2,600.00 paid for 40 travel days, 1,880.00 excluded (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E03 | Hector Ruiz | Journeyman Electrician | 69,855.90 | E-510 | 69,855.90 E-510<br>720.00 E-510 | Electrician (business-description.md, field-notes.md): CG-21.<br>Out-of-town allowance above 47.00 per day: 2,600.00 paid for 40 travel days, 1,880.00 excluded (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E04 | Aaron Weiss | Journeyman Electrician | 64,120.65 | E-510 | 64,120.65 E-510<br>720.00 E-510 | Electrician (business-description.md, field-notes.md): CG-21.<br>Out-of-town allowance above 47.00 per day: 2,600.00 paid for 40 travel days, 1,880.00 excluded (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E05 | Tyrone Banks | Electrician | 58,377.20 | E-510 | 58,377.20 E-510 | Electrician (business-description.md, field-notes.md): CG-21. | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E06 | Kyle Brandt | Apprentice Electrician | 41,260.75 | E-510 | 41,260.75 E-510<br>390.00 E-510 | Apprentice electrician on the wiring crew (business-description.md): CG-21.<br>Out-of-town allowance above 47.00 per day: 390.00 paid for 0 travel days, 0.00 excluded (HP-6). | payroll-register.csv, business-description.md, payroll-register.csv (travel_days, travel_allowance_paid) |
| PE-E07 | Linda Marsh | Office Administrator | 43,905.60 | C-110 | 43,905.60 C-110 | Runs the office and never goes to jobs (field-notes.md, 2026-07-17); no entries in site-signin-log.csv. CG-04. | payroll-register.csv, field-notes.md |

### Documented facts relied on

- Seven people on the payroll register, including the owner, Raymond Dunmore, who has not filed an election of exclusion; no subcontractors in the period (business-description.md)
- The owner leads a crew on site most days and pulls wire himself; the office administrator never goes to jobs (field-notes.md)
- site-signin-log.csv has 214 job-site sign-in days, all for Raymond Dunmore (site-signin-log.csv)
- Electricians on the Hagerstown job were paid a flat amount per day away on top of wages, in its own register column (field-notes.md, payroll-register.csv)

### Open items for Nadia Brennan to confirm

| # | About | Proposed handling | Why | Records |
|---|---|---|---|---|
| 1 | Kyle Brandt | Count all 390.00 of the allowance as payroll under E-510. | payroll-register.csv records a travel allowance but no travel days. House practice excludes up to 47.00 per travel day, so with no recorded days nothing is excluded (reading A6). | payroll-register.csv |
| 2 | Employer treats the out-of-town allowance as an expense | Apply house practice: exclude up to 47.00 per worker per travel day and count the rest as payroll. | The application says travel pay is an expense and was left out. CG-03 excludes documented reimbursements. The team's house practice caps the exclusion for out-of-town crews at 47.00 per day (HP-6). The register shows a flat per-day amount, not documented costs. | application.md, payroll-register.csv |


## Severn Homebuilders

Application APP-SH-0417, signed by Martin Severn. Audit period 2025-07-07 to 2026-07-05 (business-description.md). Files read: application.md, business-description.md, field-notes.md, insurance-certificates.csv, payroll-register.csv, site-signin-log.csv, subcontractor-payments.csv.

Employer's note on the application: "Three office staff. All of our subcontractors carry their own insurance."

**Employer's split: not accepted.** The records in the file decide the allocation (HP-7). The decision rests on payroll-register.csv, business-description.md, field-notes.md, site-signin-log.csv, subcontractor-payments.csv, insurance-certificates.csv. Each difference is on this employer's question list.

### Allocation

| Class code | Guide paragraph | Employer reported | First pass | Difference |
|---|---|---|---|---|
| C-110 | CG-04 | 177,209.40 | 117,368.70 | -59,840.70 |
| H-420 | CG-15 | 284,670.30 | 369,204.39 | +84,534.09 |
| R-310 | CG-11 | 0.00 | 18,987.39 | +18,987.39 |
| **Total** | | **461,879.70** | **505,560.48** | **+43,680.78** |

### Where and why the first pass differs from the employer's split

- **C-110** -59,840.70: out: Dana Whitcomb (59,840.70 reported here, now 59,840.70 H-420).
- **H-420** +84,534.09: in: Tidewater Drywall, invoice SV-TID-01 (uninsured subcontractor payment added, 10,944.33); Tidewater Drywall, invoice SV-TID-02 (uninsured subcontractor payment added, 13,749.06); Dana Whitcomb (reclassified, 59,840.70).
- **R-310** +18,987.39: in: Kent Island Roofing, invoice SV-KEN-02 (uninsured subcontractor payment added, 11,928.27); Kent Island Roofing, invoice SV-KEN-03 (uninsured subcontractor payment added, 7,059.12).
- How the employer's split was compared: the employer's per-person codes are inferred: exactly one assignment of the register's wages reproduces its reported head count and payroll for every code.

### Adjustments

| # | Employee or payment | Adjustment | Amount (USD) | Code | Detail | Records | Rule |
|---|---|---|---|---|---|---|---|
| 1 | Kent Island Roofing, invoice SV-KEN-02 | Uninsured subcontractor payment added | 11,928.27 | R-310 | 19,880.45 paid on 2026-03-20 for roofing. Because the certificate in the file (MD-WC-517736, 2025-04-01 to 2026-01-31) does not cover the payment date 2026-03-20, 60% (11,928.27) is added to payroll under R-310, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 2 | Kent Island Roofing, invoice SV-KEN-03 | Uninsured subcontractor payment added | 7,059.12 | R-310 | 11,765.20 paid on 2026-05-08 for roofing. Because the certificate in the file (MD-WC-517736, 2025-04-01 to 2026-01-31) does not cover the payment date 2026-05-08, 60% (7,059.12) is added to payroll under R-310, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 3 | Tidewater Drywall, invoice SV-TID-01 | Uninsured subcontractor payment added | 10,944.33 | H-420 | 18,240.55 paid on 2025-10-03 for drywall. Because no certificate of insurance for this subcontractor is in the file, 60% (10,944.33) is added to payroll under H-420, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 4 | Tidewater Drywall, invoice SV-TID-02 | Uninsured subcontractor payment added | 13,749.06 | H-420 | 22,915.10 paid on 2026-02-27 for drywall. Because no certificate of insurance for this subcontractor is in the file, 60% (13,749.06) is added to payroll under H-420, the code for the work. | subcontractor-payments.csv, insurance-certificates.csv | HP-5, CG-06 |
| 5 | Dana Whitcomb | Reclassified | 59,840.70 | H-420 | The employer reported Dana Whitcomb (Office Manager) under C-110. The records put the 59,840.70 under H-420: Office manager who drives material and paperwork out to the sites and meets inspectors there (field-notes.md, 2026-07-16). site-signin-log.csv shows 11 job-site days (2025-09-17, 2025-09-19, 2025-10-02, 2025-10-17, 2025-11-14, 2026-01-08, 2026-01-14, 2026-01-16, 2026-03-04, 2026-06-16, 2026-06-23), so the person is not clerical (HP-4: 5 or more days). Days by site code: H-420 11 day(s). The person is reported under H-420 (reading A3). | payroll-register.csv, field-notes.md, site-signin-log.csv | HP-1, HP-7 |

### Employee by employee

| ID | Name | Position | Register wages | Employer's code | First pass | Basis | Records |
|---|---|---|---|---|---|---|---|
| SH-E01 | Garrett Holm | Lead Carpenter | 66,315.40 | H-420 | 66,315.40 H-420 | Own crew doing framing, drywall, finish carpentry and site labor on single-family houses (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E02 | Victor Amadi | Carpenter | 62,780.15 | H-420 | 62,780.15 H-420 | Crew carpenter on house construction (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E03 | Peter Kowal | Carpenter | 58,442.60 | H-420 | 58,442.60 H-420 | Crew carpenter on house construction (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E04 | Andre Sutton | Laborer | 49,905.85 | H-420 | 49,905.85 H-420 | General labor at the building site (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E05 | Colin Rusk | Laborer | 47,226.30 | H-420 | 47,226.30 H-420 | General labor at the building site (business-description.md): CG-15. | payroll-register.csv, business-description.md |
| SH-E06 | Marissa Gale | Estimator | 71,250.45 | C-110 | 71,250.45 C-110 | Estimator who visits a site now and then to measure (field-notes.md, 2026-07-16). Estimating at a desk is CG-04. site-signin-log.csv shows 4 job-site day(s) (2025-07-24, 2026-01-16, 2026-03-24, 2026-04-21), fewer than 5, so the person stays C-110 (HP-4). | payroll-register.csv, field-notes.md, site-signin-log.csv |
| SH-E07 | Dana Whitcomb | Office Manager | 59,840.70 | C-110 | 59,840.70 H-420 | Office manager who drives material and paperwork out to the sites and meets inspectors there (field-notes.md, 2026-07-16). site-signin-log.csv shows 11 job-site days (2025-09-17, 2025-09-19, 2025-10-02, 2025-10-17, 2025-11-14, 2026-01-08, 2026-01-14, 2026-01-16, 2026-03-04, 2026-06-16, 2026-06-23), so the person is not clerical (HP-4: 5 or more days). Days by site code: H-420 11 day(s). The person is reported under H-420 (reading A3). | payroll-register.csv, field-notes.md, site-signin-log.csv |
| SH-E08 | Helen Ostrow | Bookkeeper | 46,118.25 | C-110 | 46,118.25 C-110 | Bookkeeper who stays in the office (field-notes.md): CG-04. | payroll-register.csv, field-notes.md |

Subcontractor payroll added:

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

### Open items for Nadia Brennan to confirm

| # | About | Proposed handling | Why | Records |
|---|---|---|---|---|
| 1 | Dana Whitcomb | Report all 59,840.70 of Dana Whitcomb's pay under H-420, the code of the house construction at the sites she visited. | 11 job-site days is at or above the 5-day threshold (HP-4). House practice does not say which code replaces C-110. H-420 is the code of the work at the sites visited (H-420 11 day(s)). Her site work is delivering material and paperwork and meeting inspectors, not construction. CG-15 covers general labor at the building site, and no other code in the guide describes the work. | site-signin-log.csv, field-notes.md |
| 2 | Kent Island Roofing | Treat the certificate issued to 'Kent Island Roofing & Siding LLC' as Kent Island Roofing's. | subcontractor-payments.csv pays 'Kent Island Roofing', but the certificate in insurance-certificates.csv is issued to 'Kent Island Roofing & Siding LLC'. The names are close but not the same. | subcontractor-payments.csv, insurance-certificates.csv |
| 3 | Employer's statement that all subcontractors are insured | Use the certificates in the file, not the application's statement. | The application says all subcontractors carry their own insurance. The file has no certificate for Tidewater Drywall, and Kent Island's certificate ends on 2026-01-31, before two of its payments. The records decide (HP-7). | application.md, insurance-certificates.csv, subcontractor-payments.csv |

### Notes on the records

- 1 sign-in row(s) in site-signin-log.csv have no employee ID (County inspector); they are not employees and were not used.
- Tenbury Ridge Framing Co.: 3 payment(s) covered by a certificate in the file, 0 not covered.
- Kent Island Roofing: 1 payment(s) covered by a certificate in the file, 2 not covered.
- Tidewater Drywall: 0 payment(s) covered by a certificate in the file, 2 not covered.
