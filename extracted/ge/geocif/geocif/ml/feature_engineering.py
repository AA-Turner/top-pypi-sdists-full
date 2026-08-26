import os

import numpy as np
import pandas as pd
from tqdm.rich import tqdm

from geocif.progress import pbar as _pbar


def compute_last_year_yield(df, target_col="Yield (tn per ha)"):
    """
    Computes the yield of the previous year for each region.

    The value is taken from the most recent year STRICTLY BEFORE each row's
    Harvest Year that has data — the same "closest prior" rule
    ``compute_lag_yield`` uses via ``only_historic=True``, so gaps in a
    region's series are tolerated. A region's earliest year has no
    predecessor and is left NaN (NaN-native models handle it).

    Before 2026-08-25 this masked on ``Harvest Year == harvest_year`` — the
    SAME year — so the column was an exact copy of ``target_col``. Two
    consequences, both now closed: the ``last_year`` baseline model
    (geocif.py ``_predict_baseline``) predicted the very value it was scored
    against, and a copy of the target reached any model with
    ``last_year_yield_as_feature = True`` or, via the ``nbr_Last Year ...``
    wrapper, ``use_spatial_neighbors = True``.

    Args:
        df (DataFrame): The original DataFrame containing yield data.
        target_col (str): The column name from which to compute the previous year yield.

    Returns:
        DataFrame: The original DataFrame enhanced with a new column for the previous year yield.
    """
    # Ensure 'Harvest Year' is treated as integer for accurate comparisons
    df["Harvest Year"] = df["Harvest Year"].astype(int)
    # Initialize the new column with NaNs
    df[f"Last Year {target_col}"] = np.nan

    for region, group in _pbar(
        df.groupby("Region"), desc="Last year yields", leave=False
    ):
        # One value per year for this region, sorted so we can look backwards.
        per_year = (
            group.dropna(subset=[target_col])
            .groupby("Harvest Year")[target_col]
            .first()
            .sort_index()
        )
        if per_year.empty:
            continue
        years = per_year.index.to_numpy()

        for harvest_year in group["Harvest Year"].unique():
            prior = years[years < harvest_year]
            if prior.size == 0:
                continue  # earliest year for this region: no predecessor
            df.loc[
                (df["Region"] == region) & (df["Harvest Year"] == harvest_year),
                f"Last Year {target_col}",
            ] = per_year.loc[prior.max()]

    return df

def compute_closest_years(all_years, harvest_year, number_lag_years, only_historic=False):
    """
    Finds the historical years closest to a given harvest year,
    excluding any future year (harvest_year itself and beyond) based on the only_historic flag.

    Args:
        all_years (array-like): List or array of all years to consider.
        harvest_year (int): The year from which to compute distance.
        number_lag_years (int): Number of closest years to return.
        only_historic (bool): If True, only consider years before the harvest year.

    Returns:
        list: The historical years closest to the given harvest year.
              Returns an empty list if no historical years exist.
    """
    # Exclude the harvest year before computation to simplify logic
    if only_historic:
        filtered_years = [year for year in all_years if year < harvest_year]
    else:
        filtered_years = [year for year in all_years if year != harvest_year]

    # If no historical years exist, return an empty list
    if not filtered_years:
        return []

    # Sort the years based on their absolute difference from the harvest year
    closest_years = np.array(filtered_years)[
        np.argsort(np.abs(np.array(filtered_years) - harvest_year))[:number_lag_years]
    ]

    return closest_years.tolist()


