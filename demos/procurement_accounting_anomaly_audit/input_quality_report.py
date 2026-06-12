r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\input_quality_report.py

Status:
Input quality report generator v0.1 for the LEO procurement/accounting anomaly demo.

Purpose:
Assess whether local CSV input files are structurally and semantically ready for
LEO procurement/accounting evidence generation.

This module checks input data quality before anomaly analysis.
It does not generate risk findings, fraud verdicts, legal conclusions, or enforcement actions.

Checked input files:
- input/procurement_records.csv
- input/supplier_profiles.csv
- input/price_benchmarks.csv

The report checks:
- required file presence;
- required columns;
- empty critical fields;
- duplicate procurement record IDs;
- duplicate supplier IDs;
- duplicate benchmark keys;
- decimal parseability;
- non-negative numeric values;
- total_value consistency with quantity * unit_price;
- unknown supplier references;
- missing benchmark coverage;
- unsupported or inconsistent currencies;
- zero-autonomy boundary.

Boundary:
- Read-only input quality assessment.
- No anomaly verdicts.
- No fraud or legal conclusions.
- No production mutation.
- No canonical registry access.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.

Run from the demo folder:
python input_quality_report.py

Output:
output/input_quality_report.json
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "input_quality_report.json"

PROCUREMENT_RECORDS_FILE = INPUT_DIR / "procurement_records.csv"
SUPPLIER_PROFILES_FILE = INPUT_DIR / "supplier_profiles.csv"
PRICE_BENCHMARKS_FILE = INPUT_DIR / "price_benchmarks.csv"

SUPPORTED_CURRENCIES = {"PLN", "EUR", "USD"}
TOTAL_VALUE_TOLERANCE = Decimal("0.01")

REQUIRED_COLUMNS = {
    "procurement_records": {
        "record_id",
        "date",
        "department",
        "supplier_id",
        "item_category",
        "item_name",
        "quantity",
        "unit_price",
        "total_value",
        "currency",
        "procurement_method",
    },
    "supplier_profiles": {
        "supplier_id",
        "supplier_name",
        "declared_activity",
        "capacity_score",
        "registration_status",
        "country",
    },
    "price_benchmarks": {
        "item_category",
        "item_name",
        "median_unit_price",
        "currency",
        "source",
    },
}

CRITICAL_FIELDS = {
    "procurement_records": [
        "record_id",
        "supplier_id",
        "item_category",
        "item_name",
        "quantity",
        "unit_price",
        "total_value",
        "currency",
    ],
    "supplier_profiles": [
        "supplier_id",
        "supplier_name",
        "declared_activity",
        "capacity_score",
    ],
    "price_benchmarks": [
        "item_category",
        "item_name",
        "median_unit_price",
        "currency",
    ],
}

NUMERIC_FIELDS = {
    "procurement_records": ["quantity", "unit_price", "total_value"],
    "supplier_profiles": ["capacity_score"],
    "price_benchmarks": ["median_unit_price"],
}

SEVERITY_ORDER = {
    "INFO": 0,
    "WARNING": 1,
    "ERROR": 2,
}


@dataclass(frozen=True)
class InputQualityIssue:
    severity: str
    code: str
    message: str
    file: str
    row_number: Optional[int] = None
    field: Optional[str] = None
    value: Optional[str] = None


@dataclass
class InputQualityReport:
    report_id: str
    generated_at: str
    input_dir: str
    status: str
    summary: Dict[str, Any]
    files: Dict[str, Dict[str, Any]]
    issues: List[InputQualityIssue] = field(default_factory=list)
    zero_autonomy_boundary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "input_dir": self.input_dir,
            "status": self.status,
            "summary": self.summary,
            "files": self.files,
            "issues": [issue.__dict__ for issue in self.issues],
            "zero_autonomy_boundary": self.zero_autonomy_boundary,
        }


@dataclass(frozen=True)
class CsvData:
    logical_name: str
    path: Path
    exists: bool
    fieldnames: List[str]
    rows: List[Dict[str, str]]


class InputQualityError(Exception):
    """Raised only for unexpected internal input quality report failures."""


def main() -> None:
    report = generate_input_quality_report(INPUT_DIR, OUTPUT_FILE)
    print(json.dumps({"status": report.status, "output": str(OUTPUT_FILE), "summary": report.summary}, indent=2))


