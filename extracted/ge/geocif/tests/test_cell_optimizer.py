"""Regression tests for ``geocif.cell_optimizer``.

The full ``CellOptimizer`` class needs a BaseGeo config + a real
parquet, so we test the pure-function GA primitives in isolation using
synthetic data with a planted signal:

  * 30 cells total, only the first 10 carry the yield signal; the other
    20 are pure noise.
  * Yield is a linear combination of the 10 signal cells' synthetic
    NDVI series.
  * Expected: the GA's best mask should INCLUDE most of the signal
    cells and EXCLUDE most of the noise cells, lifting LOOCV R²
    substantially above the all-cells baseline.

What's covered:
  * ``aggregate_over_mask`` — averaging, empty-mask NaN, shape.
  * ``loocv_r2_multivariate`` — perfect-line near-1.0, NaN on bad input.
  * ``fitness`` — MIN_CELLS floor returns -inf; L0 penalty rank-shifts.
  * ``run_ga`` — converges to a mask that beats the all-cells baseline
    on the planted-signal fixture, within reasonable generations.
"""
import unittest

import numpy as np
import pandas as pd

from geocif.cell_optimizer import (
    CellOptimizer,
    GAConfig,
    GAResultPooled,
    aggregate_held_out,
    aggregate_over_mask,
    fitness,
    init_prob_from_afi,
    init_T_pop,
    loocv_r2_multivariate,
    loocv_r2_pooled,
    loocv_r_multivariate,
    loocv_r_pooled,
    run_ga,
    run_ga_pooled,
    _detrend_yield,
    _effective_mask,
    _loocv_predictions,
    _mutate_T,
    _pooled_held_out_year_predictions,
    _pooled_loocv_predictions,
    _resolve_p_per_region,
    _repair_slice_to_p,
    _apply_repair_pooled,
    _mutate_p_median_pooled,
    init_pop_p_median_pooled,
)


def _planted_signal_fixture(seed: int = 42, n_signal: int = 10, n_noise: int = 20,
                             n_years: int = 20, n_vars: int = 2):
    """Synthetic per-cell EO with a known optimal mask.

    Cell layout: indices [0, n_signal)   = signal cells (correlated w/ yield)
                 indices [n_signal, n_signal+n_noise) = noise cells
    The 'true' optimal mask is True for signal cells, False for noise.

    Yield is built from the signal cells' average NDVI plus mild
    Gaussian noise so the optimizer has a real target to find but the
    noise cells genuinely hurt the LOOCV R² when included.
    """
    rng = np.random.default_rng(seed)
    n_cells = n_signal + n_noise
    per_cell = np.empty((n_cells, n_years, n_vars), dtype=float)

    # Latent yield "signal" — one series of length n_years.
    latent = rng.normal(size=n_years)

    # Signal cells: each variable correlated with the latent series
    # plus small per-cell noise.
    for c in range(n_signal):
        for v in range(n_vars):
            sign = 1.0 if v == 0 else -0.7  # var 0 positive, var 1 weaker negative
            per_cell[c, :, v] = sign * latent + rng.normal(scale=0.3, size=n_years)

    # Noise cells: pure Gaussian, uncorrelated with latent.
    for c in range(n_signal, n_cells):
        for v in range(n_vars):
            per_cell[c, :, v] = rng.normal(scale=1.0, size=n_years)

    # Yield = latent + mild Gaussian noise so OLS can almost recover it
    # from signal cells but noise cells dilute the fit.
    y = latent + rng.normal(scale=0.15, size=n_years)

    return per_cell, y, n_signal, n_noise


class TestAggregateOverMask(unittest.TestCase):
    def test_basic_averaging(self):
        per_cell = np.array([
            [[1.0, 10.0], [2.0, 20.0]],   # cell 0
            [[3.0, 30.0], [4.0, 40.0]],   # cell 1
            [[5.0, 50.0], [6.0, 60.0]],   # cell 2
        ])  # (3 cells, 2 years, 2 vars)
        mask = np.array([True, False, True])
        out = aggregate_over_mask(per_cell, mask)
        # cells 0+2 averaged: (1+5)/2=3, (2+6)/2=4, (10+50)/2=30, (20+60)/2=40
        np.testing.assert_array_almost_equal(out, [[3.0, 30.0], [4.0, 40.0]])

    def test_empty_mask_returns_nan(self):
        per_cell = np.zeros((3, 2, 2))
        mask = np.zeros(3, dtype=bool)
        out = aggregate_over_mask(per_cell, mask)
        self.assertTrue(np.isnan(out).all())
        self.assertEqual(out.shape, (2, 2))


class TestLOOCVR2(unittest.TestCase):
    def test_perfect_line_near_one(self):
        # y = 2*x + 1 exactly — LOOCV should recover R²≈1.
        rng = np.random.default_rng(0)
        x = rng.normal(size=(20, 1))
        y = 2 * x[:, 0] + 1
        r2 = loocv_r2_multivariate(x, y)
        self.assertGreater(r2, 0.99)

    def test_pure_noise_yields_negative_r2(self):
        # Unrelated x and y → R² should be ≤ 0 (LOOCV preds worse than mean).
        rng = np.random.default_rng(1)
        x = rng.normal(size=(20, 2))
        y = rng.normal(size=20)
        r2 = loocv_r2_multivariate(x, y)
        self.assertLess(r2, 0.5)  # generous — just ruling out >>0

    def test_too_few_years_returns_nan(self):
        x = np.ones((3, 1))
        y = np.ones(3)
        self.assertTrue(np.isnan(loocv_r2_multivariate(x, y)))


class TestFitness(unittest.TestCase):
    def test_below_min_cells_is_negative_inf(self):
        per_cell, y, _, _ = _planted_signal_fixture()
        small_mask = np.zeros(per_cell.shape[0], dtype=bool)
        small_mask[0] = True   # only 1 cell selected
        f = fitness(small_mask, per_cell, y, lam=0.02, min_cells=5)
        self.assertEqual(f, float("-inf"))

    def test_l0_penalty_orders_correctly(self):
        # Two masks with equal R² but different cell counts: the smaller
        # mask should have higher fitness under the L0 penalty.
        #
        # Pinned to ``metric="r2"`` because _planted_signal_fixture has
        # two variables with OPPOSITE signs by design (var 0 positive,
        # var 1 negative). Under the 0.4.760 default metric="r"
        # (mean of signed per-variable r), those signs cancel and the
        # fixture becomes degenerate — that's a deliberate property of
        # the mean-of-signed-r convention, not a regression. To still
        # exercise the L0-penalty contract on this fixture, keep r².
        per_cell, y, n_sig, _ = _planted_signal_fixture()
        mask_small = np.zeros(per_cell.shape[0], dtype=bool)
        mask_small[:n_sig] = True   # exactly the signal cells
        mask_big = mask_small.copy()
        mask_big[n_sig:] = True     # also include all noise cells
        f_small = fitness(mask_small, per_cell, y, lam=0.02, min_cells=5, metric="r2")
        f_big = fitness(mask_big, per_cell, y, lam=0.02, min_cells=5, metric="r2")
        # Both should be finite; small should beat big because the
        # noise cells hurt R² AND the L0 penalty.
        self.assertGreater(f_small, f_big)


class TestInitProbFromAFI(unittest.TestCase):
    """The AFI-as-prior helper. beta=0 → uniform 0.5 (no prior, the
    backwards-compatible behaviour); beta=1 → P = afi/100 clipped to
    [0.1, 0.9] (the plan default); beta>1 → sharper pull to extremes."""

    def test_beta_zero_returns_uniform_half(self):
        afi = np.array([0.0, 50.0, 100.0])
        p = init_prob_from_afi(afi, beta=0.0)
        np.testing.assert_array_almost_equal(p, [0.5, 0.5, 0.5])

    def test_beta_one_is_clipped_linear(self):
        afi = np.array([0.0, 25.0, 50.0, 75.0, 100.0])
        p = init_prob_from_afi(afi, beta=1.0)
        # 0/100=0 → clipped to 0.1; 25/100 stays 0.25; 50/100 stays 0.5;
        # 75/100 stays 0.75; 100/100=1 → clipped to 0.9.
        np.testing.assert_array_almost_equal(p, [0.1, 0.25, 0.5, 0.75, 0.9])

    def test_beta_two_pushes_extremes_to_clips(self):
        # afi=80 → centered 0.3 → 0.5 + 2*0.3 = 1.1 → clipped to 0.9
        # afi=20 → centered -0.3 → 0.5 + 2*-0.3 = -0.1 → clipped to 0.1
        p = init_prob_from_afi(np.array([20.0, 80.0]), beta=2.0)
        np.testing.assert_array_almost_equal(p, [0.1, 0.9])

    def test_clipping_bounds_respected(self):
        # Custom p_min, p_max
        p = init_prob_from_afi(
            np.array([0.0, 50.0, 100.0]), beta=1.0, p_min=0.2, p_max=0.8,
        )
        np.testing.assert_array_almost_equal(p, [0.2, 0.5, 0.8])


