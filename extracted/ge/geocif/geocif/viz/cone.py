"""Cone-of-uncertainty figures: forecast + 80% interval vs forecast issue date.

Built from a ``run_time_steps = all`` + ``estimate_ci_for_all = True`` outlook
DB (tabpfn native quantiles), this module draws, per crop:

  1. ``cone_grid_{crop}``      — hindcast validation grid: one mini-cone per
                                 harvest year vs the observed value (the
                                 calibration story; miss-years pop out in red)
  2. ``cone_anatomy_{crop}``   — one full-size cone for the live forecast year
                                 with an empirical hindcast-error band overlay
  3. ``cone_coverage_{crop}``  — per-stage hindcast coverage vs the 0.8 nominal
  4. ``cone_states_{crop}``    — per-state mini-cones for the live year

Outputs land under ``{dir_output}/{project}/ml/analysis/{Month_DD_YYYY_HHhmm}/
cone/``, split into ``plots/`` (PNG) and ``csvs/``, with a
``lookup_plots_csvs.csv`` manifest in both — the same shape the outlook
products use.

Stage semantics (the part that is easy to get backwards): under ``monthly_r``
the stages are REVERSE-cumulative. In a ``Stage Name`` like ``"Aug 1-Mar 31"``
the FIRST month is the data cutoff and the second is the earliest (planting)
month — the window is really Mar 1 - Aug 31 (see geocif/viz/leadtime.py for
the long version). The x-axis here is the forecast ISSUE date = the first day
of the month AFTER the cutoff, because that is when a forecast built on "data
through end of August" can actually be issued.

National aggregation is the comonotone one: center, lower and upper are each
the area-weighted mean of the state values. Under perfect positive dependence
(one drought hits every Corn Belt state at once) the q-quantile of the
weighted sum IS the weighted sum of q-quantiles, so the aggregate band is a
coherent quantile — and conservative w.r.t. the true, imperfect dependence.
Bounds are aggregated separately; tabpfn quantiles are asymmetric and must
never be symmetrized around the center.

Usage:
    python -m geocif.viz.cone --db <maize.db> --table united_states_of_america_maize \
        --crop maize --out <dir>
    # or, resolving bare DB names against {dir_output}/{project}/ml/db/:
    from geocif.viz import cone
    cone.run([...4 config paths...], sources={"maize": ("outlook_X.db", "united_states_of_america_maize")})
"""

import argparse
import ast
import configparser
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.viz._style import despine as _despine
from geocif.viz.leadtime import _MONTHS, _asof_month, style_ctx
from geocif.viz._outlook_db import drop_sparse_stages, load_outlook
from geocif.viz.aggregation import _write_lookup
from geocif.viz import nass as nass_mod

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"
LO = "lower CI"
HI = "upper CI"

# tn/ha -> bu/ac, per-crop bushel weights (56 lb maize, 60 lb soybean).
# Same constants as geocif/analysis.py and the 2026-09-04 deliverables README.
BU_PER_TNHA = {"maize": 15.9318, "soybean": 14.8697}

# Crop identity color is the ONLY hue that changes between the paired figures;
# reference/empirical stay neutral so the pair reads as one system.
CROP_COLORS = {"maize": "#c07a00", "soybean": "#1f6f43"}
NEUTRAL = "#555555"

# 80% central interval <-> alpha 0.2 <-> z for N(0,1) 90th percentile.
Z80 = 1.2816

# Fewest usable hindcast years a stage needs before its robust (median, MAD)
# error fit is worth drawing: below this a MAD is 0 or a half-range.
MIN_BAND_YEARS = 5


def _to_display(v, crop, units):
    """tn/ha -> display units at the plot/CSV boundary only."""
    if units == "bu/ac":
        return v * BU_PER_TNHA[crop]
    return v


def load(db_path, table, model="tabpfn"):
    """Read one crop table (outlook experiment, one model) incl. CI columns.

    Thin wrapper over the shared loader — geocif/viz/_outlook_db.py carries
    the fork history, the upsert de-duplication and the parsed-timestamp fix
    for it (Date/Time are month-name-first strings; sorting them raw could
    keep a STALE row). Cone-specific choices: one model only, CI columns
    validated, and obs-NaN rows KEPT because the live forecast year has no
    observed value yet.
    """
    return load_outlook(db_path, table, model=model,
                        extra_columns=("Area (ha)", LO, HI, "alpha"),
                        validate_ci=True)


def _plant_month(stages):
    """Planting month = modal second-token month of the stage names."""
    months = []
    for s in stages:
        if not isinstance(s, str) or "-" not in s:
            continue
        tok = s.split("-", 1)[1].strip()[:3].title()
        if tok in _MONTHS:
            months.append(_MONTHS.index(tok) + 1)
    if not months:
        return None
    return int(pd.Series(months).mode().iloc[0])


def prepare(df, min_region_frac=1.0):
    """Drop unrepresentative stages, order by issue date, restrict the sample.

    A stage covering fewer than ``min_region_frac`` of the regions describes a
    different pool of states, not an earlier forecast — dropped. The default
    demands the FULL pool: on usa_admin1, maize ``Mar 1-Mar 31`` exists solely
    because Missouri's calendar starts in March (1/10 states), maize
    ``Apr 1-Mar 31`` covers 9/10, and the soybean ``Apr 1-Apr 30`` window
    exists for only 7/11 — keeping any of them would let the common-sample
    rule silently shrink the WHOLE cone to that stage's subset, so the
    aggregate would no longer be the published 10-/11-state one. Loosen the
    fraction only if losing regions is preferable to losing early stages.

    The frame is then restricted to the (Region, year) pairs that cover every
    surviving stage THAT YEAR HAS, so the cone narrows for informational
    reasons, not because the sample changed under it. The per-year form
    matters for the live season: its later cutoffs have not happened yet, and
    an all-stages requirement would silently drop the live year entirely.
    """
    df, dropped = drop_sparse_stages(df, min_region_frac)

    stages_seen = sorted(set(df["stage"]))
    df["asof"] = [_asof_month(s, w) for s, w in zip(df["stage"], df["swd"])]
    n_undated = int(df["asof"].isna().sum())
    df = df.dropna(subset=["asof"])
    if df.empty:
        raise ValueError(
            f"no stage name maps to a forecast issue month ({n_undated} row(s) "
            f"dropped; stages seen: {stages_seen}). The cone needs "
            f"month-window stages (run_time_steps=all); pre-season stage names "
            f"like 'Pre-Season (init Aug)' have no data cutoff to place on the "
            f"x-axis."
        )
    df["asof"] = df["asof"].astype(int)

    # Season order survives calendar wrap (a Jan cutoff of an Oct-planted
    # season sorts AFTER Dec): months counted from planting, mod 12.
    plant = _plant_month(df["stage"].unique()) or int(df["asof"].min())
    df["season_order"] = (df["asof"] - plant) % 12
    # Issue month = the month after the cutoff.
    df["issue_month"] = df["asof"] % 12 + 1

    piv = df.pivot_table(index=["Region", "year"], columns="stage",
                         values=PRED, aggfunc="first")
    year_stages = df.groupby("year")["stage"].agg(lambda s: sorted(set(s)))
    keep_pairs = [
        (region, year)
        for (region, year), row in piv.iterrows()
        if row[year_stages[year]].notna().all()
    ]
    if not keep_pairs:
        # Fail closed, not open: with one complete pair the restriction keeps
        # that pair, so with none it must not silently keep everything.
        raise ValueError(
            "no (Region, year) pair covers every stage of its own year, so no "
            "common sample exists — the cone would compare shifting region "
            "pools across stages. Check the DB for partially-written stages."
        )
    df = (df.set_index(["Region", "year"])
          .loc[pd.MultiIndex.from_tuples(keep_pairs)].reset_index())
    return df, dropped, len(keep_pairs)


