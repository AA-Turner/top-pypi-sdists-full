"""Kansas maize: does irrigated share interact with in-season drought stress?

Read-only diagnostic. Answers the question that has to be settled BEFORE
spending a model run on the ``use_irrigation_share`` A/B:

  "Within Kansas, does the cross-sectional yield advantage of irrigated
   counties widen in drought years and vanish (or invert) in good ones --
   and if so, which stress CID and which month carry that interaction?"

Why an anomaly, not a level
---------------------------
Irrigated Kansas maize averages 171.3 bu/ac against dryland's 69.8. A
correlation between ``irr_share`` and raw yield just re-measures that 2.45x
level gap, which is not in dispute and is already absorbed by any model
carrying Region. The open question is whether irrigation buffers *year-to-year
variability*, so every yield here is a within-county detrended residual,
standardised by that county's own residual sd.

What it produces
----------------
``{dir_output}/ml/analysis/{stamp}/explore/irrigation_kansas/``

  tables/coverage.csv          three-way join audit (irrigation / CID / yield)
  tables/dropped_counties.csv  counties excluded from the anomaly, with reason
  tables/sign_flip.csv         corr(irr_share, % error) per year, per model
  tables/yield_gradient.csv    per-year slope of yield_z on irr_share
  tables/stress_bakeoff.csv    interaction strength, ranked, per candidate CID
  tables/timing.csv            interaction strength per single month
  plots/*.png|pdf              one figure per table above
  README.md                    the verdict, plus the knobs that change it

Knobs that change the conclusion (not cosmetic): ``min_years`` (the evidence
floor per county), ``stage_name`` (which forecast stage the residuals come
from), and ``stress_cids`` (the candidate set that the bake-off ranks).

Usage::

    from geocif.experiments import irrigation_kansas
    irrigation_kansas.run(cfg)
    irrigation_kansas.run(cfg, state="nebraska")
"""
from __future__ import annotations

import ast
import logging
import sqlite3
import warnings
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

from geocif import logger as log
from geocif.cid import irrigation as irr_mod

warnings.simplefilter(action="ignore", category=FutureWarning)
logger = logging.getLogger(__name__)

_OBS = "Observed Yield (tn per ha)"
_PRED = "Predicted Yield (tn per ha)"

# Candidate in-season stress signals. ESI first (the current configured
# default), then the precipitation / heat CIDs that are the obvious
# alternatives -- a county irrigation effect could just as well key off heat
# stress as off evaporative stress. VI indices are included as a control: they
# partly *observe* irrigation rather than the stress it offsets, so a VI win
# here would mean something different from an ESI win.
DEFAULT_STRESS_CIDS = (
    "MEAN_ESI4WK", "AUC_ESI4WK", "MIN_ESI4WK", "STD_ESI4WK",
    "PRCPTOT", "CDD", "KDD", "TX90p", "SU", "TG", "R95pTOT",
    "MEAN_NDVI", "AUC_NDVI", "MEAN_GCVI",
)

# monthly_r Stage strings are '_'-joined month numbers, descending:
# '7' = July alone, '10_9_8_7_6_5_4' = the whole Apr-Oct season.
FULL_SEASON_STAGE = "10_9_8_7_6_5_4"
SINGLE_MONTH_STAGES = ("4", "5", "6", "7", "8", "9", "10")
_MONTH_LABEL = {
    "4": "Apr", "5": "May", "6": "Jun", "7": "Jul",
    "8": "Aug", "9": "Sep", "10": "Oct",
}


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

def _style_ctx():
    import matplotlib.pyplot as plt
    try:
        import scienceplots  # noqa: F401
        return plt.style.context(["science", "no-latex"])
    except Exception:
        return plt.style.context("default")


