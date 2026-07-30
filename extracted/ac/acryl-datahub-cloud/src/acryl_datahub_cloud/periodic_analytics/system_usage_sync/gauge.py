import logging
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Optional, Sequence, Set, Tuple

import polars as pl

from acryl_datahub_cloud.periodic_analytics.constants import Layer
from acryl_datahub_cloud.periodic_analytics.partitions import HourPartition
from acryl_datahub_cloud.periodic_analytics.rollup.hourly import MERGE_KIND_LATEST
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore

logger = logging.getLogger(__name__)

METRIC_ENTITY_COUNT_ACTIVE = "entity_count_active"
METRIC_ENTITY_COUNT_SOFT_DELETED = "entity_count_soft_deleted"
METRIC_DATA_ASSETS_STORED = "data_assets_stored"
METRIC_DATA_ASSETS_STORED_SOFT_DELETED = "data_assets_stored_soft_deleted"

_ENTITY_COUNT_METRICS = (
    METRIC_ENTITY_COUNT_ACTIVE,
    METRIC_ENTITY_COUNT_SOFT_DELETED,
)

__all__ = [
    "DataAssetsStoredSnapshot",
    "METRIC_DATA_ASSETS_STORED",
    "METRIC_DATA_ASSETS_STORED_SOFT_DELETED",
    "METRIC_ENTITY_COUNT_ACTIVE",
    "METRIC_ENTITY_COUNT_SOFT_DELETED",
    "latest_entity_count_samples_from_hourly",
    "resolve_data_assets_stored",
    "resolve_data_assets_stored_snapshot",
    "samples_from_openapi_counts",
    "sum_billable_entity_types",
]


@dataclass(frozen=True)
class DataAssetsStoredSnapshot:
    """Allowlisted inventory quantities from one sealed-hour (or OpenAPI) sample set."""

    stored: int
    soft_deleted: int


def sum_billable_entity_types(
    latest_by_metric_entity: Dict[Tuple[str, str], int],
    billable_entity_types: Sequence[str],
    *,
    metric_names: Sequence[str] = _ENTITY_COUNT_METRICS,
) -> int:
    """Sum selected gauge metrics for allowlisted entity types from LATEST samples.

    Allowlist matching is case-insensitive: registry types are camelCase
    (``dataFlow``, ``mlModel``) while sealed hourly ``dimensions.entity_type``
    from GMS entity-count metrics is typically lowercase.

    Default ``metric_names`` includes active + soft_deleted (billable stored
    footprint). Pass only ``entity_count_soft_deleted`` for the soft-deleted
    companion Metronome metric.
    """
    allowlist: Set[str] = {t.casefold() for t in billable_entity_types}
    allowed_metrics: Set[str] = set(metric_names)
    total = 0
    for (metric_name, entity_type), value in latest_by_metric_entity.items():
        if entity_type.casefold() not in allowlist:
            continue
        if metric_name not in allowed_metrics:
            continue
        total += int(value)
    return total


def latest_entity_count_samples_from_hourly(
    store: ObjectStore,
    metric_family: str,
    hour: HourPartition,
) -> Dict[Tuple[str, str], int]:
    """
    Resolve gauge samples from a sealed hourly_buckets partition.

    Expects ``merge_kind=latest`` rows with ``entity_type`` inside the opaque
    ``dimensions`` JSON (not a flat bucket column). Does not apply actor_class
    billability filters — gauges use SYSTEM actors.
    """
    files = store.list_parquet_files(store.hour_dir(metric_family, Layer.HOURLY, hour))
    if not files:
        return {}

    df = (
        store.scan_bucket_parquet(files)
        .filter(pl.col("metric_name").is_in(list(_ENTITY_COUNT_METRICS)))
        .filter(pl.col("merge_kind") == MERGE_KIND_LATEST)
        .with_columns(
            pl.col("dimensions")
            .str.json_path_match("$.entity_type")
            .fill_null("")
            .alias("entity_type")
        )
        .filter(pl.col("entity_type") != "")
        # Prefer the newest sealed-hour generation when orphan/stale buckets
        # still exist for the same (metric, entity_type).
        .sort("computed_at")
        .group_by(["metric_name", "entity_type"])
        .agg(pl.col("value_sum").last().alias("value_sum"))
        .collect(engine="streaming")
    )
    if df.is_empty():
        return {}

    latest: Dict[Tuple[str, str], int] = {}
    for row in df.iter_rows(named=True):
        latest[(str(row["metric_name"]), str(row["entity_type"]))] = int(
            row["value_sum"]
        )
    return latest


def samples_from_openapi_counts(
    counts: Iterable[Dict],
) -> Dict[Tuple[str, str], int]:
    """Map OpenAPI /entities/counts payload rows into LATEST sample shape."""
    latest: Dict[Tuple[str, str], int] = {}
    for entry in counts:
        entity_type = str(entry.get("entityType") or entry.get("entity_type") or "")
        if not entity_type:
            continue
        active = int(entry.get("activeCount") or entry.get("active_count") or 0)
        soft = int(
            entry.get("softDeletedCount") or entry.get("soft_deleted_count") or 0
        )
        latest[(METRIC_ENTITY_COUNT_ACTIVE, entity_type)] = active
        latest[(METRIC_ENTITY_COUNT_SOFT_DELETED, entity_type)] = soft
    return latest


def resolve_data_assets_stored_snapshot(
    store: ObjectStore,
    metric_family: str,
    as_of_hour: HourPartition,
    billable_entity_types: Sequence[str],
    openapi_counts_fn: Optional[Callable[[], Optional[Iterable[Dict]]]] = None,
) -> Optional[DataAssetsStoredSnapshot]:
    """
    Absolute stored + soft_deleted allowlist sums from sealed hourly latest
    buckets, or None when no samples are available (caller should defer).

    ``openapi_counts_fn`` is invoked lazily only when the sealed hour yields
    no LATEST samples (cold start / empty rollup).
    """
    latest = latest_entity_count_samples_from_hourly(store, metric_family, as_of_hour)
    if not latest and openapi_counts_fn is not None:
        openapi_counts = openapi_counts_fn()
        if openapi_counts is not None:
            latest = samples_from_openapi_counts(openapi_counts)
        if latest:
            logger.info(
                "system_usage: using OpenAPI entity counts fallback (%d types)",
                len({et for _, et in latest}),
            )
    if not latest:
        return None
    return DataAssetsStoredSnapshot(
        stored=sum_billable_entity_types(latest, billable_entity_types),
        soft_deleted=sum_billable_entity_types(
            latest,
            billable_entity_types,
            metric_names=(METRIC_ENTITY_COUNT_SOFT_DELETED,),
        ),
    )


def resolve_data_assets_stored(
    store: ObjectStore,
    metric_family: str,
    as_of_hour: HourPartition,
    billable_entity_types: Sequence[str],
    openapi_counts_fn: Optional[Callable[[], Optional[Iterable[Dict]]]] = None,
) -> Optional[int]:
    """Absolute data_assets_stored (active+soft_deleted) or None when empty."""
    snapshot = resolve_data_assets_stored_snapshot(
        store,
        metric_family,
        as_of_hour,
        billable_entity_types,
        openapi_counts_fn=openapi_counts_fn,
    )
    if snapshot is None:
        return None
    return snapshot.stored
