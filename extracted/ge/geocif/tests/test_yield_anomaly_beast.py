"""Unit tests for the BEAST-based yield anomaly detector."""
import unittest

import numpy as np
import pandas as pd

try:
    import Rbeast  # noqa: F401
    HAS_BEAST = True
except ImportError:
    HAS_BEAST = False

from geocif.ml.yield_anomaly_beast import (
    AnomalyThresholds,
    detect_spikes_batch,
    detect_spikes_one_series,
)


@unittest.skipUnless(HAS_BEAST, "Rbeast not installed in this environment")
class TestDetectSpikesOneSeries(unittest.TestCase):
    """Synthetic-series tests for the per-series detector."""

    def _trend_plus_noise(self, n_years=25, slope=0.05, sigma=0.1, seed=0):
        rng = np.random.default_rng(seed)
        years = np.arange(2000, 2000 + n_years)
        base = 1.0 + slope * (years - years[0]) + rng.normal(scale=sigma, size=n_years)
        return years, base

    def test_spike_revert_is_detected_high_confidence(self):
        years, yields = self._trend_plus_noise(seed=1)
        # Plant a +6 std-dev spike in year 2012, revert next year.
        spike_idx = 12
        yields[spike_idx] += 1.0   # ~10x noise sigma
        out = detect_spikes_one_series(years, yields)
        self.assertEqual(out["status"], "ok")
        types = [f["anomaly_type"] for f in out["flags"]]
        self.assertIn("spike_revert", types,
                      msg=f"expected spike_revert; got flags: {out['flags']}")
        flag = next(f for f in out["flags"] if f["anomaly_type"] == "spike_revert")
        self.assertEqual(flag["confidence"], "high")
        self.assertEqual(flag["year"], int(years[spike_idx]))

    def test_regime_shift_is_NOT_flagged(self):
        # Plant a step change: yields jump and STAY at the new level.
        # BEAST should detect a change-point at the jump → high cp_prob
        # → our detector treats it as a real regime shift, NOT a spike.
        years, yields = self._trend_plus_noise(seed=2, n_years=30, sigma=0.05)
        step_idx = 15
        yields[step_idx:] += 1.0
        out = detect_spikes_one_series(years, yields)
        self.assertEqual(out["status"], "ok")
        # The shift year itself shouldn't appear as a noise spike.
        flagged_years = [f["year"] for f in out["flags"]
                         if f["anomaly_type"] == "spike_revert"]
        self.assertNotIn(int(years[step_idx]), flagged_years,
                         msg=f"regime shift wrongly flagged as spike_revert: "
                             f"{out['flags']}")

    def test_end_of_series_spike_is_flagged_medium_confidence(self):
        years, yields = self._trend_plus_noise(seed=3)
        # Spike at the LAST year — no t+1 to verify reversion.
        yields[-1] += 1.0
        out = detect_spikes_one_series(years, yields)
        self.assertEqual(out["status"], "ok")
        types = [f["anomaly_type"] for f in out["flags"]]
        self.assertIn("end_of_series_spike", types,
                      msg=f"end-of-series spike not detected: {out['flags']}")
        flag = next(f for f in out["flags"]
                    if f["anomaly_type"] == "end_of_series_spike")
        self.assertEqual(flag["confidence"], "medium")
        self.assertEqual(flag["year"], int(years[-1]))
        self.assertTrue(np.isnan(flag["next_year_z"]))

    def test_smooth_series_produces_zero_flags(self):
        # Clean trend + small noise → no LARGE flags expected. Note:
        # with the MAD-based robust sigma (0.4.775+), the sigma estimate
        # tightly tracks true noise, so a random ~2.5σ outlier in 25
        # draws WILL appear in a Gaussian series ~5% of the time. That's
        # statistically correct, not a false positive. We test the
        # CALIBRATED behavior: at z_threshold=3.0 (3-sigma rule), a
        # clean series should produce zero flags.
        years, yields = self._trend_plus_noise(seed=4, sigma=0.05)
        out = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(z_threshold=3.0),
        )
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["flags"], [],
                         msg=f"clean series @ z_threshold=3 produced "
                             f"false-positive flags: {out['flags']}")

    def test_short_series_skipped(self):
        years = np.arange(2010, 2015)   # 5 years < min_years=10
        yields = np.array([1.0, 1.1, 1.0, 0.95, 1.05])
        out = detect_spikes_one_series(years, yields)
        self.assertEqual(out["status"], "too_short")
        self.assertEqual(out["flags"], [])

    def test_all_nan_series(self):
        out = detect_spikes_one_series(
            np.arange(2000, 2020), np.full(20, np.nan),
        )
        self.assertEqual(out["status"], "all_nan")

    def test_nan_gap_in_middle_doesnt_crash(self):
        years, yields = self._trend_plus_noise(seed=5)
        yields[10] = np.nan   # missing year — BEAST should handle it
        out = detect_spikes_one_series(years, yields)
        self.assertEqual(out["status"], "ok")  # no crash

    def test_negative_spike_ignored_by_default(self):
        years, yields = self._trend_plus_noise(seed=6)
        yields[12] -= 1.0  # large NEGATIVE deviation
        out = detect_spikes_one_series(years, yields)
        # Default include_negative_spikes=False → no flag for the dip.
        spike_years = [f["year"] for f in out["flags"]]
        self.assertNotIn(int(years[12]), spike_years)

    def test_negative_spike_detected_when_enabled(self):
        years, yields = self._trend_plus_noise(seed=7)
        yields[12] -= 1.0
        out = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(include_negative_spikes=True),
        )
        spike_years = [f["year"] for f in out["flags"]]
        self.assertIn(int(years[12]), spike_years)


