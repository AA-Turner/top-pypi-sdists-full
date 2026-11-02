"""Durable Request start, follow, resume, and timeout behavior."""

from __future__ import annotations

import httpx
import pytest

from conftest import json_response, make_async_client, make_sync_client, run_envelope
from getanyapi import AnyAPIError, RequestPendingError, RequestSnapshot, RunResult


def snapshot(status: str, *, result: object | None = None) -> dict[str, object]:
    body: dict[str, object] = {
        "requestId": "req_123",
        "sku": "email_finding.icypeas",
        "status": status,
        "createdAt": "2026-08-04T00:00:00Z",
        "retryAfterSeconds": 1,
    }
    if result is not None:
        body["result"] = result
    return body


def test_run_follows_accepted_request(monkeypatch: pytest.MonkeyPatch) -> None:
    terminal = run_envelope({"email": "hello@example.com"})

    def respond(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(202, snapshot("queued"))
        return json_response(200, snapshot("succeeded", result=terminal))

    monkeypatch.setattr("getanyapi._transport.sleep", lambda _delay: None)
    client, recorder = make_sync_client(respond)
    result = client.run("email_finding.icypeas", {"name": "Example"})

    assert result.output.found is True
    assert [request.method for request in recorder.requests] == ["POST", "GET"]


def test_start_returns_handle_and_sets_prefer() -> None:
    def respond(_request: httpx.Request) -> httpx.Response:
        return json_response(202, snapshot("queued"))

    client, recorder = make_sync_client(respond)
    handle = client.start("email_finding.icypeas", {"name": "Example"})

    assert isinstance(handle, RequestSnapshot)
    assert handle.request_id == "req_123"
    assert recorder.last.headers["prefer"] == "respond-async"


def test_start_returns_same_key_completed_replay() -> None:
    terminal = run_envelope({"email": "hello@example.com"})

    def respond(_request: httpx.Request) -> httpx.Response:
        return json_response(200, terminal)

    client, _ = make_sync_client(respond)
    started = client.start(
        "email_finding.icypeas",
        {"name": "Example"},
        options={"idempotency_key": "same-key"},
    )

    assert isinstance(started, RunResult)
    assert started.output.found is True


def test_wait_timeout_exposes_resumable_request_id() -> None:
    def respond(_request: httpx.Request) -> httpx.Response:
        return json_response(200, snapshot("running"))

    client, _ = make_sync_client(respond)
    with pytest.raises(RequestPendingError) as raised:
        client.requests.wait("req_123", timeout=0)
    assert raised.value.durable_request_id == "req_123"


def test_poll_failure_never_repeats_the_paid_post() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(202, snapshot("queued"))
        return json_response(429, {"error": "slow down"})

    client, recorder = make_sync_client(respond)
    with pytest.raises(AnyAPIError):
        client.run("email_finding.icypeas", {"name": "Example"})

    methods = [request.method for request in recorder.requests]
    assert methods.count("POST") == 1
    assert "GET" in methods


async def test_async_run_follows_accepted_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    terminal = run_envelope({"email": "hello@example.com"})

    def respond(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(202, snapshot("queued"))
        return json_response(200, snapshot("succeeded", result=terminal))

    async def no_sleep(_delay: float) -> None:
        return None

    monkeypatch.setattr("getanyapi._async_client.asyncio.sleep", no_sleep)
    client, recorder = make_async_client(respond)
    result = await client.run("email_finding.icypeas", {"name": "Example"})

    assert result.output.found is True
    assert [request.method for request in recorder.requests] == ["POST", "GET"]
