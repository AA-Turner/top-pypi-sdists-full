# -*- coding: utf-8 -*-
"""Shift maps: one arrow per region for how a forecast moved across issues.

The election-shift map applied to forecasts: an arrow at each region whose
direction and colour say which way the forecast moved between the first
issue and the last, and whose length says by how much. One renderer serves
two sources:

* the Africa S2S model (``experiments/s2s_africa.py``): successive inits for
  the same harvest year, read from the ``forecasts.csv`` of each run. The
  runs should be replays (``s2s_africa.run(as_of_init=...)``) made with one
  version of the code and data, so the arrows carry S2S information only;
* the in-season outlook DB: successive stages (as-of months) of one harvest
  year, read through ``viz/_outlook_db.load_outlook``.

Both adapters produce the same tidy *series* frame (one row per region and
issue, ``SERIES_COLS``), :func:`compute_shifts` reduces it to one row per
region, and :func:`render` draws it. Direction is normalised per metric:
brown pointing right always means the forecast moved toward the WORSE
outcome (a higher chance of a lower-tercile yield, or a lower yield), teal
pointing left toward the better one, so both metrics read alike.

By default only regions that moved the same way at every step are drawn
(``select="consistent"``, the election map's rule): with three issues a
region that went up and then back down carries no trend, and drawing its
net change would read as one. ``select="all"`` draws every region's net
change. Besides the full-span map, one map per consecutive pair of issues
shows each update on its own (``pairs``, on by default). Arrows are faded
where the latest issue reports no forecast skill for the region. Undrawn
regions stay in the companion CSV with the reason.

Issues are ordered by a parsed date (``init_used`` for S2S, the stage's
as-of month for the outlook DB), never by sorting labels: the outlook
writer's month-name-first labels do not sort chronologically.

CLI::

    python -m geocif.viz.shift_map s2s --config <4 configs> \\
        --init 2026-08 --init 2026-09 --init 2026-10     # or --run <dir>...
    python -m geocif.viz.shift_map outlook --config <4 configs> \\
        --db outlook_X.db --table kenya_maize [--model trend] [--year 2026]
"""
import argparse
import logging
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.experiments.s2s_africa import region_suffix
from geocif.viz.aggregation import _write_lookup
from geocif.viz.s2s_africa import (
    FEWS_CPT, PROJ, _dirs, basemap, finish_map, legend_box, legend_square,
    no_skill_mask, read_boundaries)

logger = logging.getLogger(__name__)

#: Brown = toward the worse outcome, teal = toward the better one: the two
#: ends of the FEWS probability ramp the S2S choropleths use, so an arrow and
#: a polygon speak the same colour. OKLab separation of the pair: 17 (normal
#: vision), 9.7 protan, 12.3 deutan, 19.9 tritan, above the 15 / 8 floors.
WORSE, BETTER = FEWS_CPT[-1][1], FEWS_CPT[0][1]
#: Transparency of an arrow whose region has no forecast skill.
FADE = "@55"
#: Arrows lean upward like the election map's: right for worse, left for
#: better. The tilt carries no information.
TILT = 20
#: Shortest arrow drawn, so a small but drawn change is still visible.
MIN_CM = 0.25
#: GMT vector head: 0.16 cm long, 45-degree opening, half-filled shape.
#: The map arrows and the legend arrows are built from the same head so
#: they look alike.
HEAD, HEAD_MODS = "0.16c", "+a45+h0.4"
#: Map arrows: centred on the point (+jc), head at the end, heads shrink
#: on arrows shorter than 0.4 cm so a short arrow is not all head.
STYLE = f"v{HEAD}+e{HEAD_MODS}+jc+n0.4c"
PEN = "1p"
#: Outline of every forecast region, under the arrows: light enough that
#: the arrows stay the figure, dark enough to tell which region an arrow
#: sits in and which forecast regions got none.
OUTLINE_PEN = "0.3p,gray55"

SERIES_COLS = ["region_id", "region", "country", "crop", "season", "year",
               "issue", "issue_order", "value", "skill"]
#: One arrow per (combination, region); seasons are folded later.
GROUP = ["country", "crop", "season", "year", "region_id"]