def generate_input_quality_report(input_dir: Path = INPUT_DIR, output_file: Path = OUTPUT_FILE) -> InputQualityReport:
    procurement_path = input_dir / "procurement_records.csv"
    suppliers_path = input_dir / "supplier_profiles.csv"
    benchmarks_path = input_dir / "price_benchmarks.csv"

    csv_data = {
        "procurement_records": read_csv_data("procurement_records", procurement_path),
        "supplier_profiles": read_csv_data("supplier_profiles", suppliers_path),
        "price_benchmarks": read_csv_data("price_benchmarks", benchmarks_path),
    }

    issues: List[InputQualityIssue] = []
    files_summary: Dict[str, Dict[str, Any]] = {}

    for logical_name, data in csv_data.items():
        files_summary[logical_name] = build_file_summary(data)
        issues.extend(validate_file_presence_and_columns(data))
        if data.exists:
            issues.extend(validate_empty_critical_fields(data))
            issues.extend(validate_numeric_fields(data))
            issues.extend(validate_supported_currencies(data))

    if csv_data["procurement_records"].exists:
        issues.extend(validate_duplicate_keys(csv_data["procurement_records"], ["record_id"], "DUPLICATE_PROCUREMENT_RECORD_ID"))
        issues.extend(validate_total_value_consistency(csv_data["procurement_records"]))

    if csv_data["supplier_profiles"].exists:
        issues.extend(validate_duplicate_keys(csv_data["supplier_profiles"], ["supplier_id"], "DUPLICATE_SUPPLIER_ID"))

    if csv_data["price_benchmarks"].exists:
        issues.extend(validate_duplicate_keys(csv_data["price_benchmarks"], ["item_category", "item_name", "currency"], "DUPLICATE_BENCHMARK_KEY"))

    issues.extend(validate_cross_file_supplier_coverage(csv_data["procurement_records"], csv_data["supplier_profiles"]))
    issues.extend(validate_cross_file_benchmark_coverage(csv_data["procurement_records"], csv_data["price_benchmarks"]))

    status = calculate_status(issues)
    summary = build_report_summary(csv_data, issues)

    report = InputQualityReport(
        report_id="LOCAL_INPUT_QUALITY_REPORT",
        generated_at=datetime.now(timezone.utc).isoformat(),
        input_dir=str(input_dir),
        status=status,
        summary=summary,
        files=files_summary,
        issues=issues,
        zero_autonomy_boundary={
            "autonomous_enforcement_actions": 0,
            "canonical_registry_opened": False,
            "canonical_registry_mutated": False,
            "production_records_mutated": False,
            "signing_or_key_access_performed": False,
            "external_execution_performed": False,
            "pipeline_mode": "LOCAL_READ_ONLY_INPUT_QUALITY_ASSESSMENT",
        },
    )

    write_report(report, output_file)
    return report


def read_csv_data(logical_name: str, path: Path) -> CsvData:
    if not path.exists():
        return CsvData(logical_name=logical_name, path=path, exists=False, fieldnames=[], rows=[])

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [field.strip() for field in (reader.fieldnames or [])]
        rows = [{key.strip(): (value or "").strip() for key, value in row.items()} for row in reader]

    return CsvData(logical_name=logical_name, path=path, exists=True, fieldnames=fieldnames, rows=rows)


def build_file_summary(data: CsvData) -> Dict[str, Any]:
    required = REQUIRED_COLUMNS[data.logical_name]
    actual = set(data.fieldnames)
    return {
        "path": str(data.path),
        "exists": data.exists,
        "row_count": len(data.rows),
        "column_count": len(data.fieldnames),
        "required_columns_present": data.exists and required.issubset(actual),
        "missing_columns": sorted(required - actual) if data.exists else sorted(required),
        "extra_columns": sorted(actual - required) if data.exists else [],
    }


