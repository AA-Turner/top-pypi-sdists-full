"""Wire shape, query params, and retry policy (SPEC 2.2, 2.8)."""

from __future__ import annotations

import json

import httpx
import pytest

from getanyapi import ConnectionError, RateLimitedError, TimeoutError
from conftest import (
    json_response,
    make_async_client,
    make_sync_client,
    run_envelope,
)


def test_wire_shape_and_headers() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond)
    client.run("amazon.reviews", {"product": "B07", "limit": 3})

    req = rec.last
    assert req.method == "POST"
    assert req.url.path == "/v1/run/amazon.reviews"
    assert req.headers["authorization"] == "Bearer test-key"
    assert req.headers["content-type"] == "application/json"
    assert req.headers["accept"] == "application/json"
    assert json.loads(req.content) == {"product": "B07", "limit": 3}


def test_query_shaping_params() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond)
    client.run(
        "x.y",
        {},
        options={"fields": ["a", "b"], "max_items": 5, "summary": True},
    )
    q = rec.last.url.params
    assert q["fields"] == "a,b"
    assert q["max_items"] == "5"
    assert q["summary"] == "true"


def test_no_query_params_when_unset() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond)
    client.run("x.y", {})
    assert str(rec.last.url.params) == ""


def test_idempotency_key_and_body_bytes_are_stable_across_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)
    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return json_response(429, {"error": "slow down"})
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond, max_retries=1)
    client.run("x.y", {"b": 2, "a": 1})

    assert len(rec.requests) == 2
    assert rec.requests[0] is rec.requests[1]
    assert rec.requests[0].headers["idempotency-key"] == rec.requests[1].headers[
        "idempotency-key"
    ]
    assert rec.requests[0].content == rec.requests[1].content


def test_fresh_idempotency_key_for_each_new_call() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond)
    client.run("x.y", {})
    client.run("x.y", {})

    assert rec.requests[0].headers["idempotency-key"] != rec.requests[1].headers[
        "idempotency-key"
    ]


def test_per_request_idempotency_key_override() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond)
    client.run("x.y", {}, options={"idempotency_key": "customer-key"})

    assert rec.last.headers["idempotency-key"] == "customer-key"


def test_idempotency_kill_switch_omits_header() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond, idempotency="off")
    client.run("x.y", {}, options={"idempotency_key": "customer-key"})

    assert "idempotency-key" not in rec.last.headers


def test_retry_on_429_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    import getanyapi._transport as transport

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))

    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return json_response(429, {"error": "slow down"})
        return json_response(200, run_envelope({"ok": True}))

    client, _ = make_sync_client(respond, max_retries=2)
    result = client.run("x.y", {})
    assert result.output.found is True
    assert calls["n"] == 3  # 1 + 2 retries
    assert len(slept) == 2


def test_retry_exhausted_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(429, {"error": "slow"})

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(RateLimitedError):
        client.run("x.y", {})
    assert len(rec.requests) == 3


def test_no_retry_on_400(monkeypatch: pytest.MonkeyPatch) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(400, {"error": "bad"})

    from getanyapi import BadRequestError

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(BadRequestError):
        client.run("x.y", {})
    assert len(rec.requests) == 1  # no retry


def test_retry_after_header_honored(monkeypatch: pytest.MonkeyPatch) -> None:
    import getanyapi._transport as transport

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))

    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return json_response(
                429, {"error": "wait"}, headers={"retry-after": "2"}
            )
        return json_response(200, run_envelope({"ok": True}))

    client, _ = make_sync_client(respond, max_retries=1)
    client.run("x.y", {})
    assert slept == [2.0]


def test_retry_after_capped_at_max_delay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))

    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return json_response(
                429, {"error": "wait"}, headers={"retry-after": "9999"}
            )
        return json_response(200, run_envelope({"ok": True}))

    client, _ = make_sync_client(respond, max_retries=1)
    client.run("x.y", {})
    assert slept == [8.0]  # capped at maxDelay


def test_timeout_not_retried() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(TimeoutError) as exc:
        client.run("x.y", {})
    assert exc.value.status == 0
    assert len(rec.requests) == 1  # timeouts never retried


