"""Tests for the editor stall watchdog.

The batching logic is driven synchronously through _tick() with a fake
clock (no real sleeps); thread lifecycle is exercised for real with a
short interval.
"""

import unittest
from typing import Any, Dict, List, Tuple
from unittest.mock import patch

from abstra_internals.environment import _float_env
from abstra_internals.services.editor_stall_watchdog import (
    MAX_REPORTED_STALLS,
    EditorStallWatchdog,
)

INTERVAL = 1.0
THRESHOLD = 2.0
BATCH_WINDOW = 60.0


class StallBatchingTest(unittest.TestCase):
    def setUp(self):
        self.events: List[Tuple[str, Dict[str, Any]]] = []
        self.watchdog = EditorStallWatchdog(
            interval_seconds=INTERVAL,
            threshold_seconds=THRESHOLD,
            batch_window_seconds=BATCH_WINDOW,
            emit=lambda msg, attrs: self.events.append((msg, attrs)),
        )
        self.watchdog._last_wake = 0.0

    def _stall_tick(self, stall_seconds: float) -> None:
        """Simulate a tick that woke `stall_seconds` late."""
        self.watchdog._tick(self.watchdog._last_wake + INTERVAL + stall_seconds)

    def _quiet_tick(self) -> None:
        self.watchdog._tick(self.watchdog._last_wake + INTERVAL)

    def _summaries(self) -> List[Dict[str, Any]]:
        return [a for _, a in self.events if a["stage"] == "editor.stall"]

    def _markers(self) -> List[Dict[str, Any]]:
        return [a for _, a in self.events if a["stage"] == "editor.stall_started"]

    def test_on_time_wakeups_emit_nothing(self):
        self._quiet_tick()
        self._quiet_tick()
        self.assertEqual(self.events, [])

    def test_delay_below_threshold_emits_nothing(self):
        self._stall_tick(THRESHOLD - 0.1)
        self._quiet_tick()
        self.assertEqual(self.events, [])

    def test_first_stall_emits_live_marker_immediately(self):
        self._stall_tick(27.5)
        self.assertEqual(self._summaries(), [])  # episode may still be going
        markers = self._markers()
        self.assertEqual(len(markers), 1)
        self.assertAlmostEqual(markers[0]["stallSeconds"], 27.5)
        self.assertEqual(markers[0]["thresholdSeconds"], THRESHOLD)

    def test_isolated_stall_emits_marker_then_summary(self):
        self._stall_tick(27.5)
        self._quiet_tick()

        self.assertEqual(len(self.events), 2)
        first_attrs = self.events[0][1]
        self.assertEqual(first_attrs["stage"], "editor.stall_started")

        summaries = self._summaries()
        self.assertEqual(len(summaries), 1)
        attrs = summaries[0]
        self.assertEqual(attrs["stallCount"], 1)
        self.assertEqual(attrs["stallsSeconds"], [27.5])
        self.assertAlmostEqual(attrs["stallTotalSeconds"], 27.5)
        self.assertAlmostEqual(attrs["stallMaxSeconds"], 27.5)
        self.assertEqual(attrs["thresholdSeconds"], THRESHOLD)

    def test_burst_emits_single_marker_and_batches_every_duration(self):
        self._stall_tick(3.0)
        self._stall_tick(5.2)
        self._stall_tick(8.0)
        self.assertEqual(len(self._markers()), 1)  # only the episode opening
        self.assertEqual(self._summaries(), [])

        self._quiet_tick()
        summaries = self._summaries()
        self.assertEqual(len(summaries), 1)
        attrs = summaries[0]
        self.assertEqual(attrs["stallCount"], 3)
        self.assertEqual(attrs["stallsSeconds"], [3.0, 5.2, 8.0])
        self.assertAlmostEqual(attrs["stallTotalSeconds"], 16.2)
        self.assertAlmostEqual(attrs["stallMaxSeconds"], 8.0)

    def test_continuous_burst_flushes_when_window_expires(self):
        # 2.5s stalls back to back: each tick advances 3.5s (interval +
        # stall), never a quiet tick. The window must force a flush.
        ticks = 0
        while not self._summaries() and ticks < 100:
            self._stall_tick(2.5)
            ticks += 1
        summaries = self._summaries()
        self.assertEqual(len(summaries), 1)
        attrs = summaries[0]
        # Window is 60s and each stall consumes 3.5s of it.
        self.assertGreaterEqual(attrs["episodeSeconds"], BATCH_WINDOW)
        self.assertEqual(attrs["stallCount"], ticks)
        self.assertAlmostEqual(attrs["stallTotalSeconds"], 2.5 * ticks)

        # The next batch starts fresh, with a new live marker.
        self._stall_tick(4.0)
        self.assertEqual(len(self._markers()), 2)
        self._quiet_tick()
        self.assertEqual(len(self._summaries()), 2)
        self.assertEqual(self._summaries()[1]["stallsSeconds"], [4.0])

    def test_episode_duration_covers_first_stall_start_to_flush(self):
        self._stall_tick(10.0)
        self._quiet_tick()
        attrs = self._summaries()[0]
        # Episode starts when the first stall began (wake time minus the
        # stall) and ends at the flushing tick, one interval later.
        self.assertAlmostEqual(attrs["episodeSeconds"], 10.0 + INTERVAL)

    def test_reported_durations_are_capped_but_count_is_exact(self):
        watchdog = EditorStallWatchdog(
            interval_seconds=INTERVAL,
            threshold_seconds=THRESHOLD,
            batch_window_seconds=10_000.0,
            emit=lambda msg, attrs: self.events.append((msg, attrs)),
        )
        watchdog._last_wake = 0.0
        for _ in range(MAX_REPORTED_STALLS + 5):
            watchdog._tick(watchdog._last_wake + INTERVAL + 2.5)
        watchdog._tick(watchdog._last_wake + INTERVAL)

        summaries = self._summaries()
        self.assertEqual(len(summaries), 1)
        attrs = summaries[0]
        self.assertEqual(attrs["stallCount"], MAX_REPORTED_STALLS + 5)
        self.assertEqual(len(attrs["stallsSeconds"]), MAX_REPORTED_STALLS)
        self.assertAlmostEqual(
            attrs["stallTotalSeconds"], 2.5 * (MAX_REPORTED_STALLS + 5)
        )

    def test_stop_flushes_pending_batch(self):
        self._stall_tick(6.0)
        self.assertEqual(self._summaries(), [])

        self.watchdog.stop(timeout=0.1)
        summaries = self._summaries()
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0]["stallsSeconds"], [6.0])

    def test_stop_without_pending_batch_emits_nothing(self):
        self._quiet_tick()
        self.watchdog.stop(timeout=0.1)
        self.assertEqual(self.events, [])

    def test_emission_error_does_not_break_next_ticks(self):
        def flaky_emit(msg, attrs):
            self.events.append((msg, attrs))
            raise RuntimeError("boom")

        self.watchdog._emit = flaky_emit
        self._stall_tick(6.0)  # marker raises inside, swallowed
        self._quiet_tick()  # flush raises inside, swallowed, batch reset
        self._stall_tick(3.0)
        self._quiet_tick()
        self.assertEqual(len(self._markers()), 2)
        summaries = self._summaries()
        self.assertEqual(len(summaries), 2)
        self.assertEqual(summaries[1]["stallsSeconds"], [3.0])


