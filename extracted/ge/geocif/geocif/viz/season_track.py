# -*- coding: utf-8 -*-
"""Season track: one season's national yield forecast, pre-season to harvest.

Puts the two forecast systems on one time axis, by the date each forecast
was made, one panel per harvest year:

* **pre-season** - the S2S model (``experiments/s2s_africa.py``), one
  forecast per NOAA init from four months before planting up to the planting
  month, read from that run's ``hindcasts.csv`` (leave-one-year-out
  predictions per unit, lead and year). An init is dated the 11th of its
  month, when NOAA PSL posts it.
* **in-season** - one model of a GEOCIF outlook DB, one forecast per stage
  (``snake_data.load_forecasts``: as-of month from the stage name, issued the
  first day of the following month, causal area fill for a missing year).

Each system is weighted to the national value with ``snake_data.to_national``
(the outlook products' rule) over its own units and areas: HarvestStat area
for the S2S units, the DB's ``Area (ha)`` for the outlook regions. The
observed line is the outlook DB's national observed yield (the S2S run's
HarvestStat value where the DB has none, with a warning when both exist and
differ by more than 1%); the trend line is the S2S run's leave-one-year-out
linear trend, the baseline its anomalies are built on.

In every year with an observation both systems are hindcasts: the plotted
year was held out of training, but later years were not, so a panel is not
what a system running in real time would have issued that season.

Year choice (``years=None``): among years with an observation, a trend and
both systems, rank by the share of the trend's miss the forecasts removed,
``skill = 1 - mean(|forecast - obs|) / |trend - obs|`` over every plotted
forecast, and draw the top ``n_years``. 1 is perfect and 0 no better than
the trend. A year that lands on trend has nothing to beat and ranks last
(skill undefined at a zero miss). The absolute form, ``gain = |trend - obs|
- mean(|forecast - obs|)``, is reported beside it but not ranked on: it
favours a year the trend missed badly even when the forecasts missed it
almost as badly (Zimbabwe 2007: observed 0.49 t/ha, forecasts about 0.75).

Outputs (``out``): ``plots/season_track_{stem}.png`` with a notes text file
beside it (definitions, the per-forecast values and errors, the year ranking
and each lead's national skill over all years, with N), ``csvs/`` with the
plotted values and the ranking, and ``lookup_plots_csvs.csv`` in both.

Usage:
    python -m geocif.viz.season_track --db outlook_10_11_2026_23h00.db \\
        --table zimbabwe_maize --model kumo \\
        --s2s-run <...>/explore/s2s_africa_southern_africa \\
        --country Zimbabwe --crop maize --out <dir> [--years 2016 2013]
"""
import argparse
import calendar
import logging
import re
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.utils import display_model_name
from geocif.viz._outlook_db import OBS
from geocif.viz._style import MONTHS, despine, style_ctx
from geocif.viz.aggregation import _write_lookup
from geocif.viz.snake_data import AREA, load_forecasts, to_national

logger = logging.getLogger(__name__)

#: NOAA PSL posts each S2S init around the 11th of the init month.
S2S_POST_DAY = 11
#: Pre-season inits run from MAX_OFFSET months before planting to the
#: planting month itself (offset 0); later inits fall inside the in-season
#: stretch and are left out unless ``min_offset`` says otherwise.
MIN_OFFSET = 0
PRE, INS = "pre-season", "in-season"
#: Observed yields of the two sources that differ by more than this are
#: reported: the panels draw one observed line for both.
OBS_TOLERANCE = 0.01

