"""Phenology-aligned multi-country pooling for the simple S2S model.

Pools training rows ACROSS countries at the same offset-before-planting, so
South Africa's August init (planting Nov) aligns with Kenya's November init
(planting Mar): every pooled row describes "the S2S view k months before
planting", z-scored per region against that region's own real-hindcast
climatology. Anomalies are fractional vs an in-experiment leave-one-year-out
linear trend, computed identically for every country.

Pooling experiments per target country (classification-first):
    own          target country only (the baseline)
    +<c>         target + one candidate country
    all          every candidate pooled
    transfer     every candidate EXCEPT the target (cross-border test)

Leakage control: LOYO folds drop the fold YEAR from every country -- ENSO
years are shared across southern Africa, so per-country exclusion would leak.

Outputs (dated tree .../explore/s2s_pooled_model/): eligibility.csv,
pooling_experiments.csv, predictions_nextseason.csv (+ class probabilities),
README.md; every table is CSV.
"""
import glob
import re
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

import logging

from geocif.experiments.s2s_simple_model import (
    FEATURES, _fold_bins, _to_class, fit_ols, load_s2s_dir, predict_ols)
from geocif.experiments import s2s_eligibility as elig

logger = logging.getLogger(__name__)

MAX_OFFSET = 4          # offsets (months before planting) 1..4; 4 has no GF
SEASON_LEN = 4          # season aggregate = planting .. planting+3
REAL_INIT_YEARS = (1993, 2016)   # NOAA S2S hindcast members
N_BOOT = 500


# ---------------------------------------------------------------------------
# per-country data assembly
# ---------------------------------------------------------------------------
def season_months(planting):
    return [(planting - 1 + i) % 12 + 1 for i in range(SEASON_LEN)]


def lead_map(planting, offset):
    """{target_month: lead} for the init issued `offset` months pre-planting."""
    out = {}
    for i, tm in enumerate(season_months(planting)):
        lead = offset + i
        if lead <= 6:
            out[tm] = lead
    return out


def init_calendar(planting, offset, harvest_year, wraps):
    """(init_year, init_month) for a given harvest year."""
    plant_year = harvest_year - 1 if wraps else harvest_year
    im = planting - offset
    iy = plant_year
    if im <= 0:
        im += 12
        iy -= 1
    return iy, im


_S2S_CACHE = {}


def _load_cached(s2s_dir, var):
    key = (str(s2s_dir), var)
    if key not in _S2S_CACHE:
        _S2S_CACHE[key] = load_s2s_dir(s2s_dir, var)
    return _S2S_CACHE[key]


def country_features(s2s_dir, planting, wraps, offset, years):
    """(region, year, z_PRCPTOT, z_TMEAN[, z_P_GF], DRYHEAT) for one offset."""
    lm = lead_map(planting, offset)
    smon = list(lm)
    gf = [m for m in season_months(planting)[2:4] if m in lm]
    tp = _load_cached(s2s_dir, "tprate")
    t2 = _load_cached(s2s_dir, "t2m")
    real_harvests = [y for y in range(REAL_INIT_YEARS[0] + 1, REAL_INIT_YEARS[1] + 2)]

    rows = []
    for region in sorted(tp["region"].unique()):
        raw = {}
        for y in sorted(set(years) | set(real_harvests)):
            iy, im = init_calendar(planting, offset, y, wraps)
            def vals(df, var):
                r = df[(df.region == region) & (df.init_year == iy)
                       & (df.month == im)]
                if r.empty:
                    return {}
                row = r.iloc[0]
                return {tm: float(row[f"s2s_{var}_lead{l}"])
                        for tm, l in lm.items()
                        if np.isfinite(row.get(f"s2s_{var}_lead{l}", np.nan))}
            p, t = vals(tp, "tprate"), vals(t2, "t2m")
            if len(p) < len(smon) or len(t) < len(smon):
                continue
            raw[y] = {"PRCPTOT": float(np.mean([p[m] for m in smon])),
                      "TMEAN": float(np.mean([t[m] for m in smon]))}
            if gf:
                raw[y]["P_GF"] = float(np.mean([p[m] for m in gf]))
        ref = [raw[y] for y in real_harvests if y in raw]
        if len(ref) < 10:
            continue
        keys = ["PRCPTOT", "TMEAN"] + (["P_GF"] if gf else [])
        st = {k: (float(np.mean([r[k] for r in ref])),
                  float(np.std([r[k] for r in ref], ddof=1))) for k in keys}
        for y, v in raw.items():
            if y not in years:
                continue
            z = {f"z_{k}": (v[k] - st[k][0]) / st[k][1] for k in keys}
            rows.append({"region": region, "year": int(y), **z,
                         "DRYHEAT": z["z_PRCPTOT"] * z["z_TMEAN"]})
    return pd.DataFrame(rows)


