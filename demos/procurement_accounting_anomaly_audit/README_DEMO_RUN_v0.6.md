# LEO Procurement / Accounting Anomaly Review Dashboard

# README Demo Run v0.6

Canonical save path:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\README_DEMO_RUN_v0.6.md`

Canonical dashboard file:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html`

Required input report:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\output\demo_evidence_report.json`

Recommended export archive path:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\exports\human_review_packages\`

Validated export package example:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\exports\human_review_packages\LEO_LOCAL_HUMAN_REVIEW_PACKAGE_v5_0_reliability_state_layer_2026-05-27_054848.json`

Current accepted baseline checkpoint:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_REVIEWER_WORKFLOW_HARDENING_WORKING_BASELINE_CHECKPOINT_v0.1.md`

Document status: DEMO RUN README

Dashboard version: v0.6 — Reviewer Workflow Hardening

Demo status: LOCAL DEMO READY WITH WARNINGS

---

# 1. Purpose

This README explains how to run the local LEO Procurement / Accounting Anomaly Review Dashboard demo.

The dashboard demonstrates a local, human-controlled institutional review workflow for procurement/accounting anomaly review.

It shows how LEO can:

* load a structured evidence report;
* display procurement/accounting review signals;
* link findings to evidence;
* show reliability and source-trust limitations;
* guide a human reviewer through priority findings;
* record local reviewer actions;
* generate a local reviewer memo;
* export a local human review package.

This demo is not a production deployment.

This demo is not a legal, audit, compliance, or enforcement system.

---

# 2. What this demo shows

The demo shows the following workflow:

```text
INPUT -> ANALYSIS -> EVIDENCE -> RELIABILITY -> HUMAN REVIEW -> EXPORT
```

The dashboard helps a reviewer understand:

* what findings were detected;
* which findings should be reviewed first;
* what evidence is linked to each finding;
* what rule/protocol context is available;
* what reliability state applies;
* what source trust limitations exist;
* what remains unresolved;
* whether the export is ready with warnings.

---

# 3. What this demo does not do

The demo does not:

* issue fraud verdicts;
* issue legal conclusions;
* certify donor compliance;
* approve or reject expenses;
* block payments;
* sanction suppliers;
* mutate source evidence;
* mutate production records;
* mutate the canonical registry;
* perform digital signing;
* create cryptographic hashes;
* create an external audit certification;
* store review state in a production database.

The demo is human-review-only.

---

# 4. Required files

To run the demo, the following files should exist.

## 4.1 Dashboard file

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html
```

## 4.2 Evidence report input file

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\output\demo_evidence_report.json
```

## 4.3 Optional existing export archive folder

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\exports\human_review_packages\
```

If the export folder does not exist, create it manually before archiving exported packages.

---

# 5. Recommended browser

Use a modern desktop browser such as:

* Chrome;
* Edge;
* Firefox.

The dashboard uses browser-local behavior and local file loading.

It is not a server application in v0.6.

---

# 6. How to open the dashboard

1. Open this file in a browser:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html
```

2. The dashboard should open in dark theme.

3. Confirm that the page shows LEO Procurement / Accounting Anomaly Review Dashboard.

4. Confirm that view modes are visible:

```text
Executive View
Reviewer View
Technical View
```

---

# 7. How to load the evidence report

1. Find the file upload control in the dashboard.

2. Select:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\output\demo_evidence_report.json
```

3. After loading, confirm the dashboard displays the expected baseline:

```text
21 findings
21 evidence objects
7 suppliers
7 high-risk review signals
19 unresolved findings
2 reviewed annotations
RELIABILITY_GUARDED
READY_WITH_WARNINGS
EXPORT_READY_WITH_WARNINGS
```

---

# 8. Recommended first view for demonstrations

Start with:

```text
Executive View
```

Executive View is intended for:

* non-technical viewers;
* institutional officials;
* foundation collaborators;
* donors;
* public-sector contacts;
* first-time reviewers.

It should show the main institutional state without exposing all technical detail at once.

---

# 9. What to show first

Recommended first explanation sequence:

```text
1. Executive Summary
2. Source Trust and Provenance
3. Priority Review Queue
4. Review Completion panel
5. Export Readiness Gate
```

This gives the viewer a clear understanding before opening technical details.

---

# 10. How to explain Executive Summary

The Executive Summary answers:

```text
What happened?
How many findings exist?
How many require review?
How many are unresolved?
Did LEO take autonomous action?
```

Expected explanation:

```text
LEO detected review signals in the provided procurement/accounting data.
The system does not make decisions.
It creates a structured review workspace for a human reviewer.
```

---

# 11. How to explain Source Trust and Provenance

The Source Trust and Provenance block explains whether LEO can fully trust the source data.