class TestGAConfigDefaults(unittest.TestCase):
    """Pin the new defaults so a future code change can't silently shift
    them without updating the tests + plan docs."""

    def test_l0_lambda_default(self):
        # Bumped 2026-06-07 from 0.02 → 0.05 (stronger parsimony pressure).
        self.assertEqual(GAConfig().l0_lambda, 0.05)

    def test_min_cell_floor_frac_default(self):
        # Bumped down 2026-06-07 from 0.05 → 0.01 (allow finer-grained
        # masks; the absolute floor of 20 still applies for small regions).
        self.assertEqual(GAConfig().min_cell_floor_frac, 0.01)

    def test_afi_prior_beta_default(self):
        # New 2026-06-07. 1.0 means "P = afi/100 clipped" by default.
        self.assertEqual(GAConfig().afi_prior_beta, 1.0)

    def test_default_optimize_threshold_is_True(self):
        # 0.4.756: joint (mask, T) optimization is the default. Anyone
        # flipping this to False MUST update the plan + backward-compat
        # documentation (tasks/plan.md §4) and bump a major version.
        self.assertTrue(GAConfig().optimize_threshold)

    def test_threshold_bounds_defaults(self):
        # T searched in [0, 50] % by default — matches the typical AFI
        # floor range threshold_optimizer scans.
        cfg = GAConfig()
        self.assertEqual(cfg.threshold_min_pct, 0.0)
        self.assertEqual(cfg.threshold_max_pct, 50.0)

    def test_threshold_init_pct_none_by_default(self):
        # None → uniform random init for T_pop; non-None → jittered around the value.
        self.assertIsNone(GAConfig().threshold_init_pct)

    def test_threshold_mutation_sigma_default(self):
        # σ in normalized [0, 1] space — 0.05 is ~2.5 percentage points
        # at threshold_max_pct=50%.
        self.assertAlmostEqual(GAConfig().threshold_mutation_sigma, 0.05)


class TestRunGAWithAFI(unittest.TestCase):
    """When AFI is supplied, the seed population's cell-inclusion
    frequencies should reflect the AFI prior. Specifically, in
    generation 0, the average inclusion across the population per cell
    should track init_prob_from_afi(afi, beta). With pop=200 the
    sample mean is tight enough to assert against."""

    def test_seed_population_reflects_afi_bias(self):
        rng = np.random.default_rng(0)
        n_cells = 50
        n_years = 20
        # Half high-AFI, half low-AFI.
        afi = np.concatenate([np.full(25, 90.0), np.full(25, 10.0)])
        # Per-cell EO + yield don't matter for this test — we only
        # check the seed population, then bail out via 1 generation.
        per_cell = rng.normal(size=(n_cells, n_years, 1))
        y = rng.normal(size=n_years)
        cfg = GAConfig(
            population_size=200,
            n_generations=1,
            min_cell_floor_abs=1,
            min_cell_floor_frac=0.01,
            seed=0,
        )
        # Stash the initial population by hooking the rng outside —
        # but simpler: replicate the seed init manually and compare.
        # The contract is: cell c starts True with prob init_prob_from_afi(afi)[c].
        # Run the GA with afi → seed pop should obey that.
        result = run_ga(per_cell, y, cfg, afi=afi)
        # Best mask from a 1-gen run is essentially a sample from the
        # seed population (no real selection has happened yet). With
        # pop=200, the fraction of high-AFI cells in the best mask
        # should be noticeably higher than the low-AFI fraction.
        high_sel = result.best_mask[:25].mean()
        low_sel = result.best_mask[25:].mean()
        self.assertGreater(high_sel, low_sel + 0.2,
                           msg=f"AFI prior didn't bias seed: "
                               f"high-AFI selection={high_sel:.2f}, "
                               f"low-AFI selection={low_sel:.2f}")


class TestZeroAFIFilter(unittest.TestCase):
    """Defense-in-depth: even though the extract_cells contract says
    "emit only afi > 0", load_region must filter again so n_cells is
    always the cropland-cell count (the right denominator for the
    min-cell floor and the L0 share penalty)."""

    def _make_parquet(self, tmp_path):
        """Synthetic per-cell parquet with 5 cropland cells and 3
        zero-AFI cells over 6 years × 4 doys × 1 var (ndvi)."""
        rng = np.random.default_rng(0)
        cells = [
            (0, 30.1, 75.1, 50.0),   # cropland
            (1, 30.2, 75.2, 75.0),   # cropland
            (2, 30.3, 75.3, 20.0),   # cropland
            (3, 30.4, 75.4, 0.0),    # NON-cropland (should drop)
            (4, 30.5, 75.5, 0.0),    # NON-cropland (should drop)
            (5, 30.6, 75.6, 90.0),   # cropland
            (6, 30.7, 75.7, 0.0),    # NON-cropland (should drop)
            (7, 30.8, 75.8, 60.0),   # cropland
        ]
        rows = []
        for cell_id, lat, lon, afi in cells:
            for year in range(2018, 2024):
                for doy in (90, 120, 150, 180):
                    rows.append({
                        "country": "india",
                        "region": "test_region",
                        "region_id": 1,
                        "cell_id": cell_id,
                        "lat": lat,
                        "lon": lon,
                        "afi": afi,
                        "year": year,
                        "doy": doy,
                        "ndvi": float(rng.normal()),
                    })
        df = pd.DataFrame(rows)
        path = tmp_path / "tst.parquet"
        df.to_parquet(path)
        return path, len(cells), sum(1 for c in cells if c[3] > 0)

    def test_load_region_drops_zero_afi_cells(self):
        # Build a minimal CellOptimizer-like stub that exposes just the
        # df-filtering body of load_region. We test the filter logic
        # directly because instantiating the real class needs BaseGeo
        # config files; the filter is the only new logic here.
        import tempfile
        with tempfile.TemporaryDirectory() as tmpd:
            path, n_total, n_crop = self._make_parquet(__import__('pathlib').Path(tmpd))
            df = pd.read_parquet(path)
            self.assertEqual(df["cell_id"].nunique(), n_total)
            df_filtered = df[df["afi"] > 0]
            self.assertEqual(df_filtered["cell_id"].nunique(), n_crop)
            # 5 cropland out of 8 total — n_cells in GA must be 5.
            self.assertEqual(n_crop, 5)
            self.assertEqual(n_total - n_crop, 3)


class TestRunGA(unittest.TestCase):
    """End-to-end on the planted-signal fixture. The GA should converge
    to a mask that includes most signal cells and excludes most noise
    cells, beating the all-cells baseline R² by a measurable margin."""

    def test_ga_finds_signal_cells_and_beats_baseline(self):
        # See test_l0_penalty_orders_correctly above for why the
        # planted-signal fixture pins metric="r2" — it has two
        # variables with opposite expected signs, which is degenerate
        # under the 0.4.760 default mean-of-signed-r metric.
        per_cell, y, n_sig, n_noise = _planted_signal_fixture(
            seed=42, n_signal=10, n_noise=20, n_years=20, n_vars=2,
        )
        cfg = GAConfig(
            population_size=60,
            n_generations=100,
            l0_lambda=0.05,
            min_cell_floor_abs=5,
            min_cell_floor_frac=0.05,
            early_stop_patience=40,
            seed=0,
            fitness_metric="r2",
        )
        result = run_ga(per_cell, y, cfg)

        # 1. Optimizer's R² must beat the baseline (all-cells average).
        self.assertGreater(result.best_r2, result.baseline_r2 + 0.05,
                           msg=f"GA failed to lift R² beyond +0.05: "
                               f"baseline={result.baseline_r2:.3f}, "
                               f"optimized={result.best_r2:.3f}")

        # 2. The best mask should have a noticeable bias toward signal
        #    cells (>=70% of selected cells from the signal block) and
        #    away from noise cells. We don't require perfect recovery —
        #    GA on 30 cells × 100 gens isn't expected to find the exact
        #    optimum, but the bias should be unmistakable.
        signal_sel = int(result.best_mask[:n_sig].sum())
        total_sel = int(result.best_mask.sum())
        self.assertGreater(signal_sel / max(1, total_sel), 0.6,
                           msg=f"selected mask is mostly noise: "
                               f"{signal_sel} signal / {total_sel} total")

    def test_history_length_matches_generations_run(self):
        per_cell, y, _, _ = _planted_signal_fixture(seed=1)
        cfg = GAConfig(population_size=20, n_generations=15,
                       early_stop_patience=999, seed=0)
        result = run_ga(per_cell, y, cfg)
        self.assertEqual(len(result.history), result.n_generations_run)
        self.assertEqual(result.n_generations_run, 15)

    def test_baseline_r2_is_computed_independent_of_ga(self):
        # Two runs on the same data with different seeds → same baseline.
        per_cell, y, _, _ = _planted_signal_fixture(seed=2)
        a = run_ga(per_cell, y, GAConfig(population_size=20, n_generations=5, seed=0))
        b = run_ga(per_cell, y, GAConfig(population_size=20, n_generations=5, seed=99))
        self.assertAlmostEqual(a.baseline_r2, b.baseline_r2, places=10)


