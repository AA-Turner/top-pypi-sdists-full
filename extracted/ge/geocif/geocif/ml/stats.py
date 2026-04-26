import os
import numpy as np
import pandas as pd
from tqdm.rich import tqdm


def get_yld_prd(df, name_crop, cntr, region, calendar_year, region_column="ADM1_NAME"):
    """
    Example input: ('United States of America', 'Wyoming', 2000)
    Example output: 1.614
    Args:
        df:
        cntr:
        region:
        calendar_year:

    Returns:

    """
    # Get yield and production for country for specific year
    val = np.nan

    # Resolve year column key: Excel files may have int columns, CSVs may have string columns
    year_str = str(calendar_year)
    if year_str in df.columns:
        year_col = year_str
    elif calendar_year in df.columns:
        year_col = calendar_year
    else:
        year_col = None

    # df.columns.values: [u'ADM0_NAME', u'ADM1_NAME', u'ADM2_NAME', u'str_ID', u'num_ID', 1990 ... 2015]
    if year_col is not None:
        # Find if country and region exists in calendar
        df_tmp = df.copy()
        
        if name_crop == "rice":
            if cntr == "Viet nam":
                df_tmp = df.loc[df.Season == "Spring Paddy"]
            elif cntr == "Thailand":
                df_tmp = df.loc[df.Season == "Major Season"]
            elif cntr == "China":
                df_tmp = df.loc[df.Season == "Single-cropping and Middle-season Rice"]
            elif cntr == "India":
                df_tmp = df.loc[df.Season == "Kharif"]
            elif cntr == "Bangladesh":  # HACK for Bangladesh rice
                df_tmp = df.loc[df.Season == "Boro"]
        elif name_crop == "maize" and cntr in [
            "Austria",
            "Belgium",
            "Bulgaria",
            "Croatia",
            "Czech  Republic",
            "Denmark",
            "Germany",
            "Greece",
            "Hungary",
            "Italy",
            "Lithuania",
            "Luxembourg",
            "Netherlands",
            "Poland",
            "Portugal",
            "Romania",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden",
            "United Kingdom",
        ]:
            df_tmp = df.loc[df.Season == "Grain Maize and Corn-cob-mix"]
        elif name_crop == "maize" and cntr in ["France"]:
            df_tmp = df.loc[df.Season == "Green Maize"]

        if not df_tmp.empty:
            if cntr != "Vietnam":
                mask_tmp_country = (
                    df_tmp["ADM0_NAME"].str.lower() == cntr.replace("_", " ").lower()
                )
            else:
                mask_tmp_country = df_tmp["ADM0_NAME"].str.lower() == "viet nam"
            if region:
                mask_tmp_adm1 = df_tmp[region_column].str.lower() == region.lower()
            else:
                # ADM1_NAME column should be NaN to get country level stats
                mask_tmp_adm1 = df_tmp[region_column].isnull()

            # CM_Season should be 1 for the Main season
            # TODO: Make this user specified
            if "CM_Season" in df_tmp.columns:
                mask_cm_season = df_tmp["CM_Season"] == 1
                val = df_tmp.loc[mask_tmp_country & mask_tmp_adm1 & mask_cm_season][year_col]
            else:
                val = df_tmp.loc[mask_tmp_country & mask_tmp_adm1][year_col]

            try:
                if val.isnull().all():
                    val = np.nan
                else:
                    val = val.values[0]
            except (IndexError, KeyError, AttributeError):
                val = np.nan

        else:
            # The values[-1] is a hack to accommodate multiple types of green maize
            vals = df[year_col]
            val = vals.values[-1] if not vals.empty else np.nan

    # Replace yield/production value of 0 with NaN
    val = np.nan if val == 0.0 else val

    return val


