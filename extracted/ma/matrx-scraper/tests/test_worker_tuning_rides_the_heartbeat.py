"""The worker's tuning comes from the control plane's settings, never from its environment (2026-11-20)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from matrx_scraper.cloud_browser.worker import machine_browsers, models, runtime

SRC = Path(runtime.__file__).parent


def test_the_worker_reads_no_tuning_environment_variable() -> None:
    for name in ("runtime.py", "server.py", "machine_browsers.py"):
        text = (SRC / name).read_text()
        for var in ("BROWSER_WORKER_MAX_BROWSERS", "BROWSER_WORKER_LEASE_WATCHDOG_GRACE_SECONDS", "BROWSER_WORKER_LEFTOVER_CHROME_GRACE_SECONDS"):
            assert f'environ.get("{var}"' not in text, (name, var)


def test_the_heartbeat_carries_the_two_values_and_bounds_them() -> None:
    fields = models.HeartbeatRequest.model_fields
    assert "lease_watchdog_grace_seconds" in fields and "leftover_chrome_grace_seconds" in fields
    with pytest.raises(ValidationError):
        models.HeartbeatRequest.model_validate({"lease_watchdog_grace_seconds": 0})


def test_the_ceiling_is_the_settings_own_top() -> None:
    assert machine_browsers.DEFAULT_MAX_BROWSERS == 16


def test_a_sent_grace_replaces_the_builtin_one() -> None:
    worker = runtime.BrowserWorker.__new__(runtime.BrowserWorker)
    worker._terminating = False
    worker.health = "healthy"
    now = datetime.now(UTC)
    worker._lease_expires_at = now - timedelta(seconds=10)
    worker._watchdog_grace_s = None
    assert worker._lease_watchdog_should_fire(now) is False  # inside the built-in 90 s
    worker._watchdog_grace_s = 5.0
    assert worker._lease_watchdog_should_fire(now) is True  # the control plane's 5 s


def test_a_fresh_worker_holds_no_tuning_until_a_heartbeat_sends_it() -> None:
    assert runtime.LEASE_WATCHDOG_GRACE_SECONDS == 90.0
    assert runtime.LEFTOVER_CHROME_GRACE_SECONDS == 3.0
