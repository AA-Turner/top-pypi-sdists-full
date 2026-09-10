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

from geocif.viz.aggregation import _write_lookup

logger = logging.getLogger(__name__)

NODATA = "#d9d9d9"          # grey for no data: never white, which reads as water
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
NOSKILL_PATTERN = "p8+r100+fblack+b-"
# Regions whose record is too short to judge get their own mark: saying
# "no skill" about a region we cannot score is a claim we have not earned.
# A BACK-slanting line hatch, mirroring the forward no-skill hatch — the
# two read as the same family of caveat and are still separable at a
# glance. (Pattern 19 was tried first and draws DOTS, which read as
# plotted data rather than as an overlay.)
UNKNOWN_PATTERN = "p9+r100+fgray35+b-"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
REAL_YEARS = list(range(1994, 2018))     # real S2S hindcast members
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
    """scienceplots when available, plain matplotlib otherwise."""
    _use_agg()
    import matplotlib.pyplot as plt

    try:
        import scienceplots  # noqa: F401
        return plt.style.context(["science", "no-latex"])
    except Exception:
        return plt.style.context("default")


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
        for a in (ax, ax2):
            for s in ("top", "right"):
                a.spines[s].set_visible(False)
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
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
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
                for sp in ("top", "right"):
                    ax.spines[sp].set_visible(False)
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
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
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
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
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
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        save(fig, "coverage", "coverage.csv",
             "why each HarvestStat combination is or is not forecastable")

    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"charts -> {base} ({len(lookup)} figures)")
    return base


