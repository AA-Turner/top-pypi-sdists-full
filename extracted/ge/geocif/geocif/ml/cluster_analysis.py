"""
Cluster analysis of regions by CID profiles.

Identifies region groups with similar climatic impact driver patterns
and determines which CIDs are most associated with high or low target
values (yield or proxy) within each cluster.

Pipeline:
    1. Resolve target (yield vs proxy CID)
    2. Summarize region CID profiles (per-region mean across years)
    3. PCA for dimensionality reduction (handles CID collinearity)
    4. Ward's hierarchical clustering with silhouette-based k selection
    5. Kruskal-Wallis + Cohen's d for CID discrimination per cluster
    6. Mutual information for CID-target association per cluster
    7. Visualizations: maps, dendrogram, biplot, heatmap, boxplot
"""

import os
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, fcluster, ward
from scipy.stats import kruskal
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_regression
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from geocif import utils
from geocif.ml.feature_engineering import find_optimal_kmeans

DEFAULT_TARGET = "Yield (tn per ha)"
DEFAULT_PROXY = "AUC_NDVI"
FIXED_COLUMNS = ["Country", "Region", "Crop", "Area", "Season", "Harvest Year"]
STAT_COLUMNS = ["Area (ha)", "Production (tn)"]


# ---------------------------------------------------------------------------
# 1. Target resolution
# ---------------------------------------------------------------------------

def resolve_target(df, target_col=DEFAULT_TARGET, proxy_prefix=DEFAULT_PROXY):
    """Decide whether to use yield or a proxy CID as the analysis target.

    If ``target_col`` is present and has non-null values, use it directly.
    Otherwise, average all columns matching ``{proxy_prefix}_*`` into a
    synthetic ``_proxy_target`` column (added in place).

    Returns:
        (effective_target_col, yield_available)
    """
    if target_col in df.columns and df[target_col].notna().any():
        return target_col, True

    proxy_cols = [c for c in df.columns if c.startswith(f"{proxy_prefix}_")]
    if not proxy_cols:
        available = [c for c in df.columns if c not in FIXED_COLUMNS]
        raise ValueError(
            f"No yield data in '{target_col}' and no proxy columns "
            f"matching '{proxy_prefix}_*'. Available: {available[:20]}"
        )

    df["_proxy_target"] = df[proxy_cols].mean(axis=1)
    return "_proxy_target", False


# ---------------------------------------------------------------------------
# 2. CID column detection
# ---------------------------------------------------------------------------

def detect_cid_columns(df, target_col=DEFAULT_TARGET):
    """Identify CID feature columns in a wide-format ML DataFrame.

    Delegates to ``utils.filter_cid_columns`` with standard fixed/stat columns.
    """
    return utils.filter_cid_columns(df, FIXED_COLUMNS, target_col, STAT_COLUMNS)


# ---------------------------------------------------------------------------
# 3. Region profile summarization
# ---------------------------------------------------------------------------

def summarize_region_cid_profiles(df, cid_columns, target_col=DEFAULT_TARGET):
    """Compute per-region mean of each CID and target across harvest years.

    Returns:
        DataFrame indexed by Region with one column per CID (mean value)
        plus ``target_mean``.
    """
    agg_cols = [c for c in cid_columns if c in df.columns]
    cols_to_agg = agg_cols + ([target_col] if target_col in df.columns else [])

    grouped = df.groupby("Region")[cols_to_agg].mean()

    if target_col in grouped.columns:
        grouped = grouped.rename(columns={target_col: "target_mean"})

    # Drop columns that are all NaN
    n_before = len(grouped.columns)
    grouped = grouped.dropna(axis=1, how="all")
    n_dropped = n_before - len(grouped.columns)
    if n_dropped > 0:
        warnings.warn(f"Dropped {n_dropped} all-NaN CID columns from profiles")

    return grouped


# ---------------------------------------------------------------------------
# 4. PCA dimensionality reduction
# ---------------------------------------------------------------------------

