"""Client metadata and wrapper precedence at the HTTP boundary."""

import platform

import httpx
import pytest
import respx

from composio_client import AsyncComposio, ClientIdentity, Composio, ComposioError, NoAuth, ProjectAuth
from composio_client._version import __version__

from .conftest import BASE_URL


def assert_defaults(headers: httpx.Headers) -> None:
    assert headers["x-client-provenance"] == "composio-client"
    assert headers["x-client-version"] == __version__
    assert headers["x-client-library"] == "composio-client"
    assert headers["x-client-library-version"] == __version__
    assert headers["x-client-language"] == "python"
    assert headers["x-runtime"] == "python"
    assert headers["x-client-runtime"] == "python"
    assert headers["x-runtime-version"] == platform.python_version()
    assert headers["user-agent"] == f"Composio/Python {__version__}"


@pytest.mark.respx(base_url=BASE_URL)
def test_sync_defaults(client: Composio, respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    client.get("/api/v3.1/tools")
    assert_defaults(route.calls.last.request.headers)


@pytest.mark.respx(base_url=BASE_URL)
async def test_async_defaults(async_client: AsyncComposio, respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    await async_client.get("/api/v3.1/tools")
    assert_defaults(route.calls.last.request.headers)


@pytest.mark.respx(base_url=BASE_URL)
def test_sync_wrapper_and_request_precedence(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    with Composio(
        auth=NoAuth(),
        base_url=BASE_URL,
        default_headers={
            "X-Client-Provenance": "composio",
            "X-Client-Version": "0.24.0",
            "X-Runtime": "python CPython 3.12.0",
        },
    ) as client:
        client.get("/api/v3.1/tools")
        headers = route.calls.last.request.headers
        assert headers["x-client-provenance"] == "composio"
        assert headers["x-client-version"] == "0.24.0"
        assert headers["x-runtime"] == "python CPython 3.12.0"
        assert headers["x-client-runtime"] == "python"
        assert headers["x-client-library-version"] == __version__
        client.get(
            "/api/v3.1/tools",
            options={
                "headers": {
                    "X-Client-Provenance": "custom",
                    "X-Client-Version": "1.0.0",
                    "X-Runtime-Version": None,
                }
            },
        )
        headers = route.calls.last.request.headers
        assert headers["x-client-provenance"] == "custom"
        assert headers["x-client-version"] == "1.0.0"
        assert "x-runtime-version" not in headers


@pytest.mark.respx(base_url=BASE_URL)
async def test_async_wrapper_precedence(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    async with AsyncComposio(
        auth=NoAuth(),
        base_url=BASE_URL,
        default_headers={
            "X-Client-Provenance": "composio",
            "X-Client-Version": "0.24.0",
            "X-Runtime": "python CPython 3.12.0",
        },
    ) as client:
        await client.get("/api/v3.1/tools")
        assert route.calls.last.request.headers["x-client-provenance"] == "composio"
        await client.get("/api/v3.1/tools", options={"headers": {"X-Client-Version": "0.25.0"}})
        assert route.calls.last.request.headers["x-client-version"] == "0.25.0"
        assert route.calls.last.request.headers["x-client-library-version"] == __version__


IDENTITY_HEADERS = (
    "x-client-provenance",
    "x-client-version",
    "x-client-library",
    "x-client-library-version",
    "x-client-language",
    "x-client-runtime",
    "x-runtime",
    "x-runtime-version",
)


def assert_no_identity(headers: httpx.Headers) -> None:
    assert [name for name in IDENTITY_HEADERS if name in headers] == []


@pytest.mark.parametrize(
    ("path", "dispatched"),
    [
        # concatenated onto base_url, so the authority becomes `api.testhttps`
        ("https://storage.invalid/file", "https://api.testhttps//storage.invalid/file"),
        (".storage.invalid/file", "https://api.test.storage.invalid/file"),
    ],
)
def test_identity_is_not_added_to_another_origin(path: str, dispatched: str) -> None:
    requests: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    transport = httpx.MockTransport(respond)
    with Composio(auth=NoAuth(), base_url=BASE_URL, http_client=httpx.Client(transport=transport)) as client:
        client.get(path)
        client.get("/api/v3.1/tools")

    assert str(requests[0].url) == dispatched
    assert_no_identity(requests[0].headers)
    assert requests[0].headers["user-agent"] == f"Composio/Python {__version__}"
    assert_defaults(requests[1].headers)


@respx.mock
def test_sync_redirect_to_another_origin_drops_identity(client: Composio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(302, headers={"location": "https://storage.invalid/x"})
    )
    target = respx.get("https://storage.invalid/x").mock(return_value=httpx.Response(200, json={}))
    client.get("/echo")
    assert_defaults(respx.calls[0].request.headers)
    assert_no_identity(target.calls.last.request.headers)


@respx.mock
async def test_async_redirect_to_another_origin_drops_identity(async_client: AsyncComposio) -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(302, headers={"location": "https://storage.invalid/x"})
    )
    target = respx.get("https://storage.invalid/x").mock(return_value=httpx.Response(200, json={}))
    await async_client.get("/echo")
    assert_defaults(respx.calls[0].request.headers)
    assert_no_identity(target.calls.last.request.headers)


SDK = ClientIdentity(
    product="composio", version="0.9.0", source="PYTHON_SDK", framework="openai", runtime="CPython"
)
LIBRARY_OWNED = ("x-client-library", "x-client-library-version", "x-client-language")
PRODUCT_OWNED = (
    "x-client-provenance",
    "x-client-version",
    "x-sdk-version",
    "x-source",
    "x-framework",
    "x-runtime",
    "x-client-runtime",
    "x-runtime-version",
)


def assert_identity(headers: httpx.Headers) -> None:
    assert headers["x-client-provenance"] == "composio"
    assert headers["x-client-version"] == "0.9.0"
    assert headers["x-sdk-version"] == "0.9.0"
    assert headers["x-source"] == "PYTHON_SDK"
    assert headers["x-framework"] == "openai"
    assert headers["x-runtime"] == "CPython"
    assert headers["x-client-runtime"] == "python"
    assert headers["x-runtime-version"] == platform.python_version()
    assert headers["x-client-library"] == "composio-client"
    assert headers["x-client-library-version"] == __version__
    assert headers["x-client-language"] == "python"


@pytest.mark.respx(base_url=BASE_URL)
def test_sync_identity(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    with Composio(auth=NoAuth(), base_url=BASE_URL, identity=SDK) as client:
        client.get("/api/v3.1/tools")
    assert_identity(route.calls.last.request.headers)


@pytest.mark.respx(base_url=BASE_URL)
async def test_async_identity(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    async with AsyncComposio(auth=NoAuth(), base_url=BASE_URL, identity=SDK) as client:
        await client.get("/api/v3.1/tools")
    assert_identity(route.calls.last.request.headers)


@pytest.mark.respx(base_url=BASE_URL)
def test_identity_without_legacy_labels(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    identity = ClientIdentity(product="p", version="1")
    with Composio(auth=NoAuth(), base_url=BASE_URL, identity=identity) as client:
        client.get("/api/v3.1/tools")
    headers = route.calls.last.request.headers
    assert headers["x-runtime"] == "python"
    assert "x-source" not in headers
    assert "x-framework" not in headers


@pytest.mark.respx(base_url=BASE_URL)
def test_no_sdk_labels_without_identity(client: Composio, respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    client.get("/api/v3.1/tools")
    headers = route.calls.last.request.headers
    assert [name for name in ("x-sdk-version", "x-source", "x-framework") if name in headers] == []


@pytest.mark.parametrize("name", [*LIBRARY_OWNED, *(name.upper() for name in LIBRARY_OWNED)])
@pytest.mark.parametrize("value", ["value", None])
def test_library_headers_refused_in_default_headers(name: str, value: str | None) -> None:
    with pytest.raises(ComposioError, match=f"The `{name.lower()}` header is set by the client"):
        Composio(auth=NoAuth(), base_url=BASE_URL, default_headers={name: value})


@pytest.mark.parametrize("name", PRODUCT_OWNED)
def test_product_headers_refused_beside_identity(name: str) -> None:
    with pytest.raises(ComposioError, match=f"The `{name}` header is set by `identity`"):
        AsyncComposio(auth=NoAuth(), base_url=BASE_URL, identity=SDK, default_headers={name: "x"})


@respx.mock
def test_identity_header_on_a_call_is_refused_before_sending() -> None:
    route = respx.get(f"{BASE_URL}/api/v3.1/tools").respond(200, json={})
    with Composio(auth=NoAuth(), base_url=BASE_URL, identity=SDK) as client:
        with pytest.raises(ComposioError, match="The `x-source` header is set by `identity`"):
            client.get("/api/v3.1/tools", options={"headers": {"X-Source": "other"}})
        with pytest.raises(ComposioError, match="The `x-client-library` header is set by the client"):
            client.get("/api/v3.1/tools", headers={"x-client-library": "spoofed"})
        with pytest.raises(ComposioError, match="The `x-client-provenance` header is set by `identity`"):
            client.post("/api/v3.1/tools", body={}, headers={"x-client-provenance": "spoofed"})
    assert not route.called


def test_library_header_through_custom_headers_is_refused() -> None:
    with pytest.raises(ComposioError, match="The `x-client-language` header is set by the client"):
        Composio.from_env({"COMPOSIO_CUSTOM_HEADERS": "x-client-language: typescript"}, auth=NoAuth())


@pytest.mark.parametrize(
    "kwargs",
    [
        {"product": "", "version": "1"},
        {"product": " p", "version": "1"},
        {"product": "p", "version": "1\r\nx-api-key: k"},
        {"product": "p", "version": "1", "framework": "café"},
        {"product": "p", "version": "1", "source": 42},
    ],
)
def test_invalid_identity_is_refused(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="must be a non-empty string"):
        ClientIdentity(**kwargs)  # type: ignore[arg-type]


def test_identity_must_be_a_client_identity() -> None:
    with pytest.raises(TypeError, match="`identity` must be a `ClientIdentity`"):
        Composio(auth=NoAuth(), base_url=BASE_URL, identity={"product": "p", "version": "1"})  # type: ignore[arg-type]


def test_identity_is_frozen() -> None:
    with pytest.raises(AttributeError):
        SDK.product = "other"  # type: ignore[misc]


@pytest.mark.respx(base_url=BASE_URL)
def test_with_options_keeps_and_replaces_identity(respx_mock: respx.MockRouter) -> None:
    route = respx_mock.get("/api/v3.1/tools").respond(200, json={})
    with Composio(auth=NoAuth(), base_url=BASE_URL, identity=SDK) as client:
        client.with_options(max_retries=0).get("/api/v3.1/tools")
        assert route.calls.last.request.headers["x-client-provenance"] == "composio"
        client.with_options(identity=ClientIdentity(product="other", version="2")).get("/api/v3.1/tools")
        assert route.calls.last.request.headers["x-client-provenance"] == "other"
        with pytest.raises(ComposioError):
            client.with_options(default_headers={"x-framework": "f"})


@respx.mock
def test_identity_stays_on_the_api_origin() -> None:
    respx.get(f"{BASE_URL}/echo").mock(
        return_value=httpx.Response(302, headers={"location": "https://storage.invalid/x"})
    )
    target = respx.get("https://storage.invalid/x").mock(return_value=httpx.Response(200, json={}))
    with Composio(auth=ProjectAuth("ak_test"), base_url=BASE_URL, identity=SDK) as client:
        client.get("/echo")
    assert_identity(respx.calls[0].request.headers)
    hop = target.calls.last.request.headers
    assert [name for name in (*LIBRARY_OWNED, *PRODUCT_OWNED) if name in hop] == []
