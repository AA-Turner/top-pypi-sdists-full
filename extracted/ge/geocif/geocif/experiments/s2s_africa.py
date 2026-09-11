"""Africa-wide pre-season S2S forecasts for HarvestStat country x crop x season.

Extends the single-country pre-season model to every FEWS NET African
country that HarvestStat covers. Three inputs, all keyed so they join
exactly:

* **Yields** — ``hvstat_africa_data_v1.0.csv``, keyed by ``fnid``.
* **Calendar** — ``EWCM_*.xlsx``: 24 half-month bins per admin/livelihood
  zone coded 1=planting, 2=growing, 3=harvest, 4=post-harvest. EWCM has
  **no bean sheet for Africa** (its soybean sheets carry African rows but
  no data), so beans fall back to HarvestStat's own ``planting_month`` /
  ``harvest_month`` columns. Every combination records which source it
  used in ``calendar_source``.
* **S2S** — per-region CSVs whose ``region_id`` IS the HarvestStat
  ``fnid``, so the join needs no name matching and is insensitive to
  which admin level the extraction ran at.

Only **extended-term** forecasts are produced: a combination is forecast
only while its next season has not started. ``in_season`` combinations
belong to the in-season CID system and are excluded with that reason.

Usage::

    from geocif.experiments import s2s_africa
    out = s2s_africa.run(parser=parser)
"""
import ast
import glob
import logging
import re
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

from geocif.experiments.s2s_eligibility import window_state
from geocif.experiments.s2s_pooled_model import (
    REAL_INIT_YEARS, init_calendar, lead_map, season_months)
from geocif.experiments.s2s_simple_model import (
    FEATURES, _fold_bins, _to_class, fit_ols, predict_ols)
from geocif.utils import PRIMARY_SEASON_NAMES, SECONDARY_SEASON_NAMES

logger = logging.getLogger(__name__)

# Crop label -> the HarvestStat ``product`` values that count as that crop.
CROP_PRODUCTS = {
    "maize": ["Maize"],
    "beans": ["Beans (mixed)"],
}
# Crop label -> EWCM sheet stem. Beans are absent from EWCM for Africa.
EWCM_STEM = {"maize": "maize"}

MIN_YEARS = 12          # usable harvest years needed to fit + score
MIN_UNITS = 5           # admin units needed for within-year ranking
MAX_OFFSET = 4          # months before planting (1..4); 4 loses grain-fill
OOS_TOLERANCE = 1.0     # sd beyond the training range still called in-support
N_PERM = 300            # year-block permutations behind the skill test
PERM_ALPHA = 0.05       # one-sided; NOT corrected for the 17-combination sweep
# Skill bar used when no permutation test is run. Anderson et al. 2024
# use ROC > 0.6, following the prior global crop-forecast literature;
# set to 0.5 here by request. Note what that costs: the LOYO null sits
# near 0.45, so a PURE NOISE region clears 0.5 roughly 36% of the time
# on a 22-year record (against 22% at 0.6).
SKILL_ROC_THRESHOLD = 0.5
# What actually limits a per-region AUC is RECORD LENGTH, not the number of
# low-tercile events. Measured on pure noise, the AUC sampling sd falls
# smoothly with events — 0.304 (1), 0.220 (2), 0.185 (3), 0.166 (4), 0.152
# (5), 0.139 (7), 0.133 (9) — with no cliff anywhere, so a low-event cut is
# an arbitrary proxy. Regions flagged by one turn out to have an ordinary
# low-year share (median 0.300, right at the tercile rate) and merely a
# short record (median 12 years vs 19). So gate on years, reusing MIN_YEARS,
# and keep a low-event guard only for the genuinely degenerate cases: 0
# events makes AUC undefined and 1 gives sd 0.30 with a 40% false-positive
# rate against a 0.6 bar.
MIN_LOW_YEARS = 2
# Above this backtested trend-extrapolation error a t/ha number is dominated
# by not knowing the baseline rather than by the climate signal (median
# across Africa is ~50% error against a ~27% climate signal), so the yield
# level is written to the CSV but withheld from the maps.
TREND_EXTRAP_MAX_PCT = 20.0
EVAL_SPAN = (1995, 2016)   # real-S2S hindcast era

# HarvestStat country -> EWCM country spelling, where they differ.
EWCM_ALIAS = {
    "Tanzania, United Republic of": "United Republic of Tanzania",
    "DRC": "Democratic Republic of the Congo",
}
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BIN_COLS = [f"{m}_{h}" for m in MONTHS for h in (1, 15)]


# ---------------------------------------------------------------------------
# yields
# ---------------------------------------------------------------------------
def load_yields(hvstat_csv, products):
    """Filtered, PS-aggregated HarvestStat rows for ``products``."""
    from geocif.production_analysis._common import load_filtered_hvstat

    df = load_filtered_hvstat(hvstat_csv)
    df = df[df["product"].isin(products)].copy()
    df = df.rename(columns={"yield": "obs", "harvest_year": "year"})
    return df[["fnid", "country", "product", "season_name", "year", "obs"]]


def causal_trend_fnid(obs):
    """Leave-one-year-out linear trend per fnid (never sees its own year)."""
    rows = []
    for fnid, g in obs.groupby("fnid"):
        g = g.sort_values("year")
        if len(g) < 8:
            continue
        yrs = g["year"].to_numpy(dtype=float)
        vals = g["obs"].to_numpy(dtype=float)
        for i in range(len(g)):
            m = np.ones(len(g), dtype=bool)
            m[i] = False
            b, a = np.polyfit(yrs[m], vals[m], 1)
            rows.append({"fnid": fnid, "year": int(yrs[i]), "obs": vals[i],
                         "trend": float(b * yrs[i] + a)})
    d = pd.DataFrame(rows)
    if d.empty:
        return d
    d = d[d["trend"] > 0].copy()
    d["anom"] = d["obs"] / d["trend"] - 1
    return d


# ---------------------------------------------------------------------------
# crop calendar
# ---------------------------------------------------------------------------
def season_index(season_name):
    """1 for a primary season, 2 for a secondary one, else 1.

    Exact membership alone is not enough: HarvestStat writes
    ``'North 2nd Season'`` while the shared list holds ``'2nd Season'``, so
    an exact test missed it and the default of 1 handed a SECOND-season crop
    the ``maize_1`` EWCM sheet — the wrong planting month, window and leads.
    So fall back to a substring test, secondary first (a name like
    ``'Long/Dry'`` carries both a primary and a secondary token, and the
    secondary reading is the safer default for a calendar lookup). ``-off``
    is treated as secondary, mirroring ``Main-off`` and ``Cold-off``, which
    the list already classifies that way.

    Names resolved by anything other than an exact match are logged, so a
    reclassification is auditable rather than silent.
    """
    if season_name in PRIMARY_SEASON_NAMES:
        return 1
    if season_name in SECONDARY_SEASON_NAMES:
        return 2
    name = str(season_name).lower()
    for tag in [s.lower() for s in SECONDARY_SEASON_NAMES] + ["-off"]:
        if tag in name:
            logger.info(f"season '{season_name}' -> 2 (matched '{tag}')")
            return 2
    for tag in (s.lower() for s in PRIMARY_SEASON_NAMES):
        if tag in name:
            logger.info(f"season '{season_name}' -> 1 (matched '{tag}')")
            return 1
    return 1