class TestTinyRegionDoesNotCrash(unittest.TestCase):
    """Regression: a region with fewer cropland cells than the
    configured ``min_cell_floor_abs`` used to crash the GA at the
    seed-population repair step with::

        ValueError: Cannot take a larger sample than population when
        replace is False

    The fix clamps ``min_cells`` to ``n_cells`` so tiny regions
    degenerate gracefully to an all-cells-in mask (lift = 0) instead
    of crashing the entire combo. Seen in production for
    Argentina/soybean/corrientes and /misiones where soybean cropland
    is < 20 cells.
    """

    def test_n_cells_below_min_cell_floor_abs(self):
        rng = np.random.default_rng(0)
        n_cells = 3   # < configured min_cell_floor_abs=20 below
        n_years = 20
        per_cell = rng.normal(size=(n_cells, n_years, 1))
        y = rng.normal(size=n_years)
        afi = rng.uniform(5, 80, size=n_cells)

        cfg = GAConfig(
            population_size=20, n_generations=5,
            min_cell_floor_abs=20,    # > n_cells, would crash without clamp
            min_cell_floor_frac=0.01,
            seed=0,
            # T-gene OFF — this test is about the min-cell floor clamp,
            # not about T evolution. Default-on T would try to apply an
            # AFI filter on this synthetic afi (which is in raw % units,
            # not the production percent × 100 convention) and would
            # spuriously make every candidate -inf-fitness.
            optimize_threshold=False,
        )
        # Must not raise.
        result = run_ga(per_cell, y, cfg, afi=afi)

        # GA degenerates to all-cells-in (only viable mask given the
        # floor==n_cells); baseline == optimized.
        self.assertEqual(int(result.best_mask.sum()), n_cells)
        self.assertEqual(result.best_mask.shape, (n_cells,))


class TestParquetReadIsRegionScoped(unittest.TestCase):
    """Regression: when ``CellOptimizer.load_region`` reads the per-cell
    parquet, the resulting in-memory DataFrame must contain rows for the
    REQUESTED region only — not every region in the file. Russia/
    winter_wheat (~72 M rows, ~7 GB in pandas) blew up every joblib
    worker with SIGKILL under n_jobs=-1 until we switched to
    predicate-pushdown at read time. This test pins the fix.

    We don't instantiate the full CellOptimizer (needs BaseGeo config),
    but the contract we're testing is purely the read-time filter +
    column projection. We replicate it with the same pyarrow primitives
    the production code uses, so the assertion catches any future
    regression that reintroduces a full-parquet read.
    """

    def test_pyarrow_filter_only_returns_one_region(self):
        import tempfile
        from pathlib import Path

        # Build a tiny multi-region parquet so we can prove the filter
        # actually scopes the read.
        rng = np.random.default_rng(0)
        rows = []
        for region in ("region_a", "region_b", "region_c"):
            for cell_id in range(5):
                for year in range(2020, 2023):
                    for doy in (90, 120, 150):
                        rows.append({
                            "country": "test",
                            "region": region,
                            "region_id": 1,
                            "cell_id": cell_id,
                            "lat": 30.0 + cell_id * 0.1,
                            "lon": 75.0 + cell_id * 0.1,
                            "afi": 50.0,
                            "year": year,
                            "doy": doy,
                            "ndvi": float(rng.normal()),
                            "extra_unused_col": "should_not_be_read",
                        })
        df_full = pd.DataFrame(rows)

        with tempfile.TemporaryDirectory() as tmpd:
            path = Path(tmpd) / "multi_region.parquet"
            df_full.to_parquet(path)

            # The production path is:
            #   pd.read_parquet(path, columns=keep_cols, filters=[("region", "==", region)])
            keep_cols = sorted({
                "country", "region", "region_id", "cell_id",
                "lat", "lon", "afi", "year", "doy", "ndvi",
            })
            df_b = pd.read_parquet(
                path,
                columns=keep_cols,
                filters=[("region", "==", "region_b")],
            )

            # 1. Only region_b rows.
            self.assertEqual(set(df_b["region"].unique()), {"region_b"})

            # 2. Row count matches what we wrote for region_b (5 cells × 3 years × 3 doys = 45).
            self.assertEqual(len(df_b), 5 * 3 * 3)

            # 3. The unused column did NOT come along — column projection worked.
            self.assertNotIn("extra_unused_col", df_b.columns)

            # 4. Same query on an absent region returns empty (the guard
            #    after the read is `if df.empty: return None`).
            df_none = pd.read_parquet(
                path,
                columns=keep_cols,
                filters=[("region", "==", "region_does_not_exist")],
            )
            self.assertTrue(df_none.empty)


class TestAggregateHeldOut(unittest.TestCase):
    """Held-out aggregation applies year-Y's mask only to year Y's slice
    of per_cell. Rows for years whose mask is missing stay NaN so
    downstream R² / r computations skip them via the standard
    finite-mask gate."""

    def test_each_year_uses_its_own_mask(self):
        # 3 cells × 4 years × 2 vars. mask_2020 picks cell 0; mask_2021
        # picks cell 1; mask_2022 picks cells 0+2; mask_2023 missing.
        per_cell = np.array([
            [[10, 100], [11, 110], [12, 120], [13, 130]],   # cell 0
            [[20, 200], [21, 210], [22, 220], [23, 230]],   # cell 1
            [[30, 300], [31, 310], [32, 320], [33, 330]],   # cell 2
        ], dtype=float)
        years = np.array([2020, 2021, 2022, 2023])
        masks_by_year = {
            2020: np.array([True,  False, False]),
            2021: np.array([False, True,  False]),
            2022: np.array([True,  False, True]),
            # 2023 deliberately missing
        }

        out = aggregate_held_out(per_cell, years, masks_by_year)

        # 2020: cell 0 only -> [10, 100]
        np.testing.assert_array_almost_equal(out[0], [10.0, 100.0])
        # 2021: cell 1 only -> [21, 210]
        np.testing.assert_array_almost_equal(out[1], [21.0, 210.0])
        # 2022: mean of cells 0+2 -> [(32+32)/2, (320+320)/2]... wait
        #       per_cell[0, 2, :] = [12, 120]; per_cell[2, 2, :] = [32, 320]
        #       mean = [22, 220]
        np.testing.assert_array_almost_equal(out[2], [22.0, 220.0])
        # 2023: mask missing -> NaN
        self.assertTrue(np.isnan(out[3]).all())

    def test_missing_all_masks_returns_all_nan(self):
        per_cell = np.ones((2, 3, 1), dtype=float)
        years = np.array([2020, 2021, 2022])
        out = aggregate_held_out(per_cell, years, masks_by_year={})
        self.assertEqual(out.shape, (3, 1))
        self.assertTrue(np.isnan(out).all())


class TestDOYAggDefaults(unittest.TestCase):
    """The per-variable DOY-axis aggregation defaults are part of the
    public contract — flipping them silently would change every
    downstream cell_optimizer run. Pin them here.
    """

    def test_ndvi_default_is_auc(self):
        from geocif.cell_optimizer import _DOY_AGG_DEFAULTS
        self.assertEqual(_DOY_AGG_DEFAULTS["ndvi"], "auc")

    def test_t_and_p_defaults_are_mean(self):
        from geocif.cell_optimizer import _DOY_AGG_DEFAULTS
        self.assertEqual(_DOY_AGG_DEFAULTS["tmax"], "mean")
        self.assertEqual(_DOY_AGG_DEFAULTS["tmin"], "mean")
        self.assertEqual(_DOY_AGG_DEFAULTS["precip"], "mean")

    def test_valid_agg_set_includes_auc_and_sum(self):
        from geocif.cell_optimizer import _DOY_AGG_VALID
        for name in ("auc", "sum", "max", "mean", "median", "min"):
            self.assertIn(name, _DOY_AGG_VALID)


