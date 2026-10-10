"""`search`'s arguments, pinned AT THE MCP TOOL-CALL BOUNDARY.

Every other search test in this suite calls ``ResearchReadService`` directly, so
none of them prove anything about how FastMCP binds arguments. That distinction
is the whole point here.

The tool was `search_knowledge` until 2026-10-08 and carried a `corpora`
argument bound only to reject (the old name of `search_in`) plus a `curated_only`
no-op; the rename removed all three outright. These tests assert the
MCP-OBSERVABLE contract, not an internal exception: tool failures travel as an
``isError`` result inside HTTP 200 (see test_mcp_threading.py's error contract),
never as a transport-level status.
"""

from __future__ import annotations

import asyncio
import json

import httpx
from mcp.server.transport_security import TransportSecuritySettings

from probe.mcp.server import create_server

_OPEN = TransportSecuritySettings(
    enable_dns_rebinding_protection=False, allowed_hosts=["*"], allowed_origins=["*"]
)
_HEADERS = {
    "Authorization": "Bearer probe_pat_test",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


class _RecordingService:
    """Captures what the tool body actually received, so a silently-dropped
    argument is visible rather than inferred from a green assertion."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def search(self, query: str, **kwargs: object) -> dict:
        self.calls.append({"query": query, **kwargs})
        return {"data": {"results": []}}


def _tool_call(name: str, arguments: dict, req_id: int = 1) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }


def _call(svc: object, arguments: dict, name: str = "search") -> dict:
    async def run() -> httpx.Response:
        mcp = create_server(svc, transport_security=_OPEN)
        mcp.settings.streamable_http_path = "/mcp"
        inner = mcp.streamable_http_app()
        async with inner.router.lifespan_context(inner):
            transport = httpx.ASGITransport(app=inner)
            async with httpx.AsyncClient(transport=transport, base_url="http://mcp.test") as c:
                return await c.post(
                    "/mcp", json=_tool_call(name, arguments), headers=_HEADERS
                )

    response = asyncio.run(run())
    assert response.status_code == 200, response.text
    body = response.text
    # streamable-http may frame the JSON-RPC body as SSE; take the data line.
    if body.lstrip().startswith("event:") or "\ndata: " in body:
        body = next(ln[len("data: ") :] for ln in body.splitlines() if ln.startswith("data: "))
    payload = json.loads(body)
    assert "result" in payload, payload
    return payload["result"]


def _error_text(result: dict) -> str:
    assert result.get("isError") is True, result
    return "".join(part.get("text", "") for part in result.get("content", []))


def test_the_tool_binds_search_in_and_semantic_through_fastmcp() -> None:
    """The positive control: what the agent sends is what the service receives."""
    svc = _RecordingService()
    result = _call(svc, {"query": "q", "search_in": ["documents"], "semantic": False})
    assert result.get("isError") is not True, result
    assert svc.calls[0]["search_in"] == ["documents"]
    assert svc.calls[0]["semantic"] is False


def test_omitting_the_filters_is_an_unfiltered_semantic_search() -> None:
    svc = _RecordingService()
    result = _call(svc, {"query": "q"})
    assert result.get("isError") is not True, result
    assert svc.calls[0]["search_in"] is None
    assert svc.calls[0]["semantic"] is True


def test_the_old_tool_name_is_gone_not_aliased() -> None:
    """`search_knowledge` was renamed outright on 2026-10-08 (no alias): a call
    to it is refused with the replacement named (`_RETIRED_TOOLS`), and the
    service never runs."""
    svc = _RecordingService()
    result = _call(svc, {"query": "q"}, name="search_knowledge")
    assert "Call `search` instead" in _error_text(result)
    assert svc.calls == []


def test_the_removed_shims_are_refused_not_silently_dropped() -> None:
    """`corpora` and `curated_only` went with the rename. The tool refuses an
    undeclared argument by name rather than ignoring it, so a stale caller is
    told instead of getting an unfiltered search."""
    for stale in ({"corpora": ["transcripts"]}, {"curated_only": True}):
        svc = _RecordingService()
        result = _call(svc, {"query": "q", **stale})
        assert next(iter(stale)) in _error_text(result)
        assert svc.calls == []


# -- strict parameter enums ----------------------------------------------------
def test_an_unknown_search_in_value_is_rejected_with_the_valid_set_named() -> None:
    """`search_in` is typed as ToolCorpus, so the vocabulary ships as a schema
    enum and pydantic rejects anything else BEFORE the tool body runs.

    The payoff is the message: it names the offending index, the bad value, and
    every accepted value. `unsupported_values` could only ever report the first
    two, and only after a network round trip.
    """
    svc = _RecordingService()
    result = _call(svc, {"query": "q", "search_in": ["bogus"]})
    text = _error_text(result)
    for valid in ("files", "documents", "transcripts", "experiments"):
        assert valid in text, text
    assert "bogus" in text, text
    assert svc.calls == []


def test_one_bad_value_rejects_the_whole_search_in_list() -> None:
    """The deliberate trade for strictness.

    Before the enum, ["documents", "bogus"] searched documents and flagged bogus
    in `unsupported_values`. Now the call fails outright. That is the accepted
    cost: the rows it used to return were for the value the caller already got
    right, and the rejection hands an LLM caller the correct vocabulary so the
    retry succeeds on the next turn.
    """
    svc = _RecordingService()
    result = _call(svc, {"query": "q", "search_in": ["documents", "bogus"]})
    assert _error_text(result)
    assert svc.calls == []


def test_an_unknown_collapse_value_is_rejected_at_the_schema() -> None:
    """Same treatment for `collapse`, which had the identical hole: a fixed
    vocabulary enforced only by a hand-written check in service.py, invisible to
    every caller reading the schema."""
    svc = _RecordingService()
    result = _call(svc, {"query": "q", "collapse": "run"})
    assert "experiment" in _error_text(result)
    assert svc.calls == []


def test_the_documented_defaults_still_bind() -> None:
    """Guards the guard: a typo in either annotation could make every ordinary
    call fail, and the rejection tests above would still pass."""
    svc = _RecordingService()
    assert _call(svc, {"query": "q"}).get("isError") is not True
    assert (
        _call(svc, {"query": "q", "search_in": ["files"], "collapse": None}).get("isError")
        is not True
    )
    assert svc.calls[-1]["search_in"] == ["files"]
    assert svc.calls[-1]["collapse"] is None


# -- entity: `filters` -> `view_options`, the same shim for the same reason -----


class _RecordingEntityService:
    """Same idea as `_RecordingService`: what did the tool body actually pass on?"""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def get_entity(self, ref, view, token_budget, cursor, filters, verbose=False) -> dict:
        self.calls.append({"ref": ref, "view": str(view), "filters": filters})
        return {"data": {"kind": "run"}, "completeness": {"state": "complete", "missing": []}}


def test_entity_accepts_the_old_filters_name_as_an_alias_for_one_release() -> None:
    """A tool that merely DROPPED `filters` would run the view's default shape
    under a success envelope -- a transcript read back whole where a grep was
    asked for. The hosted server serves sessions whose tool list predates the
    rename, so the old name is bound and HONOURED, not rejected."""
    svc = _RecordingEntityService()
    result = _call(svc, {"refs": ["run:x"], "filters": {"grep": "a"}}, name="entity")
    assert result.get("isError") is not True, result
    assert svc.calls[0]["filters"] == {"grep": "a"}


def test_entity_rejects_filters_even_when_view_options_is_also_given() -> None:
    svc = _RecordingEntityService()
    result = _call(
        svc,
        {"refs": ["run:x"], "filters": {"grep": "a"}, "view_options": {"grep": "a"}},
        name="entity",
    )
    assert "view_options" in _error_text(result)
    assert svc.calls == []


def test_entity_view_options_bind_through_fastmcp() -> None:
    svc = _RecordingEntityService()
    result = _call(svc, {"refs": ["run:x"], "view_options": {"grep": "a"}}, name="entity")
    assert result.get("isError") is not True, result
    assert svc.calls[0]["filters"] == {"grep": "a"}


def test_entity_omitting_both_is_a_plain_read_not_an_error() -> None:
    svc = _RecordingEntityService()
    result = _call(svc, {"refs": ["run:x"]}, name="entity")
    assert result.get("isError") is not True, result
    assert svc.calls[0]["filters"] is None


def test_entity_filters_is_advertised_as_deprecated_and_names_view_options() -> None:
    tools = asyncio.run(create_server(_RecordingEntityService()).list_tools())
    schema = next(t for t in tools if t.name == "entity").inputSchema
    assert schema["properties"]["filters"]["deprecated"] is True
    assert "view_options" in schema["properties"]["filters"]["description"]
    assert "view_options" in schema["properties"]
