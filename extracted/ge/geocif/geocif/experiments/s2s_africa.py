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
    """1 for a primary season, 2 for a secondary one, else 1."""
    if season_name in PRIMARY_SEASON_NAMES:
        return 1
    if season_name in SECONDARY_SEASON_NAMES:
        return 2
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


def features_for_offset(offset):
    """The feature list an init at ``offset`` can actually construct."""
    return FEATURES if offset <= 3 else [f for f in FEATURES if f != "z_P_GF"]


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
    a = anoms.dropna(subset=["anom"])
    for fnid, g in a.groupby("fnid"):
        v = g.set_index("year")["anom"]
        for y, val in v.items():
            tr = v.drop(index=y)
            if len(tr) < 9:
                continue
            e = _fold_bins(tr)
            tab[(fnid, int(y))] = (e, int(_to_class(val, e) == 0))
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
    return out


def permutation_auc(train, feats, eval_years, anoms, edges, obs_auc,
                    n_perm=N_PERM, seed=20260908):
    """Year-block permutation null for the classification AUC.

    AUC 0.5 is the WRONG benchmark for this estimator. Leave-one-year-out
    with an intercept biases predictions upward in exactly the years the
    fold removed, so a model with no information scores BELOW 0.5: across
    the 17 African combinations the null averages 0.445, not 0.500. Judging
    skill against 0.5 therefore mislabels combinations in both directions.

    The permutation keeps year blocks intact — one year->year map applied to
    every unit at once — so the spatial covariance within a season and the
    serial structure of the target survive; only the correspondence between
    predictor year and yield year is destroyed.
    """
    rng = np.random.default_rng(seed)
    fcols = [c for c in set(feats) | {"DRYHEAT"} if c in train.columns]
    feat = train.set_index(["fnid", "year"])[fcols]
    years = sorted(train.year.unique())
    null = []
    for _ in range(int(n_perm)):
        perm = dict(zip(years, rng.permutation(years)))
        t = train.copy()
        idx = pd.MultiIndex.from_arrays(
            [t.fnid.to_numpy(), t.year.map(perm).to_numpy()])
        vals = feat.reindex(idx)
        for c in fcols:
            t[c] = vals[c].to_numpy()
        t = t.dropna(subset=fcols)
        if len(t) < 40:
            continue
        s = score_combo(loyo(t, feats, eval_years), anoms, edges)
        if s.get("auc") is not None:
            null.append(s["auc"])
    if not null or obs_auc is None:
        return {}
    null = np.array(null)
    return {"null_auc": round(float(null.mean()), 3),
            "null_auc_sd": round(float(null.std()), 3),
            "null_auc_p95": round(float(np.percentile(null, 95)), 3),
            "perm_p": round(float((null >= obs_auc).mean()), 3),
            "n_perm": int(len(null))}


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
# main
# ---------------------------------------------------------------------------
def run(path_config_files=None, *, parser=None, logger_obj=None,
        threshold_dir="crop_t0", crops=("maize", "beans"), today=None,
        hvstat_csv=None, calendar_xlsx=None, countries=None,
        eval_years=None, out_dir=None, n_perm=N_PERM, figures=True):
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
    ts = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    out = Path(out_dir) if out_dir else (
        root / "ml" / "analysis" / ts / "explore" / "s2s_africa")
    out.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(hvstat_csv)
    products = [p for c in crops for p in CROP_PRODUCTS[c]]
    ylds = load_yields(hvstat_csv, products)
    if countries:
        ylds = ylds[ylds.country.isin(countries)]
    prod_to_crop = {p: c for c, ps in CROP_PRODUCTS.items() for p in ps}
    logger.info(f"yield rows: {len(ylds)} | countries: {ylds.country.nunique()}")

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
            fl = features_for_offset(off)
            fx = build_features(tp, t2, cal["planting_month"], cal["wraps"],
                                off, sorted(anoms.year.unique()), fnids)
            if fx.empty:
                continue
            d = anoms.merge(fx, on=["fnid", "year"], how="inner")
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

        fl = features_for_offset(off_used)
        fx_h = build_features(tp, t2, cal["planting_month"], cal["wraps"],
                              off_used, sorted(anoms.year.unique()), fnids)
        train = anoms.merge(fx_h, on=["fnid", "year"], how="inner").dropna(
            subset=["anom"])
        if len(train) < 40:
            rec.update(status="no_train",
                       reason=f"training pool too small ({len(train)})")
            combos.append(rec)
            excluded.append(rec)
            continue
        # Re-apply the history gate AFTER the join. MIN_YEARS was checked on
        # the raw HarvestStat record; the S2S join can cut it hard and the
        # row-count gate above does not notice, because units multiply. Kenya
        # Short passed on 189 rows spanning only 8 years — too few even to
        # form a leave-one-out national tercile, and the effective sample
        # size of a pooled AUC is years, not unit-years.
        n_train_years = int(train.year.nunique())
        rec["n_train_years"] = n_train_years
        if n_train_years < MIN_YEARS:
            rec.update(status="too_short",
                       reason=f"only {n_train_years} years survive the S2S "
                              f"join (need {MIN_YEARS}); "
                              f"{len(train)} unit-years over "
                              f"{train.fnid.nunique()} units")
            combos.append(rec)
            excluded.append(rec)
            continue
        res = fit_ols(train, fl)
        fxc, oos = clip_to_support(fx_f, train, fl)
        fxc["ahat"] = predict_ols(res, fxc, fl)

        lo_f = loyo(train, fl, [y for y in eval_years if y in set(train.year)])
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
                sk["auc"], n_perm=n_perm))
        has_skill = bool(sk.get("perm_p") is not None
                         and sk["perm_p"] < PERM_ALPHA)
        in_support = bool(oos["oos_max_sigma"].max() <= OOS_TOLERANCE)
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
                # skill AT THE ISSUED LEAD
                "skill_auc": sk.get("auc"), "skill_low_recall": sk.get("low_recall"),
                "skill_far": sk.get("far"), "skill_rrmse": sk.get("rrmse"),
                "skill_rrmse_trend": sk.get("rrmse_trend"),
                "beats_trend": sk.get("beats_trend"),
                # skill is AUC vs this combination's own permutation null
                "null_auc": sk.get("null_auc"), "perm_p": sk.get("perm_p"),
                "has_skill": has_skill,
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
                   best_offset=best["offset"], best_auc=skb.get("auc"),
                   has_skill=has_skill, in_support=in_support,
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
            f"(issued at offset {off_used}, AUC {sk.get('auc')} vs null "
            f"{sk.get('null_auc')}, p={sk.get('perm_p')}"
            f"{'' if has_skill else ' — NO SKILL at this lead'}; "
            f"best offset {best['offset']} AUC {skb.get('auc')}{oos_note})")

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
                       version=__version__, threshold_dir=threshold_dir)
    return out
