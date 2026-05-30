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

Floor vs ceiling — different semantics, different production fates
--------------------------------------------------------------------
As of geoprepare 0.6.253, the two sweep directions have asymmetric
meanings AND different production-knob applicability:

  * ``floor``  T = keep cells with crop fraction > T% (absolute lower
                 bound, per-cell). Matches production geoextract's
                 ``[<country>] floor`` knob exactly (see
                 ``geoprepare/base.py:127-130``: ``limit_type = "floor"
                 if self.threshold else "ceil"``, masking always
                 evaluates ``afi_data >= limit*100``). The pooled-best
                 floor threshold is the actionable answer — paste it
                 verbatim as ``[<country>] floor = T``.

  * ``ceiling`` T = keep the top-T% of in-region cropland cells ranked
                 by crop fraction (rank-based / per-region quantile).
                 There is **no production geoextract knob with this
                 semantics** — ``[<country>] ceil`` in production is
                 still an absolute lower bound, not a rank percentile.
                 The ceiling-direction pooled-best is **analysis-only**:
                 useful for understanding how marginal-cropland inclusion
                 affects NDVI↔yield correlation, but NOT directly
                 transferable to a production-config setting.

Practical reading: scan the pooled CSV / log line for the floor row
with the highest |Pearson r|; that's your production threshold. Ceiling
rows are informative for understanding the signal-noise envelope but
do not have a one-to-one production mapping.
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
        """Sweep CSV lives at ``${dir_output}/threshold_sweep/{country}/
        {crop}/{country}_{crop}_s{season}_sweep.csv`` — same project-
        suffixed dir geoprepare.extract_sweep writes to (BaseGeo's
        parse_config sets ``dir_output = ${PATHS:dir_output} /
        {project_name}`` on BOTH sides, so the paths line up directly).

        An earlier version of this method stripped the project_name
        segment based on the wrong assumption that extract_sweep wrote
        to an un-suffixed root — verified false against Z: layout
        (Z:\\cmongp1\\GEO\\outputs\\geocif\\threshold_sweep\\...).
        """
        return (
            self.dir_output / "threshold_sweep" / country / crop
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
        # Empty-input guard: aggregate_seasonal can return 0 rows if the
        # sweep CSV was empty / malformed for this (country, crop, season).
        # Passing an empty df to add_statistics → add_GEOGLAM_statistics
        # crashes on `df.loc[:, stat] = np.nan` ("cannot set a frame with
        # no defined index and a scalar"). Short-circuit here.
        if df_agg.empty:
            self.logger.warning(
                f"  yield join: skipping ({country}, {crop}, s{season}) — "
                f"aggregated DF is empty (sweep CSV may have produced no rows)."
            )
            return df_agg.assign(**{"Yield (tn per ha)": np.nan})

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
            label=f"{country}/{crop}/s{season}",
        )
        # Defensive: add_statistics' hvstat-path process_group only adds
        # the Yield column to groups that find a matching FEWSNET row.
        # If NO group matched (e.g. Sudan winter_wheat — country/crop is
        # in HvStat but no rows pass the qc/PS filter for that admin),
        # the column never gets added and downstream code KeyErrors.
        # Backfill as all-NaN so the schema is stable.
        if "Yield (tn per ha)" not in df_joined.columns:
            df_joined = df_joined.assign(**{"Yield (tn per ha)": np.nan})

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
        # Column contract — always present in the returned DataFrame
        # even when df_joined has zero rows (groupby below produces no
        # groups, `pd.DataFrame([])` would otherwise return a 0×0 frame
        # and break rank_and_filter's `df["n_years"]` access).
        _METRIC_COLS = [
            "region", "direction", "threshold",
            "n_years", "n_fallback_years",
            "metric_name", "metric_value",
        ]
        # Empty / schema-incomplete guard — covers both
        # "no rows produced upstream" AND "yield column missing because
        # add_statistics' hvstat path matched nothing". Either way
        # there's no metric to compute.
        if df_joined.empty or "Yield (tn per ha)" not in df_joined.columns:
            return pd.DataFrame(columns=_METRIC_COLS)

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
        return pd.DataFrame(rows, columns=_METRIC_COLS)

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
        # Empty-input guard — when df_metric has the column contract but
        # zero rows (e.g. yield join produced no matched years), short-
        # circuit to a 0-row frame with the downstream columns added so
        # compute_pooled / write_summary / plot don't KeyError.
        if df.empty:
            df["trustworthy"] = pd.Series(dtype=bool)
            df["rank_within_region"] = pd.Series(dtype=float)
            return df
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
            best_t = int(best['threshold'])
            # Direction-specific interpretation — geoprepare 0.6.253+
            # made floor and ceiling semantically asymmetric. floor =
            # absolute lower bound (matches production geoextract.txt
            # [<country>] floor); ceiling = rank-based quantile, no
            # equivalent production knob.
            if best['direction'] == 'floor':
                interp = (
                    f"(absolute: keep cells with crop fraction > {best_t}%; "
                    f"paste as [<country>] floor = {best_t})"
                )
            else:
                interp = (
                    f"(rank-based: keep top {best_t}% of in-region cropland "
                    f"cells; ANALYSIS-ONLY — no production knob with this "
                    f"semantics)"
                )
            self.logger.info(
                f"  POOLED BEST for ({country}, {crop}, s{season}): "
                f"direction={best['direction']} threshold={best_t} "
                f"pooled {best['metric_name']}={best['pooled_metric']:.4f} "
                f"(n_regions_trusted={int(best['n_regions_trusted'])}) {interp}"
            )
        return out_dir

    def plot(self, df_ranked: pd.DataFrame, df_pooled: pd.DataFrame,
             country: str, crop: str, season: int, out_dir: Path) -> None:
        """Two-panel metric-vs-threshold plot.

        Floor and ceiling get separate panels because, as of geoprepare
        0.6.253, their x-axis units are NOT comparable:
          * floor   T = crop-fraction lower bound (absolute %).
          * ceiling T = top-T% of in-region cropland cells (rank quantile).
        Sharing a single x-axis (the pre-0.6.253 layout) silently fused
        two different unit systems on the same number line.

        Each panel keeps the original thin-per-region + bold-pooled
        pattern. The red best-threshold marker is drawn ONLY on the
        panel matching the pooled-best direction, so the visual cue
        and the actionable answer agree.
        """
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
        metric_label = (
            "|Pearson r|" if self.metric_name == "pearson" else "LOOCV RMSE"
        )
        fig, (ax_floor, ax_ceil) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

        # Pooled-best info (for the panel-specific axvline).
        best_direction = None
        best_threshold = None
        if not df_pooled.empty:
            best = df_pooled.iloc[0]
            best_direction = best["direction"]
            best_threshold = int(best["threshold"])

        # Per-direction sub-plot rendering — same per-region thin +
        # bold pooled pattern as before, just split across two axes.
        panels = {
            "floor": (
                ax_floor,
                "Floor threshold (%) — keep cells with crop fraction > T%",
                "absolute lower bound, matches production [<country>] floor",
            ),
            "ceiling": (
                ax_ceil,
                "Ceiling threshold (%) — keep top T% of in-region cells by rank",
                "rank-based quantile — ANALYSIS ONLY (no production knob)",
            ),
        }
        for direction, (ax, xlabel, subtitle) in panels.items():
            # Thin per-region lines for this direction.
            sub_ranked = df_ranked[df_ranked["direction"] == direction]
            for region, grp in sub_ranked.groupby("region"):
                grp_sorted = grp.sort_values("threshold")
                ax.plot(
                    grp_sorted["threshold"], grp_sorted["metric_value"],
                    linestyle="-", alpha=0.35, linewidth=0.9,
                    label="_nolegend_",
                )

            # Bold pooled line for this direction.
            sub_pooled = df_pooled[df_pooled["direction"] == direction] if not df_pooled.empty else pd.DataFrame()
            if not sub_pooled.empty:
                sub_pooled_sorted = sub_pooled.sort_values("threshold")
                ax.plot(
                    sub_pooled_sorted["threshold"],
                    sub_pooled_sorted["pooled_metric"],
                    linestyle="-", color="black", linewidth=2.2,
                    label="pooled",
                )

            # Best-threshold marker — only on the matching panel.
            if best_direction == direction and best_threshold is not None:
                ax.axvline(
                    best_threshold, color="red", linestyle=":",
                    linewidth=1.4, alpha=0.8,
                    label=f"best: {best_threshold}",
                )

            ax.set_xlabel(xlabel)
            ax.set_title(f"{direction}\n({subtitle})", fontsize=10)
            ax.grid(True, alpha=0.3)
            # Only draw the legend if any artist has a real label.
            _, labels = ax.get_legend_handles_labels()
            if labels:
                ax.legend(loc="best", fontsize=8)

        ax_floor.set_ylabel(metric_label)
        fig.suptitle(
            f"{country} {crop} s{season} — {metric_label} vs threshold "
            f"(geoprepare 0.6.253+ semantics)",
            fontsize=12,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.96])

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
    # Cross-country cumulative plot
    # ----------------------------------------------------------------------

    def cumulative_root(self) -> Path:
        """Top-level dir holding ALL per-country threshold_sweep_summary
        subdirs for this run. The cumulative plot lands here (one level
        above the per-country dirs since it spans them).
        """
        return (
            self.dir_output / "ml" / "analysis" / self.today_tag
            / "threshold_sweep_summary"
        )

    def _read_all_pooled_csvs(self):
        """Read every per-country ``*_pooled.csv`` under the cumulative
        root and concatenate into one long-form frame with country/crop/
        season columns derived from the path. Returns ``None`` when
        nothing is found (caller logs + bails)."""
        cum_root = self.cumulative_root()
        pooled_csvs = sorted(cum_root.glob("*/*/*_pooled.csv"))
        if not pooled_csvs:
            self.logger.warning(
                f"  cumulative outputs: no per-country pooled CSVs found under "
                f"{cum_root}; skipping."
            )
            return None

        frames = []
        for csv_path in pooled_csvs:
            try:
                df = pd.read_csv(csv_path)
            except Exception as exc:  # noqa: BLE001
                self.logger.warning(
                    f"  cumulative outputs: skipping unreadable {csv_path}: {exc}"
                )
                continue
            if df.empty:
                continue
            # Filename: {country}_{crop}_s{season}_pooled.csv. The
            # country/crop have underscores in some cases (e.g.
            # winter_wheat, united_states_of_america) so parse from the
            # path's parent dirs which are guaranteed clean.
            country_part = csv_path.parent.parent.name
            crop_part = csv_path.parent.name
            # Season: parse the s{N} from the stem.
            stem = csv_path.stem  # "<country>_<crop>_s<N>_pooled"
            try:
                season_token = stem.split("_s")[-1].split("_")[0]
                season_int = int(season_token)
            except (ValueError, IndexError):
                season_int = 1
            df = df.assign(
                country=country_part,
                crop=crop_part,
                season=season_int,
            )
            frames.append(df)
        if not frames:
            self.logger.warning(
                "  cumulative outputs: every pooled CSV was empty/unreadable; skipping."
            )
            return None

        return pd.concat(frames, ignore_index=True)

    def _write_one_cumulative_plot(self, df_combo, crop, season, plt) -> Path:
        """Two-panel cross-country plot for one (crop, season) combo.
        Returns the PNG path. ``plt`` is the already-imported matplotlib
        module (caller imports once and passes in so we don't reimport
        per combo).
        """
        cum_root = self.cumulative_root()
        ascending = self.metric_name == "loocv_rmse"
        metric_label = (
            "|Pearson r|" if self.metric_name == "pearson" else "LOOCV RMSE"
        )

        # Per-country best within this combo.
        best_per_country_dir = (
            df_combo.sort_values(
                ["country", "direction", "pooled_metric"],
                ascending=[True, True, ascending],
            )
            .groupby(["country", "direction"], as_index=False)
            .first()
        )

        countries_list = sorted(df_combo["country"].unique())
        cmap = plt.get_cmap("tab20")
        country_colour = {
            c: cmap(i % cmap.N) for i, c in enumerate(countries_list)
        }

        fig, (ax_floor, ax_ceil) = plt.subplots(
            1, 2, figsize=(16, 6), sharey=True,
        )
        panels = {
            "floor": (
                ax_floor,
                "Floor threshold (%) — keep cells with crop fraction > T%",
                "absolute lower bound, matches production [<country>] floor",
            ),
            "ceiling": (
                ax_ceil,
                "Ceiling threshold (%) — keep top T% of in-region cells by rank",
                "rank-based quantile — ANALYSIS ONLY (no production knob)",
            ),
        }
        for direction, (ax, xlabel, subtitle) in panels.items():
            sub = df_combo[df_combo["direction"] == direction]
            if sub.empty:
                ax.text(
                    0.5, 0.5, f"(no {direction} data)",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=11, alpha=0.6,
                )
                ax.set_xlabel(xlabel)
                ax.set_title(f"{direction}\n({subtitle})", fontsize=10)
                continue

            for country, grp in sub.groupby("country"):
                grp_sorted = grp.sort_values("threshold")
                ax.plot(
                    grp_sorted["threshold"], grp_sorted["pooled_metric"],
                    color=country_colour[country],
                    linewidth=1.2, alpha=0.75, label="_nolegend_",
                )

            best_sub = best_per_country_dir[best_per_country_dir["direction"] == direction]
            for _, row in best_sub.iterrows():
                ax.scatter(
                    row["threshold"], row["pooled_metric"],
                    color=country_colour[row["country"]],
                    s=40, zorder=5, edgecolor="black", linewidths=0.4,
                )
            # Annotate top-5 countries in this panel — by pooled_metric
            # at their own best (Pearson: max; LOOCV: min).
            top5 = (
                best_sub.sort_values("pooled_metric", ascending=ascending)
                        .head(5)
            )
            for _, row in top5.iterrows():
                ax.annotate(
                    row["country"],
                    xy=(row["threshold"], row["pooled_metric"]),
                    xytext=(4, 4), textcoords="offset points",
                    fontsize=8, alpha=0.9,
                )

            ax.set_xlabel(xlabel)
            ax.set_title(f"{direction}\n({subtitle})", fontsize=10)
            ax.grid(True, alpha=0.3)

        ax_floor.set_ylabel(metric_label)
        fig.suptitle(
            f"Cross-country cumulative — {crop} season {season} — {metric_label} "
            f"(n={len(countries_list)} countries; top-5 per panel annotated)",
            fontsize=11,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.95])

        png_path = cum_root / f"cumulative_{crop}_s{season}.png"
        fig.savefig(png_path, dpi=130)
        plt.close(fig)
        return png_path

    def _write_one_cumulative_table(self, df_combo, crop, season, plt):
        """Matplotlib-rendered table image for one (crop, season).
        Returns (png_path, csv_path). Columns:
        Country | Floor T | Floor metric | Ceiling T | Ceiling metric |
        Pick | Apply.

        Sorted by max(floor, ceiling) descending for Pearson, ascending
        for LOOCV RMSE — best countries at the top.
        """
        cum_root = self.cumulative_root()
        ascending = self.metric_name == "loocv_rmse"
        metric_label = (
            "|r|" if self.metric_name == "pearson" else "RMSE"
        )

        # Per-country best per direction within this combo.
        best = (
            df_combo.sort_values(
                ["country", "direction", "pooled_metric"],
                ascending=[True, True, ascending],
            )
            .groupby(["country", "direction"], as_index=False)
            .first()
        )
        # Pivot to one row per country, with floor / ceiling side-by-side.
        floor = best[best["direction"] == "floor"][
            ["country", "threshold", "pooled_metric"]
        ].rename(columns={"threshold": "floor_T", "pooled_metric": "floor_metric"})
        ceil = best[best["direction"] == "ceiling"][
            ["country", "threshold", "pooled_metric"]
        ].rename(columns={"threshold": "ceil_T", "pooled_metric": "ceil_metric"})
        table_df = floor.merge(ceil, on="country", how="outer")

        # Pick = direction with the better metric (or whichever exists
        # if only one side has data).
        def _pick(row):
            f_ok = pd.notna(row["floor_metric"])
            c_ok = pd.notna(row["ceil_metric"])
            if f_ok and c_ok:
                if ascending:
                    return "floor" if row["floor_metric"] <= row["ceil_metric"] else "ceiling"
                return "floor" if row["floor_metric"] >= row["ceil_metric"] else "ceiling"
            if f_ok:
                return "floor"
            if c_ok:
                return "ceiling"
            return "—"
        table_df["pick"] = table_df.apply(_pick, axis=1)

        def _apply(row):
            if row["pick"] == "floor" and pd.notna(row.get("floor_T")):
                return f"floor = {int(row['floor_T'])}"
            if row["pick"] == "ceiling":
                return "ANALYSIS-ONLY"
            return "—"
        table_df["apply"] = table_df.apply(_apply, axis=1)

        # Sort by the better-of-the-two metric so the best countries
        # are at the top of the table.
        if ascending:
            table_df["sort_key"] = table_df[["floor_metric", "ceil_metric"]].min(axis=1)
            table_df = table_df.sort_values("sort_key", ascending=True, na_position="last")
        else:
            table_df["sort_key"] = table_df[["floor_metric", "ceil_metric"]].max(axis=1)
            table_df = table_df.sort_values("sort_key", ascending=False, na_position="last")
        table_df = table_df.drop(columns="sort_key").reset_index(drop=True)

        # Render matplotlib table.
        n_rows = len(table_df)
        fig_height = max(2.5, 0.32 * n_rows + 1.2)
        fig, ax = plt.subplots(figsize=(11, fig_height))
        ax.axis("off")
        ax.set_title(
            f"Cross-country best thresholds — {crop} season {season} "
            f"(metric: {metric_label})",
            fontsize=12, pad=12,
        )

        col_labels = [
            "Country", f"Floor T", f"Floor {metric_label}",
            f"Ceiling T", f"Ceiling {metric_label}",
            "Pick", "Apply (production geoextract.txt)",
        ]
        cell_text = []
        for _, row in table_df.iterrows():
            cell_text.append([
                str(row["country"]),
                "—" if pd.isna(row["floor_T"]) else str(int(row["floor_T"])),
                "—" if pd.isna(row["floor_metric"]) else f"{row['floor_metric']:.3f}",
                "—" if pd.isna(row["ceil_T"]) else str(int(row["ceil_T"])),
                "—" if pd.isna(row["ceil_metric"]) else f"{row['ceil_metric']:.3f}",
                row["pick"],
                row["apply"],
            ])
        if not cell_text:
            cell_text = [["(no data)" for _ in col_labels]]
        tbl = ax.table(
            cellText=cell_text, colLabels=col_labels,
            cellLoc="center", loc="center",
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1.0, 1.2)
        # Highlight header.
        for j in range(len(col_labels)):
            cell = tbl[(0, j)]
            cell.set_facecolor("#2b6cb0")
            cell.set_text_props(color="white", weight="bold")
        # Light-highlight rows where pick=floor (actionable) vs ceiling.
        for i, row in table_df.iterrows():
            colour = "#e6fffa" if row["pick"] == "floor" else "#fff5f5"
            for j in range(len(col_labels)):
                tbl[(i + 1, j)].set_facecolor(colour)

        fig.tight_layout()
        png_path = cum_root / f"cumulative_{crop}_s{season}_table.png"
        fig.savefig(png_path, dpi=140, bbox_inches="tight")
        plt.close(fig)

        # Companion CSV — the same data behind the image.
        csv_path = cum_root / f"cumulative_{crop}_s{season}_table.csv"
        table_df.to_csv(csv_path, index=False)
        return png_path, csv_path

    def write_cumulative_outputs(self) -> None:
        """Cross-country cumulative outputs — one plot + one table image
        + their companion CSVs PER (crop, season) combo.

        Each combo's plot has one line per country (national-scale,
        pooled-across-regions). Each combo's table shows per-country
        floor & ceiling best, the pick, and a paste-ready production
        knob string. A top-level ``lookup_cumulative.csv`` maps every
        plot/table to its companion CSV per the plot-CSV-pairs rule.

        Crop × season is preserved as the splitting axis — NDVI-wheat
        and NDVI-rice tell different stories and shouldn't share a
        chart.
        """
        if not self.do_plot:
            return

        all_pooled = self._read_all_pooled_csvs()
        if all_pooled is None or all_pooled.empty:
            return

        # Companion long-form table — full series identification per
        # plot-CSV-pairs. Mirrors the schema of the previous
        # cumulative_all_countries_plot_data.csv but split per combo
        # via the lookup CSV below.
        ascending = self.metric_name == "loocv_rmse"
        best_per_country_dir = (
            all_pooled.sort_values(
                ["country", "crop", "season", "direction", "pooled_metric"],
                ascending=[True, True, True, True, ascending],
            )
            .groupby(["country", "crop", "season", "direction"], as_index=False)
            .first()
        )

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  cumulative outputs: matplotlib unavailable: {exc}"
            )
            return

        cum_root = self.cumulative_root()
        combos = sorted(set(zip(all_pooled["crop"], all_pooled["season"])))
        lookup_rows = []
        for crop, season in combos:
            df_combo = all_pooled[
                (all_pooled["crop"] == crop) & (all_pooled["season"] == season)
            ].copy()
            if df_combo.empty:
                continue

            # Plot
            png_plot = self._write_one_cumulative_plot(df_combo, crop, season, plt)
            # Plot's companion CSV
            best_keys = set(zip(
                best_per_country_dir["country"], best_per_country_dir["crop"],
                best_per_country_dir["season"], best_per_country_dir["direction"],
                best_per_country_dir["threshold"].astype(int),
            ))
            plot_data = df_combo[[
                "country", "crop", "season", "direction", "threshold",
                "pooled_metric", "n_regions_trusted", "metric_name",
            ]].copy()
            plot_data["is_best"] = [
                (c, cr, int(s), d, int(t)) in best_keys
                for c, cr, s, d, t in zip(
                    plot_data["country"], plot_data["crop"], plot_data["season"],
                    plot_data["direction"], plot_data["threshold"],
                )
            ]
            csv_plot = cum_root / f"cumulative_{crop}_s{season}_plot_data.csv"
            plot_data.to_csv(csv_plot, index=False)

            # Table image + its companion CSV
            png_table, csv_table = self._write_one_cumulative_table(
                df_combo, crop, season, plt,
            )

            lookup_rows.extend([
                {"crop": crop, "season": int(season), "kind": "plot",
                 "image": png_plot.name, "data_csv": csv_plot.name},
                {"crop": crop, "season": int(season), "kind": "table",
                 "image": png_table.name, "data_csv": csv_table.name},
            ])
            self.logger.info(
                f"  wrote {png_plot.name} + {csv_plot.name} "
                f"+ {png_table.name} + {csv_table.name}"
            )

        # Lookup CSV — maps every plot/table to its data csv at one
        # glance, per the plot-CSV-pairs convention's "lookup table"
        # requirement (see memory: feedback_plot_csv_pairs.md).
        if lookup_rows:
            lookup_path = cum_root / "lookup_cumulative.csv"
            pd.DataFrame(lookup_rows).to_csv(lookup_path, index=False)
            self.logger.info(f"  wrote {lookup_path}")

        self.logger.info(
            f"  cumulative outputs: {len(combos)} (crop, season) combos × "
            f"{all_pooled['country'].nunique()} countries"
        )

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
        import traceback
        for combo in self.create_run_combinations():
            try:
                self.process_one(*combo)
            except Exception as exc:  # noqa: BLE001
                # geocif's custom Logger doesn't expose `.exception()`;
                # use `.error()` + a manually formatted traceback so the
                # loop survives and the user can see which combo failed.
                self.logger.error(
                    f"  threshold-optimizer FAILED for {combo}: "
                    f"{type(exc).__name__}: {exc}\n"
                    + traceback.format_exc()
                )
        # Cross-country cumulative outputs — runs once after all
        # per-combo work; reads back the per-country pooled CSVs and
        # emits one plot + one table image (+ companion CSVs) PER
        # (crop, season) combo at the top of threshold_sweep_summary/,
        # plus a lookup CSV mapping plots/tables to data CSVs.
        try:
            self.write_cumulative_outputs()
        except Exception as exc:  # noqa: BLE001
            self.logger.error(
                f"  cumulative outputs FAILED: {type(exc).__name__}: {exc}\n"
                + traceback.format_exc()
            )