COLORS = {PRE: "#eb6834", INS: "#2a78d6"}
MARKERS = {PRE: "s", INS: "D"}
C_OBS = "#0b0b0b"
C_TREND = "#8a8984"
INK2 = "#52514e"
SHADE_PRE = "#f4f3f0"
SHADE_PLANT = "#e6e5e0"


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------
def load_s2s(run_dir, country, crop, season_name=None):
    """The ``hindcasts.csv`` rows of one country x crop x season."""
    path = Path(run_dir) / "hindcasts.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found: the S2S run predates hindcasts.csv; rerun "
            f"experiments.s2s_africa (as_of_init= reproduces a past issue)")
    h = pd.read_csv(path)
    h = h[(h["country"] == country) & (h["crop"] == crop)]
    if season_name is not None:
        h = h[h["season_name"] == season_name]
    seasons = sorted(h["season_name"].unique())
    if len(seasons) > 1:
        raise ValueError(f"{country} {crop} has S2S seasons {seasons}; "
                         f"pass season_name")
    if h.empty:
        raise ValueError(f"{path}: no hindcast rows for {country} {crop}"
                         + (f" {season_name}" if season_name else ""))
    return h.reset_index(drop=True)


def _months_from_planting(when, plant_year, plant_month):
    """Position on the season axis: 0 = first day of the planting month,
    fractional within a month."""
    days = calendar.monthrange(when.year, when.month)[1]
    return ((when.year - plant_year) * 12 + when.month - plant_month
            + (when.day - 1) / days)


