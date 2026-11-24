"""A loaded page is never a failed navigation because its network never went quiet.

Live evidence, 2026-11-06 (conversation a2d03e88): ``cloud_browser(action="navigate",
wait_for="networkidle")`` on a qz.com article failed with ``Page.goto: Timeout 30000ms
exceeded … waiting until "networkidle"``. The page had loaded — the very next call, with
``domcontentloaded``, read its 17,245 characters. News pages keep ads, trackers and live
sockets open forever, so ``networkidle`` as a hard goto condition can never be met there.

Rule: ``networkidle`` loads the page first, then waits a bounded grace for quiet (the host's
``cloud_browser.fleet.networkidle_grace_ms`` knob, else the navigation timeout); when the grace
runs out the navigation still succeeds and says so in ``notice``.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

actions = importlib.import_module("matrx_scraper.ai_browser.actions")


class TimeoutError(Exception):  # noqa: A001 - Playwright's own class name
    pass


class _Resp:
    status = 200


class NeverQuietPage:
    """Loads fine; its network never goes idle (a news page with ads)."""

    url = "https://qz.com/should-you-buy-the-dip-smartasset"

    def __init__(self) -> None:
        self.goto_waits: list[str] = []

    async def goto(self, url: str, *, wait_until: str, timeout: int) -> _Resp:  # noqa: ASYNC109 - Playwright signature
        self.goto_waits.append(wait_until)
        if wait_until == "networkidle":
            raise TimeoutError(f"Page.goto: Timeout {timeout}ms exceeded.")
        return _Resp()

    async def wait_for_load_state(self, state: str, *, timeout: int) -> None:  # noqa: ASYNC109 - Playwright signature
        if state == "load":
            return None
        assert state == "networkidle"
        self.grace = timeout
        raise TimeoutError(f"Timeout {timeout}ms exceeded.")

    async def title(self) -> str:
        return "Should you buy the dip?"


class QuietPage(NeverQuietPage):
    async def wait_for_load_state(self, state: str, *, timeout: int) -> None:  # noqa: ASYNC109 - Playwright signature
        return None


class _Session:
    session_id = "sess1"

    def __init__(self, page: Any) -> None:
        self.page = page


class _Mgr:
    def __init__(self, page: Any) -> None:
        self.session = _Session(page)

    async def get(self, session_id: str) -> _Session:
        return self.session


@pytest.fixture(autouse=True)
def _public(monkeypatch: pytest.MonkeyPatch) -> None:
    async def target(url: str) -> str:
        return url

    async def proxy(_: Any) -> None:
        return None

    async def landing(_: Any) -> None:
        return None

    monkeypatch.setattr(actions, "guard_target", target)
    monkeypatch.setattr(actions, "guard_proxy", proxy)
    monkeypatch.setattr(actions, "guard_landing", landing)


async def _navigate(page: Any, wait_until: str = "networkidle", **kwargs: Any) -> Any:
    mgr = _Mgr(page)
    resolve = actions._resolve_session

    async def fake_resolve(session_id: str, *, mgr: Any) -> tuple[Any, None]:
        return mgr.session, None

    actions._resolve_session = fake_resolve
    try:
        return await actions.navigate(
            page.url, session_id="sess1", wait_until=wait_until, mgr=mgr, **kwargs
        )
    finally:
        actions._resolve_session = resolve


@pytest.mark.asyncio
async def test_a_page_that_never_goes_quiet_still_navigates_and_says_so() -> None:
    page = NeverQuietPage()
    result = await _navigate(page, networkidle_grace_ms=8000)
    assert result.success, result.error_message
    assert result.http_status == 200
    assert result.notice and "never went quiet within 8s" in result.notice
    assert page.goto_waits == ["domcontentloaded"]
    assert page.grace == 8000


@pytest.mark.asyncio
async def test_without_a_grace_the_navigation_timeout_bounds_the_wait() -> None:
    page = NeverQuietPage()
    result = await _navigate(page, timeout_ms=20_000)
    assert result.success and result.notice
    assert page.grace == 20_000


def test_the_worker_command_carries_the_grace_only_when_set() -> None:
    commands = importlib.import_module("matrx_scraper.cloud_browser.worker.commands")
    plain = commands.NavigateCommand(url="https://example.com")
    assert "networkidle_grace_ms" not in plain.model_dump(mode="json", exclude_none=True)
    idle = commands.NavigateCommand(
        url="https://example.com", wait_until="networkidle", networkidle_grace_ms=8000
    )
    assert idle.model_dump(mode="json", exclude_none=True)["networkidle_grace_ms"] == 8000


@pytest.mark.asyncio
async def test_a_page_that_goes_quiet_carries_no_notice() -> None:
    result = await _navigate(QuietPage())
    assert result.success
    assert result.notice is None


class NeverLoadedPage(NeverQuietPage):
    """A heavy app (Gmail, live 2026-11-23): its document arrives at once, but its ``load`` event
    does not fire inside 30 s, so ``goto(wait_until="load")`` timed out a page a person could use."""

    url = "https://mail.google.com/mail/u/0/#inbox"

    async def goto(self, url: str, *, wait_until: str, timeout: int) -> _Resp:  # noqa: ASYNC109 - Playwright signature
        self.goto_waits.append(wait_until)
        if wait_until in ("load", "networkidle"):
            raise TimeoutError(f"Page.goto: Timeout {timeout}ms exceeded.")
        return _Resp()

    async def wait_for_load_state(self, state: str, *, timeout: int) -> None:  # noqa: ASYNC109 - Playwright signature
        self.load_wait = (state, timeout)
        raise TimeoutError(f"Timeout {timeout}ms exceeded.")


@pytest.mark.asyncio
async def test_a_page_whose_load_never_fires_still_navigates_and_says_so() -> None:
    page = NeverLoadedPage()
    result = await _navigate(page, wait_until="load")
    assert result.success, result.error_message
    assert result.http_status == 200
    assert result.notice and "had not finished loading within 30s" in result.notice
    assert page.goto_waits == ["domcontentloaded"]
    assert page.load_wait[0] == "load" and 0 < page.load_wait[1] <= 30_000


@pytest.mark.asyncio
async def test_a_page_that_loads_carries_no_notice() -> None:
    result = await _navigate(QuietPage(), wait_until="load")
    assert result.success
    assert result.notice is None


@pytest.mark.asyncio
async def test_a_page_that_never_arrives_still_fails() -> None:
    class DeadPage(NeverLoadedPage):
        async def goto(self, url: str, *, wait_until: str, timeout: int) -> _Resp:  # noqa: ASYNC109
            raise TimeoutError(f"Page.goto: Timeout {timeout}ms exceeded.")

    result = await _navigate(DeadPage(), wait_until="load")
    assert not result.success
    assert result.error_type == "navigation"
