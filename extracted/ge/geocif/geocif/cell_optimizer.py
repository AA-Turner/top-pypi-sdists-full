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
import pyarrow.parquet as pq

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


def _ndvi_byte_to_unit(arr):
    """Rescale Mark's byte-scale NDVI (≈50..250) to unit NDVI (≈0..1).

    Mirrors ``geocif/cid/indices.py:standardize_dataframe``'s formula
    ``(byte − 50) / 200``. Pass-through (no rescale) when the array is
    already in unit scale — heuristic: max(arr) ≤ 1.0.

    Only used for display labels in plots; the GA itself doesn't care
    about scale because Pearson r and OLS R² are scale-invariant.
    """
    arr = np.asarray(arr, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return arr
    if float(np.nanmax(finite)) <= 1.0:
        return arr
    return (arr - 50.0) / 200.0


def _display_var_name(var: str) -> str:
    """Map internal variable slug to the label used on plot axes.
    NDVI / tmax / tmin / precip get conventional capitalisation."""
    return {
        "ndvi": "NDVI",
        "tmax": "Tmax",
        "tmin": "Tmin",
        "precip": "Precipitation",
    }.get(var.lower(), var)


def _display_region_name(region: str) -> str:
    """Slug → human label for plot titles: replace underscores with
    spaces and apply title case. ``buenos_aires`` → ``Buenos Aires``,
    ``new_south_wales`` → ``New South Wales``.
    """
    return str(region).replace("_", " ").title()


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

    # Clamp the min-cell floor to n_cells. The configured floor can
    # exceed the cropland-cell count for very small regions (e.g.
    # Argentina/soybean/Corrientes has < min_cell_floor_abs=20 cells);
    # without the clamp the seed-population repair tries to sample
    # ``need = min_cells - sum`` cells from a smaller "off" pool and
    # numpy raises "Cannot take a larger sample than population when
    # replace is False". Clamping makes ``min_cells == n_cells`` for
    # tiny regions: every genome becomes all-True after repair, the
    # GA degenerates to a single configuration (baseline R² ==
    # optimized R², lift = 0), and the region's production mask
    # simply includes every cell.
    min_cells_raw = max(
        cfg.min_cell_floor_abs,
        int(np.ceil(cfg.min_cell_floor_frac * n_cells)),
    )
    min_cells = min(min_cells_raw, n_cells)
    if min_cells < min_cells_raw and logger is not None:
        logger.warning(
            f"  min-cell floor clamped {min_cells_raw} -> {min_cells} "
            f"because region has only {n_cells} cropland cells; GA "
            f"degenerates to all-cells-in for this region"
        )
    mut_rate = cfg.mutation_rate if cfg.mutation_rate is not None else 2.0 / max(1, n_cells)

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
            years    : tuple of int years aligned with the second axis
                       of per_cell (and with y). Returned so plots can
                       colour points by year.
        """
        path = self.cells_parquet_path(country, crop, season)
        if not path.is_file():
            self.logger.warning(
                f"  cells parquet not found for ({country}, {crop}, s{season}) at "
                f"{path} — run `geoprepare.extract_cells` upstream first; skipping."
            )
            return None

        # Read schema first so we can both validate required columns AND
        # decide which optional var columns to pull — without paying the
        # cost of reading the full parquet body.
        schema = pq.read_schema(path)
        available = set(schema.names)
        missing = _REQUIRED_COLS - available
        if missing:
            self.logger.warning(
                f"  parquet {path} missing required columns {sorted(missing)}; skipping."
            )
            return None
        var_cols = tuple(v for v in _VAR_COLS if v in available)
        if not var_cols:
            self.logger.warning(
                f"  no var columns ({_VAR_COLS}) in parquet — nothing to optimize."
            )
            return None

        # Project + predicate-pushdown at read time: pull ONLY this region's
        # rows and ONLY the columns we use. Without this, every joblib
        # worker materialized the full multi-region parquet (~7 GB for
        # russia/winter_wheat: 72 M rows × 10 cols in pandas) and the
        # node OOM-killed workers under n_jobs=-1. With this, each
        # worker's DataFrame is bounded by one region's rows — ~500 MB
        # worst case, ~100 MB typical.
        keep_cols = sorted(_REQUIRED_COLS | set(var_cols))
        df = pd.read_parquet(
            path,
            columns=keep_cols,
            filters=[("region", "==", region)],
        )
        if df.empty:
            self.logger.warning(
                f"  no rows for region={region!r} in {path}; skipping."
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
        return per_cell, y, cell_meta, var_cols, tuple(years)

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

        per_cell, y, cell_meta, var_cols, years = loaded
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
                out_dir=out_dir, stem=stem,
                country=country, region=region,
                years=years,
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

        # Per-variable Pearson r between yield and each EO variable's
        # seasonal aggregate. Computed twice — once with all cells
        # (baseline) and once with the GA's optimized mask — so the
        # cross-region rollup can show how the optimizer impacts each
        # variable's correlation independently. The multivariate
        # baseline_r2 / optimized_r2 above don't separate the
        # contributions per variable; these columns do.
        base_x = aggregate_over_mask(per_cell, np.ones(n_cells, dtype=bool))
        opt_x = aggregate_over_mask(per_cell, result.best_mask)
        per_var_r: dict = {}
        for vi, vname in enumerate(var_cols):
            for tag, x_full in (("baseline", base_x), ("optimized", opt_x)):
                xv = x_full[:, vi]
                m = np.isfinite(xv) & np.isfinite(y)
                if m.sum() >= 3 and float(np.nanstd(xv[m])) > 0 and float(np.nanstd(y[m])) > 0:
                    r_val = float(np.corrcoef(xv[m], y[m])[0, 1])
                else:
                    r_val = float("nan")
                per_var_r[f"{tag}_r_{vname}"] = r_val

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
            **per_var_r,
        }
        return {"summary": summary, "production_rows": production_rows}

    # ------------------------------------------------------------------
    # Diagnostic plots
    # ------------------------------------------------------------------

    def _load_country_boundary_gdf(self, country: str):
        """Lazy-load and per-process-cache the country's boundary
        GeoDataFrame. Used by ``_add_locator_inset`` to draw the
        country-context inset on each mask map. Returns None if
        geopandas is unavailable, the boundary file is missing, or
        the country doesn't appear in the shapefile.

        Caching is intra-process — joblib workers each load once. With
        ~50 regions per country that's ~50 redundant loads avoided per
        worker, but the first region's load still pays the ~100ms read
        cost.
        """
        if not hasattr(self, "_boundary_cache"):
            self._boundary_cache = {}
        if country in self._boundary_cache:
            return self._boundary_cache[country]

        try:
            import geopandas as gpd
        except ImportError:
            self.logger.warning(
                "geopandas not installed — skipping locator-inset map "
                "on mask plots (install geopandas to enable)"
            )
            self._boundary_cache[country] = None
            return None

        country_key = country.lower().replace(" ", "_")
        boundary_file = None
        if self.parser.has_option(country_key, "boundary_file"):
            boundary_file = self.parser.get(country_key, "boundary_file")
        elif self.parser.has_option("DEFAULT", "boundary_file"):
            boundary_file = self.parser.get("DEFAULT", "boundary_file")
        if not boundary_file:
            self._boundary_cache[country] = None
            return None

        try:
            dir_boundary = Path(self.parser.get("PATHS", "dir_boundary_files"))
        except Exception:
            self._boundary_cache[country] = None
            return None
        fp = dir_boundary / boundary_file
        if not fp.exists():
            self.logger.warning(
                f"  boundary shapefile not found: {fp} — locator inset "
                f"will be skipped for {country}"
            )
            self._boundary_cache[country] = None
            return None

        try:
            gdf = gpd.read_file(fp)
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  failed to read boundary shapefile {fp}: {exc}"
            )
            self._boundary_cache[country] = None
            return None

        # Filter to the country. The shared global Level_1.shp carries
        # admin units for every country; we only want one country's.
        if "ADM0_NAME" in gdf.columns:
            country_str = country.replace("_", " ").title()
            gdf = gdf[gdf["ADM0_NAME"].str.lower() == country_str.lower()]
        # Keep only polygon geometries.
        gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
        if gdf.empty:
            self.logger.warning(
                f"  no polygons found for {country} in {fp.name}; "
                f"locator inset will be skipped"
            )
            self._boundary_cache[country] = None
            return None

        self._boundary_cache[country] = gdf
        return gdf

    def _add_locator_inset(self, ax, country: str, region: str,
                            region_id=None) -> None:
        """Add a small country-context map inside the top-right of the
        main axes, with the current region highlighted in royalblue.
        Mirrors agmet._add_inset_map's approach: aspect-correct sizing
        from the country's bounding box, ID-based highlight when
        available with a name-match fallback. Silently skips if the
        boundary file can't be loaded or the region can't be matched.
        """
        gdf = self._load_country_boundary_gdf(country)
        if gdf is None or gdf.empty:
            return
        try:
            # Compute the country's geo aspect (dx/dy) from its total
            # bounds so the inset doesn't squash tall/narrow countries
            # (Chile, Norway) or stretch wide ones. Same logic as
            # agmet._add_inset_map at agmet/plot.py.
            bounds = gdf.total_bounds   # [minx, miny, maxx, maxy]
            dx = float(bounds[2] - bounds[0])
            dy = float(bounds[3] - bounds[1])
            if dx <= 0 or dy <= 0:
                return
            geo_aspect = dx / dy

            # Inset box: cap at 22% axes width OR 22% axes height,
            # whichever lets the country fit at its true aspect.
            box_max = 0.22
            if geo_aspect >= 1:
                # Wider than tall → cap on width.
                w = box_max
                h = w / geo_aspect
            else:
                # Taller than wide → cap on height.
                h = box_max
                w = h * geo_aspect
            # Anchor box at top-right of the axes with a small inset.
            x0 = 0.99 - w
            y0 = 0.99 - h
            inset_ax = ax.inset_axes([x0, y0, w, h])
            inset_ax.set_axis_off()

            # Keep only polygon geometries (drop stray points/lines).
            gdf_poly = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
            if gdf_poly.empty:
                return

            # Country outline as a single dissolved polygon — avoids
            # internal admin boundaries crowding a thumbnail-sized map.
            dissolved = gdf_poly.dissolve()
            dissolved.plot(
                ax=inset_ax, color="lightgray", edgecolor="black", linewidth=0.6,
            )

            # Highlight the region. Prefer ADM_ID match when both
            # region_id and the column are available — that's the
            # only reliable disambiguator when ADM1_NAME values
            # collide across countries (agmet flagged this for US
            # counties like Kiowa appearing in CO/KS/OK).
            highlighted = False
            if region_id is not None and "ADM_ID" in gdf_poly.columns:
                mask = gdf_poly["ADM_ID"].astype(str) == str(region_id)
                if mask.any():
                    gdf_poly[mask].plot(
                        ax=inset_ax, color="royalblue", edgecolor="royalblue",
                    )
                    highlighted = True

            if not highlighted:
                # Fall back to name match against ADM<N>_NAME for the
                # configured admin_level.
                country_key = country.lower().replace(" ", "_")
                admin_level = (
                    self.parser.get(country_key, "admin_level", fallback=None)
                    or self.parser.get("DEFAULT", "admin_level", fallback="admin_1")
                )
                level_num = admin_level.replace("admin_", "") if admin_level else "1"
                name_col = next(
                    (c for c in [f"ADM{level_num}_NAME", f"ADMIN{level_num}"]
                     if c in gdf_poly.columns),
                    None,
                )
                if name_col is not None:
                    region_norm = str(region).lower().replace("_", " ").strip()
                    mask = (
                        gdf_poly[name_col].astype(str).str.lower()
                            .str.replace("_", " ").str.strip()
                        == region_norm
                    )
                    if mask.any():
                        gdf_poly[mask].plot(
                            ax=inset_ax, color="royalblue", edgecolor="royalblue",
                        )

            # Lock geographic aspect so the country isn't distorted by
            # the inset box's shape. Without this, matplotlib stretches
            # the polygons to fill the inset axes irrespective of true
            # lat/lon ratio.
            inset_ax.set_aspect("equal")
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  locator inset failed for {region}: {exc}")

    def _plot_diagnostics(
        self, result, per_cell, y, cell_meta, var_cols,
        out_dir: Path, stem: str, country: str, region: str,
        years=None,
    ):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        # Pull region_id from cell_meta (all rows for a region share the
        # same region_id). Passed to _add_locator_inset so the inset
        # prefers an ADM_ID match over name-matching — only reliable
        # disambiguator when region names collide.
        region_id = None
        if "region_id" in cell_meta.columns and not cell_meta.empty:
            rid_val = cell_meta["region_id"].iloc[0]
            if pd.notna(rid_val):
                region_id = rid_val

        # 1. Mask map — lat/lon scatter, BOTH in and out cells coloured
        # by AFI on the same viridis ramp so the eye can answer "did
        # the GA disagree with the AFI cropmask?" at a glance.
        #   * Out cells: faded (alpha=0.30), small, no edge — recedes
        #     visually but AFI is still readable from the colour.
        #   * In cells:  vivid (alpha=0.95), larger, black ring —
        #     pops out as "what the GA kept".
        # Shared vmin/vmax across both scatters so the colourbar maps
        # cleanly to either population.
        included = result.best_mask
        afi_all = cell_meta["afi"].to_numpy(dtype=float)
        afi_vmin = float(np.nanmin(afi_all)) if afi_all.size else 0.0
        afi_vmax = float(np.nanmax(afi_all)) if afi_all.size else 100.0
        if afi_vmax <= afi_vmin:
            # Degenerate single-AFI-value region — give the colormap a
            # finite range so it renders without warnings.
            afi_vmax = afi_vmin + 1.0

        fig, ax = plt.subplots(figsize=(7, 6))
        ax.scatter(
            cell_meta.loc[~included, "lon"], cell_meta.loc[~included, "lat"],
            c=cell_meta.loc[~included, "afi"], s=12, cmap="viridis",
            vmin=afi_vmin, vmax=afi_vmax, alpha=0.30,
            label=f"out (n={(~included).sum()})", edgecolors="none",
        )
        sc_in = ax.scatter(
            cell_meta.loc[included, "lon"], cell_meta.loc[included, "lat"],
            c=cell_meta.loc[included, "afi"], s=28, cmap="viridis",
            vmin=afi_vmin, vmax=afi_vmax, alpha=0.95,
            label=f"in (n={included.sum()})", edgecolors="black", linewidths=0.4,
        )
        fig.colorbar(sc_in, ax=ax, fraction=0.04, pad=0.02,
                     label="AFI (crop fraction %)")
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        ax.set_title(
            f"{_display_region_name(region)} — selected cells\n"
            f"R²: {result.baseline_r2:.3f} (all cells) → "
            f"{result.best_r2:.3f} (optimized), lift = "
            f"{(result.best_r2 - result.baseline_r2):+.3f}"
        )
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(True, alpha=0.3)
        # Country-context inset — top-right of the axes, region in red.
        self._add_locator_inset(ax, country=country, region=region,
                                 region_id=region_id)
        fig.tight_layout()
        fig.savefig(out_dir / f"{stem}_mask_map.png", dpi=130)
        plt.close(fig)

        # 2. Fitness history. "best fitness" = R² minus the L0 size
        # penalty (λ × |mask|/n_cells); "best R²" = the same mask's R²
        # without the penalty applied. The gap between the two lines is
        # the size penalty being paid by the GA's current best mask.
        fig, ax = plt.subplots(figsize=(8, 4.5))
        h = result.history
        ax.plot(h["generation"], h["best_fit"], color="#1f77b4",
                linewidth=1.6, label="best fitness")
        ax.plot(h["generation"], h["mean_fit"], color="#1f77b4",
                linewidth=1.0, alpha=0.4, linestyle="--", label="mean fitness")
        ax.plot(h["generation"], h["best_r2"], color="#d62728",
                linewidth=1.4, label="best R²")
        ax.axhline(result.baseline_r2, color="gray", linestyle=":",
                   linewidth=1.0, label=f"baseline R² = {result.baseline_r2:.3f}")
        ax.set_xlabel("generation")
        ax.set_ylabel("fitness / R²")
        ax.set_title(f"{_display_region_name(region)} — GA convergence")
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, alpha=0.3)
        # Fitness equation annotation — shows the actual objective the
        # GA optimizes so a reader can decode the blue-vs-red gap as
        # the L0 size penalty being paid. Lower-right corner stays
        # clear of the convergence curves which rise to the right.
        eqn = (
            f"fitness = R² − λ·(|mask|/n_cells)"
            f"     λ = {self.ga.l0_lambda:g}"
        )
        ax.text(
            0.99, 0.02, eqn,
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="white", edgecolor="gray",
                      linewidth=0.5, alpha=0.9),
        )
        # Plain-English caption at the bottom of the figure so a
        # non-LLM reader doesn't have to decode the equation box to
        # understand what fitness is. The split across two lines keeps
        # the caption inside the 8-inch figure width at fontsize 8.
        caption = (
            "Fitness = how well a cell-mask predicts yield (R²), minus a "
            "small penalty for using too many cells (λ × fraction-of-"
            "cells-selected).\n"
            "The single number the GA tries to maximise."
        )
        # Reserve bottom margin for the caption.
        fig.tight_layout(rect=[0, 0.12, 1, 1])
        fig.text(
            0.5, 0.02, caption,
            ha="center", va="bottom",
            fontsize=8, style="italic",
        )
        fig.savefig(out_dir / f"{stem}_fitness_history.png", dpi=130)
        plt.close(fig)

        # 3. Pre/post yield-vs-EO scatter, one row per var, two cols.
        # Each dot is a year; the colour ramp (viridis) shows the year
        # so trends across the time axis are readable on the same axes.
        # NDVI is rescaled from byte-scale (≈50-250) to unit (0-1) to
        # match the convention used elsewhere in geocif; variable
        # labels are properly capitalised via _display_var_name.
        # Figure dimensions: wider than tall per-row so the year colorbar
        # has room to sit alongside the right panel without clipping its
        # X-axis tick labels. Was (8, 2.6 × n_vars) — too squat at n=1
        # and the colorbar crowded the rightmost ticks.
        n_vars = len(var_cols)
        fig, axes = plt.subplots(
            n_vars, 2, figsize=(11, 3.5 * n_vars),
            sharey=False, squeeze=False,
        )
        base_x = aggregate_over_mask(per_cell, np.ones(per_cell.shape[0], dtype=bool))
        opt_x = aggregate_over_mask(per_cell, result.best_mask)

        # Year array for colouring. When None (synthetic test), use a
        # linear index so the colormap still works.
        years_arr = (
            np.asarray(years, dtype=int) if years is not None
            else np.arange(per_cell.shape[1], dtype=int)
        )

        last_sc = None  # last scatter handle for the shared colorbar
        for vi, v in enumerate(var_cols):
            display_name = _display_var_name(v)
            for ci, (xv_raw, title) in enumerate(
                [(base_x[:, vi], "all cells"), (opt_x[:, vi], "optimized")]
            ):
                ax = axes[vi][ci]
                # Rescale NDVI byte-scale → unit so the X-axis matches
                # the convention used elsewhere in geocif. Other vars
                # pass through untouched.
                xv = _ndvi_byte_to_unit(xv_raw) if v.lower() == "ndvi" else xv_raw
                mask = np.isfinite(xv) & np.isfinite(y)
                if mask.sum() >= 2:
                    sc = ax.scatter(
                        xv[mask], y[mask],
                        c=years_arr[mask], cmap="viridis",
                        vmin=int(years_arr.min()),
                        vmax=int(years_arr.max()),
                        s=28, alpha=0.85,
                        edgecolors="black", linewidths=0.3,
                    )
                    last_sc = sc
                    if mask.sum() >= 3 and xv[mask].std() > 0:
                        r = float(np.corrcoef(xv[mask], y[mask])[0, 1])
                        ax.set_title(
                            f"{display_name} — {title} (r={r:+.2f})", fontsize=9,
                        )
                    else:
                        ax.set_title(f"{display_name} — {title}", fontsize=9)
                else:
                    ax.set_title(f"{display_name} — {title} (no data)", fontsize=9)
                ax.set_xlabel(display_name)
                ax.set_ylabel("yield (tn/ha)")
                ax.grid(True, alpha=0.3)

        # Single shared colorbar at the right edge showing the year
        # mapping; integer year ticks so it reads as a calendar legend
        # rather than a continuous variable.
        if last_sc is not None:
            cbar = fig.colorbar(
                last_sc, ax=axes, fraction=0.025, pad=0.02, label="year",
            )
            # Integer year ticks across the actual span.
            yr_min, yr_max = int(years_arr.min()), int(years_arr.max())
            # Cap to ~8 ticks for readability on a 5-year span vs a 25-year span.
            n_ticks = min(8, max(2, yr_max - yr_min + 1))
            tick_positions = np.linspace(yr_min, yr_max, n_ticks).round().astype(int)
            cbar.set_ticks(tick_positions)
            cbar.set_ticklabels([str(t) for t in tick_positions])

        fig.suptitle(
            f"{_display_region_name(region)} — pre/post comparison per variable",
            fontsize=11,
        )
        # tight_layout's rect leaves whitespace for the suptitle AND the
        # colorbar; without rect=[..., 0.92, ...] the colorbar collides
        # with the suptitle on tall figures.
        fig.tight_layout(rect=[0, 0, 0.92, 0.96])
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
        # Master CSV at the root for convenience (every region from
        # every country × crop × season in one place).
        master_csv = out_dir / "summary.csv"
        df.to_csv(master_csv, index=False)
        self.logger.info(f"  wrote {master_csv}")

        if not self.do_plot or len(df) < 2:
            return
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        # Split outputs by (country, crop, season). Lifts and R²s aren't
        # comparable across crops or countries (different yield series,
        # different baseline difficulty), so a single histogram or
        # scatter mixing them all hides more than it shows. Per-combo
        # folders keep the plots readable.
        group_cols = [c for c in ("country", "crop", "season") if c in df.columns]
        if not group_cols:
            self.logger.warning(
                "  cross-region df missing country/crop/season columns; "
                "writing only master summary.csv"
            )
            return

        for keys, grp in df.groupby(group_cols):
            # Normalize keys to a flat tuple even when group_cols has length 1.
            keys = keys if isinstance(keys, tuple) else (keys,)
            kv = dict(zip(group_cols, keys))
            country = str(kv.get("country", "_unknown"))
            crop = str(kv.get("crop", "_unknown"))
            season = int(kv.get("season", 1))

            sub_dir = out_dir / country / crop
            sub_dir.mkdir(parents=True, exist_ok=True)
            stem = f"s{season}"

            # Mean area per region for this combo — pulled via the
            # canonical add_statistics dispatcher so the source (AMIS /
            # HarvestStat / per-country override) is selected
            # automatically. Used to size dots in the baseline-vs-
            # optimized scatter; empty dict if anything fails, in which
            # case the scatter falls back to uniform dot size.
            mean_areas = self._fetch_mean_areas(
                country=country, crop=crop,
                regions=list(grp["region"].astype(str).unique()),
                current_year=self._current_year_or_default(),
                season=season,
            )
            if mean_areas:
                grp = grp.assign(
                    mean_area_ha=grp["region"].astype(str).map(mean_areas),
                )
                n_with_area = int(grp["mean_area_ha"].notna().sum())
                self.logger.info(
                    f"  {country}/{crop}/{stem}: mean_area_ha resolved "
                    f"for {n_with_area}/{len(grp)} regions"
                )
                # Rewrite the per-combo CSV with the new column.
                sub_csv = sub_dir / f"summary_{stem}.csv"
                grp.to_csv(sub_csv, index=False)
            else:
                # No area data — write CSV without the mean_area_ha column.
                sub_csv = sub_dir / f"summary_{stem}.csv"
                grp.to_csv(sub_csv, index=False)

            if len(grp) < 2:
                self.logger.info(
                    f"  {country}/{crop}/{stem}: only {len(grp)} regions, "
                    f"skipping cross-region plots"
                )
                continue

            self._cross_region_plots(grp, sub_dir, stem, country, crop, season, plt)
            self.logger.info(
                f"  cross-region plots → {sub_dir} ({len(grp)} regions)"
            )

    def _current_year_or_default(self) -> int:
        """Best-effort current-year resolver for the mean-area lookup
        window. Tries ML.current_year / DEFAULT.current_year config,
        falls back to the system year."""
        for sec in ("ML", "DEFAULT"):
            if self.parser.has_option(sec, "current_year"):
                try:
                    return int(self.parser.get(sec, "current_year"))
                except (ValueError, TypeError):
                    pass
        import arrow as _ar
        return int(_ar.utcnow().year)

    def _fetch_mean_areas(
        self, country: str, crop: str, regions, current_year=None,
        n_years: int = 10, season: int = 1,
    ) -> dict:
        """Pull per-region mean ``Area (ha)`` over the past
        ``n_years`` via the canonical ``ml_stats.add_statistics``
        dispatcher. Routes through HarvestStat / AMIS / per-country
        override files automatically (same path used for yield
        lookups), so this works uniformly across countries.

        Returns ``{region: float}`` (mean over years; NaN-tolerant).
        Returns ``{}`` on any failure so the caller can fall back to
        uniform dot sizes instead of crashing the cross-region step.
        """
        if not regions or self.parser is None:
            return {}
        try:
            import pandas as pd
            from pathlib import Path as _Path
            from geocif.ml import stats as ml_stats
            from geocif.agmet import utils as agmet_utils
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  mean-area fetch skipped (import failed): {exc}"
            )
            return {}

        # Resolve dir_production_statistics — geobase.txt's PATHS
        # section provides it via interpolation when parser was loaded
        # with ExtendedInterpolation.
        try:
            dir_stats = _Path(self.parser.get("PATHS", "dir_production_statistics"))
        except Exception:
            try:
                dir_metadata = _Path(self.parser.get("PATHS", "dir_metadata"))
                dir_stats = dir_metadata / "production_statistics"
            except Exception:
                self.logger.warning(
                    "  mean-area fetch skipped: could not resolve "
                    "dir_production_statistics from parser"
                )
                return {}
        if not dir_stats.exists():
            self.logger.warning(
                f"  mean-area fetch skipped: {dir_stats} not found"
            )
            return {}

        country_str = str(country).replace("_", " ").title()
        try:
            crop_str = agmet_utils.get_crop_name(crop)
        except Exception:
            crop_str = str(crop).replace("_", " ").title()

        country_key = str(country).lower().replace(" ", "_")
        if self.parser.has_option(country_key, "admin_level"):
            admin_zone = self.parser.get(country_key, "admin_level")
        elif self.parser.has_option("DEFAULT", "admin_level"):
            admin_zone = self.parser.get("DEFAULT", "admin_level")
        else:
            admin_zone = "admin_1"

        ref_year = int(current_year) if current_year else self._current_year_or_default()
        years = list(range(ref_year - n_years, ref_year))
        rows = [
            {"Region": r, "Harvest Year": y, "Season": int(season)}
            for r in regions for y in years
        ]
        if not rows:
            return {}
        df_in = pd.DataFrame(rows)
        try:
            df_out = ml_stats.add_statistics(
                dir_stats=dir_stats,
                df=df_in,
                country=country_str,
                crop=crop_str,
                admin_zone=admin_zone,
                stats=["Yield (tn per ha)", "Area (ha)"],
                method="",
                parser=self.parser,
                label=f"cell-optimizer-area/{country}/{crop}",
            )
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  mean-area fetch failed for {country}/{crop}: {exc}"
            )
            return {}

        if "Area (ha)" not in df_out.columns:
            return {}

        # Mean area per region, NaN-tolerant. NaN means "AMIS/HarvestStat
        # has no area data for this region/crop/year window" — the
        # plotter handles this by giving those dots a fallback size.
        out: dict = {}
        area_col = "Area (ha)"
        for region in regions:
            sub = df_out[df_out["Region"].astype(str) == str(region)]
            if sub.empty:
                continue
            vals = sub[area_col].astype(float).dropna()
            if vals.empty:
                continue
            out[str(region)] = float(vals.mean())
        return out

    def _cross_region_plots(self, grp, sub_dir, stem, country, crop, season, plt):
        """Render the two cross-region diagnostics for one
        (country, crop, season) group: lift histogram + baseline-vs-
        optimized scatter. Factored out so the layout for the two
        figures is defined once instead of duplicated.
        """
        # 1. Lift histogram
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(grp["lift"], bins=min(20, max(5, len(grp) // 2)),
                color="#1f77b4", alpha=0.8, edgecolor="black")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.axvline(grp["lift"].mean(), color="red", linestyle="--",
                   linewidth=1.2, label=f"mean lift = {grp['lift'].mean():+.3f}")
        ax.set_xlabel("LOOCV R² lift (optimized − baseline)")
        ax.set_ylabel("regions")
        ax.set_title(
            f"{country.title()} {crop.title()} s{season} — "
            f"cell-optimizer lift across {len(grp)} regions"
        )
        ax.legend(loc="best", fontsize=9)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(sub_dir / f"lift_distribution_{stem}.png", dpi=130)
        plt.close(fig)

        # 2. Baseline vs optimized R² scatter — one dot per region with
        # y=x reference, coloured by lift, top-5 labeled. When
        # mean_area_ha is present in grp, dot size encodes the region's
        # average crop area (log-scaled — area distributions span 2-3
        # orders of magnitude). Regions with NaN area get a fallback
        # mid-range size + thinner outline so they're distinguishable
        # as "size unknown".
        fig, ax = plt.subplots(figsize=(7, 7))

        # Compute dot sizes.
        S_FALLBACK = 60.0       # used when no area data at all
        S_NAN = 45.0            # this region has no area but others do
        S_MIN, S_MAX = 25.0, 250.0
        has_area = "mean_area_ha" in grp.columns
        area_finite = (
            grp["mean_area_ha"].notna() if has_area
            else pd.Series([False] * len(grp), index=grp.index)
        )
        if has_area and area_finite.any():
            a = grp["mean_area_ha"].astype(float).to_numpy()
            valid = np.isfinite(a) & (a > 0)
            if valid.sum() >= 2 and (a[valid].max() > a[valid].min()):
                # Log-scale so 100 ha and 10M ha both render readably.
                la = np.log10(a[valid] + 1.0)
                la_min, la_max = float(la.min()), float(la.max())
                # Apply to every row; NaNs / non-positive get S_NAN.
                sizes = np.full_like(a, S_NAN, dtype=float)
                la_all = np.where(valid, np.log10(a + 1.0), la_min)
                sizes[valid] = S_MIN + (S_MAX - S_MIN) * (
                    (la_all[valid] - la_min) / (la_max - la_min)
                )
            else:
                # All-same area or only one finite — fall back to fixed size.
                sizes = np.full(len(grp), S_FALLBACK, dtype=float)
        else:
            sizes = np.full(len(grp), S_FALLBACK, dtype=float)

        # Thinner outline for "size unknown" dots so they're visually distinct.
        if has_area and area_finite.any():
            edge_widths = np.where(area_finite.to_numpy(), 0.4, 0.15)
        else:
            edge_widths = np.full(len(grp), 0.4, dtype=float)

        sc = ax.scatter(
            grp["baseline_r2"], grp["optimized_r2"],
            c=grp["lift"].to_numpy(), cmap="RdYlGn",
            s=sizes, alpha=0.85, edgecolors="black", linewidths=edge_widths,
        )
        lo = float(min(grp["baseline_r2"].min(), grp["optimized_r2"].min(), 0.0)) - 0.05
        hi = float(max(grp["baseline_r2"].max(), grp["optimized_r2"].max(), 1.0)) + 0.05
        ax.plot([lo, hi], [lo, hi], color="gray", linestyle="--",
                linewidth=1.0, alpha=0.7, label="y = x (no lift)")
        # Label top-5 by lift so the biggest wins are named on the chart.
        for _, row in grp.nlargest(min(5, len(grp)), "lift").iterrows():
            ax.annotate(
                str(row["region"]),
                xy=(row["baseline_r2"], row["optimized_r2"]),
                xytext=(4, 4), textcoords="offset points",
                fontsize=8, alpha=0.85,
            )
        fig.colorbar(sc, ax=ax, fraction=0.04, pad=0.02, label="lift (Δ R²)")

        # Title — note size encoding when active.
        if has_area and area_finite.any():
            size_hint = "; dot size ∝ mean area (ha, log)"
        else:
            size_hint = ""
        ax.set_xlabel("baseline R² (all cells)")
        ax.set_ylabel("optimized R² (GA-selected cells)")
        ax.set_title(
            f"{country.title()} {crop.title()} s{season} — R² before vs "
            f"after\n({len(grp)} regions; mean lift = "
            f"{grp['lift'].mean():+.3f}{size_hint})"
        )
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_aspect("equal")

        # Size legend showing 10th / 50th / 90th-percentile areas, when
        # area is encoded. Lower-left corner stays clear of the lift
        # colorbar (right) and the y=x reference annotation (lower right).
        if has_area and area_finite.any():
            from matplotlib.lines import Line2D
            a_valid = grp.loc[area_finite, "mean_area_ha"].astype(float).to_numpy()
            la_min = float(np.log10(a_valid.min() + 1.0))
            la_max = float(np.log10(a_valid.max() + 1.0))

            def _area_to_size(a_val):
                la = np.log10(a_val + 1.0)
                if la_max <= la_min:
                    return S_FALLBACK
                return S_MIN + (S_MAX - S_MIN) * (la - la_min) / (la_max - la_min)

            def _fmt_area(a_val):
                if a_val >= 1e6:
                    return f"{a_val / 1e6:.1f} M ha"
                if a_val >= 1e3:
                    return f"{a_val / 1e3:.0f} K ha"
                return f"{int(a_val)} ha"

            percentiles = np.percentile(a_valid, [10, 50, 90])
            legend_handles = [
                Line2D(
                    [], [], marker="o", linestyle="", color="lightgray",
                    markersize=np.sqrt(_area_to_size(a_val)),
                    markeredgecolor="black", markeredgewidth=0.4,
                    label=_fmt_area(a_val),
                )
                for a_val in percentiles
            ]
            # Two legends — keep the y=x reference line legend AND the
            # size legend visible. Add y=x first then attach size legend
            # separately so they don't overwrite each other.
            yx_legend = ax.legend(loc="lower right", fontsize=9)
            ax.add_artist(yx_legend)
            ax.legend(
                handles=legend_handles, loc="lower left", fontsize=8,
                title="region area", title_fontsize=8, frameon=True,
            )
        else:
            ax.legend(loc="lower right", fontsize=9)

        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(sub_dir / f"baseline_vs_optimized_r2_{stem}.png", dpi=130)
        plt.close(fig)

        # 3. Per-variable r before vs after — one row per variable
        # present in summary.csv (NDVI / tmax / tmin / precip etc.).
        # Each row: baseline Pearson r on the X-axis, optimized
        # Pearson r on the Y, one dot per region, y=x reference line,
        # colour by per-variable lift, top-3 regions labelled.
        # Complements baseline_vs_optimized_r2.png (which is joint
        # multivariate R²) by showing how the optimizer's mask impacts
        # each variable's individual correlation with yield.
        self._plot_r_per_variable(grp, sub_dir, stem, country, crop, season, plt)

    def _plot_r_per_variable(self, grp, sub_dir, stem, country, crop, season, plt):
        """Per-variable r-impact across regions. Reads
        ``baseline_r_<var>`` and ``optimized_r_<var>`` columns from the
        summary DataFrame; silently skips when none are present
        (older summaries pre-dating this feature, or single-var
        parquets that only produce one pair).
        """
        # Discover which variables have baseline/optimized r columns.
        var_pairs = []
        for col in grp.columns:
            if col.startswith("baseline_r_"):
                var = col[len("baseline_r_"):]
                opt_col = f"optimized_r_{var}"
                if opt_col in grp.columns:
                    var_pairs.append((var, col, opt_col))
        if not var_pairs:
            self.logger.info(
                f"  {country}/{crop}/{stem}: no per-variable r columns "
                f"in summary — skipping r_per_variable plot"
            )
            return

        n = len(var_pairs)
        fig, axes = plt.subplots(n, 1, figsize=(7, 6 * n), squeeze=False)

        for vi, (var, base_col, opt_col) in enumerate(var_pairs):
            ax = axes[vi][0]
            mask = grp[base_col].notna() & grp[opt_col].notna()
            sub = grp[mask].copy()
            if sub.empty:
                ax.set_axis_off()
                ax.text(
                    0.5, 0.5, f"{_display_var_name(var)}: no data",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=11,
                )
                continue

            sub["r_lift"] = sub[opt_col] - sub[base_col]
            sc = ax.scatter(
                sub[base_col], sub[opt_col],
                c=sub["r_lift"].to_numpy(), cmap="RdYlGn",
                vmin=-max(abs(sub["r_lift"].min()), abs(sub["r_lift"].max()), 0.01),
                vmax= max(abs(sub["r_lift"].min()), abs(sub["r_lift"].max()), 0.01),
                s=42, alpha=0.85, edgecolors="black", linewidths=0.4,
            )
            # y=x reference line.
            lo = float(min(sub[base_col].min(), sub[opt_col].min(), -1.0)) - 0.05
            hi = float(max(sub[base_col].max(), sub[opt_col].max(), 1.0)) + 0.05
            # Symmetric bounds around 0 for readability.
            bound = max(abs(lo), abs(hi))
            lo, hi = -bound, bound
            ax.plot([lo, hi], [lo, hi], color="gray", linestyle="--",
                    linewidth=1.0, alpha=0.7, label="y = x (no impact)")
            ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)
            ax.axvline(0, color="black", linewidth=0.4, alpha=0.4)
            # Label top-3 by |r_lift|.
            for _, row in sub.reindex(
                sub["r_lift"].abs().sort_values(ascending=False).index
            ).head(3).iterrows():
                ax.annotate(
                    _display_region_name(str(row["region"])),
                    xy=(row[base_col], row[opt_col]),
                    xytext=(4, 4), textcoords="offset points",
                    fontsize=8, alpha=0.85,
                )
            fig.colorbar(
                sc, ax=ax, fraction=0.04, pad=0.02,
                label=f"r lift (Δ r for {_display_var_name(var)})",
            )
            mean_lift = float(sub["r_lift"].mean())
            ax.set_xlabel(f"baseline r — yield vs {_display_var_name(var)}")
            ax.set_ylabel(f"optimized r — yield vs {_display_var_name(var)}")
            ax.set_title(
                f"{_display_var_name(var)} — {len(sub)} regions; "
                f"mean Δr = {mean_lift:+.3f}"
            )
            ax.set_xlim(lo, hi)
            ax.set_ylim(lo, hi)
            ax.set_aspect("equal")
            ax.legend(loc="lower right", fontsize=8)
            ax.grid(True, alpha=0.3)

        fig.suptitle(
            f"{country.title()} {crop.title()} s{season} — "
            f"per-variable Pearson r impact across regions",
            fontsize=12,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.97])
        fig.savefig(sub_dir / f"r_per_variable_{stem}.png", dpi=130)
        plt.close(fig)

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

        if production_frames:
            # Combine the per-region per-cell rows once; reused for the
            # production parquet AND the national mask plot. Avoids
            # concatenating twice.
            combined_cells = pd.concat(production_frames, ignore_index=True)
            if self.write_production_mask:
                self._write_production_mask(
                    country, crop, season, combined_cells,
                )
            if self.do_plot:
                self._plot_national_mask(
                    country, crop, season, combined_cells,
                )

        return summary_rows

    def _plot_national_mask(
        self, country: str, crop: str, season: int, df_cells,
    ) -> None:
        """One country-scale map showing every cell across every region
        in this (country, crop, season) combo, coloured by AFI with the
        in-vs-out distinction preserved via alpha and size. The same
        visual conventions as the per-region ``_mask_map.png`` so the
        eye can move between scales without re-calibrating.

        Country boundary outline (dissolved) is overlaid for context
        when geopandas + the shapefile are available; if not, the dots
        still plot — the inset failure is silent.
        """
        if df_cells is None or df_cells.empty:
            return
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        afi_all = df_cells["afi"].to_numpy(dtype=float)
        afi_vmin = float(np.nanmin(afi_all)) if afi_all.size else 0.0
        afi_vmax = float(np.nanmax(afi_all)) if afi_all.size else 100.0
        if afi_vmax <= afi_vmin:
            afi_vmax = afi_vmin + 1.0

        included = df_cells["included"].astype(bool)
        out_cells = df_cells[~included]
        in_cells = df_cells[included]

        fig, ax = plt.subplots(figsize=(10, 10))

        # Country boundary first so dots sit on top of the outline.
        gdf = self._load_country_boundary_gdf(country)
        if gdf is not None and not gdf.empty:
            try:
                gdf_poly = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]
                if not gdf_poly.empty:
                    gdf_poly.dissolve().boundary.plot(
                        ax=ax, color="black", linewidth=0.5, alpha=0.6,
                    )
            except Exception:
                pass

        # Out cells: small + faded, AFI-coloured.
        if not out_cells.empty:
            ax.scatter(
                out_cells["lon"], out_cells["lat"],
                c=out_cells["afi"], cmap="viridis",
                vmin=afi_vmin, vmax=afi_vmax,
                s=4, alpha=0.25, edgecolors="none",
                label=f"out (n={len(out_cells):,})",
            )
        # In cells: larger + vivid, with black ring so they pop against
        # the faded out-population. The shared vmin/vmax keeps colours
        # comparable between in and out populations.
        sc_in = None
        if not in_cells.empty:
            sc_in = ax.scatter(
                in_cells["lon"], in_cells["lat"],
                c=in_cells["afi"], cmap="viridis",
                vmin=afi_vmin, vmax=afi_vmax,
                s=10, alpha=0.95, edgecolors="black", linewidths=0.15,
                label=f"in (n={len(in_cells):,})",
            )
        if sc_in is not None:
            fig.colorbar(sc_in, ax=ax, fraction=0.04, pad=0.02,
                         label="AFI (crop fraction %)")

        n_in = int(included.sum())
        n_total = int(len(df_cells))
        pct = (100.0 * n_in / n_total) if n_total else 0.0
        country_display = country.replace("_", " ").title()
        crop_display = crop.replace("_", " ").title()
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        ax.set_title(
            f"{country_display} {crop_display} s{season} — "
            f"national selected cells\n"
            f"{n_in:,}/{n_total:,} cells selected ({pct:.1f}%) "
            f"across {df_cells['region'].nunique()} regions"
        )
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)
        if not in_cells.empty or not out_cells.empty:
            ax.legend(loc="best", fontsize=9)
        fig.tight_layout()

        # File sits at country/crop scope (alongside the production
        # parquet's sibling diagnostics), not under regions_s<season>/.
        out_path = (
            self.summary_dir(country, crop)
            / f"{country}_{crop}_s{season}_national_mask.png"
        )
        fig.savefig(out_path, dpi=130)
        plt.close(fig)
        self.logger.info(
            f"  wrote national mask map -> {out_path} "
            f"({n_in:,}/{n_total:,} cells)"
        )

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
