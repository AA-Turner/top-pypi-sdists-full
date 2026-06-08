"""Per-cell EO mask optimizer — consumer for ``geoprepare.extract_cells``.

Threshold-sweep optimizes a single absolute or rank-based threshold T
applied uniformly to all cropland cells in a region. This module asks a
different question: forget the uniform threshold — for each cell
independently, should it be IN or OUT of the seasonal aggregate? Find
the binary cell mask that maximizes the LOOCV-validated multivariate
fit between yield and the seasonal aggregates of NDVI / tmax / tmin /
precip taken over the selected cells.

Pipeline per (country, crop, season, region)::

    1. Load the per-cell parquet emitted by extract_cells.
    2. Collapse the DOY axis to a seasonal value per cell × year × var
       (NDVI = max, tmax/tmin/precip = mean — same agg policy as
       threshold_optimizer).
    3. Join yield via geocif.ml.stats.add_statistics (the canonical
       AMIS-aware path; the Jun 2026 region-normalization + synonym
       fixes apply here for free).
    4. Run a binary-genome GA over the cells, maximizing the fitness
            f(mask) = LOOCV_R²(yield ~ aggregated{NDVI, T, P}) − λ·share
       where ``share = mask.mean()`` and ``λ`` is the L0 penalty. A
       MIN_CELLS floor (max(20, 5 % of n_cells)) prevents degenerate
       1-cell solutions.
    5. Write outputs: best_mask.npy, history.csv, mask_map.png,
       fitness_history.png, pre_post.png + a cross-region summary CSV.

Design decisions locked 2026-06-07 in chat with the user:
  * Single shared mask across NDVI / T / P (one mask says "these are the
    cells that represent the crop here"; cleaner physics than per-var
    masks; one extraction + one experiment).
  * Fitness = LOOCV R² of yield ~ {NDVI, T, P} from a multivariate
    linear regression — validated against held-out years, captures the
    joint signal, bounded above by 1.0.
  * L0 penalty + MIN_CELLS floor (lighter than spatial-smoothness;
    nested CV deferred until we want to publish generalization claims).
  * First end-to-end test = single region (india/maize/madhya_pradesh).

The contract this module reads against — parquet columns the upstream
``extract_cells`` must write — is documented in the
``CellOptimizer.cells_parquet_path`` docstring and on the loader
(``CellOptimizer.load_region``).
"""
from __future__ import annotations

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import arrow as ar
import numpy as np
import pandas as pd

from geoprepare import base

from geocif.agmet import utils as agmet_utils
from geocif.ml import stats as ml_stats


# Columns the parquet MUST carry (var columns are gated by config).
_REQUIRED_COLS = frozenset({
    "country", "region", "region_id", "cell_id",
    "lat", "lon", "afi", "year", "doy",
})

# Variables the GA can use. Order matters only for output column order.
_VAR_COLS = ("ndvi", "tmax", "tmin", "precip")

# Aggregation per variable when collapsing the DOY axis to a seasonal
# value. NDVI tracks peak greenness (max); T and P are accumulated /
# averaged over the season (mean). Matches threshold_optimizer's policy
# for NDVI; T/P are new and the mean is the conservative default.
_DOY_AGG = {
    "ndvi":   "max",
    "tmax":   "mean",
    "tmin":   "mean",
    "precip": "mean",
}


# ----------------------------------------------------------------------
# Pure-function fitness primitives — unit-testable in isolation
# ----------------------------------------------------------------------


