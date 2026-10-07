"""The 3.x (Stainless) client conventions kept by custom/supermemory/_compat.py."""

import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

import supermemory
from supermemory import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AsyncSupermemory,
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    Supermemory,
    SupermemoryError,
)
from supermemory.errors import NotFoundError as GeneratedNotFoundError

Handler = Callable[[httpx.Request], httpx.Response]

NS_PAGE = {"namespaces": [], "pagination": {"currentPage": 1, "limit": 10, "totalItems": 0, "totalPages": 0}}


def _ok(captured: list[httpx.Request], body: Any = None) -> Handler:
    def handle(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={} if body is None else body)

    return handle


def _client(handler: Handler, **kwargs: Any) -> Supermemory:
    return Supermemory(api_key="sm_test", http_client=httpx.Client(transport=httpx.MockTransport(handler)), **kwargs)


def test_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPERMEMORY_API_KEY", raising=False)
    with pytest.raises(SupermemoryError, match="api_key client option must be set"):
        Supermemory()


def test_env_base_url_and_custom_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPERMEMORY_BASE_URL", "https://staging.example.com")
    monkeypatch.setenv("SUPERMEMORY_CUSTOM_HEADERS", "X-Team: core\nX-Env: test")
    captured: list[httpx.Request] = []
    _client(_ok(captured)).namespaces.list()
    assert str(captured[0].url) == "https://staging.example.com/ns"
    assert captured[0].headers["x-team"] == "core"
    assert captured[0].headers["x-env"] == "test"


def test_default_headers_and_query() -> None:
    captured: list[httpx.Request] = []
    client = _client(_ok(captured), default_headers={"X-App": "demo"}, default_query={"trace": "1"})
    client.search("user_alex", query="hi")
    assert captured[0].headers["x-app"] == "demo"
    assert captured[0].url.params["trace"] == "1"


def test_per_call_options() -> None:
    captured: list[httpx.Request] = []
    _client(_ok(captured)).search(
        "user_alex",
        query="hi",
        extra_headers={"X-Req": "1"},
        extra_query={"debug": "true"},
        extra_body={"experimental": True},
        timeout=5,
    )
    (request,) = captured
    assert request.headers["x-req"] == "1"
    assert request.url.params["debug"] == "true"
    assert json.loads(request.content) == {"query": "hi", "experimental": True}
    assert request.extensions["timeout"]["read"] == 5


def test_with_options_keeps_settings() -> None:
    captured: list[httpx.Request] = []
    client = _client(_ok(captured), default_headers={"X-App": "demo"})
    derived = client.with_options(max_retries=0, default_headers={"X-Extra": "1"})
    derived.namespaces.list()
    assert derived.max_retries == 0
    assert derived.api_key == "sm_test"
    assert captured[0].headers["x-app"] == "demo"
    assert captured[0].headers["x-extra"] == "1"


@pytest.mark.parametrize(
    "status,cls",
    [
        (401, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (503, InternalServerError),
        (418, APIStatusError),
    ],
)
def test_status_errors(status: int, cls: type) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json={"error": "nope"}, headers={"x-request-id": "req_1"})

    client = _client(handle, max_retries=0)
    with pytest.raises(cls) as exc:
        client.documents.get("user_alex", "doc1")
    err = exc.value
    assert isinstance(err, APIStatusError) and isinstance(err, APIError) and isinstance(err, SupermemoryError)
    assert err.status_code == status
    assert err.body == {"error": "nope"}
    assert err.message == f"Error code: {status} - {{'error': 'nope'}}"
    assert str(err) == err.message
    assert err.response is not None and err.response.headers["x-request-id"] == "req_1"
    assert err.request is not None and err.request.url.path == "/ns/user_alex/document/doc1"


def test_status_error_also_matches_generated_class() -> None:
    client = _client(lambda _: httpx.Response(404, json={"error": "missing"}))
    with pytest.raises(GeneratedNotFoundError):
        client.documents.get("user_alex", "doc1")


def test_timeout_error() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    with pytest.raises(APITimeoutError) as exc:
        _client(handle, max_retries=0).namespaces.list()
    assert isinstance(exc.value, APIConnectionError)
    assert exc.value.request is not None


