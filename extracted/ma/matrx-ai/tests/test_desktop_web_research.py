"""desktop_web research: matrx-local's Research tool on Matrx 2 (matrx-desktop migration row
local.tool.research). Search runs on the server (the computer holds no provider key); every result is
read on the user's computer with the existing ``web.scrape`` op, in batches the op allows; the pages'
text comes back together, and nothing is invented when there is nothing to read.

The fake answers exactly as aidream's local_proxy ``POST /op/{cap.op}`` does (test_desktop_tools.py).
"""

from __future__ import annotations

import json

import httpx
import pytest
from test_desktop_tools import CLOUD, DESKTOP, _bind

from matrx_ai.tools import _sandbox_proxy as proxy
from matrx_ai.tools.arg_models.desktop_args import DesktopWebArgs
from matrx_ai.tools.implementations import desktop
from matrx_ai.tools.models import ToolContext

pytestmark = pytest.mark.asyncio


def _computer(monkeypatch: pytest.MonkeyPatch) -> list[httpx.Request]:
    """The computer's web.scrape: each URL read, its text says which page it was."""
    seen: list[httpx.Request] = []
    real = httpx.AsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        urls = json.loads(request.content)["urls"]
        pages = [
            {
                "url": u,
                "ok": "broken" not in u,
                "status": 200 if "broken" not in u else 503,
                "title": f"Title of {u}",
                "text": f"Body of {u}" if "broken" not in u else "",
                "truncated": False,
                "links": [],
                "error": None if "broken" not in u else "HTTP 503",
                "via": "http",
            }
            for u in urls
        ]
        return httpx.Response(200, json={"pages": pages, "elapsed_ms": 5})

    monkeypatch.setattr(
        proxy.httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(handler), **kw)
    )
    return seen


def _search(
    monkeypatch: pytest.MonkeyPatch, per_query: dict[str, list[str]]
) -> list[tuple[str, int]]:
    asked: list[tuple[str, int]] = []

    async def hits(query: str, count: int, freshness: str | None) -> list[dict[str, str]]:
        asked.append((query, count))
        if query == "boom":
            raise RuntimeError("provider down")
        return [{"title": f"T {u}", "url": u, "description": ""} for u in per_query.get(query, [])]

    monkeypatch.setattr(desktop, "_research_hits", hits)
    return asked


async def test_research_is_a_desktop_web_action_the_model_can_name() -> None:
    a = DesktopWebArgs(action="research", queries=["matrx"], count=3)
    assert a.action == "research"
    assert "research" in DesktopWebArgs.model_json_schema()["properties"]["action"]["enum"]


async def test_research_searches_on_the_server_and_reads_every_result_on_the_computer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _computer(monkeypatch)
    asked = _search(
        monkeypatch,
        {
            "alpha": ["https://a.example/1", "https://a.example/2", "https://shared.example/"],
            "beta": ["https://shared.example/", "https://broken.example/"],
        },
    )
    _bind(DESKTOP)
    r = await desktop.desktop_web(
        {"action": "research", "queries": ["alpha", "beta"], "count": 3},
        ToolContext(call_id="r1", tool_name="desktop_web"),
    )
    assert r.success, r.error
    assert asked == [("alpha", 3), ("beta", 3)]
    # One scrape op on the computer, every unique URL once, in rank order.
    assert [q.url.path.rsplit("/", 1)[-1] for q in seen] == ["web.scrape"]
    assert json.loads(seen[0].content)["urls"] == [
        "https://a.example/1",
        "https://a.example/2",
        "https://shared.example/",
        "https://broken.example/",
    ]
    out = r.output
    assert out["action"] == "research"
    assert out["pages_read"] == 3 and out["pages_failed"] == 1
    assert (
        "Body of https://a.example/1" in out["text"]
        and "Body of https://shared.example/" in out["text"]
    )
    failed = [p for p in out["pages"] if not p["ok"]]
    assert failed == [
        {
            "url": "https://broken.example/",
            "title": "Title of https://broken.example/",
            "ok": False,
            "error": "HTTP 503",
            "via": "http",
        }
    ]


async def test_research_reads_more_than_twenty_pages_in_batches_the_op_allows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _computer(monkeypatch)
    _search(
        monkeypatch, {f"q{i}": [f"https://p{i}-{j}.example/" for j in range(10)] for i in range(3)}
    )
    _bind(DESKTOP)
    r = await desktop.desktop_web(
        {"action": "research", "queries": ["q0", "q1", "q2"], "count": 10},
        ToolContext(call_id="r2", tool_name="desktop_web"),
    )
    assert r.success, r.error
    assert [len(json.loads(q.content)["urls"]) for q in seen] == [20, 10]
    assert r.output["pages_read"] == 30


async def test_research_with_nothing_to_read_fails_and_says_why_never_an_empty_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _computer(monkeypatch)
    _search(monkeypatch, {})
    _bind(DESKTOP)
    r = await desktop.desktop_web(
        {"action": "research", "queries": ["nothing", "boom"]},
        ToolContext(call_id="r3", tool_name="desktop_web"),
    )
    assert not r.success
    assert r.error is not None and "provider down" in r.error.message
    assert seen == []


async def test_research_without_queries_or_a_computer_sends_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _computer(monkeypatch)
    asked = _search(monkeypatch, {"x": ["https://x.example/"]})
    _bind(DESKTOP)
    r = await desktop.desktop_web(
        {"action": "research"}, ToolContext(call_id="r4", tool_name="desktop_web")
    )
    assert not r.success and r.error is not None and "queries" in r.error.message
    _bind(CLOUD)
    r = await desktop.desktop_web(
        {"action": "research", "queries": ["x"]}, ToolContext(call_id="r5", tool_name="desktop_web")
    )
    assert not r.success
    assert seen == [] and asked == []


async def test_research_saves_pages_in_the_organization_the_conversation_carries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools import organization_hold

    seen = _computer(monkeypatch)
    _search(monkeypatch, {"x": ["https://x.example/"]})
    _bind(DESKTOP)
    org = "7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11"
    monkeypatch.setattr(organization_hold, "carried_organization_id", lambda _ctx: org)
    r = await desktop.desktop_web(
        {"action": "research", "queries": ["x"]}, ToolContext(call_id="r6", tool_name="desktop_web")
    )
    assert r.success, r.error
    assert json.loads(seen[0].content)["land"] == {
        "organization_id": org,
        "keep": False,
        "attach_to": [],
    }


async def test_research_text_budget_is_the_desktop_research_knob(monkeypatch: pytest.MonkeyPatch) -> None:
    """``agents.desktop_research.text_max_chars`` (was _RESEARCH_TEXT_BUDGET): the row decides where the cut is."""
    from matrx_ai import knobs

    _computer(monkeypatch)
    _search(monkeypatch, {"q": [f"https://p{j}.example/" for j in range(20)]})
    _bind(DESKTOP)
    monkeypatch.setattr(knobs, "_reader", None)
    r = await desktop.desktop_web({"action": "research", "queries": ["q"], "count": 20},
                                  ToolContext(call_id="r9", tool_name="desktop_web"))
    assert r.success and "[Cut at" not in r.output["text"], "the seeded 60,000 holds 20 short pages"
    monkeypatch.setattr(knobs, "_reader", lambda f, k: {("agents.desktop_research", "text_max_chars"): 1_000}[(f, k)])
    r = await desktop.desktop_web({"action": "research", "queries": ["q"], "count": 20},
                                  ToolContext(call_id="r10", tool_name="desktop_web"))
    assert r.success and "[Cut at 1,000 of" in r.output["text"]