@unittest.skipUnless(HAS_BEAST, "Rbeast not installed in this environment")
class TestDetectSpikesBatch(unittest.TestCase):
    """Multi-series orchestration test."""

    def _build_panel(self):
        # Two regions, both with 25 years; A has a spike+revert at 2012,
        # B is clean.
        rng = np.random.default_rng(0)
        years = np.arange(2000, 2025)
        rows = []
        for region, plant_spike in [("A", True), ("B", False)]:
            y = 1.0 + 0.05 * (years - years[0]) + rng.normal(scale=0.08, size=years.size)
            if plant_spike:
                y[12] += 0.9
            for yr, val in zip(years, y):
                rows.append({
                    "country": "Testland",
                    "crop": "Maize",
                    "region": region,
                    "season": "Annual",
                    "year": int(yr),
                    "yield": float(val),
                })
        return pd.DataFrame(rows)

    def test_batch_finds_planted_spike_only_in_A(self):
        df = self._build_panel()
        flagged = detect_spikes_batch(
            df,
            group_cols=("country", "crop", "region", "season"),
            year_col="year", target_col="yield",
        )
        # Region A should have at least one spike_revert; region B zero.
        a_flags = flagged[flagged["region"] == "A"]
        b_flags = flagged[flagged["region"] == "B"]
        self.assertGreater(len(a_flags), 0,
                           msg=f"region A spike not detected; flagged df: {flagged}")
        a_types = set(a_flags["anomaly_type"])
        self.assertIn("spike_revert", a_types)
        self.assertEqual(len(b_flags), 0,
                         msg=f"region B (clean) falsely flagged: {b_flags}")

    def test_batch_returns_empty_for_empty_input(self):
        df = pd.DataFrame(
            columns=["country", "crop", "region", "season", "year", "yield"],
        )
        out = detect_spikes_batch(
            df,
            group_cols=("country", "crop", "region", "season"),
            year_col="year", target_col="yield",
        )
        self.assertEqual(len(out), 0)