def s2s_national(h, country, min_offset=MIN_OFFSET):
    """National pre-season forecast per (year, offset) from S2S unit rows.

    Columns: year, offset, date_made, label, value, obs, trend, n_units,
    aggregation, plant_year, plant_month.
    """
    h = h[h["offset"] >= min_offset]
    if h.empty:
        raise ValueError(f"no S2S hindcasts at offset >= {min_offset}")
    frame = pd.DataFrame({"Region": h["fnid"].values, "year": h["year"].values,
                          "offset": h["offset"].values,
                          "yhat": h["yhat_tha"].values, "trend": h["trend"].values,
                          OBS: h["obs"].values, AREA: h["area"].values})
    nat = to_national(frame, country, value_col="yhat", by=("year", "offset"))
    tr = to_national(frame, country, value_col="trend", by=("year", "offset"))
    nat = nat.merge(tr[["year", "offset", "value"]].rename(
        columns={"value": "trend"}), on=["year", "offset"], how="left")
    inits = h.drop_duplicates(["year", "offset"])[
        ["year", "offset", "init_year", "init_month"]]
    nat = nat.merge(inits, on=["year", "offset"], how="left")
    # planting = init + offset months
    total = nat["init_year"] * 12 + nat["init_month"] - 1 + nat["offset"]
    nat["plant_year"] = (total // 12).astype(int)
    nat["plant_month"] = (total % 12 + 1).astype(int)
    nat["date_made"] = [date(int(y), int(m), S2S_POST_DAY)
                        for y, m in zip(nat["init_year"], nat["init_month"])]
    nat["label"] = [f"{MONTHS[int(m) - 1]} init" for m in nat["init_month"]]
    return nat.drop(columns=["init_year", "init_month"])


def outlook_national(db, table, model, country, season=None):
    """National in-season forecast per (year, stage) from an outlook DB.

    Columns: year, stage, date_made, label, value, obs, n_units, aggregation.
    """
    fc = load_forecasts(db, table, model=model, season=season)
    nat = to_national(fc, country, by=("year", "stage"))
    dates = fc.drop_duplicates(["year", "stage"])[["year", "stage", "issue_date"]]
    nat = nat.merge(dates, on=["year", "stage"], how="left")
    nat = nat.rename(columns={"issue_date": "date_made"})
    nat["label"] = [f"{MONTHS[d.month - 1]} {d.day}" for d in nat["date_made"]]
    return nat


def build_track(pre, ins):
    """Long table of every national forecast, plus one row per year with the
    observed yield and trend the panels draw.

    ``track``: year, system, label, date_made, x (months from planting),
    value, n_units, aggregation. ``years``: year, obs, obs_s2s, obs_outlook,
    trend, plant_year, plant_month.
    """
    plant = pre.drop_duplicates("year").set_index("year")[
        ["plant_year", "plant_month"]]
    obs_in = ins.groupby("year")["obs"].first()
    obs_pre = pre.groupby("year")["obs"].first()
    trend = pre.groupby("year")["trend"].first()
    years = sorted(set(pre["year"]) | set(ins["year"]))
    info = pd.DataFrame({"year": years})
    info["obs_outlook"] = info["year"].map(obs_in)
    info["obs_s2s"] = info["year"].map(obs_pre)
    info["obs"] = info["obs_outlook"].fillna(info["obs_s2s"])
    info["trend"] = info["year"].map(trend)
    both = info.dropna(subset=["obs_outlook", "obs_s2s"])
    off = both[(both["obs_outlook"] / both["obs_s2s"] - 1).abs() > OBS_TOLERANCE]
    if not off.empty:
        logger.warning(
            f"observed national yields of the outlook DB and the S2S run differ "
            f"by more than {OBS_TOLERANCE:.0%} in {off['year'].tolist()}; the "
            f"panels draw the outlook DB's")
    # A year without S2S rows (outside its hindcast era) has no init to
    # anchor the planting date: borrow the planting month and shift the year.
    if plant.empty:
        raise ValueError("no S2S rows to anchor the planting month")
    pm = int(plant["plant_month"].mode().iloc[0])
    lag = int((plant["plant_year"] - plant.index).mode().iloc[0])
    info["plant_month"] = info["year"].map(plant["plant_month"]).fillna(pm).astype(int)
    info["plant_year"] = info["year"].map(plant["plant_year"]).fillna(
        info["year"] + lag).astype(int)

    rows = []
    for system, nat in ((PRE, pre), (INS, ins)):
        for _, r in nat.iterrows():
            rows.append({"year": int(r["year"]), "system": system,
                         "label": r["label"], "date_made": r["date_made"],
                         "value": r["value"], "n_units": r["n_units"],
                         "aggregation": r["aggregation"]})
    track = pd.DataFrame(rows)
    p = info.set_index("year")
    track["x"] = [_months_from_planting(d, p.at[y, "plant_year"],
                                        p.at[y, "plant_month"])
                  for d, y in zip(track["date_made"], track["year"])]
    track = track.sort_values(["year", "x"]).reset_index(drop=True)
    track["obs"] = track["year"].map(p["obs"])
    track["error_pct"] = 100 * (track["value"] / track["obs"] - 1)
    return track, info


def rank_years(track, info):
    """Years with an observation, a trend and both systems, best first by
    ``skill = 1 - mean(|forecast - obs|) / |trend - obs|`` (NaN, ranked
    last, when the trend hit the observation exactly)."""
    p = info.set_index("year")
    rows = []
    for y, g in track.groupby("year"):
        obs, trend = p.at[y, "obs"], p.at[y, "trend"]
        if pd.isna(obs) or pd.isna(trend) or g["system"].nunique() < 2:
            continue
        err = (g["value"] - obs).abs()
        miss = abs(trend - obs)
        rows.append({"year": int(y), "obs": obs, "trend": trend,
                     "trend_abs_err": miss,
                     "mean_abs_err": err.mean(),
                     "mean_abs_err_pre": err[g["system"] == PRE].mean(),
                     "mean_abs_err_in": err[g["system"] == INS].mean(),
                     "skill": 1 - err.mean() / miss if miss > 0 else np.nan,
                     "gain": miss - err.mean(),
                     "n_forecasts": len(g)})
    cols = ["year", "obs", "trend", "trend_abs_err", "mean_abs_err",
            "mean_abs_err_pre", "mean_abs_err_in", "skill", "gain",
            "n_forecasts"]
    out = pd.DataFrame(rows, columns=cols)
    return out.sort_values("skill", ascending=False, na_position="last") \
        .reset_index(drop=True)


def lead_skill(track, info):
    """National skill of each lead over every year with an observation:
    N, RMSE, MAPE, R2 (1 - SSE/SST)."""
    obs = info.set_index("year")["obs"]
    rows = []
    for (system, label), g in track.groupby(["system", "label"], sort=False):
        o = g["year"].map(obs)
        ok = o.notna() & g["value"].notna()
        if ok.sum() < 3:
            continue
        p, o = g.loc[ok, "value"].to_numpy(), o[ok].to_numpy()
        e = p - o
        sst = ((o - o.mean()) ** 2).sum()
        rows.append({"system": system, "label": label, "x": g["x"].mean(),
                     "n": int(ok.sum()),
                     "years": f"{int(g.loc[ok, 'year'].min())}-"
                              f"{int(g.loc[ok, 'year'].max())}",
                     "rmse": float(np.sqrt((e ** 2).mean())),
                     "mape": float((np.abs(e) / o).mean() * 100),
                     "r2": float(1 - (e ** 2).sum() / sst) if sst > 0 else np.nan})
    out = pd.DataFrame(rows)
    return out.sort_values(["system", "x"], ascending=[False, True]) \
        .drop(columns="x").reset_index(drop=True) if not out.empty else out


# ---------------------------------------------------------------------------
# figure
# ---------------------------------------------------------------------------
def _season_title(year, plant_year):
    if plant_year < year:
        return f"{year} harvest ({plant_year}/{str(year)[2:]} season)"
    return f"{year} harvest"


def plot(track, info, years, out_png, *, crop, model, units="t/ha"):
    """One panel per year, stacked in the order given: pre-season and
    in-season forecasts by the date made, with the observed yield and the
    trend as reference lines. Returns ``out_png``."""
    import matplotlib.pyplot as plt

    p = info.set_index("year")
    sub = track[track["year"].isin(years)]
    if sub.empty:
        raise ValueError(f"no forecasts for years {list(years)}")
    x0 = np.floor(sub["x"].min()) - 0.6
    x1 = sub["x"].max() + 0.6
    refs = pd.concat([sub["value"], p.loc[list(years), "obs"],
                      p.loc[list(years), "trend"]]).dropna()
    ymax = float(refs.max()) * 1.25
    labels = {PRE: "Pre-season forecast (S2S)",
              INS: f"In-season forecast ({display_model_name(model)})"}

    with style_ctx():
        fig, axes = plt.subplots(len(years), 1, figsize=(6.6, 2.9 * len(years)),
                                 sharey=True, squeeze=False)
        axes = axes[:, 0]
        for ax, year in zip(axes, years):
            obs, trend = p.at[year, "obs"], p.at[year, "trend"]
            pm = int(p.at[year, "plant_month"])
            ax.axvspan(x0, 0, color=SHADE_PRE, lw=0, zorder=0)
            ax.axvspan(0, 1, color=SHADE_PLANT, lw=0, zorder=0)
            for value, color, ls, lw, text in (
                    (trend, C_TREND, ":", 1.0, "Trend"),
                    (obs, C_OBS, "--", 1.1, "Observed")):
                if pd.isna(value):
                    continue
                ax.axhline(value, color=color, lw=lw, ls=ls, zorder=1)
                ax.text(1.01, value / ymax, f"{text}\n{value:.2f}",
                        transform=ax.transAxes, ha="left", va="center",
                        fontsize=7.5, linespacing=1.1,
                        color=C_OBS if text == "Observed" else INK2)
            g = sub[sub["year"] == year]
            for system in (PRE, INS):
                s = g[g["system"] == system]
                if s.empty:
                    continue
                ax.plot(s["x"], s["value"], color=COLORS[system], lw=1.6,
                        marker=MARKERS[system], ms=5 if system == PRE else 4.6,
                        mec="white", mew=0.8, zorder=3, label=labels[system])
                # the last value of each series, the one a reader quotes
                ax.annotate(f"{s['value'].iloc[-1]:.2f}",
                            (s["x"].iloc[-1], s["value"].iloc[-1]),
                            xytext=(0, 7), textcoords="offset points",
                            ha="center", fontsize=7.5, color=INK2)
            for xc, text in ((x0 / 2, "Pre-season"), (0.5, "Planting"),
                             ((1 + x1) / 2, "In-season")):
                ax.text(xc, ymax * 0.97, text, ha="center", va="top",
                        fontsize=8, color=INK2)
            ticks = np.arange(np.ceil(x0), np.floor(x1) + 1)
            ax.set_xticks(ticks)
            ax.set_xticklabels([MONTHS[(pm - 1 + int(t)) % 12] for t in ticks])
            ax.tick_params(axis="x", which="minor", bottom=False)
            ax.set_xlim(x0, x1)
            ax.set_ylim(0, ymax)
            ax.set_ylabel(f"National {crop} yield ({units})")
            ax.set_title(_season_title(year, int(p.at[year, "plant_year"])),
                         fontsize=9, loc="left", pad=3)
            despine(ax)
        axes[-1].set_xlabel("Month the forecast was made")
        handles = [plt.Line2D([], [], color=COLORS[s], lw=1.6, marker=MARKERS[s],
                              ms=5, mec="white", mew=0.8) for s in (PRE, INS)]
        axes[-1].legend(handles, [labels[PRE], labels[INS]], loc="upper center",
                        bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False,
                        handlelength=2.2)
        fig.tight_layout(h_pad=1.2)
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)
    return out_png