def pick_s2s_dir(country_root, yield_regions):
    """Best-matching s2s dir for a country: the admin level whose region
    names overlap the yield regions most. Returns None when nothing joins."""
    best, best_n = None, 0
    for ad in sorted(glob.glob(str(Path(country_root) / "admin_*"))):
        d = Path(ad) / "cr"
        if not (d / "s2s_tprate").exists():
            continue
        regs = set()
        for f in glob.glob(str(d / "s2s_tprate" / "*.csv")):
            m = re.search(r"_([a-z_\-]+)_(\d{4})_s2s_", Path(f).name)
            if m:
                regs.add(m.group(1).replace("-", "_"))
        n = len(regs & set(yield_regions))
        if n > best_n:
            best, best_n = str(d), n
    return best


def load_yields(stats_csv, target="Yield (tn per ha)"):
    """(region, year, obs) from a statistics file (deduped)."""
    df = pd.read_csv(stats_csv, usecols=["Region", "Harvest Year", target],
                     engine="pyarrow")
    df = df.dropna().drop_duplicates(["Region", "Harvest Year"])
    df["region"] = (df["Region"].str.lower().str.replace(" ", "_")
                    .str.replace("-", "_"))
    return df.rename(columns={"Harvest Year": "year", target: "obs"})[
        ["region", "year", "obs"]]


def causal_trend(obs):
    """LOYO linear trend per region: fit on all OTHER years."""
    rows = []
    for region, g in obs.groupby("region"):
        g = g.sort_values("year")
        if len(g) < 8:
            continue
        for _, r in g.iterrows():
            tr = g[g.year != r.year]
            b, a = np.polyfit(tr["year"], tr["obs"], 1)
            rows.append({"region": region, "year": int(r.year),
                         "obs": r.obs, "trend": float(b * r.year + a)})
    d = pd.DataFrame(rows)
    d = d[d["trend"] > 0]
    d["anom"] = d["obs"] / d["trend"] - 1
    return d


# ---------------------------------------------------------------------------
# pooled LOYO + classification scoring
# ---------------------------------------------------------------------------
def pooled_loyo(data, feats, eval_years, target_country, train_countries):
    """LOYO by YEAR across all countries; predictions for target rows only."""
    outs = []
    for y in eval_years:
        train = data[(data.year != y) & data.anom.notna()
                     & data.country.isin(train_countries)]
        test = data[(data.year == y) & (data.country == target_country)].copy()
        if test.empty or len(train) < 40:
            continue
        res = fit_ols(train, feats)
        test["ahat"] = predict_ols(res, test, feats)
        outs.append(test)
    return pd.concat(outs, ignore_index=True) if outs else pd.DataFrame()