def _bounds_from_bins(v):
    """(planting_month, harvest_month, wraps) from one 24-bin row.

    Each EWCM row is a single cyclic run 0->1->2->3->4->0, so the season
    is found by locating the start of the planting run and walking
    forward. Rows carrying any -1 are 'crop not grown here' and are
    rejected outright — a bare 'any value > 0' test would accept the
    Central African Republic / Vakaga row (23 bins of -1 plus a stray 3)
    and report a December planting.
    """
    v = np.asarray(v, dtype=float)
    if len(v) != 24 or np.isnan(v).any():
        return None
    if (v == -1).any() or not (v > 0).any():
        return None
    ones = [i for i in range(24) if v[i] == 1 and v[(i - 1) % 24] != 1]
    if not ones:
        return None
    plant_bin = ones[0]
    order = [(plant_bin + k) % 24 for k in range(24)]
    threes = [i for i in order if v[i] == 3]
    if threes:
        harv_bin = threes[-1]
    else:
        nz = [i for i in order if v[i] in (1, 2, 3)]
        harv_bin = nz[-1] if nz else plant_bin
    return (plant_bin // 2 + 1, harv_bin // 2 + 1,
            bool(order.index(harv_bin) > 0 and harv_bin < plant_bin))


def ewcm_calendar(xlsx_path, country, crop, season_idx):
    """Modal (planting, harvest, wraps) across a country's EWCM zones."""
    stem = EWCM_STEM.get(crop)
    if stem is None:
        return None
    path = Path(xlsx_path)
    if not path.exists():
        return None
    sheet = f"{stem}_{season_idx}"
    try:
        xl = pd.ExcelFile(path)
        if sheet not in xl.sheet_names:
            if stem in xl.sheet_names:
                sheet = stem
            else:
                xl.close()
                return None
        df = pd.read_excel(xl, sheet_name=sheet)
    except Exception as e:                     # pragma: no cover - IO guard
        logger.warning(f"EWCM read failed for {country}/{sheet}: {e}")
        return None
    finally:
        try:
            xl.close()
        except Exception:
            pass

    ccol = next((c for c in df.columns if c.lower() == "country"), None)
    if ccol is None:
        return None
    want = EWCM_ALIAS.get(country, country).lower().strip()
    rows = df[df[ccol].astype(str).str.lower().str.strip() == want]
    if rows.empty:
        return None
    cols = [c for c in BIN_COLS if c in df.columns]
    if len(cols) != 24:
        return None

    got = [_bounds_from_bins(r) for _, r in rows[cols].iterrows()]
    got = [g for g in got if g]
    if not got:
        return None
    plant = int(pd.Series([g[0] for g in got]).mode().iloc[0])
    same = [g for g in got if g[0] == plant]
    harvest = int(pd.Series([g[1] for g in same]).mode().iloc[0])
    return {"planting_month": plant, "harvest_month": harvest,
            "wraps": bool(same[0][2]), "calendar_source": f"EWCM:{sheet}",
            "n_zones": len(got),
            "planting_min": int(min(g[0] for g in got)),
            "planting_max": int(max(g[0] for g in got))}


def hvstat_calendar(raw_rows):
    """(planting, harvest, wraps) from HarvestStat's own month columns.

    The fallback for crops EWCM does not cover (beans). ``raw_rows`` are
    the unaggregated HarvestStat rows for one country x product x season.
    """
    r = raw_rows.dropna(subset=["planting_month", "harvest_month"])
    r = r[(r["planting_month"] > 0) & (r["harvest_month"] > 0)]
    if r.empty:
        return None
    plant = int(r["planting_month"].mode().iloc[0])
    harvest = int(r["harvest_month"].mode().iloc[0])
    py = r["planting_year"]
    hy = r["harvest_year"]
    wraps = bool((hy > py).mode().iloc[0]) if (hy > py).any() else harvest < plant
    return {"planting_month": plant, "harvest_month": harvest, "wraps": wraps,
            "calendar_source": "hvstat", "n_zones": int(r["fnid"].nunique()),
            "planting_min": int(r["planting_month"].min()),
            "planting_max": int(r["planting_month"].max())}


# ---------------------------------------------------------------------------
# S2S features (joined on fnid)
# ---------------------------------------------------------------------------
def country_slug(country, threshold_root):
    """Directory slug holding a country's S2S extraction, or None.

    The extraction names directories after the BOUNDARY FILE's country
    (``Tanzania``), which is not always the HarvestStat spelling
    (``Tanzania, United Republic of``) nor the config section
    (``united_republic_of_tanzania``). Try the plausible spellings and
    accept whichever directory actually holds S2S files.
    """
    base = country.lower().strip()
    cands = [
        base.replace(" ", "_").replace(",", ""),
        base.replace(",", "").replace(" ", "_"),
        re.sub(r",.*$", "", base).strip().replace(" ", "_"),   # "tanzania"
    ]
    # "Tanzania, United Republic of" -> "united_republic_of_tanzania"
    if "," in base:
        head, tail = [x.strip() for x in base.split(",", 1)]
        cands.append(f"{tail}_{head}".replace(" ", "_"))
    for s in dict.fromkeys(cands):
        if glob.glob(str(Path(threshold_root) / s / "admin_*" / "cr"
                         / "s2s_tprate" / "*.csv")):
            return s
    return None


def load_s2s_fnid(country_root, var):
    """All S2S rows for a country keyed by fnid.

    Reads every ``admin_*`` extraction present and de-duplicates on
    (fnid, year, month): the same polygon can be written under more than
    one admin level, with identical values, because the level only sets
    the label and folder — the data is per-FNID either way.
    """
    frames = []
    for d in sorted(glob.glob(str(Path(country_root) / "admin_*" / "cr"
                                  / f"s2s_{var}"))):
        for f in glob.glob(str(Path(d) / "*.csv")):
            try:
                frames.append(pd.read_csv(f))
            except Exception:
                continue
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df = df.rename(columns={"region_id": "fnid"})
    return df.drop_duplicates(["fnid", "year", "month"])


def build_features(tp, t2, planting, wraps, offset, years, fnids):
    """z-scored S2S features per (fnid, harvest year) for one init offset."""
    lm = lead_map(planting, offset)
    smon = list(lm)
    gf = [m for m in season_months(planting)[2:4] if m in lm]
    if not smon:
        return pd.DataFrame()
    real = list(range(REAL_INIT_YEARS[0] + 1, REAL_INIT_YEARS[1] + 2))
    tp_i = tp.set_index(["fnid", "year", "month"]).sort_index()
    t2_i = t2.set_index(["fnid", "year", "month"]).sort_index()

    rows = []
    for fnid in fnids:
        raw = {}
        for y in sorted(set(years) | set(real)):
            iy, im = init_calendar(planting, offset, y, wraps)
            try:
                rp = tp_i.loc[(fnid, iy, im)]
                rt = t2_i.loc[(fnid, iy, im)]
            except KeyError:
                continue
            if isinstance(rp, pd.DataFrame):
                rp = rp.iloc[0]
            if isinstance(rt, pd.DataFrame):
                rt = rt.iloc[0]
            p = {tm: float(rp.get(f"s2s_tprate_lead{l}", np.nan))
                 for tm, l in lm.items()}
            t = {tm: float(rt.get(f"s2s_t2m_lead{l}", np.nan))
                 for tm, l in lm.items()}
            if any(not np.isfinite(x) for x in p.values()):
                continue
            if any(not np.isfinite(x) for x in t.values()):
                continue
            raw[y] = {"PRCPTOT": float(np.mean([p[m] for m in smon])),
                      "TMEAN": float(np.mean([t[m] for m in smon]))}
            if gf:
                raw[y]["P_GF"] = float(np.mean([p[m] for m in gf]))
        ref = [raw[y] for y in real if y in raw]
        if len(ref) < 10:
            continue
        keys = ["PRCPTOT", "TMEAN"] + (["P_GF"] if gf else [])
        st = {}
        for k in keys:
            arr = np.array([r[k] for r in ref], dtype=float)
            sd = float(arr.std(ddof=1))
            if not np.isfinite(sd) or sd == 0:
                st = None
                break
            st[k] = (float(arr.mean()), sd)
        if st is None:
            continue
        for y, v in raw.items():
            if y not in years:
                continue
            z = {f"z_{k}": (v[k] - st[k][0]) / st[k][1] for k in keys}
            rows.append({"fnid": fnid, "year": int(y), **z,
                         "DRYHEAT": z["z_PRCPTOT"] * z["z_TMEAN"]})
    return pd.DataFrame(rows)


