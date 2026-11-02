"""Status to error class mapping and request-id capture (SPEC 3.6)."""

from __future__ import annotations

import httpx
import pytest

from getanyapi import (
    AnyAPIError,
    AuthenticationError,
    BadRequestError,
    InsufficientBalanceError,
    NotFoundError,
    RateLimitedError,
    UpstreamError,
)
from conftest import json_response, make_sync_client

_CASES = [
    (400, BadRequestError),
    (401, AuthenticationError),
    (402, InsufficientBalanceError),
    (404, NotFoundError),
    (429, RateLimitedError),
    (502, UpstreamError),
    (418, AnyAPIError),  # unmapped -> base
    (500, AnyAPIError),
]


@pytest.mark.parametrize(("status", "cls"), _CASES)
def test_status_maps_to_error_class(
    status: int, cls: type[AnyAPIError]
) -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(
            status,
            {"error": f"boom {status}"},
            # The gateway's real header name (SPEC 2.6), not the conventional one.
            headers={"X-Anyapi-Request-Id": "req-123"},
        )

    client, _ = make_sync_client(respond, max_retries=0)
    with pytest.raises(cls) as exc:
        client.run("amazon.reviews", {"product": "B0"})
    assert exc.value.status == status
    assert exc.value.request_id == "req-123"
    assert str(exc.value) == f"boom {status}"
    # For mapped statuses, the class must be exact (not just a base match).
    assert type(exc.value) is cls


def test_unparseable_body_uses_fallback_message() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return httpx.Response(400, content=b"not json")

    client, _ = make_sync_client(respond, max_retries=0)
    with pytest.raises(BadRequestError) as exc:
        client.run("amazon.reviews", {})
    assert "status 400" in str(exc.value)
    assert exc.value.request_id is None


def test_error_body_code_is_exposed() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(
            409,
            {
                "error": "the key is already running",
                "code": "idempotency_in_progress",
            },
        )

    client, _ = make_sync_client(respond, max_retries=0)
    with pytest.raises(AnyAPIError) as exc:
        client.run("amazon.reviews", {"product": "B0"})
    assert exc.value.code == "idempotency_in_progress"


def _request_id_for(headers: dict[str, str]) -> str | None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(400, {"error": "nope"}, headers=headers)

    client, _ = make_sync_client(respond, max_retries=0)
    with pytest.raises(BadRequestError) as exc:
        client.run("amazon.reviews", {"product": "B0"})
    return exc.value.request_id


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        # Through v0.9.7 the SDK read only x-request-id, which the gateway never sends,
        # so request_id was always None in production.
        ({"X-Anyapi-Request-Id": "req_gw"}, "req_gw"),
        ({"x-request-id": "req_proxy"}, "req_proxy"),
        ({"X-Anyapi-Request-Id": "req_gw", "x-request-id": "req_proxy"}, "req_gw"),
        ({}, None),
    ],
)
def test_request_id_header_resolution(
    headers: dict[str, str], expected: str | None
) -> None:
    assert _request_id_for(headers) == expected
