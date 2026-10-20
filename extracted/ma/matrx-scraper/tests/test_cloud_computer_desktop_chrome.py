"""The agent's Chrome on a Cloud Computer desktop (owner report, 2026-10-17).

He saw a bare full-screen Chrome over the taskbar on a white about:blank, and
closing it left a black screen. On a desktop session the window is a normal
maximized window (the window manager keeps it above the taskbar), it opens on a
real new-tab page, and a window the person closes stays closed until the agent
needs it (test_cloud_computer_stream_and_chrome_close.py). The
browser fleet (no desktop session) keeps its full-screen kiosk flags.
"""

from __future__ import annotations

import asyncio
import os
import socket
import sys
import types

import pytest

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker import runtime as rt


class _Page:
    def __init__(self) -> None:
        self.url = "about:blank"
        self.visited: list[str] = []

    def on(self, *_args) -> None:  # noqa: ANN002
        return None

    async def goto(self, url: str, **_kwargs) -> None:  # noqa: ANN003
        self.visited.append(url)
        self.url = url

    async def close(self) -> None:
        self.closed = True
        self.context.pages.remove(self)

    async def bring_to_front(self) -> None:
        self.context.front = self


class _Context:
    def __init__(self) -> None:
        self.pages = [_Page()]
        self.pages[0].context = self
        self.front = None
        self.handlers: dict[str, object] = {}
        self.browser = None

    def on(self, event: str, handler) -> None:  # noqa: ANN001
        self.handlers[event] = handler

    async def add_init_script(self, _script: str) -> None:
        return None

    async def new_page(self) -> _Page:
        page = _Page()
        page.context = self
        self.pages.append(page)
        return page


class _Playwright:
    def __init__(self, launches: list[dict]) -> None:
        self.launches = launches
        self.contexts: list[_Context] = []
        parent = self

        class _Chromium:
            async def launch_persistent_context(self, **kwargs):  # noqa: ANN003
                parent.launches.append(kwargs)
                ctx = _Context()
                parent.contexts.append(ctx)
                return ctx

        self.chromium = _Chromium()

    async def stop(self) -> None:
        return None


@pytest.fixture
def fake_playwright(monkeypatch):
    launches: list[dict] = []
    holder: dict[str, _Playwright] = {}

    class _Starter:
        async def start(self):
            pw = _Playwright(launches)
            holder.setdefault("first", pw)
            holder["last"] = pw
            return pw

    module = types.ModuleType("playwright.async_api")
    module.async_playwright = lambda: _Starter()  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "playwright.async_api", module)

    async def no_guard(_ctx) -> None:  # noqa: ANN001
        return None

    monkeypatch.setattr(rt, "install_egress_guard", no_guard)
    return launches, holder


def _worker(tmp_path) -> rt.BrowserWorker:
    worker = rt.BrowserWorker(worker_id="worker-a")
    worker.run_id = "run-a"
    worker.profile_id = "profile-a"
    worker.run_mode = "handoff_capable"
    worker._user_data_dir = str(tmp_path / "profile")
    worker.health = "healthy"
    return worker


_POLICY = M.LaunchPolicy(run_mode="handoff_capable")
_DISPLAY = M.DisplayConfig(kind="xvfb", width=1440, height=900)


async def test_desktop_chrome_is_a_maximized_window_on_a_new_tab_page(
    fake_playwright, monkeypatch, tmp_path
):
    launches, holder = fake_playwright
    monkeypatch.setenv("BROWSER_WORKER_DESKTOP_SESSION", "/usr/local/bin/cloud-computer-desktop")
    worker = _worker(tmp_path)

    await worker._launch_context(_POLICY, _DISPLAY)

    args = launches[0]["args"]
    assert "--start-maximized" in args
    assert f"--class={rt.AGENT_CHROME_WINDOW_CLASS}" in args
    assert "--hide-crash-restore-bubble" in args  # live 2026-10-17: bubble after a reopen
    assert "--test-type" in args
    assert not any(a.startswith(("--window-size", "--window-position")) for a in args)
    assert holder["last"].contexts[0].pages[0].visited == [rt.DESKTOP_START_PAGE]


async def test_fleet_chrome_keeps_its_full_screen_window(fake_playwright, monkeypatch, tmp_path):
    launches, holder = fake_playwright
    monkeypatch.delenv("BROWSER_WORKER_DESKTOP_SESSION", raising=False)
    worker = _worker(tmp_path)

    await worker._launch_context(_POLICY, _DISPLAY)

    args = launches[0]["args"]
    assert "--window-position=0,0" in args and "--window-size=1440,900" in args
    assert "--start-maximized" not in args
    assert holder["last"].contexts[0].pages[0].visited == []


async def test_a_fleet_chrome_that_closes_is_a_crash_not_a_reopen(
    fake_playwright, monkeypatch, tmp_path
):
    launches, holder = fake_playwright
    monkeypatch.delenv("BROWSER_WORKER_DESKTOP_SESSION", raising=False)
    worker = _worker(tmp_path)
    await worker._launch_context(_POLICY, _DISPLAY)

    holder["last"].contexts[0].handlers["close"]()

    assert worker._reopen_task is None
    assert worker.health == "browser_crashed"
    assert len(launches) == 1


def test_the_profile_lock_holder_is_read_from_chromiums_singleton_lock(tmp_path):
    udd = tmp_path / "profile"
    udd.mkdir()
    assert rt._profile_lock_holder(str(udd)) is None  # no lock: nothing to wait on
    os.symlink(f"{socket.gethostname()}-4242", udd / "SingletonLock")
    assert rt._profile_lock_holder(str(udd)) == 4242
    (udd / "SingletonLock").unlink()
    os.symlink("another-host-4242", udd / "SingletonLock")
    assert rt._profile_lock_holder(str(udd)) is None  # another host's process is not ours to wait on


@pytest.mark.skipif(not hasattr(os, "pidfd_open"), reason="pidfd is Linux-only")
async def test_the_reopen_waits_for_the_closed_chrome_to_exit(tmp_path):
    proc = await asyncio.create_subprocess_exec(sys.executable, "-c", "import time; time.sleep(0.3)")
    try:
        waiter = asyncio.ensure_future(rt._wait_for_process_exit(proc.pid))
        await asyncio.sleep(0.05)
        assert not waiter.done()  # the holder is alive: the reopen waits
        await proc.wait()
        await asyncio.wait_for(waiter, timeout=2)  # and resolves once it exits
    finally:
        if proc.returncode is None:
            proc.kill()
