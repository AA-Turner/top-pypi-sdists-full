from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Set, Tuple

import polars as pl

from acryl_datahub_cloud.periodic_analytics.billing_sync.mtd_keys import format_mtd_key
from acryl_datahub_cloud.periodic_analytics.constants import Layer
from acryl_datahub_cloud.periodic_analytics.fencing import (
    authoritative_job_run_ids,
    fence_by_job_run_id,
)
from acryl_datahub_cloud.periodic_analytics.partitions import (
    DayPartition,
    HourPartition,
    MonthPartition,
    days_of_period_through,
    hours_of_period_through,
)
from acryl_datahub_cloud.periodic_analytics.registry import MetricRegistry
from acryl_datahub_cloud.periodic_analytics.rollup.monthly import MissingDailyInputError
from acryl_datahub_cloud.periodic_analytics.schema import actor_class_in_expr
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore


def _nonblank_dimension_values(
    metric_family: str,
    metric_name: str,
    dims: List[str],
    row: Dict[str, object],
    total: int,
) -> Optional[Dict[str, str]]:
    """Return dim→value for MTD keying, or None for a zero blank combo.

    Null/empty dimension values must not become ``request_api=""`` (etc.) keys:
    Metronome billable metrics filter on concrete channel labels and would miss
    those buckets. Positive totals with a blank dim hard-fail so billable
    traffic is not silently dropped.
    """
    values: Dict[str, str] = {}
    blank_dims: List[str] = []
    for dim in dims:
        raw = row[dim]
        if raw is None:
            blank_dims.append(dim)
            continue
        text = str(raw).strip()
        if not text:
            blank_dims.append(dim)
            continue
        values[dim] = text
    if not blank_dims:
        return values
    if total == 0:
        return None
    raise ValueError(
        f"{metric_family}.{metric_name} has billable rows with blank "
        f"metronome_dimensions {blank_dims} (value_sum={total}) — refusing "
        "to emit an empty-dimension MTD key that Metronome filters would miss"
    )


def _metrics_by_actor_classes(
    registry: MetricRegistry, metric_family: str, names: List[str]
) -> Dict[Tuple[str, ...], List[str]]:
    grouped: Dict[Tuple[str, ...], List[str]] = defaultdict(list)
    for name in names:
        classes = tuple(
            registry.spec(metric_family, name).require_billable_actor_classes()
        )
        grouped[classes].append(name)
    return grouped


def _accumulate_dimensional_additive(
    mtd: Dict[str, int],
    additive_lf: pl.LazyFrame,
    registry: MetricRegistry,
    metric_family: str,
    dim_additive: List[str],
) -> None:
    # Dimensional metrics (e.g. api_calls × request_api) keep one MTD key per
    # dim combo. Blank dim values are refused — see _nonblank_dimension_values.
    # Each metric applies its own billable_actor_classes allowlist.
    for name in dim_additive:
        billable = actor_class_in_expr(
            registry.spec(metric_family, name).require_billable_actor_classes()
        )
        dims = registry.spec(metric_family, name).metronome_dimensions
        missing = [d for d in dims if d not in additive_lf.collect_schema().names()]
        if missing:
            raise ValueError(
                f"{metric_family}.{name} metronome_dimensions {missing} "
                "missing from additive bucket columns"
            )
        dim_totals = (
            additive_lf.filter((pl.col("metric_name") == name) & billable)
            .group_by(dims)
            .agg(pl.col("value_sum").sum())
            .collect(engine="streaming")
        )
        for row in dim_totals.iter_rows(named=True):
            total = int(row.pop("value_sum"))
            dim_values = _nonblank_dimension_values(
                metric_family, name, dims, row, total
            )
            if dim_values is None:
                continue
            mtd[format_mtd_key(name, dim_values)] = total
        # Ensure a zero key is not required — absent dims simply omit.


def resolve_contiguous_as_of_hour(
    period: str,
    hourly_completed: Set[str],
    now: datetime,
    lag_minutes: int,
) -> Optional[HourPartition]:
    """Latest hour H in ``period`` with contiguous watermarks and input lag elapsed."""
    if now.tzinfo is None:
        raise ValueError("resolve_contiguous_as_of_hour requires a timezone-aware now")
    now_utc = now.astimezone(timezone.utc)
    lag = timedelta(minutes=lag_minutes)
    last: Optional[HourPartition] = None
    for day in MonthPartition.from_key(period).days:
        for hour in day.hours:
            if now_utc < hour.end + lag:
                return last
            if hour.key not in hourly_completed:
                return last
            last = hour
    return last


def period_files(
    store: ObjectStore, metric_family: str, layer: Layer, days: List[DayPartition]
) -> List[str]:
    # Shared with billing_sync/derivation.py for day-only scans.
    files: List[str] = []
    missing: List[str] = []
    for day in days:
        day_files = store.list_parquet_files(store.day_dir(metric_family, layer, day))
        if not day_files:
            missing.append(day.key)
        files.extend(day_files)
    if missing:
        raise MissingDailyInputError(days[0].month, missing)
    return files