# ---------------------------------------------------------------------------
# maps
# ---------------------------------------------------------------------------
def _write_cpt(path, stops):
    """Discrete CPT with over/under set so clipped tails stay visible."""
    lines = [f"{lo}\t{c}\t{hi}\t{c}"
             for (lo, c), (hi, _) in zip(stops[:-1], stops[1:])]
    lines += [f"B\t{stops[0][1]}", f"F\t{stops[-1][1]}", f"N\t{NODATA}"]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def maps(out, gpkg, title_year=None):
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

    out = Path(out)
    base, dir_plots, dir_csvs = _dirs(out, "maps")
    fc = pd.read_csv(out / "forecasts.csv")
    cb = pd.read_csv(out / "combinations.csv")
    if fc.empty:
        logger.info("no forecasts to map")
        return base
    year = title_year or int(fc["harvest_year"].mode().iloc[0])
    gdf = gpd.read_file(gpkg)[["FNID", "ADMIN0", "geometry"]].rename(
        columns={"FNID": "fnid"})
    lookup = []

    def basemap(fig, title):
        pygmt.config(MAP_FRAME_TYPE="plain", FONT_TITLE="13p,Helvetica,black",
                     FONT_ANNOT_PRIMARY="9p", FONT_LABEL="10p")
        fig.basemap(region=REGION, projection=PROJ, frame=["af", f"+t{title}"])
        fig.coast(land=NODATA, water="white", shorelines="0.3p,gray40",
                  area_thresh=5000, borders="1/0.5p,gray55")

    def finish(fig, stem, csv_name, desc):
        # National borders drawn last and heavier than the admin-unit pens, so
        # the country outline stays legible over a dense choropleth.
        fig.coast(shorelines="0.5p,gray20", area_thresh=5000,
                  borders="1/0.9p,gray25")
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
        for state, patt in (("no_skill", NOSKILL_PATTERN),
                            ("insufficient", UNKNOWN_PATTERN)):
            sub = frame[frame[col] == state]
            if sub.empty:
                continue
            f = Path(td) / f"{state}.gmt"
            sub[["fnid", "geometry"]].to_file(f, driver="OGR_GMT")
            fig.plot(data=str(f), fill=patt, pen="0.15p,gray30", close=True)

    def choropleth(crop):
        d = fc[fc.crop == crop]
        if d.empty:
            return
        keep = [c for c in ("fnid", "country", "season_name", "P_low", "P_mid",
                            "P_high", "ahat", "offset_used", "skill_auc",
                            "null_auc", "perm_p", "has_skill", "in_support",
                            "oos_max_sigma", "n_clipped", "oos_feature",
                            "region_auc", "region_r2",
                            "region_n_low", "region_skill")
                if c in d.columns]
        d = d.sort_values("P_low", ascending=False).drop_duplicates("fnid")[keep]
        g = gdf.merge(d, on="fnid", how="inner")
        if g.empty:
            return
        csv_name = f"map_p_low_{crop}.csv"
        g.drop(columns="geometry").round(4).to_csv(dir_csvs / csv_name,
                                                   index=False)
        fig = pygmt.Figure()
        basemap(fig, f"Probability of lower tercile {crop} yields, {year}")
        with tempfile.TemporaryDirectory() as td:
            cpt = Path(td) / "fews.cpt"
            _write_cpt(cpt, FEWS_CPT)
            poly = Path(td) / "poly.gmt"
            g[["fnid", "P_low", "geometry"]].to_file(poly, driver="OGR_GMT")
            fig.plot(data=str(poly), fill="+z", cmap=str(cpt),
                     pen="0.15p,gray30", close=True, aspatial="Z=P_low")
            _hatch_by_region(fig, g, td)
            fig.colorbar(cmap=str(cpt),
                         frame="x+lProbability of lower tercile crop yields",
                         position="JBC+w10c/0.35c+h+o0c/1.1c+e")
            spec = Path(td) / "legend.txt"
            spec.write_text("\n".join([
                "G 0.05c",
                f"S 0.3c s 0.32c {NODATA} 0.2p,gray40 0.75c "
                f"No forecast or data available",
                f"S 0.3c s 0.32c {NOSKILL_PATTERN} 0.2p,gray40 0.75c "
                f"No forecast skill at this lead",
            ]) + "\n", encoding="utf-8")
            fig.legend(spec=str(spec), position="JBL+jBL+o0.3c/0.3c+w6.6c",
                       box="+gwhite+p0.4p,gray50")
        finish(fig, f"map_p_low_{crop}", csv_name,
               f"P(lower tercile) {crop} {year}, hatched where skill fails")

    def anomaly_map(crop):
        """The regression prediction: % departure from trend per unit.

        This is the honest regression product — it needs no absolute yield
        level, so it is publishable everywhere the classification map is.
        """
        d = fc[fc.crop == crop]
        if d.empty or "ahat" not in d.columns:
            return
        keep = [c for c in ("fnid", "country", "season_name", "ahat",
                            "r2", "perm_r2_p", "r2_within",
                            "perm_r2_within_p", "has_skill", "in_support",
                            "oos_max_sigma", "region_auc", "region_r2",
                            "region_n_low", "region_skill") if c in d.columns]
        d = (d.sort_values("ahat").drop_duplicates("fnid")[keep].copy())
        d["ahat_pct"] = (100 * d["ahat"]).round(1)
        g = gdf.merge(d, on="fnid", how="inner")
        if g.empty:
            return
        csv_name = f"map_anomaly_{crop}.csv"
        g.drop(columns="geometry").round(4).to_csv(dir_csvs / csv_name,
                                                   index=False)
        fig = pygmt.Figure()
        basemap(fig, f"Predicted {crop} yield departure from trend, {year}")
        with tempfile.TemporaryDirectory() as td:
            cpt = Path(td) / "anom.cpt"
            _write_cpt(cpt, ANOM_CPT)
            poly = Path(td) / "poly.gmt"
            g[["fnid", "ahat_pct", "geometry"]].to_file(poly,
                                                        driver="OGR_GMT")
            fig.plot(data=str(poly), fill="+z", cmap=str(cpt),
                     pen="0.15p,gray30", close=True, aspatial="Z=ahat_pct")
            _hatch_by_region(fig, g, td)
            fig.colorbar(cmap=str(cpt),
                         frame="x+lPredicted yield departure from trend (%)",
                         position="JBC+w10c/0.35c+h+o0c/1.1c+e")
            spec = Path(td) / "legend.txt"
            spec.write_text("\n".join([
                "G 0.05c",
                f"S 0.3c s 0.32c {NODATA} 0.2p,gray40 0.75c "
                f"No forecast or data available",
                f"S 0.3c s 0.32c {NOSKILL_PATTERN} 0.2p,gray40 0.75c "
                f"No forecast skill at this lead",
            ]) + "\n", encoding="utf-8")
            fig.legend(spec=str(spec), position="JBL+jBL+o0.3c/0.3c+w6.6c",
                       box="+gwhite+p0.4p,gray50")
        finish(fig, f"map_anomaly_{crop}", csv_name,
               f"predicted {crop} yield anomaly {year}, % vs trend")

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
        d = d.sort_values("yhat_tha").drop_duplicates("fnid").copy()
        ok = d["trend_extrap_err_pct"].notna() & (
            d["trend_extrap_err_pct"] <= max_err)
        if not ok.any():
            logger.info(f"no {crop} combination has a trend extrapolation "
                        f"within {max_err}% — t/ha map skipped")
            return
        keep = [c for c in ("fnid", "country", "season_name", "ahat",
                            "trend_tha", "yhat_tha", "extrap_years",
                            "trend_extrap_err_pct", "has_skill")
                if c in d.columns]
        g = gdf.merge(d[keep], on="fnid", how="inner")
        if g.empty:
            return
        csv_name = f"map_yield_tha_{crop}.csv"
        g.drop(columns="geometry").round(4).to_csv(dir_csvs / csv_name,
                                                   index=False)
        pub = g[g["trend_extrap_err_pct"] <= max_err]
        held = g[g["trend_extrap_err_pct"] > max_err]

        fig = pygmt.Figure()
        basemap(fig, f"Predicted {crop} yield, {year}")
        with tempfile.TemporaryDirectory() as td:
            cpt = Path(td) / "yield.cpt"
            _write_cpt(cpt, YIELD_CPT)
            if not held.empty:
                p = Path(td) / "held.gmt"
                held[["fnid", "geometry"]].to_file(p, driver="OGR_GMT")
                fig.plot(data=str(p), fill="#bdbdbd", pen="0.15p,gray40",
                         close=True)
            poly = Path(td) / "poly.gmt"
            pub[["fnid", "yhat_tha", "geometry"]].to_file(poly,
                                                          driver="OGR_GMT")
            fig.plot(data=str(poly), fill="+z", cmap=str(cpt),
                     pen="0.15p,gray30", close=True, aspatial="Z=yhat_tha")
            _hatch_by_region(fig, pub, td)
            fig.colorbar(cmap=str(cpt),
                         frame="x+lPredicted yield (t/ha)",
                         position="JBC+w10c/0.35c+h+o0c/1.1c+e")
            spec = Path(td) / "legend.txt"
            spec.write_text("\n".join([
                "G 0.05c",
                f"S 0.3c s 0.32c {NODATA} 0.2p,gray40 0.75c "
                f"No forecast or data available",
                f"S 0.3c s 0.32c #bdbdbd 0.2p,gray40 0.75c "
                f"Withheld: trend baseline extrapolated too far",
                f"S 0.3c s 0.32c {NOSKILL_PATTERN} 0.2p,gray40 0.75c "
                f"No forecast skill at this lead",
            ]) + "\n", encoding="utf-8")
            fig.legend(spec=str(spec), position="JBL+jBL+o0.3c/0.3c+w8.0c",
                       box="+gwhite+p0.4p,gray50")
        finish(fig, f"map_yield_tha_{crop}", csv_name,
               f"predicted {crop} yield t/ha {year}, withheld where the "
               f"trend baseline extrapolates beyond {max_err}%")

    def region_roc_map(crop):
        """Per-region hindcast ROC — how well each polygon has been called.

        The companion to the forecast maps: those say what we expect, this
        says where the record supports expecting anything. Diverging on 0.5,
        with the 0.6 skill bar on a colour break.
        """
        if "region_auc" not in fc.columns:
            return
        d = fc[fc.crop == crop].dropna(subset=["region_auc"])
        if d.empty:
            return
        keep = [c for c in ("fnid", "country", "season_name", "region_auc",
                            "region_r2", "region_n_years", "region_n_low",
                            "region_skill") if c in d.columns]
        d = d.drop_duplicates("fnid")[keep]
        g = gdf.merge(d, on="fnid", how="inner")
        if g.empty:
            return
        csv_name = f"map_region_roc_{crop}.csv"
        g.drop(columns="geometry").round(4).to_csv(dir_csvs / csv_name,
                                                   index=False)
        fig = pygmt.Figure()
        basemap(fig, f"Hindcast skill by region, {crop} ({year} forecast lead)")
        with tempfile.TemporaryDirectory() as td:
            cpt = Path(td) / "roc.cpt"
            _write_cpt(cpt, ROC_CPT)
            poly = Path(td) / "poly.gmt"
            g[["fnid", "region_auc", "geometry"]].to_file(poly,
                                                          driver="OGR_GMT")
            fig.plot(data=str(poly), fill="+z", cmap=str(cpt),
                     pen="0.15p,gray30", close=True, aspatial="Z=region_auc")
            if "region_skill" in g.columns:
                unk = g[g.region_skill == "insufficient"]
                if not unk.empty:
                    f = Path(td) / "unk.gmt"
                    unk[["fnid", "geometry"]].to_file(f, driver="OGR_GMT")
                    fig.plot(data=str(f), fill=UNKNOWN_PATTERN,
                             pen="0.15p,gray30", close=True)
            fig.colorbar(cmap=str(cpt),
                         frame="x+lHindcast ROC for bottom-tercile years",
                         position="JBC+w10c/0.35c+h+o0c/1.1c+e")
            spec = Path(td) / "legend.txt"
            spec.write_text("\n".join([
                "G 0.05c",
                f"S 0.3c s 0.32c {NODATA} 0.2p,gray40 0.75c "
                f"No forecast or data available",
                f"S 0.3c s 0.32c {UNKNOWN_PATTERN} 0.2p,gray40 0.75c "
                f"Too few poor years on record to judge",
            ]) + "\n", encoding="utf-8")
            fig.legend(spec=str(spec), position="JBL+jBL+o0.3c/0.3c+w7.4c",
                       box="+gwhite+p0.4p,gray50")
        finish(fig, f"map_region_roc_{crop}", csv_name,
               f"per-region hindcast ROC for bottom-tercile {crop} years")

    def support_map():
        """How far outside the fitted range the forecast predictors sat.

        ``in_support`` can be False everywhere, in which case the binary flag
        carries no spatial information and only the magnitude does.
        """
        if "oos_max_sigma" not in fc.columns:
            return
        d = (fc.sort_values("oos_max_sigma", ascending=False)
               .drop_duplicates("fnid")[["fnid", "country", "crop",
                                         "season_name", "oos_max_sigma",
                                         "oos_feature", "n_clipped"]])
        g = gdf.merge(d, on="fnid", how="inner")
        if g.empty:
            return
        csv_name = "map_out_of_support.csv"
        g.drop(columns="geometry").round(3).to_csv(dir_csvs / csv_name,
                                                   index=False)
        fig = pygmt.Figure()
        basemap(fig, f"Distance of the {year} S2S predictors outside "
                     f"training range")
        with tempfile.TemporaryDirectory() as td:
            cpt = Path(td) / "oos.cpt"
            _write_cpt(cpt, OOS_CPT)
            poly = Path(td) / "poly.gmt"
            g[["fnid", "oos_max_sigma", "geometry"]].to_file(
                poly, driver="OGR_GMT")
            fig.plot(data=str(poly), fill="+z", cmap=str(cpt),
                     pen="0.15p,gray30", close=True,
                     aspatial="Z=oos_max_sigma")
            fig.colorbar(
                cmap=str(cpt),
                frame="x+lStandard deviations beyond the training range",
                position="JBC+w10c/0.35c+h+o0c/1.1c+e")
        finish(fig, "map_out_of_support", csv_name,
               "worst per-unit predictor exceedance of the training range, in sd")

    def coverage_map():
        st = cb.groupby("country")["status"].apply(
            lambda s: "forecast" if (s == "forecast").any()
            else ("in_season" if (s == "in_season").any() else "not_forecast"))
        tab = st.rename("coverage").reset_index()
        csv_name = "map_coverage.csv"
        tab.to_csv(dir_csvs / csv_name, index=False)
        cols = {"forecast": ("#1b7837", "forecast issued"),
                "in_season": ("#7fb3d5", "season already under way"),
                "not_forecast": (NODATA, "not forecastable yet")}
        g = gdf.merge(tab, left_on="ADMIN0", right_on="country", how="left")
        fig = pygmt.Figure()
        basemap(fig, f"Pre-season forecast coverage, {year}")
        for key, (col, _) in cols.items():
            sub = g[g["coverage"] == key]
            if not sub.empty:
                fig.plot(data=sub[["geometry"]], fill=col, pen="0.15p,gray40",
                         close=True)
        with tempfile.TemporaryDirectory() as td:
            spec = Path(td) / "legend.txt"
            spec.write_text("\n".join(
                ["G 0.05c"] + [f"S 0.3c s 0.35c {c} 0.2p,gray40 0.75c {lab}"
                               for c, lab in cols.values()]) + "\n",
                encoding="utf-8")
            fig.legend(spec=str(spec), position="JBL+jBL+o0.4c/0.4c+w5.4c",
                       box="+gwhite+p0.4p,gray50")
        finish(fig, "map_coverage", csv_name,
               "which HarvestStat country x crop x season could be forecast")

    for crop in sorted(fc["crop"].unique()):
        choropleth(crop)      # classification: P(lower tercile)
        anomaly_map(crop)     # regression: % vs trend
        yield_map(crop)       # regression: t/ha, where the baseline holds
        region_roc_map(crop)  # where the record supports a call at all
    support_map()
    coverage_map()
    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"maps -> {base} ({len(lookup)} figures)")
    return base


