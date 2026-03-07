"""Spatial neighbor feature engineering for GraphSAGE-style message passing.

Computes yield-correlation-weighted averages of neighboring regions' features
and appends them as nbr_* columns. Works with all existing model types.
"""

import math
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance between two points in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def build_neighbor_graph(
    df: pd.DataFrame,
    admin_col: str = "Region",
    lat_col: str = "lat",
    lon_col: str = "lon",
    yield_col: str = "Yield (tn per ha)",
    method: str = "knn",
    k: int = 5,
) -> Dict[str, List[Tuple[str, float]]]:
    """Build adjacency graph with yield-correlation edge weights.

    Args:
        df: Training DataFrame (wide format, one row per region-year).
        admin_col: Column identifying admin regions.
        lat_col, lon_col: Coordinate columns.
        yield_col: Yield column for computing correlations.
            Use detrended yield if available.
        method: 'knn' (k-nearest by distance) or 'full' (all-to-all).
        k: Number of neighbors for knn method.

    Returns:
        {region: [(neighbor, weight), ...]} with normalized weights.
    """
    # Region centroids
    centroids = (
        df.dropna(subset=[lat_col, lon_col])
        .groupby(admin_col)[[lat_col, lon_col]]
        .mean()
    )
    regions = centroids.index.tolist()
    n = len(regions)

    if n < 2:
        return {r: [] for r in regions}

    # Pairwise distances
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine_km(
                centroids.iloc[i][lat_col],
                centroids.iloc[i][lon_col],
                centroids.iloc[j][lat_col],
                centroids.iloc[j][lon_col],
            )
            dist[i, j] = d
            dist[j, i] = d

    # Build adjacency
    adjacency: Dict[int, List[int]] = {}
    for i in range(n):
        if method == "knn":
            # k nearest (exclude self)
            dists_i = dist[i].copy()
            dists_i[i] = np.inf
            kk = min(k, n - 1)
            neighbors = np.argsort(dists_i)[:kk].tolist()
        else:  # full
            neighbors = [j for j in range(n) if j != i]
        adjacency[i] = neighbors

    # Yield time series per region for correlation
    yield_pivot = df.pivot_table(
        index="Harvest Year", columns=admin_col, values=yield_col, aggfunc="mean"
    )

    # Compute edge weights (Pearson correlation, clamped ≥ 0)
    graph: Dict[str, List[Tuple[str, float]]] = {}
    for i, region_i in enumerate(regions):
        edges = []
        for j in adjacency[i]:
            region_j = regions[j]
            yi = yield_pivot.get(region_i)
            yj = yield_pivot.get(region_j)
            if yi is None or yj is None:
                edges.append((region_j, 0.0))
                continue

            mask = yi.notna() & yj.notna()
            common = mask.sum()
            if common < 3:
                edges.append((region_j, 0.0))
                continue

            corr = yi[mask].corr(yj[mask])
            weight = max(0.0, corr) if not np.isnan(corr) else 0.0
            edges.append((region_j, weight))

        # Normalize weights to sum to 1
        total_w = sum(w for _, w in edges)
        if total_w > 0:
            edges = [(nbr, w / total_w) for nbr, w in edges]

        graph[region_i] = edges

    return graph