def classify_score(lo, anoms_t, eval_years):
    """Detrended tercile classification metrics + AUC on target rows."""
    from sklearn.metrics import roc_auc_score

    a = anoms_t.dropna(subset=["anom"])
    recs = []
    for _, r in lo.dropna(subset=["ahat"]).iterrows():
        tr = a[(a.region == r.region) & (a.year != r.year)]["anom"]
        te = a[(a.region == r.region) & (a.year == r.year)]["anom"]
        if len(tr) < 9 or te.empty:
            continue
        e = _fold_bins(tr)
        recs.append({"year": r.year, "event": int(_to_class(te.iloc[0], e) == 0),
                     "pred_c": int(_to_class(r.ahat, e)), "score": -r.ahat})
    rec = pd.DataFrame(recs)
    if rec.empty or rec.event.nunique() < 2:
        return {}
    low = rec[rec.event == 1]
    nl = rec[rec.event == 0]
    return {
        "n": len(rec),
        # binary agreement: predicted-low vs observed-low
        "acc_bin": round(float(((rec.pred_c == 0) == (rec.event == 1)).mean()), 3),
        "low_recall": round(float((low.pred_c == 0).mean()), 3),
        "far": round(float((nl.pred_c == 0).mean()), 3),
        "auc": round(float(roc_auc_score(rec.event, rec.score)), 3),
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def run(path_config_files=None, *, parser=None, logger_obj=None,
        threshold_dir="crop_t0", crop="maize", eval_years=None,
        countries=None, today=None, eligibility_csv=None,
        skip_experiments=False):
    """Eligibility scan -> pooled experiments -> next-season forecasts.

    ``eligibility_csv`` reuses a previous scan instead of re-walking the
    output tree; the scan parses every merged crop CSV, which is minutes of
    I/O over a network share and changes only when new data lands.
    ``skip_experiments`` jumps straight to the forecasts using a
    ``best_variants.csv`` that sits beside the reused eligibility scan.
    """
    if parser is None:
        from geocif import logger as log
        logger_obj, parser = log.setup_logger_parser(path_config_files)
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    root = Path(parser.get("PATHS", "dir_output")) / project
    ts = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    out = root / "ml" / "analysis" / ts / "explore" / "s2s_pooled_model"
    out.mkdir(parents=True, exist_ok=True)
    eval_years = eval_years or list(range(1995, 2017))

    # ---- 1. eligibility ----
    if eligibility_csv:
        edf = pd.read_csv(eligibility_csv)
        edf.to_csv(out / "eligibility.csv", index=False)
        logger.info(f"reused eligibility scan: {eligibility_csv}")
    else:
        edf = elig.run(parser=parser, threshold_dir=threshold_dir, today=today,
                       out_dir=out)
    pool_rows = edf[(edf.crop == crop) & (edf.s2s_files > 0)
                    & edf.has_yield_stats]
    if countries:
        pool_rows = pool_rows[pool_rows.country.isin(countries)]
    cands = list(pool_rows.country)
    targets = list(pool_rows[pool_rows.runnable_now].country)
    logger.info(f"pool candidates: {cands} | runnable targets: {targets}")

    # ---- 2. assemble per-country frames ----
    meta, anoms, feats = {}, {}, {}
    stats_dir = root / "cid" / "indices" / "monthly_r" / "global"
    for _, r in pool_rows.iterrows():
        c = r.country
        cs, cr = c.title().replace("_", " "), crop.title().replace("_", " ")
        obs = load_yields(stats_dir / f"{cs}_{cr}_statistics_monthly_r.csv")
        an = causal_trend(obs)
        # A country may have S2S extracted at SEVERAL admin levels (Malawi has
        # both). Pick the level whose region names actually join the yields —
        # taking the first directory silently chose admin_1 for a country whose
        # yields are districts, producing zero overlap.
        s2s_dir = pick_s2s_dir(root / threshold_dir / c, set(an.region.unique()))
        if s2s_dir is None:
            logger.warning(f"{c}: no S2S directory joins its yield regions — skipped")
            continue
        meta[c] = {"planting": int(r.planting_month), "wraps": bool(r.wraps),
                   "harvest_year": int(r.harvest_year), "s2s_dir": s2s_dir}
        anoms[c] = an
        feats[c] = {}
        for off in range(1, MAX_OFFSET + 1):
            fx = country_features(s2s_dir, meta[c]["planting"], meta[c]["wraps"],
                                  off, sorted(an.year.unique()))
            feats[c][off] = fx
        logger.info(f"{c}: {len(an)} anomaly rows, planting "
                    f"{meta[c]['planting']}, features per offset "
                    f"{[len(feats[c][o]) for o in range(1, MAX_OFFSET + 1)]}")
        # region levels must actually join (e.g. Malawi: admin-1 S2S vs
        # district yields -> zero overlap). Drop such countries with a
        # clear reason instead of crashing downstream.
        probe = an.merge(feats[c][min(3, MAX_OFFSET)], on=["region", "year"])
        if probe.empty:
            logger.warning(
                f"{c}: yield regions and S2S regions do not overlap "
                f"(yields: {sorted(an.region.unique())[:3]}... vs S2S: "
                f"{sorted(feats[c][3].region.unique())[:3]}...) — excluded. "
                f"Needs matching-level S2S extraction or a region crosswalk.")
            meta.pop(c); anoms.pop(c); feats.pop(c)

    cands = [c for c in cands if c in meta]
    targets = [t for t in targets if t in meta]
    logger.info(f"post-assembly candidates: {cands} | targets: {targets}")

    # ---- 3. pooling experiments ----
    exp_rows = []
    if skip_experiments:
        prior = Path(eligibility_csv).parent / "best_variants.csv"             if eligibility_csv else None
        if prior and prior.exists():
            exp = pd.read_csv(Path(eligibility_csv).parent /
                              "pooling_experiments.csv")
            exp.to_csv(out / "pooling_experiments.csv", index=False)
            bv = pd.read_csv(prior)
            bv.to_csv(out / "best_variants.csv", index=False)
            best = {r.target: {"variant": r.variant,
                               "mean_auc": float(r.mean_auc)}
                    for _, r in bv.iterrows()}
            logger.info(f"reused prior experiments; best variants: {best}")
        else:
            raise FileNotFoundError(
                "skip_experiments needs best_variants.csv beside eligibility_csv")
    else:
      for tgt in (targets or cands):
          variants = {"own": [tgt], "all": cands,
                      "transfer": [c for c in cands if c != tgt]}
          for c in cands:
              if c != tgt:
                  variants[f"+{c}"] = [tgt, c]
          for off in range(1, MAX_OFFSET + 1):
              fl = FEATURES if off <= 3 else [f for f in FEATURES if f != "z_P_GF"]
              frames = []
              for c in cands:
                  fx = feats[c][off]
                  if fx.empty or (off <= 3 and "z_P_GF" not in fx.columns):
                      continue
                  d = anoms[c].merge(fx, on=["region", "year"], how="inner")
                  d["country"] = c
                  frames.append(d)
              if not frames:
                  continue
              data = pd.concat(frames, ignore_index=True)
              for vname, vcountries in variants.items():
                  if not vcountries or tgt not in cands:
                      continue
                  lo = pooled_loyo(data, fl, eval_years, tgt, vcountries)
                  if lo.empty:
                      continue
                  s = classify_score(lo, anoms[tgt], eval_years)
                  if s:
                      exp_rows.append({"target": tgt, "variant": vname,
                                       "offset": off, **s})
    exp = pd.DataFrame(exp_rows)
    exp.to_csv(out / "pooling_experiments.csv", index=False)

    # ---- 4. best variant per target (mean AUC over offsets 1-3) ----
    best = {}
    if not exp.empty:
        core = exp[exp.offset <= 3]
        m = core.groupby(["target", "variant"])["auc"].mean().reset_index()
        for tgt, g in m.groupby("target"):
            g = g.sort_values("auc", ascending=False)
            best[tgt] = {"variant": g.iloc[0]["variant"],
                         "mean_auc": round(float(g.iloc[0]["auc"]), 3)}
    pd.DataFrame([{"target": k, **v} for k, v in best.items()]).to_csv(
        out / "best_variants.csv", index=False)

    # ---- 5. next-season forecast for runnable targets ----
    pred_rows = []
    for tgt in targets:
        mt = meta[tgt]
        hy = mt["harvest_year"]
        # freshest USABLE offset with published data
        chosen = None
        for off in range(1, MAX_OFFSET + 1):
            fx = country_features(mt["s2s_dir"], mt["planting"], mt["wraps"],
                                  off, [hy])
            if not fx.empty:
                chosen = (off, fx)
                break
        if chosen is None:
            logger.warning(f"{tgt}: no published usable init for {hy}")
            continue
        off, fx = chosen
        fl = FEATURES if off <= 3 else [f for f in FEATURES if f != "z_P_GF"]
        vname = best.get(tgt, {}).get("variant", "own")
        vcountries = ([tgt] if vname == "own" else cands if vname == "all"
                      else [c for c in cands if c != tgt] if vname == "transfer"
                      else [tgt, vname[1:]])
        frames = []
        for c in vcountries:
            d = anoms[c].merge(feats[c][off], on=["region", "year"], how="inner")
            d["country"] = c
            frames.append(d)
        train = pd.concat(frames, ignore_index=True).dropna(subset=["anom"])
        if len(train) < 40:
            logger.warning(f"{tgt}: training pool too small ({len(train)}) — "
                           f"forecast skipped")
            continue
        res = fit_ols(train, fl)
        # clip to training support
        fxc = fx.copy()
        for f in fl:
            if f == "DRYHEAT":
                continue
            fxc[f] = fxc[f].clip(float(train[f].min()), float(train[f].max()))
        fxc["DRYHEAT"] = (fxc["z_PRCPTOT"] * fxc["z_TMEAN"]).clip(
            float(train["DRYHEAT"].min()), float(train["DRYHEAT"].max()))
        fxc["ahat"] = predict_ols(res, fxc, fl)
        # class probabilities from pooled LOYO residuals of the same variant
        lo = pooled_loyo(pd.concat(frames, ignore_index=True), fl,
                         eval_years, tgt, vcountries)
        lo2 = lo.merge(anoms[tgt][["region", "year", "anom"]],
                       on=["region", "year"], suffixes=("", "_o"))
        obs_a = lo2["anom_o"] if "anom_o" in lo2.columns else lo2["anom"]
        rr = (obs_a - lo2["ahat"]).dropna().to_numpy()
        a_t = anoms[tgt].dropna(subset=["anom"])
        for _, r in fxc.iterrows():
            hist = a_t[a_t.region == r.region]["anom"]
            if len(hist) < 9:
                continue
            e = _fold_bins(hist)
            x = r["ahat"] + rr
            pred_rows.append({
                "target": tgt, "harvest_year": hy, "offset_used": off,
                "variant": vname, "region": r.region,
                "ahat": round(float(r["ahat"]), 3),
                "P_low": round(float((x < e[0]).mean()), 3),
                "P_mid": round(float(((x >= e[0]) & (x < e[-1])).mean()), 3),
                "P_high": round(float((x >= e[-1]).mean()), 3),
                "P_below_trend": round(float((x < 0).mean()), 3),
            })
    preds = pd.DataFrame(pred_rows)
    preds.to_csv(out / "predictions_nextseason.csv", index=False)

    (out / "README.md").write_text(
        f"# s2s_pooled_model\n\ncandidates: {cands}\ntargets: {targets}\n"
        f"best variants: {best}\n\nPhenology-aligned pooling at offsets 1-"
        f"{MAX_OFFSET} months pre-planting; year-excluded LOYO across all "
        f"countries; detrended tercile classification.\n", encoding="utf-8")
    logger.info(f"outputs -> {out}")
    return out