# Selectable predictor sets. `rain` is the DEFAULT: it drops temperature
# and the interaction entirely. `full` is the historical four-term model,
# kept selectable for comparison.
#
# Why `rain` exists, measured on the climatology-filtered pipeline:
# z_TMEAN correlates with YEAR at mean r = +0.593 and significantly in
# 16 of 16 combinations (rainfall: +0.010, 7 of 16). The target is
# detrended per unit, so it carries no year-index component at all — the
# temperature channel therefore feeds the fit a trend the target cannot
# contain. Removing z_TMEAN's own trend does not rescue it (mean R2
# -0.174 -> -0.150) but dropping temperature outright does
# (-0.174 -> -0.064; national -0.695 -> -0.344), while AUC is unchanged
# to slightly better. It also sheds the whole out-of-support problem:
# every large excursion is z_TMEAN or DRYHEAT, and NOAA's real-time
# stream runs ~1.3 C warmer than the hindcast it is standardised against
# while tprate shows no such break.
#
# Measured side by side on the same run: AUC 0.457 -> 0.463, national
# 0.412 -> 0.418, R2 -0.174 -> -0.064, national R2 -0.695 -> -0.344,
# combinations clearing AUC 0.5 six -> eight, and the median forecast
# unit goes from 2.97 sd OUTSIDE the fitted range to 0.00 (worst case
# 27.2 sd -> 3.9). The out-of-support problem was almost entirely a
# temperature problem. ~40% of the apparent signal went with it: 474 of
# 647 regions moved toward climatology and the count above P_low 0.67
# fell from 53 to 23.
#
# `rain_main` is kept only as a control — grain-fill rainfall carries
# real information (dropping it costs AUC 0.463 -> 0.407).
FEATURE_SETS = {
    "full": list(FEATURES),
    "rain": ["z_PRCPTOT", "z_P_GF"],
    "rain_main": ["z_PRCPTOT"],
    "no_interact": ["z_PRCPTOT", "z_TMEAN", "z_P_GF"],
}
DEFAULT_FEATURE_SET = "rain"


def features_for_offset(offset, feature_set=DEFAULT_FEATURE_SET):
    """The feature list an init at ``offset`` can actually construct.

    Offsets beyond 3 lose grain-fill rainfall: the window would sit past
    lead 6, the edge of the S2S horizon.
    """
    feats = FEATURE_SETS.get(feature_set, FEATURE_SETS[DEFAULT_FEATURE_SET])
    if offset > 3:
        feats = [f for f in feats if f != "z_P_GF"]
    return list(feats)


def real_harvest_years(planting, offset, wraps, years):
    """The harvest years backed by a REAL S2S forecast, not climatology fill.

    NOAA's archive stops at the 1993-2016 hindcast and geoprepare gap-fills
    every later init with the per-(fnid, month, lead) hindcast MEAN, writing
    a byte-identical copy for each year. Those rows reach the model as ONE
    repeated design point at the unit's climatological centre (all four
    predictors ~0) paired with genuinely varying yields, so they behave as
    shrinkage toward the origin: they pull the intercept and, because
    DRYHEAT = 0 sits off the design centroid (E[z_P*z_T] != 0), they drag
    the DRYHEAT slope specifically. Left in, they FLATTER every skill
    metric — for Zimbabwe maize 48 of 224 training rows were fill, and
    removing them moves R2 from -0.151 to -0.390 and mean P_low from 0.618
    to 0.487.

    The predecessor (``s2s_simple_model.REAL_HARVESTS``) filtered these out;
    the filter was lost when this module was written. Derived per combination
    rather than hardcoded, because a wrapped season maps harvest H to init
    H-1 and an unwrapped one to init H.
    """
    return [y for y in years
            if init_calendar(planting, offset, int(y), wraps)[0]
            <= REAL_INIT_YEARS[1]]


def clip_to_support(fx, train, feats):
    """Clip forecast features to the training range, and MEASURE the clip.

    A linear model evaluated outside its training support returns a boundary
    value, not a forecast, and clipping silently turns "we have never seen
    this" into "we are certain". That is not hypothetical here: NOAA's S2S
    real-time stream runs ~1.3 C warmer than its 1993-2016 hindcast members
    (South Africa, Aug init: hindcast mean 18.55 C, hottest hindcast year
    19.30 C, 2026 forecast 19.82 C) while tprate shows no such shift. So
    z_TMEAN lands at +3.5 to +5.7 sd in EVERY country and DRYHEAT
    (= z_PRCPTOT * z_TMEAN) inherits it, pinning half the continent to its
    training extreme and manufacturing confident-looking probabilities.

    Returns the clipped frame plus a per-row report: how many features were
    clipped, the worst exceedance in training standard deviations, and which
    feature it was.
    """
    fxc = fx.copy()
    exceed = pd.DataFrame(index=fx.index)
    for f in feats:
        if f == "DRYHEAT":
            raw = fx["z_PRCPTOT"] * fx["z_TMEAN"]
        else:
            raw = fx[f]
        lo, hi = float(train[f].min()), float(train[f].max())
        sd = float(train[f].std(ddof=1)) or 1.0
        exceed[f] = np.maximum((raw - hi) / sd, (lo - raw) / sd).clip(lower=0)
        fxc[f] = raw.clip(lo, hi)
    rep = pd.DataFrame({
        "n_clipped": (exceed > 0).sum(axis=1),
        "oos_max_sigma": exceed.max(axis=1),
        "oos_feature": exceed.idxmax(axis=1).where(
            exceed.max(axis=1) > 0, ""),
    }, index=fx.index)
    return fxc, rep


# ---------------------------------------------------------------------------
# hindcast + forecast for one combination
# ---------------------------------------------------------------------------
def loyo(data, feats, eval_years):
    """Leave-one-year-out predictions (the fold year never trains)."""
    outs = []
    for y in eval_years:
        train = data[(data.year != y) & data.anom.notna()]
        test = data[data.year == y].copy()
        if test.empty or len(train) < 40:
            continue
        res = fit_ols(train, feats)
        test["ahat"] = predict_ols(res, test, feats)
        outs.append(test)
    return pd.concat(outs, ignore_index=True) if outs else pd.DataFrame()


def edge_table(anoms):
    """Leave-one-out tercile edges and low-tercile event per (fnid, year).

    These depend only on the yields, so they are the same for every model,
    every offset and every permutation — computing them once instead of once
    per scored row is what makes the permutation test affordable (hours to
    minutes).
    """
    tab = {}
    degenerate = 0
    a = anoms.dropna(subset=["anom"])
    for fnid, g in a.groupby("fnid"):
        v = g.set_index("year")["anom"]
        for y, val in v.items():
            tr = v.drop(index=y)
            if len(tr) < 9:
                continue
            e = _fold_bins(tr)
            # _fold_bins uses pd.qcut(duplicates="drop"), which SILENTLY
            # collapses bins when anomalies tie: 1 inner edge gives two
            # classes, 0 gives one, and with constant yields every year is
            # then labelled "low". Nothing raises — the labels just stop
            # being terciles. Skip those folds and count them rather than
            # scoring against a boundary that does not mean what it says.
            if len(e) < 2:
                degenerate += 1
                continue
            tab[(fnid, int(y))] = (e, int(_to_class(val, e) == 0))
    if degenerate:
        logger.warning(
            f"tercile edges collapsed on {degenerate} folds (tied anomalies); "
            f"those unit-years are unlabelled and excluded from scoring")
    return tab


