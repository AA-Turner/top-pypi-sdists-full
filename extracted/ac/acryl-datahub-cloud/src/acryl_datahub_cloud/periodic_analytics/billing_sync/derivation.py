from typing import Dict, List, Optional, Set

import polars as pl

from acryl_datahub_cloud.periodic_analytics.billing_sync.mtd import (
    period_files_through_hour,
    scan_with_daily_fence,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.usage_operations import (
    UsageOperationsConfig,
)
from acryl_datahub_cloud.periodic_analytics.constants import Layer
from acryl_datahub_cloud.periodic_analytics.fencing import authoritative_job_run_ids
from acryl_datahub_cloud.periodic_analytics.partitions import HourPartition
from acryl_datahub_cloud.periodic_analytics.registry import (
    RULE_FILTER_INGESTION_ENDPOINT,
    RULE_MULTIPLY_DEFAULT_COST_UNITS,
    RULE_PERIOD_DISTINCT,
    RULE_SUM_BILLABLE_ENTITY_TYPES,
    MetricRegistry,
    MetricSpec,
)
from acryl_datahub_cloud.periodic_analytics.schema import actor_class_in_expr
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore
from datahub.ingestion.api.source import SourceReport

UNKNOWN_USAGE_OPERATION_LABEL = "<absent>"


def compute_derived_metrics(
    store: ObjectStore,
    registry: MetricRegistry,
    usage_operations: UsageOperationsConfig,
    metric_family: str,
    period: str,
    as_of_hour: HourPartition,
    excluded_identities: List[str],
    report: SourceReport,
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
    daily_completed: Optional[Set[str]] = None,
) -> Dict[str, int]:
    derived = {
        name: spec
        for name, spec in registry.metrics(metric_family).items()
        if spec.is_derived
    }
    if not derived:
        return {}

    if as_of_hour.day.month.key != period:
        raise ValueError(f"as_of_hour {as_of_hour.key!r} is not in period {period!r}")
    daily_done = daily_completed if daily_completed is not None else set()
    values: Dict[str, int] = {}
    for name, spec in sorted(derived.items()):
        if spec.rule == RULE_FILTER_INGESTION_ENDPOINT:
            values[name] = _filter_ingestion_endpoint(
                store,
                metric_family,
                as_of_hour,
                daily_done,
                spec,
                usage_operations,
                report,
                name,
                daily_wm,
                hourly_wm,
            )
        elif spec.rule == RULE_MULTIPLY_DEFAULT_COST_UNITS:
            values[name] = _multiply_default_cost_units(
                store,
                metric_family,
                as_of_hour,
                daily_done,
                spec,
                usage_operations,
                report,
                name,
                daily_wm,
                hourly_wm,
            )
        elif spec.rule == RULE_PERIOD_DISTINCT:
            values[name] = _period_distinct(
                store,
                metric_family,
                as_of_hour,
                daily_done,
                spec,
                excluded_identities,
                daily_wm,
                hourly_wm,
            )
        elif spec.rule == RULE_SUM_BILLABLE_ENTITY_TYPES:
            raise ValueError(
                f"{name} uses rule={RULE_SUM_BILLABLE_ENTITY_TYPES} which must be "
                "computed on the system_usage gauge path in billing-sync "
                "(LATEST from sealed hourly_buckets or OpenAPI, not additive MTD) "
                "— refusing api_usage derivation path"
            )
        else:
            raise ValueError(f"unrecognized derivation rule {spec.rule!r} for {name}")
    return values


def _grouped_additive_source_rows(
    store: ObjectStore,
    metric_family: str,
    as_of_hour: HourPartition,
    daily_completed: Set[str],
    source_names: List[str],
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
    billable_actor_classes: List[str],
) -> pl.DataFrame:
    scan = period_files_through_hour(
        store,
        metric_family,
        Layer.DAILY_ADDITIVE,
        Layer.HOURLY,
        as_of_hour,
        daily_completed,
    )
    authoritative = (
        authoritative_job_run_ids(daily_wm, scan.day_keys, Layer.DAILY_ADDITIVE.value)
        if scan.day_keys
        else {}
    )
    hourly_authoritative = (
        authoritative_job_run_ids(hourly_wm, scan.hour_keys, Layer.HOURLY.value)
        if scan.hour_keys
        else {}
    )
    lf = scan_with_daily_fence(store, scan, authoritative, hourly_authoritative)
    if lf is None:
        return pl.DataFrame(schema={"usage_operation": pl.Utf8, "value_sum": pl.Int64})
    return (
        lf.filter(
            pl.col("metric_name").is_in(source_names)
            & actor_class_in_expr(billable_actor_classes)
        )
        .group_by("usage_operation")
        .agg(pl.col("value_sum").sum())
        .collect(engine="streaming")
    )


def _report_unknown_usage_operations(
    report: SourceReport, metric_name: str, unknown_ops: Dict[str, int]
) -> None:
    if not unknown_ops:
        return
    report.warning(
        title="unknown usage_operation in derived metric computation",
        message=(
            f"derived metric {metric_name}: {len(unknown_ops)} unknown "
            f"usage_operation value(s) totalling {sum(unknown_ops.values())} "
            f"source unit(s): {sorted(unknown_ops)}"
        ),
    )


def _filter_ingestion_endpoint(
    store: ObjectStore,
    metric_family: str,
    as_of_hour: HourPartition,
    daily_completed: Set[str],
    spec: MetricSpec,
    usage_operations: UsageOperationsConfig,
    report: SourceReport,
    name: str,
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
) -> int:
    grouped = _grouped_additive_source_rows(
        store,
        metric_family,
        as_of_hour,
        daily_completed,
        spec.derived_from or [],
        daily_wm,
        hourly_wm,
        spec.require_billable_actor_classes(),
    )
    total = 0
    unknown_ops: Dict[str, int] = {}
    for usage_operation, value_sum in grouped.iter_rows():
        if not usage_operations.is_known(usage_operation):
            label = usage_operation or UNKNOWN_USAGE_OPERATION_LABEL
            unknown_ops[label] = unknown_ops.get(label, 0) + int(value_sum)
            continue
        if usage_operations.is_ingestion_endpoint(usage_operation):
            total += int(value_sum)
    _report_unknown_usage_operations(report, name, unknown_ops)
    return total


def _multiply_default_cost_units(
    store: ObjectStore,
    metric_family: str,
    as_of_hour: HourPartition,
    daily_completed: Set[str],
    spec: MetricSpec,
    usage_operations: UsageOperationsConfig,
    report: SourceReport,
    name: str,
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
) -> int:
    grouped = _grouped_additive_source_rows(
        store,
        metric_family,
        as_of_hour,
        daily_completed,
        spec.derived_from or [],
        daily_wm,
        hourly_wm,
        spec.require_billable_actor_classes(),
    )
    total = 0
    unknown_ops: Dict[str, int] = {}
    for usage_operation, value_sum in grouped.iter_rows():
        if not usage_operations.is_known(usage_operation):
            label = usage_operation or UNKNOWN_USAGE_OPERATION_LABEL
            unknown_ops[label] = unknown_ops.get(label, 0) + int(value_sum)
        total += int(value_sum) * usage_operations.default_cost_units(usage_operation)
    _report_unknown_usage_operations(report, name, unknown_ops)
    return total


def _period_distinct(
    store: ObjectStore,
    metric_family: str,
    as_of_hour: HourPartition,
    daily_completed: Set[str],
    spec: MetricSpec,
    excluded_identities: List[str],
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
) -> int:
    scan = period_files_through_hour(
        store,
        metric_family,
        Layer.DAILY_DISTINCT,
        Layer.HOURLY_DISTINCT,
        as_of_hour,
        daily_completed,
    )
    # R11: DAILY_DISTINCT shares the DAILY_ADDITIVE watermark (see mtd.py).
    authoritative = (
        authoritative_job_run_ids(daily_wm, scan.day_keys, Layer.DAILY_ADDITIVE.value)
        if scan.day_keys
        else {}
    )
    # R11: HOURLY_DISTINCT shares the single HOURLY watermark (see mtd.py /
    # rollup/daily.py's run_compact_daily_distinct).
    hourly_authoritative = (
        authoritative_job_run_ids(
            hourly_wm, scan.hour_keys, Layer.HOURLY_DISTINCT.value
        )
        if scan.hour_keys
        else {}
    )
    lf = scan_with_daily_fence(
        store,
        scan,
        authoritative,
        hourly_authoritative,
        bucket_schema=False,
    )
    if lf is None:
        return 0
    count = (
        lf.filter(
            pl.col("metric_name").is_in(spec.derived_from or [])
            & actor_class_in_expr(spec.require_billable_actor_classes())
            & ~pl.col("distinct_value").is_in(excluded_identities)
        )
        .select(pl.col("distinct_value").n_unique())
        .collect(engine="streaming")
        .item()
    )
    return int(count or 0)
