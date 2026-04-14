import os
import pandas as pd
from tqdm.rich import tqdm
import matplotlib.pyplot as plt
import Rbeast as rb

import always
import Code.base.constants as cc

BASE_DIR = cc.dir_yld


def find_outlier(df):
    """

    Args:
        df:

    Returns:

    """
    # Loop over country, admin_1, product, season_name, crop_production_system, indicator
    # For each group, get the yield, area, and production values
    # Compute z-scores for yield, area, and production
    # Add z-scores to the dataframe
    # Save the dataframe to a csv file
    group_by = [
        "country",
        "admin_1",
        "product",
        "season_name",
        "crop_production_system",
        "indicator",
    ]
    groups = df.groupby(group_by)

    for key, group in tqdm(groups):
        country, admin_1, product, season_name, crop_production_system, indicator = key

        if indicator != "yield":
            continue

        mask = (
            (df["country"] == country)
            & (df["admin_1"] == admin_1)
            & (df["product"] == product)
            & (df["season_name"] == season_name)
            & (df["crop_production_system"] == crop_production_system)
        )
        if len(group) < 5:
            continue
        # if len(group) > 5:
        #     breakpoint()
        #     # See https://github.com/hamiddashti/greeness/blob/main/codes/src/11_plotting.ipynb
        #     o = rb.beast(
        #         group["value"], start=int(group["harvest_year"].iloc[0]), season="none"
        #     )
        #     rb.plot(o)
        #     breakpoint()
        mask_yield = mask & (df["indicator"] == "yield")
        # mask_area = mask & (df["indicator"] == "area")
        # mask_production = mask & (df["indicator"] == "production")

        yield_info = df[mask_yield]["value"]
        # area_info = df[mask_area]["value"]
        # production_info = df[mask_production]["value"]

        # Compute z-score based on a 5-year rolling window, centered on the current year
        yield_z = (
            yield_info - yield_info.rolling(7, min_periods=3, center=True).mean()
        ) / yield_info.rolling(7, min_periods=3, center=True).std()
        # area_z = (area_info - area_info.rolling(5).mean()) / area_info.rolling(5).std()
        # production_z = (production_info - production_info.rolling(5).mean()) / production_info.rolling(5).std()

        # Add z-scores to the dataframe
        df.loc[mask_yield, "yield_z"] = yield_z
        # df.loc[mask_area, "value"] = area_z
        # df.loc[mask_production, "value"] = production_z

    return df


