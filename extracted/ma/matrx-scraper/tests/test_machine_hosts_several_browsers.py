"""A Cloud Computer hosts several named browsers, each its own run (W7 phase 1).

Breaks each test catches:
- a second profile on the machine is refused ``already_bootstrapped`` (today's
  one-run worker), which is what pushed every second browser onto the fleet;
- a command for browser A lands in browser B (routing by run_id broken);
- shutting down A stops B, or restarts B's Chrome;
- the same profile bootstrapped twice gets a second Chromium on one profile;
- a full host launches a browser anyway.

Real Chromium (headless ``automation_only``), no fakes of the worker itself.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.cloud_browser.worker import BrowserWorker, StubControlPlane  # noqa: E402
from matrx_scraper.cloud_browser.worker import runtime  # noqa: E402
from matrx_scraper.cloud_browser.worker.machine_browsers import MachineBrowsers  # noqa: E402

CHROMIUM = pytest.mark.skipif(
    not any(Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")).glob("chromium-*")),
    reason="no chromium browser binary",
)


def _host(max_browsers: int = 4) -> MachineBrowsers:
    def new() -> BrowserWorker:
        return BrowserWorker(worker_id="machine-worker")

    return MachineBrowsers(new(), factory=new, max_browsers=max_browsers)


def _page(text: str) -> str:
    return f"data:text/html,<html><head><title>{text}</title></head><body><h1>{text}</h1></body></html>"


async def _load(host: MachineBrowsers, run_id: str, text: str) -> None:
    worker = host._route(run_id)  # noqa: SLF001
    page = worker.page_object(worker.active_page_id)
    await page.goto(_page(text), wait_until="commit")


async def _text(stub: StubControlPlane) -> str:
    """What this run's own browser shows, asked THROUGH the host (routed by run_id)."""
    reply = await stub.observe(include=["pages"])
    assert reply.ok, reply.error
    return str(reply.model_dump())


@CHROMIUM
@pytest.mark.asyncio
async def test_two_profiles_run_side_by_side_and_never_touch_each_other(tmp_path) -> None:
    host = _host()
    a = StubControlPlane(host, profile_id="prof_a")  # type: ignore[arg-type]
    b = StubControlPlane(host, profile_id="prof_b")  # type: ignore[arg-type]
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    try:
        boot_a = await a.bootstrap(user_data_dir=str(tmp_path / "a"))
        boot_b = await b.bootstrap(user_data_dir=str(tmp_path / "b"))
        assert boot_a.accepted, boot_a.error
        assert boot_b.accepted, boot_b.error  # today: already_bootstrapped
        assert len({id(w) for w in host.workers}) == 2
        assert {row["run_id"] for row in host.browsers()} == {a.run_id, b.run_id}

        await _load(host, a.run_id, "browser-A")
        await _load(host, b.run_id, "browser-B")
        text_a, text_b = await _text(a), await _text(b)
        assert "browser-A" in text_a and "browser-B" not in text_a
        assert "browser-B" in text_b and "browser-A" not in text_b

        pid_b = runtime._profile_lock_holder(str(tmp_path / "b"))  # noqa: SLF001
        stopped = await a.shutdown()
        assert stopped.ok, stopped.error
        assert "browser-B" in await _text(b), "shutting A down leaves B serving"
        assert runtime._profile_lock_holder(str(tmp_path / "b")) == pid_b, "B's Chrome untouched"

        # A stopped browser's worker is reused for the next run, not leaked.
        c = StubControlPlane(host, profile_id="prof_c")  # type: ignore[arg-type]
        (tmp_path / "c").mkdir()
        assert (await c.bootstrap(user_data_dir=str(tmp_path / "c"))).accepted
        assert len(host.workers) == 2
        await c.shutdown()
    finally:
        await host.terminate_gracefully(reason="test")


@CHROMIUM
@pytest.mark.asyncio
async def test_same_profile_twice_is_refused_and_a_full_host_launches_nothing(tmp_path) -> None:
    host = _host(max_browsers=1)
    a = StubControlPlane(host, profile_id="prof_a")  # type: ignore[arg-type]
    again = StubControlPlane(host, profile_id="prof_a")  # type: ignore[arg-type]
    other = StubControlPlane(host, profile_id="prof_b")  # type: ignore[arg-type]
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    try:
        assert (await a.bootstrap(user_data_dir=str(tmp_path / "a"))).accepted
        twice = await again.bootstrap(user_data_dir=str(tmp_path / "a"))
        assert not twice.accepted and twice.error.code == "already_bootstrapped"
        full = await other.bootstrap(user_data_dir=str(tmp_path / "b"))
        assert not full.accepted and full.error.code == "machine_browsers_full"
        assert len(host.workers) == 1
        assert runtime._profile_lock_holder(str(tmp_path / "b")) is None  # noqa: SLF001
    finally:
        await host.terminate_gracefully(reason="test")
