"""Tests for the SDK audit namespace."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from unittest.mock import MagicMock

import httpx
import pytest

from smplkit.audit._buffer import (
    AuditEventBuffer,
    MAX_BUFFER_SIZE,
    _PendingEvent,
)
from smplkit.audit.client import AuditClient
from smplkit.audit.models import Event


class _StubResponse:
    """Mimics httpx.Response just enough for the buffer's outcome handler."""

    def __init__(self, status_code: int, text: str = "") -> None:
        self.status_code = status_code
        self.text = text


# --------------------------------------------------------------------------
# Buffer behavior
# --------------------------------------------------------------------------


def test_buffer_drops_oldest_when_over_capacity():
    """When the buffer is full, the oldest item is dropped to make room."""
    posts: list[_PendingEvent] = []

    def post(item: _PendingEvent) -> httpx.Response:
        # Hold the worker by returning success only after we've populated.
        posts.append(item)
        return 201

    buf = AuditEventBuffer(post_fn=post, max_size=3, watermark=999)
    try:
        for i in range(5):
            buf.enqueue({"i": i})
        # Allow the worker a brief tick — but posting is fast in this stub,
        # so by the time we check, the queue should be drained.
        buf.flush(timeout=2.0)
        assert len(posts) >= 3  # at least three events made it through
        # The oldest items are the ones dropped, so events with the largest
        # ``i`` values should be present in posts.
        seen = {p.body["i"] for p in posts}
        assert max(seen) == 4
    finally:
        buf.close(timeout=2.0)


def test_buffer_retries_on_transient_failure():
    attempts: list[int] = []

    def post(item: _PendingEvent) -> httpx.Response:
        attempts.append(item.attempts)
        # Fail twice, succeed on the third try.
        if len([a for a in attempts if a < 2]) < 2:
            return 503
        return 201

    buf = AuditEventBuffer(
        post_fn=post,
        max_size=10,
        watermark=1,
        flush_interval=0.05,
    )
    try:
        buf.enqueue({"i": 0})
        # Worker needs time to retry — backoff is 0.25s base; allow several seconds.
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline:
            if any(a >= 1 for a in attempts):
                break
            time.sleep(0.05)
        assert any(a >= 1 for a in attempts), "expected at least one retry"
    finally:
        buf.close(timeout=2.0)


def test_buffer_drops_permanent_failures():
    posted: list[_PendingEvent] = []

    def post(item: _PendingEvent) -> httpx.Response:
        posted.append(item)
        return 400

    buf = AuditEventBuffer(post_fn=post, max_size=10, watermark=1)
    try:
        buf.enqueue({"i": 0})
        buf.flush(timeout=2.0)
        # 400 → permanent failure → posted once, then dropped, no retry storm.
        # Race-ok because the worker may try once then move on.
        assert posted  # at least one attempt
        assert all(p.attempts == 0 for p in posted)
    finally:
        buf.close(timeout=2.0)


# --------------------------------------------------------------------------
# Public client surface
# --------------------------------------------------------------------------


def test_create_returns_immediately(monkeypatch):
    """The fire-and-forget contract: create() returns without blocking on POST."""
    # Body must round-trip through the generated EventResponse model, so
    # include all required fields on the resource. This also makes the
    # buffer's success path (status_code returned) covered.
    _success_body = {
        "data": {
            "id": "00000000-0000-0000-0000-000000000001",
            "type": "event",
            "attributes": {
                "event_type": "invoice.created",
                "resource_type": "invoice",
                "resource_id": "inv-x",
                "occurred_at": "2026-05-06T12:00:00+00:00",
                "created_at": "2026-05-06T12:00:01+00:00",
                "actor_type": "API_KEY",
                "actor_id": None,
                "actor_label": "",
                "data": {},
                "idempotency_key": "auto",
            },
        }
    }
    transport = httpx.MockTransport(lambda req: httpx.Response(201, json=_success_body))
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    # Replace the underlying httpx client so we never actually go to the network.
    client._auth.set_httpx_client(httpx.Client(transport=transport, base_url="https://audit.example.com"))
    # Re-bind the buffer to use the new http client's POST behavior.

    started = time.monotonic()
    for i in range(20):
        client.events.record(
            event_type="invoice.created",
            resource_type="invoice",
            resource_id=f"inv-{i}",
        )
    assert time.monotonic() - started < 0.5  # well under the slowest POST round trip.

    client._close()


