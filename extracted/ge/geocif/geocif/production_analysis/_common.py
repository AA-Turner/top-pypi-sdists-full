"""Shared helpers for the production_analysis (BEAST) pipeline.

Five small functions used by ``beast_runner``, ``beast_plots`` and
``beast_sensitivity`` — kept here so the three stages stay thin.
"""
import ast
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl

# Rbeast is heavy + optional in some environments (e.g. test venvs without
# the binary wheel installed). The loaders here don't need it — only
# ``run_beast`` does — so the import is deferred to call-site to keep
# ``import _common`` cheap and test-safe.

logger = logging.getLogger(__name__)


def load_filtered_hvstat(input_csv):
    """Read HvStat Africa CSV and apply the canonical PS handling.

    Single source of truth shared with ``geocif.ml.stats.add_statistics``
    — both call sites consume the same whitelist + area-weighted
    aggregation, so the BEAST pipeline and the ML join see the same
    yield numbers.

    Pipeline:
      1. Drop rows flagged as outliers / low-variance (``qc_flag != 0``).
      2. Drop missing or non-positive yield.
      3. Drop non-whitelisted production systems
         (``geocif.ml.stats.STANDARD_PRODUCTION_SYSTEMS`` — 10 canonical
         labels). The other 17 PS values in HvStat (``A1 (PS)``,
         ``LSCF (PS)``, ``dam irrigation``, …) are non-standard /
         project-specific and excluded as noise.
      4. Aggregate across surviving PS per
         (country, admin_1, admin_2, product, season_name, harvest_year)
         via area-weighted ``total_production / total_area``
         (``geocif.ml.stats.aggregate_yield_across_ps``). After this
         step each (country, admin, crop, season, year) has ONE row
         instead of one per PS — matches what the ML pipeline join sees.
      5. Set ``crop_production_system = "aggregated"`` as a single
         synthetic value so ``beast_runner.GROUP_KEYS`` still has the
         column for its groupby (constant per series, harmless).
      6. Add ``admin`` column = ``admin_2`` when present, else ``admin_1``.
    """
    # Lazy import to avoid a circular dependency at module load (stats.py
    # is imported by ml/ which has heavier transitive deps).
    from geocif.ml.stats import (
        STANDARD_PRODUCTION_SYSTEMS,
        aggregate_yield_across_ps,
    )

    df = pd.read_csv(input_csv)
    df = df[df["qc_flag"] == 0].copy()
    df = df[df["yield"].notna() & (df["yield"] > 0)]
    df = df[df["crop_production_system"].isin(STANDARD_PRODUCTION_SYSTEMS)]
    if df.empty:
        return df

    key_cols = [
        "fnid", "country", "country_code", "admin_1", "admin_2",
        "product", "season_name", "harvest_year",
    ]

    def _agg_group(group):
        agg_y, agg_a, agg_p = aggregate_yield_across_ps(
            group["yield"], group["area"], group["production"],
        )
        return pd.Series({
            "yield": agg_y,
            "area": agg_a,
            "production": agg_p,
            "qc_flag": 0,
            "crop_production_system": "aggregated",
        })

    agg_df = (
        df.groupby(key_cols, dropna=False, observed=True)
          .apply(_agg_group, include_groups=False)
          .reset_index()
    )
    # Drop rows where aggregation collapsed to NaN (no valid yield in the group).
    agg_df = agg_df[agg_df["yield"].notna() & (agg_df["yield"] > 0)]
    agg_df["admin"] = np.where(
        agg_df["admin_2"] != "none", agg_df["admin_2"], agg_df["admin_1"],
    )
    return agg_df


# Sheet names in the per-crop AMIS XLSX (e.g. maize_1.xlsx) — match what
# geocif.ml.stats.add_GEOGLAM_statistics also expects.
_AMIS_SHEETS = {
    "yield": "Yield (tn per ha)",
    "area": "Area (ha)",
    "production": "Production (tn)",
}