def add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone, crop=None, country=None):
    """

    Args:
        dir_stats:
        df:
        stats:
        method:
        admin_zone:

    Returns:

    """
    # Create empty columns for all the ag statistics
    for stat in stats:
        df.loc[:, stat] = np.nan

    # Fill in the ag statistics columns with data when available
    # Compute national scale statistics

    if crop is None:
        crop = df["Crop"].unique()[0]
    # Change crop to lower case and replace space by _
    crop = crop.lower().replace(" ", "_")
    season = df["Season"].unique()[0]

    # Read in the area stats for the crop and season
    # HACK: Bangladesh rice uses country-specific filename
    if country is None:
        country = df["Country"].unique()[0]
    if crop == "rice" and country.lower() == "bangladesh":
        stat_file = dir_stats / "bangladesh_rice.xlsx"
    else:
        stat_file = dir_stats / f"{crop}_{season}.xlsx"

    for stat in stats:
        if os.path.isfile(stat_file):
            df_stat = pd.read_excel(stat_file, sheet_name=stat)
        else:
            continue

        # Loop over each Country, Region, harvest year combination and add the area
        grp = df.groupby(["Region", "Harvest Year"], dropna=False)
        for key, group in tqdm(grp, desc=f"Adding {stat} {method}", leave=False):
            region, year = key

            df_adm0 = pd.DataFrame()
            if not df_stat.empty:
                tmp = df_stat["ADM0_NAME"].str.lower()
                if country != "vietnam":  # Hack alert
                    mask_country = tmp == country.replace("_", " ").lower()
                else:
                    mask_country = tmp == "viet nam"
                df_adm0 = df_stat.loc[mask_country]

            if df_adm0.empty:
                continue

            # Get the statistic for the country and year
            region_column = "ADM2_NAME" if admin_zone == "admin_2" else "ADM1_NAME"
            val = get_yld_prd(
                df_adm0,
                crop,  # maize
                cntr=country,  # Brazil
                region=region,  # Mato Grasso
                calendar_year=year,
                region_column=region_column,
            )

            # Add the statistic to the dataframe
            df.loc[group.index, stat] = val

    return df