def run_pca(df_profiles, variance_threshold=0.85):
    """Z-score standardize and apply PCA, retaining components for the
    given cumulative variance threshold.

    Args:
        df_profiles: Region x CID DataFrame (output of summarize_region_cid_profiles).
        variance_threshold: Cumulative explained variance to retain.

    Returns:
        (scores, loadings, n_components, pca_object):
            - scores: DataFrame (Region x PC) of transformed values
            - loadings: DataFrame (CID x PC) of component loadings
            - n_components: Number of retained components
            - pca_object: Fitted PCA instance
    """
    # Drop target_mean before PCA — it's not a CID feature
    feature_cols = [c for c in df_profiles.columns if c != "target_mean"]
    X = df_profiles[feature_cols].fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Full PCA first, then determine n_components
    pca_full = PCA().fit(X_scaled)
    cumvar = np.cumsum(pca_full.explained_variance_ratio_)
    n_components = int(np.searchsorted(cumvar, variance_threshold) + 1)
    n_components = min(n_components, len(feature_cols), len(df_profiles))

    pca = PCA(n_components=n_components)
    scores_arr = pca.fit_transform(X_scaled)

    pc_names = [f"PC{i+1}" for i in range(n_components)]
    scores = pd.DataFrame(scores_arr, index=df_profiles.index, columns=pc_names)
    loadings = pd.DataFrame(
        pca.components_.T, index=feature_cols, columns=pc_names
    )

    return scores, loadings, n_components, pca


# ---------------------------------------------------------------------------
# 5. Ward's hierarchical clustering
# ---------------------------------------------------------------------------

def cluster_regions_ward(scores, max_k=8):
    """Cluster regions using Ward's hierarchical clustering on PCA scores.

    Optimal k is selected by silhouette analysis.

    Returns:
        (labels_df, optimal_k, linkage_matrix):
            - labels_df: DataFrame with columns ["Region", "Cluster"]
            - optimal_k: Chosen number of clusters
            - linkage_matrix: Linkage matrix for dendrogram
    """
    X = scores.values
    n_regions = len(scores)

    if n_regions < 3:
        warnings.warn(f"Only {n_regions} regions — skipping clustering, assigning all to cluster 0")
        return (
            pd.DataFrame({"Region": scores.index, "Cluster": 0}),
            1,
            None,
        )

    linkage_matrix = ward(X)

    # Silhouette analysis for optimal k
    k_range = range(2, min(max_k + 1, n_regions))
    best_k, best_score = 2, -1

    for k in k_range:
        labels = fcluster(linkage_matrix, t=k, criterion="maxclust")
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(X, labels)
        if score > best_score:
            best_k, best_score = k, score

    labels = fcluster(linkage_matrix, t=best_k, criterion="maxclust")
    # Shift to 0-indexed
    labels = labels - 1

    labels_df = pd.DataFrame({"Region": scores.index, "Cluster": labels})
    return labels_df, best_k, linkage_matrix


# ---------------------------------------------------------------------------
# 6. CID discrimination per cluster (Kruskal-Wallis + Cohen's d)
# ---------------------------------------------------------------------------

def _cohens_d(group, grand):
    """Cohen's d between a group mean and the grand mean."""
    pooled_std = grand.std()
    if pooled_std == 0:
        return 0.0
    return (group.mean() - grand.mean()) / pooled_std


def _benjamini_hochberg(pvalues):
    """Benjamini-Hochberg FDR correction."""
    n = len(pvalues)
    if n == 0:
        return np.array([])
    sorted_idx = np.argsort(pvalues)
    sorted_pv = np.array(pvalues)[sorted_idx]
    adjusted = np.empty(n)
    adjusted[sorted_idx[-1]] = sorted_pv[-1]
    for i in range(n - 2, -1, -1):
        adjusted[sorted_idx[i]] = min(
            adjusted[sorted_idx[i + 1]],
            sorted_pv[i] * n / (i + 1),
        )
    return np.clip(adjusted, 0, 1)


