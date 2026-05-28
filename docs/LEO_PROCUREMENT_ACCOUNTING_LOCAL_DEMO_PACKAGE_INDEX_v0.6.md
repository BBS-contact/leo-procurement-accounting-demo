# LEO Procurement / Accounting Anomaly Review Dashboard

# Local Demo Package Index v0.6

Canonical save path:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_LOCAL_DEMO_PACKAGE_INDEX_v0.6.md`

Canonical dashboard file:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html`

Demo package branch:

`Procurement / Accounting controlled demo-readiness and final local package branch`

Current accepted dashboard baseline:

`PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_REVIEWER_WORKFLOW_HARDENING_WORKING_BASELINE_ACCEPTED`

Document status: LOCAL DEMO PACKAGE INDEX

Dashboard version: v0.6 — Reviewer Workflow Hardening

Demo status: DEMO_READY_WITH_WARNINGS

Pilot discussion status: PILOT_DISCUSSION_READY_WITH_BOUNDARIES

Production status: NOT_PRODUCTION_READY

---

# 1. Purpose

This document is the local demo package index for the LEO Procurement / Accounting Anomaly Review Dashboard v0.6.

Its purpose is to collect the current demonstration package into one navigable reference.

This file helps prevent confusion about:

* which dashboard file is current;
* which input report is required;
* where exported packages should be saved;
* which documents explain the demo;
* which documents explain limitations;
* which checkpoint defines the accepted baseline;
* what must not be changed or overclaimed.

This index is not a new analytical layer.

It is a package map.

---

# 2. Current package status

The current package status is:

```text
LOCAL_DEMO_PACKAGE_V0_6_INDEXED
```

The dashboard is suitable for:

* local demonstration;
* institutional walkthrough;
* reviewer workflow explanation;
* pilot discussion;
* partner/funder conversation;
* technical review of prototype boundaries.

The dashboard is not suitable for:

* production deployment;
* legal certification;
* donor compliance certification;
* final accounting decision;
* payment control;
* supplier sanction;
* autonomous enforcement.

---

# 3. Canonical root folder for this demo

Canonical demo folder:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\
```

All files in this index belong to this local demo branch unless explicitly stated otherwise.

---

# 4. Current canonical dashboard

Current dashboard file:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html
```

Current dashboard state:

```text
v0.6 — Reviewer Workflow Hardening
```

Confirmed capabilities:

* dark-theme local dashboard;
* local evidence report loading;
* Executive View;
* Reviewer View;
* Technical View;
* Executive Summary;
* Source Trust and Provenance block;
* Priority Review Queue;
* Guided Review Flow;
* Review Completion panel;
* Export Readiness Gate;
* finding-level reliability state;
* rule trace context;
* donor/grant protocol context;
* audit event timeline;
* graph relationship view;
* reviewer actions in localStorage;
* reviewer memo generation;
* local human review package export;
* export integrity manifest;
* zero-autonomy boundary.

---

# 5. Required input report

Required input report:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\output\demo_evidence_report.json
```

Expected baseline after loading:

```text
21 findings
21 evidence objects
7 suppliers
7 high-risk review signals
2 reviewed annotations
19 unresolved findings
RELIABILITY_GUARDED
READY_WITH_WARNINGS
USER_PROVIDED_UNVERIFIED
EXPORT_READY_WITH_WARNINGS
```

If these values are not visible, verify that the correct input report is loaded.

---

# 6. Recommended export archive folder

Recommended export archive folder:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\exports\human_review_packages\
```

Validated export package example:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\exports\human_review_packages\LEO_LOCAL_HUMAN_REVIEW_PACKAGE_v5_0_reliability_state_layer_2026-05-27_054848.json
```

Do not overwrite older exported packages unless explicitly instructed.

Exported packages are local review artifacts.

They are not legal certification, external audit submission, production archive, or institutional approval.

---

# 7. Core demo package documents

## 7.1 Demo run README

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\README_DEMO_RUN_v0.6.md
```

Purpose:

Explains how to open the dashboard, load the evidence report, review findings, generate exports, and understand local prototype boundaries.

Use when:

* someone needs to run the demo;
* someone needs practical startup instructions;
* the dashboard must be opened without developer guidance.

---

