r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\human_review_package_validator.py

Status:
Human review package validator v0.1 for the LEO procurement/accounting anomaly demo.

Purpose:
Validate an exported LEO local human review package independently of the dashboard.

The validator checks:
- package JSON file existence and parseability;
- package identity fields;
- source report identity;
- summary consistency;
- zero-autonomy boundary;
- findings list consistency;
- human_review object presence and validity;
- reviewed findings count consistency;
- dashboard/export-compatible finding fields;
- absence of forbidden legal/fraud/enforcement verdict phrases.

Boundary:
- Validation only.
- No production mutation.
- No canonical registry access.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.
- No legal/fraud conclusion.

Run from the demo folder:
python human_review_package_validator.py leo_human_review_package_LOCAL_DEMO_REPORT.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PACKAGE_PATH = BASE_DIR / "leo_human_review_package_LOCAL_DEMO_REPORT.json"

EXPECTED_PACKAGE_TYPE = "LEO_LOCAL_HUMAN_REVIEW_PACKAGE"
EXPECTED_PACKAGE_VERSION = "v2.0"
EXPECTED_SOURCE_REPORT_ID = "LOCAL_DEMO_REPORT"

VALID_HUMAN_REVIEW_ACTIONS = {
    "UNREVIEWED",
    "ACCEPT_AS_JUSTIFIED",
    "ESCALATE_FOR_REVIEW",
    "MARK_FALSE_POSITIVE",
    "NEEDS_MORE_EVIDENCE",
}

REVIEWED_ACTIONS = VALID_HUMAN_REVIEW_ACTIONS - {"UNREVIEWED"}

REQUIRED_TOP_LEVEL_FIELDS = {
    "package_type",
    "package_version",
    "source_report_id",
    "source_name",
    "exported_at",
    "zero_autonomy_boundary",
    "summary",
    "findings",
}

REQUIRED_SUMMARY_FIELDS = {
    "findings_count",
    "evidence_count",
    "supplier_count",
    "high_or_critical_findings_count",
    "reviewed_findings_count",
}

REQUIRED_ZERO_AUTONOMY_FIELDS = {
    "autonomous_enforcement_actions",
    "canonical_registry_opened",
    "canonical_registry_mutated",
    "production_records_mutated",
    "signing_or_key_access_performed",
    "external_execution_performed",
}

REQUIRED_FINDING_FIELDS = {
    "id",
    "title",
    "severity",
    "supplier",
    "subject",
    "detected_signal",
    "risk_meaning",
    "reviewer_question",
    "recommendation",
    "evidence_ids",
    "human_review",
}

FORBIDDEN_VERDICT_PHRASES = {
    "fraud occurred",
    "fraud proven",
    "corruption proved",
    "corruption proven",
    "legal conclusion issued",
    "payment blocked",
    "supplier punished",
    "autonomous enforcement performed",
    "guilty supplier",
    "illegal transaction confirmed",
}

ALLOWED_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    location: str


@dataclass
class ValidationResult:
    is_valid: bool
    package_path: str
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

    def add_error(self, code: str, message: str, location: str) -> None:
        self.errors.append(ValidationIssue(code=code, message=message, location=location))
        self.is_valid = False

    def add_warning(self, code: str, message: str, location: str) -> None:
        self.warnings.append(ValidationIssue(code=code, message=message, location=location))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "package_path": self.package_path,
            "summary": self.summary,
            "errors": [issue.__dict__ for issue in self.errors],
            "warnings": [issue.__dict__ for issue in self.warnings],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a LEO local human review package JSON file.")
    parser.add_argument(
        "package_path",
        nargs="?",
        default=str(DEFAULT_PACKAGE_PATH),
        help="Path to exported human review package JSON.",
    )
    args = parser.parse_args()

    result = validate_package_file(Path(args.package_path))
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    if not result.is_valid:
        raise SystemExit(1)