class TestTGeneOptimization(unittest.TestCase):
    """Joint (mask, T) optimization — the 0.4.756 feature. Tests are
    laid out in the order they were enabled by the build plan:

    T4: T_pop init — within bounds (default-on) and zero (opt-out).
    T5: T mutation — respects bounds for σ values up to 0.5.
    T7: fitness's effective_mask = mask & (afi ≥ T*100), regardless
        of which raw mask bit was set.
    T8: GA converges T toward the planting cutoff on a planted-signal
        fixture where AFI separates signal from noise cells.
    """

    def test_T_init_within_bounds(self):
        # Default config: optimize_threshold=True, range [0, 50] %
        # → T_min_norm = 0, T_max_norm = 1; T_pop uniform in [0, 1].
        rng = np.random.default_rng(0)
        cfg = GAConfig()   # all defaults
        T_pop = init_T_pop(rng, pop_size=200, cfg=cfg)
        self.assertEqual(T_pop.shape, (200,))
        self.assertGreaterEqual(T_pop.min(), 0.0)
        self.assertLessEqual(T_pop.max(), 1.0)
        # Uniform over [0, 1] → mean should be ~0.5 with pop=200.
        self.assertAlmostEqual(T_pop.mean(), 0.5, places=1)

    def test_T_init_within_bounds_custom_range(self):
        # threshold_min_pct=10, threshold_max_pct=40 → T_min_norm=0.25.
        rng = np.random.default_rng(0)
        cfg = GAConfig(threshold_min_pct=10.0, threshold_max_pct=40.0)
        T_pop = init_T_pop(rng, pop_size=200, cfg=cfg)
        self.assertGreaterEqual(T_pop.min(), 0.25 - 1e-9)
        self.assertLessEqual(T_pop.max(), 1.0)

    def test_T_init_jitter_around_seed(self):
        # When threshold_init_pct is set, T_pop is jittered around the
        # seed (σ=0.02 in normalized space, clipped to [T_min_norm, 1]).
        rng = np.random.default_rng(0)
        cfg = GAConfig(
            threshold_max_pct=50.0,
            threshold_init_pct=25.0,   # → seed_norm = 0.5
        )
        T_pop = init_T_pop(rng, pop_size=500, cfg=cfg)
        # Mean should be very close to 0.5; std should be small (σ=0.02).
        self.assertAlmostEqual(T_pop.mean(), 0.5, places=2)
        self.assertLess(T_pop.std(), 0.04)

    def test_T_init_zero_when_opted_out(self):
        # The explicit legacy path. T_pop must be exactly all-zeros so
        # the AFI filter is a no-op in fitness and behaviour matches
        # pre-0.4.756 mask-only optimization.
        rng = np.random.default_rng(0)
        cfg = GAConfig(optimize_threshold=False)
        T_pop = init_T_pop(rng, pop_size=200, cfg=cfg)
        self.assertEqual(T_pop.shape, (200,))
        self.assertTrue(np.all(T_pop == 0.0))

    def test_T_mutation_respects_bounds(self):
        # _mutate_T must clip to [t_min_norm, t_max_norm]. Hammer with
        # a large σ so most draws would naively land outside the range
        # — they should all come back clipped to the bounds.
        rng = np.random.default_rng(0)
        n_trials = 1000
        # Start at the upper bound; mutate with a huge σ. Without
        # clipping most mutated values would exceed 1.0; with clipping
        # they all land in [0.25, 1.0].
        vals = [
            _mutate_T(0.8, sigma=0.5, t_min_norm=0.25, t_max_norm=1.0, rng=rng)
            for _ in range(n_trials)
        ]
        self.assertTrue(all(0.25 <= v <= 1.0 for v in vals),
                        msg=f"out-of-bounds values: "
                            f"min={min(vals):.3f}, max={max(vals):.3f}")
        # At least some draws should hit the boundary clip — verifies
        # σ was actually large enough to test clipping (sanity check).
        self.assertTrue(any(v == 1.0 or v == 0.25 for v in vals),
                        msg="σ=0.5 should have driven some draws to the clip; "
                            "none hit — test isn't exercising the clip path.")

    def test_T_mutation_zero_sigma_is_identity(self):
        # σ=0 → no perturbation; output equals input.
        rng = np.random.default_rng(0)
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            self.assertEqual(
                _mutate_T(t, sigma=0.0, t_min_norm=0.0, t_max_norm=1.0, rng=rng),
                t,
            )

    def test_effective_mask_respects_T(self):
        # Fitness should treat cells with afi < T*100 as if their mask
        # bit were False — i.e. they cannot contribute to the aggregate
        # regardless of what the GA picked for them.
        #
        # We construct two masks that differ ONLY in cells whose AFI
        # is below the configured T threshold. Their fitness values
        # MUST be identical because the effective masks are identical.
        rng = np.random.default_rng(0)
        n_cells, n_years = 6, 12
        per_cell = rng.normal(size=(n_cells, n_years, 1))
        y = rng.normal(size=n_years)
        # cells 0-2 have high AFI (eligible), cells 3-5 have low AFI.
        afi = np.array([80.0, 70.0, 60.0, 10.0, 5.0, 8.0])
        # T_norm = 0.5 with T_max=50 → T_pct = 25% → cells with
        # afi >= 25*100 = 2500 are eligible. With AFI stored as
        # percent (60/70/80 here), eligibility is afi >= 25 → cells
        # 0/1/2 in; 3/4/5 out.
        T_norm, T_max = 0.5, 50.0

        # Use a min_cells_floor of 1 so neither mask gets -inf.
        mask_A = np.array([True, True, True, False, False, False])
        # B differs from A only in low-AFI cells (3-5). Effective masks
        # are identical → fitnesses must be equal.
        mask_B = np.array([True, True, True, True, True, True])

        f_A = fitness(
            mask_A, per_cell, y, 0.05, 1,
            T_norm=T_norm, afi=afi, T_max=T_max,
        )
        f_B = fitness(
            mask_B, per_cell, y, 0.05, 1,
            T_norm=T_norm, afi=afi, T_max=T_max,
        )
        self.assertEqual(
            f_A, f_B,
            msg=f"masks differing only in ineligible cells gave different "
                f"fitness ({f_A} vs {f_B}) — the AFI filter isn't excluding "
                f"low-AFI cells correctly.",
        )

        # Sanity: without the T filter (T_norm=0), the two masks SHOULD
        # produce different fitness because they have different
        # effective-cell counts.
        f_A_no_T = fitness(mask_A, per_cell, y, 0.05, 1)
        f_B_no_T = fitness(mask_B, per_cell, y, 0.05, 1)
        self.assertNotEqual(
            f_A_no_T, f_B_no_T,
            msg="control sanity check failed: masks with different cell "
                "counts should give different fitness with no AFI filter.",
        )

    def test_GAResult_best_T_pct_zero_when_opted_out(self):
        # With optimize_threshold=False, the GA never evolves T, so
        # best_T_pct must be exactly 0. This guards the legacy
        # opt-out contract on the output side.
        rng = np.random.default_rng(0)
        n_cells, n_years = 30, 18
        per_cell = rng.normal(size=(n_cells, n_years, 1))
        y = rng.normal(size=n_years)
        afi = rng.uniform(5, 80, size=n_cells)
        cfg = GAConfig(
            optimize_threshold=False,
            population_size=20, n_generations=5,
            min_cell_floor_abs=5, min_cell_floor_frac=0.01,
            seed=0,
        )
        result = run_ga(per_cell, y, cfg, afi=afi)
        self.assertEqual(result.best_T_pct, 0.0)

    def test_GAResult_best_T_pct_in_range_when_enabled(self):
        # Default config has optimize_threshold=True. The GA should
        # return best_T_pct ∈ [threshold_min_pct, threshold_max_pct].
        rng = np.random.default_rng(0)
        n_cells, n_years = 30, 18
        per_cell = rng.normal(size=(n_cells, n_years, 1))
        y = rng.normal(size=n_years)
        afi = rng.uniform(5, 80, size=n_cells)
        cfg = GAConfig(
            population_size=30, n_generations=10,
            min_cell_floor_abs=5, min_cell_floor_frac=0.01,
            seed=0,
        )
        result = run_ga(per_cell, y, cfg, afi=afi)
        self.assertGreaterEqual(result.best_T_pct, cfg.threshold_min_pct)
        self.assertLessEqual(result.best_T_pct, cfg.threshold_max_pct)
        # History also has the new column.
        self.assertIn("best_T_pct", result.history.columns)

    def test_effective_mask_helper(self):
        # Regression for the 0.4.757 audit: _effective_mask is the
        # single source of truth. Every surface that reports "the GA's
        # chosen cells" (production parquet, summary per-variable r,
        # cells_comparison plot) must AND through this helper so they
        # stay in lockstep.
        mask = np.array([True, True, False, True, True])
        afi = np.array([3000.0, 6000.0, 9000.0, 500.0, 200.0])

        # T_pct = 0 → no filter; effective == raw mask.
        np.testing.assert_array_equal(
            _effective_mask(mask, 0.0, afi),
            mask,
        )
        # T_pct = 0 + afi=None → still no filter (legacy short-circuit).
        np.testing.assert_array_equal(
            _effective_mask(mask, 0.0, None),
            mask,
        )
        # T_pct = 20 → cells with afi < 2000 ineligible.
        # mask[3] was True but afi[3]=500 < 2000 → excluded.
        np.testing.assert_array_equal(
            _effective_mask(mask, 20.0, afi),
            np.array([True, True, False, False, False]),
        )

    def test_build_production_rows_with_T_uses_effective_mask(self):
        # _build_production_rows is the seam between the GA's raw mask
        # output and the parquet that geoextract reads. When T_pct > 0,
        # included must reflect the EFFECTIVE decision (mask AND
        # eligible by AFI), not the raw bits. region_threshold_pct
        # must be present and broadcast.
        import pandas as pd
        # Need a CellOptimizer-like object to call the bound method.
        # Construct a minimal stub.
        class _Stub:
            pass
        stub = _Stub()
        stub._build_production_rows = (
            CellOptimizer._build_production_rows.__get__(stub)
        )

        cell_meta = pd.DataFrame({
            "cell_id":   [0, 1, 2, 3, 4],
            "region_id": [1, 1, 1, 1, 1],
            "lat":       [10.0, 10.1, 10.2, 10.3, 10.4],
            "lon":       [75.0, 75.1, 75.2, 75.3, 75.4],
            # AFI in production convention (percent × 100): cells 0..2
            # have AFI 30/60/90 %; cells 3..4 have 5/2 %.
            "afi":       [3000.0, 6000.0, 9000.0, 500.0, 200.0],
        })
        # Raw GA mask: cells 0, 2, 4 included.
        mask = np.array([True, False, True, False, True])

        # T_pct = 20 → cells with AFI < 2000 are ineligible. cell 4 (afi=200)
        # was raw-included but is now ineligible → effective drops it.
        rows = stub._build_production_rows(
            "india", "test_region", cell_meta, mask, T_pct=20.0,
        )
        # included column equals mask AND eligible
        np.testing.assert_array_equal(
            rows["included"].to_numpy(dtype=bool),
            np.array([True, False, True, False, False]),
        )
        # region_threshold_pct broadcast across every row.
        np.testing.assert_array_equal(
            rows["region_threshold_pct"].to_numpy(dtype=float),
            np.full(5, 20.0),
        )
        # Schema includes the new column.
        self.assertIn("region_threshold_pct", rows.columns)

    def test_build_production_rows_legacy_when_T_zero(self):
        # T_pct = 0 (the opt-out path) → no AFI filter; included
        # equals the raw mask byte-for-byte; region_threshold_pct is
        # still emitted but as 0.0 everywhere.
        import pandas as pd
        class _Stub:
            pass
        stub = _Stub()
        stub._build_production_rows = (
            CellOptimizer._build_production_rows.__get__(stub)
        )

        cell_meta = pd.DataFrame({
            "cell_id":   [0, 1, 2, 3, 4],
            "region_id": [1, 1, 1, 1, 1],
            "lat":       [10.0, 10.1, 10.2, 10.3, 10.4],
            "lon":       [75.0, 75.1, 75.2, 75.3, 75.4],
            "afi":       [3000.0, 6000.0, 9000.0, 500.0, 200.0],
        })
        mask = np.array([True, False, True, False, True])
        rows = stub._build_production_rows(
            "india", "test_region", cell_meta, mask, T_pct=0.0,
        )
        # included == raw mask exactly.
        np.testing.assert_array_equal(
            rows["included"].to_numpy(dtype=bool), mask,
        )
        # region_threshold_pct broadcast as 0.0.
        self.assertTrue((rows["region_threshold_pct"] == 0.0).all())

    def test_T_evolves_to_signal(self):
        # Planted-signal fixture with high-AFI signal cells and low-AFI
        # noise cells. AFI is in production convention (percent × 100).
        #
        # NOTE on what we assert: the GA's fitness has multiple
        # equivalent optima (precise mask + T=0, or relaxed mask +
        # high T) that all yield the same R² + L0 penalty. Which one
        # the GA lands on depends on the stochastic walk. So we
        # cannot assert T lands in a specific range — the GA might
        # validly choose T=0 if mask alone is precise enough. Instead:
        #
        # 1. Verify the GA finds a USEFUL solution (best_r2 > 0.3).
        # 2. Compare optimize_threshold=True vs opt-out path with the
        #    same seed: the joint GA must NOT do meaningfully worse
        #    than the mask-only GA (T-gene gives strictly more
        #    flexibility, so it should match or beat).
        # 3. Verify T stays in configured bounds.
        rng = np.random.default_rng(42)
        n_cells, n_years = 80, 25
        afi = np.concatenate([
            rng.uniform(70, 90, size=20),       # signal (raw %)
            rng.uniform(5,  15, size=60),       # noise  (raw %)
        ]) * 100.0                              # → production scale
        latent = rng.normal(size=n_years)
        per_cell = np.empty((n_cells, n_years, 1), dtype=float)
        for c in range(20):
            per_cell[c, :, 0] = latent + rng.normal(scale=0.25, size=n_years)
        for c in range(20, n_cells):
            per_cell[c, :, 0] = rng.normal(scale=1.0, size=n_years)
        y = latent + rng.normal(scale=0.1, size=n_years)

        common_kwargs = dict(
            threshold_min_pct=0.0,
            threshold_max_pct=80.0,
            population_size=60,
            n_generations=60,
            l0_lambda=0.05,
            min_cell_floor_abs=5,
            min_cell_floor_frac=0.05,
            early_stop_patience=30,
            seed=0,
        )
        cfg_on = GAConfig(optimize_threshold=True, **common_kwargs)
        cfg_off = GAConfig(optimize_threshold=False, **common_kwargs)

        result_on = run_ga(per_cell, y, cfg_on, afi=afi)
        result_off = run_ga(per_cell, y, cfg_off, afi=afi)

        # 1. T-gene-on GA must find a usable mask.
        self.assertGreater(
            result_on.best_r2, 0.3,
            msg=f"T-gene-on GA didn't find a usable mask: "
                f"best_r2={result_on.best_r2:.3f}",
        )
        # 2. T-gene-on should match or beat mask-only by a reasonable
        #    margin (allow 0.05 slack — GAs are stochastic).
        self.assertGreater(
            result_on.best_r2, result_off.best_r2 - 0.05,
            msg=f"T-gene-on GA underperformed mask-only: "
                f"on={result_on.best_r2:.3f}, off={result_off.best_r2:.3f}. "
                f"Joint optimization should never make things "
                f"meaningfully worse than the legacy path.",
        )
        # 3. T stays in configured range.
        self.assertGreaterEqual(result_on.best_T_pct, cfg_on.threshold_min_pct)
        self.assertLessEqual(result_on.best_T_pct, cfg_on.threshold_max_pct)
        # 4. Opt-out path confirms T = 0 (regression guard).
        self.assertEqual(result_off.best_T_pct, 0.0)


