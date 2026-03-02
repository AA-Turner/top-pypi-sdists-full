"""
Feature correlation and embedding utilities for GEOCIF.

Refactored version with fixes for:
- Mutable default arguments
- Redundant import aliases
- Performance improvements (vectorization)
- Better type hints and documentation
"""

from collections import Counter
from typing import Optional

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from tqdm import tqdm


def extract_regions(
    X: pd.DataFrame, 
    y: pd.Series, 
    regions: Optional[list] = None
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Extract data for specific regions.
    
    Args:
        X: Input DataFrame containing features and 'Region' column
        y: Target Series
        regions: List of region identifiers to extract. If None, returns empty data.
        
    Returns:
        Tuple of (filtered X, filtered y) with reset indices
    """
    if regions is None:
        regions = []
    
    X_copy = X.copy()
    y_copy = y.copy()

    mask = X_copy["Region"].isin(regions)
    indices = X_copy[mask].index
    
    X_filtered = X_copy.loc[indices, :].reset_index(drop=True)
    y_filtered = y_copy.loc[indices].reset_index(drop=True)

    return X_filtered, y_filtered


def _compute_correlations_slow(X: pd.DataFrame, y: pd.Series) -> dict:
    """
    Compute Pearson correlations for each numeric feature (loop-based).
    
    This is the slower, more explicit version. Use _compute_correlations_fast
    for better performance on large datasets.
    
    Args:
        X: Input DataFrame with features
        y: Target Series
        
    Returns:
        Dictionary mapping feature names to correlation values
    """
    feature_correlations = {}

    # Get numeric columns only
    numeric_cols = X.select_dtypes(include=[np.number]).columns

    for feature in numeric_cols:
        f_series = X[feature]

        # Create mask for valid (non-NaN) values in both arrays
        mask = ~(np.isnan(y) | np.isnan(f_series))
        y_filtered = y[mask]
        f_series_filtered = f_series[mask]

        # Need at least 3 points for meaningful correlation
        if len(y_filtered) < 3:
            feature_correlations[feature] = np.nan
            continue

        # Handle zero variance cases
        if np.std(f_series_filtered) == 0 or np.std(y_filtered) == 0:
            feature_correlations[feature] = np.nan
            continue

        try:
            r, _ = pearsonr(y_filtered, f_series_filtered)
            feature_correlations[feature] = round(r, 3)
        except Exception:
            feature_correlations[feature] = np.nan

    return feature_correlations


def _compute_correlations_fast(X: pd.DataFrame, y: pd.Series) -> pd.Series:
    """
    Compute Pearson correlations using vectorized pandas operations.
    
    This is significantly faster than the loop-based version for large DataFrames.
    
    Args:
        X: Input DataFrame with numeric features
        y: Target Series
        
    Returns:
        Series with correlation values indexed by feature name
    """
    # Select only numeric columns
    numeric_df = X.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        return pd.Series(dtype=float)
    
    # Use pandas corrwith for vectorized correlation
    correlations = numeric_df.corrwith(y).round(3)
    
    return correlations.dropna()


def find_most_common_top_feature(top_feature_by_region: dict) -> Counter:
    """
    Find the most common top feature across regions.
    
    Args:
        top_feature_by_region: Dictionary mapping region_id to 
                               ([feature_names], [correlation_values])
        
    Returns:
        Counter with feature occurrence counts
    """
    if not top_feature_by_region:
        return Counter()
    
    # Extract the first (top) feature from each region
    top_features = [
        value[0][0] 
        for value in top_feature_by_region.values()
        if value[0]  # Ensure non-empty
    ]

    return Counter(top_features)


def get_top_correlated_features(
    inputs: pd.DataFrame, 
    targets: pd.Series
) -> tuple[dict, Counter]:
    """
    Get the most correlated feature for each region.
    
    Args:
        inputs: DataFrame with features and 'Region' column
        targets: Target Series aligned with inputs
        
    Returns:
        Tuple of:
            - Dictionary mapping region_id to ([top_feature], [top_correlation])
            - Counter with occurrence counts of top features
    """
    feature_by_region = {}

    for region_id in inputs["Region"].unique():
        X, y = extract_regions(inputs, targets, regions=[region_id])

        if X.empty or len(y) < 3:
            continue

        # Use fast vectorized correlation
        correlations = _compute_correlations_fast(X, y)
        
        # Filter out NaN values
        correlations = correlations.dropna()

        if correlations.empty:
            continue

        # Sort by absolute correlation value (descending)
        sorted_correlations = correlations.abs().sort_values(ascending=False)
        
        top_feature = sorted_correlations.index[0]
        top_corr = correlations[top_feature]  # Keep original sign
        
        feature_by_region[region_id] = ([top_feature], [top_corr])

    counter = find_most_common_top_feature(feature_by_region)

    return feature_by_region, counter


def get_all_features_correlation(
    inputs: pd.DataFrame,
    targets: pd.Series,
    method: str
) -> pd.DataFrame:
    """
    Compute correlations for all features, pivoted by time period.
    
    Fast vectorized version that handles feature names with or without spaces.
    
    Args:
        inputs: DataFrame with numeric features and 'Region' column
        targets: Target Series aligned with inputs
        method: Method string used as column name in output (e.g., 'dekad_r')
        
    Returns:
        DataFrame with columns: Region, method, and one column per metric
    """
    numeric_cols = inputs.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        return pd.DataFrame()

    # Prepare working DataFrame
    df_all = inputs[numeric_cols + ["Region"]].copy()
    df_all["__target__"] = targets.values

    frames: list[pd.DataFrame] = []

    for region_id, group in tqdm(df_all.groupby("Region", sort=False), leave=False):
        # Vectorized correlation computation
        correlations = group[numeric_cols].corrwith(group["__target__"]).round(3).dropna()
        
        if correlations.empty:
            continue

        # Parse feature names: split on first space to get (metric, time_period)
        # Example: "NDVI Jan-Feb" -> ("NDVI", "Jan-Feb")
        # Example: "NDVI_compound Jan-Feb" -> ("NDVI_compound", "Jan-Feb")
        feature_index = pd.Series(correlations.index)
        split_result = feature_index.str.split(" ", n=1, expand=True)
        
        # Handle case where no spaces exist in feature names
        if split_result.shape[1] == 1:
            split_result[1] = ""
        
        # Ensure consistent column naming
        split_result.columns = [0, 1]

        # Build result DataFrame
        df_region = pd.DataFrame({
            "Metric": split_result[0].values,
            method: split_result[1].values,
            "Value": correlations.values
        })
        
        # Pivot to wide format: rows=time_period, columns=metrics
        df_region = (
            df_region
            .pivot_table(
                index=method, 
                columns="Metric",
                values="Value", 
                aggfunc="first"
            )
            .reset_index()
        )
        
        df_region.insert(0, "Region", region_id)
        frames.append(df_region)

    if not frames:
        return pd.DataFrame()
    
    return pd.concat(frames, ignore_index=True)


# =============================================================================
# Utility Functions
# =============================================================================

def compute_feature_importance_by_correlation(
    df: pd.DataFrame,
    target_col: str,
    feature_cols: Optional[list] = None,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Rank features by absolute correlation with target.
    
    Args:
        df: DataFrame with features and target
        target_col: Name of target column
        feature_cols: List of feature columns. If None, uses all numeric columns.
        top_n: Number of top features to return
        
    Returns:
        DataFrame with columns ['Feature', 'Correlation', 'Abs_Correlation']
    """
    if feature_cols is None:
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        feature_cols = [c for c in feature_cols if c != target_col]
    
    target = df[target_col]
    features_df = df[feature_cols]
    
    correlations = features_df.corrwith(target).round(3)
    
    result = pd.DataFrame({
        'Feature': correlations.index,
        'Correlation': correlations.values,
        'Abs_Correlation': correlations.abs().values
    })
    
    result = result.sort_values('Abs_Correlation', ascending=False).head(top_n)
    result = result.reset_index(drop=True)
    
    return result