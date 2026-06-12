r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\tests\test_human_review_package_validator.py

Status:
Pytest coverage for human_review_package_validator.py v0.1.

Purpose:
Verify that the LEO human review package validator accepts a valid exported
human review package and rejects malformed, unsafe, or internally inconsistent
package payloads.

Boundary:
- Test-only validation.
- Local package fixture only.
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
PACKAGE_FILE = DEMO_DIR / "leo_human_review_package_LOCAL_DEMO_REPORT.json"

if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

import human_review_package_validator as validator  # noqa: E402


@pytest.fixture(scope="module")
def valid_package_payload() -> dict:
    assert PACKAGE_FILE.exists(), (
        "Expected exported human review package fixture is missing: "
        f"{PACKAGE_FILE}. Export it from leo_demo_dashboard.html before running this test."
    )
    with PACKAGE_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_valid_reviewed_package_file_passes_validation(valid_package_payload: dict) -> None:
    result = validator.validate_package_file(PACKAGE_FILE)

    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == []
    assert result.summary["package_type"] == "LEO_LOCAL_HUMAN_REVIEW_PACKAGE"
    assert result.summary["package_version"] == "v2.0"
    assert result.summary["source_report_id"] == "LOCAL_DEMO_REPORT"
    assert result.summary["findings_count"] == 21
    assert result.summary["evidence_count"] == 21
    assert result.summary["supplier_count"] == 7
    assert result.summary["high_or_critical_findings_count"] == 7
    assert result.summary["reviewed_findings_count"] == 1


def test_valid_reviewed_package_payload_passes_validation(valid_package_payload: dict) -> None:
    result = validator.validate_package_payload(valid_package_payload)

    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == []


def test_valid_package_contains_expected_reviewed_ev001(valid_package_payload: dict) -> None:
    ev001 = finding_by_id(valid_package_payload, "EV-001")

    assert ev001["title"] == "Price above benchmark"
    assert ev001["severity"] == "CRITICAL"
    assert ev001["supplier"] == "North Bridge Office Supplies Sp. z o.o."
    assert ev001["human_review"]["action"] == "ESCALATE_FOR_REVIEW"
    assert (
        ev001["human_review"]["note"]
        == "Price requires documented justification, benchmark explanation, and procurement need confirmation."
    )
    assert ev001["human_review"]["updatedAt"]


def test_missing_package_file_fails_validation(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing_human_review_package.json"

    result = validator.validate_package_file(missing_file)

    assert result.is_valid is False
    assert_error_code(result, "PACKAGE_FILE_MISSING")


def test_invalid_json_file_fails_validation(tmp_path: Path) -> None:
    broken_file = tmp_path / "broken_human_review_package.json"
    broken_file.write_text("{not valid json", encoding="utf-8")

    result = validator.validate_package_file(broken_file)

    assert result.is_valid is False
    assert_error_code(result, "PACKAGE_JSON_INVALID")


def test_wrong_package_type_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["package_type"] = "WRONG_PACKAGE"

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "PACKAGE_TYPE_INVALID")


def test_wrong_package_version_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["package_version"] = "v0.0"

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "PACKAGE_VERSION_INVALID")


def test_wrong_source_report_id_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["source_report_id"] = "OTHER_REPORT"

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "SOURCE_REPORT_ID_INVALID")


def test_missing_top_level_field_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    del payload["summary"]

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "TOP_LEVEL_FIELD_MISSING")


def test_summary_findings_count_mismatch_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["summary"]["findings_count"] = 999

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "SUMMARY_FINDINGS_COUNT_MISMATCH")


def test_reviewed_findings_count_mismatch_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["summary"]["reviewed_findings_count"] = 0

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "SUMMARY_REVIEWED_COUNT_MISMATCH")


def test_corrupted_zero_autonomy_boundary_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["zero_autonomy_boundary"]["canonical_registry_mutated"] = True

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "ZERO_AUTONOMY_FIELD_NOT_FALSE")


def test_autonomous_enforcement_action_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["zero_autonomy_boundary"]["autonomous_enforcement_actions"] = 1

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "AUTONOMOUS_ENFORCEMENT_NOT_ZERO")


def test_invalid_human_review_action_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["findings"][0]["human_review"]["action"] = "APPROVE_PAYMENT"

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "HUMAN_REVIEW_ACTION_INVALID")


def test_reviewed_finding_without_note_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    ev001 = payload["findings"][0]
    ev001["human_review"]["action"] = "ESCALATE_FOR_REVIEW"
    ev001["human_review"]["note"] = ""
    ev001["human_review"]["updatedAt"] = "2026-05-10T08:00:19.507Z"

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "REVIEWED_FINDING_NOTE_MISSING")


def test_reviewed_finding_without_updated_at_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    ev001 = payload["findings"][0]
    ev001["human_review"]["action"] = "ESCALATE_FOR_REVIEW"
    ev001["human_review"]["note"] = "Valid reviewer note."
    ev001["human_review"]["updatedAt"] = None

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "REVIEWED_FINDING_UPDATED_AT_MISSING")


def test_duplicate_finding_id_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["findings"][1]["id"] = payload["findings"][0]["id"]

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "FINDING_ID_DUPLICATE")


def test_invalid_severity_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["findings"][0]["severity"] = "SEVERE"

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "FINDING_SEVERITY_INVALID")


def test_forbidden_verdict_phrase_fails_validation(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    payload["findings"][0]["detected_signal"] = "Fraud occurred in this procurement."

    result = validator.validate_package_payload(payload)

    assert result.is_valid is False
    assert_error_code(result, "FORBIDDEN_VERDICT_PHRASE_FOUND")


def test_unreviewed_finding_with_note_emits_warning_not_error(valid_package_payload: dict) -> None:
    payload = deepcopy(valid_package_payload)
    ev002 = finding_by_id(payload, "EV-002")
    ev002["human_review"]["action"] = "UNREVIEWED"
    ev002["human_review"]["note"] = "Unexpected note on unreviewed finding."

    result = validator.validate_package_payload(payload)

    assert result.is_valid is True
    assert_warning_code(result, "UNREVIEWED_FINDING_HAS_NOTE")


def finding_by_id(package: dict, finding_id: str) -> dict:
    for finding in package["findings"]:
        if finding["id"] == finding_id:
            return finding
    raise AssertionError(f"Finding not found: {finding_id}")


def assert_error_code(result: validator.ValidationResult, code: str) -> None:
    assert code in {issue.code for issue in result.errors}, result.to_dict()


def assert_warning_code(result: validator.ValidationResult, code: str) -> None:
    assert code in {issue.code for issue in result.warnings}, result.to_dict()