def _amis_collect_combinations(parser):
    """Walk the parser to produce a list of (country_section, crop, season)
    triplets that need AMIS XLSX data. Mirrors the iteration pattern used
    by ``AgmetGeo.create_run_combinations`` and the threshold optimizer.

    Returns ``[(country_section_name, crop_str, season_int), ...]`` —
    country_section_name is the lowercase section key (matches
    ``parser.has_option(country, "boundary_file")`` semantics).
    """
    if not parser.has_option("DEFAULT", "countries"):
        return []
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    combos = []
    for country in countries:
        if parser.has_option(country, "crops"):
            crops = ast.literal_eval(parser.get(country, "crops"))
        elif parser.has_option("DEFAULT", "crops"):
            crops = ast.literal_eval(parser.get("DEFAULT", "crops"))
        else:
            continue
        if parser.has_option(country, "seasons"):
            seasons = ast.literal_eval(parser.get(country, "seasons"))
        elif parser.has_option("DEFAULT", "seasons"):
            seasons = ast.literal_eval(parser.get("DEFAULT", "seasons"))
        else:
            seasons = [1]
        for crop in crops:
            for season in seasons:
                combos.append((country, str(crop), int(season)))
    return combos


def _amis_melt_sheet(df_sheet, indicator, value_name="value"):
    """Melt one wide-format AMIS XLSX sheet into long form.

    Sheet schema (confirmed via direct inspection):
        ADM0_NAME | ADM1_NAME | ADM2_NAME | Season | Data Source | num_ID
        | <year_1> | <year_2> | ... | <year_N>

    Year columns are int-coerced; any non-year columns left of the year
    block are kept as id_vars. Returns long DataFrame with columns:
    ADM0_NAME, ADM1_NAME, ADM2_NAME, Season, harvest_year, <value_name>.
    """
    # Identify year columns: any column whose header parses as an int
    # in a plausible harvest-year range.
    year_cols = []
    id_cols = []
    for c in df_sheet.columns:
        try:
            y = int(c)
            if 1900 <= y <= 2100:
                year_cols.append(c)
                continue
        except (TypeError, ValueError):
            pass
        id_cols.append(c)
    keep_id = [c for c in ("ADM0_NAME", "ADM1_NAME", "ADM2_NAME", "Season") if c in id_cols]
    if not year_cols or not keep_id:
        return pd.DataFrame()
    long = df_sheet[keep_id + year_cols].melt(
        id_vars=keep_id, value_vars=year_cols,
        var_name="harvest_year", value_name=value_name,
    )
    long["harvest_year"] = long["harvest_year"].astype(int)
    return long


def _amis_load_one_workbook(xlsx_path, crop, season):
    """Load one per-crop AMIS XLSX and pivot into the long-form schema
    BEAST expects.

    Reads the three indicator sheets (Area / Production / Yield),
    melts year columns to long, joins on (admin keys + year + season),
    and produces a DataFrame with the columns BEAST consumes — same
    shape as ``load_filtered_hvstat`` output (modulo the AMIS-specific
    column values: synthetic ``fnid``, ``crop_production_system="none"``,
    ``qc_flag=0``).

    Returns an empty DataFrame if the file doesn't exist or the yield
    sheet has no numeric year columns.
    """
    xlsx_path = Path(xlsx_path)
    if not xlsx_path.is_file():
        logger.warning("AMIS XLSX not found, skipping: %s", xlsx_path)
        return pd.DataFrame()

    try:
        sheets = pd.read_excel(xlsx_path, sheet_name=None)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to read %s: %s", xlsx_path, exc)
        return pd.DataFrame()

    parts = []
    for ind_key, sheet_name in _AMIS_SHEETS.items():
        if sheet_name not in sheets:
            continue
        long_part = _amis_melt_sheet(
            sheets[sheet_name], indicator=ind_key, value_name=ind_key,
        )
        if long_part.empty:
            continue
        parts.append(long_part.set_index(
            ["ADM0_NAME", "ADM1_NAME", "ADM2_NAME", "Season", "harvest_year"]
        ))

    if not parts:
        return pd.DataFrame()

    # Outer-join on the shared index so missing area/production don't
    # drop yield rows.
    wide = pd.concat(parts, axis=1, join="outer").reset_index()
    # Coerce indicator columns to numeric so downstream `yield > 0`
    # filter and BEAST's float arrays work.
    for ind in _AMIS_SHEETS:
        if ind in wide.columns:
            wide[ind] = pd.to_numeric(wide[ind], errors="coerce")
        else:
            wide[ind] = np.nan

    # Fabricate the BEAST-required column names.
    # admin_1/admin_2: hvstat uses literal "none" for missing admin_2 and
    # downstream code (e.g. _common.py:22, beast_spatial pick_admin_col)
    # compares against that literal — match it exactly.
    wide["admin_1"] = wide["ADM1_NAME"].astype(str)
    wide["admin_2"] = wide["ADM2_NAME"].where(
        wide["ADM2_NAME"].notna() & (wide["ADM2_NAME"].astype(str) != ""),
        "none",
    ).astype(str)

    # country_name: normalize ADM0_NAME → lowercase + underscores so it
    # matches the [<country>] config-section convention used by
    # beast_spatial's per-country boundary_file lookup.
    wide["country"] = (
        wide["ADM0_NAME"].astype(str).str.strip().str.lower().str.replace(" ", "_")
    )
    # Also keep the original ADM0_NAME-cased value for any downstream
    # report code that compares against title-case country names.
    wide["country_name"] = wide["ADM0_NAME"].astype(str)
    wide["country_code"] = ""  # AMIS XLSX has no ISO code column; left blank

    wide["product"] = str(crop).replace("_", " ").title()
    wide["season_name"] = wide["Season"].astype(str)
    wide["crop_production_system"] = "none"
    wide["qc_flag"] = 0

    # Synthetic fnid — only used as a groupby/dedup key downstream;
    # confirmed via grep that no code parses fnid structurally.
    wide["fnid"] = (
        "amis_"
        + wide["country"].astype(str) + "_"
        + wide["admin_1"].astype(str) + "_"
        + wide["admin_2"].astype(str) + "_"
        + wide["season_name"].astype(str) + "_"
        + str(season) + "_"
        + str(crop)
    ).str.replace(r"\s+", "_", regex=True)

    return wide