def compute_cid_discrimination(df_profiles, cluster_labels, cid_columns):
    """For each CID, test whether it differs across clusters and compute
    effect sizes.

    Uses Kruskal-Wallis (non-parametric) with Benjamini-Hochberg correction.
    Cohen's d measures effect size per cluster vs grand mean.

    Returns:
        DataFrame with columns: CID, Cluster, kw_pvalue, adj_pvalue, cohens_d.
    """
    df = df_profiles.copy()
    cid_cols = [c for c in cid_columns if c in df.columns]

    # Merge cluster labels
    if "Cluster" not in df.columns:
        cl = cluster_labels.set_index("Region")["Cluster"]
        df = df.join(cl)

    clusters = sorted(df["Cluster"].unique())
    if len(clusters) < 2:
        return pd.DataFrame(columns=["CID", "Cluster", "kw_pvalue", "adj_pvalue", "cohens_d"])

    # Kruskal-Wallis per CID
    kw_results = {}
    for cid in cid_cols:
        groups = [df.loc[df["Cluster"] == c, cid].dropna().values for c in clusters]
        groups = [g for g in groups if len(g) > 0]
        if len(groups) < 2:
            kw_results[cid] = np.nan
            continue
        try:
            _, pval = kruskal(*groups)
            kw_results[cid] = pval
        except ValueError:
            kw_results[cid] = np.nan

    # BH correction
    cid_names = list(kw_results.keys())
    raw_pvals = [kw_results[c] for c in cid_names]
    # Replace NaN with 1.0 for correction
    raw_pvals_clean = [p if not np.isnan(p) else 1.0 for p in raw_pvals]
    adj_pvals = _benjamini_hochberg(raw_pvals_clean)

    # Cohen's d per cluster
    rows = []
    for i, cid in enumerate(cid_names):
        grand = df[cid].dropna()
        for cluster in clusters:
            group = df.loc[df["Cluster"] == cluster, cid].dropna()
            d = _cohens_d(group, grand)
            rows.append({
                "CID": cid,
                "Cluster": cluster,
                "kw_pvalue": raw_pvals[i],
                "adj_pvalue": adj_pvals[i],
                "cohens_d": d,
            })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 7. CID-target association via mutual information
# ---------------------------------------------------------------------------

def compute_cid_target_association(df, cluster_labels, target_col, cid_columns):
    """Compute mutual information between each CID and the target, per cluster.

    Returns:
        DataFrame with columns: CID, Cluster, mutual_info.
    """
    df_merged = df.merge(cluster_labels, on="Region", how="left")
    cid_cols = [c for c in cid_columns if c in df_merged.columns]
    clusters = sorted(df_merged["Cluster"].unique())

    rows = []
    for cluster in clusters:
        mask = df_merged["Cluster"] == cluster
        df_c = df_merged.loc[mask].dropna(subset=[target_col])

        if len(df_c) < 5:
            for cid in cid_cols:
                rows.append({"CID": cid, "Cluster": cluster, "mutual_info": np.nan})
            continue

        X = df_c[cid_cols].fillna(0).values
        y = df_c[target_col].values

        try:
            mi = mutual_info_regression(X, y, random_state=42)
        except ValueError:
            mi = np.full(len(cid_cols), np.nan)

        for j, cid in enumerate(cid_cols):
            rows.append({"CID": cid, "Cluster": cluster, "mutual_info": mi[j]})

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 8. Visualizations
# ---------------------------------------------------------------------------

