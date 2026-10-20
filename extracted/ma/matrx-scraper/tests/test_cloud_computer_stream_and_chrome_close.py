"""Cloud Computer owner report, 2026-10-17: the screen dropped on Take control,
the first picture took ~20 s, a Chrome the person closed came back on its own
with "Chrome didn't shut down correctly", and the Web Store said "Installation
is not enabled". Each test fails on the code before the fix."""
from __future__ import annotations

import asyncio
import json

from fastapi.testclient import TestClient

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor
from matrx_scraper.cloud_browser.worker import http_app
from matrx_scraper.cloud_browser.worker import runtime as rt
from matrx_scraper.cloud_browser.worker.identity import DESKTOP_IGNORED_DEFAULT_ARGS

from test_cloud_computer_desktop_chrome import _DISPLAY, _POLICY, _worker, fake_playwright  # noqa: F401


class _Stream:
    def __init__(self, keep_warm: bool) -> None:
        self.keep_warm = keep_warm
        self.calls: list[str] = []

    def stop(self) -> None:
        self.calls.append("stop")

    def clear_rtc(self) -> None:
        self.calls.append("clear")


def test_a_kept_warm_stream_never_stops_when_idle() -> None:
    warm, fleet = _Stream(True), _Stream(False)
    http_app._end_idle_stream(warm)
    http_app._end_idle_stream(fleet)
    assert warm.calls == []
    assert fleet.calls == ["stop", "clear"]


def test_a_warm_start_writes_a_placeholder_rtc_file_first(tmp_path, monkeypatch) -> None:
    sup = SelkiesSupervisor(keep_warm=True, rtc_config_path=str(tmp_path / "rtc.json"))
    started: list[bool] = []
    monkeypatch.setattr(sup, "start", lambda: started.append(True))
    sup.start_warm()
    assert started == [True]
    assert json.loads((tmp_path / "rtc.json").read_text())["iceServers"]
    cold = SelkiesSupervisor(rtc_config_path=str(tmp_path / "cold.json"))
    monkeypatch.setattr(cold, "start", lambda: started.append(False))
    cold.start_warm()
    assert started == [True]


def test_the_profile_is_marked_cleanly_exited(tmp_path) -> None:
    prefs = tmp_path / "Default" / "Preferences"
    prefs.parent.mkdir()
    prefs.write_text(json.dumps({"profile": {"exit_type": "Crashed", "exited_cleanly": False}, "x": 1}))
    rt.mark_profile_exited_cleanly(str(tmp_path))
    data = json.loads(prefs.read_text())
    assert data["profile"] == {"exit_type": "Normal", "exited_cleanly": True}
    assert data["x"] == 1
    rt.mark_profile_exited_cleanly(str(tmp_path / "missing"))  # first run: no error


async def test_a_chrome_the_person_closed_stays_closed_until_needed(
    fake_playwright, monkeypatch, tmp_path  # noqa: F811
):
    launches, holder = fake_playwright
    monkeypatch.setenv("BROWSER_WORKER_DESKTOP_SESSION", "/usr/local/bin/cloud-computer-desktop")
    worker = _worker(tmp_path)
    await worker._launch_context(_POLICY, _DISPLAY)

    holder["last"].contexts[0].handlers["close"]()  # the person closed the window
    await asyncio.wait_for(worker._reopen_task, timeout=2)
    await asyncio.sleep(0)
    assert len(launches) == 1  # nothing reopened on its own
    assert worker.desktop_browser_closed and worker.context is None
    assert worker.health == "healthy"

    assert await worker.ensure_desktop_browser() is True  # the agent's next command
    assert len(launches) == 2
    assert launches[1]["user_data_dir"] == launches[0]["user_data_dir"]
    assert not worker.desktop_browser_closed
    assert await worker.ensure_desktop_browser() is False


async def test_the_desktop_chrome_can_install_extensions_the_fleet_cannot(
    fake_playwright, monkeypatch, tmp_path  # noqa: F811
):
    launches, _ = fake_playwright
    monkeypatch.setenv("BROWSER_WORKER_DESKTOP_SESSION", "/usr/local/bin/cloud-computer-desktop")
    await _worker(tmp_path)._launch_context(_POLICY, _DISPLAY)
    monkeypatch.delenv("BROWSER_WORKER_DESKTOP_SESSION")
    await _worker(tmp_path / "fleet")._launch_context(_POLICY, _DISPLAY)
    for arg in DESKTOP_IGNORED_DEFAULT_ARGS:
        assert arg in launches[0]["ignore_default_args"]
        assert arg not in launches[1]["ignore_default_args"]