## 7.2 Demo storyline

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_DEMO_STORYLINE_v0.6.md
```

Purpose:

Explains the story of the demo: what problem it addresses, how LEO transforms data into review signals, and how to explain the value of the module.

Use when:

* preparing a presentation;
* explaining LEO to a new person;
* discussing the module with partners or funders.

---

## 7.3 Executive walkthrough for officials

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_EXECUTIVE_WALKTHROUGH_FOR_OFFICIALS_v0.6.md
```

Purpose:

Provides a short, non-technical walkthrough for officials and institutional leaders.

Use when:

* demonstrating LEO to a public-sector contact;
* presenting to a non-technical viewer;
* explaining what to look at first in Executive View.

---

## 7.4 Reviewer workflow walkthrough

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_REVIEWER_WORKFLOW_WALKTHROUGH_v0.6.md
```

Purpose:

Explains how a human reviewer should use the dashboard: queue, findings, notes, actions, review completion, and export readiness.

Use when:

* training a reviewer;
* explaining reviewer actions;
* checking what unresolved / escalated / notes mean;
* preparing a local review session.

---

## 7.5 Local prototype limitations and production readiness boundary

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
```

Purpose:

Defines current limitations: data quality dependency, false-positive risk, source provenance limitation, localStorage limitation, no production storage, no hash/signature, no legal/compliance authority.

Use when:

* discussing limitations honestly;
* preparing pilot discussion;
* avoiding production-readiness overclaims;
* explaining what future development must solve.

---

# 8. Baseline and planning documents

## 8.1 v0.6 working baseline checkpoint

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_REVIEWER_WORKFLOW_HARDENING_WORKING_BASELINE_CHECKPOINT_v0.1.md
```

Purpose:

Records the accepted v0.6 working baseline after export validation.

Use when:

* checking current accepted state;
* preventing regression;
* confirming counts and boundary values;
* resuming development in later sessions.

---

## 8.2 v0.6 demo readiness and walkthrough package plan

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_DEMO_READINESS_AND_WALKTHROUGH_PACKAGE_PLAN_v0.1.md
```

Purpose:

Defines the demo-readiness package and required walkthrough files.

Use when:

* checking why these documentation files exist;
* continuing demo package completion;
* confirming no new deep architecture layer is intended.

---

## 8.3 Reviewer workflow hardening implementation plan

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_REVIEWER_WORKFLOW_HARDENING_IMPLEMENTATION_PLAN_v0.1.md
```

Purpose:

Defined the v0.6 workflow hardening phase before implementation.

Use when:

* checking why Review Completion panel and Export Readiness Gate were added;
* reviewing workflow-hardening design intent.

---

## 8.4 Executive view and priority review queue checklist

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_EXECUTIVE_VIEW_AND_PRIORITY_REVIEW_QUEUE_IMPLEMENTATION_CHECKLIST_v0.1.md
```

Purpose:

Defined Executive View, Priority Queue, Guided Review Flow, compact institutional cards, and human-readable explanations.

Use when:

* checking institutional usability design;
* validating dashboard layout priorities.

---

## 8.5 Institutional dashboard usability consolidation plan

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_INSTITUTIONAL_DASHBOARD_USABILITY_CONSOLIDATION_PLAN_v0.1.md
```

Purpose:

Defined the transition from technical review dashboard to institutional usability model.

Use when:

* checking why the dashboard has Executive / Reviewer / Technical layers;
* preventing UI overload.

---

## 8.6 Trusted data ingestion and source provenance layer

File:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_TRUSTED_DATA_INGESTION_AND_SOURCE_PROVENANCE_LAYER_v0.1.md
```

Purpose:

Defines future source-trust architecture and why user-provided data must remain guarded until trusted ingestion exists.

Use when:

* discussing data manipulation risk;
* explaining why source trust is USER_PROVIDED_UNVERIFIED;
* planning future connectors.

---

# 9. Export package structure to expect

A valid v0.6 export should include:

```text
package_type
package_version
integrity_manifest
runtime_operational_state
review_completion_summary
rule_trace_summary
reliability_state_summary
protocol_library_context
audit_event_timeline_summary
reviewer_workflow_hardening_summary
export_readiness_summary
unresolved_flags
boundary_labels
boundary_declaration
zero_autonomy_boundary
audit_trace
limitations
summary
findings
```

If `reviewer_workflow_hardening_summary` or `export_readiness_summary` is missing, the export should not be treated as the accepted v0.6 baseline export.

