# -*- coding: utf-8 -*-
"""Config, runner and CLI for the snake chart.

Reads the ``[snake]`` section of the geocif config bundle (keys written there
literally only, so ``[DEFAULT]`` values cannot leak in, the cone's rule),
resolves the outlook DB and its run folder, builds the tracks with
:mod:`geocif.viz.snake_data`, draws with :mod:`geocif.viz.snake` and writes,
beside the run's ``outlook/`` folder::

    <run>/snake/plots/snake_{country}_{crop}_{model}_{region}_s{season}_{year}.png
    <run>/snake/csvs/snake_{country}_{crop}_{model}_{region}_s{season}_{year}.csv

The companion CSV is the tidy table with every z-score's inputs (raw value,
baseline mean / trend, sd, years, observation date and its kind, the run date
of each DB row). ``yield_outlook.run`` calls :func:`run` through
``_render_snake_figures`` (``[ML] make_snake_plots``: unset = on for admin_1
countries, off for admin_2; True or False applies to all); the CLI
re-plots from an existing DB::

    python -m geocif.viz.snake_run --config geobase.txt countries.txt crops.txt geocif.txt \\
        --db outlook_09_17_2026_14h18.db --table kenya_maize --model tabpfn --year 2026

Config::

    [ML]
    make_snake_plots = True

    [snake]
    cids = ['PRCPTOT', 'MEAN_ESI4WK', 'AUC_NDVI']  ; any CID from cid/definitions.py, at most 4 rows; 'cci', 'usda_yield' for the US
    invert = {}                                ; {CID: True/False} overrides the sign (Heat, Drought, ETREF are inverted by default)
    labels = {}                                ; {CID: row label}
    regions = ['all']                          ; every modeled unit (admin_1 or admin_2, as run); 'national' or names
    model =                                    ; empty = the run's first ML model in its models list
    layout = runs                              ; runs | split
    split =                                    ; split mode: step index of the last upper-lane issue
    deadband = 0.1                             ; smaller reversals stay on their lane; 0 = every reversal turns
    max_lanes = 3
    baseline_years = []                        ; empty = every year in the pool except the target
    baseline_last =                            ; N = indicator normal from the N years before the target year
    window = stage                             ; stage (cumulative) | month (as-of month only)
    obs_dates = observed                       ; observed (merged daily inputs, nominal fallback) | nominal
    formats = ['png']                          ; add 'pdf' for a vector copy
    cci_scale = repo                           ; repo (0-100) | plan (100-500)
    nass_offline = False
    title = {region}                           ; may use {region} {country} {crop} {year}; none = no title
    subtitle =                                 ; empty = none
    show_source = False                        ; footer with sources, baseline and caveats
    show_roles = False                         ; role under each row label
    palette = viridis                          ; dot colours: viridis, blues, magma, oranges, teal, accent, or a colormap
"""
import argparse
import ast
import configparser
import logging
import sqlite3
import sys
from pathlib import Path

import pandas as pd

from geocif.viz import snake
from geocif.viz import snake_data as sd

logger = logging.getLogger(__name__)

DEFAULTS = {
    "rows": ["PRCPTOT", "MEAN_ESI4WK", "AUC_NDVI"],
    "cids": None,
    "invert": {},
    "labels": {},
    "regions": ["all"],
    "model": None,
    "layout": "runs",
    "split": None,
    "deadband": 0.1,
    "max_lanes": 3,
    "baseline_years": None,
    "baseline_last": None,
    "window": "stage",
    "obs_dates": "observed",
    "formats": ["png"],
    "min_region_frac": 1.0,
    "cci_scale": "repo",
    "nass_offline": False,
    "title": "{region}",
    "subtitle": None,
    "show_source": False,
    "show_roles": False,
    "palette": "viridis",
}
USDA_ROWS = ("cci", "cci_ge", "usda_yield")
#: Baseline models never drawn as the forecast row unless asked for by name.
BASELINE_MODELS = {"null", "trend", "trend_all", "median", "analog", "last_year"}


def pick_model(db, table, models_in_db):
    """The model to draw when ``[snake] model`` is unset and the DB holds
    several: the first ML model of the run's own ``models`` list (its config
    table), else the first non-baseline model in the DB. None when there is
    no ML model."""
    ml = [m for m in models_in_db if m not in BASELINE_MODELS]
    if not ml:
        return None
    country = table.rsplit("_", 1)[0]
    order = sd.literal(sd.run_config(db, country).get("models"), []) or []
    for m in order if isinstance(order, (list, tuple)) else []:
        if m in ml:
            return m
    return ml[0]


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------
def _parser(path_config_files):
    parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),
                                       inline_comment_prefixes=(";",))
    parser.read([str(p) for p in path_config_files])
    return parser