def plot_dendrogram(linkage_matrix, regions, labels, dir_output):
    """Dendrogram with branches colored by cluster."""
    if linkage_matrix is None:
        return None

    fig, ax = plt.subplots(figsize=(max(8, len(regions) * 0.5), 6))
    dendrogram(
        linkage_matrix,
        labels=list(regions),
        leaf_rotation=90,
        color_threshold=linkage_matrix[-(len(set(labels)) - 1), 2] if len(set(labels)) > 1 else 0,
        ax=ax,
    )
    ax.set_title("Hierarchical Clustering Dendrogram (Ward's Method)")
    ax.set_ylabel("Distance")
    plt.tight_layout()

    path = Path(dir_output) / "dendrogram.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_pca_biplot(scores, loadings, labels_df, dir_output, top_n_arrows=10):
    """PCA biplot: regions as points colored by cluster, CID loadings as arrows."""
    if scores.shape[1] < 2:
        return None

    fig, ax = plt.subplots(figsize=(10, 8))

    # Merge cluster labels
    merged = scores.join(labels_df.set_index("Region")["Cluster"])
    clusters = sorted(merged["Cluster"].unique())
    cmap = plt.cm.get_cmap("tab10", max(len(clusters), 1))

    for c in clusters:
        subset = merged[merged["Cluster"] == c]
        ax.scatter(subset["PC1"], subset["PC2"], c=[cmap(c)], label=f"Cluster {c}",
                   s=80, edgecolors="k", linewidth=0.5, zorder=3)
        for region, row in subset.iterrows():
            ax.annotate(region, (row["PC1"], row["PC2"]), fontsize=7,
                        ha="center", va="bottom", alpha=0.7)

    # Top loading arrows
    loading_mag = (loadings["PC1"] ** 2 + loadings["PC2"] ** 2) ** 0.5
    top_cids = loading_mag.nlargest(top_n_arrows).index
    scale = max(scores["PC1"].abs().max(), scores["PC2"].abs().max()) / loadings.loc[top_cids].abs().max().max()

    for cid in top_cids:
        ax.annotate(
            "", xy=(loadings.loc[cid, "PC1"] * scale * 0.8,
                     loadings.loc[cid, "PC2"] * scale * 0.8),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="red", lw=1.2, alpha=0.6),
        )
        ax.text(loadings.loc[cid, "PC1"] * scale * 0.85,
                loadings.loc[cid, "PC2"] * scale * 0.85,
                cid, fontsize=6, color="red", alpha=0.8)

    ax.set_xlabel(f"PC1")
    ax.set_ylabel(f"PC2")
    ax.set_title("PCA Biplot — Regions by CID Profile Cluster")
    ax.legend(loc="best", fontsize=8)
    ax.axhline(0, ls="--", lw=0.5, c="grey")
    ax.axvline(0, ls="--", lw=0.5, c="grey")
    plt.tight_layout()

    path = Path(dir_output) / "pca_biplot.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_discrimination_heatmap(df_discrimination, dir_output, top_n=20):
    """Heatmap of Cohen's d (cluster x CID) with significance stars."""
    if df_discrimination.empty:
        return None

    # Select top CIDs by mean absolute Cohen's d
    mean_d = df_discrimination.groupby("CID")["cohens_d"].apply(lambda x: x.abs().mean())
    top_cids = mean_d.nlargest(top_n).index.tolist()

    df_top = df_discrimination[df_discrimination["CID"].isin(top_cids)]
    pivot = df_top.pivot_table(index="Cluster", columns="CID", values="cohens_d")
    pvals = df_top.pivot_table(index="Cluster", columns="CID", values="adj_pvalue")

    # Build annotation matrix with significance stars
    annot = pivot.copy().astype(str)
    for col in pivot.columns:
        for idx in pivot.index:
            d_val = pivot.loc[idx, col]
            p_val = pvals.loc[idx, col] if col in pvals.columns and idx in pvals.index else 1.0
            stars = "**" if p_val < 0.01 else ("*" if p_val < 0.05 else "")
            annot.loc[idx, col] = f"{d_val:.2f}{stars}"

    fig, ax = plt.subplots(figsize=(max(10, len(top_cids) * 0.6), max(4, len(pivot) * 1.2)))
    sns.heatmap(
        pivot, annot=annot, fmt="", cmap="RdBu_r", center=0,
        linewidths=0.5, ax=ax, cbar_kws={"label": "Cohen's d"},
    )
    ax.set_title("CID Discrimination by Cluster\n(* p<0.05, ** p<0.01, Kruskal-Wallis + BH)")
    ax.set_ylabel("Cluster")
    ax.set_xlabel("")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()

    path = Path(dir_output) / "discrimination_heatmap.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_target_by_cluster(df, cluster_labels, target_col, dir_output):
    """Boxplot of target distribution per cluster."""
    df_merged = df.merge(cluster_labels, on="Region", how="left")

    if target_col not in df_merged.columns:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df_merged, x="Cluster", y=target_col, ax=ax, palette="Set2")
    ax.set_title(f"{target_col} Distribution by Cluster")
    plt.tight_layout()

    path = Path(dir_output) / "target_by_cluster.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_cluster_map(gdf, cluster_labels, dir_output, countries=None):
    """Choropleth map of regions colored by cluster assignment."""
    from geocif.viz import plot as vizplot

    df_map = cluster_labels.copy()
    # Build "Country Region" merge key (lowercase) matching viz.plot.plot_map convention
    if "Country" in df_map.columns:
        df_map["Country Region"] = (
            df_map["Country"].str.strip() + " " + df_map["Region"].str.strip()
        ).str.lower()
    else:
        df_map["Country Region"] = df_map["Region"].str.lower()

    n_clusters = df_map["Cluster"].nunique()
    dict_lup = {i: f"Cluster {i}" for i in sorted(df_map["Cluster"].unique())}

    vizplot.plot_map(
        gdf,
        df_map,
        merge_col="Country Region",
        name_country=countries,
        name_col="Cluster",
        dir_out=str(dir_output),
        fname="cluster_map.png",
        title="Region Clusters by CID Profile",
        label="Cluster",
        dict_lup=dict_lup,
        series="qualitative",
        annotate_regions=True,
    )
    return Path(dir_output) / "cluster_map.png"


