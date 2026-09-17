"""Unit tests for :mod:`geocif.phenology.core` (DESIGN.md section 3).

Index convention throughout: every ``*_idx`` is a 0-based integer position
along axis 0 of the cube (axis 0 = time, one step = one day); the caller maps
index 0 to the calendar origin (normally the planting-window start). Rain and
PET are mm/day, soil storage and thresholds are mm, every ``*_days`` is days.

Hand-computed expectations carry the arithmetic in a comment next to them.
"""

from __future__ import annotations

import time
import unittest
from datetime import date, timedelta

import numpy as np

from geocif.phenology.core import (
    CessationParams,
    CessationStatus,
    OnsetParams,
    OnsetStatus,
    SeasonState,
    _cessation_index_1d,
    _onset_index_1d,
    _spell_lookahead,
    cessation_index,
    combine_pet,
    conditional_onset_probability,
    hargreaves_pet,
    onset_climatology,
    onset_index,
    onset_percentile,
    onset_state,
    season_phenology,
)

#: Default detector used by most acceptance cases (DESIGN section 3.1).
DEFAULT_ONSET = OnsetParams()
DEFAULT_CESSATION = CessationParams()

#: 1-D oracle status strings -> the int8 codes the vectorised path returns.
_ONSET_STATUS_FROM_STR = {
    "ok": int(OnsetStatus.OK),
    "insufficient_data": int(OnsetStatus.INSUFFICIENT_DATA),
    "no_trigger": int(OnsetStatus.NO_TRIGGER),
    "no_data": int(OnsetStatus.NO_DATA),
}
_CESSATION_STATUS_FROM_STR = {
    "ok": int(CessationStatus.OK),
    "no_onset": int(CessationStatus.NO_ONSET),
    "no_range": int(CessationStatus.NO_RANGE),
    "right_censored": int(CessationStatus.RIGHT_CENSORED),
}


def _scalar(arr) -> float:
    """Return a 0-d / 1-element array as a Python float (NaN stays NaN)."""
    return float(np.asarray(arr).reshape(-1)[0])


# ---------------------------------------------------------------------------
# DESIGN 3.10 acceptance items 1, 2, 3 (onset)
# ---------------------------------------------------------------------------
class TestAcceptanceOnset(unittest.TestCase):
    """DESIGN section 3.10 items 1-3, worded as written in the contract."""

    def test_item1_clean_trigger_gives_onset_9(self) -> None:
        """1. 0 mm x 9 days, 20 mm on day 10, then 5 mm/day x 40 -> onset 9."""
        pr = np.concatenate([np.zeros(9), [20.0], np.full(40, 5.0)])  # T = 50
        onset, status = onset_index(pr, 0, 48, DEFAULT_ONSET)
        # W[9] = pr[7] + pr[8] + pr[9] = 0 + 0 + 20 = 20 >= 20 mm; 9 >= window_days-1 = 2;
        # look-ahead 9 + 30 = 39 <= T = 50; no day after index 9 is dry (5 mm >= 1 mm)
        # and the longest dry run before it is 9 days < dry_spell_days = 10.
        self.assertEqual(_scalar(onset), 9.0)
        self.assertEqual(int(status), int(OnsetStatus.OK))

    def test_item2_false_start_rejected(self) -> None:
        """2. 20 mm day 10, then 15 days < 1 mm, then 5 mm/day -> onset > 9."""
        pr = np.concatenate([np.zeros(9), [20.0], np.zeros(15), np.full(40, 5.0)])
        onset, status = onset_index(pr, 0, 60, DEFAULT_ONSET)
        # Candidate 9 is invalidated: indices 10..24 are dry, so r[19] = 10 and a
        # qualifying spell ENDS at 19..24, inside the look-ahead [9+10-1, 9+30-1] = [18, 38].
        # The literal wording ("then 5 mm/day") never re-triggers, because the
        # 3-day window only reaches 5+5+5 = 15 mm < 20 mm: the answer is no onset,
        # which is still "not 9".
        self.assertTrue(np.isnan(_scalar(onset)))
        self.assertEqual(int(status), int(OnsetStatus.NO_TRIGGER))

        # Same false start, but with enough rain afterwards to re-trigger: the
        # onset must land strictly after the rejected candidate.
        pr2 = np.concatenate([np.zeros(9), [20.0], np.zeros(15), np.full(60, 10.0)])
        onset2, status2 = onset_index(pr2, 0, 80, DEFAULT_ONSET)
        # W[26] = pr[24] + pr[25] + pr[26] = 0 + 10 + 10 = 20 >= 20 mm, and nothing
        # after index 25 is dry, so look-ahead [35, 55] is spell-free.
        self.assertEqual(_scalar(onset2), 26.0)
        self.assertEqual(int(status2), int(OnsetStatus.OK))
        self.assertGreater(_scalar(onset2), 9.0)

    def test_item3_partial_window_not_accepted(self) -> None:
        """3. 25 mm on day 0 -> onset != 0 (a partial window never qualifies)."""
        pr = np.concatenate([[25.0], np.full(60, 5.0)])
        onset, status = onset_index(pr, 0, 60, DEFAULT_ONSET)
        # Index 0 has only one day of the 3-day window, so t >= window_days-1 = 2
        # fails. The first full window is W[2] = 25 + 5 + 5 = 35 >= 20 mm.
        self.assertNotEqual(_scalar(onset), 0.0)
        self.assertEqual(_scalar(onset), 2.0)
        self.assertEqual(int(status), int(OnsetStatus.OK))


