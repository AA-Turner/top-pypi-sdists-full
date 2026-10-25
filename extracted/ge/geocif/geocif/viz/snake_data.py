# -*- coding: utf-8 -*-
"""Data tracks for the snake chart: forecasts, indicators and LOYO baselines.

Builds the tidy long table that :func:`geocif.viz.snake.plot_snake` draws,
for one (country, crop, season, harvest year) and one model, from

* the outlook DB (``viz/_outlook_db.load_outlook``): the predicted yield per
  region and stage, the observed yields of the hindcast years, the area
  weights, the ``Selected Features`` lists and the run's ``config_*`` table;
* the per-year CID tables that ``indices_runner`` writes
  (``cid/indices/{method}/{admin_zone}/{country}/{crop}/{country}_{crop}_s{season}_{year}.csv``),
  keyed on the same ``Stage_ID`` chain as the DB rows, for the indicator
  values of every year;
* optionally the merged daily inputs (``crop_t0/{country}/{country}_{crop}_s{season}.csv``)
  for the real last observation date of each indicator, so the causality
  guard (``obs_date <= issue_date``) can actually fail.

Leakage rules, enforced here and nowhere else:

* every baseline drops the target harvest year before fitting (leave one
  year out); the yield trend reuses GEOCIF's own detrending
  (``ml/trend.detrend_dataframe`` + ``gaussian_expected_for_year``) on the
  observed series with the target year removed, sorted by year, on a copy;
* ``[<country>] training_year_start`` floors the baseline years so that
  "normal" is what the model trained on;
* the live year's ``Area (ha)`` is NULL in the DB, so weights are filled
  causally: the mean of the last three known years of that region.

Stage conventions (``method = monthly_r`` only): ``Stage Name`` is
reverse-cumulative (``"Aug 1-Apr 30"`` = data Apr 1 to Aug 31), the as-of
month is its first token (``leadtime._asof_month``), the issue date is the
first day of the following month and the nominal observation date the last
day of the as-of month. ``Stage_ID`` is the month chain ``"8_7_6_5_4"``.
"""
import ast
import calendar
import logging
import sqlite3
from dataclasses import dataclass, replace
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.viz._outlook_db import OBS, PRED, drop_sparse_stages, load_outlook
from geocif.viz.leadtime import _asof_month, _season_order

logger = logging.getLogger(__name__)

AREA = "Area (ha)"
MAX_INDICATORS = 4
#: Sources of the CID value for a row; the CID tables carry both windows.
WINDOWS = ("stage", "month")


# ---------------------------------------------------------------------------
# indicator registry
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class IndicatorMeta:
    """What one indicator row is made of.

    ``cid`` is the ``Index`` name in the CID tables (``MEAN_NDVI``,
    ``PRCPTOT``); ``family`` is the part of a feature name that identifies
    the same quantity under another aggregator (``NDVI`` for ``MEAN_NDVI``
    and ``AUC_NDVI``) and decides the role; ``variable`` is the merged daily
    input column that carries the observation dates; ``invert`` flips the
    sign so that right always means more favorable for yield; ``role`` is the
    default role, resolved per run by :func:`resolve_role`.
    """
    key: str
    label: str
    unit: str
    invert: bool
    role: str
    source: str          # "cid" | "nass_cci" | "nass_yield"
    cid: str = ""
    family: str = ""
    variable: str = ""
    description: str = ""

    def with_label(self, label):
        return replace(self, label=label)


def _m(key, label, unit, invert, cid, variable, description, role="input", source="cid"):
    fam = cid.split("_", 1)[1] if "_" in cid and cid.split("_", 1)[0] in (
        "MEAN", "MAX", "MIN", "STD", "AUC", "SUM") else cid
    return IndicatorMeta(key, label, unit, invert, role, source, cid, fam, variable, description)


#: Default rows. Threshold counts and totals only: ICCLIM percentile indices
#: (TX90p, R95p, WSDI, ...) use a base period that includes hindcast target
#: years, so they are not offered.
INDICATOR_META = {m.key: m for m in [
    _m("ndvi", "NDVI", "", False, "MEAN_NDVI", "ndvi", "Mean NDVI over the window"),
    _m("ndvi_max", "NDVI (peak)", "", False, "MAX_NDVI", "ndvi", "Max NDVI over the window"),
    _m("ndvi_auc", "NDVI (area under curve)", "", False, "AUC_NDVI", "ndvi",
       "Area under the NDVI curve over the window: greenness accumulated"),
    _m("gcvi", "GCVI", "", False, "MEAN_GCVI", "gcvi", "Mean green chlorophyll vegetation index"),
    _m("fpar", "FPAR", "", False, "MEAN_FPAR", "fpar_mo6", "Mean fraction of absorbed PAR"),
    _m("esi", "Evaporative stress (ESI)", "", False, "MEAN_ESI4WK", "esi_4wk",
       "Mean 4-week evaporative stress index; higher is wetter"),
    _m("esi_auc", "Evaporative stress (ESI, cumulative)", "", False, "AUC_ESI4WK", "esi_4wk",
       "Area under the 4-week ESI curve"),
    _m("rain", "Rainfall (CHIRPS)", "mm", False, "PRCPTOT", "chirps", "Total precipitation on wet days"),
    _m("rain_max5d", "Heaviest 5-day rain", "mm", True, "RX5day", "chirps", "Max 5-day precipitation"),
    _m("dry_spell", "Longest dry spell", "days", True, "CDD", "chirps", "Max consecutive dry days"),
    _m("dry_days", "Dry days (< 1 mm)", "days", True, "DD", "chirps",
       "Number of days with less than 1 mm of rain"),
    _m("heat", "Heat days (Tmax > 25 C)", "days", True, "SU", "chirts_era5_tmax", "Summer days"),
    _m("heat_run", "Longest heat run", "days", True, "CSU", "chirts_era5_tmax",
       "Max consecutive summer days"),
    _m("kdd", "Killing degree days", "degree-days", True, "KDD", "chirts_era5_tmax",
       "Sum of Tmax - 32 C over hot days"),
    _m("tmax", "Mean daily maximum", "C", True, "TX", "chirts_era5_tmax", "Mean Tmax"),
    _m("etref", "Reference ET", "mm/day", True, "MEAN_ETREF", "etref", "Mean reference evapotranspiration"),
    _m("cci", "Crop condition (USDA)", "index", False, "MEAN_CCI", "",
       "USDA NASS crop condition index, 0-100", role="independent", source="nass_cci"),
    _m("cci_ge", "Good + excellent share (USDA)", "%", False, "MEAN_CCIGE", "",
       "USDA NASS good plus excellent share", role="independent", source="nass_cci"),
    IndicatorMeta("usda_yield", "USDA yield forecast", "bu/ac", False, "independent",
                  "nass_yield", "", "USDA_YIELD", "", "NASS monthly state yield forecast"),
]}


