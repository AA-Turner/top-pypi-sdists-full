"""Parent-level (admin_1 / national) model-performance aggregation.

When yield_outlook runs at admin level X, this module additionally produces
model-performance outputs at every HIGHER admin level:

* an ``admin_2`` (county) run also gets ``admin_1`` (state) and ``national``
  aggregations;
* an ``admin_1`` (state) run gets a ``national`` aggregation.

Aggregation is an area-weighted mean of observed / predicted yields per
(parent, Harvest Year) — groups with missing or zero weights fall back to a
plain unweighted mean (logged once per call). The county -> state mapping
reuses :func:`geocif.ml.stats.admin1_lookup`, which shares file resolution and
name normalization with the yield join, so the two can never disagree.

Outputs per (country, crop, model, level), ``<level>`` in
``{admin_1, national}``:

* ``outlook/plots/<model>/<country>/<crop>/<level>/`` — pooled obs-vs-pred
  scatter (+ hexbin companion, both via ``diagnostics.scatter_obs_pred`` so
  the house square-limits / metric-annotation style is identical), a national
  obs-vs-pred yearly time series (national level only), and per-parent rRMSE%
  / r² choropleths (admin_1 level only, via ``diagnostics.metric_choropleth``
  -> ``viz.plot.plot_map`` with its default pygmt backend).
* ``outlook/csvs/<model>/<country>/<crop>/<level>/`` — the exact plotted data
  for every plot, the aggregated predictions frame, and the per-parent
  metrics table.
* ``lookup_plots_csvs.csv`` in BOTH level directories: maps each plot
  filename (relative to the plots level dir) to its companion CSV filename
  (relative to the csvs level dir).

The whole feature is gated at the call site
(``yield_outlook._generate_diagnostics``) by ``[ML] plot_parent_aggregations``
(default True) and wrapped in try/except — it can never fail the run.
Boundary for the admin_1 maps: ``[ML] parent_boundary_admin_1`` (filename
under ``[PATHS] dir_boundary_files``; falls back to ``Level_1.shp``). When the
file is missing or fewer than 50% of parent names match the shapefile's
ADM1_NAME, the maps are skipped with a logged warning — never a crash.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

OBS_COL = "Observed Yield (tn per ha)"
PRED_COL = "Predicted Yield (tn per ha)"
UNKNOWN_PARENT = "unknown"
POOLED_LABEL = "ALL (pooled)"

# Minimum fraction of parent names that must match the boundary shapefile's
# ADM1_NAME for the choropleths to render (below this the map would be mostly
# empty and misleading — skip it instead).
MIN_BOUNDARY_MATCH_FRACTION = 0.5

# Which HIGHER levels each run level aggregates to, in render order.
_LEVELS_ABOVE = {
    "admin_2": ["admin_1", "national"],
    "admin_1": ["national"],
}

_LEVEL_DISPLAY = {
    "admin_1": "Admin-1 aggregate",
    "national": "National aggregate",
}


def parent_levels_for(admin_zone):
    """Higher admin levels to aggregate to for a run at ``admin_zone``.

    ``admin_2`` -> ``["admin_1", "national"]``; ``admin_1`` -> ``["national"]``;
    anything else (including ``national`` itself) -> ``[]``.
    """
    return list(_LEVELS_ABOVE.get(str(admin_zone).strip().lower(), []))


def _display_name(token):
    """Config token -> display form (``united_states_of_america`` ->
    ``United States Of America``). Mirrors how yield_outlook builds
    country/crop display names everywhere else."""
    return str(token).title().replace("_", " ")


def build_level_map(regions, level, country, parser=None):
    """Map each child region to its parent name at ``level``.

    Args:
        regions: iterable of child Region names as they appear in the
            predictions frame (display form, e.g. ``"Iowa Adair"``).
        level: ``"admin_1"`` or ``"national"``.
        country: country config token (e.g. ``"united_states_of_america"``).
        parser: config parser — needed for the admin_1 mapping
            (``[PATHS] dir_production_statistics`` + stats-file resolution).

    Returns:
        dict of NORMALIZED child region name -> parent display name.
        For admin_1, children without a stats-file mapping map to
        ``"unknown"`` (kept downstream, flagged in the metrics CSV).
        Empty dict when ``level`` is unrecognized.
    """
    from geocif.ml import stats as ml_stats

    country_display = _display_name(country)
    norm_regions = {ml_stats._norm_region_name(r) for r in regions}

    if level == "national":
        return {r: country_display for r in norm_regions}

    if level == "admin_1":
        mapping = {}
        if parser is not None:
            try:
                dir_stats = Path(parser.get("PATHS", "dir_production_statistics"))
                mapping = ml_stats.admin1_lookup(
                    dir_stats, country_display, parser=parser
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    f"parent aggregation: admin1_lookup failed for "
                    f"{country_display} ({type(exc).__name__}: {exc}); "
                    f"all regions will map to '{UNKNOWN_PARENT}'"
                )
                mapping = {}
        return {r: mapping.get(r, UNKNOWN_PARENT) for r in norm_regions}

    return {}


def aggregate_predictions(df, level_map, weight_col="Area (ha)"):
    """Aggregate child-region predictions to parent units.

    Per (parent, Harvest Year[, Model]) group, observed and predicted yields
    are area-weighted means ``sum(y * w) / sum(w)``. A group falls back to the
    plain unweighted mean when ``weight_col`` is absent or any row in the
    group has a missing/zero/negative weight (logged once per call, not per
    group). Observed-NaN rows are excluded from the observed aggregate (and
    therefore from metric computation downstream) while predictions are
    aggregated over ALL child rows that have a prediction.

    Args:
        df: predictions frame with columns Region, Harvest Year,
            ``OBS_COL``, ``PRED_COL`` and optionally Model / ``weight_col``.
        level_map: normalized child region name -> parent name (see
            :func:`build_level_map`). Children missing from the map get
            parent ``"unknown"``.
        weight_col: weight column name (default ``"Area (ha)"``).

    Returns:
        DataFrame with columns: Region (the PARENT name), Harvest Year,
        [Model], ``OBS_COL``, ``PRED_COL``, ``Area (ha)`` (summed weights of
        the predicted rows; NaN for unweighted groups), ``N Units`` (child
        regions contributing a prediction), ``Aggregation``
        ("area-weighted" | "unweighted") and ``Unmapped Parent`` (bool).
    """
    from geocif.ml import stats as ml_stats

    if df is None or df.empty:
        return pd.DataFrame()

    work = df.copy()
    work["__parent"] = (
        ml_stats._norm_region_series(work["Region"])
        .map(level_map)
        .fillna(UNKNOWN_PARENT)
    )

    group_keys = ["__parent", "Harvest Year"]
    has_model = "Model" in work.columns
    if has_model:
        group_keys.append("Model")

    has_weight_col = weight_col in work.columns
    n_fallback_groups = 0
    rows = []
    for keys, g in work.groupby(group_keys, dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if has_weight_col:
            w = pd.to_numeric(g[weight_col], errors="coerce")
            weights_ok = bool(w.notna().all() and (w > 0).all())
        else:
            w = pd.Series(np.nan, index=g.index)
            weights_ok = False
        if not weights_ok:
            n_fallback_groups += 1

        def _agg(col):
            """(weighted-or-unweighted mean, n contributing rows, sum of
            weights) over the non-NaN rows of ``col``."""
            vals = pd.to_numeric(g[col], errors="coerce")
            mask = vals.notna()
            if not mask.any():
                return np.nan, 0, np.nan
            if weights_ok:
                ww = w[mask]
                return (
                    float((vals[mask] * ww).sum() / ww.sum()),
                    int(mask.sum()),
                    float(ww.sum()),
                )
            return float(vals[mask].mean()), int(mask.sum()), np.nan

        pred_val, n_pred, area_sum = _agg(PRED_COL)
        obs_val, _, _ = _agg(OBS_COL)

        row = {"Region": keys[0], "Harvest Year": keys[1]}
        if has_model:
            row["Model"] = keys[2]
        row.update({
            OBS_COL: obs_val,
            PRED_COL: pred_val,
            "Area (ha)": area_sum,
            "N Units": n_pred,
            "Aggregation": "area-weighted" if weights_ok else "unweighted",
            "Unmapped Parent": keys[0] == UNKNOWN_PARENT,
        })
        rows.append(row)

    if n_fallback_groups:
        logger.warning(
            f"aggregate_predictions: {n_fallback_groups} group(s) had a "
            f"missing/zero '{weight_col}' weight; used unweighted means for "
            f"those groups"
        )
    return pd.DataFrame(rows).reset_index(drop=True)


def compute_metrics(parent_df):
    """Per-parent-unit + pooled skill metrics from an aggregated frame.

    Only rows with BOTH observed and predicted values enter the metrics
    (observed-NaN parent-years are aggregated for display but never scored).

    Metrics: r² = 1 - SSE/SST (NaN when <2 rows or SST == 0),
    rRMSE% = 100 * RMSE / mean(obs) (NaN when mean(obs) <= 0),
    MAPE% = mean(|pred - obs| / |obs|) * 100 over obs != 0 rows.

    Returns a DataFrame with one row per parent plus one pooled row
    (Region = ``"ALL (pooled)"``, ``Is Pooled`` = True) computed across every
    scored parent-year at this level. ``Unmapped Parent`` flags the
    ``"unknown"`` catch-all parent.
    """
    if parent_df is None or parent_df.empty:
        return pd.DataFrame()
    scored = parent_df.dropna(subset=[OBS_COL, PRED_COL])
    if scored.empty:
        return pd.DataFrame()

    def _metrics(g):
        obs = g[OBS_COL].astype(float).to_numpy()
        pred = g[PRED_COL].astype(float).to_numpy()
        err = pred - obs
        n = len(g)
        rmse = float(np.sqrt(np.mean(err ** 2)))
        obs_mean = float(np.mean(obs))
        rrmse = 100.0 * rmse / obs_mean if obs_mean > 0 else np.nan
        nz = obs != 0
        mape = (
            float(np.mean(np.abs(err[nz] / obs[nz])) * 100.0)
            if nz.any() else np.nan
        )
        sst = float(np.sum((obs - obs_mean) ** 2))
        sse = float(np.sum(err ** 2))
        r2 = (1.0 - sse / sst) if (n >= 2 and sst > 0) else np.nan
        return {"N": n, "r2": r2, "rRMSE (%)": rrmse, "MAPE (%)": mape}

    rows = []
    for parent, g in scored.groupby("Region", sort=True):
        unmapped = (
            bool(g["Unmapped Parent"].any())
            if "Unmapped Parent" in g.columns
            else str(parent) == UNKNOWN_PARENT
        )
        rows.append({
            "Region": parent,
            **_metrics(g),
            "Is Pooled": False,
            "Unmapped Parent": unmapped,
        })
    rows.append({
        "Region": POOLED_LABEL,
        **_metrics(scored),
        "Is Pooled": True,
        "Unmapped Parent": False,
    })
    return pd.DataFrame(rows)


def _plot_national_timeseries(parent_df, title, out_path, yield_units="Mg/ha"):
    """One-panel national yearly time series: observed vs predicted lines.

    Returns True when a figure was written (so the caller only records a
    plot->CSV lookup row for files that exist)."""
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    from . import diagnostics as diag

    d = parent_df.dropna(subset=["Harvest Year"]).sort_values("Harvest Year")
    obs = d.dropna(subset=[OBS_COL])
    pred = d.dropna(subset=[PRED_COL])
    if obs.empty and pred.empty:
        return False

    with diag._science_style_context():
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.grid(True, linestyle="--", alpha=0.5)
        if not obs.empty:
            ax.plot(
                obs["Harvest Year"], obs[OBS_COL],
                color="black", marker="o", markersize=4, linewidth=1.2,
                label="Observed",
            )
        if not pred.empty:
            ax.plot(
                pred["Harvest Year"], pred[PRED_COL],
                color="#1f77b4", marker="s", markersize=4, linewidth=1.2,
                linestyle="--", label="Predicted",
            )
        ax.set_xlabel("Harvest Year")
        ax.set_ylabel(f"Yield ({yield_units})")
        ax.set_title(title, fontsize=10)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend(frameon=False)
        plt.tight_layout()
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=250, bbox_inches="tight")
        plt.close(fig)
    return True


def _load_parent_boundary(parser, country):
    """Load the admin_1 boundary for the aggregated maps.

    Resolution: ``[ML] parent_boundary_admin_1`` (filename under
    ``[PATHS] dir_boundary_files``) -> fallback ``Level_1.shp``. The frame is
    standardized via ``utils.load_country_boundary_gdf`` when possible (raw
    ``gpd.read_file`` as fallback), the admin-1 name column is renamed to
    ``ADM1_NAME``, and rows are filtered to ``country`` when an ADM0 column
    exists.

    Returns:
        (GeoDataFrame, None) on success or (None, reason_str) on any failure
        — callers log the reason and skip the maps, never crash.
    """
    if parser is None:
        return None, "no config parser available"
    try:
        dir_bnd = Path(parser.get("PATHS", "dir_boundary_files"))
    except Exception:  # noqa: BLE001
        return None, "[PATHS] dir_boundary_files not configured"

    fname = parser.get("ML", "parent_boundary_admin_1", fallback=None)
    path = dir_bnd / (fname or "Level_1.shp")
    if not path.is_file():
        return None, f"boundary file not found: {path}"

    gdf = None
    try:
        from geocif.utils import load_country_boundary_gdf
        gdf = load_country_boundary_gdf(parser, path)
    except Exception:  # noqa: BLE001
        try:
            import geopandas as gpd
            gdf = gpd.read_file(path, engine="pyogrio")
        except Exception as exc:  # noqa: BLE001
            return None, f"failed to read {path}: {type(exc).__name__}: {exc}"

    adm1_col = next(
        (c for c in ("ADM1_NAME", "ADMIN1", "NAME_1", "name1",
                     "admin1_name", "adm1_name")
         if c in gdf.columns),
        None,
    )
    if adm1_col is None:
        return None, f"no admin-1 name column found in {path}"
    if adm1_col != "ADM1_NAME":
        gdf = gdf.rename(columns={adm1_col: "ADM1_NAME"})

    adm0_col = next(
        (c for c in ("ADM0_NAME", "ADMIN0", "NAME_0") if c in gdf.columns),
        None,
    )
    if adm0_col is not None:
        want = str(country).replace("_", " ").lower()
        sub = gdf[
            gdf[adm0_col].astype(str).str.replace("_", " ").str.lower() == want
        ]
        if len(sub):
            gdf = sub
    return gdf.copy(), None


def _render_parent_maps(df_metrics, country, stem, dir_plots, parser,
                        lookup_rows, metrics_csv_name):
    """Per-parent rRMSE% and r² choropleths (admin_1 level).

    Reuses ``diagnostics.metric_choropleth`` (-> ``viz.plot.plot_map``,
    default pygmt backend) so style matches the native metric maps. Skips —
    with a logged warning, never a crash — when the boundary can't be loaded
    or fewer than ``MIN_BOUNDARY_MATCH_FRACTION`` of parent names match the
    shapefile's ADM1_NAME (case-insensitive, underscore-normalized: the same
    ``stats._norm_region_*`` rule the yield join uses).
    """
    from geocif.ml import stats as ml_stats
    from . import diagnostics as diag

    boundary, reason = _load_parent_boundary(parser, country)
    if boundary is None:
        logger.warning(
            f"parent aggregation maps skipped for {stem}: {reason}"
        )
        return

    df_map = df_metrics[
        (~df_metrics["Is Pooled"]) & (~df_metrics["Unmapped Parent"])
    ].copy()
    if df_map.empty:
        logger.warning(
            f"parent aggregation maps skipped for {stem}: no mapped parents"
        )
        return

    parents_norm = set(ml_stats._norm_region_series(df_map["Region"]))
    shp_norm = set(ml_stats._norm_region_series(boundary["ADM1_NAME"]))
    matched = parents_norm & shp_norm
    frac = len(matched) / len(parents_norm) if parents_norm else 0.0
    if frac < MIN_BOUNDARY_MATCH_FRACTION:
        logger.warning(
            f"parent aggregation maps skipped for {stem}: only "
            f"{len(matched)}/{len(parents_norm)} parent names match the "
            f"boundary's ADM1_NAME (need >= "
            f"{MIN_BOUNDARY_MATCH_FRACTION:.0%})"
        )
        return

    country_display = _display_name(country)
    bnd = boundary.copy()
    bnd["Country Region"] = (
        country_display.lower() + " "
        + ml_stats._norm_region_series(bnd["ADM1_NAME"])
    )
    df_map["Country Region"] = (
        country_display.lower() + " "
        + ml_stats._norm_region_series(df_map["Region"])
    )

    # rRMSE%: lower is better -> reversed Bamako (low = light), floor at 0.
    rrmse_png = f"rrmse_map_{stem}.png"
    diag.metric_choropleth(
        bnd, df_map, [country_display], False, dir_plots, rrmse_png,
        col="rRMSE (%)", label="rRMSE (%)", vmin=0.0, value_fmt="{:.1f}",
    )
    lookup_rows.append(
        (rrmse_png, metrics_csv_name, "per-parent rRMSE% choropleth")
    )
    # r²: higher is better -> non-reversed Bamako, ceiling at 1.
    r2_png = f"r2_map_{stem}.png"
    diag.metric_choropleth(
        bnd, df_map, [country_display], False, dir_plots, r2_png,
        col="r2", label="r²", vmax=1.0, higher_is_better=True,
    )
    lookup_rows.append(
        (r2_png, metrics_csv_name, "per-parent r² choropleth")
    )


def _write_lookup(lookup_rows, dir_plots, dir_csvs):
    """Write the plot -> CSV lookup table into BOTH level directories.

    ``plot_file`` is relative to the plots level dir; ``csv_file`` is
    relative to the csvs level dir."""
    if not lookup_rows:
        return
    df = pd.DataFrame(
        lookup_rows, columns=["plot_file", "csv_file", "description"]
    )
    df.to_csv(Path(dir_plots) / "lookup_plots_csvs.csv", index=False)
    df.to_csv(Path(dir_csvs) / "lookup_plots_csvs.csv", index=False)


def render_parent_aggregations(df, country, crop, model, dir_outlook,
                               parser=None, admin_zone="admin_1",
                               yield_units="Mg/ha"):
    """Produce every parent-level performance output for one
    (country, crop, model) combo.

    Called from ``yield_outlook._generate_diagnostics`` after the native
    per-stage diagnostics (works identically in full-ML and reuse_db runs,
    since both re-enter that stage). ``df`` is the same predictions frame the
    native diagnostics consume (display units already applied).

    Multi-stage frames are first reduced to one row per (Region, Harvest
    Year) keeping the latest stage — the same rule yield_outlook's native
    MAPE diagnostics use — so a child region is never double-counted within
    a parent-year.
    """
    levels = parent_levels_for(admin_zone)
    if not levels:
        logger.info(
            f"parent aggregation: nothing above admin_zone="
            f"'{admin_zone}' for {country} {crop} {model}; skipping"
        )
        return
    if (df is None or df.empty
            or OBS_COL not in df.columns or PRED_COL not in df.columns):
        return

    from . import diagnostics as diag

    d = df.copy()
    if "Stage Name" in d.columns and d["Stage Name"].dropna().nunique() > 1:
        d = (
            d.sort_values("Stage Name")
            .groupby(["Region", "Harvest Year"], as_index=False)
            .last()
        )

    country_display = _display_name(country)
    crop_display = _display_name(crop)
    title_base = f"{country_display} {crop_display} — {model}"

    for level in levels:
        level_map = build_level_map(
            d["Region"].dropna().unique(), level, country, parser
        )
        if not level_map:
            continue
        if level == "admin_1" and all(
            v == UNKNOWN_PARENT for v in level_map.values()
        ):
            logger.warning(
                f"parent aggregation: no admin_2->admin_1 mapping available "
                f"for {country_display}; skipping the admin_1 level for "
                f"{crop} {model}"
            )
            continue

        parent_df = aggregate_predictions(d, level_map)
        if parent_df.empty:
            continue

        dir_plots = Path(dir_outlook) / "plots" / model / country / crop / level
        dir_csvs = Path(dir_outlook) / "csvs" / model / country / crop / level
        dir_plots.mkdir(parents=True, exist_ok=True)
        dir_csvs.mkdir(parents=True, exist_ok=True)

        stem = f"{level}_{country}_{crop}_{model}"
        level_title = f"{title_base} — {_LEVEL_DISPLAY.get(level, level)}"
        lookup_rows = []

        # Full aggregated frame — the data source every plot at this level
        # derives from (also useful on its own for downstream analysis).
        agg_csv = f"aggregated_predictions_{stem}.csv"
        parent_df.to_csv(dir_csvs / agg_csv, index=False)

        # (a) pooled obs-vs-pred scatter (house style via scatter_obs_pred;
        # also emits the hexbin companion). CSV = exactly the scored rows.
        df_scatter = parent_df.dropna(subset=[OBS_COL, PRED_COL])
        if len(df_scatter) >= 2:
            scatter_png = f"scatter_{stem}.png"
            scatter_csv = f"scatter_{stem}.csv"
            diag.scatter_obs_pred(
                df_scatter, level_title, dir_plots, scatter_png,
                yield_units=yield_units,
            )
            df_scatter.to_csv(dir_csvs / scatter_csv, index=False)
            lookup_rows.append(
                (scatter_png, scatter_csv, "pooled obs-vs-pred scatter")
            )
            lookup_rows.append((
                f"scatter_{stem}_hexbin.png", scatter_csv,
                "hexbin density companion of the pooled scatter",
            ))

        # (b) per-parent-unit metrics CSV (+ pooled row).
        df_metrics = compute_metrics(parent_df)
        metrics_csv = f"metrics_{stem}.csv"
        if not df_metrics.empty:
            df_metrics.to_csv(dir_csvs / metrics_csv, index=False)

        # (c) national yearly time series (single parent unit -> one panel).
        if level == "national":
            ts_png = f"timeseries_{stem}.png"
            ts_csv = f"timeseries_{stem}.csv"
            try:
                wrote = _plot_national_timeseries(
                    parent_df, level_title, dir_plots / ts_png,
                    yield_units=yield_units,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    f"national time-series plot failed for {stem} "
                    f"(non-fatal): {type(exc).__name__}: {exc}"
                )
                wrote = False
            if wrote:
                parent_df.to_csv(dir_csvs / ts_csv, index=False)
                lookup_rows.append((
                    ts_png, ts_csv,
                    "national yearly observed-vs-predicted time series",
                ))

        # (d) per-parent rRMSE% / r² choropleths — only levels with a
        # boundary (national is a single unit -> no map).
        if level == "admin_1" and not df_metrics.empty:
            try:
                _render_parent_maps(
                    df_metrics, country, stem, dir_plots, parser,
                    lookup_rows, metrics_csv,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    f"parent aggregation maps failed for {stem} "
                    f"(non-fatal): {type(exc).__name__}: {exc}"
                )

        _write_lookup(lookup_rows, dir_plots, dir_csvs)
        logger.info(
            f"parent aggregation ({level}): wrote "
            f"{len(lookup_rows)} plot(s) + CSVs for {country} {crop} {model} "
            f"-> {dir_plots}"
        )
