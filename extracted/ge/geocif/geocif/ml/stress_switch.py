"""Stress switch: turn target detrending OFF for a LOOCV fold that looks like a
national collapse year.

Detrending (``check_yield_trend``) is the right default for trend-following
years and for the forecast year, but it structurally over-predicts collapses:
usa_admin1 maize 2012 scored R2 0.31 / +14.8% national with tabicl trend-on,
0.90 with tabpfn trend-off. Per fold this module asks whether the national
June-August NDVI says "collapse"; if so, geocif fits that fold without
detrending (and without trend features) instead.

Per held-out season Y, using TRAINING years only for every fit:

1. National yield shock per training year: area-weighted yield over
   area-weighted per-region linear trend, minus 1. Weights = each region's
   mean area over the 3 previous years.
2. National NDVI signal per year: each region's Jun-Aug ``MEAN_NDVI``
   z-scored on the training years, area-weighted to one number.
3. OLS shock ~ NDVI signal on the training years; predict Y's shock.
4. Switch when the predicted shock is below ``-THRESHOLD_SD`` standard
   deviations of the training shocks.

Validated offline (2026-09-27..30) only for United States maize: it fires in
2012 alone at both admin_1 and admin_2 (0 false alarms in 2005-2026) and lifts
2012 R2 0.31 -> 0.90 (state) / 0.46 -> 0.75 (county). For soybean it fires in
2008 and 2012 without helping. Config (``[ML]``, see ``settings``):

    stress_switch = True                                  ; default
    stress_switch_countries = ['united_states_of_america'] ; default
    stress_switch_crops = ['maize']                       ; default
"""
import ast

import numpy as np
import pandas as pd

INDEX = "MEAN_NDVI"
WINDOW = "8_7_6"  # Jun-Aug Stage_ID; complete in every US state by the Sep forecast
THRESHOLD_SD = 1.0
MIN_YEARS = 8
DEFAULT_COUNTRIES = ["united_states_of_america"]
DEFAULT_CROPS = ["maize"]
VALIDATED = {("united_states_of_america", "maize")}


def _norm(name):
    return str(name).strip().lower().replace(" ", "_")


def settings(parser):
    """(enabled, countries, crops) from ``[ML]``; on for US maize by default."""
    enabled = parser.getboolean("ML", "stress_switch", fallback=True)
    countries = ast.literal_eval(parser.get("ML", "stress_switch_countries", fallback=str(DEFAULT_COUNTRIES)))
    crops = ast.literal_eval(parser.get("ML", "stress_switch_crops", fallback=str(DEFAULT_CROPS)))
    return enabled, [_norm(c) for c in countries], [_norm(c) for c in crops]


def applies(country, crop, countries, crops):
    return _norm(country) in countries and _norm(crop) in crops


def is_validated(country, crop):
    return (_norm(country), _norm(crop)) in VALIDATED


def extract_signal(df_long):
    """Raw Jun-Aug NDVI per (Region, Harvest Year) from the long CID table,
    or None when it is absent. Pass the frame already filtered to the current
    simulation stage: an earlier stage does not contain the window, so a July
    forecast can never read August NDVI."""
    need = {"Index", "Stage_ID", "CID", "Region", "Harvest Year"}
    if df_long is None or not need.issubset(df_long.columns):
        return None
    d = df_long[(df_long["Index"] == INDEX) & (df_long["Stage_ID"].astype(str) == WINDOW)]
    if d.empty:
        return None
    years = pd.to_numeric(d["Harvest Year"], errors="coerce")
    d = d.assign(**{"Harvest Year": years}).dropna(subset=["Harvest Year", "CID"])
    d = d.astype({"Harvest Year": int})
    s = d.groupby(["Region", "Harvest Year"], observed=True)["CID"].mean()
    return s if len(s) else None


def _trailing_area(area, region, year, first):
    """Mean area over the 3 years before ``year``; ``area`` is a plain dict.
    The first year of a record has no predecessor, so it falls back to the
    region's earliest-3-year mean (``first``) — weights only, area is not the
    target. Without it the record's first year drops out of the fit (usa_admin1
    starts in 2002, a drought year, and losing it hid the 2012 signal)."""
    vals = [area.get((region, y), np.nan) for y in range(year - 3, year)]
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else first.get(region, np.nan)