def fill_weights(df):
    """Fill missing ``Area (ha)`` per region from its other years.

    The live forecast year has no NASS area yet, so its rows carry NULL —
    without this the live year (only) silently aggregates unweighted while
    every hindcast year is area-weighted.
    """
    df = df.sort_values("year").copy()
    df["Area (ha)"] = df.groupby("Region")["Area (ha)"].transform(
        lambda s: s.ffill().bfill()
    )
    return df


def national(df):
    """Comonotone national aggregate: one row per (stage, year).

    Center/obs are the area-weighted mean over states; the CI bounds are the
    area-weighted mean of the state bounds, and are NaN unless EVERY state in
    the group has a bound (a partial-CI aggregate would mix comonotone and
    point values). Falls back to an unweighted mean when weights are missing
    or all zero, and records which was used.
    """
    rows = []
    for (stage, asof, order, issue, year), g in df.groupby(
        ["stage", "asof", "season_order", "issue_month", "year"]
    ):
        w = g["Area (ha)"]
        weighted = w.notna().all() and float(w.sum()) > 0
        wv = w.values if weighted else np.ones(len(g))

        def _agg(col):
            # pred/CI: NaN unless EVERY state contributes (a partial comonotone
            # aggregate would silently change the pool between stages).
            v = g[col].values
            if np.isnan(v).any():
                return np.nan
            return float(np.average(v, weights=wv))

        # Observed is aggregated over whichever states report it: USDA gaps
        # (e.g. no Mississippi soybean estimate in the August report) are the
        # norm for the live year. n_obs_states records the actual pool so the
        # calibration statistics can insist on full coverage.
        ov = g[OBS].values
        has_obs = ~np.isnan(ov)
        nat_obs = (float(np.average(ov[has_obs], weights=wv[has_obs]))
                   if has_obs.any() else np.nan)

        rows.append({
            "stage": stage, "asof": asof, "season_order": order,
            "issue_month": issue, "year": int(year),
            "nat_obs": nat_obs, "nat_pred": _agg(PRED),
            "nat_lo": _agg(LO), "nat_hi": _agg(HI),
            "n_states": int(g["Region"].nunique()),
            # Regions, not rows: a row count would exceed n_states on a
            # duplicated DB and silently fail every full-pool filter below.
            "n_obs_states": int(g.loc[has_obs, "Region"].nunique()),
            "aggregation": "area-weighted" if weighted else "unweighted",
        })
    out = pd.DataFrame(rows)
    return out.sort_values(["year", "season_order"]).reset_index(drop=True)


def live_aggregation(nat, forecast_year):
    """The weighting scheme actually used for the plotted forecast year."""
    live = nat[nat["year"] == forecast_year]
    schemes = set(live["aggregation"]) or set(nat["aggregation"])
    return "mixed" if len(schemes) > 1 else (schemes.pop() if schemes else "unweighted")


def hindcast_mask(nat, forecast_year):
    """Hindcast rows usable for calibration statistics.

    Three conditions, all necessary for the quoted numbers to describe the
    plotted band: the year is not the forecast year, observed exists for the
    FULL region pool (a partial-pool observed is a different aggregate), and
    the weighting scheme matches the live year's — an area-weighted hindcast
    fitted around an unweighted live center would describe a different
    quantity than the one drawn.
    """
    return (
        (nat["year"] != forecast_year)
        & nat["nat_obs"].notna()
        & (nat["n_obs_states"] == nat["n_states"])
        & (nat["aggregation"] == live_aggregation(nat, forecast_year))
    )


def empirical_band(nat, forecast_year, z=Z80):
    """Hindcast-error band parameters per stage, on log-ratios.

    Errors are multiplicative — yields trend upward across the hindcast span,
    so proportional errors are far closer to exchangeable than additive ones,
    and the known failure mode (over-predicting collapse years) is
    proportional. Per stage: mu = median log-ratio, sigma = 1.4826 * MAD
    (robust to 2012/2015 dominating a ~21-sample fit), then sigma is made
    non-increasing in issue order (isotonic PAVA): more season observed can
    not mean more *climatological* uncertainty. mu is left per-stage — it is
    already an average, and it honestly carries any persistent bias.
    """
    hist = nat[hindcast_mask(nat, forecast_year) & nat["nat_pred"].notna()]
    rows = []
    for (stage, order), g in hist.groupby(["stage", "season_order"]):
        lr = np.log(g["nat_obs"].values / g["nat_pred"].values)
        if len(lr) < MIN_BAND_YEARS:
            # A MAD from 1-2 points is 0 (or a half-range), which would draw a
            # confident band from nothing. Drop the stage instead.
            print(f"empirical band: stage {stage!r} has {len(lr)} usable "
                  f"hindcast year(s) (< {MIN_BAND_YEARS}) — no band for it")
            continue
        mu = float(np.median(lr))
        sig = float(1.4826 * np.median(np.abs(lr - mu)))
        rows.append({"stage": stage, "season_order": order,
                     "mu_log": mu, "sigma_log_raw": sig, "n_hindcast_years": len(lr)})
    if not rows:
        return pd.DataFrame(columns=["stage", "season_order", "mu_log",
                                     "sigma_log_raw", "sigma_log_isotonic",
                                     "n_hindcast_years", "z"])
    band = pd.DataFrame(rows).sort_values("season_order").reset_index(drop=True)
    try:
        from sklearn.isotonic import IsotonicRegression
        iso = IsotonicRegression(increasing=False)
        band["sigma_log_isotonic"] = iso.fit_transform(
            band["season_order"].values.astype(float),
            band["sigma_log_raw"].values,
        )
    except Exception:  # sklearn is a hard geocif dep, but degrade gracefully
        band["sigma_log_isotonic"] = band["sigma_log_raw"]
    band["z"] = z
    return band