def plot_cid_maps(gdf, df_profiles, df_discrimination, dir_output, countries=None, top_n=3):
    """Choropleth maps for the top discriminating CIDs across all clusters."""
    from geocif.viz import plot as vizplot

    if df_discrimination.empty:
        return []

    # Select top CIDs globally by mean absolute Cohen's d
    mean_d = df_discrimination.groupby("CID")["cohens_d"].apply(lambda x: x.abs().mean())
    top_cids = mean_d.nlargest(top_n).index.tolist()

    paths = []
    for cid in top_cids:
        if cid not in df_profiles.columns:
            continue

        df_map = df_profiles[[cid]].reset_index()
        df_map.columns = ["Region", cid]
        df_map["Country Region"] = df_map["Region"].str.lower()

        vizplot.plot_map(
            gdf,
            df_map,
            merge_col="Country Region",
            name_country=countries,
            name_col=cid,
            dir_out=str(dir_output),
            fname=f"cid_map_{cid}.png",
            title=f"Mean {cid} by Region",
            label=cid,
            series="sequential",
            annotate_regions=True,
        )
        paths.append(Path(dir_output) / f"cid_map_{cid}.png")

    return paths


# ---------------------------------------------------------------------------
# 9. Main entry point
# ---------------------------------------------------------------------------