def read_config(path_config_files):
    """Settings for a run: paths from ``[PATHS]`` / ``[DEFAULT]``, the
    ``[snake]`` keys written literally (a probe parser with a default section
    no file uses keeps ``[DEFAULT]`` values such as ``crops`` out), the NASS
    key, the crop-condition CSV and the yield display map."""
    parser = _parser(path_config_files)
    probe = configparser.ConfigParser(default_section="__snake_no_default__",
                                      interpolation=None, inline_comment_prefixes=(";",))
    probe.read([str(p) for p in path_config_files])
    own = {sec: set(probe.options(sec)) for sec in probe.sections()}

    def _lit(section, option, default=None):
        if option not in own.get(section, ()):
            return default
        raw = parser.get(section, option).strip()
        if raw == "":
            return default
        try:
            return ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            return raw

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    root = dir_output / project
    meta_dir = (Path(parser.get("PATHS", "dir_metadata"))
                if parser.has_option("PATHS", "dir_metadata") else root.parent / "inputs" / "metadata")
    cfg = dict(DEFAULTS)
    for key in DEFAULTS:
        cfg[key] = _lit("snake", key, DEFAULTS[key])
    cfg.update({
        "dir_output": dir_output, "project": project, "root": root, "dir_metadata": meta_dir,
        "nass_key": _lit("NASS", "api_key"),
        "cci_file": parser.get("DEFAULT", "cci_file", fallback="").strip() or None,
        "yield_units": parser.get("ML", "yield_units", fallback="Mg/ha"),
        "yield_display": _lit("ML", "yield_display", {}) or {},
    })
    # [snake] cids is the option; rows is kept as an alias (cids wins)
    if cfg.get("cids"):
        cfg["rows"] = cfg["cids"]
    if isinstance(cfg["rows"], str):
        cfg["rows"] = [cfg["rows"]]
    if isinstance(cfg["invert"], (list, tuple)):
        cfg["invert"] = {c: True for c in cfg["invert"]}
    cfg["invert"] = {str(k).upper(): bool(v) for k, v in (cfg["invert"] or {}).items()}
    cfg["labels"] = {str(k).upper(): str(v) for k, v in (cfg["labels"] or {}).items()}
    if isinstance(cfg["regions"], str):
        cfg["regions"] = [cfg["regions"]]
    if isinstance(cfg["formats"], str):
        cfg["formats"] = [cfg["formats"]]
    return cfg


def display_for(cfg, crop):
    """``(unit, factor)`` for the raw yield column: ``[ML] yield_display``
    (for example ``{"maize": ["bu/ac", 15.9318]}``) else ``[ML] yield_units``
    and 1. The DB stays in tn/ha; the factor applies to ``value_raw`` only."""
    disp = cfg.get("yield_display") or {}
    if isinstance(disp, dict) and crop in disp:
        return str(disp[crop][0]), float(disp[crop][1])
    return str(cfg.get("yield_units") or "Mg/ha"), 1.0


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------
def _distinct(db, table, column):
    con = sqlite3.connect(f"file:{Path(db)}?mode=ro", uri=True)
    try:
        cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()
        if column not in cols:
            return []
        vals = pd.read_sql(f'SELECT DISTINCT "{column}" AS v FROM "{table}" '
                           f"WHERE \"Experiment Name\" = 'outlook'", con)["v"]
    finally:
        con.close()
    return sorted(v for v in vals.dropna().unique())


def resolve_db(root, db):
    db = Path(db)
    return db if db.is_absolute() else Path(root) / "ml" / "db" / db


def run_dir_for(root, db):
    from geocif.experiments.s2s_africa import run_stamp
    from geocif.viz.shift_map import outlook_run_dir

    return outlook_run_dir(root, db) or Path(root) / "ml" / "analysis" / run_stamp()


def slug(text):
    return str(text).strip().lower().replace(" ", "_").replace("/", "_")


