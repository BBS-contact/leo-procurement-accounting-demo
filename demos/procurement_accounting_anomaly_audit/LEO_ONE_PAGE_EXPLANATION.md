# LEO — One-Page Explanation

Canonical path:
`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\LEO_ONE_PAGE_EXPLANATION.md`

Status: ONE-PAGE EXPLANATION v0.1

Demo baseline:
`leo_demo_dashboard.html v0.4 — presentation-ready local demo baseline`

---

## 1. What LEO is

LEO is a human-controlled institutional integrity and evidence review system.

It helps an institution review procurement, accounting, governance, and decision records by detecting review-worthy patterns, explaining why they matter, linking them to evidence, and preparing them for accountable human review.

LEO is not designed to replace people.

LEO is designed to make institutional responsibility more visible, reviewable, and easier to preserve.

Core formulation:

`LEO turns institutional uncertainty into evidence, reviewer questions, accountable human review, and audit-ready memory before damage occurs.`

---

## 2. The problem LEO addresses

Many institutional failures do not start as obvious fraud.

They often start as weak records, missing explanations, unclear supplier suitability, undocumented price differences, fragmented procurement decisions, or decisions that cannot be reconstructed later.

Common institutional problems include:

* procurement prices that are not compared to benchmarks;
* suppliers whose activity or capacity is not clearly suitable for the procurement;
* repeated threshold-near purchases that are reviewed separately instead of as a pattern;
* large quantities without operational justification;
* audit trails that are incomplete or hard to reconstruct;
* decisions that depend on informal memory instead of documented evidence;
* honest staff lacking tools to detect and document risk early.

Traditional audit often happens after damage occurs.

LEO is intended to support review before damage occurs.

---

## 3. What LEO does differently

LEO does not only display data.

LEO structures review.

For each risk signal, LEO aims to provide:

1. detected signal;
2. evidence ID or evidence lineage;
3. reason text;
4. risk meaning;
5. reviewer question;
6. recommended human review action;
7. explicit non-verdict boundary;
8. exportable review memory.

This means LEO does not merely say:

`Risk: HIGH`

It should help the reviewer understand:

`What was detected?`

`Why does it matter?`

`What evidence supports it?`

`What should a human verify next?`

`What did the human reviewer decide?`

---

## 4. What LEO is not

LEO is not an autonomous fraud detector.

LEO is not an enforcement engine.

LEO is not a legal decision-maker.

LEO is not a payment-blocking system.

LEO is not a replacement for auditors, accountants, lawyers, managers, boards, or institutional officers.

LEO does not state that fraud occurred.

LEO states that a record or pattern differs from expected procurement/accounting behavior and deserves human review.

Correct interpretation:

`LEO identified evidence-backed review signals that require human evaluation.`

---

## 5. Why non-autonomy is a strength

Non-autonomy is not a limitation of LEO.

It is a design principle.

Institutions need accountability, not unaccountable automated authority.

LEO is designed to support human responsibility by showing evidence, asking the right review questions, and recording human decisions without automatically enforcing outcomes.

Default boundaries:

* no autonomous enforcement;
* no fraud verdict;
* no legal conclusion;
* no payment blocking;
* no supplier punishment;
* no production mutation;
* no canonical registry mutation;
* no signing/key access;
* no external execution.

This makes LEO more suitable for sensitive institutional settings where evidence, proportionality, due process, and human responsibility matter.

---

## 6. Current demo example

The current local demo is a procurement/accounting anomaly review dashboard.

Path:

`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\leo_demo_dashboard.html`

The demo loads:

`output\demo_evidence_report.json`

Confirmed demo results:

* `17` findings;
* `17` evidence objects;
* `7` suppliers;
* `7` high or critical risk findings;
* `0` autonomous actions;
* `0` production mutations;
* `0` canonical registry mutations.

The dashboard shows:

* price benchmark anomalies;
* supplier capacity risk;
* supplier activity mismatch;
* unusual quantity signal;
* threshold fragmentation pattern;
* supplier-level risk overview;
* evidence object index;
* reviewer questions;
* human review actions;
* exportable review package.

---

## 7. Example findings from the demo

### Price above benchmark

Evidence:

`EV-001`

Signal:

`Observed unit price (230.00 PLN) is 2.30x benchmark median (100.00 PLN).`

Reviewer question:

`Is there documented justification for the price difference?`

Interpretation:

This is not a fraud verdict. It is a price justification review signal.

### Threshold fragmentation cluster

Supplier:

`MicroNova Trade Sp. z o.o.`

Evidence:

`EV-014`, `EV-015`, `EV-016`, `EV-017`

Signal:

Multiple threshold-near fragments detected for the same supplier, department, and category.

Reviewer question:

`Were these records split for legitimate operational reasons, or should they be treated as one procurement cluster?`

Interpretation:

This shows LEO can identify a repeated pattern, not only isolated row-level anomalies.

### Supplier capacity risk

Evidence:

`EV-003`

Signal:

`Low-capacity supplier (0.25) received high-value procurement (97500.00 PLN).`

Reviewer question:

`Can the supplier prove operational capability for this value and scope?`

Interpretation:

This is a capability verification signal, not a conclusion that the supplier failed.

### Unusual quantity signal

Evidence:

`EV-013`

Signal:

`Large procurement quantity detected (500 units). The operational need and delivery context should be reviewed.`

Reviewer question:

`Is the quantity supported by real need, delivery plan, and usage evidence?`

Interpretation:

This is a documentation and operational justification signal.

---

## 8. Human review and export package

The demo supports a local human review workflow.

A reviewer can mark a finding as:

* `Accept as justified`;
* `Escalate for review`;
* `Mark false positive`;
* `Needs more evidence`.

In the tested demo cycle, `EV-001` was marked as:

`ESCALATE_FOR_REVIEW`

with the reviewer note:

`Price requires documented justification, benchmark explanation, and procurement need confirmation.`

The dashboard exported a human review package:

`LEO_LOCAL_HUMAN_REVIEW_PACKAGE v2.0`

The package confirmed:

* `reviewed_findings_count`: `1`;
* `EV-001` human review action: `ESCALATE_FOR_REVIEW`;
* no autonomous enforcement;
* no canonical registry mutation;
* no production mutation;
* no signing/key access;
* no external execution.

This demonstrates the full cycle:

`INPUT → ANALYSIS → EVIDENCE → HUMAN REVIEW → EXPORTABLE REPORT`

---

## 9. Why LEO could be useful

LEO could be useful for institutions that need to improve reviewability, governance discipline, and evidence-based decision support.

Potential users include:

* foundations;
* non-profit organizations;
* public institutions;
* municipalities;
* schools and universities;
* hospitals;
* humanitarian organizations;
* donor-funded projects;
* internal audit teams;
* compliance teams;
* procurement review teams;
* governance boards.

LEO can help these institutions:

* detect weak records earlier;
* ask better review questions;
* document risk before decisions are finalized;
* preserve review memory;
* reduce audit reconstruction problems;
* support donor trust;
* protect honest staff by showing that risk was noticed and reviewed;
* create a disciplined human review process.

---

## 10. Current maturity level

The current system is a local prototype/demo baseline.

It is suitable for:

* demonstration;
* expert discussion;
* product direction validation;
* governance and audit feedback;
* technical review;
* early pilot design.

It is not yet suitable for:

* production deployment;
* live procurement integration;
* automated enforcement;
* legal reliance;
* operational payment blocking;
* canonical registry mutation;
* external system execution.

The correct next step is not to overclaim maturity.

The correct next step is to build a clear presentation/readiness package, obtain expert review, and then design a controlled pilot scope.

---

## 11. Strategic value

The strategic value of LEO is not that it is “AI that decides.”

The strategic value is that it can become infrastructure for responsible institutional review.

LEO can help institutions move from:

`unclear records → structured evidence`

`vague suspicion → reviewer question`

`hidden risk → visible review queue`

`untraceable decision → audit-ready memory`

`automated claim → human accountability`

This is the core reason LEO can matter.

---

## 12. Short final summary

LEO is a human-controlled system for institutional integrity, evidence review, and audit-ready memory.

It does not accuse, enforce, or replace human authority.

It helps institutions detect review-worthy risks early, explain them clearly, preserve evidence, ask better questions, and record human judgment before damage occurs.

Short version:

`LEO turns uncertainty into evidence, questions, and accountable human review.`