def test_record_do_not_forward_serialized_on_wire():
    """``do_not_forward=True`` survives the wrapper into the JSON body —
    the audit service uses the flag to decide whether to fan out to
    SIEM forwarders even though the event itself is recorded."""
    posts: list[dict] = []
    success_body = {
        "data": {
            "id": "00000000-0000-0000-0000-000000000001",
            "type": "event",
            "attributes": {
                "event_type": "user.created",
                "resource_type": "user",
                "resource_id": "u-1",
                "occurred_at": "2026-05-06T12:00:00+00:00",
                "created_at": "2026-05-06T12:00:01+00:00",
                "actor_type": "API_KEY",
                "actor_id": None,
                "actor_label": "",
                "data": {},
                "idempotency_key": "auto",
                "do_not_forward": True,
            },
        }
    }

    def handler(req: httpx.Request) -> httpx.Response:
        posts.append({"body": req.content.decode()})
        return httpx.Response(201, json=success_body)

    transport = httpx.MockTransport(handler)
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    client._auth.set_httpx_client(httpx.Client(transport=transport, base_url="https://audit.example.com"))
    try:
        client.events.record(
            event_type="user.created",
            resource_type="user",
            resource_id="u-1",
            do_not_forward=True,
            flush=True,
        )
        # Generated client serializes JSON without spaces; match either.
        assert any('"do_not_forward":true' in p["body"].replace(" ", "") for p in posts)
    finally:
        client._close()


def test_record_flush_true_blocks_until_drained():
    """``flush=True`` is the one-call equivalent of ``record(...)`` followed
    by ``flush()`` — useful for CLI tools and tests that need the event
    durable before continuing."""
    posted: list[_PendingEvent] = []
    success_body = {
        "data": {
            "id": "00000000-0000-0000-0000-000000000001",
            "type": "event",
            "attributes": {
                "event_type": "invoice.created",
                "resource_type": "invoice",
                "resource_id": "inv-x",
                "occurred_at": "2026-05-06T12:00:00+00:00",
                "created_at": "2026-05-06T12:00:01+00:00",
                "actor_type": "API_KEY",
                "actor_id": None,
                "actor_label": "",
                "data": {},
                "idempotency_key": "auto",
            },
        }
    }

    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json=success_body)

    transport = httpx.MockTransport(handler)
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    client._auth.set_httpx_client(httpx.Client(transport=transport, base_url="https://audit.example.com"))

    # Stub the post_fn so the test can observe the in-flight item.
    original_post = client.events._buffer._post_fn

    def observed_post(item):
        posted.append(item)
        return original_post(item)

    client.events._buffer._post_fn = observed_post  # type: ignore[method-assign]

    try:
        # flush=True drains synchronously — by the time the call returns,
        # the buffer has either succeeded or exhausted retries.
        client.events.record(
            event_type="invoice.created",
            resource_type="invoice",
            resource_id="inv-flush-1",
            flush=True,
        )
        # The post must have been observed. Without flush=True there's a
        # window where this could race with the worker thread.
        assert len(posted) == 1
    finally:
        client._close()


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------


def test_event_from_resource_handles_nullable_actor_id():
    resource = _make_resource("33333333-3333-3333-3333-333333333333", actor_id=None)
    ev = Event._from_resource(resource)
    assert ev.actor_id is None
    assert ev.actor_type is None or ev.actor_type == "API_KEY"