# ---------------------------------------------------------------------------
# building and drawing
# ---------------------------------------------------------------------------
def indicator_metas(keys, invert=None, labels=None):
    """The CID-backed rows among ``keys``: registry keys (``rain``) or any CID
    name from ``cid/definitions.py`` (``PRCPTOT``, ``R10mm``); ``invert`` and
    ``labels`` map a CID (upper case) to a sign or a row label. USDA rows are
    built separately."""
    invert, labels = invert or {}, labels or {}
    metas, unknown = [], []
    for k in keys:
        try:
            base = sd.lookup_indicator(k)
            cid = (base.cid or str(k)).upper()
            metas.append(sd.lookup_indicator(k, label=labels.get(cid) or labels.get(str(k).upper()),
                                             invert=invert.get(cid, invert.get(str(k).upper()))))
        except KeyError:
            unknown.append(k)
    if unknown:
        raise ValueError(f"unknown snake cids {unknown}: use a CID from cid/definitions.py "
                         f"or a key of INDICATOR_META ({sorted(sd.INDICATOR_META)})")
    return [m for m in metas if m.source == "cid"]


def usda_keys(keys):
    out = []
    for k in keys:
        try:
            m = sd.lookup_indicator(k)
        except KeyError:
            continue
        if m.source != "cid":
            out.append(m.key)
    return out


def build(cfg, *, db, table, model, year=None, season=None, region=None, nass_session=None,
          cache_dir=None):
    """Tracks and metadata for one figure. Returns ``(tracks, meta, context)``
    where ``context`` carries the resolved year, season and display unit."""
    prep = prepare(cfg, db=db, table=table, model=model, year=year, season=season,
                   nass_session=nass_session, cache_dir=cache_dir)
    return build_region(prep, region)


def prepare(cfg, *, db, table, model, year=None, season=None, nass_session=None,
            cache_dir=None):
    """Everything one table's figures share, read once: forecasts, the run's
    config and selected features, the CID tables, observation dates per
    region and the USDA frames. :func:`build_region` makes each figure."""
    from geocif.viz import nass as _nass

    country, crop = table.rsplit("_", 1)
    fc = sd.load_forecasts(db, table, model=model, season=season,
                           min_region_frac=cfg["min_region_frac"])
    year = int(year) if year is not None else int(fc["year"].max())
    if not (fc["year"] == year).any():
        raise ValueError(f"{table}: no rows for harvest year {year}")
    rcfg = sd.run_config(db, country)
    method = str(rcfg.get("method", "monthly_r")).strip().lower()
    if method != "monthly_r":
        raise ValueError(f"{table}: the snake chart needs method = monthly_r, the run used {method!r} "
                         f"(sub-monthly stages collapse onto one issue month)")
    admin_zone = str(rcfg.get("admin_zone", "admin_1")).strip()
    sel = sd.selected_by_stage(db, table, model)
    candidates = sd.candidate_families(rcfg)
    tys = rcfg.get("training_year_start")
    tys = int(tys) if tys not in (None, "", "None") else None
    metas = indicator_metas(cfg["rows"], cfg.get("invert"), cfg.get("labels"))
    years = sorted(set(fc["year"].astype(int)))
    # Indicator normal: the last N years before the target when asked for,
    # else [snake] baseline_years, else every other year of the pool.
    baseline_years = (sd.last_years(year, cfg["baseline_last"]) if cfg.get("baseline_last")
                      else cfg["baseline_years"])
    season_token = int(season) if season is not None else (
        int(fc["Season"].dropna().iloc[0]) if fc["Season"].notna().any() else 1)
    cid = (sd.load_cid_years(cfg["root"], method, admin_zone, country, crop, season_token, years,
                             indices=[m.cid for m in metas])
           if metas else pd.DataFrame(columns=["Region", "year", "Stage", "Index", "CID"]))
    obs_by_region = {}
    if cfg["obs_dates"] == "observed" and metas:
        daily = Path(cfg["root"]) / "crop_t0" / country / f"{country}_{crop}_s{season_token}.csv"
        variables = sorted({m.variable for m in metas if m.variable})
        obs_by_region = sd.observed_dates_by_region(daily, variables, year) if daily.exists() else {}
        if not obs_by_region:
            logger.info(f"{table}: no merged daily inputs at {daily}; nominal observation dates")
    usda = [k for k in usda_keys(cfg["rows"]) if k in USDA_ROWS]
    weekly = nass_frame = None
    cache_dir = Path(cache_dir) if cache_dir else None
    if "cci" in usda or "cci_ge" in usda:
        weekly = _nass.load_nass_crop_condition(
            crop, None, years, csv_path=cfg.get("cci_file"), api_key=cfg.get("nass_key"),
            cache=(cache_dir / "nass_condition_cache.csv") if cache_dir else None,
            offline=bool(cfg.get("nass_offline")), session=nass_session)
    if "usda_yield" in usda:
        nass_frame = _nass.fetch(_nass.nass_api_key(cfg.get("nass_key")), [year], crops=(crop,),
                                 cache=(cache_dir / "nass_quickstats_cache.csv") if cache_dir else None,
                                 offline=bool(cfg.get("nass_offline")), session=nass_session)
    units = sorted(fc.loc[fc["year"] == year, "Region"].unique())
    return {"cfg": cfg, "fc": fc, "rcfg": rcfg, "sel": sel, "candidates": candidates, "tys": tys,
            "metas": metas, "baseline_years": baseline_years, "cid": cid,
            "obs_by_region": obs_by_region, "usda": usda, "weekly": weekly,
            "nass_frame": nass_frame, "display": display_for(cfg, crop), "year": year,
            "season": season_token, "country": country, "crop": crop, "model": model,
            "table": table, "units": units, "admin_zone": admin_zone}


