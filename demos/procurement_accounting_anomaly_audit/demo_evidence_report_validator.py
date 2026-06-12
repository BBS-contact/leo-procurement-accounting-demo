r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\demo_evidence_report_validator.py

Status:
Generated evidence report validator v0.1 for the LEO procurement/accounting anomaly demo.

Purpose:
Validate a generated LEO evidence report independently of the input pipeline.

The validator checks:
- JSON file existence and parseability;
- top-level report structure;
- required summary fields;
- required zero-autonomy boundary fields;
- evidence/findings list consistency;
- dashboard-compatible aliases;
- finding-level required fields;
- signal family consistency;
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
python demo_evidence_report_validator.py output\demo_evidence_report.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_PATH = BASE_DIR / "output" / "demo_evidence_report.json"

ALLOWED_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"}
REQUIRED_TOP_LEVEL_FIELDS = {
    "report_id",
    "generated_at",
    "source_name",
    "zero_autonomy_boundary",
    "summary",
    "evidence",
    "findings",
}
REQUIRED_SUMMARY_FIELDS = {
    "findings_count",
    "evidence_count",
    "supplier_count",
    "high_or_critical_findings_count",
    "reviewed_findings_count",
    "signal_families",
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
    "source_records",
    "signal_family",
}
REQUIRED_DASHBOARD_ALIAS_FIELDS = {
    "reason",
    "description",
    "type",
    "signal_title",
    "risk_level",
    "recommended_action",
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


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    location: str


@dataclass
class ValidationResult:
    is_valid: bool
    report_path: str
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
            "report_path": self.report_path,
            "summary": self.summary,
            "errors": [issue.__dict__ for issue in self.errors],
            "warnings": [issue.__dict__ for issue in self.warnings],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a LEO generated evidence report JSON file.")
    parser.add_argument(
        "report_path",
        nargs="?",
        default=str(DEFAULT_REPORT_PATH),
        help="Path to generated evidence report JSON. Defaults to output/demo_evidence_report.json.",
    )
    args = parser.parse_args()

    result = validate_report_file(Path(args.report_path))
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    if not result.is_valid:
        raise SystemExit(1)


def validate_report_file(report_path: Path) -> ValidationResult:
    result = ValidationResult(is_valid=True, report_path=str(report_path))

    if not report_path.exists():
        result.add_error("REPORT_FILE_MISSING", f"Report file does not exist: {report_path}", "report_path")
        return result

    try:
        with report_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        result.add_error("REPORT_JSON_INVALID", f"Invalid JSON: {exc}", "report_path")
        return result

    validate_report_payload(payload, result)
    return result


def validate_report_payload(payload: Any, result: Optional[ValidationResult] = None) -> ValidationResult:
    if result is None:
        result = ValidationResult(is_valid=True, report_path="<in-memory>")

    if not isinstance(payload, dict):
        result.add_error("REPORT_NOT_OBJECT", "Report payload must be a JSON object.", "$")
        return result

    validate_top_level_fields(payload, result)
    if result.errors:
        return result

    validate_summary(payload["summary"], payload, result)
    validate_zero_autonomy_boundary(payload["zero_autonomy_boundary"], result)
    validate_evidence_and_findings(payload, result)
    validate_forbidden_verdict_phrases(payload, result)
    collect_result_summary(payload, result)

    return result


def validate_top_level_fields(payload: Mapping[str, Any], result: ValidationResult) -> None:
    missing = REQUIRED_TOP_LEVEL_FIELDS - set(payload.keys())
    for field_name in sorted(missing):
        result.add_error("TOP_LEVEL_FIELD_MISSING", f"Missing top-level field: {field_name}", f"$.{field_name}")

    if "report_id" in payload and not non_empty_string(payload["report_id"]):
        result.add_error("REPORT_ID_INVALID", "report_id must be a non-empty string.", "$.report_id")

    if "generated_at" in payload and not non_empty_string(payload["generated_at"]):
        result.add_error("GENERATED_AT_INVALID", "generated_at must be a non-empty string.", "$.generated_at")

    if "source_name" in payload and not non_empty_string(payload["source_name"]):
        result.add_error("SOURCE_NAME_INVALID", "source_name must be a non-empty string.", "$.source_name")

    if "summary" in payload and not isinstance(payload["summary"], dict):
        result.add_error("SUMMARY_INVALID", "summary must be an object.", "$.summary")

    if "zero_autonomy_boundary" in payload and not isinstance(payload["zero_autonomy_boundary"], dict):
        result.add_error(
            "ZERO_AUTONOMY_BOUNDARY_INVALID",
            "zero_autonomy_boundary must be an object.",
            "$.zero_autonomy_boundary",
        )

    if "evidence" in payload and not isinstance(payload["evidence"], list):
        result.add_error("EVIDENCE_INVALID", "evidence must be a list.", "$.evidence")

    if "findings" in payload and not isinstance(payload["findings"], list):
        result.add_error("FINDINGS_INVALID", "findings must be a list.", "$.findings")


def validate_summary(summary: Mapping[str, Any], payload: Mapping[str, Any], result: ValidationResult) -> None:
    missing = REQUIRED_SUMMARY_FIELDS - set(summary.keys())
    for field_name in sorted(missing):
        result.add_error("SUMMARY_FIELD_MISSING", f"Missing summary field: {field_name}", f"$.summary.{field_name}")

    if result.errors:
        return

    evidence = payload.get("evidence", [])
    findings = payload.get("findings", [])

    check_non_negative_int(summary.get("findings_count"), "SUMMARY_FINDINGS_COUNT_INVALID", "$.summary.findings_count", result)
    check_non_negative_int(summary.get("evidence_count"), "SUMMARY_EVIDENCE_COUNT_INVALID", "$.summary.evidence_count", result)
    check_non_negative_int(summary.get("supplier_count"), "SUMMARY_SUPPLIER_COUNT_INVALID", "$.summary.supplier_count", result)
    check_non_negative_int(
        summary.get("high_or_critical_findings_count"),
        "SUMMARY_HIGH_CRITICAL_COUNT_INVALID",
        "$.summary.high_or_critical_findings_count",
        result,
    )
    check_non_negative_int(
        summary.get("reviewed_findings_count"),
        "SUMMARY_REVIEWED_COUNT_INVALID",
        "$.summary.reviewed_findings_count",
        result,
    )

    if not isinstance(summary.get("signal_families"), dict):
        result.add_error("SUMMARY_SIGNAL_FAMILIES_INVALID", "signal_families must be an object.", "$.summary.signal_families")
        return

    if isinstance(evidence, list) and summary.get("evidence_count") != len(evidence):
        result.add_error(
            "SUMMARY_EVIDENCE_COUNT_MISMATCH",
            f"summary.evidence_count={summary.get('evidence_count')} but evidence length={len(evidence)}.",
            "$.summary.evidence_count",
        )

    if isinstance(findings, list) and summary.get("findings_count") != len(findings):
        result.add_error(
            "SUMMARY_FINDINGS_COUNT_MISMATCH",
            f"summary.findings_count={summary.get('findings_count')} but findings length={len(findings)}.",
            "$.summary.findings_count",
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

    expected_false_fields = [
        "canonical_registry_opened",
        "canonical_registry_mutated",
        "production_records_mutated",
        "signing_or_key_access_performed",
        "external_execution_performed",
    ]

    if boundary.get("autonomous_enforcement_actions") != 0:
        result.add_error(
            "AUTONOMOUS_ENFORCEMENT_NOT_ZERO",
            "autonomous_enforcement_actions must be 0.",
            "$.zero_autonomy_boundary.autonomous_enforcement_actions",
        )

    for field_name in expected_false_fields:
        if boundary.get(field_name) is not False:
            result.add_error(
                "ZERO_AUTONOMY_FIELD_NOT_FALSE",
                f"{field_name} must be false.",
                f"$.zero_autonomy_boundary.{field_name}",
            )


def validate_evidence_and_findings(payload: Mapping[str, Any], result: ValidationResult) -> None:
    evidence = payload.get("evidence", [])
    findings = payload.get("findings", [])

    if not isinstance(evidence, list) or not isinstance(findings, list):
        return

    if len(evidence) == 0:
        result.add_warning("EVIDENCE_EMPTY", "evidence list is empty.", "$.evidence")

    if len(findings) == 0:
        result.add_warning("FINDINGS_EMPTY", "findings list is empty.", "$.findings")

    evidence_ids = collect_ids(evidence, "$.evidence", result)
    finding_ids = collect_ids(findings, "$.findings", result)

    if evidence_ids != finding_ids:
        result.add_error(
            "EVIDENCE_FINDING_IDS_MISMATCH",
            "evidence IDs and finding IDs must match for this local demo report format.",
            "$.evidence / $.findings",
        )

    for index, finding in enumerate(findings):
        validate_finding(finding, f"$.findings[{index}]", result)

    validate_summary_signal_family_counts(payload.get("summary", {}), findings, result)
    validate_high_or_critical_count(payload.get("summary", {}), findings, result)
    validate_supplier_count(payload.get("summary", {}), findings, result)


def validate_finding(finding: Any, location: str, result: ValidationResult) -> None:
    if not isinstance(finding, dict):
        result.add_error("FINDING_NOT_OBJECT", "Finding must be an object.", location)
        return

    missing_required = REQUIRED_FINDING_FIELDS - set(finding.keys())
    for field_name in sorted(missing_required):
        result.add_error("FINDING_FIELD_MISSING", f"Missing finding field: {field_name}", f"{location}.{field_name}")

    missing_alias = REQUIRED_DASHBOARD_ALIAS_FIELDS - set(finding.keys())
    for field_name in sorted(missing_alias):
        result.add_error("DASHBOARD_ALIAS_FIELD_MISSING", f"Missing dashboard alias field: {field_name}", f"{location}.{field_name}")

    if missing_required or missing_alias:
        return

    if not non_empty_string(finding["id"]) or not str(finding["id"]).startswith("EV-"):
        result.add_error("FINDING_ID_INVALID", "Finding id must be a non-empty EV-* string.", f"{location}.id")

    if finding["severity"] not in ALLOWED_SEVERITIES:
        result.add_error("FINDING_SEVERITY_INVALID", f"Invalid severity: {finding['severity']}", f"{location}.severity")

    for field_name in [
        "title",
        "supplier",
        "subject",
        "detected_signal",
        "risk_meaning",
        "reviewer_question",
        "recommendation",
        "signal_family",
    ]:
        if not non_empty_string(finding.get(field_name)):
            result.add_error("FINDING_TEXT_FIELD_EMPTY", f"{field_name} must be a non-empty string.", f"{location}.{field_name}")

    if finding.get("reason") != finding.get("detected_signal"):
        result.add_error("DASHBOARD_REASON_ALIAS_MISMATCH", "reason must equal detected_signal.", f"{location}.reason")

    if finding.get("description") != finding.get("detected_signal"):
        result.add_error("DASHBOARD_DESCRIPTION_ALIAS_MISMATCH", "description must equal detected_signal.", f"{location}.description")

    if finding.get("type") != "EVIDENCE_OBJECT":
        result.add_error("DASHBOARD_TYPE_INVALID", "type must be EVIDENCE_OBJECT.", f"{location}.type")

    if finding.get("signal_title") != finding.get("title"):
        result.add_error("DASHBOARD_SIGNAL_TITLE_ALIAS_MISMATCH", "signal_title must equal title.", f"{location}.signal_title")

    if finding.get("risk_level") != finding.get("severity"):
        result.add_error("DASHBOARD_RISK_LEVEL_ALIAS_MISMATCH", "risk_level must equal severity.", f"{location}.risk_level")

    if finding.get("recommended_action") != finding.get("recommendation"):
        result.add_error(
            "DASHBOARD_RECOMMENDED_ACTION_ALIAS_MISMATCH",
            "recommended_action must equal recommendation.",
            f"{location}.recommended_action",
        )

    if not isinstance(finding.get("evidence_ids"), list) or not finding["evidence_ids"]:
        result.add_error("FINDING_EVIDENCE_IDS_INVALID", "evidence_ids must be a non-empty list.", f"{location}.evidence_ids")
    elif finding["id"] not in finding["evidence_ids"]:
        result.add_error("FINDING_ID_NOT_IN_EVIDENCE_IDS", "finding id must be included in evidence_ids.", f"{location}.evidence_ids")

    if not isinstance(finding.get("source_records"), list) or not finding["source_records"]:
        result.add_error("FINDING_SOURCE_RECORDS_INVALID", "source_records must be a non-empty list.", f"{location}.source_records")


def validate_summary_signal_family_counts(summary: Mapping[str, Any], findings: List[Any], result: ValidationResult) -> None:
    signal_families = summary.get("signal_families")
    if not isinstance(signal_families, dict):
        return

    actual_counts: Dict[str, int] = {}
    for finding in findings:
        if isinstance(finding, dict) and isinstance(finding.get("signal_family"), str):
            family = finding["signal_family"]
            actual_counts[family] = actual_counts.get(family, 0) + 1

    if signal_families != actual_counts:
        result.add_error(
            "SUMMARY_SIGNAL_FAMILY_COUNTS_MISMATCH",
            f"summary.signal_families={signal_families} but actual={actual_counts}.",
            "$.summary.signal_families",
        )


def validate_high_or_critical_count(summary: Mapping[str, Any], findings: List[Any], result: ValidationResult) -> None:
    expected = summary.get("high_or_critical_findings_count")
    actual = sum(
        1
        for finding in findings
        if isinstance(finding, dict) and finding.get("severity") in {"HIGH", "CRITICAL"}
    )
    if expected != actual:
        result.add_error(
            "SUMMARY_HIGH_CRITICAL_COUNT_MISMATCH",
            f"summary.high_or_critical_findings_count={expected} but actual={actual}.",
            "$.summary.high_or_critical_findings_count",
        )


def validate_supplier_count(summary: Mapping[str, Any], findings: List[Any], result: ValidationResult) -> None:
    expected = summary.get("supplier_count")
    actual = len({finding.get("supplier") for finding in findings if isinstance(finding, dict) and finding.get("supplier")})
    if expected != actual:
        result.add_error(
            "SUMMARY_SUPPLIER_COUNT_MISMATCH",
            f"summary.supplier_count={expected} but actual={actual}.",
            "$.summary.supplier_count",
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
        "report_id": payload.get("report_id"),
        "generated_at": payload.get("generated_at"),
        "source_name": payload.get("source_name"),
        "findings_count": summary.get("findings_count"),
        "evidence_count": summary.get("evidence_count"),
        "supplier_count": summary.get("supplier_count"),
        "high_or_critical_findings_count": summary.get("high_or_critical_findings_count"),
        "signal_families": summary.get("signal_families"),
    }


def collect_ids(items: List[Any], location: str, result: ValidationResult) -> List[str]:
    ids: List[str] = []
    seen = set()
    for index, item in enumerate(items):
        item_location = f"{location}[{index}]"
        if not isinstance(item, dict):
            result.add_error("ITEM_NOT_OBJECT", "Item must be an object.", item_location)
            continue
        item_id = item.get("id")
        if not non_empty_string(item_id):
            result.add_error("ITEM_ID_MISSING", "Item id is missing or empty.", f"{item_location}.id")
            continue
        if item_id in seen:
            result.add_error("ITEM_ID_DUPLICATE", f"Duplicate item id: {item_id}", f"{item_location}.id")
            continue
        seen.add(item_id)
        ids.append(str(item_id))
    return ids


def check_non_negative_int(value: Any, code: str, location: str, result: ValidationResult) -> None:
    if not isinstance(value, int) or value < 0:
        result.add_error(code, "Value must be a non-negative integer.", location)


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


if __name__ == "__main__":
    main()
