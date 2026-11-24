"""STARTING IS NOT DEAD (2026-11-16): a slow-starting browser is never killed by the probe deadline.

A person's default profile (288 MB, months of use) took longer than the 5 s
liveness deadline to answer after every launch. The first command probed it,
called it dead, relaunched it once under the same 5 s, and ended the run
"The browser stopped (the browser did not answer within 5s) and could not be
restarted" on every start for ten days, while a new 41 MB profile worked.

A Chromium that has not answered since launch gets the launch budget; one that
has answered keeps the short deadline (the 2026-10-22 zombie rule).
"""

from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

PROBE_S = 0.2


class _SlowContext:
    """A browser whose cookie read takes ``delay_s``."""

    browser = None

    def __init__(self, delay_s: float) -> None:
        self.delay_s = delay_s

    async def cookies(self, _url: str) -> list:
        await asyncio.sleep(self.delay_s)
        return []


def _worker(delay_s: float, *, answered: bool) -> BrowserWorker:
    worker = object.__new__(BrowserWorker)
    worker._context = _SlowContext(delay_s)
    worker._pages = {"p": SimpleNamespace(closed_at=None, page=object())}
    worker._launched_at = time.monotonic()
    worker._answered_since_launch = answered
    worker._liveness_timeout_s = PROBE_S
    worker._browser_down_reason = None
    worker._person_closed = False
    worker._last_launch = (object(), None)
    worker._closing_intentionally = False
    worker._terminating = False
    worker._checkpoint_in_progress = False
    worker._controller = SimpleNamespace(state="agent_control")
    worker._command_lock = asyncio.Lock()
    worker._agent_inflight = 0
    relaunches: list[str] = []

    async def _relaunch(why: str) -> bool:
        relaunches.append(why)
        return False

    worker._relaunch_dead_browser = _relaunch  # type: ignore[method-assign]
    worker.relaunches = relaunches  # type: ignore[attr-defined]
    return worker


async def test_a_command_waits_for_a_browser_that_is_still_starting():
    worker = _worker(PROBE_S * 3, answered=False)
    alive, why = await worker._browser_alive(PROBE_S)
    assert alive, why
    assert worker._answered_since_launch


async def test_a_heartbeat_makes_no_claim_about_a_browser_that_is_still_starting():
    worker = _worker(PROBE_S * 3, answered=False)
    assert await worker._heartbeat_liveness() is None
    assert worker.relaunches == []  # type: ignore[attr-defined]


async def test_a_browser_that_answered_once_keeps_the_short_deadline():
    worker = _worker(PROBE_S * 3, answered=True)
    alive, why = await worker._browser_alive(PROBE_S)
    assert not alive
    assert why.startswith("the browser did not answer within")
    assert await worker._heartbeat_liveness() == "down"
    assert len(worker.relaunches) == 1  # type: ignore[attr-defined]


async def test_a_browser_silent_past_the_launch_budget_is_dead():
    worker = _worker(PROBE_S * 3, answered=False)
    worker._launched_at = time.monotonic() - M.BOOTSTRAP_LAUNCH_TIMEOUT_SECONDS - 1
    alive, _ = await worker._browser_alive(PROBE_S)
    assert not alive
    assert await worker._heartbeat_liveness() == "down"