def _hour_files(
    store: ObjectStore,
    metric_family: str,
    layer: Layer,
    hours: List[HourPartition],
) -> List[str]:
    files: List[str] = []
    for hour in hours:
        # Empty rolled-up hours may have a watermark but no parquet when
        # there was no activity — treat missing files as zero contribution.
        files.extend(
            store.list_parquet_files(store.hour_dir(metric_family, layer, hour))
        )
    return files


@dataclass
class PeriodFileScan:
    # Split by source grain so callers can fence each side against its own
    # watermark's authoritative generation (RunLock steal protection -- see
    # fencing.py). A rollup lease-steal can leave an orphaned generation
    # beside the winner's output at EITHER grain -- daily compaction and
    # hourly rollup both write unique-per-run filenames -- so both day_files
    # and hour_files must be fenced before use; see scan_with_daily_fence.
    day_files: List[str]
    day_keys: List[str]
    hour_files: List[str]
    hour_keys: List[str]


def period_files_through_hour(
    store: ObjectStore,
    metric_family: str,
    daily_layer: Layer,
    hourly_layer: Layer,
    as_of_hour: HourPartition,
    daily_completed: Set[str],
) -> PeriodFileScan:
    """Hybrid daily (complete days) + hourly (as_of day / incomplete days) file list."""
    day_files: List[str] = []
    day_keys: List[str] = []
    hour_files: List[str] = []
    hour_keys: List[str] = []
    period = as_of_hour.day.month.key
    for day in MonthPartition.from_key(period).days:
        if day.key > as_of_hour.dt:
            break
        if day.key < as_of_hour.dt:
            if day.key in daily_completed:
                completed_day_files = store.list_parquet_files(
                    store.day_dir(metric_family, daily_layer, day)
                )
                if not completed_day_files:
                    raise MissingDailyInputError(day.month, [day.key])
                day_files.extend(completed_day_files)
                day_keys.append(day.key)
            else:
                hour_files.extend(
                    _hour_files(store, metric_family, hourly_layer, day.hours)
                )
                hour_keys.extend(h.key for h in day.hours)
            continue
        # as_of day: prefer full daily when the day is complete and as_of is
        # end-of-day; otherwise sum/union hourly through as_of.hour.
        if as_of_hour.hour == 23 and day.key in daily_completed:
            completed_day_files = store.list_parquet_files(
                store.day_dir(metric_family, daily_layer, day)
            )
            if not completed_day_files:
                raise MissingDailyInputError(day.month, [day.key])
            day_files.extend(completed_day_files)
            day_keys.append(day.key)
        else:
            hours = [h for h in day.hours if h.hour <= as_of_hour.hour]
            hour_files.extend(_hour_files(store, metric_family, hourly_layer, hours))
            hour_keys.extend(h.key for h in hours)
    return PeriodFileScan(
        day_files=day_files,
        day_keys=day_keys,
        hour_files=hour_files,
        hour_keys=hour_keys,
    )


def scan_with_daily_fence(
    store: ObjectStore,
    scan: PeriodFileScan,
    authoritative: Dict[str, str],
    hourly_authoritative: Dict[str, str],
    *,
    bucket_schema: bool = True,
) -> Optional[pl.LazyFrame]:
    """Fences both the day-sourced and hour-sourced portions of a
    period_files_through_hour scan against their respective watermarks'
    authoritative generation -- see PeriodFileScan. A rollup lease-steal can
    leave an orphaned hourly generation beside the winner's bucket-<uuid>.parquet
    (the hourly watermark records only the winner's job_run_id), so the
    hour-sourced read needs the same fence rollup/daily.py already applies
    when it merges hourly output into daily compaction.

    bucket_schema=True uses the additive/latest union schema (access-channel
    flats + opaque dimensions). Distinct sidecars must pass False — they carry
    distinct_value, which is not in BUCKET_SCAN_SCHEMA and would be dropped.
    """
    scan_fn = store.scan_bucket_parquet if bucket_schema else store.scan_parquet
    frames: List[pl.LazyFrame] = []
    if scan.day_files:
        frames.append(fence_by_job_run_id(scan_fn(scan.day_files), authoritative))
    if scan.hour_files:
        frames.append(
            fence_by_job_run_id(scan_fn(scan.hour_files), hourly_authoritative)
        )
    if not frames:
        return None
    if len(frames) == 1:
        return frames[0]
    # Day-sourced (DAILY_ADDITIVE/DAILY_DISTINCT) and hour-sourced (HOURLY/
    # HOURLY_DISTINCT) parquet share the same column set but not the same
    # column order (they're built by separate row-construction code paths),
    # so "vertical" concat's strict schema match fails; "diagonal" aligns by
    # column name instead.
    return pl.concat(frames, how="diagonal")