def test_the_desktop_open_browser_door_answers_only_the_machine() -> None:
    class W:
        worker_id = "w"
        health = "healthy"
        context = object()

        def set_human_control_preparer(self, *_a) -> None:  # noqa: ANN002
            pass

        async def ensure_desktop_browser(self) -> bool:
            return True

    app = http_app.create_worker_app(W())  # type: ignore[arg-type]
    remote = TestClient(app, client=("10.0.0.9", 1234))
    assert remote.post("/desktop/open-browser").status_code == 403
    local = TestClient(app, client=("127.0.0.1", 1234))
    assert local.post("/desktop/open-browser").json() == {"reopened": True, "open": True}


async def test_a_reopened_chrome_shows_exactly_the_agents_tabs(
    fake_playwright, monkeypatch, tmp_path  # noqa: F811
):
    """Live 2026-10-17: after the person closed Chrome, the agent's reopen put a
    blank tab in front of its page, and later there were four tabs (one real,
    three blank). A reopen restores the agent's tabs, its active one in front."""
    launches, holder = fake_playwright
    monkeypatch.setenv("BROWSER_WORKER_DESKTOP_SESSION", "/usr/local/bin/cloud-computer-desktop")
    worker = _worker(tmp_path)
    await worker._launch_context(_POLICY, _DISPLAY)
    first = holder["last"].contexts[0]
    first.pages[0].url = "https://en.wikipedia.org/wiki/Keyboard"
    second = await first.new_page()
    worker._on_new_page(second)
    second.url = "https://example.com/"
    worker._active_page_id = next(
        pid for pid, tp in worker._pages.items() if tp.page is first.pages[0]
    )
    worker._remember_agent_tabs()

    first.handlers["close"]()  # the person closed the window
    await asyncio.wait_for(worker._reopen_task, timeout=2)
    for _ in range(2):  # reopen twice: nothing piles up
        assert await worker.ensure_desktop_browser() is True
        ctx = holder["last"].contexts[0]
        assert [p.url for p in ctx.pages] == ["https://en.wikipedia.org/wiki/Keyboard", "https://example.com/"]
        assert ctx.front is ctx.pages[0]
        assert worker._pages[worker._active_page_id].page is ctx.pages[0]
        worker._remember_agent_tabs()
        ctx.handlers["close"]()
        await asyncio.wait_for(worker._reopen_task, timeout=2)
    assert len(launches) == 3


async def test_chromes_own_session_restore_is_off_on_the_desktop(tmp_path) -> None:
    prefs = tmp_path / "Default" / "Preferences"
    prefs.parent.mkdir()
    prefs.write_text(json.dumps({"session": {"restore_on_startup": 1}, "x": 1}))
    rt.turn_off_chrome_session_restore(str(tmp_path))
    data = json.loads(prefs.read_text())
    assert data["session"]["restore_on_startup"] == 5 and data["x"] == 1


def test_a_chrome_left_on_the_profile_is_found_in_proc(tmp_path) -> None:
    """Live 2026-10-17: the reopen failed "Opening in existing browser session"
    because the closed window's browser process still held the profile."""
    proc = tmp_path / "proc"
    profile = "/home/browser-worker/profile"
    for pid, args in {
        "101": ["/opt/google/chrome/chrome", f"--user-data-dir={profile}", "about:blank"],
        "102": ["/opt/google/chrome/chrome", "--type=renderer", f"--user-data-dir={profile}"],
        "103": ["/opt/google/chrome/chrome", "--user-data-dir=/other"],
        "self": ["x"],
    }.items():
        (proc / pid).mkdir(parents=True)
        (proc / pid / "cmdline").write_bytes(b"\0".join(a.encode() for a in args) + b"\0")
    assert rt._profile_chrome_pids(profile, proc_root=str(proc)) == [101]
    assert rt._profile_chrome_pids(None, proc_root=str(proc)) == []


async def test_a_leftover_chrome_is_ended_before_the_reopen(
    fake_playwright, monkeypatch, tmp_path  # noqa: F811
):
    launches, holder = fake_playwright
    monkeypatch.setenv("BROWSER_WORKER_DESKTOP_SESSION", "/usr/local/bin/cloud-computer-desktop")
    ended: list[str | None] = []

    async def _end(user_data_dir):
        ended.append(user_data_dir)
        return []

    monkeypatch.setattr(rt, "end_leftover_chrome", _end)
    worker = _worker(tmp_path)
    await worker._launch_context(_POLICY, _DISPLAY)
    holder["last"].contexts[0].handlers["close"]()
    await asyncio.wait_for(worker._reopen_task, timeout=2)
    ended.clear()
    assert await worker.ensure_desktop_browser() is True
    assert ended == [worker._user_data_dir]
    assert len(launches) == 2
