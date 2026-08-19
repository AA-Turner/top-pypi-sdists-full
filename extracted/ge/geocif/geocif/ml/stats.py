import ast
import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd
from geocif.progress import pbar as _pbar

logger = logging.getLogger(__name__)


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


# Single definition of the region-name matching rule used everywhere a
# production-statistics admin column is compared against a pipeline region:
# case-insensitive, underscores normalized to spaces (geoprepare extraction
# converts spaces to underscores). Scalar + vectorized shapes of the SAME
# rule — keep them in sync.
def _norm_region_name(s) -> str:
    return str(s).lower().replace("_", " ")


def _norm_region_series(s: pd.Series) -> pd.Series:
    return s.astype(str).str.lower().str.replace("_", " ", regex=False)


def parse_run_regions(raw, crop=None, log=None):
    """Parse a ``run_regions`` config value into a list of names, or None.

    Accepts either form::

        run_regions = ["illinois", "iowa"]                 ; all crops
        run_regions = {"maize": ["illinois"], "soybean": [...]}

    Returns None — meaning "no filtering" — when the value is unset,
    unparseable, not a list/dict, or a dict with no entry for ``crop``. A
    malformed value never raises: it is logged and treated as unset.

    Shared by the ML frame filter (geocif._get_run_region_selection) and the
    CID-generation filter, so the two can never interpret the same config
    differently.
    """
    log = log or logger
    if not raw:
        return None

    try:
        selection = ast.literal_eval(str(raw))
    except (ValueError, SyntaxError) as exc:
        log.warning(f"Failed to parse run_regions ({raw!r}): {exc}. Running all regions.")
        return None

    if isinstance(selection, dict):
        crop_key = str(crop or "").strip().lower().replace(" ", "_")
        by_crop = {
            str(k).strip().lower().replace(" ", "_"): v for k, v in selection.items()
        }
        if crop_key not in by_crop:
            log.info(f"run_regions has no entry for crop '{crop}' — running all regions")
            return None
        selection = by_crop[crop_key]

    if isinstance(selection, str):
        selection = [selection]
    if not isinstance(selection, (list, tuple, set)):
        log.warning(
            f"run_regions must be a list or a {{crop: list}} dict, got "
            f"{type(selection).__name__} — ignoring, running all regions."
        )
        return None

    names = [str(name).strip() for name in selection if str(name).strip()]
    return names or None


def _resolve_stats_file(country, parser=None) -> str:
    """Resolve the production-statistics filename for a country.

    Order: per-country ``production_statistics_file`` config option →
    ``[DEFAULT]`` option → hvstat default. (Extracted from add_statistics so
    every consumer of the yield files shares one resolution rule.)
    """
    fn = "hvstat_africa_data_v1.0.csv"
    if parser is not None:
        country_key = country.lower().replace(" ", "_")
        if parser.has_option(country_key, "production_statistics_file"):
            fn = parser.get(country_key, "production_statistics_file")
        elif parser.has_option("DEFAULT", "production_statistics_file"):
            fn = parser.get("DEFAULT", "production_statistics_file")
    if country == "Illinois":
        fn = "illinois.csv"
    return fn


def admin1_lookup(dir_stats, country, parser=None):
    """Map normalized admin_2 (county) names -> admin_1 (state) names.

    Read from the same production-statistics file the yield join uses (via
    _resolve_stats_file) with the same name normalization, so the mapping can
    never disagree with the join. Backs the optional 'State' categorical for
    admin_2 runs. Returns {} when the file or columns are unavailable.
    """
    path = Path(dir_stats) / _resolve_stats_file(country, parser)
    if not path.is_file():
        return {}
    df = pd.read_csv(
        path, low_memory=False,
        usecols=lambda c: c in ("country", "admin_1", "admin_2"),
    )
    if not {"country", "admin_1", "admin_2"}.issubset(df.columns):
        return {}
    df = df[df["country"] == country].dropna(subset=["admin_1", "admin_2"])
    if df.empty:
        return {}
    return dict(zip(_norm_region_series(df["admin_2"]), df["admin_1"].astype(str)))


