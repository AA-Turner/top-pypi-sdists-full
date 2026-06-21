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

# Default DOY-axis aggregations per variable. Each instance of
# CellOptimizer reads per-variable overrides from
# ``[CELL_OPTIMIZER] {var}_doy_agg`` in geocif.txt; the values below are
# the fallbacks.
#
# NDVI default is ``auc`` (area-under-curve, integrated over the
# season) — picks up sustained greenness across the growing window,
# not just the peak. Matches the GEOGLAM ``AUC_NDVI`` definition. The
# previous default was ``max``; flip back via ``ndvi_doy_agg = max``
# in the config if you want peak-only behaviour.
#
# T and P are accumulated / averaged over the season (mean). The
# conservative default for new variables.
_DOY_AGG_DEFAULTS = {
    "ndvi":   "auc",
    "tmax":   "mean",
    "tmin":   "mean",
    "precip": "mean",
}

# Allowed agg values per variable. ``auc`` is an alias for ``sum``
# (literal area-under-curve over evenly-spaced DOY samples == sum of
# samples up to a constant cadence factor that cancels in correlation
# and OLS — so we map auc → sum at the pandas-groupby layer). The
# others are passed through to pandas.GroupBy.agg as-is.
_DOY_AGG_VALID = frozenset({"auc", "sum", "max", "mean", "median", "min"})

# Backwards-compat module-level alias — referenced by older tests and
# external scripts. Updated to the new defaults.
_DOY_AGG = _DOY_AGG_DEFAULTS


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
    *,
    T_norm: float = 0.0,
    afi: Optional[np.ndarray] = None,
    T_max: float = 50.0,
) -> float:
    """GA objective. Negative-infinity when the EFFECTIVE mask violates
    the MIN_CELLS floor (keeps tournament selection from ever picking a
    degenerate genome). Otherwise LOOCV R² minus the L0 share penalty.

    With the joint (mask, T) optimization (0.4.756+), each candidate
    carries its own AFI threshold ``T_norm ∈ [0, 1]`` (normalized; the
    raw % is ``T_norm × T_max``). When ``T_norm > 0`` and ``afi`` is
    supplied, the effective mask is ``mask & (afi ≥ T_pct × 100)``,
    i.e. cells must pass BOTH the GA's bit AND the per-region AFI
    floor T_pct. When ``T_norm == 0`` or ``afi is None`` (the legacy
    opt-out path), eligibility is universal and the function returns
    the same value as the pre-0.4.756 mask-only signature.
    """
    if T_norm > 0.0 and afi is not None:
        T_pct = T_norm * T_max
        eligible = afi >= T_pct * 100.0
        effective = mask & eligible
    else:
        effective = mask
    sel = int(effective.sum())
    if sel < min_cells:
        return float("-inf")
    x = aggregate_over_mask(per_cell, effective)
    r2 = loocv_r2_multivariate(x, y)
    if not np.isfinite(r2):
        return float("-inf")
    # L0 penalty on the EFFECTIVE share — staying consistent with the
    # in-use cell count. When the AFI filter is a no-op, this equals
    # the legacy raw-mask penalty.
    return r2 - lam * (sel / mask.size)


def _effective_mask(
    raw_mask: np.ndarray, T_pct: float, afi: Optional[np.ndarray],
) -> np.ndarray:
    """The mask production extraction actually applies: ``raw_mask AND
    (afi >= T_pct * 100)`` when the AFI threshold T is in play, just
    ``raw_mask`` otherwise. Centralises the rule so summary stats,
    diagnostic plots, and the production parquet stay in lockstep —
    early prototypes had each surface re-derive the effective mask
    inconsistently and the summary's per-variable r disagreed with
    the production parquet's `included` flag.
    """
    if T_pct > 0.0 and afi is not None:
        return raw_mask & (np.asarray(afi) >= T_pct * 100.0)
    return raw_mask


def aggregate_held_out(
    per_cell: np.ndarray,
    years: np.ndarray,
    masks_by_year: dict,
) -> np.ndarray:
    """For each year Y, aggregate that year's per-cell EO using mask_Y
    (the GA-selected mask trained on every year EXCEPT Y). Returns an
    ``(n_years, n_vars)`` array of out-of-sample aggregations.

    When ``masks_by_year`` is missing an entry for year Y (e.g. that
    year's GA was skipped because too few finite-yield years remained
    after holding it out), the corresponding row is left as NaN —
    downstream R² / r computations skip those years naturally.

    This is the building block for the honest-LOOCV diagnostic stack:
    each year's EO aggregate was computed without that year's yield
    informing the cell selection, so the resulting yield-vs-EO fit is
    genuinely out-of-sample.
    """
    n_years, n_vars = len(years), per_cell.shape[2]
    out = np.full((n_years, n_vars), np.nan, dtype=float)
    years_arr = np.asarray(years, dtype=int)
    for i, year in enumerate(years_arr):
        Y = int(year)
        if Y not in masks_by_year:
            continue
        mask_Y = masks_by_year[Y]
        # Single-year slice: (n_cells, 1, n_vars). aggregate_over_mask
        # returns (1, n_vars) — flatten to (n_vars,).
        out[i] = aggregate_over_mask(
            per_cell[:, i:i + 1, :], mask_Y,
        )[0]
    return out


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
    min_cell_floor_abs: int = 5
    min_cell_floor_frac: float = 0.01    # ↓ from 0.05: allow finer-grained selections
    init_inclusion_prob: float = 0.5     # fallback when afi prior is disabled
    afi_prior_beta: float = 1.0          # 0 → no prior (uniform 0.5); 1 → P = afi/100 clipped
    seed: Optional[int] = None           # set for reproducibility
    # Joint optimization of AFI threshold T% alongside the cell mask.
    # When True (default 0.4.756+), every candidate carries its own
    # ``T_norm ∈ [threshold_min_pct/threshold_max_pct, 1]`` and the
    # fitness function applies ``effective_mask = mask & (afi ≥ T*100)``
    # before the LOOCV R² + L0 penalty. Operators wanting the legacy
    # mask-only behaviour set this to False; T then stays at 0 and the
    # AFI eligibility filter is a no-op.
    optimize_threshold: bool = True
    threshold_min_pct: float = 0.0       # lower bound on T in raw % units
    threshold_max_pct: float = 50.0      # upper bound on T in raw % units
    # Seed value for the T population: when None, draw uniform random
    # in [threshold_min_pct, threshold_max_pct]; when set, every genome
    # starts near this value with small jitter so the GA can refine
    # from a known good T (e.g. one threshold_optimizer found earlier).
    threshold_init_pct: Optional[float] = None
    # Gaussian σ for per-generation T mutation, in normalized [0, 1]
    # space (0.05 ≈ 2.5 percentage points at threshold_max_pct=50%).
    threshold_mutation_sigma: float = 0.05


@dataclass
class GAResult:
    """Wraps the final state + history. Plots and CSV writers read from
    this directly so callers don't shuttle individual arrays around."""

    best_mask: np.ndarray            # (n_cells,) bool
    best_fitness: float
    best_r2: float                   # fitness without the L0 penalty
    history: pd.DataFrame            # columns: generation, best_fit, mean_fit, best_r2, n_selected, best_T_pct
    n_cells: int
    n_generations_run: int
    baseline_r2: float               # LOOCV R² with mask = all-True (no selection)
    best_T_pct: float = 0.0          # AFI threshold (raw %) for the best mask; 0 when optimize_threshold=False


def init_T_pop(
    rng: np.random.Generator,
    pop_size: int,
    cfg: "GAConfig",
) -> np.ndarray:
    """Initialize the per-candidate AFI threshold gene (T_pop), shape
    ``(pop_size,) float`` in normalized [0, 1] space.

    * ``cfg.optimize_threshold == False`` (legacy opt-out) → all zeros;
      AFI filter is a no-op, GA reduces to mask-only search.
    * ``optimize_threshold == True`` + ``threshold_init_pct is None``
      (default) → uniform random in ``[T_min_norm, 1.0]`` so the seed
      population spans the full configured T range.
    * ``optimize_threshold == True`` + ``threshold_init_pct`` set →
      small jitter (σ=0.02 in normalized space) around the seed, so the
      GA can refine from a known-good T (e.g. one threshold_optimizer
      already found) without losing population diversity.

    Extracted to a module-level helper so it's unit-testable in
    isolation (T_pop is otherwise local to ``run_ga``).
    """
    T_max = cfg.threshold_max_pct
    T_min_norm = cfg.threshold_min_pct / T_max if T_max > 0 else 0.0
    if not cfg.optimize_threshold:
        return np.zeros(pop_size, dtype=float)
    if cfg.threshold_init_pct is None:
        return rng.uniform(T_min_norm, 1.0, size=pop_size)
    seed_norm = float(cfg.threshold_init_pct) / T_max if T_max > 0 else 0.0
    return np.clip(
        seed_norm + rng.normal(0.0, 0.02, size=pop_size),
        T_min_norm, 1.0,
    )


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


