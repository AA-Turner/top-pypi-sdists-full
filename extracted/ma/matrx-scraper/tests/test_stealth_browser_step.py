"""knowledge.scraper.browser_engine: `current` (default) vs `stealth` - one path, chosen by the knob."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_scraper import orchestrator, stealth_browser
from matrx_scraper.parser import knobs
from matrx_scraper.scraper import RequestType


@pytest.fixture(autouse=True)
def _reset_knobs():
    yield
    knobs.configure_parser_knobs(None)


def _bind(value: Any) -> None:
    def reader(key: str) -> Any:
        if key == "browser_engine":
            return value
        raise KeyError(key)  # every other knob keeps its mirrored default

    knobs.configure_parser_knobs(reader)


def test_default_is_stealth_when_installed_and_unbound_host_uses_the_mirror(monkeypatch) -> None:
    monkeypatch.setattr(stealth_browser, "stealth_available", lambda: True)
    assert stealth_browser.browser_engine() == "stealth"
    assert stealth_browser.use_stealth() is True


def test_unknown_engine_value_falls_back_to_the_default() -> None:
    _bind("turbo")
    assert stealth_browser.browser_engine() == stealth_browser.DEFAULT_ENGINE


def test_stealth_without_scrapling_announces_and_uses_current(monkeypatch, caplog) -> None:
    _bind("stealth")
    monkeypatch.setattr(stealth_browser, "stealth_available", lambda: False)
    with caplog.at_level("WARNING"):
        assert stealth_browser.use_stealth() is False
    assert "scrapling is not installed" in caplog.text


class _Pool:
    called = False

    async def fetch(self, url: str, **kwargs: Any):
        _Pool.called = True
        return "<html><body><p>pool body text here</p></body></html>", url, 200, {}, "pool"


def _run(monkeypatch, engine: str) -> Any:
    _bind(engine)
    monkeypatch.setattr(stealth_browser, "stealth_available", lambda: True)
    seen: dict[str, Any] = {}

    async def fake_stealth(url: str, **kwargs: Any):
        seen.update(kwargs, url=url)
        return "<html><head><title>S</title></head><body><p>stealth body text here</p></body></html>", url, 200, {}, "S"

    monkeypatch.setattr(stealth_browser, "stealth_fetch", fake_stealth)
    _Pool.called = False
    result = asyncio.run(
        orchestrator._fetch_and_parse(
            "https://example.com/",
            request_type=RequestType.BROWSER,
            use_proxy=False,
            fast=True,
            browser_pool=_Pool(),
            user_agent=None,
        )
    )
    return result, seen


def test_orchestrator_routes_browser_step_to_stealth_when_knob_says_so(monkeypatch) -> None:
    _, seen = _run(monkeypatch, "stealth")
    assert seen["url"] == "https://example.com/"
    assert _Pool.called is False


def test_orchestrator_keeps_the_pool_when_knob_is_current(monkeypatch) -> None:
    _, seen = _run(monkeypatch, "current")
    assert seen == {}
    assert _Pool.called is True


def test_a_failing_stealth_fetch_falls_back_to_the_current_engine(monkeypatch) -> None:
    _bind("stealth")
    monkeypatch.setattr(stealth_browser, "stealth_available", lambda: True)

    async def boom(url: str, **kwargs: Any):
        raise TimeoutError("page.goto timed out")

    monkeypatch.setattr(stealth_browser, "stealth_fetch", boom)
    _Pool.called = False
    result = asyncio.run(
        orchestrator._fetch_and_parse(
            "https://example.com/",
            request_type=RequestType.BROWSER,
            use_proxy=False,
            fast=True,
            browser_pool=_Pool(),
            user_agent=None,
        )
    )
    assert _Pool.called is True
    assert result.title == "pool"


def test_a_desktop_host_never_gets_a_visible_browser(monkeypatch):
    """A person's Mac/Windows/Linux desktop must never see a browser window pop up: headful runs
    only inside our own Xvfb on Linux (2026-10-18: Chrome for Testing windows stopped a developer's work)."""
    from matrx_scraper import stealth_browser as sb

    monkeypatch.setattr(sb, "_xvfb", None)
    for platform in ("darwin", "win32"):
        monkeypatch.setattr(sb.sys, "platform", platform)
        monkeypatch.setenv("DISPLAY", ":0")
        assert sb._ensure_display() is False
    # A Linux desktop with its own DISPLAY but no Xvfb binary also stays headless.
    monkeypatch.setattr(sb.sys, "platform", "linux")
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setattr(sb.shutil, "which", lambda _name: None)
    assert sb._ensure_display() is False
