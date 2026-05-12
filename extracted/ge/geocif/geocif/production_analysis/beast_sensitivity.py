"""Sensitivity analysis for BEAST changepoint detection.

Varies three parameter families that most affect CP detection:
  (A) tcp_minmax upper bound  how many CPs BEAST is allowed to fit
  (B) tseg_minlength          minimum segment length (filters short-segment CPs)
  (C) mcmc_seed               Monte Carlo variability across runs

Stratified sample of ~N_HIGH+N_MED+N_LOW+N_NONE series across CP-confidence
levels. Each config produces a row per series; stability is measured
relative to the baseline config.

Outputs (under ``[BEAST].output_dir``):
  sensitivity_raw.csv      per-series CP outputs under each config
  sensitivity_summary.csv  stability metrics vs baseline
  fig5_sensitivity.png     four-panel diagnostic figure

Run (after ``beast_runner.run``)::

    from geocif.production_analysis import beast_sensitivity
    beast_sensitivity.run("path/to/geocif.txt")
"""
import argparse
import time
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from geocif.production_analysis.config import load_config
from geocif.production_analysis import _common

warnings.filterwarnings("ignore")

_common.init_mpl_rcparams()

GROUP_KEYS = ["fnid", "product", "season_name", "crop_production_system"]


def _stratify(res, n_high, n_med, n_low, n_none, seed=0):
    high = res[res["cp1_prob"] >= 0.95]
    med = res[(res["cp1_prob"] >= 0.5) & (res["cp1_prob"] < 0.95)]
    low = res[(res["cp1_prob"] >= 0.1) & (res["cp1_prob"] < 0.5)]
    nocp = res[(res["cp1_prob"] < 0.1) | (res["cp1_prob"].isna())]
    return pd.concat([
        high.sample(min(n_high, len(high)), random_state=seed),
        med.sample(min(n_med, len(med)), random_state=seed),
        low.sample(min(n_low, len(low)), random_state=seed),
        nocp.sample(min(n_none, len(nocp)), random_state=seed),
    ])


def _build_series_cache(cfg, sample_keys):
    df = _common.load_filtered_hvstat(cfg.input_csv)

    print("Building series cache...")
    t0 = time.time()
    series_cache = {}
    for key, sub in df.groupby(GROUP_KEYS, observed=True):
        if key not in sample_keys:
            continue
        y, y0, _ = _common.build_annual_series(sub)
        series_cache[key] = (y, y0)
    print(f"Cached {len(series_cache)} series in {time.time() - t0:.0f}s")
    return series_cache


def _run_one_config(name, tcp_minmax, tseg_minlength, mcmc_seed, series_cache, cfg):
    rows = []
    t0 = time.time()
    for key, (y, y0) in series_cache.items():
        try:
            o = _common.run_beast(
                y, y0, cfg,
                tcp_minmax=tcp_minmax,
                tseg_minlength=tseg_minlength,
                mcmc_seed=mcmc_seed,
            )
            ncp_m = np.atleast_1d(o.trend.ncp_median)[0]
            cp_years, cp_probs = _common.extract_sorted_cps(o)
            row = {
                "config": name, **dict(zip(GROUP_KEYS, key)),
                "ncp_median": ncp_m if np.isfinite(ncp_m) else np.nan,
                "cp1_year": cp_years[0] if len(cp_years) else np.nan,
                "cp1_prob": cp_probs[0] if len(cp_probs) else np.nan,
                "cp2_year": cp_years[1] if len(cp_years) >= 2 else np.nan,
                "cp2_prob": cp_probs[1] if len(cp_probs) >= 2 else np.nan,
            }
        except Exception as e:
            row = {"config": name, **dict(zip(GROUP_KEYS, key)),
                   "error": str(e)[:80]}
        rows.append(row)
    print(f"  {name}: {time.time() - t0:.0f}s")
    return rows


def _compute_stability(sens, cfg_names):
    base = sens[sens["config"] == "baseline"].set_index(GROUP_KEYS)
    other_configs = [n for n in cfg_names if n != "baseline"]
    stability = []
    for cfg_name in other_configs:
        cur = sens[sens["config"] == cfg_name].set_index(GROUP_KEYS)
        m = base[["ncp_median", "cp1_year", "cp1_prob"]].join(
            cur[["ncp_median", "cp1_year", "cp1_prob"]],
            lsuffix="_base", rsuffix="_cur", how="inner",
        )
        have_cp = m["cp1_year_base"].notna() & m["cp1_year_cur"].notna()
        cp_yr_stable = 100 * (
            (m["cp1_year_base"] - m["cp1_year_cur"]).abs() <= 2
        )[have_cp].mean()
        have_ncp = m["ncp_median_base"].notna() & m["ncp_median_cur"].notna()
        ncp_stable = 100 * (
            (m["ncp_median_base"] - m["ncp_median_cur"]).abs() <= 1
        )[have_ncp].mean()
        stability.append({
            "config": cfg_name,
            "cp1_year_within_2yr_pct": cp_yr_stable,
            "ncp_within_1_pct": ncp_stable,
            "mean_delta_ncp": (m["ncp_median_cur"] - m["ncp_median_base"]).mean(),
            "mean_delta_cp1_prob": (m["cp1_prob_cur"] - m["cp1_prob_base"]).mean(),
            "n_compared": len(m),
        })
    return pd.DataFrame(stability)