def test_pre_send_connect_error_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    calls = {"n": 0}

    def respond(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("refused", request=req)
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_sync_client(respond, max_retries=2)
    result = client.run("x.y", {})
    assert result.output.found is True
    assert len(rec.requests) == 2


def test_idempotent_get_retries_post_send_read_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)
    calls = {"n": 0}

    def respond(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ReadError("response reset", request=req)
        return json_response(200, {"usd": 1.25})

    client, rec = make_sync_client(respond, max_retries=1)
    result = client.balance()
    assert result.usd == 1.25
    assert len(rec.requests) == 2
    assert "idempotency-key" not in rec.requests[0].headers


def test_billed_post_does_not_retry_post_send_read_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(req: httpx.Request) -> httpx.Response:
        raise httpx.ReadError("response reset", request=req)

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(ConnectionError) as exc:
        client.run("x.y", {"query": "sent"})
    assert exc.value.status == 0
    assert len(rec.requests) == 1


def test_per_request_max_retries_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(429, {"error": "slow"})

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(RateLimitedError):
        client.run("x.y", {}, options={"max_retries": 0})
    assert len(rec.requests) == 1  # override wins


async def test_async_retry_on_429(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio

    slept: list[float] = []

    async def fake_sleep(s: float) -> None:
        slept.append(s)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return json_response(429, {"error": "slow"})
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_async_client(respond, max_retries=2)
    result = await client.run("x.y", {})
    assert result.output.found is True
    assert len(rec.requests) == 3
    assert len(slept) == 2
    await client.aclose()


async def test_async_idempotency_key_reused_across_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    async def fake_sleep(_s: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return json_response(429, {"error": "slow"})
        return json_response(200, run_envelope({"ok": True}))

    client, rec = make_async_client(respond, max_retries=1)
    await client.run("x.y", {"query": "stable"})

    assert len(rec.requests) == 2
    assert rec.requests[0] is rec.requests[1]
    assert rec.requests[0].headers["idempotency-key"] == rec.requests[1].headers[
        "idempotency-key"
    ]
    assert rec.requests[0].content == rec.requests[1].content
    await client.aclose()


async def test_async_timeout_not_retried() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    client, rec = make_async_client(respond, max_retries=2)
    with pytest.raises(TimeoutError):
        await client.run("x.y", {})
    assert len(rec.requests) == 1
    await client.aclose()


async def test_async_idempotent_get_retries_post_send_read_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    async def fake_sleep(_s: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    calls = {"n": 0}

    def respond(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ReadError("response reset", request=req)
        return json_response(200, {"usd": 1.25})

    client, rec = make_async_client(respond, max_retries=1)
    result = await client.balance()
    assert result.usd == 1.25
    assert len(rec.requests) == 2
    await client.aclose()


async def test_async_billed_post_does_not_retry_post_send_read_error() -> None:
    def respond(req: httpx.Request) -> httpx.Response:
        raise httpx.ReadError("response reset", request=req)

    client, rec = make_async_client(respond, max_retries=2)
    with pytest.raises(ConnectionError):
        await client.run("x.y", {"query": "sent"})
    assert len(rec.requests) == 1
    await client.aclose()


# -- 409 idempotency_in_progress (SPEC 2.8) -------------------------------


def in_progress_response(retry_after: str | None = "30") -> httpx.Response:
    """The gateway's 409 for a key whose run is still executing."""
    headers = {"retry-after": retry_after} if retry_after is not None else None
    return json_response(
        409,
        {
            "error": "a request with this idempotency key is still in progress",
            "code": "idempotency_in_progress",
        },
        headers=headers,
    )


def test_in_progress_409_retries_then_replays(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))
    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return in_progress_response()
        return json_response(200, run_envelope({"ok": True}, replayed=True))

    client, rec = make_sync_client(respond)
    result = client.run("x.y", {"query": "sent"})

    assert result.replayed is True
    assert result.output.found is True
    assert len(rec.requests) == 2
    # The full 30s the server asked for, NOT the 8s ordinary-backoff ceiling.
    assert slept == [30.0]


def test_in_progress_409_reuses_the_same_idempotency_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    monkeypatch.setattr(transport, "sleep", lambda _s: None)
    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return in_progress_response()
        return json_response(200, run_envelope({"ok": True}, replayed=True))

    client, rec = make_sync_client(respond)
    client.run("x.y", {"query": "sent"})

    assert rec.requests[0] is rec.requests[1]
    assert (
        rec.requests[0].headers["idempotency-key"]
        == rec.requests[1].headers["idempotency-key"]
    )


def test_idempotency_conflict_409_is_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(
            409,
            {
                "error": "this key was already used for a different request",
                "code": "idempotency_conflict",
            },
            headers={"retry-after": "30"},
        )

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(AnyAPIError) as exc:
        client.run("x.y", {"query": "sent"})
    assert exc.value.status == 409
    assert exc.value.code == "idempotency_conflict"
    assert len(rec.requests) == 1


def test_idempotency_needs_review_409_is_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(
            409,
            {"error": "needs review", "code": "idempotency_needs_review"},
        )

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(AnyAPIError):
        client.run("x.y", {"query": "sent"})
    assert len(rec.requests) == 1


def test_uncoded_409_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(409, {"error": "conflict"})

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(AnyAPIError):
        client.run("x.y", {"query": "sent"})
    assert len(rec.requests) == 1


def test_in_progress_retry_after_over_budget_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))

    def respond(_req: httpx.Request) -> httpx.Response:
        return in_progress_response("3600")

    client, rec = make_sync_client(respond, max_retries=2)
    with pytest.raises(AnyAPIError) as exc:
        client.run("x.y", {"query": "sent"})
    assert exc.value.code == "idempotency_in_progress"
    assert len(rec.requests) == 1  # no attempt burned on a wait that is too long
    assert slept == []


def test_in_progress_budget_stops_before_max_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))

    def respond(_req: httpx.Request) -> httpx.Response:
        return in_progress_response()

    client, rec = make_sync_client(respond, max_retries=5)
    with pytest.raises(AnyAPIError):
        client.run("x.y", {"query": "sent"})
    # 30s + 30s spends the 60s default budget; a third wait is unaffordable.
    assert slept == [30.0, 30.0]
    assert len(rec.requests) == 3