def score_combo(lo, anoms, edges=None):
    """Detrended-tercile classification + rRMSE vs the trend baseline."""
    from sklearn.metrics import roc_auc_score

    if edges is None:
        edges = edge_table(anoms)
    recs = []
    for fnid, y, ah in zip(lo["fnid"].to_numpy(), lo["year"].to_numpy(),
                           lo["ahat"].to_numpy()):
        t = edges.get((fnid, int(y)))
        if t is None or not np.isfinite(ah):
            continue
        e, event = t
        recs.append({"event": event, "pred_c": int(_to_class(ah, e)),
                     "score": -ah})
    rec = pd.DataFrame(recs)
    obs = lo["obs"]
    pred = lo["trend"] * (1 + lo["ahat"])
    rrmse = 100 * float(np.sqrt(((obs - pred) ** 2).mean())) / float(obs.mean())
    rr_tr = 100 * float(np.sqrt(((obs - lo["trend"]) ** 2).mean())) / float(obs.mean())
    out = {"n": int(len(lo)), "rrmse": round(rrmse, 2),
           "rrmse_trend": round(rr_tr, 2),
           "beats_trend": bool(rrmse < rr_tr)}
    if not rec.empty and rec.event.nunique() == 2:
        low, nl = rec[rec.event == 1], rec[rec.event == 0]
        out.update({
            "auc": round(float(roc_auc_score(rec.event, rec.score)), 3),
            "low_recall": round(float((low.pred_c == 0).mean()), 3),
            "far": round(float((nl.pred_c == 0).mean()), 3)})
    # The pooled AUC alone hides which question the model can answer; carry
    # the national and spatial split alongside it everywhere, and the
    # regression metrics too — rRMSE without R2 is half the picture.
    out.update({k: v for k, v in decomposed_auc(lo, anoms, edges).items()
                if k != "auc"})
    out.update(decomposed_r2(lo))
    out["n_years"] = int(lo["year"].nunique())
    return out


def decomposed_auc(lo, anoms, edges):
    """Split the pooled region-year AUC into the two abilities it conflates.

    A pooled AUC over region-years looks like it rests on hundreds of
    samples, but when the model calls a year wrong it gets EVERY region in
    that country wrong at once — so the effective sample size is YEARS, not
    unit-years, and the pooled number is very nearly the between-year one
    (Zambia maize: 1,345 region-years, 19 years, pooled 0.546 vs
    between-year 0.512).

    ``auc_national``  one value per year, event = bottom tercile of the
                      national series. This is Anderson et al.'s task.
    ``auc_spatial``   within each year separately, can the model rank WHICH
                      regions land in their own bottom tercile? Averaged
                      over years, weighted by regions.

    The two answer different questions and can point opposite ways: South
    Africa maize is anti-skilled nationally (0.330) and the best in Africa
    spatially (0.667).
    """
    from sklearn.metrics import roc_auc_score

    out = {}
    lo = lo.dropna(subset=["ahat"])
    if lo.empty:
        return out

    ev, sc = [], []
    for fnid, y, ah in zip(lo["fnid"].to_numpy(), lo["year"].to_numpy(),
                           lo["ahat"].to_numpy()):
        t = edges.get((fnid, int(y)))
        if t is None or not np.isfinite(ah):
            continue
        ev.append(t[1])
        sc.append(-ah)
    if len(set(ev)) == 2:
        out["auc"] = round(float(roc_auc_score(ev, sc)), 3)

    nat = lo.groupby("year").agg(ahat=("ahat", "mean"), obs=("obs", "mean"),
                                 trend=("trend", "mean"))
    nat["anom"] = nat["obs"] / nat["trend"] - 1
    nev, nsc = [], []
    for y in nat.index:
        tr = nat["anom"].drop(index=y)
        if len(tr) < 9:
            continue
        e = _fold_bins(tr)
        nev.append(int(_to_class(nat.loc[y, "anom"], e) == 0))
        nsc.append(-nat.loc[y, "ahat"])
    if len(set(nev)) == 2:
        out["auc_national"] = round(float(roc_auc_score(nev, nsc)), 3)

    aucs, wts = [], []
    for y, gy in lo.groupby("year"):
        e2, s2 = [], []
        for fnid, ah in zip(gy["fnid"].to_numpy(), gy["ahat"].to_numpy()):
            t = edges.get((fnid, int(y)))
            if t is None or not np.isfinite(ah):
                continue
            e2.append(t[1])
            s2.append(-ah)
        if len(set(e2)) == 2 and len(e2) >= MIN_UNITS:
            aucs.append(roc_auc_score(e2, s2))
            wts.append(len(e2))
    if aucs:
        out["auc_spatial"] = round(float(np.average(aucs, weights=wts)), 3)
        out["n_spatial_years"] = int(len(aucs))
    return out


def per_region_skill(lo, anoms, edges):
    """AUC and R2 for EACH region over its own years.

    The national and spatial metrics never score a region on its own
    timeline: national averages the regions away, spatial compares regions
    WITHIN a year. A choropleth needs the per-region verdict, because every
    polygon makes its own claim.

    Noisy by construction — ~22 years with ~7 low-tercile events gives an
    AUC sampling sd near 0.14, and a pure-noise region clears ROC 0.6 about
    23% of the time — so ``region_n_years`` and ``region_n_low`` travel with
    the score. Regions too short to judge are marked ``insufficient``
    rather than called ``no_skill``, which would claim more than the record
    supports.
    """
    from sklearn.metrics import roc_auc_score

    out = {}
    d = lo.dropna(subset=["ahat"])
    for fnid, g in d.groupby("fnid"):
        ev, sc = [], []
        for y, ah in zip(g["year"].to_numpy(), g["ahat"].to_numpy()):
            t = edges.get((fnid, int(y)))
            if t is None or not np.isfinite(ah):
                continue
            ev.append(t[1])
            sc.append(-ah)
        rec = {"region_n_years": len(ev), "region_n_low": int(sum(ev))}
        if len(set(ev)) == 2:
            rec["region_auc"] = round(float(roc_auc_score(ev, sc)), 3)
        obs_a = g["obs"] / g["trend"] - 1
        sst = float(((obs_a - obs_a.mean()) ** 2).sum())
        if sst > 0:
            rec["region_r2"] = round(
                1 - float(((obs_a - g["ahat"]) ** 2).sum()) / sst, 3)
        # Two states only. A region with no computable AUC (no low year,
        # or no scorable fold) still cannot be called either way, so it
        # keeps a null verdict and the map leaves it unhatched rather
        # than asserting no-skill.
        if rec.get("region_auc") is None:
            rec["region_skill"] = None
        elif rec["region_auc"] > SKILL_ROC_THRESHOLD:
            rec["region_skill"] = "skill"
        else:
            rec["region_skill"] = "no_skill"
        out[fnid] = rec
    return out


def _r2(y, yhat):
    y, yhat = np.asarray(y, dtype=float), np.asarray(yhat, dtype=float)
    m = np.isfinite(y) & np.isfinite(yhat)
    y, yhat = y[m], yhat[m]
    if len(y) < 3:
        return None
    sst = float(((y - y.mean()) ** 2).sum())
    if sst <= 0:
        return None
    return 1.0 - float(((y - yhat) ** 2).sum()) / sst


