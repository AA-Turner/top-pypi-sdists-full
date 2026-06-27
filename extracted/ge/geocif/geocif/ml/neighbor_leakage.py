"""Within-year neighbor-yield leakage for the yield-outlook forecast loop.

Idea: yields are spatially autocorrelated, so a neighbor region's yield at
the forecast year carries information about THIS region's yield at the
same year. The standard outlook holds out the whole forecast year from
training. This module optionally injects ``k`` nearest-by-centroid
neighbors' forecast-year rows back into ``df_train`` — letting the model
learn within-year context. Hindcast-only (real-time forecasts have no
known yields to leak).

Cheap per-year design: ONE model per forecast year (or per cluster when
``cluster_strategy`` produces multiple), with the UNION of every test
region's ``k`` nearest neighbors leaked in. Region remains a categorical
feature, so the model learns per-region behaviour from the row labels.
See the docstring of ``inject_leaked_rows`` for the exact algorithm.

Strict per-region (one model per region with only its own k neighbors)
would be more pure but costs ~n_regions× the wall-clock. Not implemented
here; if the cheap version shows a clear lift in sensitivity sweeps,
strict is a v2 candidate.
"""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd


LEAK_COLUMN = "__leaked_from_year__"


def build_centroid_lookup_from_gdf(
    gdf,
    region_col: str = "ADM1_NAME",
) -> dict:
    """Centroid lookup: ``{region_name -> (lat, lon)}``.

    Reads ``gdf.geometry.centroid`` and pairs it with ``gdf[region_col]``.
    Region names that appear multiple times in the gdf (e.g. multi-polygon
    administrative units) use the centroid of the FIRST occurrence — the
    geometry is presumed already-dissolved per region by the caller.

    Returns an empty dict on degenerate input (missing column, no rows).
    """
    if gdf is None or len(gdf) == 0 or region_col not in gdf.columns:
        return {}
    try:
        # Suppress the GeoPandas centroid-projected-CRS warning — for the
        # nearest-neighbor distance we just need a rough lat/lon centroid,
        # not an area-preserving one. The Euclidean distance on lat/lon
        # within one country is a fine proxy.
        import warnings as _w
        with _w.catch_warnings():
            _w.simplefilter("ignore")
            cents = gdf.geometry.centroid
    except Exception:
        return {}
    out: dict = {}
    for name, c in zip(gdf[region_col].astype(str), cents):
        if name in out:
            continue
        try:
            out[name] = (float(c.y), float(c.x))
        except Exception:
            continue
    return out


def find_k_nearest_centroids(
    centroids: dict,
    target_region: str,
    k: int,
) -> list:
    """K nearest regions to ``target_region`` by Euclidean lat/lon distance.

    Excludes the target itself. Clamps to ``min(k, n_other_regions)`` —
    returns fewer than k when the country has fewer than k+1 regions.
    Returns an empty list when the target isn't in the lookup.
    """
    if k <= 0 or target_region not in centroids:
        return []
    target_lat, target_lon = centroids[target_region]
    candidates = []
    for r, (lat, lon) in centroids.items():
        if r == target_region:
            continue
        d2 = (lat - target_lat) ** 2 + (lon - target_lon) ** 2
        candidates.append((d2, r))
    candidates.sort()
    return [r for _, r in candidates[:k]]


def inject_leaked_rows(
    df_train: pd.DataFrame,
    df_full: pd.DataFrame,
    test_regions: list,
    target_year: int,
    centroids: dict,
    k: int,
    target_col: str,
    region_col: str = "Region",
    year_col: str = "Harvest Year",
    logger: Optional[logging.Logger] = None,
) -> pd.DataFrame:
    """Append leaked neighbor rows to ``df_train``.

    Algorithm (cheap per-year):
      1. For each region in ``test_regions``, find its k nearest centroid
         neighbors (excluding itself).
      2. UNION the neighbors across all test regions → ``leak_set``.
      3. Pull rows from ``df_full`` where
         ``region_col ∈ leak_set AND year_col == target_year AND
         target_col is not NaN``.
      4. Tag the leaked rows with ``__leaked_from_year__ = target_year``.
      5. Concatenate to ``df_train`` and return.

    No-ops (returns ``df_train`` unchanged) when:
      * ``k <= 0``
      * No leak candidates have finite yield at ``target_year`` (real-time
        forecast mode — neighbors are also forecast regions with NaN
        yield).

    Logs a warning when k is clamped per region (target country has fewer
    than k+1 regions).
    """
    if k <= 0:
        return df_train
    if not centroids:
        if logger is not None:
            logger.warning(
                "  neighbor_leakage: empty centroid lookup; skipping injection."
            )
        return df_train

    leak_set = set()
    n_clamped = 0
    for r in test_regions:
        nn = find_k_nearest_centroids(centroids, str(r), k)
        if len(nn) < k:
            n_clamped += 1
        leak_set.update(nn)

    if not leak_set:
        if logger is not None:
            logger.warning(
                "  neighbor_leakage: no neighbors found for any test region "
                "(check centroid lookup vs test_regions match); skipping."
            )
        return df_train

    if n_clamped and logger is not None:
        logger.info(
            f"  neighbor_leakage: k={k} clamped for {n_clamped} test region(s) "
            f"(country has < k+1 regions in the centroid lookup)"
        )

    mask = (
        df_full[region_col].astype(str).isin(leak_set)
        & (df_full[year_col] == target_year)
        & df_full[target_col].notna()
    )
    df_leak = df_full[mask].copy()
    if df_leak.empty:
        if logger is not None:
            logger.warning(
                f"  neighbor_leakage: 0 finite-yield rows at year={target_year} "
                f"for the {len(leak_set)} neighbor regions — likely a real-time "
                f"forecast year with no known yields. Skipping injection."
            )
        return df_train

    df_leak[LEAK_COLUMN] = int(target_year)
    if LEAK_COLUMN not in df_train.columns:
        df_train = df_train.assign(**{LEAK_COLUMN: pd.NA})

    if logger is not None:
        logger.info(
            f"  neighbor_leakage: injected {len(df_leak)} leaked rows from "
            f"{len(leak_set)} neighbors at year={target_year} (k={k}, "
            f"|test_regions|={len(test_regions)})"
        )
    return pd.concat([df_train, df_leak], ignore_index=True)