def compute_median_statistics(
    df, all_seasons_with_yield, number_median_years, target_col="Yield (tn per ha)",
    only_historic=True,
):
    """
    Enhances the DataFrame with a new column that contains the median yield from the closest lag years.

    Args:
        df (DataFrame): The original DataFrame containing yield data.
        all_seasons_with_yield (array-like): List of seasons that have yield data.
        number_median_years (int): Number of years to consider for computing the median yield.
        target_col (str): The column name from which to compute the median yield.
        only_historic (bool): Restrict the window to years strictly BEFORE each
            row's Harvest Year (default True). The pre-2026-08-25 behavior
            (False) picked the *closest* years in either direction, so a 2018
            row's "Median ..." column averaged 2019/2020 values — future
            information that is unavailable at deployment time and leaked into
            every hindcast fold (directly when *_as_feature was on, and via the
            ``nbr_`` neighbor wrapper even when it was off). Earliest years now
            get NaN instead of a future-only window; NaN-native models handle it.

    Returns:
        DataFrame: The original DataFrame enhanced with a new column for median lag yield.
    """
    # Ensure 'Harvest Year' is treated as integer for accurate comparisons
    df["Harvest Year"] = df["Harvest Year"].astype(int)
    # Initialize the new column with NaNs
    df[f"Median {target_col}"] = np.nan

    for region, group in _pbar(df.groupby("Region"), desc="Median yield", leave=False):
        unique_years = group["Harvest Year"].unique()

        # Check if the target column is empty for the current group
        if group[target_col].isnull().all():
            continue

        for harvest_year in unique_years:
            closest_years = compute_closest_years(
                all_seasons_with_yield, harvest_year, number_median_years,
                only_historic=only_historic,
            )
            if not closest_years:
                continue
            mask = (group["Harvest Year"].isin(closest_years)) & (
                group["Region"] == region
            )
            median_yield = group.loc[mask, target_col].mean()
            df.loc[
                (df["Region"] == region) & (df["Harvest Year"] == harvest_year),
                f"Median {target_col}",
            ] = median_yield

    return df


def compute_user_median_statistics(df, user_years, target_col="Yield (tn per ha)"):
    """
    Enhances the DataFrame with a new column that contains the median yield computed
    using only the yields from the user-specified list of years.

    Args:
        df (DataFrame): The original DataFrame containing yield data.
        user_years (array-like): List of years to consider for computing the median yield.
        target_col (str): The column name from which to compute the median yield.

    Returns:
        DataFrame: The original DataFrame enhanced with a new column for median yield.
    """
    # Ensure 'Harvest Year' is treated as integer for accurate comparisons.
    df["Harvest Year"] = df["Harvest Year"].astype(int)

    # Sort the user_years list to reliably extract the earliest and latest years.
    user_years_sorted = sorted(user_years)
    first_year = user_years_sorted[0]
    last_year = user_years_sorted[-1]

    # Define the new column name to include the range of years.
    new_col_name = f"Median {target_col} ({first_year}-{last_year})"

    # Initialize the new column with NaN values.
    df[new_col_name] = np.nan

    # Group by region and compute the median yield for the specified years.
    for region, group in _pbar(df.groupby("Region"), desc="Median yield", leave=False):
        # Skip if the target column is completely null for this region.
        if group[target_col].isnull().all():
            continue

        # Filter the rows to only include harvest years that are in the user provided list.
        mask = group["Harvest Year"].isin(user_years)
        median_yield = group.loc[mask, target_col].mean()

        # Assign the computed median yield to all rows in the current region.
        df.loc[df["Region"] == region, new_col_name] = median_yield

    return df


