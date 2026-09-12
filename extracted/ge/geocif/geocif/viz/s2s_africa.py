# -*- coding: utf-8 -*-
"""Figures and README for the Africa-wide pre-season S2S run.

Consumes an ``s2s_africa`` output directory (``combinations.csv``,
``forecasts.csv``, ``skill.csv``, ``excluded.csv``) and renders three figure
families plus the run README.

Layout follows the outlook products (``viz/aggregation.py``,
``viz/cone.py``): every family is ``<family>/plots/`` for PNG and
``<family>/csvs/`` for the backing table, with a ``lookup_plots_csvs.csv``
manifest written into both. PNG only — no PDFs.

The skill panels plot AUC against each combination's own year-block
permutation null rather than against 0.5. Leave-one-year-out with an
intercept biases predictions upward in exactly the year the fold removed, so
an uninformative model scores ~0.445 here; drawing 0.5 as the reference
marked six combinations as skilful when two are.

PyGMT and geopandas are only imported inside :func:`maps`, so a machine
without the GMT C library can still render the charts and heatmaps.
"""
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.viz._style import (
    MONTHS as MON, NODATA, despine as _despine, style_ctx as _shared_ctx)
from geocif.viz.aggregation import _write_lookup

logger = logging.getLogger(__name__)

REGION = [-20, 52, -36, 25]
PROJ = "M15c"
# FEWS NET ENSO-forecast ramp: teal (low probability) -> cream (the 0.33
# climatological tercile) -> brown (high).
FEWS_CPT = [
    (0.15, "#01665e"), (0.20, "#35978f"), (0.25, "#80cdc1"),
    (0.30, "#c7eae5"), (0.35, "#f5f0e1"), (0.40, "#dfc27d"),
    (0.45, "#bf812d"), (0.50, "#8c510a"),
]
# Per-region ROC. Diverging on 0.5 (no discrimination), with the 0.6
# skill bar falling on a colour break so it reads off the bar.
ROC_CPT = [(0.2, "#762a83"), (0.3, "#9970ab"), (0.4, "#c2a5cf"),
           (0.45, "#e7d4e8"), (0.5, "#f7f7f7"), (0.55, "#d9f0d3"),
           (0.6, "#a6dba0"), (0.7, "#5aae61"), (0.8, "#1b7837")]
OOS_CPT = [(0, "#ffffcc"), (2, "#ffeda0"), (4, "#fed976"), (6, "#feb24c"),
           (9, "#fd8d3c"), (12, "#f03b20"), (20, "#bd0026"), (30, "#7a0177")]
# Predicted yield anomaly, % vs trend. Same brown=bad / teal=good sense as
# the FEWS probability ramp so the two maps read together, and reversed
# relative to it because here a NEGATIVE value is the bad one.
ANOM_CPT = [(-50, "#8c510a"), (-40, "#bf812d"), (-30, "#dfc27d"),
            (-20, "#e8d9a8"), (-10, "#f5f0e1"), (0, "#f5f0e1"),
            (10, "#c7eae5"), (20, "#80cdc1"), (30, "#35978f"),
            (40, "#01665e"), (50, "#01443e")]
YIELD_CPT = [(0, "#fff7ec"), (0.5, "#fee8c8"), (1.0, "#fdd49e"),
             (1.5, "#fdbb84"), (2.0, "#fc8d59"), (3.0, "#ef6548"),
             (4.0, "#d7301f"), (6.0, "#990000")]
# Transparent pattern BACKGROUND (+b-) is the whole trick: with +bwhite the
# hatch is opaque and wipes out the choropleth underneath. Low +r = coarse,
# open hatch, so the fill still reads through the gaps.
# +r sets the pattern resolution: a COARSE hatch (low dpi) skips
# small polygons entirely — a 40 km district can fall between two
# lines and render as though it had no verdict. 300 dpi puts
# several lines across the smallest admin unit in the set.
NOSKILL_PATTERN = "p8+r300+fblack+b-"
# Legends go BELOW the frame, not inside it. `JBL+jBL` put the box in the
# open Atlantic on the continent-wide extent, but the same anchor lands on
# the Western Cape once the map is cropped to southern Africa — a legend
# box sitting over a forecast region hides the thing the map is for.
# 0.9c, not 0.25c: the frame's longitude annotations occupy the first
# ~0.6c below it, and a smaller offset put the box on top of "10E"/"20E".
LEGEND_POS = "JBL+jTL+o0c/0.9c+w{w}c"
# ...which pushes the shared colorbar down to clear the legend.
CBAR_OFFSET = "+o0c/3.3c+e"
#: Land outside the analysis. Near-white so the map reads as open ground the
#: way the single-country outlook maps do, but not white, which reads as
#: water. Distinct from NODATA, which means "admin unit in the analysis with
#: no forecast this cycle" and is the darker grey the legend names.
LAND = "#f2f2f2"
#: t/ha map: units whose trend baseline extrapolates too far to publish.
WITHHELD = "#bdbdbd"
# LEGACY fallback only (_predictor_heatmaps_legacy): the panel path
# reads the era from predictors.csv, which the experiment derives
# per combination via real_harvest_years().
REAL_YEARS = list(range(1994, 2018))
ROW_LABEL = {"z_PRCPTOT": "Season rainfall", "z_TMEAN": "Season temperature",
             "z_P_GF": "Grain-fill rainfall",
             "DRYHEAT": "Dry × hot (interaction)"}


# ---------------------------------------------------------------------------
# shared helpers
# ---------------------------------------------------------------------------
def _dirs(out, family):
    base = Path(out) / "figures" / family
    plots, csvs = base / "plots", base / "csvs"
    for d in (plots, csvs):
        d.mkdir(parents=True, exist_ok=True)
    return base, plots, csvs


_NON_INTERACTIVE = ("agg", "pdf", "svg", "ps", "cairo", "template")


def _use_agg():
    """Force a headless backend before any figure is created.

    Without this matplotlib picks up TkAgg from the environment and every
    savefig goes through a GUI toolkit: slow, and flaky enough under load
    that figures intermittently fail to appear (two file-existence tests
    failed only when the whole suite ran together). Rendering here is always
    to disk, so an interactive backend is never wanted.
    """
    import matplotlib

    if matplotlib.get_backend().lower() not in _NON_INTERACTIVE:
        matplotlib.use("Agg", force=True)


def _style_ctx():
    """Headless backend, then the shared scienceplots-or-default context."""
    _use_agg()
    return _shared_ctx()


def month_span(months):
    """'Nov–Feb' for a contiguous run, the single name when there is one."""
    if not months:
        return ""
    names = [MON[m - 1] for m in months]
    return f"{names[0]}–{names[-1]}" if len(names) > 1 else names[0]