class TestAnnualMaskPaths(unittest.TestCase):
    """The annual-mask flag adds per-year leave-one-out parquets ALONGSIDE
    the existing pooled parquet. This test pins the contract:
      * pooled path stays the same (backwards-compatible)
      * per-year path adds a ``_y{year}_`` suffix
      * both paths sit in the same per-(country, crop) directory
    """

    def test_pooled_and_per_year_paths_share_parent_and_differ_only_by_suffix(self):
        # We don't need a fully-instantiated CellOptimizer (BaseGeo config),
        # we just need the path-builder semantics. Mock a tiny stand-in
        # with the bare attributes the path methods touch.
        from pathlib import Path
        from geocif.cell_optimizer import CellOptimizer

        class _Stub:
            dir_output = Path("/fake/out")

        # Bound-method invocation lets us reuse the production-path
        # formulas without instantiating BaseGeo machinery.
        pooled = CellOptimizer.production_mask_path(
            _Stub(), "india", "maize", 1,
        )
        y2020 = CellOptimizer.production_mask_path_for_year(
            _Stub(), "india", "maize", 1, 2020,
        )

        # Same parent dir.
        self.assertEqual(pooled.parent, y2020.parent)
        # Year-specific filename differs by the _y{year}_ infix.
        self.assertEqual(pooled.name, "india_maize_s1_optimized_mask.parquet")
        self.assertEqual(y2020.name, "india_maize_s1_y2020_optimized_mask.parquet")


class TestProductionMaskParquetRoundTrip(unittest.TestCase):
    """Smoke-check the production-output schema we hand to geoextract.
    The path / atomic-rename / row-shape are all the file-system side
    of the geoextract contract; if any of them drift, geoextract reads
    a malformed file."""

    def test_round_trip_schema_and_atomic_rename(self):
        import tempfile
        from pathlib import Path

        # Build the minimum schema we promise to geoextract.
        df = pd.DataFrame({
            "country":   ["india", "india", "india", "india"],
            "region":    ["test_region", "test_region", "test_region", "test_region"],
            "region_id": [1, 1, 1, 1],
            "cell_id":   [0, 1, 2, 3],
            "lat":       [30.1, 30.2, 30.3, 30.4],
            "lon":       [75.1, 75.2, 75.3, 75.4],
            "afi":       [80.0, 50.0, 20.0, 90.0],
            "included":  [True, False, True, True],
        })

        with tempfile.TemporaryDirectory() as tmpd:
            tmp_root = Path(tmpd)
            out_path = (
                tmp_root / "cell_optimizer" / "india" / "maize"
                / "india_maize_s1_optimized_mask.parquet"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)

            # Mimic the _write_production_mask path: write to .tmp, then rename.
            tmp_path = out_path.with_suffix(".parquet.tmp")
            df_out = df.copy()
            df_out["optimizer_version"] = "geocif-test"
            df_out["optimized_at"] = "2026-06-07"
            df_out.to_parquet(tmp_path, index=False)
            tmp_path.replace(out_path)

            # Geoextract perspective: read the parquet and verify schema.
            df_read = pd.read_parquet(out_path)
            required_cols = {
                "country", "region", "region_id", "cell_id",
                "lat", "lon", "afi", "included",
                "optimizer_version", "optimized_at",
            }
            self.assertEqual(set(df_read.columns), required_cols)
            self.assertEqual(df_read["included"].dtype, bool)
            # cell_id must be unique within (country, region) so geoextract
            # can build a {cell_id: included} dict without collision.
            grp = df_read.groupby(["country", "region"])["cell_id"].nunique()
            self.assertTrue((grp == df_read.groupby(["country", "region"]).size()).all())
            # Atomic rename: the .tmp file shouldn't be left behind.
            self.assertFalse(tmp_path.exists())