@dataclass(frozen=True)
class Metric:
    """What one shift map measures, and how a change becomes an arrow."""
    key: str
    label: str            # the quantity, for titles
    units: str
    worse_is_up: bool     # a rise is the worse outcome (P_low); a fall is (yield)
    cm_per_unit: float    # arrow length per unit of net change
    worse_text: str       # legend: "Toward <worse_text>"
    better_text: str
    min_change: float = 0.0   # smaller net changes are listed, not drawn
    max_cm: float = 2.5       # longest arrow; the CSV keeps the true change
    fmt: str = "{:+.1f}"

    @property
    def per_cm(self):
        """The change one centimetre of arrow stands for."""
        return 1.0 / self.cm_per_unit


P_LOW = Metric("p_low", "chance of a lower-tercile yield", "pp", True, 0.1,
               "a higher chance of a lower-tercile yield",
               "a lower chance of a lower-tercile yield", min_change=2.0)
YIELD_MGHA = Metric("yield_mgha", "predicted yield", "Mg/ha", False, 2.0,
                    "a lower yield", "a higher yield", min_change=0.05,
                    fmt="{:+.2f}")
YIELD_PCT = Metric("yield_pct", "predicted yield departure from trend", "%",
                   False, 0.1, "a lower yield", "a higher yield",
                   min_change=2.0)
METRICS = {m.key: m for m in (P_LOW, YIELD_MGHA, YIELD_PCT)}


# ---------------------------------------------------------------------------
# sources -> series
# ---------------------------------------------------------------------------
#: forecasts.csv column and the factor that puts it in the metric's units.
S2S_VALUE = {"p_low": ("P_low", 100.0), "yield_pct": ("ahat", 100.0),
             "yield_mgha": ("yhat_tha", 1.0)}


def s2s_series(run_dirs, metric):
    """One row per (combination, region, issue) from s2s_africa run dirs.

    Issues are ordered by the parsed ``init_used`` (written since 0.4.1081);
    a run without it predates the column and is refused rather than ordered
    by directory name. An issue present in two runs keeps the later-listed
    one, with a warning.
    """
    col, scale = S2S_VALUE[metric.key]
    frames = []
    for d in run_dirs:
        d = Path(d)
        fc = pd.read_csv(d / "forecasts.csv")
        if fc.empty:
            logger.info(f"{d}: no forecasts")
            continue
        if "init_used" not in fc.columns:
            raise ValueError(f"{d}: forecasts.csv has no init_used column "
                             f"(written by geocif >= 0.4.1081); re-run it")
        if col not in fc.columns:
            raise ValueError(f"{d}: forecasts.csv has no {col} column")
        init = pd.to_datetime(fc["init_used"], format="%Y-%m")
        frames.append(pd.DataFrame({
            "region_id": fc["fnid"], "region": fc["fnid"],
            "country": fc["country"], "crop": fc["crop"],
            "season": fc["season_name"],
            "year": fc["harvest_year"].astype(int),
            "issue": fc["init_used"],
            "issue_order": init.dt.year * 12 + init.dt.month,
            "value": fc[col] * scale,
            "skill": ~no_skill_mask(fc),
        }))
    if not frames:
        return pd.DataFrame(columns=SERIES_COLS)
    s = pd.concat(frames, ignore_index=True).dropna(subset=["value"])
    dup = s.duplicated(GROUP + ["issue"], keep="last")
    if dup.any():
        logger.warning(f"{int(dup.sum())} (region, issue) rows appear in "
                       f"more than one run; the later-listed run wins")
        s = s[~dup]
    return s[SERIES_COLS].reset_index(drop=True)