def test_timeout_object_is_forwarded_whole() -> None:
    captured: list[httpx.Request] = []
    client = _client(_ok(captured, NS_PAGE), timeout=httpx.Timeout(10.0, connect=2.5))
    client.namespaces.list()
    assert captured[0].extensions["timeout"] == {"connect": 2.5, "read": 10.0, "write": 10.0, "pool": 10.0}

    client.namespaces.list(timeout=httpx.Timeout(20.0, connect=1.0))
    assert captured[1].extensions["timeout"]["connect"] == 1.0
    assert captured[1].extensions["timeout"]["read"] == 20.0


def test_timeout_none_disables_timeouts() -> None:
    from supermemory import NOT_GIVEN

    captured: list[httpx.Request] = []
    off = {"connect": None, "read": None, "write": None, "pool": None}

    _client(_ok(captured, NS_PAGE)).namespaces.list()
    assert captured[0].extensions["timeout"] == {"connect": 5.0, "read": 60.0, "write": 60.0, "pool": 60.0}

    _client(_ok(captured, NS_PAGE), timeout=None).namespaces.list()
    assert captured[1].extensions["timeout"] == off

    client = _client(_ok(captured, NS_PAGE), timeout=10.0)
    client.namespaces.list(timeout=None)
    assert captured[2].extensions["timeout"] == off
    client.namespaces.list(timeout=NOT_GIVEN)
    assert captured[3].extensions["timeout"]["read"] == 10.0
    client.with_options(timeout=None).namespaces.list()
    assert captured[4].extensions["timeout"] == off


def test_read_timeout_is_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    import supermemory.core.http_client as http_client

    monkeypatch.setattr(http_client.time, "sleep", lambda _: None)
    calls = 0

    def handle(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("slow", request=request)
        return httpx.Response(200, json=NS_PAGE)

    assert _client(handle, max_retries=2).namespaces.list().namespaces == []
    assert calls == 2


def test_connection_error() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    with pytest.raises(APIConnectionError) as exc:
        _client(handle, max_retries=0).namespaces.list()
    assert not isinstance(exc.value, APITimeoutError)


def test_raw_response() -> None:
    captured: list[httpx.Request] = []
    client = _client(_ok(captured, {"results": [], "searchTime": 3.5}))
    raw = client.with_raw_response.search("user_alex", query="hi", extra_headers={"X-Req": "1"})
    assert raw.status_code == 200
    assert raw.http_response.status_code == 200
    assert raw.parse().search_time == 3.5
    assert captured[0].headers["x-req"] == "1"


def test_model_helpers() -> None:
    client = _client(_ok([], {"results": [], "searchTime": 3.5}))
    response = client.search("user_alex", query="hi")
    assert response.to_dict() == {"results": [], "searchTime": 3.5}
    assert response.to_dict(use_api_names=False) == {"results": [], "search_time": 3.5}
    assert json.loads(response.to_json()) == {"results": [], "searchTime": 3.5}


def test_exports() -> None:
    assert supermemory.Client is Supermemory
    assert supermemory.__version__
    assert supermemory.DEFAULT_MAX_RETRIES == 2
    assert supermemory.DEFAULT_TIMEOUT == httpx.Timeout(60, connect=5.0)


async def test_async_conventions() -> None:
    captured: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if request.url.path.endswith("/missing"):
            return httpx.Response(404, json={"error": "missing"})
        return httpx.Response(200, json={"results": [], "searchTime": 1})

    client = AsyncSupermemory(
        api_key="sm_test",
        default_query={"trace": "1"},
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
    )
    await client.search("user_alex", query="hi", extra_headers={"X-Req": "1"})
    assert captured[0].headers["x-req"] == "1"
    assert captured[0].url.params["trace"] == "1"

    raw = await client.with_raw_response.search("user_alex", query="hi")
    assert (await raw.parse()).search_time == 1

    with pytest.raises(NotFoundError) as exc:
        await client.documents.get("user_alex", "missing")
    assert exc.value.response is not None and exc.value.response.status_code == 404
