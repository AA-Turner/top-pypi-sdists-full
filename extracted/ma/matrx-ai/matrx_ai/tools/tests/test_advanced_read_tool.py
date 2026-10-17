"""The agent side of the advanced reader: the ONE hint line on failed covered pages, and the
``advanced_read`` tool that calls the host's retry door (allow=fast by default)."""

from __future__ import annotations

from typing import Any

import pytest
from matrx_scraper import _ext
from matrx_scraper.coverage import EXT_READER
from matrx_scraper.features import read_page as rp

from matrx_ai.tools.implementations.advanced_read import advanced_read
from matrx_ai.tools.implementations.web import web_read
from matrx_ai.tools.models import ToolContext

UNL = {"service": "unlocker", "label": "advanced reader", "speed": "fast", "typical_seconds": 7.0,
       "unit": "page", "points_per_unit": 30, "returns": "the full page text"}


def _ctx() -> ToolContext:
    return ToolContext(call_id="c1")


@pytest.fixture(autouse=True)
def _clean():
    saved = _ext._registry.get(EXT_READER)
    _ext._registry.pop(EXT_READER, None)
    yield
    _ext._registry.pop(EXT_READER, None)
    if saved is not None:
        _ext._registry[EXT_READER] = saved


def _reads(results: dict[str, dict[str, Any]]):
    async def fake(url: str = None, stream_handler=None, call_id=None):
        return results[url]
    return fake


async def test_web_read_adds_one_hint_line_when_failed_pages_are_covered(monkeypatch):
    wall = {"status": "error", "result": "Sorry could not access this page.", "text": "",
            "verdict": {"failed": True, "reason": "challenge", "detail": "bot check"}, "coverage": [UNL]}
    monkeypatch.setattr(rp, "read_page_mcp_quick", _reads({"https://a.example/x": wall, "https://b.example/y": wall}))
    res = await web_read({"urls": ["https://a.example/x", "https://b.example/y"]}, _ctx())
    assert res.success and len(res.model_notices) == 1
    line = res.model_notices[0]
    assert line.startswith("2 pages failed") and "advanced_read" in line and "~30 points" in line
    pages = res.output["pages"]
    assert pages[0]["coverage"][0]["service"] == "unlocker" and pages[0]["verdict"]["reason"] == "challenge"


async def test_web_read_adds_no_hint_when_nothing_failed_or_nothing_covers(monkeypatch):
    bare = {"status": "error", "result": "Sorry", "text": ""}
    monkeypatch.setattr(rp, "read_page_mcp_quick", _reads({"https://a.example/x": bare}))
    res = await web_read({"urls": ["https://a.example/x"]}, _ctx())
    assert res.success and res.model_notices == []


async def test_advanced_read_tool_calls_the_door_with_fast_by_default():
    seen: list[Any] = []

    async def door(urls, allow):
        seen.append((urls, allow))
        return [{"url": urls[0], "ok": True, "reader": "advanced reader", "seconds": 6.4, "points": 30,
                 "text": "The real page.", "message": "Read by the advanced reader. 6.4 s, 30 points."}]

    _ext.configure_ext(advanced_reader=door)
    res = await advanced_read({"urls": ["https://a.example/x"]}, _ctx())
    assert seen == [(["https://a.example/x"], "fast")]
    assert res.success and res.output["succeeded"] == 1 and res.output["points_total"] == 30
    page = res.output["pages"][0]
    assert page["reader"] == "advanced reader" and "The real page." in str(page)


async def test_advanced_read_tool_without_a_door_says_so_and_bills_nothing():
    res = await advanced_read({"urls": ["https://a.example/x"]}, _ctx())
    assert not res.success and "not set up" in res.error.message


async def test_advanced_read_tool_turns_a_points_refusal_into_a_sentence():
    class Refusal(Exception):
        code = "usage_limit"
        user_message = "You've used all your points for now. Upgrade your plan to keep going."

    async def door(urls, allow):
        raise Refusal()

    _ext.configure_ext(advanced_reader=door)
    res = await advanced_read({"urls": ["https://a.example/x"]}, _ctx())
    assert not res.success and res.error.message.startswith("You've used all your points")
    assert "Do not retry" in (res.error.suggested_action or "")


async def test_the_agent_tool_is_fast_only_and_cannot_ask_for_slow_data():
    """Owner rule: slow structured datasets only on a person's click. The tool has no ``allow`` argument and
    always calls the door with "fast"; a model that sends allow="all" is refused before anything runs."""
    from pydantic import ValidationError

    from matrx_ai.tools.arg_models.web_args import AdvancedReadArgs

    assert "allow" not in AdvancedReadArgs.model_fields
    seen: list[Any] = []

    async def door(urls, allow):
        seen.append(allow)
        return []

    _ext.configure_ext(advanced_reader=door)
    with pytest.raises(ValidationError):
        await advanced_read({"urls": ["https://a.example/x"], "allow": "all"}, _ctx())
    assert seen == []
    await advanced_read({"urls": ["https://a.example/x"]}, _ctx())
    assert seen == ["fast"]
