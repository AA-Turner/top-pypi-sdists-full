import json
import tempfile
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from abstra_internals.services.web_editor_heartbeat import WebEditorHeartbeat


class FakeClock:
    def __init__(self, start: datetime):
        self._now = start
        self._lock = threading.Lock()

    def __call__(self) -> datetime:
        with self._lock:
            return self._now

    def advance(self, delta: timedelta) -> None:
        with self._lock:
            self._now += delta


def _make_heartbeat(
    tmp: Path,
    *,
    clock=None,
    interval=timedelta(milliseconds=20),
    staleness_threshold=timedelta(days=3),
) -> WebEditorHeartbeat:
    return WebEditorHeartbeat(
        path=tmp / "heartbeat.json",
        interval=interval,
        staleness_threshold=staleness_threshold,
        clock=clock or (lambda: datetime.now(timezone.utc)),
    )


class WebEditorHeartbeatTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_dir.name)

    def tearDown(self):
        self._tmp_dir.cleanup()

    def test_missing_file_is_treated_as_fresh(self):
        hb = _make_heartbeat(self.tmp)
        self.assertFalse(hb.path.exists())
        self.assertFalse(hb.is_stale())

    def test_corrupted_file_is_treated_as_fresh_and_discarded(self):
        hb = _make_heartbeat(self.tmp)
        hb.path.parent.mkdir(parents=True, exist_ok=True)
        hb.path.write_text("not-json{{{", encoding="utf-8")
        self.assertFalse(hb.is_stale())
        self.assertFalse(
            hb.path.exists(),
            "corrupted heartbeat should be deleted to avoid log spam on subsequent reads",
        )

    def test_file_without_updated_at_is_treated_as_fresh_and_discarded(self):
        hb = _make_heartbeat(self.tmp)
        hb.path.parent.mkdir(parents=True, exist_ok=True)
        hb.path.write_text(json.dumps({"foo": "bar"}), encoding="utf-8")
        self.assertFalse(hb.is_stale())
        self.assertFalse(
            hb.path.exists(),
            "heartbeat with missing 'updated_at' should be discarded",
        )

    def test_fresh_heartbeat_is_not_stale(self):
        clock = FakeClock(datetime(2026, 1, 1, tzinfo=timezone.utc))
        hb = _make_heartbeat(
            self.tmp, clock=clock, staleness_threshold=timedelta(days=3)
        )
        hb.update()
        clock.advance(timedelta(days=2, hours=23))
        self.assertFalse(hb.is_stale())

    def test_old_heartbeat_is_stale(self):
        clock = FakeClock(datetime(2026, 1, 1, tzinfo=timezone.utc))
        hb = _make_heartbeat(
            self.tmp, clock=clock, staleness_threshold=timedelta(days=3)
        )
        hb.update()
        clock.advance(timedelta(days=3, seconds=1))
        self.assertTrue(hb.is_stale())

    def test_naive_iso_timestamp_is_assumed_utc(self):
        hb = _make_heartbeat(self.tmp)
        hb.path.parent.mkdir(parents=True, exist_ok=True)
        hb.path.write_text(
            json.dumps({"updated_at": "2026-01-01T00:00:00"}),
            encoding="utf-8",
        )
        self.assertTrue(hb.is_stale())

    def test_update_writes_valid_json_with_updated_at(self):
        clock = FakeClock(datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc))
        hb = _make_heartbeat(self.tmp, clock=clock)

        hb.update()

        data = json.loads(hb.path.read_text(encoding="utf-8"))
        self.assertEqual(data["updated_at"], "2026-04-30T12:00:00+00:00")

    def test_update_is_atomic_no_tmp_leftover(self):
        hb = _make_heartbeat(self.tmp)
        hb.update()
        leftovers = list(hb.path.parent.glob("*.tmp"))
        self.assertEqual(leftovers, [])

    def test_update_creates_parent_dir(self):
        nested = self.tmp / "deeply" / "nested" / "dir"
        hb = WebEditorHeartbeat(
            path=nested / "heartbeat.json",
            interval=timedelta(seconds=1),
            staleness_threshold=timedelta(days=1),
        )
        hb.update()
        self.assertTrue(hb.path.exists())

    def test_start_writes_first_heartbeat_quickly(self):
        hb = _make_heartbeat(self.tmp, interval=timedelta(seconds=10))
        hb.start()
        try:
            for _ in range(50):
                if hb.path.exists():
                    break
                time.sleep(0.02)
            self.assertTrue(hb.path.exists())
        finally:
            hb.stop()

    def test_stop_unblocks_long_interval_quickly(self):
        hb = _make_heartbeat(self.tmp, interval=timedelta(seconds=60))
        hb.start()
        for _ in range(50):
            if hb.path.exists():
                break
            time.sleep(0.02)
        started = time.monotonic()
        hb.stop(timeout=2.0)
        elapsed = time.monotonic() - started
        self.assertLess(elapsed, 1.0)

    def test_double_start_is_idempotent(self):
        hb = _make_heartbeat(self.tmp, interval=timedelta(seconds=60))
        try:
            hb.start()
            first_thread = hb._thread
            hb.start()
            self.assertIs(hb._thread, first_thread)
        finally:
            hb.stop()

    def test_stop_without_start_is_safe(self):
        hb = _make_heartbeat(self.tmp)
        hb.stop()