# ---------------------------------------------------------------------------
# DESIGN 3.10 acceptance items 4, 5, 6 (cessation)
# ---------------------------------------------------------------------------
class TestAcceptanceCessation(unittest.TestCase):
    """DESIGN section 3.10 items 4-6."""

    def test_item4_cessation_varies_across_years(self) -> None:
        """4. Multi-year synthetic data with a moving rain-stop date -> std > 3 days.

        24 "years" are laid out as 24 pixels of one (T, Y) cube; each year rains
        10 mm/day until its own stop index, then nothing, against a constant
        5 mm/day PET.
        """
        rng = np.random.default_rng(4242)
        n_years, n_time = 24, 365
        stops = 200 + rng.integers(-30, 31, size=n_years)  # rain-stop index per year
        pr = np.zeros((n_time, n_years), dtype="float64")
        for y, stop in enumerate(stops):
            pr[: int(stop), y] = 10.0
        pet = np.full((n_time, n_years), 5.0)

        out = season_phenology(pr, pet, 0, 300, n_time - 1, DEFAULT_ONSET, DEFAULT_CESSATION)
        eos = out["eos"]
        self.assertTrue(np.all(np.isfinite(eos)), f"a year failed to cease: {eos}")
        # Bucket is at the 100 mm cap when the rain stops (10 - 5 = +5 mm/day), then
        # drains 5 mm/day: empty at stop-1+20 = stop+19, the 5-day empty run ends at
        # stop+23 and cessation = stop+23-5+1 = stop+19.
        np.testing.assert_array_equal(eos, (stops + 19).astype("float32"))
        self.assertGreater(float(np.std(eos, ddof=1)), 3.0)

    def test_item5_permanently_wet_is_right_censored(self) -> None:
        """5. 8 mm/day rain vs 4 mm/day PET -> NaN cessation, RIGHT_CENSORED."""
        n_time = 200
        pr = np.full(n_time, 8.0)
        pet = np.full(n_time, 4.0)
        onset, _ = onset_index(pr, 0, 150, DEFAULT_ONSET)
        cess, status, at_floor = cessation_index(
            pr, pet, onset, n_time - 1, DEFAULT_CESSATION
        )
        # S gains 8 - 4 = +4 mm/day and is capped at 100 mm; it never reaches 0.
        self.assertTrue(np.isnan(_scalar(cess)))
        self.assertEqual(int(status), int(CessationStatus.RIGHT_CENSORED))
        self.assertFalse(bool(at_floor))

    def test_item6_clean_dry_down(self) -> None:
        """6. Rain stops day 100, PET 5, WHC 100 -> cessation ~120 (within 5 days)."""
        n_time = 200
        pr = np.zeros(n_time)
        pr[:100] = 10.0
        pet = np.full(n_time, 5.0)
        onset, _ = onset_index(pr, 0, 150, DEFAULT_ONSET)
        cess, status, at_floor = cessation_index(
            pr, pet, onset, n_time - 1, DEFAULT_CESSATION
        )
        # S = 100 mm (cap) at index 99; from index 100 it loses 5 mm/day, so
        # S = 100 - 5*(t-99) hits 0 at t = 119. The 5-day empty run ends at 123 and
        # cessation = 123 - 5 + 1 = 119, i.e. 120 +/- empty_persist_days.
        self.assertEqual(_scalar(cess), 119.0)
        self.assertLessEqual(abs(_scalar(cess) - 120.0), DEFAULT_CESSATION.empty_persist_days)
        self.assertEqual(int(status), int(CessationStatus.OK))
        self.assertFalse(bool(at_floor))


# ---------------------------------------------------------------------------
# DESIGN 3.10 acceptance items 7, 8
# ---------------------------------------------------------------------------
class TestAcceptanceCrossYearAndLgs(unittest.TestCase):
    """DESIGN section 3.10 items 7-8."""

    def test_item7_cross_year_mean_lands_mid_december(self) -> None:
        """7. Indices are days since planting start; mean(mid-Nov, mid-Jan) = mid-Dec."""
        origin = date(2025, 10, 1)  # index 0 = planting-window start
        n_time = 200
        pr = np.zeros((n_time, 2))
        # pixel 0: rain from 15 Nov 2025 (index 45); pixel 1: from 15 Jan 2026 (index 106)
        start_a = (date(2025, 11, 15) - origin).days
        start_b = (date(2026, 1, 15) - origin).days
        self.assertEqual((start_a, start_b), (45, 106))
        pr[start_a:, 0] = 10.0
        pr[start_b:, 1] = 10.0

        onset, status = onset_index(pr, 0, 180, DEFAULT_ONSET)
        # First full 20 mm window is the second rain day: W = 0 + 10 + 10 = 20 mm.
        np.testing.assert_array_equal(onset, np.array([46.0, 107.0], dtype="float32"))
        np.testing.assert_array_equal(status, np.array([0, 0], dtype="int8"))
        self.assertEqual(origin + timedelta(days=46), date(2025, 11, 16))  # mid-Nov
        self.assertEqual(origin + timedelta(days=107), date(2026, 1, 16))  # mid-Jan

        mean_idx = float(np.mean(onset))  # (46 + 107) / 2 = 76.5
        self.assertEqual(mean_idx, 76.5)
        mean_date = origin + timedelta(days=mean_idx)
        # 1 Oct 2025 + 76.5 days = 16 Dec 2025 12:00 -> mid-December.
        self.assertEqual(mean_date.date() if hasattr(mean_date, "date") else mean_date,
                         date(2025, 12, 16))

    def test_item8_lgs_equals_eos_minus_sos_exactly(self) -> None:
        """8. LGS == EOS - SOS exactly, elementwise, for every finite pixel."""
        rng = np.random.default_rng(808)
        n_time, n_pix = 300, 64
        pr = np.where(rng.random((n_time, n_pix)) < 0.3, rng.gamma(2.0, 6.0, (n_time, n_pix)), 0.0)
        pet = rng.uniform(3.0, 6.0, size=(n_time, n_pix))
        out = season_phenology(pr, pet, 5, 150, n_time - 1, DEFAULT_ONSET, DEFAULT_CESSATION)
        expected = (out["eos"] - out["sos"]).astype("float32")
        np.testing.assert_array_equal(out["lgs"], expected)
        finite = np.isfinite(out["lgs"])
        self.assertGreater(int(finite.sum()), 0)
        np.testing.assert_array_equal(
            out["lgs"][finite], out["eos"][finite] - out["sos"][finite]
        )