def outlook_series(db, table, *, model=None, year=None, metric=YIELD_MGHA):
    """One row per (region, stage) of one harvest year of an outlook table.

    Stages are ordered by their as-of month in season order (leadtime's
    rule), never by label. The DB carries predicted yield in Mg/ha only.
    ``year`` defaults to the latest harvest year in the table; ``model``
    must be given when the table holds more than one.
    """
    from geocif.utils import country_region_key
    from geocif.viz._outlook_db import PRED, load_outlook
    from geocif.viz.leadtime import _asof_month, _season_order

    if metric.key != YIELD_MGHA.key:
        raise ValueError(f"the outlook DB carries predicted yield in Mg/ha; "
                         f"{metric.key!r} is not available from it")
    df = load_outlook(db, table, model=model, text_columns=("Country", "Crop"))
    if df.empty:
        return pd.DataFrame(columns=SERIES_COLS)
    models = sorted(df["Model"].dropna().unique())
    if len(models) > 1:
        raise ValueError(f"{table} holds models {models}; pass model=")
    year = int(year if year is not None else df["year"].max())
    df = df[df["year"] == year].copy()
    if df.empty:
        raise ValueError(f"{table}: no outlook rows for harvest year {year}")
    df["asof"] = [_asof_month(s, w) for s, w in zip(df["stage"], df["swd"])]
    df = df.dropna(subset=["asof"])
    if df.empty:
        raise ValueError(f"{table} {year}: no stage name maps to an as-of "
                         f"month (month-window stages are needed)")
    order = _season_order(df["asof"].astype(int))
    # Country/Crop come from the DB when present: a pooled table holds
    # several countries, in Title Case rather than config slugs, and the
    # key normalises both. The table name is the fallback for older DBs.
    country, crop = table.rsplit("_", 1)
    countries = df["Country"].fillna(country)
    if df["Crop"].notna().any():
        crop = df["Crop"].dropna().iloc[0]
    return pd.DataFrame({
        "region_id": country_region_key(countries, df["Region"]),
        "region": df["Region"], "country": countries, "crop": crop,
        "season": "", "year": year,
        "issue": df["swd"].where(df["swd"].notna(), df["stage"]),
        "issue_order": df["asof"].astype(int).map(order),
        "value": df[PRED], "skill": np.nan,
    })[SERIES_COLS].reset_index(drop=True)


# ---------------------------------------------------------------------------
# series -> shifts
# ---------------------------------------------------------------------------
SHIFT_COLS = GROUP + ["region", "n_issues", "first_issue", "last_issue",
                      "first", "last", "delta", "signed", "consistent",
                      "skill", "drawn", "reason", "path"]


def compute_shifts(series, metric, select="consistent"):
    """One row per (combination, region): first and last value, net change.

    ``signed`` is the change toward the worse outcome (positive = worse), so
    both metrics draw the same way. ``consistent`` is the election map's
    rule: every step moved the way the net change did. ``drawn`` applies
    ``select`` and ``metric.min_change``; undrawn rows stay in the frame
    with the reason. A region seen at one issue only has no shift.
    """
    if select not in ("consistent", "all"):
        raise ValueError(f"select must be 'consistent' or 'all', "
                         f"got {select!r}")
    rows = []
    s = series.sort_values(GROUP + ["issue_order"], kind="stable")
    for key, g in s.groupby(GROUP, sort=False, dropna=False):
        v = g["value"].to_numpy(dtype=float)
        if len(v) < 2:
            continue
        delta = float(v[-1] - v[0])
        steps = np.diff(v)
        consistent = bool(delta != 0
                          and np.all(np.sign(steps) == np.sign(delta)))
        if abs(delta) < metric.min_change:
            reason = f"net change below {metric.min_change:g} {metric.units}"
        elif not consistent and select == "consistent":
            reason = ("a step moved neither way" if np.any(steps == 0)
                      else "direction changed between issues")
        else:
            reason = ""
        rows.append({
            **dict(zip(GROUP, key)), "region": g["region"].iloc[-1],
            "n_issues": len(v),
            "first_issue": g["issue"].iloc[0], "last_issue": g["issue"].iloc[-1],
            "first": float(v[0]), "last": float(v[-1]), "delta": delta,
            "signed": delta if metric.worse_is_up else -delta,
            "consistent": consistent, "skill": g["skill"].iloc[-1],
            "drawn": reason == "", "reason": reason,
            "path": " > ".join(f"{x:g}" for x in v)})
    return pd.DataFrame(rows, columns=SHIFT_COLS)


def one_per_region(shifts):
    """Keep one row per region on a map: the season with the larger move.

    A region grown in two seasons appears under both; the map has one
    arrow per polygon, so the larger movement is drawn and the CSV keeps
    ``season`` to say which. Drawn rows take precedence over undrawn ones.
    """
    if shifts.empty:
        return shifts
    ranked = (shifts.assign(_abs=shifts["signed"].abs())
              .sort_values(["drawn", "_abs"], ascending=[False, False],
                           kind="stable"))
    out = ranked.drop_duplicates("region_id", keep="first").drop(columns="_abs")
    n = len(shifts) - len(out)
    if n:
        logger.info(f"{n} region-season rows folded into their region's "
                    f"larger move")
    return out


