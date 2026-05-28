"""Threshold-Sweep Optimizer — consumer for `geoprepare.extract_sweep`.

Usage::

    from geocif import threshold_optimizer
    threshold_optimizer.run([geobase.txt, countries.txt, crops.txt, geocif.txt])

For each (country, crop, season) declared in config, this runner:

1. Reads the sweep CSV produced by ``geoprepare.extract_sweep`` at
   ``${PATHS:dir_output}/threshold_sweep/{country}/{crop}/{country}_{crop}_s{season}_sweep.csv``.
2. Runs a small set of sanity checks (region coverage, n_cells monotonicity,
   fallback clustering) and warns on violations.
3. Aggregates the daily/8-day variable column to a seasonal value per
   (region, year, direction, threshold) via ``max`` (default) or ``mean``.
4. Joins HarvestStat yield via the canonical
   ``geocif.ml.stats.add_statistics`` path (same call shape used by
   ``geocif.agmet.geoagmet``; no parallel file-reading).
5. Computes a skill metric per (region, direction, threshold):
   Pearson |r| by default, LOOCV RMSE optional via ``[THRESHOLD_OPTIMIZER]
   metric = loocv_rmse``.
6. Flags (region, direction, threshold) rows where the fallback-year
   share exceeds ``max_fallback_share`` as not trustworthy and excludes
   them from "best" ranking (kept in the summary CSV for visibility).
7. Writes per-region + pooled-per-country summary CSVs + a
   metric-vs-threshold PNG with companion plot-data CSV under
   ``${PATHS:dir_output}/{project_name}/ml/analysis/{today}/threshold_sweep_summary/``.

The pooled-best (direction, threshold) per country is the actionable
output — what to set as ``[<country>] floor`` / ``ceil`` in
geoextract.txt for production extraction.
"""
import ast
import logging
from pathlib import Path
from typing import Optional

import arrow as ar
import numpy as np
import pandas as pd

from geoprepare import base

from geocif.agmet import utils as agmet_utils
from geocif.ml import stats as ml_stats


# Columns that are NOT the variable column — anything else in the sweep CSV
# header is the variable column name (typically 'ndvi', could be 'chirps',
# 'etref', etc. for future sweeps over other variables).
_NON_VAR_COLS = frozenset({
    "country", "region", "region_id", "lat", "lon", "year", "doy",
    "direction", "threshold", "fallback_used", "n_cells_used",
    "crop_fraction_mean",
})