def build_region(prep, region=None):
    """Tracks for one figure: one modeled unit (``region`` as named in the
    outlook table) or the national aggregate (``None``)."""
    cfg, fc, year = prep["cfg"], prep["fc"], prep["year"]
    country, crop, display = prep["country"], prep["crop"], prep["display"]
    obs = prep["obs_by_region"]
    obs_dates = (obs.get(sd.region_key(region)) or None) if region is not None else (obs.get("*") or None)
    extra = []
    for metric in ("cci", "cci_ge"):
        if metric in prep["usda"] and prep["weekly"] is not None:
            extra.append(sd.build_cci_track(
                prep["weekly"], fc, country=country, target_year=year, metric=metric,
                baseline_years=prep["baseline_years"], training_year_start=prep["tys"],
                selected=prep["sel"], candidates=prep["candidates"], region=region,
                cci_scale=cfg["cci_scale"]))
    if "usda_yield" in prep["usda"] and prep["nass_frame"] is not None:
        if region is not None:
            logger.info("USDA yield forecast row is national only; skipped for a region")
        else:
            _, base = sd.build_yield_track(
                fc, country=country, crop=crop, target_year=year,
                model_type=str(prep["rcfg"].get("detrend_method") or "gaussian").strip().lower(),
                training_year_start=prep["tys"], display=display)
            extra.append(sd.build_usda_yield_track(prep["nass_frame"], fc, base, country=country,
                                                   crop=crop, target_year=year, display=display))
    tracks, meta = sd.build_tracks(
        fc, prep["cid"], prep["metas"], country=country, crop=crop, target_year=year,
        cfg=prep["rcfg"], window=cfg["window"], baseline_years=prep["baseline_years"],
        display=display, selected=prep["sel"], obs_dates=obs_dates, region=region,
        extra_tracks=extra)
    meta["sources"] = [f"GEOCIF {prep['model']}"] + meta["sources"][1:]
    context = {"year": year, "season": prep["season"], "display": display,
               "model": prep["model"], "country": country, "crop": crop, "region": region,
               "admin_zone": prep["admin_zone"]}
    return tracks, meta, context


def render(tracks, meta, context, cfg, *, dir_plots, dir_csvs, title=None, subtitle=None):
    """Draw one figure, write PNG/PDF + the companion CSV, return the lookup row."""
    import matplotlib.pyplot as plt

    region = context["region"] or "national"
    stem = (f"snake_{context['country']}_{context['crop']}_{context['model']}_"
            f"{slug(region)}_s{context['season']}_{context['year']}")
    headline = title if title is not None else cfg.get("title")
    if headline is not None and str(headline).strip().lower() in ("", "none"):
        headline = None
    if headline:
        place = context["region"] or str(context["country"]).replace("_", " ").title()
        headline = str(headline).format(region=place, country=context["country"],
                                        crop=context["crop"], year=context["year"])
    subtitle = subtitle or cfg.get("subtitle") or None
    source = snake.source_line(meta)
    fig, ax = snake.plot_snake(tracks, layout=cfg["layout"], split=cfg["split"],
                               deadband=float(cfg["deadband"]), max_lanes=int(cfg["max_lanes"]),
                               title=headline, subtitle=subtitle,
                               source=source if cfg.get("show_source") else None,
                               show_roles=bool(cfg.get("show_roles")),
                               palette=cfg.get("palette") or snake.DEFAULT_PALETTE)
    written = snake.save_snake(fig, Path(dir_plots) / stem, formats=tuple(cfg["formats"]))
    plt.close(fig)
    csv = Path(dir_csvs) / f"{stem}.csv"
    out = tracks.copy()
    # The footer text (sources, baseline, caveats) always travels with the data.
    out["title"] = headline or ""
    out["source_line"] = source
    out.to_csv(csv, index=False)
    desc = (f"{context['country']} {context['crop']} {context['year']} {region}: GEOCIF "
            f"{context['model']} forecast and indicator rows per issue month, standardized anomalies")
    return written + [csv], (f"{stem}.{cfg['formats'][0]}", csv.name, desc)  # lookup row kept for callers