---

# 10. Validated baseline export values

Validated values from accepted export:

```text
findings_count: 21
evidence_objects_count: 21
suppliers_count: 7
high_or_critical_findings_count: 7
reviewed_findings_count: 2
unresolved_findings_count: 19
protocol_rule_count: 7
protocol_linked_findings_count: 21
unique_protocol_rule_references_count: 5
timeline_events_count: 137
autonomous_actions_count: 0
```

Workflow hardening values:

```text
workflow_layer_version: v0.6-reviewer-workflow-hardening
review_status: REVIEW_HAS_UNRESOLVED_ITEMS
reviewed_annotations_count: 2
unresolved_findings_count: 19
escalated_count: 2
needs_more_evidence_count: 0
missing_required_note_count: 0
missing_recommended_note_count: 1
source_trust_level: USER_PROVIDED_UNVERIFIED
interpretation_strength: GUARDED
```

Export readiness values:

```text
export_status: EXPORT_READY_WITH_WARNINGS
reliability_state: RELIABILITY_GUARDED
local_prototype_boundary: true
cryptographic_hash_included: false
digital_signature_included: false
external_timestamp_included: false
production_archive_created: false
legal_certification_created: false
enforcement_triggered: false
production_mutation: false
canonical_registry_mutation: false
```

---

# 11. Protocol and rule context files

The demo package references protocol and rule trace files under local protocol folders.

Important current protocol context:

```text
DONOR_GRANT_REVIEW v0.1
```

Important rule families include:

```text
PROC-FRAGMENTATION-CLUSTER-001
PROC-PRICE-BENCHMARK-001
PROC-QUANTITY-REVIEW-001
PROC-SUPPLIER-ACTIVITY-001
PROC-SUPPLIER-CAPACITY-001
```

Protocol context is review criteria only.

It does not create donor compliance verdicts, legal conclusions, fraud verdicts, or enforcement.

---

# 12. What to open for different audiences

## 12.1 Official or non-technical viewer

Open first:

```text
leo_demo_dashboard.html
```

Then use:

```text
LEO_EXECUTIVE_WALKTHROUGH_FOR_OFFICIALS_v0.6.md
```

Do not start with protocol internals or raw JSON.

---

## 12.2 Reviewer or auditor

Open first:

```text
leo_demo_dashboard.html
```

Then use:

```text
LEO_REVIEWER_WORKFLOW_WALKTHROUGH_v0.6.md
```

Focus on findings, notes, unresolved state, and export readiness.

---

## 12.3 Partner or funder

Use:

```text
LEO_PROCUREMENT_ACCOUNTING_DEMO_STORYLINE_v0.6.md
LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
```

Explain both value and limitations.

---

## 12.4 Developer or technical advisor

Use:

```text
LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_REVIEWER_WORKFLOW_HARDENING_WORKING_BASELINE_CHECKPOINT_v0.1.md
LEO_TRUSTED_DATA_INGESTION_AND_SOURCE_PROVENANCE_LAYER_v0.1.md
LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
```

Focus on architecture boundaries, trusted ingestion, storage, and future production path.

---

# 13. Recommended demo sequence

Recommended sequence for live demo:

```text
1. Open leo_demo_dashboard.html.
2. Load output\demo_evidence_report.json.
3. Select Executive View.
4. Show Executive Summary.
5. Show Source Trust and Provenance.
6. Show Priority Review Queue.
7. Open EV-001 as example finding.
8. Show reviewer question and rule trace.
9. Show Reliability state.
10. Show Review Completion panel.
11. Show Export Readiness Gate.
12. Export local review package.
13. Explain export boundaries.
```

Recommended duration:

```text
5 to 8 minutes for executive demo
15 to 25 minutes for technical/reviewer walkthrough
```

---

# 14. Correct project positioning

Correct positioning:

```text
LEO is a human-controlled institutional review support system.
```

Expanded positioning:

```text
LEO helps institutions transform procurement/accounting uncertainty into evidence-linked review signals, reviewer questions, reliability warnings, and exportable local review packages without autonomous enforcement.
```

---

# 15. Claims allowed

Allowed claims:

```text
LEO detects review signals.
LEO links findings to evidence.
LEO provides rule trace and protocol context.
LEO shows source trust limitations.
LEO shows reliability state.
LEO supports local reviewer annotations.
LEO exports local review packages.
LEO remains human-review-only.
LEO is a local prototype ready for demo and pilot discussion with boundaries.
```

