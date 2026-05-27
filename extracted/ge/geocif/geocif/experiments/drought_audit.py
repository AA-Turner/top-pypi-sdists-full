"""Drought-year input audit — does the data actually carry the drought signal?

Standalone read-only diagnostic. For each (country, crop) and a hand-curated
list of extreme years, it answers:

  "For drought years, do our high-residual-coupling CIDs look anomalous the
   way they should, or do they look ~normal?"

The actionable take-home is a one-line verdict per combo:

  - "signal intact (median |z| = X.XX) — modelling change next"
  - "signal weak (median |z| = X.XX) — input pipeline first"

Usage::

    from geocif.experiments import drought_audit
    drought_audit.run(cfg, extreme_years=[2011, 2017, 2019, 2020, 2021])
"""

import ast
import logging
import sqlite3
import warnings
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

from geocif import logger as log
from geocif import yield_outlook
from geocif.experiments.residuals_vs_cid import (
    _CANON_OBS,
    _CANON_PRED,
    _load_statistics_csv,
)

warnings.simplefilter(action="ignore", category=FutureWarning)
logger = logging.getLogger(__name__)


# Fallback list when no residuals_vs_cid ranking exists yet.
_DEFAULT_CIDS = [
    "PRCPTOT", "CDD", "STD_ETREF", "MIN_ETREF",
    "AUC_NDVI", "MAX_NDVI",
    "MEAN_FLDAS_SoilMoist_tavg_LEAD0",
    "MEAN_FLDAS_TotalPrecip_tavg_LEAD0",
    "R75p", "WSDI",
]


# ---------------------------------------------------------------------------
# CID column selection
# ---------------------------------------------------------------------------

def _pick_cid_columns(df_wide, cid_bases):
    """For each base CID name, find every wide-format column matching it.

    Wide columns look like ``"PRCPTOT Jul 1-Apr 30"`` after the long→wide
    pivot in _load_statistics_csv; the base name is the prefix before the
    space-separated stage suffix.
    """
    out = []
    for base in cid_bases:
        for col in df_wide.columns:
            if col == base or str(col).startswith(f"{base} "):
                out.append(col)
    return out


