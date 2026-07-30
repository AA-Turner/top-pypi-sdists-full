import logging
from typing import List

import polars as pl

from acryl_datahub_cloud.periodic_analytics.constants import (
    BUCKET_GROUP_KEYS,
    LATEST_BUCKET_GROUP_KEYS,
    Layer,
)
from acryl_datahub_cloud.periodic_analytics.fencing import (
    authoritative_job_run_ids,
    fence_by_job_run_id,
)
from acryl_datahub_cloud.periodic_analytics.partitions import DayPartition
from acryl_datahub_cloud.periodic_analytics.rollup.hourly import (
    MERGE_KIND_ADDITIVE,
    MERGE_KIND_LATEST,
    _bucket_metadata,
)
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore

logger = logging.getLogger(__name__)

# Sidecar identity key, excluding the identity payload column itself — callers
# select SIDECAR_KEYS + ["distinct_value"] so the union/unique step de-dupes on
# the full identity, not just the dimension slice.
SIDECAR_KEYS: List[str] = [
    "customer_id",
    "instance_id",
    "metric_family",
    "metric_name",
    "actor_class",
]

# Supported merge_kind values in hourly_buckets input for daily compaction.
_SUPPORTED_BUCKET_MERGE_KINDS = {MERGE_KIND_ADDITIVE, MERGE_KIND_LATEST}


class MissingHourlyInputError(Exception):
    def __init__(self, day: DayPartition, missing_hours: List[str]) -> None:
        self.day = day
        self.missing_hours = missing_hours
        # TG-3: daily compaction requires all 24 hourly watermarks — no partial
        # aggregation fallback is supported, by design.
        super().__init__(
            f"cannot compact dt={day.key}: {len(missing_hours)} hourly partition(s) "
            f"have not been rolled up yet ({missing_hours}); run the hourly rollup "
            "(catch-up or restate) first"
        )


class UnsupportedMergeKindError(Exception):
    def __init__(self, layer: str, found_kinds: List[str]) -> None:
        self.layer = layer
        self.found_kinds = found_kinds
        super().__init__(
            f"refusing to compact {layer} input containing merge_kind(s) "
            f"{found_kinds}: supported bucket kinds are "
            f"{sorted(_SUPPORTED_BUCKET_MERGE_KINDS)} (additive=sum, "
            "latest=mean of hourly gauges); distinct uses the sidecar path"
        )


def _collect_hour_files(
    store: ObjectStore, metric_family: str, day: DayPartition, layer: Layer
) -> List[str]:
    files: List[str] = []
    missing: List[str] = []
    for hour in day.hours:
        hour_files = store.list_parquet_files(
            store.hour_dir(metric_family, layer, hour)
        )
        if not hour_files:
            missing.append(hour.key)
        files.extend(hour_files)
    if missing:
        raise MissingHourlyInputError(day, missing)
    return files


def _assert_supported_bucket_kinds(lf: pl.LazyFrame, layer: str) -> None:
    kinds = (
        lf.select(pl.col("merge_kind").unique())
        .collect(engine="streaming")["merge_kind"]
        .to_list()
    )
    foreign = [k for k in kinds if k not in _SUPPORTED_BUCKET_MERGE_KINDS]
    if foreign:
        raise UnsupportedMergeKindError(layer, foreign)


def _mean_int(expr: pl.Expr) -> pl.Expr:
    """Sparse mean over present hours, rounded to int64 for Metronome/storage."""
    return expr.mean().round(0).cast(pl.Int64)


def run_compact_daily_additive(
    store: ObjectStore,
    metric_family: str,
    day: DayPartition,
    job_run_id: str,
    hourly_wm: WatermarkStore,
) -> int:
    """Compact hourly_buckets: additive→sum, latest→mean (sparse over hours present).

    Name retained for callers; output may contain both merge_kind rows.
    """
    files = _collect_hour_files(store, metric_family, day, Layer.HOURLY)
    authoritative = authoritative_job_run_ids(
        hourly_wm, [h.key for h in day.hours], Layer.HOURLY.value
    )
    lf = fence_by_job_run_id(store.scan_bucket_parquet(files), authoritative)
    _assert_supported_bucket_kinds(lf, Layer.DAILY_ADDITIVE.value)

    additive = (
        lf.filter(pl.col("merge_kind") == MERGE_KIND_ADDITIVE)
        .group_by(BUCKET_GROUP_KEYS)
        .agg(pl.col("value_sum").sum())
        .with_columns(
            _bucket_metadata(day.key, "daily", MERGE_KIND_ADDITIVE, job_run_id)
        )
        .collect(engine="streaming")
    )
    # Sparse mean: hours without a row for a key do not contribute (not zero-
    # filled). Matches intermittent gauge publishes. Uses latest-only group
    # keys (opaque dimensions) — not additive access-channel flats.
    latest = (
        lf.filter(pl.col("merge_kind") == MERGE_KIND_LATEST)
        .group_by(LATEST_BUCKET_GROUP_KEYS)
        .agg(_mean_int(pl.col("value_sum")).alias("value_sum"))
        .with_columns(_bucket_metadata(day.key, "daily", MERGE_KIND_LATEST, job_run_id))
        .collect(engine="streaming")
    )
    day_dir = store.day_dir(metric_family, Layer.DAILY_ADDITIVE, day)
    if additive.height and latest.height:
        store.write_parquet(additive, day_dir, store.new_file_name("bucket"))
        store.write_parquet(latest, day_dir, store.new_file_name("bucket"))
    elif latest.height:
        store.write_parquet(latest, day_dir, store.new_file_name("bucket"))
    else:
        store.write_parquet(additive, day_dir, store.new_file_name("bucket"))
    rows = additive.height + latest.height
    logger.info(
        "daily bucket compaction dt=%s: %d rows (additive+latest)",
        day.key,
        rows,
    )
    return rows


def run_compact_daily_distinct(
    store: ObjectStore,
    metric_family: str,
    day: DayPartition,
    job_run_id: str,
    hourly_wm: WatermarkStore,
) -> int:
    files = _collect_hour_files(store, metric_family, day, Layer.HOURLY_DISTINCT)
    # R11: HOURLY_DISTINCT shares the single HOURLY watermark (see
    # rollup_source.py), so the same authoritative-generation map applies.
    authoritative = authoritative_job_run_ids(
        hourly_wm, [h.key for h in day.hours], Layer.HOURLY_DISTINCT.value
    )
    df = (
        fence_by_job_run_id(store.scan_parquet(files), authoritative)
        .select(SIDECAR_KEYS + ["distinct_value"])
        .unique()
        .with_columns(_bucket_metadata(day.key, "daily", "distinct", job_run_id))
        .collect(engine="streaming")
    )
    store.write_parquet(
        df,
        store.day_dir(metric_family, Layer.DAILY_DISTINCT, day),
        store.new_file_name("distinct"),
    )
    logger.info("daily distinct compaction dt=%s: %d rows", day.key, df.height)
    return df.height
