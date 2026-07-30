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
from acryl_datahub_cloud.periodic_analytics.partitions import MonthPartition
from acryl_datahub_cloud.periodic_analytics.rollup.daily import (
    _assert_supported_bucket_kinds,
    _mean_int,
)
from acryl_datahub_cloud.periodic_analytics.rollup.hourly import (
    MERGE_KIND_ADDITIVE,
    MERGE_KIND_LATEST,
    _bucket_metadata,
)
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore

logger = logging.getLogger(__name__)


class MissingDailyInputError(Exception):
    def __init__(self, month: MonthPartition, missing_days: List[str]) -> None:
        self.month = month
        self.missing_days = missing_days
        # TG-3: monthly compaction requires every day of the calendar month to
        # be complete — no partial aggregation fallback is supported, by
        # design.
        super().__init__(
            f"cannot compact period={month.key}: {len(missing_days)} daily partition(s) "
            f"have not been rolled up yet ({missing_days}); run the daily rollup "
            "(catch-up or restate) first"
        )


def _collect_day_files(
    store: ObjectStore, metric_family: str, month: MonthPartition
) -> List[str]:
    files: List[str] = []
    missing: List[str] = []
    for day in month.days:
        day_files = store.list_parquet_files(
            store.day_dir(metric_family, Layer.DAILY_ADDITIVE, day)
        )
        if not day_files:
            missing.append(day.key)
        files.extend(day_files)
    if missing:
        raise MissingDailyInputError(month, missing)
    return files


def run_compact_monthly(
    store: ObjectStore,
    metric_family: str,
    month: MonthPartition,
    job_run_id: str,
    daily_wm: WatermarkStore,
) -> int:
    files = _collect_day_files(store, metric_family, month)
    authoritative = authoritative_job_run_ids(
        daily_wm, [d.key for d in month.days], Layer.DAILY_ADDITIVE.value
    )
    lf = fence_by_job_run_id(store.scan_bucket_parquet(files), authoritative)
    _assert_supported_bucket_kinds(lf, Layer.MONTHLY.value)

    additive = (
        lf.filter(pl.col("merge_kind") == MERGE_KIND_ADDITIVE)
        .group_by(BUCKET_GROUP_KEYS)
        .agg(pl.col("value_sum").sum())
        .with_columns(
            _bucket_metadata(month.key, "monthly", MERGE_KIND_ADDITIVE, job_run_id)
        )
        .collect(engine="streaming")
    )
    latest = (
        lf.filter(pl.col("merge_kind") == MERGE_KIND_LATEST)
        .group_by(LATEST_BUCKET_GROUP_KEYS)
        .agg(_mean_int(pl.col("value_sum")).alias("value_sum"))
        .with_columns(
            _bucket_metadata(month.key, "monthly", MERGE_KIND_LATEST, job_run_id)
        )
        .collect(engine="streaming")
    )
    period_dir = store.period_dir(metric_family, Layer.MONTHLY, month.key)
    if additive.height and latest.height:
        store.write_parquet(additive, period_dir, store.new_file_name("bucket"))
        store.write_parquet(latest, period_dir, store.new_file_name("bucket"))
    elif latest.height:
        store.write_parquet(latest, period_dir, store.new_file_name("bucket"))
    else:
        store.write_parquet(additive, period_dir, store.new_file_name("bucket"))
    rows = additive.height + latest.height
    logger.info(
        "monthly compaction period=%s: %d rows (additive+latest)",
        month.key,
        rows,
    )
    return rows
