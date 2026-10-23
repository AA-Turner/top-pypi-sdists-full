"""THE ZOMBIE BROWSER (2026-10-22): a renewed lease must mean a browser that answers.

Run 20fc9558 on a Cloud Computer had a dead Chromium ("Target page, context or
browser has been closed", no pages) while every lease renewal answered ok, so
the run stayed "running", its viewer reconnected to an empty stream for good,
and an agent navigate failed. These tests kill the real Chromium under a
running worker and prove:

- a heartbeat that asks for liveness notices, relaunches ONCE on the same
  profile, and answers ``relaunched`` (then ``running``);
- a command on a dead browser relaunches it and retries once instead of failing;
- a relaunch that fails answers ``down`` with the reason, health
  ``browser_crashed``, and every later command is refused as ``browser_crashed``;
- a browser that hangs (the pipe held open by its children) is dead after the
  probe deadline, never "running".
"""

from __future__ import annotations

import asyncio
import os
import signal
import subprocess
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.cloud_browser.worker import BrowserWorker, StubControlPlane  # noqa: E402
from matrx_scraper.cloud_browser.worker import commands as C  # noqa: E402
from matrx_scraper.cloud_browser.worker import models as M  # noqa: E402

PROBE_MS = 3000
DATA_PAGE = "data:text/html,<html><body><h1 id='h'>alive</h1></body></html>"


def _chromium_available() -> bool:
    base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    return base.exists() and any(base.glob("chromium*"))


CHROMIUM = pytest.mark.skipif(not _chromium_available(), reason="no chromium browser binary")


@pytest.fixture
def profile_dir(tmp_path: Path) -> str:
    path = tmp_path / "profile"
    path.mkdir()
    return str(path)


def _chrome_main_pids(user_data_dir: str) -> list[int]:
    """The Chromium BROWSER process(es) on this profile: the one without ``--type=``."""
    out = subprocess.run(["ps", "-axww", "-o", "pid=,command="], capture_output=True, text=True).stdout
    pids = []
    for line in out.splitlines():
        pid, _, command = line.strip().partition(" ")
        if f"--user-data-dir={user_data_dir}" in command and "--type=" not in command:
            pids.append(int(pid))
    return pids


async def _kill_chrome(user_data_dir: str) -> None:
    pids = _chrome_main_pids(user_data_dir)
    assert pids, "found no Chromium browser process to kill"
    for pid in pids:
        os.kill(pid, signal.SIGKILL)
    for _ in range(50):
        if not _chrome_main_pids(user_data_dir):
            break
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.5)  # let Playwright see the pipe close


async def _load_data_page(worker: BrowserWorker) -> None:
    page = worker.page_object(worker.active_page_id)
    await page.goto(DATA_PAGE, wait_until="commit")


async def _booted(profile_dir: str) -> tuple[BrowserWorker, StubControlPlane]:
    worker = BrowserWorker(worker_id="worker-zombie")
    stub = StubControlPlane(worker)
    boot = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert boot.ok and boot.accepted
    return worker, stub


@CHROMIUM
async def test_heartbeat_notices_a_killed_chromium_and_relaunches_it_once(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        first = await stub.heartbeat(liveness_probe_timeout_ms=PROBE_MS)
        assert first.ok and first.browser_state == "running"

        await _kill_chrome(profile_dir)

        after = await stub.heartbeat(liveness_probe_timeout_ms=PROBE_MS)
        assert after.ok
        assert after.browser_state == "relaunched", after
        assert after.worker_health == "healthy"
        assert _chrome_main_pids(profile_dir), "no Chromium is running after the relaunch"

        again = await stub.heartbeat(liveness_probe_timeout_ms=PROBE_MS)
        assert again.browser_state == "running"

        await _load_data_page(worker)
        page = worker.page_object(worker.active_page_id)
        assert await page.evaluate("document.getElementById('h').textContent") == "alive"
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_a_command_on_a_killed_chromium_relaunches_and_retries_once(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        await stub.heartbeat(liveness_probe_timeout_ms=PROBE_MS)
        await _kill_chrome(profile_dir)

        # No heartbeat in between: the command itself finds the dead browser.
        # (A blank page answers get_text "navigate first" — a LIVE page's answer;
        # a dead browser answers error_type "browser", "...has been closed".)
        revived = await stub.command(C.GetTextCommand())
        assert revived.ok, revived
        assert revived.result is not None and revived.result.error_type != "browser", revived.result
        assert worker.health == "healthy"
        await _load_data_page(worker)
        page = worker.page_object(worker.active_page_id)
        assert await page.evaluate("document.getElementById('h').textContent") == "alive"
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_a_failed_relaunch_is_down_never_running(
    profile_dir: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        await _kill_chrome(profile_dir)

        async def refuse(_policy, _display):  # noqa: ANN001, ANN202
            raise RuntimeError("chrome would not start")

        monkeypatch.setattr(worker, "_launch_context", refuse)
        hb = await stub.heartbeat(liveness_probe_timeout_ms=PROBE_MS)
        assert hb.browser_state == "down"
        assert hb.browser_down_reason and "could not be restarted" in hb.browser_down_reason
        assert hb.worker_health == "browser_crashed"
        # Only ONE relaunch: the next heartbeat does not try again, it stays down.
        assert (await stub.heartbeat(liveness_probe_timeout_ms=PROBE_MS)).browser_state == "down"

        refused = await stub.command(C.GetTextCommand())
        assert not refused.ok and refused.error is not None
        assert refused.error.code == "browser_crashed"
    finally:
        monkeypatch.undo()
        await stub.shutdown()


async def test_a_hung_browser_is_dead_after_the_probe_deadline() -> None:
    """Chromium's main process gone but its children hold the pipe: Playwright
    never sees a close, and every call just waits. The probe deadline decides."""
    worker = BrowserWorker(worker_id="worker-hung")

    class _HungContext:
        browser = None

        async def cookies(self, *_a):  # noqa: ANN002, ANN202
            await asyncio.sleep(3600)

    worker._context = _HungContext()
    alive, why = await worker._browser_alive(0.2)
    assert alive is False and "did not answer within 0.2s" in why


def test_heartbeat_without_the_probe_field_is_what_an_old_server_sends() -> None:
    """A server that predates the probe sends no field and gets no claim."""
    fields = M.HeartbeatRequest.model_fields
    assert fields["liveness_probe_timeout_ms"].default is None
    assert M.HeartbeatResponse.model_fields["browser_state"].default is None
