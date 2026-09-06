"""Simple literature-grounded S2S pre-season yield model (LOYO benchmark).

A transparent 4-predictor linear model in the spirit of the Kenya hybrid
anomaly model: the trend baseline supplies the level, a pooled OLS on
physically meaningful S2S forecast anomalies supplies the year-to-year
departure. Fitted and scored in the exact leave-one-year-out harness used by
the ML benchmarks (trend/null/catboost/cubist/tabpfn from the hindcast DB),
then applied to the forecast season.

Target
    a[r, y] = obs[r, y] / trend[r, y] - 1          (fractional anomaly)
    yhat    = trend * (1 + ahat)

Predictors (August init, leads 3-6 -> Nov..Feb, z-scored per region against
the real-hindcast climatology, harvests 1994-2017):
    z_PRCPTOT   season-total forecast precipitation      (ETCCDI PRCPTOT;
                Walker & Schulze 2008; Landman & Goddard 2002)
    z_TMEAN     season-mean forecast 2-m temperature     (Lobell et al. 2011;
                Schlenker & Lobell 2010)
    z_P_GF      grain-fill window (Jan-Feb) precipitation (Tadross et al.
                2005; du Plessis 2003)
    DRYHEAT     z_PRCPTOT x z_TMEAN interaction          (Lobell et al. 2011;
                Matiu et al. 2017)

Usage::

    from geocif.experiments import s2s_simple_model
    s2s_simple_model.run(cfg_geocif)                 # cfg = 4-file list

Outputs land under {dir_output}/{project}/ml/analysis/{ts}/explore/
s2s_simple_model/ — every figure has a companion CSV.
"""
import ast
import glob
import re
import sqlite3
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

import logging

logger = logging.getLogger(__name__)

# Init-month lead maps: lead k from init m targets calendar month (m+k-1)%12+1.
# Each init sees only the part of the Nov-Feb season within its 6 leads.
INIT_LEAD_MAPS = {
    6: {11: 5, 12: 6},                      # Jun: Nov-Dec only
    7: {11: 4, 12: 5, 1: 6},                # Jul: Nov-Jan
    8: {11: 3, 12: 4, 1: 5, 2: 6},          # Aug: full season
    9: {11: 2, 12: 3, 1: 4, 2: 5},          # Sep: full season
    10: {11: 1, 12: 2, 1: 3, 2: 4},         # Oct: full season
}
AUG_LEAD = INIT_LEAD_MAPS[8]
SEASON_MONTHS = [11, 12, 1, 2]
GRAINFILL_MONTHS = [1, 2]
# Harvest years whose August init is a real hindcast member (init 1993-2016)
REAL_HARVESTS = list(range(1994, 2018))
EVAL_YEARS = list(range(1995, 2017))       # LOYO evaluation window (real era)
CLIM_FILL_YEARS = list(range(2017, 2027))  # climatology-fill era (context only)
FEATURES = ["z_PRCPTOT", "z_TMEAN", "z_P_GF", "DRYHEAT"]
BAD_YEARS = [2016, 1999, 2015, 2001, 2007]


# ---------------------------------------------------------------------------
# S2S loading + feature construction
# ---------------------------------------------------------------------------
def load_s2s_dir(s2s_dir, var):
    """Read per-region NOAA-S2S CSVs for one variable into a long frame."""
    frames = []
    for f in glob.glob(str(Path(s2s_dir) / f"s2s_{var}" / "*.csv")):
        m = re.search(r"_([a-z_\-]+)_(\d{4})_s2s_", Path(f).name)
        if not m:
            continue
        d = pd.read_csv(f)
        d["region"] = m.group(1).replace("-", "_")
        d["init_year"] = int(m.group(2))
        frames.append(d)
    if not frames:
        raise FileNotFoundError(f"No s2s_{var} CSVs under {s2s_dir}")
    return pd.concat(frames, ignore_index=True)


def aug_init_values(df, var, harvest_year, region, init_month=8):
    """{target_month: value} from one init of harvest_year - 1."""
    lead_map = INIT_LEAD_MAPS[init_month]
    r = df[(df["region"] == region) & (df["init_year"] == harvest_year - 1)
           & (df["month"] == init_month)]
    if r.empty:
        return {}
    row = r.iloc[0]
    out = {}
    for tm, lead in lead_map.items():
        v = row.get(f"s2s_{var}_lead{lead}", np.nan)
        if np.isfinite(v):
            out[tm] = float(v)
    return out


