# LEO Procurement and Accounting Anomaly Audit — Controlled Demo Report

**Report type:** Controlled prototype demonstration  
**System:** LEO  
**Mode:** Advisory analysis only  
**Dataset:** Synthetic demonstration dataset  
**Production status:** Not production  
**Generated at:** 2026-05-09T04:34:12.150387+00:00  

## Advisory Disclaimer

This report is advisory only. It identifies patterns requiring human review. It does not establish legal wrongdoing, prove corruption, accuse any real entity, or authorize enforcement action. The dataset used in this demonstration is synthetic and controlled.

## Executive Summary

LEO processed 20 synthetic procurement records, 7 suppliers, 7 procurement item definitions, and 10 contract fragments. The system identified 17 advisory anomalies requiring human review, including 7 high/critical findings and 10 medium-risk findings. No autonomous enforcement action was taken or authorized.

All findings require human review before any institutional interpretation or action.

Autonomous enforcement actions: 0  
Canonical registry mutations: 0  
Production records modified: 0  

## Dataset Summary

| Metric | Value |
|---|---|
| Suppliers | 7 |
| Procurement items | 7 |
| Procurement records | 20 |
| Contract fragments | 10 |
| Synthetic dataset | Yes |
| Real personal data | No |
| Production data | No |

## Detection Summary

| Anomaly type | Count | Highest severity | Human review required |
|---|---|---|---|
| PRICE_ANOMALY | 2 | CRITICAL_REVIEW_REQUIRED | Yes |
| ENTITY_CAPABILITY_ANOMALY | 1 | HIGH | Yes |
| ENTITY_CATEGORY_MISMATCH | 9 | MEDIUM | Yes |
| QUANTITY_ANOMALY | 1 | MEDIUM | Yes |
| FRAGMENTATION_ANOMALY | 4 | HIGH | Yes |
| TEMPORAL_ANOMALY | 0 | NONE | No |

## High-Risk Findings

### H-001 — PRICE_ANOMALY

**Severity:** CRITICAL_REVIEW_REQUIRED  
**Source record:** REC-004  
**Supplier:** North Bridge Office Supplies Sp. z o.o.  
**Item:** A4 printer paper box  
**Observed value:** 230.0 PLN  
**Reference value:** 100.0 PLN  
**Ratio:** 2.3x reference  
**Explanation:** Observed unit price (230.00 PLN) is 2.30x benchmark median (100.00 PLN).  
**Human review recommendation:** Review benchmark source, procurement justification, and alternative market offers before any institutional conclusion.  

### H-002 — PRICE_ANOMALY

**Severity:** HIGH  
**Source record:** REC-018  
**Supplier:** QuickBuild Technical Services Sp. z o.o.  
**Item:** Minor renovation service  
**Observed value:** 15000.0 PLN  
**Reference value:** 8000.0 PLN  
**Ratio:** 1.88x reference  
**Explanation:** Observed unit price (15000.00 PLN) is 1.88x benchmark median (8000.00 PLN).  
**Human review recommendation:** Review benchmark source, procurement justification, and alternative market offers before any institutional conclusion.  

### H-003 — ENTITY_CAPABILITY_ANOMALY

**Severity:** HIGH  
**Source record:** REC-005  
**Supplier:** FreshStart Consulting Sp. z o.o.  
**Item:** Laptop computer  
**Observed value:** 97500.0 PLN  
**Reference value:** 50000.0 PLN  
**Explanation:** Low-capacity supplier (0.25) received high-value procurement (97500.00 PLN).  
**Human review recommendation:** Verify supplier capacity, registration history, staffing or delivery capability, and supporting documentation.  

### H-004 — FRAGMENTATION_ANOMALY

**Severity:** HIGH  
**Source record:** FRAG-001  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** construction_services  
**Observed value:** 9600.0 PLN  
**Reference value:** 10000.0 PLN  
**Explanation:** Multiple threshold-near fragments detected for the same supplier, department, and category. Cumulative value: 38500.00 PLN.  
**Human review recommendation:** Review related contract fragments together and verify whether the split structure has a legitimate operational explanation.  

### H-005 — FRAGMENTATION_ANOMALY

**Severity:** HIGH  
**Source record:** FRAG-002  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** construction_services  
**Observed value:** 9700.0 PLN  
**Reference value:** 10000.0 PLN  
**Explanation:** Multiple threshold-near fragments detected for the same supplier, department, and category. Cumulative value: 38500.00 PLN.  
**Human review recommendation:** Review related contract fragments together and verify whether the split structure has a legitimate operational explanation.  

### H-006 — FRAGMENTATION_ANOMALY

