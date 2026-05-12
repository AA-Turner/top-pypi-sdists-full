"""BEAST changepoint detection on HarvestStat Africa subnational yield series.

Filtering:
  - qc_flag == 0 (drop outliers and low-variance flagged rows)
  - yield > 0 and not null
  - >= MIN_YEARS unique harvest years per series

Series unit: (fnid, product, season_name, crop_production_system)
  - fnid resolves to admin_2 in 15 countries, admin_1 in 18 (use whichever is finer)

Outputs (under ``[BEAST].output_dir``):
  beast_results.csv   one row per series, top-3 CPs + metadata
  beast_top_cps.csv   long-form table of every CP with prob >= strong_cp_threshold

Run::

    from geocif.production_analysis import beast_runner
    beast_runner.run("path/to/geocif.txt")
"""
import argparse
import time
import warnings

import numpy as np
import pandas as pd

from geocif.production_analysis.config import load_config
from geocif.production_analysis import _common

warnings.filterwarnings("ignore")


def to_int_or_nan(x):
    """Cast scalar to int, returning NaN if non-finite (handles BEAST NaN)."""
    v = np.atleast_1d(x)[0]
    return int(v) if np.isfinite(v) else np.nan


GROUP_KEYS = [
    "fnid", "country", "admin", "admin_level",
    "product", "season_name", "crop_production_system",
]


def _filter_to_series_with_min_years(df, min_years):
    yr_counts = df.groupby(GROUP_KEYS, observed=True)["harvest_year"].nunique()
    keep = yr_counts[yr_counts >= min_years].reset_index()[GROUP_KEYS]
    df = df.merge(keep, on=GROUP_KEYS, how="inner")
    print(f"Series to run: {len(keep):,}")
    return df, keep


def run(path_config_file):
    cfg = load_config(path_config_file)

    print(f"Reading {cfg.input_csv.name}...")
    df = _common.load_filtered_hvstat(cfg.input_csv)
    df["admin_level"] = np.where(df["admin_2"] != "none", "admin_2", "admin_1")
    df, keep = _filter_to_series_with_min_years(df, cfg.min_years)

    results, top_cps = [], []
    t_start = time.time()

    for i, (key, sub) in enumerate(df.groupby(GROUP_KEYS, observed=True), 1):
        y, y0, full = _common.build_annual_series(sub)
        y1 = y0 + len(y) - 1
        n = len(y)
        n_obs = int(np.isfinite(y).sum())

        try:
            o = _common.run_beast(y, y0, cfg)
        except Exception as e:
            results.append({**dict(zip(GROUP_KEYS, key)),
                            "n_years_span": n, "n_obs": n_obs,
                            "year_start": y0, "year_end": y1,
                            "error": str(e)[:120]})
            continue

        cp_years, cp_probs = _common.extract_sorted_cps(o)
        cp_years = cp_years.astype(int)

        q = max(5, n // 4)
        mean_first = float(np.nanmean(y[:q]))
        mean_last = float(np.nanmean(y[-q:]))

        row = {**dict(zip(GROUP_KEYS, key)),
               "year_start": y0, "year_end": y1,
               "n_years_span": n, "n_obs": n_obs,
               "mean_yield_first_quartile": mean_first,
               "mean_yield_last_quartile": mean_last,
               "overall_change_pct": (
                   100 * (mean_last - mean_first) / mean_first
                   if mean_first > 0 else np.nan
               ),
               "ncp_median": to_int_or_nan(o.trend.ncp_median),
               "ncp_mode": to_int_or_nan(o.trend.ncp_mode)}
        for k in range(3):
            row[f"cp{k+1}_year"] = int(cp_years[k]) if k < len(cp_years) else np.nan
            row[f"cp{k+1}_prob"] = float(cp_probs[k]) if k < len(cp_probs) else np.nan
        results.append(row)

        for cy, cp in zip(cp_years, cp_probs):
            if cp >= cfg.strong_cp_threshold:
                top_cps.append({**dict(zip(GROUP_KEYS, key)),
                                "cp_year": int(cy), "cp_prob": float(cp),
                                "year_start": y0, "year_end": y1, "n_obs": n_obs})

        if i % 500 == 0:
            elapsed = time.time() - t_start
            eta = (len(keep) - i) / (i / elapsed)
            print(f"  {i:>5}/{len(keep)} | {elapsed:.0f}s elapsed | ETA {eta:.0f}s")

    print(f"Finished {len(results)} series in {time.time() - t_start:.0f}s")

    res = pd.DataFrame(results)
    out_results = cfg.output_dir / "beast_results.csv"
    res.to_csv(out_results, index=False)
    print(f"Wrote {out_results}: {res.shape}")

    cps_df = pd.DataFrame(top_cps)
    out_cps = cfg.output_dir / "beast_top_cps.csv"
    cps_df.to_csv(out_cps, index=False)
    print(f"Wrote {out_cps}: {cps_df.shape}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("config", nargs="+",
                   help="Path(s) to config file(s); later files override earlier")
    args = p.parse_args()
    run(args.config if len(args.config) > 1 else args.config[0])