if __name__ == "__main__":
    crops = ["Wheat", "Sorghum", "Rice", "Barley", "Millet", "Fonio", "Maize"]
    df_fewsnet = pd.read_csv(cc.dir_yld / "hvstat_data.csv")
    # Subset to following product: Wheat, Sorghum, Rice, Barley, Millet, Fonio
    df_fewsnet = df_fewsnet[df_fewsnet["product"].isin(crops)]
    # Only use QC_flag == 0
    df_fewsnet = df_fewsnet[df_fewsnet["QC_flag"] == 0]

    for crop in crops:
        os.makedirs(BASE_DIR / crop, exist_ok=True)
        df_fewsnet_sub = df_fewsnet[df_fewsnet["product"] == crop]

        if not os.path.isfile(BASE_DIR / crop / f"adm_crop_production_z_{crop}.csv"):
            # In rows where admin_2 != "none", replace admin_1 with admin_2
            df_fewsnet_sub.loc[
                df_fewsnet_sub["admin_2"] != "none", "admin_1"
            ] = df_fewsnet_sub["admin_2"]

            df_output = find_outlier(df_fewsnet_sub)

            df_output.to_csv(
                BASE_DIR / crop / f"adm_crop_production_z_{crop}.csv", index=False
            )
        else:
            df_output = pd.read_csv(
                BASE_DIR / crop / f"adm_crop_production_z_{crop}.csv"
            )

        df_fewsnet_sub.loc[
            df_fewsnet_sub["admin_2"] != "none", "admin_1"
        ] = df_fewsnet_sub["admin_2"]

        # Create a column called Z-Score Category based on the value of the z-score
        # The categories are:
        # < -2 : Extremely Low
        # -2 to -1: Very Low
        # -1 to 0: Low
        # 0 to 1: Average
        # 1 to 2: High
        # > 2: Very High
        df_output["Z-Score Category"] = pd.cut(
            df_output["yield_z"],
            bins=[-float("inf"), -2.0, -0.5, 0.5, 2.0, float("inf")],
            labels=["Extremely Low", "Very Low", "Average", "High", "Very High"],
        )

        # Subset df_output to Very High only
        df_output_high = df_output[df_output["Z-Score Category"] == "Very High"]
        # Get yield data from df_fewsnet for the "country", "admin_1", "product", "season_name", "crop_production_system", "indicator" in df_output_high
        groups = ["country", "admin_1", "season_name", "crop_production_system"]
        # groupby groups
        # for each group, plot the yield data
        # Save the plot to a file
        for key, group in df_output_high.groupby(groups):
            country, admin_1, season_name, crop_production_system = key
            mask = (
                (df_fewsnet_sub["country"] == country)
                & (df_fewsnet_sub["admin_1"] == admin_1)
                & (df_fewsnet_sub["product"] == crop)
                & (df_fewsnet_sub["season_name"] == season_name)
                & (df_fewsnet_sub["crop_production_system"] == crop_production_system)
            )
            # convert harvest_year column in df_fewsnet to int
            df_fewsnet_sub["harvest_year"] = df_fewsnet_sub["harvest_year"].astype(int)

            df_yield = df_fewsnet_sub[mask & (df_fewsnet_sub["indicator"] == "yield")]
            df_production = df_fewsnet_sub[
                mask & (df_fewsnet_sub["indicator"] == "production")
            ]
            df_area = df_fewsnet_sub[mask & (df_fewsnet_sub["indicator"] == "area")]

            df_yield["harvest_year"] = df_yield["harvest_year"].astype(int)
            df_production["harvest_year"] = df_production["harvest_year"].astype(int)
            df_area["harvest_year"] = df_area["harvest_year"].astype(int)

            if df_yield[mask].empty:
                continue

            outlier_year = int(group["harvest_year"].values[0])
            fnid = group["fnid"].values[0]

            # Add 3 subplots, first for area
            plt.figure(figsize=(10, 10))
            plt.subplot(3, 1, 1)
            plt.plot(
                df_yield[mask]["harvest_year"].astype(int), df_yield[mask]["value"]
            )
            # Add a circle for each year where yield is available
            plt.scatter(
                df_yield[mask]["harvest_year"].astype(int), df_yield[mask]["value"]
            )
            # Draw a horizontal line at the average df_yield[mask]["value"]
            plt.axhline(df_yield[mask]["value"].mean(), color="red", linestyle="--")
            # Place a tick on x-axis at every year and make labels vertical
            plt.xticks(df_yield[mask]["harvest_year"].astype(int)[::2], rotation=90)
            # Draw a * at the outlier year
            try:
                plt.scatter(
                    outlier_year,
                    df_yield[mask]["value"]
                    .loc[df_yield[mask]["harvest_year"] == outlier_year]
                    .values[0],
                    color="red",
                    marker="*",
                )
            except:
                breakpoint()
            plt.title(
                f"{country}, {admin_1}, {crop}, {season_name}, {crop_production_system}, yield"
                f"\nFNID: {fnid} \nOutlier Year: {outlier_year}"
            )
            plt.xlabel("Year")
            plt.ylabel("Yield")

            # Add subplot for production and area
            plt.subplot(3, 1, 2)
            plt.plot(
                df_production[mask]["harvest_year"].astype(int),
                df_production[mask]["value"],
            )
            plt.scatter(
                df_production[mask]["harvest_year"].astype(int),
                df_production[mask]["value"],
            )
            # Place a tick on x-axis at every year
            plt.xticks(
                df_production[mask]["harvest_year"].astype(int)[::2], rotation=90
            )
            plt.xlabel("Year")
            plt.ylabel("Production")

            plt.subplot(3, 1, 3)
            plt.plot(df_area[mask]["harvest_year"].astype(int), df_area[mask]["value"])
            plt.scatter(
                df_area[mask]["harvest_year"].astype(int), df_area[mask]["value"]
            )
            # Place a tick on x-axis at every year
            plt.xticks(df_area[mask]["harvest_year"].astype(int)[::2], rotation=90)
            plt.xlabel("Year")
            plt.ylabel("Area")

            try:
                os.makedirs(BASE_DIR / crop, exist_ok=True)
                plt.savefig(
                    BASE_DIR
                    / crop
                    / f"{fnid}_{country}_{admin_1}_{crop}_{season_name}.png"
                )
            except:
                breakpoint()
            plt.tight_layout()
            plt.close()

    # drop rows where yield_z is NaN
    df_output = df_output.dropna(subset=["yield_z"])
    df_output.to_csv(BASE_DIR / "adm_crop_production_z.csv", index=False)

    # Create a histogram of the Z-Score Category
    # Order the x-axis as "Extremely Low", "Very Low", "Average", "High", "Very High"
    df_output["Z-Score Category"].value_counts().loc[
        ["Extremely Low", "Very Low", "Average", "High", "Very High"]
    ].plot(kind="bar")

    # Make the y-axis log scale
    plt.yscale("log")
    plt.title("Z-Score Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Yield Observations (Maize)")
    plt.tight_layout()
    # Save the histogram to a file
    plt.savefig(BASE_DIR / "Z-Score_Yield_Category.png")
    plt.close()
