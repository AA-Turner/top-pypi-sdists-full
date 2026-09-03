"""Genetic algorithm over WHICH forecast-year regions to promote into training.

Companion to :mod:`geocif.ml.region_selection`, which does the promotion. This
module answers the second half of the question: *does it matter which regions
report early?* It searches the space of fixed-size region subsets for the one
that most improves skill on the regions still held out.

**These are UPPER-BOUND numbers.** The GA optimises the very year being
forecast, so it uses information an operational forecast would not have. The
result bounds what early-reporting data could be worth; it is not achievable
skill. Always report it beside the ``random`` arm — ``random - none`` is the
value of having early data at all, ``ga - random`` is the value of choosing
well, and the GA figure alone tells you neither.

Design notes
------------
* **Cardinality is pinned**, not penalised. A candidate always promotes exactly
  ``p = round(fraction * n_regions)`` regions, so every fitness evaluation is
  directly comparable and the search cannot cheat by promoting more.
  ``_repair_to_p`` restores the count after crossover and mutation — the same
  p-median trick ``cell_optimizer`` uses for cropmask cells.
* **Fitness is expensive**: one evaluation is a full model refit (measured ~67 s
  for tabpfn on kenya's 257 regions). The GA loop itself is therefore sequential
  by necessity — tournament selection needs the whole generation's fitnesses —
  but a generation's candidates are independent, so the caller evaluates them
  concurrently. Budget accordingly: pop x gens evaluations per forecast year.
* Deterministic given ``seed``, so a run can be reproduced or resumed.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence

import numpy as np


@dataclass(frozen=True)
class RegionGAConfig:
    """GA hyper-parameters. Defaults are sized for the real cost of a fitness
    evaluation (a model refit), NOT for cell_optimizer's cheap OLS fitness —
    its pop=100 x gens=200 would be 20,000 refits per forecast year.
    """
    population_size: int = 20
    n_generations: int = 15
    tournament_k: int = 3
    crossover_p: float = 0.5
    mutation_rate: Optional[float] = None   # None -> 2/n_regions
    elitism: int = 2
    early_stop_patience: int = 5
    seed: int = 0


@dataclass
class RegionGAResult:
    best_regions: list
    best_fitness: float
    history: list = field(default_factory=list)   # per-gen (best, mean)
    n_evaluations: int = 0
    stopped_early: bool = False
    n_regions: int = 0
    p: int = 0


def _repair_to_p(mask: np.ndarray, p: int, rng: np.random.Generator) -> None:
    """In-place: force ``mask.sum() == p`` by flipping random bits.

    Ported from ``cell_optimizer._repair_slice_to_p``. Uniform crossover and
    bit-flip mutation both break the cardinality constraint, so every child is
    repaired before evaluation — otherwise candidates promoting more regions
    would win on volume rather than on choice.
    """
    cur = int(mask.sum())
    if cur == p:
        return
    if cur > p:
        on = np.flatnonzero(mask)
        mask[rng.choice(on, size=cur - p, replace=False)] = False
    else:
        off = np.flatnonzero(~mask)
        if off.size == 0:
            return
        mask[rng.choice(off, size=min(p - cur, off.size), replace=False)] = True


def _init_population(pop_size: int, n: int, p: int,
                     rng: np.random.Generator) -> np.ndarray:
    pop = np.zeros((pop_size, n), dtype=bool)
    for i in range(pop_size):
        pop[i, rng.choice(n, size=p, replace=False)] = True
    return pop


def _tournament_idx(n_pop: int, fits: np.ndarray, k: int,
                    rng: np.random.Generator) -> int:
    cand = rng.integers(0, n_pop, size=k)
    return int(cand[np.argmax(fits[cand])])


def _uniform_crossover(a: np.ndarray, b: np.ndarray, p: float,
                       rng: np.random.Generator) -> np.ndarray:
    take_b = rng.random(a.shape) < p
    child = a.copy()
    child[take_b] = b[take_b]
    return child


def _mutate(g: np.ndarray, p: float, rng: np.random.Generator) -> np.ndarray:
    return np.logical_xor(g, rng.random(g.shape) < p)


def run_region_ga(
    regions: Sequence[str],
    fraction: float,
    evaluate: Callable[[Sequence[list]], Sequence[float]],
    cfg: Optional[RegionGAConfig] = None,
    logger: Optional[logging.Logger] = None,
) -> RegionGAResult:
    """Search for the region subset maximising ``evaluate``.

    Args:
        regions: candidate region names (must all have a known forecast-year
            yield — see ``region_selection.apply_region_promotion``).
        fraction: share of regions to promote (0.05 = 5%).
        evaluate: takes a LIST of candidate region-name lists and returns one
            fitness per candidate, higher-is-better. Batched so the caller can
            evaluate a generation concurrently — each evaluation is a model
            refit, so serial evaluation is impractical.
        cfg: GA hyper-parameters.

    Returns a :class:`RegionGAResult`. Fitness is whatever ``evaluate``
    returns; NaN/None fitnesses are treated as ``-inf`` so a candidate whose
    refit failed simply loses rather than crashing the search.
    """
    from .region_selection import n_to_promote

    cfg = cfg or RegionGAConfig()
    names = [str(r) for r in regions]
    n = len(names)
    p = n_to_promote(n, fraction)
    if n == 0 or p == 0:
        return RegionGAResult([], float("-inf"), n_regions=n, p=p)

    rng = np.random.default_rng(int(cfg.seed))
    mut = cfg.mutation_rate if cfg.mutation_rate is not None else 2.0 / max(n, 1)

    def _decode(mask: np.ndarray) -> list:
        return sorted(names[i] for i in np.flatnonzero(mask))

    def _fits(pop: np.ndarray) -> np.ndarray:
        raw = evaluate([_decode(m) for m in pop])
        out = np.full(len(pop), -np.inf, dtype=float)
        for i, v in enumerate(raw):
            if v is None:
                continue
            v = float(v)
            if np.isfinite(v):
                out[i] = v
        return out

    pop = _init_population(cfg.population_size, n, p, rng)
    fits = _fits(pop)
    n_evals = len(pop)
    best_i = int(np.argmax(fits))
    best_mask, best_fit = pop[best_i].copy(), float(fits[best_i])
    history = [(best_fit, float(np.mean(fits[np.isfinite(fits)]))
                if np.isfinite(fits).any() else float("nan"))]
    since_improve = 0
    stopped_early = False

    if logger is not None:
        logger.info(
            f"  region_ga: n_regions={n} p={p} ({fraction:.1%}) "
            f"pop={cfg.population_size} gens={cfg.n_generations} "
            f"-> up to {cfg.population_size * (cfg.n_generations + 1)} refits; "
            f"gen0 best={best_fit:+.4f}"
        )

    for gen in range(1, cfg.n_generations + 1):
        order = np.argsort(-fits)                       # elites first
        new = [pop[i].copy() for i in order[: max(0, cfg.elitism)]]
        while len(new) < cfg.population_size:
            a = pop[_tournament_idx(len(pop), fits, cfg.tournament_k, rng)]
            b = pop[_tournament_idx(len(pop), fits, cfg.tournament_k, rng)]
            child = _uniform_crossover(a, b, cfg.crossover_p, rng)
            child = _mutate(child, mut, rng)
            _repair_to_p(child, p, rng)                 # cardinality invariant
            new.append(child)
        pop = np.array(new, dtype=bool)
        fits = _fits(pop)
        n_evals += len(pop)

        gen_i = int(np.argmax(fits))
        if float(fits[gen_i]) > best_fit:
            best_fit = float(fits[gen_i])
            best_mask = pop[gen_i].copy()
            since_improve = 0
        else:
            since_improve += 1
        history.append((best_fit, float(np.mean(fits[np.isfinite(fits)]))
                        if np.isfinite(fits).any() else float("nan")))
        if logger is not None:
            logger.info(f"  region_ga: gen {gen}/{cfg.n_generations} "
                        f"best={best_fit:+.4f} (no-improve {since_improve})")
        if cfg.early_stop_patience and since_improve >= cfg.early_stop_patience:
            stopped_early = True
            if logger is not None:
                logger.info(f"  region_ga: early stop at gen {gen} "
                            f"({since_improve} generations without improvement)")
            break

    return RegionGAResult(
        best_regions=_decode(best_mask),
        best_fitness=best_fit,
        history=history,
        n_evaluations=n_evals,
        stopped_early=stopped_early,
        n_regions=n,
        p=p,
    )