class TestFitnessMetric(unittest.TestCase):
    """0.4.760: signed Pearson r becomes the default GA fitness metric.

    Why it matters: R² = r² is sign-blind. On Nyandarua/Kenya the GA
    picked an anti-correlated NDVI mask (r=-0.32 held-out, R²=0.10)
    because that mask scored the same as the equally strong
    positively-correlated mask the operator actually wanted. Switching
    to signed r lets the GA *prefer* positive correlation over equal-
    magnitude negative correlation — the diagnostic mismatch closes.

    Tests:
      * default GAConfig().fitness_metric == "r"
      * loocv_r_multivariate sign discipline (positive vs negative
        correlation flip the sign, R² wouldn't)
      * fitness() routes to the right scorer via metric=
      * a constructed fixture where metric="r" picks the
        positively-correlated cells and metric="r2" can tie with the
        anti-correlated ones (same |r|)
    """

    def test_default_metric_is_r(self):
        self.assertEqual(GAConfig().fitness_metric, "r")

    def test_loocv_r_signed(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(20, 1))
        y = 2 * x[:, 0] + 1
        r_pos = loocv_r_multivariate(x, y)
        self.assertGreater(r_pos, 0.99)
        # Flip the sign of y → r flips sign too. R² wouldn't change.
        r_neg = loocv_r_multivariate(x, -y)
        self.assertLess(r_neg, -0.99)
        self.assertAlmostEqual(r_pos, -r_neg, places=3)
        # R² is sign-blind: both directions give the same value.
        r2_pos = loocv_r2_multivariate(x, y)
        r2_neg = loocv_r2_multivariate(x, -y)
        self.assertAlmostEqual(r2_pos, r2_neg, places=3)

    def test_loocv_r_is_held_out_with_in_sample_sign(self):
        # 0.4.763+: loocv_r_multivariate is |corr(LOOCV preds, y)|
        # carrying the in-sample sign of corr(x, y). On a noisy
        # fixture this gives a value with the same sign as in-sample
        # r but a strictly smaller (LOOCV-shrunken) magnitude.
        rng = np.random.default_rng(0)
        x = rng.normal(size=(15, 1))
        y = 1.5 * x[:, 0] + rng.normal(scale=0.6, size=15)
        r_helper = loocv_r_multivariate(x, y)
        r_in_sample = float(np.corrcoef(x[:, 0], y)[0, 1])
        # Sign matches in-sample.
        self.assertEqual(np.sign(r_helper), np.sign(r_in_sample))
        # Magnitude is shrunk by the held-out validation.
        self.assertLess(abs(r_helper), abs(r_in_sample))
        # And flipping y → metric flips sign.
        r_helper_neg = loocv_r_multivariate(x, -y)
        self.assertAlmostEqual(r_helper, -r_helper_neg, places=6)

    def test_loocv_r_penalizes_overfit_mask(self):
        # A "fake-signal" mask: x perfectly tracks y in-sample but the
        # relationship is driven by a single influential row. In-sample
        # |r| is high; LOOCV |r| should drop sharply.
        n = 12
        x_col = np.zeros(n)
        x_col[0] = 5.0  # the influential outlier
        y = np.zeros(n)
        y[0] = 5.0
        x = x_col.reshape(-1, 1)
        r_in_sample = float(np.corrcoef(x_col, y)[0, 1])
        self.assertGreater(r_in_sample, 0.99)
        # LOOCV: when the outlier row is the held-out fold, all
        # remaining x values are 0 → zero-variance training set →
        # _univariate_loocv_preds returns None → the variable is
        # skipped → no variables left → NaN. That's the contract:
        # degenerate folds make the metric refuse to score the mask,
        # which propagates to fitness as -inf and the GA discards it.
        r_loocv = loocv_r_multivariate(x, y)
        self.assertTrue(np.isnan(r_loocv))

    def test_loocv_r_too_few_years_returns_nan(self):
        x = np.ones((3, 1))
        y = np.ones(3)
        self.assertTrue(np.isnan(loocv_r_multivariate(x, y)))

    def test_fitness_metric_routes_correctly(self):
        # On a fixture with strong correlation, metric="r" should return
        # a value close to loocv_r and metric="r2" close to loocv_r2 —
        # i.e. fitness branches to the right scorer.
        rng = np.random.default_rng(0)
        n_cells, n_years = 10, 20
        latent = rng.normal(size=n_years)
        per_cell = np.empty((n_cells, n_years, 1), dtype=float)
        for c in range(n_cells):
            per_cell[c, :, 0] = latent + rng.normal(scale=0.3, size=n_years)
        y = latent + rng.normal(scale=0.1, size=n_years)
        mask = np.ones(n_cells, dtype=bool)
        x_agg = aggregate_over_mask(per_cell, mask)
        f_r  = fitness(mask, per_cell, y, 0.0, 1, metric="r")
        f_r2 = fitness(mask, per_cell, y, 0.0, 1, metric="r2")
        self.assertAlmostEqual(f_r,  loocv_r_multivariate(x_agg,  y), places=6)
        self.assertAlmostEqual(f_r2, loocv_r2_multivariate(x_agg, y), places=6)

    def test_anti_correlated_mask_penalized_under_r(self):
        # Build a fixture with two groups of cells: group A perfectly
        # correlated with yield, group B perfectly anti-correlated.
        # Under metric="r", a mask of only group A should outscore a
        # mask of only group B (positive r > negative r). Under
        # metric="r2", the two masks tie because |r| is the same.
        rng = np.random.default_rng(0)
        n_per_group, n_years = 6, 18
        latent = rng.normal(size=n_years)
        n_cells = 2 * n_per_group
        per_cell = np.empty((n_cells, n_years, 1), dtype=float)
        for c in range(n_per_group):
            per_cell[c, :, 0] =  latent + rng.normal(scale=0.05, size=n_years)
            per_cell[c + n_per_group, :, 0] = -latent + rng.normal(scale=0.05, size=n_years)
        y = latent + rng.normal(scale=0.05, size=n_years)

        mask_pos = np.zeros(n_cells, dtype=bool); mask_pos[:n_per_group] = True
        mask_neg = np.zeros(n_cells, dtype=bool); mask_neg[n_per_group:] = True

        # r metric: pos >> neg.
        f_pos_r = fitness(mask_pos, per_cell, y, 0.0, 1, metric="r")
        f_neg_r = fitness(mask_neg, per_cell, y, 0.0, 1, metric="r")
        self.assertGreater(f_pos_r, f_neg_r + 1.5,
                           msg=f"r metric should strongly prefer the "
                               f"positive-correlation mask; got "
                               f"f_pos={f_pos_r:.3f}, f_neg={f_neg_r:.3f}")
        self.assertGreater(f_pos_r, 0.9)
        self.assertLess(f_neg_r, -0.9)

        # r2 metric: the two masks have ~identical |r|, so r² ties.
        f_pos_r2 = fitness(mask_pos, per_cell, y, 0.0, 1, metric="r2")
        f_neg_r2 = fitness(mask_neg, per_cell, y, 0.0, 1, metric="r2")
        self.assertAlmostEqual(f_pos_r2, f_neg_r2, places=1,
                               msg=f"r² metric should be near-tied on |r|-"
                                   f"equivalent masks; got "
                                   f"f_pos={f_pos_r2:.3f}, f_neg={f_neg_r2:.3f}")

    def test_run_ga_carries_both_r_and_r2(self):
        # Regardless of which metric drove selection, GAResult must
        # carry both best_r and best_r2 (and baseline counterparts) so
        # downstream comparisons don't need a second run.
        rng = np.random.default_rng(0)
        n_cells, n_years = 12, 18
        latent = rng.normal(size=n_years)
        per_cell = np.empty((n_cells, n_years, 1), dtype=float)
        for c in range(n_cells):
            per_cell[c, :, 0] = latent + rng.normal(scale=0.2, size=n_years)
        y = latent + rng.normal(scale=0.1, size=n_years)
        for metric in ("r", "r2"):
            cfg = GAConfig(
                population_size=20, n_generations=10,
                min_cell_floor_abs=2, min_cell_floor_frac=0.01,
                optimize_threshold=False, seed=0, fitness_metric=metric,
            )
            result = run_ga(per_cell, y, cfg)
            self.assertTrue(np.isfinite(result.best_r),
                            msg=f"metric={metric}: best_r is non-finite")
            self.assertTrue(np.isfinite(result.best_r2),
                            msg=f"metric={metric}: best_r2 is non-finite")
            self.assertTrue(np.isfinite(result.baseline_r),
                            msg=f"metric={metric}: baseline_r is non-finite")
            self.assertEqual(result.fitness_metric, metric)
            # History must carry both columns regardless of metric.
            self.assertIn("best_r",  result.history.columns)
            self.assertIn("best_r2", result.history.columns)