def _save(fig, out_dir: Path, name: str):
    import matplotlib.pyplot as plt
    for ext in ("png", "pdf"):
        fig.savefig(out_dir / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def _load_cids(cid_dir: Path, country: str, crop: str, state: str,
               stress_cids, stages) -> pd.DataFrame:
    """Read the per-year CID CSVs, keeping only one state and one CID set.

    The merged global statistics CSV for the USA is ~10 GB (every county,
    every stage, long format); the per-year files are ~1.8M rows each and
    filter down to a few thousand Kansas rows apiece, so they are the cheap
    path to the same numbers.
    """
    pattern = f"{country}_{crop}_s*.csv"
    files = sorted(cid_dir.glob(pattern))
    if not files:
        logger.warning(f"no CID CSVs matching {cid_dir / pattern}")
        return pd.DataFrame()

    state_prefix = state.replace("_", " ").title() + " "
    want_cids = set(stress_cids)
    want_stages = set(str(s) for s in stages)
    frames = []
    for f in files:
        try:
            df = pd.read_csv(
                f, usecols=["CID", "Region", "Stage", "Harvest Year", "Index"]
            )
        except (ValueError, OSError) as e:
            logger.warning(f"  unreadable {f.name} ({type(e).__name__}: {e})")
            continue
        df = df[
            df["Region"].astype(str).str.startswith(state_prefix)
            & df["Index"].isin(want_cids)
            & df["Stage"].astype(str).isin(want_stages)
        ]
        logger.info(f"  {f.name}: kept {len(df)} rows")
        if not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out["Harvest Year"] = pd.to_numeric(out["Harvest Year"], errors="coerce")
    out["CID"] = pd.to_numeric(out["CID"], errors="coerce")
    out = out.dropna(subset=["Harvest Year", "CID"])
    out["Harvest Year"] = out["Harvest Year"].astype(int)
    out["Stage"] = out["Stage"].astype(str)
    return out


def _pivot_stage(df_long: pd.DataFrame, stage: str) -> pd.DataFrame:
    """One stage -> wide frame keyed on (Region, Harvest Year)."""
    d = df_long[df_long["Stage"] == str(stage)]
    if d.empty:
        return pd.DataFrame()
    w = d.pivot_table(
        index=["Region", "Harvest Year"],
        columns="Index",
        values="CID",
        aggfunc="first",
    ).reset_index()
    w.columns.name = None
    return w


def _load_yields(db_path: Path, table: str, state: str) -> pd.DataFrame:
    """Observed + predicted yields from the outlook DB, one state only."""
    state_prefix = state.replace("_", " ").title() + " "
    uri = f"file:{db_path}?mode=ro&immutable=1"
    con = sqlite3.connect(uri, uri=True)
    try:
        df = pd.read_sql_query(
            f'SELECT Region, "Harvest Year", Model, "Stage Name", '
            f'"{_OBS}" AS obs, "{_PRED}" AS pred '
            f'FROM "{table}" WHERE Region LIKE ?',
            con,
            params=(state_prefix + "%",),
        )
    finally:
        con.close()
    df["Harvest Year"] = pd.to_numeric(df["Harvest Year"], errors="coerce")
    df["obs"] = pd.to_numeric(df["obs"], errors="coerce")
    df["pred"] = pd.to_numeric(df["pred"], errors="coerce")
    df = df.dropna(subset=["Harvest Year", "obs"])
    df["Harvest Year"] = df["Harvest Year"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def _theilsen(x: np.ndarray, y: np.ndarray):
    """Median-of-pairwise-slopes fit. Robust to the odd catastrophic year."""
    n = len(x)
    if n < 3:
        return np.nan, np.nan
    slopes = []
    for i in range(n - 1):
        dx = x[i + 1:] - x[i]
        ok = dx != 0
        if ok.any():
            slopes.append((y[i + 1:][ok] - y[i]) / dx[ok])
    if not slopes:
        return np.nan, np.nan
    m = float(np.median(np.concatenate(slopes)))
    b = float(np.median(y - m * x))
    return m, b


def _yield_anomaly(df_obs: pd.DataFrame, min_years: int):
    """Within-county detrended, sd-standardised yield residual.

    Returns ``(frame with yield_z, dropped-county report)``. Dropping is
    logged rather than silent: a county excluded here is a county the whole
    diagnostic never sees.
    """
    keep, dropped = [], []
    for region, g in df_obs.groupby("Region", sort=True):
        g = g.sort_values("Harvest Year")
        if len(g) < min_years:
            dropped.append({"Region": region, "n_years": len(g),
                            "reason": f"fewer than {min_years} years"})
            continue
        x = g["Harvest Year"].to_numpy(float)
        y = g["obs"].to_numpy(float)
        m, b = _theilsen(x, y)
        if not np.isfinite(m):
            dropped.append({"Region": region, "n_years": len(g),
                            "reason": "trend fit failed"})
            continue
        resid = y - (m * x + b)
        sd = float(np.std(resid, ddof=1))
        if not np.isfinite(sd) or sd == 0:
            dropped.append({"Region": region, "n_years": len(g),
                            "reason": "zero residual variance"})
            continue
        g = g.copy()
        g["yield_resid"] = resid
        g["yield_z"] = resid / sd
        keep.append(g)
    out = pd.concat(keep, ignore_index=True) if keep else pd.DataFrame()
    return out, pd.DataFrame(dropped)


def _within_county_z(df: pd.DataFrame, col: str, by: str = "Region"):
    """Standardise a CID within each county, so the contrast is temporal.

    A raw CID level is largely a west-east geography signal in Kansas, and
    that is exactly what ``irr_share`` also encodes; z-scoring within county
    strips the shared geography so the interaction term is about years, not
    about where the county sits.
    """
    g = df.groupby(by)[col]
    mu = g.transform("mean")
    sd = g.transform("std").replace(0.0, np.nan)
    return (df[col] - mu) / sd


def _ols(X: np.ndarray, y: np.ndarray):
    """Plain OLS with t-stats. Returns ``(beta, tstat, r2, n)`` or None."""
    n, k = X.shape
    if n <= k:
        return None
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = n - k
    sigma2 = float(resid @ resid) / dof
    try:
        xtx_inv = np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        return None
    se = np.sqrt(np.maximum(np.diag(xtx_inv) * sigma2, 0.0))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, beta / se, np.nan)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / ss_tot if ss_tot > 0 else np.nan
    return beta, t, r2, n


def _interaction_fit(df: pd.DataFrame, cid_col: str, min_rows: int = 50):
    """``yield_z ~ irr_share + cid_z + irr_share:cid_z``.

    Reports the interaction coefficient, its t-stat, and the R2 gained over
    the same model without the interaction. Delta-R2 is the honest measure of
    whether the interaction earns a feature slot; a large t on a tiny
    delta-R2 is a precisely estimated irrelevance.
    """
    d = df[["yield_z", "irr_share", cid_col]].replace(
        [np.inf, -np.inf], np.nan
    ).dropna()
    if len(d) < min_rows:
        return None
    y = d["yield_z"].to_numpy(float)
    irr = d["irr_share"].to_numpy(float)
    cid = d[cid_col].to_numpy(float)
    ones = np.ones(len(d))

    base = _ols(np.column_stack([ones, irr, cid]), y)
    full = _ols(np.column_stack([ones, irr, cid, irr * cid]), y)
    if base is None or full is None:
        return None
    return {
        "n": int(full[3]),
        "beta_irr": float(full[0][1]),
        "beta_cid": float(full[0][2]),
        "beta_interaction": float(full[0][3]),
        "t_interaction": float(full[1][3]),
        "r2_base": float(base[2]),
        "r2_full": float(full[2]),
        "delta_r2": float(full[2] - base[2]),
    }


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------

def _analysis_sign_flip(df_pred, irr, tables_dir, plots_dir, stage_name,
                        min_counties):
    """corr(irr_share, % prediction error) per year -- the docstring claim."""
    d = df_pred[df_pred["Stage Name"] == stage_name].copy()
    if d.empty:
        logger.warning(f"sign_flip: no rows at stage '{stage_name}'")
        return pd.DataFrame()
    d = d[d["obs"] > 0].copy()
    d["pct_err"] = (d["pred"] - d["obs"]) / d["obs"] * 100.0
    d = d.merge(irr, on=["Region", "Harvest Year"], how="inner")

    rows = []
    for (model, year), g in d.groupby(["Model", "Harvest Year"]):
        gg = g[["irr_share", "pct_err"]].replace(
            [np.inf, -np.inf], np.nan
        ).dropna()
        if len(gg) < min_counties or gg["irr_share"].nunique() < 5:
            continue
        rows.append({
            "Model": model,
            "Harvest Year": int(year),
            "n_counties": len(gg),
            "pearson_r": float(gg["irr_share"].corr(gg["pct_err"])),
            "spearman_r": float(
                gg["irr_share"].corr(gg["pct_err"], method="spearman")
            ),
            "mean_pct_err": float(gg["pct_err"].mean()),
        })
    res = pd.DataFrame(rows)
    if res.empty:
        return res
    res = res.sort_values(["Model", "Harvest Year"])
    res.to_csv(tables_dir / "sign_flip.csv", index=False)

    import matplotlib.pyplot as plt
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(8.0, 4.2))
        for model, g in res.groupby("Model"):
            ax.plot(g["Harvest Year"], g["pearson_r"], marker="o",
                    ms=4, lw=1.4, label=str(model))
        ax.axhline(0.0, color="0.35", lw=0.8)
        ax.set_xlabel("Harvest year")
        ax.set_ylabel("corr(irrigated share, % prediction error)")
        ax.set_title("Irrigation vs prediction error, Kansas maize")
        ax.legend(frameon=False, fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        _save(fig, plots_dir, "sign_flip")
    return res


def _analysis_yield_gradient(df, irr, stress_col, tables_dir, plots_dir,
                             min_counties):
    """Per-year slope of yield_z on irr_share, against that year's stress."""
    d = df.merge(irr, on=["Region", "Harvest Year"], how="inner")
    zcol = f"{stress_col}__z"
    if zcol not in d.columns:
        logger.warning(f"yield_gradient: {zcol} absent")
        return pd.DataFrame()
    rows = []
    for year, g in d.groupby("Harvest Year"):
        gg = g[["yield_z", "irr_share", zcol]].replace(
            [np.inf, -np.inf], np.nan
        ).dropna()
        if len(gg) < min_counties or gg["irr_share"].nunique() < 5:
            continue
        x = gg["irr_share"].to_numpy(float)
        y = gg["yield_z"].to_numpy(float)
        fit = _ols(np.column_stack([np.ones(len(x)), x]), y)
        if fit is None:
            continue
        rows.append({
            "Harvest Year": int(year),
            "n_counties": len(gg),
            "slope": float(fit[0][1]),
            "t_slope": float(fit[1][1]),
            "r2": float(fit[2]),
            "state_stress_z": float(gg[zcol].mean()),
            "state_mean_yield_z": float(gg["yield_z"].mean()),
        })
    res = pd.DataFrame(rows)
    if res.empty:
        return res
    res = res.sort_values("Harvest Year")
    res.to_csv(tables_dir / "yield_gradient.csv", index=False)

    import matplotlib.pyplot as plt
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(6.6, 4.8))
        ax.scatter(res["state_stress_z"], res["slope"], s=36,
                   color="#0C5DA5", zorder=3, edgecolor="white",
                   linewidth=0.5)
        for _, r in res.iterrows():
            ax.annotate(f"{int(r['Harvest Year'])}",
                        (r["state_stress_z"], r["slope"]),
                        textcoords="offset points", xytext=(4, 3),
                        fontsize=7.5, color="0.3")
        if len(res) >= 3:
            xs_all = res["state_stress_z"].to_numpy(float)
            fit = _ols(np.column_stack([np.ones(len(res)), xs_all]),
                       res["slope"].to_numpy(float))
            if fit is not None:
                xs = np.linspace(xs_all.min(), xs_all.max(), 50)
                ax.plot(xs, fit[0][0] + fit[0][1] * xs, color="#FF2C00",
                        lw=1.3, zorder=2,
                        label=f"OLS, $R^2$ = {fit[2]:.2f}")
                ax.legend(frameon=False, fontsize=9)
        ax.axhline(0.0, color="0.35", lw=0.8, zorder=1)
        ax.set_xlabel(f"Kansas mean {stress_col} (within-county z)")
        ax.set_ylabel("Slope of yield anomaly on irrigated share")
        ax.set_title("Irrigation yield advantage vs drought severity")
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        _save(fig, plots_dir, "yield_gradient")
    return res