#: CID categories (cid/definitions.py) where a higher value hurts the crop:
#: their rows are inverted so that right still means more favorable.
INVERT_CATEGORIES = {"Heat", "Drought", "ETREF"}
#: Merged daily input column behind each CID category, for observation dates.
CATEGORY_VARIABLE = {"Rain": "chirps", "Drought": "chirps", "Compound": "chirps",
                     "h-Index": "chirps", "Heat": "chirts_era5_tmax",
                     "Temperature": "chirts_era5_tmax", "Cold": "chirts_era5_tmin",
                     "ESI": "esi_4wk", "FPAR": "fpar_mo6", "FPAR5K": "fpar_mo6_5km",
                     "ETREF": "etref"}
#: ICCLIM indices whose percentile base period spans every year, the target
#: year included: usable, but the raw value already depends on that year.
PERCENTILE_CIDS = {"TG90p", "TN90p", "TX90p", "TG10p", "TN10p", "WSDI", "CSDI",
                   "R75p", "R75pTOT", "R95p", "R95pTOT", "R99p", "R99pTOT"}


def cid_catalogue():
    """``{CID: (category, description)}`` for every staged CID that
    ``cid/definitions.py`` defines (climate indices and EO aggregates)."""
    from geocif.cid import definitions as d

    out = {}
    for name in ("dict_indices", "dict_ndvi", "dict_etref", "dict_gcvi", "dict_fpar",
                 "dict_fpar5k", "dict_esi4wk", "dict_hindex", "dict_cci", "dict_ccige"):
        for cid, spec in getattr(d, name, {}).items():
            out[cid] = (spec[0], spec[1])
    return out


def make_indicator(cid, *, label=None, invert=None):
    """An indicator row for any CID in ``cid/definitions.py`` that the
    registry does not describe: label = the CID name, sign from its category
    (``INVERT_CATEGORIES``), observation dates from the category's daily
    variable (``CATEGORY_VARIABLE``; VI from the index's own band)."""
    cat = cid_catalogue()
    match = next((c for c in cat if c.upper() == str(cid).upper()), None)
    if match is None:
        raise KeyError(cid)
    category, description = cat[match]
    if category == "VI":
        variable = "gcvi" if "GCVI" in match.upper() else "ndvi"
    else:
        variable = CATEGORY_VARIABLE.get(category, "")
    if match in PERCENTILE_CIDS:
        logger.warning(f"{match}: percentile index whose base period includes the target "
                       f"year; its raw value is not leave-one-year-out")
    inv = (category in INVERT_CATEGORIES) if invert is None else bool(invert)
    return IndicatorMeta(match.lower(), label or match, "", inv, "input", "cid", match,
                         feature_family(match), variable, description)


def lookup_indicator(key, *, label=None, invert=None):
    """Registry entry by key (``"rain"``) or CID name (``"PRCPTOT"``,
    case-insensitive), else a row built from ``cid/definitions.py`` for any
    other CID (:func:`make_indicator`). ``label`` / ``invert`` override the
    defaults. Raises ``KeyError`` when the name is unknown everywhere."""
    if key in INDICATOR_META:
        m = INDICATOR_META[key]
    else:
        by_cid = {m.cid.upper(): m for m in INDICATOR_META.values() if m.cid}
        m = by_cid.get(str(key).upper())
        if m is None:
            return make_indicator(key, label=label, invert=invert)
    if label is not None:
        m = replace(m, label=label)
    if invert is not None:
        m = replace(m, invert=bool(invert))
    return m


def last_years(target_year, n):
    """The ``n`` harvest years before ``target_year``: the baseline of
    ``[snake] baseline_last``."""
    return list(range(int(target_year) - int(n), int(target_year)))


def feature_family(name):
    """``"NDVI"`` for ``"MEAN_NDVI Aug 1-Apr 30"``; ``"PRCPTOT"`` for
    ``"PRCPTOT May 1-May 31"``; ``"CCI"`` for ``"DELTA_MEAN_CCI Sep"``."""
    cid = str(name).split(" ", 1)[0]
    parts = cid.split("_")
    while parts and parts[0] in ("DELTA", "MEAN", "MAX", "MIN", "STD", "AUC", "SUM"):
        parts = parts[1:]
    return "_".join(parts) if parts else cid


# ---------------------------------------------------------------------------
# the run's own configuration, from the DB
# ---------------------------------------------------------------------------
def run_config(db_path, country=None):
    """Options of the run that wrote ``db_path``, from its ``config_*`` table.

    Returns ``{option: value}`` (strings as written), each option taken from
    the most specific section among ``[<country>]``, ``[ML]`` and ``[DEFAULT]``
    (other sections, e.g. another country's, are ignored). Empty when the
    table is missing.
    """
    con = sqlite3.connect(f"file:{Path(db_path)}?mode=ro", uri=True)
    try:
        names = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' "
                            "AND name LIKE 'config_%' ORDER BY name", con)["name"].tolist()
        if not names:
            return {}
        cfg = pd.read_sql(f'SELECT "Section", "Option", "Value" FROM "{names[-1]}"', con)
    finally:
        con.close()
    cfg["Option"] = cfg["Option"].astype(str).str.lower()
    rank = {}
    for i, sec in enumerate([s for s in (country, "ML", "DEFAULT") if s]):
        rank[sec] = i
    # Only the country's own section, [ML] and [DEFAULT]: the table holds every
    # section of the bundle, and a key written for another country (Kenya's
    # training_year_start) must not reach this one.
    cfg = cfg[cfg["Section"].isin(list(rank))].copy()
    cfg["_rank"] = cfg["Section"].map(rank)
    cfg = cfg.sort_values(["Option", "_rank"], kind="stable").drop_duplicates("Option")
    return dict(zip(cfg["Option"], cfg["Value"].astype(str)))


def literal(value, default=None):
    """``ast.literal_eval`` of a config string, the raw string if that fails."""
    if value is None:
        return default
    s = str(value).strip()
    if not s:
        return default
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return s


# ---------------------------------------------------------------------------
# stages and dates
# ---------------------------------------------------------------------------
def stage_id_from_name(stage, swd):
    """``"8_7_6_5_4"`` for ``"Aug 1-Apr 30"``: the reverse-cumulative month
    chain from the as-of month back to the planting month."""
    from geocif.viz.leadtime import _MONTH_NUM

    asof = _asof_month(stage, swd)
    if asof is None or not isinstance(stage, str) or "-" not in stage:
        return None
    plant_tok = stage.split("-", 1)[1].strip()[:3].title()
    plant = _MONTH_NUM.get(plant_tok)
    if plant is None:
        return None
    months = []
    m = asof
    while True:
        months.append(m)
        if m == plant:
            break
        m = 12 if m == 1 else m - 1
        if len(months) > 12:
            return None
    return "_".join(str(x) for x in months)