def _try_top_cids_from_ranking(dir_output_root, project_name, country, crop,
                               model, top_k=10):
    """Lift the top-k CID base names from the most recent residuals_vs_cid
    ranking_pooled.csv for this combo, if one exists. Returns [] otherwise."""
    explore_root = Path(dir_output_root) / project_name / "ml" / "analysis"
    if not explore_root.exists():
        return []
    pattern = (
        f"explore/residuals_vs_cid/{country}_{crop}/{model}/all_cids/"
        f"ranking_pooled.csv"
    )
    matches = sorted(
        explore_root.glob(f"*/{pattern}"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        return []
    try:
        df = pd.read_csv(matches[0])
        return df.head(top_k)["cid"].astype(str).tolist()
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Per-region z-scores: extreme year value vs normal-year stats
# ---------------------------------------------------------------------------

def _compute_per_region_zscores(df, cid_cols, extreme_years, admin_col="Region"):
    """For each (Region, CID, extreme_year), compute the z-score of the
    extreme year's CID value relative to normal-year stats for that region.

    A small |z| means the extreme year looks like a normal year in that CID
    (signal failure). Returns long-format DataFrame.
    """
    rows = []
    extreme_set = set(extreme_years)
    for col in cid_cols:
        for region, sub in df.groupby(admin_col):
            normal = sub.loc[
                ~sub["Harvest Year"].isin(extreme_set), col
            ].dropna()
            if normal.size < 3:
                continue
            mu = float(normal.mean())
            sd = float(normal.std(ddof=0))
            if not np.isfinite(sd) or sd < 1e-9:
                continue
            for _, row in sub.iterrows():
                yr = int(row["Harvest Year"])
                if yr not in extreme_set:
                    continue
                val = row[col]
                if not np.isfinite(val):
                    continue
                z = (val - mu) / sd
                rows.append({
                    "Region": region,
                    "CID": col,
                    "extreme_year": yr,
                    "extreme_value": float(val),
                    "normal_mean": mu,
                    "normal_std": sd,
                    "z": float(z),
                    "abs_z": float(abs(z)),
                })
    return pd.DataFrame(rows)


def _compute_nan_rates(df, cid_cols):
    """Per (CID, Year) NaN % across all regions in df."""
    rows = []
    for col in cid_cols:
        per_year = df.groupby("Harvest Year")[col].agg(
            n="size",
            n_nan=lambda s: int(s.isna().sum()),
        )
        per_year["nan_pct"] = 100.0 * per_year["n_nan"] / per_year["n"]
        per_year = per_year.reset_index()
        per_year["CID"] = col
        rows.append(per_year)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def _compute_yield_dropout(df, target="Yield (tn per ha)"):
    """For each year: how many regions reported a yield, and which are missing.

    Helps explain N drops (e.g. 33 → 23 in 2020-21) — are regions silently
    falling out of the training/test set because they reported zero?
    """
    if target not in df.columns:
        return pd.DataFrame()
    yld = (
        df.dropna(subset=[target])[["Region", "Harvest Year", target]]
        .drop_duplicates(subset=["Region", "Harvest Year"])
    )
    all_regions = set(yld["Region"].unique())
    rows = []
    for year, g in yld.groupby("Harvest Year"):
        present = set(g["Region"])
        missing = sorted(all_regions - present)
        rows.append({
            "Harvest Year": year,
            "n_regions_with_yield": len(present),
            "n_regions_missing_yield": len(missing),
            "missing_regions": "; ".join(missing),
        })
    return pd.DataFrame(rows).sort_values("Harvest Year")


# ---------------------------------------------------------------------------
# Residual coupling split (uses the outlook DB)
# ---------------------------------------------------------------------------

def _compute_residual_coupling_split(df_joined, cid_cols, extreme_years):
    """Pearson r between residual and per-region z-scored CID, computed
    separately on extreme-year rows vs normal-year rows.

    If |r| is larger in extreme years, the model is under-using signal that
    IS in the data. If |r| is smaller, the signal isn't there to use.
    """
    from scipy import stats as sps

    rows = []
    extreme_set = set(extreme_years)
    for col in cid_cols:
        sub = df_joined.dropna(subset=[col, "Residual"]).copy()
        if sub.empty:
            continue
        # Per-region z-score (same encoding as residuals_vs_cid uses)
        sub["z"] = sub.groupby("Region")[col].transform(
            lambda s: (s - s.mean())
                      / (s.std(ddof=0) if s.std(ddof=0) > 1e-9 else np.nan)
        )
        sub = sub.dropna(subset=["z"])
        if sub.empty:
            continue
        e = sub[sub["Harvest Year"].isin(extreme_set)]
        n = sub[~sub["Harvest Year"].isin(extreme_set)]
        out = {"CID": col}
        for label, dat in (("extreme", e), ("normal", n)):
            if (len(dat) >= 4
                    and dat["z"].std() > 0
                    and dat["Residual"].std() > 0):
                r, p = sps.pearsonr(dat["z"], dat["Residual"])
                out[f"{label}_r"] = float(r)
                out[f"{label}_p"] = float(p)
                out[f"{label}_n"] = int(len(dat))
            else:
                out[f"{label}_r"] = np.nan
                out[f"{label}_p"] = np.nan
                out[f"{label}_n"] = int(len(dat))
        rows.append(out)
    df = pd.DataFrame(rows)
    if not df.empty:
        df["abs_extreme"] = df["extreme_r"].abs()
        df["abs_normal"] = df["normal_r"].abs()
        df["delta_abs_r"] = df["abs_extreme"] - df["abs_normal"]
    return df


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def _plot_yield_timeseries(df, region, out_path, extreme_years,
                           target="Yield (tn per ha)"):
    """One PNG per region: observed yield over time, drought years shaded red."""
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    sub = df[df["Region"] == region].dropna(subset=[target]).copy()
    if sub.empty:
        return
    sub = (
        sub.sort_values("Harvest Year")
        .drop_duplicates(subset=["Harvest Year"])
    )

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(sub["Harvest Year"], sub[target],
                color="black", marker="o", linewidth=1.2, markersize=4,
                label="Observed")
        for y in extreme_years:
            ax.axvspan(y - 0.4, y + 0.4, alpha=0.22, color="red")
        ax.set_xlabel("Harvest Year")
        ax.set_ylabel("Yield (tn/ha)")
        ax.set_title(
            f"Observed yield — {region}  (drought years shaded)",
            fontsize=10,
        )
        ax.legend(loc="best", fontsize=8)
        plt.tight_layout()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
        plt.close(fig)


def _plot_cid_violin(df, cid_col, out_path, extreme_years):
    """One PNG per CID: box per year across regions, drought years shaded."""
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scienceplots  # noqa: F401

    sub = df.dropna(subset=[cid_col])[["Harvest Year", cid_col]].copy()
    if sub.empty:
        return
    sub = sub.sort_values("Harvest Year")
    sub["Harvest Year"] = sub["Harvest Year"].astype(int)

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(
            figsize=(max(10, sub["Harvest Year"].nunique() * 0.35), 5)
        )
        sns.boxplot(
            data=sub, x="Harvest Year", y=cid_col, ax=ax,
            color="lightgray", width=0.5,
        )
        years_sorted = sorted(sub["Harvest Year"].unique())
        for i, y in enumerate(years_sorted):
            if y in extreme_years:
                ax.axvspan(i - 0.45, i + 0.45, alpha=0.18, color="red")
        ax.set_xlabel("Harvest Year")
        ax.set_ylabel(cid_col)
        ax.set_title(
            f"{cid_col} — distribution by year (drought years shaded)",
            fontsize=10,
        )
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
        plt.close(fig)


# ---------------------------------------------------------------------------
# README writer
# ---------------------------------------------------------------------------

def _write_readme(out_dir, results_by_combo):
    """Top-line verdict per (country, crop) combo."""
    lines = [
        "# Drought-year audit — top-line verdicts\n",
        "Read each verdict to decide where to invest next: model change "
        "(signal intact) vs input pipeline (signal weak).\n",
    ]
    for (country, crop), info in sorted(results_by_combo.items()):
        median_abs_z = info.get("median_abs_z", float("nan"))
        worst_nan_pct = info.get("worst_nan_pct", float("nan"))
        worst_nan_cid = info.get("worst_nan_cid", "")
        verdict = info.get("verdict", "unknown")
        coupling_note = info.get("coupling_note", "")
        lines.append(f"## {country.title()} {crop.title()}\n")
        lines.append(
            f"- Median |z| across audited CIDs in extreme years: "
            f"**{median_abs_z:.2f}** "
            f"({'signal intact' if np.isfinite(median_abs_z) and median_abs_z >= 1.0 else 'signal weak'})"
        )
        if np.isfinite(worst_nan_pct) and worst_nan_pct > 0:
            lines.append(
                f"- Worst NaN rate in extreme years: "
                f"**{worst_nan_pct:.1f}%** (`{worst_nan_cid}`)"
            )
        if coupling_note:
            lines.append(f"- {coupling_note}")
        lines.append(f"- **Verdict**: {verdict}\n")
    Path(out_dir, "README.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(
    path_config_files=None,
    *,
    extreme_years=None,
    cids=None,
    outlook_db=None,
    parser=None,
    logger_obj=None,
):
    """Drought-year input audit.

    Args:
        path_config_files: list of geocif config file paths.
        extreme_years: list[int]. Default Somalia drought set
            ``[2011, 2017, 2019, 2020, 2021]``.
        cids: None (auto-detect from residuals_vs_cid ranking), "all" (use
            every CID), or explicit list of base CID names.
        outlook_db: explicit path to outlook DB. None = auto-detect newest
            ``outlook_*.db`` under ``{dir_output}/ml/db/``.
    """
    if extreme_years is None:
        extreme_years = [2011, 2017, 2019, 2020, 2021]
    extreme_years = [int(y) for y in extreme_years]

    if parser is None:
        if path_config_files is None:
            path_config_files = [Path("../config/geocif.txt")]
        logger_obj, parser = log.setup_logger_parser(path_config_files)

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output_root = Path(parser.get("PATHS", "dir_output"))
    dir_output = dir_output_root / project_name
    target = parser.get("ML", "target", fallback="Yield (tn per ha)")

    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    out_root = (
        dir_output / "ml" / "analysis" / today / "explore" / "drought_audit"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    logger.info(
        f"drought_audit — extreme_years={extreme_years}, out={out_root}"
    )

    # Auto-detect outlook DB
    db_path = None
    if outlook_db:
        db_path = Path(outlook_db)
    else:
        db_dir = dir_output / "ml" / "db"
        if db_dir.exists():
            candidates = sorted(
                db_dir.glob("outlook_*.db"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if candidates:
                db_path = candidates[0]
                logger.info(f"  auto-detected outlook DB: {db_path}")

    results_by_combo = {}

    for country in countries:
        try:
            crops = ast.literal_eval(parser.get(country, "crops"))
        except Exception:
            continue
        method = parser.get(country, "method", fallback="monthly_r")

        for crop in crops:
            logger.info(f"=== {country} {crop} ===")
            df_wide = _load_statistics_csv(
                dir_output, method, country, crop,
            )
            if df_wide.empty:
                logger.warning(
                    f"{country} {crop}: no statistics CSV; skipping"
                )
                continue

            # Resolve CID list
            cids_resolved = cids
            if cids_resolved is None:
                for model_name in ("catboost", "tabpfn", "tabicl"):
                    cids_resolved = _try_top_cids_from_ranking(
                        dir_output_root, project_name, country, crop,
                        model_name, top_k=10,
                    )
                    if cids_resolved:
                        logger.info(
                            f"  using top-10 CIDs from {model_name} "
                            f"residuals_vs_cid ranking"
                        )
                        break
                if not cids_resolved:
                    cids_resolved = _DEFAULT_CIDS
                    logger.info(
                        f"  using fallback default CID list "
                        f"({len(cids_resolved)} CIDs)"
                    )
            elif isinstance(cids_resolved, str) and cids_resolved.lower() == "all":
                # Use every CID column found in the wide df
                from geocif import utils as ut
                cids_resolved = ut.filter_cid_columns(
                    df_wide,
                    fixed_cols=["Country", "Region", "Harvest Year",
                                "Stage Name", "Season"],
                    target=target,
                    stat_cols=["Area (ha)", "Production (tn)"],
                )

            cid_cols = _pick_cid_columns(df_wide, cids_resolved)
            if not cid_cols:
                logger.warning(
                    f"{country} {crop}: none of the configured CIDs "
                    f"({cids_resolved[:5]}...) found as columns; skipping"
                )
                continue
            logger.info(
                f"  {len(cid_cols)} matching CID columns under audit"
            )

            combo_dir = out_root / f"{country}_{crop}"
            combo_dir.mkdir(parents=True, exist_ok=True)

            # 1. Per-region z-scores in extreme years
            z_df = _compute_per_region_zscores(
                df_wide, cid_cols, extreme_years,
            )
            if not z_df.empty:
                summary = (
                    z_df.groupby(["extreme_year", "CID"])["abs_z"]
                    .agg(["median", "count"])
                    .reset_index()
                    .rename(columns={
                        "median": "median_abs_z",
                        "count": "n_regions",
                    })
                )
                summary.to_csv(combo_dir / "summary.csv", index=False)

                # Signal failures: CIDs where most regions show |z| < 1
                sig_fail = (
                    z_df.assign(below_one=(z_df["abs_z"] < 1).astype(int))
                    .groupby(["extreme_year", "CID"])["below_one"]
                    .agg(["sum", "count"])
                    .reset_index()
                    .rename(columns={
                        "sum": "n_regions_failing",
                        "count": "n_regions_total",
                    })
                )
                sig_fail["pct_failing"] = (
                    100.0 * sig_fail["n_regions_failing"]
                    / sig_fail["n_regions_total"]
                )
                sig_fail.sort_values(
                    ["extreme_year", "pct_failing"],
                    ascending=[True, False],
                ).to_csv(combo_dir / "signal_failures.csv", index=False)

            # 2. NaN rates by year
            nan_df = _compute_nan_rates(df_wide, cid_cols)
            if not nan_df.empty:
                nan_df.to_csv(
                    combo_dir / "nan_rates_by_year.csv", index=False,
                )

            # 3. Yield dropout by year
            dropout = _compute_yield_dropout(df_wide, target=target)
            if not dropout.empty:
                dropout.to_csv(
                    combo_dir / "yield_dropout_by_year.csv", index=False,
                )

            # 4. Residual coupling split — extreme vs normal years
            coupling_note = ""
            if db_path is not None and db_path.exists():
                con = sqlite3.connect(db_path)
                try:
                    tables = pd.read_sql(
                        "SELECT name FROM sqlite_master "
                        "WHERE type='table' AND name=?",
                        con, params=(f"{country}_{crop}",),
                    )
                    if not tables.empty:
                        models = pd.read_sql(
                            f'SELECT DISTINCT Model FROM "{country}_{crop}" '
                            f'WHERE "Experiment Name"="outlook" '
                            f'AND Model NOT IN ("null","trend","trend_all") LIMIT 1',
                            con,
                        )
                    else:
                        models = pd.DataFrame()
                finally:
                    con.close()
                if not models.empty:
                    model = models.iloc[0]["Model"]
                    df_resid = yield_outlook._query_predictions(
                        db_path, f"{country}_{crop}", model,
                        experiment_name="outlook",
                    )
                    if not df_resid.empty:
                        df_resid = df_resid.dropna(
                            subset=[_CANON_PRED, _CANON_OBS]
                        ).copy()
                        df_resid["Residual"] = (
                            df_resid[_CANON_OBS] - df_resid[_CANON_PRED]
                        )
                        df_resid["Harvest Year"] = (
                            df_resid["Harvest Year"].astype(int)
                        )
                        # Align Country casing for the merge
                        df_resid["Country"] = (
                            df_resid["Country"].astype(str)
                            .str.lower().str.replace(" ", "_")
                        )
                        df_wide_lk = df_wide.copy()
                        df_wide_lk["Country"] = (
                            df_wide_lk["Country"].astype(str)
                            .str.lower().str.replace(" ", "_")
                        )
                        join_keys = [
                            k for k in ("Country", "Region",
                                        "Harvest Year", "Stage Name")
                            if k in df_resid.columns and k in df_wide_lk.columns
                        ]
                        df_joined = df_resid.merge(
                            df_wide_lk, on=join_keys, how="inner",
                        )
                        if not df_joined.empty:
                            coupling = _compute_residual_coupling_split(
                                df_joined, cid_cols, extreme_years,
                            )
                            if not coupling.empty:
                                coupling.to_csv(
                                    combo_dir
                                    / "extreme_vs_normal_coupling.csv",
                                    index=False,
                                )
                                # Top-line note: did residual coupling
                                # strengthen or weaken in extreme years?
                                med_extreme = float(
                                    coupling["abs_extreme"].median()
                                )
                                med_normal = float(
                                    coupling["abs_normal"].median()
                                )
                                if (np.isfinite(med_extreme)
                                        and np.isfinite(med_normal)):
                                    direction = (
                                        "stronger" if med_extreme > med_normal
                                        else "weaker"
                                    )
                                    coupling_note = (
                                        f"Residual–CID coupling is "
                                        f"{direction} in extreme years "
                                        f"(median |r|: extreme="
                                        f"{med_extreme:.2f}, normal="
                                        f"{med_normal:.2f})"
                                    )

            # 5. Plots — top-yield regions + top CIDs
            plots_dir = combo_dir / "plots"
            plots_dir.mkdir(exist_ok=True)
            if target in df_wide.columns:
                region_means = (
                    df_wide.dropna(subset=[target])
                    .groupby("Region")[target]
                    .mean()
                    .sort_values(ascending=False)
                    .head(8)
                )
                for region in region_means.index:
                    safe = str(region).replace(" ", "_").replace("/", "_")
                    _plot_yield_timeseries(
                        df_wide, region,
                        plots_dir / f"yield_timeseries_{safe}.png",
                        extreme_years, target=target,
                    )
            for cid in cid_cols[:6]:
                safe = str(cid).replace(" ", "_").replace("/", "_")
                _plot_cid_violin(
                    df_wide, cid,
                    plots_dir / f"cid_violin_{safe}.png",
                    extreme_years,
                )

            # Top-line verdict
            median_abs_z = (
                float(z_df["abs_z"].median()) if not z_df.empty
                else float("nan")
            )
            extreme_nan = (
                nan_df[nan_df["Harvest Year"].isin(extreme_years)]
                .sort_values("nan_pct", ascending=False).head(1)
                if not nan_df.empty else pd.DataFrame()
            )
            worst_nan_pct = (
                float(extreme_nan["nan_pct"].iloc[0])
                if not extreme_nan.empty else float("nan")
            )
            worst_nan_cid = (
                str(extreme_nan["CID"].iloc[0])
                if not extreme_nan.empty else ""
            )
            if np.isfinite(median_abs_z) and median_abs_z >= 1.0:
                verdict = (
                    f"signal intact (median |z| = {median_abs_z:.2f}) "
                    f"— modelling change next"
                )
            else:
                verdict = (
                    f"signal weak (median |z| = {median_abs_z:.2f}) "
                    f"— input pipeline first"
                )
            results_by_combo[(country, crop)] = {
                "median_abs_z": median_abs_z,
                "worst_nan_pct": worst_nan_pct,
                "worst_nan_cid": worst_nan_cid,
                "coupling_note": coupling_note,
                "verdict": verdict,
            }
            logger.info(f"  [{country} {crop}] verdict: {verdict}")

    if results_by_combo:
        _write_readme(out_root, results_by_combo)
        logger.info(
            f"drought_audit done → {out_root / 'README.md'}"
        )
    else:
        logger.warning(
            "drought_audit produced no results — no usable (country, crop) combos"
        )

    return out_root