def regions_with_yields(dir_stats, country, crop, admin_zone, parser=None):
    """Normalized names of regions with at least one usable yield record.

    Reads the same file ``add_statistics`` would (via _resolve_stats_file)
    and applies the same row hygiene it applies before joining: the
    Wheat→Winter Wheat product rename, ``qc_flag == 0``, the (country,
    product) mask, and the standard crop_production_system filter. A region
    survives if ANY season/year row has a non-null yield — deliberately
    conservative (no season filtering), so it removes only regions that can
    never produce a yield row for this (country, crop) at this admin zone.

    Args:
        dir_stats: directory holding the production-statistics CSVs.
        country: display form, e.g. "United States Of America".
        crop: display form, e.g. "Maize".
        admin_zone: which admin column names the regions — "admin_1" or
            "admin_2". This is what makes the filter scale-generic.
        parser: config parser for the file-resolution options.

    Returns:
        set of normalized region names, or None when the answer is unknown
        (missing file/columns, or no rows for this country+crop — e.g.
        GEOGLAM-format countries) — callers must treat None as "do not
        filter".
    """
    path = Path(dir_stats) / _resolve_stats_file(country, parser)
    if not path.is_file():
        return None
    df = pd.read_csv(path, low_memory=False)
    required = {"country", "product", "yield", admin_zone}
    if not required.issubset(df.columns):
        return None
    if "product" in df.columns:
        df.loc[:, "product"] = df["product"].replace("Wheat", "Winter Wheat")
    if "qc_flag" in df.columns:
        df = df[df["qc_flag"] == 0]
    if "crop_production_system" in df.columns:
        df = df[df["crop_production_system"].isin(STANDARD_PRODUCTION_SYSTEMS)]
    df = df[(df["country"] == country) & (df["product"] == crop)]
    if df.empty:
        return None
    df = df[df["yield"].notna()]
    return set(_norm_region_series(df[admin_zone]).dropna())


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
    # Prefer the stored yield column (per-source curated value) over
    # production/area. Reason: for merged HS+SPE files (e.g. togo), a
    # single row may have area from HS and production from SPE — two
    # different sources with different geographic scopes / methodologies.
    # Recomputing yield = prod/area across such rows produces spurious
    # values (togo Centrale 2006: 1.53 t/ha per HS but 2.69 t/ha via
    # prod/area from mixed sources). The stored yield column, when
    # present, was curated per-source per the file's merge strategy
    # (see "SPE_data_curation" report) and is the reliable value.
    if total_area and total_area > 0 and yield_values.notna().any():
        agg_yield = (
            (yield_values.fillna(0) * area_values.fillna(0)).sum()
            / total_area
        )
    elif total_area and total_area > 0 and total_prod and total_prod > 0:
        # Fall-through: yield column genuinely missing. Standard case
        # for un-filled SPE rows where the curator hadn't derived yield
        # from prod/area yet (see PDF Section 5.2: 43 fills of this type
        # in the togo SPE source).
        agg_yield = total_prod / total_area
    else:
        agg_yield = yield_values.mean(skipna=True)
    return agg_yield, total_area, total_prod


def _object_join_key(series):
    """Column values as an object-dtype merge-key array whose semantics
    reproduce the legacy elementwise ``==`` scans: numeric values match
    across int/float dtypes (2019 == 2019.0 — Python hash/equality),
    strings never match numbers, and missing values map to NaN. Callers
    must drop NaN keys from the lookup (right) side, because pandas
    merge pairs NaN with NaN while ``==`` never did.

    Built via factorize so a multi-million-row pipeline frame only boxes
    each distinct key value once.
    """
    codes, uniques = pd.factorize(series, use_na_sentinel=True)
    uarr = np.asarray(uniques, dtype=object)
    out = np.full(len(codes), np.nan, dtype=object)
    seen = codes >= 0
    out[seen] = uarr[codes[seen]]
    return out


def _norm_region_key(series):
    """``_norm_region_series`` applied through factorize: each distinct
    region name is normalized once instead of once per row (the pipeline
    frame side of the yield join can hold millions of rows). NaN → NaN;
    callers drop NaN group keys beforehand (mirroring the legacy groupby
    ``dropna=True`` behavior), so NaN keys never reach the merge.
    """
    codes, uniques = pd.factorize(series, use_na_sentinel=True)
    norm = _norm_region_series(pd.Series(np.asarray(uniques, dtype=object)))
    narr = norm.to_numpy(dtype=object)
    out = np.full(len(codes), np.nan, dtype=object)
    seen = codes >= 0
    out[seen] = narr[codes[seen]]
    return out


