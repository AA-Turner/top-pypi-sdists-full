"""Spatial neighbor feature engineering for GraphSAGE-style message passing.

Computes yield-correlation-weighted averages of neighboring regions' features
and appends them as nbr_* columns. Works with all existing model types.
"""

import math
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from tqdm.rich import tqdm


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


_N_FALLBACK_YEARS = 5


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

    When a neighbor has no data for the target year (e.g. forecast year),
    falls back to the average of the neighbor's last 5 available years.

    Uses vectorized numpy operations for speed — results are accumulated
    in pre-allocated arrays and assigned to the DataFrame in bulk.

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
    n_rows = len(df)
    n_feat = len(feature_cols)

    # Pre-allocate numpy output arrays (avoid per-group .loc writes)
    out_features = np.full((n_rows, n_feat), np.nan)
    out_yield_hist = np.full(n_rows, np.nan)
    out_corr_mean = np.zeros(n_rows)
    out_n_neighbors = np.zeros(n_rows, dtype=int)

    # Pre-build feature matrix for O(1) row lookups
    feat_matrix = df[feature_cols].values.astype(float)

    # Pre-index: {(region, year): row_indices} and first-row lookup
    grouped_idx = df.groupby([admin_col, year_col]).indices
    first_row = {}
    for (r, y), idx in grouped_idx.items():
        first_row[(r, y)] = idx[0]

    # Pre-compute per-region yield medians
    yield_medians = df.groupby(admin_col)[yield_col].median().to_dict()

    # Pre-compute last-N-year feature averages per region (numpy arrays)
    region_avg = {}
    for region in neighbor_graph:
        region_rows = df[df[admin_col] == region].sort_values(year_col, ascending=False)
        recent = region_rows.drop_duplicates(subset=[year_col]).head(_N_FALLBACK_YEARS)
        if not recent.empty:
            region_avg[region] = recent[feature_cols].values.astype(float).mean(axis=0)

    # Pre-compute per-region mean correlation and active edges
    region_meta = {}
    for region, edges in neighbor_graph.items():
        active = [(nbr, w) for nbr, w in edges if w > 0]
        mean_corr = np.mean([w for _, w in edges]) if edges else 0.0
        region_meta[region] = (active, mean_corr)

    for (region, year), indices in tqdm(grouped_idx.items(), desc="Neighbor features", leave=False):
        meta = region_meta.get(region)
        if meta is None:
            out_yield_hist[indices] = yield_medians.get(region, np.nan)
            continue

        active_edges, mean_corr = meta
        out_n_neighbors[indices] = len(active_edges)
        out_corr_mean[indices] = mean_corr

        if not active_edges:
            out_yield_hist[indices] = yield_medians.get(region, np.nan)
            continue

        # Collect neighbor feature vectors
        nbr_vals_list = []
        nbr_w_list = []
        nbr_med_list = []

        for nbr, w in active_edges:
            fr = first_row.get((nbr, year))
            if fr is not None:
                nbr_vals_list.append(feat_matrix[fr])
            else:
                avg = region_avg.get(nbr)
                if avg is None:
                    continue
                nbr_vals_list.append(avg)
            nbr_w_list.append(w)
            nbr_med_list.append(yield_medians.get(nbr, np.nan))

        if not nbr_vals_list:
            out_yield_hist[indices] = yield_medians.get(region, np.nan)
            continue

        vals = np.array(nbr_vals_list)    # (k, n_feat)
        weights = np.array(nbr_w_list)    # (k,)

        # Vectorized weighted mean per feature, handling NaN
        valid_mask = ~np.isnan(vals)       # (k, n_feat)
        # Broadcast weights to (k, n_feat) and zero out NaN positions
        w_broad = np.where(valid_mask, weights[:, None], 0.0)
        w_sums = w_broad.sum(axis=0)       # (n_feat,)

        # Weighted mean where weights exist, else NaN
        has_valid = w_sums > 0
        wmean = np.where(
            has_valid,
            np.where(valid_mask, vals * weights[:, None], 0.0).sum(axis=0) / np.where(has_valid, w_sums, 1.0),
            np.nan,
        )
        out_features[indices] = wmean

        # Weighted mean of neighbor median yields
        med_arr = np.array(nbr_med_list)
        valid_med = ~np.isnan(med_arr)
        if valid_med.any():
            w_valid = weights[valid_med]
            w_sum = w_valid.sum()
            nbr_med = np.average(med_arr[valid_med], weights=w_valid) if w_sum > 0 else np.nanmean(med_arr)
        else:
            nbr_med = yield_medians.get(region, np.nan)
        out_yield_hist[indices] = nbr_med

    # Bulk assignment via pd.concat to avoid DataFrame fragmentation
    nbr_cols = [f"{prefix}{c}" for c in feature_cols]
    new_data = pd.DataFrame(out_features, columns=nbr_cols, index=df.index)
    new_data[f"{prefix}mean_yield_hist"] = out_yield_hist
    new_data[f"{prefix}yield_corr_mean"] = out_corr_mean
    new_data["n_neighbors"] = out_n_neighbors
    df = pd.concat([df, new_data], axis=1)

    return df
