"""RequestSizeLimitMiddleware — closes #239.

Security review of PR #238 (typed-handler dispatch) flagged that every
tool call now runs ``model_validate`` unconditionally, with no input
size bound. A hostile caller can submit arbitrarily large JSON and
exhaust CPU / memory at the validation step.

This middleware caps request body size at the ASGI boundary — before
FastMCP or a2a-sdk parses the JSON. Two patterns:

- **Content-Length fast-fail**. Client advertises a body bigger than
  the cap; reject with 413 before reading a byte.
- **Streaming accounting**. Chunked transfers (no Content-Length) are
  buffered and counted; 413 the moment the total crosses the cap.

These tests exercise the middleware directly via the ASGI protocol
(no HTTP socket, no httpx) so they're fast and deterministic.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from adcp.server._size_limit import (
    DEFAULT_MAX_REQUEST_BYTES,
    RequestSizeLimitMiddleware,
)

# ---------------------------------------------------------------------------
# ASGI test harness — minimal async scope/receive/send plumbing
# ---------------------------------------------------------------------------


def _scope(method: str, headers: Iterable[tuple[bytes, bytes]] = ()) -> dict[str, Any]:
    return {
        "type": "http",
        "method": method,
        "path": "/mcp",
        "headers": list(headers),
    }


def _body_messages(body: bytes, chunk_size: int = 0) -> list[dict[str, Any]]:
    """Produce http.request messages that carry ``body`` as one chunk
    (``chunk_size=0``) or multiple (``chunk_size=N``)."""
    if chunk_size <= 0:
        return [{"type": "http.request", "body": body, "more_body": False}]
    chunks = [body[i : i + chunk_size] for i in range(0, len(body), chunk_size)] or [b""]
    return [
        {"type": "http.request", "body": chunk, "more_body": i < len(chunks) - 1}
        for i, chunk in enumerate(chunks)
    ]


class _MockApp:
    """Records what the middleware forwarded."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        received_body = b""
        while True:
            msg = await receive()
            if msg["type"] == "http.disconnect":
                break
            if msg["type"] == "http.request":
                received_body += msg.get("body", b"")
                if not msg.get("more_body", False):
                    break
        self.calls.append({"scope": scope, "body": received_body})
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": b'{"ok": true}',
                "more_body": False,
            }
        )


async def _run(
    middleware: RequestSizeLimitMiddleware,
    scope: dict[str, Any],
    body_messages: list[dict[str, Any]],
) -> dict[str, Any]:
    """Drive the middleware once. Returns {status, body, app_saw}."""
    received = iter(body_messages)
    sent_start: dict[str, Any] | None = None
    sent_body = bytearray()

    async def receive() -> dict[str, Any]:
        try:
            return next(received)
        except StopIteration:
            return {"type": "http.disconnect"}

    async def send(msg: dict[str, Any]) -> None:
        nonlocal sent_start
        if msg["type"] == "http.response.start":
            sent_start = msg
        elif msg["type"] == "http.response.body":
            sent_body.extend(msg.get("body", b""))

    await middleware(scope, receive, send)
    return {
        "status": sent_start["status"] if sent_start else None,
        "body": bytes(sent_body),
    }


# ---------------------------------------------------------------------------
# Content-Length fast-fail
# ---------------------------------------------------------------------------


async def test_content_length_over_cap_rejects_with_413_before_reading_body():
    """**Primary guard.** A client advertising Content-Length bigger
    than the cap is rejected immediately — the middleware doesn't even
    receive the body."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=1024)

    result = await _run(
        mw,
        _scope("POST", headers=[(b"content-length", b"999999")]),
        # Body messages are provided but should never be read.
        _body_messages(b"x" * 999999),
    )

    assert result["status"] == 413
    assert b"Payload too large" in result["body"]
    assert app.calls == [], "inner app must not be invoked on oversized request"


async def test_content_length_at_cap_passes_through():
    """Boundary case. Exactly equal to the cap is allowed."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=10)

    result = await _run(
        mw,
        _scope("POST", headers=[(b"content-length", b"10")]),
        _body_messages(b"x" * 10),
    )

    assert result["status"] == 200
    assert len(app.calls) == 1
    assert app.calls[0]["body"] == b"x" * 10


