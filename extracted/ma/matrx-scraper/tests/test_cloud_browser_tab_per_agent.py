"""TAB PER AGENT (2026-10-22): several agents share one person's Chrome.

Before: the worker had one command lock and one active page per run, so two
agents attached to the same browser drove each other's tab — agent B's navigate
replaced agent A's page under it, and A read B's site back. These tests run two
agents against ONE real Chromium and prove:

- two agents navigating different sites AT THE SAME TIME each read back their
  own page (``agent_ref`` routes each command to that agent's tab);
- one agent's slow command never holds up another agent's command;
- a tab a person closed is reopened at that agent's last page on its next
  command, and the other agent's tab is untouched;
- an agent closing its tab ends only its page;
- past the tab limit (knob ``cloud_browser.agent_tabs.max_per_browser``) the
  agent idle longest gives up its tab instead of anyone being blocked;
- a screenshot with ``agent_ref`` pictures that agent's tab.
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.ai_browser import actions as A  # noqa: E402
from matrx_scraper.cloud_browser.worker import BrowserWorker, StubControlPlane  # noqa: E402
from matrx_scraper.cloud_browser.worker import commands as C  # noqa: E402

SITES = {
    "https://site-a.test/": "<html><head><title>A</title></head><body><h1>alpha page</h1></body></html>",
    "https://site-b.test/": "<html><head><title>B</title></head><body><h1>bravo page</h1></body></html>",
    "https://site-c.test/": "<html><head><title>C</title></head><body><h1>charlie page</h1></body></html>",
}


#: How long site C takes to answer. Agent A's whole command must finish while
#: this is still loading.
SLOW_SECONDS = 8


def _chromium_available() -> bool:
    base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    return base.exists() and any(base.glob("chromium*"))


CHROMIUM = pytest.mark.skipif(not _chromium_available(), reason="no chromium browser binary")


@pytest.fixture
def profile_dir(tmp_path: Path) -> str:
    path = tmp_path / "profile"
    path.mkdir()
    return str(path)


@pytest.fixture(autouse=True)
def _test_sites_are_reachable(monkeypatch: pytest.MonkeyPatch) -> None:
    """``*.test`` never resolves; the SSRF gate is not the subject here (its
    own tests pin it), so it passes these three test sites through."""

    async def _target(url: str) -> str:
        return url

    async def _landing(_page) -> None:  # noqa: ANN001
        return None

    monkeypatch.setattr(A, "guard_target", _target)
    monkeypatch.setattr(A, "guard_landing", _landing)


async def _booted(profile_dir: str) -> tuple[BrowserWorker, StubControlPlane]:
    worker = BrowserWorker(worker_id="worker-tabs")
    stub = StubControlPlane(worker)
    boot = await stub.bootstrap(user_data_dir=profile_dir, run_mode="automation_only")
    assert boot.ok and boot.accepted

    async def _serve(route) -> None:  # noqa: ANN001
        url = route.request.url
        body = SITES.get(url)
        if body is None:
            await route.fulfill(status=404, body="no such test page")
            return
        if url == "https://site-c.test/":
            await asyncio.sleep(SLOW_SECONDS)  # a slow site: its navigate holds its agent
        await route.fulfill(status=200, content_type="text/html", body=body)

    await worker.context.route("https://*.test/**", _serve)
    return worker, stub


async def _text(stub: StubControlPlane, agent: str) -> str:
    reply = await stub.command(C.GetTextCommand(), agent_ref=agent)
    assert reply.ok, reply
    return reply.result.text or ""


@CHROMIUM
async def test_two_agents_navigate_at_once_and_each_reads_its_own_page(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        nav_a, nav_b = await asyncio.gather(
            stub.command(C.NavigateCommand(url="https://site-a.test/"), agent_ref="conv-a"),
            stub.command(C.NavigateCommand(url="https://site-b.test/"), agent_ref="conv-b"),
        )
        assert nav_a.ok and nav_a.result.success, nav_a
        assert nav_b.ok and nav_b.result.success, nav_b
        assert nav_a.active_page_id != nav_b.active_page_id, "two agents were given one tab"

        text_a, text_b = await asyncio.gather(_text(stub, "conv-a"), _text(stub, "conv-b"))
        assert "alpha page" in text_a and "bravo" not in text_a, text_a
        assert "bravo page" in text_b and "alpha" not in text_b, text_b

        # Interleaved again, in the other order: still each its own.
        assert "bravo page" in await _text(stub, "conv-b")
        assert "alpha page" in await _text(stub, "conv-a")
        live = [p for p in (await stub.observe()).page_inventory.pages if not p.is_closed]
        assert len(live) == 2, live
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_a_slow_agent_never_holds_up_another_agent(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        await stub.command(C.NavigateCommand(url="https://site-a.test/"), agent_ref="conv-a")
        slow = asyncio.create_task(
            stub.command(C.NavigateCommand(url="https://site-c.test/"), agent_ref="conv-slow")
        )
        await asyncio.sleep(0.5)  # the slow navigate is in flight
        started = time.monotonic()
        text = await _text(stub, "conv-a")
        waited = time.monotonic() - started
        assert "alpha page" in text
        # The property: A's whole command finished while B's page was still
        # loading. (No wall-clock bound: a loaded test machine makes any
        # threshold flaky, and ordering alone proves A never queued behind B.)
        assert not slow.done(), f"agent A ({waited:.1f}s) finished only after the other agent's page load"
        done = await slow
        assert done.ok and done.result.success, done
        assert "charlie page" in await _text(stub, "conv-slow")
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_a_closed_tab_reopens_for_its_agent_and_leaves_the_other_alone(
    profile_dir: str,
) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        a = await stub.command(C.NavigateCommand(url="https://site-a.test/"), agent_ref="conv-a")
        b = await stub.command(C.NavigateCommand(url="https://site-b.test/"), agent_ref="conv-b")
        page_b = worker.page_object(b.active_page_id)

        # A person closes agent A's tab (Take control, or on the desktop).
        await worker.page_object(a.active_page_id).close()
        await asyncio.sleep(0.2)

        assert "alpha page" in await _text(stub, "conv-a"), "A's tab did not come back at its page"
        assert not page_b.is_closed()
        assert "bravo page" in await _text(stub, "conv-b")
        assert worker.page_object((await stub.command(C.GetTextCommand(), agent_ref="conv-b")).active_page_id) is page_b
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_an_agent_closing_its_tab_ends_only_its_page(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        a = await stub.command(C.NavigateCommand(url="https://site-a.test/"), agent_ref="conv-a")
        b = await stub.command(C.NavigateCommand(url="https://site-b.test/"), agent_ref="conv-b")
        closed = await stub.command(C.ClosePageCommand(), agent_ref="conv-a")
        assert closed.ok and closed.result.closed, closed
        assert worker.page_object(a.active_page_id).is_closed()
        assert not worker.page_object(b.active_page_id).is_closed()
        assert "bravo page" in await _text(stub, "conv-b")

        # A cannot close B's tab by naming it.
        refused = await stub.command(
            C.ClosePageCommand(target_page_id=b.active_page_id), agent_ref="conv-a"
        )
        assert not refused.ok and refused.error.code == "page_owned_by_other_agent", refused
        assert not worker.page_object(b.active_page_id).is_closed()
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_past_the_tab_limit_the_idlest_agent_gives_up_its_tab(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        await stub.command(
            C.NavigateCommand(url="https://site-a.test/"), agent_ref="conv-a", agent_tab_limit=2
        )
        await stub.command(
            C.NavigateCommand(url="https://site-b.test/"), agent_ref="conv-b", agent_tab_limit=2
        )
        c = await stub.command(
            C.NavigateCommand(url="https://site-c.test/"), agent_ref="conv-c", agent_tab_limit=2
        )
        assert c.ok and c.result.success, c
        await asyncio.sleep(0.3)
        live = [p for p in (await stub.observe()).page_inventory.pages if not p.is_closed]
        assert len(live) == 2, live
        # A (idle longest) gets a fresh tab at its own page when it comes back.
        assert "alpha page" in await _text(stub, "conv-a")
    finally:
        await stub.shutdown()


@CHROMIUM
async def test_a_screenshot_pictures_the_asking_agents_tab(profile_dir: str) -> None:
    worker, stub = await _booted(profile_dir)
    try:
        a = await stub.command(C.NavigateCommand(url="https://site-a.test/"), agent_ref="conv-a")
        await stub.command(C.NavigateCommand(url="https://site-b.test/"), agent_ref="conv-b")
        assert worker.active_page_id != a.active_page_id  # B is in front now
        shot_a = await stub.capture(agent_ref="conv-a")
        shot_front = await stub.capture()
        assert shot_a.ok and shot_a.captured and shot_front.ok and shot_front.captured
        # The front tab is B's; A's picture is A's page, not what is in front.
        assert shot_a.artifact.image_base64 != shot_front.artifact.image_base64
        await stub.command(C.GetTextCommand(), agent_ref="conv-a")  # A in front now
        again_front = await stub.capture()
        assert again_front.artifact.image_base64 == shot_a.artifact.image_base64
    finally:
        await stub.shutdown()