def _analysis_stress_bakeoff(df, irr, cid_cols, tables_dir, plots_dir):
    """Rank candidate stress CIDs by the R2 their interaction adds."""
    d = df.merge(irr, on=["Region", "Harvest Year"], how="inner")
    rows = []
    for col in cid_cols:
        zcol = f"{col}__z"
        if zcol not in d.columns:
            continue
        fit = _interaction_fit(d.rename(columns={zcol: "cid_z"}), "cid_z")
        if fit is None:
            logger.warning(f"  bakeoff: {col} -- too few usable rows")
            continue
        fit["cid"] = col
        rows.append(fit)
    res = pd.DataFrame(rows)
    if res.empty:
        return res
    res = res.sort_values("delta_r2", ascending=False)
    res = res[["cid", "n", "beta_irr", "beta_cid", "beta_interaction",
               "t_interaction", "r2_base", "r2_full", "delta_r2"]]
    res.to_csv(tables_dir / "stress_bakeoff.csv", index=False)

    import matplotlib.pyplot as plt
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(7.0, 0.34 * len(res) + 1.8))
        order = res.iloc[::-1]
        ax.barh(order["cid"], order["delta_r2"], color="#0C5DA5", height=0.62)
        ax.set_xlabel("Gain in $R^2$ from the irrigation x stress interaction")
        ax.set_title("Which stress signal carries the irrigation interaction")
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        _save(fig, plots_dir, "stress_bakeoff")
    return res