**Severity:** HIGH  
**Source record:** FRAG-003  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** construction_services  
**Observed value:** 9800.0 PLN  
**Reference value:** 10000.0 PLN  
**Explanation:** Multiple threshold-near fragments detected for the same supplier, department, and category. Cumulative value: 38500.00 PLN.  
**Human review recommendation:** Review related contract fragments together and verify whether the split structure has a legitimate operational explanation.  

### H-007 — FRAGMENTATION_ANOMALY

**Severity:** HIGH  
**Source record:** FRAG-004  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** construction_services  
**Observed value:** 9400.0 PLN  
**Reference value:** 10000.0 PLN  
**Explanation:** Multiple threshold-near fragments detected for the same supplier, department, and category. Cumulative value: 38500.00 PLN.  
**Human review recommendation:** Review related contract fragments together and verify whether the split structure has a legitimate operational explanation.  

## Medium-Risk Findings

### M-001 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-005  
**Supplier:** FreshStart Consulting Sp. z o.o.  
**Item:** Laptop computer  
**Explanation:** Supplier declared activity ('consulting') does not clearly align with item category ('IT_equipment'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-002 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-006  
**Supplier:** GreenLeaf Catering Sp. z o.o.  
**Item:** Medical protective gloves pack  
**Explanation:** Supplier declared activity ('catering') does not clearly align with item category ('medical_equipment'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-003 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-007  
**Supplier:** MedPaper Logistics Sp. z o.o.  
**Item:** Medical protective gloves pack  
**Explanation:** Supplier declared activity ('logistics') does not clearly align with item category ('medical_equipment'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-004 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-009  
**Supplier:** QuickBuild Technical Services Sp. z o.o.  
**Item:** Website maintenance service  
**Explanation:** Supplier declared activity ('construction_services') does not clearly align with item category ('IT_services'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-005 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-010  
**Supplier:** FreshStart Consulting Sp. z o.o.  
**Item:** Minor renovation service  
**Explanation:** Supplier declared activity ('consulting') does not clearly align with item category ('construction_services'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-006 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-013  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** Minor renovation service  
**Explanation:** Supplier declared activity ('general_trade') does not clearly align with item category ('construction_services'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-007 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-014  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** Minor renovation service  
**Explanation:** Supplier declared activity ('general_trade') does not clearly align with item category ('construction_services'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-008 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-015  
**Supplier:** MicroNova Trade Sp. z o.o.  
**Item:** Minor renovation service  
**Explanation:** Supplier declared activity ('general_trade') does not clearly align with item category ('construction_services'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-009 — ENTITY_CATEGORY_MISMATCH

**Severity:** MEDIUM  
**Source record:** REC-016  
**Supplier:** ClearMed Equipment Group Sp. z o.o.  
**Item:** Laptop computer  
**Explanation:** Supplier declared activity ('medical_equipment') does not clearly align with item category ('IT_equipment'). This may be explainable, but it requires human review.  
**Human review recommendation:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.  

### M-010 — QUANTITY_ANOMALY

**Severity:** MEDIUM  
**Source record:** REC-008  
**Supplier:** North Bridge Office Supplies Sp. z o.o.  
**Item:** Office chair  
**Observed value:** 500.0 PLN  
**Reference value:** 100.0 PLN  
**Explanation:** Large procurement quantity detected (500 units). The operational need and delivery context should be reviewed.  
**Human review recommendation:** Confirm operational need, delivery evidence, storage capacity, and approval rationale for the unusual quantity.  

## Evidence Table

| Evidence ID | Severity | Anomaly Type | Source | Supplier | Item/Category | Human Review |
|---|---|---|---|---|---|---|
| EV-001 | CRITICAL_REVIEW_REQUIRED | PRICE_ANOMALY | REC-004 | North Bridge Office Supplies Sp. z o.o. | A4 printer paper box | Yes |
| EV-002 | HIGH | PRICE_ANOMALY | REC-018 | QuickBuild Technical Services Sp. z o.o. | Minor renovation service | Yes |
| EV-003 | HIGH | ENTITY_CAPABILITY_ANOMALY | REC-005 | FreshStart Consulting Sp. z o.o. | Laptop computer | Yes |
| EV-004 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-005 | FreshStart Consulting Sp. z o.o. | Laptop computer | Yes |
| EV-005 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-006 | GreenLeaf Catering Sp. z o.o. | Medical protective gloves pack | Yes |
| EV-006 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-007 | MedPaper Logistics Sp. z o.o. | Medical protective gloves pack | Yes |
| EV-007 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-009 | QuickBuild Technical Services Sp. z o.o. | Website maintenance service | Yes |
| EV-008 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-010 | FreshStart Consulting Sp. z o.o. | Minor renovation service | Yes |
| EV-009 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-013 | MicroNova Trade Sp. z o.o. | Minor renovation service | Yes |
| EV-010 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-014 | MicroNova Trade Sp. z o.o. | Minor renovation service | Yes |
| EV-011 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-015 | MicroNova Trade Sp. z o.o. | Minor renovation service | Yes |
| EV-012 | MEDIUM | ENTITY_CATEGORY_MISMATCH | REC-016 | ClearMed Equipment Group Sp. z o.o. | Laptop computer | Yes |
| EV-013 | MEDIUM | QUANTITY_ANOMALY | REC-008 | North Bridge Office Supplies Sp. z o.o. | Office chair | Yes |
| EV-014 | HIGH | FRAGMENTATION_ANOMALY | FRAG-001 | MicroNova Trade Sp. z o.o. | construction_services | Yes |
| EV-015 | HIGH | FRAGMENTATION_ANOMALY | FRAG-002 | MicroNova Trade Sp. z o.o. | construction_services | Yes |
| EV-016 | HIGH | FRAGMENTATION_ANOMALY | FRAG-003 | MicroNova Trade Sp. z o.o. | construction_services | Yes |
| EV-017 | HIGH | FRAGMENTATION_ANOMALY | FRAG-004 | MicroNova Trade Sp. z o.o. | construction_services | Yes |

## Supplier Risk Overview

| Supplier ID | Supplier Name | Finding Count | Highest Severity | Main Concern | Human Review Priority |
|---|---|---|---|---|---|
| SUP-001 | North Bridge Office Supplies Sp. z o.o. | 2 | CRITICAL_REVIEW_REQUIRED | PRICE_ANOMALY | CRITICAL_REVIEW_REQUIRED |
| SUP-006 | MicroNova Trade Sp. z o.o. | 7 | HIGH | FRAGMENTATION_ANOMALY | HIGH |
| SUP-004 | FreshStart Consulting Sp. z o.o. | 3 | HIGH | ENTITY_CATEGORY_MISMATCH | HIGH |
| SUP-003 | QuickBuild Technical Services Sp. z o.o. | 2 | HIGH | PRICE_ANOMALY | HIGH |
| SUP-005 | GreenLeaf Catering Sp. z o.o. | 1 | MEDIUM | ENTITY_CATEGORY_MISMATCH | MEDIUM |
| SUP-007 | MedPaper Logistics Sp. z o.o. | 1 | MEDIUM | ENTITY_CATEGORY_MISMATCH | MEDIUM |
| SUP-002 | ClearMed Equipment Group Sp. z o.o. | 1 | MEDIUM | ENTITY_CATEGORY_MISMATCH | MEDIUM |

## Human Review Recommendations

- **PRICE_ANOMALY:** Review benchmark source, procurement justification, and alternative market offers before any institutional conclusion.
- **ENTITY_CAPABILITY_ANOMALY:** Verify supplier capacity, registration history, staffing or delivery capability, and supporting documentation.
- **ENTITY_CATEGORY_MISMATCH:** Verify supplier declared activity, procurement justification, and whether the supplier can legitimately provide the requested item or service.
- **QUANTITY_ANOMALY:** Confirm operational need, delivery evidence, storage capacity, and approval rationale for the unusual quantity.
- **FRAGMENTATION_ANOMALY:** Review related contract fragments together and verify whether the split structure has a legitimate operational explanation.

LEO does not execute these recommendations. They are advisory prompts for authorized human review.

## Method and Scope

This controlled demonstration applies rule-based and evidence-oriented anomaly checks to synthetic procurement/accounting records. The checks include benchmark price deviation, supplier capability concerns, category mismatch, quantity inconsistency, and fragmentation patterns. The purpose is to demonstrate advisory analysis and evidence structuring, not legal determination. Benchmark values are synthetic.

## Limitations

- The dataset is synthetic.
- Benchmark values are synthetic.
- Findings are advisory only.
- No legal conclusion is made.
- No production deployment is implied.
- No autonomous action is performed.
- Human review is mandatory.
- Real-world deployment would require legal, security, data protection, and institutional validation.

## Non-Autonomous Boundary Statement

LEO does not execute institutional actions in this demonstration. LEO does not make binding institutional decisions in this demonstration. LEO does not execute enforcement actions, mutate production records, open canonical registries, append canonical truth, access cryptographic keys, or replace human judgment. The final authority remains with authorized human reviewers.

## Appendix: Machine Output References

Companion technical outputs:

- demo_evidence_report.json
- demo_anomaly_table.csv
