"""knowledge.scraper.stealth_retry: a read the judge marks failed gets ONE stealth retry; a good read is untouched."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import pytest

from matrx_scraper import orchestrator, stealth_browser
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.parser import knobs

URL = "https://example.com/page"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setattr(stealth_browser, "stealth_available", lambda: True)
    monkeypatch.setattr(stealth_browser, "STEALTH_RETRY_DEFAULT", True)
    yield
    knobs.configure_parser_knobs(None)


def _result(*, text: str, status: int = 200, title: str = "T", success: bool = True) -> ScrapeResult:
    r = ScrapeResult(url=URL, response_url=URL, success=success, content_type="html")
    r.text_data = text
    r.ai_research_content = text
    r.status_code = status
    r.title = title
    r.content_chars = len(text)
    r.engine = "http"
    return r


GOOD = _result(text="A real article. " * 60)
WALL = _result(text="Just a moment...", status=403, title="Just a moment...", success=False)


def _run(monkeypatch, original: ScrapeResult, *, rendered: ScrapeResult | None, deadline: float | None = None):
    calls: list[dict[str, Any]] = []

    async def fake(url: str, **kwargs: Any):
        calls.append(kwargs)
        if rendered is None:
            raise TimeoutError("stealth timed out")
        return rendered

    monkeypatch.setattr(orchestrator, "_fetch_and_parse", fake)
    out = asyncio.run(
        orchestrator._maybe_retry_with_stealth(
            original, url=URL, use_proxy=False, fast=True, browser_pool=None, user_agent=None, deadline=deadline
        )
    )
    return out, calls


def test_a_page_that_read_fine_is_returned_untouched_and_nothing_runs(monkeypatch) -> None:
    out, calls = _run(monkeypatch, GOOD, rendered=_result(text="x" * 5000))
    assert out is GOOD and calls == []


def test_a_failed_read_is_retried_once_with_the_stealth_engine_and_the_rescue_is_adopted(monkeypatch) -> None:
    rescue = _result(text="The real page text. " * 80)
    out, calls = _run(monkeypatch, WALL, rendered=rescue)
    assert out is rescue and out.escalated is True
    assert len(calls) == 1 and calls[0]["force_engine"] == "stealth"


def test_when_stealth_also_fails_the_original_answer_stands(monkeypatch) -> None:
    out, calls = _run(monkeypatch, WALL, rendered=None)
    assert out is WALL and len(calls) == 1


def test_when_stealth_returns_another_wall_the_original_answer_stands(monkeypatch) -> None:
    out, _ = _run(monkeypatch, WALL, rendered=_result(text="Just a moment...", status=403, title="Just a moment..."))
    assert out is WALL


def test_the_knob_off_means_no_retry(monkeypatch) -> None:
    knobs.configure_parser_knobs(lambda key: False if key == "stealth_retry" else (_ for _ in ()).throw(KeyError(key)))
    out, calls = _run(monkeypatch, WALL, rendered=_result(text="x" * 5000))
    assert out is WALL and calls == []


def test_no_time_left_in_the_callers_budget_skips_the_retry(monkeypatch) -> None:
    out, calls = _run(monkeypatch, WALL, rendered=_result(text="x" * 5000), deadline=time.monotonic() + 3)
    assert out is WALL and calls == []


def test_enough_time_left_still_retries(monkeypatch) -> None:
    out, calls = _run(monkeypatch, WALL, rendered=_result(text="The real page. " * 80), deadline=time.monotonic() + 60)
    assert len(calls) == 1 and out is not WALL


def test_a_page_missing_everywhere_is_not_retried(monkeypatch) -> None:
    gone = _result(text="Not found", status=404, title="Not Found", success=False)
    out, calls = _run(monkeypatch, gone, rendered=_result(text="x" * 5000))
    assert out is gone and calls == []


def test_a_run_already_on_the_stealth_engine_is_not_retried_again(monkeypatch) -> None:
    knobs.configure_parser_knobs(lambda key: "stealth" if key == "browser_engine" else (_ for _ in ()).throw(KeyError(key)))
    out, calls = _run(monkeypatch, WALL, rendered=_result(text="x" * 5000))
    assert out is WALL and calls == []


def test_the_retry_is_born_off_and_a_per_call_override_turns_it_on(monkeypatch) -> None:
    monkeypatch.undo()  # the autouse fixture turned the default on for the tests above; look at the shipped value
    import importlib

    assert importlib.reload(stealth_browser).STEALTH_RETRY_DEFAULT is False


def test_a_per_call_force_runs_the_retry_even_with_the_knob_off(monkeypatch) -> None:
    monkeypatch.setattr(stealth_browser, "STEALTH_RETRY_DEFAULT", False)
    calls: list = []

    async def fake(url, **kw):
        calls.append(kw)
        return _result(text="The real page. " * 80)

    monkeypatch.setattr(orchestrator, "_fetch_and_parse", fake)
    run = lambda force: asyncio.run(orchestrator._maybe_retry_with_stealth(  # noqa: E731
        WALL, url=URL, use_proxy=False, fast=True, browser_pool=None, user_agent=None, deadline=None, force=force))
    assert run(None) is WALL and calls == []
    assert run(True) is not WALL and len(calls) == 1


def test_the_code_default_is_current() -> None:
    assert stealth_browser.DEFAULT_ENGINE == "current"


def test_a_chat_origin_read_with_less_than_the_minimum_left_never_retries(monkeypatch) -> None:
    """The deadline rides the context: no explicit `deadline` is passed, yet a chat read (15 s budget < 20 s) skips."""
    calls: list[Any] = []

    async def fake(url: str, **kwargs: Any):
        calls.append(kwargs)
        return _result(text="The real page. " * 80)

    monkeypatch.setattr(orchestrator, "_fetch_and_parse", fake)

    async def go():
        return await orchestrator._maybe_retry_with_stealth(
            WALL, url=URL, use_proxy=False, fast=True, browser_pool=None, user_agent=None, deadline=None
        )

    with stealth_browser.chat_read_budget():
        assert asyncio.run(go()) is WALL
    assert calls == []
    # the same read outside a chat budget (a screen run / job) still retries
    out = asyncio.run(go())
    assert len(calls) == 1 and out is not WALL


def test_the_agent_scrape_tool_runs_inside_the_chat_budget(monkeypatch) -> None:
    from matrx_scraper.ai_tools import specs

    seen: list[Any] = []

    async def fake_scrape(url: str, **kw: Any):
        seen.append(stealth_browser.current_read_deadline())
        return {"ok": True}

    monkeypatch.setattr(orchestrator, "scrape", fake_scrape)
    asyncio.run(specs._scraper_scrape({"url": URL}))
    assert seen and seen[0] is not None
    assert stealth_browser.current_read_deadline() is None


def test_a_second_retry_while_the_slot_is_busy_skips_stealth_and_keeps_its_answer(monkeypatch) -> None:
    """knowledge.scraper.stealth_max_concurrent (default 1): the second concurrent retry never queues and never launches."""
    stealth_browser._stealth_slots_in_use = 0
    started = asyncio.Event()
    release = asyncio.Event()
    calls: list[str] = []
    rescue = _result(text="The real page text. " * 80)

    async def fake(url: str, **kwargs: Any):
        calls.append(url)
        started.set()
        await release.wait()
        return rescue

    monkeypatch.setattr(orchestrator, "_fetch_and_parse", fake)

    async def go():
        def retry(original):
            return orchestrator._maybe_retry_with_stealth(
                original, url=URL, use_proxy=False, fast=True, browser_pool=None, user_agent=None, deadline=None
            )

        first = asyncio.create_task(retry(WALL))
        await started.wait()
        second = await asyncio.wait_for(retry(WALL), 1)  # returns at once: no queueing behind the first
        release.set()
        return await first, second

    first, second = asyncio.run(go())
    assert first is rescue
    assert second is WALL and len(calls) == 1
    assert stealth_browser._stealth_slots_in_use == 0  # the slot is released afterwards


def test_the_slot_is_released_when_the_retry_fails_and_the_cap_follows_the_knob(monkeypatch) -> None:
    stealth_browser._stealth_slots_in_use = 0
    out, calls = _run(monkeypatch, WALL, rendered=None)
    assert out is WALL and len(calls) == 1 and stealth_browser._stealth_slots_in_use == 0
    monkeypatch.setattr(knobs, "parser_knob", lambda key, mirror: 2 if key == "stealth_max_concurrent" else mirror)
    assert stealth_browser.stealth_max_concurrent() == 2
    assert stealth_browser.try_acquire_stealth_slot() and stealth_browser.try_acquire_stealth_slot()
    assert not stealth_browser.try_acquire_stealth_slot()
    stealth_browser.release_stealth_slot()
    stealth_browser.release_stealth_slot()
    assert stealth_browser._stealth_slots_in_use == 0