@unittest.skipUnless(HAS_BEAST, "Rbeast not installed in this environment")
class TestClimatologyPadding(unittest.TestCase):
    """Regression tests for the optional right-edge climatology pad.

    The pad is consumed inside BEAST and trimmed off before any
    residual/MAD/z/classifier work, so it must:
      (a) not change result-dict shape (still len == original n_steps),
      (b) leave the end_of_series_spike bucket intact (no synthetic
          revert verification leaks through the trim), and
      (c) reduce endpoint trend-bending bias when a spike sits at y_end
          — i.e. trend[t_end] stays closer to the historical mean and
          the z-score grows.
    """

    def _flat_with_endpoint_spike(self, n_years=25, baseline=1.0, sigma=0.05,
                                   spike=0.6, seed=11):
        rng = np.random.default_rng(seed)
        years = np.arange(2000, 2000 + n_years)
        yields = baseline + rng.normal(scale=sigma, size=n_years)
        yields[-1] += spike  # large positive spike at the LAST year
        return years, yields

    def test_padding_preserves_output_array_lengths(self):
        years, yields = self._flat_with_endpoint_spike()
        out = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(pad_climatology=True, n_pad_years=5),
        )
        self.assertEqual(out["status"], "ok")
        # The pad must be trimmed off — every per-year array stays at
        # the original length.
        self.assertEqual(len(out["years"]), len(years))
        self.assertEqual(len(out["trend"]), len(years))
        self.assertEqual(len(out["cp_prob"]), len(years))
        self.assertEqual(len(out["residual"]), len(years))
        self.assertEqual(len(out["z_score"]), len(years))
        # Pad metadata should be exposed for diagnostics.
        self.assertEqual(out["n_pad_years"], 5)
        self.assertTrue(np.isfinite(out["climatology"]))

    def test_padding_preserves_end_of_series_bucket(self):
        # A spike at y_end with padding ON should still classify as
        # end_of_series_spike — NOT as a synthetic spike_revert just
        # because the pad values match climatology. This is the core
        # safety property of Option A.
        years, yields = self._flat_with_endpoint_spike()
        out = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(pad_climatology=True, n_pad_years=5),
        )
        self.assertEqual(out["status"], "ok")
        end_flags = [f for f in out["flags"] if f["year"] == int(years[-1])]
        self.assertEqual(len(end_flags), 1,
                         msg=f"expected exactly one flag at y_end; got {out['flags']}")
        self.assertEqual(end_flags[0]["anomaly_type"], "end_of_series_spike",
                         msg=f"padding leaked into revert verification: "
                             f"{end_flags[0]}")
        # next_year_z must remain NaN — the classifier must not see the
        # pad values.
        self.assertTrue(np.isnan(end_flags[0]["next_year_z"]))

    def test_padding_reduces_endpoint_trend_bias(self):
        # With padding OFF, BEAST's posterior trend at y_end gets pulled
        # toward the last observation (the spike), so the residual /
        # z-score at y_end is artificially small. With padding ON, the
        # synthetic climatology values to the right anchor the trend
        # near the historical mean, so the residual / z grows.
        years, yields = self._flat_with_endpoint_spike()

        out_off = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(pad_climatology=False),
        )
        out_on = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(pad_climatology=True, n_pad_years=5),
        )
        self.assertEqual(out_off["status"], "ok")
        self.assertEqual(out_on["status"], "ok")

        trend_off = out_off["trend"][-1]
        trend_on = out_on["trend"][-1]
        obs = float(yields[-1])

        # Trend ON should be CLOSER to the historical mean (smaller),
        # i.e. farther below the spiked observation.
        self.assertLess(trend_on, trend_off,
                        msg=f"padding didn't lower endpoint trend: "
                            f"trend_off={trend_off:.4f}, trend_on={trend_on:.4f}")
        # And the residual ON should be LARGER in absolute value.
        self.assertGreater(abs(obs - trend_on), abs(obs - trend_off),
                           msg=f"padding didn't grow endpoint residual: "
                               f"|obs-trend_off|={abs(obs-trend_off):.4f}, "
                               f"|obs-trend_on|={abs(obs-trend_on):.4f}")

    def test_padding_off_keeps_endpoint_flag_behavior(self):
        # Backstop: with the flag explicitly OFF, the detector still
        # behaves like the pre-padding code path on the same fixture.
        years, yields = self._flat_with_endpoint_spike()
        out = detect_spikes_one_series(
            years, yields,
            thresholds=AnomalyThresholds(pad_climatology=False),
        )
        self.assertEqual(out["status"], "ok")
        # n_pad_years recorded as 0 when padding is off.
        self.assertEqual(out["n_pad_years"], 0)
        # Climatology is computed only when padding kicks in.
        self.assertTrue(np.isnan(out["climatology"]))


class TestAnomalyThresholdsDefaults(unittest.TestCase):
    """Pure-Python tests that don't need BEAST."""

    def test_defaults_match_spec(self):
        t = AnomalyThresholds()
        self.assertEqual(t.z_threshold, 2.0)
        self.assertEqual(t.cp_threshold, 0.5)
        self.assertEqual(t.revert_threshold, 1.0)
        self.assertEqual(t.min_years, 10)
        self.assertFalse(t.include_negative_spikes)
        # New climatology-padding fields default on with n_pad_years=5,
        # method='mean'.
        self.assertTrue(t.pad_climatology)
        self.assertEqual(t.n_pad_years, 5)
        self.assertEqual(t.climatology_method, "mean")


if __name__ == "__main__":
    unittest.main()
