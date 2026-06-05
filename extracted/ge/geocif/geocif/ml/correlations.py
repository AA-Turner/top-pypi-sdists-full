"""
Correlation analysis and heatmap visualization for GEOCIF.

Refactored version with fixes for:
- Missing return statements
- Dead code removal
- Division by zero protection
- Import organization
- Code duplication
- Performance improvements (vectorization, caching)
- Variable shadowing
"""

import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import palettable as pal
import pandas as pd
import seaborn as sns  # Moved to module level
from tqdm.rich import tqdm

from geocif import utils
from geocif.progress import pbar as _pbar
from geocif.ml import embedding
from geocif.ml import stages as stages_module  # Renamed to avoid shadowing


# =============================================================================
# Helper Functions
# =============================================================================

def _filter_by_correlation_threshold(df_corr: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Filter DataFrame columns by correlation threshold.
    
    Args:
        df_corr: DataFrame with correlation values
        threshold: Minimum absolute mean correlation to keep column
        
    Returns:
        Filtered DataFrame
    """
    if df_corr.empty:
        return df_corr
    mask = abs(df_corr.mean()) > threshold
    return df_corr.loc[:, mask]


def _compute_absolute_medians(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute absolute median values for each column.
    
    Args:
        df: DataFrame with correlation values
        
    Returns:
        DataFrame with columns ['CID', 'Median']
    """
    if df.empty:
        return pd.DataFrame(columns=['CID', 'Median'])

    absolute_medians = df.abs().median()
    result = absolute_medians.reset_index()
    result.columns = ['CID', 'Median']
    return result


def _build_stage_info_cache(stages_features: list, method: str) -> dict:
    """
    Pre-compute stage information to avoid repeated function calls.
    
    Args:
        stages_features: List of stage strings
        method: Method string (dekad, biweekly, monthly)
        
    Returns:
        Dictionary mapping stage -> stage_info dict
    """
    return {
        stage: stages_module.get_stage_information_dict(f"GD4_{stage}", method)
        for stage in stages_features
    }


# =============================================================================
# Main Functions
# =============================================================================

def most_correlated_feature_by_time(df_train: pd.DataFrame, 
                                     simulation_stages: list, 
                                     target_col: str) -> pd.DataFrame:
    """
    Find the most correlated feature at each time stage.
    
    Args:
        df_train: Training DataFrame with features and target
        simulation_stages: List of stage identifiers
        target_col: Name of target column
        
    Returns:
        DataFrame with most correlated feature info by time stage
    """
    frames = []
    
    # Build cumulative stage lists
    cumulative_stages = [
        simulation_stages[:idx + 1] 
        for idx in range(len(simulation_stages))
    ]

    for stage_list in _pbar(cumulative_stages, leave=False,
                           desc="Compute most correlated feature"):
        current_stage = stage_list[-1]
        current_feature_set = [
            col for col in df_train.columns 
            if col.endswith(f"_{current_stage}")
        ]

        if not current_feature_set:
            continue

        # Get the most correlated feature for each region
        top_feature_by_region, counter = embedding.get_top_correlated_features(
            df_train[current_feature_set + ["Region"]],
            df_train[target_col],
        )

        if not counter:
            continue

        # Get most common feature
        most_common = counter.most_common(1)[0]
        feature_name = most_common[0]
        occurrence_count = most_common[1]

        # Calculate average score for the top feature (with protection)
        feature_scores = [
            value[1][0]
            for key, value in top_feature_by_region.items()
            if feature_name in value[0]
        ]
        
        if not feature_scores:
            continue
            
        average_score = sum(feature_scores) / len(feature_scores)
        feature_category = utils.remove_last_part(feature_name)

        df_row = pd.DataFrame({
            "Stage": [current_stage],
            "Date": [utils.dict_growth_stages.get(current_stage, "Unknown")],
            "Feature with Highest Correlation": [feature_name],
            "Feature Category": [feature_category],
            "Score": [average_score],
            "Number of Occurrences": [occurrence_count],
        })
        frames.append(df_row)

    if not frames:
        return pd.DataFrame()
    
    return pd.concat(frames, ignore_index=True)


def plot_feature_corr_by_time(df: pd.DataFrame, **kwargs) -> None:
    """
    Plot correlation heatmap by time with optional map.
    
    Args:
        df: DataFrame with correlation values (features x time stages)
        **kwargs: Configuration options including:
            - country: Country name
            - crop: Crop name
            - dir_output: Output directory path
            - forecast_season: Forecast season identifier
            - national_correlation: Boolean for national vs regional
            - groupby: Column name for grouping
            - plot_map: Boolean to include map
            - region_name: Name of region for title
            - region_id: ID of region
            - dg_country: GeoDataFrame for map plotting
    """
    # Extract kwargs
    country = kwargs.get("country", "Unknown")
    crop = kwargs.get("crop", "Unknown")
    dir_output = kwargs.get("dir_output")
    national_correlation = kwargs.get("national_correlation", False)
    group_by = kwargs.get("groupby")
    plot_map = kwargs.get("plot_map", False)
    region_name = kwargs.get("region_name", "")
    region_id = kwargs.get("region_id", "unknown")
    metric_label = kwargs.get("metric_label", "Concordance Correlation Coefficient")
    metric_dir = kwargs.get("metric_dir", "ccc")

    # Setup figure and gridspec
    fig = plt.figure(figsize=(10, 5))
    
    if plot_map:
        gs = fig.add_gridspec(
            3, 2, 
            height_ratios=[6, 5, 1], 
            width_ratios=[5, 1.5], 
            hspace=0.6, 
            wspace=0.0
        )
        ax_map = fig.add_subplot(gs[0, 1])
        ax_empty = fig.add_subplot(gs[2, 1])
    else:
        gs = fig.add_gridspec(3, 1, height_ratios=[6, 5, 1], hspace=0.6, wspace=0.0)

    ax_heatmap = fig.add_subplot(gs[0:2, 0])
    cbar_ax = fig.add_subplot(gs[2, 0])

    # Transpose and reverse columns (work on copy to avoid modifying input)
    df_plot = df.T
    df_plot = df_plot[df_plot.columns[::-1]]
    
    # Colormap: R² is 0–1 (sequential); CCC is –1 to +1 (diverging)
    cmap = (
        pal.colorbrewer.sequential.YlOrRd_9.get_mpl_colormap()
        if metric_dir == "r2"
        else pal.cartocolors.diverging.Earth_5.get_mpl_colormap()
    )

    # Create heatmap
    sns.heatmap(
        df_plot,
        ax=ax_heatmap,
        annot=True,
        cmap=cmap,
        fmt=".2f",
        square=False,
        linewidths=0.5,
        linecolor="white",
        cbar_ax=cbar_ax,
        cbar_kws={"orientation": "horizontal"},
        annot_kws={"size": 4},
        xticklabels=True,
        yticklabels=True,
    )
    ax_heatmap.tick_params(left=False, bottom=False)

    # Plot map if requested
    if plot_map:
        dg_country = kwargs.get("dg_country")
        
        if dg_country is not None:
            dg_country.plot(
                ax=ax_map,
                color="white",
                edgecolor="black",
                linewidth=1.0,
                facecolor=None,
                legend=False,
            )

            if not national_correlation and group_by is not None:
                dg_region = dg_country[dg_country[group_by] == region_id]
                if not dg_region.empty:
                    dg_region.plot(
                        ax=ax_map, 
                        color="blue", 
                        edgecolor="blue", 
                        linewidth=1.0, 
                        legend=False
                    )
                    ax_map.set_title(f"Region: {region_id}", color="blue")

        # Clean up map axes
        ax_map.axis("off")
        for spine in ax_map.spines.values():
            spine.set_visible(False)
        ax_empty.axis("off")

    # Style the heatmap
    cbar_ax.set_title(metric_label, loc="left", size="small")
    ax_heatmap.set_xticklabels(
        ax_heatmap.get_xticklabels(), size="x-small", rotation=0, fontsize=5
    )
    ax_heatmap.set_yticklabels(
        ax_heatmap.get_yticklabels(), size="x-small", fontsize=5
    )
    ax_heatmap.set_xlabel("")
    ax_heatmap.set_ylabel(" ")
    cbar_ax.tick_params(axis="both", which="major", labelsize=5)

    # Set titles
    country_title = country.title().replace("_", " ")
    crop_title = crop.title().replace("_", " ")
    display_region = region_name if not national_correlation else ""
    
    ax_heatmap.set_title(f"{country_title}, {crop_title}", fontsize=12, pad=18)
    ax_heatmap.text(
        0.5, 1.02,
        display_region,
        transform=ax_heatmap.transAxes,
        ha='center', 
        va='bottom',
        fontsize=8
    )

    # Save figure
    if not national_correlation:
        fname = f"{country}_{crop}_{region_id}_corr_feature_by_time.png"
    else:
        fname = f"{country}_{crop}_corr_feature_by_time.png"

    if dir_output is not None:
        dir_save = dir_output / metric_dir
        os.makedirs(dir_save, exist_ok=True)
        plt.savefig(dir_save / fname, dpi=250)
    
    plt.close(fig)


def plot_feature_scatter_by_time(
    df_raw: pd.DataFrame,
    df_corr: pd.DataFrame,
    **kwargs,
) -> None:
    """Grid of (feature, yield) scatter plots — one tile per heatmap cell.

    Renders the raw data underlying each (stage, feature) cell of the
    corresponding ccc/r2 heatmap, so callers can see *how* each correlation
    value was computed. Saved at ``dir_output / scatter / ...``, one level
    above the existing ``ccc/`` and ``r2/`` subdirs.

    Top features only (sorted by |median correlation across stages|),
    capped at ``top_n`` so the grid stays readable. Annotates each tile
    with the correlation value from ``df_corr``.

    Args:
        df_raw: Per-region DataFrame containing feature columns + target.
            Columns are expected to be wide-format ``"<CID> <Stage Name>"``.
        df_corr: Correlation matrix (rows = stage labels, cols = CIDs)
            — same frame ``plot_feature_corr_by_time`` consumes.
        **kwargs: country, crop, target_col, dir_output, region_id,
            region_name, national_correlation, metric_dir, metric_label,
            top_n (default 16).
    """
    if df_corr is None or df_corr.empty or df_raw is None or df_raw.empty:
        return

    target_col = kwargs.get("target_col")
    dir_output = kwargs.get("dir_output")
    country = kwargs.get("country", "Unknown")
    crop = kwargs.get("crop", "Unknown")
    region_id = kwargs.get("region_id")
    region_name = kwargs.get("region_name", "")
    national_correlation = kwargs.get("national_correlation", False)
    metric_dir = kwargs.get("metric_dir", "ccc")
    metric_label = kwargs.get("metric_label", "CCC")
    top_n = int(kwargs.get("top_n", 16))

    if dir_output is None or target_col is None or target_col not in df_raw.columns:
        return

    # Pick top-N features by |median across stages|. Ties broken by order.
    abs_medians = df_corr.abs().median(axis=0).sort_values(ascending=False)
    top_features = [f for f in abs_medians.index.tolist() if pd.notna(abs_medians[f])][:top_n]
    if not top_features:
        return

    stages = df_corr.index.tolist()
    n_stages = len(stages)
    n_feats = len(top_features)

    y_full = df_raw[target_col]
    y_valid = y_full.dropna()
    if y_valid.empty:
        return
    y_lim = (float(y_valid.min()), float(y_valid.max()))

    # Layout: when there's only one stage, ignore the stage dimension and
    # arrange the features in a near-square grid (otherwise 16 features
    # become a 16×1 column ~25 inches tall). With multiple stages keep
    # features-as-rows × stages-as-cols since the axis labels carry
    # information; cap the column count too so wide stage counts don't
    # produce unreadable figures.
    MAX_COLS = 5
    if n_stages == 1:
        # Near-square: ~sqrt(n) columns, capped at MAX_COLS.
        n_cols = min(MAX_COLS, max(1, int(np.ceil(np.sqrt(n_feats)))))
        n_rows = int(np.ceil(n_feats / n_cols))
        fig_w = min(2.4 * n_cols + 0.6, 16)
        fig_h = min(2.0 * n_rows + 0.8, 22)
    else:
        # Multi-stage: features × stages grid. Cap stages displayed at
        # MAX_COLS so the figure stays printable; extra stages dropped
        # (they're already shown in the heatmap, which keeps all stages).
        n_cols = min(MAX_COLS, n_stages)
        n_rows = n_feats
        fig_w = min(2.0 * n_cols + 1.0, 16)
        fig_h = min(1.5 * n_rows + 0.8, 26)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_w, fig_h), squeeze=False)

    def _match_column(feat_name: str, stage_label: str) -> Optional[str]:
        # Heatmap stage labels are start-only (e.g. "May 1"); raw columns
        # carry the full range ("PRCPTOT May 1-May 31"). Match on prefix.
        stage_str = str(stage_label).strip()
        return next(
            (
                c for c in df_raw.columns
                if isinstance(c, str)
                and c.startswith(f"{feat_name} ")
                and c.split(" ", 1)[1].startswith(stage_str)
            ),
            None,
        )

    def _draw_tile(ax, feat_name: str, stage_label: str, *, show_xlabel: str = "") -> bool:
        col_match = _match_column(feat_name, stage_label)
        if col_match is None:
            ax.set_axis_off()
            return False
        x = df_raw[col_match]
        mask = x.notna() & y_full.notna()
        if mask.sum() < 2:
            ax.set_axis_off()
            return False
        xv = x[mask].to_numpy(dtype=float)
        yv = y_full[mask].to_numpy(dtype=float)
        ax.scatter(xv, yv, s=8, alpha=0.5, c="tab:blue", edgecolors="none")

        # Always compute BOTH metrics inline from the scatter points
        # themselves (rather than reading whichever metric is in df_corr)
        # so the annotated values match exactly what the eye sees in this
        # tile. The df_corr value is the per-region mean used by the
        # heatmap; the inline values are the pooled stats — the gap
        # between them is itself diagnostic (heatmap CCC high but pooled
        # r² low ⇒ signal is between-region, not within-region).
        r2_inline = np.nan
        ccc_inline = np.nan
        if xv.size >= 2 and np.std(xv) > 0 and np.std(yv) > 0:
            r = np.corrcoef(xv, yv)[0, 1]
            if np.isfinite(r):
                r2_inline = float(r * r)
            mx, my = float(np.mean(xv)), float(np.mean(yv))
            vx, vy = float(np.var(xv)), float(np.var(yv))
            cov = float(np.mean((xv - mx) * (yv - my)))
            denom = vx + vy + (mx - my) ** 2
            if denom > 0:
                ccc_inline = 2 * cov / denom

        lines = [
            f"r²={r2_inline:.2f}" if np.isfinite(r2_inline) else "r²=—",
            f"ccc={ccc_inline:.2f}" if np.isfinite(ccc_inline) else "ccc=—",
            f"n={int(mask.sum())}",
        ]
        ax.text(
            0.02, 0.98, "\n".join(lines),
            transform=ax.transAxes,
            fontsize=6, va="top", ha="left",
            bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=1),
        )
        ax.set_ylim(y_lim)
        ax.tick_params(labelsize=5)
        ax.grid(True, alpha=0.2, linewidth=0.4)
        if show_xlabel:
            ax.set_xlabel(show_xlabel, fontsize=6)
        return True

    if n_stages == 1:
        # Single-stage layout: features tiled in a near-square grid.
        stage_label = stages[0]
        axes_flat = axes.flatten()
        for k, feat in enumerate(top_features):
            ax = axes_flat[k]
            ok = _draw_tile(ax, feat, stage_label, show_xlabel=feat)
            if ok:
                # Per-tile column index → only leftmost column gets y label.
                if k % n_cols == 0:
                    ax.set_ylabel(target_col, fontsize=6)
        # Hide unused tiles in the trailing partial row.
        for k in range(n_feats, len(axes_flat)):
            axes_flat[k].set_axis_off()
    else:
        # Multi-stage layout: features as rows, stages as columns.
        # Stages truncated to first n_cols (≤ MAX_COLS) — extras stay in
        # the heatmap. Stages are already in chronological order for
        # most methods, so this drops the latest stages last.
        stages_shown = stages[:n_cols]
        for i, feat in enumerate(top_features):
            for j, stage in enumerate(stages_shown):
                ax = axes[i][j]
                _draw_tile(ax, feat, stage)
                if i == 0:
                    ax.set_title(str(stage).strip(), fontsize=7)
                if j == 0:
                    ax.set_ylabel(
                        feat, fontsize=6, rotation=0,
                        ha="right", va="center", labelpad=24,
                    )

    # Suptitle: keep concise so it actually fits. Truncate the region-name
    # list (can be 100+ entries when cluster_strategy=single pools every
    # admin unit) to first 3 + count.
    country_title = country.title().replace("_", " ")
    crop_title = crop.title().replace("_", " ")
    region_suffix = ""
    if region_name:
        names = [n.strip() for n in str(region_name).split(",") if n.strip()]
        if len(names) <= 3:
            region_suffix = f" — {', '.join(names)}"
        else:
            region_suffix = f" — {', '.join(names[:3])} (+{len(names) - 3} more)"
    stage_note = f"  stage: {stages[0]}" if n_stages == 1 else ""
    fig.suptitle(
        f"{country_title}, {crop_title}{region_suffix}  "
        f"(top-{n_feats} by |{metric_dir.upper()}|{stage_note})",
        fontsize=10,
    )
    # Reserve ~5% at the top for the suptitle so it doesn't collide with
    # the first row of tiles.
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    if not national_correlation and region_id is not None:
        fname = f"{country}_{crop}_{region_id}_scatter_feature_by_time.png"
    else:
        fname = f"{country}_{crop}_scatter_feature_by_time.png"

    dir_save = dir_output / "scatter"
    os.makedirs(dir_save, exist_ok=True)
    plt.savefig(dir_save / fname, dpi=200)
    plt.close(fig)