Current demo state:

```text
Source trust: USER_PROVIDED_UNVERIFIED
Interpretation strength: GUARDED
Input quality: READY_WITH_WARNINGS
```

Recommended explanation:

```text
LEO does not assume that uploaded files are automatically authentic.
Because this demo uses user-provided local files, strong institutional conclusions remain restricted.
The findings are review signals, not final verdicts.
```

---

# 12. How to explain Priority Review Queue

The Priority Review Queue answers:

```text
What should the reviewer inspect first?
```

It helps avoid a flat list of findings.

Recommended explanation:

```text
The dashboard prioritizes unresolved and high-risk review signals so the reviewer is not forced to inspect all findings equally.
```

The queue is a workflow aid.

It is not a legal severity ranking.

---

# 13. How to inspect a finding

To inspect a finding:

1. Open a finding card.
2. Read the title, severity, supplier, and explanation.
3. Review the evidence IDs.
4. Read the reviewer question.
5. Open rule trace or protocol context if needed.
6. Check reliability state.
7. Select a reviewer action only if appropriate.
8. Add a reviewer note where recommended or required.

A finding is a review signal.

It is not a fraud conclusion.

---

# 14. Recommended finding to show in a demo

A useful first finding to show is:

```text
EV-001 — Price above benchmark
```

It is useful because it demonstrates:

* a clear review signal;
* evidence linkage;
* rule trace;
* reviewer question;
* reliability state;
* local reviewer action;
* boundary discipline.

Recommended explanation:

```text
LEO identifies that the observed price is above benchmark.
It does not say fraud occurred.
It asks whether there is documented justification.
```

---

# 15. How to explain reviewer actions

Reviewer actions are local annotations.

They help organize human review.

They do not create institutional decisions.

Possible actions may include:

```text
Escalate for review
Needs more evidence
Accept as justified for review context
Mark false positive with reason
Defer with reason
```

Reviewer actions are stored locally in browser storage until exported.

---

# 16. How to explain Review Completion panel

The Review Completion panel answers:

```text
How much review work remains?
```

Current expected demo state:

```text
Total findings: 21
Reviewed annotations: 2
Unresolved findings: 19
Escalated findings: 2
Missing required notes: 0
Missing recommended notes: 1
Review status: REVIEW_HAS_UNRESOLVED_ITEMS
```

Recommended explanation:

```text
The dashboard shows that review has started but is not complete.
The export can be generated, but it is not archive-clean or final.
```

---

# 17. How to explain Export Readiness Gate

The Export Readiness Gate answers:

```text
Can the reviewer responsibly export this package now?
```

Current expected status:

```text
EXPORT_READY_WITH_WARNINGS
```

This means the export is allowed as a local review artifact, but warnings remain.

Expected warnings include:

```text
Unresolved findings remain.
Recommended reviewer notes may be missing.
Source data is user-provided and unverified.
Input quality is READY_WITH_WARNINGS.
Export is local only.
No cryptographic hash, digital signature, or external timestamp is included.
```

---

# 18. How to export a review package