def decomposed_r2(lo):
    """Regression skill on the anomaly scale, split the same three ways.

    The trend baseline predicts anom = 0 and observed anomalies average ~0,
    so **R2 > 0 is very nearly "beats trend"** and this agrees with
    ``beats_trend`` by construction.

    ``r2``           all unit-years, around the pooled mean
    ``r2_national``  year means only — can the model call the year's SIZE
    ``r2_within``    both series demeaned BY YEAR (the fixed-effects R2) —
                     can it call the spread across regions inside a year

    Discrimination and magnitude come apart: Somalia maize Deyr ranks years
    well (national AUC 0.776, p=0.007) but has national R2 ~ 0. It can say
    which years are bad, not how bad.

    The national split is NOISIER at small unit counts, but not biased. A
    purely spatial predictor scores a national R2 of ~0 on average at every
    unit count; what changes is the spread, because the year-mean of a
    spatial predictor is a sample mean. Measured over 10 seeds, the largest
    national R2 a spatial-only predictor reached was +0.33 at 5 units,
    +0.20 at 9, +0.07 at 45 and +0.04 at 200. So read a national score on
    few units (South Africa, 9 provinces) with wider error bars than one on
    many (Zambia, 71) — the permutation null already absorbs this, since it
    is computed per combination on that combination's own units.
    """
    d = lo.dropna(subset=["ahat"]).copy()
    if d.empty:
        return {}
    d["anom_obs"] = d["obs"] / d["trend"] - 1
    out = {}
    v = _r2(d["anom_obs"], d["ahat"])
    if v is not None:
        out["r2"] = round(v, 3)

    nat = d.groupby("year").agg(obs=("obs", "mean"), trend=("trend", "mean"),
                                ahat=("ahat", "mean"))
    v = _r2(nat["obs"] / nat["trend"] - 1, nat["ahat"])
    if v is not None:
        out["r2_national"] = round(v, 3)

    a = d["anom_obs"] - d.groupby("year")["anom_obs"].transform("mean")
    p = d["ahat"] - d.groupby("year")["ahat"].transform("mean")
    v = _r2(a, p)
    if v is not None:
        out["r2_within"] = round(v, 3)
    return out