def row_label(feat, season_mon, grainfill_mon):
    """Two-line y label: the predictor, then the months it aggregates."""
    name = ROW_LABEL.get(feat, feat)
    if feat in ("z_PRCPTOT", "z_TMEAN"):
        return f"{name}\n({month_span(season_mon)})"
    if feat == "z_P_GF":
        return f"{name}\n({month_span(grainfill_mon)})"
    return name                          # the interaction spans both windows


# ---------------------------------------------------------------------------
# charts
# ---------------------------------------------------------------------------
def charts(out):
    """Risk ranking beside skill, skill vs lead, spread, support, coverage."""
    _use_agg()
    import matplotlib.pyplot as plt

    out = Path(out)
    base, dir_plots, dir_csvs = _dirs(out, "charts")
    fc = pd.read_csv(out / "forecasts.csv")
    sk = pd.read_csv(out / "skill.csv")
    cb = pd.read_csv(out / "combinations.csv")
    if fc.empty:
        logger.info("no forecasts to chart")
        return base
    fc["combo"] = fc["country"] + " · " + fc["crop"]
    lookup = []

    def save(fig, name, csv_name, desc):
        fig.savefig(dir_plots / f"{name}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        lookup.append((f"{name}.png", csv_name, desc))

    spec = {"mean_P_low": ("P_low", "mean"), "min_P_low": ("P_low", "min"),
            "max_P_low": ("P_low", "max"), "units": ("fnid", "size"),
            "auc": ("skill_auc", "first"), "beats": ("beats_trend", "first")}
    for name, col, how in (("null_auc", "null_auc", "first"),
                           ("perm_p", "perm_p", "first"),
                           ("has_skill", "has_skill", "first"),
                           ("oos", "oos_max_sigma", "max")):
        if col in fc.columns:
            spec[name] = (col, how)
    agg = fc.groupby("combo").agg(**spec).sort_values("mean_P_low")
    agg.round(4).to_csv(dir_csvs / "risk_ranking.csv")
    has_skill = "has_skill" in agg.columns

    # -- fig 1: risk beside skill, shared y so one is never read without the other
    with _style_ctx():
        fig, (ax, ax2) = plt.subplots(
            1, 2, figsize=(9.6, 0.34 * len(agg) + 1.6), sharey=True,
            gridspec_kw={"width_ratios": [2.1, 1.2]})
        y = np.arange(len(agg))
        ax.barh(y, agg["mean_P_low"], height=0.6, color="#c0392b", alpha=.85)
        ax.hlines(y, agg["min_P_low"], agg["max_P_low"], color="#4d4d4d",
                  lw=1.1)
        ax.axvline(1 / 3, color="0.4", lw=0.9, ls="--")
        ax.set_yticks(y, agg.index)
        ax.set_xlim(0, 1)
        ax.set_xlabel("P(bottom tercile), mean of admin units")
        ax.set_title("Pre-season risk", loc="left")

        if "null_auc" in agg.columns:
            ax2.hlines(y, agg["null_auc"], agg["auc"], color="0.75", lw=1.0,
                       zorder=1)
            ax2.scatter(agg["null_auc"], y, s=18, marker="|", color="0.45",
                        zorder=2, label="permutation null")
        fill = (["#1b7837" if h else "#b0b0b0" for h in agg["has_skill"]]
                if has_skill else "#b0b0b0")
        ax2.scatter(agg["auc"], y, s=30, c=fill, zorder=3,
                    label="hindcast AUC (green: beats its null, p<0.05)")
        ax2.set_xlim(0.15, 0.8)
        ax2.set_xlabel("Bad-year discrimination (AUC)")
        ax2.set_title("Skill at the issued lead", loc="left")
        ax2.legend(loc="lower right", fontsize=7, frameon=False)
        _despine(ax, ax2)
        save(fig, "risk_ranking", "risk_ranking.csv",
             "risk per combination beside its hindcast AUC and permutation null")

    # -- fig 2: skill against lead time
    s = sk.dropna(subset=["auc"]).copy()
    s["combo"] = s["country"] + " · " + s["crop"]
    piv = s.pivot_table(index="offset", columns="combo", values="auc")
    piv.round(4).to_csv(dir_csvs / "skill_vs_lead.csv")
    null_mean = (float(agg["null_auc"].mean())
                 if "null_auc" in agg.columns else None)
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(5.6, 3.7))
        for c in piv.columns:
            ax.plot(piv.index, piv[c], color="0.78", lw=1.0, marker="o", ms=2.5)
        med = piv.median(axis=1)
        ax.plot(med.index, med.values, color="#1f4e79", lw=2.2, marker="o",
                ms=5, label="median across combinations")
        if null_mean and np.isfinite(null_mean):
            ax.axhline(null_mean, color="#c0392b", lw=1.3, ls="--",
                       label=f"permutation null ({null_mean:.3f})")
        ax.axhline(0.5, color="0.6", lw=0.8, ls=":", label="AUC 0.5")
        ax.set_xticks(sorted(piv.index))
        ax.set_xlabel("Months before planting (forecast issue)")
        ax.set_ylabel("Hindcast AUC")
        ax.set_title("Bad-year discrimination by lead time", loc="left")
        ax.legend(loc="lower left", fontsize=7, frameon=False)
        _despine(ax)
        save(fig, "skill_vs_lead", "skill_vs_lead.csv",
             "AUC vs lead per combination, against the permutation null")

    # -- fig 2b: the two abilities the pooled AUC conflates
    if {"auc_national", "auc_spatial"} <= set(fc.columns):
        spec2 = {}
        for c in ("auc", "auc_national", "auc_spatial", "null_auc",
                  "null_auc_national", "null_auc_spatial", "perm_p",
                  "perm_national_p", "perm_spatial_p", "n_years"):
            if c in fc.columns:
                spec2[c] = (c, "first")
        dec = fc.groupby("combo").agg(**spec2)
        dec = dec.sort_values("auc_national", ascending=True)
        dec.round(4).to_csv(dir_csvs / "skill_decomposition.csv")
        with _style_ctx():
            fig, axes = plt.subplots(
                1, 2, figsize=(8.8, 0.34 * len(dec) + 1.6), sharey=True)
            y = np.arange(len(dec))
            for ax, (col, nul, pv, ttl) in zip(axes, (
                    ("auc_national", "null_auc_national", "perm_national_p",
                     "National: which YEARS are bad"),
                    ("auc_spatial", "null_auc_spatial", "perm_spatial_p",
                     "Spatial: which REGIONS, within a year"))):
                if nul in dec.columns:
                    ax.hlines(y, dec[nul], dec[col], color="0.75", lw=1.0,
                              zorder=1)
                    ax.scatter(dec[nul], y, s=18, marker="|", color="0.45",
                               zorder=2)
                sig = (dec[pv] < 0.05) if pv in dec.columns else False
                ax.scatter(dec[col], y, s=30, zorder=3,
                           c=["#1b7837" if s else "#b0b0b0" for s in sig]
                           if pv in dec.columns else "#b0b0b0")
                ax.set_xlim(0.05, 0.95)
                ax.set_xlabel("AUC")
                ax.set_title(ttl, loc="left", fontsize=9)
                _despine(ax)
            axes[0].set_yticks(y, dec.index)
            save(fig, "skill_decomposition", "skill_decomposition.csv",
                 "national vs spatial skill, each against its own null "
                 "(green: p<0.05)")

    # -- fig 3: within-country spread of unit-level risk
    order = agg.index.tolist()
    data = [fc.loc[fc.combo == c, "P_low"].values for c in order]
    pd.concat([fc[fc.combo == c][["combo", "fnid", "P_low"]] for c in order]
              ).to_csv(dir_csvs / "risk_spread.csv", index=False)
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(7.4, 0.32 * len(order) + 1.4))
        bp = ax.boxplot(data, vert=False, widths=.55, patch_artist=True,
                        medianprops=dict(color="#1f1f1f"), showfliers=False)
        for p in bp["boxes"]:
            p.set_facecolor("#d5e3ef")
            p.set_edgecolor("#4d4d4d")
        for i, d in enumerate(data):
            ax.scatter(d, np.full(len(d), i + 1) + np.random.default_rng(i)
                       .normal(0, .07, len(d)), s=7, color="#c0392b",
                       alpha=.55, zorder=3)
        ax.axvline(1 / 3, color="0.4", lw=0.9, ls="--")
        ax.set_yticks(range(1, len(order) + 1), order)
        ax.set_xlim(0, 1)
        ax.set_xlabel("P(bottom tercile) per admin unit")
        ax.set_title("Spread of risk within each country", loc="left")
        _despine(ax)
        save(fig, "risk_spread", "risk_spread.csv",
             "per-unit P(bottom tercile) distribution within each combination")

    # -- fig 4: how far outside training support the predictors sat
    if "oos" in agg.columns:
        o = agg.sort_values("oos")
        o[["oos"]].round(2).to_csv(dir_csvs / "out_of_support.csv")
        with _style_ctx():
            fig, ax = plt.subplots(figsize=(6.4, 0.32 * len(o) + 1.4))
            ax.barh(np.arange(len(o)), o["oos"], height=.6, color="#8c510a",
                    alpha=.85)
            ax.axvline(1.0, color="0.4", lw=0.9, ls="--")
            ax.set_yticks(np.arange(len(o)), o.index)
            ax.set_xlabel(
                "Worst predictor exceedance of the training range (sd)")
            ax.set_title("Forecast predictors outside the fitted range",
                         loc="left")
            _despine(ax)
            save(fig, "out_of_support", "out_of_support.csv",
                 "worst predictor exceedance of training support, per combination")

    # -- fig 5: coverage of the HarvestStat footprint
    cnt = cb["status"].value_counts()
    cnt.rename_axis("status").reset_index(name="combinations").to_csv(
        dir_csvs / "coverage.csv", index=False)
    lbl = {"forecast": "forecast", "too_early": "window not open yet",
           "in_season": "season under way", "too_short": "history too short",
           "no_init": "no published init", "no_calendar": "no crop calendar",
           "no_s2s": "no S2S data", "no_join": "units do not join",
           "no_hindcast": "no scorable hindcast", "no_trend": "no trend",
           "no_train": "training pool too small"}
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(5.6, 2.9))
        c2 = cnt.sort_values()
        cols = ["#1b7837" if i == "forecast" else "#b0b0b0" for i in c2.index]
        ax.barh([lbl.get(i, i) for i in c2.index], c2.values, color=cols,
                height=.62)
        ax.set_xlabel("Country × crop × season combinations")
        ax.set_title("Coverage of the HarvestStat footprint", loc="left")
        _despine(ax)
        save(fig, "coverage", "coverage.csv",
             "why each HarvestStat combination is or is not forecastable")

    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"charts -> {base} ({len(lookup)} figures)")
    return base


