r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\tests\test_input_quality_report.py

Status:
Pytest coverage for input_quality_report.py v0.1.

Purpose:
Verify that the LEO procurement/accounting input quality report accepts clean
sample CSV input and detects malformed, incomplete, or cross-file-inconsistent
input data before anomaly analysis.

Boundary:
- Test-only validation.
- Local temporary CSV fixtures only for negative tests.
- No production mutation.
- No canonical registry access or mutation.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable, List, Mapping

import pytest


RUNTIME_DIR = Path(__file__).resolve().parents[1]
DEMO_DIR = RUNTIME_DIR / "demos" / "procurement_accounting_anomaly_audit"
INPUT_DIR = DEMO_DIR / "input"
OUTPUT_FILE = DEMO_DIR / "output" / "input_quality_report.json"

if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

import input_quality_report as quality  # noqa: E402


PROCUREMENT_COLUMNS = [
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
]

SUPPLIER_COLUMNS = [
    "supplier_id",
    "supplier_name",
    "declared_activity",
    "capacity_score",
    "registration_status",
    "country",
]

BENCHMARK_COLUMNS = [
    "item_category",
    "item_name",
    "median_unit_price",
    "currency",
    "source",
]

BASE_PROCUREMENT_ROWS = [
    {
        "record_id": "P-001",
        "date": "2026-01-10",
        "department": "Administration",
        "supplier_id": "S-001",
        "item_category": "office_supplies",
        "item_name": "Printer paper A4",
        "quantity": "500",
        "unit_price": "230.00",
        "total_value": "115000.00",
        "currency": "PLN",
        "procurement_method": "direct_purchase",
    }
]

BASE_SUPPLIER_ROWS = [
    {
        "supplier_id": "S-001",
        "supplier_name": "North Bridge Office Supplies Sp. z o.o.",
        "declared_activity": "office_supplies",
        "capacity_score": "0.80",
        "registration_status": "active",
        "country": "PL",
    }
]

BASE_BENCHMARK_ROWS = [
    {
        "item_category": "office_supplies",
        "item_name": "Printer paper A4",
        "median_unit_price": "100.00",
        "currency": "PLN",
        "source": "unit_test_benchmark",
    }
]


def test_clean_sample_input_generates_ready_for_analysis_report() -> None:
    report = quality.generate_input_quality_report(INPUT_DIR, OUTPUT_FILE)

    assert report.status == "READY_FOR_ANALYSIS"
    assert report.summary["file_count"] == 3
    assert report.summary["existing_file_count"] == 3
    assert report.summary["procurement_record_count"] == 14
    assert report.summary["supplier_profile_count"] == 7
    assert report.summary["benchmark_count"] == 14
    assert report.summary["issue_count"] == 0
    assert report.summary["error_count"] == 0
    assert report.summary["warning_count"] == 0
    assert report.summary["ready_for_analysis"] is True
    assert report.issues == []
    assert OUTPUT_FILE.exists()


def test_written_quality_report_json_is_parseable_and_consistent() -> None:
    report = quality.generate_input_quality_report(INPUT_DIR, OUTPUT_FILE)

    with OUTPUT_FILE.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    assert payload["report_id"] == "LOCAL_INPUT_QUALITY_REPORT"
    assert payload["status"] == report.status
    assert payload["summary"] == report.summary
    assert payload["issues"] == []
    assert payload["zero_autonomy_boundary"]["autonomous_enforcement_actions"] == 0
    assert payload["zero_autonomy_boundary"]["canonical_registry_opened"] is False
    assert payload["zero_autonomy_boundary"]["canonical_registry_mutated"] is False
    assert payload["zero_autonomy_boundary"]["production_records_mutated"] is False
    assert payload["zero_autonomy_boundary"]["signing_or_key_access_performed"] is False
    assert payload["zero_autonomy_boundary"]["external_execution_performed"] is False


def test_missing_file_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    (tmp_path / "supplier_profiles.csv").unlink()

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert report.summary["ready_for_analysis"] is False
    assert_issue_code(report, "INPUT_FILE_MISSING")


def test_missing_required_column_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    write_csv(tmp_path / "procurement_records.csv", [column for column in PROCUREMENT_COLUMNS if column != "supplier_id"], BASE_PROCUREMENT_ROWS)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "REQUIRED_COLUMN_MISSING")