def features_for_init(init_month):
    """Feature list for an init: z_P_GF exists only when Jan-Feb are visible."""
    vis = set(INIT_LEAD_MAPS[init_month])
    if all(m in vis for m in GRAINFILL_MONTHS):
        return list(FEATURES)
    return [f for f in FEATURES if f != "z_P_GF"]


def build_features(s2s_dir, regions, harvest_years, init_month=8, _cache={}):
    """Feature frame (region, year, z_PRCPTOT, z_TMEAN, z_P_GF, DRYHEAT).

    z-scores are computed per region against the REAL_HARVESTS climatology
    only — never against the years being predicted (the climatology is a
    fixed forecast-system reference, shared by every fold exactly as the
    published S2S anomaly products are).
    """
    key = str(s2s_dir)
    if key not in _cache:
        _cache.clear()
        _cache[key] = (load_s2s_dir(s2s_dir, "tprate"), load_s2s_dir(s2s_dir, "t2m"))
    tp, t2 = _cache[key]
    season = list(INIT_LEAD_MAPS[init_month])
    gf = [m for m in GRAINFILL_MONTHS if m in season]

    rows = []
    for region in regions:
        # raw seasonal aggregates per harvest year
        raw = {}
        for y in set(harvest_years) | set(REAL_HARVESTS):
            p = aug_init_values(tp, "tprate", y, region, init_month)
            t = aug_init_values(t2, "t2m", y, region, init_month)
            if len(p) < len(season) or len(t) < len(season):
                continue
            raw[y] = {
                "PRCPTOT": float(np.mean([p[m] for m in season])),
                "TMEAN": float(np.mean([t[m] for m in season])),
            }
            if gf:
                raw[y]["P_GF"] = float(np.mean([p[m] for m in gf]))
        ref = [raw[y] for y in REAL_HARVESTS if y in raw]
        if len(ref) < 10:
            logger.warning(f"{region}: only {len(ref)} climatology years — skipped")
            continue
        keys = ["PRCPTOT", "TMEAN"] + (["P_GF"] if gf else [])
        stats = {}
        for k in keys:
            arr = np.array([r[k] for r in ref])
            stats[k] = (float(arr.mean()), float(arr.std(ddof=1)))
        for y in harvest_years:
            if y not in raw:
                logger.warning(f"{region} {y}: incomplete init-{init_month} S2S — excluded")
                continue
            z = {f"z_{k}": (raw[y][k] - stats[k][0]) / stats[k][1] for k in keys}
            rows.append({"region": region, "year": y, **z,
                         "DRYHEAT": z["z_PRCPTOT"] * z["z_TMEAN"]})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# DB loading
