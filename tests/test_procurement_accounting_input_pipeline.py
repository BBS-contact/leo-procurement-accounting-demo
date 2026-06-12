r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\tests\test_procurement_accounting_input_pipeline.py

Status:
Pytest coverage for the local LEO procurement/accounting input pipeline v0.1.

Purpose:
Verify that the local read-only CSV input pipeline can generate a dashboard-compatible
LEO evidence report from sample institutional records without autonomous enforcement,
canonical registry mutation, production mutation, key access, or external execution.

Boundary:
- Test-only validation.
- Local sample CSV data only.
- No production mutation.
- No canonical registry access or mutation.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


RUNTIME_DIR = Path(__file__).resolve().parents[1]
DEMO_DIR = RUNTIME_DIR / "demos" / "procurement_accounting_anomaly_audit"
INPUT_DIR = DEMO_DIR / "input"
OUTPUT_FILE = DEMO_DIR / "output" / "demo_evidence_report.json"

if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

import procurement_accounting_input_pipeline as pipeline  # noqa: E402


EXPECTED_SIGNAL_FAMILIES = {
    "price_above_benchmark": 2,
    "supplier_capacity_risk": 1,
    "supplier_activity_mismatch": 12,
    "unusual_quantity_signal": 2,
    "threshold_fragmentation_pattern": 4,
}


@pytest.fixture(scope="module")
def generated_report() -> dict:
    result = pipeline.run_pipeline(INPUT_DIR, OUTPUT_FILE)
    assert result.summary["findings_count"] == 21
    assert OUTPUT_FILE.exists()

    with OUTPUT_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_required_sample_input_files_exist() -> None:
    assert (INPUT_DIR / "procurement_records.csv").exists()
    assert (INPUT_DIR / "supplier_profiles.csv").exists()
    assert (INPUT_DIR / "price_benchmarks.csv").exists()


def test_pipeline_generates_dashboard_compatible_report(generated_report: dict) -> None:
    assert generated_report["report_id"] == "LOCAL_DEMO_REPORT"
    assert generated_report["source_name"] == "procurement_accounting_input_pipeline.py"
    assert generated_report["generated_at"]
    assert isinstance(generated_report["evidence"], list)
    assert isinstance(generated_report["findings"], list)
    assert len(generated_report["evidence"]) == 21
    assert len(generated_report["findings"]) == 21


def test_summary_matches_pipeline_generated_baseline(generated_report: dict) -> None:
    summary = generated_report["summary"]

    assert summary["findings_count"] == 21
    assert summary["evidence_count"] == 21
    assert summary["supplier_count"] == 7
    assert summary["high_or_critical_findings_count"] == 7
    assert summary["reviewed_findings_count"] == 0
    assert summary["signal_families"] == EXPECTED_SIGNAL_FAMILIES


def test_zero_autonomy_boundary_is_clean(generated_report: dict) -> None:
    boundary = generated_report["zero_autonomy_boundary"]

    assert boundary["autonomous_enforcement_actions"] == 0
    assert boundary["canonical_registry_opened"] is False
    assert boundary["canonical_registry_mutated"] is False
    assert boundary["production_records_mutated"] is False
    assert boundary["signing_or_key_access_performed"] is False
    assert boundary["external_execution_performed"] is False
    assert boundary["pipeline_mode"] == "LOCAL_READ_ONLY_DEMO"