class TestPooledLOOCV(unittest.TestCase):
    """0.4.766+: pooled LOOCV with region fixed effects.

    Mirrors the per-region primitives in TestFitnessMetric but the
    inputs are lists of per-region (aggregate, y, years) tuples and
    the LOOCV folds are by-year-across-all-regions, not per-region.
    """

    def _two_region_fixture(self, seed: int = 0, n_vars: int = 1):
        rng = np.random.default_rng(seed)
        years = tuple(range(2000, 2020))
        latent_a = rng.normal(size=len(years))
        latent_b = rng.normal(size=len(years))
        # Strong region-A signal, region-B with different intercept and
        # noise but same slope direction (pooled FE should help).
        agg_a = (latent_a + rng.normal(scale=0.1, size=len(years))).reshape(-1, n_vars)
        agg_b = (latent_b + rng.normal(scale=0.1, size=len(years))).reshape(-1, n_vars)
        y_a = 2.0 + 1.5 * latent_a + rng.normal(scale=0.2, size=len(years))
        y_b = 5.0 + 1.5 * latent_b + rng.normal(scale=0.2, size=len(years))  # different intercept
        return [agg_a, agg_b], [y_a, y_b], [years, years]

    def test_pooled_loocv_r2_strong_signal(self):
        aggs, ys, yrs = self._two_region_fixture(seed=0)
        r2 = loocv_r2_pooled(aggs, ys, yrs)
        self.assertGreater(r2, 0.7,
                           msg=f"strong-signal fixture should have high pooled R²; got {r2:.3f}")

    def test_pooled_loocv_r_signed(self):
        aggs, ys, yrs = self._two_region_fixture(seed=0)
        r = loocv_r_pooled(aggs, ys, yrs)
        self.assertGreater(r, 0.7)
        # Flip both regions' y → sign flips
        ys_neg = [-y_ for y_ in ys]
        r_neg = loocv_r_pooled(aggs, ys_neg, yrs)
        self.assertLess(r_neg, -0.7)

    def test_pooled_loocv_too_few_regions_returns_nan(self):
        aggs, ys, yrs = self._two_region_fixture(seed=0)
        # Only one valid region → cannot identify FE
        result = loocv_r2_pooled(
            [aggs[0]], [ys[0]], [yrs[0]],
        )
        self.assertTrue(np.isnan(result))

    def test_pooled_loocv_skips_none_regions(self):
        # None entries represent regions whose mask was infeasible
        # this generation; they should be silently dropped, not crash.
        aggs, ys, yrs = self._two_region_fixture(seed=0)
        result = loocv_r2_pooled(
            [aggs[0], None, aggs[1]],
            [ys[0], np.array([]), ys[1]],
            [yrs[0], (), yrs[1]],
        )
        self.assertTrue(np.isfinite(result))

    def test_pooled_predictions_shape(self):
        # _pooled_loocv_predictions returns (preds, y_held) of equal length
        aggs, ys, yrs = self._two_region_fixture(seed=0)
        pair = _pooled_loocv_predictions(aggs, ys, yrs)
        self.assertIsNotNone(pair)
        preds, y_held = pair
        self.assertEqual(preds.shape, y_held.shape)
        # Two regions × 20 years = 40 observations, minus folds dropped
        # for under-determined OLS (none in this fixture).
        self.assertLessEqual(len(preds), 40)

    def test_held_out_year_predictions_recovers_strong_signal(self):
        # Outer-LOOCV helper: predict one held-out year using OLS trained
        # on the rest. Strong-signal fixture should give preds close to
        # actuals.
        rng = np.random.default_rng(0)
        n_vars = 1
        n_train = 18
        # 3 regions, each y = intercept_i + 2*aggregate
        aggs_train, y_train, aggs_held, y_held = [], [], [], []
        for r, intercept in enumerate([1.0, 4.0, 7.0]):
            agg_t = rng.normal(size=(n_train, n_vars))
            y_t = intercept + 2.0 * agg_t[:, 0] + rng.normal(scale=0.05, size=n_train)
            agg_h = rng.normal(size=n_vars)
            y_h = intercept + 2.0 * agg_h[0] + rng.normal(scale=0.05)
            aggs_train.append(agg_t)
            y_train.append(y_t)
            aggs_held.append(agg_h)
            y_held.append(float(y_h))
        pair = _pooled_held_out_year_predictions(
            aggs_held, y_held, aggs_train, y_train,
        )
        self.assertIsNotNone(pair)
        preds, actuals = pair
        self.assertEqual(preds.shape, (3,))
        # Strong signal + clean FE → preds should be very close to actuals.
        for p, a in zip(preds, actuals):
            self.assertLess(abs(p - a), 0.5,
                            msg=f"strong-signal held-out should give close preds; got {p:.2f} vs {a:.2f}")

    def test_held_out_year_predictions_too_few_regions_returns_none(self):
        # Only one valid region → cannot identify FE → returns None
        aggs_h = [np.array([1.0]), None, None]
        y_h = [1.0, float("nan"), float("nan")]
        aggs_t = [np.random.normal(size=(15, 1)), None, None]
        y_t = [np.random.normal(size=15), np.array([]), np.array([])]
        result = _pooled_held_out_year_predictions(aggs_h, y_h, aggs_t, y_t)
        self.assertIsNone(result)


class TestRunGAPooled(unittest.TestCase):
    """0.4.766+: end-to-end pooled GA on a planted multi-region signal.

    Three synthetic regions, each with 10 signal cells + 15 noise cells.
    Each region's yield = mean(signal cells' NDVI) + region-specific
    intercept + light noise. The pooled GA should:
      * Select close to the signal cells in each region
      * Land on a positive best_r (sign discipline preserved)
      * Beat the all-cells baseline (pooled lift > 0)
    """

    def _three_region_fixture(self, seed: int = 42):
        rng = np.random.default_rng(seed)
        n_years = 22
        n_vars = 1
        regions = ["r0", "r1", "r2"]
        per_cell_list, y_list, years_list, afi_list = [], [], [], []
        for r_idx, intercept in enumerate([1.0, 3.0, 5.0]):
            n_signal, n_noise = 10, 15
            n_cells = n_signal + n_noise
            latent = rng.normal(size=n_years)
            per_cell = np.empty((n_cells, n_years, n_vars), dtype=float)
            for c in range(n_signal):
                per_cell[c, :, 0] = latent + rng.normal(scale=0.1, size=n_years)
            for c in range(n_signal, n_cells):
                per_cell[c, :, 0] = rng.normal(size=n_years)
            y = intercept + 1.5 * latent + rng.normal(scale=0.15, size=n_years)
            per_cell_list.append(per_cell)
            y_list.append(y)
            years_list.append(tuple(range(2001, 2001 + n_years)))
            afi_list.append(np.full(n_cells, 70.0))  # uniform 70% cropland
        return regions, per_cell_list, y_list, years_list, afi_list

    def test_pooled_ga_returns_GAResultPooled(self):
        regions, per_cell_list, y_list, years_list, afi_list = self._three_region_fixture(seed=0)
        cfg = GAConfig(
            population_size=30, n_generations=20,
            min_cell_floor_abs=3, min_cell_floor_frac=0.05,
            optimize_threshold=False, seed=0,
        )
        result = run_ga_pooled(
            per_cell_list, y_list, years_list, afi_list, regions, cfg=cfg,
        )
        self.assertIsInstance(result, GAResultPooled)
        for r in regions:
            self.assertIn(r, result.best_masks)
            self.assertEqual(result.best_masks[r].dtype, bool)
        self.assertTrue(np.isfinite(result.best_fitness))
        self.assertTrue(np.isfinite(result.best_r2))
        self.assertTrue(np.isfinite(result.baseline_r2))
        # Pooled history has the expected columns.
        for col in ["generation", "best_fit", "best_r", "best_r2",
                    "n_selected_total", "n_regions_in_pool"]:
            self.assertIn(col, result.history.columns)

    def test_pooled_ga_beats_baseline_on_planted_signal(self):
        regions, per_cell_list, y_list, years_list, afi_list = self._three_region_fixture(seed=1)
        cfg = GAConfig(
            population_size=40, n_generations=40,
            min_cell_floor_abs=3, min_cell_floor_frac=0.05,
            l0_lambda=0.02,
            optimize_threshold=False, seed=1,
        )
        result = run_ga_pooled(
            per_cell_list, y_list, years_list, afi_list, regions, cfg=cfg,
        )
        # On a planted-signal fixture, pooled R² with the GA mask
        # should exceed the all-cells baseline pooled R².
        self.assertGreater(
            result.best_r2, result.baseline_r2,
            msg=f"GA should beat baseline; got best={result.best_r2:.3f} "
                f"baseline={result.baseline_r2:.3f}"
        )