---

# 16. Claims not allowed

Do not claim:

```text
LEO proves corruption.
LEO detects fraud as a verdict.
LEO certifies compliance.
LEO replaces auditors.
LEO replaces officials.
LEO is production-ready.
LEO can block payments.
LEO can sanction suppliers.
LEO guarantees source data authenticity.
LEO produces legal evidence.
```

---

# 17. Current known limitations

Current known limitations:

```text
local prototype only
manual local file loading
user-provided unverified source data
READY_WITH_WARNINGS input quality
browser localStorage review state
no production database
no cryptographic hash
no digital signature
no external timestamp
no trusted ingestion connector
no multi-user workflow
no production archive
no legal/compliance authority
```

These are documented in:

```text
LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
```

---

# 18. Future path after demo package

After this demo package, future work should be controlled.

Recommended next directions may include:

```text
1. Final demo-readiness checkpoint.
2. Optional screenshot walkthrough package.
3. Optional lightweight presentation script.
4. Pilot partner feedback collection.
5. Trusted ingestion connector planning.
6. Secure storage planning.
7. Next LEO module continuation.
```

Do not immediately return to uncontrolled deep architecture expansion.

---

# 19. Regression guard

Future updates must preserve:

```text
21 findings baseline
21 evidence objects baseline
7 suppliers baseline
RELIABILITY_GUARDED
READY_WITH_WARNINGS
USER_PROVIDED_UNVERIFIED
EXPORT_READY_WITH_WARNINGS
Executive / Reviewer / Technical View modes
Priority Review Queue
Review Completion panel
Export Readiness Gate
reviewer_workflow_hardening_summary
export_readiness_summary
zero autonomy
no production mutation
no canonical registry mutation
```

---

# 20. Package completeness checklist

Current local demo package should contain:

```text
[ ] leo_demo_dashboard.html
[ ] output\demo_evidence_report.json
[ ] README_DEMO_RUN_v0.6.md
[ ] docs\LEO_PROCUREMENT_ACCOUNTING_DEMO_STORYLINE_v0.6.md
[ ] docs\LEO_EXECUTIVE_WALKTHROUGH_FOR_OFFICIALS_v0.6.md
[ ] docs\LEO_REVIEWER_WORKFLOW_WALKTHROUGH_v0.6.md
[ ] docs\LEO_LOCAL_PROTOTYPE_LIMITATIONS_AND_PRODUCTION_READINESS_BOUNDARY_v0.1.md
[ ] docs\LEO_PROCUREMENT_ACCOUNTING_LOCAL_DEMO_PACKAGE_INDEX_v0.6.md
[ ] docs\LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_REVIEWER_WORKFLOW_HARDENING_WORKING_BASELINE_CHECKPOINT_v0.1.md
[ ] exports\human_review_packages\LEO_LOCAL_HUMAN_REVIEW_PACKAGE_v5_0_reliability_state_layer_2026-05-27_054848.json
```

The final demo-readiness checkpoint should confirm this checklist.

---

# 21. Recommended immediate next file

Recommended next file:

```text
LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_FINAL_DEMO_READINESS_CHECKPOINT_v0.1.md
```

Recommended canonical path:

```text
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\docs\LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_FINAL_DEMO_READINESS_CHECKPOINT_v0.1.md
```

Purpose:

Confirm that the v0.6 dashboard and its demo package are ready for controlled demonstration with warnings.

---

# 22. Boundary statement

This index organizes the v0.6 local demo package.

It does not authorize new functionality.

It does not alter dashboard logic.

It does not alter evidence logic.

It does not create legal conclusions.

It does not create donor compliance determinations.

It does not create fraud verdicts.

It does not approve or reject expenses.

It does not trigger enforcement.

It does not mutate source evidence.

It does not mutate production records.

It does not mutate the canonical registry.

---

# 23. Current continuation marker

After saving this index, continue with:

```text
LEO_PROCUREMENT_ACCOUNTING_DASHBOARD_V0_6_FINAL_DEMO_READINESS_CHECKPOINT_v0.1.md
```

Do not modify dashboard code by default.

Do not add new analytical layers by default.

Do not regenerate previous demo package files.

Proceed to final demo-readiness checkpoint for this procurement/accounting dashboard branch.