def predict_shock(yields, area, ndvi, year):
    """Decide whether held-out season ``year`` is a collapse year.

    Args:
        yields: observed yields of the TRAINING years, indexed (region, year).
        area: harvested area indexed (region, year); any years (not the target).
        ndvi: raw Jun-Aug NDVI indexed (region, year), from ``extract_signal``.
        year: the held-out season.

    Returns:
        dict with ``fired`` (bool), ``s_hat`` (predicted national shock),
        ``tau`` (sd of training shocks), ``z`` (national NDVI signal of
        ``year``) and ``reason`` when the rule could not be evaluated.
    """
    out = {"fired": False, "s_hat": np.nan, "tau": np.nan, "z": np.nan, "reason": ""}
    yields = yields.dropna()
    yields.index = pd.MultiIndex.from_arrays(
        [yields.index.get_level_values(0).astype(str), yields.index.get_level_values(1).astype(int)])
    train = sorted({int(y) for _, y in yields.index if int(y) != int(year)})
    if len(train) < MIN_YEARS:
        out["reason"] = f"only {len(train)} training years"
        return out

    trend = {}
    for region, g in yields.groupby(level=0):
        g = g.droplevel(0)
        g = g[g.index.astype(int) != int(year)]
        if len(g) >= MIN_YEARS:
            b1, b0 = np.polyfit(g.index.astype(float), g.values.astype(float), 1)
            trend[region] = (b0, b1)
    if not trend:
        out["reason"] = "no region with enough training years"
        return out
    regions = sorted(trend)
    y_d = yields.to_dict()
    a_d = {(str(r), int(y)): float(v) for (r, y), v in area.dropna().items()}
    first = {}
    for (r, y), v in sorted(a_d.items(), key=lambda kv: kv[0][1]):
        first.setdefault(r, []).append(v)
    first = {r: float(np.mean(v[:3])) for r, v in first.items()}

    def national_shock(y):
        num = den = 0.0
        for r in regions:
            v, w = y_d.get((r, y), np.nan), _trailing_area(a_d, r, y, first)
            if np.isfinite(v) and np.isfinite(w):
                num += w * v
                den += w * (trend[r][0] + trend[r][1] * y)
        return num / den - 1 if den > 0 else np.nan

    def national_z(y):
        num = den = 0.0
        for r, zr in z_by_region.items():
            v, w = zr.get(y, np.nan), _trailing_area(a_d, r, y, first)
            if np.isfinite(v) and np.isfinite(w):
                num += w * v
                den += w
        return num / den if den > 0 else np.nan

    ndvi_by_region = {}
    for (r, y), v in ndvi.dropna().items():
        ndvi_by_region.setdefault(str(r), {})[int(y)] = float(v)
    z_by_region = {}
    for r in regions:
        v = pd.Series(ndvi_by_region.get(r, {}), dtype=float)
        mu, sd = v.reindex(train).mean(), v.reindex(train).std()
        if np.isfinite(sd) and sd > 0:
            z_by_region[r] = ((v - mu) / sd).to_dict()
    if not z_by_region:
        out["reason"] = f"no {INDEX} {WINDOW} signal"
        return out

    shock = np.array([national_shock(y) for y in train])
    z_tr = np.array([national_z(y) for y in train])
    z_y = national_z(int(year))
    ok = np.isfinite(shock) & np.isfinite(z_tr)
    if ok.sum() < MIN_YEARS or not np.isfinite(z_y):
        out["reason"] = (f"no {INDEX} {WINDOW} signal for {year}" if not np.isfinite(z_y)
                         else f"only {ok.sum()} years with shock and signal")
        return out

    b1, b0 = np.polyfit(z_tr[ok], shock[ok], 1)
    tau = float(np.std(shock[np.isfinite(shock)], ddof=1))
    s_hat = float(b0 + b1 * z_y)
    out.update(fired=bool(s_hat < -THRESHOLD_SD * tau), s_hat=s_hat, tau=tau, z=float(z_y))
    return out