# ---------------------------------------------------------------------------
# shifts -> map
# ---------------------------------------------------------------------------
def arrow_geometry(signed, metric):
    """(angle, length_cm) for pygmt's ``direction``.

    The angle is counter-clockwise from horizontal, so ``TILT`` points
    right-and-up (worse) and ``180 - TILT`` left-and-up (better). Length is
    the net change scaled, clipped to [MIN_CM, metric.max_cm].
    """
    signed = np.asarray(signed, dtype=float)
    angle = np.where(signed >= 0, TILT, 180 - TILT)
    length = np.clip(np.abs(signed) * metric.cm_per_unit, MIN_CM,
                     metric.max_cm)
    return angle, length


def region_frame(gdf, key_col, labels=None):
    """One polygon per region: ``region_id``, ``geometry`` (and ``region``
    when ``labels`` is given). A boundary file with two polygons for one key
    is dissolved, or the region would get two arrows and two outlines."""
    import geopandas as gpd

    g = gpd.GeoDataFrame({"region_id": gdf[key_col].to_numpy()},
                         geometry=gdf.geometry.to_numpy(), crs=gdf.crs)
    if labels is not None:
        g["region"] = np.asarray(labels)
    if g["region_id"].duplicated().any():
        g = g.dissolve(by="region_id", as_index=False, aggfunc="first")
    return g


def legend_rows(metric, faded):
    """pslegend rows: the two directions, the faded state, the scale."""
    def arrow(head, fill, text):
        # pslegend: the symbol code carries the head size and modifiers
        # (without the size nothing is drawn), the size column is the
        # length; +b puts the head at the start, so the row points left
        return (f"S 0.3c v{HEAD}{head}{HEAD_MODS} 1.0c {fill} {PEN},{fill} "
                f"1.5c {text}")

    rows = [arrow("+e", WORSE, f"Toward {metric.worse_text}"),
            arrow("+b", BETTER, f"Toward {metric.better_text}")]
    if faded:
        rows.append(arrow("+e", WORSE + FADE,
                          "No forecast skill for the region at the latest "
                          "issue"))
    rows.append(legend_square("-", "Forecast region; no arrow = no clear "
                                   "change", pen=OUTLINE_PEN, text_x="1.5c"))
    rows.append(arrow("+e", "gray40",
                      f"1 cm of arrow = {metric.per_cm:g} {metric.units} of "
                      f"change; arrows capped at "
                      f"{metric.max_cm * metric.per_cm:g} {metric.units}"))
    return rows


def month_label(init):
    """'Aug 2026' for '2026-08'; any other label unchanged."""
    try:
        return pd.to_datetime(init, format="%Y-%m").strftime("%b %Y")
    except (ValueError, TypeError):
        return str(init)


def subtitle_text(issue_word, issues, select):
    """One short line: a GMT subtitle never wraps. ``issue_word`` is the
    singular noun for an issue ("init", "issue")."""
    word = f"{issue_word.capitalize()}s"
    if len(issues) == 2:
        return f"{word} {issues[0]} to {issues[1]}; change between the two"
    span = (f"{word} {issues[0]} to {issues[-1]}" if len(issues) > 1
            else f"{word} {issues[0]}")
    rule = ("arrows where every issue moved the same way"
            if select == "consistent" else "net change, first to last issue")
    return f"{span}; {rule}"


def spans(series, pairs=True):
    """The issue sets to map, as ``(issues, subset)``: the whole span, then
    each consecutive pair of issues when ``pairs``.

    A two-issue series is its own only pair, so it yields once. A region
    missing one issue of a pair has no shift in that pair.
    """
    issues = (series[["issue", "issue_order"]].drop_duplicates()
              .sort_values("issue_order")["issue"].tolist())
    yield issues, series
    if pairs and len(issues) > 2:
        for a, b in zip(issues, issues[1:]):
            yield [a, b], series[series["issue"].isin([a, b])]


