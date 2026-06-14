"""Coverage-targeted tests for the audit namespace.

Fills in branches that ``test_audit.py`` doesn't directly exercise so the
100% line-coverage gate stays green: list filter passthrough, get error
paths, AsyncAuditClient delegation, _build_attributes' optional data
and data fields, and the buffer's gave-up + safe-body paths.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from unittest.mock import MagicMock

import httpx

from smplkit.audit._buffer import (
    AuditEventBuffer,
    MAX_ATTEMPTS_PER_ITEM,
    _PendingEvent,
)
from smplkit.audit.clients import AsyncAuditClient, AuditClient


def test_buffer_enqueue_silent_when_closed() -> None:
    buf = AuditEventBuffer(post_fn=lambda item: 201)
    buf.close(timeout=1.0)
    # No-op: enqueue on a closed buffer just returns.
    buf.enqueue({"x": 1})


def test_buffer_flush_warns_on_timeout() -> None:
    """Hold one item in the queue and flush below the retry backoff."""
    attempts: list[int] = []

    def post(item: _PendingEvent) -> httpx.Response:
        attempts.append(item.attempts)
        return 503

    buf = AuditEventBuffer(post_fn=post, max_size=10, watermark=999)
    try:
        buf.enqueue({"i": 1})
        # Flush below the 250ms backoff so the queue stays non-empty.
        start = time.monotonic()
        buf.flush(timeout=0.05)
        assert time.monotonic() - start >= 0.04
    finally:
        buf.close(timeout=2.0)


def test_buffer_gives_up_after_max_attempts() -> None:
    attempts = [0]

    def post(item: _PendingEvent) -> httpx.Response:
        attempts[0] += 1
        return 503

    buf = AuditEventBuffer(
        post_fn=post,
        max_size=10,
        watermark=1,
        flush_interval=0.025,
    )
    try:
        buf.enqueue({"i": 1})
        deadline = time.monotonic() + 8.0
        while time.monotonic() < deadline:
            if attempts[0] >= MAX_ATTEMPTS_PER_ITEM:
                break
            time.sleep(0.05)
        assert attempts[0] >= MAX_ATTEMPTS_PER_ITEM
    finally:
        buf.close(timeout=2.0)


def test_buffer_post_raising_treated_as_transient() -> None:
    calls = [0]

    def post(item: _PendingEvent):
        calls[0] += 1
        if calls[0] == 1:
            raise RuntimeError("simulated network blip")
        return 201

    buf = AuditEventBuffer(post_fn=post, max_size=10, watermark=1, flush_interval=0.05)
    try:
        buf.enqueue({"i": 1})
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if calls[0] >= 2:
                break
            time.sleep(0.05)
        assert calls[0] >= 2
    finally:
        buf.close(timeout=2.0)


# --------------------------------------------------------------------------
# AuditClient — branches not exercised in test_audit.py
# --------------------------------------------------------------------------


def test_create_nests_snapshot_inside_data() -> None:
    """Snapshots are recorded by nesting inside ``data``; the SDK does not
    expose a separate ``snapshot`` parameter and the wire body has no
    top-level ``snapshot`` attribute."""
    import json as _json

    seen_bodies: list[dict] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen_bodies.append(_json.loads(req.read()))
        return httpx.Response(
            201,
            json={
                "data": {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "type": "event",
                    "attributes": {
                        "event_type": "invoice.created",
                        "resource_type": "invoice",
                        "resource_id": "inv-1",
                        "occurred_at": "2026-05-06T12:00:00+00:00",
                        "created_at": "2026-05-06T12:00:01+00:00",
                        "actor_type": "API_KEY",
                        "actor_id": None,
                        "actor_label": "",
                        "data": {"snapshot": {"total_cents": 4900}, "request_id": "req-1"},
                        "idempotency_key": "k-1",
                    },
                }
            },
        )

    transport = httpx.MockTransport(handler)
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    client._auth.set_httpx_client(httpx.Client(transport=transport, base_url="https://audit.example.com"))
    try:
        client.events.record(
            event_type="invoice.created",
            resource_type="invoice",
            resource_id="inv-1",
            occurred_at=datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc),
            data={"snapshot": {"total_cents": 4900}, "request_id": "req-1"},
            idempotency_key="k-1",
        )
        client.events.flush(timeout=2.0)
        assert seen_bodies, "the buffer should have flushed at least one body"
        attrs = seen_bodies[0]["data"]["attributes"]
        assert "snapshot" not in attrs
        assert attrs["data"] == {
            "snapshot": {"total_cents": 4900},
            "request_id": "req-1",
        }
        assert attrs["occurred_at"].startswith("2026-05-06T12:00:00")
    finally:
        client._close()


def test_post_wrapper_returns_httpx_error_on_connection_failure() -> None:
    """Cover the audit client's POST-wrapper try/except (lines 80-81).

    A transport that raises httpx.ConnectError on every request forces
    the buffer's post wrapper into its except branch, where it returns
    the exception. The buffer reads it as transient and retries — we
    just need to assert at least one round-trip happened.
    """
    calls = [0]

    def handler(req: httpx.Request) -> httpx.Response:
        calls[0] += 1
        raise httpx.ConnectError("simulated connect failure")

    transport = httpx.MockTransport(handler)
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    client._auth.set_httpx_client(httpx.Client(transport=transport, base_url="https://audit.example.com"))
    try:
        client.events.record(event_type="x", resource_type="y", resource_id="1")
        # Force a drain pass via flush; the wrapper's except clause runs.
        client.events.flush(timeout=0.5)
        assert calls[0] >= 1
    finally:
        client._close()


def test_async_client_owns_its_own_genuinely_async_surface() -> None:
    """The async client is no longer a sync delegate — it builds its own
    transport and async sub-clients (no ``_inner``)."""
    from smplkit.audit.clients import AsyncEventsClient

    client = AsyncAuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    assert not hasattr(client, "_inner")
    assert isinstance(client.events, AsyncEventsClient)
    assert client._owns_transport is True
    import asyncio

    asyncio.run(client._close())


def test_audit_client_extra_headers_reach_transport() -> None:
    """extra_headers are stored on _auth and applied as defaults to every request."""
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com", extra_headers={"X-Test": "v"})
    assert client._auth._headers.get("X-Test") == "v"
    client._close()


def test_audit_client_context_manager_closes_owned_transport() -> None:
    """The public close()/context manager tears down an owned transport."""
    with AuditClient(api_key="sk_api_test", base_url="https://audit.example.com") as client:
        assert client._owns_transport is True
        client._auth.set_httpx_client(
            httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(204)), base_url="https://e.com")
        )
    # __exit__ -> close() -> _close(): owned transport closed.
    assert client._auth.get_httpx_client().is_closed


def test_audit_client_borrowed_transport_not_closed() -> None:
    """An injected (borrowed) transport is never closed by the audit client —
    the owning client handles teardown."""
    from smplkit._generated.audit.client import AuthenticatedClient as _AuditAuthClient

    auth = _AuditAuthClient(base_url="https://audit.example.com", token="sk_api_test")
    auth.set_httpx_client(
        httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(204)), base_url="https://e.com")
    )
    client = AuditClient(auth_client=auth)
    assert client._owns_transport is False
    client._close()  # closes the buffer only; must NOT close the borrowed transport
    assert auth._client is not None


def test_audit_client_standalone_resolves_transport() -> None:
    """Constructing without base_url forces the config-resolution path in
    ``_audit_transport`` (resolves the audit URL from base_domain)."""
    client = AuditClient(api_key="sk_api_test", base_domain="example.com", scheme="https", environment="prod")
    assert client._owns_transport is True
    # Environment routes through the body / filter[environment], not a header.
    assert "X-Smplkit-Environment" not in client._auth._headers
    assert client._environment == "prod"
    assert "audit.example.com" in str(client._auth._base_url)
    client._close()


def test_async_audit_client_extra_headers_reach_transport() -> None:
    """The async client stamps extra_headers on its own transport."""
    client = AsyncAuditClient(
        api_key="sk_api_test", base_url="https://audit.example.com", extra_headers={"X-Test": "v"}
    )
    assert client._auth._headers.get("X-Test") == "v"
    import asyncio

    asyncio.run(client._close())


_ = MagicMock  # silence unused-import warnings on aggressive linters