def trend_extrapolation(obs, harvest_year, min_record=12):
    """How wrong is the trend level a t/ha forecast would rest on?

    The tercile product needs no absolute level — its edges come from the
    anomaly distribution. A yield number in t/ha does, and the HarvestStat
    records end anywhere from 2010 (Madagascar) to 2024, i.e. a 3 to 17 year
    extrapolation to 2027. Backtest it at the horizon actually required:
    hold out the last k years, fit the per-unit linear trend on the rest,
    and score the k-th year out.

    Across the 17 African combinations the median error is ~50% while the
    median climate signal the model applies is ~27%, so **the trend
    extrapolation dominates the error budget in 14 of 17** — which is why
    the pipeline publishes anomalies and terciles rather than t/ha.
    """
    k = int(harvest_year) - int(obs["year"].max())
    errs, rel = [], []
    for _, u in obs.groupby("fnid"):
        u = u.sort_values("year")
        if len(u) < min_record:
            continue
        yr = u["year"].to_numpy(dtype=float)
        v = u["obs"].to_numpy(dtype=float)
        kk = int(min(max(k, 1), len(u) // 2))
        if len(yr) - kk < 8:
            continue
        b, a = np.polyfit(yr[:-kk], v[:-kk], 1)
        pred = b * yr[-1] + a
        errs.append(abs(v[-1] - pred))
        if v[-1] > 0:
            rel.append(abs(v[-1] - pred) / v[-1])
    if not errs:
        return {"extrap_years": k, "extrap_units": 0}
    return {"extrap_years": k, "extrap_units": len(errs),
            "trend_extrap_err_tha": round(float(np.median(errs)), 3),
            "trend_extrap_err_pct": (round(100 * float(np.median(rel)), 1)
                                     if rel else None)}


def trend_level(obs, year, min_record=8):
    """{fnid: trend yield at ``year``}, from the unit's full linear record.

    This is the baseline a t/ha number rests on. It uses ALL of the unit's
    observations (unlike :func:`causal_trend_fnid`, which must hold out the
    scored year) because the forecast season has no observation to hold out.
    Extrapolation error is not measured here — :func:`trend_extrapolation`
    does that for the combination, and it is what decides whether the level
    is fit to publish.
    """
    out = {}
    for fnid, u in obs.groupby("fnid"):
        u = u.sort_values("year")
        if len(u) < min_record:
            continue
        b, a = np.polyfit(u["year"].to_numpy(dtype=float),
                          u["obs"].to_numpy(dtype=float), 1)
        lvl = float(b * int(year) + a)
        if lvl > 0:
            out[fnid] = lvl
    return out


def permutation_auc(train, feats, eval_years, anoms, edges, obs,
                    n_perm=N_PERM, seed=20260908):
    """Year-block permutation nulls for all three skill metrics.

    AUC 0.5 is the WRONG benchmark for this estimator. Leave-one-year-out
    with an intercept biases predictions upward in exactly the years the
    fold removed, so a model with no information scores BELOW 0.5: across
    the 17 African combinations the pooled null averages 0.445.

    Measured nulls confirm where that bias lives: **spatial 0.500**
    (0.494-0.506 across all 17), **national 0.417**, pooled in between at
    0.449. Within a single year there is no removed-year mean to shift, so
    the bias is entirely a between-year effect — which is also why the
    spatial metric can be read against 0.5 and the other two cannot.

    The permutation keeps year blocks intact — one year->year map applied to
    every unit at once — so the spatial covariance within a season and the
    serial structure of the target survive; only the correspondence between
    predictor year and yield year is destroyed.

    ``obs`` may be a float (the pooled AUC) or the dict from
    :func:`decomposed_auc`, in which case every metric present is tested.
    """
    if obs is None:
        return {}
    if not isinstance(obs, dict):
        obs = {"auc": obs}
    keys = [k for k in ("auc", "auc_national", "auc_spatial",
                        "r2", "r2_national", "r2_within")
            if k in obs and obs[k] is not None]
    if not keys:
        return {}

    rng = np.random.default_rng(seed)
    fcols = [c for c in set(feats) | {"DRYHEAT"} if c in train.columns]
    # The permutation must be scored on the SAME panel as the observed
    # statistic, or the p-value is not an exchangeability test. The panel is
    # unbalanced (units have different year spans), so a global year->year
    # map sends some rows to a (fnid, year) the unit never had; reindex
    # returns NaN and the row is deleted. Measured on a mildly unbalanced
    # panel that lost 15% of rows per draw, up to 26% in the worst, and it
    # biased p CONSERVATIVELY (mean perm_p 0.744 unbalanced vs 0.653
    # balanced against a nominal 0.5) — so it was under-declaring skill.
    #
    # Fix: restrict to the rectangular core — units holding the full year
    # span — and score the OBSERVED statistic on that same core. Nothing is
    # dropped mid-permutation, so every draw sees an identical panel.
    years = sorted(train.year.unique())
    spans = train.groupby("fnid")["year"].nunique()
    full = spans[spans == len(years)].index
    if len(full) >= MIN_UNITS:
        core = train[train.fnid.isin(full)].copy()
    else:
        # Too few complete units: trim the year span instead, keeping the
        # years held by the most units, then the units holding all of them.
        per_year = train.groupby("year")["fnid"].nunique()
        keep_y = per_year[per_year >= per_year.max()].index
        core = train[train.year.isin(keep_y)].copy()
        spans = core.groupby("fnid")["year"].nunique()
        core = core[core.fnid.isin(spans[spans == len(keep_y)].index)]
    if len(core) < 40:
        return {}
    core_years = [y for y in eval_years if y in set(core.year)]
    obs_core = {**decomposed_auc(loyo(core, feats, core_years), anoms, edges),
                **decomposed_r2(loyo(core, feats, core_years))}
    keys = [k for k in keys if obs_core.get(k) is not None]
    if not keys:
        return {}

    feat = core.set_index(["fnid", "year"])[fcols]
    years = sorted(core.year.unique())
    null = {k: [] for k in keys}
    dropped = 0
    for _ in range(int(n_perm)):
        perm = dict(zip(years, rng.permutation(years)))
        t = core.copy()
        idx = pd.MultiIndex.from_arrays(
            [t.fnid.to_numpy(), t.year.map(perm).to_numpy()])
        vals = feat.reindex(idx)
        for c in fcols:
            t[c] = vals[c].to_numpy()
        if t[fcols].isna().any().any():      # must not happen on the core
            dropped += 1
            continue
        eval_years_p = core_years
        # One permutation pass scores BOTH metric families — running the
        # classification and regression nulls separately would double the
        # cost for identical permutations.
        lo_p = loyo(t, feats, eval_years_p)
        s = {**decomposed_auc(lo_p, anoms, edges), **decomposed_r2(lo_p)}
        for k in keys:
            if s.get(k) is not None:
                null[k].append(s[k])

    # The pooled metric keeps its historical column names so existing
    # readers of null_auc / perm_p do not have to change.
    names = {"auc": ("null_auc", "perm_p"),
             "auc_national": ("null_auc_national", "perm_national_p"),
             "auc_spatial": ("null_auc_spatial", "perm_spatial_p"),
             "r2": ("null_r2", "perm_r2_p"),
             "r2_national": ("null_r2_national", "perm_r2_national_p"),
             "r2_within": ("null_r2_within", "perm_r2_within_p")}
    out = {}
    for k in keys:
        arr = np.array(null[k])
        if not len(arr):
            continue
        null_col, p_col = names[k]
        out[null_col] = round(float(arr.mean()), 3)
        # Compare against the observed statistic recomputed on the SAME
        # rectangular core the null was drawn on — not the full-panel value
        # in `obs`, which is what made the old p-values non-exchangeable.
        out[p_col] = round(float((arr >= obs_core[k]).mean()), 3)
        if k == "auc":
            out["null_auc_sd"] = round(float(arr.std()), 3)
            out["null_auc_p95"] = round(float(np.percentile(arr, 95)), 3)
            out["perm_core_rows"] = int(len(core))
            out["perm_core_units"] = int(core.fnid.nunique())
            out["perm_core_years"] = int(core.year.nunique())
            out["auc_core"] = round(float(obs_core["auc"]), 3)
            if dropped:
                out["perm_draws_dropped"] = int(dropped)
            out["n_perm"] = int(len(arr))
    return out


def class_probabilities(ahat, hist_anoms, residuals):
    """P(low/mid/high) for one unit from the model's own error spread."""
    if len(hist_anoms) < 9 or len(residuals) < 10:
        return None
    e = _fold_bins(hist_anoms)
    x = ahat + residuals
    return {"P_low": round(float((x < e[0]).mean()), 3),
            "P_mid": round(float(((x >= e[0]) & (x < e[-1])).mean()), 3),
            "P_high": round(float((x >= e[-1]).mean()), 3),
            "P_below_trend": round(float((x < 0).mean()), 3)}


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------
def config_list(parser, key, section="ML"):
    """A `["a", "b"]`-style config value as a list, or None when absent.

    geocif configs write lists as Python literals, so `ast.literal_eval` is
    the parser the rest of the codebase already uses. A bare comma string is
    accepted too, because that is what a hand-edited config usually holds.
    """
    if not parser.has_option(section, key):
        return None
    raw = parser.get(section, key).strip()
    if not raw:
        return None
    try:
        val = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        val = [p.strip() for p in raw.split(",")]
    if isinstance(val, str):
        val = [val]
    return [str(v).strip() for v in val if str(v).strip()] or None


def config_extent(parser, key="s2s_map_extent", section="ML"):
    """Map extent as `[lon_min, lon_max, lat_min, lat_max]`, or None.

    A malformed extent is refused rather than defaulted: a silently
    continent-wide map from a regional config would be read as "this region
    has no forecast anywhere else", which is the opposite of the truth.
    """
    vals = config_list(parser, key, section)
    if vals is None:
        return None
    if len(vals) != 4:
        raise ValueError(f"{key} needs 4 numbers "
                         f"(lon_min, lon_max, lat_min, lat_max), got {vals}")
    x0, x1, y0, y1 = (float(v) for v in vals)
    if x0 >= x1 or y0 >= y1:
        raise ValueError(f"{key} is not increasing: {[x0, x1, y0, y1]}")
    return [x0, x1, y0, y1]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def run(path_config_files=None, *, parser=None, logger_obj=None,
        threshold_dir="crop_t0", crops=("maize", "beans"), today=None,
        hvstat_csv=None, calendar_xlsx=None, countries=None,
        eval_years=None, out_dir=None, n_perm=N_PERM, figures=True,
        feature_set=None):
    """Enumerate, score and forecast every eligible HarvestStat combination."""
    if parser is None:
        from geocif import logger as log
        logger_obj, parser = log.setup_logger_parser(path_config_files)
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    root = Path(parser.get("PATHS", "dir_output")) / project
    meta = Path(parser.get("PATHS", "dir_metadata")) if parser.has_option(
        "PATHS", "dir_metadata") else root.parent / "inputs" / "metadata"
    hvstat_csv = hvstat_csv or (meta / "production_statistics"
                                / "hvstat_africa_data_v1.0.csv")
    calendar_xlsx = calendar_xlsx or (meta / "crop_calendars"
                                      / "EWCM_2026-01-05.xlsx")
    eval_years = eval_years or list(range(EVAL_SPAN[0], EVAL_SPAN[1] + 1))
    if feature_set is None:
        feature_set = parser.get("ML", "s2s_feature_set",
                                 fallback=DEFAULT_FEATURE_SET)
    # A regional config restricts the run to its own countries and crops
    # its own maps, so southern and eastern Africa are separate runs rather
    # than separate views of one. Keys are optional: absent means all Africa.
    if countries is None:
        countries = config_list(parser, "s2s_countries")
    region_label = parser.get("ML", "s2s_region_label", fallback="")
    map_extent = config_extent(parser)
    if feature_set not in FEATURE_SETS:
        raise ValueError(f"unknown feature_set {feature_set!r}; "
                         f"choose from {sorted(FEATURE_SETS)}")
    logger.info(f"feature set {feature_set!r}: "
                f"{FEATURE_SETS[feature_set]}")
    ts = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    suffix = "" if feature_set == DEFAULT_FEATURE_SET else f"_{feature_set}"
    if region_label:
        # Region goes in the directory name: two regional runs launched in
        # the same minute would otherwise land in the same timestamped dir.
        suffix += "_" + re.sub(r"\W+", "_", region_label.lower()).strip("_")
    out = Path(out_dir) if out_dir else (
        root / "ml" / "analysis" / ts / "explore" / f"s2s_africa{suffix}")
    out.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(hvstat_csv)
    products = [p for c in crops for p in CROP_PRODUCTS[c]]
    ylds = load_yields(hvstat_csv, products)
    if countries:
        ylds = ylds[ylds.country.isin(countries)]
    prod_to_crop = {p: c for c, ps in CROP_PRODUCTS.items() for p in ps}
    logger.info(f"yield rows: {len(ylds)} | countries: "
                f"{ylds.country.nunique()}"
                + (f" | region {region_label!r}" if region_label else "")
                + (f" | extent {map_extent}" if map_extent else ""))
    if countries:
        missing = sorted(set(countries) - set(ylds.country.unique()))
        if missing:
            # Silently dropping a misspelt country would look like "that
            # country has no forecastable season", which is a different story.
            logger.warning(f"s2s_countries not in the yield table: {missing}")

    combos, skills, forecasts, excluded = [], [], [], []
    s2s_cache = {}

    for (country, product, season_name), g in ylds.groupby(
            ["country", "product", "season_name"]):
        crop = prod_to_crop[product]
        rec = {"country": country, "crop": crop, "product": product,
               "season_name": season_name, "n_years": int(g.year.nunique()),
               "n_units": int(g.fnid.nunique()),
               "year_min": int(g.year.min()), "year_max": int(g.year.max())}

        # --- calendar ---
        cal = ewcm_calendar(calendar_xlsx, country, crop,
                            season_index(season_name))
        if cal is None:
            sub = raw[(raw.country == country) & (raw["product"] == product)
                      & (raw.season_name == season_name)]
            cal = hvstat_calendar(sub)
        if cal is None:
            rec.update(status="no_calendar", reason="no EWCM row and no "
                                                    "HarvestStat planting month")
            combos.append(rec)
            excluded.append(rec)
            continue
        rec.update(cal)

        # --- eligibility (extended-term only) ---
        st = window_state(cal["planting_month"], cal["wraps"], today=today)
        rec.update({k: st[k] for k in ("status", "planting", "harvest_year",
                                       "usable_from")})
        if st["status"] != "open":
            rec["reason"] = ("season already under way — in-season system owns it"
                             if st["status"] == "in_season"
                             else f"pre-season window opens {st['usable_from']}")
            combos.append(rec)
            excluded.append(rec)
            continue
        if rec["n_years"] < MIN_YEARS or rec["n_units"] < MIN_UNITS:
            rec["reason"] = (f"insufficient history "
                             f"({rec['n_years']} yrs, {rec['n_units']} units; "
                             f"need {MIN_YEARS}/{MIN_UNITS})")
            rec["status"] = "too_short"
            combos.append(rec)
            excluded.append(rec)
            continue

        # --- S2S ---
        slug = country_slug(country, root / threshold_dir)
        if slug is None:
            rec.update(status="no_s2s",
                       reason="no S2S directory found for country")
            combos.append(rec)
            excluded.append(rec)
            continue
        croot = root / threshold_dir / slug
        if slug not in s2s_cache:
            s2s_cache[slug] = (load_s2s_fnid(croot, "tprate"),
                               load_s2s_fnid(croot, "t2m"))
        tp, t2 = s2s_cache[slug]
        if tp.empty or t2.empty:
            rec.update(status="no_s2s", reason="no S2S extraction for country")
            combos.append(rec)
            excluded.append(rec)
            continue

        anoms = causal_trend_fnid(g[["fnid", "year", "obs"]])
        if anoms.empty:
            rec.update(status="no_trend", reason="no unit with >=8 years")
            combos.append(rec)
            excluded.append(rec)
            continue
        fnids = sorted(set(anoms.fnid) & set(tp.fnid))
        if len(fnids) < MIN_UNITS:
            rec.update(status="no_join",
                       reason=f"only {len(fnids)} fnids join S2S")
            combos.append(rec)
            excluded.append(rec)
            continue
        rec["n_joined"] = len(fnids)

        # --- hindcast across offsets ---
        hy = st["harvest_year"]
        best = None
        skill_by_offset = {}
        edges = edge_table(anoms)
        train_by_offset = {}
        for off in range(1, MAX_OFFSET + 1):
            fl = features_for_offset(off, feature_set)
            fx = build_features(tp, t2, cal["planting_month"], cal["wraps"],
                                off, sorted(anoms.year.unique()), fnids)
            if fx.empty:
                continue
            d = anoms.merge(fx, on=["fnid", "year"], how="inner")
            # Drop the climatology-fill era: see real_harvest_years.
            d = d[d.year.isin(real_harvest_years(
                cal["planting_month"], off, cal["wraps"],
                sorted(d.year.unique())))]
            if len(d) < 40:
                continue
            lo = loyo(d, fl, [y for y in eval_years if y in set(d.year)])
            if lo.empty:
                continue
            s = score_combo(lo, anoms, edges)
            train_by_offset[off] = d
            row = {**{k: rec[k] for k in ("country", "crop", "season_name")},
                   "offset": off, **s}
            skills.append(row)
            skill_by_offset[off] = s
            if s.get("auc") is not None and (
                    best is None or s["auc"] > best["skill"].get("auc", 0)):
                best = {"offset": off, "feats": fl, "data": d, "lo": lo,
                        "skill": s}
        if best is None:
            rec.update(status="no_hindcast",
                       reason="no offset produced a scorable hindcast")
            combos.append(rec)
            excluded.append(rec)
            continue

        # --- forecast the pending season with the freshest usable init ---
        fx_f = None
        for off in range(1, MAX_OFFSET + 1):
            cand = build_features(tp, t2, cal["planting_month"], cal["wraps"],
                                  off, [hy], fnids)
            if not cand.empty:
                fx_f, off_used = cand, off
                break
        if fx_f is None:
            rec.update(status="no_init",
                       reason="no published init covers the pending season")
            combos.append(rec)
            excluded.append(rec)
            continue

        fl = features_for_offset(off_used, feature_set)
        fx_h = build_features(tp, t2, cal["planting_month"], cal["wraps"],
                              off_used, sorted(anoms.year.unique()), fnids)
        train = anoms.merge(fx_h, on=["fnid", "year"], how="inner").dropna(
            subset=["anom"])
        # Drop the climatology-fill era before fitting: see
        # real_harvest_years. Left in, ~21% of these rows are one repeated
        # design point and they flatter every metric downstream.
        n_all = len(train)
        train = train[train.year.isin(real_harvest_years(
            cal["planting_month"], off_used, cal["wraps"],
            sorted(train.year.unique())))]
        rec["n_climfill_dropped"] = int(n_all - len(train))
        if len(train) < 40:
            rec.update(status="no_train",
                       reason=f"training pool too small ({len(train)})")
            combos.append(rec)
            excluded.append(rec)
            continue
        # Re-apply the history gate AFTER the join. MIN_YEARS was checked on
        # the raw HarvestStat record; the S2S join can cut it hard and the
        # row-count gate above does not notice, because units multiply.
        #
        # Gate on the SCORABLE years — the joined years that fall inside the
        # evaluation span and therefore produce LOYO folds — not on the size
        # of the training frame. Those differ: Kenya Short has enough
        # training years but only 8 inside 1995-2016, so its skill cannot be
        # measured (its national AUC is literally undefined, needing >=9
        # years to form a leave-one-out tercile) even though it trains fine.
        # Gating on train.year.nunique() let it through.
        n_train_years = int(train.year.nunique())
        scorable = sorted(set(train.year) & set(eval_years))
        rec["n_train_years"] = n_train_years
        rec["n_scorable_years"] = len(scorable)
        if min(n_train_years, len(scorable)) < MIN_YEARS:
            rec.update(status="too_short",
                       reason=f"{len(scorable)} scorable years and "
                              f"{n_train_years} training years survive the "
                              f"S2S join (need {MIN_YEARS} of each); "
                              f"{len(train)} unit-years over "
                              f"{train.fnid.nunique()} units")
            combos.append(rec)
            excluded.append(rec)
            continue
        res = fit_ols(train, fl)
        fxc, oos = clip_to_support(fx_f, train, fl)
        fxc["ahat"] = predict_ols(res, fxc, fl)

        lo_f = loyo(train, fl, [y for y in eval_years if y in set(train.year)])
        reg_skill = per_region_skill(lo_f, anoms, edges)
        resid = ((lo_f["obs"] / lo_f["trend"] - 1) - lo_f["ahat"]).dropna(
        ).to_numpy() if not lo_f.empty else np.array([])
        # Report the skill of the init the forecast was ACTUALLY issued from,
        # not the best-scoring one. The freshest usable init is often not the
        # most skilful: Kenya Short is issued at offset 2 (AUC 0.31, worse
        # than chance) while its best offset scores 0.49 — quoting the latter
        # beside the forecast overstated it.
        sk = dict(skill_by_offset.get(off_used) or {})
        skb = best["skill"]
        # Skill is decided against this combination's OWN permutation null,
        # not against 0.5 — see permutation_auc for why 0.5 is wrong here.
        if n_perm and sk.get("auc") is not None:
            sk.update(permutation_auc(
                train_by_offset.get(off_used, train), fl,
                [y for y in eval_years if y in set(train.year)], anoms, edges,
                sk, n_perm=n_perm))
        # Permutation test when it was run; otherwise Anderson's ROC bar.
        def _gate(p_key, auc_key):
            if sk.get(p_key) is not None:
                return bool(sk[p_key] < PERM_ALPHA)
            a = sk.get(auc_key)
            return bool(a is not None and a > SKILL_ROC_THRESHOLD)

        has_skill = _gate("perm_p", "auc")
        # The two abilities are reported separately because they can point
        # opposite ways: South Africa maize is anti-skilled nationally and
        # the best in Africa spatially.
        has_national_skill = _gate("perm_national_p", "auc_national")
        has_spatial_skill = _gate("perm_spatial_p", "auc_spatial")
        in_support = bool(oos["oos_max_sigma"].max() <= OOS_TOLERANCE)
        # A t/ha forecast needs a trend level for the pending season, and
        # these records end anywhere from 2010 to 2024. Measure the
        # extrapolation the level would rest on so the anomaly-only output
        # is a stated choice rather than an omission.
        tex = trend_extrapolation(g[["fnid", "year", "obs"]], hy)
        lvl = trend_level(g[["fnid", "year", "obs"]], hy)
        for _, r in fxc.iterrows():
            hist = anoms[anoms.fnid == r.fnid]["anom"]
            pr = class_probabilities(float(r["ahat"]), hist, resid)
            if pr is None:
                continue
            forecasts.append({
                "country": country, "crop": crop, "season_name": season_name,
                "harvest_year": hy, "fnid": r.fnid,
                "offset_used": off_used, "planting_month": cal["planting_month"],
                "calendar_source": cal["calendar_source"],
                "ahat": round(float(r["ahat"]), 3), **pr,
                "feature_set": feature_set,
                # skill AT THE ISSUED LEAD
                "skill_auc": sk.get("auc"), "skill_low_recall": sk.get("low_recall"),
                "skill_far": sk.get("far"), "skill_rrmse": sk.get("rrmse"),
                "skill_rrmse_trend": sk.get("rrmse_trend"),
                "beats_trend": sk.get("beats_trend"),
                # skill is AUC vs this combination's own permutation null
                "null_auc": sk.get("null_auc"), "perm_p": sk.get("perm_p"),
                "has_skill": has_skill,
                # THIS region judged on its own timeline — what the map
                # hatches on, since every polygon makes its own claim
                **reg_skill.get(r.fnid, {"region_skill": "insufficient"}),
                # ... split into the two questions it conflates
                "auc_national": sk.get("auc_national"),
                "null_auc_national": sk.get("null_auc_national"),
                "perm_national_p": sk.get("perm_national_p"),
                "has_national_skill": has_national_skill,
                "auc_spatial": sk.get("auc_spatial"),
                "null_auc_spatial": sk.get("null_auc_spatial"),
                "perm_spatial_p": sk.get("perm_spatial_p"),
                "has_spatial_skill": has_spatial_skill,
                "n_years": sk.get("n_years"),
                # regression skill: R2 > 0 on the anomaly scale is very
                # nearly "beats trend", and each has its own null
                "r2": sk.get("r2"), "null_r2": sk.get("null_r2"),
                "perm_r2_p": sk.get("perm_r2_p"),
                "r2_national": sk.get("r2_national"),
                "perm_r2_national_p": sk.get("perm_r2_national_p"),
                "r2_within": sk.get("r2_within"),
                "perm_r2_within_p": sk.get("perm_r2_within_p"),
                # the yield level and what it rests on. trend_extrap_err_pct
                # is the gate: above TREND_EXTRAP_MAX_PCT the t/ha number is
                # dominated by not knowing the baseline, not by the climate
                # signal, and must not be mapped.
                "trend_tha": (round(lvl[r.fnid], 3)
                              if r.fnid in lvl else None),
                "yhat_tha": (round(lvl[r.fnid] * (1 + float(r["ahat"])), 3)
                             if r.fnid in lvl else None),
                **{k: v for k, v in tex.items()},
                # how far outside the training range this unit's predictors
                # sat BEFORE clipping — a clipped prediction is a boundary
                # value, not a forecast, and must be readable as such
                "n_clipped": int(oos.loc[r.name, "n_clipped"]),
                "oos_max_sigma": round(float(oos.loc[r.name, "oos_max_sigma"]), 2),
                "oos_feature": oos.loc[r.name, "oos_feature"],
                "in_support": in_support,
                # best lead, kept separate so the two are never conflated
                "best_offset": best["offset"], "best_auc": skb.get("auc")})
        rec.update(status="forecast", offset_used=off_used,
                   feature_set=feature_set,
                   best_offset=best["offset"], best_auc=skb.get("auc"),
                   has_skill=has_skill, in_support=in_support,
                   has_national_skill=has_national_skill,
                   has_spatial_skill=has_spatial_skill, **tex,
                   clip_frac=round(float((oos["n_clipped"] > 0).mean()), 3),
                   oos_max_sigma=round(float(oos["oos_max_sigma"].max()), 2),
                   oos_feature=oos.loc[oos["oos_max_sigma"].idxmax(),
                                       "oos_feature"],
                   **{f"skill_{k}": v for k, v in sk.items()})
        combos.append(rec)
        oos_note = "" if in_support else (
            f"; OUT OF SUPPORT — {rec['oos_feature']} "
            f"{rec['oos_max_sigma']} sd beyond training range, "
            f"{100 * rec['clip_frac']:.0f}% of units clipped")
        logger.info(
            f"{country} {crop} {season_name}: forecast {len(fxc)} units "
            f"over {sk.get('n_years')} yrs (issued at offset {off_used}; "
            f"pooled AUC {sk.get('auc')} vs null {sk.get('null_auc')} "
            f"p={sk.get('perm_p')}"
            f"{'' if has_skill else ' — NO SKILL at this lead'}; "
            f"national {sk.get('auc_national')} vs {sk.get('null_auc_national')} "
            f"p={sk.get('perm_national_p')}; "
            f"spatial {sk.get('auc_spatial')} vs {sk.get('null_auc_spatial')} "
            f"p={sk.get('perm_spatial_p')}; "
            f"R2 {sk.get('r2')} nat {sk.get('r2_national')} "
            f"within {sk.get('r2_within')}; "
            f"trend extrapolated {tex.get('extrap_years')} yr "
            f"(+/-{tex.get('trend_extrap_err_pct')}%){oos_note})")

    cdf = pd.DataFrame(combos)
    cdf.to_csv(out / "combinations.csv", index=False)
    pd.DataFrame(skills).to_csv(out / "skill.csv", index=False)
    fdf = pd.DataFrame(forecasts)
    fdf.to_csv(out / "forecasts.csv", index=False)
    pd.DataFrame(excluded).to_csv(out / "excluded.csv", index=False)

    n_fc = int((cdf["status"] == "forecast").sum()) if not cdf.empty else 0
    logger.info(f"combinations: {len(cdf)} | forecast: {n_fc} | "
                f"units forecast: {len(fdf)} | outputs -> {out}")

    if figures and n_fc:
        # Imported here, not at module scope: viz.s2s_africa reads this
        # module's feature builders, and matplotlib/pygmt should not be a
        # hard dependency of running the analysis.
        from geocif import __version__
        from geocif.viz import s2s_africa as viz

        gpkg = meta / "boundary_files" / "adm_shapefile.gpkg"
        viz.render_all(out, root, hvstat_csv,
                       gpkg=gpkg if gpkg.exists() else None,
                       version=__version__, threshold_dir=threshold_dir,
                       extent=map_extent, label=region_label)
    return out
