# LEO Procurement / Accounting Local Review Demo v0.6

Canonical save path:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_PUBLIC_REPOSITORY_README_v0.1.md`

Recommended public repository README path after publication staging:

`demos/procurement_accounting_anomaly_audit/README.md`

Related repository publication precheck:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_REPOSITORY_PUBLICATION_PRECHECK_v0.1.md`

Related dashboard file:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html`

Document status: PUBLIC REPOSITORY README SOURCE

Dashboard version: v0.6 — Reviewer Workflow Hardening

Publication status: README PREPARED, NOT YET PUBLISHED

---

# LEO Procurement / Accounting Local Review Demo v0.6

This folder contains a local demonstration of the LEO Procurement / Accounting Review Module v0.6.

The demo shows how procurement/accounting data can be transformed into evidence-linked review signals, reviewer questions, reliability warnings, source-trust boundaries, and local review packages.

The demo is human-review-only.

It does not create fraud verdicts, legal conclusions, compliance certifications, payment decisions, supplier sanctions, or enforcement actions.

---

# Status

```text
LOCAL PROTOTYPE ONLY
HUMAN REVIEW ONLY
NO AUTONOMOUS ENFORCEMENT
NO FRAUD VERDICT
NO LEGAL CERTIFICATION
NO DONOR COMPLIANCE CERTIFICATION
NO PAYMENT DECISION
NO SUPPLIER SANCTION
NOT PRODUCTION READY
DEMO DATA ONLY
```

---

# What this demo does

The demo dashboard can:

* load a structured procurement/accounting evidence report;
* display evidence-linked review signals;
* show source trust and provenance warnings;
* show reliability state;
* prioritize findings for human review;
* display rule trace and protocol context;
* record local reviewer actions in browser storage;
* show unresolved review work;
* generate a local reviewer memo;
* export a local human review package with warnings and boundaries.

The demo is intended to show a review workflow, not an autonomous decision system.

---

# What this demo does not do

This demo does not:

* prove fraud;
* prove corruption;
* issue legal conclusions;
* certify donor compliance;
* approve or reject expenses;
* block payments;
* sanction suppliers;
* replace auditors;
* replace officials;
* guarantee source data authenticity;
* create production audit evidence;
* mutate source records;
* mutate production records;
* mutate any canonical registry.

All findings are review signals only.

Human review remains required.

---

# Current demo baseline

The current v0.6 demo baseline is:

```text
21 findings
21 evidence objects
7 suppliers
7 high-risk review signals
19 unresolved findings
2 reviewed annotations
RELIABILITY_GUARDED
READY_WITH_WARNINGS
USER_PROVIDED_UNVERIFIED
EXPORT_READY_WITH_WARNINGS
0 autonomous enforcement actions
production mutation: false
canonical registry mutation: false
```

These values are expected when the included demo evidence report is loaded.

---

# Folder contents

Recommended public folder structure:

```text
demos/procurement_accounting_anomaly_audit/
  README.md
  leo_demo_dashboard.html
  output/
    demo_evidence_report.json
  docs/
    LEO_PROCUREMENT_ACCOUNTING_ONE_PAGE_EXTERNAL_EXPLANATION_v0.6.md
    LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
    LEO_PROCUREMENT_ACCOUNTING_LOCAL_DEMO_PACKAGE_INDEX_v0.6.md
    LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_FINAL_DEMO_READINESS_CHECKPOINT_v0.1.md
  sample_exports/
    LEO_LOCAL_HUMAN_REVIEW_PACKAGE_SAMPLE_v0.6.json
```

---

# How to run the demo locally

1. Open the dashboard file in a modern desktop browser:

```text
leo_demo_dashboard.html
```

2. Load the demo evidence report when prompted or through the file upload control:

```text
output/demo_evidence_report.json
```

3. Start with:

```text
Executive View
```

4. Review the main dashboard sections:

```text
Executive Summary
Source Trust and Provenance
Priority Review Queue
Review Completion
Export Readiness
```

5. Open a finding card to inspect evidence, rule trace, reviewer question, and reliability state.

6. Use reviewer actions only as local annotations.

7. Export a local human review package if needed.

---

# Recommended demo flow

Recommended live walkthrough:

```text
1. Open leo_demo_dashboard.html.
2. Load output/demo_evidence_report.json.
3. Show Executive Summary.
4. Show Source Trust and Provenance.
5. Show Priority Review Queue.
6. Open one finding, for example EV-001.
7. Show evidence, rule trace, and reviewer question.
8. Show Reliability state.
9. Show Review Completion panel.
10. Show Export Readiness Gate.
11. Export local review package.
12. Explain boundaries.
```

Recommended duration:

```text
5 to 8 minutes for executive overview
15 to 25 minutes for reviewer or technical walkthrough
```

---

# Key concept

A finding is not a verdict.

A finding means:

```text
This item should be reviewed by a human.
```

A finding does not mean:

```text
fraud was proven
law was violated
compliance failed
payment must be blocked
supplier must be sanctioned
```

---

# Source trust and reliability

The current demo uses local demo data.

Current source trust state:

```text
USER_PROVIDED_UNVERIFIED
```

Current input quality state:

```text
READY_WITH_WARNINGS
```

Current reliability state:

```text
RELIABILITY_GUARDED
```

This means the demo can show review logic, but strong institutional conclusions remain restricted.

Future production versions would require trusted ingestion, cross-source verification, secure storage, and stronger provenance controls.

---

# Export package meaning

The exported package is a local human review package.

It may contain:

* findings;
* evidence references;
* reviewer actions;
* review completion summary;
* reliability summary;
* source trust warnings;
* rule trace summary;
* protocol context;
* audit timeline summary;
* export readiness summary;
* boundary declarations.

The exported package is not legal certification, external audit submission, production archive, or institutional approval.

---

# Known limitations

The current demo has important limitations:

* local browser-based execution;
* manual local file loading;
* browser localStorage for reviewer actions;
* user-provided unverified source data;
* no production database;
* no trusted ingestion connector;
* no cryptographic hash or digital signature;
* no external timestamp;
* no multi-user workflow;
* no production archive;
* no legal or compliance authority.

See:

```text
docs/LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
```

---

# Future development direction

Future work may include:

* trusted data ingestion connectors;
* accounting system exports;
* bank export comparison;
* procurement platform data;
* public registry verification;
* secure storage;
* reviewer identity and role model;
* audit-grade persistence;
* larger demo-safe datasets;
* controlled institutional pilot testing.

These are not included in v0.6.

---

# Correct public description

```text
LEO helps institutions turn procurement and accounting uncertainty into evidence-linked review signals, reviewer questions, reliability warnings, and exportable local review packages without autonomous enforcement.
```

---

# Safety boundary

This demo is provided as a local prototype for demonstration and pilot discussion.

It must not be used as a production audit system, legal decision system, donor compliance certification system, payment control system, or enforcement system.

---

# Repository publication note

Before publishing or updating this folder, verify that included files contain only demo-safe data and no private keys, credentials, tokens, real bank records, real confidential accounting records, private personal data, or private foundation documents.

If there is doubt about a file, do not publish it until reviewed.

---

# Current continuation marker

This README source is prepared for repository publication staging.

Recommended next step:

```text
Prepare a clean repository publication staging folder and verify the exact file list before Git commit or upload.
```

No Git commit is authorized by this document alone.
