import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

import polars as pl

from acryl_datahub_cloud.periodic_analytics import schema
from acryl_datahub_cloud.periodic_analytics.constants import SCHEMA_VERSION, Layer
from acryl_datahub_cloud.periodic_analytics.partitions import HourPartition
from acryl_datahub_cloud.periodic_analytics.registry import MetricRegistry
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore

logger = logging.getLogger(__name__)

# JSONPath per access-channel dimensions-JSON key, precomputed once rather
# than re-formatted on every call.
_DIMENSION_JSON_PATHS: Dict[str, str] = {
    key: f"$.{key}" for key in schema.DIMENSION_KEYS
}

ADDITIVE_GROUP_COLS: List[str] = (
    ["customer_id", "instance_id"] + schema.DIMENSION_COLUMNS + ["actor_class"]
)
# Latest gauges: do not reuse ADDITIVE_GROUP_COLS (api_usage access-channel
# flats). Family-specific keys live in the opaque dimensions JSON.
LATEST_GROUP_COLS: List[str] = [
    "customer_id",
    "instance_id",
    "actor_class",
    "dimensions",
]
LATEST_OUTPUT_COLS: List[str] = [
    "customer_id",
    "instance_id",
    "actor_class",
    "dimensions",
    "metric_name",
    "value_sum",
    "metric_family",
    "granularity",
    "time_bucket",
    "merge_kind",
    "job_run_id",
    "computed_at",
    "schema_version",
]
DISTINCT_SELECT_COLS: List[str] = [
    "customer_id",
    "instance_id",
    "metric_name",
    "actor_class",
]

MERGE_KIND_ADDITIVE = "additive"
MERGE_KIND_DISTINCT = "distinct"
MERGE_KIND_LATEST = "latest"


@dataclass
class HourlyResult:
    rows_scanned: int
    additive_rows: int
    distinct_rows: int
    latest_rows: int
    unregistered_rows: int


def _bucket_metadata(
    time_bucket: str, granularity: str, merge_kind: str, job_run_id: str
) -> List[pl.Expr]:
    return [
        pl.lit(granularity).alias("granularity"),
        pl.lit(time_bucket).alias("time_bucket"),
        pl.lit(merge_kind).alias("merge_kind"),
        pl.lit(job_run_id).alias("job_run_id"),
        pl.lit(datetime.now(timezone.utc)).alias("computed_at"),
        pl.lit(SCHEMA_VERSION).alias("schema_version"),
    ]


def _extract_dimensions(lf: pl.LazyFrame) -> pl.LazyFrame:
    # Streaming-friendly per-key extraction (str.json_path_match) instead of a
    # full json_decode into a struct — a key absent from a row's JSON (the
    # writer omits usage_operation/actor_class when null) yields None, which
    # fill_null("") normalizes to the empty-string dimension value.
    # Only access-channel DIMENSION_KEYS are promoted; JSON-only keys
    # (entity_type, …) stay in the dimensions blob for latest grouping.
    return lf.with_columns(
        [
            pl.col("dimensions")
            .str.json_path_match(_DIMENSION_JSON_PATHS[key])
            .fill_null("")
            .alias(key)
            for key in schema.DIMENSION_KEYS
        ]
    )


def _write_hourly_buckets(
    store: ObjectStore,
    metric_family: str,
    hour: HourPartition,
    additive: pl.DataFrame,
    latest: pl.DataFrame,
) -> None:
    """Write additive and latest as separate files when both are non-empty.

    Keeps additive api_usage free of a dimensions column and latest gauges
    free of empty access-channel flats. Empty hours still land one empty
    additive-shaped file so the hour dir exists for watermarking.
    """
    hour_dir = store.hour_dir(metric_family, Layer.HOURLY, hour)
    if additive.height and latest.height:
        store.write_parquet(additive, hour_dir, store.new_file_name("bucket"))
        store.write_parquet(latest, hour_dir, store.new_file_name("bucket"))
        return
    if latest.height:
        store.write_parquet(latest, hour_dir, store.new_file_name("bucket"))
        return
    store.write_parquet(additive, hour_dir, store.new_file_name("bucket"))