def _analysis_timing(monthly_long, df_yield, irr, best_cid,
                     tables_dir, plots_dir):
    """Interaction strength month by month for the winning stress CID."""
    rows = []
    for stage in SINGLE_MONTH_STAGES:
        w = _pivot_stage(monthly_long, stage)
        if w.empty or best_cid not in w.columns:
            continue
        m = df_yield.merge(w, on=["Region", "Harvest Year"], how="inner")
        m = m.merge(irr, on=["Region", "Harvest Year"], how="inner")
        if m.empty:
            continue
        m["cid_z"] = _within_county_z(m, best_cid)
        fit = _interaction_fit(m, "cid_z")
        if fit is None:
            continue
        fit["month"] = _MONTH_LABEL[stage]
        fit["month_num"] = int(stage)
        rows.append(fit)
    res = pd.DataFrame(rows)
    if res.empty:
        return res
    res = res.sort_values("month_num")
    res.to_csv(tables_dir / "timing.csv", index=False)

    import matplotlib.pyplot as plt
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(6.4, 4.0))
        ax.plot(res["month"], res["delta_r2"], marker="o", ms=5, lw=1.5,
                color="#0C5DA5")
        ax.set_xlabel("Month")
        ax.set_ylabel("Gain in $R^2$ from the interaction")
        ax.set_title(f"When irrigation x {best_cid} matters, Kansas maize")
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        _save(fig, plots_dir, "timing")
    return res


