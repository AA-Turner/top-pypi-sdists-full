import os
import numpy as np
import pandas as pd
from geocif.progress import pbar as _pbar


# Canonical production-system whitelist used by HvStat Africa data
# (geocif/ml/stats.py:add_statistics and production_analysis/_common.py:
# load_filtered_hvstat both filter to these labels). The HvStat CSV
# carries 27 unique PS values across all countries; the 17 not listed
# here are non-standard / project-specific and excluded as noise.
# Tuple so it's immutable at import time.
STANDARD_PRODUCTION_SYSTEMS = (
    "none",
    "Small-scale (PS)",
    "Commercial (PS)",
    "Communal (PS)",
    "All (PS)",
    "irrigated",
    "rainfed",
    "Rainfed (PS)",
    "agro_pastoral",
    "riverine",
)


# Region-name synonym map — applied AFTER normalize (lower / underscore→
# space / strip period) to bridge convention drift between the boundary
# shapefile (which the sweep reads) and AMIS yield files. Keyed by the
# canonical country name. Values map any one form to the same target
# form; the resolver applies it to BOTH sides of the comparison so the
# direction of disagreement doesn't matter.
#
# India entries trace to two causes (Jun 7 2026 audit):
#   * Stale shapefile: Level_1.shp still has pre-2011 "Orissa" and
#     pre-2007 "Uttaranchal" instead of "Odisha" / "Uttarakhand".
#   * Convention drift: AMIS abbreviates "Dadra and Nagar Haveli" as
#     "D & N Haveli", spells Chhattisgarh with one t, and uses "Delhi"
#     where the shapefile has "New Delhi".
# Without these synonyms the boundary→AMIS join silently produced NaN
# for these regions; with them, India maize coverage goes from 26/31
# (84%) to 31/31 (100%) over AMIS-listed Indian states.
_REGION_SYNONYMS = {
    "India": {
        # sweep slug (normalized)     : AMIS form (normalized)
        "orissa":                       "odisha",
        "uttaranchal":                  "uttarakhand",
        "chhattisgarh":                 "chattisgarh",
        "new delhi":                    "delhi",
        "dadra and nagar haveli":       "d & n haveli",
    },
}


def _canonicalize_region(region_norm, country):
    """Map a normalized region name to its canonical form for the given
    country. Returns the input unchanged when no synonym applies.
    Country lookup is exact (post-normalization callers pass the same
    string into _REGION_SYNONYMS as the keys here)."""
    return _REGION_SYNONYMS.get(country, {}).get(region_norm, region_norm)


def aggregate_yield_across_ps(yield_values, area_values, prod_values):
    """Area-weighted aggregation across multiple production-system rows
    for one (region, year) combo.

    When a (country, admin, crop, season, year) appears in HvStat under
    multiple whitelisted PS labels (e.g. ``Rainfed (PS)`` + ``irrigated``
    for the same district), this collapses them into a single yield via
    total_production / total_area so each system contributes
    proportionally to its area.

    Returns ``(agg_yield, total_area, total_prod)`` — all NaN-safe
    scalars. ``area`` and ``prod`` use ``sum(skipna=True)``; the yield
    falls back through three branches: prod/area when both are positive;
    area-weighted yield mean when only area is positive; plain mean as
    last resort.

    Used by both ``add_statistics`` (per-(region, year) join groups) and
    ``production_analysis._common.load_filtered_hvstat`` (per-series
    groupby) so the PS aggregation logic lives in one place.
    """
    yield_values = yield_values.replace([0, np.inf, -np.inf], np.nan)
    area_values = area_values.replace([0, np.inf, -np.inf], np.nan)
    prod_values = prod_values.replace([0, np.inf, -np.inf], np.nan)
    total_area = area_values.sum(skipna=True)
    total_prod = prod_values.sum(skipna=True)
    if total_area and total_area > 0 and total_prod and total_prod > 0:
        agg_yield = total_prod / total_area
    elif total_area and total_area > 0 and yield_values.notna().any():
        agg_yield = (
            (yield_values.fillna(0) * area_values.fillna(0)).sum()
            / total_area
        )
    else:
        agg_yield = yield_values.mean(skipna=True)
    return agg_yield, total_area, total_prod


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
                # Normalize slug-vs-canonical asymmetry between callers:
                # extract_sweep writes region names as lowercase + underscore
                # ("andhra_pradesh", "district_of_columbia") while AMIS stores
                # canonical Title-Case with spaces ("Andhra Pradesh",
                # "District of Columbia"). The old comparison lowercased both
                # sides but kept underscores on the lhs and spaces on the rhs,
                # so multi-word region names (most of India's admin1, USA
                # multi-word states, etc.) never matched and yielded NaN
                # downstream — flagged by the India soybean threshold-sweep
                # audit (Jun 7 2026): every state had n_years=0 / metric=NaN.
                # Single-word states (Iowa, Alabama, Gujarat) passed by
                # coincidence because no underscore existed to mismatch.
                #
                # Also strip periods — AMIS uses trailing-period abbreviations
                # for Russian regions ("Adygeya Rep.", "Bashkortostan Rep.")
                # while the sweep CSV slugifies these to "adygeya_rep" with
                # no period. Lift Russia's Pearson-correlation coverage from
                # ~33% to ~50% (the rest are genuinely Far East regions with
                # no AMIS data).
                def _norm(s):
                    return (
                        str(s).lower().replace("_", " ").replace(".", "").strip()
                        if pd.notna(s) else s
                    )
                # Canonicalize both sides via the country-keyed synonym
                # map so stale-shapefile names ("orissa") and AMIS
                # variants ("odisha") resolve to the same key. Applied
                # post-_norm so both inputs are in the same lowercase /
                # space / no-period space.
                adm1_norm = df_tmp[region_column].map(_norm).map(
                    lambda s: _canonicalize_region(s, cntr)
                )
                region_norm = _canonicalize_region(_norm(region), cntr)
                mask_tmp_adm1 = adm1_norm == region_norm
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