def validate_package_file(package_path: Path) -> ValidationResult:
    result = ValidationResult(is_valid=True, package_path=str(package_path))

    if not package_path.exists():
        result.add_error("PACKAGE_FILE_MISSING", f"Package file does not exist: {package_path}", "package_path")
        return result

    try:
        with package_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        result.add_error("PACKAGE_JSON_INVALID", f"Invalid JSON: {exc}", "package_path")
        return result

    validate_package_payload(payload, result)
    return result


def validate_package_payload(payload: Any, result: Optional[ValidationResult] = None) -> ValidationResult:
    if result is None:
        result = ValidationResult(is_valid=True, package_path="<in-memory>")

    if not isinstance(payload, dict):
        result.add_error("PACKAGE_NOT_OBJECT", "Package payload must be a JSON object.", "$")
        return result

    validate_top_level_fields(payload, result)
    if result.errors:
        return result

    validate_identity_fields(payload, result)
    validate_summary(payload["summary"], payload, result)
    validate_zero_autonomy_boundary(payload["zero_autonomy_boundary"], result)
    validate_findings(payload["findings"], payload["summary"], result)
    validate_forbidden_verdict_phrases(payload, result)
    collect_result_summary(payload, result)

    return result


def validate_top_level_fields(payload: Mapping[str, Any], result: ValidationResult) -> None:
    missing = REQUIRED_TOP_LEVEL_FIELDS - set(payload.keys())
    for field_name in sorted(missing):
        result.add_error("TOP_LEVEL_FIELD_MISSING", f"Missing top-level field: {field_name}", f"$.{field_name}")

    if "summary" in payload and not isinstance(payload["summary"], dict):
        result.add_error("SUMMARY_INVALID", "summary must be an object.", "$.summary")

    if "zero_autonomy_boundary" in payload and not isinstance(payload["zero_autonomy_boundary"], dict):
        result.add_error(
            "ZERO_AUTONOMY_BOUNDARY_INVALID",
            "zero_autonomy_boundary must be an object.",
            "$.zero_autonomy_boundary",
        )

    if "findings" in payload and not isinstance(payload["findings"], list):
        result.add_error("FINDINGS_INVALID", "findings must be a list.", "$.findings")


def validate_identity_fields(payload: Mapping[str, Any], result: ValidationResult) -> None:
    if payload.get("package_type") != EXPECTED_PACKAGE_TYPE:
        result.add_error(
            "PACKAGE_TYPE_INVALID",
            f"package_type must be {EXPECTED_PACKAGE_TYPE}.",
            "$.package_type",
        )

    if payload.get("package_version") != EXPECTED_PACKAGE_VERSION:
        result.add_error(
            "PACKAGE_VERSION_INVALID",
            f"package_version must be {EXPECTED_PACKAGE_VERSION}.",
            "$.package_version",
        )

    if payload.get("source_report_id") != EXPECTED_SOURCE_REPORT_ID:
        result.add_error(
            "SOURCE_REPORT_ID_INVALID",
            f"source_report_id must be {EXPECTED_SOURCE_REPORT_ID}.",
            "$.source_report_id",
        )

    if not non_empty_string(payload.get("source_name")):
        result.add_error("SOURCE_NAME_INVALID", "source_name must be a non-empty string.", "$.source_name")

    if not non_empty_string(payload.get("exported_at")):
        result.add_error("EXPORTED_AT_INVALID", "exported_at must be a non-empty string.", "$.exported_at")


def validate_summary(summary: Mapping[str, Any], payload: Mapping[str, Any], result: ValidationResult) -> None:
    missing = REQUIRED_SUMMARY_FIELDS - set(summary.keys())
    for field_name in sorted(missing):
        result.add_error("SUMMARY_FIELD_MISSING", f"Missing summary field: {field_name}", f"$.summary.{field_name}")

    if result.errors:
        return

    findings = payload.get("findings", [])

    for field_name in sorted(REQUIRED_SUMMARY_FIELDS):
        check_non_negative_int(
            summary.get(field_name),
            "SUMMARY_NUMERIC_FIELD_INVALID",
            f"$.summary.{field_name}",
            result,
        )

    if isinstance(findings, list) and summary.get("findings_count") != len(findings):
        result.add_error(
            "SUMMARY_FINDINGS_COUNT_MISMATCH",
            f"summary.findings_count={summary.get('findings_count')} but findings length={len(findings)}.",
            "$.summary.findings_count",
        )

    if isinstance(findings, list) and summary.get("evidence_count") != len(findings):
        result.add_error(
            "SUMMARY_EVIDENCE_COUNT_MISMATCH",
            f"summary.evidence_count={summary.get('evidence_count')} but findings length={len(findings)}.",
            "$.summary.evidence_count",
        )