def add_neighbor_features(
    df: pd.DataFrame,
    neighbor_graph: Dict[str, List[Tuple[str, float]]],
    feature_cols: List[str],
    admin_col: str = "Region",
    year_col: str = "Harvest Year",
    yield_col: str = "Yield (tn per ha)",
    prefix: str = "nbr_",
) -> pd.DataFrame:
    """Add neighbor-aggregated features to the DataFrame.

    For each (region, year), computes weighted mean of neighbors' features
    using the yield-correlation edge weights from the neighbor graph.

    Args:
        df: DataFrame to augment (train or test).
        neighbor_graph: Output of build_neighbor_graph.
        feature_cols: Columns to aggregate across neighbors.
        admin_col: Region column name.
        year_col: Year column name.
        yield_col: Yield column for computing nbr_mean_yield_hist.
        prefix: Prefix for new columns.

    Returns:
        DataFrame with nbr_* columns appended.
    """
    df = df.copy()

    nbr_cols = [f"{prefix}{c}" for c in feature_cols]
    for col in nbr_cols:
        df[col] = np.nan

    df[f"{prefix}mean_yield_hist"] = np.nan
    df[f"{prefix}yield_corr_mean"] = np.nan
    df["n_neighbors"] = 0

    # Pre-index: {(region, year): row_indices}
    grouped_idx = df.groupby([admin_col, year_col]).indices

    # Pre-compute per-region yield medians for nbr_mean_yield_hist
    yield_medians = df.groupby(admin_col)[yield_col].median()

    for (region, year), indices in grouped_idx.items():
        edges = neighbor_graph.get(region, [])
        active_edges = [(nbr, w) for nbr, w in edges if w > 0]
        n_nbrs = len(active_edges)
        df.loc[df.index[indices], "n_neighbors"] = n_nbrs

        # Mean edge weight for this region
        if edges:
            mean_corr = np.mean([w for _, w in edges])
        else:
            mean_corr = 0.0
        df.loc[df.index[indices], f"{prefix}yield_corr_mean"] = mean_corr

        if not active_edges:
            # Self-loop fallback: use own feature values
            for fi, fc in enumerate(feature_cols):
                df.loc[df.index[indices], nbr_cols[fi]] = df.loc[
                    df.index[indices], fc
                ].values

            # Own median yield
            own_med = yield_medians.get(region, np.nan)
            df.loc[df.index[indices], f"{prefix}mean_yield_hist"] = own_med
            continue

        # Collect neighbor feature values for this year
        nbr_values = []
        nbr_weights = []
        nbr_yield_meds = []

        for nbr, w in active_edges:
            nbr_idx = grouped_idx.get((nbr, year))
            if nbr_idx is None or len(nbr_idx) == 0:
                continue
            nbr_row = df.iloc[nbr_idx[0]]
            nbr_values.append(nbr_row[feature_cols].values.astype(float))
            nbr_weights.append(w)
            nbr_yield_meds.append(yield_medians.get(nbr, np.nan))

        if not nbr_values:
            # No neighbors found for this year — self-loop
            for fi, fc in enumerate(feature_cols):
                df.loc[df.index[indices], nbr_cols[fi]] = df.loc[
                    df.index[indices], fc
                ].values
            own_med = yield_medians.get(region, np.nan)
            df.loc[df.index[indices], f"{prefix}mean_yield_hist"] = own_med
            continue

        vals = np.array(nbr_values)  # (n_neighbors, n_features)
        weights = np.array(nbr_weights)  # (n_neighbors,)

        # Weighted mean per feature, skipping NaN
        for fi in range(len(feature_cols)):
            col_vals = vals[:, fi]
            valid = ~np.isnan(col_vals)
            if valid.any():
                w_valid = weights[valid]
                w_sum = w_valid.sum()
                if w_sum > 0:
                    wmean = np.average(col_vals[valid], weights=w_valid)
                else:
                    wmean = np.nanmean(col_vals)
                df.loc[df.index[indices], nbr_cols[fi]] = wmean
            else:
                # All neighbors NaN — use own value
                df.loc[df.index[indices], nbr_cols[fi]] = df.loc[
                    df.index[indices], feature_cols[fi]
                ].values

        # Weighted mean of neighbors' historical median yield
        med_arr = np.array(nbr_yield_meds)
        valid_med = ~np.isnan(med_arr)
        if valid_med.any():
            w_valid = weights[valid_med]
            w_sum = w_valid.sum()
            if w_sum > 0:
                nbr_med = np.average(med_arr[valid_med], weights=w_valid)
            else:
                nbr_med = np.nanmean(med_arr)
        else:
            nbr_med = yield_medians.get(region, np.nan)
        df.loc[df.index[indices], f"{prefix}mean_yield_hist"] = nbr_med

    return df
