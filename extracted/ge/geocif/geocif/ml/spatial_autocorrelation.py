import warnings

from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
from pysal.lib import weights

warnings.filterwarnings("ignore")


def validate_inputs(df_results, required_columns):
    """

    Args:
        df_results:
        required_columns:

    Returns:

    """
    if not all(column in df_results.columns for column in required_columns):
        raise ValueError(
            f"df_results must contain the following columns: {required_columns}"
        )


def preprocess_data(df_results, dg_country):
    """

    Args:
        df_results:
        dg_country:

    Returns:

    """
    df = df_results.drop_duplicates()
    df = df.dropna(subset=["Yield (tn per ha)"])

    dg_country = dg_country.drop_duplicates(subset="Country Region")
    dg_country = dg_country.dropna(subset=["Country Region", "Region_ID", "geometry"])

    df["Country Region"] = (df["Country"] + " " + df["Region"]).str.lower()
    dg_country["Country Region"] = dg_country["Country Region"].str.lower()
    dg_country = dg_country[dg_country["Country Region"].isin(df["Country Region"])]

    dg_country.reset_index(drop=True, inplace=True)

    merged_df = dg_country.merge(df, on="Country Region", how="inner")

    return merged_df


def create_base_weights(merged_df):
    """

    Args:
        merged_df:

    Returns:

    """
    dg = merged_df[["Country Region", "geometry"]].drop_duplicates()

    try:
        w_base = weights.Queen.from_dataframe(dg)
    except Exception as e:
        raise RuntimeError(f"Failed to create spatial weights: {e}")

    no_neighbors = [
        index for index, neighbors in w_base.neighbors.items() if len(neighbors) == 0
    ]
    if no_neighbors:
        dg = dg.drop(index=no_neighbors[0]).reset_index(drop=True)
        w_base = weights.Queen.from_dataframe(dg[["Country Region", "geometry"]])

    return w_base, dg


def create_weights_for_year(dg_country, regions_with_data, year):
    """

    Args:
        dg_country:
        regions_with_data:

    Returns:

    """
    dg = dg_country[dg_country["Country Region"].isin(regions_with_data)]
    dg = dg.reset_index(drop=True)

    wt = weights.Queen.from_dataframe(dg)

    no_neighbors = [
        index for index, neighbors in wt.neighbors.items() if len(neighbors) == 0
    ]
    if no_neighbors:
        dg = dg.drop(index=no_neighbors[0]).reset_index(drop=True)
        wt = weights.Queen.from_dataframe(dg[["Country Region", "geometry"]])

    return wt, dg


def compute_morans_i(merged_df):
    """

    Args:
        merged_df:
        dg_country:

    Returns:

    """
    from pysal.explore import esda

    # Drop any regions with missing data
    merged_df = merged_df.dropna(subset=["Yield (tn per ha)"])

    years = merged_df["Harvest Year"].unique()
    results = {"Harvest Year": [], "Moran's I": [], "p-value": [], "Significant": []}

    for year in tqdm(years, desc="Compute Moran's I"):
        year_data = merged_df[merged_df["Harvest Year"] == year]
        regions_with_data = year_data["Country Region"].unique()
        if len(regions_with_data) < 3:
            continue
        year_data = year_data[year_data["Country Region"].isin(regions_with_data)]

        y = year_data[
            ["Country Region", "Region", "Yield (tn per ha)"]
        ].drop_duplicates()
        dg_country = year_data[["Country Region", "geometry"]].drop_duplicates()

        w, x = create_weights_for_year(dg_country, regions_with_data, year)
        y = y[y["Country Region"].isin(x["Country Region"])]
        if len(y) > 1:
            try:
                mi = esda.Moran(y["Yield (tn per ha)"].values, w, permutations=999)
            except:
                breakpoint()
            results["Harvest Year"].append(year)
            try:
                results["Moran's I"].append(mi.I)
            except:
                breakpoint()
            results["p-value"].append(mi.p_sim)
            results["Significant"].append(mi.p_sim < 0.1)
        else:
            results["Harvest Year"].append(year)
            results["Moran's I"].append(None)
            results["p-value"].append(None)
            results["Significant"].append(False)

    return pd.DataFrame(results)


def plot_morans_i_time_series(results_df, country, crop, dir_output):
    """

    Args:
        results_df:
        country:
        crop:
        dir_output:

    Returns:

    """
    plt.figure(figsize=(10, 6))

    significant = results_df[results_df["Significant"]]
    plt.scatter(
        significant["Harvest Year"],
        significant["Moran's I"],
        color="red",
        label="Significant (p < 0.1)",
    )

    not_significant = results_df[~results_df["Significant"]]
    plt.plot(
        not_significant["Harvest Year"],
        not_significant["Moran's I"],
        marker="o",
        linestyle="-",
        color="blue",
        label="Non-Significant",
    )

    plt.ylabel("Moran's I")
    plt.legend()
    plt.grid(True)
    plt.savefig(dir_output / f"{country}_{crop}.png")
    plt.close()


def compute_spatial_autocorrelation(df_results, **kwargs):
    """

    Args:
        df_results:
        **kwargs:

    Returns:

    """
    country = kwargs.get("country")
    crop = kwargs.get("crop")
    dg_country = kwargs.get("dg_country")
    dir_output = kwargs.get("dir_output")

    required_columns = [
        "Country",
        "Crop",
        "Region",
        "Harvest Year",
        "Yield (tn per ha)",
    ]
    validate_inputs(df_results, required_columns)

    merged_df = preprocess_data(df_results, dg_country)
    if merged_df.empty:
        raise ValueError("No valid data available after preprocessing")

    results_df = compute_morans_i(merged_df)

    plot_morans_i_time_series(results_df, country, crop, dir_output)