def run_cluster_analysis(
    df,
    dir_output,
    target_col=DEFAULT_TARGET,
    proxy_prefix=DEFAULT_PROXY,
    cid_columns=None,
    gdf=None,
    countries=None,
    max_clusters=8,
    top_n_cids=20,
    variance_threshold=0.85,
    logger=None,
):
    """Run the full cluster analysis pipeline.

    Args:
        df: Wide-format ML DataFrame from ``create_ml_dataframe()``.
        dir_output: Base output directory. Results saved under ``clusters/``.
        target_col: Preferred target column (e.g. "Yield (tn per ha)").
        proxy_prefix: Proxy CID prefix when yield is unavailable (e.g. "AUC_NDVI").
        cid_columns: Explicit CID column list. Auto-detected if None.
        gdf: GeoDataFrame with region geometries for map plots. Optional.
        countries: List of country names for maps. Optional.
        max_clusters: Maximum clusters for silhouette selection.
        top_n_cids: Number of top CIDs in discrimination heatmap.
        variance_threshold: Cumulative variance for PCA component retention.
        logger: Logger instance. Optional.

    Returns:
        Dict with keys: effective_target, yield_available, cluster_labels,
        optimal_k, discrimination, association, profiles, loadings, paths.
    """
    _log = logger.info if logger else print

    dir_out = Path(dir_output) / "clusters"
    os.makedirs(dir_out, exist_ok=True)

    # 1. Resolve target
    effective_target, yield_available = resolve_target(df, target_col, proxy_prefix)
    scenario = "yield" if yield_available else f"proxy ({proxy_prefix})"
    _log(f"Cluster analysis — target: {effective_target} (scenario: {scenario})")

    # 2. Detect CID columns
    if cid_columns is None:
        cid_columns = detect_cid_columns(df, effective_target)
    _log(f"  {len(cid_columns)} CID features detected")

    # 3. Summarize region profiles
    df_profiles = summarize_region_cid_profiles(df, cid_columns, effective_target)
    _log(f"  {len(df_profiles)} regions profiled")

    # 4. PCA
    scores, loadings, n_components, pca = run_pca(df_profiles, variance_threshold)
    var_explained = sum(pca.explained_variance_ratio_) * 100
    _log(f"  PCA: {n_components} components explain {var_explained:.1f}% variance")

    # 5. Cluster
    cluster_labels, optimal_k, linkage_matrix = cluster_regions_ward(scores, max_clusters)
    _log(f"  Ward's clustering: {optimal_k} clusters (silhouette-selected)")

    # K-Means cross-check
    feature_matrix = df_profiles.drop(columns=["target_mean"], errors="ignore")
    feature_matrix = feature_matrix.fillna(0).replace([np.inf, -np.inf], 0)
    km_labels, km_k, _ = find_optimal_kmeans(feature_matrix, max_clusters=max_clusters)
    _log(f"  K-Means cross-check: {km_k} clusters (elbow method)")

    # 6. CID discrimination
    profile_cids = [c for c in cid_columns if c in df_profiles.columns]
    df_discrimination = compute_cid_discrimination(df_profiles, cluster_labels, profile_cids)

    # 7. CID-target association
    df_association = compute_cid_target_association(
        df, cluster_labels, effective_target, cid_columns
    )

    # 8. Save CSVs
    cluster_labels.to_csv(dir_out / "cluster_labels.csv", index=False)
    df_profiles.to_csv(dir_out / "region_cid_profiles.csv")
    loadings.to_csv(dir_out / "pca_loadings.csv")
    df_discrimination.to_csv(dir_out / "cid_discrimination.csv", index=False)
    df_association.to_csv(dir_out / "cid_target_association.csv", index=False)
    _log(f"  CSVs saved to {dir_out}")

    # 9. Plots
    paths = {}
    paths["dendrogram"] = plot_dendrogram(
        linkage_matrix, scores.index, cluster_labels["Cluster"].values, dir_out
    )
    paths["biplot"] = plot_pca_biplot(scores, loadings, cluster_labels, dir_out)
    paths["heatmap"] = plot_discrimination_heatmap(df_discrimination, dir_out, top_n=top_n_cids)
    paths["boxplot"] = plot_target_by_cluster(df, cluster_labels, effective_target, dir_out)

    # 10. Maps (if GeoDataFrame provided)
    if gdf is not None:
        paths["cluster_map"] = plot_cluster_map(gdf, cluster_labels, dir_out, countries)
        paths["cid_maps"] = plot_cid_maps(
            gdf, df_profiles, df_discrimination, dir_out, countries, top_n=3
        )
        _log(f"  Maps saved to {dir_out}")

    _log("  Cluster analysis complete")

    return {
        "effective_target": effective_target,
        "yield_available": yield_available,
        "cluster_labels": cluster_labels,
        "optimal_k": optimal_k,
        "discrimination": df_discrimination,
        "association": df_association,
        "profiles": df_profiles,
        "loadings": loadings,
        "paths": paths,
    }