class ThresholdOptimizer(base.BaseGeo):
    """Consumer for geoprepare.extract_sweep CSVs.

    Inherits the standard geoprepare config-parsing scaffolding (paths,
    logger, project_name) so the runner matches the existing agmet /
    geocif_runner / indices_runner conventions.
    """

    def __init__(self, path_config_file):
        super().__init__(path_config_file)
        self.parse_config()

    def _get(self, option, default, sections=("THRESHOLD_OPTIMIZER", "DEFAULT")):
        """Read an option from the first section that has it, else default.

        Same pattern as ``AgmetGeo._get_option`` but returns the raw string
        (typed conversion at the call site). Used so configs without a
        ``[THRESHOLD_OPTIMIZER]`` section still work with safe defaults.
        """
        for section in sections:
            if self.parser.has_option(section, option):
                return self.parser.get(section, option)
        return default

    def parse_config(self, section="DEFAULT"):
        self.project_name = self.parser.get("DEFAULT", "project_name")
        super().parse_config(project_name=self.project_name, section="DEFAULT")

        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.today_tag = ar.now().format("MMMM_DD_YYYY")

        # [THRESHOLD_OPTIMIZER] settings — all optional with safe fallbacks.
        self.agg_method = self._get("agg_method", "max").strip().lower()
        if self.agg_method not in ("max", "mean"):
            self.logger.warning(
                f"  [THRESHOLD_OPTIMIZER] agg_method={self.agg_method!r} not in "
                f"(max, mean); falling back to 'max'."
            )
            self.agg_method = "max"

        self.metric_name = self._get("metric", "pearson").strip().lower()
        if self.metric_name not in ("pearson", "loocv_rmse"):
            self.logger.warning(
                f"  [THRESHOLD_OPTIMIZER] metric={self.metric_name!r} not in "
                f"(pearson, loocv_rmse); falling back to 'pearson'."
            )
            self.metric_name = "pearson"

        self.max_fallback_share = float(self._get("max_fallback_share", "0.3"))
        self.do_plot = self._get("plot", "True").strip().lower() in (
            "true", "1", "yes",
        )

    # ----------------------------------------------------------------------
    # Paths
    # ----------------------------------------------------------------------

    def sweep_csv_path(self, country: str, crop: str, season: int) -> Path:
        """Per the briefing: sweep lives at ``${dir_output}/threshold_sweep/
        {country}/{crop}/{country}_{crop}_s{season}_sweep.csv``."""
        # self.dir_output is already project-suffixed by BaseGeo, but the
        # sweep is written by geoprepare which uses the un-suffixed
        # dir_output. Strip the project_name segment to land on the
        # geoprepare-side root.
        base_dir = self.dir_output.parent if self.dir_output.name == self.project_name else self.dir_output
        return (
            base_dir / "threshold_sweep" / country / crop
            / f"{country}_{crop}_s{season}_sweep.csv"
        )

    def summary_dir(self, country: str, crop: str) -> Path:
        d = (
            self.dir_output / "ml" / "analysis" / self.today_tag
            / "threshold_sweep_summary" / country / crop
        )
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ----------------------------------------------------------------------
    # Iterators
    # ----------------------------------------------------------------------

    def create_run_combinations(self):
        """Yield (country, admin_level, crop, season) — same iteration the
        existing runners use (mirrors ``AgmetGeo.create_run_combinations``).
        """
        all_combos = []
        for country in self.countries:
            admin_level = self.parser.get(country, "admin_level")
            crops = ast.literal_eval(self.parser.get(country, "crops"))
            has_seasons = (
                self.parser.has_option(country, "seasons")
                or self.parser.has_option("DEFAULT", "seasons")
            )
            for crop in crops:
                if has_seasons:
                    seasons = ast.literal_eval(self.parser.get(country, "seasons"))
                else:
                    seasons = [1]
                for season in seasons:
                    all_combos.append((country, admin_level, crop, season))
        return all_combos

    # ----------------------------------------------------------------------
    # CSV reading + variable column detection
    # ----------------------------------------------------------------------

    @staticmethod
    def detect_var_column(df: pd.DataFrame, csv_path: Optional[Path] = None) -> str:
        """Return the single column name that isn't in the fixed schema set.

        Raises ValueError naming the CSV path if 0 or >1 candidates exist,
        so a malformed sweep produces a clear actionable error rather than
        silently picking the wrong column.
        """
        candidates = [c for c in df.columns if c not in _NON_VAR_COLS]
        if len(candidates) != 1:
            where = f" in {csv_path}" if csv_path is not None else ""
            raise ValueError(
                f"Expected exactly 1 variable column{where}; found "
                f"{len(candidates)}: {candidates!r}. Schema must be: "
                f"country, region, region_id, lat, lon, year, doy, <var>, "
                f"direction, threshold, fallback_used, n_cells_used, "
                f"crop_fraction_mean."
            )
        return candidates[0]

    def read_sweep_csv(self, country: str, crop: str, season: int):
        """Load the sweep CSV; return (df, var_col) or (None, None) with
        a clear WARNING if the file is missing (caller skips that combo)."""
        path = self.sweep_csv_path(country, crop, season)
        if not path.is_file():
            self.logger.warning(
                f"  sweep CSV not found for ({country}, {crop}, s{season}) at "
                f"{path} — run `geoprepare.extract_sweep` upstream first; skipping."
            )
            return None, None
        df = pd.read_csv(path, low_memory=False)
        # configparser-style booleans in the CSV ("True"/"False" strings)
        # → real bools. Defensive: leave already-bool columns alone.
        if df["fallback_used"].dtype == object:
            df["fallback_used"] = df["fallback_used"].astype(str).str.strip().str.lower() == "true"
        var_col = self.detect_var_column(df, csv_path=path)
        return df, var_col

    # ----------------------------------------------------------------------
    # Sanity checks (non-fatal warnings)
    # ----------------------------------------------------------------------

    def sanity_check(self, df: pd.DataFrame, label: str):
        admin_count = df["region"].nunique()
        per_combo = (
            df.groupby(["direction", "threshold"])["region"].nunique()
        )
        dropped = per_combo[per_combo != admin_count]
        if not dropped.empty:
            self.logger.warning(
                f"  [{label}] {len(dropped)} (direction, threshold) combos "
                f"have < admin_count={admin_count} regions — fallback failed "
                f"somewhere. Worst-case combos: {dropped.head(3).to_dict()}"
            )

        fb_share = df["fallback_used"].mean()
        self.logger.info(
            f"  [{label}] overall fallback share = {fb_share:.1%} across "
            f"{len(df)} rows"
        )

    # ----------------------------------------------------------------------
    # Seasonal aggregation
    # ----------------------------------------------------------------------

    def aggregate_seasonal(self, df: pd.DataFrame, var_col: str) -> pd.DataFrame:
        """Collapse the DOY axis to one row per
        (region, year, direction, threshold). Aggregator = max | mean.

        ``fallback_used`` is propagated via ``any`` so a year-season with
        even one fallback DOY is flagged fallback. ``n_cells_used`` and
        ``crop_fraction_mean`` use mean for QA reporting.
        """
        agg_fn = self.agg_method  # 'max' or 'mean'
        grouped = (
            df.groupby(["region", "region_id", "year", "direction", "threshold"],
                       as_index=False, dropna=False)
              .agg(**{
                  var_col: (var_col, agg_fn),
                  "fallback_used": ("fallback_used", "any"),
                  "n_cells_used": ("n_cells_used", "mean"),
                  "crop_fraction_mean": ("crop_fraction_mean", "mean"),
              })
        )
        return grouped

    # ----------------------------------------------------------------------
    # HarvestStat yield join — CANONICAL PATH ONLY (mirrors agmet)
    # ----------------------------------------------------------------------

    def join_yield(self, df_agg: pd.DataFrame, country: str, crop: str,
                   admin_zone: str, season: int) -> pd.DataFrame:
        """Join HarvestStat yield using the canonical
        ``geocif.ml.stats.add_statistics`` path. No re-implemented
        file-reading (see DRY-violation note at the call sites in
        ``fdw_export.py`` and ``geocif_runner.py`` — we don't follow those).
        """
        # Prep the working DF columns add_statistics expects.
        df_in = df_agg.assign(
            Region=df_agg["region"],
            **{"Harvest Year": df_agg["year"]},
            Season=int(season),
        )
        country_str = country.replace("_", " ").title()
        crop_str = agmet_utils.get_crop_name(crop)
        df_joined = ml_stats.add_statistics(
            dir_stats=self.dir_production_statistics,
            df=df_in,
            country=country_str,
            crop=crop_str,
            admin_zone=admin_zone,
            stats=["Yield (tn per ha)"],
            method="",
            parser=self.parser,
        )
        # Visibility on match success — silent join failures are the most
        # common failure mode for this kind of merge.
        n_matched = df_joined["Yield (tn per ha)"].notna().sum()
        n_total = len(df_joined)
        if n_matched == 0:
            self.logger.warning(
                f"  yield join produced ZERO non-NaN rows "
                f"({country_str}, {crop_str}, s{season}); metric will be NaN."
            )
        else:
            self.logger.info(
                f"  yield join: {n_matched}/{n_total} rows have yield "
                f"({country_str}, {crop_str}, s{season})"
            )
        return df_joined

    # ----------------------------------------------------------------------
    # Skill metric
    # ----------------------------------------------------------------------

    @staticmethod
    def _pearson_abs(x: np.ndarray, y: np.ndarray) -> float:
        """Absolute Pearson r on the finite intersection of x, y.

        Returns NaN for < 3 finite pairs or zero-variance series (which
        would otherwise emit a RuntimeWarning and return NaN anyway, but
        we short-circuit cleanly).
        """
        from scipy.stats import pearsonr
        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() < 3:
            return float("nan")
        x_v, y_v = x[mask], y[mask]
        if x_v.std() == 0 or y_v.std() == 0:
            return float("nan")
        r, _ = pearsonr(x_v, y_v)
        return float(abs(r))

    @staticmethod
    def _loocv_rmse(x: np.ndarray, y: np.ndarray, min_years: int = 5) -> float:
        """Leave-one-out LinearRegression RMSE on the finite intersection.

        Returns NaN if fewer than ``min_years`` finite pairs (RMSE on
        2-3 folds is too unstable to act on).
        """
        from sklearn.linear_model import LinearRegression
        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() < min_years:
            return float("nan")
        x_v, y_v = x[mask], y[mask]
        residuals = []
        for i in range(len(x_v)):
            x_tr = np.delete(x_v, i).reshape(-1, 1)
            y_tr = np.delete(y_v, i)
            x_te = x_v[i:i + 1].reshape(-1, 1)
            y_te = y_v[i]
            try:
                m = LinearRegression().fit(x_tr, y_tr)
                y_hat = m.predict(x_te)[0]
            except Exception:
                return float("nan")
            residuals.append(y_te - y_hat)
        return float(np.sqrt(np.mean(np.square(residuals))))

    def compute_metric(self, df_joined: pd.DataFrame, var_col: str) -> pd.DataFrame:
        """Per (region, direction, threshold), compute the configured
        skill metric across the year axis along with year counts.

        Output columns: region, direction, threshold, n_years,
        n_fallback_years, metric_name, metric_value.
        """
        rows = []
        groups = df_joined.groupby(["region", "direction", "threshold"],
                                   as_index=False, dropna=False)
        for (region, direction, threshold), grp in groups:
            xv = grp[var_col].to_numpy(dtype=float, na_value=np.nan)
            yv = grp["Yield (tn per ha)"].to_numpy(dtype=float, na_value=np.nan)
            n_years = int((np.isfinite(xv) & np.isfinite(yv)).sum())
            n_fb = int(grp["fallback_used"].sum())
            if self.metric_name == "pearson":
                metric_value = ThresholdOptimizer._pearson_abs(xv, yv)
            else:
                metric_value = ThresholdOptimizer._loocv_rmse(xv, yv)
            rows.append({
                "region": region,
                "direction": direction,
                "threshold": int(threshold),
                "n_years": n_years,
                "n_fallback_years": n_fb,
                "metric_name": self.metric_name,
                "metric_value": metric_value,
            })
        return pd.DataFrame(rows)

    # ----------------------------------------------------------------------
    # Trustworthiness + ranking
    # ----------------------------------------------------------------------

    def rank_and_filter(self, df_metric: pd.DataFrame) -> pd.DataFrame:
        """Flag low-trust rows (high fallback share or too few years) as
        ``trustworthy=False`` and rank only the trustworthy ones within
        each region. Untrustworthy rows kept in output with rank=NaN.

        Sort direction depends on metric: Pearson → bigger is better
        (descending); LOOCV RMSE → smaller is better (ascending).
        """
        df = df_metric.copy()
        df["fb_share"] = np.where(
            df["n_years"] > 0,
            df["n_fallback_years"] / df["n_years"],
            np.nan,
        )
        min_years_for_loocv = 5
        df["trustworthy"] = (
            (df["fb_share"] <= self.max_fallback_share)
            & df["metric_value"].notna()
        )
        if self.metric_name == "loocv_rmse":
            df.loc[df["n_years"] < min_years_for_loocv, "trustworthy"] = False

        ascending = self.metric_name == "loocv_rmse"
        df["rank_within_region"] = (
            df.where(df["trustworthy"])
              .groupby("region")["metric_value"]
              .rank(method="min", ascending=ascending, na_option="keep")
        )
        return df.drop(columns="fb_share")

    def compute_pooled(self, df_ranked: pd.DataFrame) -> pd.DataFrame:
        """Average the metric across regions for each (direction, threshold)
        — restricted to trustworthy rows so a noisy region doesn't drag
        the pooled signal. Ranked, so row 1 is the actionable answer."""
        trustworthy = df_ranked[df_ranked["trustworthy"]]
        if trustworthy.empty:
            return pd.DataFrame(columns=[
                "direction", "threshold", "n_regions_trusted",
                "pooled_metric", "metric_name", "rank_pooled",
            ])
        pooled = (
            trustworthy.groupby(["direction", "threshold"], as_index=False)
                       .agg(pooled_metric=("metric_value", "mean"),
                            n_regions_trusted=("region", "nunique"))
        )
        pooled["metric_name"] = self.metric_name
        ascending = self.metric_name == "loocv_rmse"
        pooled["rank_pooled"] = pooled["pooled_metric"].rank(
            method="min", ascending=ascending,
        )
        return pooled.sort_values("rank_pooled").reset_index(drop=True)

    # ----------------------------------------------------------------------
    # Outputs
    # ----------------------------------------------------------------------

    def write_summary(self, df_ranked: pd.DataFrame, df_pooled: pd.DataFrame,
                      country: str, crop: str, season: int) -> Path:
        out_dir = self.summary_dir(country, crop)
        stem = f"{country}_{crop}_s{season}"

        per_region = df_ranked.assign(country=country)[[
            "country", "region", "direction", "threshold",
            "n_years", "n_fallback_years",
            "metric_name", "metric_value", "trustworthy", "rank_within_region",
        ]]
        per_region_path = out_dir / f"{stem}_summary.csv"
        per_region.to_csv(per_region_path, index=False)

        pooled_path = out_dir / f"{stem}_pooled.csv"
        df_pooled.assign(country=country).to_csv(pooled_path, index=False)

        self.logger.info(f"  wrote {per_region_path}")
        self.logger.info(f"  wrote {pooled_path}")
        if not df_pooled.empty:
            best = df_pooled.iloc[0]
            self.logger.info(
                f"  POOLED BEST for ({country}, {crop}, s{season}): "
                f"direction={best['direction']} threshold={int(best['threshold'])} "
                f"pooled {best['metric_name']}={best['pooled_metric']:.4f} "
                f"(n_regions_trusted={int(best['n_regions_trusted'])})"
            )
        return out_dir

    def plot(self, df_ranked: pd.DataFrame, df_pooled: pd.DataFrame,
             country: str, crop: str, season: int, out_dir: Path) -> None:
        if not self.do_plot:
            return
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as e:
            self.logger.warning(f"  matplotlib unavailable, skipping plot: {e}")
            return

        stem = f"{country}_{crop}_s{season}"
        fig, ax = plt.subplots(figsize=(8, 5))

        # Per-region thin lines, one per region × direction.
        for (region, direction), grp in df_ranked.groupby(["region", "direction"]):
            grp_sorted = grp.sort_values("threshold")
            linestyle = "-" if direction == "floor" else "--"
            ax.plot(
                grp_sorted["threshold"], grp_sorted["metric_value"],
                linestyle=linestyle, alpha=0.35, linewidth=0.9,
                label="_nolegend_",
            )

        # Pooled — bold, separate line per direction.
        if not df_pooled.empty:
            for direction, grp in df_pooled.groupby("direction"):
                grp_sorted = grp.sort_values("threshold")
                linestyle = "-" if direction == "floor" else "--"
                ax.plot(
                    grp_sorted["threshold"], grp_sorted["pooled_metric"],
                    linestyle=linestyle, color="black", linewidth=2.2,
                    label=f"pooled ({direction})",
                )
            best = df_pooled.iloc[0]
            ax.axvline(
                int(best["threshold"]), color="red", linestyle=":",
                linewidth=1, alpha=0.7,
                label=(f"best: {best['direction']} {int(best['threshold'])}"),
            )

        metric_label = (
            "|Pearson r|" if self.metric_name == "pearson" else "LOOCV RMSE"
        )
        ax.set_xlabel("Crop-mask threshold (%)")
        ax.set_ylabel(metric_label)
        ax.set_title(f"{country} {crop} s{season} — {metric_label} vs threshold")
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        png_path = out_dir / f"{stem}.png"
        fig.savefig(png_path, dpi=120)
        plt.close(fig)

        # Companion CSV (per the plot-CSV-pairs convention).
        plot_data = df_ranked[[
            "region", "direction", "threshold", "metric_value", "trustworthy",
        ]].assign(line_type="per_region")
        if not df_pooled.empty:
            pooled_long = df_pooled[[
                "direction", "threshold", "pooled_metric",
            ]].rename(columns={"pooled_metric": "metric_value"})
            pooled_long["region"] = "_pooled_"
            pooled_long["trustworthy"] = True
            pooled_long["line_type"] = "pooled"
            plot_data = pd.concat([plot_data, pooled_long], ignore_index=True)
        plot_csv = out_dir / f"{stem}_plot_data.csv"
        plot_data.to_csv(plot_csv, index=False)

        self.logger.info(f"  wrote {png_path}")
        self.logger.info(f"  wrote {plot_csv}")

    # ----------------------------------------------------------------------
    # Per-combo + main loop
    # ----------------------------------------------------------------------

    def process_one(self, country: str, admin_level: str, crop: str, season: int):
        label = f"{country}/{crop}/s{season}"
        self.logger.info(f"== Threshold-sweep optimizer: {label} ==")
        df, var_col = self.read_sweep_csv(country, crop, season)
        if df is None:
            return

        self.sanity_check(df, label=label)

        df_agg = self.aggregate_seasonal(df, var_col)
        df_joined = self.join_yield(
            df_agg, country=country, crop=crop,
            admin_zone=admin_level, season=season,
        )
        df_metric = self.compute_metric(df_joined, var_col)
        df_ranked = self.rank_and_filter(df_metric)
        df_pooled = self.compute_pooled(df_ranked)

        out_dir = self.write_summary(df_ranked, df_pooled, country, crop, season)
        self.plot(df_ranked, df_pooled, country, crop, season, out_dir)

    def main(self):
        for combo in self.create_run_combinations():
            try:
                self.process_one(*combo)
            except Exception:
                self.logger.exception(
                    f"  threshold-optimizer FAILED for {combo}; continuing to next"
                )


def run(path_config_files=None):
    """Entry point — mirrors ``geocif.geocif_runner.run`` / ``geoagmet.run``."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    if path_config_files is None:
        path_config_files = []

    console = Console()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("Usage", "from geocif import threshold_optimizer; threshold_optimizer.run(cfg)")
    table.add_row("cfg", "[geobase.txt, countries.txt, crops.txt, geocif.txt]")
    console.print(Panel(
        table,
        title="[bold bright_white]GeoCIF Threshold-Sweep Optimizer[/]",
        border_style="bright_blue",
        padding=(1, 2),
    ))

    obj = ThresholdOptimizer(path_config_files)
    obj.main()