async def test_malformed_content_length_falls_through_to_streaming_check():
    """A non-numeric Content-Length header shouldn't crash the
    middleware — it falls through to the streaming body check."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=100)

    result = await _run(
        mw,
        _scope("POST", headers=[(b"content-length", b"not-a-number")]),
        _body_messages(b"x" * 50),
    )

    # Body was 50 bytes, under the 100-byte cap — request succeeds.
    assert result["status"] == 200
    assert app.calls[0]["body"] == b"x" * 50


# ---------------------------------------------------------------------------
# Streaming accounting (chunked / no Content-Length)
# ---------------------------------------------------------------------------


async def test_chunked_body_exceeding_cap_mid_stream_rejects():
    """Defense-in-depth. No Content-Length header, body streamed across
    multiple chunks. Middleware totals bytes as they arrive and 413s
    the moment the total crosses the cap. The inner app must never
    see a chunk from a request that blew the budget."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=100)

    # 5 × 50 = 250 bytes total, no Content-Length.
    result = await _run(
        mw,
        _scope("POST"),
        _body_messages(b"x" * 250, chunk_size=50),
    )

    assert result["status"] == 413
    assert app.calls == []


async def test_single_chunk_exceeding_cap_rejects():
    """**Regression guard**: a single ``http.request`` message whose
    body alone exceeds the cap must still be rejected. No Content-
    Length, one giant chunk — the streaming accounting check fires
    on iteration 1. Easy to regress with a naive "read at least one
    chunk" refactor."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=100)

    result = await _run(
        mw,
        _scope("POST"),
        [{"type": "http.request", "body": b"x" * 10_000, "more_body": False}],
    )

    assert result["status"] == 413
    assert app.calls == []


async def test_413_body_includes_cap_value():
    """Legitimate clients need to know the limit they hit — the cap
    isn't a secret, and a bare "too large" forces adopters to grep
    docs. Include the number."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=1024)

    result = await _run(
        mw,
        _scope("POST", headers=[(b"content-length", b"9999")]),
        _body_messages(b""),
    )

    assert result["status"] == 413
    assert b"1024" in result["body"]
    assert b"bytes" in result["body"]


async def test_chunked_body_under_cap_passes_through():
    """Chunked body totalling less than the cap is forwarded to the
    app verbatim — inner app sees the full body reassembled."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=1000)

    payload = b"hello-world-" * 10  # 120 bytes
    result = await _run(
        mw,
        _scope("POST"),
        _body_messages(payload, chunk_size=25),
    )

    assert result["status"] == 200
    assert app.calls[0]["body"] == payload


# ---------------------------------------------------------------------------
# Bypasses — methods without bodies
# ---------------------------------------------------------------------------


async def test_get_bypasses_body_check():
    """GET requests skip the size check entirely — they don't have
    request bodies in any protocol we serve. A GET to /.well-known/
    agent.json or an MCP notifications stream must not be gated on
    Content-Length."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=1)

    # Content-Length would blow the 1-byte cap, but GET bypasses.
    result = await _run(
        mw,
        _scope("GET", headers=[(b"content-length", b"999")]),
        _body_messages(b""),
    )

    assert result["status"] == 200
    assert len(app.calls) == 1


async def test_head_and_options_bypass_body_check():
    """Same bypass for HEAD and OPTIONS — preflight and health-check
    methods never have bodies."""
    app = _MockApp()
    mw = RequestSizeLimitMiddleware(app, max_bytes=1)

    for method in ("HEAD", "OPTIONS"):
        result = await _run(
            mw,
            _scope(method, headers=[(b"content-length", b"999")]),
            _body_messages(b""),
        )
        assert result["status"] == 200, f"{method} should bypass"


# ---------------------------------------------------------------------------
# Non-HTTP scopes pass through (WebSocket, lifespan)
# ---------------------------------------------------------------------------