def compute_lag_yield(
    df, all_seasons_with_yield, forecast_season, number_lag_years, target_col="Yield (tn per ha)"
):
    # For the number of years specified in self.number_lag_years, add the yield of that number of years
    # ago to the dataframe
    # For example, if number_lag_years is 3, then the yield of each year upto 3 years ago will be added
    # to the dataframe
    # The yield of the previous year is already added to the dataframe
    # Ensure 'Harvest Year' is treated as integer for accurate comparisons
    df["Harvest Year"] = df["Harvest Year"].astype(int)

    # Pre-allocate all lag columns with NaN so the inner loop writes to
    # existing columns instead of triggering a frame.insert each time —
    # avoids pandas PerformanceWarning about a fragmented DataFrame.
    for idx in range(number_lag_years):
        col = f"t -{idx + 1} {target_col}"
        if col not in df.columns:
            df[col] = np.nan

    for region, group in _pbar(df.groupby("Region"), desc="Lag yields", leave=False):
        unique_years = group["Harvest Year"].unique()

        # Check if the target column is empty for the current group
        if group[target_col].isnull().all():
            continue

        for harvest_year in unique_years:
            closest_years = compute_closest_years(
                all_seasons_with_yield, harvest_year, number_lag_years, only_historic=True
            )

            # For each year in the closest years, add the yield to the dataframe as a new column
            for idx, year in enumerate(closest_years):
                col = f"t -{idx + 1} {target_col}"

                mask_group_year = group["Harvest Year"] == year
                mask_region = (df["Region"] == region) & (
                    df["Harvest Year"] == harvest_year
                )
                yield_value = group.loc[mask_group_year, target_col].values

                if yield_value.size > 0:
                    df.loc[mask_region, col] = yield_value[0]
                else:
                    # Add median yield
                    mask_group_median = group["Harvest Year"].isin(closest_years)
                    median_yield = group.loc[mask_group_median, target_col].mean()

                    df.loc[mask_region, col] = median_yield

    return df


def compute_analogous_yield(
    df,
    all_seasons_with_yield,
    number_lag_years,
    target_col="Yield (tn per ha)",
    var="ESI4WK",
):
    """
    Computes and adds analogous year and its yield based on the similarity of environmental conditions.

    Args:
        df (pd.DataFrame): Input dataframe with yield and environmental data.
        all_seasons_with_yield (array-like): List of seasons that have yield data.
        number_lag_years (int): Number of years to consider for finding analogous years.
        target_col (str): The column name to use for yield data.
        var (str): The environmental variable prefix to find similarity.

    Returns:
        pd.DataFrame: The dataframe with added columns for analogous year and its yield.
    """
    from sklearn.metrics import root_mean_squared_error

    # Determine relevant columns based on the environmental variable
    if "ESI4WK" in var:
        var_columns = [col for col in df.columns if var in col]
    else:
        var_columns = [col for col in df.columns if "ESI" not in col]

    # Early exit if only one variable column is found
    if len(var_columns) == 1:
        df["Analogous Year"] = np.nan
        df["Analogous Year Yield"] = df[f"Median {target_col}"]
        return df

    # Initialize the new columns to NaN
    df["Analogous Year"] = np.nan
    df["Analogous Year Yield"] = np.nan

    all_years = df["Harvest Year"].unique()

    for harvest_year in _pbar(all_years, desc="Computing analogous yields", leave=False):
        lag_years = compute_closest_years(
            all_seasons_with_yield, harvest_year, number_lag_years
        )

        for region in df["Region"].unique():
            # Filter current year and region dataset
            df_current = df[
                (df["Harvest Year"] == harvest_year) & (df["Region"] == region)
            ]
            # Filter dataset for lag years and the same region
            df_lag = df[(df["Harvest Year"].isin(lag_years)) & (df["Region"] == region)]

            if df_current.empty or df_lag.empty:
                continue  # Skip if no data available for comparison

            # Calculate RMSE between the current year's profile and each of the lag years' profiles
            min_rmse, analogous_year, analogous_yield = np.inf, np.nan, np.nan
            for _, row_current in df_current.iterrows():
                for _, row_lag in df_lag.iterrows():
                    # Remove NaNs from both row_current and row_lag
                    arr1 = row_current[var_columns]
                    arr2 = row_lag[var_columns]

                    # Identify the positions where array1 is not NaN
                    not_nan_indices = ~np.isnan(arr1.astype("float").values)

                    # Remove NaNs from array1 and corresponding elements from array2
                    arr1 = arr1[not_nan_indices]
                    arr2 = arr2[not_nan_indices]

                    try:
                        rmse = root_mean_squared_error(arr1, arr2)
                    except (ValueError, TypeError):
                        continue
                    if rmse < min_rmse:
                        min_rmse = rmse
                        analogous_year = row_lag["Harvest Year"]
                        analogous_yield = row_lag[target_col]

            # Update the DataFrame with the found analogous year and yield
            mask = (df["Region"] == region) & (df["Harvest Year"] == harvest_year)
            df.loc[mask, "Analogous Year"] = analogous_year
            df.loc[mask, "Analogous Year Yield"] = (
                analogous_yield
                if not np.isnan(analogous_yield)
                else df.loc[mask, f"Median {target_col}"]
            )

    return df