def add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone, crop=None, country=None, label=""):
    """

    Args:
        dir_stats:
        df:
        stats:
        method:
        admin_zone:

    Returns:

    """
    # Empty-df guard: callers (e.g. geocif.threshold_optimizer.join_yield)
    # may hand a 0-row df when upstream produced nothing. The
    # `df.loc[:, stat] = np.nan` assignment below raises ValueError
    # ("cannot set a frame with no defined index and a scalar") on an
    # empty df, AND the `df["Crop"|"Season"].unique()[0]` lines below
    # would IndexError. Return the df untouched — no stats can be added
    # when there are no rows anyway.
    if df.empty:
        for stat in stats:
            if stat not in df.columns:
                df[stat] = pd.Series(dtype=float)
        return df

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
        pbar_desc = (
            f"Adding {stat} {method} ({label})" if label
            else f"Adding {stat} {method}"
        )
        for key, group in _pbar(grp, desc=pbar_desc, leave=False):
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
        df = add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone, crop=crop, country=country, label=label)
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
        df = add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone, crop=crop, country=country, label=label)
    else:
        from geocif.utils import PRIMARY_SEASON_NAMES, SECONDARY_SEASON_NAMES

        # Determine which season_names exist for this country/crop
        country_crop_mask = (df_fewsnet["country"] == country) & (df_fewsnet["product"] == crop)
        available_seasons = set(df_fewsnet.loc[country_crop_mask, "season_name"].unique())

        def _resolve_season_filter(season_num):
            """Pick the hvstat season_name for a given CID season number."""
            # Per-country override: Kenya Maize hvstat uses "Annual" rows;
            # Long/Short are not the canonical season labels for that crop.
            if country == "Kenya" and crop == "Maize" and "Annual" in available_seasons:
                return ["Annual"]
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
                df_fewsnet["crop_production_system"].isin(STANDARD_PRODUCTION_SYSTEMS)
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
                    df_fewsnet["crop_production_system"].isin(STANDARD_PRODUCTION_SYSTEMS)
                    & (df_fewsnet["harvest_year"] == harvest_year)
                    & (df_fewsnet["product"] == crop)
                    & (df_fewsnet["season_name"] == "Annual")
                )
                mask_combined = mask_yield_annual & mask_region
                yield_value = df_fewsnet.loc[mask_combined, "yield"]
                area_value = df_fewsnet.loc[mask_combined, "area"]
                prod_value = df_fewsnet.loc[mask_combined, "production"]

            # df.loc[bool_mask, "col"] always returns a Series here, but
            # the pandas stubs union the return type with scalars — guard
            # via len() with an explicit cast so static checkers and
            # runtime agree.
            yield_series = pd.Series(yield_value)
            if len(yield_series) > 0:
                # Area-weighted aggregation across PS — same logic used by
                # production_analysis._common.load_filtered_hvstat, lifted
                # to aggregate_yield_across_ps so both call sites share it.
                agg_yield, total_area, total_prod = aggregate_yield_across_ps(
                    yield_series,
                    pd.Series(area_value),
                    pd.Series(prod_value),
                )
                group.loc[:, target_col] = agg_yield
                group.loc[:, "Area (ha)"] = total_area if total_area > 0 else np.nan
                group.loc[:, "Production (tn)"] = (
                    total_prod if total_prod > 0 else np.nan
                )

            return group

        # Process each group with a progress bar
        results = []
        stats_desc = f"Adding yield/area/production stats ({label})" if label else "Adding yield/area/production stats"
        for keys, group in _pbar(
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