# ---------------------------------------------------------------------------
# maps
# ---------------------------------------------------------------------------
def _write_cpt(path, stops):
    """Continuous CPT with over/under set so clipped tails stay visible.

    Each segment interpolates between its two stop colours (`lo cA hi cB`)
    rather than repeating one (`lo cA hi cA`, the stepped form this used to
    write). The single-country outlook maps carry a smooth ramp, and a
    stepped bar beside a smooth one reads as a different product.
    """
    lines = [f"{lo}\t{ca}\t{hi}\t{cb}"
             for (lo, ca), (hi, cb) in zip(stops[:-1], stops[1:])]
    lines += [f"B\t{stops[0][1]}", f"F\t{stops[-1][1]}", f"N\t{NODATA}"]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def defensible_baseline(frame, max_err):
    """Units whose trend baseline is good enough to publish a t/ha number.

    Module level, not a closure inside :func:`maps`, so it is reachable
    without GMT: everything else in the t/ha map runs inside pygmt, and a
    mask that decides which units are shown at all should not be testable
    only on a machine that can render.

    NaN means "no defensible baseline" — the same statement as exceeding
    ``max_err``, so both fall outside. A bare ``> max_err`` filter drops
    NaN units from the shown AND withheld layers, and they then render as
    land outside the analysis.
    """
    err = frame["trend_extrap_err_pct"]
    return err.notna() & (err <= max_err)