def month_end(year, month):
    return date(int(year), int(month), calendar.monthrange(int(year), int(month))[1])


def stage_calendar_year(asof, order, harvest_year):
    """Calendar year of the as-of month: the harvest year, or the year before
    for months of a season that started the previous calendar year (the
    ``_season_order`` positions above 12 are the harvest-year months)."""
    if max(order.values()) <= 12:
        return int(harvest_year)
    return int(harvest_year) if order[asof] > 12 else int(harvest_year) - 1


def stage_dates(asof, order, harvest_year):
    """``(obs_date, issue_date)``: last day of the as-of month and the first
    day of the next month."""
    y = stage_calendar_year(asof, order, harvest_year)
    obs = month_end(y, asof)
    return obs, obs + timedelta(days=1)


# ---------------------------------------------------------------------------
# forecasts
# ---------------------------------------------------------------------------
def load_forecasts(db_path, table, *, model, season=None, min_region_frac=1.0):
    """Outlook rows of one model with stage, as-of month, dates and weights.

    Columns: ``Region, year, stage, swd, stage_id, asof, order, obs_date,
    issue_date, Season, Country, Area (ha), run_date`` plus ``OBS`` / ``PRED``.
    Pre-season stages (no as-of month) are dropped with a note; stages that
    cover fewer than ``min_region_frac`` of the regions are dropped as in the
    cone. The live year's missing area is filled causally.
    """
    df = load_outlook(db_path, table, model=model,
                      extra_columns=(AREA, "Season"),
                      text_columns=("Country", "Stage_ID"),
                      key_extra=("Season",))
    if df.empty:
        raise ValueError(f"{table}: no outlook rows for model {model!r}")
    if season is not None and df["Season"].notna().any():
        df = df[df["Season"] == season]
        if df.empty:
            raise ValueError(f"{table}: no rows for Season {season}")
    seasons = sorted(df["Season"].dropna().unique())
    if len(seasons) > 1:
        raise ValueError(f"{table} holds seasons {seasons}; pass season=")
    df, dropped = drop_sparse_stages(df, min_region_frac)
    if dropped:
        logger.info(f"{table}: dropped sparse stages {dropped}")
    df["asof"] = [_asof_month(s, w) for s, w in zip(df["stage"], df["swd"])]
    n_pre = int(df["asof"].isna().sum())
    if n_pre:
        logger.info(f"{table}: {n_pre} row(s) without an as-of month "
                    f"(pre-season stages) left out of the snake")
        df = df.dropna(subset=["asof"])
    if df.empty:
        raise ValueError(f"{table}: no month-window stages (run_time_steps=all needed)")
    df["asof"] = df["asof"].astype(int)
    order = _season_order(df["asof"])
    df["order"] = df["asof"].map(order)
    sid = df["Stage_ID"] if "Stage_ID" in df.columns else pd.Series(np.nan, index=df.index)
    df["stage_id"] = [s if isinstance(s, str) and s.strip() else stage_id_from_name(st, w)
                      for s, st, w in zip(sid, df["stage"], df["swd"])]
    dates = [stage_dates(a, order, y) for a, y in zip(df["asof"], df["year"])]
    df["obs_date"] = [d[0] for d in dates]
    df["issue_date"] = [d[1] for d in dates]
    df["run_date"] = pd.to_datetime(df["Date"], format="%B_%d_%Y", errors="coerce").dt.date \
        if "Date" in df.columns else pd.NaT
    df["year"] = df["year"].astype(int)
    df = causal_area(df)
    return df.reset_index(drop=True)


def causal_area(df, col=AREA, n=3):
    """Fill a region's missing ``Area (ha)`` for year Y with the mean of its
    last ``n`` known areas before Y (the ``stress_switch._trailing_area``
    rule); with none before Y, the mean of its earliest ``n`` known areas.
    Adds ``area_filled`` (bool)."""
    df = df.copy()
    df["area_filled"] = False
    known = (df.dropna(subset=[col])[["Region", "year", col]]
             .drop_duplicates(["Region", "year"]).sort_values("year"))
    by_region = {r: g for r, g in known.groupby("Region")}
    fill = {}
    for (region, year), g in df[df[col].isna()].groupby(["Region", "year"]):
        k = by_region.get(region)
        if k is None or k.empty:
            continue
        before = k[k["year"] < year].tail(n)
        src = before if not before.empty else k.head(n)
        fill[(region, year)] = float(src[col].mean())
    if fill:
        idx = df[col].isna()
        keys = list(zip(df.loc[idx, "Region"], df.loc[idx, "year"]))
        vals = [fill.get(k, np.nan) for k in keys]
        df.loc[idx, col] = vals
        df.loc[idx, "area_filled"] = [k in fill for k in keys]
    return df