def test_empty_critical_field_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["supplier_id"] = ""
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "CRITICAL_FIELD_EMPTY")


def test_invalid_decimal_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["unit_price"] = "not-a-number"
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "NUMERIC_FIELD_INVALID")


def test_negative_numeric_value_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["quantity"] = "-1"
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "NUMERIC_FIELD_NEGATIVE")


def test_duplicate_procurement_record_id_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows.append(dict(rows[0]))
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "DUPLICATE_PROCUREMENT_RECORD_ID")


def test_duplicate_supplier_id_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_SUPPLIER_ROWS)
    rows.append(dict(rows[0]))
    write_csv(tmp_path / "supplier_profiles.csv", SUPPLIER_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "DUPLICATE_SUPPLIER_ID")


def test_duplicate_benchmark_key_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_BENCHMARK_ROWS)
    rows.append(dict(rows[0]))
    write_csv(tmp_path / "price_benchmarks.csv", BENCHMARK_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "DUPLICATE_BENCHMARK_KEY")


def test_unknown_supplier_reference_blocks_analysis(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["supplier_id"] = "S-999"
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "BLOCKED_BY_INPUT_ERRORS"
    assert_issue_code(report, "UNKNOWN_SUPPLIER_REFERENCE")


def test_total_value_mismatch_generates_warning(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["total_value"] = "1.00"
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "READY_WITH_WARNINGS"
    assert report.summary["ready_for_analysis"] is True
    assert_issue_code(report, "TOTAL_VALUE_MISMATCH")
    assert report.summary["warning_count"] == 1
    assert report.summary["error_count"] == 0


def test_missing_benchmark_coverage_generates_warning(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["item_name"] = "Unbenchmarked item"
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "READY_WITH_WARNINGS"
    assert report.summary["ready_for_analysis"] is True
    assert_issue_code(report, "MISSING_BENCHMARK_COVERAGE")
    assert report.summary["warning_count"] == 1
    assert report.summary["error_count"] == 0


def test_unsupported_currency_generates_warning(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["currency"] = "CHF"
    write_csv(tmp_path / "procurement_records.csv", PROCUREMENT_COLUMNS, rows)

    benchmark_rows = clone_rows(BASE_BENCHMARK_ROWS)
    benchmark_rows[0]["currency"] = "CHF"
    write_csv(tmp_path / "price_benchmarks.csv", BENCHMARK_COLUMNS, benchmark_rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    assert report.status == "READY_WITH_WARNINGS"
    assert report.summary["ready_for_analysis"] is True
    assert_issue_code(report, "UNSUPPORTED_CURRENCY")
    assert report.summary["warning_count"] >= 1
    assert report.summary["error_count"] == 0


def test_file_summary_reports_missing_and_extra_columns(tmp_path: Path) -> None:
    write_minimal_clean_fixture(tmp_path)
    columns = PROCUREMENT_COLUMNS + ["extra_demo_column"]
    rows = clone_rows(BASE_PROCUREMENT_ROWS)
    rows[0]["extra_demo_column"] = "extra"
    write_csv(tmp_path / "procurement_records.csv", columns, rows)

    report = quality.generate_input_quality_report(tmp_path, tmp_path / "out.json")

    procurement_summary = report.files["procurement_records"]
    assert procurement_summary["exists"] is True
    assert procurement_summary["required_columns_present"] is True
    assert procurement_summary["missing_columns"] == []
    assert procurement_summary["extra_columns"] == ["extra_demo_column"]


def write_minimal_clean_fixture(base_dir: Path) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    write_csv(base_dir / "procurement_records.csv", PROCUREMENT_COLUMNS, BASE_PROCUREMENT_ROWS)
    write_csv(base_dir / "supplier_profiles.csv", SUPPLIER_COLUMNS, BASE_SUPPLIER_ROWS)
    write_csv(base_dir / "price_benchmarks.csv", BENCHMARK_COLUMNS, BASE_BENCHMARK_ROWS)


def write_csv(path: Path, fieldnames: List[str], rows: List[Mapping[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def clone_rows(rows: Iterable[Mapping[str, str]]) -> List[dict[str, str]]:
    return [dict(row) for row in rows]


def assert_issue_code(report: quality.InputQualityReport, code: str) -> None:
    assert code in {issue.code for issue in report.issues}, report.to_dict()