def test_every_finding_has_dashboard_compatible_fields(generated_report: dict) -> None:
    for finding in generated_report["findings"]:
        assert finding["id"].startswith("EV-")
        assert finding["title"]
        assert finding["severity"] in {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
        assert finding["supplier"]
        assert finding["subject"]
        assert finding["detected_signal"]
        assert finding["reason"] == finding["detected_signal"]
        assert finding["description"] == finding["detected_signal"]
        assert finding["type"] == "EVIDENCE_OBJECT"
        assert finding["signal_title"] == finding["title"]
        assert finding["risk_level"] == finding["severity"]
        assert finding["risk_meaning"]
        assert finding["reviewer_question"]
        assert finding["recommendation"]
        assert finding["recommended_action"] == finding["recommendation"]
        assert finding["evidence_ids"] == [finding["id"]]
        assert finding["source_records"]
        assert finding["signal_family"]


def test_ev001_price_above_benchmark_is_present(generated_report: dict) -> None:
    ev001 = finding_by_id(generated_report, "EV-001")

    assert ev001["title"] == "Price above benchmark"
    assert ev001["severity"] == "CRITICAL"
    assert ev001["supplier"] == "North Bridge Office Supplies Sp. z o.o."
    assert "2.30x benchmark median" in ev001["detected_signal"]
    assert ev001["reviewer_question"] == "Is there documented justification for the price difference?"
    assert ev001["signal_family"] == "price_above_benchmark"


def test_ev003_second_price_signal_is_present(generated_report: dict) -> None:
    ev003 = finding_by_id(generated_report, "EV-003")

    assert ev003["title"] == "Price above benchmark"
    assert ev003["severity"] == "HIGH"
    assert ev003["supplier"] == "QuickBuild Technical Services Sp. z o.o."
    assert "1.88x benchmark median" in ev003["detected_signal"]
    assert ev003["signal_family"] == "price_above_benchmark"


def test_ev005_supplier_capacity_risk_is_present(generated_report: dict) -> None:
    ev005 = finding_by_id(generated_report, "EV-005")

    assert ev005["title"] == "Supplier capacity risk"
    assert ev005["severity"] == "HIGH"
    assert ev005["supplier"] == "FreshStart Consulting Sp. z o.o."
    assert "Low-capacity supplier (0.25)" in ev005["detected_signal"]
    assert ev005["reviewer_question"] == "Can the supplier prove operational capability for this value and scope?"
    assert ev005["signal_family"] == "supplier_capacity_risk"


def test_unusual_quantity_signals_are_present(generated_report: dict) -> None:
    quantity_findings = findings_by_family(generated_report, "unusual_quantity_signal")

    assert len(quantity_findings) == 2
    assert {finding["id"] for finding in quantity_findings} == {"EV-002", "EV-016"}
    assert all(finding["title"] == "Unusual quantity signal" for finding in quantity_findings)
    assert all("Large procurement quantity detected" in finding["detected_signal"] for finding in quantity_findings)


def test_supplier_activity_mismatch_count_and_examples(generated_report: dict) -> None:
    activity_findings = findings_by_family(generated_report, "supplier_activity_mismatch")

    assert len(activity_findings) == 12
    assert finding_by_id(generated_report, "EV-004")["supplier"] == "QuickBuild Technical Services Sp. z o.o."
    assert finding_by_id(generated_report, "EV-006")["supplier"] == "FreshStart Consulting Sp. z o.o."
    assert finding_by_id(generated_report, "EV-015")["supplier"] == "ClearMed Equipment Group Sp. z o.o."


def test_micronova_threshold_fragmentation_cluster_is_present(generated_report: dict) -> None:
    cluster_findings = findings_by_family(generated_report, "threshold_fragmentation_pattern")

    assert len(cluster_findings) == 4
    assert {finding["id"] for finding in cluster_findings} == {"EV-018", "EV-019", "EV-020", "EV-021"}
    assert all(finding["supplier"] == "MicroNova Trade Sp. z o.o." for finding in cluster_findings)
    assert all(finding["severity"] == "HIGH" for finding in cluster_findings)
    assert all("Cumulative value: 38500.00 PLN" in finding["detected_signal"] for finding in cluster_findings)
    assert all(
        finding["reviewer_question"]
        == "Were these records split for legitimate operational reasons, or should they be treated as one procurement cluster?"
        for finding in cluster_findings
    )


def test_high_or_critical_findings_count_matches_actual_findings(generated_report: dict) -> None:
    high_or_critical = [
        finding for finding in generated_report["findings"] if finding["severity"] in {"HIGH", "CRITICAL"}
    ]

    assert len(high_or_critical) == generated_report["summary"]["high_or_critical_findings_count"]
    assert len(high_or_critical) == 7


def test_no_fraud_or_legal_verdict_fields_are_emitted(generated_report: dict) -> None:
    serialized = json.dumps(generated_report, ensure_ascii=False).lower()

    forbidden_phrases = [
        "fraud occurred",
        "corruption proved",
        "legal conclusion issued",
        "payment blocked",
        "supplier punished",
        "autonomous enforcement performed",
    ]

    for phrase in forbidden_phrases:
        assert phrase not in serialized


def finding_by_id(report: dict, finding_id: str) -> dict:
    for finding in report["findings"]:
        if finding["id"] == finding_id:
            return finding
    raise AssertionError(f"Finding not found: {finding_id}")


def findings_by_family(report: dict, signal_family: str) -> list[dict]:
    return [finding for finding in report["findings"] if finding["signal_family"] == signal_family]