# ---------------------------------------------------------------------------
# weighting regions to the national series
# ---------------------------------------------------------------------------
def to_national(df, country, value_col=PRED, obs_col=OBS, by=("year", "stage")):
    """Area-weighted national value per group through
    ``viz.aggregation.aggregate_predictions`` (the outlook products' rule:
    one child set, children without a usable weight dropped, unweighted
    only when none has one). Returns ``[*by, value, obs, n_units, aggregation]``.
    """
    from geocif.viz.aggregation import aggregate_predictions, build_level_map

    rows = []
    level_map = build_level_map(df["Region"].unique(), "national", country)
    for keys, g in df.groupby(list(by), sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        work = pd.DataFrame({
            "Region": g["Region"].values, "Harvest Year": g["year"].values,
            OBS: g[obs_col].values if obs_col in g.columns else np.nan,
            PRED: g[value_col].values, AREA: g[AREA].values if AREA in g.columns else np.nan,
        })
        agg = aggregate_predictions(work, level_map, weight_col=AREA)
        if agg.empty:
            continue
        a = agg.iloc[0]
        rows.append({**dict(zip(by, keys)), "value": a[PRED], "obs": a[OBS],
                     "n_units": int(a["N Units"]), "aggregation": a["Aggregation"]})
    return pd.DataFrame(rows, columns=[*by, "value", "obs", "n_units", "aggregation"])


# ---------------------------------------------------------------------------
# baselines
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Baseline:
    """A leave-one-year-out trend and spread for one target year.

    ``space`` is ``"percent"`` for the gaussian detrend (GEOCIF's default:
    anomalies are ``100 * (Y - E) / E``) and ``"absolute"`` for the OLS
    trends, so :meth:`z` divides like with like.
    """
    target_year: int
    trend: float
    sd: float
    space: str
    model_type: str
    years: tuple

    @property
    def n(self):
        return len(self.years)

    def anomaly(self, value):
        if self.space == "percent":
            return 100.0 * (value - self.trend) / self.trend
        return value - self.trend

    def z(self, value):
        return self.anomaly(value) / self.sd


def loyo_baseline(years, values, target_year, *, model_type="gaussian",
                  training_year_start=None, min_years=5):
    """Fit GEOCIF's detrend on the observed series without the target year.

    ``years`` / ``values`` are the observed yields per year (any order, NaNs
    allowed). The target year is dropped, years before
    ``training_year_start`` are dropped, the rest is sorted and copied before
    ``ml.trend.detrend_dataframe`` sees it (it mutates its input and the
    gaussian filter runs in row order). The trend at the target year comes
    from ``gaussian_expected_for_year`` (interpolating the local smooth,
    which is how GEOCIF retrends a held-out year) or from the fitted OLS
    model; the spread is the sd (ddof 1) of the detrended training series.
    """
    from statsmodels.tools.tools import add_constant

    from geocif.ml import trend as _trend

    s = pd.DataFrame({"Harvest Year": pd.to_numeric(pd.Series(years), errors="coerce"),
                      "y": pd.to_numeric(pd.Series(values), errors="coerce")}).dropna()
    s = s[s["Harvest Year"].astype(int) != int(target_year)]
    if training_year_start is not None:
        s = s[s["Harvest Year"] >= int(training_year_start)]
    s = s.sort_values("Harvest Year").reset_index(drop=True)
    if len(s) < min_years:
        raise ValueError(f"only {len(s)} training year(s) for {target_year}; need {min_years}")
    s["Harvest Year"] = s["Harvest Year"].astype(int)
    fit_df = s.copy()
    dd = _trend.detrend_dataframe(fit_df, "y", model_type=model_type)
    kind = dd.model_type if isinstance(dd.model_type, str) else model_type
    if kind == "gaussian":
        at_target = _trend.gaussian_expected_for_year(dd.trend_model, target_year)
        detrended = pd.Series(dd.detrended_series.values, index=s["Harvest Year"].values)
        space = "percent"
    elif kind in ("mean", "linear", "quadratic"):
        t = np.array([float(target_year)])
        if kind == "mean":
            x = np.ones(1)
        elif kind == "linear":
            x = add_constant(t, has_constant="add")
        else:
            x = add_constant(np.column_stack((t, t ** 2)), has_constant="add")
        at_target = float(np.asarray(dd.trend_model.predict(x))[0])
        detrended = pd.Series(np.asarray(dd.detrended_series, dtype=float),
                              index=s["Harvest Year"].values)
        space = "absolute"
    else:
        raise ValueError(f"detrend method {kind!r} has no held-out-year trend")
    detrended = detrended.dropna()
    sd = float(detrended.std(ddof=1))
    # A spread at floating-point noise level (a perfectly linear series under
    # the linear detrend) would turn every anomaly into a huge z: refuse it.
    scale = 1.0 if space == "percent" else max(1.0, abs(float(at_target)))
    if not np.isfinite(sd) or sd <= 1e-9 * scale:
        raise ValueError(f"degenerate spread ({sd}) for {target_year}")
    if not np.isfinite(at_target) or (space == "percent" and at_target <= 0):
        raise ValueError(f"degenerate trend ({at_target}) for {target_year}")
    return Baseline(int(target_year), float(at_target), sd, space, kind,
                    tuple(int(y) for y in s["Harvest Year"]))


def standardize(values_by_year, target_year, *, baseline_years=None, min_years=5):
    """``(z, mean, sd, n)`` of the target year's value against the other
    years. ``values_by_year`` is a Series indexed by year; ``baseline_years``
    is an iterable of years or a ``(first, last)`` pair; the target year is
    always excluded. Raises when fewer than ``min_years`` remain or the
    spread is zero. ``z`` is NaN when the target year has no value."""
    s = pd.to_numeric(pd.Series(values_by_year), errors="coerce").dropna()
    s.index = s.index.astype(int)
    target = float(s.get(int(target_year), np.nan))
    base = s[s.index != int(target_year)]
    if baseline_years is not None:
        yrs = list(baseline_years)
        if len(yrs) == 2 and all(isinstance(y, (int, np.integer)) for y in yrs) and yrs[0] <= yrs[1] \
                and yrs[1] - yrs[0] > 1:
            base = base[(base.index >= yrs[0]) & (base.index <= yrs[1])]
        else:
            base = base[base.index.isin([int(y) for y in yrs])]
    if len(base) < min_years:
        raise ValueError(f"only {len(base)} baseline year(s) for {target_year}; need {min_years}")
    mean, sd = float(base.mean()), float(base.std(ddof=1))
    # A spread at floating-point noise level (a flat series whose weights
    # drift) would turn any anomaly into a huge z: refuse it like a zero.
    if not np.isfinite(sd) or sd <= 1e-9 * max(1.0, abs(mean)):
        raise ValueError(f"zero spread in the baseline for {target_year}")
    z = (target - mean) / sd if np.isfinite(target) else np.nan
    return z, mean, sd, int(len(base))


# ---------------------------------------------------------------------------
# CID tables
# ---------------------------------------------------------------------------
def cid_dir(root, method, admin_zone, country, crop):
    return Path(root) / "cid" / "indices" / method / admin_zone / country / crop


def load_cid_years(root, method, admin_zone, country, crop, season, years, indices=None):
    """Long CID rows ``[Region, year, Stage, Index, CID]`` of the per-year
    tables, restricted to ``indices`` when given. Missing years are skipped
    with a warning (they simply have no value)."""
    d = cid_dir(root, method, admin_zone, country, crop)
    frames, missing = [], []
    for y in sorted({int(v) for v in years}):
        p = d / f"{country}_{crop}_s{int(season)}_{y}.csv"
        if not p.exists():
            missing.append(y)
            continue
        f = pd.read_csv(p, usecols=["Region", "Harvest Year", "Stage", "Index", "CID"],
                        dtype={"Stage": str})
        if indices is not None:
            f = f[f["Index"].isin(list(indices))]
        frames.append(f)
    if missing:
        logger.warning(f"{country} {crop} s{season}: no CID table for {missing}")
    if not frames:
        return pd.DataFrame(columns=["Region", "year", "Stage", "Index", "CID"])
    out = pd.concat(frames, ignore_index=True).rename(columns={"Harvest Year": "year"})
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    out["CID"] = pd.to_numeric(out["CID"], errors="coerce")
    return out.dropna(subset=["year"]).reset_index(drop=True)


def window_stage_id(stage_id, window):
    """The CID ``Stage`` token to read for a row: the full cumulative chain
    (``"stage"``) or the as-of month alone (``"month"``)."""
    if window not in WINDOWS:
        raise ValueError(f"window must be one of {WINDOWS}, got {window!r}")
    s = str(stage_id)
    return s if window == "stage" else s.split("_", 1)[0]


def indicator_by_year(cid_long, cid, stage_id, *, window="stage"):
    """``[Region, year, value, stage_used]`` of one CID at one window across
    all years.

    ``window="month"`` reads the as-of month alone. ``window="stage"`` reads
    each region's own cumulative window: the longest leading part of the
    table's stage chain that the region's CID rows carry. The outlook table
    names one chain for every region (``8_7_6_5_4_3`` when the earliest
    calendar starts in March), but each region's indices start at its own
    planting month (Iowa ``8_7_6_5_4``, South Dakota ``8_7_6_5``), so an
    exact match would leave every later-planted region empty. The chain
    picked for a region is used in every year.
    """
    sub = cid_long[cid_long["Index"] == cid]
    if sub.empty:
        return pd.DataFrame(columns=["Region", "year", "value", "stage_used"])
    stages = sub["Stage"].astype(str)
    if window == "month":
        tok = window_stage_id(stage_id, window)
        pick = sub[stages == tok].assign(stage_used=tok)
    else:
        window_stage_id(stage_id, window)                # validates the window
        tokens = str(stage_id).split("_")
        prefixes = ["_".join(tokens[:k]) for k in range(len(tokens), 0, -1)]
        frames = []
        for region, g in sub.assign(_stage=stages).groupby("Region", sort=False):
            have = set(g["_stage"])
            chain = next((p for p in prefixes if p in have), None)
            if chain is not None:
                frames.append(g[g["_stage"] == chain].assign(stage_used=chain))
        pick = pd.concat(frames, ignore_index=True) if frames else sub.iloc[0:0].assign(stage_used="")
    out = pick[["Region", "year", "CID", "stage_used"]].rename(columns={"CID": "value"})
    return out.dropna(subset=["value"]).drop_duplicates(["Region", "year"]).reset_index(drop=True)


def national_indicator(values, weights, country):
    """Area-weighted national value per year. ``values`` is
    ``[Region, year, value]``; ``weights`` is ``[Region, year, Area (ha)]``
    (the forecasts' causally filled areas). Returns a Series indexed by year."""
    w = weights[["Region", "year", AREA]].drop_duplicates(["Region", "year"])
    merged = values.merge(w, on=["Region", "year"], how="left")
    # a region-year never forecast has no weight; take the region's latest known
    fallback = w.sort_values("year").groupby("Region")[AREA].last()
    merged[AREA] = merged[AREA].fillna(merged["Region"].map(fallback))
    merged["stage"] = "all"
    nat = to_national(merged, country, value_col="value", obs_col=None, by=("year",))
    if nat.empty:
        return pd.Series(dtype=float)
    return pd.Series(nat["value"].values, index=nat["year"].astype(int).values).sort_index()


# ---------------------------------------------------------------------------
# observation dates from the merged daily inputs
# ---------------------------------------------------------------------------
def observed_dates(crop_t0_csv, variables, year, *, regions=None, chunksize=200_000):
    """Sorted arrays of dates on which each variable had a value, for the
    given calendar year (and the previous one, for seasons that wrap), read
    from the merged daily inputs in chunks. Missing variables are skipped."""
    p = Path(crop_t0_csv)
    if not p.exists():
        return {}
    header = pd.read_csv(p, nrows=0).columns.tolist()
    keep = [v for v in variables if v in header]
    if not keep or "datetime" not in header:
        return {}
    usecols = ["datetime", "region"] + keep
    found = {v: set() for v in keep}
    for chunk in pd.read_csv(p, usecols=usecols, chunksize=chunksize):
        dt = pd.to_datetime(chunk["datetime"], errors="coerce")
        mask = dt.dt.year.isin([int(year), int(year) - 1])
        if regions is not None:
            mask &= chunk["region"].isin(list(regions))
        if not mask.any():
            continue
        sub = chunk[mask]
        d = dt[mask]
        for v in keep:
            ok = pd.to_numeric(sub[v], errors="coerce").notna()
            found[v].update(d[ok].dt.date.unique().tolist())
    return {v: np.array(sorted(s)) for v, s in found.items() if s}


def region_key(name):
    """Comparable spelling of a region name across sources: ``"Homa Bay"``,
    ``"homa_bay"`` and ``"HOMA BAY"`` all give ``"homa_bay"``."""
    import re

    return re.sub(r"[\s_]+", "_", str(name).strip().lower())


def observed_dates_by_region(crop_t0_csv, variables, year, *, chunksize=200_000):
    """``{region_key: {variable: sorted dates with a value}}`` for the
    calendar year (and the previous one), in one chunked pass over the merged
    daily inputs; the key ``"*"`` holds the union over regions."""
    p = Path(crop_t0_csv)
    if not p.exists():
        return {}
    header = pd.read_csv(p, nrows=0).columns.tolist()
    keep = [v for v in variables if v in header]
    if not keep or "datetime" not in header or "region" not in header:
        return {}
    found = {}
    for chunk in pd.read_csv(p, usecols=["datetime", "region"] + keep, chunksize=chunksize):
        dt = pd.to_datetime(chunk["datetime"], errors="coerce")
        mask = dt.dt.year.isin([int(year), int(year) - 1])
        if not mask.any():
            continue
        sub, d = chunk[mask], dt[mask].dt.date
        keys = sub["region"].map(region_key)
        for v in keep:
            ok = pd.to_numeric(sub[v], errors="coerce").notna()
            for k, day in zip(keys[ok], d[ok]):
                found.setdefault(k, {}).setdefault(v, set()).add(day)
                found.setdefault("*", {}).setdefault(v, set()).add(day)
    return {k: {v: np.array(sorted(s)) for v, s in by_var.items()} for k, by_var in found.items()}


def last_observed(dates, cutoff):
    """Last date in ``dates`` on or before ``cutoff`` (a ``date``), or None."""
    if dates is None or len(dates) == 0:
        return None
    arr = np.asarray(dates)
    ok = arr[arr <= cutoff]
    return ok.max() if len(ok) else None


# ---------------------------------------------------------------------------
# roles
# ---------------------------------------------------------------------------
def selected_by_stage(db_path, table, model):
    """``{stage name: set of selected feature names}`` (union over regions)."""
    con = sqlite3.connect(f"file:{Path(db_path)}?mode=ro", uri=True)
    try:
        cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()
        if "Selected Features" not in cols:
            return {}
        df = pd.read_sql(f'SELECT DISTINCT "Stage Name", "Selected Features" FROM "{table}" '
                         f"WHERE \"Experiment Name\" = 'outlook' AND \"Model\" = ?",
                         con, params=(model,))
    finally:
        con.close()
    out = {}
    for stage, raw in zip(df["Stage Name"], df["Selected Features"]):
        feats = literal(raw, []) if isinstance(raw, str) else []
        if not isinstance(feats, (list, tuple)):
            feats = []
        out.setdefault(stage, set()).update(str(f) for f in feats)
    return out


def candidate_families(cfg):
    """CID families the run offered the model (``[DEFAULT] use_cids``; ``['all']``
    means every family) plus ``CCI`` / ``CCIGE`` when ``cci_file`` was set."""
    use = literal(cfg.get("use_cids"), ["all"])
    fams = set()
    allf = False
    if isinstance(use, (list, tuple)):
        for u in use:
            if str(u).lower() == "all":
                allf = True
            else:
                fams.add(feature_family(str(u)))
    elif isinstance(use, str) and use.lower() == "all":
        allf = True
    cci = bool(str(cfg.get("cci_file") or "").strip())
    return {"all": allf, "families": fams, "cci": cci}


def resolve_role(meta, stage, selected, candidates):
    """Role of an indicator row at one stage and whether its family was
    selected there.

    A CID row is an ``input`` whenever its family was a candidate of the run
    (``use_cids = ['all']`` offers every family); the NASS condition rows are
    inputs only when the run set ``cci_file`` (production does), and the
    USDA yield forecast is never one. ``selected`` says whether the model's
    final feature list at that stage carried the family.
    """
    feats = selected.get(stage, set()) if selected else set()
    picked = any(feature_family(f) == meta.family for f in feats)
    if meta.source == "nass_yield":
        return "independent", False
    if meta.source == "nass_cci":
        return ("input" if candidates.get("cci") else "independent"), picked
    if candidates.get("all") or meta.family in candidates.get("families", set()) or picked:
        return "input", picked
    return "independent", picked


# ---------------------------------------------------------------------------
# tracks
# ---------------------------------------------------------------------------
def observed_series(fc):
    """Observed yield per (Region, year): the same at every stage."""
    obs = fc.dropna(subset=[OBS]).drop_duplicates(["Region", "year"])
    return obs[["Region", "year", OBS, AREA]]


def build_yield_track(fc, *, country, crop, target_year, model_type="gaussian",
                      training_year_start=None, display=("t/ha", 1.0), region=None,
                      label=None, min_years=5):
    """Target row: the national (or one region's) predicted yield per issue of
    ``target_year`` as a LOYO standardized anomaly. Returns ``(rows, baseline)``.
    """
    unit, factor = display
    label = label or f"{str(crop).replace('_', ' ').title()} yield forecast"
    if region is None:
        obs_nat = to_national(observed_series(fc).assign(stage="obs"), country,
                              value_col=OBS, obs_col=None, by=("year",))
        obs_by_year = pd.Series(obs_nat["value"].values, index=obs_nat["year"].values)
        live = fc[fc["year"] == int(target_year)]
        nat = to_national(live, country, by=("year", "stage"))
        pred_by_stage = {s: v for s, v in zip(nat["stage"], nat["value"])}
        n_units = {s: n for s, n in zip(nat["stage"], nat["n_units"])}
        aggregation = {s: a for s, a in zip(nat["stage"], nat["aggregation"])}
        scope = "national"
    else:
        sub = fc[fc["Region"] == region]
        if sub.empty:
            raise ValueError(f"region {region!r} not in the forecasts")
        o = observed_series(sub)
        obs_by_year = pd.Series(o[OBS].values, index=o["year"].values)
        live = sub[sub["year"] == int(target_year)]
        pred_by_stage = dict(zip(live["stage"], live[PRED]))
        n_units = {s: 1 for s in pred_by_stage}
        aggregation = {s: "region" for s in pred_by_stage}
        scope = region
    base = loyo_baseline(obs_by_year.index, obs_by_year.values, target_year,
                         model_type=model_type, training_year_start=training_year_start,
                         min_years=min_years)
    stages = (live.drop_duplicates("stage").sort_values("order")
              [["stage", "swd", "stage_id", "asof", "order", "obs_date", "issue_date", "run_date"]])
    rows = []
    for st in stages.itertuples(index=False):
        pred = pred_by_stage.get(st.stage, np.nan)
        if not np.isfinite(pred):
            continue
        rows.append({
            "row": label, "role": "target", "issue_date": st.issue_date,
            "value_std": base.z(pred), "value_raw": pred * factor, "unit": unit,
            "invert": False, "obs_date": st.obs_date, "obs_date_kind": "nominal",
            "stage": st.stage, "stage_id": st.stage_id, "asof_month": st.asof,
            "scope": scope, "value_tnha": pred, "anomaly": base.anomaly(pred),
            "baseline_trend": base.trend, "baseline_sd": base.sd, "baseline_space": base.space,
            "baseline_n": base.n, "baseline_years": f"{base.years[0]}-{base.years[-1]}",
            "normal_raw": base.trend * factor,
            "n_units": n_units.get(st.stage), "aggregation": aggregation.get(st.stage),
            "selected": True, "source": "GEOCIF", "run_date": st.run_date,
        })
    return pd.DataFrame(rows), base


def build_indicator_track(meta, fc, cid_long, *, country, target_year, window="stage",
                          baseline_years=None, training_year_start=None, selected=None,
                          candidates=None, obs_dates=None, region=None, min_years=5):
    """One indicator row per issue of ``target_year``: the CID at the stage's
    window, weighted to the national series, standardized against the other
    years (target excluded, ``training_year_start`` floor), sign flipped when
    ``meta.invert``."""
    live = fc[fc["year"] == int(target_year)]
    stages = (live.drop_duplicates("stage").sort_values("order")
              [["stage", "swd", "stage_id", "asof", "order", "obs_date", "issue_date", "run_date"]])
    weights = fc[["Region", "year", AREA]]
    candidates = candidates or {"all": True, "families": set(), "cci": False}
    rows = []
    for st in stages.itertuples(index=False):
        if st.stage_id is None:
            continue
        vals = indicator_by_year(cid_long, meta.cid, st.stage_id, window=window)
        if region is not None:
            vals = vals[vals["Region"].map(region_key) == region_key(region)]
            series = pd.Series(vals["value"].values, index=vals["year"].astype(int).values)
        else:
            series = (national_indicator(vals[["Region", "year", "value"]], weights, country)
                      if not vals.empty else pd.Series(dtype=float))
        used = sorted(set(vals["stage_used"])) if "stage_used" in vals else []
        if series.empty or int(target_year) not in series.index:
            logger.info(f"{meta.key}: no value at stage {st.stage!r} for {target_year}")
            continue
        if training_year_start is not None:
            series = series[(series.index >= int(training_year_start)) | (series.index == int(target_year))]
        try:
            z, mean, sd, n = standardize(series, target_year, baseline_years=baseline_years,
                                         min_years=min_years)
        except ValueError as exc:
            logger.warning(f"{meta.key} at {st.stage!r}: {exc}")
            continue
        role, picked = resolve_role(meta, st.stage, selected or {}, candidates)
        obs_kind, obs = "nominal", st.obs_date
        if obs_dates and meta.variable in obs_dates:
            real = last_observed(obs_dates[meta.variable], st.obs_date)
            if real is not None:
                obs, obs_kind = real, "observed"
        raw = float(series.loc[int(target_year)])
        rows.append({
            "row": meta.label, "role": role, "issue_date": st.issue_date,
            "value_std": -z if meta.invert else z, "value_raw": raw, "unit": meta.unit,
            "invert": bool(meta.invert), "obs_date": obs, "obs_date_kind": obs_kind,
            "stage": st.stage, "stage_id": st.stage_id, "asof_month": st.asof,
            "scope": region or "national", "cid": meta.cid, "window": window,
            "window_stage": used[0] if len(used) == 1 else ("per region" if used else None),
            "baseline_mean": mean, "baseline_sd": sd, "baseline_n": n, "normal_raw": mean,
            "selected": picked, "source": meta.source, "run_date": st.run_date,
        })
    return pd.DataFrame(rows)


def build_tracks(fc, cid_long, metas, *, country, crop, target_year, cfg=None,
                 window="stage", baseline_years=None, display=("t/ha", 1.0),
                 selected=None, obs_dates=None, region=None, yield_label=None,
                 extra_tracks=(), min_years=5):
    """The tidy long table plus metadata for the source line.

    ``metas`` are the indicator rows (at most four, CID-sourced); rows from
    other sources (USDA, Phase 3) come through ``extra_tracks`` as finished
    frames. Raises when more than four indicator rows result.
    """
    from geocif.viz import snake

    cfg = cfg or {}
    requested = [m.label for m in metas] + [
        str(r) for t in extra_tracks for r in pd.DataFrame(t).get("row", pd.Series(dtype=object)).unique()]
    if len(set(requested)) > MAX_INDICATORS:
        raise ValueError(f"{len(set(requested))} indicator rows requested "
                         f"({', '.join(sorted(set(requested)))}); at most {MAX_INDICATORS}")
    model_type = str(cfg.get("detrend_method") or "gaussian").strip().lower()
    tys = cfg.get("training_year_start")
    tys = int(tys) if tys not in (None, "", "None") else None
    candidates = candidate_families(cfg)

    yield_rows, base = build_yield_track(
        fc, country=country, crop=crop, target_year=target_year, model_type=model_type,
        training_year_start=tys, display=display, region=region, label=yield_label,
        min_years=min_years)
    frames = [yield_rows]
    for meta in metas:
        if meta.source != "cid":
            raise ValueError(f"{meta.key}: non-CID rows come through extra_tracks")
        frames.append(build_indicator_track(
            meta, fc, cid_long, country=country, target_year=target_year, window=window,
            baseline_years=baseline_years, training_year_start=tys, selected=selected,
            candidates=candidates, obs_dates=obs_dates, region=region, min_years=min_years))
    frames.extend(pd.DataFrame(t) for t in extra_tracks)
    tracks = pd.concat([f for f in frames if f is not None and not f.empty], ignore_index=True)
    n_ind = tracks.loc[tracks["role"] != "target", "row"].nunique()
    if n_ind > MAX_INDICATORS:
        raise ValueError(f"{n_ind} indicator rows requested; at most {MAX_INDICATORS}")
    tracks = snake.validate_tracks(tracks)

    run_dates = sorted({d for d in tracks.get("run_date", pd.Series(dtype=object)).dropna()})
    notes = ["Earlier issues of the live year are re-forecasts made with today's data and "
             "training pool, not the forecasts published at the time"]
    if len(run_dates) > 1:
        notes.append(f"Rows come from runs on {', '.join(str(d) for d in run_dates)}")
    missing = _missing_issues(tracks)
    if missing:
        notes.append("Missing issues: " + "; ".join(missing))
    flat = flat_rows(tracks)
    if flat:
        notes.append(f"{', '.join(flat)} barely vary between years (spread under 1% of "
                     f"the mean), so their moves are small in absolute terms")
    sources = ["GEOCIF"] + [m.label for m in metas] + [
        str(s) for s in sorted({str(x) for t in extra_tracks for x in pd.DataFrame(t).get("source", [])})]
    meta = {"issues": sorted(set(tracks["issue_date"])), "sources": sources,
            "baseline": (base.years[0], base.years[-1]), "target_year": int(target_year),
            "notes": notes, "yield_baseline": base}
    return tracks, meta


def flat_rows(tracks, cv=0.01):
    """Indicator rows whose baseline spread is under ``cv`` of the baseline
    mean at the latest issue (a count that saturates, e.g. every day above
    25 C): their sigma moves are real but describe tiny absolute changes."""
    if "baseline_mean" not in tracks.columns:
        return []
    out = []
    for row, g in tracks[tracks["role"] != "target"].groupby("row", sort=False):
        g = g.sort_values("issue_date")
        m, sd_ = g["baseline_mean"].iloc[-1], g["baseline_sd"].iloc[-1]
        if pd.notna(m) and pd.notna(sd_) and abs(m) > 0 and sd_ / abs(m) < cv:
            out.append(str(row))
    return out


def _missing_issues(tracks):
    issues = sorted(set(tracks["issue_date"]))
    out = []
    for row, g in tracks.groupby("row", sort=False):
        have = set(g["issue_date"])
        gaps = [d.strftime("%b %Y") for d in issues if d not in have]
        if gaps:
            out.append(f"{row} ({', '.join(gaps)})")
    return out


# ---------------------------------------------------------------------------
# USDA rows (Phase 3): crop condition and the NASS yield forecast
# ---------------------------------------------------------------------------
def norm_region(name):
    """``"north_carolina"`` for ``"North Carolina"``: the CCI spelling."""
    return str(name).strip().lower().replace(" ", "_")


def same_date_in_year(d, year):
    """``d`` moved to ``year`` (Feb 29 becomes Feb 28)."""
    try:
        return d.replace(year=int(year))
    except ValueError:
        return d.replace(year=int(year), day=28)


def condition_at(weekly, when, *, metric="cci", max_age_days=21):
    """Per region, the latest report with ``week_ending`` on or before
    ``when`` and at most ``max_age_days`` old: ``[region, value, week_ending]``."""
    when = pd.Timestamp(when)
    w = weekly[(weekly["week_ending"] <= when)
               & (weekly["week_ending"] >= when - pd.Timedelta(days=max_age_days))]
    latest = w.sort_values("week_ending").groupby("region", sort=False).tail(1)
    return latest[["region", metric, "week_ending"]].rename(columns={metric: "value"})


def _region_lookup(fc):
    return {norm_region(r): r for r in fc["Region"].unique()}


def build_cci_track(weekly, fc, *, country, target_year, metric="cci", meta=None,
                    baseline_years=None, training_year_start=None, selected=None,
                    candidates=None, region=None, min_years=5, cci_scale="repo",
                    max_age_days=21):
    """USDA crop-condition row: at each issue the latest weekly report on or
    before the issue date, area-weighted over the states of the forecast
    pool, standardized against the same date in the other years (target
    excluded). ``obs_date`` is the report's ``week_ending`` (observed)."""
    meta = meta or INDICATOR_META["cci" if metric == "cci" else "cci_ge"]
    candidates = candidates or {"all": True, "families": set(), "cci": True}
    w = weekly.copy()
    w["week_ending"] = pd.to_datetime(w["week_ending"], errors="coerce")
    w["region"] = w["region"].map(norm_region)
    w[metric] = pd.to_numeric(w[metric], errors="coerce")
    w = w.dropna(subset=["week_ending", metric])
    if region is not None:
        w = w[w["region"] == norm_region(region)]
    if w.empty:
        logger.warning(f"{meta.key}: no crop-condition rows for the pool")
        return pd.DataFrame()
    lookup = _region_lookup(fc)
    live = fc[fc["year"] == int(target_year)]
    stages = (live.drop_duplicates("stage").sort_values("order")
              [["stage", "swd", "stage_id", "asof", "order", "obs_date", "issue_date", "run_date"]])
    years = sorted(set(fc["year"].astype(int)) | {int(target_year)})
    if training_year_start is not None:
        years = [y for y in years if y >= int(training_year_start) or y == int(target_year)]
    weights = fc[["Region", "year", AREA]].drop_duplicates(["Region", "year"])
    rows = []
    for st in stages.itertuples(index=False):
        frames, used_dates = [], []
        for y in years:
            when = same_date_in_year(st.issue_date, y)
            at = condition_at(w, when, metric=metric, max_age_days=max_age_days)
            if at.empty:
                continue
            at = at.assign(Region=at["region"].map(lookup), year=int(y)).dropna(subset=["Region"])
            if at.empty:
                continue
            if y == int(target_year):
                used_dates = list(at["week_ending"])
            frames.append(at[["Region", "year", "value"]])
        if not frames:
            continue
        vals = pd.concat(frames, ignore_index=True)
        if region is not None:
            series = pd.Series(vals["value"].values, index=vals["year"].values)
        else:
            series = national_indicator(vals, weights, country)
        if series.empty or int(target_year) not in series.index:
            logger.info(f"{meta.key}: no condition value for the {st.stage!r} issue of {target_year}")
            continue
        try:
            z, mean, sd, n = standardize(series, target_year, baseline_years=baseline_years,
                                         min_years=min_years)
        except ValueError as exc:
            logger.warning(f"{meta.key} at {st.stage!r}: {exc}")
            continue
        role, picked = resolve_role(meta, st.stage, selected or {}, candidates)
        raw = float(series.loc[int(target_year)])
        if metric == "cci" and cci_scale == "plan":
            raw = 100.0 + 4.0 * raw
        obs = max(used_dates).date() if used_dates else st.obs_date
        rows.append({
            "row": meta.label, "role": role, "issue_date": st.issue_date,
            "value_std": -z if meta.invert else z, "value_raw": raw,
            "unit": meta.unit if cci_scale == "repo" else "index (100-500)",
            "invert": bool(meta.invert), "obs_date": obs,
            "obs_date_kind": "observed" if used_dates else "nominal",
            "stage": st.stage, "stage_id": st.stage_id, "asof_month": st.asof,
            "scope": region or "national", "cid": meta.cid, "window": "latest report",
            "window_stage": None, "baseline_mean": mean, "baseline_sd": sd, "baseline_n": n,
            "normal_raw": (100.0 + 4.0 * mean) if (metric == "cci" and cci_scale == "plan") else mean,
            "selected": picked, "source": "USDA NASS crop condition", "run_date": st.run_date,
        })
    return pd.DataFrame(rows)


def build_usda_yield_track(nass_frame, fc, baseline, *, country, crop, target_year,
                           display=("t/ha", 1.0), label="USDA yield forecast",
                           min_pool_frac=0.8):
    """Independent US row: the NASS monthly state yield forecast of the as-of
    month (the August report serves the September issue), area-weighted over
    the states of the forecast pool and measured on the SAME leave-one-year-out
    yield baseline as the GEOCIF row, so the two rows share a yardstick.
    ``obs_date`` is the report's load time. Months without a NASS forecast
    (before August for corn) are gaps."""
    from geocif.viz.cone import BU_PER_TNHA

    factor = BU_PER_TNHA.get(crop)
    if factor is None:
        raise ValueError(f"no bushel conversion for crop {crop!r}")
    unit, disp_factor = display
    sub = nass_frame[(nass_frame["crop"] == crop) & nass_frame["ref_month"].notna()
                     & (pd.to_numeric(nass_frame["year"], errors="coerce") == int(target_year))]
    if sub.empty:
        logger.info(f"USDA yield: no {target_year} monthly forecast for {crop}")
        return pd.DataFrame()
    lookup = _region_lookup(fc)
    live = fc[fc["year"] == int(target_year)]
    pool = set(live["Region"].unique())
    stages = (live.drop_duplicates("stage").sort_values("order")
              [["stage", "swd", "stage_id", "asof", "order", "obs_date", "issue_date", "run_date"]])
    weights = fc[["Region", "year", AREA]].drop_duplicates(["Region", "year"])
    rows = []
    for st in stages.itertuples(index=False):
        m = sub[pd.to_numeric(sub["ref_month"], errors="coerce") == int(st.asof)].copy()
        m["Region"] = m["Region"].map(lambda r: lookup.get(norm_region(r)))
        m = m.dropna(subset=["Region"])
        if m.empty:
            continue
        covered = len(set(m["Region"]) & pool)
        if covered < min_pool_frac * len(pool):
            logger.info(f"USDA yield: {st.stage!r} covers {covered} of {len(pool)} states; skipped")
            continue
        vals = pd.DataFrame({"Region": m["Region"].values, "year": int(target_year),
                             "value": m["yield_bu_ac"].values / factor})
        nat = national_indicator(vals, weights, country)
        if nat.empty:
            continue
        value_tnha = float(nat.iloc[0])
        load = pd.to_datetime(m["load_time"], errors="coerce").max()
        obs = load.date() if pd.notna(load) else st.obs_date
        rows.append({
            "row": label, "role": "independent", "issue_date": st.issue_date,
            "value_std": baseline.z(value_tnha), "value_raw": value_tnha * disp_factor,
            "unit": unit, "invert": False, "obs_date": obs,
            "obs_date_kind": "observed" if pd.notna(load) else "nominal",
            "stage": st.stage, "stage_id": st.stage_id, "asof_month": st.asof,
            "scope": "national", "value_tnha": value_tnha, "anomaly": baseline.anomaly(value_tnha),
            "baseline_trend": baseline.trend, "baseline_sd": baseline.sd,
            "baseline_space": baseline.space, "baseline_n": baseline.n,
            "normal_raw": baseline.trend * disp_factor,
            "n_units": int(len(vals)), "selected": False,
            "source": "USDA NASS yield forecast", "run_date": st.run_date,
        })
    return pd.DataFrame(rows)