def aggregate_over_mask(
    per_cell: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    """Average a (n_cells, n_years, n_vars) array along the cells axis
    using a boolean mask. Returns (n_years, n_vars).

    Returns an all-NaN frame if the mask is empty so callers don't have
    to special-case it (the LOOCV path will then return NaN naturally).
    """
    if mask.sum() == 0:
        return np.full(per_cell.shape[1:], np.nan, dtype=float)
    sel = per_cell[mask]                       # (n_sel, n_years, n_vars)
    return np.nanmean(sel, axis=0)             # (n_years, n_vars)


def loocv_r2_multivariate(
    x: np.ndarray,
    y: np.ndarray,
    min_years: int = 5,
) -> float:
    """Leave-one-out R² of ``y ~ X`` via OLS. ``x`` is (n_years, n_vars),
    ``y`` is (n_years,). Returns NaN if too few finite paired years.

    R² here is the coefficient of determination on the held-out
    predictions, computed against the mean of the FULL y series. Same
    flavour as sklearn's ``cross_val_score(scoring='r2')`` with
    LeaveOneOut, hand-coded to avoid the sklearn import overhead inside
    a GA inner loop that runs thousands of times.
    """
    from sklearn.linear_model import LinearRegression

    if x.ndim != 2 or y.ndim != 1 or x.shape[0] != y.shape[0]:
        return float("nan")

    finite_mask = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    if finite_mask.sum() < min_years:
        return float("nan")

    xf, yf = x[finite_mask], y[finite_mask]
    n = xf.shape[0]
    preds = np.empty(n, dtype=float)
    for i in range(n):
        idx = np.arange(n) != i
        try:
            m = LinearRegression().fit(xf[idx], yf[idx])
            preds[i] = m.predict(xf[i : i + 1])[0]
        except Exception:
            return float("nan")

    y_mean = yf.mean()
    ss_res = float(np.sum((yf - preds) ** 2))
    ss_tot = float(np.sum((yf - y_mean) ** 2))
    if ss_tot == 0.0:
        return float("nan")
    return 1.0 - ss_res / ss_tot


def fitness(
    mask: np.ndarray,
    per_cell: np.ndarray,
    y: np.ndarray,
    lam: float,
    min_cells: int,
) -> float:
    """GA objective. Negative-infinity when the mask violates the
    MIN_CELLS floor, which keeps tournament selection from ever picking
    a degenerate genome. Otherwise LOOCV R² minus the L0 share penalty.
    """
    sel = int(mask.sum())
    if sel < min_cells:
        return float("-inf")
    x = aggregate_over_mask(per_cell, mask)
    r2 = loocv_r2_multivariate(x, y)
    if not np.isfinite(r2):
        return float("-inf")
    return r2 - lam * (sel / mask.size)


# ----------------------------------------------------------------------
# GA primitives
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class GAConfig:
    """All tunables in one place. Defaults reflect the 2026-06-07 plan
    update: stronger parsimony pressure (l0_lambda 0.02→0.05), tighter
    min-cell floor (0.05→0.01 of cropland cells), AFI-as-prior init."""

    population_size: int = 100
    n_generations: int = 200
    tournament_k: int = 3
    crossover_p: float = 0.5     # uniform crossover bit-swap probability
    mutation_rate: Optional[float] = None  # None → 2 / n_cells (see init_population)
    elitism: int = 5
    early_stop_patience: int = 30
    l0_lambda: float = 0.05      # ↑ from 0.02: stronger parsimony pressure
    min_cell_floor_abs: int = 20
    min_cell_floor_frac: float = 0.01    # ↓ from 0.05: allow finer-grained selections
    init_inclusion_prob: float = 0.5     # fallback when afi prior is disabled
    afi_prior_beta: float = 1.0          # 0 → no prior (uniform 0.5); 1 → P = afi/100 clipped
    seed: Optional[int] = None           # set for reproducibility


@dataclass
class GAResult:
    """Wraps the final state + history. Plots and CSV writers read from
    this directly so callers don't shuttle individual arrays around."""

    best_mask: np.ndarray            # (n_cells,) bool
    best_fitness: float
    best_r2: float                   # fitness without the L0 penalty
    history: pd.DataFrame            # columns: generation, best_fit, mean_fit, best_r2, n_selected
    n_cells: int
    n_generations_run: int
    baseline_r2: float               # LOOCV R² with mask = all-True (no selection)


def init_prob_from_afi(
    afi: np.ndarray,
    beta: float = 1.0,
    p_min: float = 0.1,
    p_max: float = 0.9,
) -> np.ndarray:
    """Per-cell inclusion probability for the seed population, biased by
    cropland fraction (AFI as prior).

    The plan called this "linear: P = afi/100 clipped to [0.1, 0.9]" at
    beta=1. The general form scales the bias strength: beta=0 returns
    uniform 0.5 (no prior, current default-of-defaults); beta=1 returns
    P = afi/100 clipped; beta>1 pushes high-AFI cells toward p_max and
    low-AFI cells toward p_min more aggressively (sigmoid-like).

    Parameters
    ----------
    afi : (n_cells,) float, percent in [0, 100]
    beta : bias strength. 0 disables the prior.
    p_min, p_max : clipping bounds so no cell starts at probability 0 or 1
        (always keep some chance of either inclusion or exclusion at gen 0).

    Returns
    -------
    prob : (n_cells,) float in [p_min, p_max].
    """
    afi = np.asarray(afi, dtype=float)
    if beta == 0:
        return np.full(afi.shape, 0.5, dtype=float)
    centered = (afi / 100.0) - 0.5          # in [-0.5, 0.5] if afi in [0, 100]
    prob = 0.5 + beta * centered            # at beta=1 this is just afi/100
    return np.clip(prob, p_min, p_max).astype(float)


def _tournament_select(
    pop: np.ndarray, fits: np.ndarray, k: int, rng: np.random.Generator,
) -> np.ndarray:
    """Pick one parent via k-way tournament. Returns the picked genome."""
    idx = rng.integers(0, pop.shape[0], size=k)
    winner = idx[np.argmax(fits[idx])]
    return pop[winner].copy()


def _uniform_crossover(
    a: np.ndarray, b: np.ndarray, p: float, rng: np.random.Generator,
) -> np.ndarray:
    """Per-bit uniform crossover. p is the probability of taking a bit
    from parent b (so p=0.5 is a fair coin flip per bit)."""
    pick_b = rng.random(a.shape) < p
    child = a.copy()
    child[pick_b] = b[pick_b]
    return child


def _mutate(
    g: np.ndarray, p: float, rng: np.random.Generator,
) -> np.ndarray:
    """Bit-flip mutation with per-bit probability p."""
    flip = rng.random(g.shape) < p
    return np.logical_xor(g, flip)


def run_ga(
    per_cell: np.ndarray,
    y: np.ndarray,
    cfg: GAConfig = GAConfig(),
    afi: Optional[np.ndarray] = None,
    logger: Optional[logging.Logger] = None,
) -> GAResult:
    """Run the GA over a binary cell mask. ``per_cell`` is shape
    (n_cells, n_years, n_vars); ``y`` is (n_years,); ``afi`` is the
    per-cell cropland fraction in [0, 100] used as a *prior on initial
    inclusion probability* (does not enter the fitness function).

    When ``afi`` is None, the seed population uses a uniform
    ``cfg.init_inclusion_prob`` per bit (backwards-compatible default
    for synthetic tests that have no AFI). When supplied, cell c starts
    in genome g with probability ``init_prob_from_afi(afi, beta)[c]``.

    The fitness function calls ``loocv_r2_multivariate`` once per
    genome per generation — that's ~population_size × n_generations
    LOOCV evaluations. For 100 × 200 = 20k LOOCV fits with n_years≈25
    each, expect ~30–60 s per region on a single core. The runner
    parallelizes across regions via joblib; within-region parallelism
    is left for later (the GA step is sequential by design — tournament
    selection needs all fitnesses before it can build the next gen).
    """
    rng = np.random.default_rng(cfg.seed)
    n_cells = per_cell.shape[0]
    pop_size = cfg.population_size

    min_cells = max(cfg.min_cell_floor_abs, int(np.ceil(cfg.min_cell_floor_frac * n_cells)))
    mut_rate = cfg.mutation_rate if cfg.mutation_rate is not None else 2.0 / n_cells

    # Baseline: all cells included (no selection). Reported alongside
    # the GA's best to quantify lift.
    baseline_mask = np.ones(n_cells, dtype=bool)
    baseline_r2 = loocv_r2_multivariate(
        aggregate_over_mask(per_cell, baseline_mask), y
    )

    # Per-cell inclusion probability for the seed population. When AFI
    # is given and afi_prior_beta != 0, high-AFI cells start "in" more
    # often than low-AFI cells. Otherwise fall back to the scalar
    # init_inclusion_prob (uniform Bernoulli per bit).
    if afi is not None and cfg.afi_prior_beta != 0:
        prob = init_prob_from_afi(afi, beta=cfg.afi_prior_beta)
    else:
        prob = np.full(n_cells, cfg.init_inclusion_prob, dtype=float)

    # Seed population: Bernoulli(prob[c]) per (genome, cell), then
    # repair to the min-cell floor by force-including extra random
    # cells. Pure-random init can land below the floor; -inf fitness
    # wastes generations.
    pop = rng.random((pop_size, n_cells)) < prob[None, :]
    for i in range(pop_size):
        if pop[i].sum() < min_cells:
            off = np.flatnonzero(~pop[i])
            need = min_cells - pop[i].sum()
            pop[i, rng.choice(off, size=need, replace=False)] = True

    fits = np.array([fitness(g, per_cell, y, cfg.l0_lambda, min_cells) for g in pop])

    history_rows = []
    best_seen = -np.inf
    stagnant = 0

    for gen in range(cfg.n_generations):
        # Track stats
        cur_best_idx = int(np.argmax(fits))
        cur_best = float(fits[cur_best_idx])
        cur_mean = float(np.mean(fits[np.isfinite(fits)])) if np.isfinite(fits).any() else float("nan")
        best_mask_now = pop[cur_best_idx]
        cur_r2 = loocv_r2_multivariate(
            aggregate_over_mask(per_cell, best_mask_now), y
        )
        history_rows.append({
            "generation":  gen,
            "best_fit":    cur_best,
            "mean_fit":    cur_mean,
            "best_r2":     cur_r2,
            "n_selected":  int(best_mask_now.sum()),
        })

        if logger is not None and (gen % 25 == 0 or gen == cfg.n_generations - 1):
            logger.info(
                f"  gen {gen:>4d}/{cfg.n_generations}: best_fit={cur_best:.4f} "
                f"best_r2={cur_r2:.4f} mean_fit={cur_mean:.4f} "
                f"n_selected={int(best_mask_now.sum())}/{n_cells}"
            )

        # Early stop
        if cur_best > best_seen + 1e-6:
            best_seen = cur_best
            stagnant = 0
        else:
            stagnant += 1
            if stagnant >= cfg.early_stop_patience:
                if logger is not None:
                    logger.info(
                        f"  early-stop at gen {gen}: no improvement for "
                        f"{stagnant} generations"
                    )
                break

        # Build next population: elitism + tournament-selected offspring
        elite_idx = np.argsort(fits)[-cfg.elitism:][::-1]
        new_pop = [pop[i].copy() for i in elite_idx]
        while len(new_pop) < pop_size:
            p1 = _tournament_select(pop, fits, cfg.tournament_k, rng)
            p2 = _tournament_select(pop, fits, cfg.tournament_k, rng)
            child = _uniform_crossover(p1, p2, cfg.crossover_p, rng)
            child = _mutate(child, mut_rate, rng)
            new_pop.append(child)
        pop = np.asarray(new_pop, dtype=bool)
        fits = np.array([fitness(g, per_cell, y, cfg.l0_lambda, min_cells) for g in pop])

    # Final pick
    final_idx = int(np.argmax(fits))
    best_mask = pop[final_idx].copy()
    best_fit = float(fits[final_idx])
    best_r2 = loocv_r2_multivariate(
        aggregate_over_mask(per_cell, best_mask), y
    )

    return GAResult(
        best_mask=best_mask,
        best_fitness=best_fit,
        best_r2=best_r2 if np.isfinite(best_r2) else float("nan"),
        history=pd.DataFrame(history_rows),
        n_cells=n_cells,
        n_generations_run=len(history_rows),
        baseline_r2=baseline_r2 if np.isfinite(baseline_r2) else float("nan"),
    )


# ----------------------------------------------------------------------
# BaseGeo-integrated runner
# ----------------------------------------------------------------------


class CellOptimizer(base.BaseGeo):
    """Top-level orchestrator. Mirrors ThresholdOptimizer's structure
    so the runner / paths / config conventions line up with the rest
    of the geocif pipeline (logger, today_tag, dir_output, etc.).
    """

    def __init__(self, path_config_file):
        super().__init__(path_config_file)
        # Store original config-file paths so joblib workers can
        # re-instantiate this class inside their own processes (BaseGeo
        # holds an open log handle that doesn't survive pickling).
        self._config_files = path_config_file
        self.parse_config()

    def _get(self, option, default, sections=("CELL_OPTIMIZER", "DEFAULT")):
        """Read an option from the first section that has it."""
        for section in sections:
            if self.parser.has_option(section, option):
                return self.parser.get(section, option)
        return default

    def parse_config(self, section="DEFAULT"):
        self.project_name = self.parser.get("DEFAULT", "project_name")
        super().parse_config(project_name=self.project_name, section="DEFAULT")

        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.today_tag = ar.now().format("MMMM_DD_YYYY")

        # GA tunables — all optional, safe defaults from GAConfig.
        defaults = GAConfig()
        self.ga = GAConfig(
            population_size=int(self._get("population_size", defaults.population_size)),
            n_generations=int(self._get("n_generations", defaults.n_generations)),
            tournament_k=int(self._get("tournament_k", defaults.tournament_k)),
            crossover_p=float(self._get("crossover_p", defaults.crossover_p)),
            mutation_rate=(
                float(self._get("mutation_rate", "nan")) if self._get("mutation_rate", "") else None
            ),
            elitism=int(self._get("elitism", defaults.elitism)),
            early_stop_patience=int(self._get("early_stop_patience", defaults.early_stop_patience)),
            l0_lambda=float(self._get("l0_lambda", defaults.l0_lambda)),
            min_cell_floor_abs=int(self._get("min_cell_floor_abs", defaults.min_cell_floor_abs)),
            min_cell_floor_frac=float(self._get("min_cell_floor_frac", defaults.min_cell_floor_frac)),
            init_inclusion_prob=float(self._get("init_inclusion_prob", defaults.init_inclusion_prob)),
            afi_prior_beta=float(self._get("afi_prior_beta", defaults.afi_prior_beta)),
            seed=int(self._get("seed", "0")) if self._get("seed", "") else None,
        )
        # Runner-level knobs (not GA inner-loop hyperparams).
        self.n_jobs = int(self._get("n_jobs", "-1"))
        self.write_production_mask = self._get(
            "write_production_mask", "True"
        ).strip().lower() in ("true", "1", "yes")
        self.do_plot = self._get("plot", "True").strip().lower() in (
            "true", "1", "yes",
        )

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    def cells_parquet_path(self, country: str, crop: str, season: int) -> Path:
        """Per-region parquet contract — must match what
        ``geoprepare.extract_cells`` writes:

            ${dir_output}/cell_optimizer/{country}/{crop}/
                {country}_{crop}_s{season}_cells.parquet

        Schema (long-format, one row per cell × year × doy):
            country, region, region_id, cell_id, lat, lon, afi,
            year, doy, <var columns gated by [CELL_OPTIMIZER] variables>

        ``cell_id`` must be stable across years and doys for the same
        region (linear index into the region's read window). The set of
        cell_ids in a region must be identical for every (year, doy)
        slice — the GA aggregates along the time axis per cell.

        Cropland filter: the contract requires geoprepare to emit only
        cells with afi > 0 (cropland subset). ``load_region`` also
        applies this filter defensively, so n_cells inside the GA is
        always the cropland-cell count — the right denominator for the
        min-cell floor and the L0 share penalty.
        """
        return (
            self.dir_output / "cell_optimizer" / country / crop
            / f"{country}_{crop}_s{season}_cells.parquet"
        )

    def summary_dir(self, country: str, crop: str) -> Path:
        d = (
            self.dir_output / "ml" / "analysis" / self.today_tag
            / "cell_optimizer" / country / crop
        )
        d.mkdir(parents=True, exist_ok=True)
        return d

    def regions_dir(self, country: str, crop: str, season: int) -> Path:
        d = self.summary_dir(country, crop) / f"regions_s{season}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def cross_region_dir(self) -> Path:
        d = (
            self.dir_output / "ml" / "analysis" / self.today_tag
            / "cell_optimizer" / "_cross_region"
        )
        d.mkdir(parents=True, exist_ok=True)
        return d

    def production_mask_path(self, country: str, crop: str, season: int) -> Path:
        """Stable (no date-stamp) production output that geoextract reads
        to apply the GA-optimized mask during EO extraction. New runs
        overwrite. The path is a sibling to the extract_cells input so
        geoextract finds inputs and the optimized mask in one tree.

        Schema (one row per region × cell):
            country, region, region_id, cell_id, lat, lon, afi,
            included (bool), optimizer_version, optimized_at (ISO date)

        Geoextract integration (to be implemented on their side):
        when extracting EO for (country, crop, region, season), look up
        this file. If present, build the cropland mask from the
        ``included`` column instead of from a uniform AFI threshold.
        Key match is by cell_id, which is the linear index into the
        region's read window — same ordering as
        ``geoprepare.extract_cells`` emits.
        """
        return (
            self.dir_output / "cell_optimizer" / country / crop
            / f"{country}_{crop}_s{season}_optimized_mask.parquet"
        )

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_region(self, country: str, crop: str, season: int, region: str):
        """Load the per-cell parquet, filter to one region, collapse to
        (per_cell_year_var, y) suitable for the GA. Returns None if the
        parquet is missing or the region has no usable rows.

        Returns a 4-tuple ``(per_cell, y, cell_meta, var_cols)``:
            per_cell : (n_cells, n_years, n_vars) float
            y        : (n_years,) float — joined yield
            cell_meta: DataFrame columns (cell_id, lat, lon, afi) — one
                       row per cell, indexed 0..n_cells-1 matching the
                       first axis of per_cell
            var_cols : tuple of var names in the same order as the third
                       axis of per_cell
        """
        path = self.cells_parquet_path(country, crop, season)
        if not path.is_file():
            self.logger.warning(
                f"  cells parquet not found for ({country}, {crop}, s{season}) at "
                f"{path} — run `geoprepare.extract_cells` upstream first; skipping."
            )
            return None

        df = pd.read_parquet(path)
        missing = _REQUIRED_COLS - set(df.columns)
        if missing:
            self.logger.warning(
                f"  parquet {path} missing required columns {sorted(missing)}; skipping."
            )
            return None

        df = df[df["region"] == region]
        if df.empty:
            self.logger.warning(
                f"  no rows for region={region!r} in {path}; skipping."
            )
            return None

        # Detect available var columns (config-gated upstream).
        var_cols = tuple(v for v in _VAR_COLS if v in df.columns)
        if not var_cols:
            self.logger.warning(
                f"  no var columns ({_VAR_COLS}) in parquet — nothing to optimize."
            )
            return None

        # Drop zero-cropland cells BEFORE any aggregation. The
        # extract_cells contract says "emit only cells with afi > 0",
        # but we don't rely on it — non-cropland cells passing through
        # would pad n_cells, push the min-cell floor up artificially,
        # and dilute the cell-averaged seasonal aggregate with zero-
        # contribution rows. Filtering here makes n_cells == cropland
        # cells, which is the right denominator for both the floor and
        # the L0 share penalty.
        n_before = df["cell_id"].nunique()
        df = df[df["afi"] > 0].copy()
        n_after = df["cell_id"].nunique()
        if n_before != n_after:
            self.logger.info(
                f"  dropped {n_before - n_after} zero-AFI cells (kept "
                f"{n_after} cropland cells out of {n_before} in parquet)"
            )
        if df.empty:
            self.logger.warning(
                f"  region={region!r} has no cells with afi > 0; skipping."
            )
            return None

        # Collapse DOY: per (cell_id, year) reduce each var with its
        # configured agg (NDVI=max, others=mean). Build wide tensor.
        agg_map = {v: _DOY_AGG[v] for v in var_cols}
        per_cell_year = (
            df.groupby(["cell_id", "year"], sort=True, as_index=False)
              .agg(agg_map)
        )
        cell_meta = (
            df.groupby("cell_id", sort=True)[["lat", "lon", "afi", "region_id"]]
              .first()
              .reset_index()
        )
        years = sorted(per_cell_year["year"].unique())
        cell_ids = sorted(per_cell_year["cell_id"].unique())
        cell_idx = {c: i for i, c in enumerate(cell_ids)}
        year_idx = {y: i for i, y in enumerate(years)}

        per_cell = np.full(
            (len(cell_ids), len(years), len(var_cols)), np.nan, dtype=float
        )
        for _, row in per_cell_year.iterrows():
            ci = cell_idx[row["cell_id"]]
            yi = year_idx[row["year"]]
            for vi, v in enumerate(var_cols):
                per_cell[ci, yi, vi] = row[v]

        # Yield join via the canonical AMIS-aware path. add_statistics
        # expects Region, Harvest Year, Season — same shape as
        # threshold_optimizer.join_yield.
        df_in = pd.DataFrame({
            "Region": region,
            "Harvest Year": years,
            "Season": int(season),
        })
        admin_zone = self.parser.get(country, "admin_level")
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
            label=f"{country}/{crop}/s{season}/{region}",
        )
        if "Yield (tn per ha)" not in df_joined.columns:
            df_joined = df_joined.assign(**{"Yield (tn per ha)": np.nan})
        y = df_joined["Yield (tn per ha)"].to_numpy(dtype=float)

        # Reindex cell_meta to match per_cell's first axis.
        cell_meta = cell_meta.set_index("cell_id").reindex(cell_ids).reset_index()
        return per_cell, y, cell_meta, var_cols

    # ------------------------------------------------------------------
    # Per-region runner
    # ------------------------------------------------------------------

    def process_region(
        self, country: str, crop: str, season: int, region: str,
    ):
        label = f"{country}/{crop}/s{season}/{region}"
        self.logger.info(f"== CellOptimizer: {label} ==")

        loaded = self.load_region(country, crop, season, region)
        if loaded is None:
            return None

        per_cell, y, cell_meta, var_cols = loaded
        n_cells = per_cell.shape[0]
        n_years_finite = int(np.isfinite(y).sum())
        if n_years_finite < 5:
            self.logger.warning(
                f"  only {n_years_finite} finite-yield years for {label}; "
                f"LOOCV R² needs >=5. Skipping."
            )
            return None

        self.logger.info(
            f"  loaded {n_cells} cells x {per_cell.shape[1]} years x "
            f"{len(var_cols)} vars ({list(var_cols)}); "
            f"{n_years_finite} finite-yield years."
        )

        # AFI as prior — pass the per-cell crop-fraction vector so the
        # seed population is biased toward high-AFI cells (does NOT
        # enter the fitness function; only shifts where the GA starts).
        afi_vec = cell_meta["afi"].to_numpy(dtype=float)
        result = run_ga(per_cell, y, self.ga, afi=afi_vec, logger=self.logger)

        self.logger.info(
            f"  best fitness = {result.best_fitness:.4f}, "
            f"best R^2 = {result.best_r2:.4f} (baseline R^2 = "
            f"{result.baseline_r2:.4f}, lift = "
            f"{(result.best_r2 - result.baseline_r2):+.4f}), "
            f"selected {result.best_mask.sum()}/{n_cells} cells, "
            f"ran {result.n_generations_run} generations"
        )

        # Write date-stamped diagnostic outputs
        out_dir = self.regions_dir(country, crop, season)
        stem = f"{country}_{crop}_s{season}_{region}"
        np.save(out_dir / f"{stem}_best_mask.npy", result.best_mask)
        result.history.to_csv(out_dir / f"{stem}_history.csv", index=False)

        if self.do_plot:
            self._plot_diagnostics(
                result, per_cell, y, cell_meta, var_cols,
                out_dir=out_dir, stem=stem, region=region,
            )

        # Per-cell rows for the production-mask parquet. One row per
        # cell, with the GA's included/excluded decision plus the
        # original cell metadata so geoextract can match on cell_id.
        # region_id was populated by load_region from the parquet.
        production_rows = cell_meta.copy()
        production_rows["country"] = country
        production_rows["region"] = region
        production_rows["included"] = result.best_mask
        # Order to match the documented contract.
        production_rows = production_rows[[
            "country", "region", "region_id", "cell_id",
            "lat", "lon", "afi", "included",
        ]]

        # Per-region summary row (returned to caller for cross-region rollup)
        summary = {
            "country":         country,
            "crop":            crop,
            "season":          int(season),
            "region":          region,
            "n_cells":         int(n_cells),
            "n_selected":      int(result.best_mask.sum()),
            "selected_frac":   float(result.best_mask.mean()),
            "baseline_r2":     float(result.baseline_r2),
            "optimized_r2":    float(result.best_r2),
            "lift":            float(result.best_r2 - result.baseline_r2),
            "n_gens_run":      int(result.n_generations_run),
        }
        return {"summary": summary, "production_rows": production_rows}

    # ------------------------------------------------------------------
    # Diagnostic plots
    # ------------------------------------------------------------------

    def _plot_diagnostics(
        self, result, per_cell, y, cell_meta, var_cols,
        out_dir: Path, stem: str, region: str,
    ):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        # 1. Mask map — lat/lon scatter coloured by inclusion
        fig, ax = plt.subplots(figsize=(7, 6))
        included = result.best_mask
        ax.scatter(
            cell_meta.loc[~included, "lon"], cell_meta.loc[~included, "lat"],
            c="lightgray", s=14, alpha=0.6, label=f"out (n={(~included).sum()})",
            edgecolors="none",
        )
        ax.scatter(
            cell_meta.loc[included, "lon"], cell_meta.loc[included, "lat"],
            c=cell_meta.loc[included, "afi"], s=22, cmap="viridis",
            label=f"in (n={included.sum()})", edgecolors="black", linewidths=0.3,
        )
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        ax.set_title(
            f"{region} — selected cells\n"
            f"R^2: {result.baseline_r2:.3f} (all cells) -> "
            f"{result.best_r2:.3f} (optimized), lift = "
            f"{(result.best_r2 - result.baseline_r2):+.3f}"
        )
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_dir / f"{stem}_mask_map.png", dpi=130)
        plt.close(fig)

        # 2. Fitness history
        fig, ax = plt.subplots(figsize=(8, 4.5))
        h = result.history
        ax.plot(h["generation"], h["best_fit"], color="#1f77b4",
                linewidth=1.6, label="best fitness")
        ax.plot(h["generation"], h["mean_fit"], color="#1f77b4",
                linewidth=1.0, alpha=0.4, linestyle="--", label="mean fitness")
        ax.plot(h["generation"], h["best_r2"], color="#d62728",
                linewidth=1.4, label="best R^2 (unpenalized)")
        ax.axhline(result.baseline_r2, color="gray", linestyle=":",
                   linewidth=1.0, label=f"baseline R^2 = {result.baseline_r2:.3f}")
        ax.set_xlabel("generation")
        ax.set_ylabel("fitness / R^2")
        ax.set_title(f"{region} — GA convergence")
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_dir / f"{stem}_fitness_history.png", dpi=130)
        plt.close(fig)

        # 3. Pre/post yield-vs-EO scatter, one row per var, two cols
        n_vars = len(var_cols)
        fig, axes = plt.subplots(
            n_vars, 2, figsize=(8, 2.6 * n_vars),
            sharey=False, squeeze=False,
        )
        base_x = aggregate_over_mask(per_cell, np.ones(per_cell.shape[0], dtype=bool))
        opt_x = aggregate_over_mask(per_cell, result.best_mask)
        for vi, v in enumerate(var_cols):
            for ci, (xv, title) in enumerate(
                [(base_x[:, vi], "all cells"), (opt_x[:, vi], "optimized")]
            ):
                ax = axes[vi][ci]
                mask = np.isfinite(xv) & np.isfinite(y)
                if mask.sum() >= 2:
                    ax.scatter(xv[mask], y[mask], s=20, alpha=0.7, c="#1f77b4")
                    if mask.sum() >= 3 and xv[mask].std() > 0:
                        r = float(np.corrcoef(xv[mask], y[mask])[0, 1])
                        ax.set_title(f"{v} — {title} (r={r:+.2f})", fontsize=9)
                    else:
                        ax.set_title(f"{v} — {title}", fontsize=9)
                else:
                    ax.set_title(f"{v} — {title} (no data)", fontsize=9)
                ax.set_xlabel(v)
                ax.set_ylabel("yield (tn/ha)")
                ax.grid(True, alpha=0.3)
        fig.suptitle(f"{region} — pre/post comparison per variable", fontsize=11)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        fig.savefig(out_dir / f"{stem}_pre_post.png", dpi=130)
        plt.close(fig)

        self.logger.info(f"  wrote diagnostic plots to {out_dir}")

    # ------------------------------------------------------------------
    # Cross-region rollup
    # ------------------------------------------------------------------

    def write_cross_region_summary(self, summary_rows):
        if not summary_rows:
            self.logger.warning("  no per-region results — skipping cross-region summary.")
            return

        df = pd.DataFrame(summary_rows)
        out_dir = self.cross_region_dir()
        csv_path = out_dir / "summary.csv"
        df.to_csv(csv_path, index=False)
        self.logger.info(f"  wrote {csv_path}")

        if not self.do_plot or len(df) < 2:
            return
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(df["lift"], bins=20, color="#1f77b4", alpha=0.8, edgecolor="black")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.axvline(df["lift"].mean(), color="red", linestyle="--",
                   linewidth=1.2, label=f"mean lift = {df['lift'].mean():+.3f}")
        ax.set_xlabel("LOOCV R^2 lift (optimized - baseline)")
        ax.set_ylabel("regions")
        ax.set_title(f"Cell-optimizer lift across {len(df)} regions")
        ax.legend(loc="best", fontsize=9)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_dir / "lift_distribution.png", dpi=130)
        plt.close(fig)
        self.logger.info(f"  wrote {out_dir / 'lift_distribution.png'}")

    # ------------------------------------------------------------------
    # Top-level entry
    # ------------------------------------------------------------------

    def create_run_combinations(self):
        """Yield (country, admin_level, crop, season). Region iteration
        happens inside process_one because regions come from the parquet,
        not config."""
        combos = []
        for country in self.countries:
            admin_level = self.parser.get(country, "admin_level")
            crops = ast.literal_eval(self.parser.get(country, "crops"))
            has_seasons = (
                self.parser.has_option(country, "seasons")
                or self.parser.has_option("DEFAULT", "seasons")
            )
            for crop in crops:
                seasons = (
                    ast.literal_eval(self.parser.get(country, "seasons"))
                    if has_seasons else [1]
                )
                for season in seasons:
                    combos.append((country, admin_level, crop, season))
        return combos

    def process_one(self, country, admin_level, crop, season):
        """Iterate every region present in the parquet for this combo.
        Region iteration is parallelized via joblib when n_jobs != 1;
        the production-mask parquet is written here once all regions
        for this combo complete (one parquet per country×crop×season).
        """
        path = self.cells_parquet_path(country, crop, season)
        if not path.is_file():
            self.logger.warning(
                f"  parquet missing for ({country}, {crop}, s{season}): {path}"
            )
            return []
        regions = sorted(
            pd.read_parquet(path, columns=["region"])["region"].unique()
        )
        self.logger.info(
            f"  {country}/{crop}/s{season}: {len(regions)} regions in parquet"
            f" (n_jobs={self.n_jobs})"
        )

        if self.n_jobs == 1:
            results = []
            for region in regions:
                try:
                    results.append(self.process_region(country, crop, season, region))
                except Exception as exc:  # noqa: BLE001
                    self.logger.error(
                        f"  process_region failed on {region}: {exc}"
                    )
                    results.append(None)
        else:
            from joblib import Parallel, delayed
            # Workers re-instantiate CellOptimizer from the original
            # config-file path because BaseGeo's logger handle isn't
            # picklable. Each worker reads its own region from the
            # parquet — the per-worker IO overhead is small compared
            # to the GA's runtime (~100s/region single-thread).
            results = Parallel(n_jobs=self.n_jobs, backend="loky")(
                delayed(_process_region_worker)(
                    self._config_files, country, crop, season, region,
                )
                for region in regions
            )

        # Filter Nones (skipped regions) and split summary vs production rows.
        summary_rows, production_frames = [], []
        for r in results:
            if r is None:
                continue
            summary_rows.append(r["summary"])
            production_frames.append(r["production_rows"])

        if self.write_production_mask and production_frames:
            self._write_production_mask(
                country, crop, season,
                pd.concat(production_frames, ignore_index=True),
            )

        return summary_rows

    def _write_production_mask(
        self, country: str, crop: str, season: int, df: pd.DataFrame,
    ) -> None:
        """Write the per-cell included/excluded answer to a stable
        parquet path that geoextract reads to build its production
        crop mask. Atomic via tmp + rename so geoextract never sees a
        partial file.
        """
        from geocif import __version__ as _geocif_version

        df = df.copy()
        df["optimizer_version"] = f"geocif-{_geocif_version}"
        df["optimized_at"] = ar.now().format("YYYY-MM-DD")

        out_path = self.production_mask_path(country, crop, season)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = out_path.with_suffix(".parquet.tmp")
        df.to_parquet(tmp_path, index=False)
        tmp_path.replace(out_path)   # atomic on POSIX; near-atomic on NTFS
        n_inc = int(df["included"].sum())
        n_tot = len(df)
        self.logger.info(
            f"  wrote production mask -> {out_path} "
            f"({n_inc}/{n_tot} cells included, "
            f"{df['region'].nunique()} regions)"
        )

    def main(self):
        import traceback
        all_summary = []
        for country, admin_level, crop, season in self.create_run_combinations():
            try:
                rows = self.process_one(country, admin_level, crop, season)
                all_summary.extend(rows)
            except Exception as exc:  # noqa: BLE001
                self.logger.error(
                    f"  CellOptimizer failed on ({country}, {crop}, s{season}): "
                    f"{exc}\n{traceback.format_exc()}"
                )
        self.write_cross_region_summary(all_summary)


def _process_region_worker(
    config_files, country: str, crop: str, season: int, region: str,
):
    """Top-level worker for joblib (must be importable for pickling).
    Each worker constructs its own CellOptimizer from the config file
    path — BaseGeo's open logger handle isn't picklable, so we can't
    ship the parent's instance into the worker.

    Returns the same dict shape as CellOptimizer.process_region:
    ``{"summary": {...}, "production_rows": DataFrame}`` or ``None``
    if the region was skipped.
    """
    try:
        opt = CellOptimizer(config_files)
        return opt.process_region(country, crop, season, region)
    except Exception as exc:  # noqa: BLE001
        # The parent's logger isn't visible here; print so the user
        # sees something in the joblib worker stderr stream.
        import traceback
        print(
            f"[cell_optimizer worker] failed on "
            f"{country}/{crop}/s{season}/{region}: {exc}\n"
            f"{traceback.format_exc()}",
            flush=True,
        )
        return None


def run(path_config_files):
    """Entry point analogous to ``threshold_optimizer.run``."""
    opt = CellOptimizer(path_config_files)
    opt.main()