def _analysis_residual_headroom(df_pred, irr, season_z, stress_col,
                                tables_dir, plots_dir, stage_name,
                                drought_frac=0.33, stress_sign=-1.0):
    """How much of the CURRENT model's error does irrigation x stress explain?

    This is the question a skill A/B ultimately answers, asked directly of the
    existing predictions: regress each model's % error on
    ``irr_share + stress_z + irr_share:stress_z``. The R2 is the share of
    today's error that irrigation information could in principle remove -- an
    upper bound on what the feature can buy, since a real model must estimate
    those coefficients out of sample rather than being handed them.

    Reported separately for the most-stressed years (the worst
    ``drought_frac`` of seasons by state mean stress) and the rest, because a
    feature that only pays in drought years is still worth having but will
    look weak on a pooled average.

    ``stress_sign`` is the sign of the CID's effect on yield, so the split
    picks the right tail: -1 for a CID where a HIGH value is bad (TX90p, KDD,
    CDD -- hot or dry), +1 for one where a high value is good (NDVI, PRCPTOT,
    ESI). Getting this backwards would label the best seasons "stressed" and
    silently invert the headline, so it is a parameter rather than an
    assumption -- ``run()`` reads it from the bake-off's fitted ``beta_cid``.
    """
    d = df_pred[df_pred["Stage Name"] == stage_name].copy()
    if d.empty:
        logger.warning(f"residual_headroom: no rows at stage '{stage_name}'")
        return pd.DataFrame()
    d = d[d["obs"] > 0].copy()
    d["pct_err"] = (d["pred"] - d["obs"]) / d["obs"] * 100.0
    d = d.merge(irr, on=["Region", "Harvest Year"], how="inner")

    zcol = f"{stress_col}__z"
    if zcol not in season_z.columns:
        logger.warning(f"residual_headroom: {zcol} absent")
        return pd.DataFrame()
    d = d.merge(
        season_z[["Region", "Harvest Year", zcol]],
        on=["Region", "Harvest Year"], how="inner",
    )
    if d.empty:
        return pd.DataFrame()

    # Split seasons by state mean stress, taking the tail that depresses
    # yield: the high end when stress_sign < 0 (TX90p: hot is bad), the low
    # end when stress_sign > 0 (NDVI: brown is bad).
    per_year = d.groupby("Harvest Year")[zcol].mean()
    n_drought = max(1, int(round(len(per_year) * drought_frac)))
    worst_first = per_year.sort_values(ascending=(stress_sign > 0))
    stressed = set(worst_first.head(n_drought).index)

    rows = []
    for model, g in d.groupby("Model"):
        for label, sub in (
            ("all", g),
            ("stressed", g[g["Harvest Year"].isin(stressed)]),
            ("other", g[~g["Harvest Year"].isin(stressed)]),
        ):
            s = sub[["pct_err", "irr_share", zcol]].replace(
                [np.inf, -np.inf], np.nan
            ).dropna()
            if len(s) < 50:
                continue
            y = s["pct_err"].to_numpy(float)
            irr_v = s["irr_share"].to_numpy(float)
            cid_v = s[zcol].to_numpy(float)
            ones = np.ones(len(s))
            irr_only = _ols(np.column_stack([ones, irr_v]), y)
            full = _ols(
                np.column_stack([ones, irr_v, cid_v, irr_v * cid_v]), y
            )
            if full is None or irr_only is None:
                continue
            rows.append({
                "Model": model,
                "years": label,
                "n": int(full[3]),
                "n_years": int(sub["Harvest Year"].nunique()),
                "r2_irr_only": float(irr_only[2]),
                "r2_irr_x_stress": float(full[2]),
                "beta_interaction": float(full[0][3]),
                "t_interaction": float(full[1][3]),
                "mean_abs_pct_err": float(np.abs(y).mean()),
            })
    res = pd.DataFrame(rows)
    if res.empty:
        return res
    res = res.sort_values(["Model", "years"])
    res.to_csv(tables_dir / "residual_headroom.csv", index=False)

    import matplotlib.pyplot as plt
    piv = res.pivot_table(
        index="Model", columns="years", values="r2_irr_x_stress"
    )
    order = [c for c in ("stressed", "other", "all") if c in piv.columns]
    with _style_ctx():
        fig, ax = plt.subplots(figsize=(6.8, 4.0))
        width = 0.8 / max(len(order), 1)
        xs = np.arange(len(piv.index))
        colors = {"stressed": "#FF2C00", "other": "#0C5DA5", "all": "#7F7F7F"}
        for i, col in enumerate(order):
            ax.bar(xs + i * width, piv[col].to_numpy(float), width,
                   label=col, color=colors.get(col, "#0C5DA5"))
        ax.set_xticks(xs + width * (len(order) - 1) / 2)
        ax.set_xticklabels(list(piv.index))
        ax.set_ylabel("Share of % error explained by irrigation x stress")
        ax.set_title("Headroom in the current model's error")
        ax.legend(frameon=False, fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)
        _save(fig, plots_dir, "residual_headroom")
    return res


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _write_readme(out_dir: Path, ctx: dict, bakeoff, gradient, timing,
                  sign_flip, headroom=None):
    lines = [
        f"# Irrigation x drought diagnostic -- {ctx['state']} {ctx['crop']}",
        "",
        f"- outlook DB: `{ctx['db_path']}`",
        f"- residual stage: `{ctx['stage_name']}`",
        f"- season stage for CIDs: `{FULL_SEASON_STAGE}` (Apr-Oct)",
        f"- counties in the anomaly: {ctx['n_counties']} "
        f"({ctx['n_dropped']} dropped, see dropped_counties.csv)",
        f"- years: {ctx['year_min']}-{ctx['year_max']}",
        f"- evidence floor: min_years = {ctx['min_years']}, "
        f"min_counties = {ctx['min_counties']}",
        "",
        "## Verdict",
        "",
    ]

    verdict = []
    if bakeoff is not None and not bakeoff.empty:
        top = bakeoff.iloc[0]
        verdict.append(
            f"Best stress CID: **{top['cid']}** -- interaction "
            f"beta = {top['beta_interaction']:.3f} "
            f"(t = {top['t_interaction']:.2f}), "
            f"delta R2 = {top['delta_r2']:.4f} "
            f"over a no-interaction model at R2 = {top['r2_base']:.4f}."
        )
        configured = ctx.get("configured_stress_cid")
        if configured and configured in set(bakeoff["cid"]):
            rank = int(
                bakeoff.reset_index(drop=True)
                .index[bakeoff.reset_index(drop=True)["cid"] == configured][0]
            ) + 1
            verdict.append(
                f"The configured `irrigation_stress_cid = {configured}` "
                f"ranks {rank} of {len(bakeoff)}."
            )
    if gradient is not None and not gradient.empty and len(gradient) >= 3:
        r = float(gradient["state_stress_z"].corr(gradient["slope"]))
        verdict.append(
            f"Per-year slope of yield anomaly on irrigated share correlates "
            f"{r:+.2f} with state mean stress across "
            f"{len(gradient)} years."
        )
    if timing is not None and not timing.empty:
        best = timing.sort_values("delta_r2", ascending=False).iloc[0]
        verdict.append(
            f"Interaction peaks in **{best['month']}** "
            f"(delta R2 = {best['delta_r2']:.4f})."
        )
    if sign_flip is not None and not sign_flip.empty:
        s = sign_flip.groupby("Harvest Year")["pearson_r"].mean()
        verdict.append(
            f"corr(irr_share, % error) ranges "
            f"{s.min():+.2f} to {s.max():+.2f} across years "
            f"(sign flips: {'yes' if s.min() < 0 < s.max() else 'no'})."
        )
    if headroom is not None and not headroom.empty:
        for label, tag in (("stressed", "stressed years"), ("all", "all years")):
            sub = headroom[headroom["years"] == label]
            if sub.empty:
                continue
            best = sub.sort_values("r2_irr_x_stress", ascending=False).iloc[0]
            verdict.append(
                f"Headroom, {tag}: irrigation x stress explains "
                f"{best['r2_irr_x_stress']:.1%} of {best['Model']}'s % error "
                f"(irrigated share alone: {best['r2_irr_only']:.1%})."
            )
    lines += [f"- {v}" for v in verdict] or ["- No analysis produced output."]

    lines += [
        "",
        "## Knobs that change the story",
        "",
        "- `min_years` -- the per-county evidence floor for fitting a trend.",
        "- `stage_name` -- which forecast stage the % errors come from; early "
        "stages have less information and larger errors.",
        "- `stress_cids` -- the candidate set the bake-off ranks.",
        "- Yields are within-county Theil-Sen detrended residuals divided by "
        "the county's own residual sd. Raw levels would measure the "
        "irrigated/dryland level gap instead.",
    ]
    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(
    path_config_files=None,
    *,
    state="kansas",
    country="united_states_of_america",
    crop="maize",
    outlook_db=None,
    stage_name="Sep 1-Apr 30",
    stress_cids=None,
    min_years=12,
    min_counties=30,
    parser=None,
    logger_obj=None,
):
    """Kansas irrigation x drought diagnostic.

    Args:
        state: admin_1 name; county Regions are matched by ``"<State> "``.
        outlook_db: explicit outlook DB path. None = newest ``outlook_*.db``
            under ``{dir_output}/ml/db/``.
        stage_name: forecast stage whose residuals feed the sign-flip check.
        stress_cids: candidate CIDs for the bake-off. None = module default.
        min_years: per-county evidence floor for the detrended anomaly.
        min_counties: minimum counties before a per-year statistic is kept.
    """
    if parser is None:
        if path_config_files is None:
            path_config_files = [Path("../config/geocif.txt")]
        logger_obj, parser = log.setup_logger_parser(path_config_files)

    stress_cids = tuple(stress_cids or DEFAULT_STRESS_CIDS)
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
    dir_metadata = parser.get("PATHS", "dir_metadata")
    method = parser.get(country, "method", fallback="monthly_r")
    admin_level = parser.get(country, "admin_level", fallback="admin_2")
    configured_stress = parser.get(
        "ML", "irrigation_stress_cid", fallback="MEAN_ESI4WK"
    ).strip()

    stamp = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    out_dir = (
        dir_output / "ml" / "analysis" / stamp / "explore" / "irrigation_kansas"
    )
    tables_dir = out_dir / "tables"
    plots_dir = out_dir / "plots"
    for d in (tables_dir, plots_dir):
        d.mkdir(parents=True, exist_ok=True)
    logger.info(f"irrigation_kansas -- {state} {crop}, out = {out_dir}")

    # ---- yields -----------------------------------------------------------
    if outlook_db:
        db_path = Path(outlook_db)
    else:
        db_dir = dir_output / "ml" / "db"
        cands = sorted(db_dir.glob("outlook_*.db"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
        if not cands:
            logger.error(f"no outlook_*.db under {db_dir}")
            return
        db_path = cands[0]
    logger.info(f"outlook DB: {db_path}")

    df_pred = _load_yields(db_path, f"{country}_{crop}", state)
    if df_pred.empty:
        logger.error(f"no {state} rows in {db_path}")
        return
    logger.info(
        f"outlook rows: {len(df_pred)}, "
        f"{df_pred['Region'].nunique()} counties, "
        f"models = {sorted(df_pred['Model'].unique())}"
    )

    df_obs = (
        df_pred[["Region", "Harvest Year", "obs"]]
        .drop_duplicates(subset=["Region", "Harvest Year"])
        .reset_index(drop=True)
    )
    df_yield, dropped = _yield_anomaly(df_obs, min_years)
    if df_yield.empty:
        logger.error("no county cleared the anomaly evidence floor")
        return
    if not dropped.empty:
        dropped.to_csv(tables_dir / "dropped_counties.csv", index=False)
        logger.warning(
            f"dropped {len(dropped)} counties from the anomaly "
            f"(reasons in dropped_counties.csv)"
        )

    # ---- irrigation share -------------------------------------------------
    years = sorted(df_yield["Harvest Year"].unique().tolist())
    csv_path = irr_mod.resolve_csv_path(parser, dir_metadata)
    frame = irr_mod.get_irrigation_frame(csv_path, crop, years=years)
    if frame is None or frame.empty:
        logger.error(f"no irrigation coverage for {crop} at {csv_path}")
        return
    irr = frame.rename(columns={"year": "Harvest Year"})
    # geocif Regions are "Kansas Ford"; the census key is normalised.
    df_yield["region_key"] = df_yield["Region"].map(irr_mod.normalize_region)
    key_to_region = (
        df_yield[["region_key", "Region"]].drop_duplicates()
    )
    irr = irr.merge(key_to_region, left_on="region", right_on="region_key",
                    how="inner")[["Region", "Harvest Year", "irr_share"]]
    logger.info(
        f"irrigation join: {irr['Region'].nunique()} counties matched "
        f"of {df_yield['Region'].nunique()} with a yield anomaly"
    )

    # ---- CIDs -------------------------------------------------------------
    cid_dir = (
        dir_output / "cid" / "indices" / method / admin_level / country / crop
    )
    wanted_stages = (FULL_SEASON_STAGE,) + SINGLE_MONTH_STAGES
    cid_long = _load_cids(cid_dir, country, crop, state, stress_cids,
                          wanted_stages)
    if cid_long.empty:
        logger.error(f"no CID rows for {state} under {cid_dir}")
        return
    logger.info(
        f"CID rows: {len(cid_long)}, "
        f"indices = {sorted(cid_long['Index'].unique())}"
    )

    season = _pivot_stage(cid_long, FULL_SEASON_STAGE)
    if season.empty:
        logger.error(f"no rows at the full-season stage {FULL_SEASON_STAGE}")
        return

    merged = df_yield.merge(season, on=["Region", "Harvest Year"], how="inner")
    cid_cols = [c for c in stress_cids if c in merged.columns]
    for c in cid_cols:
        merged[f"{c}__z"] = _within_county_z(merged, c)
    logger.info(
        f"analysis frame: {len(merged)} county-years, "
        f"{merged['Region'].nunique()} counties, "
        f"{len(cid_cols)} usable CIDs"
    )

    # ---- coverage audit ---------------------------------------------------
    coverage = pd.DataFrame([{
        "counties_in_outlook_db": int(df_pred["Region"].nunique()),
        "counties_with_yield_anomaly": int(df_yield["Region"].nunique()),
        "counties_dropped_by_floor": int(len(dropped)),
        "counties_with_irrigation": int(irr["Region"].nunique()),
        "counties_with_cids": int(season["Region"].nunique()),
        "counties_in_three_way_join": int(
            merged.merge(irr, on=["Region", "Harvest Year"])["Region"].nunique()
        ),
        "county_years_analysed": int(len(merged)),
        "year_min": int(min(years)),
        "year_max": int(max(years)),
        "usable_cids": ",".join(cid_cols),
    }])
    coverage.to_csv(tables_dir / "coverage.csv", index=False)
    logger.info(f"coverage: {coverage.to_dict('records')[0]}")

    # ---- analyses ---------------------------------------------------------
    sign_flip = _analysis_sign_flip(
        df_pred, irr, tables_dir, plots_dir, stage_name, min_counties
    )
    bakeoff = _analysis_stress_bakeoff(
        merged, irr, cid_cols, tables_dir, plots_dir
    )
    headline = (
        bakeoff.iloc[0]["cid"]
        if bakeoff is not None and not bakeoff.empty
        else (configured_stress if configured_stress in cid_cols else cid_cols[0])
    )
    gradient = _analysis_yield_gradient(
        merged, irr, headline, tables_dir, plots_dir, min_counties
    )
    timing = _analysis_timing(
        cid_long, df_yield, irr, headline, tables_dir, plots_dir
    )
    # Orientation of the headline CID, read off its fitted main effect on
    # yield rather than assumed from the CID's name.
    stress_sign = -1.0
    if bakeoff is not None and not bakeoff.empty:
        row = bakeoff[bakeoff["cid"] == headline]
        if not row.empty and np.isfinite(row.iloc[0]["beta_cid"]):
            stress_sign = 1.0 if row.iloc[0]["beta_cid"] > 0 else -1.0
    logger.info(
        f"headroom: stress CID {headline} has beta_cid sign "
        f"{'+' if stress_sign > 0 else '-'}; stressed years are the "
        f"{'lowest' if stress_sign > 0 else 'highest'} {headline}"
    )
    headroom = _analysis_residual_headroom(
        df_pred, irr, merged, headline, tables_dir, plots_dir, stage_name,
        stress_sign=stress_sign,
    )

    _write_readme(
        out_dir,
        {
            "state": state, "crop": crop, "db_path": db_path,
            "stage_name": stage_name,
            "n_counties": int(merged["Region"].nunique()),
            "n_dropped": int(len(dropped)),
            "year_min": min(years), "year_max": max(years),
            "min_years": min_years, "min_counties": min_counties,
            "configured_stress_cid": configured_stress,
        },
        bakeoff, gradient, timing, sign_flip, headroom,
    )
    logger.info(f"done -- {out_dir}")
    return {
        "out_dir": out_dir, "coverage": coverage, "sign_flip": sign_flip,
        "bakeoff": bakeoff, "gradient": gradient, "timing": timing,
        "headroom": headroom,
    }