# ---------------------------------------------------------------------------
# _spell_lookahead exactness
# ---------------------------------------------------------------------------
class TestSpellLookahead(unittest.TestCase):
    """``_spell_lookahead`` must equal a brute-force nested loop over t and s."""

    @staticmethod
    def _brute(flag: np.ndarray, dry_spell_days: int, validation_days: int) -> np.ndarray:
        """Nested-loop reference for ``any(flag[t+dsd-1 .. t+vd-1])`` (clipped)."""
        n_time, n_pix = flag.shape
        out = np.zeros((n_time, n_pix), dtype=bool)
        for t in range(n_time):
            for s in range(t + dry_spell_days - 1, min(t + validation_days, n_time)):
                if s < 0:
                    continue
                out[t] |= flag[s]
        return out

    def test_matches_brute_force_over_parameter_grid(self) -> None:
        rng = np.random.default_rng(13)
        for n_time in (1, 2, 17, 60):
            flag = rng.random((n_time, 9)) < 0.25
            for dry_spell_days, validation_days in [
                (1, 1), (1, 5), (3, 10), (10, 30), (10, 10), (15, 45), (30, 10)
            ]:
                with self.subTest(n_time=n_time, dsd=dry_spell_days, vd=validation_days):
                    got = _spell_lookahead(flag, dry_spell_days, validation_days)
                    want = self._brute(flag, dry_spell_days, validation_days)
                    np.testing.assert_array_equal(got, want)

    def test_empty_window_is_false(self) -> None:
        """dry_spell_days-1 beyond validation_days leaves an empty window -> all False."""
        flag = np.ones((20, 3), dtype=bool)
        got = _spell_lookahead(flag, dry_spell_days=30, validation_days=10)
        self.assertFalse(bool(got.any()))


# ---------------------------------------------------------------------------
# 2-D vs 1-D oracle agreement
# ---------------------------------------------------------------------------
class TestOracleAgreement(unittest.TestCase):
    """Vectorised onset/cessation must equal the private 1-D oracles per pixel."""

    @staticmethod
    def _make_series(seed: int, n_time: int, n_pix: int, wet_lo: float, wet_hi: float):
        """Seeded rain/PET cubes with NaNs injected in both; no pixel is all-NaN."""
        rng = np.random.default_rng(seed)
        wet_p = rng.uniform(wet_lo, wet_hi, size=n_pix)
        pr = np.where(
            rng.random((n_time, n_pix)) < wet_p, rng.gamma(2.0, 6.0, size=(n_time, n_pix)), 0.0
        )
        pet = rng.uniform(2.0, 7.0, size=(n_time, n_pix))
        pr[rng.random((n_time, n_pix)) < 0.03] = np.nan
        pet[rng.random((n_time, n_pix)) < 0.03] = np.nan
        pr[0] = 0.0  # guarantee at least one finite rain day per pixel
        return pr, pet

    def test_agreement_across_parameter_sets_and_regimes(self) -> None:
        n_time, n_pix = 240, 250  # >= 200 pixels, per-pixel differing bounds below
        rng = np.random.default_rng(99)
        # per-pixel DIFFERING season bounds (arrays, not scalars)
        search_start = rng.integers(0, 40, size=n_pix).astype("float64")
        season_end = rng.integers(60, 180, size=n_pix).astype("float64")
        search_end = rng.integers(100, 300, size=n_pix).astype("float64")

        param_sets = [
            (OnsetParams(), CessationParams()),
            (
                OnsetParams(
                    precip_threshold=35.0,
                    window_days=5,
                    dry_spell_days=7,
                    dry_day_threshold=2.0,
                    validation_days=21,
                ),
                CessationParams(
                    soil_whc=60.0,
                    min_season_days=30,
                    empty_persist_days=3,
                    initial_storage=25.0,
                ),
            ),
            (
                OnsetParams(
                    precip_threshold=10.0,
                    window_days=1,
                    dry_spell_days=15,
                    dry_day_threshold=0.5,
                    validation_days=45,
                ),
                CessationParams(soil_whc=150.0, min_season_days=90, empty_persist_days=7),
            ),
        ]
        regimes = [("wet", 0.25, 0.60), ("dry", 0.02, 0.15)]

        seen_onset_status, seen_cess_status = set(), set()
        for regime, wet_lo, wet_hi in regimes:
            pr, pet = self._make_series(1000 + len(regime), n_time, n_pix, wet_lo, wet_hi)
            for k, (op, cp) in enumerate(param_sets):
                with self.subTest(regime=regime, params=k):
                    onset2d, status2d = onset_index(pr, search_start, season_end, op)
                    cess2d, cstatus2d, _ = cessation_index(
                        pr, pet, onset2d, search_end, cp
                    )
                    seen_onset_status.update(np.unique(status2d).tolist())
                    seen_cess_status.update(np.unique(cstatus2d).tolist())
                    for i in range(n_pix):
                        o1, so1 = _onset_index_1d(
                            pr[:, i],
                            season_end[i],
                            op.precip_threshold,
                            op.window_days,
                            op.dry_spell_days,
                            op.dry_day_threshold,
                            op.validation_days,
                            search_start_idx=search_start[i],
                        )
                        np.testing.assert_allclose(
                            float(onset2d[i]), o1, err_msg=f"onset pixel {i}"
                        )
                        self.assertEqual(
                            int(status2d[i]),
                            _ONSET_STATUS_FROM_STR[so1],
                            msg=f"onset status pixel {i}",
                        )
                        c1, sc1 = _cessation_index_1d(
                            pr[:, i],
                            pet[:, i],
                            onset2d[i],
                            search_end[i],
                            cp.soil_whc,
                            cp.min_season_days,
                            cp.empty_persist_days,
                            initial_storage=cp.initial_storage,
                        )
                        np.testing.assert_allclose(
                            float(cess2d[i]), c1, err_msg=f"cessation pixel {i}"
                        )
                        self.assertEqual(
                            int(cstatus2d[i]),
                            _CESSATION_STATUS_FROM_STR[sc1],
                            msg=f"cessation status pixel {i}",
                        )
        # the random regimes must actually exercise more than the happy path
        self.assertIn(int(OnsetStatus.OK), seen_onset_status)
        self.assertIn(int(OnsetStatus.NO_TRIGGER), seen_onset_status)
        self.assertIn(int(CessationStatus.OK), seen_cess_status)
        self.assertIn(int(CessationStatus.RIGHT_CENSORED), seen_cess_status)

    def test_pixel_shapes_are_preserved(self) -> None:
        """A (T, rows, cols) cube gives (rows, cols) outputs equal to the flat run."""
        rng = np.random.default_rng(5)
        n_time, rows, cols = 120, 7, 11
        pr = np.where(
            rng.random((n_time, rows, cols)) < 0.3,
            rng.gamma(2.0, 6.0, (n_time, rows, cols)),
            0.0,
        )
        pet = rng.uniform(3.0, 6.0, size=(n_time, rows, cols))
        start = rng.integers(0, 10, size=(rows, cols)).astype("float64")
        end = rng.integers(50, 100, size=(rows, cols)).astype("float64")
        onset3d, status3d = onset_index(pr, start, end, DEFAULT_ONSET)
        self.assertEqual(onset3d.shape, (rows, cols))
        onset2d, status2d = onset_index(
            pr.reshape(n_time, rows * cols), start.ravel(), end.ravel(), DEFAULT_ONSET
        )
        np.testing.assert_array_equal(onset3d.ravel(), onset2d)
        np.testing.assert_array_equal(status3d.ravel(), status2d)
        cess3d, _, _ = cessation_index(pr, pet, onset3d, n_time - 1, DEFAULT_CESSATION)
        self.assertEqual(cess3d.shape, (rows, cols))

    def test_all_nan_pixel_is_no_data_not_no_trigger(self) -> None:
        """Documented divergence from the oracle: all-NaN -> NO_DATA (DESIGN 3.3)."""
        pr = np.zeros((60, 2))
        pr[:, 1] = np.nan
        onset, status = onset_index(pr, 0, 50, DEFAULT_ONSET)
        self.assertEqual(int(status[1]), int(OnsetStatus.NO_DATA))
        self.assertTrue(np.isnan(float(onset[1])))
        # the 1-D oracle has no NO_DATA branch for an all-NaN (non-empty) series
        _, oracle_status = _onset_index_1d(
            pr[:, 1],
            50,
            DEFAULT_ONSET.precip_threshold,
            DEFAULT_ONSET.window_days,
            DEFAULT_ONSET.dry_spell_days,
            DEFAULT_ONSET.dry_day_threshold,
            DEFAULT_ONSET.validation_days,
        )
        self.assertEqual(oracle_status, "no_trigger")


