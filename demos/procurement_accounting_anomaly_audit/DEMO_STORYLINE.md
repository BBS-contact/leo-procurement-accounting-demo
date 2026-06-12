# LEO Procurement / Accounting Anomaly Demo — Storyline

Canonical path:
`D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\DEMO_STORYLINE.md`

Status: DEMO STORYLINE v0.1

Demo baseline:
`leo_demo_dashboard.html v0.4 — presentation-ready local demo baseline`

---

## 1. Purpose of this document

This document provides a practical presentation storyline for explaining the LEO procurement/accounting anomaly demo to an external reviewer, advisor, technical specialist, governance specialist, auditor, donor representative, or institutional partner.

The goal is not to impress the viewer with abstract AI terminology.

The goal is to make the viewer understand:

1. what LEO does;
2. what LEO does not do;
3. why the demo matters;
4. how evidence is shown;
5. how human review works;
6. why this could be useful to real institutions.

Core presentation message:

`LEO turns institutional uncertainty into evidence, reviewer questions, accountable human review, and audit-ready memory before damage occurs.`

---

## 2. Short opening explanation

Use this opening when presenting the demo:

> LEO is a human-controlled institutional integrity and evidence review system. In this demo, it reviews procurement and accounting records, detects unusual patterns, explains why they may matter, links them to evidence IDs, and prepares them for human review. It does not accuse anyone, does not decide fraud, does not block payments, and does not replace human judgment.

Alternative shorter version:

> LEO is not an autonomous fraud detector. It is a review system that helps institutions see weak records, suspicious patterns, and missing justifications early, before they become audit, governance, donor, or legal problems.

---

## 3. What to show first

Open:

`leo_demo_dashboard.html`

Load:

`output\demo_evidence_report.json`

After loading, start with the top dashboard explanation.

Point out these three boxes:

1. `What LEO analyzes`
2. `What LEO shows`
3. `What humans decide`

Explain:

> LEO analyzes institutional records. It does not simply generate a score. It shows why a record deserves review and what question a human reviewer should ask.

Then point to:

`What LEO does not do`

Explain:

> This boundary is central. LEO does not enforce, does not punish, does not block, does not mutate production records, and does not make legal conclusions. It supports accountable review.

---

## 4. Expected dashboard numbers

After loading the current demo evidence report, the dashboard should show:

* `Findings`: `17`
* `Evidence objects`: `17`
* `Suppliers`: `7`
* `High+ risk`: `7`
* `Human-reviewed`: initially `0`
* `Autonomous actions`: `0`

How to explain these numbers:

> The demo contains 17 evidence-backed signals across 7 suppliers. Seven of these are high or critical risk. The important number is also zero: autonomous actions are zero. LEO is not executing decisions. It is preparing evidence for human review.

---

## 5. How to explain the workflow

Point to the workflow row:

`INPUT → ANALYSIS → EVIDENCE → HUMAN REVIEW → REPORT`

Explain each step:

### Input

> LEO receives procurement/accounting records, supplier information, benchmark context, and transaction facts.

### Analysis

> LEO compares values, detects mismatches, identifies unusual quantities, and groups repeated patterns such as threshold-near procurement fragments.

### Evidence

> Each signal receives an evidence ID. This means the viewer can trace what LEO is showing back to a specific evidence object.

### Human review

> A human reviewer decides whether the signal is justified, should be escalated, is a false positive, or requires more documents.

### Report

> The system generates a local review memo and an exportable human review package. This creates audit-ready memory without changing production records.

---

## 6. Explain “This is not a fraud verdict” clearly

This section should always be shown before discussing specific suppliers.

Use this wording:

> LEO does not say fraud occurred. LEO says that a record or pattern differs from expected procurement/accounting behavior and deserves human review.

Then explain:

> This distinction matters legally and institutionally. A responsible system should not accuse people automatically. It should show evidence, explain the reason, and require a human review path.

Do not skip this point.

It protects the system from being misunderstood as an automated accusation engine.

---

## 7. What LEO found — signal families

Point to the section:

`What LEO found`

Explain the signal families:

### Prices above benchmark

Expected count:

`2`

Explanation:

> LEO found records where the observed unit price is materially above the benchmark median. This does not automatically mean wrongdoing. It means the price difference should be justified by documents, quality, urgency, specification, or market conditions.

### Supplier capacity risk

Expected count:

`1`

Explanation:

> LEO found a high-value procurement assigned to a supplier with weak indicated capacity. The reviewer should ask whether the supplier can realistically deliver the required scope.

### Supplier activity mismatch

Expected count:

`9`

Explanation:

> LEO found suppliers whose declared business activity does not clearly match the purchased category. This may be explainable, but the contract file should justify why the supplier is suitable.

### Unusual quantity

Expected count:

`1`

Explanation:

> LEO found a large procurement quantity that requires operational need, delivery, and usage justification.

### Threshold fragmentation

Expected count:

`4`

Explanation:

> LEO found several threshold-near procurement fragments that should be reviewed as a cluster, not as isolated records.

---

## 8. Key example 1 — EV-001 price anomaly

Search or point to:

`EV-001`

Expected title:

`Price above benchmark`

Expected severity:

`CRITICAL`

Expected detected signal:

`Observed unit price (230.00 PLN) is 2.30x benchmark median (100.00 PLN).`

How to explain:

> This is a price review signal. LEO detected that the unit price is 2.30 times the benchmark median. That does not prove fraud. It means the institution should ask for documented justification: was the item higher quality, urgent, specialized, bundled with service, or affected by market conditions?

Point to the reviewer question:

`Is there documented justification for the price difference?`

Explain:

> This is one of LEO’s strongest design choices. It does not only show a risk label. It gives the human reviewer the question that should be answered before the institution relies on the record.

Recommended demo action:

Set `EV-001` to:

`Escalate for review`

Use this reviewer note:

`Price requires documented justification, benchmark explanation, and procurement need confirmation.`

Then show that `Human-reviewed` changes from `0` to `1`.

---

## 9. Key example 2 — MicroNova threshold fragmentation cluster

Point to:

`Pattern cluster summary`

Expected cluster:

`Threshold fragmentation cluster`

Expected supplier:

`MicroNova Trade Sp. z o.o.`

Expected evidence IDs:

* `EV-014`
* `EV-015`
* `EV-016`
* `EV-017`

Expected cumulative value:

`38500.00 PLN`

How to explain:

> This is important because LEO is not only looking at isolated records. It can show repeated pattern behavior. Here, several threshold-near fragments appear for the same supplier and related procurement context. LEO groups them into a cluster and asks whether they were split for legitimate operational reasons or whether they should be reviewed as one procurement cluster.

Point to the reviewer question:

`Were these records split for legitimate operational reasons, or should they be treated as one procurement cluster?`

Explain:

> This is not an accusation. It is a pattern-level review question. It helps the institution avoid looking at each row separately when the risk exists in the relationship between rows.

Why this example matters:

> This example shows LEO’s value beyond simple scoring. It can help reviewers notice structural patterns that are easy to miss manually.

---

## 10. Key example 3 — EV-003 supplier capacity risk

Search or point to:

`EV-003`

Expected title:

`Supplier capacity risk`

Expected severity:

`HIGH`

Expected detected signal:

`Low-capacity supplier (0.25) received high-value procurement (97500.00 PLN).`

How to explain:

> LEO detected that a supplier with weak indicated capacity received a high-value procurement. This does not mean the supplier cannot deliver. But it means the reviewer should check capacity, staffing, equipment, subcontracting, prior experience, and delivery proof.

Point to the reviewer question:

`Can the supplier prove operational capability for this value and scope?`

Explain:

> LEO converts a vague concern into a concrete review question. This is useful for governance and audit because it directs the human reviewer to the missing proof.

---

## 11. Key example 4 — EV-013 unusual quantity signal

Search or point to:

`EV-013`

Expected title:

`Unusual quantity signal`

Expected severity:

`MEDIUM`

Expected detected signal:

`Large procurement quantity detected (500 units). The operational need and delivery context should be reviewed.`

How to explain:

> LEO detected a quantity that is large enough to require justification. This may be perfectly legitimate, but the institution should be able to show why this quantity was needed, how it will be delivered, and how it will be used.

Point to the reviewer question:

`Is the quantity supported by real need, delivery plan, and usage evidence?`

Explain:

> This is a good example of LEO detecting not corruption, but weak institutional explanation. Many real risks begin as missing justification, not obvious wrongdoing.

---

## 12. How to explain supplier overview

Point to:

`Supplier risk overview`

Expected suppliers include:

* `North Bridge Office Supplies Sp. z o.o.`
* `MicroNova Trade Sp. z o.o.`
* `FreshStart Consulting Sp. z o.o.`
* `QuickBuild Technical Services Sp. z o.o.`
* `ClearMed Equipment Group Sp. z o.o.`
* `GreenLeaf Catering Sp. z o.o.`
* `MedPaper Logistics Sp. z o.o.`

How to explain:

> LEO groups evidence by supplier. This allows the reviewer to see whether risk is isolated or concentrated. A single medium signal may be low priority, but repeated findings around the same supplier may deserve closer review.

Important point:

> Supplier grouping is not a blacklist. It is a review queue.

---

## 13. How to explain the evidence object index

Point to:

`Evidence object index`

Explain:

> This table is the evidence index. It shows the evidence ID, detected signal, severity, supplier or subject, and reason text. This matters because LEO should not produce unexplained recommendations. Every signal should be traceable.

Use this principle:

`No evidence — no signal.`

Then explain:

> If a reviewer disagrees with a signal, that disagreement can be recorded. The evidence is not deleted. The human interpretation is added to the review memory.

---

## 14. How to demonstrate human review

Use `EV-001`.

Steps:

1. Search for `EV-001`.

2. Select `Escalate for review`.

3. Add the note:

   `Price requires documented justification, benchmark explanation, and procurement need confirmation.`

4. Show that the dashboard metric changes:

   `Human-reviewed: 1`

5. Explain:

> This is the human-in-the-loop part. LEO did not decide the institutional outcome. It prepared the finding, evidence, reason, question, and recommendation. The human reviewer recorded the review action and note.

---

## 15. How to explain the reviewer memo

Point to:

`Reviewer memo preview`

Explain:

> The memo converts the dashboard state into a readable review document. It includes purpose, institutional value, zero-autonomy boundary, executive summary, representative priorities, pattern clusters, supplier focus, findings, and human review actions.

Important point:

> The memo is not a legal report. It is a local review artifact that helps preserve what was seen, what was asked, and what the human reviewer did.

---

## 16. How to explain the export package

Click:

`Export human review package`

Expected exported package:

`LEO_LOCAL_HUMAN_REVIEW_PACKAGE v2.0`

Explain:

> The exported package is the machine-readable review memory. It records the findings, evidence IDs, human review action, reviewer note, and zero-autonomy boundary.

For the tested EV-001 review, the package should show:

```json
"human_review": {
  "action": "ESCALATE_FOR_REVIEW",
  "note": "Price requires documented justification, benchmark explanation, and procurement need confirmation.",
  "updatedAt": "..."
}
```

Also show the boundary:

```json
"zero_autonomy_boundary": {
  "autonomous_enforcement_actions": 0,
  "canonical_registry_opened": false,
  "canonical_registry_mutated": false,
  "production_records_mutated": false,
  "signing_or_key_access_performed": false,
  "external_execution_performed": false
}
```

Explain:

> This proves that the review action was recorded, while production and canonical systems remained untouched.

---

## 17. What not to claim during the presentation

Do not say:

`LEO detected fraud.`

Do not say:

`LEO proved corruption.`

Do not say:

`LEO automatically blocks risky procurement.`

Do not say:

`LEO replaces auditors or lawyers.`

Do not say:

`LEO is production-ready.`

Do not say:

`LEO makes final decisions.`

Correct wording:

`LEO detected evidence-backed review signals.`

`LEO identified records that require human review.`

`LEO helps structure institutional review before damage occurs.`

`LEO supports human judgment and audit-ready memory.`

---

## 18. How to answer likely questions

### Question: Is this an anti-corruption system?

Recommended answer:

> It can support anti-corruption work, but it is broader than that. LEO is an institutional integrity and evidence review system. It helps detect weak records, unexplained patterns, missing justifications, and review-worthy anomalies before they become larger problems.

### Question: Does LEO decide whether something is illegal?

Recommended answer:

> No. LEO does not make legal conclusions. It shows evidence-backed risk signals and reviewer questions. Legal interpretation remains with qualified human professionals.

### Question: Can LEO block a payment or contract?

Recommended answer:

> Not in this demo, and not by default. The design is human-controlled. LEO can support review before a decision, but it does not execute enforcement actions autonomously.

### Question: What makes this different from a dashboard?

Recommended answer:

> A normal dashboard displays data. LEO structures institutional review. It links signals to evidence, explains why they matter, asks reviewer questions, records human review decisions, and exports review memory.

### Question: What makes this different from a fraud detector?

Recommended answer:

> A fraud detector often tries to classify something as fraud or not fraud. LEO does not do that. LEO identifies review-worthy signals and preserves an accountable human review path.

### Question: Why is non-autonomy important?

Recommended answer:

> Because institutional responsibility should remain human. LEO supports review, evidence, and accountability without creating an unaccountable automated authority.

### Question: Is this ready for real deployment?

Recommended answer:

> No. This is a local prototype/demo baseline. It is ready for demonstration, expert review, and product direction validation, but not production use.

---

## 19. Suggested presentation sequence

Use this sequence for a 5–7 minute demo.

### Minute 1 — Positioning

Explain what LEO is and what it is not.

Key phrase:

`LEO is a human-controlled institutional integrity and evidence review system.`

### Minute 2 — Dashboard overview

Show the top metrics and zero-autonomy boundary.

Key phrase:

`The most important number here is also zero: autonomous actions are zero.`

### Minute 3 — Signal families

Show `What LEO found`.

Explain price, capacity, activity mismatch, quantity, and threshold fragmentation.

### Minute 4 — Concrete examples

Show:

* `EV-001` price benchmark anomaly;
* MicroNova threshold fragmentation cluster;
* `EV-003` supplier capacity risk;
* `EV-013` unusual quantity signal.

### Minute 5 — Human review

Mark `EV-001` as `Escalate for review` and add the reviewer note.

Show `Human-reviewed: 1`.

### Minute 6 — Export package

Export the package and explain that review memory is preserved without production mutation.

### Minute 7 — Closing

Explain institutional value.

Key phrase:

`LEO helps institutions make reviewable decisions before damage occurs.`

---

## 20. Suggested closing statement

Use this closing:

> The value of LEO is not that it replaces people. The value is that it helps an institution see risk earlier, ask better questions, preserve evidence, record human judgment, and create audit-ready memory. It is designed to support responsible institutions, not to become an autonomous authority.

Alternative shorter closing:

> LEO turns uncertainty into evidence, questions, and accountable human review.

---

## 21. Presentation success criteria

The presentation is successful if the viewer can explain the following after watching:

1. LEO reviews institutional records.
2. LEO detects evidence-backed risk signals.
3. LEO does not issue fraud verdicts.
4. LEO does not make legal conclusions.
5. LEO does not enforce or mutate production records.
6. Each signal has evidence and a reviewer question.
7. A human reviewer records the review action.
8. The review can be exported as a package.
9. The system is useful because it creates audit-ready institutional memory.
10. The current system is a local prototype/demo baseline, not production software.

---

## 22. Final note for presenter

Do not overclaim.

Do not present LEO as magic.

Do not present LEO as an autonomous judge.

The strongest version of LEO is disciplined, transparent, evidence-based, and human-controlled.

The correct message is:

`LEO does not replace responsibility. LEO makes responsibility visible, reviewable, and easier to preserve.`