def maps(out, gpkg, title_year=None, extent=None, label=""):
    """PyGMT choropleths, per crop and diagnostic.

    Per crop: P(lower tercile) — the classification product; predicted
    departure from trend — the regression product, which needs no absolute
    level; and predicted t/ha, withheld wherever the trend baseline has to
    be extrapolated too far to mean anything. Plus the out-of-support and
    coverage diagnostics.
    """
    import tempfile

    import geopandas as gpd
    import pygmt

    from geocif.experiments.s2s_africa import TREND_EXTRAP_MAX_PCT
    # Imported HERE, not at module scope: _pygmt_render imports pygmt at its
    # top (it doubles as a standalone subprocess renderer), and this module
    # must stay importable on a machine with no GMT so the charts and
    # heatmaps still render. The style constants come from the GMT-free
    # viz/_style, so nothing pygmt-shaped is needed at module scope.
    from geocif.viz._style import BORDER_PEN, CBAR_POS, COAST_KW, POLY_PEN

    out = Path(out)
    base, dir_plots, dir_csvs = _dirs(out, "maps")
    # The extent comes from the run's config ([ML] s2s_map_extent), so a
    # regional config crops its own maps. Falls back to all of Africa.
    extent, proj, sfx = (extent or REGION), PROJ, ""
    where = f" in {label}" if label else ""
    fc = pd.read_csv(out / "forecasts.csv")
    cb = pd.read_csv(out / "combinations.csv")
    if fc.empty:
        logger.info("no forecasts to map")
        return base
    year = title_year or int(fc["harvest_year"].mode().iloc[0])
    # ADMIN1/ADMIN2 ride along for the per-map CSVs, which is where a reader
    # looks up which region a polygon is. They are deliberately NOT drawn on
    # the map: see the note on annotations above _value_map.
    gdf = gpd.read_file(gpkg)[
        ["FNID", "ADMIN0", "ADMIN1", "ADMIN2", "geometry"]].rename(
        columns={"FNID": "fnid"})
    lookup = []

    def basemap(fig, title):
        # Default (fancy) frame and the shared coast styling, so these read
        # as the same product as the single-country outlook maps. `land` is
        # ours: those maps cover one country and leave everything else white,
        # but this one spans a continent and white would read as ocean.
        # Only the title is overridden. FONT_LABEL / FONT_ANNOT_PRIMARY keep
        # their GMT defaults so the colorbar label and axis annotations are
        # the same size as on the single-country outlook maps; the title is
        # shrunk because these carry a crop, a region and a year, where the
        # outlook titles carry one metric.
        pygmt.config(FONT_TITLE="15p,Helvetica,black")
        fig.basemap(region=extent, projection=proj,
                    frame=["af", f"+t{title}"])
        fig.coast(land=LAND, water="white", **COAST_KW)

    def finish(fig, stem, csv_name, desc):
        # National borders drawn last and heavier than the admin-unit pens, so
        # the country outline stays legible over a dense choropleth.
        fig.coast(borders=BORDER_PEN, area_thresh=5000)
        fig.savefig(dir_plots / f"{stem}.png", dpi=350)
        lookup.append((f"{stem}.png", csv_name, desc))

    def _hatch_by_region(fig, frame, td):
        """Mark each polygon on ITS OWN verdict, not the country's.

        A country-level flag paints every region with one brush: South
        Africa was stamped "no skill" wholesale even though four Highveld
        provinces carry the signal. region_skill is computed per region on
        its own timeline, with an explicit third state for regions holding
        too few low-tercile years to score.
        """
        col = "region_skill" if "region_skill" in frame.columns else None
        if col is None:                       # older outputs: fall back
            if "has_skill" not in frame.columns:
                return
            frame = frame.assign(region_skill=np.where(
                frame["has_skill"].astype(bool), "skill", "no_skill"))
            col = "region_skill"
        sub = frame[frame[col] == "no_skill"]
        if sub.empty:
            return
        f = Path(td) / "noskill.gmt"
        sub[["fnid", "geometry"]].to_file(f, driver="OGR_GMT")
        fig.plot(data=str(f), fill=NOSKILL_PATTERN, pen=POLY_PEN,
                 close=True)

    def _sq(fill, text):
        """One legend row: a filled square beside its meaning."""
        return f"S 0.3c s 0.32c {fill} 0.2p,gray40 0.75c {text}"

    BASE_LEGEND = [_sq(NODATA, "No forecast or data available"),
                   _sq(NOSKILL_PATTERN, "No forecast skill at this lead")]

    def _legend(fig, td, rows, width):
        spec = Path(td) / "legend.txt"
        spec.write_text("\n".join(["G 0.05c"] + rows) + "\n",
                        encoding="utf-8")
        fig.legend(spec=str(spec), position=LEGEND_POS.format(w=width),
                   box="+gwhite+p0.4p,gray50")

    def _join(d, csv_name, nd=4):
        """Merge onto the boundary frame and write the companion CSV."""
        g = gdf.merge(d, on="fnid", how="inner")
        if g.empty:
            return None
        tab = g.drop(columns="geometry")
        (tab.round(nd) if nd else tab).to_csv(dir_csvs / csv_name,
                                              index=False)
        return g

    def _value_map(g, *, stem, title, value_col, cpt_stops, cbar_label,
                   csv_name, desc, hatch=True,
                   legend_rows=None, legend_w=6.6, withheld=None):
        """The one shape every value choropleth shares.

        CPT -> polygons coloured by ``value_col`` -> per-region hatch ->
        centroid labels -> colorbar -> legend. The five value maps differ
        only in these parameters, so the shape lives once and a styling fix
        lands on all of them.
        """
        fig = pygmt.Figure()
        basemap(fig, title)
        with tempfile.TemporaryDirectory() as td:
            cpt = Path(td) / "v.cpt"
            _write_cpt(cpt, cpt_stops)
            if withheld is not None and not withheld.empty:
                # under the choropleth, so a unit both withheld and coloured
                # can never happen silently — the caller splits the frame
                w = Path(td) / "held.gmt"
                withheld[["fnid", "geometry"]].to_file(w, driver="OGR_GMT")
                fig.plot(data=str(w), fill=WITHHELD, pen=POLY_PEN,
                         close=True)
            poly = Path(td) / "poly.gmt"
            g[["fnid", value_col, "geometry"]].to_file(poly,
                                                       driver="OGR_GMT")
            fig.plot(data=str(poly), fill="+z", cmap=str(cpt), pen=POLY_PEN,
                     close=True, aspatial=f"Z={value_col}")
            if hatch:
                _hatch_by_region(fig, g, td)
            # no legend to clear -> the bar keeps the tight default offset;
            # +e extenders stay on either way, the tails carry real values
            fig.colorbar(cmap=str(cpt), frame=f"x+l{cbar_label}",
                         position=CBAR_POS + (CBAR_OFFSET if legend_rows
                                              else "+e"))
            if legend_rows:
                _legend(fig, td, legend_rows, legend_w)
        finish(fig, stem, csv_name, desc)

    def choropleth(crop):
        d = fc[fc.crop == crop]
        if d.empty:
            return
        d = (d.sort_values("P_low", ascending=False).drop_duplicates("fnid")
             .filter(items=["fnid", "country", "season_name", "P_low",
                            "P_mid", "P_high", "ahat", "offset_used",
                            "skill_auc", "null_auc", "perm_p", "has_skill",
                            "in_support", "oos_max_sigma", "n_clipped",
                            "oos_feature", "region_auc", "region_r2",
                            "region_n_low", "region_skill"]))
        csv_name = f"map_p_low_{crop}{sfx}.csv"
        g = _join(d, csv_name)
        if g is None:
            return
        _value_map(
            g, stem=f"map_p_low_{crop}{sfx}", csv_name=csv_name,
            title=f"Probability of lower tercile {crop} yields{where}, "
                  f"{year}",
            value_col="P_low", cpt_stops=FEWS_CPT,
            cbar_label="Probability of lower tercile crop yields",
            legend_rows=BASE_LEGEND,
            desc=f"P(lower tercile) {crop} {year}, hatched where skill "
                 f"fails")

    def anomaly_map(crop):
        """The regression prediction: % departure from trend per unit.

        This is the honest regression product — it needs no absolute yield
        level, so it is publishable everywhere the classification map is.
        """
        d = fc[fc.crop == crop]
        if d.empty or "ahat" not in d.columns:
            return
        d = (d.sort_values("ahat").drop_duplicates("fnid")
             .filter(items=["fnid", "country", "season_name", "ahat",
                            "r2", "perm_r2_p", "r2_within",
                            "perm_r2_within_p", "has_skill", "in_support",
                            "oos_max_sigma", "region_auc", "region_r2",
                            "region_n_low", "region_skill"]).copy())
        d["ahat_pct"] = (100 * d["ahat"]).round(1)
        csv_name = f"map_anomaly_{crop}{sfx}.csv"
        g = _join(d, csv_name)
        if g is None:
            return
        _value_map(
            g, stem=f"map_anomaly_{crop}{sfx}", csv_name=csv_name,
            title=f"Predicted {crop} yield departure from trend{where}, "
                  f"{year}",
            value_col="ahat_pct", cpt_stops=ANOM_CPT,
            cbar_label="Predicted yield departure from trend (%)",
            legend_rows=BASE_LEGEND,
            desc=f"predicted {crop} yield anomaly {year}, % vs trend")

    def yield_map(crop, max_err=TREND_EXTRAP_MAX_PCT):
        """Predicted yield in t/ha — only where the baseline is defensible.

        A t/ha number needs a trend level for the forecast season, and these
        records end from 2010 to 2024. Where the backtested extrapolation
        error exceeds ``max_err`` the number is dominated by not knowing the
        baseline rather than by the climate signal, so those units are drawn
        as withheld rather than coloured. Skipped entirely if nothing
        qualifies, so the map never implies coverage it does not have.
        """
        if "yhat_tha" not in fc.columns:
            return
        d = fc[fc.crop == crop].dropna(subset=["yhat_tha"])
        if d.empty:
            return
        d = d.sort_values("yhat_tha").drop_duplicates("fnid")
        if not defensible_baseline(d, max_err).any():
            logger.info(f"no {crop} combination has a trend extrapolation "
                        f"within {max_err}% — t/ha map skipped")
            return
        d = d.filter(items=["fnid", "country", "season_name", "ahat",
                            "trend_tha", "yhat_tha", "extrap_years",
                            "trend_extrap_err_pct", "has_skill"])
        csv_name = f"map_yield_tha_{crop}{sfx}.csv"
        g = _join(d, csv_name)
        if g is None:
            return
        ok_g = defensible_baseline(g, max_err)
        _value_map(
            g[ok_g], withheld=g[~ok_g],
            stem=f"map_yield_tha_{crop}{sfx}", csv_name=csv_name,
            title=f"Predicted {crop} yield{where}, {year}",
            value_col="yhat_tha", cpt_stops=YIELD_CPT,
            cbar_label="Predicted yield (t/ha)",
            legend_rows=[BASE_LEGEND[0],
                         _sq(WITHHELD, "Withheld: trend baseline "
                                       "extrapolated too far"),
                         BASE_LEGEND[1]],
            legend_w=8.0,
            desc=f"predicted {crop} yield t/ha {year}, withheld where the "
                 f"trend baseline extrapolates beyond {max_err}%")

    def region_roc_map(crop):
        """Per-region hindcast ROC — how well each polygon has been called.

        The companion to the forecast maps: those say what we expect, this
        says where the record supports expecting anything. Diverging on 0.5,
        with the 0.6 skill bar on a colour break. No hatch: the values ARE
        the verdict here.
        """
        if "region_auc" not in fc.columns:
            return
        d = fc[fc.crop == crop].dropna(subset=["region_auc"])
        if d.empty:
            return
        # Same dedup policy as the P_low map (worst P_low wins), so for the
        # 13 two-season countries every map describes the SAME chosen
        # forecast — an unsorted drop_duplicates left the row shown to
        # whatever order the CSV happened to arrive in.
        d = (d.sort_values("P_low", ascending=False)
             .drop_duplicates("fnid")
             .filter(items=["fnid", "country", "season_name", "region_auc",
                            "region_r2", "region_n_years", "region_n_low",
                            "region_skill"]))
        csv_name = f"map_region_roc_{crop}{sfx}.csv"
        g = _join(d, csv_name)
        if g is None:
            return
        _value_map(
            g, stem=f"map_region_roc_{crop}{sfx}", csv_name=csv_name,
            title=f"Hindcast skill by region, {crop}{where} ({year} lead)",
            value_col="region_auc", cpt_stops=ROC_CPT, hatch=False,
            cbar_label="Hindcast ROC for bottom-tercile years",
            legend_rows=BASE_LEGEND[:1], legend_w=7.4,
            desc=f"per-region hindcast ROC for bottom-tercile {crop} years")

    def season_map(crop):
        """Which season index was forecast for each country.

        HarvestStat carries a second season for 13 countries and only a
        first for the rest, and the season chosen sets the planting month,
        the aggregation window and the forecast leads — so it belongs on
        the page rather than buried in combinations.csv.
        """
        from geocif.experiments.s2s_africa import season_index

        d = fc[fc.crop == crop]
        if d.empty:
            return
        # dedup aligned with the P_low map (see region_roc_map) — this map's
        # entire message is WHICH season was forecast, so it must name the
        # season behind the probability the reader just looked at
        d = (d.sort_values("P_low", ascending=False).drop_duplicates("fnid")
             [["fnid", "country", "season_name"]].copy())
        d["season_idx"] = d.season_name.map(season_index)
        g = gdf.merge(d, on="fnid", how="inner")
        if g.empty:
            return
        csv_name = f"map_season_{crop}{sfx}.csv"
        g.drop(columns="geometry").to_csv(dir_csvs / csv_name, index=False)
        cols = {1: ("#2c6fa8", "Season 1 (primary)"),
                2: ("#c26a1b", "Season 2 (secondary)")}
        fig = pygmt.Figure()
        basemap(fig, f"Season forecast for each {crop} area{where}, {year}")
        with tempfile.TemporaryDirectory() as td:
            for idx, (col, _) in cols.items():
                sub = g[g.season_idx == idx]
                if sub.empty:
                    continue
                f = Path(td) / f"s{idx}.gmt"
                sub[["fnid", "geometry"]].to_file(f, driver="OGR_GMT")
                fig.plot(data=str(f), fill=col, pen=POLY_PEN, close=True)
            rows = []
            for idx, (col, lab) in cols.items():
                if int((g.season_idx == idx).sum()):
                    names = ", ".join(sorted(set(
                        g.loc[g.season_idx == idx, "season_name"])))
                    rows.append(_sq(col, f"{lab}: {names}"))
            rows.append(_sq(NODATA, "Not forecast this cycle"))
            _legend(fig, td, rows, 9.4)
        finish(fig, f"map_season_{crop}{sfx}", csv_name,
               f"which HarvestStat season was forecast for each {crop} area")

    def support_map():
        """How far outside the fitted range the forecast predictors sat.

        ``in_support`` can be False everywhere, in which case the binary flag
        carries no spatial information and only the magnitude does. No hatch
        and no legend: a diagnostic, not a forecast.
        """
        if "oos_max_sigma" not in fc.columns:
            return
        d = (fc.sort_values("oos_max_sigma", ascending=False)
               .drop_duplicates("fnid")[["fnid", "country", "crop",
                                         "season_name", "oos_max_sigma",
                                         "oos_feature", "n_clipped"]])
        csv_name = f"map_out_of_support{sfx}.csv"
        g = _join(d, csv_name, nd=3)
        if g is None:
            return
        _value_map(
            g, stem=f"map_out_of_support{sfx}", csv_name=csv_name,
            title=f"Distance of the {year} S2S predictors outside "
                  f"training range{where}",
            value_col="oos_max_sigma", cpt_stops=OOS_CPT,
            hatch=False,
            cbar_label="Standard deviations beyond the training range",
            desc="worst per-unit predictor exceedance of the training "
                 "range, in sd")

    def coverage_map():
        st = cb.groupby("country")["status"].apply(
            lambda s: "forecast" if (s == "forecast").any()
            else ("in_season" if (s == "in_season").any() else "not_forecast"))
        tab = st.rename("coverage").reset_index()
        csv_name = f"map_coverage{sfx}.csv"
        tab.to_csv(dir_csvs / csv_name, index=False)
        cols = {"forecast": ("#1b7837", "forecast issued"),
                "in_season": ("#7fb3d5", "season already under way"),
                "not_forecast": (NODATA, "not forecastable yet")}
        g = gdf.merge(tab, left_on="ADMIN0", right_on="country", how="left")
        fig = pygmt.Figure()
        basemap(fig, f"Pre-season forecast coverage{where}, {year}")
        for key, (col, _) in cols.items():
            sub = g[g["coverage"] == key]
            if not sub.empty:
                fig.plot(data=sub[["geometry"]], fill=col, pen=POLY_PEN,
                         close=True)
        with tempfile.TemporaryDirectory() as td:
            _legend(fig, td, [_sq(c, lab) for c, lab in cols.values()],
                    5.4)
        finish(fig, f"map_coverage{sfx}", csv_name,
               "which HarvestStat country x crop x season could be forecast")

    for crop in sorted(fc["crop"].unique()):
        choropleth(crop)      # classification: P(lower tercile)
        anomaly_map(crop)     # regression: % vs trend
        yield_map(crop)       # regression: t/ha, where the baseline holds
        region_roc_map(crop)  # where the record supports a call at all
        season_map(crop)      # which season index was forecast
    support_map()
    coverage_map()
    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"maps -> {base} ({len(lookup)} figures)")
    return base


