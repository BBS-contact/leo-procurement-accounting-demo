r"""
Canonical path:
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\procurement_accounting_input_pipeline.py

Status:
Prototype input pipeline v0.1 for the LEO procurement/accounting anomaly demo.

Purpose:
Read local CSV input files, validate their structure, normalize procurement records,
run demo-level anomaly analysis, and generate output/demo_evidence_report.json for
leo_demo_dashboard.html.

Boundary:
- Local demo/prototype pipeline only.
- Read-only input processing.
- No production mutation.
- No canonical registry access.
- No autonomous enforcement.
- No signing/key access.
- No external API calls.
- No legal/fraud conclusion.

Expected folder structure:
D:\BBS-09-01-2026\leo\runtime\demos\procurement_accounting_anomaly_audit\
  input\
    procurement_records.csv
    supplier_profiles.csv
    price_benchmarks.csv
  output\
    demo_evidence_report.json

Run from the demo folder:
python procurement_accounting_input_pipeline.py
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "demo_evidence_report.json"

PROCUREMENT_RECORDS_FILE = INPUT_DIR / "procurement_records.csv"
SUPPLIER_PROFILES_FILE = INPUT_DIR / "supplier_profiles.csv"
PRICE_BENCHMARKS_FILE = INPUT_DIR / "price_benchmarks.csv"

PRICE_CRITICAL_RATIO = Decimal("2.0")
PRICE_HIGH_RATIO = Decimal("1.5")
LOW_SUPPLIER_CAPACITY_THRESHOLD = Decimal("0.40")
HIGH_VALUE_PROCUREMENT_THRESHOLD = Decimal("50000.00")
LARGE_QUANTITY_THRESHOLD = Decimal("250")
THRESHOLD_FRAGMENT_MIN_VALUE = Decimal("9000.00")
THRESHOLD_FRAGMENT_MAX_VALUE = Decimal("10000.00")
THRESHOLD_FRAGMENT_MIN_COUNT = 3


class PipelineError(Exception):
    """Raised when the local demo input pipeline cannot produce a valid report."""


@dataclass(frozen=True)
class ProcurementRecord:
    record_id: str
    date: str
    department: str
    supplier_id: str
    item_category: str
    item_name: str
    quantity: Decimal
    unit_price: Decimal
    total_value: Decimal
    currency: str
    procurement_method: str


@dataclass(frozen=True)
class SupplierProfile:
    supplier_id: str
    supplier_name: str
    declared_activity: str
    capacity_score: Decimal
    registration_status: str
    country: str


@dataclass(frozen=True)
class PriceBenchmark:
    item_category: str
    item_name: str
    median_unit_price: Decimal
    currency: str
    source: str


@dataclass(frozen=True)
class EvidenceObject:
    id: str
    title: str
    severity: str
    supplier: str
    subject: str
    detected_signal: str
    risk_meaning: str
    reviewer_question: str
    recommendation: str
    evidence_ids: List[str]
    source_records: List[str]
    signal_family: str
    raw_context: Dict[str, Any]


@dataclass(frozen=True)
class PipelineResult:
    report_id: str
    generated_at: str
    source_name: str
    evidence: List[EvidenceObject]
    findings: List[EvidenceObject]
    zero_autonomy_boundary: Dict[str, Any]
    summary: Dict[str, Any]


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


ALLOWED_ACTIVITY_BY_CATEGORY = {
    "office_supplies": {"office_supplies", "general_trade"},
    "it_equipment": {"it_equipment", "it_services", "technology", "general_trade"},
    "it_services": {"it_services", "technology", "consulting"},
    "medical_equipment": {"medical_equipment", "medical_supplies"},
    "construction_services": {"construction_services", "engineering", "renovation"},
}


def main() -> None:
    result = run_pipeline(INPUT_DIR, OUTPUT_FILE)
    print(json.dumps({"status": "OK", "output": str(OUTPUT_FILE), "summary": result.summary}, indent=2))


def run_pipeline(input_dir: Path = INPUT_DIR, output_file: Path = OUTPUT_FILE) -> PipelineResult:
    procurement_file = input_dir / "procurement_records.csv"
    suppliers_file = input_dir / "supplier_profiles.csv"
    benchmarks_file = input_dir / "price_benchmarks.csv"

    ensure_input_files_exist([procurement_file, suppliers_file, benchmarks_file])

    procurement_records = load_procurement_records(procurement_file)
    supplier_profiles = load_supplier_profiles(suppliers_file)
    price_benchmarks = load_price_benchmarks(benchmarks_file)

    evidence = analyze_records(procurement_records, supplier_profiles, price_benchmarks)
    result = build_pipeline_result(evidence)
    write_report(result, output_file)
    return result


def ensure_input_files_exist(paths: Iterable[Path]) -> None:
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise PipelineError("Missing required input file(s): " + ", ".join(missing))


def read_csv_rows(path: Path, logical_name: str) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise PipelineError(f"{path} has no header row.")
        actual_columns = {column.strip() for column in reader.fieldnames}
        missing = REQUIRED_COLUMNS[logical_name] - actual_columns
        if missing:
            raise PipelineError(f"{path} is missing required columns: {sorted(missing)}")
        return [{key.strip(): (value or "").strip() for key, value in row.items()} for row in reader]


def load_procurement_records(path: Path) -> List[ProcurementRecord]:
    rows = read_csv_rows(path, "procurement_records")
    records: List[ProcurementRecord] = []
    for index, row in enumerate(rows, start=2):
        records.append(
            ProcurementRecord(
                record_id=required_text(row, "record_id", path, index),
                date=required_text(row, "date", path, index),
                department=required_text(row, "department", path, index),
                supplier_id=required_text(row, "supplier_id", path, index),
                item_category=normalize_token(required_text(row, "item_category", path, index)),
                item_name=required_text(row, "item_name", path, index),
                quantity=parse_decimal(required_text(row, "quantity", path, index), path, index, "quantity"),
                unit_price=parse_decimal(required_text(row, "unit_price", path, index), path, index, "unit_price"),
                total_value=parse_decimal(required_text(row, "total_value", path, index), path, index, "total_value"),
                currency=required_text(row, "currency", path, index).upper(),
                procurement_method=required_text(row, "procurement_method", path, index),
            )
        )
    return records


def load_supplier_profiles(path: Path) -> Dict[str, SupplierProfile]:
    rows = read_csv_rows(path, "supplier_profiles")
    profiles: Dict[str, SupplierProfile] = {}
    for index, row in enumerate(rows, start=2):
        profile = SupplierProfile(
            supplier_id=required_text(row, "supplier_id", path, index),
            supplier_name=required_text(row, "supplier_name", path, index),
            declared_activity=normalize_token(required_text(row, "declared_activity", path, index)),
            capacity_score=parse_decimal(required_text(row, "capacity_score", path, index), path, index, "capacity_score"),
            registration_status=required_text(row, "registration_status", path, index),
            country=required_text(row, "country", path, index),
        )
        profiles[profile.supplier_id] = profile
    return profiles


def load_price_benchmarks(path: Path) -> Dict[Tuple[str, str, str], PriceBenchmark]:
    rows = read_csv_rows(path, "price_benchmarks")
    benchmarks: Dict[Tuple[str, str, str], PriceBenchmark] = {}
    for index, row in enumerate(rows, start=2):
        benchmark = PriceBenchmark(
            item_category=normalize_token(required_text(row, "item_category", path, index)),
            item_name=required_text(row, "item_name", path, index),
            median_unit_price=parse_decimal(required_text(row, "median_unit_price", path, index), path, index, "median_unit_price"),
            currency=required_text(row, "currency", path, index).upper(),
            source=required_text(row, "source", path, index),
        )
        benchmarks[(benchmark.item_category, normalize_token(benchmark.item_name), benchmark.currency)] = benchmark
    return benchmarks


def analyze_records(
    procurement_records: List[ProcurementRecord],
    supplier_profiles: Dict[str, SupplierProfile],
    price_benchmarks: Dict[Tuple[str, str, str], PriceBenchmark],
) -> List[EvidenceObject]:
    evidence: List[EvidenceObject] = []

    for record in procurement_records:
        supplier = supplier_profiles.get(record.supplier_id)
        if supplier is None:
            evidence.append(build_missing_supplier_evidence(record, len(evidence) + 1))
            continue

        price_signal = detect_price_signal(record, supplier, price_benchmarks, len(evidence) + 1)
        if price_signal is not None:
            evidence.append(price_signal)

        capacity_signal = detect_supplier_capacity_signal(record, supplier, len(evidence) + 1)
        if capacity_signal is not None:
            evidence.append(capacity_signal)

        activity_signal = detect_supplier_activity_mismatch(record, supplier, len(evidence) + 1)
        if activity_signal is not None:
            evidence.append(activity_signal)

        quantity_signal = detect_unusual_quantity_signal(record, supplier, len(evidence) + 1)
        if quantity_signal is not None:
            evidence.append(quantity_signal)

    evidence.extend(detect_threshold_fragmentation(procurement_records, supplier_profiles, len(evidence) + 1))

    return renumber_evidence(evidence)


def detect_price_signal(
    record: ProcurementRecord,
    supplier: SupplierProfile,
    benchmarks: Dict[Tuple[str, str, str], PriceBenchmark],
    next_number: int,
) -> Optional[EvidenceObject]:
    benchmark = benchmarks.get((record.item_category, normalize_token(record.item_name), record.currency))
    if benchmark is None or benchmark.median_unit_price <= 0:
        return None

    ratio = safe_decimal_ratio(record.unit_price, benchmark.median_unit_price)
    if ratio < PRICE_HIGH_RATIO:
        return None

    severity = "CRITICAL" if ratio >= PRICE_CRITICAL_RATIO else "HIGH"
    detected_signal = (
        f"Observed unit price ({format_money(record.unit_price)} {record.currency}) is "
        f"{format_ratio(ratio)}x benchmark median ({format_money(benchmark.median_unit_price)} {record.currency})."
    )

    return EvidenceObject(
        id=evidence_id(next_number),
        title="Price above benchmark",
        severity=severity,
        supplier=supplier.supplier_name,
        subject=supplier.supplier_name,
        detected_signal=detected_signal,
        risk_meaning=(
            "The paid or proposed unit price is materially higher than the benchmark. "
            "This may be legitimate, but it requires justification such as quality, urgency, "
            "specification, or market conditions."
        ),
        reviewer_question="Is there documented justification for the price difference?",
        recommendation="Escalate for human review before any institutional decision.",
        evidence_ids=[evidence_id(next_number)],
        source_records=[record.record_id],
        signal_family="price_above_benchmark",
        raw_context={
            "record_id": record.record_id,
            "item_category": record.item_category,
            "item_name": record.item_name,
            "unit_price": decimal_to_json(record.unit_price),
            "benchmark_median_unit_price": decimal_to_json(benchmark.median_unit_price),
            "ratio": decimal_to_json(ratio),
            "benchmark_source": benchmark.source,
        },
    )


def detect_supplier_capacity_signal(record: ProcurementRecord, supplier: SupplierProfile, next_number: int) -> Optional[EvidenceObject]:
    if supplier.capacity_score >= LOW_SUPPLIER_CAPACITY_THRESHOLD:
        return None
    if record.total_value < HIGH_VALUE_PROCUREMENT_THRESHOLD:
        return None

    return EvidenceObject(
        id=evidence_id(next_number),
        title="Supplier capacity risk",
        severity="HIGH",
        supplier=supplier.supplier_name,
        subject=supplier.supplier_name,
        detected_signal=(
            f"Low-capacity supplier ({format_decimal(supplier.capacity_score)}) received high-value "
            f"procurement ({format_money(record.total_value)} {record.currency})."
        ),
        risk_meaning=(
            "The supplier capacity appears weak relative to the procurement value. "
            "The reviewer should check whether the supplier can realistically deliver."
        ),
        reviewer_question="Can the supplier prove operational capability for this value and scope?",
        recommendation="Escalate for human review before any institutional decision.",
        evidence_ids=[evidence_id(next_number)],
        source_records=[record.record_id],
        signal_family="supplier_capacity_risk",
        raw_context={
            "record_id": record.record_id,
            "supplier_id": supplier.supplier_id,
            "capacity_score": decimal_to_json(supplier.capacity_score),
            "total_value": decimal_to_json(record.total_value),
            "currency": record.currency,
        },
    )


def detect_supplier_activity_mismatch(record: ProcurementRecord, supplier: SupplierProfile, next_number: int) -> Optional[EvidenceObject]:
    allowed = ALLOWED_ACTIVITY_BY_CATEGORY.get(record.item_category, set())
    if supplier.declared_activity in allowed:
        return None

    return EvidenceObject(
        id=evidence_id(next_number),
        title="Supplier activity mismatch",
        severity="MEDIUM",
        supplier=supplier.supplier_name,
        subject=supplier.supplier_name,
        detected_signal=(
            f"Supplier declared activity ('{supplier.declared_activity}') does not clearly align with "
            f"item category ('{record.item_category}'). This may be explainable, but it requires human review."
        ),
        risk_meaning=(
            "The supplier's declared activity does not clearly match the purchased category. "
            "This may indicate a documentation gap, subcontracting, or an unsuitable supplier."
        ),
        reviewer_question="Does the contract file explain why this supplier is suitable for this category?",
        recommendation="Request contextual verification and supporting evidence.",
        evidence_ids=[evidence_id(next_number)],
        source_records=[record.record_id],
        signal_family="supplier_activity_mismatch",
        raw_context={
            "record_id": record.record_id,
            "supplier_id": supplier.supplier_id,
            "declared_activity": supplier.declared_activity,
            "item_category": record.item_category,
        },
    )


def detect_unusual_quantity_signal(record: ProcurementRecord, supplier: SupplierProfile, next_number: int) -> Optional[EvidenceObject]:
    if record.quantity < LARGE_QUANTITY_THRESHOLD:
        return None

    return EvidenceObject(
        id=evidence_id(next_number),
        title="Unusual quantity signal",
        severity="MEDIUM",
        supplier=supplier.supplier_name,
        subject=supplier.supplier_name,
        detected_signal=(
            f"Large procurement quantity detected ({format_decimal(record.quantity)} units). "
            "The operational need and delivery context should be reviewed."
        ),
        risk_meaning="The quantity is large enough to require operational justification, delivery context, and need verification.",
        reviewer_question="Is the quantity supported by real need, delivery plan, and usage evidence?",
        recommendation="Request contextual verification and supporting evidence.",
        evidence_ids=[evidence_id(next_number)],
        source_records=[record.record_id],
        signal_family="unusual_quantity_signal",
        raw_context={
            "record_id": record.record_id,
            "quantity": decimal_to_json(record.quantity),
            "threshold": decimal_to_json(LARGE_QUANTITY_THRESHOLD),
        },
    )


def detect_threshold_fragmentation(
    records: List[ProcurementRecord],
    suppliers: Dict[str, SupplierProfile],
    start_number: int,
) -> List[EvidenceObject]:
    grouped: Dict[Tuple[str, str, str, str], List[ProcurementRecord]] = {}
    for record in records:
        if THRESHOLD_FRAGMENT_MIN_VALUE <= record.total_value <= THRESHOLD_FRAGMENT_MAX_VALUE:
            key = (record.supplier_id, record.department, record.item_category, record.currency)
            grouped.setdefault(key, []).append(record)

    evidence: List[EvidenceObject] = []
    next_number = start_number

    for (supplier_id, department, item_category, currency), group in sorted(grouped.items()):
        if len(group) < THRESHOLD_FRAGMENT_MIN_COUNT:
            continue
        supplier = suppliers.get(supplier_id)
        supplier_name = supplier.supplier_name if supplier else f"Unknown supplier ({supplier_id})"
        cumulative_value = sum_decimal(record.total_value for record in group)
        source_records = [record.record_id for record in group]

        for record in group:
            current_id = evidence_id(next_number)
            evidence.append(
                EvidenceObject(
                    id=current_id,
                    title="Threshold fragmentation pattern",
                    severity="HIGH",
                    supplier=supplier_name,
                    subject=supplier_name,
                    detected_signal=(
                        "Multiple threshold-near fragments detected for the same supplier, department, and category. "
                        f"Cumulative value: {format_money(cumulative_value)} {currency}."
                    ),
                    risk_meaning=(
                        "Several purchases appear close to a threshold and belong to the same supplier/category context. "
                        "This may indicate artificial splitting and should be reviewed as a cluster."
                    ),
                    reviewer_question=(
                        "Were these records split for legitimate operational reasons, or should they be treated as one procurement cluster?"
                    ),
                    recommendation="Escalate for human review before any institutional decision.",
                    evidence_ids=[current_id],
                    source_records=source_records,
                    signal_family="threshold_fragmentation_pattern",
                    raw_context={
                        "record_id": record.record_id,
                        "supplier_id": supplier_id,
                        "department": department,
                        "item_category": item_category,
                        "currency": currency,
                        "cluster_record_ids": source_records,
                        "cluster_count": len(group),
                        "cumulative_value": decimal_to_json(cumulative_value),
                    },
                )
            )
            next_number += 1

    return evidence


def build_missing_supplier_evidence(record: ProcurementRecord, next_number: int) -> EvidenceObject:
    current_id = evidence_id(next_number)
    return EvidenceObject(
        id=current_id,
        title="Missing supplier profile",
        severity="HIGH",
        supplier=f"Unknown supplier ({record.supplier_id})",
        subject=f"Unknown supplier ({record.supplier_id})",
        detected_signal=f"Procurement record references supplier_id '{record.supplier_id}', but no supplier profile was provided.",
        risk_meaning="Supplier identity or profile data is missing, which prevents normal supplier review.",
        reviewer_question="Can the institution provide a valid supplier profile for this procurement record?",
        recommendation="Request missing supplier profile before relying on the record.",
        evidence_ids=[current_id],
        source_records=[record.record_id],
        signal_family="missing_supplier_profile",
        raw_context={"record_id": record.record_id, "supplier_id": record.supplier_id},
    )


def renumber_evidence(evidence: List[EvidenceObject]) -> List[EvidenceObject]:
    renumbered: List[EvidenceObject] = []
    for index, item in enumerate(evidence, start=1):
        new_id = evidence_id(index)
        renumbered.append(
            EvidenceObject(
                id=new_id,
                title=item.title,
                severity=item.severity,
                supplier=item.supplier,
                subject=item.subject,
                detected_signal=item.detected_signal,
                risk_meaning=item.risk_meaning,
                reviewer_question=item.reviewer_question,
                recommendation=item.recommendation,
                evidence_ids=[new_id],
                source_records=item.source_records,
                signal_family=item.signal_family,
                raw_context=item.raw_context,
            )
        )
    return renumbered


def build_pipeline_result(evidence: List[EvidenceObject]) -> PipelineResult:
    generated_at = datetime.now(timezone.utc).isoformat()
    supplier_names = sorted({item.supplier for item in evidence})
    high_or_critical = [item for item in evidence if item.severity in {"HIGH", "CRITICAL"}]

    summary = {
        "findings_count": len(evidence),
        "evidence_count": len(evidence),
        "supplier_count": len(supplier_names),
        "high_or_critical_findings_count": len(high_or_critical),
        "reviewed_findings_count": 0,
        "signal_families": count_signal_families(evidence),
    }

    return PipelineResult(
        report_id="LOCAL_DEMO_REPORT",
        generated_at=generated_at,
        source_name="procurement_accounting_input_pipeline.py",
        evidence=evidence,
        findings=evidence,
        zero_autonomy_boundary={
            "autonomous_enforcement_actions": 0,
            "canonical_registry_opened": False,
            "canonical_registry_mutated": False,
            "production_records_mutated": False,
            "signing_or_key_access_performed": False,
            "external_execution_performed": False,
            "pipeline_mode": "LOCAL_READ_ONLY_DEMO",
        },
        summary=summary,
    )


def write_report(result: PipelineResult, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    payload = pipeline_result_to_json(result)
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def pipeline_result_to_json(result: PipelineResult) -> Dict[str, Any]:
    return {
        "report_id": result.report_id,
        "generated_at": result.generated_at,
        "source_name": result.source_name,
        "zero_autonomy_boundary": result.zero_autonomy_boundary,
        "summary": result.summary,
        "evidence": [evidence_to_json(item) for item in result.evidence],
        "findings": [evidence_to_json(item) for item in result.findings],
    }


def evidence_to_json(item: EvidenceObject) -> Dict[str, Any]:
    data = asdict(item)

    # Dashboard-compatible aliases.
    # The dashboard can read flexible JSON shapes, but it expects a human-readable
    # signal text under fields such as "reason" or "description".
    data["reason"] = item.detected_signal
    data["description"] = item.detected_signal
    data["type"] = "EVIDENCE_OBJECT"

    # Keep explicit semantic fields for future runtime consumers.
    data["signal_title"] = item.title
    data["risk_level"] = item.severity
    data["recommended_action"] = item.recommendation

    return data


def count_signal_families(evidence: List[EvidenceObject]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in evidence:
        counts[item.signal_family] = counts.get(item.signal_family, 0) + 1
    return counts


def required_text(row: Dict[str, str], column: str, path: Path, line_number: int) -> str:
    value = row.get(column, "").strip()
    if value == "":
        raise PipelineError(f"{path}:{line_number} has empty required value for column '{column}'.")
    return value


def parse_decimal(value: str, path: Path, line_number: int, column: str) -> Decimal:
    try:
        return Decimal(value.replace(",", "."))
    except (InvalidOperation, ValueError) as exc:
        raise PipelineError(f"{path}:{line_number} has invalid decimal value for column '{column}': {value}") from exc


def normalize_token(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def evidence_id(number: int) -> str:
    return f"EV-{number:03d}"


def safe_decimal_ratio(numerator: Decimal, denominator: Decimal) -> Decimal:
    if denominator == 0:
        return Decimal("0")
    return numerator / denominator


def format_money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def format_decimal(value: Decimal) -> str:
    normalized = value.normalize()
    return format(normalized, "f")


def format_ratio(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def decimal_to_json(value: Decimal) -> str:
    return format(value, "f")


def sum_decimal(values: Iterable[Decimal]) -> Decimal:
    total = Decimal("0")
    for value in values:
        total += value
    return total


if __name__ == "__main__":
    main()