def test_max_in_progress_wait_client_and_request_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))

    def respond(_req: httpx.Request) -> httpx.Response:
        return in_progress_response()

    client, rec = make_sync_client(
        respond, max_retries=5, max_in_progress_wait=30.0
    )
    with pytest.raises(AnyAPIError):
        client.run("x.y", {"query": "sent"})
    assert slept == [30.0]
    assert len(rec.requests) == 2

    strict, rec2 = make_sync_client(respond, max_retries=5)
    with pytest.raises(AnyAPIError):
        strict.run("x.y", {"query": "sent"}, options={"max_in_progress_wait": 0})
    assert len(rec2.requests) == 1


def test_in_progress_without_retry_after_uses_ordinary_backoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport

    slept: list[float] = []
    monkeypatch.setattr(transport, "sleep", lambda s: slept.append(s))
    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return in_progress_response(None)
        return json_response(200, run_envelope({"ok": True}, replayed=True))

    client, rec = make_sync_client(respond)
    client.run("x.y", {"query": "sent"})
    assert len(rec.requests) == 2
    assert len(slept) == 1
    assert 0.25 <= slept[0] <= 0.75  # jittered 500ms base, not 30s


def test_in_progress_respects_max_retries_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import getanyapi._transport as transport
    from getanyapi import AnyAPIError

    monkeypatch.setattr(transport, "sleep", lambda _s: None)

    def respond(_req: httpx.Request) -> httpx.Response:
        return in_progress_response()

    client, rec = make_sync_client(respond, max_retries=5)
    with pytest.raises(AnyAPIError):
        client.run("x.y", {}, options={"max_retries": 0})
    assert len(rec.requests) == 1


async def test_async_in_progress_409_retries_then_replays(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    slept: list[float] = []

    async def fake_sleep(s: float) -> None:
        slept.append(s)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    calls = {"n": 0}

    def respond(_req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return in_progress_response()
        return json_response(200, run_envelope({"ok": True}, replayed=True))

    client, rec = make_async_client(respond)
    result = await client.run("x.y", {"query": "sent"})
    assert result.replayed is True
    assert len(rec.requests) == 2
    assert slept == [30.0]
    await client.aclose()


async def test_async_idempotency_conflict_409_is_not_retried() -> None:
    from getanyapi import AnyAPIError

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(
            409,
            {"error": "different request", "code": "idempotency_conflict"},
            headers={"retry-after": "30"},
        )

    client, rec = make_async_client(respond, max_retries=2)
    with pytest.raises(AnyAPIError) as exc:
        await client.run("x.y", {"query": "sent"})
    assert exc.value.code == "idempotency_conflict"
    assert len(rec.requests) == 1
    await client.aclose()


async def test_async_in_progress_budget_stops_before_max_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from getanyapi import AnyAPIError

    slept: list[float] = []

    async def fake_sleep(s: float) -> None:
        slept.append(s)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    def respond(_req: httpx.Request) -> httpx.Response:
        return in_progress_response()

    client, rec = make_async_client(respond, max_retries=5)
    with pytest.raises(AnyAPIError):
        await client.run("x.y", {"query": "sent"})
    assert slept == [30.0, 30.0]
    assert len(rec.requests) == 3
    await client.aclose()