def coverage(nat, forecast_year):
    """Per-stage fraction of hindcast years with nat_obs inside the band."""
    hist = nat[hindcast_mask(nat, forecast_year)
               & nat["nat_lo"].notna() & nat["nat_hi"].notna()]
    rows = []
    for (stage, order, issue), g in hist.groupby(
        ["stage", "season_order", "issue_month"]
    ):
        inside = (g["nat_lo"] <= g["nat_obs"]) & (g["nat_obs"] <= g["nat_hi"])
        rows.append({"stage": stage, "season_order": order, "issue_month": issue,
                     "coverage": float(inside.mean()), "n_years": len(g)})
    if not rows:
        return pd.DataFrame(columns=["stage", "season_order", "issue_month",
                                     "coverage", "n_years"])
    return pd.DataFrame(rows).sort_values("season_order").reset_index(drop=True)


def _issue_labels(nat):
    """Ordered (season_order, issue_month, label) triples for the x-axis."""
    key = (nat[["season_order", "issue_month"]].drop_duplicates()
           .sort_values("season_order"))
    return [(int(r["season_order"]), int(r["issue_month"]),
             f"{_MONTHS[int(r['issue_month']) - 1]} 1")
            for _, r in key.iterrows()]


def _finish_axes(ax):
    _despine(ax)


def _save(fig, out_stem):
    out_stem = Path(out_stem)
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    return out_stem.with_suffix(".png")


def _agg_label(nat, forecast_year, n_states):
    """Axis label wording that matches the weighting actually applied."""
    scheme = live_aggregation(nat, forecast_year)
    if scheme == "area-weighted":
        return f"area-weighted {n_states}-state aggregate"
    if scheme == "mixed":
        return f"{n_states}-state aggregate (weighting varies by stage)"
    return f"unweighted {n_states}-state aggregate"


def _label_bottom_axes(axes, n_used, ncols):
    """Re-enable x tick labels on the lowest USED axis of every column.

    With sharex=True matplotlib turns labelbottom off for every non-bottom-row
    axis at creation, and hiding the trailing empty axes of a partial last row
    does not hand their labels back — whole columns would lose the
    forecast-issue-date axis, which is the figure's point.
    """
    for col in range(ncols):
        used = [i for i in range(n_used) if i % ncols == col]
        if used:
            axes[used[-1]].tick_params(labelbottom=True)


def _coverage_note(cov, n_states, agg_label):
    """One-line calibration summary for stdout and the run log.

    Deliberately NOT drawn on any figure: the house style keeps prose off the
    canvas, so these numbers travel in the companion CSV and the paper text.
    """
    tail = f"{agg_label.capitalize()}, not the published US national yield."
    if cov.empty or cov["coverage"].isna().all():
        return (f"Interval is 80% nominal; no hindcast year had a full-pool "
                f"observed value, so coverage of the plotted band could not be "
                f"measured here. {tail}")
    lo, hi = float(cov["coverage"].min()), float(cov["coverage"].max())
    yrs = int(cov["n_years"].min())
    return (f"Interval is 80% nominal; hindcast coverage of the plotted band "
            f"{lo:.0%}-{hi:.0%} across stages (>= {yrs} years per stage); "
            f"{tail}")