# ---------------------------------------------------------------------------
# Monitor state machine
# ---------------------------------------------------------------------------
class TestSeasonStates(unittest.TestCase):
    """Every :class:`SeasonState` reachable from a hand-built rain series."""

    def test_before_window(self) -> None:
        """Search opens at index 50 but the as-of day is index 19."""
        out = onset_state(np.zeros(20), 50, 200, DEFAULT_ONSET)
        self.assertEqual(int(out["state"]), int(SeasonState.BEFORE_WINDOW))
        self.assertTrue(np.isnan(_scalar(out["onset_idx"])))
        self.assertTrue(np.isnan(_scalar(out["candidate_idx"])))

    def test_not_started(self) -> None:
        """Search open since index 0, no rain, so no candidate yet."""
        out = onset_state(np.zeros(20), 0, 200, DEFAULT_ONSET)
        self.assertEqual(int(out["state"]), int(SeasonState.NOT_STARTED))
        self.assertTrue(np.isnan(_scalar(out["candidate_idx"])))

    def test_false_start(self) -> None:
        """A candidate episode that a dry spell has already invalidated."""
        pr = np.zeros(35)
        pr[9] = 20.0
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        # triggers at 9, 10, 11 (W = 20, 20, 20 mm); indices 12..34 are dry, so
        # r[21] = 10 and spells end at 21..34, inside look-ahead [20, 40] of index 11.
        self.assertEqual(int(out["state"]), int(SeasonState.FALSE_START))
        self.assertEqual(_scalar(out["candidate_idx"]), 11.0)
        self.assertTrue(np.isnan(_scalar(out["onset_idx"])))
        self.assertTrue(np.isnan(_scalar(out["days_to_confirm"])))
        self.assertEqual(_scalar(out["days_since_candidate"]), 34.0 - 11.0)  # as-of 34

    def test_provisional_days_to_confirm(self) -> None:
        """Latest candidate still inside its 30-day validation window."""
        pr = np.full(20, 2.0)
        pr[:9] = 0.0
        pr[9] = 20.0
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        # triggers at 9 (0+0+20), 10 (0+20+2 = 22), 11 (20+2+2 = 24); W[12] = 6 < 20.
        # Latest candidate 11 has look-ahead 11 + 30 = 41 > T_obs = 20 -> pending.
        self.assertEqual(int(out["state"]), int(SeasonState.PROVISIONAL))
        self.assertEqual(_scalar(out["candidate_idx"]), 11.0)
        # days_to_confirm = candidate_idx + validation_days - T_obs = 11 + 30 - 20 = 21
        self.assertEqual(_scalar(out["days_to_confirm"]), 21.0)
        self.assertEqual(_scalar(out["days_since_candidate"]), 8.0)  # 19 - 11

    def test_confirmed_uses_first_confirmed_candidate(self) -> None:
        """Two confirmed episodes -> onset is the FIRST, not the latest."""
        pr = np.full(150, 2.0)
        pr[:9] = 0.0
        pr[9] = 20.0
        pr[60] = 20.0
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        # Both episodes have a full 30-day look-ahead inside T_obs = 150 and no day
        # after index 8 is dry (2 mm >= 1 mm), so both confirm; onset = first = 9.
        self.assertEqual(int(out["state"]), int(SeasonState.CONFIRMED))
        self.assertEqual(_scalar(out["onset_idx"]), 9.0)
        self.assertEqual(_scalar(out["candidate_idx"]), 62.0)  # latest trigger day
        self.assertTrue(np.isnan(_scalar(out["days_to_confirm"])))
        self.assertEqual(int(out["n_false_starts"]), 0)

    def test_no_onset_after_season_end_plus_validation(self) -> None:
        """T_obs-1 > season_end + validation_days with nothing confirmed."""
        out = onset_state(np.zeros(100), 0, 20, DEFAULT_ONSET)
        # as-of 99 > season_end 20 + validation_days 30 = 50
        self.assertEqual(int(out["state"]), int(SeasonState.NO_ONSET))

        pr = np.zeros(100)
        pr[9] = 20.0  # an invalidated candidate must not downgrade NO_ONSET
        out2 = onset_state(pr, 0, 20, DEFAULT_ONSET)
        self.assertEqual(int(out2["state"]), int(SeasonState.NO_ONSET))
        self.assertEqual(int(out2["n_false_starts"]), 1)

    def test_all_states_in_one_vectorised_call(self) -> None:
        """The six states co-exist across pixels of a single call."""
        n_time = 150
        pr = np.zeros((n_time, 6))
        search_start = np.array([200.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        season_end = np.array([300.0, 300.0, 300.0, 300.0, 300.0, 20.0])
        pr[:, 2] = 0.0
        pr[9, 2] = 20.0  # false start: invalidated by the long dry tail
        pr[9, 3] = 20.0  # episode 9..11, invalidated by the dry run that follows
        pr[125:, 3] = 20.0  # episode 125..149 is still pending at as-of 149
        pr[:, 4] = 2.0
        pr[:9, 4] = 0.0
        pr[9, 4] = 20.0  # confirmed
        out = onset_state(pr, search_start, season_end, DEFAULT_ONSET)
        expected = np.array(
            [
                int(SeasonState.BEFORE_WINDOW),
                int(SeasonState.NOT_STARTED),
                int(SeasonState.FALSE_START),
                int(SeasonState.PROVISIONAL),
                int(SeasonState.CONFIRMED),
                int(SeasonState.NO_ONSET),
            ],
            dtype="int8",
        )
        np.testing.assert_array_equal(out["state"], expected)

    def test_nodata_pixel_state_is_minus_one(self) -> None:
        out = onset_state(np.full(30, np.nan), 0, 200, DEFAULT_ONSET)
        self.assertEqual(int(out["state"]), -1)
        self.assertTrue(np.isnan(_scalar(out["onset_idx"])))


class TestOnsetStateExtras(unittest.TestCase):
    """The reported extras of :func:`onset_state` (DESIGN section 3.7)."""

    def test_trailing_rain_sums(self) -> None:
        """rain_10d / rain_30d are trailing sums at the as-of day; NaN counts 0 mm."""
        pr = np.arange(40, dtype="float64")  # 0, 1, 2, ..., 39 mm
        pr[35] = np.nan
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        # last 10 days = indices 30..39 = 30+31+32+33+34+0+36+37+38+39 = 310 mm
        self.assertEqual(_scalar(out["rain_10d"]), 310.0)
        # last 30 days = indices 10..39; sum(10..39) = (10+39)*30/2 = 735, minus 35 = 700
        self.assertEqual(_scalar(out["rain_30d"]), 700.0)

    def test_dry_run_now_and_nan_breaks_the_run(self) -> None:
        """dry_run_now = r[T_obs-1]; a NaN day is not dry and resets the counter."""
        pr = np.full(30, 5.0)
        pr[23:] = 0.0  # 7 dry days: indices 23..29
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        self.assertEqual(int(out["dry_run_now"]), 7)

        pr2 = pr.copy()
        pr2[26] = np.nan  # breaks the run: only indices 27..29 remain
        out2 = onset_state(pr2, 0, 200, DEFAULT_ONSET)
        self.assertEqual(int(out2["dry_run_now"]), 3)

    def test_n_false_starts_counts_episodes_not_days(self) -> None:
        """Two multi-day trigger episodes, both invalidated -> n_false_starts == 2."""
        pr = np.zeros(60)
        pr[9] = pr[10] = pr[11] = 20.0  # triggers at 9, 10, 11, 12, 13 -> ONE episode
        pr[40] = 20.0  # triggers at 40, 41, 42 -> a SECOND episode
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        self.assertEqual(int(out["n_false_starts"]), 2)
        self.assertEqual(int(out["state"]), int(SeasonState.FALSE_START))
        self.assertEqual(_scalar(out["candidate_idx"]), 42.0)

    def test_days_since_candidate(self) -> None:
        pr = np.zeros(35)
        pr[9] = 20.0
        out = onset_state(pr, 0, 200, DEFAULT_ONSET)
        # as-of = T_obs - 1 = 34; latest trigger = 11 -> 34 - 11 = 23
        self.assertEqual(_scalar(out["days_since_candidate"]), 23.0)

    def test_forecast_trigger_uses_the_concatenated_series(self) -> None:
        """fcst_trigger_idx needs the observed tail; it never changes the state."""
        obs = np.zeros(20)
        obs[18] = obs[19] = 8.0  # W[19] = 0 + 8 + 8 = 16 mm < 20 -> no observed trigger
        fcst = np.zeros(16)
        fcst[0] = 10.0
        base = onset_state(obs, 0, 200, DEFAULT_ONSET)
        with_fcst = onset_state(obs, 0, 200, DEFAULT_ONSET, fcst)
        # concatenated W[20] = obs[18] + obs[19] + fcst[0] = 8 + 8 + 10 = 26 >= 20 mm
        self.assertEqual(_scalar(with_fcst["fcst_trigger_idx"]), 20.0)
        # the forecast alone (10 mm on one day) would never reach the 20 mm threshold
        self.assertLess(fcst.sum(), DEFAULT_ONSET.precip_threshold * 2)
        self.assertEqual(int(with_fcst["state"]), int(base["state"]))
        self.assertEqual(int(with_fcst["state"]), int(SeasonState.NOT_STARTED))

    def test_forecast_absent_gives_nan(self) -> None:
        obs = np.zeros(20)
        obs[18] = obs[19] = 8.0
        out = onset_state(obs, 0, 200, DEFAULT_ONSET)
        self.assertTrue(np.isnan(_scalar(out["fcst_trigger_idx"])))

    def test_forecast_never_confirms_a_state(self) -> None:
        """A forecast that triggers cannot move PROVISIONAL/NOT_STARTED to CONFIRMED."""
        obs = np.full(20, 2.0)
        obs[:9] = 0.0
        obs[9] = 20.0
        fcst = np.full(16, 30.0)
        out = onset_state(obs, 0, 200, DEFAULT_ONSET, fcst)
        self.assertEqual(int(out["state"]), int(SeasonState.PROVISIONAL))
        self.assertTrue(np.isnan(_scalar(out["onset_idx"])))
        self.assertTrue(np.isfinite(_scalar(out["fcst_trigger_idx"])))

    def test_forecast_shape_mismatch_raises(self) -> None:
        obs = np.zeros((20, 3))
        with self.assertRaises(ValueError):
            onset_state(obs, 0, 200, DEFAULT_ONSET, np.zeros((16, 4)))


# ---------------------------------------------------------------------------
# Statuses, floor flag and NaN semantics
# ---------------------------------------------------------------------------
class TestStatusesAndFlags(unittest.TestCase):
    """Onset/cessation status codes and the ``eos_at_floor`` diagnostic."""

    def test_insufficient_data_vs_no_trigger(self) -> None:
        """A candidate without a full look-ahead is INSUFFICIENT_DATA, not NO_TRIGGER."""
        pr_short = np.full(20, 8.0)  # W = 24 mm >= 20 from index 2, but 2 + 30 > 20
        onset, status = onset_index(pr_short, 0, 19, DEFAULT_ONSET)
        self.assertTrue(np.isnan(_scalar(onset)))
        self.assertEqual(int(status), int(OnsetStatus.INSUFFICIENT_DATA))

        pr_weak = np.full(100, 2.0)  # W = 6 mm < 20 mm anywhere, and no dry day
        onset2, status2 = onset_index(pr_weak, 0, 90, DEFAULT_ONSET)
        self.assertTrue(np.isnan(_scalar(onset2)))
        self.assertEqual(int(status2), int(OnsetStatus.NO_TRIGGER))

    def test_no_data_for_all_nan_pixel(self) -> None:
        onset, status = onset_index(np.full(60, np.nan), 0, 50, DEFAULT_ONSET)
        self.assertTrue(np.isnan(_scalar(onset)))
        self.assertEqual(int(status), int(OnsetStatus.NO_DATA))

    def test_cessation_statuses(self) -> None:
        n_time = 200
        pr = np.zeros((n_time, 3))
        pet = np.full((n_time, 3), 5.0)
        onset = np.array([np.nan, 10.0, 0.0])
        search_end = np.array([n_time - 1.0, 10.0, n_time - 1.0])
        cess, status, _ = cessation_index(pr, pet, onset, search_end, DEFAULT_CESSATION)
        self.assertEqual(int(status[0]), int(CessationStatus.NO_ONSET))  # onset NaN
        self.assertEqual(int(status[1]), int(CessationStatus.NO_RANGE))  # end <= onset
        self.assertEqual(int(status[2]), int(CessationStatus.OK))
        self.assertTrue(np.isnan(float(cess[0])))
        self.assertTrue(np.isnan(float(cess[1])))

    def test_eos_at_floor_true_exactly_when_the_gate_binds(self) -> None:
        """eos_at_floor marks the minimum-season gate, and only that."""
        n_time = 200
        pet = np.full(n_time, 5.0)
        params = CessationParams(
            soil_whc=100.0, min_season_days=60, empty_persist_days=5, initial_storage=0.0
        )
        # (a) bucket empty from day one: the answer is pinned by the gate.
        pr_dry = np.zeros(n_time)
        cess_a, status_a, floor_a = cessation_index(pr_dry, pet, 0.0, n_time - 1, params)
        # earliest possible = onset + min_season_days - empty_persist_days + 1
        #                   = 0 + 60 - 5 + 1 = 56
        self.assertEqual(_scalar(cess_a), 56.0)
        self.assertEqual(int(status_a), int(CessationStatus.OK))
        self.assertTrue(bool(floor_a))

        # (b) same gate, but the bucket only empties much later: not at the floor.
        pr_wet = np.zeros(n_time)
        pr_wet[:100] = 10.0
        cess_b, status_b, floor_b = cessation_index(pr_wet, pet, 0.0, n_time - 1, params)
        # S caps at 100 mm, drains 5 mm/day from index 100 -> empty at 119,
        # run of 5 ends at 123, cessation = 123 - 5 + 1 = 119 > 56.
        self.assertEqual(_scalar(cess_b), 119.0)
        self.assertFalse(bool(floor_b))
        self.assertEqual(int(status_b), int(CessationStatus.OK))

    def test_nan_rain_breaks_a_dry_run_and_counts_zero_mm(self) -> None:
        """A NaN rain day is not dry (it resets r) and adds 0 mm to the window."""
        pr = np.concatenate([np.zeros(9), [20.0], np.zeros(15), np.full(65, 10.0)])
        onset_a, status_a = onset_index(pr, 0, 80, DEFAULT_ONSET)
        # 15 consecutive dry days (10..24) invalidate the candidate at index 9
        self.assertEqual(_scalar(onset_a), 26.0)
        self.assertEqual(int(status_a), int(OnsetStatus.OK))

        pr_nan = pr.copy()
        pr_nan[17] = np.nan  # splits the dry run into 7 + 7 days, both < 10
        onset_b, status_b = onset_index(pr_nan, 0, 80, DEFAULT_ONSET)
        self.assertEqual(_scalar(onset_b), 9.0)
        self.assertEqual(int(status_b), int(OnsetStatus.OK))
        # the NaN day itself contributes 0 mm: W[17] = pr[15] + pr[16] + 0 = 0 mm
        out = onset_state(pr_nan[:18], 0, 200, DEFAULT_ONSET)
        # trailing 10 days = indices 8..17 = 0 + 20 + 0*7 + NaN -> 20 mm: the NaN
        # day adds 0 mm, exactly as a real 0 mm day would.
        self.assertEqual(_scalar(out["rain_10d"]), 20.0)
        zeroed = pr_nan[:18].copy()
        zeroed[17] = 0.0
        self.assertEqual(
            _scalar(onset_state(zeroed, 0, 200, DEFAULT_ONSET)["rain_10d"]),
            _scalar(out["rain_10d"]),
        )
        self.assertEqual(int(out["dry_run_now"]), 0)  # index 17 is NaN -> not dry
        # ... whereas a real 0 mm day there would leave an 8-day run (indices 10..17)
        self.assertEqual(int(onset_state(zeroed, 0, 200, DEFAULT_ONSET)["dry_run_now"]), 8)

    def test_season_phenology_reports_first_candidate_and_false_starts(self) -> None:
        """first_candidate is the first trigger day, validated or not."""
        pr = np.concatenate([np.zeros(9), [20.0], np.zeros(15), np.full(65, 10.0)])
        out = season_phenology(pr, np.full(pr.size, 5.0), 0, 80, pr.size - 1)
        self.assertEqual(_scalar(out["first_candidate"]), 9.0)
        self.assertEqual(_scalar(out["sos"]), 26.0)
        # one candidate EPISODE (indices 9, 10, 11) ends before the onset at 26
        self.assertEqual(int(out["n_false_starts"]), 1)


# ---------------------------------------------------------------------------
# PET
# ---------------------------------------------------------------------------
class TestPet(unittest.TestCase):
    """:func:`hargreaves_pet` sanity and :func:`combine_pet` precedence."""

    def test_hand_computed_value_at_the_equator(self) -> None:
        """FAO-56 HG at lat 0, DOY 1, Tmin 15 / Tmax 25 degC."""
        got = _scalar(hargreaves_pet(np.array([15.0]), np.array([25.0]), np.array([1.0]), 0.0))
        # dr   = 1 + 0.033*cos(2*pi*1/365)            = 1.0329951
        # decl = 0.409*sin(2*pi*1/365 - 1.39)         = -0.4010081
        # ws   = arccos(-tan(0)*tan(decl)) = arccos(0) = pi/2
        # Ra   = (1440/pi)*0.0820*dr*(0 + cos(decl)*sin(pi/2)) = 35.746026 MJ m-2 d-1
        # ET0  = 0.0023*0.408*35.746026*(20 + 17.8)*sqrt(10)   = 4.0096602 mm/day
        self.assertAlmostEqual(got, 4.0096602, places=6)

    def test_positive_and_increasing_with_diurnal_range(self) -> None:
        """ET0 > 0 and grows with Tmax - Tmin at a fixed mean temperature."""
        doy = np.arange(1, 366, dtype="float64")
        tmean = 22.0
        narrow = hargreaves_pet(
            np.full(365, tmean - 2.0), np.full(365, tmean + 2.0), doy, 10.0
        )
        wide = hargreaves_pet(
            np.full(365, tmean - 8.0), np.full(365, tmean + 8.0), doy, 10.0
        )
        self.assertTrue(np.all(narrow > 0.0))
        self.assertTrue(np.all(wide > narrow))
        # sqrt(16)/sqrt(4) = 2 exactly, everything else in the product is identical
        np.testing.assert_allclose(wide, 2.0 * narrow, rtol=1e-12)

    def test_broadcasting_over_a_time_axis(self) -> None:
        """A (T,) doy vector broadcasts across a (T, rows, cols) cube and per-row lat."""
        n_time, rows, cols = 12, 4, 5
        doy = np.linspace(1, 350, n_time)
        tmin = np.full((n_time, rows, cols), 12.0)
        tmax = np.full((n_time, rows, cols), 28.0)
        lat = np.linspace(-20.0, 20.0, rows)
        pet = hargreaves_pet(tmin, tmax, doy, lat)
        self.assertEqual(pet.shape, (n_time, rows, cols))
        self.assertTrue(np.all(pet > 0.0))
        # every column of a row is the same latitude, so the row is constant
        for r in range(rows):
            np.testing.assert_allclose(
                pet[:, r, :], np.repeat(pet[:, r, :1], cols, axis=1), rtol=1e-12
            )
        # one pixel must equal the scalar call for the same inputs
        one = hargreaves_pet(np.full(n_time, 12.0), np.full(n_time, 28.0), doy, lat[2])
        np.testing.assert_allclose(pet[:, 2, 0], one, rtol=1e-12)

    def test_combine_pet_prefers_etref_and_fills_from_hargreaves(self) -> None:
        n_time = 10
        doy = np.arange(1, n_time + 1, dtype="float64")
        tmin = np.full(n_time, 12.0)
        tmax = np.full(n_time, 28.0)
        etref = np.full(n_time, 3.5)
        etref[3:6] = np.nan  # the stalled-source case
        out = combine_pet(etref, tmin, tmax, doy, 5.0)
        hg = hargreaves_pet(tmin, tmax, doy, 5.0)
        np.testing.assert_allclose(out[:3], 3.5)
        np.testing.assert_allclose(out[6:], 3.5)
        np.testing.assert_allclose(out[3:6], hg[3:6])
        self.assertTrue(np.all(np.isfinite(out)))

    def test_combine_pet_leaves_nan_when_no_fallback(self) -> None:
        etref = np.array([1.0, np.nan, 2.0])
        out = combine_pet(etref, None, None, None, None)
        self.assertTrue(np.isnan(out[1]))
        np.testing.assert_allclose(out[[0, 2]], [1.0, 2.0])

    def test_combine_pet_leaves_nan_when_hargreaves_is_nan(self) -> None:
        etref = np.array([1.0, np.nan, 2.0])
        tmin = np.array([10.0, np.nan, 10.0])
        tmax = np.array([20.0, np.nan, 20.0])
        out = combine_pet(etref, tmin, tmax, np.array([1.0, 2.0, 3.0]), 0.0)
        self.assertTrue(np.isnan(out[1]))


# ---------------------------------------------------------------------------
# Climatology helpers
# ---------------------------------------------------------------------------
class TestClimatology(unittest.TestCase):
    """DESIGN section 3.8 statistics over a (Y, ...) stack of yearly onset indices."""

    def test_onset_climatology_min_valid_years_masking(self) -> None:
        # pixel 0: 3 valid years; pixel 1: 5 valid years
        stack = np.array(
            [
                [10.0, 1.0],
                [np.nan, 2.0],
                [20.0, 3.0],
                [np.nan, 4.0],
                [30.0, 5.0],
            ]
        )
        out = onset_climatology(stack, min_valid_years=4)
        np.testing.assert_array_equal(out["n_valid"], np.array([3, 5], dtype="int16"))
        self.assertTrue(np.isnan(float(out["median"][0])))  # 3 < 4 -> masked
        self.assertTrue(np.isnan(float(out["p25"][0])))
        self.assertTrue(np.isnan(float(out["std"][0])))
        # pixel 1: [1,2,3,4,5] -> median 3, p25 2, p75 4,
        # std(ddof=1) = sqrt(((2^2)+(1^2)+0+(1^2)+(2^2))/4) = sqrt(10/4) = 1.5811388
        self.assertAlmostEqual(float(out["median"][1]), 3.0, places=6)
        self.assertAlmostEqual(float(out["p25"][1]), 2.0, places=6)
        self.assertAlmostEqual(float(out["p75"][1]), 4.0, places=6)
        self.assertAlmostEqual(float(out["std"][1]), 1.5811388, places=6)
        # frac_no_onset = 1 - n_valid / Y = 1 - 3/5 = 0.4 and 1 - 5/5 = 0.0
        np.testing.assert_allclose(out["frac_no_onset"], [0.4, 0.0], rtol=1e-6)

    def test_onset_climatology_needs_two_years_for_std(self) -> None:
        stack = np.array([[5.0], [np.nan], [np.nan]])
        out = onset_climatology(stack, min_valid_years=1)
        self.assertEqual(int(out["n_valid"][0]), 1)
        self.assertAlmostEqual(float(out["median"][0]), 5.0, places=6)
        self.assertTrue(np.isnan(float(out["std"][0])))  # ddof=1 needs n >= 2

    def test_conditional_onset_probability_hand_computed(self) -> None:
        """P(d < onset <= d + horizon | onset > d or never) on a 6-year stack."""
        stack = np.array([10.0, 20.0, 30.0, np.nan, 45.0, 5.0])  # one pixel, 6 years
        p = conditional_onset_probability(stack, 15.0, 20, min_years=1)
        # onset > 15      -> years 20, 30, 45                    -> denominator adds 3
        # onset is NaN    -> 1 year                              -> denominator = 4
        # 15 < onset <= 35 -> years 20, 30                       -> numerator   = 2
        # P = 2 / 4 = 0.5
        self.assertAlmostEqual(_scalar(p), 0.5, places=6)

    def test_conditional_onset_probability_min_years_and_nan_d(self) -> None:
        stack = np.array([[10.0, 10.0], [20.0, np.nan], [30.0, 30.0]])
        p = conditional_onset_probability(stack, np.array([5.0, np.nan]), 30, min_years=3)
        # pixel 0 denominator = years with onset > 5 = 3 >= min_years -> defined,
        #   numerator = 5 < onset <= 35 = 3 -> 1.0
        self.assertAlmostEqual(float(p[0]), 1.0, places=6)
        self.assertTrue(np.isnan(float(p[1])))  # d is NaN
        p2 = conditional_onset_probability(stack[:, :1], 5.0, 30, min_years=4)
        self.assertTrue(np.isnan(_scalar(p2)))  # denominator 3 < min_years 4

    def test_onset_percentile_hand_computed(self) -> None:
        stack = np.array([10.0, 20.0, 30.0, np.nan, 45.0, 5.0])
        # valid years = [10, 20, 30, 45, 5] -> n = 5; onset <= 25 -> 10, 20, 5 -> 3
        # share = 3 / 5 = 0.6
        self.assertAlmostEqual(_scalar(onset_percentile(stack, 25.0)), 0.6, places=6)
        # value below every year -> 0.0; above every year -> 1.0
        self.assertAlmostEqual(_scalar(onset_percentile(stack, 0.0)), 0.0, places=6)
        self.assertAlmostEqual(_scalar(onset_percentile(stack, 100.0)), 1.0, places=6)

    def test_onset_percentile_nan_value_and_min_valid_years(self) -> None:
        stack = np.array([[10.0, np.nan], [20.0, np.nan]])
        share = onset_percentile(stack, np.array([15.0, 15.0]), min_valid_years=1)
        self.assertAlmostEqual(float(share[0]), 0.5, places=6)  # 1 of 2 years <= 15
        self.assertTrue(np.isnan(float(share[1])))  # no valid years
        self.assertTrue(np.isnan(_scalar(onset_percentile(stack[:, :1], np.nan))))


# ---------------------------------------------------------------------------
# Performance sanity
# ---------------------------------------------------------------------------
class TestPerformance(unittest.TestCase):
    """A realistic window must run in seconds, not minutes."""

    def test_season_phenology_on_400x200x200(self) -> None:
        rng = np.random.default_rng(2026)
        n_time, rows, cols = 400, 200, 200
        pr = np.where(
            rng.random((n_time, rows, cols)) < 0.35,
            rng.gamma(2.0, 5.0, size=(n_time, rows, cols)),
            0.0,
        ).astype("float32")
        pet = rng.uniform(3.0, 6.0, size=(n_time, rows, cols)).astype("float32")
        started = time.perf_counter()
        out = season_phenology(pr, pet, 10, 200, n_time - 1, DEFAULT_ONSET, DEFAULT_CESSATION)
        elapsed = time.perf_counter() - started
        print(f"season_phenology T={n_time} {rows}x{cols} took {elapsed:.2f} s")
        self.assertEqual(out["sos"].shape, (rows, cols))
        self.assertEqual(out["sos"].dtype, np.dtype("float32"))
        self.assertEqual(out["sos_status"].dtype, np.dtype("int8"))
        self.assertEqual(out["n_false_starts"].dtype, np.dtype("int16"))
        self.assertEqual(out["eos_at_floor"].dtype, np.dtype("bool"))
        self.assertTrue(np.isfinite(out["sos"]).any())
        self.assertLess(elapsed, 60.0, f"season_phenology took {elapsed:.1f} s")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