def run(path_config_files, *, db, table, model=None, year=None, season=None, regions=None,
        out=None, nass_session=None, **overrides):
    """Snake charts for one outlook table: one figure per modeled unit (the
    admin_1 or admin_2 regions the run forecast; ``[snake] regions = ['all']``,
    the default), per named region or for the national aggregate, and per
    season present. Returns the files written."""
    cfg = read_config(path_config_files)
    cfg.update({k: v for k, v in overrides.items() if v is not None})
    root = cfg["root"]
    db = resolve_db(root, db)
    if not db.exists():
        raise FileNotFoundError(db)
    model = model or cfg.get("model")
    models = _distinct(db, table, "Model")
    if model is None:
        model = models[0] if len(models) == 1 else pick_model(db, table, models)
        if model is None:
            raise ValueError(f"{table} holds only baseline models {models}; set [snake] model")
        if len(models) > 1:
            logger.info(f"snake {table}: drawing {model} (from {models}); set [snake] model to choose")
    seasons = [season] if season is not None else (_distinct(db, table, "Season") or [None])
    out_base = Path(out) if out else run_dir_for(root, db) / "snake"
    dir_plots, dir_csvs = out_base / "plots", out_base / "csvs"
    for d in (dir_plots, dir_csvs):
        d.mkdir(parents=True, exist_ok=True)
    written, lookup = [], []
    for s in seasons:
        s = int(s) if s is not None and not pd.isna(s) else None
        try:
            prep = prepare(cfg, db=db, table=table, model=model, year=year, season=s,
                           nass_session=nass_session, cache_dir=dir_csvs)
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"snake {table} season {s} skipped: {type(exc).__name__}: {exc}")
            continue
        targets = []
        for region in (regions or cfg["regions"]):
            name = str(region).lower() if region is not None else "national"
            if name == "national":
                targets.append(None)
            elif name == "all":
                targets.extend(prep["units"])      # every unit the model ran at
            else:
                targets.append(region)
        for target in dict.fromkeys(targets):
            try:
                tracks, meta, context = build_region(prep, target)
                files, row = render(tracks, meta, context, cfg, dir_plots=dir_plots,
                                    dir_csvs=dir_csvs, title=overrides.get("title"))
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"snake {table} season {s} region {target or 'national'} "
                               f"skipped: {type(exc).__name__}: {exc}")
                continue
            written += files
            lookup.append(row)
    logger.info(f"snake: wrote {len(written)} file(s) under {out_base}")
    return written


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--config", nargs="+", required=True,
                   help="geobase, countries, crops, geocif config files")
    p.add_argument("--db", required=True, help="outlook_*.db; a bare name is looked up in ml/db")
    p.add_argument("--table", action="append", required=True,
                   help="{country}_{crop} table (repeatable)")
    p.add_argument("--model")
    p.add_argument("--year", type=int)
    p.add_argument("--season", type=int)
    p.add_argument("--region", action="append",
                   help="all (default: every modeled unit), national, or a region name")
    p.add_argument("--cids", "--rows", nargs="+", dest="rows",
                   help="indicator rows: CID names (PRCPTOT, MEAN_ESI4WK, ...) or registry keys")
    p.add_argument("--window", choices=sd.WINDOWS)
    p.add_argument("--baseline-last", type=int, dest="baseline_last",
                   help="indicator normal from the N years before the target year")
    p.add_argument("--layout", choices=snake.LAYOUTS)
    p.add_argument("--title")
    p.add_argument("--out")
    ns = p.parse_args(argv)
    written = []
    for table in ns.table:
        written += run(ns.config, db=ns.db, table=table, model=ns.model, year=ns.year,
                       season=ns.season, regions=ns.region, out=ns.out, rows=ns.rows,
                       window=ns.window, layout=ns.layout, title=ns.title,
                       baseline_last=ns.baseline_last)
    for w in written:
        print(w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