1. Review the dashboard state.
2. Check Review Completion panel.
3. Check Export Readiness Gate.
4. Click the export button.
5. Save the exported JSON file into:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\exports\human_review_packages\
```

6. Keep the exported package with its generated timestamped file name.

---

# 19. What export means

The exported JSON package is:

```text
LOCAL HUMAN REVIEW PACKAGE
```

It contains:

* findings;
* evidence references;
* reviewer actions;
* reliability summary;
* protocol context;
* timeline summary;
* export readiness summary;
* boundary declarations.

It is useful for local review memory and demonstration.

---

# 20. What export does not mean

The exported package is not:

* legal certification;
* external audit submission;
* donor compliance approval;
* final accounting decision;
* payment approval;
* supplier sanction;
* production archive;
* cryptographic proof;
* government evidence certification.

This must be stated clearly in demonstrations.

---

# 21. Expected validated export indicators

A valid v0.6 export should include:

```text
reviewer_workflow_hardening_summary
export_readiness_summary
review_completion_summary
reliability_state_summary
rule_trace_summary
protocol_library_context
audit_event_timeline_summary
integrity_manifest
zero_autonomy_boundary
boundary_declaration
```

If these sections are missing, the export should not be treated as v0.6 baseline export.

---

# 22. Expected validated export values

Expected values:

```text
findings_count: 21
evidence_objects_count: 21
suppliers_count: 7
unresolved_findings_count: 19
reviewed_findings_count: 2
aggregated_report_reliability: RELIABILITY_GUARDED
input_quality_status: READY_WITH_WARNINGS
source_trust_level: USER_PROVIDED_UNVERIFIED
interpretation_strength: GUARDED
export_status: EXPORT_READY_WITH_WARNINGS
autonomous_enforcement_actions: 0
production_mutation: false
canonical_registry_mutation: false
```

---

# 23. Troubleshooting

## 23.1 Dashboard opens but no data appears

Check that the input report was selected manually:

```text
output\demo_evidence_report.json
```

The dashboard does not automatically load the local file in all browsers.

## 23.2 Review actions are missing

Review actions are stored in browser localStorage.

If a different browser, private mode, or cleared storage is used, previous local reviewer actions may not appear.

## 23.3 Export file has unexpected counts

Check that the correct input file was loaded.

Check that localStorage did not contain old review actions from a previous run.

## 23.4 Browser blocks local behavior

Try another modern desktop browser.

Use normal browsing mode, not strict private mode.

---

# 24. Current known limitations

The current demo has these known limitations:

```text
local prototype only
manual local file loading
user-provided unverified source data
READY_WITH_WARNINGS input quality state
browser localStorage review state
no production database
no cryptographic hash
no digital signature
no external timestamp
no trusted ingestion connector
no multi-user workflow
no production archive
```

These limitations are known and intentional at v0.6.

---

# 25. Data quality warning

The current input quality state is:

```text
READY_WITH_WARNINGS
```

This means:

```text
Analysis may proceed.
Human review is required.
False-positive review load may be elevated.
Strong conclusions remain restricted.
```

---

# 26. Source trust warning

The current source trust state is:

```text
USER_PROVIDED_UNVERIFIED
```

This means:

```text
LEO can analyze the provided data.
LEO does not guarantee that the data was not changed before ingestion.
Cross-source verification is not yet production-grade.
Human verification remains required.
```

---

# 27. LocalStorage warning

The dashboard uses browser localStorage for local reviewer actions.

This means:

```text
review state is local to the browser;
review state may disappear if storage is cleared;
review state is not multi-user;
review state is not production archive;
review state is not suitable for large institutional datasets.
```

Exporting the package is required to preserve a local review snapshot outside browser storage.

---

# 28. Recommended demo duration

Recommended short demonstration duration:

```text
5 to 8 minutes
```

Recommended extended technical walkthrough:

```text
15 to 25 minutes
```

Do not start a first-time demo with internal architecture documents.

Start with the dashboard.

---

# 29. Recommended demo script outline

Use this order:

```text
1. This is a local human-review prototype.
2. LEO loads procurement/accounting evidence data.
3. LEO detects review signals, not verdicts.
4. LEO shows source trust and reliability limits.
5. LEO prioritizes what should be reviewed first.
6. A human reviewer can inspect evidence and rule context.
7. Reviewer actions remain local annotations.
8. Export creates a local review package with warnings.
9. LEO does not enforce, approve, punish, or certify.
```

---

# 30. Recommended closing statement for demo

Recommended closing statement:

```text
This prototype demonstrates how LEO can help an institution move from unclear procurement/accounting data toward structured, evidence-linked, human-controlled review.

It does not replace officials, auditors, accountants, or legal reviewers.

It gives them a clearer review workspace and preserves the boundaries of human responsibility.
```

---

# 31. Demo readiness checklist

Before showing the demo, confirm:

```text
[ ] leo_demo_dashboard.html opens.
[ ] demo_evidence_report.json loads.
[ ] Executive View is visible.
[ ] Source Trust and Provenance block is visible.
[ ] Priority Review Queue is visible.
[ ] Review Completion panel is visible.
[ ] Export Readiness Gate is visible.
[ ] At least one finding can be opened.
[ ] Rule trace is visible.
[ ] Reliability state is visible.
[ ] Export package downloads.
[ ] Export contains reviewer_workflow_hardening_summary.
[ ] Export contains export_readiness_summary.
[ ] Export confirms autonomous_actions_count: 0.
[ ] Export confirms production_mutation: false.
[ ] Export confirms canonical_registry_mutation: false.
```

---

# 32. Boundary statement

The v0.6 dashboard is a local human-review-only institutional prototype.

It supports review.

It supports evidence visibility.

It supports reliability warnings.

It supports source trust transparency.

It supports exportable local review packages.

It does not create legal conclusions.

It does not create donor compliance determinations.

It does not create fraud verdicts.

It does not approve or reject expenses.

It does not trigger enforcement.

It does not mutate source evidence.

It does not mutate production records.

It does not mutate the canonical registry.

---

# 33. Current continuation marker

After saving this README, continue with:

```text
LEO_PROCUREMENT_ACCOUNTING_DEMO_STORYLINE_v0.6.md
```

Recommended canonical path:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_DEMO_STORYLINE_v0.6.md
```

Do not modify dashboard code by default.

Do not add new analytical layers by default.

Proceed with demo package completion.