def compute_mtd(
    store: ObjectStore,
    registry: MetricRegistry,
    metric_family: str,
    period: str,
    as_of_hour: HourPartition,
    excluded_identities: List[str],
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
    daily_completed: Optional[Set[str]] = None,
) -> Dict[str, int]:
    if as_of_hour.day.month.key != period:
        raise ValueError(f"as_of_hour {as_of_hour.key!r} is not in period {period!r}")
    daily_done = daily_completed if daily_completed is not None else set()
    metronome = set(registry.metronome_names(metric_family))
    additive = [n for n in registry.additive_names(metric_family) if n in metronome]
    distinct = [n for n in registry.distinct_names(metric_family) if n in metronome]
    # Dimensional metronome metrics omit a flat zero key — MTD keys are only
    # emitted per metronome_dimensions combo (see format_mtd_key).
    mtd: Dict[str, int] = {
        name: 0
        for name in metronome
        if not registry.spec(metric_family, name).metronome_dimensions
    }

    # period_files_through_hour's missing-day check runs (and can raise)
    # before the authoritative-generation lookup below, same precedence as
    # before this fence existed -- a day with no rollup output at all is
    # still reported as MissingDailyInputError, not the fencing error.
    additive_scan = period_files_through_hour(
        store, metric_family, Layer.DAILY_ADDITIVE, Layer.HOURLY, as_of_hour, daily_done
    )
    distinct_scan = period_files_through_hour(
        store,
        metric_family,
        Layer.DAILY_DISTINCT,
        Layer.HOURLY_DISTINCT,
        as_of_hour,
        daily_done,
    )
    # R11: DAILY_ADDITIVE/DAILY_DISTINCT share one watermark, so the same
    # authoritative-generation map fences both day-sourced scans below (the
    # two scans always agree on which days are daily_completed, since both
    # are driven by the same daily_done/as_of_hour inputs). The single HOURLY
    # watermark (shared by HOURLY/HOURLY_DISTINCT the same way) fences both
    # hour-sourced scans below for the identical reason -- both are driven by
    # the same daily_done/as_of_hour inputs, so their hour_keys always agree.
    authoritative = (
        authoritative_job_run_ids(
            daily_wm, additive_scan.day_keys, Layer.DAILY_ADDITIVE.value
        )
        if additive_scan.day_keys
        else {}
    )
    hourly_authoritative = (
        authoritative_job_run_ids(
            hourly_wm, additive_scan.hour_keys, Layer.HOURLY.value
        )
        if additive_scan.hour_keys
        else {}
    )

    additive_lf = scan_with_daily_fence(
        store, additive_scan, authoritative, hourly_authoritative
    )
    if additive and additive_lf is not None:
        # Split flat vs dimensional metronome additives. Dimensional metrics
        # (e.g. api_calls × request_api) keep one MTD key per dim combo.
        flat_additive = [
            n
            for n in additive
            if not registry.spec(metric_family, n).metronome_dimensions
        ]
        dim_additive = [
            n for n in additive if registry.spec(metric_family, n).metronome_dimensions
        ]
        for classes, names in _metrics_by_actor_classes(
            registry, metric_family, flat_additive
        ).items():
            additive_totals = (
                additive_lf.filter(
                    pl.col("metric_name").is_in(names) & actor_class_in_expr(classes)
                )
                .group_by("metric_name")
                .agg(pl.col("value_sum").sum())
                .collect(engine="streaming")
            )
            for name, total in additive_totals.iter_rows():
                mtd[name] = int(total)
        _accumulate_dimensional_additive(
            mtd, additive_lf, registry, metric_family, dim_additive
        )

    distinct_lf = scan_with_daily_fence(
        store,
        distinct_scan,
        authoritative,
        hourly_authoritative,
        bucket_schema=False,
    )
    if distinct and distinct_lf is not None:
        # DP-25 identity exclusions apply on top of each metric's actor_class
        # allowlist from the registry.
        for classes, names in _metrics_by_actor_classes(
            registry, metric_family, distinct
        ).items():
            distinct_counts = (
                distinct_lf.filter(
                    pl.col("metric_name").is_in(names)
                    & actor_class_in_expr(classes)
                    & ~pl.col("distinct_value").is_in(excluded_identities)  # DP-25
                )
                .group_by("metric_name")
                .agg(pl.col("distinct_value").n_unique())  # TG-7 union-then-count
                .collect(engine="streaming")
            )
            for name, count in distinct_counts.iter_rows():
                mtd[name] = int(count)
    return mtd


# Retained for callers/tests that still pass a day key; prefer compute_mtd.
def compute_mtd_through_date(
    store: ObjectStore,
    registry: MetricRegistry,
    metric_family: str,
    period: str,
    as_of_date: str,
    excluded_identities: List[str],
    daily_wm: WatermarkStore,
    hourly_wm: WatermarkStore,
) -> Dict[str, int]:
    days = days_of_period_through(period, as_of_date)
    if not days:
        return {name: 0 for name in registry.metronome_names(metric_family)}
    as_of_hour = HourPartition(dt=as_of_date, hour=23)
    daily_completed = {d.key for d in days}
    return compute_mtd(
        store,
        registry,
        metric_family,
        period,
        as_of_hour,
        excluded_identities,
        daily_wm,
        hourly_wm,
        daily_completed=daily_completed,
    )


def hours_needed_for_as_of(
    period: str, as_of_hour: HourPartition
) -> List[HourPartition]:
    return hours_of_period_through(period, as_of_hour)