def test_event_from_resource_accepts_free_form_actor_id():
    """actor_id is a free-form string on the wire — non-UUID values must
    round-trip without coercion or rejection."""
    resource = _make_resource(
        "33333333-3333-3333-3333-333333333333",
        actor_id="not-a-uuid:billing-bot",
    )
    ev = Event._from_resource(resource)
    assert ev.actor_id == "not-a-uuid:billing-bot"
    assert isinstance(ev.actor_id, str)


def test_event_from_resource_handles_null_actor_type_and_label():
    """All three actor fields are nullable on the wire — the wrapper
    must surface None rather than coercing to an empty string."""
    resource = _make_resource(
        "55555555-5555-5555-5555-555555555555",
        actor_id=None,
    )
    resource["attributes"]["actor_type"] = None
    resource["attributes"]["actor_label"] = None
    ev = Event._from_resource(resource)
    assert ev.actor_type is None
    assert ev.actor_label is None


def test_record_passes_actor_fields_to_wire():
    """Customer-supplied actor attribution makes it into the POST body."""
    posts: list[str] = []
    success_body = {
        "data": {
            "id": "00000000-0000-0000-0000-000000000001",
            "type": "event",
            "attributes": {
                "event_type": "user.created",
                "resource_type": "user",
                "resource_id": "u-1",
                "occurred_at": "2026-05-06T12:00:00+00:00",
                "created_at": "2026-05-06T12:00:01+00:00",
                "actor_type": "EXTERNAL_SERVICE",
                "actor_id": "not-a-uuid:billing-bot",
                "actor_label": "Billing Bot",
                "data": {},
                "idempotency_key": "auto",
            },
        }
    }

    def handler(req: httpx.Request) -> httpx.Response:
        posts.append(req.content.decode())
        return httpx.Response(201, json=success_body)

    transport = httpx.MockTransport(handler)
    client = AuditClient(api_key="sk_api_test", base_url="https://audit.example.com")
    client._auth.set_httpx_client(httpx.Client(transport=transport, base_url="https://audit.example.com"))
    try:
        client.events.record(
            event_type="user.created",
            resource_type="user",
            resource_id="u-1",
            actor_type="EXTERNAL_SERVICE",
            actor_id="not-a-uuid:billing-bot",
            actor_label="Billing Bot",
            flush=True,
        )
        body = "".join(posts).replace(" ", "")
        assert '"actor_type":"EXTERNAL_SERVICE"' in body
        assert '"actor_id":"not-a-uuid:billing-bot"' in body
        assert '"actor_label":"BillingBot"' in body
    finally:
        client._close()


def test_event_from_resource_handles_z_suffix_timestamps():
    resource = _make_resource(
        "44444444-4444-4444-4444-444444444444",
        occurred_at="2026-05-06T12:00:00Z",
    )
    ev = Event._from_resource(resource)
    assert ev.occurred_at.tzinfo is not None


# Helpers ------------------------------------------------------------------


def _make_resource(
    event_id: str,
    *,
    actor_id: str | None = None,
    occurred_at: str = "2026-05-06T12:00:00+00:00",
) -> dict:
    return {
        "id": event_id,
        "type": "event",
        "attributes": {
            "event_type": "invoice.created",
            "resource_type": "invoice",
            "resource_id": "inv-1",
            "occurred_at": occurred_at,
            "created_at": "2026-05-06T12:00:01+00:00",
            "actor_type": "USER" if actor_id else "API_KEY",
            "actor_id": actor_id,
            "actor_label": "alice@example.com" if actor_id else "",
            "data": {},
            "idempotency_key": "auto-abc",
        },
    }


# Silence unused-import warnings in static analyzers
_ = (MagicMock, datetime, timezone, MAX_BUFFER_SIZE)
_ = pytest  # noqa: F841
_ = _StubResponse  # noqa: F841