def _plot_sensitivity(sens, stab, cfg_names, output_path):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    # (a) Stability bars
    ax = axes[0, 0]
    x = np.arange(len(stab))
    w = 0.4
    ax.bar(x - w / 2, stab["cp1_year_within_2yr_pct"], w,
           label="Top-CP year within ±2 yr", color="#c0392b")
    ax.bar(x + w / 2, stab["ncp_within_1_pct"], w,
           label="# CPs within ±1", color="#2980b9")
    ax.set_xticks(x)
    ax.set_xticklabels(stab["config"], rotation=20, ha="right")
    ax.set_ylabel("% of series stable vs baseline")
    ax.set_title("(a) Stability of CP detection across configurations")
    ax.set_ylim(0, 105)
    ax.legend(fontsize=9, loc="lower right")
    for i, (a, b) in enumerate(zip(
        stab["cp1_year_within_2yr_pct"], stab["ncp_within_1_pct"]
    )):
        ax.text(i - w / 2, a + 1, f"{a:.0f}%", ha="center", fontsize=8)
        ax.text(i + w / 2, b + 1, f"{b:.0f}%", ha="center", fontsize=8)

    # (b) Distribution of #CPs by config
    ax = axes[0, 1]
    data = [sens[sens["config"] == c]["ncp_median"].dropna().values
            for c in cfg_names]
    positions = range(len(cfg_names))
    parts = ax.violinplot(data, positions=positions,
                          showmedians=True, widths=0.7)
    for pc in parts["bodies"]:
        pc.set_facecolor("#27ae60")
        pc.set_alpha(0.6)
    ax.set_xticks(positions)
    ax.set_xticklabels(cfg_names, rotation=20, ha="right")
    ax.set_ylabel("# trend CPs (posterior median)")
    ax.set_title("(b) Distribution of detected #CPs per config")

    base = sens[sens["config"] == "baseline"].set_index(GROUP_KEYS)

    # (c) Top-CP year scatter: baseline vs alt
    ax = axes[1, 0]
    scatter_colors = {
        "tcp_max3": "#e74c3c", "tcp_max10": "#16a085",
        "tseg_min3": "#f39c12", "tseg_min7": "#8e44ad",
    }
    for cfg_name in cfg_names:
        if cfg_name not in scatter_colors:
            continue
        cur = sens[sens["config"] == cfg_name].set_index(GROUP_KEYS)
        m = (base[["cp1_year"]].join(
            cur[["cp1_year"]], lsuffix="_b", rsuffix="_c", how="inner"
        ).dropna())
        ax.scatter(m["cp1_year_b"], m["cp1_year_c"], s=8, alpha=0.4,
                   color=scatter_colors[cfg_name], label=cfg_name)
    lo, hi = 1960, 2025
    ax.plot([lo, hi], [lo, hi], "k--", lw=1, alpha=0.5, label="1:1")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("Top-CP year (baseline)")
    ax.set_ylabel("Top-CP year (alt config)")
    ax.set_title("(c) Top-CP year: baseline vs alternate configs")
    ax.legend(fontsize=8, loc="upper left")

    # (d) MCMC seed variability — Δcp1_prob histogram
    ax = axes[1, 1]
    seed_colors = {"seed1": "#3498db", "seed100": "#9b59b6"}
    for cfg_name in cfg_names:
        if cfg_name not in seed_colors:
            continue
        cur = sens[sens["config"] == cfg_name].set_index(GROUP_KEYS)
        m = (base[["cp1_prob"]].join(
            cur[["cp1_prob"]], lsuffix="_b", rsuffix="_c", how="inner"
        ).dropna())
        diff = m["cp1_prob_c"] - m["cp1_prob_b"]
        ax.hist(diff, bins=50, alpha=0.55, color=seed_colors[cfg_name],
                label=f"{cfg_name}: σ = {diff.std():.3f}")
    ax.axvline(0, color="k", lw=1)
    ax.set_xlabel("Δ cp1_prob (alt seed − baseline)")
    ax.set_ylabel("Number of series")
    ax.set_title("(d) Monte Carlo error from MCMC seed (cp1_prob differences)")
    ax.legend(fontsize=9)

    plt.suptitle("BEAST sensitivity analysis · HarvestStat Africa",
                 fontweight="bold", y=1.00)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def run(path_config_file):
    cfg = load_config(path_config_file)

    res = pd.read_csv(cfg.output_dir / "beast_results.csv")
    res = res[res["ncp_median"].notna()].copy()
    sample = _stratify(
        res, cfg.sens_n_high, cfg.sens_n_med, cfg.sens_n_low, cfg.sens_n_none
    )
    print(f"Sample size: {len(sample)}")

    sample_keys = set(tuple(r) for r in sample[GROUP_KEYS].to_records(index=False))
    series_cache = _build_series_cache(cfg, sample_keys)

    print("Running configs...")
    all_rows = []
    cfg_names = []
    for entry in cfg.sens_configs:
        name = entry["name"]
        cfg_names.append(name)
        all_rows.extend(_run_one_config(
            name, entry["tcp_minmax"], entry["tseg_minlength"],
            entry["mcmc_seed"], series_cache, cfg,
        ))

    sens = pd.DataFrame(all_rows)
    out_raw = cfg.output_dir / "sensitivity_raw.csv"
    sens.to_csv(out_raw, index=False)
    print(f"Wrote {out_raw}: {sens.shape}")

    stab = _compute_stability(sens, cfg_names)
    out_summary = cfg.output_dir / "sensitivity_summary.csv"
    stab.to_csv(out_summary, index=False)
    print("\n=== Sensitivity summary (vs baseline) ===")
    print(stab.to_string(index=False))

    _plot_sensitivity(sens, stab, cfg_names, cfg.output_dir / "fig5_sensitivity.png")
    print("Saved fig5_sensitivity.png")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("config", nargs="+",
                   help="Path(s) to config file(s); later files override earlier")
    args = p.parse_args()
    run(args.config if len(args.config) > 1 else args.config[0])