def _tournament_idx(
    n_pop: int, fits: np.ndarray, k: int, rng: np.random.Generator,
) -> int:
    """Pick one parent via k-way tournament. Returns the WINNER INDEX
    (rather than the genome) so callers can use it to slice into
    multiple parallel population arrays — e.g. ``pop[idx]`` AND
    ``T_pop[idx]`` — keeping the mask and T genes paired through
    selection.
    """
    candidates = rng.integers(0, n_pop, size=k)
    return int(candidates[np.argmax(fits[candidates])])


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


def _mutate_T(
    t_norm: float,
    sigma: float,
    t_min_norm: float,
    t_max_norm: float,
    rng: np.random.Generator,
) -> float:
    """Gaussian perturbation of the T gene, clipped to its valid range.

    Used by run_ga when ``cfg.optimize_threshold`` is True. The mutation
    operates in the normalized ``[T_min_norm, T_max_norm]`` space — the
    same space ``init_T_pop`` returns. Caller is responsible for
    multiplying by ``cfg.threshold_max_pct`` when reporting in raw %.
    """
    new = float(t_norm) + float(rng.normal(0.0, sigma))
    return float(np.clip(new, t_min_norm, t_max_norm))


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
    # exceed the cropland-cell count for very small regions (e.g. the
    # "city" admin units with < min_cell_floor_abs cells);
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

    # T_pop: per-candidate AFI-threshold gene (normalized [0, 1]). See
    # ``init_T_pop`` for the init rule (depends on optimize_threshold +
    # threshold_init_pct). When optimize_threshold is False, T_pop is
    # all zeros and the AFI filter is a no-op.
    T_pop = init_T_pop(rng, pop_size, cfg)
    T_min_norm = (
        cfg.threshold_min_pct / cfg.threshold_max_pct
        if cfg.threshold_max_pct > 0 else 0.0
    )

    fits = np.array([
        fitness(
            pop[i], per_cell, y, cfg.l0_lambda, min_cells,
            T_norm=float(T_pop[i]), afi=afi, T_max=cfg.threshold_max_pct,
        )
        for i in range(pop.shape[0])
    ])

    history_rows = []
    best_seen = -np.inf
    stagnant = 0

    for gen in range(cfg.n_generations):
        # Track stats. The per-generation best_r2 / n_selected use the
        # EFFECTIVE mask (raw mask AND AFI eligibility), matching what
        # the fitness function actually scored — so the curve in
        # fitness_history.png reflects the cells that genuinely
        # contributed to the regression, not the cells the genome
        # nominally selected. When optimize_threshold=False (T=0 for
        # all candidates) the effective mask equals the raw mask, so
        # the legacy behaviour is preserved byte-for-byte.
        cur_best_idx = int(np.argmax(fits))
        cur_best = float(fits[cur_best_idx])
        cur_mean = float(np.mean(fits[np.isfinite(fits)])) if np.isfinite(fits).any() else float("nan")
        best_mask_now = pop[cur_best_idx]
        cur_T_norm = float(T_pop[cur_best_idx])
        cur_T_pct = cur_T_norm * cfg.threshold_max_pct
        if cur_T_norm > 0.0 and afi is not None:
            effective_now = best_mask_now & (afi >= cur_T_pct * 100.0)
        else:
            effective_now = best_mask_now
        cur_r2 = loocv_r2_multivariate(
            aggregate_over_mask(per_cell, effective_now), y
        )
        history_rows.append({
            "generation":  gen,
            "best_fit":    cur_best,
            "mean_fit":    cur_mean,
            "best_r2":     cur_r2,
            "n_selected":  int(effective_now.sum()),
            "best_T_pct":  cur_T_pct,
        })

        if logger is not None and (gen % 25 == 0 or gen == cfg.n_generations - 1):
            logger.info(
                f"  gen {gen:>4d}/{cfg.n_generations}: best_fit={cur_best:.4f} "
                f"best_r2={cur_r2:.4f} mean_fit={cur_mean:.4f} "
                f"n_selected={int(effective_now.sum())}/{n_cells} "
                f"T={cur_T_pct:.1f}%"
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

        # Build next population: elitism + tournament-selected offspring.
        # Mask and T are evolved together — tournament returns a single
        # winner_idx that's used to slice BOTH ``pop[idx]`` and
        # ``T_pop[idx]``, keeping the two genes paired through
        # selection. Crossover is per-bit uniform for the mask and a
        # 50/50 coin flip for T (mirrors the mask operator at p=0.5).
        # Mutation is bit-flip for the mask + Gaussian for T.
        elite_idx = np.argsort(fits)[-cfg.elitism:][::-1]
        new_pop = [pop[i].copy() for i in elite_idx]
        new_T_pop = [float(T_pop[i]) for i in elite_idx]
        while len(new_pop) < pop_size:
            p1_idx = _tournament_idx(pop.shape[0], fits, cfg.tournament_k, rng)
            p2_idx = _tournament_idx(pop.shape[0], fits, cfg.tournament_k, rng)
            # Mask: per-bit uniform crossover, then bit-flip mutation.
            child_mask = _uniform_crossover(
                pop[p1_idx], pop[p2_idx], cfg.crossover_p, rng,
            )
            child_mask = _mutate(child_mask, mut_rate, rng)
            # T: 50/50 swap from either parent, then Gaussian mutation
            # (only when optimize_threshold=True; otherwise T_pop stays
            # all zeros and mutate is a no-op).
            child_T = (
                float(T_pop[p1_idx]) if rng.random() < 0.5
                else float(T_pop[p2_idx])
            )
            if cfg.optimize_threshold:
                child_T = _mutate_T(
                    child_T, cfg.threshold_mutation_sigma,
                    T_min_norm, 1.0, rng,
                )
            new_pop.append(child_mask)
            new_T_pop.append(child_T)
        pop = np.asarray(new_pop, dtype=bool)
        T_pop = np.asarray(new_T_pop, dtype=float)
        fits = np.array([
            fitness(
                pop[i], per_cell, y, cfg.l0_lambda, min_cells,
                T_norm=float(T_pop[i]), afi=afi, T_max=cfg.threshold_max_pct,
            )
            for i in range(pop.shape[0])
        ])

    # Final pick. best_T_pct comes from the winning candidate's T_pop
    # entry (raw % units, denormalized from [0,1]). best_r2 is computed
    # on the EFFECTIVE mask — same convention as the per-generation
    # history rows above — so the reported R² matches what the GA
    # scored. Downstream callers use best_mask as the raw mask and
    # apply T separately if they want the effective view.
    final_idx = int(np.argmax(fits))
    best_mask = pop[final_idx].copy()
    best_fit = float(fits[final_idx])
    best_T_norm = float(T_pop[final_idx])
    best_T_pct = best_T_norm * cfg.threshold_max_pct
    if best_T_norm > 0.0 and afi is not None:
        best_effective = best_mask & (afi >= best_T_pct * 100.0)
    else:
        best_effective = best_mask
    best_r2 = loocv_r2_multivariate(
        aggregate_over_mask(per_cell, best_effective), y
    )

    return GAResult(
        best_mask=best_mask,
        best_fitness=best_fit,
        best_r2=best_r2 if np.isfinite(best_r2) else float("nan"),
        history=pd.DataFrame(history_rows),
        n_cells=n_cells,
        n_generations_run=len(history_rows),
        baseline_r2=baseline_r2 if np.isfinite(baseline_r2) else float("nan"),
        best_T_pct=float(best_T_pct),
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
            optimize_threshold=self._get(
                "optimize_threshold", str(defaults.optimize_threshold),
            ).strip().lower() in ("true", "1", "yes"),
            threshold_min_pct=float(self._get("threshold_min_pct", defaults.threshold_min_pct)),
            threshold_max_pct=float(self._get("threshold_max_pct", defaults.threshold_max_pct)),
            threshold_init_pct=(
                float(self._get("threshold_init_pct", "nan"))
                if self._get("threshold_init_pct", "")
                else None
            ),
            threshold_mutation_sigma=float(self._get(
                "threshold_mutation_sigma", defaults.threshold_mutation_sigma,
            )),
        )
        # Runner-level knobs (not GA inner-loop hyperparams).
        self.n_jobs = int(self._get("n_jobs", "-1"))
        self.write_production_mask = self._get(
            "write_production_mask", "True"
        ).strip().lower() in ("true", "1", "yes")
        self.do_plot = self._get("plot", "True").strip().lower() in (
            "true", "1", "yes",
        )
        # Annual masks (anti-overfitting): when True, run the GA n_years+1
        # times per region. For each historical year Y, the GA trains on
        # all years EXCEPT Y, producing mask_Y — used for year Y's EO
        # extraction. Year Y's own yield never sees the cell selection,
        # so the mask is genuinely held out and the overfitting failure
        # mode where the GA picks cells that happen to fit Y is closed.
        # Plus one pooled run on ALL years for current/forecast years
        # (which have no yield to hold out). Default OFF — annual mode
        # is roughly (n_years+1)× slower than the pooled-only default.
        self.annual_mask = self._get("annual_mask", "False").strip().lower() in (
            "true", "1", "yes",
        )
        # DOY-axis aggregation per variable. Defaults from
        # _DOY_AGG_DEFAULTS (NDVI=auc, T/P=mean). Override per variable
        # with ``{var}_doy_agg = max|mean|median|sum|auc|min``.
        # ``auc`` is treated as ``sum`` over the configured DOY samples
        # — i.e. seasonal integral assuming uniform cadence (the
        # constant cadence factor cancels in OLS).
        self.doy_agg: dict = {}
        for var, default in _DOY_AGG_DEFAULTS.items():
            raw = self._get(f"{var}_doy_agg", default).strip().lower()
            if raw not in _DOY_AGG_VALID:
                self.logger.warning(
                    f"  [CELL_OPTIMIZER] {var}_doy_agg = {raw!r} is not "
                    f"in {sorted(_DOY_AGG_VALID)} — falling back to "
                    f"default {default!r}"
                )
                raw = default
            self.doy_agg[var] = raw

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

    def regions_dir(
        self, country: str, crop: str, season: int, mode: str = "pooled",
    ) -> Path:
        """Per-region diagnostic dir. ``mode`` selects which fit variant:

        * ``"pooled"`` — the all-years GA (in-sample fit; the
          backwards-compatible default).
        * ``"held_out"`` — only populated when ``annual_mask = True``.
          Diagnostics computed from per-year leave-one-out masks
          (out-of-sample by construction).

        Both subdirs sit under the same ``regions_s{season}`` parent so
        a side-by-side ``ls pooled held_out`` makes the two views easy
        to diff.
        """
        d = self.summary_dir(country, crop) / f"regions_s{season}" / mode
        d.mkdir(parents=True, exist_ok=True)
        return d

    def cross_region_dir(self, mode: str = "pooled") -> Path:
        """Cross-region rollup dir. ``mode`` partitions the same way
        ``regions_dir`` does — ``pooled/`` for the all-years GA stats,
        ``held_out/`` for the per-year leave-one-out aggregates.

        The master ``summary.csv`` (with BOTH pooled and held_out
        columns side by side for easy inspection) sits at the parent
        ``_cross_region`` dir, not under a mode subdir.
        """
        d = (
            self.dir_output / "ml" / "analysis" / self.today_tag
            / "cell_optimizer" / "_cross_region" / mode
        )
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _cross_region_root(self) -> Path:
        """Root of the cross-region tree — used for the master
        summary.csv that carries both pooled + held_out columns."""
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

        When ``annual_mask = True``, additional per-year files are
        written alongside this one (see ``production_mask_path_for_year``)
        and geoextract should prefer the year-specific file when the
        extraction year matches.
        """
        return (
            self.dir_output / "cell_optimizer" / country / crop
            / f"{country}_{crop}_s{season}_optimized_mask.parquet"
        )

    def production_mask_path_for_year(
        self, country: str, crop: str, season: int, year: int,
    ) -> Path:
        """Per-year leave-one-out production mask path. Same parent dir
        as ``production_mask_path``, with a ``_y{year}`` suffix:

            ${dir_output}/cell_optimizer/{country}/{crop}/
                {country}_{crop}_s{season}_y{year}_optimized_mask.parquet

        Only written when ``annual_mask = True``. Geoextract loaders
        should try this path FIRST for a given (country, crop, season,
        year) and fall back to the pooled ``production_mask_path`` only
        when this file is missing (forecast/current years have no
        leave-one-out file because the GA needs that year's yield to
        produce one).
        """
        return (
            self.dir_output / "cell_optimizer" / country / crop
            / f"{country}_{crop}_s{season}_y{int(year)}_optimized_mask.parquet"
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
        # configured agg. NDVI defaults to AUC (sum over DOY); T and P
        # default to mean. Per-variable overrides come from
        # [CELL_OPTIMIZER] {var}_doy_agg in geocif.txt. ``auc`` maps to
        # pandas ``sum`` — area-under-curve over evenly-spaced DOY
        # samples is the sum up to a constant cadence factor that
        # cancels in OLS and correlation.
        def _pandas_agg(name: str) -> str:
            return "sum" if name == "auc" else name
        agg_map = {v: _pandas_agg(self.doy_agg.get(v, "mean")) for v in var_cols}
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

    def _build_production_rows(
        self, country, region, cell_meta, mask, T_pct=0.0,
    ):
        """Shape the per-cell included/excluded decisions into the
        production-parquet row contract. Used once per GA run (pooled
        or per-year-leave-out).

        ``mask`` is the RAW GA mask (boolean per cell). ``T_pct`` is
        the GA-selected AFI threshold in raw % units (0 when the
        opt-out path was active). The written ``included`` column is
        the EFFECTIVE decision (``_effective_mask`` helper) — i.e.
        what geoextract should respect. A new column
        ``region_threshold_pct`` carries T_pct broadcast across every
        cell of the region so geoextract or downstream consumers can
        recover the optimizer's T choice without re-deriving it.
        """
        afi_vals = cell_meta["afi"].to_numpy(dtype=float)
        effective = _effective_mask(mask, T_pct, afi_vals)
        rows = cell_meta.copy()
        rows["country"] = country
        rows["region"] = region
        rows["included"] = effective
        rows["region_threshold_pct"] = float(T_pct)
        return rows[[
            "country", "region", "region_id", "cell_id",
            "lat", "lon", "afi", "included", "region_threshold_pct",
        ]]

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

        # --- Pooled GA: trained on all years. Used for forecast/current
        # years when no held-out year is available, and as the fallback
        # mask when annual mode is off. Also drives the diagnostic plots
        # + cross-region summary (the per-year masks would multiply
        # plot+summary output by n_years and overwhelm the operator).
        result = run_ga(per_cell, y, self.ga, afi=afi_vec, logger=self.logger)

        self.logger.info(
            f"  pooled R^2 (representative cells) = {result.best_r2:.4f}, "
            f"R^2 (all cropland cells) = {result.baseline_r2:.4f}, "
            f"Δ = {(result.best_r2 - result.baseline_r2):+.4f}; "
            f"{result.best_mask.sum()}/{n_cells} cells selected"
        )

        # Per-year (leave-one-out) masks — anti-overfitting opt-in. For
        # each historical year Y, run the GA on data EXCLUDING Y so
        # mask_Y never saw year Y's yield. Then mask_Y is applied to
        # year Y's EO extraction downstream — out-of-sample by
        # construction. The pooled mask above remains the fallback for
        # current/forecast years (which have no yield to hold out).
        production_by_year: dict = {
            None: self._build_production_rows(
                country, region, cell_meta, result.best_mask,
                T_pct=result.best_T_pct,
            ),
        }
        results_by_year: dict = {}   # int year -> GAResult, used for held-out diagnostics
        if self.annual_mask:
            years_arr = np.asarray(years, dtype=int)
            for held_out_year in years_arr:
                keep_mask = years_arr != held_out_year
                per_cell_train = per_cell[:, keep_mask, :]
                y_train = y[keep_mask]
                n_train_finite = int(np.isfinite(y_train).sum())
                if n_train_finite < 5:
                    self.logger.warning(
                        f"  annual mask y={held_out_year}: only "
                        f"{n_train_finite} finite-yield years in training "
                        f"set; LOOCV R² needs >=5. Skipping this year."
                    )
                    continue
                result_y = run_ga(
                    per_cell_train, y_train, self.ga,
                    afi=afi_vec, logger=None,   # silence per-year inner logs
                )
                self.logger.info(
                    f"  annual y={int(held_out_year)}: R²="
                    f"{result_y.best_r2:.3f} (baseline {result_y.baseline_r2:.3f}), "
                    f"{int(result_y.best_mask.sum())}/{n_cells} cells, "
                    f"T={result_y.best_T_pct:.1f}%"
                )
                production_by_year[int(held_out_year)] = self._build_production_rows(
                    country, region, cell_meta, result_y.best_mask,
                    T_pct=result_y.best_T_pct,
                )
                results_by_year[int(held_out_year)] = result_y
        masks_by_year = {y: r.best_mask for y, r in results_by_year.items()}

        # Diagnostic outputs — pooled GA in regions_s{season}/pooled/.
        # The held-out variant lives in regions_s{season}/held_out/ and
        # is populated below only when annual_mask is on.
        out_dir_pooled = self.regions_dir(country, crop, season, mode="pooled")
        stem = f"{country}_{crop}_s{season}_{region}"
        np.save(out_dir_pooled / f"{stem}_best_mask.npy", result.best_mask)
        result.history.to_csv(out_dir_pooled / f"{stem}_history.csv", index=False)

        if self.do_plot:
            self._plot_diagnostics(
                result, per_cell, y, cell_meta, var_cols,
                out_dir=out_dir_pooled, stem=stem,
                country=country, region=region,
                years=years,
            )

        # Per-variable Pearson r — pooled (yield vs aggregated EO using
        # the pooled EFFECTIVE mask) AND, when annual_mask is on,
        # held-out (each year's EO aggregated by mask_Y AND eligible).
        # Both flavours flow into the summary row so the cross-region
        # rollup can split them. Using the EFFECTIVE mask here (not the
        # raw mask) keeps the summary's optimized_r_<var> column in
        # lockstep with the production parquet's `included` flag —
        # otherwise operators see one r in the diagnostic and a
        # different one downstream.
        base_x = aggregate_over_mask(per_cell, np.ones(n_cells, dtype=bool))
        effective_pooled = _effective_mask(
            result.best_mask, result.best_T_pct, afi_vec,
        )
        opt_x = aggregate_over_mask(per_cell, effective_pooled)
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

        # Held-out (per-year) diagnostics — only when annual_mask is on.
        # x_held_out[i] = aggregate of year-i per-cell EO using
        # mask_Y AND eligible-by-T_Y (the EFFECTIVE mask for that
        # year's GA). Production extraction for year Y applies T_Y's
        # AFI filter on top of mask_Y, so the held-out R² must use
        # effective masks too — otherwise summary's held_out R² would
        # disagree with what the per-year parquet's `included` column
        # actually drives in production.
        held_out_summary: dict = {}
        x_held_out = None
        if self.annual_mask and results_by_year:
            effective_masks_by_year = {
                yr: _effective_mask(r.best_mask, r.best_T_pct, afi_vec)
                for yr, r in results_by_year.items()
            }
            x_held_out = aggregate_held_out(
                per_cell, years, effective_masks_by_year,
            )
            held_out_r2 = loocv_r2_multivariate(x_held_out, y)
            held_out_per_var: dict = {}
            for vi, vname in enumerate(var_cols):
                xv = x_held_out[:, vi]
                m = np.isfinite(xv) & np.isfinite(y)
                if m.sum() >= 3 and float(np.nanstd(xv[m])) > 0 and float(np.nanstd(y[m])) > 0:
                    held_out_per_var[f"held_out_r_{vname}"] = float(
                        np.corrcoef(xv[m], y[m])[0, 1]
                    )
                else:
                    held_out_per_var[f"held_out_r_{vname}"] = float("nan")

            self.logger.info(
                f"  held-out (per-year masks) R^2 = "
                f"{held_out_r2 if np.isfinite(held_out_r2) else float('nan'):.4f}; "
                f"{len(masks_by_year)}/{len(years)} years contributed"
            )

            # Held-out T stats — mean and stddev of best_T_pct across
            # the leave-one-out years. Lets operators see whether each
            # year's GA agreed on a similar T (low stddev = stable
            # signal) or scattered (high stddev = T didn't matter or
            # data is noisy).
            per_year_T = np.array(
                [float(r.best_T_pct) for r in results_by_year.values()],
                dtype=float,
            )
            held_out_summary = {
                "held_out_optimized_r2": (
                    float(held_out_r2) if np.isfinite(held_out_r2)
                    else float("nan")
                ),
                "held_out_lift": (
                    float(held_out_r2 - result.baseline_r2)
                    if np.isfinite(held_out_r2) else float("nan")
                ),
                "held_out_n_years_used": int(len(masks_by_year)),
                "held_out_mean_T_pct": float(per_year_T.mean()) if per_year_T.size else 0.0,
                "held_out_std_T_pct":  float(per_year_T.std())  if per_year_T.size else 0.0,
                **held_out_per_var,
            }

            # Save the per-year per-region artifacts mirroring the
            # pooled ones, then call the same plot helpers with the
            # held-out inputs.
            out_dir_held = self.regions_dir(country, crop, season, mode="held_out")
            region_id_for_plots = self._extract_region_id(cell_meta)
            # Per-year mask matrix (n_years_done, n_cells) — preserves
            # the inter-year variation that the frequency vector
            # collapses.
            masks_matrix = np.stack(list(masks_by_year.values()), axis=0)
            np.save(
                out_dir_held / f"{stem}_per_year_masks.npy",
                masks_matrix,
            )
            # Selection frequency: fraction of leave-one-out years each
            # cell was kept. Mirrors result.best_mask in shape but
            # carries continuous information.
            selection_frequency = masks_matrix.mean(axis=0)
            np.save(
                out_dir_held / f"{stem}_selection_frequency.npy",
                selection_frequency,
            )
            # Concatenated GA convergence history with a held_out_year
            # column — counterpart to the pooled _history.csv.
            histories_concat = pd.concat(
                [
                    res.history.assign(held_out_year=int(y_label))
                    for y_label, res in results_by_year.items()
                ],
                ignore_index=True,
            )
            histories_concat.to_csv(
                out_dir_held / f"{stem}_history.csv", index=False,
            )

            if self.do_plot:
                # 1. Mask map — same helper, continuous selection
                # frequency instead of a 0/1 binary mask.
                self._plot_mask_map(
                    cell_meta=cell_meta,
                    selection=selection_frequency,
                    baseline_r2=result.baseline_r2,
                    optimized_r2=(
                        float(held_out_r2) if np.isfinite(held_out_r2)
                        else result.best_r2
                    ),
                    out_dir=out_dir_held, stem=stem,
                    country=country, region=region,
                    region_id=region_id_for_plots,
                    mode_label="held-out (per-year masks)",
                    n_years=len(masks_by_year),
                )
                # 2. Fitness history — multi-curve overlay, one per year.
                histories_for_plot = [
                    (int(y_label), res.history)
                    for y_label, res in results_by_year.items()
                ]
                self._plot_fitness_history(
                    histories=histories_for_plot,
                    baseline_r2=result.baseline_r2,
                    out_dir=out_dir_held, stem=stem, region=region,
                    mode_label="held-out (per-year masks)",
                )
                # 3. Cells comparison — same helper, x_held_out feeds the
                # right column instead of the pooled opt_x.
                self._plot_cells_comparison(
                    base_x=base_x, opt_x=x_held_out, y=y,
                    var_cols=var_cols, years=years,
                    out_dir=out_dir_held, stem=stem,
                    region=region,
                    title_suffix="yield vs EO (held-out, per-year masks)",
                )

        # Per-region summary row (returned to caller for cross-region
        # rollup). Pooled stats + held_out stats (NaN when annual_mask
        # is off). Per-year stats would multiply rows by n_years;
        # aggregate analysis is downstream.
        # n_effective: cells the GA actually kept after applying its
        # chosen T (= what geoextract will aggregate over). When T=0
        # this equals n_selected; when T>0 it can be smaller.
        if result.best_T_pct > 0.0:
            eligible_pooled = afi_vec >= result.best_T_pct * 100.0
            n_effective = int((result.best_mask & eligible_pooled).sum())
        else:
            n_effective = int(result.best_mask.sum())
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
            "annual_mask":     bool(self.annual_mask),
            # T-gene: the AFI threshold the GA picked for the pooled
            # mask, in raw % units. 0 when optimize_threshold=False
            # (opt-out path). n_effective is the per-region cell count
            # AFTER applying T's eligibility filter — what production
            # extraction will actually aggregate over.
            "best_T_pct":      float(result.best_T_pct),
            "n_effective":     n_effective,
            **per_var_r,
            **held_out_summary,
        }
        return {"summary": summary, "production_rows_by_year": production_by_year}

    # ------------------------------------------------------------------
    # Diagnostic plots
    # ------------------------------------------------------------------

    def _load_country_boundary_gdf(self, country: str):
        """Lazy-load and per-process-cache the country's boundary
        GeoDataFrame. Used by ``_add_locator_inset`` to draw the
        country-context inset on each mask map. Returns None if
        geopandas is unavailable, the boundary file is missing, or
        the country doesn't appear in the shapefile.

        Delegates to ``geocif.utils.load_country_boundary_gdf``, which
        reads the config-driven column mapping (``[adm_shapefile]``
        section in geobase.txt with ``adm0_col = ADMIN0`` etc.) and
        renames columns to the standard ``ADM0_NAME / ADM1_NAME /
        ADM_ID`` set. That keeps the per-country filter and the
        downstream highlight match working regardless of which
        shapefile convention is in play.

        Caching is intra-process — joblib workers each load once.
        """
        if not hasattr(self, "_boundary_cache"):
            self._boundary_cache = {}
        if country in self._boundary_cache:
            return self._boundary_cache[country]

        try:
            import geopandas as gpd  # noqa: F401  — verify importable
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
            from geocif.utils import load_country_boundary_gdf
            gdf = load_country_boundary_gdf(self.parser, fp, country=country)
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                f"  failed to read boundary shapefile {fp}: {exc}"
            )
            self._boundary_cache[country] = None
            return None

        # Keep only polygon geometries (drop stray points / lines).
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

    @staticmethod
    def _extract_region_id(cell_meta) -> object:
        """First non-null region_id from cell_meta. Used by the inset
        locator to prefer an ADM_ID match over name-matching — the
        only reliable disambiguator when region names collide."""
        if "region_id" in cell_meta.columns and not cell_meta.empty:
            rid_val = cell_meta["region_id"].iloc[0]
            if pd.notna(rid_val):
                return rid_val
        return None

    def _plot_mask_map(
        self, *, cell_meta, selection,
        baseline_r2, optimized_r2,
        out_dir, stem, country, region, region_id,
        mode_label, n_years=None,
    ):
        """Per-region cell-position scatter — color encodes AFI %,
        marker size encodes ``selection`` (fraction of GA runs that
        kept the cell). Same call signature works for both modes:

        * Pooled (``selection`` ∈ {0, 1}): the two values collapse to
          the original "in / out" view — small/faded for never, large/
          vivid with black ring for always.
        * Held-out (``selection`` ∈ [0, 1]): size and alpha grade
          continuously with selection frequency, showing both *which*
          cells were ever picked and *how often* across the leave-one-
          out years.

        ``mode_label`` lands in the title; ``n_years`` shows how many
        leave-one-out runs the frequency was computed from (held-out
        only — omit for pooled).
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        sel = np.asarray(selection, dtype=float)
        afi_pct = cell_meta["afi"].to_numpy(dtype=float) / 100.0
        afi_vmin = float(np.nanmin(afi_pct)) if afi_pct.size else 0.0
        afi_vmax = float(np.nanmax(afi_pct)) if afi_pct.size else 100.0
        if afi_vmax <= afi_vmin:
            afi_vmax = afi_vmin + 1.0

        # Bin cells into never-selected vs ever-selected so the never
        # population recedes visually but stays readable.
        never = sel <= 0.0
        ever = ~never

        fig, ax = plt.subplots(figsize=(7, 6))
        # Never-selected: small + faded, AFI-coloured.
        if never.any():
            ax.scatter(
                cell_meta.loc[never, "lon"], cell_meta.loc[never, "lat"],
                c=afi_pct[never], s=12, cmap="viridis",
                vmin=afi_vmin, vmax=afi_vmax, alpha=0.30,
                label=f"other cropland (n={int(never.sum())})",
                edgecolors="none",
            )
        # Ever-selected: size and alpha scale with selection level.
        # For pooled (sel ∈ {0, 1}) this collapses to fixed (28, 0.95).
        # For held-out (sel ∈ [0, 1]) cells picked more often render
        # larger and more vivid.
        sc_in = None
        if ever.any():
            sel_ever = sel[ever]
            sizes = 14.0 + 14.0 * sel_ever          # 14 → 28 as sel goes 0 → 1
            alphas = 0.55 + 0.40 * sel_ever         # 0.55 → 0.95
            edge_widths = 0.20 + 0.20 * sel_ever    # 0.20 → 0.40
            sc_in = ax.scatter(
                cell_meta.loc[ever, "lon"], cell_meta.loc[ever, "lat"],
                c=afi_pct[ever], s=sizes, cmap="viridis",
                vmin=afi_vmin, vmax=afi_vmax,
                alpha=alphas, edgecolors="black", linewidths=edge_widths,
                label=f"representative (n={int(ever.sum())})",
            )
        cbar_handle = sc_in if sc_in is not None else None
        if cbar_handle is not None:
            fig.colorbar(
                cbar_handle, ax=ax, fraction=0.04, pad=0.02,
                label="AFI (crop fraction %)",
            )

        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        years_suffix = f" across {n_years} leave-one-out years" if n_years else ""
        ax.set_title(
            f"{_display_region_name(region)} — representative cells "
            f"[{mode_label}]{years_suffix}\n"
            f"R²: {baseline_r2:.3f} (all cropland cells) → "
            f"{optimized_r2:.3f} (representative cells), "
            f"Δ = {(optimized_r2 - baseline_r2):+.3f}"
        )
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(True, alpha=0.3)
        self._add_locator_inset(
            ax, country=country, region=region, region_id=region_id,
        )
        fig.tight_layout()
        fig.savefig(out_dir / f"{stem}_mask_map.png", dpi=130)
        plt.close(fig)

    def _plot_fitness_history(
        self, *, histories, baseline_r2, out_dir, stem, region,
        mode_label,
    ):
        """GA convergence trace. ``histories`` is a list of (label_or_None,
        DataFrame) pairs:

        * Pooled mode: one (None, history) entry. Renders the classic
          best_fit / mean_fit / best_r2 trio plus the baseline line.
        * Held-out mode: one entry per leave-one-out year. Each year's
          best_r2 curve is drawn faded, and a per-generation median
          (across years) is overlaid in bold. Lets the operator spot
          year-to-year convergence inconsistencies at a glance.

        Both variants share the equation annotation + plain-English
        caption — that text is the same regardless of mode.
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return
        if not histories:
            return

        fig, ax = plt.subplots(figsize=(8, 4.5))
        is_multi = len(histories) > 1
        if not is_multi:
            # Pooled-style: full best_fit + mean_fit + best_r2 stack.
            _, h = histories[0]
            ax.plot(h["generation"], h["best_fit"], color="#1f77b4",
                    linewidth=1.6, label="best fitness")
            ax.plot(h["generation"], h["mean_fit"], color="#1f77b4",
                    linewidth=1.0, alpha=0.4, linestyle="--",
                    label="mean fitness")
            ax.plot(h["generation"], h["best_r2"], color="#d62728",
                    linewidth=1.4, label="best R²")
        else:
            # Held-out-style: faded best_r2 per year + bold median curve.
            # `years_arr` indexes a viridis ramp so the eye can see if
            # earlier vs later leave-out years converge differently.
            year_labels = [label for label, _ in histories if label is not None]
            cmap = plt.get_cmap("viridis")
            if year_labels:
                lo, hi = min(year_labels), max(year_labels)
            else:
                lo, hi = 0, len(histories) - 1
            # Collect best_r2 across years on a common generation grid
            # via outer-merge for the median curve. NaNs are tolerated
            # by np.nanmedian.
            all_r2 = []
            for label, h in histories:
                t = (label - lo) / max(1, (hi - lo)) if label is not None else 0.5
                ax.plot(
                    h["generation"], h["best_r2"],
                    color=cmap(t), linewidth=0.9, alpha=0.40,
                )
                all_r2.append((h["generation"].to_numpy(), h["best_r2"].to_numpy()))
            # Median curve: align on max-generation grid.
            max_gen = max(int(g.max()) for g, _ in all_r2) if all_r2 else 0
            stack = np.full((len(all_r2), max_gen + 1), np.nan)
            for i, (g, r) in enumerate(all_r2):
                g_int = g.astype(int)
                # Last-known-value fill: each year's GA may early-stop,
                # so propagate the final best_r2 forward across the
                # remaining generations before taking the cross-year
                # median. Otherwise NaNs would dominate.
                last_val = np.nan
                cur_r = np.full(max_gen + 1, np.nan)
                lookup = dict(zip(g_int, r))
                for gen in range(max_gen + 1):
                    if gen in lookup:
                        last_val = lookup[gen]
                    cur_r[gen] = last_val
                stack[i] = cur_r
            median_curve = np.nanmedian(stack, axis=0)
            ax.plot(
                np.arange(max_gen + 1), median_curve,
                color="black", linewidth=2.0,
                label=f"median best R² across {len(histories)} years",
            )

        ax.axhline(
            baseline_r2, color="gray", linestyle=":", linewidth=1.0,
            label=f"baseline R² = {baseline_r2:.3f}",
        )
        ax.set_xlabel("generation")
        ax.set_ylabel("fitness / R²")
        ax.set_title(
            f"{_display_region_name(region)} — GA convergence [{mode_label}]"
        )
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, alpha=0.3)
        # Fitness equation + plain-English caption — same regardless of mode.
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
        caption = (
            "Fitness = how well a cell-mask predicts yield (R²), minus a "
            "small penalty for using too many cells (λ × fraction-of-"
            "cells-selected).\n"
            "The single number the GA tries to maximise."
        )
        fig.tight_layout(rect=[0, 0.12, 1, 1])
        fig.text(
            0.5, 0.02, caption,
            ha="center", va="bottom",
            fontsize=8, style="italic",
        )
        fig.savefig(out_dir / f"{stem}_fitness_history.png", dpi=130)
        plt.close(fig)

    def _plot_diagnostics(
        self, result, per_cell, y, cell_meta, var_cols,
        out_dir: Path, stem: str, country: str, region: str,
        years=None,
    ):
        """Pooled-mode per-region diagnostic plots. Three figures:
        ``_mask_map.png`` (binary in/out), ``_fitness_history.png``
        (GA convergence), ``_cells_comparison.png`` (yield-vs-EO
        scatter). All three reuse the same helpers as the held-out
        variant — see ``process_region`` for the held-out call site.
        """
        region_id = self._extract_region_id(cell_meta)
        self._plot_mask_map(
            cell_meta=cell_meta,
            selection=result.best_mask.astype(float),
            baseline_r2=result.baseline_r2, optimized_r2=result.best_r2,
            out_dir=out_dir, stem=stem,
            country=country, region=region, region_id=region_id,
            mode_label="pooled",
        )
        self._plot_fitness_history(
            histories=[(None, result.history)],
            baseline_r2=result.baseline_r2,
            out_dir=out_dir, stem=stem, region=region,
            mode_label="pooled",
        )
        # Use the EFFECTIVE mask (raw mask AND eligible-by-T) so the
        # right panel of cells_comparison reflects exactly what
        # production extraction will aggregate. Matches per_var_r and
        # the parquet's `included` column.
        afi_vec = cell_meta["afi"].to_numpy(dtype=float)
        effective_pooled = _effective_mask(
            result.best_mask, result.best_T_pct, afi_vec,
        )
        base_x = aggregate_over_mask(per_cell, np.ones(per_cell.shape[0], dtype=bool))
        opt_x = aggregate_over_mask(per_cell, effective_pooled)
        self._plot_cells_comparison(
            base_x=base_x, opt_x=opt_x, y=y, var_cols=var_cols,
            years=years if years is not None
                  else np.arange(per_cell.shape[1], dtype=int),
            out_dir=out_dir, stem=stem, region=region,
            title_suffix="yield vs EO: all cells vs representative cells",
        )
        self.logger.info(f"  wrote diagnostic plots to {out_dir}")

    def _plot_cells_comparison(
        self, *, base_x, opt_x, y, var_cols, years, out_dir, stem, region,
        title_suffix,
    ):
        """Per-region yield-vs-EO scatter — one row per var, two cols
        (all-cells baseline left, optimizer-selected right). Used by:

        * Pooled diagnostic (``opt_x`` = pooled mask's aggregation).
        * Held-out diagnostic (``opt_x`` = per-year mask aggregation
          ``x_held_out``) when ``annual_mask = True``.

        Dots = years; colour ramp = year (viridis). NDVI rescaled to
        unit scale when present. Both call sites get identical layout
        so visual comparison is direct.
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"  matplotlib unavailable: {exc}")
            return

        n_vars = len(var_cols)
        # constrained_layout instead of tight_layout below — fig.colorbar
        # with ax=<full subplot array> isn't compatible with tight_layout
        # and emits a UserWarning per region every run. constrained
        # layout handles the shared colorbar geometry natively.
        fig, axes = plt.subplots(
            n_vars, 2, figsize=(11, 3.5 * n_vars),
            sharey=False, squeeze=False,
            layout="constrained",
        )

        years_arr = np.asarray(years, dtype=int)
        last_sc = None
        for vi, v in enumerate(var_cols):
            display_name = _display_var_name(v)
            for ci, (xv_raw, title) in enumerate(
                [(base_x[:, vi], "all cropland cells"),
                 (opt_x[:, vi], "representative cells")]
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

        if last_sc is not None:
            cbar = fig.colorbar(
                last_sc, ax=axes, fraction=0.025, pad=0.02, label="year",
            )
            yr_min, yr_max = int(years_arr.min()), int(years_arr.max())
            n_ticks = min(8, max(2, yr_max - yr_min + 1))
            tick_positions = np.linspace(yr_min, yr_max, n_ticks).round().astype(int)
            cbar.set_ticks(tick_positions)
            cbar.set_ticklabels([str(t) for t in tick_positions])

        fig.suptitle(
            f"{_display_region_name(region)} — {title_suffix}",
            fontsize=11,
        )
        # constrained_layout (set at subplots time) handles spacing —
        # no manual tight_layout call needed.
        fig.savefig(out_dir / f"{stem}_cells_comparison.png", dpi=130)
        plt.close(fig)

    # ------------------------------------------------------------------
    # Cross-region rollup
    # ------------------------------------------------------------------

    def write_cross_region_summary(self, summary_rows):
        if not summary_rows:
            self.logger.warning("  no per-region results — skipping cross-region summary.")
            return

        df = pd.DataFrame(summary_rows)
        # Master CSV at the cross-region root (NOT inside a mode subdir)
        # — carries every column (pooled + held_out side by side) for
        # one-stop inspection across every country / crop / season.
        master_dir = self._cross_region_root()
        master_csv = master_dir / "summary.csv"
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

        # Build the list of (mode, lift_col, optimized_col, per_var_r_prefix)
        # tuples to emit. Pooled is always emitted; held-out only when the
        # column is actually populated (annual_mask had data in at least
        # one region of this run).
        modes_to_emit = [
            ("pooled", "lift", "optimized_r2", "optimized_r_"),
        ]
        if "held_out_optimized_r2" in df.columns and df["held_out_optimized_r2"].notna().any():
            modes_to_emit.append(
                ("held_out", "held_out_lift", "held_out_optimized_r2", "held_out_r_"),
            )

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
            stem = f"s{season}"

            # Mean area per region — pulled once per combo via the
            # canonical add_statistics dispatcher; reused across modes.
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

            for mode, lift_col, opt_col, per_var_r_prefix in modes_to_emit:
                # For held_out, drop rows where the held-out columns are
                # NaN (regions whose annual_mask runs produced no
                # successful per-year masks). Avoids plotting a histogram
                # over NaNs and gives a clean region count in the title.
                if mode == "held_out":
                    sub_grp = grp[grp[opt_col].notna()].copy()
                else:
                    sub_grp = grp.copy()

                sub_dir = self.cross_region_dir(mode=mode) / country / crop
                sub_dir.mkdir(parents=True, exist_ok=True)

                sub_csv = sub_dir / f"summary_{stem}.csv"
                sub_grp.to_csv(sub_csv, index=False)

                if len(sub_grp) < 2:
                    self.logger.info(
                        f"  {country}/{crop}/{stem}/{mode}: only "
                        f"{len(sub_grp)} regions, skipping plots"
                    )
                    continue

                self._cross_region_plots(
                    sub_grp, sub_dir, stem, country, crop, season, plt,
                    lift_col=lift_col, opt_col=opt_col,
                    per_var_r_prefix=per_var_r_prefix, mode=mode,
                )
                self.logger.info(
                    f"  cross-region plots ({mode}) → {sub_dir} "
                    f"({len(sub_grp)} regions)"
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

    def _cross_region_plots(
        self, grp, sub_dir, stem, country, crop, season, plt,
        *, lift_col="lift", opt_col="optimized_r2",
        per_var_r_prefix="optimized_r_", mode="pooled",
    ):
        """Render the cross-region diagnostics for one (country, crop,
        season) group: R² improvement histogram + all-vs-representative
        scatter + per-variable r impact.

        ``lift_col`` / ``opt_col`` / ``per_var_r_prefix`` parametrize
        the source columns so the same layout serves both the pooled
        run (``lift``, ``optimized_r2``, ``optimized_r_<var>``) and the
        held-out run (``held_out_lift``, ``held_out_optimized_r2``,
        ``held_out_r_<var>``). ``mode`` only shapes title text — the
        actual values come from ``grp[<col>]``.
        """
        mode_label = {"pooled": "pooled (in-sample)",
                      "held_out": "held-out (per-year masks)"}.get(mode, mode)

        # 1. R² improvement histogram (representative − all cropland cells)
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(grp[lift_col], bins=min(20, max(5, len(grp) // 2)),
                color="#1f77b4", alpha=0.8, edgecolor="black")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.axvline(grp[lift_col].mean(), color="red", linestyle="--",
                   linewidth=1.2,
                   label=f"mean Δ = {grp[lift_col].mean():+.3f}")
        ax.set_xlabel(
            "LOOCV R² improvement (representative cells − all cropland cells)"
        )
        ax.set_ylabel("regions")
        ax.set_title(
            f"{country.title()} {crop.title()} s{season} — "
            f"R² improvement from representative cells [{mode_label}], "
            f"{len(grp)} regions"
        )
        ax.legend(loc="best", fontsize=9)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(sub_dir / f"r2_improvement_{stem}.png", dpi=130)
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
            grp["baseline_r2"], grp[opt_col],
            c=grp[lift_col].to_numpy(), cmap="RdYlGn",
            s=sizes, alpha=0.85, edgecolors="black", linewidths=edge_widths,
        )
        lo = float(min(grp["baseline_r2"].min(), grp[opt_col].min(), 0.0)) - 0.05
        hi = float(max(grp["baseline_r2"].max(), grp[opt_col].max(), 1.0)) + 0.05
        ax.plot([lo, hi], [lo, hi], color="gray", linestyle="--",
                linewidth=1.0, alpha=0.7,
                label="y = x (no improvement)")
        # Label top-5 by improvement so the biggest wins are named.
        for _, row in grp.nlargest(min(5, len(grp)), lift_col).iterrows():
            ax.annotate(
                str(row["region"]),
                xy=(row["baseline_r2"], row[opt_col]),
                xytext=(4, 4), textcoords="offset points",
                fontsize=8, alpha=0.85,
            )
        fig.colorbar(
            sc, ax=ax, fraction=0.04, pad=0.02,
            label="Δ R² (representative − all cells)",
        )

        # Title — note size encoding when active.
        if has_area and area_finite.any():
            size_hint = "; dot size ∝ mean area (ha, log)"
        else:
            size_hint = ""
        ax.set_xlabel("R² with all cropland cells")
        ax.set_ylabel("R² with representative cells")
        ax.set_title(
            f"{country.title()} {crop.title()} s{season} — "
            f"R² with representative vs all cells [{mode_label}]\n"
            f"({len(grp)} regions; mean Δ = "
            f"{grp[lift_col].mean():+.3f}{size_hint})"
        )
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_aspect("equal")

        # Size legend showing 10th / 50th / 90th-percentile areas, when
        # area is encoded. Lower-left corner stays clear of the Δ R²
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
        fig.savefig(sub_dir / f"r2_comparison_{stem}.png", dpi=130)
        plt.close(fig)

        # 3. Per-variable Pearson r — one row per variable present in
        # summary.csv (NDVI / tmax / tmin / precip etc.). Each row:
        # r with all cropland cells on the X-axis, r with representative
        # cells on the Y, one dot per region, y=x reference line,
        # colour by Δr, top-3 regions labelled. Complements
        # r2_comparison.png (which is joint multivariate R²) by showing
        # how the cell selection affects each variable's individual
        # correlation with yield.
        self._plot_r_per_variable(
            grp, sub_dir, stem, country, crop, season, plt,
            per_var_r_prefix=per_var_r_prefix, mode=mode,
        )

    def _plot_r_per_variable(
        self, grp, sub_dir, stem, country, crop, season, plt,
        *, per_var_r_prefix="optimized_r_", mode="pooled",
    ):
        """Per-variable r-impact across regions. Reads
        ``baseline_r_<var>`` and ``{per_var_r_prefix}<var>`` columns
        from the summary DataFrame; silently skips when none are
        present (older summaries or single-var parquets that only
        produce a baseline column).
        """
        mode_label = {"pooled": "pooled (in-sample)",
                      "held_out": "held-out (per-year masks)"}.get(mode, mode)

        # Discover which variables have baseline + <prefix><var> columns.
        var_pairs = []
        for col in grp.columns:
            if col.startswith("baseline_r_"):
                var = col[len("baseline_r_"):]
                opt_col = f"{per_var_r_prefix}{var}"
                if opt_col in grp.columns:
                    var_pairs.append((var, col, opt_col))
        if not var_pairs:
            self.logger.info(
                f"  {country}/{crop}/{stem}/{mode}: no per-variable r columns "
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
                    linewidth=1.0, alpha=0.7, label="y = x")
            ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)
            ax.axvline(0, color="black", linewidth=0.4, alpha=0.4)
            # Label top-3 by |Δr|.
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
                label=f"Δ r for {_display_var_name(var)}",
            )
            mean_lift = float(sub["r_lift"].mean())
            ax.set_xlabel(
                f"r — yield vs {_display_var_name(var)} (all cropland cells)"
            )
            ax.set_ylabel(
                f"r — yield vs {_display_var_name(var)} (representative cells)"
            )
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
            f"per-variable Pearson r: all cells vs representative cells "
            f"[{mode_label}]",
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

        # Progress bar driven by per-region completion. With n_jobs > 1
        # the joblib workers write nothing to the parent stdout (their
        # logger handles aren't picklable), so without this bar the
        # operator only sees the startup banner until the run finishes.
        # The postfix shows the most recently completed region.
        from tqdm.auto import tqdm
        pbar_desc = f"{country}/{crop}/s{season}"

        if self.n_jobs == 1:
            results = []
            with tqdm(total=len(regions), desc=pbar_desc) as pbar:
                for region in regions:
                    try:
                        r = self.process_region(country, crop, season, region)
                    except Exception as exc:  # noqa: BLE001
                        self.logger.error(
                            f"  process_region failed on {region}: {exc}"
                        )
                        r = None
                    pbar.set_postfix_str(f"last={region}")
                    pbar.update(1)
                    results.append(r)
        else:
            from joblib import Parallel, delayed
            # Workers re-instantiate CellOptimizer from the original
            # config-file path because BaseGeo's logger handle isn't
            # picklable. Each worker reads its own region from the
            # parquet — the per-worker IO overhead is small compared
            # to the GA's runtime (~100s/region single-thread).
            #
            # ``return_as='generator_unordered'`` lets tqdm tick on
            # each completed region instead of blocking until all of
            # them finish. Requires joblib >= 1.3 (pinned via geocif
            # deps).
            try:
                results_iter = Parallel(
                    n_jobs=self.n_jobs, backend="loky",
                    return_as="generator_unordered",
                )(
                    delayed(_process_region_worker)(
                        self._config_files, country, crop, season, region,
                    )
                    for region in regions
                )
                # Workers return (region_name, payload) tuples — see
                # _process_region_worker. The tuple lets the postfix
                # name the region even when the payload is None
                # (region skipped or worker error), which is the
                # common case for the first few completions (tiny
                # "city" regions with insufficient yield years).
                results = []
                with tqdm(total=len(regions), desc=pbar_desc) as pbar:
                    for wrapped in results_iter:
                        region_done, r = wrapped
                        status = "skipped" if r is None else "done"
                        pbar.set_postfix_str(f"{status}: {region_done}")
                        pbar.update(1)
                        results.append(r)
            except TypeError:
                # joblib < 1.3 doesn't support return_as — fall back
                # to a blocking call with a single end-of-batch update.
                # No per-region tick but the run still works. Strip
                # the (region, payload) wrapper so downstream code
                # sees the same shape as the n_jobs=1 path.
                self.logger.warning(
                    "  joblib < 1.3 detected — per-region progress bar "
                    "disabled; upgrade joblib for live ticks"
                )
                wrapped_results = Parallel(n_jobs=self.n_jobs, backend="loky")(
                    delayed(_process_region_worker)(
                        self._config_files, country, crop, season, region,
                    )
                    for region in regions
                )
                results = [r for _, r in wrapped_results]

        # Filter Nones (skipped regions). Each surviving result carries a
        # ``production_rows_by_year`` dict keyed by year (None = pooled
        # / forecast-year fallback, int = leave-one-out mask for that
        # year). Bucket by year so each year's parquet sees every
        # region's rows.
        summary_rows = []
        frames_by_year: dict = {}
        for r in results:
            if r is None:
                continue
            summary_rows.append(r["summary"])
            rows_by_year = r.get("production_rows_by_year")
            if rows_by_year is None:
                continue
            for year_key, frame in rows_by_year.items():
                frames_by_year.setdefault(year_key, []).append(frame)

        if frames_by_year:
            # Pooled (year_key=None) drives the production-mask default
            # AND the pooled national-mask plot. Per-year frames feed
            # the held-out national-mask via per-cell mean(included)
            # frequency.
            pooled_frames = frames_by_year.get(None, [])
            combined_pooled = (
                pd.concat(pooled_frames, ignore_index=True)
                if pooled_frames else None
            )
            if self.write_production_mask:
                for year_key, frames in frames_by_year.items():
                    combined = pd.concat(frames, ignore_index=True)
                    self._write_production_mask(
                        country, crop, season, combined, year=year_key,
                    )
            if self.do_plot and combined_pooled is not None:
                self._plot_national_mask(
                    country, crop, season, combined_pooled,
                    mode="pooled", selection_col="included",
                )
                # Held-out national mask — selection frequency per cell
                # across leave-one-out years. Built from the per-year
                # frames (those keyed by int years, not None).
                per_year_frames = [
                    df for k, frames in frames_by_year.items()
                    if k is not None for df in frames
                ]
                if per_year_frames:
                    combined_held = pd.concat(per_year_frames, ignore_index=True)
                    # Per-cell selection frequency = mean(included)
                    # across years for the same (country, region, cell_id).
                    # Carry through the static metadata (lat, lon, afi)
                    # via 'first' since they're invariant.
                    freq_df = (
                        combined_held
                        .assign(included=combined_held["included"].astype(float))
                        .groupby(
                            ["country", "region", "region_id", "cell_id"],
                            sort=False, as_index=False,
                        )
                        .agg(
                            lat=("lat", "first"),
                            lon=("lon", "first"),
                            afi=("afi", "first"),
                            frequency=("included", "mean"),
                        )
                    )
                    self._plot_national_mask(
                        country, crop, season, freq_df,
                        mode="held_out", selection_col="frequency",
                    )

        return summary_rows

    def _plot_national_mask(
        self, country: str, crop: str, season: int, df_cells,
        mode: str = "pooled", selection_col: str = "included",
    ) -> None:
        """Country-scale map of every cell across every region for one
        (country, crop, season) combo. ``selection_col`` is the float-
        or-bool column carrying each cell's selection level:

        * Pooled (``selection_col="included"``, bool): in/out binary —
          two visual classes, mirroring the per-region ``_mask_map.png``.
        * Held-out (``selection_col="frequency"``, float ∈ [0, 1]):
          marker size and alpha grade with the leave-one-out selection
          frequency. ``0`` = never selected, ``1`` = every year.

        File goes under ``summary_dir(country, crop)/{mode}/``. Same
        helper renders both views — the selection column is the only
        thing that changes.
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
        if selection_col not in df_cells.columns:
            self.logger.warning(
                f"  national mask ({mode}): selection column "
                f"{selection_col!r} missing from df_cells; skipping"
            )
            return

        # AFI is percent × 100 in the parquet (geoprepare convention);
        # divide for an honest 0..100 % colourbar.
        afi_pct = df_cells["afi"].astype(float).to_numpy() / 100.0
        afi_vmin = float(np.nanmin(afi_pct)) if afi_pct.size else 0.0
        afi_vmax = float(np.nanmax(afi_pct)) if afi_pct.size else 100.0
        if afi_vmax <= afi_vmin:
            afi_vmax = afi_vmin + 1.0

        sel = df_cells[selection_col].astype(float).to_numpy()
        never_mask = sel <= 0.0
        ever_mask = ~never_mask
        df_never = df_cells[never_mask]
        df_ever = df_cells[ever_mask]

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

        # Never-selected cells: small + faded.
        if not df_never.empty:
            ax.scatter(
                df_never["lon"], df_never["lat"],
                c=afi_pct[never_mask], cmap="viridis",
                vmin=afi_vmin, vmax=afi_vmax,
                s=4, alpha=0.25, edgecolors="none",
                label=f"other cropland (n={len(df_never):,})",
            )
        # Ever-selected: size + alpha scale with selection level.
        # Pooled (sel ∈ {0, 1}): collapses to (10, 0.95) — original
        # binary view. Held-out: continuous from (5, 0.50) at sel=0+
        # up to (12, 0.95) at sel=1.
        sc_in = None
        if not df_ever.empty:
            sel_ever = sel[ever_mask]
            sizes = 5.0 + 7.0 * sel_ever          # 5 → 12
            alphas = 0.50 + 0.45 * sel_ever       # 0.50 → 0.95
            sc_in = ax.scatter(
                df_ever["lon"], df_ever["lat"],
                c=afi_pct[ever_mask], cmap="viridis",
                vmin=afi_vmin, vmax=afi_vmax,
                s=sizes, alpha=alphas,
                edgecolors="black", linewidths=0.15,
                label=f"representative (n={len(df_ever):,})",
            )
        if sc_in is not None:
            fig.colorbar(sc_in, ax=ax, fraction=0.04, pad=0.02,
                         label="AFI (crop fraction %)")

        n_ever = int(ever_mask.sum())
        n_total = int(len(df_cells))
        pct_ever = (100.0 * n_ever / n_total) if n_total else 0.0
        country_display = country.replace("_", " ").title()
        crop_display = crop.replace("_", " ").title()
        mode_suffix = {
            "pooled": "",
            "held_out": " [held-out, marker size = selection frequency]",
        }.get(mode, "")
        ax.set_xlabel("longitude")
        ax.set_ylabel("latitude")
        ax.set_title(
            f"{country_display} {crop_display} s{season} — "
            f"representative cells{mode_suffix}\n"
            f"{n_ever:,}/{n_total:,} cells ({pct_ever:.1f}%) "
            f"across {df_cells['region'].nunique()} regions"
        )
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)
        if n_ever or len(df_never):
            ax.legend(loc="best", fontsize=9)
        fig.tight_layout()

        # File sits at country/crop/{mode} scope so the pooled vs
        # held-out separation is consistent with the per-region and
        # cross-region diagnostics.
        mode_dir = self.summary_dir(country, crop) / mode
        mode_dir.mkdir(parents=True, exist_ok=True)
        out_path = mode_dir / f"{country}_{crop}_s{season}_national_mask.png"
        fig.savefig(out_path, dpi=130)
        plt.close(fig)
        self.logger.info(
            f"  wrote {mode} national mask map -> {out_path} "
            f"({n_ever:,}/{n_total:,} cells)"
        )

    def _write_production_mask(
        self, country: str, crop: str, season: int, df: pd.DataFrame,
        *, year=None,
    ) -> None:
        """Write the per-cell included/excluded answer to a stable
        parquet path that geoextract reads to build its production
        crop mask. Atomic via tmp + rename so geoextract never sees a
        partial file.

        When ``year`` is ``None`` the pooled mask is written to the
        canonical path (``production_mask_path``). When ``year`` is an
        int, the leave-one-out mask for that year is written to
        ``production_mask_path_for_year(year)`` instead.
        """
        from geocif import __version__ as _geocif_version

        df = df.copy()
        df["optimizer_version"] = f"geocif-{_geocif_version}"
        df["optimized_at"] = ar.now().format("YYYY-MM-DD")
        if year is None:
            out_path = self.production_mask_path(country, crop, season)
            label = "pooled"
        else:
            out_path = self.production_mask_path_for_year(
                country, crop, season, int(year),
            )
            label = f"leave-one-out y={int(year)}"
            df["leave_one_out_year"] = int(year)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = out_path.with_suffix(".parquet.tmp")
        df.to_parquet(tmp_path, index=False)
        tmp_path.replace(out_path)   # atomic on POSIX; near-atomic on NTFS
        n_inc = int(df["included"].sum())
        n_tot = len(df)
        self.logger.info(
            f"  wrote {label} production mask -> {out_path} "
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

    Always returns a 2-tuple ``(region, payload)`` so the parent's
    tqdm postfix can show *which* region just completed, even when the
    payload is ``None`` (region skipped — e.g. insufficient yield
    years — or the worker raised). Without this wrapper, the
    generator-unordered iteration on the parent side has no way to
    label a None result with its region.
    """
    try:
        opt = CellOptimizer(config_files)
        return region, opt.process_region(country, crop, season, region)
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
        return region, None


def run(path_config_files):
    """Entry point analogous to ``threshold_optimizer.run``. Prints a
    Rich-formatted startup banner summarising countries/crops/seasons,
    the GA hyperparameters, and where outputs land, then dispatches
    to ``CellOptimizer.main``.
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    opt = CellOptimizer(path_config_files)

    from geocif import __version__ as _geocif_version

    # Crops + seasons: per-country lists from the config, deduped.
    all_crops, all_seasons = set(), set()
    for country in opt.countries:
        if opt.parser.has_option(country, "crops"):
            try:
                all_crops.update(
                    ast.literal_eval(opt.parser.get(country, "crops"))
                )
            except (ValueError, SyntaxError):
                pass
        if opt.parser.has_option(country, "seasons"):
            try:
                all_seasons.update(
                    int(s) for s in ast.literal_eval(
                        opt.parser.get(country, "seasons")
                    )
                )
            except (ValueError, SyntaxError):
                pass
    if not all_seasons:
        all_seasons = {1}
    crops_str = ", ".join(sorted(all_crops)) if all_crops else "(none configured)"
    seasons_str = ", ".join(str(s) for s in sorted(all_seasons))

    # DOY agg display — show ndvi prominently (the typical primary
    # variable) with the others on the same line.
    doy_agg_str = ", ".join(
        f"{v}={opt.doy_agg.get(v, '?')}" for v in ("ndvi", "tmax", "tmin", "precip")
    )

    cells_input_root = opt.dir_output / "cell_optimizer"
    diag_output_root = (
        opt.dir_output / "ml" / "analysis" / opt.today_tag / "cell_optimizer"
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
        r"from geocif import cell_optimizer; cell_optimizer.run(cfg)",
    )
    table.add_row("Countries", _esc(", ".join(opt.countries) or "(none)"))
    table.add_row("Crops", _esc(crops_str))
    table.add_row("Seasons", seasons_str)
    table.add_row("annual_mask", str(opt.annual_mask))
    table.add_row("DOY agg", doy_agg_str)
    table.add_row(
        "GA",
        f"pop={opt.ga.population_size}, gens={opt.ga.n_generations}, "
        f"λ={opt.ga.l0_lambda:g}, min_cells_floor="
        f"max({opt.ga.min_cell_floor_abs}, "
        f"{opt.ga.min_cell_floor_frac:.0%} of cells), "
        f"early_stop={opt.ga.early_stop_patience}",
    )
    if opt.ga.optimize_threshold:
        seed_hint = (
            f", seed={opt.ga.threshold_init_pct:g}%"
            if opt.ga.threshold_init_pct is not None else ""
        )
        t_row = (
            f"on, T ∈ [{opt.ga.threshold_min_pct:g}, "
            f"{opt.ga.threshold_max_pct:g}] %  "
            f"σ={opt.ga.threshold_mutation_sigma:g}{seed_hint}"
        )
    else:
        t_row = "off (legacy mask-only path)"
    table.add_row("T optimization", t_row)
    table.add_row("n_jobs", str(opt.n_jobs))
    table.add_row("plot", str(opt.do_plot))
    table.add_row("write_production_mask", str(opt.write_production_mask))
    table.add_row("Cells input root", _esc(cells_input_root))
    table.add_row("Diagnostic output", _esc(diag_output_root))
    console.print(Panel(
        table,
        title="[bold bright_white]GeoCIF Cell Optimizer[/]",
        border_style="bright_blue",
        padding=(1, 2),
    ))

    opt.main()