# ---------------------------------------------------------------------------
def load_db_stage(db_path, table, stage_name="Pre-Season (init Aug)"):
    """Latest row per (Model, Region, Harvest Year) for one init stage."""
    con = sqlite3.connect(db_path)
    df = pd.read_sql(f'SELECT * FROM "{table}"', con)
    con.close()
    df = df[df["Stage Name"] == stage_name].copy()
    df["_ts"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str),
                               errors="coerce", format="mixed")
    df = df.sort_values("_ts").groupby(
        ["Model", "Region", "Harvest Year"], as_index=False).last()
    for c in ("Predicted Yield (tn per ha)", "Observed Yield (tn per ha)"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["Harvest Year"] = df["Harvest Year"].astype(int)
    df["region"] = (df["Region"].str.lower().str.replace(" ", "_")
                    .str.replace("-", "_"))
    return df


def anomaly_frame(db):
    """(region, year, obs, trend, anom) from the hindcast DB's trend model."""
    tr = db[db["Model"] == "trend"][
        ["region", "Harvest Year", "Predicted Yield (tn per ha)",
         "Observed Yield (tn per ha)"]].rename(
        columns={"Harvest Year": "year",
                 "Predicted Yield (tn per ha)": "trend",
                 "Observed Yield (tn per ha)": "obs"})
    tr = tr.dropna(subset=["trend"])
    tr["anom"] = tr["obs"] / tr["trend"] - 1
    return tr


# ---------------------------------------------------------------------------
# Fitting + LOYO
# ---------------------------------------------------------------------------
def fit_ols(train, feats):
    import statsmodels.api as sm

    X = sm.add_constant(train[feats].to_numpy(), has_constant="add")
    y = train["anom"].to_numpy()
    return sm.OLS(y, X).fit()


def predict_ols(res, df, feats):
    import statsmodels.api as sm

    X = sm.add_constant(df[feats].to_numpy(), has_constant="add")
    return res.predict(X)


def _fit_predict_ols(train, test, feats):
    res = fit_ols(train, feats)
    return predict_ols(res, test, feats)


def _fit_predict_gam(train, test, feats):
    """pyGAM: univariate splines on each feature (incl. the DRYHEAT column)."""
    from pygam import LinearGAM, s

    terms = s(0)
    for i in range(1, len(feats)):
        terms = terms + s(i)
    gam = LinearGAM(terms).gridsearch(
        train[feats].to_numpy(), train["anom"].to_numpy(), progress=False)
    return gam.predict(test[feats].to_numpy())


GAM_TE_FEATS = ["z_PRCPTOT", "z_TMEAN", "z_P_GF"]


def _fit_predict_gam_te(train, test, feats):
    """pyGAM with a tensor-product P x T surface instead of the hand-made
    DRYHEAT column — the GAM-native way to learn the interaction shape."""
    from pygam import LinearGAM, s, te

    f = GAM_TE_FEATS
    gam = LinearGAM(s(0) + s(1) + s(2) + te(0, 1)).gridsearch(
        train[f].to_numpy(), train["anom"].to_numpy(), progress=False)
    return gam.predict(test[f].to_numpy())


def _fit_predict_bass(train, test, feats):
    """pyBASS (Bayesian MARS) via the roster's sklearn-style wrapper."""
    from geocif.ml.trainers import BassRegressor

    np.random.seed(42)  # pyBASS draws from the global numpy RNG
    m = BassRegressor()
    m.fit(train[feats].to_numpy(), train["anom"].to_numpy())
    return m.predict(test[feats].to_numpy())


LEARNERS = {
    "ols": _fit_predict_ols,
    "gam": _fit_predict_gam,
    "gam_te": _fit_predict_gam_te,
    "bass": _fit_predict_bass,
}


def loyo(data, feats, years, learner="ols"):
    """Leave-one-year-out predictions over `years` (train never sees the fold
    year). Returns row-level frame with ahat and yhat."""
    fp = LEARNERS[learner]
    outs = []
    for y in years:
        train = data[(data["year"] != y) & data["anom"].notna()]
        test = data[data["year"] == y].copy()
        if test.empty or len(train) < 30:
            continue
        test["ahat"] = np.asarray(fp(train, test, feats), dtype=float)
        test["yhat"] = test["trend"] * (1 + test["ahat"])
        outs.append(test)
    return pd.concat(outs, ignore_index=True) if outs else pd.DataFrame()


# ---------------------------------------------------------------------------
# Scoring (same scorecard as the session benchmarks)
# ---------------------------------------------------------------------------
def _r2(o, p):
    sst = float(((o - o.mean()) ** 2).sum())
    return np.nan if sst == 0 else 1 - float(((o - p) ** 2).sum()) / sst


def score(df, pred_col="yhat", obs_col="obs", trend_col="trend"):
    # rows without an observation (e.g. Northern Cape 2010-2014) cannot be
    # scored; dropping them here keeps corrcoef/percentiles NaN-free
    df = df.dropna(subset=[obs_col, pred_col, trend_col])
    o, p = df[obs_col], df[pred_col]
    oa, pa = o - df[trend_col], p - df[trend_col]
    per_year = df.groupby("year").apply(
        lambda g: _r2(g[obs_col], g[pred_col]), include_groups=False)
    return {
        "pooled_R2": round(_r2(o, p), 3),
        "rRMSE_pct": round(100 * float(np.sqrt(((o - p) ** 2).mean())) / float(o.mean()), 2),
        "anom_r": round(float(np.corrcoef(oa, pa)[0, 1]), 3) if pa.std() > 0 else np.nan,
        "within_yr_R2_mean": round(float(per_year.mean()), 3),
        "n": int(len(df)),
    }


def drought_table(df, national=True):
    rows = []
    nat = df.groupby("year")[["obs", "trend", "yhat"]].mean()
    for y in BAD_YEARS:
        if y not in nat.index:
            continue
        r = nat.loc[y]
        denom = r["trend"] - r["obs"]
        rows.append({
            "year": y,
            "obs": round(r["obs"], 2), "trend": round(r["trend"], 2),
            "pred": round(r["yhat"], 2),
            "short_pct": round(100 * (r["obs"] / r["trend"] - 1), 1),
            "below_trend_call": bool(r["yhat"] < 0.95 * r["trend"]),
            "capture_pct": round(100 * (r["trend"] - r["yhat"]) / denom, 0)
            if abs(denom) > 1e-9 else np.nan,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Classification view: per-region tercile classes on ONE shared label set
# ---------------------------------------------------------------------------
def _fold_bins(obs_train):
    """Tercile edges from training-year observed yields (qcut convention)."""
    _, edges = pd.qcut(obs_train, q=3, retbins=True, duplicates="drop")
    return edges[1:-1]  # inner edges


def _to_class(values, inner_edges):
    return np.digitize(np.asarray(values, dtype=float), inner_edges)


def classification_eval(data, pred_sources, years, native=True,
                        label_mode="tercile_raw"):
    """Score every prediction source on identical per-fold tercile labels.

    pred_sources: {name: frame with region, year, yhat} (regression scale).
    For each fold year y and region r, class bins come from all OTHER years
    for r; the fold's observed and predicted values are digitized with those
    bins. Includes a persistence baseline (last year's observed class) and a
    native multinomial logistic on FEATURES.

    label_mode:
        "tercile_raw"  — bins on raw observed yields (matches geocif's native
            CLASSIFICATION mode, but the bins inherit the trend: early years
            are automatically "low", and the trend baseline wins the task by
            construction).
        "tercile_anom" — bins on DETRENDED fractional anomalies
            (obs/trend - 1); predictions are detrended identically
            (pred/trend - 1). This is the climate-signal classification.
    """
    obs = data.dropna(subset=["obs"])[["region", "year", "obs"]].copy()
    if label_mode == "tercile_anom":
        tr = data.dropna(subset=["obs", "trend"])[["region", "year", "obs", "trend"]]
        obs = tr[["region", "year"]].copy()
        obs["obs"] = tr["obs"] / tr["trend"] - 1
        trend_lut = tr.set_index(["region", "year"])["trend"]
        new_sources = {}
        for name, pf in pred_sources.items():
            pf = pf.copy()
            idx = pd.MultiIndex.from_frame(pf[["region", "year"]])
            t = trend_lut.reindex(idx).to_numpy()
            pf["yhat"] = pf["yhat"].to_numpy() / t - 1
            new_sources[name] = pf.dropna(subset=["yhat"])
        pred_sources = new_sources
    rows = []

    def _score_rows(recs, name):
        rec = pd.DataFrame(recs)
        if rec.empty:
            return
        acc = float((rec.pred_c == rec.obs_c).mean())
        low = rec[rec.obs_c == 0]
        rec0 = float((low.pred_c == 0).mean()) if len(low) else np.nan
        calls = rec[rec.pred_c == 0]
        prec0 = float((calls.obs_c == 0).mean()) if len(calls) else np.nan
        rows.append({"model": name, "acc": round(acc, 3),
                     "low_recall": round(rec0, 3),
                     "low_precision": round(prec0, 3), "n": len(rec)})

    # regression-then-classify for every prediction source
    for name, pf in pred_sources.items():
        recs = []
        for (r, y), g in pf.groupby(["region", "year"]):
            if y not in years:
                continue
            tr_obs = obs[(obs.region == r) & (obs.year != y)]["obs"]
            te_obs = obs[(obs.region == r) & (obs.year == y)]["obs"]
            if len(tr_obs) < 9 or te_obs.empty:
                continue
            edges = _fold_bins(tr_obs)
            recs.append({"obs_c": int(_to_class(te_obs.iloc[0], edges)),
                         "pred_c": int(_to_class(g["yhat"].iloc[0], edges))})
        _score_rows(recs, name)

    # persistence baseline: last year's observed class
    recs = []
    for (r, y), g in obs.groupby(["region", "year"]):
        if y not in years:
            continue
        prev = obs[(obs.region == r) & (obs.year == y - 1)]["obs"]
        tr_obs = obs[(obs.region == r) & (obs.year != y)]["obs"]
        if prev.empty or len(tr_obs) < 9:
            continue
        edges = _fold_bins(tr_obs)
        recs.append({"obs_c": int(_to_class(g["obs"].iloc[0], edges)),
                     "pred_c": int(_to_class(prev.iloc[0], edges))})
    _score_rows(recs, "persistence_class")

    # native multinomial logistic on the same features, LOYO
    if not native:
        return pd.DataFrame(rows)
    from sklearn.linear_model import LogisticRegression
    feats = [f for f in FEATURES if f in data.columns]
    recs = []
    d = data.dropna(subset=["obs"] + feats)
    for y in years:
        train = d[d.year != y]
        test = d[d.year == y]
        if test.empty:
            continue
        ytr, yte = [], []
        ok_tr, ok_te = [], []
        for idx, row in train.iterrows():
            tr_obs = d[(d.region == row.region) & (d.year != y)
                       & (d.index != idx)]["obs"]
            if len(tr_obs) < 9:
                continue
            ytr.append(int(_to_class(row.obs, _fold_bins(tr_obs))))
            ok_tr.append(idx)
        for idx, row in test.iterrows():
            tr_obs = d[(d.region == row.region) & (d.year != y)]["obs"]
            if len(tr_obs) < 9:
                continue
            ok_te.append(idx)
            yte.append(int(_to_class(row.obs, _fold_bins(tr_obs))))
        if not ok_te:
            continue
        clf = LogisticRegression(max_iter=2000)
        clf.fit(train.loc[ok_tr, feats].to_numpy(), ytr)
        pc = clf.predict(test.loc[ok_te, feats].to_numpy())
        recs += [{"obs_c": o, "pred_c": int(p)} for o, p in zip(yte, pc)]
    _score_rows(recs, "logistic_native")

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def run(path_config_files=None, *, parser=None, logger_obj=None,
        hindcast_db=None, forecast_db=None, s2s_dir=None,
        country="south_africa", crop="maize"):
    """Fit + LOYO-score the simple S2S model and forecast the pending season.

    Args:
        path_config_files: standard 4-file cfg list (geobase, countries,
            crops, geocif). Unused if ``parser`` is given.
        parser: pre-built ConfigParser (optional).
        hindcast_db / forecast_db: db filenames or full paths; default to
            ``sa_maize_hindcast_s2s_full.db`` / ``sa_maize_2027_preseason.db``
            under {dir_output}/{project}/ml/db.
        s2s_dir: root holding ``s2s_t2m``/``s2s_tprate`` per-region CSV dirs;
            default {dir_output}/{project}/crop_t0/{country}/{admin}/cr.
    """
    import os

    if parser is None:
        from geocif import logger as log
        if path_config_files is None:
            path_config_files = [Path("../config/geocif.txt")]
        logger_obj, parser = log.setup_logger_parser(path_config_files)

    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project
    admin = parser.get(country, "admin_level", fallback="admin_1")

    def _db(name, default):
        name = name or default
        return Path(name) if os.sep in str(name) else dir_output / "ml" / "db" / name

    hind_path = _db(hindcast_db, "sa_maize_hindcast_s2s_full.db")
    fcst_path = _db(forecast_db, "sa_maize_2027_preseason.db")
    s2s_root = Path(s2s_dir) if s2s_dir else (
        dir_output / "crop_t0" / country / admin / "cr")

    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    out = dir_output / "ml" / "analysis" / today / "explore" / "s2s_simple_model"
    out.mkdir(parents=True, exist_ok=True)
    table = f"{country}_{crop}"

    # ---- assemble data ----
    hdb = load_db_stage(hind_path, table)
    anoms = anomaly_frame(hdb)
    regions = sorted(anoms["region"].unique())
    feats_hist = build_features(s2s_root, regions,
                                sorted(anoms["year"].unique()))
    data = anoms.merge(feats_hist, on=["region", "year"], how="inner")
    logger.info(f"assembled {len(data)} region-years over {data['year'].min()}"
                f"-{data['year'].max()} for {len(regions)} regions")

    # ---- full-fit coefficients (real era, reporting only) ----
    train_real = data[data["year"].isin(EVAL_YEARS) & data["anom"].notna()]
    res = fit_ols(train_real, FEATURES)
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    import statsmodels.api as sm
    Xv = sm.add_constant(train_real[FEATURES].to_numpy())
    coefs = pd.DataFrame({
        "term": ["const"] + FEATURES,
        "beta": np.round(res.params, 4),
        "se_HC3": np.round(res.HC3_se, 4),
        "p_HC3": np.round(2 * (1 - __import__("scipy").stats.t.cdf(
            np.abs(res.params / res.HC3_se), res.df_resid)), 4),
        "vif": [np.nan] + [round(variance_inflation_factor(Xv, i), 2)
                           for i in range(1, Xv.shape[1])],
    })
    coefs.to_csv(out / "coefficients.csv", index=False)

    # ---- LOYO: this model + ablations ----
    ablation_sets = [
        ("P", ["z_PRCPTOT"]),
        ("P+T", ["z_PRCPTOT", "z_TMEAN"]),
        ("P+T+GF", ["z_PRCPTOT", "z_TMEAN", "z_P_GF"]),
        ("P+T+GF+DRYHEAT", FEATURES),
    ]
    ab_rows, loyo_full = [], None
    for name, feats in ablation_sets:
        lo = loyo(data, feats, EVAL_YEARS)
        s = score(lo)
        ab_rows.append({"model": name, **s})
        if feats == FEATURES:
            loyo_full = lo
    ablation = pd.DataFrame(ab_rows)
    ablation.to_csv(out / "ablation.csv", index=False)
    loyo_full.to_csv(out / "loyo_rowlevel.csv", index=False)

    # climatology-fill era, context only
    lo_fill = loyo(data, FEATURES, [y for y in CLIM_FILL_YEARS
                                    if y in set(data["year"])])
    fill_score = score(lo_fill) if not lo_fill.empty else {}

    # ---- benchmarks from the same DB, same rows ----
    keys = loyo_full[["region", "year"]]
    bench_rows = [{"model": "s2s_linear", **score(loyo_full)}]
    for m in ("trend", "null", "catboost", "cubist", "tabpfn"):
        bm = hdb[hdb["Model"] == m][["region", "Harvest Year",
                                     "Predicted Yield (tn per ha)"]].rename(
            columns={"Harvest Year": "year",
                     "Predicted Yield (tn per ha)": "yhat"})
        j = loyo_full[["region", "year", "obs", "trend"]].merge(
            bm, on=["region", "year"], how="inner")
        if not j.empty:
            bench_rows.append({"model": m, **score(j)})
    # ---- alternative learners on the SAME features + harness ----
    learner_loyo = {"ols": loyo_full}
    for lrn in ("gam", "gam_te", "bass"):
        try:
            lo = loyo(data, FEATURES, EVAL_YEARS, learner=lrn)
            learner_loyo[lrn] = lo
            bench_rows.append({"model": f"s2s_{lrn}", **score(lo)})
        except Exception as e:
            logger.warning(f"learner {lrn} failed: {e}")
    bench = pd.DataFrame(bench_rows)
    bench.to_csv(out / "skill_vs_benchmarks.csv", index=False)

    # ---- classification view (shared tercile labels) ----
    pred_sources = {f"s2s_{k}" if k != "ols" else "s2s_linear":
                    v[["region", "year", "yhat"]] for k, v in learner_loyo.items()}
    for m in ("trend", "catboost", "cubist", "tabpfn"):
        bm = hdb[hdb["Model"] == m][["region", "Harvest Year",
                                     "Predicted Yield (tn per ha)"]].rename(
            columns={"Harvest Year": "year",
                     "Predicted Yield (tn per ha)": "yhat"})
        pred_sources[m] = bm
    cls = classification_eval(data, pred_sources, EVAL_YEARS)
    cls.to_csv(out / "classification.csv", index=False)

    dr_frames = []
    for lrn, lo in learner_loyo.items():
        d = drought_table(lo)
        d.insert(0, "learner", lrn)
        dr_frames.append(d)
    dr_all = pd.concat(dr_frames, ignore_index=True)
    dr_all.to_csv(out / "drought_years.csv", index=False)
    dr = dr_all[dr_all["learner"] == "ols"].drop(columns=["learner"])

    # ---- 2027 (or pending-season) forecast ----
    fdb = load_db_stage(fcst_path, table)
    fyear = int(fdb["Harvest Year"].max())
    ftr = fdb[fdb["Model"] == "trend"][["region", "Predicted Yield (tn per ha)"]]
    ftr = ftr.rename(columns={"Predicted Yield (tn per ha)": "trend"})
    f27 = build_features(s2s_root, regions, [fyear])
    f27 = f27.merge(ftr, on="region", how="inner")
    res_all = fit_ols(data[data["anom"].notna() &
                           data["year"].isin(REAL_HARVESTS)], FEATURES)
    # A linear model must not be extrapolated far beyond its training
    # support: the pending season's DRYHEAT (z_P x z_T) can sit several units
    # outside anything the OLS ever saw (record-warm forecasts vs a 1994-2017
    # base). Clip every feature to the pooled training min/max and report the
    # unclipped prediction as a sensitivity column.
    support = {f: (float(train_real[f].min()), float(train_real[f].max()))
               for f in FEATURES}
    f27["ahat_raw"] = predict_ols(res_all, f27, FEATURES)
    f27_c = f27.copy()
    for f in ("z_PRCPTOT", "z_TMEAN", "z_P_GF"):
        f27_c[f] = f27_c[f].clip(*support[f])
    f27_c["DRYHEAT"] = (f27_c["z_PRCPTOT"] * f27_c["z_TMEAN"]).clip(*support["DRYHEAT"])
    f27["was_clipped"] = (f27[FEATURES].to_numpy()
                          != f27_c[FEATURES].to_numpy()).any(axis=1)
    f27[[f + "_clip" for f in FEATURES]] = f27_c[FEATURES].to_numpy()
    f27["ahat"] = predict_ols(res_all, f27_c, FEATURES)
    f27["yhat"] = f27["trend"] * (1 + f27["ahat"])
    f27["yhat_raw"] = f27["trend"] * (1 + f27["ahat_raw"])
    # empirical 80% interval from LOYO fractional residuals (pooled, NaN-safe)
    lf = loyo_full.dropna(subset=["obs", "trend", "ahat"])
    resid = (lf["obs"] / lf["trend"] - 1) - lf["ahat"]
    q10, q90 = np.percentile(resid, [10, 90])
    f27["lo80"] = f27["trend"] * (1 + f27["ahat"] + q10)
    f27["hi80"] = f27["trend"] * (1 + f27["ahat"] + q90)
    train_full = data[data["anom"].notna() & data["year"].isin(REAL_HARVESTS)]
    for lrn in ("gam", "gam_te", "bass"):
        if lrn not in learner_loyo:
            continue
        try:
            ah = np.asarray(LEARNERS[lrn](train_full, f27_c, FEATURES), dtype=float)
            f27[f"yhat_{lrn}"] = f27["trend"] * (1 + ah)
        except Exception as e:
            logger.warning(f"2027 prediction with {lrn} failed: {e}")
    f27 = f27.sort_values("region")
    f27.round(3).to_csv(out / f"predictions_{fyear}.csv", index=False)

    # ---- figures (each with companion CSV already written above) ----
    _figures(out, loyo_full, bench, dr)

    # ---- month-by-month skill (OLS learner, per-init window + climatology) ----
    stage_names = {6: "Pre-Season (init Jun)", 7: "Pre-Season (init Jul)",
                   8: "Pre-Season (init Aug)", 9: "Pre-Season (init Sep)",
                   10: "Pre-Season (init Oct)"}
    monthly_rows = []
    for im in (6, 7, 8, 9, 10):
        feats_im = features_for_init(im)
        fx = build_features(s2s_root, regions, sorted(anoms["year"].unique()),
                            init_month=im)
        dm = anoms.merge(fx, on=["region", "year"], how="inner")
        if dm.empty:
            continue
        lo = loyo(dm, feats_im, EVAL_YEARS)
        s = score(lo)
        cl = classification_eval(dm, {"m": lo[["region", "year", "yhat"]]},
                                 EVAL_YEARS, native=False)
        crow = cl[cl["model"] == "m"].iloc[0] if not cl.empty else {}
        monthly_rows.append({
            "init": stage_names[im].split("init ")[1].rstrip(")"),
            "features": "+".join(f.replace("z_", "") for f in feats_im),
            **s,
            "class_acc": crow.get("acc", np.nan),
            "class_low_recall": crow.get("low_recall", np.nan),
        })
    monthly = pd.DataFrame(monthly_rows)
    monthly.to_csv(out / "monthly_skill.csv", index=False)

    # ---- README verdict ----
    s_own = bench.loc[bench["model"] == "s2s_linear"].iloc[0]
    s_tr = bench.loc[bench["model"] == "trend"].iloc[0]
    n_clip = int(f27["was_clipped"].sum())
    verdict = (f"s2s_linear LOYO {EVAL_YEARS[0]}-{EVAL_YEARS[-1]}: rRMSE "
               f"{s_own['rRMSE_pct']}% vs trend {s_tr['rRMSE_pct']}%, anomaly-r "
               f"{s_own['anom_r']}. {fyear} national mean "
               f"{f27['yhat'].mean():.2f} t/ha "
               f"({100 * (f27['yhat'] / f27['trend'] - 1).mean():+.1f}% vs trend; "
               f"{n_clip}/{len(f27)} provinces clipped to training support, "
               f"unclipped sensitivity "
               f"{100 * (f27['yhat_raw'] / f27['trend'] - 1).mean():+.1f}%).")
    (out / "README.md").write_text(
        f"# s2s_simple_model\n\n{verdict}\n\nClimatology-fill era (context "
        f"only): {fill_score}\n\nConstruction: Aug init, leads 3-6 -> Nov-Feb; "
        f"z per region vs real-hindcast climatology (harvests 1994-2017); "
        f"target = fractional anomaly vs the trend baseline; pooled OLS; "
        f"LOYO over {EVAL_YEARS[0]}-{EVAL_YEARS[-1]}.\n", encoding="utf-8")
    logger.info(verdict)
    logger.info(f"outputs -> {out}")
    return out


def _figures(out, loyo_full, bench, dr):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def style_ctx():
        try:
            import scienceplots  # noqa: F401
            return plt.style.context(["science", "no-latex"])
        except Exception:
            return plt.style.context("default")

    # 1. obs vs pred anomaly scatter (pooled LOYO)
    with style_ctx():
        fig, axx = plt.subplots(figsize=(4.4, 4.2))
        oa = 100 * (loyo_full["obs"] / loyo_full["trend"] - 1)
        pa = 100 * loyo_full["ahat"]
        axx.scatter(pa, oa, s=14, alpha=0.65, edgecolors="none")
        lim = max(abs(pd.concat([oa, pa]))) * 1.08
        axx.plot([-lim, lim], [-lim, lim], lw=0.8, color="0.5", ls="--")
        axx.axhline(0, lw=0.6, color="0.75")
        axx.axvline(0, lw=0.6, color="0.75")
        axx.set_xlabel("Predicted anomaly vs trend (%)")
        axx.set_ylabel("Observed anomaly vs trend (%)")
        axx.set_title("s2s_linear, LOYO region-years", loc="left")
        for s in ("top", "right"):
            axx.spines[s].set_visible(False)
        fig.savefig(out / "anomaly_scatter.png", dpi=300, bbox_inches="tight")
        fig.savefig(out / "anomaly_scatter.pdf", bbox_inches="tight")
        plt.close(fig)
    pd.DataFrame({"pred_anom_pct": pa, "obs_anom_pct": oa,
                  "region": loyo_full["region"], "year": loyo_full["year"]}
                 ).to_csv(out / "anomaly_scatter.csv", index=False)

    # 2. skill vs benchmarks
    with style_ctx():
        fig, axx = plt.subplots(figsize=(5.4, 3.2))
        b = bench.sort_values("rRMSE_pct")
        axx.barh(b["model"], b["rRMSE_pct"], height=0.62)
        axx.set_xlabel("rRMSE (%) — LOYO, real-S2S era")
        axx.set_title("Pre-season skill, August init", loc="left")
        for s in ("top", "right"):
            axx.spines[s].set_visible(False)
        fig.savefig(out / "skill_vs_benchmarks.png", dpi=300, bbox_inches="tight")
        fig.savefig(out / "skill_vs_benchmarks.pdf", bbox_inches="tight")
        plt.close(fig)

    # 3. drought-year capture
    with style_ctx():
        fig, axx = plt.subplots(figsize=(5.4, 3.2))
        x = np.arange(len(dr))
        w = 0.27
        axx.bar(x - w, dr["obs"], width=w, label="observed")
        axx.bar(x, dr["trend"], width=w, label="trend")
        axx.bar(x + w, dr["pred"], width=w, label="s2s_linear")
        axx.set_xticks(x, dr["year"].astype(str))
        axx.set_ylabel("National yield (t/ha)")
        axx.set_title("Major shortfall years", loc="left")
        axx.legend(frameon=False, fontsize=8)
        for s in ("top", "right"):
            axx.spines[s].set_visible(False)
        fig.savefig(out / "drought_years.png", dpi=300, bbox_inches="tight")
        fig.savefig(out / "drought_years.pdf", bbox_inches="tight")
        plt.close(fig)