# ---------------------------------------------------------------------------
# predictor heatmaps
# ---------------------------------------------------------------------------
def _draw_heatmap(m, feats, years, real_years, smon, gfm, title, stem,
                  dir_plots, dir_csvs):
    """One predictor-by-year heatmap. Shared by the panel and legacy paths.

    Scale to the HISTORICAL spread, not the full range: the forecast year
    can sit several sigma outside anything on record, and letting it set
    the scale flattens two decades of history into a uniform pale block.
    The forecast column saturates and the colourbar arrows make that
    visible.
    """
    import matplotlib.pyplot as plt

    data = m[feats].T.to_numpy(dtype=float)
    hist = m.loc[[y for y in years if y in real_years],
                 feats].to_numpy(dtype=float)
    vmax = (float(np.nanpercentile(np.abs(hist), 98))
            if np.isfinite(hist).any() else 1.0)
    vmax = max(vmax, 0.5)
    with _style_ctx():
        fig, ax = plt.subplots(
            figsize=(max(6.2, 0.30 * len(years) + 3.4),
                     0.62 * len(feats) + 1.9))
        im_ = ax.imshow(data, cmap="RdBu", vmin=-vmax, vmax=vmax,
                        aspect="auto", interpolation="nearest")
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels([str(y) for y in years], rotation=90,
                           fontsize=8.5)
        ax.set_yticks(range(len(feats)))
        ax.set_yticklabels([row_label(f, smon, gfm) for f in feats],
                           fontsize=10)
        for lb in ax.get_yticklabels():
            lb.set_linespacing(1.35)
        ax.axvline(len(years) - 1.5, color="black", lw=1.6)
        ax.set_title(title, loc="left", fontsize=11)
        cbar = fig.colorbar(im_, ax=ax, pad=0.015, fraction=0.03,
                            extend="both")
        cbar.set_label(
            f"Z-score vs {min(real_years)}\u2013{max(real_years)} "
            f"S2S hindcast", fontsize=9)
        cbar.ax.tick_params(labelsize=8)
        ax.set_xlabel("Harvest year", fontsize=9)
        fig.savefig(dir_plots / f"{stem}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
    m.round(4).to_csv(dir_csvs / f"{stem}.csv")


def _heatmap_stem(country, crop, season):
    return (f"{country.replace(' ', '_').replace(',', '')}_{crop}_"
            f"{season.replace('/', '_')}")


def predictor_heatmaps(out, root, hvstat_csv, threshold_dir="crop_t0"):
    """Per combination, the model's predictors by year beside the forecast.

    Renders from the ``predictors.csv`` panel the experiment writes, so
    the heatmaps show exactly the features the model was fitted on. Only
    real-hindcast years are shown plus the forecast year: the 2017+
    seasons are climatology gap-fill in the NOAA archive -- every year
    identical by construction -- so plotting them would show a flat band
    that looks like signal and is not (the panel tags them
    ``climatology_fill``).

    Outputs written before 0.4.1022 carry no panel; those fall back to
    recomputing the features in-place, with a warning, so an old run
    directory stays renderable.
    """
    _use_agg()
    out = Path(out)
    panel_csv = out / "predictors.csv"
    if not panel_csv.exists():
        logger.warning(
            f"{panel_csv} not found (pre-0.4.1022 output) -- falling back "
            f"to recomputing predictors in the viz layer; rerun the "
            f"experiment to render from the persisted panel")
        return _predictor_heatmaps_legacy(out, root, hvstat_csv,
                                          threshold_dir)

    base, dir_plots, dir_csvs = _dirs(out, "predictor_heatmaps")
    panel = pd.read_csv(panel_csv)
    cb = pd.read_csv(out / "combinations.csv")
    cb = cb[cb.status == "forecast"].set_index(
        ["country", "crop", "season_name"])
    tidy, lookup = [], []

    for (country, crop, season), sub in panel.groupby(
            ["country", "crop", "season_name"], sort=True):
        shown = sub[sub.kind.isin(["hindcast", "forecast"])]
        real_years = sorted(shown.loc[shown.kind == "hindcast", "year"]
                            .unique())
        fc_years = sorted(shown.loc[shown.kind == "forecast", "year"]
                          .unique())
        if not real_years or not fc_years:
            continue
        years = real_years + fc_years
        feats = list(pd.unique(sub.predictor))
        m = (shown.pivot_table(index="year", columns="predictor",
                               values="value", aggfunc="first")
             .reindex(years).reindex(columns=feats))
        m.index.name = "year"
        off = int(sub["offset"].iloc[0])
        n_units = int(sub["n_units"].iloc[0])
        for f in feats:
            for y in years:
                v = m.loc[y, f]
                tidy.append({"country": country, "crop": crop,
                             "season_name": season, "offset": off,
                             "predictor": f, "year": int(y),
                             "value": (float(v) if np.isfinite(v)
                                       else np.nan),
                             "n_units": n_units})

        smon = [int(x) for x in
                str(sub["season_months"].iloc[0]).split(",") if x]
        gfm = [int(x) for x in
               str(sub["gf_months"].iloc[0]).split(",") if x]
        iy, im = int(sub["init_year"].iloc[0]), int(sub["init_month"].iloc[0])
        try:
            r = cb.loc[(country, crop, season)]
        except KeyError:
            logger.warning(f"panel combination {country}/{crop}/{season} "
                           f"missing from combinations.csv -- skipped")
            continue
        hy = int(fc_years[-1])
        plant_m, harv_m = int(r.planting_month), int(r.harvest_month)
        plant_y = hy - 1 if bool(r.wraps) else hy
        title = (f"{country} \u00b7 {crop.capitalize()} \u00b7 {season} "
                 f"season \u2014 planted {MON[plant_m - 1]} {plant_y}, "
                 f"harvested {MON[harv_m - 1]} {hy} "
                 f"(S2S init {MON[im - 1]} {iy})")
        stem = _heatmap_stem(country, crop, season)
        _draw_heatmap(m, feats, years, real_years, smon, gfm, title, stem,
                      dir_plots, dir_csvs)
        lookup.append((f"{stem}.png", f"{stem}.csv",
                       f"{country} {crop.capitalize()} {season} \u2014 S2S "
                       f"predictors, init {MON[im - 1]} {iy}"))

    pd.DataFrame(tidy).round(4).to_csv(
        dir_csvs / "predictor_values_all.csv", index=False)
    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"predictor heatmaps -> {base} ({len(lookup)} figures)")
    return base