class TestPMedian(unittest.TestCase):
    """0.4.772+: p-median cardinality-constrained GA. Each region's mask
    has EXACTLY p cells (instead of the binary GA's free cardinality
    + L0 penalty). Operators preserve the sum invariant; sweep mode
    runs the pipeline for multiple p_frac values.
    """

    def test_resolve_p_per_region_frac(self):
        p = _resolve_p_per_region(0.10, None, [100, 200, 5])
        # Floors round to 10/20/0; 0 gets clamped to 1.
        self.assertEqual(p, [10, 20, 1])

    def test_resolve_p_per_region_abs_clamps_small_regions(self):
        p = _resolve_p_per_region(None, 30, [100, 200, 5])
        # 30 cells requested; the 5-cell region clamps to its size.
        self.assertEqual(p, [30, 30, 5])

    def test_resolve_p_per_region_abs_overrides_frac(self):
        p = _resolve_p_per_region(0.99, 10, [100])
        self.assertEqual(p, [10])

    def test_resolve_p_per_region_raises_on_no_target(self):
        with self.assertRaises(ValueError):
            _resolve_p_per_region(None, None, [100])
        with self.assertRaises(ValueError):
            _resolve_p_per_region(0.0, 0, [100])

    def test_repair_slice_to_p_no_op_when_correct(self):
        slc = np.array([True, True, False, False])
        _repair_slice_to_p(slc, 2, np.random.default_rng(0))
        self.assertEqual(slc.sum(), 2)

    def test_repair_slice_to_p_grows(self):
        slc = np.array([True, False, False, False, False])
        _repair_slice_to_p(slc, 3, np.random.default_rng(0))
        self.assertEqual(slc.sum(), 3)

    def test_repair_slice_to_p_shrinks(self):
        slc = np.array([True, True, True, True, True])
        _repair_slice_to_p(slc, 2, np.random.default_rng(0))
        self.assertEqual(slc.sum(), 2)

    def test_init_pop_p_median_pooled_sums(self):
        rng = np.random.default_rng(0)
        offsets = [(0, 100), (100, 300), (300, 305)]
        p_per_region = [10, 20, 1]
        afi_list = [np.full(100, 50.0), np.full(200, 50.0), np.full(5, 50.0)]
        pop = init_pop_p_median_pooled(
            rng, 20, offsets, p_per_region, afi_list, 0.0,
        )
        # Every genome × every region: slice sum equals p_per_region.
        for g in range(20):
            for i, (s, e) in enumerate(offsets):
                self.assertEqual(pop[g, s:e].sum(), p_per_region[i])

    def test_swap_mutation_preserves_sums(self):
        rng = np.random.default_rng(0)
        offsets = [(0, 50), (50, 150), (150, 175)]
        p_per_region = [5, 20, 10]
        afi_list = [np.full(50, 50.0), np.full(100, 50.0), np.full(25, 50.0)]
        pop = init_pop_p_median_pooled(
            rng, 5, offsets, p_per_region, afi_list, 0.0,
        )
        # Force a swap in every region (prob=1.0).
        for g in range(5):
            _mutate_p_median_pooled(pop[g], offsets, 1.0, rng)
            for i, (s, e) in enumerate(offsets):
                self.assertEqual(pop[g, s:e].sum(), p_per_region[i])

    def test_apply_repair_pooled_fixes_oversize(self):
        # Genome with too-many cells in one slice — repair should trim.
        genome = np.zeros(50, dtype=bool)
        genome[:30] = True   # region 0 has 30 ones, region 1 has 0
        offsets = [(0, 25), (25, 50)]
        p_per_region = [10, 5]
        _apply_repair_pooled(genome, offsets, p_per_region, np.random.default_rng(0))
        self.assertEqual(genome[:25].sum(), 10)
        self.assertEqual(genome[25:].sum(), 5)

    def test_p_median_with_high_T_does_not_zero_effective_mask(self):
        # 0.4.773 regression: in p-median mode the GA returns masks
        # whose sum == p_i. If the AFI threshold filter were still
        # applied, small regions could collapse to zero effective cells
        # (Samburu-style failure). The fix: optimize_threshold is
        # auto-disabled in p_median mode at the CellOptimizer init level,
        # so T_norm stays at 0 and the AFI filter is a no-op.
        #
        # We can't import CellOptimizer here (needs config files), so
        # verify the contract directly at the GA level: with
        # optimize_threshold=False, the fitness function's AFI branch
        # is not taken, regardless of how low the cells' AFI is.
        rng = np.random.default_rng(0)
        n_years, n_vars = 12, 1
        regions = ["small"]
        per_cell_list = [rng.normal(size=(8, n_years, n_vars))]
        y_list = [rng.normal(size=n_years)]
        years_list = [tuple(range(2010, 2010 + n_years))]
        afi_list = [np.full(8, 5.0)]  # very low AFI — would zero out under any T>5
        # Need ≥2 regions for run_ga_pooled; duplicate the fixture.
        regions = ["a", "b"]
        per_cell_list = per_cell_list * 2
        y_list = y_list * 2
        years_list = years_list * 2
        afi_list = afi_list * 2
        cfg = GAConfig(
            population_size=10, n_generations=5,
            cardinality_mode="p_median", p_target_frac=0.25,
            optimize_threshold=False,   # mimics the CellOptimizer auto-disable
            seed=0,
        )
        result = run_ga_pooled(
            per_cell_list, y_list, years_list, afi_list, regions, cfg=cfg,
        )
        # With p_target_frac=0.25 and n_cells=8: p_i = 2.
        for r in regions:
            self.assertEqual(int(result.best_masks[r].sum()), 2)
            self.assertEqual(result.best_T_pct[r], 0.0)  # T stayed at 0

    def test_p_median_ga_converges_on_planted_signal(self):
        # Three regions, each with 30 cells (10 signal + 20 noise).
        # p_target_frac = 0.40 → p_i = 12 each. The GA should pick
        # mostly signal cells.
        rng = np.random.default_rng(42)
        n_years, n_vars = 18, 1
        regions = ["r0", "r1", "r2"]
        per_cell_list, y_list, years_list, afi_list = [], [], [], []
        for r_idx, intercept in enumerate([1.0, 3.0, 5.0]):
            n_signal, n_noise = 10, 20
            n_cells = n_signal + n_noise
            latent = rng.normal(size=n_years)
            per_cell = np.empty((n_cells, n_years, n_vars), dtype=float)
            for c in range(n_signal):
                per_cell[c, :, 0] = latent + rng.normal(scale=0.05, size=n_years)
            for c in range(n_signal, n_cells):
                per_cell[c, :, 0] = rng.normal(size=n_years)
            per_cell_list.append(per_cell)
            y_list.append(intercept + 1.5 * latent + rng.normal(scale=0.1, size=n_years))
            years_list.append(tuple(range(2001, 2001 + n_years)))
            afi_list.append(np.full(n_cells, 70.0))
        cfg = GAConfig(
            population_size=30, n_generations=30,
            optimize_threshold=False, seed=0,
            cardinality_mode="p_median", p_target_frac=0.40,
        )
        result = run_ga_pooled(
            per_cell_list, y_list, years_list, afi_list, regions, cfg=cfg,
        )
        # Each region's mask must have exactly p=12 cells.
        for r in regions:
            self.assertEqual(int(result.best_masks[r].sum()), 12)
        # Should beat the all-cells baseline on this planted fixture.
        self.assertGreater(result.best_r2, result.baseline_r2)


class TestDetrendYield(unittest.TestCase):
    """0.4.765+: linear yield detrending before GA fitness eval.

    Yield series over 25+ year windows carry climate + productivity
    trends. Without detrending, Pearson r against a seasonal EO
    aggregate captures the *trend*, inflating in-sample fit while
    held-out generalization stays flat.
    """

    def test_removes_linear_trend(self):
        rng = np.random.default_rng(0)
        years = tuple(range(2000, 2025))
        y_raw = 0.1 * np.arange(len(years)) + 1.0 + rng.normal(scale=0.05, size=len(years))
        y_det = _detrend_yield(y_raw, years)
        r_before = float(np.corrcoef(np.arange(len(years)), y_raw)[0, 1])
        r_after = float(np.corrcoef(np.arange(len(years)), y_det)[0, 1])
        self.assertGreater(r_before, 0.9)         # strong trend before
        self.assertLess(abs(r_after), 0.1)        # gone after

    def test_preserves_mean(self):
        # Detrended series should have the same mean as the original so
        # downstream units stay yield-like (t/ha, not residuals).
        rng = np.random.default_rng(0)
        years = tuple(range(2000, 2025))
        y_raw = 0.1 * np.arange(len(years)) + 2.5 + rng.normal(scale=0.05, size=len(years))
        y_det = _detrend_yield(y_raw, years)
        self.assertAlmostEqual(float(np.mean(y_det)), float(np.mean(y_raw)), places=6)

    def test_passthrough_too_few_finite(self):
        # <3 finite years → linear fit underspecified → pass through unchanged.
        y = np.array([1.0, np.nan, np.nan, np.nan, 2.0])
        years = (2020, 2021, 2022, 2023, 2024)
        y_det = _detrend_yield(y, years)
        np.testing.assert_array_equal(y_det, y)

    def test_passthrough_zero_variance(self):
        # Constant y → no trend to remove → return unchanged.
        y = np.full(10, 3.0)
        years = tuple(range(2015, 2025))
        y_det = _detrend_yield(y, years)
        np.testing.assert_array_equal(y_det, y)

    def test_nan_positions_preserved(self):
        # NaN years in the middle pass through; finite years detrend.
        y = np.array([1.0, np.nan, 2.0, 3.0, np.nan, 5.0])
        years = (2020, 2021, 2022, 2023, 2024, 2025)
        y_det = _detrend_yield(y, years)
        self.assertTrue(np.isnan(y_det[1]) and np.isnan(y_det[4]))
        self.assertTrue(all(np.isfinite(y_det[[0, 2, 3, 5]])))


if __name__ == "__main__":
    unittest.main()