def render(shifts, regions, metric, *, title, subtitle, stem, dir_plots,
           dir_csvs, extent=None, proj=PROJ, desc="", lookup=None):
    """Draw one shift map and write its companion CSV.

    ``regions`` (from :func:`region_frame`) are the forecast regions: each
    is outlined, and an arrow sits at a point inside it. Every region in
    ``shifts`` goes to the CSV with its arrow geometry and reason; only
    ``drawn`` rows with a polygon get an arrow. Faded arrows are drawn
    first so a skilled arrow is never hidden under one.
    """
    import pygmt

    pts = regions.geometry.representative_point()
    cent = pd.DataFrame({"region_id": regions["region_id"].to_numpy(),
                         "lon": pts.x.to_numpy(), "lat": pts.y.to_numpy()})
    if "region" in regions.columns:
        cent["region"] = regions["region"].to_numpy()
    g = shifts.merge(cent, on="region_id", how="left",
                     suffixes=("", "_cent"))
    if "region_cent" in g.columns:
        g["region"] = g["region_cent"].where(g["region_cent"].notna(),
                                             g["region"])
        g = g.drop(columns="region_cent")
    nomatch = g["lon"].isna()
    if nomatch.any():
        logger.warning(f"{stem}: {int(nomatch.sum())} regions have no "
                       f"boundary polygon and are not drawn")
    g["angle"], g["length_cm"] = arrow_geometry(g["signed"], metric)
    csv_name = f"{stem}.csv"
    g.round(4).to_csv(dir_csvs / csv_name, index=False)

    d = g[g["drawn"] & ~nomatch]
    faded = d["skill"].eq(False)
    fig = pygmt.Figure()
    basemap(fig, title, extent, proj, subtitle=subtitle)
    with tempfile.TemporaryDirectory() as td:
        if not regions.empty:
            f = Path(td) / "regions.gmt"
            regions[["region_id", "geometry"]].to_file(f, driver="OGR_GMT")
            fig.plot(data=str(f), pen=OUTLINE_PEN, close=True)
        for fade in (True, False):
            for worse in (True, False):
                sub = d[(faded == fade) & ((d["signed"] >= 0) == worse)]
                if sub.empty:
                    continue
                col = (WORSE if worse else BETTER) + (FADE if fade else "")
                fig.plot(x=sub["lon"].to_numpy(), y=sub["lat"].to_numpy(),
                         style=STYLE,
                         direction=[sub["angle"].to_numpy(),
                                    sub["length_cm"].to_numpy()],
                         pen=f"{PEN},{col}", fill=col)
        legend_box(fig, td, legend_rows(metric, bool(faded.any())), 11.5)
    png = Path(dir_plots) / f"{stem}.png"
    finish_map(fig, png)
    if lookup is not None:
        lookup.append((png.name, csv_name, desc))
    logger.info(f"{stem}: {len(d)} arrows ({int(faded.sum())} faded) of "
                f"{len(g)} regions")
    return png


# ---------------------------------------------------------------------------
# drivers
# ---------------------------------------------------------------------------
def _finish(lookup, base, dir_plots, dir_csvs):
    _write_lookup(lookup, dir_plots, dir_csvs)
    logger.info(f"shift maps -> {base} ({len(lookup)} figures)")
    return base


def render_series(series, metric, regions, *, title, stem, issue_word, select,
                  pairs, dir_plots, dir_csvs, lookup, desc, extent=None,
                  proj=PROJ):
    """The maps of one series (one crop): the full span and, when
    ``pairs``, one per consecutive pair of issues, named ``<stem>`` and
    ``<stem>_<a>_to_<b>``. Every map outlines the series' regions, so the
    pair maps share one outline set. ``desc`` is the lookup text up to the
    span."""
    regions = regions[regions["region_id"].isin(series["region_id"])]
    full = next(spans(series, False))[0]
    for issues, sub in spans(series, pairs):
        labels = [month_label(i) for i in issues]
        suffix = (region_suffix(f"{issues[0]} to {issues[-1]}")
                  if issues != full else "")
        render(one_per_region(compute_shifts(sub, metric, select)), regions,
               metric, title=title,
               subtitle=subtitle_text(issue_word, labels, select),
               stem=stem + suffix, dir_plots=dir_plots, dir_csvs=dir_csvs,
               extent=extent, proj=proj, lookup=lookup,
               desc=f"{desc} from the {labels[0]} to the {labels[-1]} "
                    f"{issue_word}")


