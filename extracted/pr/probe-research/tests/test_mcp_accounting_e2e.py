"""End to end through the REAL MCP SDK, not a stand-in inner app.

Every other accounting test substitutes its own ASGI app for the MCP server, which
leaves the load-bearing assumption untested: `note_tool` runs on an anyio worker thread
whose context is a COPY, and whether that copy still points at this request's holder
depends on WHERE the MCP SDK starts its server task. In stateless mode
`StreamableHTTPSessionManager` starts it from inside the request task, so the copy is
made there and the holder is shared. If a future SDK release moves that call -- or if
`stateless_http` is ever turned off -- every event would carry `tool=None`, `emit()`
would drop it, and the feature would go silently to zero with the whole suite green.

So this drives the actual `http_app()`: real lifespan, real JSON-RPC, real FastMCP
dispatch. The backend is unreachable on purpose (PROBE_BASE_URL points at a dead host),
because a tool that fails upstream still returns its error inside an HTTP 200 -- the
bytes still went out, so they must still be counted.
"""

from __future__ import annotations

import asyncio
import json

import pytest


def _scope(path: str = "/mcp") -> dict:
    return {
        "type": "http",
        "method": "POST",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [
            (b"authorization", b"Bearer probe_pat_smoke"),
            (b"content-type", b"application/json"),
            (b"accept", b"application/json, text/event-stream"),
            (b"x-probe-client", b"plugin"),
            (b"x-probe-client-version", b"0.44.0"),
            (b"x-probe-agent", b"claude_code"),
            (b"x-probe-agent-session", b"385cbaab-3a35-4e8f-91d7-cc57826261e4"),
        ],
        "client": ("127.0.0.1", 1),
        "scheme": "http",
        "http_version": "1.1",
        "server": ("test", 80),
        "root_path": "",
    }


async def _post(app, body: dict) -> tuple[int | None, bytes]:
    payload = json.dumps(body).encode()
    out: dict = {"status": None, "body": b""}
    sent = {"done": False}

    async def receive():
        if sent["done"]:
            return {"type": "http.disconnect"}
        sent["done"] = True
        return {"type": "http.request", "body": payload, "more_body": False}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]
        elif msg["type"] == "http.response.body":
            out["body"] += msg.get("body", b"") or b""

    await app(_scope(), receive, send)
    return out["status"], out["body"]


@pytest.fixture
def live_app(monkeypatch):
    """The real hosted app, with its lifespan running and its sender captured."""
    monkeypatch.setenv("PROBE_MCP_VERIFY_TOKEN", "0")
    monkeypatch.setenv("PROBE_MCP_TOKEN", "probe_pat_smoke")
    monkeypatch.setenv("PROBE_BASE_URL", "http://api.invalid:9")
    monkeypatch.setenv("PROBE_TELEMETRY", "on")

    from probe.mcp import accounting
    from probe.mcp.server import http_app

    monkeypatch.setenv(accounting.ANALYTICS_ENV, "1")

    captured: list[dict] = []
    sender = accounting._Sender()
    sender.put = captured.append  # type: ignore[method-assign]
    monkeypatch.setattr(accounting, "_ensure_sender", lambda: sender)

    return http_app(), captured


def _run(app, captured, steps):
    async def go():
        inbox: asyncio.Queue = asyncio.Queue()
        await inbox.put({"type": "lifespan.startup"})
        started: list[str] = []

        async def receive():
            return await inbox.get()

        async def send(msg):
            started.append(msg["type"])

        task = asyncio.create_task(app({"type": "lifespan"}, receive, send))
        for _ in range(200):
            await asyncio.sleep(0.01)
            if started:
                break
        assert started, "the MCP session manager never started"

        results = []
        for body in steps:
            results.append(await _post(app, body))
        await asyncio.sleep(0.05)

        await inbox.put({"type": "lifespan.shutdown"})
        try:
            await asyncio.wait_for(task, timeout=5)
        except Exception:
            task.cancel()
        return results

    return asyncio.run(go())


_INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "e2e", "version": "1"},
    },
}
_LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
_CALL = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {"name": "browse", "arguments": {"limit": 1}},
}
# Deliberately omits `view`. The default is what most callers get, and `card` is the
# common shape worth seeing -- so the default must be resolved, not left blank.
_ENTITY_DEFAULT_VIEW = {
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {"name": "entity", "arguments": {"refs": ["run:some-run-slug"]}},
}
_ENTITY_EXPLICIT_VIEW = {
    "jsonrpc": "2.0",
    "id": 5,
    "method": "tools/call",
    "params": {
        "name": "entity",
        "arguments": {"refs": ["run:some-run-slug"], "view": "trajectory"},
    },
}


def test_a_real_tool_call_is_counted_and_attributed(live_app) -> None:
    app, captured = live_app
    results = _run(app, captured, [_INIT, _LIST, _CALL])
    (_, _), (_, _), (status, body) = results

    assert status == 200
    assert len(captured) == 1, "the real SDK path produced no accounting event"
    entry = captured[0]
    props = entry["properties"]

    # THE assertion: the tool name crossed the real worker-thread boundary.
    assert props["tool"] == "browse", (
        "note_tool did not reach the ASGI task through the real MCP SDK -- the "
        "context-copy assumption this module rests on no longer holds"
    )
    # And the count is the actual bytes we put on the wire, not an estimate.
    assert props["response_bytes"] == len(body)
    assert props["agent"] == "claude_code"
    assert props["agent_session_id"] == "385cbaab-3a35-4e8f-91d7-cc57826261e4"
    assert props["client_kind"] == "plugin"
    assert entry["timestamp"], "no emit-time stamp: the series would be on ingest time"
    from probe.mcp.budget import count_tokens

    result = json.loads(body)["result"]
    assert "structuredContent" not in result
    assert len(result["content"]) == 1
    text = result["content"][0]["text"]
    assert props["reference_tokens"] == count_tokens(text)
    assert props["response_text_bytes"] == len(text.encode("utf-8"))
    assert props["reference_encoding"] == "o200k_base_frozen_v1"
    assert props["token_budget"] == 2000
    assert props["has_continuation"] is False
    assert {key for key in props if "token" in key.lower()} == {
        "reference_tokens", "token_budget"
    }
    assert "probe_pat_smoke" not in json.dumps(entry)
    def strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for item in value.values():
                yield from strings(item)
        elif isinstance(value, list):
            for item in value:
                yield from strings(item)

    assert not any(text in value for value in strings(entry))


def test_connect_time_traffic_is_not_counted(live_app) -> None:
    """initialize and tools/list are the excluded fixed cost. They are BIG -- roughly
    32KB together on the wire -- which is exactly why leaving them in silently would
    swamp the per-call numbers this event exists to produce."""
    app, captured = live_app
    (init_status, init_body), (list_status, list_body) = _run(app, captured, [_INIT, _LIST])

    assert init_status == 200 and list_status == 200
    assert len(init_body) > 1000 and len(list_body) > 10_000, "connect traffic got smaller?"
    assert captured == [], "connect-time traffic must not be counted"


def test_an_omitted_view_is_recorded_as_the_default(live_app) -> None:
    """Most get_entity callers never pass `view`, and the default they get is `card` --
    the compact default shape. Reading only the passed kwargs would file that
    traffic under no view at all, which is exactly the majority."""
    app, captured = live_app
    _run(app, captured, [_INIT, _ENTITY_DEFAULT_VIEW])

    assert len(captured) == 1
    props = captured[0]["properties"]
    assert props["tool"] == "entity"
    assert props["view"] == "card", (
        "the default view was not resolved -- most get_entity traffic would be unlabelled"
    )


def test_an_explicit_view_is_recorded(live_app) -> None:
    app, captured = live_app
    _run(app, captured, [_INIT, _ENTITY_EXPLICIT_VIEW])

    assert len(captured) == 1
    assert captured[0]["properties"]["view"] == "trajectory"


def test_a_tool_without_a_view_argument_carries_none(live_app) -> None:
    app, captured = live_app
    _run(app, captured, [_INIT, _CALL])

    assert len(captured) == 1
    assert "view" not in captured[0]["properties"]
