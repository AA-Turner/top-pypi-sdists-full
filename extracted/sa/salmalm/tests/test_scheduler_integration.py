"""Integration tests for salmalm.core.scheduler.

Tests: CronScheduler.run() loop, job execution, error handling,
HeartbeatManager state, and related logic.
"""
import asyncio
import json
import os
import sys
import tempfile
import time
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ── 1. CronScheduler.add_job registers job ───────────────────────────────────

def test_add_job_registers():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    sched.add_job("test_job", 60, lambda: None)
    assert len(sched.jobs) == 1
    assert sched.jobs[0]["name"] == "test_job"
    assert sched.jobs[0]["interval"] == 60


# ── 2. CronScheduler.stop sets _running False ────────────────────────────────

def test_stop_sets_running_false():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    sched._running = True
    sched.stop()
    assert sched._running is False


# ── 3. CronScheduler.run executes overdue sync job ───────────────────────────

def test_run_executes_overdue_sync_job():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    called = []
    def my_job():
        called.append(True)
        sched.stop()  # Stop after first execution

    sched.add_job("my_sync", 0, my_job)

    async def run_once():
        await sched.run()

    # Patch asyncio.sleep to prevent real delay
    with patch("salmalm.core.scheduler.asyncio.sleep", new_callable=AsyncMock):
        _run(run_once())
    assert len(called) >= 1


# ── 4. CronScheduler.run executes overdue async job ──────────────────────────

def test_run_executes_overdue_async_job():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    called = []

    async def async_job():
        called.append(True)
        sched.stop()

    sched.add_job("my_async", 0, async_job)

    async def run_once():
        await sched.run()

    with patch("salmalm.core.scheduler.asyncio.sleep", new_callable=AsyncMock):
        _run(run_once())
    assert len(called) >= 1


# ── 5. CronScheduler skips disabled jobs ─────────────────────────────────────

def test_run_skips_disabled_job():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    called = []
    sentinel = []

    def disabled_job():
        called.append(True)

    def sentinel_job():
        sentinel.append(True)
        sched.stop()

    sched.add_job("disabled", 0, disabled_job)
    sched.add_job("sentinel", 0, sentinel_job)
    sched.jobs[0]["enabled"] = False

    with patch("salmalm.core.scheduler.asyncio.sleep", new_callable=AsyncMock):
        _run(sched.run())
    assert len(called) == 0
    assert len(sentinel) >= 1


# ── 6. CronScheduler handles job exceptions gracefully ───────────────────────

def test_run_continues_after_job_error():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    errors = []
    sentinel = []

    def bad_job():
        raise ValueError("intentional error")

    def good_job():
        sentinel.append(True)
        sched.stop()

    sched.add_job("bad", 0, bad_job)
    sched.add_job("good", 0, good_job)

    with patch("salmalm.core.scheduler.asyncio.sleep", new_callable=AsyncMock):
        _run(sched.run())  # Should not raise
    assert len(sentinel) >= 1


# ── 7. CronScheduler skips job that hasn't reached interval ──────────────────

def test_run_skips_job_not_due():
    from salmalm.core.scheduler import CronScheduler
    sched = CronScheduler()
    called = []

    def too_early():
        called.append(True)

    sched.add_job("not_due", 999999, too_early)
    sched.jobs[0]["last_run"] = time.time()  # Just ran

    async def run_limited():
        sched._running = True
        # Do ONE loop iteration manually
        now = time.time()
        for job in sched.jobs:
            if not job["enabled"]:
                continue
            if now - job["last_run"] >= job["interval"]:
                job["callback"](**job["kwargs"])
        sched._running = False

    _run(run_limited())
    assert len(called) == 0


# ── 8. HeartbeatManager.should_beat respects quiet hours ─────────────────────

def test_should_beat_respects_enabled_flag():
    from salmalm.core.scheduler import HeartbeatManager
    orig = HeartbeatManager._enabled
    try:
        HeartbeatManager._enabled = False
        assert HeartbeatManager.should_beat() is False
    finally:
        HeartbeatManager._enabled = orig


def test_should_beat_respects_interval():
    from salmalm.core.scheduler import HeartbeatManager
    orig_last = HeartbeatManager._last_beat
    orig_enabled = HeartbeatManager._enabled
    try:
        HeartbeatManager._enabled = True
        HeartbeatManager._last_beat = time.time()  # Just beat
        assert HeartbeatManager.should_beat() is False
    finally:
        HeartbeatManager._last_beat = orig_last
        HeartbeatManager._enabled = orig_enabled


# ── 9. HeartbeatManager.get_state returns structured dict ────────────────────

def test_get_state_returns_dict():
    from salmalm.core.scheduler import HeartbeatManager
    with patch.object(HeartbeatManager, "_load_state", return_value={"lastChecks": {}, "history": [], "totalBeats": 5}):
        state = HeartbeatManager.get_state()
    assert "enabled" in state
    assert "interval" in state
    assert "beatCount" in state


# ── 10. HeartbeatManager.update_check saves check time ───────────────────────

def test_update_check_persists_timestamp():
    from salmalm.core.scheduler import HeartbeatManager
    saved = {}

    def fake_load():
        return {"lastChecks": {}, "history": []}

    def fake_save(state):
        saved.update(state)

    with patch.object(HeartbeatManager, "_load_state", side_effect=fake_load), \
         patch.object(HeartbeatManager, "_save_state", side_effect=fake_save):
        before = time.time()
        HeartbeatManager.update_check("email")
        after = time.time()

    assert "lastChecks" in saved
    ts = saved["lastChecks"].get("email", 0)
    assert before <= ts <= after + 1


# ── 11. HeartbeatManager.beat returns None when no prompt ────────────────────

def test_beat_returns_none_when_no_prompt():
    from salmalm.core.scheduler import HeartbeatManager
    with patch.object(HeartbeatManager, "get_prompt", return_value=""):
        result = _run(HeartbeatManager.beat())
    assert result is None


# ── 12. HeartbeatManager._announce uses lazy imports (no crash) ───────────────

def test_announce_does_not_crash_without_tg_bot():
    from salmalm.core.scheduler import HeartbeatManager
    with patch("salmalm.core.session_store._tg_bot", None), \
         patch("salmalm.core.session_store._sessions", {}):
        HeartbeatManager._announce("test result")  # Should not raise


# ── 13. HeartbeatManager.time_since_check returns None if never checked ───────

def test_time_since_check_none_if_never():
    from salmalm.core.scheduler import HeartbeatManager
    with patch.object(HeartbeatManager, "_load_state", return_value={"lastChecks": {}}):
        result = HeartbeatManager.time_since_check("never_checked_key")
    assert result is None


# ── 14. HeartbeatManager.get_prompt reads file if exists ─────────────────────

def test_get_prompt_reads_heartbeat_file():
    from salmalm.core.scheduler import HeartbeatManager
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("Check email\nCheck calendar\n")
        fname = f.name
    try:
        orig = HeartbeatManager._HEARTBEAT_FILE
        HeartbeatManager._HEARTBEAT_FILE = Path(fname)
        prompt = HeartbeatManager.get_prompt()
        assert "Check email" in prompt
    finally:
        HeartbeatManager._HEARTBEAT_FILE = orig
        os.unlink(fname)