def validate_file_presence_and_columns(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    if not data.exists:
        issues.append(
            InputQualityIssue(
                severity="ERROR",
                code="INPUT_FILE_MISSING",
                message=f"Required input file is missing: {data.path}",
                file=str(data.path),
            )
        )
        return issues

    actual = set(data.fieldnames)
    missing = REQUIRED_COLUMNS[data.logical_name] - actual
    for column in sorted(missing):
        issues.append(
            InputQualityIssue(
                severity="ERROR",
                code="REQUIRED_COLUMN_MISSING",
                message=f"Required column is missing: {column}",
                file=str(data.path),
                field=column,
            )
        )

    if len(data.rows) == 0:
        issues.append(
            InputQualityIssue(
                severity="WARNING",
                code="INPUT_FILE_EMPTY",
                message="Input file has a header but no data rows.",
                file=str(data.path),
            )
        )

    return issues


def validate_empty_critical_fields(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    available_fields = set(data.fieldnames)
    for row_index, row in enumerate(data.rows, start=2):
        for field_name in CRITICAL_FIELDS[data.logical_name]:
            if field_name not in available_fields:
                continue
            if row.get(field_name, "").strip() == "":
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="CRITICAL_FIELD_EMPTY",
                        message=f"Critical field is empty: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                    )
                )
    return issues


def validate_numeric_fields(data: CsvData) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    available_fields = set(data.fieldnames)
    for row_index, row in enumerate(data.rows, start=2):
        for field_name in NUMERIC_FIELDS[data.logical_name]:
            if field_name not in available_fields:
                continue
            raw_value = row.get(field_name, "").strip()
            if raw_value == "":
                continue
            parsed = parse_decimal_or_none(raw_value)
            if parsed is None:
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="NUMERIC_FIELD_INVALID",
                        message=f"Numeric field is not parseable: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                        value=raw_value,
                    )
                )
                continue
            if parsed < 0:
                issues.append(
                    InputQualityIssue(
                        severity="ERROR",
                        code="NUMERIC_FIELD_NEGATIVE",
                        message=f"Numeric field must not be negative: {field_name}",
                        file=str(data.path),
                        row_number=row_index,
                        field=field_name,
                        value=raw_value,
                    )
                )
    return issues


def validate_supported_currencies(data: CsvData) -> List[InputQualityIssue]:
    if "currency" not in data.fieldnames:
        return []

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(data.rows, start=2):
        currency = row.get("currency", "").strip().upper()
        if currency == "":
            continue
        if currency not in SUPPORTED_CURRENCIES:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="UNSUPPORTED_CURRENCY",
                    message=f"Currency is not in the supported demo currency set: {currency}",
                    file=str(data.path),
                    row_number=row_index,
                    field="currency",
                    value=currency,
                )
            )
    return issues


def validate_duplicate_keys(data: CsvData, key_fields: Sequence[str], code: str) -> List[InputQualityIssue]:
    issues: List[InputQualityIssue] = []
    if not set(key_fields).issubset(set(data.fieldnames)):
        return issues

    seen: Dict[Tuple[str, ...], int] = {}
    for row_index, row in enumerate(data.rows, start=2):
        key = tuple(normalize_key_value(row.get(field_name, "")) for field_name in key_fields)
        if any(value == "" for value in key):
            continue
        if key in seen:
            issues.append(
                InputQualityIssue(
                    severity="ERROR",
                    code=code,
                    message=f"Duplicate key detected for fields {list(key_fields)}: {key}",
                    file=str(data.path),
                    row_number=row_index,
                    field="|".join(key_fields),
                    value="|".join(key),
                )
            )
        else:
            seen[key] = row_index
    return issues


def validate_total_value_consistency(data: CsvData) -> List[InputQualityIssue]:
    required = {"quantity", "unit_price", "total_value", "record_id"}
    if not required.issubset(set(data.fieldnames)):
        return []

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(data.rows, start=2):
        quantity = parse_decimal_or_none(row.get("quantity", ""))
        unit_price = parse_decimal_or_none(row.get("unit_price", ""))
        total_value = parse_decimal_or_none(row.get("total_value", ""))
        if quantity is None or unit_price is None or total_value is None:
            continue

        expected_total = quantity * unit_price
        difference = abs(expected_total - total_value)
        if difference > TOTAL_VALUE_TOLERANCE:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="TOTAL_VALUE_MISMATCH",
                    message=(
                        "total_value does not match quantity * unit_price within tolerance. "
                        f"Expected {format_decimal(expected_total)}, got {format_decimal(total_value)}."
                    ),
                    file=str(data.path),
                    row_number=row_index,
                    field="total_value",
                    value=row.get("total_value", ""),
                )
            )
    return issues


