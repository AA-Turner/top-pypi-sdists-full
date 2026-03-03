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
import palettable as pal
import pandas as pd
import seaborn as sns  # Moved to module level
from tqdm import tqdm

from geocif import utils
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
        DataFrame with columns ['CEI', 'Median']
    """
    if df.empty:
        return pd.DataFrame(columns=['CEI', 'Median'])
    
    absolute_medians = df.abs().median()
    result = absolute_medians.reset_index()
    result.columns = ['CEI', 'Median']
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

    for stage_list in tqdm(cumulative_stages, leave=False, 
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
    
    # Create heatmap
    sns.heatmap(
        df_plot,
        ax=ax_heatmap,
        annot=True,
        cmap=pal.cartocolors.diverging.Earth_5.get_mpl_colormap(),
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
    cbar_ax.set_title("Correlation Coefficient", loc="left", size="small")
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
        os.makedirs(dir_output, exist_ok=True)
        plt.savefig(dir_output / fname, dpi=250)
    
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
    
    for stage in tqdm(stages_features, leave=False, desc="Calculating correlations"):
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
            method
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
        Tuple of (selected_features_df, best_cei_array)
    """
    # Remove columns with >50% NaN
    df_corr = df_corr.dropna(thresh=len(df_corr) / 2, axis=1)
    
    if df_corr.empty:
        return pd.DataFrame(columns=['CEI', 'Median']), {}

    # Filter by threshold
    df_filtered = _filter_by_correlation_threshold(df_corr, threshold)
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['CEI', 'Median']), {}

    # Compute medians
    absolute_median_df = _compute_absolute_medians(df_filtered)

    # Compute best CEI by type (vectorized)
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

    # Get best CEI per type
    best_cei = (
        df_metrics.groupby("Type")
        .apply(lambda x: x.nlargest(1, "Value")["Metric"].iloc[0])
        .values
    )

    # Plot
    kwargs_copy = kwargs.copy()
    kwargs_copy["region_id"] = region_id
    kwargs_copy["region_name"] = ", ".join(str(x) for x in group['Region'].unique())
    plot_feature_corr_by_time(df_filtered, **kwargs_copy)

    return absolute_median_df, best_cei


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
        Tuple of (dict_selected_features, dict_best_cei)
    """
    national_correlation = kwargs.get("national_correlation", False)
    group_by = kwargs.get("groupby")
    combined_dict = kwargs.get("combined_dict", {})
    threshold = kwargs.get("correlation_threshold", 0.0)

    dict_selected_features = {}
    dict_best_cei = {}

    if not national_correlation:
        groups = df.groupby(group_by)
        
        for region_id, group in tqdm(
            groups, 
            desc=f"Compute all correlated feature by {group_by}", 
            leave=False
        ):
            df_corr = _all_correlated_feature_by_time(group, **kwargs)

            if not df_corr.empty:
                selected_df, best_cei = _process_region_correlations(
                    df_corr, threshold, combined_dict, region_id, group, kwargs
                )
                dict_selected_features[region_id] = selected_df
                dict_best_cei[region_id] = best_cei
            else:
                # Fallback to full dataset (HACK from original)
                df_corr_full = _all_correlated_feature_by_time(df, **kwargs)
                
                if not df_corr_full.empty:
                    df_filtered = _filter_by_correlation_threshold(df_corr_full, threshold)
                    dict_selected_features[region_id] = _compute_absolute_medians(df_filtered)
                else:
                    dict_selected_features[region_id] = pd.DataFrame(columns=['CEI', 'Median'])
                    
                dict_best_cei[region_id] = {}
    else:
        # National correlation
        df_corr = _all_correlated_feature_by_time(df, **kwargs)
        df_filtered = _filter_by_correlation_threshold(df_corr, threshold)
        
        dict_selected_features[0] = _compute_absolute_medians(df_filtered)
        
        if not df_corr.empty:
            plot_feature_corr_by_time(df_corr, **kwargs)

    return dict_selected_features, dict_best_cei