"""Tests for the region-selection GA (geocif/ml/region_ga.py).

The GA searches for which forecast-year regions to promote into training. Its
load-bearing invariant is CARDINALITY: every candidate must promote exactly
``p = round(fraction * n)`` regions. Without that the search cheats — a
candidate promoting more regions wins on volume rather than on choice, and the
"value of choosing well" number becomes meaningless.

Fitness here is a cheap synthetic function; in production one evaluation is a
full model refit.
"""

import numpy as np
import pytest

from geocif.ml.region_ga import (
    RegionGAConfig,
    _repair_to_p,
    run_region_ga,
)

REGIONS = [f"region_{i:02d}" for i in range(40)]


def _planted(good, noise=0.0, seed=0):
    """Fitness = overlap with a planted 'informative' set, optionally noisy."""
    rng = np.random.default_rng(seed)
    good = set(good)

    def evaluate(candidates):
        return [len(good & set(c)) + (rng.normal(0, noise) if noise else 0.0)
                for c in candidates]
    return evaluate


# ------------------------------------------------------------- cardinality

@pytest.mark.parametrize("start,p", [(0, 5), (40, 5), (3, 5), (9, 5), (5, 5)])
def test_repair_hits_p_exactly(start, p):
    rng = np.random.default_rng(0)
    mask = np.zeros(40, dtype=bool)
    if start:
        mask[:start] = True
    _repair_to_p(mask, p, rng)
    assert int(mask.sum()) == p


def test_every_evaluated_candidate_has_exact_cardinality():
    """The invariant, checked on EVERY candidate the GA ever evaluates."""
    seen = []

    def evaluate(candidates):
        seen.extend(candidates)
        return [float(len(c)) for c in candidates]

    run_region_ga(REGIONS, 0.10, evaluate,
                  RegionGAConfig(population_size=8, n_generations=4, seed=1))
    assert seen, "GA evaluated nothing"
    sizes = {len(c) for c in seen}
    assert sizes == {4}, f"expected every candidate to promote exactly 4, got {sizes}"
    # and never a duplicate region within a candidate
    assert all(len(set(c)) == len(c) for c in seen)


def test_candidates_are_drawn_only_from_supplied_regions():
    seen = []

    def evaluate(candidates):
        seen.extend(candidates)
        return [0.0] * len(candidates)

    run_region_ga(REGIONS, 0.1, evaluate,
                  RegionGAConfig(population_size=6, n_generations=3, seed=2))
    assert set().union(*map(set, seen)) <= set(REGIONS)


# ------------------------------------------------------------------ search

def test_ga_finds_the_planted_informative_regions():
    good = REGIONS[:4]
    res = run_region_ga(REGIONS, 0.10, _planted(good),
                        RegionGAConfig(population_size=30, n_generations=25, seed=3))
    assert len(res.best_regions) == 4
    # should recover most of the planted set; exact recovery isn't guaranteed
    # by a stochastic search, but 4/4 on a clean signal is the usual outcome
    assert len(set(good) & set(res.best_regions)) >= 3
    assert res.best_fitness >= 3


def test_ga_beats_a_random_subset_on_a_learnable_signal():
    """The GA only earns its cost if it beats blind selection."""
    good = set(REGIONS[:4])
    res = run_region_ga(REGIONS, 0.10, _planted(good),
                        RegionGAConfig(population_size=30, n_generations=25, seed=4))
    rng = np.random.default_rng(0)
    random_fit = np.mean([
        len(good & set(rng.choice(REGIONS, size=4, replace=False)))
        for _ in range(500)
    ])
    assert res.best_fitness > random_fit


def test_is_deterministic_for_a_given_seed():
    a = run_region_ga(REGIONS, 0.1, _planted(REGIONS[:4]),
                      RegionGAConfig(population_size=10, n_generations=5, seed=11))
    b = run_region_ga(REGIONS, 0.1, _planted(REGIONS[:4]),
                      RegionGAConfig(population_size=10, n_generations=5, seed=11))
    assert a.best_regions == b.best_regions and a.best_fitness == b.best_fitness


def test_best_fitness_never_decreases():
    res = run_region_ga(REGIONS, 0.1, _planted(REGIONS[:4], noise=0.3),
                        RegionGAConfig(population_size=12, n_generations=10, seed=5))
    bests = [h[0] for h in res.history]
    assert bests == sorted(bests), "elitism must make the incumbent monotone"


# ------------------------------------------------------------- robustness

def test_failed_evaluations_lose_rather_than_crash():
    """A candidate whose refit blew up returns None/NaN — it must not kill the run."""
    def evaluate(candidates):
        out = []
        for i, c in enumerate(candidates):
            if i % 3 == 0:
                out.append(None)
            elif i % 3 == 1:
                out.append(float("nan"))
            else:
                out.append(float(len(set(REGIONS[:4]) & set(c))))
        return out

    res = run_region_ga(REGIONS, 0.1, evaluate,
                        RegionGAConfig(population_size=9, n_generations=3, seed=6))
    assert np.isfinite(res.best_fitness)


def test_early_stop_saves_evaluations():
    flat = lambda cands: [1.0] * len(cands)  # noqa: E731 — no signal at all
    res = run_region_ga(REGIONS, 0.1, flat,
                        RegionGAConfig(population_size=8, n_generations=50,
                                       early_stop_patience=3, seed=7))
    assert res.stopped_early
    assert res.n_evaluations < 8 * 51


def test_degenerate_inputs_return_empty():
    assert run_region_ga([], 0.05, lambda c: []).best_regions == []
    assert run_region_ga(REGIONS, 0.0, lambda c: []).best_regions == []