def add_statistics(
    dir_stats,
    df,
    country,
    crop,
    admin_zone,
    stats,
    method,
    target_col="Yield (tn per ha)",
    parser=None,
    label="",
):
    """

    Args:
        df:
        country:
        crop:
        admin_zone:
        stats:
        method:
        target_col:

    Returns:

    """
    # HACK: Bangladesh rice uses GEOGLAM format
    if country == "Bangladesh" and crop == "Rice":
        df = add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone, crop=crop, country=country)
        # Add columns for obj.stats_cols
        for col in ["Area"]:
            df.loc[:, col] = np.nan
        return df
    
    # Read hvstat filename: per-country override → DEFAULT override → hardcoded default
    default_fn = "hvstat_africa_data_v1.0.csv"
    if parser is not None:
        country_key = country.lower().replace(" ", "_")
        if parser.has_option(country_key, "production_statistics_file"):
            default_fn = parser.get(country_key, "production_statistics_file")
        elif parser.has_option("DEFAULT", "production_statistics_file"):
            default_fn = parser.get("DEFAULT", "production_statistics_file")

    if country == "Illinois":
        fn = "illinois.csv"
    else:
        fn = default_fn
    df_fewsnet = pd.read_csv(dir_stats / fn, low_memory=False)
    # HACK
    #if country == "Afghanistan":
    #    df_fewsnet.loc[:, "product"] = (
    #        df_fewsnet["season_name"] + " " + df_fewsnet["product"]
    #    )

    # Hack replace Wheat in product column in df_fewsnet with Winter Wheat
    if "product" in df_fewsnet.columns:
        df_fewsnet.loc[:, "product"] = df_fewsnet["product"].replace("Wheat", "Winter Wheat")

    # Check if country and crop exist in the fewsnet database
    mask = (df_fewsnet["country"] == country) & (df_fewsnet["product"] == crop)

    # If qc_flag column exists, filter out rows with qc_flag != 0
    if "qc_flag" in df_fewsnet.columns:
        df_fewsnet = df_fewsnet[df_fewsnet["qc_flag"] == 0]

    if mask.sum() == 0:
        df = add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone, crop=crop, country=country)
    else:
        from geocif.utils import PRIMARY_SEASON_NAMES, SECONDARY_SEASON_NAMES

        # Determine which season_names exist for this country/crop
        country_crop_mask = (df_fewsnet["country"] == country) & (df_fewsnet["product"] == crop)
        available_seasons = set(df_fewsnet.loc[country_crop_mask, "season_name"].unique())

        def _resolve_season_filter(season_num):
            """Pick the hvstat season_name for a given CID season number."""
            if season_num == 1:
                for name in PRIMARY_SEASON_NAMES:
                    if name in available_seasons:
                        return [name]
            elif season_num == 2:
                for name in SECONDARY_SEASON_NAMES:
                    if name in available_seasons:
                        return [name]
            # Fallback: use "Annual" only if no seasonal match was found
            if "Annual" in available_seasons:
                return ["Annual"]
            return []

        # Group by Season too if the column exists
        group_by = ["Region", "Harvest Year"]
        has_season = "Season" in df.columns
        if has_season:
            group_by.append("Season")

        # Pre-compute the season filter for each season number ONCE,
        # so ALL regions use the same season_name consistently.
        season_filters = {}
        if has_season:
            for s in df["Season"].unique():
                season_filters[s] = _resolve_season_filter(s)
        else:
            season_filters[None] = _resolve_season_filter(1)

        groups = df.groupby(group_by)

        # Define processing for each group
        def process_group(group, region, harvest_year, season=None):
            season_filter = season_filters.get(season, season_filters.get(None, []))

            # Case-insensitive region matching (normalize underscores to spaces
            # because geoprepare extraction converts spaces to underscores)
            mask_region = df_fewsnet[admin_zone].str.lower().str.replace("_", " ") == region.lower().replace("_", " ")
            mask_yield = (
                df_fewsnet["crop_production_system"].isin(
                    [
                        "none",
                        "Small-scale (PS)",
                        "Commercial (PS)",
                        "All (PS)",
                        "irrigated",
                        "rainfed",
                        "Rainfed (PS)",
                        "agro_pastoral",
                        "riverine"
                    ]
                )
                & (df_fewsnet["harvest_year"] == harvest_year)
                & (df_fewsnet["product"] == crop)
                & df_fewsnet["season_name"].isin(season_filter)
            )

            # Fetching values for each statistic
            mask_combined = mask_yield & mask_region

            yield_value = df_fewsnet.loc[mask_combined, "yield"]
            area_value = df_fewsnet.loc[mask_combined, "area"]
            prod_value = df_fewsnet.loc[mask_combined, "production"]

            # Fallback to "Annual" for Malawi Maize when primary season has no data
            if yield_value.empty and country == "Malawi" and crop == "Maize" and "Annual" in available_seasons and "Annual" not in season_filter:
                mask_yield_annual = (
                    df_fewsnet["crop_production_system"].isin(
                        [
                            "none",
                            "Small-scale (PS)",
                            "Commercial (PS)",
                            "All (PS)",
                            "irrigated",
                            "rainfed",
                            "Rainfed (PS)",
                            "agro_pastoral",
                            "riverine"
                        ]
                    )
                    & (df_fewsnet["harvest_year"] == harvest_year)
                    & (df_fewsnet["product"] == crop)
                    & (df_fewsnet["season_name"] == "Annual")
                )
                mask_combined = mask_yield_annual & mask_region
                yield_value = df_fewsnet.loc[mask_combined, "yield"]
                area_value = df_fewsnet.loc[mask_combined, "area"]
                prod_value = df_fewsnet.loc[mask_combined, "production"]

            # Replace any inf or 0 values by NaN
            yield_value = yield_value.replace([0, np.inf, -np.inf], np.nan)
            area_value = area_value.replace([0, np.inf, -np.inf], np.nan)
            prod_value = prod_value.replace([0, np.inf, -np.inf], np.nan)

            if not yield_value.empty:
                group.loc[:, target_col] = yield_value.values[0]
                group.loc[:, "Area (ha)"] = area_value.values[0]
                group.loc[:, "Production (tn)"] = prod_value.values[0]

            return group

        # Process each group with a progress bar
        results = []
        stats_desc = f"Adding yield/area/production stats ({label})" if label else "Adding yield/area/production stats"
        for keys, group in tqdm(
            groups, total=len(groups), desc=stats_desc, leave=False
        ):
            if has_season:
                region, harvest_year, season = keys
            else:
                region, harvest_year = keys
                season = None
            processed_group = process_group(group.copy(), region, harvest_year, season)
            results.append(processed_group)

        df = pd.concat(results)

    # Add columns for obj.stats_cols
    for col in ["Area"]:
        df.loc[:, col] = np.nan

    return df