def validate_zero_autonomy_boundary(boundary: Mapping[str, Any], result: ValidationResult) -> None:
    missing = REQUIRED_ZERO_AUTONOMY_FIELDS - set(boundary.keys())
    for field_name in sorted(missing):
        result.add_error(
            "ZERO_AUTONOMY_FIELD_MISSING",
            f"Missing zero-autonomy boundary field: {field_name}",
            f"$.zero_autonomy_boundary.{field_name}",
        )

    if result.errors:
        return

    if boundary.get("autonomous_enforcement_actions") != 0:
        result.add_error(
            "AUTONOMOUS_ENFORCEMENT_NOT_ZERO",
            "autonomous_enforcement_actions must be 0.",
            "$.zero_autonomy_boundary.autonomous_enforcement_actions",
        )

    expected_false_fields = [
        "canonical_registry_opened",
        "canonical_registry_mutated",
        "production_records_mutated",
        "signing_or_key_access_performed",
        "external_execution_performed",
    ]

    for field_name in expected_false_fields:
        if boundary.get(field_name) is not False:
            result.add_error(
                "ZERO_AUTONOMY_FIELD_NOT_FALSE",
                f"{field_name} must be false.",
                f"$.zero_autonomy_boundary.{field_name}",
            )


def validate_findings(findings: List[Any], summary: Mapping[str, Any], result: ValidationResult) -> None:
    if len(findings) == 0:
        result.add_warning("FINDINGS_EMPTY", "findings list is empty.", "$.findings")

    seen_ids = set()
    reviewed_count = 0
    high_or_critical_count = 0
    supplier_names = set()

    for index, finding in enumerate(findings):
        location = f"$.findings[{index}]"
        if not isinstance(finding, dict):
            result.add_error("FINDING_NOT_OBJECT", "Finding must be an object.", location)
            continue

        validate_finding(finding, location, result)

        finding_id = finding.get("id")
        if non_empty_string(finding_id):
            if finding_id in seen_ids:
                result.add_error("FINDING_ID_DUPLICATE", f"Duplicate finding id: {finding_id}", f"{location}.id")
            seen_ids.add(finding_id)

        if finding.get("severity") in {"HIGH", "CRITICAL"}:
            high_or_critical_count += 1

        if non_empty_string(finding.get("supplier")):
            supplier_names.add(finding["supplier"])

        human_review = finding.get("human_review")
        if isinstance(human_review, dict) and human_review.get("action") in REVIEWED_ACTIONS:
            reviewed_count += 1

    if summary.get("reviewed_findings_count") != reviewed_count:
        result.add_error(
            "SUMMARY_REVIEWED_COUNT_MISMATCH",
            f"summary.reviewed_findings_count={summary.get('reviewed_findings_count')} but actual reviewed count={reviewed_count}.",
            "$.summary.reviewed_findings_count",
        )

    if summary.get("high_or_critical_findings_count") != high_or_critical_count:
        result.add_error(
            "SUMMARY_HIGH_CRITICAL_COUNT_MISMATCH",
            f"summary.high_or_critical_findings_count={summary.get('high_or_critical_findings_count')} but actual={high_or_critical_count}.",
            "$.summary.high_or_critical_findings_count",
        )

    if summary.get("supplier_count") != len(supplier_names):
        result.add_error(
            "SUMMARY_SUPPLIER_COUNT_MISMATCH",
            f"summary.supplier_count={summary.get('supplier_count')} but actual={len(supplier_names)}.",
            "$.summary.supplier_count",
        )