class FloatEnvParsingTest(unittest.TestCase):
    """environment.py is imported by every abstra entrypoint: a malformed
    watchdog knob must never crash the boot."""

    def _parse(self, raw: str) -> float:
        with patch.dict("os.environ", {"X_TEST_KNOB": raw}):
            return _float_env("X_TEST_KNOB", default=0.5, minimum=0.25)

    def test_unset_returns_default(self):
        self.assertEqual(
            _float_env("X_TEST_KNOB_UNSET", default=0.5, minimum=0.25), 0.5
        )

    def test_valid_value_is_used(self):
        self.assertEqual(self._parse("3.5"), 3.5)

    def test_empty_string_falls_back_to_default(self):
        self.assertEqual(self._parse(""), 0.5)

    def test_garbage_falls_back_to_default(self):
        self.assertEqual(self._parse("fast"), 0.5)

    def test_zero_and_negative_clamp_to_minimum(self):
        self.assertEqual(self._parse("0"), 0.25)
        self.assertEqual(self._parse("-1"), 0.25)

    def test_nan_clamps_to_minimum(self):
        self.assertEqual(self._parse("nan"), 0.25)


class ThreadLifecycleTest(unittest.TestCase):
    def test_start_and_stop_terminate_thread_quickly(self):
        events: List[Tuple[str, Dict[str, Any]]] = []
        # Real thread + `events == []` assertion: the threshold must be far
        # above anything a loaded CI runner can produce as a genuine
        # scheduling delay, or this test gets flaky.
        watchdog = EditorStallWatchdog(
            interval_seconds=0.05,
            threshold_seconds=60.0,
            emit=lambda msg, attrs: events.append((msg, attrs)),
        )
        watchdog.start()
        thread = watchdog._thread
        assert thread is not None
        self.assertTrue(thread.is_alive())

        watchdog.stop(timeout=2.0)
        self.assertFalse(thread.is_alive())
        self.assertIsNone(watchdog._thread)
        self.assertEqual(events, [])

    def test_start_is_idempotent(self):
        watchdog = EditorStallWatchdog(interval_seconds=0.05, threshold_seconds=60.0)
        watchdog.start()
        thread = watchdog._thread
        watchdog.start()
        self.assertIs(watchdog._thread, thread)
        watchdog.stop(timeout=2.0)


if __name__ == "__main__":
    unittest.main()