def _predictor_heatmaps_legacy(out, root, hvstat_csv, threshold_dir):
    """Recompute-in-viz fallback for run directories without a panel.

    DEPRECATED: everything below duplicates the experiment pipeline and
    can drift from it (it did -- REAL_YEARS vs EVAL_SPAN); it exists only
    so pre-0.4.1022 output directories stay renderable.
    """
    from geocif.experiments.s2s_africa import (
        CROP_PRODUCTS, build_features, causal_trend_fnid, country_slug,
        features_for_offset, load_s2s_fnid, load_yields)
    from geocif.experiments.s2s_pooled_model import (
        init_calendar, lead_map, season_months)

    out, root = Path(out), Path(root)
    base, dir_plots, dir_csvs = _dirs(out, "predictor_heatmaps")
    cb = pd.read_csv(out / "combinations.csv")
    fcst = cb[cb.status == "forecast"]
    if fcst.empty:
        logger.info("no forecasts to draw heatmaps for")
        return base
    ylds = load_yields(hvstat_csv,
                       [p for ps in CROP_PRODUCTS.values() for p in ps])
    tidy, lookup = [], []

    for _, r in fcst.iterrows():
        country, crop, season = r.country, r.crop, r.season_name
        off, hy = int(r.offset_used), int(r.harvest_year)
        plant_m, wraps = int(r.planting_month), bool(r.wraps)
        slug = country_slug(country, root / threshold_dir)
        if slug is None:
            continue
        tp = load_s2s_fnid(root / threshold_dir / slug, "tprate")
        t2 = load_s2s_fnid(root / threshold_dir / slug, "t2m")
        if tp.empty or t2.empty:
            continue
        g = ylds[(ylds.country == country)
                 & ylds["product"].isin(CROP_PRODUCTS[crop])
                 & (ylds.season_name == season)]
        an = causal_trend_fnid(g[["fnid", "year", "obs"]])
        fnids = sorted(set(an.fnid) & set(tp.fnid))
        if len(fnids) < 5:
            continue
        feats = features_for_offset(off)
        years = REAL_YEARS + [hy]
        fx = build_features(tp, t2, plant_m, wraps, off, years, fnids)
        if fx.empty:
            continue
        m = fx.groupby("year")[feats].mean().reindex(years)
        m.index.name = "year"
        for f in feats:
            for y in years:
                v = m.loc[y, f] if y in m.index else np.nan
                tidy.append({"country": country, "crop": crop,
                             "season_name": season, "offset": off,
                             "predictor": f, "year": y,
                             "value": float(v) if np.isfinite(v) else np.nan,
                             "n_units": len(fnids)})

        lm = lead_map(plant_m, off)
        smon = [mth for mth in season_months(plant_m) if mth in lm]
        gfm = [mth for mth in season_months(plant_m)[2:4] if mth in lm]
        iy, im = init_calendar(plant_m, off, hy, wraps)
        plant_y = hy - 1 if wraps else hy
        harv_m = int(r.harvest_month)
        title = (f"{country} \u00b7 {crop.capitalize()} \u00b7 {season} "
                 f"season \u2014 planted {MON[plant_m - 1]} {plant_y}, "
                 f"harvested {MON[harv_m - 1]} {hy} "
                 f"(S2S init {MON[im - 1]} {iy})")
        stem = _heatmap_stem(country, crop, season)
        _draw_heatmap(m, feats, years, REAL_YEARS, smon, gfm, title, stem,
                      dir_plots, dir_csvs)
        lookup.append((f"{stem}.png", f"{stem}.csv",
                       f"{country} {crop.capitalize()} {season} \u2014 S2S "
                       f"predictors, init {MON[im - 1]} {iy}"))

    pd.DataFrame(tidy).round(4).to_csv(dir_csvs / "predictor_values_all.csv",
                                       index=False)
    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"predictor heatmaps -> {base} ({len(lookup)} figures)")
    return base


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------
def readme(out, version=None):
    """Write the run README, leading with the validity caveats."""
    out = Path(out)
    cb = pd.read_csv(out / "combinations.csv")
    fc = pd.read_csv(out / "forecasts.csv")
    ex = pd.read_csv(out / "excluded.csv")
    fcc = cb[cb.status == "forecast"].copy()
    if fcc.empty:
        logger.info("no forecasts to describe")
        return None

    def mean_p(r):
        return fc[(fc.country == r.country) & (fc.crop == r.crop)
                  & (fc.season_name == r.season_name)]["P_low"].mean()

    fcc["mean_P_low"] = fcc.apply(mean_p, axis=1)
    fcc = fcc.sort_values("mean_P_low", ascending=False)

    def fmt(v, nd=3):
        return "—" if v is None or not np.isfinite(
            pd.to_numeric(v, errors="coerce")) else f"{float(v):.{nd}f}"

    rows = [
        f"| {r.country} | {r.crop} | {r.season_name} | {int(r.n_joined)} "
        f"| {r.mean_P_low:.2f} | {fmt(r.get('skill_auc'))} "
        f"| {fmt(r.get('skill_null_auc'))} | {fmt(r.get('skill_perm_p'))} "
        f"| {'**yes**' if r.get('has_skill') else 'no'} "
        f"| {fmt(r.get('oos_max_sigma'), 1)} |"
        for _, r in fcc.iterrows()]
    nxt = (ex[ex.status == "too_early"].groupby("usable_from")
           .size().rename("combinations").reset_index()
           .sort_values("usable_from")) if "usable_from" in ex.columns \
        else pd.DataFrame()
    n_skill = int(fcc["has_skill"].sum()) if "has_skill" in fcc else 0
    n_supp = int(fcc["in_support"].sum()) if "in_support" in fcc else 0
    null_mean = pd.to_numeric(fcc.get("skill_null_auc"),
                              errors="coerce").mean()
    auc_mean = pd.to_numeric(fcc.get("skill_auc"), errors="coerce").mean()
    ver = f" · geocif {version}" if version else ""

    txt = f"""# Africa-wide pre-season S2S forecasts — maize & beans

Run: `{out.parents[1].name}`{ver} · module `geocif/experiments/s2s_africa.py`

Forecasts the **next season that has not started yet** for every country x
crop x season in HarvestStat Africa. Extended-term only: once planting has
passed, a combination belongs to the in-season CID system and is excluded.

## Read this first

Two checks decide whether any number below can be taken at face value.

1. **Skill** is judged against each combination's own year-block permutation
   null, not against AUC 0.5. Leave-one-year-out with an intercept biases
   predictions upward in exactly the year the fold removed, so an
   uninformative model scores {fmt(null_mean)}, not 0.500. **{n_skill} of
   {len(fcc)}** combinations beat their null at p<0.05, against
   {0.05 * len(fcc):.1f} expected by chance. Mean AUC {fmt(auc_mean)} vs mean
   null {fmt(null_mean)}.

2. **Support** asks whether the forecast predictors sit inside the range the
   model was fitted on. **{n_supp} of {len(fcc)}** do. Where they do not, the
   prediction is a clipped boundary value rather than a forecast, and the
   probability looks confident for the wrong reason. `oos_max_sigma` in
   `forecasts.csv` is the distance, in training standard deviations.

| Country | Crop | Season | Units | mean P(low) | AUC | Null | p | Skill | Out of support (sd) |
|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

`mean P(low)` is the average probability of a bottom-tercile (detrended) yield
across the country's admin units; 0.33 is climatology. `Null` is the mean AUC
of the year-block permutations of that same combination and `p` the fraction
of them that matched or beat the observed AUC.

## Files

| File | Contents |
|---|---|
| `forecasts.csv` | per admin unit: predicted anomaly, P(low/mid/high), P(below trend), init offset used, skill at the issued lead with its permutation null, and the per-unit clipping report (`n_clipped`, `oos_max_sigma`, `oos_feature`, `in_support`) |
| `skill.csv` | per combination x lead: AUC, low-tercile recall, false-alarm rate, rRMSE, trend rRMSE |
| `combinations.csv` | every combination with planting month, calendar source, eligibility status, skill and support flags |
| `excluded.csv` | everything not forecast, with the reason |
| `figures/charts/` | risk ranking beside skill-vs-null, skill vs lead, within-country spread, out-of-support magnitude, coverage |
| `figures/maps/` | P(low) per crop on the FEWS NET ramp with no-skill hatching, the out-of-support map, coverage |
| `figures/predictor_heatmaps/` | per combination, the predictors by year beside the forecast season |

Every figure family splits into `plots/` (PNG) and `csvs/`, with a
`lookup_plots_csvs.csv` manifest in both.
"""
    if not nxt.empty:
        txt += f"""
## What becomes forecastable next

{len(ex[ex.status == 'too_early'])} combinations are too early — their pre-season window opens later:

{nxt.to_string(index=False)}

Re-running after each new S2S initialization publishes will pick them up.
"""
    (out / "README.md").write_text(txt, encoding="utf-8")
    logger.info(f"README -> {out / 'README.md'}")
    return out / "README.md"


def render_all(out, root, hvstat_csv, gpkg=None, version=None,
               threshold_dir="crop_t0", extent=None, label=""):
    """Every figure family plus the README, each failing independently.

    A missing GMT library or an unreadable boundary file must not cost the
    run its CSVs, so each family is guarded on its own.
    """
    for name, fn in (
            ("charts", lambda: charts(out)),
            ("predictor heatmaps",
             lambda: predictor_heatmaps(out, root, hvstat_csv, threshold_dir)),
            ("maps", lambda: maps(out, gpkg, extent=extent, label=label)
             if gpkg else None),
            ("README", lambda: readme(out, version))):
        try:
            fn()
        except Exception as exc:                       # noqa: BLE001
            logger.warning(f"{name} failed: {type(exc).__name__}: {exc}")
    return Path(out)
