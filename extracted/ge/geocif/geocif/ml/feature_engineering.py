import os

import numpy as np
import pandas as pd
from tqdm import tqdm


def compute_last_year_yield(df, target_col="Yield (tn per ha)"):
    """
    Computes the yield of the previous year for each region.

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

    for region, group in tqdm(
        df.groupby("Region"), desc="Last year yields", leave=False
    ):
        unique_years = group["Harvest Year"].unique()

        for harvest_year in unique_years:
            mask = (group["Harvest Year"] == harvest_year) & (group["Region"] == region)
            last_year_yield = group.loc[mask, target_col].values
            if last_year_yield.size > 0:
                df.loc[
                    (df["Region"] == region) & (df["Harvest Year"] == harvest_year),
                    f"Last Year {target_col}",
                ] = last_year_yield[0]

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
    df, all_seasons_with_yield, number_median_years, target_col="Yield (tn per ha)"
):
    """
    Enhances the DataFrame with a new column that contains the median yield from the closest lag years.

    Args:
        df (DataFrame): The original DataFrame containing yield data.
        all_seasons_with_yield (array-like): List of seasons that have yield data.
        number_median_years (int): Number of years to consider for computing the median yield.
        target_col (str): The column name from which to compute the median yield.

    Returns:
        DataFrame: The original DataFrame enhanced with a new column for median lag yield.
    """
    # Ensure 'Harvest Year' is treated as integer for accurate comparisons
    df["Harvest Year"] = df["Harvest Year"].astype(int)
    # Initialize the new column with NaNs
    df[f"Median {target_col}"] = np.nan

    for region, group in tqdm(df.groupby("Region"), desc="Median yield", leave=False):
        unique_years = group["Harvest Year"].unique()

        # Check if the target column is empty for the current group
        if group[target_col].isnull().all():
            continue

        for harvest_year in unique_years:
            closest_years = compute_closest_years(
                all_seasons_with_yield, harvest_year, number_median_years
            )
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
    for region, group in tqdm(df.groupby("Region"), desc="Median yield", leave=False):
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

    for region, group in tqdm(df.groupby("Region"), desc="Lag yields", leave=False):
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

    for harvest_year in tqdm(all_years, desc="Computing analogous yields", leave=False):
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


def detect_clusters(df, target_col="Yield (tn per ha)"):
    """

    Args:
        df:
        target_col:

    Returns:

    """
    os.environ["OMP_NUM_THREADS"] = "1"

    # Suppress warnings in this function
    import warnings

    warnings.filterwarnings("ignore")

    from kneed import KneeLocator
    from sklearn.cluster import KMeans

    # Get the yield of each region in df_results
    df_yield = df[["Region", "Harvest Year", target_col]]

    # Drop any columns with missing values
    df_yield = df_yield.dropna()

    # Pivot the DataFrame to have regions as rows and years as columns with their corresponding yields
    df_yield_pivot = df_yield.pivot_table(
        index="Region",
        columns="Harvest Year",
        values=target_col,
        aggfunc="mean",
    )

    # Fill rows with median value of the row
    df_na = df_yield_pivot.median(axis=1)
    # Fill NaNs in df_yield_pivot with value from df_na
    df_yield_pivot = df_yield_pivot.fillna(df_na, axis=0)

    # Fill data with Median values rowwise
    df_yield_pivot = df_yield_pivot.apply(lambda row: row.fillna(row.median()), axis=1)

    # Normalize the data
    # scaler = StandardScaler()
    # df_yield_normalized = scaler.fit_transform(df_yield_pivot)

    # Determine an appropriate number of clusters using the Elbow Method
    inertia = []
    range_of_clusters = range(
        1, len(df_yield_pivot)
    )  # Assuming up to 15 clusters for demonstration

    # Replace inf or NaN values with column median
    df_yield_pivot = df_yield_pivot.replace([np.inf, -np.inf], np.nan)
    df_yield_pivot = df_yield_pivot.fillna(df_yield_pivot.median())
    for n_clusters in range_of_clusters:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        try:
            kmeans.fit(df_yield_pivot)
        except:
            breakpoint()
        inertia.append(kmeans.inertia_)

    # Use KneeLocator to find the elbow point automatically
    knee_locator = KneeLocator(
        range_of_clusters, inertia, curve="convex", direction="decreasing"
    )

    # # Plot the Elbow Method for visual confirmation
    # plt.figure(figsize=(10, 6))
    # plt.plot(range_of_clusters, inertia, marker='o', linestyle='--')
    # plt.title('Elbow Method For Optimal k')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Inertia')
    # plt.xticks(range_of_clusters)
    # plt.vlines(knee_locator.knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
    # plt.show()

    # Use the detected number of clusters
    optimal_clusters = knee_locator.knee
    if optimal_clusters:
        optimal_clusters = (
            optimal_clusters + 1 if optimal_clusters > 1 else optimal_clusters
        )

        # Apply K-Means clustering with the detected optimal number of clusters
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
        kmeans.fit(df_yield_pivot)

        # Assign cluster labels to each region
        cluster_labels = kmeans.labels_

        # Create a DataFrame with region names and their respective cluster IDs
        clusters_assigned = pd.DataFrame(
            {"Region": df_yield_pivot.index, "Region_ID": cluster_labels}
        )
    else:
        # If no optimal_clusters is found, then assign all regions to a single cluster
        clusters_assigned = pd.DataFrame(
            {"Region": df_yield_pivot.index, "Region_ID": 1}
        )

    return clusters_assigned


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