def find_optimal_kmeans(feature_matrix, max_clusters=15, random_state=42):
    """Find optimal K-Means clustering using the elbow method.

    Args:
        feature_matrix: DataFrame or 2D array where rows are samples and
            columns are features. NaN/inf values should be handled before
            calling this function.
        max_clusters: Upper bound on cluster count (clamped to n_samples - 1).
        random_state: Reproducibility seed.

    Returns:
        (labels, optimal_k, inertias): Cluster labels array, chosen k, and
        list of inertia values for each k tested.
    """
    os.environ["OMP_NUM_THREADS"] = "1"

    import warnings
    warnings.filterwarnings("ignore")

    from kneed import KneeLocator
    from sklearn.cluster import KMeans

    n_samples = len(feature_matrix)
    if n_samples < 2:
        # Not enough samples to cluster — assign all to cluster 0
        labels = np.zeros(n_samples, dtype=int)
        return labels, 1, []

    k_range = range(1, min(max_clusters, n_samples))

    inertias = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state)
        km.fit(feature_matrix)
        inertias.append(km.inertia_)

    if len(inertias) < 2:
        # Only one k tested — no elbow to find
        km_single = KMeans(n_clusters=1, random_state=random_state)
        km_single.fit(feature_matrix)
        return km_single.labels_, 1, inertias

    knee = KneeLocator(
        k_range, inertias, curve="convex", direction="decreasing"
    )

    optimal_k = knee.knee
    if optimal_k and optimal_k > 1:
        optimal_k += 1

    if not optimal_k:
        optimal_k = 1

    km_final = KMeans(n_clusters=optimal_k, random_state=random_state)
    km_final.fit(feature_matrix)

    return km_final.labels_, optimal_k, inertias


def detect_clusters(df, target_col="Yield (tn per ha)"):
    """Cluster regions by their yield patterns across years.

    Args:
        df: DataFrame with columns "Region", "Harvest Year", and target_col.
        target_col: Column name for the target variable.

    Returns:
        DataFrame with columns ["Region", "Region_ID"] mapping each region
        to its cluster assignment.
    """
    df_yield = df[["Region", "Harvest Year", target_col]].dropna()

    df_pivot = df_yield.pivot_table(
        index="Region", columns="Harvest Year", values=target_col, aggfunc="mean",
    )

    if df_pivot.empty:
        regions = df_yield["Region"].unique()
        return pd.DataFrame({"Region": regions, "Region_ID": 0})

    # Fill NaNs with row median, then column median
    df_pivot = df_pivot.apply(lambda row: row.fillna(row.median()), axis=1)
    df_pivot = df_pivot.replace([np.inf, -np.inf], np.nan)
    df_pivot = df_pivot.fillna(df_pivot.median())

    labels, _, _ = find_optimal_kmeans(df_pivot)

    return pd.DataFrame({"Region": df_pivot.index, "Region_ID": labels})


def classify_target(df, target_col, number_classes):
    """

    Args:
        df:
        target_col:
        number_classes:

    Returns:

    """
    new_target_col = f"{target_col}_class"

    # Change the target column to categorical with the specified number of classes
    df[new_target_col], bins = pd.qcut(df[target_col],
                                       q=number_classes,
                                       labels=False,
                                       retbins=True,
                                       duplicates='drop')

    return df, new_target_col, bins