def _all_correlated_feature_by_time(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Compute correlations for all features across time stages.
    
    Args:
        df: DataFrame with features, target, and Region column
        **kwargs: Configuration including all_stages, target_col, method
        
    Returns:
        DataFrame with correlations indexed by stage name
    """
    all_stages = kwargs.get("all_stages", [])
    target_col = kwargs.get("target_col")
    method = kwargs.get("method")
    corr_fn = kwargs.get("corr_fn")

    if not len(all_stages):
        return pd.DataFrame()

    # Build time-stage list for the heatmap x-axis.
    # The longest stage encodes the full growing-season month order.
    longest_stage = max(all_stages, key=lambda s: len(s.split("_")))
    longest_stage_parts = longest_stage.split("_")

    # Strategy 1: individual time-period stages (2-element consecutive
    # pairs from the longest stage).  These match the ML DataFrame when
    # use_single_time_period_as_feature is True.
    all_stages_set = set(all_stages)
    individual_stages = []
    for i in range(len(longest_stage_parts) - 1):
        pair = f"{longest_stage_parts[i]}_{longest_stage_parts[i + 1]}"
        if pair in all_stages_set:
            individual_stages.append(pair)

    # Note: for _r methods, longest-stage parts run latest → earliest,
    # so pairs are in end-to-start order.  The plot function applies
    # [::-1] to flip columns to chronological order, so we keep this
    # ordering here to stay consistent with the plot's reversal.

    # Strategy 2 (fallback): progressive suffixes of the longest stage.
    # Works when the DataFrame carries cumulative (multi-period) features.
    suffix_stages = [
        "_".join(longest_stage_parts[i:])
        for i in range(len(longest_stage_parts))
    ]

    # Pick whichever strategy actually has matching columns in the data.
    stages_features = suffix_stages          # default
    if individual_stages:
        test_cache = _build_stage_info_cache(individual_stages[:1], method)
        test_name = test_cache[individual_stages[0]]["Stage Name"]
        if any(test_name in col for col in df.columns):
            stages_features = individual_stages

    # Drop rows without target
    df_clean = df.dropna(subset=[target_col])
    
    if df_clean.empty:
        return pd.DataFrame()

    # Pre-compute stage info cache
    stage_info_cache = _build_stage_info_cache(stages_features, method)

    frames = []
    
    for stage in _pbar(stages_features, leave=False, desc="Calculating correlations"):
        stage_name = stage_info_cache[stage]["Stage Name"]
        current_feature_set = [
            col for col in df_clean.columns if stage_name in col
        ]

        if not current_feature_set:
            continue

        # Get correlations for all features
        df_tmp = embedding.get_all_features_correlation(
            df_clean[current_feature_set + ["Region"]],
            df_clean[target_col],
            method,
            corr_fn=corr_fn,
        )

        if not df_tmp.empty:
            frames.append(df_tmp)

    if not frames:
        return pd.DataFrame()

    df_results = pd.concat(frames, ignore_index=True)
    
    if df_results.empty:
        return pd.DataFrame()

    # Process results
    df_results = df_results.drop(columns="Region", errors='ignore')
    df_results = df_results.groupby(method).mean()

    # Reindex by stage names (using cached values)
    all_stage_names = [stage_info_cache[stage]["Stage Name"] for stage in stages_features]
    df_results = df_results.reindex(all_stage_names)
    
    # Clean up
    df_results = df_results.dropna(how="all")
    
    if not df_results.empty:
        df_results.index = df_results.index.str.split("-").str[0]

    return df_results


def _process_region_correlations(
    df_corr: pd.DataFrame,
    threshold: float,
    combined_dict: dict,
    region_id,
    group: pd.DataFrame,
    kwargs: dict
) -> tuple:
    """
    Process correlations for a single region.
    
    Args:
        df_corr: Correlation DataFrame for the region
        threshold: Correlation threshold
        combined_dict: Dictionary mapping metrics to types
        region_id: Region identifier
        group: Group DataFrame
        kwargs: Additional kwargs for plotting
        
    Returns:
        Tuple of (selected_features_df, best_cid_array)
    """
    # Remove columns with >50% NaN
    df_corr = df_corr.dropna(thresh=len(df_corr) / 2, axis=1)
    
    if df_corr.empty:
        return pd.DataFrame(columns=['CID', 'Median']), {}

    # Filter by threshold
    df_filtered = _filter_by_correlation_threshold(df_corr, threshold)

    if df_filtered.empty:
        return pd.DataFrame(columns=['CID', 'Median']), {}

    # Compute medians
    absolute_median_df = _compute_absolute_medians(df_filtered)

    # Compute best CID by type (vectorized)
    df_metrics = (
        df_filtered.median(axis=0)
        .abs()
        .sort_values(ascending=False)
        .reset_index()
    )
    df_metrics.columns = ["Metric", "Value"]
    
    # Vectorized type assignment
    df_metrics["Type"] = df_metrics["Metric"].map(
        lambda x: combined_dict.get(x, [None])[0]
    )

    # Get best CID per type
    best_cid = (
        df_metrics.groupby("Type")
        .apply(lambda x: x.nlargest(1, "Value")["Metric"].iloc[0])
        .values
    )

    # Plot
    kwargs_copy = kwargs.copy()
    kwargs_copy["region_id"] = region_id
    kwargs_copy["region_name"] = ", ".join(str(x) for x in group['Region'].unique())
    plot_feature_corr_by_time(df_filtered, **kwargs_copy)

    # Optional diagnostic: per-region grid of raw (feature, yield) scatter
    # plots, one tile per heatmap cell. Gated by [ML] plot_correlation_scatter
    # since it can produce many files (one per region per model per forecast
    # year). Useful when the heatmap looks reasonable but downstream model
    # skill is poor — the scatter shows whether each CCC reflects real
    # cross-region structure or is being driven by a few outliers.
    if kwargs_copy.get("plot_correlation_scatter"):
        plot_feature_scatter_by_time(group, df_filtered, **kwargs_copy)

    return absolute_median_df, best_cid


def all_correlated_feature_by_time(df: pd.DataFrame, **kwargs) -> tuple:
    """
    Compute correlations for all features by time, optionally grouped by region.
    
    Args:
        df: Input DataFrame
        **kwargs: Configuration options including:
            - national_correlation: Boolean for national vs regional analysis
            - groupby: Column name for grouping
            - combined_dict: Dictionary mapping metrics to types
            - correlation_threshold: Minimum correlation threshold
            
    Returns:
        Tuple of (dict_selected_features, dict_best_cid)
    """
    national_correlation = kwargs.get("national_correlation", False)
    group_by = kwargs.get("groupby")
    combined_dict = kwargs.get("combined_dict", {})
    threshold = kwargs.get("correlation_threshold", 0.0)
    correlation_metric = kwargs.get("correlation_metric", "both")

    # Primary metric drives feature selection; extra metrics are plot-only.
    if correlation_metric == "r2":
        primary_metric = "r2"
        extra_plot_metrics = []
    elif correlation_metric == "both":
        primary_metric = "ccc"
        extra_plot_metrics = ["r2"]
    else:  # "ccc" or unrecognised
        primary_metric = "ccc"
        extra_plot_metrics = []

    def _metric_kwargs(base_kwargs, metric):
        fn = embedding._r2_corrwith if metric == "r2" else None
        label = "R² (Coefficient of Determination)" if metric == "r2" else "Concordance Correlation Coefficient"
        return {**base_kwargs, "corr_fn": fn, "metric_label": label, "metric_dir": metric}

    primary_kwargs = _metric_kwargs(kwargs, primary_metric)

    dict_selected_features = {}
    dict_best_cid = {}

    if not national_correlation:
        groups = df.groupby(group_by)

        for region_id, group in _pbar(
            groups,
            desc=f"Compute all correlated feature by {group_by}",
            leave=False
        ):
            df_corr = _all_correlated_feature_by_time(group, **primary_kwargs)

            if not df_corr.empty:
                selected_df, best_cid = _process_region_correlations(
                    df_corr, threshold, combined_dict, region_id, group, primary_kwargs
                )
                dict_selected_features[region_id] = selected_df
                dict_best_cid[region_id] = best_cid
            else:
                # Fallback to full dataset (HACK from original)
                df_corr_full = _all_correlated_feature_by_time(df, **primary_kwargs)

                if not df_corr_full.empty:
                    df_filtered = _filter_by_correlation_threshold(df_corr_full, threshold)
                    dict_selected_features[region_id] = _compute_absolute_medians(df_filtered)
                else:
                    dict_selected_features[region_id] = pd.DataFrame(columns=['CID', 'Median'])

                dict_best_cid[region_id] = {}

            # Extra plot-only metrics (no feature selection update)
            for extra_metric in extra_plot_metrics:
                extra_kwargs = _metric_kwargs(kwargs, extra_metric)
                df_corr_extra = _all_correlated_feature_by_time(group, **extra_kwargs)
                if not df_corr_extra.empty:
                    df_filtered_extra = _filter_by_correlation_threshold(df_corr_extra, threshold)
                    if not df_filtered_extra.empty:
                        kwargs_plot = extra_kwargs.copy()
                        kwargs_plot["region_id"] = region_id
                        kwargs_plot["region_name"] = ", ".join(str(x) for x in group['Region'].unique())
                        plot_feature_corr_by_time(df_filtered_extra, **kwargs_plot)
    else:
        # National correlation
        df_corr = _all_correlated_feature_by_time(df, **primary_kwargs)
        df_filtered = _filter_by_correlation_threshold(df_corr, threshold)

        dict_selected_features[0] = _compute_absolute_medians(df_filtered)

        if not df_corr.empty:
            plot_feature_corr_by_time(df_corr, **primary_kwargs)
            # National-scope scatter diagnostic (see _process_region_correlations
            # for rationale). Region-naming kept blank since national pools all
            # regions into one CCC computation.
            if primary_kwargs.get("plot_correlation_scatter"):
                plot_feature_scatter_by_time(df, df_corr, **primary_kwargs)

        # Extra plot-only metrics (national)
        for extra_metric in extra_plot_metrics:
            extra_kwargs = _metric_kwargs(kwargs, extra_metric)
            df_corr_extra = _all_correlated_feature_by_time(df, **extra_kwargs)
            if not df_corr_extra.empty:
                plot_feature_corr_by_time(df_corr_extra, **extra_kwargs)

    return dict_selected_features, dict_best_cid