def validate_finding(finding: Mapping[str, Any], location: str, result: ValidationResult) -> None:
    missing = REQUIRED_FINDING_FIELDS - set(finding.keys())
    for field_name in sorted(missing):
        result.add_error("FINDING_FIELD_MISSING", f"Missing finding field: {field_name}", f"{location}.{field_name}")

    if missing:
        return

    if not non_empty_string(finding.get("id")) or not str(finding.get("id")).startswith("EV-"):
        result.add_error("FINDING_ID_INVALID", "Finding id must be a non-empty EV-* string.", f"{location}.id")

    if finding.get("severity") not in ALLOWED_SEVERITIES:
        result.add_error("FINDING_SEVERITY_INVALID", f"Invalid severity: {finding.get('severity')}", f"{location}.severity")

    for field_name in [
        "title",
        "supplier",
        "subject",
        "detected_signal",
        "risk_meaning",
        "reviewer_question",
        "recommendation",
    ]:
        if not non_empty_string(finding.get(field_name)):
            result.add_error("FINDING_TEXT_FIELD_EMPTY", f"{field_name} must be a non-empty string.", f"{location}.{field_name}")

    if not isinstance(finding.get("evidence_ids"), list) or not finding["evidence_ids"]:
        result.add_error("FINDING_EVIDENCE_IDS_INVALID", "evidence_ids must be a non-empty list.", f"{location}.evidence_ids")
    elif finding["id"] not in finding["evidence_ids"]:
        result.add_error("FINDING_ID_NOT_IN_EVIDENCE_IDS", "finding id must be included in evidence_ids.", f"{location}.evidence_ids")

    validate_human_review(finding["human_review"], f"{location}.human_review", result)


def validate_human_review(human_review: Any, location: str, result: ValidationResult) -> None:
    if not isinstance(human_review, dict):
        result.add_error("HUMAN_REVIEW_NOT_OBJECT", "human_review must be an object.", location)
        return

    action = human_review.get("action")
    note = human_review.get("note")
    updated_at = human_review.get("updatedAt")

    if action not in VALID_HUMAN_REVIEW_ACTIONS:
        result.add_error("HUMAN_REVIEW_ACTION_INVALID", f"Invalid human review action: {action}", f"{location}.action")
        return

    if action == "UNREVIEWED":
        if note not in (None, ""):
            result.add_warning("UNREVIEWED_FINDING_HAS_NOTE", "UNREVIEWED finding has a note.", f"{location}.note")
        return

    if not non_empty_string(note):
        result.add_error(
            "REVIEWED_FINDING_NOTE_MISSING",
            "Reviewed finding must have a non-empty reviewer note.",
            f"{location}.note",
        )

    if not non_empty_string(updated_at):
        result.add_error(
            "REVIEWED_FINDING_UPDATED_AT_MISSING",
            "Reviewed finding must have a non-empty updatedAt value.",
            f"{location}.updatedAt",
        )


def validate_forbidden_verdict_phrases(payload: Mapping[str, Any], result: ValidationResult) -> None:
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for phrase in sorted(FORBIDDEN_VERDICT_PHRASES):
        if phrase in serialized:
            result.add_error(
                "FORBIDDEN_VERDICT_PHRASE_FOUND",
                f"Forbidden phrase found: {phrase}",
                "$",
            )


def collect_result_summary(payload: Mapping[str, Any], result: ValidationResult) -> None:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    result.summary = {
        "package_type": payload.get("package_type"),
        "package_version": payload.get("package_version"),
        "source_report_id": payload.get("source_report_id"),
        "source_name": payload.get("source_name"),
        "exported_at": payload.get("exported_at"),
        "findings_count": summary.get("findings_count"),
        "evidence_count": summary.get("evidence_count"),
        "supplier_count": summary.get("supplier_count"),
        "high_or_critical_findings_count": summary.get("high_or_critical_findings_count"),
        "reviewed_findings_count": summary.get("reviewed_findings_count"),
    }


def check_non_negative_int(value: Any, code: str, location: str, result: ValidationResult) -> None:
    if not isinstance(value, int) or value < 0:
        result.add_error(code, "Value must be a non-negative integer.", location)


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


if __name__ == "__main__":
    main()
