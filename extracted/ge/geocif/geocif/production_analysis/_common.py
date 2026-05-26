"""Shared helpers for the production_analysis (BEAST) pipeline.

Five small functions used by ``beast_runner``, ``beast_plots`` and
``beast_sensitivity`` — kept here so the three stages stay thin.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import Rbeast as rb


def load_filtered_hvstat(input_csv):
    """Read HvStat Africa CSV and apply the standard qc/positive-yield filter.

    Drops rows flagged as outliers / low-variance (``qc_flag != 0``) and rows
    with missing or non-positive yield.  Adds an ``admin`` column that picks
    admin_2 when present, else admin_1.
    """
    df = pd.read_csv(input_csv)
    df = df[df["qc_flag"] == 0].copy()
    df = df[df["yield"].notna() & (df["yield"] > 0)]
    df["admin"] = np.where(df["admin_2"] != "none", df["admin_2"], df["admin_1"])
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
    """
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