async def test_lifespan_scope_passes_through_untouched():
    """ASGI lifespan messages (startup/shutdown) must not be touched
    by the HTTP-body middleware — otherwise the app's startup hook
    never runs."""
    received: list[dict[str, Any]] = []

    async def lifespan_app(scope: Any, receive: Any, send: Any) -> None:
        msg = await receive()
        received.append(msg)
        await send({"type": "lifespan.startup.complete"})

    mw = RequestSizeLimitMiddleware(lifespan_app, max_bytes=10)

    scope = {"type": "lifespan"}
    messages = iter([{"type": "lifespan.startup"}])
    sent: list[dict[str, Any]] = []

    async def receive() -> dict[str, Any]:
        return next(messages)

    async def send(msg: dict[str, Any]) -> None:
        sent.append(msg)

    await mw(scope, receive, send)

    assert received == [{"type": "lifespan.startup"}]
    assert sent == [{"type": "lifespan.startup.complete"}]


# ---------------------------------------------------------------------------
# Default cap + opt-out
# ---------------------------------------------------------------------------


def test_default_cap_is_ten_megabytes():
    """The default should be big enough for realistic AdCP payloads
    (multi-package create_media_buy with creative assets) but small
    enough that adversarial traffic can't trivially exhaust validation
    CPU. 10 MB is the documented default. Regression here needs a
    deliberate doc update."""
    assert DEFAULT_MAX_REQUEST_BYTES == 10 * 1024 * 1024


async def test_zero_cap_in_wrapper_disables_middleware():
    """``serve(..., max_request_size=0)`` should skip middleware
    installation entirely — the escape hatch for sellers with
    legitimate multi-hundred-megabyte payloads. Tested at the
    wrapper layer (serve.py._wrap_with_size_limit) because the
    middleware class itself doesn't accept 0 as an opt-out."""
    from adcp.server.serve import _wrap_with_size_limit

    async def inner(scope: Any, receive: Any, send: Any) -> None:
        return None

    wrapped_none = _wrap_with_size_limit(inner, None)
    wrapped_zero = _wrap_with_size_limit(inner, 0)

    # None → wrapped with middleware (10 MB default).
    assert isinstance(wrapped_none, RequestSizeLimitMiddleware)
    # 0 → opt-out, returns the original app.
    assert wrapped_zero is inner


async def test_explicit_cap_in_wrapper_overrides_default():
    """A non-zero int overrides the 10 MB default."""
    from adcp.server.serve import _wrap_with_size_limit

    async def inner(scope: Any, receive: Any, send: Any) -> None:
        return None

    wrapped = _wrap_with_size_limit(inner, 5_000_000)
    assert isinstance(wrapped, RequestSizeLimitMiddleware)
    assert wrapped.max_bytes == 5_000_000


def test_negative_cap_raises_value_error():
    """Negative values don't have a meaningful interpretation —
    probably a typo. Fail loud at configure time instead of silently
    opting out."""
    import pytest

    from adcp.server.serve import _wrap_with_size_limit

    async def inner(scope: Any, receive: Any, send: Any) -> None:
        return None

    with pytest.raises(ValueError, match="max_request_size must be >= 0"):
        _wrap_with_size_limit(inner, -1)


async def test_zero_cap_emits_warning_log(caplog):
    """**Load-bearing breadcrumb**: a seller who configures
    ``max_request_size=0`` (typo or intentional) should see a warning
    in the startup log so they know the only Pydantic-validation DoS
    guard is disabled. A silent opt-out that only surfaces when an
    attacker finds it is the failure mode we're preventing."""
    import logging

    from adcp.server.serve import _wrap_with_size_limit

    async def inner(scope: Any, receive: Any, send: Any) -> None:
        return None

    with caplog.at_level(logging.WARNING, logger="adcp.server"):
        _wrap_with_size_limit(inner, 0)

    assert any(
        "max_request_size=0" in record.message and "disables" in record.message
        for record in caplog.records
    ), "warning log must fire when size cap is disabled"
