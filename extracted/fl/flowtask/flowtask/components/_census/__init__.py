"""
Private helper package for the CensusData and CensusVariables components.

This package is intentionally prefixed with an underscore so that
``loadComponent()`` does not attempt to treat it as a component class.

Sub-modules:
    resolver  -- Dataset path resolution, URL building, CensusQuery / CacheKey.
    transform -- Sentinel mapping, label normalization, suffix filtering.
    cache     -- Parquet read/write helpers.
    fetch     -- Async HTTP fetch (with retry) and state fan-out.
"""

from flowtask.components._census.cache import (
    cache_path,
    cache_read,
    cache_write,
    default_cache_dir,
)
from flowtask.components._census.fetch import (
    STATE_CODES,
    fan_out,
    fetch_json,
)
from flowtask.components._census.resolver import (
    CacheKey,
    CensusQuery,
    GeographyType,
    build_data_url,
    build_variables_url,
    resolve_dataset,
    scrub_url,
)
from flowtask.components._census.transform import (
    SENTINEL_VALUES,
    _build_variables_df,
    apply_sentinels,
    filter_by_suffix,
    normalize_label,
    rename_geography_column,
)

__all__ = [
    # resolver
    "GeographyType",
    "CensusQuery",
    "CacheKey",
    "resolve_dataset",
    "build_data_url",
    "build_variables_url",
    "scrub_url",
    # transform
    "SENTINEL_VALUES",
    "_build_variables_df",
    "apply_sentinels",
    "normalize_label",
    "filter_by_suffix",
    "rename_geography_column",
    # cache
    "default_cache_dir",
    "cache_path",
    "cache_read",
    "cache_write",
    # fetch
    "fetch_json",
    "fan_out",
    "STATE_CODES",
]