def notes(track, info, ranking, skill, years, *, country, crop, model, db,
          s2s_run):
    """Companion text: what the panels show, every plotted value, the year
    ranking and each lead's national skill (with N)."""
    p = info.set_index("year")
    pre = track[(track["system"] == PRE) & track["year"].isin(years)]
    inits = pre.drop_duplicates("label").sort_values("x")["label"].tolist()
    lines = [
        f"{country} {crop}: national yield forecasts by the date each was made, "
        f"harvest years {', '.join(map(str, years))} (top to bottom).",
        "",
        f"Pre-season = S2S model ({Path(s2s_run).name}, hindcasts.csv): "
        f"{', '.join(inits)}, each dated the {S2S_POST_DAY}th, when NOAA posts "
        f"it. The planting month is shaded.",
        f"In-season = {display_model_name(model)} ({Path(db).name}), one "
        f"forecast per stage, dated the first day of the month after the "
        f"stage's data cutoff.",
        "Both are leave-one-year-out hindcasts: the plotted year never trained "
        "the models, but later years did, so these are not the forecasts a "
        "system running in real time would have issued.",
        "National = area-weighted mean of each system's own units "
        "(HarvestStat area for S2S, the DB's Area (ha) for the outlook). "
        "Observed = the outlook DB's national observed yield. Trend = the S2S "
        "run's leave-one-year-out linear trend per unit, weighted the same way. "
        "Each point is one national forecast (N = 1 season).",
    ]
    for y in years:
        obs, trend = p.at[y, "obs"], p.at[y, "trend"]
        head = (f"{y}: observed {obs:.3f} t/ha" if pd.notna(obs)
                else f"{y}: no observation")
        if pd.notna(trend):
            head += f", trend {trend:.3f} t/ha"
            if pd.notna(obs):
                head += f" (observed {100 * (obs / trend - 1):+.0f}% vs trend)"
        lines += ["", head]
        for _, r in track[track["year"] == y].iterrows():
            err = f"  ({r['error_pct']:+.0f}%)" if pd.notna(r["error_pct"]) else ""
            lines.append(f"  {r['system']:<10} {r['label']:<9} "
                         f"{r['date_made'].isoformat()}  {r['value']:.3f} t/ha{err}")
    if not ranking.empty:
        lines += ["", "Year ranking, skill = 1 - mean |forecast - obs| / "
                      "|trend - obs| (gain = the same two errors subtracted, "
                      "t/ha), over years with both systems and an observation "
                      f"(N = {len(ranking)} seasons):"]
        for _, r in ranking.iterrows():
            lines.append(f"  {int(r['year'])}  skill {r['skill']:+.2f}  gain "
                         f"{r['gain']:+.3f}  trend err "
                         f"{r['trend_abs_err']:.3f}  forecast err "
                         f"{r['mean_abs_err']:.3f} (pre {r['mean_abs_err_pre']:.3f}, "
                         f"in {r['mean_abs_err_in']:.3f}, "
                         f"{int(r['n_forecasts'])} forecasts)")
    if not skill.empty:
        lines += ["", "National skill of each lead over all years with an "
                      "observation:"]
        for _, r in skill.iterrows():
            lines.append(f"  {r['system']:<10} {r['label']:<9} N={r['n']:>2} "
                         f"({r['years']})  RMSE {r['rmse']:.3f}  "
                         f"MAPE {r['mape']:5.1f}%  R2 {r['r2']:6.2f}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_")