def run(path_config_files=None):
    """Entry point — mirrors ``geocif.geocif_runner.run`` / ``geoagmet.run``.

    Parses the config first so the startup banner can surface the
    actual countries / crops / paths / key knobs being used. Each square
    bracket in a Rich Table cell is escaped with ``\\[`` because Rich
    treats ``[...]`` as inline-style markup otherwise (this was the bug
    that made the old "cfg" row render empty).
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    if path_config_files is None:
        path_config_files = []

    # Parse first so the banner can show the real config values.
    obj = ThresholdOptimizer(path_config_files)

    from geocif import __version__ as _geocif_version

    # Crops: per-country lists from the config, deduped + sorted.
    all_crops = set()
    for country in obj.countries:
        if obj.parser.has_option(country, "crops"):
            try:
                all_crops.update(ast.literal_eval(obj.parser.get(country, "crops")))
            except (ValueError, SyntaxError):
                pass
    crops_str = ", ".join(sorted(all_crops)) if all_crops else "(none configured)"

    # Paths the user cares about.
    sweep_input_root = obj.dir_output / "threshold_sweep"
    summary_output_root = (
        obj.dir_output / "ml" / "analysis" / obj.today_tag
        / "threshold_sweep_summary"
    )

    def _esc(s):
        # Escape opening brackets so Rich doesn't eat them as markup.
        return str(s).replace("[", r"\[")

    console = Console()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("Version", f"geocif {_geocif_version}")
    table.add_row(
        "Usage",
        r"from geocif import threshold_optimizer; threshold_optimizer.run(cfg)",
    )
    table.add_row("Countries", _esc(", ".join(obj.countries) or "(none)"))
    table.add_row("Crops", _esc(crops_str))
    table.add_row("agg_method", obj.agg_method)
    table.add_row("metric", obj.metric_name)
    table.add_row("max_fallback_share", str(obj.max_fallback_share))
    table.add_row("plot", str(obj.do_plot))
    table.add_row("Sweep input root", _esc(sweep_input_root))
    table.add_row("Summary output", _esc(summary_output_root))
    console.print(Panel(
        table,
        title="[bold bright_white]GeoCIF Threshold-Sweep Optimizer[/]",
        border_style="bright_blue",
        padding=(1, 2),
    ))

    obj.main()