def plot_grid(nat, cov, crop, forecast_year, out_stem, units="bu/ac", ncols=5,
              ref_label=None, track=None, model="tabpfn"):
    """Hindcast validation grid: one mini-cone per harvest year vs observed."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    color = CROP_COLORS.get(crop, "#1f4e79")
    years = sorted(nat["year"].unique())
    xt = _issue_labels(nat)
    xs = [o for o, _, _ in xt]
    n = len(years)
    nrows = int(np.ceil(n / ncols))
    n_states = int(nat["n_states"].max())
    final_order = int(nat["season_order"].max())
    agg_label = _agg_label(nat, forecast_year, n_states)
    live_has_ref = nat[(nat["year"] == forecast_year)]["nat_obs"].notna().any()
    n_ref = 0
    n_track = 0

    with style_ctx():
        fig, axes = plt.subplots(nrows, ncols, figsize=(1.9 * ncols, 1.55 * nrows),
                                 sharex=True, sharey=True)
        axes = np.atleast_1d(axes).ravel()
        for ax, year in zip(axes, years):
            g = nat[nat["year"] == year].sort_values("season_order")
            gx = g["season_order"].values
            pred = _to_display(g["nat_pred"], crop, units).values
            lo = _to_display(g["nat_lo"], crop, units).values
            hi = _to_display(g["nat_hi"], crop, units).values
            obs = g["nat_obs"].dropna()
            obs = _to_display(float(obs.iloc[0]), crop, units) if len(obs) else None

            has_band = ~(np.isnan(lo) | np.isnan(hi))
            if has_band.any():
                ax.fill_between(gx[has_band], lo[has_band], hi[has_band],
                                color=color, alpha=0.22, linewidth=0)
            ax.plot(gx, pred, color=color, lw=1.1, marker="o", ms=2.2)

            if track is not None and len(track):
                tg = track[track["year"] == year].sort_values("season_order")
                if len(tg):
                    ax.plot(tg["season_order"],
                            _to_display(tg["usda_tnha"], crop, units),
                            color=NEUTRAL, lw=0.9, marker="s", ms=2.0,
                            linestyle="-", zorder=5)
                    n_track += 1

            missed = False
            if obs is not None:
                ax.axhline(obs, color="black", linestyle="--", lw=0.8)
                n_ref += 1
                # Flag against the FINAL stage of the cone, the same stage in
                # every panel. Judging each year by its own last AVAILABLE
                # stage would compare a mid-season band in a truncated year
                # against a harvest-time band elsewhere, and quietly clear a
                # real final-stage miss.
                fin = g[g["season_order"] == final_order]
                if len(fin):
                    fin = fin.iloc[-1]
                    if pd.notna(fin["nat_lo"]) and pd.notna(fin["nat_hi"]):
                        lo_d = _to_display(fin["nat_lo"], crop, units)
                        hi_d = _to_display(fin["nat_hi"], crop, units)
                        missed = not (lo_d <= obs <= hi_d)
            label = str(year) if year != forecast_year else f"{year}*"
            ax.text(0.04, 0.94, label, transform=ax.transAxes, fontsize=8,
                    fontweight="bold", va="top",
                    color="#c0392b" if missed else "#333333")
            ax.set_xticks(xs)
            ax.set_xticklabels([lab.split()[0] for _, _, lab in xt], fontsize=6)
            ax.tick_params(labelsize=6.5)
            ax.grid(True, linestyle=":", alpha=0.3)
            _finish_axes(ax)
        for ax in axes[n:]:
            ax.set_visible(False)
        _label_bottom_axes(axes, n, ncols)

        fig.suptitle(
            f"{crop.title()} yield forecast cones vs observed, "
            f"{years[0]}-{years[-1]} — {n_states}-state aggregate ({model})",
            fontsize=11, x=0.01, ha="left",
        )
        fig.supylabel(f"Yield ({units}), {agg_label}", fontsize=9)
        fig.supxlabel("Forecast issue date (EO data through end of prior month)",
                      fontsize=9, y=0.055)
        fig.tight_layout(rect=(0.015, 0.10, 1, 0.965))
        handles = [
            Patch(facecolor=color, alpha=0.22, label="Confidence interval"),
            Line2D([], [], color=color, lw=1.4, marker="o", ms=3.5,
                   label=f"Forecast ({model})"),
        ]
        if n_ref:
            handles.append(Line2D([], [], color="black", lw=0.9, ls="--",
                                  label=ref_label or "Observed"))
        if n_track:
            handles.append(Line2D([], [], color=NEUTRAL, lw=0.9, marker="s",
                                  ms=3.0, label="USDA NASS in-season"))
        fig.legend(handles=handles, frameon=False, fontsize=8, ncol=len(handles),
                   loc="lower center", bbox_to_anchor=(0.5, 0.0))
        p = _save(fig, out_stem)
        plt.close(fig)
    return p


def plot_anatomy(nat, band, cov, crop, forecast_year, out_stem, units="bu/ac",
                 ref_label=None, track=None, model="tabpfn"):
    """Full-size cone for the live year, with the empirical band overlay."""
    import matplotlib.pyplot as plt

    color = CROP_COLORS.get(crop, "#1f4e79")
    g = nat[nat["year"] == forecast_year].sort_values("season_order")
    if g.empty:
        return None
    xt = _issue_labels(nat)
    xs = [o for o, _, _ in xt]
    n_states = int(nat["n_states"].max())
    agg_label = _agg_label(nat, forecast_year, n_states)

    gx = g["season_order"].values
    pred = _to_display(g["nat_pred"], crop, units).values
    lo = _to_display(g["nat_lo"], crop, units).values
    hi = _to_display(g["nat_hi"], crop, units).values

    with style_ctx():
        fig, ax = plt.subplots(figsize=(7.2, 4.6))

        # Historical strip: last 10 hindcast years of national observed.
        hist_obs = (nat[nat["year"] != forecast_year]
                    .dropna(subset=["nat_obs"])
                    .groupby("year")["nat_obs"].first()
                    .sort_index().tail(10))
        if len(hist_obs):
            s_lo = _to_display(float(hist_obs.min()), crop, units)
            s_hi = _to_display(float(hist_obs.max()), crop, units)
            ax.axhspan(s_lo, s_hi, color="#e8e8e8", zorder=0)
            ax.text(0.01, s_lo + 0.03 * (s_hi - s_lo),
                    f"{hist_obs.index.min()}-{hist_obs.index.max()} observed range",
                    transform=ax.get_yaxis_transform(), fontsize=7.5,
                    color="#8a8a8a", va="bottom")

        has_band = ~(np.isnan(lo) | np.isnan(hi))
        if has_band.any():
            ax.fill_between(gx[has_band], lo[has_band], hi[has_band], color=color,
                            alpha=0.22, linewidth=0,
                            label="Confidence interval (model)", zorder=2)
            ax.plot(gx[has_band], lo[has_band], color=color, lw=0.8, zorder=2)
            ax.plot(gx[has_band], hi[has_band], color=color, lw=0.8, zorder=2)

        eb = (g.merge(band, on=["stage", "season_order"], how="inner")
              if not band.empty else band)
        if not eb.empty:
            eb = eb.sort_values("season_order")
            e_lo = eb["nat_pred"] * np.exp(eb["mu_log"] - eb["z"] * eb["sigma_log_isotonic"])
            e_hi = eb["nat_pred"] * np.exp(eb["mu_log"] + eb["z"] * eb["sigma_log_isotonic"])
            yrs = int(eb["n_hindcast_years"].min())
            for i, series in enumerate((e_lo, e_hi)):
                ax.plot(eb["season_order"], _to_display(series, crop, units),
                        color=NEUTRAL, lw=1.1, linestyle="--", zorder=3,
                        label=("Confidence interval (hindcast errors)"
                               if i == 0 else None))

        ax.plot(gx, pred, color=color, lw=1.8, marker="o", ms=5,
                label=f"Forecast ({model})", zorder=4)

        if track is not None and len(track):
            tg = track[track["year"] == forecast_year].sort_values("season_order")
            if len(tg):
                ax.plot(tg["season_order"],
                        _to_display(tg["usda_tnha"], crop, units),
                        color=NEUTRAL, lw=1.5, marker="s", ms=5.5,
                        label="USDA NASS in-season forecast", zorder=5)

        obs_rows = g.dropna(subset=["nat_obs"])
        if len(obs_rows):
            r0 = obs_rows.iloc[0]
            ref = _to_display(float(r0["nat_obs"]), crop, units)
            partial = ("" if int(r0["n_obs_states"]) == int(r0["n_states"])
                       else f" ({int(r0['n_obs_states'])}/{int(r0['n_states'])} states)")
            ax.axhline(ref, color="black", linestyle="--", lw=1.1, zorder=3)
            name = ref_label or "Observed"
            ax.annotate(f"{name} {forecast_year}: {ref:.1f}{partial}", xy=(1.0, ref),
                        xycoords=ax.get_yaxis_transform(),
                        xytext=(4, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=8.5, color="black")

        ax.set_xticks(xs)
        ax.set_xticklabels([lab for _, _, lab in xt], fontsize=9)
        ax.set_xlabel("Forecast issue date (EO data through end of prior month)",
                      fontsize=10)
        ax.set_ylabel(f"Yield ({units}), {agg_label}", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(True, linestyle=":", alpha=0.4)
        _finish_axes(ax)
        ax.legend(frameon=False, fontsize=8.5, loc="lower right")
        ax.set_title(
            f"{crop.title()} {forecast_year} yield forecast cone — "
            f"{n_states}-state aggregate ({model})",
            fontsize=10.5, loc="left",
        )
        fig.subplots_adjust(right=0.80)
        p = _save(fig, out_stem)
        plt.close(fig)
    return p


def plot_coverage(cov, crop, out_stem):
    """Per-stage hindcast coverage of the national band vs the 0.8 nominal."""
    import matplotlib.pyplot as plt

    if cov.empty:
        return None
    color = CROP_COLORS.get(crop, "#1f4e79")
    with style_ctx():
        fig, ax = plt.subplots(figsize=(5.4, 3.4))
        ax.axhline(0.8, color=NEUTRAL, linestyle="--", lw=1.2)
        ax.annotate("nominal 0.80", xy=(1.0, 0.8),
                    xycoords=ax.get_yaxis_transform(), xytext=(4, 0),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=8.5, color=NEUTRAL)
        ax.plot(cov["season_order"], cov["coverage"], color=color, lw=1.7,
                marker="o", ms=5)
        ax.set_xticks(cov["season_order"].tolist())
        ax.set_xticklabels([f"{_MONTHS[m - 1]} 1" for m in cov["issue_month"]],
                           fontsize=9)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("Forecast issue date", fontsize=10)
        ax.set_ylabel("Hindcast coverage of 80% band", fontsize=10)
        ax.grid(True, linestyle=":", alpha=0.4)
        _finish_axes(ax)
        n = int(cov["n_years"].max())
        ax.set_title(f"{crop.title()} — national 80% band coverage "
                     f"across {n} hindcast years", fontsize=10.5, loc="left")
        fig.subplots_adjust(right=0.82)
        p = _save(fig, out_stem)
        plt.close(fig)
    return p


def plot_states(df, crop, forecast_year, out_stem, units="bu/ac", ncols=5,
                ref_label=None, track_states=None, model="tabpfn"):
    """Per-state mini-cones for one harvest year (no empirical band: n too small).

    ``forecast_year`` is simply the year drawn — pass a hindcast year and the
    panels show that season's full USDA monthly track (Aug/Sep/Oct) against the
    observed final, which the live year cannot show until those reports exist.
    """
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    color = CROP_COLORS.get(crop, "#1f4e79")
    live = df[df["year"] == forecast_year]
    if live.empty:
        return None
    # Order (and title) by area share, but only over the states actually
    # drawn — the live year. A state present only in hindcast years would
    # otherwise claim a panel it has no data for.
    share = live.groupby("Region")["Area (ha)"].mean()
    total = float(share.sum(skipna=True))
    has_share = share.notna().any() and total > 0
    share = share.sort_values(ascending=False) if has_share else share.sort_index()
    states = share.index.tolist()
    xt = _issue_labels(
        live.rename(columns={"season_order": "season_order",
                             "issue_month": "issue_month"})
    )
    xs = [o for o, _, _ in xt]
    n = len(states)
    nrows = int(np.ceil(n / ncols))

    n_track = 0
    track_months = []
    if track_states is not None and len(track_states):
        ty = track_states[track_states["year"] == forecast_year]
        if len(ty) and "issue_month" in ty.columns:
            track_months = sorted({int(m) for m in ty["issue_month"]})

    with style_ctx():
        fig, axes = plt.subplots(nrows, ncols, figsize=(1.9 * ncols, 1.7 * nrows),
                                 sharex=True, sharey=True)
        axes = np.atleast_1d(axes).ravel()
        for ax, state in zip(axes, states):
            g = live[live["Region"] == state].sort_values("season_order")
            gx = g["season_order"].values
            pred = _to_display(g[PRED], crop, units).values
            lo = _to_display(g[LO], crop, units).values
            hi = _to_display(g[HI], crop, units).values
            has_band = ~(np.isnan(lo) | np.isnan(hi))
            if has_band.any():
                ax.fill_between(gx[has_band], lo[has_band], hi[has_band],
                                color=color, alpha=0.22, linewidth=0)
            ax.plot(gx, pred, color=color, lw=1.1, marker="o", ms=2.2)
            if track_states is not None and len(track_states):
                ts = track_states[(track_states["year"] == forecast_year)
                                  & (track_states["Region"] == state)]
                ts = ts.sort_values("season_order")
                if len(ts):
                    ax.plot(ts["season_order"],
                            _to_display(ts["usda_tnha"], crop, units),
                            color=NEUTRAL, lw=0.9, marker="s", ms=2.0, zorder=5)
                    n_track += 1
            obs = g[OBS].dropna()
            if len(obs):
                ax.axhline(_to_display(float(obs.iloc[0]), crop, units),
                           color="black", linestyle="--", lw=0.8)
            # No fabricated 0.0%: without areas the panel is just the state.
            if has_share and pd.notna(share[state]):
                pct = 100.0 * float(share[state]) / total
                ax.set_title(f"{state.title()} ({pct:.1f}%)", fontsize=7.5)
            else:
                ax.set_title(state.title(), fontsize=7.5)
            ax.set_xticks(xs)
            ax.set_xticklabels([lab.split()[0] for _, _, lab in xt], fontsize=6)
            ax.tick_params(labelsize=6.5)
            ax.grid(True, linestyle=":", alpha=0.3)
            _finish_axes(ax)
        for ax in axes[n:]:
            ax.set_visible(False)
        _label_bottom_axes(axes, n, ncols)

        fig.suptitle(
            f"{crop.title()} {forecast_year} state forecast cones ({model})",
            fontsize=10.5, x=0.01, ha="left",
        )
        fig.supylabel(f"Yield ({units})", fontsize=9)
        fig.supxlabel("Forecast issue date (EO data through end of prior month)",
                      fontsize=9, y=0.075)
        fig.tight_layout(rect=(0.015, 0.13, 1, 0.955))
        handles = [
            Patch(facecolor=color, alpha=0.22, label="Confidence interval"),
            Line2D([], [], color=color, lw=1.4, marker="o", ms=3.5,
                   label=f"Forecast ({model})"),
        ]
        if live[OBS].notna().any():
            handles.append(Line2D([], [], color="black", lw=0.9, ls="--",
                                  label=ref_label or "Observed"))
        if n_track:
            handles.append(Line2D([], [], color=NEUTRAL, lw=0.9, marker="s",
                                  ms=3.0, label="USDA NASS in-season"))
        fig.legend(handles=handles, frameon=False, fontsize=8, ncol=len(handles),
                   loc="lower center", bbox_to_anchor=(0.5, 0.0))
        p = _save(fig, out_stem)
        plt.close(fig)
    return p


def _grid_csv(nat, band, crop, forecast_year, units, model="tabpfn"):
    """One row per year x stage: exactly what the grid + anatomy figures show."""
    out = nat.copy()
    out.insert(0, "crop", crop)
    out["model"] = model
    out["forecast_year"] = forecast_year
    if not band.empty:
        out = out.merge(band, on=["stage", "season_order"], how="left")
        out["emp_lo"] = out["nat_pred"] * np.exp(
            out["mu_log"] - out["z"] * out["sigma_log_isotonic"])
        out["emp_hi"] = out["nat_pred"] * np.exp(
            out["mu_log"] + out["z"] * out["sigma_log_isotonic"])
    for col in ("nat_obs", "nat_pred", "nat_lo", "nat_hi", "emp_lo", "emp_hi"):
        if col in out.columns:
            out[f"{col}_{units.replace('/', '_per_')}"] = _to_display(
                out[col], crop, units)
    out["buac_per_tnha"] = BU_PER_TNHA.get(crop, np.nan)
    out["alpha_nominal"] = 0.2
    inside = (out["nat_lo"].notna() & out["nat_hi"].notna()
              & out["nat_obs"].notna())
    out["inside_band"] = np.where(
        inside, (out["nat_lo"] <= out["nat_obs"]) & (out["nat_obs"] <= out["nat_hi"]),
        np.nan)
    return out


def _hindcast_errors_csv(nat, crop, forecast_year):
    """Audit trail: every footnote number is recomputable from this frame.

    ``used_in_stats`` marks the rows that actually fed mu/sigma and coverage
    (full observed pool, same weighting as the live year). Without the flag a
    reader recomputing the footnote from this CSV would include partial-pool
    years the statistics deliberately exclude, and get different numbers.
    """
    usable = hindcast_mask(nat, forecast_year)
    hist = nat[(nat["year"] != forecast_year) & nat["nat_obs"].notna()
               & nat["nat_pred"].notna()].copy()
    hist["used_in_stats"] = usable.reindex(hist.index).fillna(False).values
    hist.insert(0, "crop", crop)
    hist["ratio"] = hist["nat_obs"] / hist["nat_pred"]
    hist["log_ratio"] = np.log(hist["ratio"])
    inside = hist["nat_lo"].notna() & hist["nat_hi"].notna()
    hist["inside_band"] = np.where(
        inside,
        (hist["nat_lo"] <= hist["nat_obs"]) & (hist["nat_obs"] <= hist["nat_hi"]),
        np.nan)
    return hist


def _norm_region(name):
    """Join key for region names across sources.

    NASS titles its state names ("SOUTH DAKOTA" -> "South Dakota") while a
    geocif table may hold "south_dakota" or "south dakota"; matching on the
    raw string silently drops every reference value.
    """
    return str(name).strip().lower().replace("_", " ")


def apply_nass_finals(df, nass, crop):
    """Fill missing observed yields from NASS FINAL estimates only.

    The outlook DB has no observed value for the live season, and older
    hindcast years can carry state gaps. NASS finals close those, in tn/ha.
    In-season monthly forecasts are deliberately NOT used here: they belong on
    the reference track, not in the column every calibration statistic treats
    as truth.
    """
    final = {(y, _norm_region(r)): v
             for (y, r), v in nass_mod.finals(nass, crop).items()}
    if not final:
        return df, 0
    factor = BU_PER_TNHA.get(crop)
    if not factor:
        raise ValueError(f"cannot convert NASS bu/ac to tn/ha for crop {crop!r}")
    missing = df[OBS].isna()
    vals = [final.get((int(y), _norm_region(r))) for y, r in
            zip(df.loc[missing, "year"], df.loc[missing, "Region"])]
    filled = pd.Series(vals, index=df.index[missing], dtype="float64") / factor
    df.loc[missing, OBS] = filled
    n = int(filled.notna().sum())
    if n:
        print(f"{crop}: filled {n} observed value(s) from NASS final estimates")
    return df, n


def nass_track(nass, crop, df, forecast_year=None):
    """USDA's own in-season forecasts, on the cone's x-axis.

    Returns ``(national, per_state)``. ``national`` is one area-weighted value
    per (year, season_order) using the SAME weights as the cone, and only
    where every state in the pool has a NASS number that month — a
    part-of-the-pool average would not be comparable to the cone it is drawn
    against. ``per_state`` keeps the state-level values for the small
    multiples.
    """
    monthly = {(y, m, _norm_region(r)): v
               for (y, m, r), v in nass_mod.monthly(nass, crop).items()}
    factor = BU_PER_TNHA.get(crop)
    if not monthly or not factor:
        empty = pd.DataFrame(columns=["year", "season_order", "issue_month",
                                      "usda_tnha", "n_states"])
        return empty, pd.DataFrame(columns=["year", "season_order", "Region",
                                            "usda_tnha"])

    axis = df[["season_order", "issue_month"]].drop_duplicates()
    pool = df[["year", "Region", "Area (ha)"]].drop_duplicates(["year", "Region"])

    rows, state_rows = [], []
    for year, states in pool.groupby("year"):
        for _, ax in axis.iterrows():
            order, month = int(ax["season_order"]), int(ax["issue_month"])
            vals, wts = [], []
            for _, st in states.iterrows():
                v = monthly.get((int(year), month, _norm_region(st["Region"])))
                if v is None:
                    continue
                tnha = v / factor
                state_rows.append({"year": int(year), "season_order": order,
                                   "issue_month": month, "Region": st["Region"],
                                   "usda_tnha": tnha})
                vals.append(tnha)
                wts.append(st["Area (ha)"])
            if len(vals) != len(states):
                continue                      # partial pool: not comparable
            w = np.array(wts, dtype="float64")
            use = w if np.isfinite(w).all() and w.sum() > 0 else np.ones(len(vals))
            rows.append({"year": int(year), "season_order": order,
                         "issue_month": month,
                         "usda_tnha": float(np.average(vals, weights=use)),
                         "n_states": len(vals)})
    national = pd.DataFrame(rows, columns=["year", "season_order", "issue_month",
                                           "usda_tnha", "n_states"])
    per_state = pd.DataFrame(state_rows, columns=["year", "season_order",
                                                  "issue_month", "Region",
                                                  "usda_tnha"])
    return national, per_state.drop_duplicates(["year", "season_order", "Region"])


def _current_year():
    import arrow as ar

    return int(ar.utcnow().to("America/New_York").format("YYYY"))


def read_config(path_config_files):
    """Parse the geocif config list into the settings this module needs.

    The ``[cone]`` section drives a server run::

        [cone]
        start_year = 2005          ; first harvest year drawn in the grid
        crops      = ['maize', 'soybean']
        dbs        = {'maize': 'outlook_09_06_2026_11h31.db',
                      'soybean': 'outlook_09_06_2026_11h21.db'}
        model      = tabpfn
        units      = bu/ac         ; or tn/ha
        ncols      = 5
        states_years = [2012, 2026]  ; years to draw per-state grids for
        use_nass_reference = True  ; USDA finals + monthly in-season track
        min_region_frac    = 1.0

    ``dbs`` is required and explicit on purpose: an outlook DB written for one
    crop can contain another crop's table produced with the wrong detrend
    method, so "whatever tables are in there" is not safe. Bare filenames
    resolve against ``{dir_output}/{project}/ml/db``. The NASS API key is read
    from ``[NASS] api_key`` (geobase.txt).
    """
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        inline_comment_prefixes=(";",),
    )
    parser.read([str(p) for p in path_config_files])

    # configparser exposes EVERY [DEFAULT] key from EVERY section, and the
    # geocif bundles put `crops` and `start_year` in [DEFAULT] (crops =
    # ['maize'], start_year = 1981). Without this probe, omitting `crops` from
    # [cone] would silently render one crop and drop the other. Re-parse with a
    # default section name no file uses, so [DEFAULT] becomes an ordinary
    # section and cannot leak; values still come from the interpolating parser.
    probe = configparser.ConfigParser(
        default_section="__cone_no_default__",
        interpolation=None,
        inline_comment_prefixes=(";",),
    )
    probe.read([str(p) for p in path_config_files])
    own = {sec: set(probe.options(sec)) for sec in probe.sections()}

    def _lit(section, option, default=None):
        # Only honour a key literally written under [section].
        if option not in own.get(section, ()):
            return default
        raw = parser.get(section, option).strip()
        try:
            return ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            return raw

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    countries = _lit("DEFAULT", "countries", []) or []
    country = countries[0] if countries else None

    cfg = {
        "dir_output": dir_output,
        "project": project,
        "country": country,
        "start_year": _lit("cone", "start_year"),
        "crops": _lit("cone", "crops", ["maize", "soybean"]),
        "dbs": _lit("cone", "dbs", {}),
        "model": _lit("cone", "model", "tabpfn"),
        "units": _lit("cone", "units", "bu/ac"),
        "ncols": int(_lit("cone", "ncols", 5)),
        "states_years": _lit("cone", "states_years"),
        "min_region_frac": float(_lit("cone", "min_region_frac", 1.0)),
        "use_nass": bool(_lit("cone", "use_nass_reference", True)),
        "nass_key": _lit("NASS", "api_key"),
        "nass_offline": bool(_lit("cone", "nass_offline", False)),
    }
    return cfg


def _resolve_paths(path_config_files, sources, out):
    """Resolve bare DB filenames and the default out dir from the configs."""
    if path_config_files is None:
        return sources, out
    # ExtendedInterpolation + inline ';' comments: geobase.txt writes
    # dir_output = ${dir_base}/outputs, and every other geocif config reader
    # (logger.read_config, the runners) parses it that way. With
    # interpolation=None this silently returns the literal '${dir_base}/...'.
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        inline_comment_prefixes=(";",),
    )
    parser.read([str(p) for p in path_config_files])
    dir_output = Path(parser.get("PATHS", "dir_output"))
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_db = dir_output / project / "ml" / "db"
    resolved = {}
    for crop, (db, table) in sources.items():
        db = Path(db)
        resolved[crop] = (db if db.is_absolute() else dir_db / db, table)
    if out is None:
        import arrow as ar
        # Same run-dir convention as the outlook tree: a date-stamped folder
        # holding one subdir per product (outlook/, cone/, ...).
        ts = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
        out = dir_output / project / "ml" / "analysis" / ts / "cone"
    return resolved, out


def run(path_config_files=None, *, sources=None, out=None, model=None,
        min_region_frac=None, units=None, start_year=None, ncols=None,
        nass=None, use_nass=None, states_years=None):
    """Render every cone output for ``sources = {crop: (db_path, table)}``.

    Explicit per-crop tables are mandatory: a maize production DB can contain
    a soybean table produced with the WRONG detrend method (the Sep-4 13h33 DB
    does), so "all non-config tables" would silently plot bad data.

    With ``path_config_files`` the ``[cone]`` section supplies every setting
    (see :func:`read_config`); explicit keyword arguments override it, which is
    what the CLI uses. ``start_year`` trims the grid to harvest years at or
    after it — the calibration statistics use exactly the years drawn.
    """
    cfg = read_config(path_config_files) if path_config_files else {}
    model = model or cfg.get("model") or "tabpfn"
    units = units or cfg.get("units") or "bu/ac"
    ncols = ncols or cfg.get("ncols") or 5
    if min_region_frac is None:
        min_region_frac = cfg.get("min_region_frac", 1.0)
    if start_year is None:
        start_year = cfg.get("start_year")
    if use_nass is None:
        use_nass = cfg.get("use_nass", True)
    if states_years is None:
        states_years = cfg.get("states_years")

    if not sources and cfg.get("dbs"):
        country = cfg.get("country")
        if not country:
            raise ValueError("[cone] dbs given but [DEFAULT] countries is empty "
                             "— the crop table name needs the country")
        sources = {crop: (db, f"{country}_{crop}")
                   for crop, db in cfg["dbs"].items()
                   if crop in (cfg.get("crops") or cfg["dbs"])}
    if not sources:
        raise ValueError("sources={crop: (db_path, table)} is required "
                         "(or a [cone] dbs entry in the config)")
    sources, out = _resolve_paths(path_config_files, sources, out)
    if out is None:
        raise ValueError("out dir is required when no config files are given")
    out = Path(out)
    # Mirrored trees, as viz/aggregation.py does for the outlook products:
    # every figure in plots/, its backing table in csvs/, and the lookup
    # manifest written into both.
    dir_plots = out / "plots"
    dir_csvs = out / "csvs"
    for d in (dir_plots, dir_csvs):
        d.mkdir(parents=True, exist_ok=True)

    nass_frame = nass
    if use_nass and nass_frame is None and cfg.get("nass_key"):
        try:
            nass_frame = nass_mod.fetch(
                cfg["nass_key"],
                years=range(int(start_year or 2000), _current_year() + 1),
                crops=list(sources),
                cache=dir_csvs / "nass_quickstats_cache.csv",
                offline=cfg.get("nass_offline", False),
            )
            print(f"NASS reference: {len(nass_frame)} state-period row(s)")
        except Exception as exc:
            print(f"NASS reference unavailable ({type(exc).__name__}: {exc}); "
                  f"figures fall back to the DB's own observed yields")
            nass_frame = None
    elif use_nass and nass_frame is None:
        print("NASS reference skipped: no [NASS] api_key in the config")

    written, lookup_rows = [], []
    for crop, (db_path, table) in sources.items():
        if crop not in BU_PER_TNHA and units == "bu/ac":
            raise ValueError(f"no bu/ac conversion for crop '{crop}'")
        df = load(db_path, table, model=model)
        if df.empty:
            print(f"{crop}: no outlook rows for model={model} in {table}, skipping")
            continue
        df, dropped, n_common = prepare(df, min_region_frac=min_region_frac)
        if dropped:
            print(f"{crop}: dropped unrepresentative stage(s) {dropped}")
        print(f"{crop}: {df['Region'].nunique()} states, "
              f"{df['stage'].nunique()} stages, {n_common} common (state,year) pairs")
        df = fill_weights(df)
        forecast_year = int(df["year"].max())
        if start_year:
            keep = df["year"] >= int(start_year)
            if not keep.any():
                raise ValueError(
                    f"{crop}: [cone] start_year={start_year} excludes every "
                    f"harvest year in {table} ({int(df['year'].min())}-"
                    f"{forecast_year})")
            df = df[keep].copy()

        ref_label, track, track_states = None, None, None
        if nass_frame is not None and len(nass_frame):
            df, n_final = apply_nass_finals(df, nass_frame, crop)
            if n_final:
                ref_label = "USDA NASS final"
            track, track_states = nass_track(nass_frame, crop, df, forecast_year)
            if len(track):
                print(f"{crop}: USDA in-season track has {len(track)} "
                      f"full-pool (year, month) point(s)")
        nat = national(df)
        schemes = sorted(set(nat["aggregation"]))
        if schemes != ["area-weighted"]:
            print(f"{crop}: WARNING — national aggregation is {'/'.join(schemes)} "
                  f"(a state with no 'Area (ha)' in any year forces equal "
                  f"weights for its whole (stage, year) group); figures are "
                  f"labelled accordingly")
        band = empirical_band(nat, forecast_year)
        cov = coverage(nat, forecast_year)
        print(f"{crop}: " + _coverage_note(
            cov, int(nat["n_states"].max()),
            _agg_label(nat, forecast_year, int(nat["n_states"].max()))))
        no_ci = nat["nat_lo"].isna().all()
        if no_ci:
            print(f"{crop}: WARNING — no CI columns populated; model-CI cone "
                  f"layers and coverage are skipped, empirical band still drawn")

        grid_csv = dir_csvs / f"cone_grid_{crop}.csv"
        _grid_csv(nat, band, crop, forecast_year, units, model).to_csv(
            grid_csv, index=False)
        written.append(grid_csv)
        err_csv = dir_csvs / f"cone_hindcast_errors_{crop}.csv"
        _hindcast_errors_csv(nat, crop, forecast_year).to_csv(err_csv, index=False)
        written.append(err_csv)
        if not cov.empty:
            cov_csv = dir_csvs / f"cone_coverage_{crop}.csv"
            cov.assign(crop=crop).to_csv(cov_csv, index=False)
            written.append(cov_csv)

        p = plot_grid(nat, cov, crop, forecast_year,
                      dir_plots / f"cone_grid_{crop}", units, ncols=ncols,
                      ref_label=ref_label, track=track, model=model)
        if p:
            written.append(p)
            lookup_rows.append((p.name, grid_csv.name,
                                f"{crop} hindcast validation grid of forecast cones"))
        p = plot_anatomy(nat, band, cov, crop, forecast_year,
                         dir_plots / f"cone_anatomy_{crop}_{forecast_year}", units,
                         ref_label=ref_label, track=track, model=model)
        if p:
            written.append(p)
            lookup_rows.append((p.name, grid_csv.name,
                                f"{crop} {forecast_year} full-size cone with "
                                f"empirical hindcast-error band"))
        if not cov.empty:
            p = plot_coverage(cov, crop, dir_plots / f"cone_coverage_{crop}")
            if p:
                written.append(p)
                lookup_rows.append((p.name, f"cone_coverage_{crop}.csv",
                                    f"{crop} per-stage hindcast coverage of the "
                                    f"80% band"))
        if track is not None and len(track):
            track_csv = dir_csvs / f"cone_usda_track_{crop}.csv"
            t = track.copy()
            t.insert(0, "crop", crop)
            t[f"usda_{units.replace('/', '_per_')}"] = _to_display(
                t["usda_tnha"], crop, units)
            t.to_csv(track_csv, index=False)
            written.append(track_csv)

        state_cols = ["Region", "year", "stage", "season_order", "issue_month",
                      PRED, OBS, LO, HI, "Area (ha)"]
        want_years = states_years or [forecast_year]
        for year in want_years:
            year = int(year)
            if not (df["year"] == year).any():
                print(f"{crop}: no rows for states_years entry {year}, skipping "
                      f"its per-state grid")
                continue
            states_csv = dir_csvs / f"cone_states_{crop}_{year}.csv"
            df[df["year"] == year][state_cols].to_csv(states_csv, index=False)
            written.append(states_csv)
            p = plot_states(df, crop, year, dir_plots / f"cone_states_{crop}_{year}",
                            units, ncols=ncols, ref_label=ref_label,
                            track_states=track_states, model=model)
            if p:
                written.append(p)
                lookup_rows.append((p.name, states_csv.name,
                                    f"{crop} {year} per-state forecast cones"))

    _write_lookup(lookup_rows, dir_plots, dir_csvs)
    print(f"wrote {len(written)} file(s) to {out} "
          f"(figures in plots/, tables in csvs/)")
    return written


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--config", action="append", default=None,
                   help="geocif config file (repeatable); with these the "
                        "[cone] section supplies dbs/crops/start_year")
    p.add_argument("--db", action="append", default=None,
                   help="outlook DB (repeatable, one per crop, zipped with "
                        "--table/--crop)")
    p.add_argument("--table", action="append", default=None,
                   help="crop table in the matching --db")
    p.add_argument("--crop", action="append", default=None,
                   help="crop name for the matching --db (maize, soybean, ...)")
    p.add_argument("--out", default=None, help="output directory")
    p.add_argument("--model", default=None)
    p.add_argument("--units", default=None, choices=["bu/ac", "tn/ha"])
    p.add_argument("--start-year", type=int, default=None,
                   help="first harvest year to draw (overrides [cone])")
    p.add_argument("--states-year", action="append", type=int, default=None,
                   help="year to draw a per-state cone grid for (repeatable; "
                        "default: the live forecast year)")
    p.add_argument("--no-nass", action="store_true",
                   help="skip the USDA NASS reference/track entirely")
    a = p.parse_args(argv)

    sources = None
    if a.db or a.table or a.crop:
        if not (a.db and a.table and a.crop
                and len(a.db) == len(a.table) == len(a.crop)):
            p.error("--db, --table and --crop must be given the same number "
                    "of times")
        sources = {c: (d, t) for c, d, t in zip(a.crop, a.db, a.table)}
    if not sources and not a.config:
        p.error("give either --config (with a [cone] section) or "
                "--db/--table/--crop")
    if not a.config and not a.out:
        p.error("--out is required without --config")

    run(a.config, sources=sources, out=a.out, model=a.model, units=a.units,
        start_year=a.start_year, states_years=a.states_year,
        use_nass=False if a.no_nass else None)


if __name__ == "__main__":
    sys.exit(main())