def run(*, db, table, model, s2s_run, country, crop, out, years=None,
        n_years=2, season_name=None, season=None, min_offset=MIN_OFFSET):
    """Build, rank, draw and write the season track. Returns a dict of paths
    and frames."""
    out = Path(out)
    dir_plots, dir_csvs = out / "plots", out / "csvs"
    dir_plots.mkdir(parents=True, exist_ok=True)
    dir_csvs.mkdir(parents=True, exist_ok=True)

    pre = s2s_national(load_s2s(s2s_run, country, crop, season_name), country,
                       min_offset=min_offset)
    ins = outlook_national(db, table, model, country, season=season)
    track, info = build_track(pre, ins)
    ranking = rank_years(track, info)
    if years:
        years = [int(y) for y in years]
        missing = sorted(set(years) - set(track["year"]))
        if missing:
            raise ValueError(f"no forecasts for {missing}")
    else:
        if ranking.empty:
            raise ValueError("no year has an observation, a trend and both "
                             "systems; pass years=")
        years = ranking["year"].head(n_years).tolist()
        logger.info(f"season_track: best years by skill against trend: {years}")
    skill = lead_skill(track, info)

    stem = f"{_slug(country)}_{_slug(crop)}_{_slug(model)}_" + \
        "_".join(map(str, years))
    png = plot(track, info, years, dir_plots / f"season_track_{stem}.png",
               crop=crop, model=model)
    txt = dir_plots / f"season_track_{stem}.txt"
    txt.write_text(notes(track, info, ranking, skill, years, country=country,
                         crop=crop, model=model, db=db, s2s_run=s2s_run),
                   encoding="utf-8")
    csv = dir_csvs / f"season_track_{stem}.csv"
    track.round(4).to_csv(csv, index=False)
    csv_rank = dir_csvs / f"season_track_{stem}_ranking.csv"
    ranking.round(4).to_csv(csv_rank, index=False)
    _write_lookup([(png.name, csv.name,
                    f"{country} {crop}: pre-season (S2S) and in-season "
                    f"({display_model_name(model)}) national forecasts by date "
                    f"made, {', '.join(map(str, years))}")],
                  dir_plots, dir_csvs)
    return {"png": png, "txt": txt, "csv": csv, "ranking_csv": csv_rank,
            "years": years, "track": track, "info": info, "ranking": ranking,
            "skill": skill}


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="python -m geocif.viz.season_track",
        description="One season's national yield forecast, pre-season (S2S) "
                    "to in-season (outlook DB), by the date each was made.")
    ap.add_argument("--db", required=True, help="outlook DB path")
    ap.add_argument("--table", required=True, help="crop table, e.g. zimbabwe_maize")
    ap.add_argument("--model", required=True, help="in-season model, e.g. kumo")
    ap.add_argument("--s2s-run", required=True,
                    help="s2s_africa run directory holding hindcasts.csv")
    ap.add_argument("--country", required=True,
                    help="HarvestStat country name, e.g. Zimbabwe")
    ap.add_argument("--crop", required=True, help="crop, e.g. maize")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--years", type=int, nargs="*",
                    help="harvest years, top to bottom (default: best by skill "
                         "against trend)")
    ap.add_argument("--n-years", type=int, default=2,
                    help="how many best years when --years is not given")
    ap.add_argument("--season-name", help="S2S season_name when there are several")
    ap.add_argument("--season", type=int, help="outlook Season when there are several")
    ap.add_argument("--min-offset", type=int, default=MIN_OFFSET,
                    help="earliest S2S offset kept, in months before planting "
                         "(0 = the planting-month init; negative adds inits "
                         "issued after planting)")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    res = run(db=a.db, table=a.table, model=a.model, s2s_run=a.s2s_run,
              country=a.country, crop=a.crop, out=a.out, years=a.years,
              n_years=a.n_years, season_name=a.season_name, season=a.season,
              min_offset=a.min_offset)
    print(res["png"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