def load_filtered_amis(dir_production_statistics, parser):
    """Read AMIS per-crop XLSX workbooks for every (country, crop, season)
    declared in ``parser`` and return a long-form DataFrame with the same
    column contract as ``load_filtered_hvstat``.

    Args:
        dir_production_statistics: Path to ``${PATHS:dir_production_statistics}``
            — the directory containing ``{crop}_{season}.xlsx`` workbooks
            (e.g. ``maize_1.xlsx``, ``rice_2.xlsx``).
        parser: ConfigParser carrying ``[DEFAULT] countries`` and per-country
            ``crops`` / ``seasons`` keys (same parser used elsewhere).

    Returns:
        DataFrame ready to drop into ``beast_runner.run`` — has every
        column in ``beast_runner.GROUP_KEYS`` plus ``yield``, ``area``,
        ``production``, ``harvest_year``, ``qc_flag``, ``admin_1``,
        ``admin_2``, ``admin`` (admin_2 when present else admin_1).

    Drops rows with non-positive or NaN yield to match the hvstat
    filter behaviour. Each (crop, season) XLSX is loaded ONCE even when
    multiple configured countries share it.
    """
    dir_path = Path(dir_production_statistics)
    combos = _amis_collect_combinations(parser)
    if not combos:
        logger.warning(
            "load_filtered_amis: no (country, crop, season) combinations "
            "found in parser — set [DEFAULT] countries + [<country>] crops + "
            "[<country>] seasons before calling."
        )
        return pd.DataFrame()

    # Group by (crop, season) so each XLSX is read at most once;
    # countries-per-workbook are filtered after melt.
    unique_files = {}  # (crop, season) -> set of country sections needing it
    for country, crop, season in combos:
        unique_files.setdefault((crop, season), set()).add(country)

    frames = []
    for (crop, season), countries_needed in unique_files.items():
        xlsx_path = dir_path / f"{crop}_{season}.xlsx"
        wide = _amis_load_one_workbook(xlsx_path, crop=crop, season=season)
        if wide.empty:
            continue
        # Keep only rows whose country matches a configured country section.
        wide = wide[wide["country"].isin(countries_needed)].copy()
        if wide.empty:
            logger.warning(
                "AMIS XLSX %s loaded but no rows matched configured "
                "countries %s — check ADM0_NAME values in the workbook.",
                xlsx_path.name, sorted(countries_needed),
            )
            continue
        frames.append(wide)

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    # Match the hvstat filter at _common.py:21 — only yield-positive rows.
    df = df[df["yield"].notna() & (df["yield"] > 0)].copy()
    # admin column: admin_2 when present else admin_1 — match hvstat
    # expression at _common.py:22 exactly.
    df["admin"] = np.where(df["admin_2"] != "none", df["admin_2"], df["admin_1"])
    # admin_level: hvstat runner sets this post-load (beast_runner.py:58).
    # AMIS loader sets it inline so the output is a true drop-in — the
    # runner's overwrite line becomes idempotent on AMIS-loaded frames.
    df["admin_level"] = np.where(df["admin_2"] != "none", "admin_2", "admin_1")
    return df