def run_hourly_rollup(
    store: ObjectStore,
    registry: MetricRegistry,
    metric_family: str,
    hour: HourPartition,
    job_run_id: str,
) -> HourlyResult:
    events_dir = f"{store.layer_dir(metric_family, Layer.EVENTS)}/dt={hour.dt}"
    files = store.list_parquet_files(events_dir)

    if files:
        lf = store.scan_parquet(files)
        schema.assert_events_schema(lf)
        schema.assert_tenant_rows(
            lf, store.config.customer_id, store.config.instance_id
        )
        # Hour attribution: a row belongs to the UTC hour of its
        # window_start_us (spec). window_start_us is epoch microseconds, so
        # decode it and compare against tz-naive UTC bounds (from_epoch
        # yields a naive Datetime already representing the UTC instant).
        window_start = pl.from_epoch(pl.col("window_start_us"), time_unit="us")
        hour_start = hour.start.replace(tzinfo=None)
        hour_end = hour.end.replace(tzinfo=None)
        # No dedupe here: Tier B pre-aggregates before the events write, so no
        # message ids exist to dedupe against.
        hour_lf = lf.filter((window_start >= hour_start) & (window_start < hour_end))
        # rows_scanned reports the full dt-partition scan (pre hour-filter) —
        # it reflects I/O volume, not the post-filter row count.
        rows_scanned = lf.select(pl.len()).collect(engine="streaming").item()
    else:
        hour_lf = pl.LazyFrame(schema=schema.EVENTS_COLUMNS)
        rows_scanned = 0

    hour_lf = _extract_dimensions(hour_lf)

    additive_names = registry.additive_names(metric_family)
    distinct_names = registry.distinct_names(metric_family)
    latest_names = registry.latest_names(metric_family)
    known_names = set(additive_names) | set(distinct_names) | set(latest_names)

    unregistered_counts = (
        hour_lf.filter(~pl.col("metric_name").is_in(sorted(known_names)))
        .group_by("metric_name")
        .agg(pl.len().alias("row_count"))
        .collect(engine="streaming")
    )
    unregistered_rows = int(unregistered_counts["row_count"].sum() or 0)
    if unregistered_counts.height:
        # A metric_name landed in events without a matching registry entry
        # (e.g. schema shipped ahead of the registry update) — surface it to
        # operators and skip those rows rather than silently dropping or
        # misclassifying billable usage.
        logger.warning(
            "hourly rollup %s: %d row(s) for %d unregistered metric_name(s) "
            "skipped for family=%s: %s",
            hour.key,
            unregistered_rows,
            unregistered_counts.height,
            metric_family,
            dict(
                zip(
                    unregistered_counts["metric_name"].to_list(),
                    unregistered_counts["row_count"].to_list(),
                    strict=True,
                )
            ),
        )

    additive = (
        hour_lf.filter(pl.col("metric_name").is_in(additive_names))
        .group_by(ADDITIVE_GROUP_COLS + ["metric_name"])
        .agg(pl.col("value").sum().alias("value_sum"))
        .with_columns(pl.lit(metric_family).alias("metric_family"))
        .with_columns(
            _bucket_metadata(hour.key, "hourly", MERGE_KIND_ADDITIVE, job_run_id)
        )
        .collect(engine="streaming")
    )

    # Gauge: last sample wins per (tenant, actor_class, dimensions JSON,
    # metric_name). Order matches system_usage_sync/gauge.py —
    # (window_end_us, timestamp_ms) ascending.
    latest = (
        hour_lf.filter(pl.col("metric_name").is_in(latest_names))
        .sort(["window_end_us", "timestamp_ms"])
        .group_by(LATEST_GROUP_COLS + ["metric_name"])
        .agg(pl.col("value").last().alias("value_sum"))
        .with_columns(pl.lit(metric_family).alias("metric_family"))
        .with_columns(
            _bucket_metadata(hour.key, "hourly", MERGE_KIND_LATEST, job_run_id)
        )
        .select(LATEST_OUTPUT_COLS)
        .collect(engine="streaming")
    )

    distinct = (
        hour_lf.filter(pl.col("metric_name").is_in(distinct_names))
        .select(
            DISTINCT_SELECT_COLS + [pl.col("usage_identity").alias("distinct_value")]
        )
        .unique()
        .with_columns(pl.lit(metric_family).alias("metric_family"))
        .with_columns(
            _bucket_metadata(hour.key, "hourly", MERGE_KIND_DISTINCT, job_run_id)
        )
        .collect(engine="streaming")
    )

    # TG-8: both writes happen here; the CALLER advances the single hourly
    # watermark only after this function returns without raising.
    _write_hourly_buckets(store, metric_family, hour, additive, latest)
    store.write_parquet(
        distinct,
        store.hour_dir(metric_family, Layer.HOURLY_DISTINCT, hour),
        store.new_file_name("distinct"),
    )
    logger.info(
        "hourly rollup %s: %d events -> %d additive, %d latest, %d distinct "
        "(%d unregistered)",
        hour.key,
        rows_scanned,
        additive.height,
        latest.height,
        distinct.height,
        unregistered_rows,
    )
    return HourlyResult(
        rows_scanned=rows_scanned,
        additive_rows=additive.height,
        distinct_rows=distinct.height,
        latest_rows=latest.height,
        unregistered_rows=unregistered_rows,
    )