def validate_cross_file_supplier_coverage(procurement: CsvData, suppliers: CsvData) -> List[InputQualityIssue]:
    if not procurement.exists or not suppliers.exists:
        return []
    if "supplier_id" not in procurement.fieldnames or "supplier_id" not in suppliers.fieldnames:
        return []

    supplier_ids = {normalize_key_value(row.get("supplier_id", "")) for row in suppliers.rows if row.get("supplier_id", "")}
    issues: List[InputQualityIssue] = []

    for row_index, row in enumerate(procurement.rows, start=2):
        supplier_id = normalize_key_value(row.get("supplier_id", ""))
        if supplier_id == "":
            continue
        if supplier_id not in supplier_ids:
            issues.append(
                InputQualityIssue(
                    severity="ERROR",
                    code="UNKNOWN_SUPPLIER_REFERENCE",
                    message=f"Procurement record references supplier_id without supplier profile: {supplier_id}",
                    file=str(procurement.path),
                    row_number=row_index,
                    field="supplier_id",
                    value=supplier_id,
                )
            )
    return issues


def validate_cross_file_benchmark_coverage(procurement: CsvData, benchmarks: CsvData) -> List[InputQualityIssue]:
    if not procurement.exists or not benchmarks.exists:
        return []
    procurement_fields = {"item_category", "item_name", "currency"}
    benchmark_fields = {"item_category", "item_name", "currency"}
    if not procurement_fields.issubset(set(procurement.fieldnames)):
        return []
    if not benchmark_fields.issubset(set(benchmarks.fieldnames)):
        return []

    benchmark_keys = {
        (
            normalize_token(row.get("item_category", "")),
            normalize_token(row.get("item_name", "")),
            normalize_key_value(row.get("currency", "")).upper(),
        )
        for row in benchmarks.rows
        if row.get("item_category", "") and row.get("item_name", "") and row.get("currency", "")
    }

    issues: List[InputQualityIssue] = []
    for row_index, row in enumerate(procurement.rows, start=2):
        key = (
            normalize_token(row.get("item_category", "")),
            normalize_token(row.get("item_name", "")),
            normalize_key_value(row.get("currency", "")).upper(),
        )
        if any(value == "" for value in key):
            continue
        if key not in benchmark_keys:
            issues.append(
                InputQualityIssue(
                    severity="WARNING",
                    code="MISSING_BENCHMARK_COVERAGE",
                    message=f"No benchmark found for procurement item key: {key}",
                    file=str(procurement.path),
                    row_number=row_index,
                    field="item_category|item_name|currency",
                    value="|".join(key),
                )
            )
    return issues


def build_report_summary(csv_data: Mapping[str, CsvData], issues: List[InputQualityIssue]) -> Dict[str, Any]:
    error_count = count_issues_by_severity(issues, "ERROR")
    warning_count = count_issues_by_severity(issues, "WARNING")
    info_count = count_issues_by_severity(issues, "INFO")

    return {
        "file_count": len(csv_data),
        "existing_file_count": sum(1 for data in csv_data.values() if data.exists),
        "procurement_record_count": len(csv_data["procurement_records"].rows),
        "supplier_profile_count": len(csv_data["supplier_profiles"].rows),
        "benchmark_count": len(csv_data["price_benchmarks"].rows),
        "issue_count": len(issues),
        "error_count": error_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "ready_for_analysis": error_count == 0,
    }


def calculate_status(issues: List[InputQualityIssue]) -> str:
    if any(issue.severity == "ERROR" for issue in issues):
        return "BLOCKED_BY_INPUT_ERRORS"
    if any(issue.severity == "WARNING" for issue in issues):
        return "READY_WITH_WARNINGS"
    return "READY_FOR_ANALYSIS"


def count_issues_by_severity(issues: Iterable[InputQualityIssue], severity: str) -> int:
    return sum(1 for issue in issues if issue.severity == severity)


def write_report(report: InputQualityReport, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(report.to_dict(), handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def parse_decimal_or_none(value: str) -> Optional[Decimal]:
    try:
        return Decimal(str(value).strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        return None


def normalize_key_value(value: str) -> str:
    return str(value or "").strip()


def normalize_token(value: str) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def format_decimal(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


if __name__ == "__main__":
    main()
