"""Strata-1 tests: the hand-written dispatch kernel, exercised through a
throwaway response model so they don't depend on the generated schema shapes.

Mirrors the behavior pinned by the TS golden reference (``src/compat/request.ts``).
"""

from __future__ import annotations

import email.utils
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import httpx
import pytest
import respx
from pydantic import AnyUrl, BaseModel, ConfigDict, Field

from composio_client import (
    NOT_GIVEN,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AsyncComposio,
    AuthenticationError,
    BadRequestError,
    Composio,
    InternalServerError,
    NotFoundError,
    ProjectAuth,
    RateLimitError,
    RequestOptions,
    _base_client,
)
from composio_client._base_client import _encode_query, _merge_headers

from .conftest import API_KEY, BASE_URL


class Echo(BaseModel):
    ok: bool


class Named(BaseModel):
    name: str
    note: str | None = None


@pytest.fixture
def recorded_delays(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Replace the kernel sleep seams with recorders so no test sleeps for real."""
    delays: list[float] = []

    def record(seconds: float) -> None:
        delays.append(seconds)

    async def record_async(seconds: float) -> None:
        delays.append(seconds)

    monkeypatch.setattr(_base_client, "_sleep", record)
    monkeypatch.setattr(_base_client, "_async_sleep", record_async)
    return delays


# ---- pure helpers ----


def test_encode_query_comma_arrays_and_nested_and_none() -> None:
    encoded = dict(
        _encode_query(
            {
                "tags": ["a", "b", "c"],
                "nested": {"github": "v1", "slack": "v2"},
                "cursor": None,
                "flag": True,
                "limit": 10,
            }
        )
    )
    assert encoded["tags"] == "a,b,c"
    assert encoded["nested[github]"] == "v1"
    assert encoded["nested[slack]"] == "v2"
    assert encoded["flag"] == "true"
    assert encoded["limit"] == "10"
    assert "cursor" not in encoded


def test_merge_headers_precedence_and_delete() -> None:
    merged = _merge_headers(
        [
            {"accept": "application/json", "x-keep": "1"},
            {"x-api-key": "k"},
            {"X-Keep": None},  # case-insensitive delete
            {"x-extra": "e"},
        ]
    )
    assert merged["x-api-key"] == "k"
    assert merged["x-extra"] == "e"
    assert "x-keep" not in {k.lower() for k in merged}


# ---- request building ----


@respx.mock
def test_headers_and_body_on_post(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    result = client._request("post", "/echo", cast_to=Echo, body={"hello": "world"})
    assert result.ok is True
    request = route.calls.last.request
    assert request.headers["x-api-key"] == API_KEY
    assert request.headers["user-agent"].startswith("Composio/Python ")
    assert request.headers["content-type"] == "application/json"
    assert request.read() == b'{"hello":"world"}'


@respx.mock
def test_idempotency_key_option_stamps_the_header(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request(
        "post", "/echo", cast_to=Echo, body={"hello": "world"}, options={"idempotency_key": "key-123"}
    )

    assert route.calls.last.request.headers["idempotency-key"] == "key-123"


@respx.mock
def test_explicit_idempotency_key_header_wins_over_the_option(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request(
        "post",
        "/echo",
        cast_to=Echo,
        body={"hello": "world"},
        options={"idempotency_key": "from-option", "headers": {"idempotency-key": "from-header"}},
    )

    assert route.calls.last.request.headers["idempotency-key"] == "from-header"


@respx.mock
def test_client_default_headers_win_over_the_idempotency_key_option() -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = Composio(
        auth=ProjectAuth(API_KEY),
        base_url=BASE_URL,
        default_headers={"idempotency-key": "from-client-default"},
    )

    client._request(
        "post", "/echo", cast_to=Echo, body={"hello": "world"}, options={"idempotency_key": "from-option"}
    )

    assert route.calls.last.request.headers["idempotency-key"] == "from-client-default"


@respx.mock
def test_no_idempotency_key_header_by_default(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))

    client._request("post", "/echo", cast_to=Echo, body={"hello": "world"})

    assert "idempotency-key" not in route.calls.last.request.headers


@respx.mock
def test_not_given_body_fields_are_omitted(client: Composio) -> None:
    route = respx.patch(f"{BASE_URL}/api/v3.1/auth_configs/ac_fake").mock(
        return_value=httpx.Response(200, json={})
    )

    client.auth_configs.update(
        nanoid="ac_fake",
        type="custom",
        credentials={"client_id": "x", "client_secret": "y"},
        is_enabled_for_tool_router=NOT_GIVEN,
        tool_access_config=NOT_GIVEN,
    )

    assert json.loads(route.calls.last.request.read()) == {
        "type": "custom",
        "credentials": {"client_id": "x", "client_secret": "y"},
    }


@respx.mock
def test_query_serialization_on_get(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("get", "/echo", cast_to=Echo, query={"items": ["x", "y"], "drop": None, "n": 5})
    params = route.calls.last.request.url.params
    assert params.get("items") == "x,y"
    assert params.get("n") == "5"
    assert "drop" not in params


# ---- retries ----


@respx.mock
@pytest.mark.parametrize("method", ["post", "patch"])
def test_write_ignores_client_retries_and_idempotency_header(method: str) -> None:
    route = respx.route(method=method.upper(), url=f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(503, headers={"retry-after": "0"}, json={})
    )
    with Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL, max_retries=5) as configured:
        with pytest.raises(InternalServerError):
            configured._request(method, "/echo", cast_to=Echo, options=RequestOptions(idempotency_key="once"))
    assert route.call_count == 1


@respx.mock
@pytest.mark.parametrize("method", ["post", "patch"])
def test_write_does_not_retry_lost_response(client: Composio, method: str) -> None:
    route = respx.route(method=method.upper(), url=f"{BASE_URL}/echo").mock(
        side_effect=httpx.ReadError("response lost after the write")
    )
    with pytest.raises(APIConnectionError):
        client._request(method, "/echo", cast_to=Echo)
    assert route.call_count == 1


@respx.mock
@pytest.mark.parametrize("method", ["post", "patch"])
def test_write_retries_when_call_opts_in(client: Composio, method: str) -> None:
    route = respx.route(method=method.upper(), url=f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(503, headers={"retry-after": "0"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = client._request(method, "/echo", cast_to=Echo, options=RequestOptions(max_retries=1))
    assert result.ok is True
    assert route.call_count == 2


@respx.mock
@pytest.mark.parametrize("method", ["post", "patch"])
async def test_async_write_ignores_client_retries_and_idempotency_header(method: str) -> None:
    route = respx.route(method=method.upper(), url=f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(503, headers={"retry-after": "0"}, json={})
    )
    async with AsyncComposio(auth=ProjectAuth(API_KEY), base_url=BASE_URL, max_retries=5) as configured:
        with pytest.raises(InternalServerError):
            await configured._request(
                method, "/echo", cast_to=Echo, options=RequestOptions(idempotency_key="once")
            )
    assert route.call_count == 1


@respx.mock
@pytest.mark.parametrize("method", ["post", "patch"])
async def test_async_write_does_not_retry_lost_response(async_client: AsyncComposio, method: str) -> None:
    route = respx.route(method=method.upper(), url=f"{BASE_URL}/echo").mock(
        side_effect=httpx.ReadError("response lost after the write")
    )
    with pytest.raises(APIConnectionError):
        await async_client._request(method, "/echo", cast_to=Echo)
    assert route.call_count == 1


@respx.mock
@pytest.mark.parametrize("method", ["post", "patch"])
async def test_async_write_retries_when_call_opts_in(async_client: AsyncComposio, method: str) -> None:
    route = respx.route(method=method.upper(), url=f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(503, headers={"retry-after": "0"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = await async_client._request(method, "/echo", cast_to=Echo, options=RequestOptions(max_retries=1))
    assert result.ok is True
    assert route.call_count == 2


@respx.mock
def test_retries_on_500_then_succeeds(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(500, headers={"retry-after": "0"}, json={"error": {"message": "boom"}}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = client._request("get", "/echo", cast_to=Echo)
    assert result.ok is True
    assert route.call_count == 2


@respx.mock
def test_raw_response_reports_retries_taken(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/api/v3.1/tool_router/session/sess_123").mock(
        side_effect=[
            httpx.Response(500, headers={"retry-after": "0"}, json={}),
            httpx.Response(200, json={}),
        ]
    )

    response = client.tool_router.session.with_raw_response.retrieve("sess_123")

    assert response.retries_taken == 1
    assert route.call_count == 2


@respx.mock
def test_retries_on_429_honoring_retry_after(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(429, headers={"retry-after": "0"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 2


@respx.mock
def test_no_retry_on_400(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(400, json={"error": {"message": "bad"}})
    )
    with pytest.raises(BadRequestError):
        client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 1


@respx.mock
def test_status_errors_use_the_stainless_compatible_hook(client: Composio) -> None:
    called: list[str] = []

    def make_status_error(
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        called.append(err_msg)
        return BadRequestError("wrapped", response=response, body=body)

    client._make_status_error = make_status_error  # type: ignore[method-assign]
    respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(400, json={}))

    with pytest.raises(BadRequestError, match="wrapped"):
        client._request("get", "/echo", cast_to=Echo)
    assert called == ["Bad Request"]


@respx.mock
def test_max_retries_override_stops_retrying(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(500, headers={"retry-after": "0"}, json={})
    )
    with pytest.raises(InternalServerError):
        client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    assert route.call_count == 1


# ---- error mapping ----


@respx.mock
@pytest.mark.parametrize(
    ("status", "error_cls"),
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (503, InternalServerError),
    ],
)
def test_status_to_error_class(client: Composio, status: int, error_cls: type[Exception]) -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(status, json={"error": {"message": "nope"}})
    )
    with pytest.raises(error_cls) as excinfo:
        client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    err = excinfo.value
    assert isinstance(err, APIStatusError)
    assert err.status_code == status
    assert err.body == {"error": {"message": "nope"}}
    assert "nope" in str(err)


# A validation failure exactly as Apollo emits it (observed 2026-09-11).
VALIDATION_ENVELOPE: dict[str, Any] = {
    "error": {
        "message": "Validation error while processing request",
        "code": 400,
        "slug": "HTTP_BadRequest",
        "status": 400,
        "request_id": "req_body_only",
        "suggested_fix": "Check the payload against the schema.",
        "errors": ["Error in payload.tags: Invalid input"],
    }
}


def _status_error(client: Composio) -> APIStatusError:
    with pytest.raises(APIStatusError) as excinfo:
        client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    return excinfo.value


@respx.mock
def test_request_id_prefers_the_response_header(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(
            400, json=VALIDATION_ENVELOPE, headers={"x-request-id": "req_from_header"}
        )
    )
    err = _status_error(client)
    assert isinstance(err, BadRequestError)
    assert err.request_id == "req_from_header"


@respx.mock
def test_request_id_falls_back_to_the_envelope(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(400, json=VALIDATION_ENVELOPE))
    err = _status_error(client)
    assert err.request_id == "req_body_only"


@respx.mock
def test_details_exposes_the_typed_envelope(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(400, json=VALIDATION_ENVELOPE))
    err = _status_error(client)
    assert err.details == VALIDATION_ENVELOPE["error"]
    assert err.details is not None
    assert err.details["errors"] == ["Error in payload.tags: Invalid input"]
    assert err.body == VALIDATION_ENVELOPE


@respx.mock
def test_details_and_request_id_are_none_off_the_envelope(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(
            502, text="<html>Bad Gateway</html>", headers={"content-type": "text/html"}
        )
    )
    err = _status_error(client)
    assert isinstance(err, InternalServerError)
    assert err.details is None
    assert err.request_id is None


@respx.mock
def test_details_is_none_for_json_that_is_not_the_envelope(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(return_value=httpx.Response(404, json={"error": {"message": "nope"}}))
    err = _status_error(client)
    assert err.details is None
    assert err.request_id is None


@pytest.mark.parametrize(
    "inner",
    [
        {**VALIDATION_ENVELOPE["error"], "errors": [{"path": "tags"}]},
        {**VALIDATION_ENVELOPE["error"], "code": "400"},
        {**VALIDATION_ENVELOPE["error"], "request_id": 42},
    ],
)
def test_details_rejects_a_mistyped_optional_field(inner: dict[str, Any]) -> None:
    response = httpx.Response(400, request=httpx.Request("GET", f"{BASE_URL}/echo"))
    err = APIStatusError("400 boom", response=response, body={"error": inner})
    assert err.details is None


# ---- connection / timeout ----


@respx.mock
def test_timeout_maps_to_api_timeout_error(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(side_effect=httpx.ConnectTimeout("slow"))
    with pytest.raises(APITimeoutError):
        client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))


@respx.mock
def test_connection_error_maps_to_api_connection_error(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(side_effect=httpx.ConnectError("down"))
    with pytest.raises(APIConnectionError):
        client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))


# ---- async twins of the kernel behavior tests ----


@respx.mock
async def test_async_retries_on_500_then_succeeds(async_client: AsyncComposio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(500, headers={"retry-after": "0"}, json={"error": {"message": "boom"}}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = await async_client._request("get", "/echo", cast_to=Echo)
    assert result.ok is True
    assert route.call_count == 2
    await async_client.aclose()


@respx.mock
async def test_async_raw_response_reports_retries_taken(async_client: AsyncComposio) -> None:
    route = respx.get(f"{BASE_URL}/api/v3.1/tool_router/session/sess_123").mock(
        side_effect=[
            httpx.Response(500, headers={"retry-after": "0"}, json={}),
            httpx.Response(200, json={}),
        ]
    )

    response = await async_client.tool_router.session.with_raw_response.retrieve("sess_123")

    assert response.retries_taken == 1
    assert route.call_count == 2
    await async_client.aclose()


@respx.mock
async def test_async_no_retry_on_400(async_client: AsyncComposio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(400, json={"error": {"message": "bad"}})
    )
    with pytest.raises(BadRequestError):
        await async_client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 1
    await async_client.aclose()


@respx.mock
async def test_async_max_retries_override_stops_retrying(async_client: AsyncComposio) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(500, headers={"retry-after": "0"}, json={})
    )
    with pytest.raises(InternalServerError):
        await async_client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    assert route.call_count == 1
    await async_client.aclose()


@respx.mock
async def test_async_iterator_body_is_not_retried_empty(async_client: AsyncComposio) -> None:
    async def content():
        yield b"PAYLOAD"

    route = respx.post(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(500, headers={"retry-after": "0"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )

    with pytest.raises(InternalServerError):
        await async_client._request("post", "/echo", cast_to=Echo, content=content())

    assert route.call_count == 1
    assert route.calls[0].request.read() == b"PAYLOAD"
    await async_client.aclose()


@respx.mock
async def test_async_iterator_body_is_not_retried_after_connection_error(
    async_client: AsyncComposio,
) -> None:
    async def content():
        yield b"PAYLOAD"

    route = respx.post(f"{BASE_URL}/echo").mock(
        side_effect=[httpx.ConnectError("down"), httpx.Response(200, json={"ok": True})]
    )

    with pytest.raises(APIConnectionError):
        await async_client._request("post", "/echo", cast_to=Echo, content=content())

    assert route.call_count == 1
    await async_client.aclose()


@respx.mock
async def test_async_iterator_body_rejects_preserving_redirect(async_client: AsyncComposio) -> None:
    async def content():
        yield b"PAYLOAD"

    source = respx.post(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(307, headers={"location": "/next"})
    )
    target = respx.post(f"{BASE_URL}/next").mock(return_value=httpx.Response(200, json={"ok": True}))

    with pytest.raises(APIConnectionError, match="cannot be replayed"):
        await async_client._request("post", "/echo", cast_to=Echo, content=content())

    assert source.call_count == 1
    assert source.calls[0].request.read() == b"PAYLOAD"
    assert target.call_count == 0
    await async_client.aclose()


@respx.mock
@pytest.mark.parametrize(
    ("status", "error_cls"),
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (503, InternalServerError),
    ],
)
async def test_async_status_to_error_class(
    async_client: AsyncComposio, status: int, error_cls: type[Exception]
) -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(status, json={"error": {"message": "nope"}})
    )
    with pytest.raises(error_cls) as excinfo:
        await async_client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    err = excinfo.value
    assert isinstance(err, APIStatusError)
    assert err.status_code == status
    assert err.body == {"error": {"message": "nope"}}
    assert "nope" in str(err)
    await async_client.aclose()


@respx.mock
async def test_async_timeout_maps_to_api_timeout_error(async_client: AsyncComposio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(side_effect=httpx.ConnectTimeout("slow"))
    with pytest.raises(APITimeoutError):
        await async_client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    await async_client.aclose()


@respx.mock
async def test_async_connection_error_maps_to_api_connection_error(async_client: AsyncComposio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(side_effect=httpx.ConnectError("down"))
    with pytest.raises(APIConnectionError):
        await async_client._request("get", "/echo", cast_to=Echo, options=RequestOptions(max_retries=0))
    await async_client.aclose()


# ---- retry branches: x-should-retry / retry-after-ms / HTTP-date ----


@respx.mock
def test_x_should_retry_true_forces_retry(client: Composio, recorded_delays: list[float]) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(400, headers={"x-should-retry": "true"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = client._request("get", "/echo", cast_to=Echo)
    assert result.ok is True
    assert route.call_count == 2
    assert len(recorded_delays) == 1


@respx.mock
def test_x_should_retry_false_suppresses_retry(client: Composio, recorded_delays: list[float]) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(500, headers={"x-should-retry": "false"}, json={})
    )
    with pytest.raises(InternalServerError):
        client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 1
    assert recorded_delays == []


@respx.mock
def test_retry_after_ms_honored(client: Composio, recorded_delays: list[float]) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(429, headers={"retry-after-ms": "1500"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 2
    assert recorded_delays == [1.5]


@respx.mock
def test_retry_after_http_date_honored(client: Composio, recorded_delays: list[float]) -> None:
    retry_at = email.utils.format_datetime(datetime.now(timezone.utc) + timedelta(seconds=5), usegmt=True)
    respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(429, headers={"retry-after": retry_at}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    client._request("get", "/echo", cast_to=Echo)
    # HTTP-dates have whole-second granularity; the computed delta lands a bit
    # under the 5s we asked for but well inside the honored window.
    assert len(recorded_delays) == 1
    assert 3.0 <= recorded_delays[0] <= 5.0


@respx.mock
async def test_async_x_should_retry_true_forces_retry(
    async_client: AsyncComposio, recorded_delays: list[float]
) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(400, headers={"x-should-retry": "true"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = await async_client._request("get", "/echo", cast_to=Echo)
    assert result.ok is True
    assert route.call_count == 2
    assert len(recorded_delays) == 1
    await async_client.aclose()


@respx.mock
async def test_async_retry_after_ms_honored(
    async_client: AsyncComposio, recorded_delays: list[float]
) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(429, headers={"retry-after-ms": "1500"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    await async_client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 2
    assert recorded_delays == [1.5]
    await async_client.aclose()


# ---- regressions: malformed / out-of-range retry headers fall back to backoff ----


@respx.mock
def test_malformed_retry_after_does_not_crash(client: Composio, recorded_delays: list[float]) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(500, headers={"retry-after": "not-a-date"}, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    result = client._request("get", "/echo", cast_to=Echo)
    assert result.ok is True
    assert route.call_count == 2
    assert len(recorded_delays) == 1
    assert 0 < recorded_delays[0] <= 8.0


@respx.mock
@pytest.mark.parametrize(
    "headers",
    [
        {"retry-after-ms": "3600000"},  # one hour, in milliseconds
        {"retry-after-ms": "-100"},
        {"retry-after": "-5"},
        {"retry-after": "120"},  # >= the 60s clamp
    ],
)
def test_out_of_range_retry_headers_fall_back_to_backoff(
    client: Composio, recorded_delays: list[float], headers: dict[str, str]
) -> None:
    route = respx.get(f"{BASE_URL}/echo").mock(
        side_effect=[
            httpx.Response(500, headers=headers, json={}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    client._request("get", "/echo", cast_to=Echo)
    assert route.call_count == 2
    assert len(recorded_delays) == 1
    assert 0 < recorded_delays[0] <= 8.0


# ---- regressions: base-URL env resolution ----


def test_empty_base_url_env_resolves_to_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COMPOSIO_BASE_URL", "")
    resolved = Composio(auth=ProjectAuth(API_KEY))
    assert resolved.base_url == "https://backend.composio.dev"


# ---- regressions: body null handling (TS JSON.stringify parity) ----


@respx.mock
def test_model_body_explicit_none_sent_as_null(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("post", "/echo", cast_to=Echo, body=Named(name="x", note=None))
    assert route.calls.last.request.read() == b'{"name":"x","note":null}'


@respx.mock
def test_model_body_unset_field_omitted(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("post", "/echo", cast_to=Echo, body=Named(name="x"))
    assert route.calls.last.request.read() == b'{"name":"x"}'


@respx.mock
def test_dict_body_none_sent_as_null(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("post", "/echo", cast_to=Echo, body={"name": "x", "note": None})
    assert route.calls.last.request.read() == b'{"name":"x","note":null}'


# ---- regressions: dict bodies go through their endpoint's request model ----
#
# A plain-mapping body used to be forwarded verbatim, so pythonic field names
# reached the wire wherever the spec declared a different one. `body_model`
# routes the mapping through the generated model, which applies the aliases.
# `AliasedBody` stands in for a generated request model: it carries the same
# relaxed config `packages/codegen`'s `python-postgen` gives every generated model
# (`populate_by_name=True, extra="allow"`) so this suite keeps testing the
# kernel rather than the current spec snapshot.


class AliasedVal(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    your_domain: str | None = Field(default=None, alias="your-domain")


class AliasedBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    auth_scheme: str = Field(..., alias="authScheme")
    val: AliasedVal | None = None
    note: str | None = None


def _post_body(client: Composio, body: object) -> Any:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("post", "/echo", cast_to=Echo, body=body, body_model=AliasedBody)
    return json.loads(route.calls.last.request.read())


@respx.mock
def test_dict_body_wire_aliases_are_applied(client: Composio) -> None:
    sent = _post_body(client, {"auth_scheme": "OAUTH2", "val": {"your_domain": "acme.example.com"}})
    assert sent == {"authScheme": "OAUTH2", "val": {"your-domain": "acme.example.com"}}


@respx.mock
def test_dict_body_already_in_wire_spelling_is_unchanged(client: Composio) -> None:
    sent = _post_body(client, {"authScheme": "OAUTH2", "val": {"your-domain": "acme.example.com"}})
    assert sent == {"authScheme": "OAUTH2", "val": {"your-domain": "acme.example.com"}}


@respx.mock
def test_dict_body_unknown_keys_are_preserved(client: Composio) -> None:
    sent = _post_body(
        client,
        {
            "auth_scheme": "OAUTH2",
            "brand_new_field": "keep-me",
            "val": {"your_domain": "acme.example.com", "brand_new_val_key": "keep-nested"},
        },
    )
    assert sent == {
        "authScheme": "OAUTH2",
        "brand_new_field": "keep-me",
        "val": {"your-domain": "acme.example.com", "brand_new_val_key": "keep-nested"},
    }


@respx.mock
def test_dict_body_explicit_none_is_still_null(client: Composio) -> None:
    sent = _post_body(client, {"auth_scheme": "OAUTH2", "note": None})
    assert sent == {"authScheme": "OAUTH2", "note": None}


@respx.mock
def test_dict_body_unset_field_is_still_omitted(client: Composio) -> None:
    sent = _post_body(client, {"auth_scheme": "OAUTH2"})
    assert sent == {"authScheme": "OAUTH2"}


@respx.mock
def test_dict_body_that_the_model_would_reject_is_still_aliased(client: Composio) -> None:
    """Aliasing is a key rename, so it has no failure mode.

    This body omits the required `auth_scheme` and carries a key of a type the
    model does not admit. There is nothing to validate — the renamer walks the
    model as a name map — so the aliases still land and nothing is rejected.
    The Stainless oracle does no runtime validation either, so a body it would
    have dispatched must still be dispatched here, and aliased.
    """
    sent = _post_body(client, {"val": {"your_domain": "acme.example.com"}, "extra": 1})
    assert sent == {"val": {"your-domain": "acme.example.com"}, "extra": 1}


@respx.mock
def test_model_body_is_unaffected_by_body_model(client: Composio) -> None:
    sent = _post_body(client, AliasedBody(auth_scheme="OAUTH2", note=None))
    assert sent == {"authScheme": "OAUTH2", "note": None}


# ---- regressions: a dict body's *values* are never rewritten ----
#
# Renaming used to be `model_validate(...).model_dump(mode="json", ...)`, which
# renamed correctly but also ran pydantic's lax coercion on the way in and its
# JSON serialization on the way out. Both rewrite values the oracle sends
# verbatim. `Typed` stands in for a generated model with the annotations that
# provoked each rewrite.


class Typed(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    number: float | None = None
    url: AnyUrl | None = None
    flag: bool | None = None
    renamed: str | None = Field(default=None, alias="wire-name")


def _post_typed(client: Composio, body: object) -> Any:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("post", "/echo", cast_to=Echo, body=body, body_model=Typed)
    return json.loads(route.calls.last.request.read())


@respx.mock
@pytest.mark.parametrize(
    "value",
    [
        pytest.param(3600, id="int-into-number"),
        pytest.param(3600.5, id="float-into-number"),
        pytest.param(0, id="zero-into-number"),
        pytest.param("3600", id="string-into-number"),
        pytest.param(True, id="bool-into-number"),
        pytest.param(None, id="null-into-number"),
        pytest.param({"nested": 1}, id="object-into-number"),
    ],
)
def test_dict_body_number_field_keeps_the_callers_json_type(client: Composio, value: Any) -> None:
    sent = _post_typed(client, {"number": value, "renamed": "r"})
    assert sent == {"number": value, "wire-name": "r"}
    # an int must not become a float: `3600` and `3600.0` are different bytes
    assert type(sent["number"]) is type(value)


@respx.mock
def test_dict_body_url_field_is_not_normalized(client: Composio) -> None:
    """`AnyUrl` round-trips add a trailing slash and lowercase the authority."""
    sent = _post_typed(client, {"url": "HTTPS://Example.COM"})
    assert sent == {"url": "HTTPS://Example.COM"}


@respx.mock
def test_dict_body_bool_field_keeps_its_type(client: Composio) -> None:
    sent = _post_typed(client, {"flag": 1})
    assert sent == {"flag": 1}
    assert type(sent["flag"]) is int


# ---- regressions: union members are resolved, not smeared ----


class VariantA(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    kind: Literal["a"]
    only_on_a: str | None = Field(default=None, alias="onlyOnA")
    shared: str | None = Field(default=None, alias="sharedWire")
    amount: float | None = None


class VariantB(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    kind: Literal["b"]
    shared: str | None = Field(default=None, alias="sharedWire")


class UnionBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    variant: VariantA | VariantB | None = None
    renamed: str | None = Field(default=None, alias="wire-name")


def _post_union(client: Composio, body: object) -> Any:
    route = respx.post(f"{BASE_URL}/echo").mock(return_value=httpx.Response(200, json={"ok": True}))
    client._request("post", "/echo", cast_to=Echo, body=body, body_model=UnionBody)
    return json.loads(route.calls.last.request.read())


@respx.mock
def test_union_aliases_apply_only_to_the_resolved_member(client: Composio) -> None:
    """`only_on_a` is declared on VariantA alone, so it must not be renamed
    inside a VariantB value — the generic form of the pinned
    `redirect_url`/OAUTH1 divergence in `tests/test_tool_router.py`."""
    sent = _post_union(client, {"variant": {"kind": "b", "shared": "s", "only_on_a": "x"}})
    assert sent == {"variant": {"kind": "b", "sharedWire": "s", "only_on_a": "x"}}


@respx.mock
def test_union_member_resolves_by_discriminator_despite_an_unmodellable_sibling(
    client: Composio,
) -> None:
    """`amount` here is an object where the model says number, so no member of
    the union *validates*. The discriminator still identifies VariantA, so the
    subtree keeps its aliases instead of the whole body losing them."""
    sent = _post_union(client, {"variant": {"kind": "a", "only_on_a": "x", "amount": {"bad": 1}}})
    assert sent == {"variant": {"kind": "a", "onlyOnA": "x", "amount": {"bad": 1}}}


@respx.mock
def test_unresolvable_union_leaves_that_subtree_alone_but_not_the_body(client: Composio) -> None:
    """No discriminator matches and nothing validates, so the `variant` subtree
    is forwarded verbatim — while the rest of the body is still renamed."""
    sent = _post_union(client, {"variant": {"kind": "zzz", "only_on_a": "x"}, "renamed": "r"})
    assert sent == {"variant": {"kind": "zzz", "only_on_a": "x"}, "wire-name": "r"}


# ---- regressions: query array element serialization (JS Array.join parity) ----


def test_encode_query_array_elements_js_join_semantics() -> None:
    encoded = dict(_encode_query({"items": [True, None, 1]}))
    assert encoded["items"] == "true,,1"