def s2s_shift_maps(run_dirs, out, gpkg, *, metrics=(P_LOW,),
                   select="consistent", pairs=True, extent=None, label="",
                   proj=PROJ):
    """Maps per metric and crop from a list of s2s_africa run dirs."""
    gdf = read_boundaries(gpkg)
    adm2 = gdf["ADMIN2"].fillna("").astype(str).str.strip()
    regions = region_frame(gdf, "fnid",
                           labels=adm2.where(adm2 != "", gdf["ADMIN1"]))
    base, dir_plots, dir_csvs = _dirs(out, "shift_maps")
    where = f" in {label}" if label else ""
    lookup = []
    for metric in metrics:
        series = s2s_series(run_dirs, metric)
        if series.empty:
            logger.info(f"{metric.key}: nothing to map")
            continue
        series.to_csv(dir_csvs / f"series_{metric.key}.csv", index=False)
        for crop in sorted(series["crop"].unique()):
            sub = series[series["crop"] == crop]
            year = int(sub["year"].mode().iloc[0])
            render_series(
                sub, metric, regions,
                title=f"Change in the {metric.label}, {crop}{where}, {year}",
                stem=f"shift_{metric.key}_{crop}", issue_word="init",
                select=select, pairs=pairs, dir_plots=dir_plots,
                dir_csvs=dir_csvs, lookup=lookup, extent=extent, proj=proj,
                desc=f"{crop} {year}: change in the {metric.label}")
    return _finish(lookup, base, dir_plots, dir_csvs)


def replay_s2s(parser, inits, *, stamp=None, figures=True, **run_kw):
    """Re-issue the S2S run from each init with today's code and data,
    all into the dated folder ``stamp``, each with its own maps (the
    P(lower tercile) map of every issue beside the shift maps)."""
    from geocif.experiments import s2s_africa

    return [s2s_africa.run(parser=parser, as_of_init=i, figures=figures,
                           stamp=stamp, **run_kw) for i in inits]


def _parser(path_config_files):
    from geocif import logger as log

    _, parser = log.setup_logger_parser(path_config_files)
    return parser


def s2s_run(path_config_files, *, inits=None, runs=None, out=None,
            metrics=(P_LOW,), select="consistent", pairs=True,
            figures=True):
    """Shift maps for a regional S2S config: replay ``inits`` (or take
    existing ``runs``), then map. Region, extent and boundaries come from
    the config exactly as the S2S run reads them.

    One dated folder per job: the replays and the maps share one stamp
    (``<stamp>/explore/s2s_africa_<region>_asofYYYYMM`` beside
    ``<stamp>/explore/s2s_shift_<region>``); maps drawn from existing runs
    go beside the latest of them.
    """
    from geocif.experiments.s2s_africa import (
        analysis_dir, config_extent, region_suffix, resolve_paths, run_stamp)

    parser = _parser(path_config_files)
    _, root, meta = resolve_paths(parser)
    label = parser.get("ML", "s2s_region_label", fallback="")
    name = f"s2s_shift{region_suffix(label)}"
    if runs is None:
        if not inits:
            raise ValueError("give inits to replay or existing run dirs")
        stamp = run_stamp()
        runs = replay_s2s(parser, inits, stamp=stamp, figures=figures)
        default = analysis_dir(root, name, stamp)
    else:
        default = Path(runs[-1]).parent / name
    out = Path(out) if out else default
    out.mkdir(parents=True, exist_ok=True)
    (out / "runs.txt").write_text("\n".join(str(r) for r in runs) + "\n")
    return s2s_shift_maps(runs, out, meta / "boundary_files" / "adm_shapefile.gpkg",
                          metrics=metrics, select=select, pairs=pairs,
                          extent=config_extent(parser), label=label)


def outlook_run_dir(root, db):
    """``<root>/ml/analysis/<stamp>``, the run folder of the outlook that
    wrote ``db``: ``outlook_09_17_2026_14h18.db`` was written by the run
    whose products sit in ``September_17_2026_14h18/``. None for a DB not
    named that way."""
    import arrow as ar

    m = re.search(r"outlook_(\d{2})_(\d{2})_(\d{4})_(\d{2})h(\d{2})",
                  Path(db).name)
    if not m:
        return None
    mo, d, y, h, mi = (int(x) for x in m.groups())
    return (Path(root) / "ml" / "analysis"
            / ar.Arrow(y, mo, d, h, mi).format("MMMM_DD_YYYY_HH[h]mm"))


