"""/files-service/ready must answer "not ready" in bounded time when the database stops answering.

2026-09-25: this probe queued behind a wedged matrx-orm pool lock for 4.5 hours
while /files-service/health answered 200, so no monitor alarmed.
"""

from __future__ import annotations

import asyncio
import time

import pytest

from matrx_files.db import readiness


@pytest.mark.asyncio
async def test_readiness_reports_not_ready_within_its_timeout_when_the_database_hangs(monkeypatch):
    import matrx_files.db as db_pkg
    from matrx_files.db import models_files

    async def _hang(*_a, **_k):
        await asyncio.Event().wait()

    monkeypatch.setattr(db_pkg, "ensure_bound", lambda: None)
    monkeypatch.setattr(models_files.Files, "exists", _hang)
    readiness.clear_readiness_cache()
    started = time.monotonic()
    probe = await asyncio.wait_for(
        readiness.probe_database_readiness(max_age_seconds=0, timeout_seconds=0.3),
        timeout=5,  # the test's backstop
    )
    assert time.monotonic() - started < 2
    assert probe.ready is False
    assert probe.error_type == "TimeoutError"
    readiness.clear_readiness_cache()