def _aggregate_ps_lookup(df_stats_subset):
    """Vectorized twin of ``aggregate_yield_across_ps``: collapse
    multi-production-system stats rows into ONE row per
    (``__region``, ``__year``) key with identical semantics — zeros/±inf
    → NaN hygiene, ``sum(skipna=True)`` totals (all-NaN group → 0 →
    reported as NaN), and the same three-branch yield: area-weighted
    stored-yield mean when any yield exists and total area > 0, else
    production/area, else plain yield mean.

    Args:
        df_stats_subset: pre-filtered production-statistics rows carrying
            ``__region``/``__year`` key columns plus ``yield``/``area``/
            ``production``.

    Returns:
        DataFrame with columns ``__region``, ``__year``, ``__yld``,
        ``__area``, ``__prod`` (one row per key; ``__area``/``__prod``
        NaN unless the group total is > 0). Empty input → empty frame
        with the same columns.
    """
    sub = df_stats_subset.reset_index(drop=True)
    y = sub["yield"].replace([0, np.inf, -np.inf], np.nan)
    a = sub["area"].replace([0, np.inf, -np.inf], np.nan)
    p = sub["production"].replace([0, np.inf, -np.inf], np.nan)
    tmp = pd.DataFrame(
        {
            "__region": sub["__region"],
            "__year": sub["__year"],
            "__y": y,
            "__a": a,
            "__p": p,
            # Same product the legacy scalar path summed:
            # (yield.fillna(0) * area.fillna(0)).sum()
            "__wy": y.fillna(0) * a.fillna(0),
        }
    )
    agg = (
        tmp.groupby(["__region", "__year"], sort=False, dropna=False)
        .agg(
            __ta=("__a", "sum"),
            __tp=("__p", "sum"),
            __wys=("__wy", "sum"),
            __ym=("__y", "mean"),
            __yn=("__y", "count"),
        )
        .reset_index()
    )
    ta = agg["__ta"].to_numpy(dtype=float)
    tp = agg["__tp"].to_numpy(dtype=float)
    wys = agg["__wys"].to_numpy(dtype=float)
    ym = agg["__ym"].to_numpy(dtype=float)
    has_yield = agg["__yn"].to_numpy() > 0
    with np.errstate(divide="ignore", invalid="ignore"):
        yld = np.where(
            (ta > 0) & has_yield,
            wys / ta,
            np.where((ta > 0) & (tp > 0), tp / ta, ym),
        )
    return pd.DataFrame(
        {
            "__region": agg["__region"],
            "__year": agg["__year"],
            "__yld": yld,
            "__area": np.where(ta > 0, ta, np.nan),
            "__prod": np.where(tp > 0, tp, np.nan),
        }
    )


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
    
    # Filename: per-country override → DEFAULT override → hvstat default
    # (shared with regions_with_yields via _resolve_stats_file).
    fn = _resolve_stats_file(country, parser)
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
            # Per-country config override: [<country>] hvstat_season_override
            # in countries.txt. Value is a single season_name that MUST exist
            # in the hvstat file (e.g., "Annual", "Long", "Short", "Meher"...).
            # If unset or the given name isn't in available_seasons, falls
            # through to the legacy hardcoded / PRIMARY/SECONDARY_SEASON_NAMES
            # resolution. Applies to every CID Season (both s=1 and s=2 use
            # the same override — one override per country/crop for now).
            if parser is not None:
                country_key = country.lower().replace(" ", "_")
                if parser.has_option(country_key, "hvstat_season_override"):
                    override = parser.get(country_key, "hvstat_season_override").strip()
                    if override in available_seasons:
                        return [override]
                    # else: fall through with a note the value didn't match.
                    # (No warning here — logged once by add_statistics caller.)

            # Legacy hardcoded fallback for Kenya Maize (retained so runs with
            # no override key keep their previous behavior). Prefer the config
            # override above for any new deployment.
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

        # ------------------------------------------------------------------
        # Vectorized join. Replaces the legacy per-(Region, Harvest Year
        # [, Season]) process_group loop, which re-scanned (and re-lower-
        # cased) the full production-statistics table once per group —
        # ~53k times at US county scale. Semantics preserved exactly:
        #   * rows whose group key contains NaN are dropped (the legacy
        #     groupby used the dropna=True default); surviving rows keep
        #     their input order (legacy emitted them sorted by group key —
        #     the one deliberate difference, callers are order-agnostic);
        #   * the stats table is filtered on the PS whitelist + product +
        #     the per-Season season_name filter — deliberately NOT on
        #     country, because the legacy per-group mask never filtered on
        #     country either (admin names shared across countries pool);
        #   * region matching is case-insensitive with underscores
        #     normalized to spaces (shared _norm_region_* rule), NaN admin
        #     names normalize to the string "nan" exactly as before;
        #   * multi-PS rows collapse with aggregate_yield_across_ps logic
        #     (see _aggregate_ps_lookup);
        #   * a group "matched" when >=1 stats row survived the mask — the
        #     yield/area/production columns are created only when at least
        #     one group matched (threshold_optimizer relies on the columns
        #     staying absent when nothing matched) and unmatched rows keep
        #     any pre-existing values (NaN when the column is new);
        #   * Malawi-Maize groups the primary season_name filter left
        #     empty fall back to season_name == "Annual".
        # ------------------------------------------------------------------
        df = df.dropna(subset=group_by)
        # (dropna also returns a fresh copy, so — like the legacy
        # group.copy()+concat path — the caller's frame is never mutated.)

        if len(df):
            base_mask = (
                df_fewsnet["crop_production_system"].isin(STANDARD_PRODUCTION_SYSTEMS)
                & (df_fewsnet["product"] == crop)
            )
            df_stats = df_fewsnet.loc[
                base_mask,
                [admin_zone, "harvest_year", "season_name",
                 "yield", "area", "production"],
            ].copy()
            # Legacy `==` never matched NaN harvest_year; pandas merge
            # WOULD pair NaN keys — drop them from the lookup side.
            df_stats = df_stats[df_stats["harvest_year"].notna()]
            df_stats["__region"] = _norm_region_series(
                df_stats[admin_zone]
            ).astype(object)
            df_stats["__year"] = _object_join_key(df_stats["harvest_year"])

            # One aggregated lookup block per distinct Season number (each
            # number can resolve to a different season_name filter); keys
            # are unique within a block, and blocks are disambiguated by
            # the __season tag, so the left-merge below can never fan out.
            blocks = []
            for s, season_filter in season_filters.items():
                block = _aggregate_ps_lookup(
                    df_stats[df_stats["season_name"].isin(season_filter)]
                )
                if has_season:
                    block["__season"] = s
                blocks.append(block)
            lookup = pd.concat(blocks, ignore_index=True)

            key_cols = ["__region", "__year"]
            left = pd.DataFrame(
                {
                    "__region": _norm_region_key(df["Region"]),
                    "__year": _object_join_key(df["Harvest Year"]),
                }
            )
            if has_season:
                key_cols.append("__season")
                lookup["__season"] = lookup["__season"].astype(object)
                left["__season"] = _object_join_key(df["Season"])

            merged = left.merge(
                lookup, on=key_cols, how="left", indicator="__matched"
            )
            matched = (merged["__matched"] == "both").to_numpy()
            yld = merged["__yld"].to_numpy(dtype=float)
            area = merged["__area"].to_numpy(dtype=float)
            prod = merged["__prod"].to_numpy(dtype=float)

            # Fallback to "Annual" for Malawi Maize when the primary season
            # has no data — second merge filling only rows the first left
            # unmatched (and only for Season numbers whose filter does not
            # already include "Annual", as before).
            if (
                country == "Malawi"
                and crop == "Maize"
                and "Annual" in available_seasons
            ):
                if has_season:
                    fallback_ok = {
                        s: "Annual" not in sf for s, sf in season_filters.items()
                    }
                    eligible = (
                        df["Season"].map(fallback_ok).fillna(False)
                        .to_numpy(dtype=bool)
                    )
                else:
                    eligible = np.full(
                        len(df), "Annual" not in season_filters[None]
                    )
                need = eligible & ~matched
                if need.any():
                    annual = _aggregate_ps_lookup(
                        df_stats[df_stats["season_name"] == "Annual"]
                    )
                    m2 = left[["__region", "__year"]].merge(
                        annual, on=["__region", "__year"],
                        how="left", indicator="__matched",
                    )
                    take = (m2["__matched"] == "both").to_numpy() & need
                    yld = np.where(take, m2["__yld"].to_numpy(dtype=float), yld)
                    area = np.where(take, m2["__area"].to_numpy(dtype=float), area)
                    prod = np.where(take, m2["__prod"].to_numpy(dtype=float), prod)
                    matched = matched | take

            if matched.any():
                keep = ~pd.Series(matched)
                for col, vals in (
                    (target_col, yld),
                    ("Area (ha)", area),
                    ("Production (tn)", prod),
                ):
                    if col in df.columns:
                        # Overwrite matched rows only — legacy wrote into
                        # groups that found stats rows and left the rest
                        # untouched. Positional (index-free) so duplicate
                        # index labels can't fan out.
                        df[col] = (
                            pd.Series(df[col].to_numpy())
                            .where(keep, pd.Series(vals))
                            .to_numpy()
                        )
                    else:
                        df[col] = np.where(matched, vals, np.nan)

    # Add columns for obj.stats_cols
    for col in ["Area"]:
        df.loc[:, col] = np.nan

    return df