def outlook_run(path_config_files, db, tables, *, model=None, year=None,
                out=None, select="consistent", pairs=True, margin=0.5):
    """Shift maps of predicted yield across the stages of one harvest year,
    one map per outlook table (``{country}_{crop}``). By default they go to
    ``shift_maps/`` in the outlook run's own folder, beside ``outlook/``."""
    from geocif.experiments.s2s_africa import resolve_paths, run_stamp
    from geocif.yield_outlook import _load_shapefiles

    parser = _parser(path_config_files)
    _, root, _ = resolve_paths(parser)
    db = Path(db)
    db = db if db.is_absolute() else root / "ml" / "db" / db
    run_dir = (outlook_run_dir(root, db)
               or root / "ml" / "analysis" / run_stamp())
    base, dir_plots, dir_csvs = _dirs(Path(out) if out
                                      else run_dir / "shift_maps")
    by_table = {}
    for table in tables:
        series = outlook_series(db, table, model=model, year=year)
        if series.empty:
            logger.info(f"{table}: no outlook rows")
            continue
        series.to_csv(dir_csvs / f"series_{table}.csv", index=False)
        by_table[table] = series
    if not by_table:
        return base
    # Only the countries behind the tables: the full config may hold thirty.
    # The DB writes Title Case for pooled runs; the config wants slugs.
    def slug(c):
        return str(c).strip().lower().replace(" ", "_")

    dg, _ = _load_shapefiles(parser, countries=sorted(
        {slug(c) for s in by_table.values() for c in s["country"].unique()}))
    lookup = []
    for table, series in by_table.items():
        sub = dg[dg["Country Region"].isin(series["region_id"])]
        if sub.empty:
            logger.warning(f"{table}: no boundary polygon matches its regions")
            continue
        x0, y0, x1, y1 = sub.total_bounds
        names = ", ".join(sorted({slug(c).replace("_", " ").title()
                                  for c in series["country"].unique()}))
        crop, yr = series["crop"].iloc[0], int(series["year"].iloc[0])
        render_series(
            series, YIELD_MGHA, region_frame(sub, "Country Region"),
            title=f"Change in the predicted {crop} yield, {names}, {yr}",
            stem=f"shift_yield_mgha_{table}", issue_word="issue",
            select=select, pairs=pairs, dir_plots=dir_plots,
            dir_csvs=dir_csvs, lookup=lookup,
            extent=[x0 - margin, x1 + margin, y0 - margin, y1 + margin],
            desc=f"{table} {yr}: change in predicted yield (Mg/ha)")
    return _finish(lookup, base, dir_plots, dir_csvs)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("s2s", help="successive S2S inits of one season")
    a.add_argument("--config", nargs="+", required=True,
                   help="geobase, countries, crops, geocif config files")
    a.add_argument("--init", action="append",
                   help="YYYY-MM init to replay (repeatable)")
    a.add_argument("--run", action="append",
                   help="existing s2s_africa run dir instead (repeatable)")
    a.add_argument("--metric", action="append", choices=sorted(METRICS),
                   help="default p_low (repeatable)")
    b = sub.add_parser("outlook", help="stages of one outlook harvest year")
    b.add_argument("--config", nargs="+", required=True)
    b.add_argument("--db", required=True,
                   help="outlook_*.db; a bare name is looked up in ml/db")
    b.add_argument("--table", action="append", required=True,
                   help="{country}_{crop} table (repeatable)")
    b.add_argument("--model")
    b.add_argument("--year", type=int)
    for q in (a, b):
        q.add_argument("--select", choices=("consistent", "all"),
                       default="consistent")
        q.add_argument("--no-pairs", dest="pairs", action="store_false",
                       help="only the full-span map, no map per "
                            "consecutive pair of issues")
        q.add_argument("--out")
    ns = p.parse_args(argv)
    if ns.cmd == "s2s":
        metrics = tuple(METRICS[k] for k in (ns.metric or ["p_low"]))
        out = s2s_run(ns.config, inits=ns.init, runs=ns.run, out=ns.out,
                      metrics=metrics, select=ns.select, pairs=ns.pairs)
    else:
        out = outlook_run(ns.config, ns.db, ns.table, model=ns.model,
                          year=ns.year, out=ns.out, select=ns.select,
                          pairs=ns.pairs)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
