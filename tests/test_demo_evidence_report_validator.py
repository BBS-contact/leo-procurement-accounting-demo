r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\tests\test_demo_evidence_report_validator.py

Status:
Pytest coverage for demo_evidence_report_validator.py v0.1.

Purpose:
Verify that the generated evidence report validator accepts the current valid
LEO procurement/accounting generated report and rejects malformed, unsafe, or
non-dashboard-compatible report payloads.

Boundary:
- Test-only validation.
- Local temporary files only.
- No production mutation.
- No canonical registry access or mutation.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest


RUNTIME_DIR = Path(__file__).resolve().parents[1]
DEMO_DIR = RUNTIME_DIR / "demos" / "procurement_accounting_anomaly_audit"
INPUT_DIR = DEMO_DIR / "input"
OUTPUT_FILE = DEMO_DIR / "output" / "demo_evidence_report.json"

if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

import procurement_accounting_input_pipeline as pipeline  # noqa: E402
import demo_evidence_report_validator as validator  # noqa: E402


@pytest.fixture(scope="module")
def valid_report_payload() -> dict:
    pipeline.run_pipeline(INPUT_DIR, OUTPUT_FILE)
    with OUTPUT_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_valid_generated_report_file_passes_validation(valid_report_payload: dict) -> None:
    result = validator.validate_report_file(OUTPUT_FILE)

    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == []
    assert result.summary["report_id"] == "LOCAL_DEMO_REPORT"
    assert result.summary["findings_count"] == 21
    assert result.summary["evidence_count"] == 21
    assert result.summary["supplier_count"] == 7
    assert result.summary["high_or_critical_findings_count"] == 7


def test_valid_generated_report_payload_passes_validation(valid_report_payload: dict) -> None:
    result = validator.validate_report_payload(valid_report_payload)

    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == []
    assert result.summary["signal_families"] == {
        "price_above_benchmark": 2,
        "unusual_quantity_signal": 2,
        "supplier_activity_mismatch": 12,
        "supplier_capacity_risk": 1,
        "threshold_fragmentation_pattern": 4,
    }


def test_missing_report_file_fails_validation(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing_demo_evidence_report.json"

    result = validator.validate_report_file(missing_file)

    assert result.is_valid is False
    assert_error_code(result, "REPORT_FILE_MISSING")


def test_invalid_json_file_fails_validation(tmp_path: Path) -> None:
    broken_file = tmp_path / "broken_demo_evidence_report.json"
    broken_file.write_text("{not valid json", encoding="utf-8")

    result = validator.validate_report_file(broken_file)

    assert result.is_valid is False
    assert_error_code(result, "REPORT_JSON_INVALID")


def test_missing_top_level_field_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    del payload["summary"]

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "TOP_LEVEL_FIELD_MISSING")


def test_invalid_summary_count_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["summary"]["findings_count"] = 999

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "SUMMARY_FINDINGS_COUNT_MISMATCH")


def test_corrupted_zero_autonomy_boundary_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["zero_autonomy_boundary"]["production_records_mutated"] = True

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "ZERO_AUTONOMY_FIELD_NOT_FALSE")


def test_autonomous_enforcement_action_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["zero_autonomy_boundary"]["autonomous_enforcement_actions"] = 1

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "AUTONOMOUS_ENFORCEMENT_NOT_ZERO")


def test_missing_dashboard_alias_field_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    del payload["findings"][0]["reason"]

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "DASHBOARD_ALIAS_FIELD_MISSING")


def test_mismatched_dashboard_reason_alias_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["findings"][0]["reason"] = "Different text"

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "DASHBOARD_REASON_ALIAS_MISMATCH")


def test_invalid_finding_severity_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["findings"][0]["severity"] = "SEVERE"
    payload["findings"][0]["risk_level"] = "SEVERE"

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "FINDING_SEVERITY_INVALID")


def test_signal_family_count_mismatch_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["summary"]["signal_families"]["price_above_benchmark"] = 99

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "SUMMARY_SIGNAL_FAMILY_COUNTS_MISMATCH")


def test_evidence_and_findings_id_mismatch_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["evidence"][0]["id"] = "EV-999"

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "EVIDENCE_FINDING_IDS_MISMATCH")


def test_forbidden_verdict_phrase_fails_validation(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["findings"][0]["detected_signal"] = "Fraud occurred in this transaction."
    payload["findings"][0]["reason"] = payload["findings"][0]["detected_signal"]
    payload["findings"][0]["description"] = payload["findings"][0]["detected_signal"]

    result = validator.validate_report_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "FORBIDDEN_VERDICT_PHRASE_FOUND")


def test_empty_evidence_and_findings_emit_warnings_not_errors(valid_report_payload: dict) -> None:
    payload = deepcopy(valid_report_payload)
    payload["evidence"] = []
    payload["findings"] = []
    payload["summary"]["findings_count"] = 0
    payload["summary"]["evidence_count"] = 0
    payload["summary"]["supplier_count"] = 0
    payload["summary"]["high_or_critical_findings_count"] = 0
    payload["summary"]["signal_families"] = {}

    result = validator.validate_report_payload(payload)

    assert result.is_valid is True
    assert_error_code_absent(result, "SUMMARY_FINDINGS_COUNT_MISMATCH")
    assert_warning_code(result, "EVIDENCE_EMPTY")
    assert_warning_code(result, "FINDINGS_EMPTY")


def assert_error_code(result: validator.ValidationResult, code: str) -> None:
    assert code in {issue.code for issue in result.errors}, result.to_dict()


def assert_error_code_absent(result: validator.ValidationResult, code: str) -> None:
    assert code not in {issue.code for issue in result.errors}, result.to_dict()


def assert_warning_code(result: validator.ValidationResult, code: str) -> None:
    assert code in {issue.code for issue in result.warnings}, result.to_dict()
