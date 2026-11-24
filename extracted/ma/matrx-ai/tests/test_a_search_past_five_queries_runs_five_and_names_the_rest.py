"""More than five web queries run the first five and name the rest (C87 round 2 / C94).

OpenAI strict mode strips ``maxItems`` from the advertised schema, so no text stops a model sending 6-10 queries
(live 2026-11-09: 5 refusals). Refusing the whole search wasted the turn; now it runs five and says which were not.
"""

from __future__ import annotations

import asyncio
import sys
import types
from typing import Any

from matrx_ai.tools.arg_models.web_args import WebArgs, WebSearchWire


def test_the_wire_takes_more_than_five_and_still_advertises_five() -> None:
    wire = WebSearchWire(action="search", queries=[f"q{i}" for i in range(8)])
    assert len(wire.queries) == 8
    assert WebSearchWire.model_json_schema()["properties"]["queries"]["maxItems"] == 5
    WebArgs.model_validate({"action": "search", "queries": [f"q{i}" for i in range(8)]})


def test_the_search_runs_five_and_names_the_skipped(monkeypatch) -> None:
    ran: list[str] = []

    async def fake_quick(*, queries: list[str], **_: Any) -> dict[str, Any]:
        ran.extend(queries)
        return {"status": "success", "result": f"result for {queries[0]}"}

    mod = types.ModuleType("matrx_scraper.features.quick_search")
    mod.search_web_mcp_quick = fake_quick
    monkeypatch.setitem(sys.modules, "matrx_scraper.features.quick_search", mod)

    from matrx_ai.tools.implementations import web as web_impl

    class _Stream:
        def __init__(self, *_: Any) -> None: ...
        async def progress(self, *_: Any, **__: Any) -> None: ...

    monkeypatch.setattr(web_impl, "ToolStreamManager", _Stream)
    ctx = types.SimpleNamespace(emitter=None, call_id="c1")
    result = asyncio.run(web_impl.web_search({"queries": [f"q{i}" for i in range(7)]}, ctx))
    assert result.success
    assert ran == ["q0", "q1", "q2", "q3", "q4"]
    assert "Not searched" in result.output and '"q5", "q6"' in result.output