def build_annual_series(sub_df, value_col="yield"):
    """Collapse a per-series DataFrame into a NaN-filled annual series.

    Returns ``(y, y0, full)`` where:
      - ``y``    is the float ndarray of yields aligned to ``y0..y1`` (gaps = NaN)
      - ``y0``   is the first harvest_year as int
      - ``full`` is the merged DataFrame (handy when callers also need years/area)
    """
    agg_kwargs = {"yield_t_ha": (value_col, "mean")}
    if "area" in sub_df.columns:
        agg_kwargs["area"] = ("area", "sum")
    yr = sub_df.groupby("harvest_year", as_index=False).agg(**agg_kwargs)
    y0 = int(yr["harvest_year"].min())
    y1 = int(yr["harvest_year"].max())
    full = (pd.DataFrame({"harvest_year": np.arange(y0, y1 + 1)})
              .merge(yr, on="harvest_year", how="left"))
    y = full["yield_t_ha"].values.astype(float)
    return y, y0, full


def run_beast(y, y0, cfg, **overrides):
    """Call ``Rbeast.beast`` with the standard kwargs.

    ``cfg`` supplies ``tcp_minmax`` / ``tseg_minlength`` / ``mcmc_seed`` defaults;
    sensitivity analysis passes ``**overrides`` to vary one of them per config.

    Rbeast is imported lazily so the rest of ``_common`` (loaders, helpers)
    stays importable in environments that don't have the binary wheel.
    """
    import Rbeast as rb  # noqa: PLC0415 — lazy by design

    tcp_minmax = overrides.get("tcp_minmax", cfg.tcp_minmax)
    tseg_minlength = overrides.get("tseg_minlength", cfg.tseg_minlength)
    mcmc_seed = overrides.get("mcmc_seed", cfg.mcmc_seed)
    return rb.beast(
        y, start=y0, deltat=1, season="none",
        tcp_minmax=tcp_minmax, tseg_minlength=tseg_minlength,
        mcmc_seed=mcmc_seed,
        quiet=True, print_param=False,
        print_progress=False, print_warning=False,
    )


def extract_sorted_cps(beast_result):
    """Return ``(cp_years, cp_probs)`` sorted by descending posterior probability.

    Drops the NaN sentinel entries BEAST emits when fewer CPs are detected
    than the upper bound of ``tcp_minmax``.
    """
    cp_arr = np.atleast_1d(beast_result.trend.cp)
    cp_pr = np.atleast_1d(beast_result.trend.cpPr)
    ok = np.isfinite(cp_arr)
    cp_years = cp_arr[ok]
    cp_probs = cp_pr[ok]
    order = np.argsort(-cp_probs)
    return cp_years[order], cp_probs[order]


def pick_admin_col(gdf, df, prefer="ADM2_NAME", fallback="ADM1_NAME"):
    """Pick the admin-level column to join on between a boundary gdf and
    a long-form HvStat df.

    HvStat resolves FNID to admin_2 in 15 countries, admin_1 in 18; the
    shapefile may carry either ADM1_NAME or both ADM1_NAME and ADM2_NAME.
    Prefer the finer level (admin_2) when both sides have non-empty
    values; fall back to admin_1.

    Returns the column name as it appears in the gdf (e.g. "ADM2_NAME")
    AND the matching column in df (always lower-case "admin" because
    `load_filtered_hvstat` normalises both into a single column).

    Args:
        gdf: boundary GeoDataFrame already passed through
            ``load_country_boundary_gdf``.
        df: long-form df from ``load_filtered_hvstat`` with an "admin"
            column.
        prefer / fallback: gdf column names to try in order.

    Returns:
        (gdf_col, df_col) — column names to merge on. df_col is always
        "admin"; gdf_col is whichever of prefer/fallback has overlap
        with df["admin"].
    """
    if df.empty or "admin" not in df.columns:
        return None, None
    df_admins = set(df["admin"].astype(str).str.strip().str.lower())
    for col in (prefer, fallback):
        if col in gdf.columns:
            gdf_admins = set(gdf[col].astype(str).str.strip().str.lower())
            overlap = df_admins & gdf_admins
            if len(overlap) >= 2:
                return col, "admin"
    return None, None


def init_mpl_rcparams():
    """Apply the matplotlib defaults shared by beast_plots and beast_sensitivity."""
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 150, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "axes.grid": True,
        "grid.alpha": 0.3, "grid.linewidth": 0.5,
    })