# ---------------------------------------------------------------------------
# predictor heatmaps
# ---------------------------------------------------------------------------
def predictor_heatmaps(out, root, hvstat_csv, threshold_dir="crop_t0"):
    """Per combination, the model's predictors by year beside the forecast.

    Only the real-hindcast years are shown plus the forecast year: the
    2018-2025 seasons are climatology gap-fill in the NOAA archive -- every
    year identical by construction -- so plotting them would show a flat band
    that looks like signal and is not.
    """
    _use_agg()
    import matplotlib.pyplot as plt

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
        title = (f"{country} · {crop.capitalize()} · {season} season — "
                 f"planted {MON[plant_m - 1]} {plant_y}, "
                 f"harvested {MON[harv_m - 1]} {hy} "
                 f"(S2S init {MON[im - 1]} {iy})")

        # Scale to the HISTORICAL spread, not the full range: the forecast
        # year can sit several sigma outside anything on record, and letting
        # it set the scale flattens two decades of history into a uniform
        # pale block. The forecast column saturates and the colourbar arrows
        # make that visible.
        data = m[feats].T.to_numpy(dtype=float)
        hist = m.loc[[y for y in years if y in REAL_YEARS],
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
                f"Z-score vs {REAL_YEARS[0]}–{REAL_YEARS[-1]} S2S hindcast",
                fontsize=9)
            cbar.ax.tick_params(labelsize=8)
            ax.set_xlabel("Harvest year", fontsize=9)
            stem = (f"{country.replace(' ', '_').replace(',', '')}_{crop}_"
                    f"{season.replace('/', '_')}")
            fig.savefig(dir_plots / f"{stem}.png", dpi=300,
                        bbox_inches="tight")
            plt.close(fig)
        m.round(4).to_csv(dir_csvs / f"{stem}.csv")
        lookup.append((f"{stem}.png", f"{stem}.csv",
                       f"{country} {crop.capitalize()} {season} — S2S "
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
               threshold_dir="crop_t0"):
    """Every figure family plus the README, each failing independently.

    A missing GMT library or an unreadable boundary file must not cost the
    run its CSVs, so each family is guarded on its own.
    """
    for name, fn in (
            ("charts", lambda: charts(out)),
            ("predictor heatmaps",
             lambda: predictor_heatmaps(out, root, hvstat_csv, threshold_dir)),
            ("maps", lambda: maps(out, gpkg) if gpkg else None),
            ("README", lambda: readme(out, version))):
        try:
            fn()
        except Exception as exc:                       # noqa: BLE001
            logger.warning(f"{name} failed: {type(exc).__name__}: {exc}")
    return Path(out)
