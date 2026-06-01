import asyncio
import json as json_lib
import pickle
from time import perf_counter

import httpx
import pytest
import structlog
from hypothesis import given
from hypothesis import strategies as st
from pydantic import SecretStr
from structlog.testing import LogCapture

from arraylake.api_utils import (
    ArraylakeHttpClient,
    AsyncRetryTransport,
    TokenAuth,
    UserAuth,
    _emitted_deprecation_warnings,
    _get_proxy_from_env,
    _get_session_id,
    calc_backoff,
    handle_response,
    retry_on_exception,
)
from arraylake.config import config
from arraylake.exceptions import (
    ArraylakeClientError,
    ArraylakeHttpError,
    ArraylakeServerError,
    ArraylakeValidationError,
)
from arraylake.metastore.http_metastore import HttpMetastoreConfig
from arraylake.token import AuthException
from arraylake.types import OauthTokens


def _get_test_tokens(fname) -> dict:
    """helper function to independently load oauth tokens"""
    with fname.open() as f:
        tokens = json_lib.load(f)
    return tokens


# regression test for
# https://github.com/earth-mover/arraylake/issues/302
# https://github.com/earth-mover/arraylake/issues/303
@pytest.mark.asyncio
async def test_http_request_headers(respx_mock, token, test_token_file) -> None:
    api_url = "https://foo.com"

    if token is None:
        tokens = _get_test_tokens(test_token_file)
        test_token = tokens["id_token"]
    else:
        test_token = token

    client = ArraylakeHttpClient(api_url, token=token)

    custom_headers = {"special": "header"}

    route = respx_mock.get(api_url + "/bar").mock(return_value=httpx.Response(httpx.codes.OK))

    async def check_client(client):
        assert str(client.api_url) == api_url
        response = await client._request("GET", "bar", headers=custom_headers)
        assert response.status_code == 200

    await check_client(client)
    assert route.calls.last.request.headers["authorization"] == f"Bearer {test_token}"
    assert route.calls.last.request.headers["special"] == "header"
    c1_headers = dict(route.calls.last.request.headers)

    client2 = pickle.loads(pickle.dumps(client))

    await check_client(client2)
    assert route.calls.last.request.headers == c1_headers

    client = ArraylakeHttpClient(api_url, token=token)
    await check_client(client)
    assert route.calls.last.request.headers["authorization"] == f"Bearer {test_token}"
    assert route.calls.last.request.headers["special"] == "header"


def test_session_id_stable_within_process() -> None:
    """Two clients in the same process share one session id (the point of the feature)."""
    c1 = ArraylakeHttpClient("https://foo.com")
    c2 = ArraylakeHttpClient("https://foo.com")
    sid = _get_session_id()
    assert c1._default_headers["arraylake-session-id"] == sid
    assert c2._default_headers["arraylake-session-id"] == sid


def test_session_id_survives_pickling() -> None:
    """Session id rides along when the client is pickled → one dask cluster, one session."""
    client = ArraylakeHttpClient("https://foo.com")
    sid = client._default_headers["arraylake-session-id"]
    assert sid
    restored = pickle.loads(pickle.dumps(client))
    assert restored._default_headers["arraylake-session-id"] == sid


def test_calc_backoff() -> None:
    assert calc_backoff(0, backoff_factor=0.5, jitter_ratio=0.1, max_backoff_wait=10) == 0
    assert calc_backoff(1, backoff_factor=0.5, jitter_ratio=0.0, max_backoff_wait=10) == 0.5
    assert calc_backoff(1, backoff_factor=0.5, jitter_ratio=0.1, max_backoff_wait=10) in [0.45, 0.55]


@given(
    st.integers(min_value=0, max_value=100),
    st.floats(min_value=0, max_value=100, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, max_value=1),
    st.integers(min_value=0, max_value=100),
)
def test_calc_backoff_is_valid(attempt, backoff_factor, jitter_ratio, max_backoff_wait) -> None:
    backoff = calc_backoff(attempt, backoff_factor=backoff_factor, jitter_ratio=jitter_ratio, max_backoff_wait=max_backoff_wait)
    assert backoff >= 0
    assert backoff <= max_backoff_wait


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [429, 502, 503, 504])
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "POST"])
async def test_retries(respx_mock, status_code, method) -> None:
    mock_url = "https://foo.bar/"

    clock = []

    def side_effect(request, route):
        clock.append(perf_counter())
        if route.call_count > 2:
            return httpx.Response(200)
        return httpx.Response(status_code)

    route = respx_mock.request(method, mock_url).mock(side_effect=side_effect)
    client = ArraylakeHttpClient(mock_url)
    response = await client._request(method, "")
    assert response.status_code == 200
    assert route.call_count == 4

    # verify increasing backoff
    diff = [clock[n] - clock[n - 1] for n in range(1, len(clock))]
    assert diff[-1] > diff[0]


@pytest.mark.asyncio
async def test_retry_after_header(respx_mock) -> None:
    mock_url = "https://foo.bar/"

    clock = []
    retry_after_time = 1

    def side_effect(request, route):
        clock.append(perf_counter())
        if route.call_count > 0:
            return httpx.Response(200)
        return httpx.Response(429, headers={"Retry-After": str(retry_after_time)})

    route = respx_mock.get(mock_url).mock(side_effect=side_effect)
    client = ArraylakeHttpClient(mock_url)
    response = await client._request("GET", "")
    assert response.status_code == 200
    assert route.call_count == 2

    # verify specified wait time
    diff = clock[1] - clock[0]
    assert diff > retry_after_time


@pytest.mark.parametrize("method", ["GET", "PUT", "POST"])
@pytest.mark.parametrize("headers", [None, {"foo": "bar"}, {"Authorization": "abc"}])
@pytest.mark.parametrize("json", [None, {"abc": "xyz"}])
def test_token_auth_does_not_mutate_request(test_token, method, headers, json) -> None:
    auth = TokenAuth(test_token)
    url = "https://foo.com"
    request = httpx.Request(method, url, headers=headers, json=json)
    orig_headers = request.headers.copy()
    request = next(auth.auth_flow(request))
    # check that authorization header was inserted
    assert request.headers["Authorization"] == f"Bearer {test_token}"

    # check that the rest of the request is the same
    assert request.method == method
    assert request.url == url
    for k, header in orig_headers.items():
        # authorization is one the key that we expect to be mutated (if it was on the original request for some reason)
        if k != "authorization":  # keys are lower case
            assert header == request.headers.get(k)
    if json:
        assert json_lib.loads(request.content) == json


@pytest.mark.asyncio
async def test_user_auth_requires_login(tmp_path) -> None:
    # Note: while this test does not explicitly await anything, the UserAuth class does include an asyncio.Lock
    # therefore, we mark this test for async execution
    bad_token_file = str(tmp_path / "tokens.json")
    with config.set({"service.token_path": bad_token_file}):
        with pytest.raises(AuthException, match=r"Not logged in, please log in .*"):
            UserAuth("https://foo.com")


@pytest.mark.asyncio
async def test_auth_adds_authorization_header_token_auth(test_token, respx_mock) -> None:
    auth = TokenAuth(test_token)
    route = respx_mock.get("https://foo.com").mock(return_value=httpx.Response(httpx.codes.OK))
    async with httpx.AsyncClient(auth=auth) as client:
        await client.get("https://foo.com")
    assert route.calls.last.request.headers["Authorization"] == f"Bearer {test_token}"


@pytest.mark.asyncio
async def test_auth_adds_authorization_header_user_auth(test_token_file, respx_mock) -> None:
    auth = UserAuth("https://foo.com")
    tokens = _get_test_tokens(test_token_file)
    test_token = tokens["id_token"]
    route = respx_mock.get("https://foo.com").mock(return_value=httpx.Response(httpx.codes.OK))
    async with httpx.AsyncClient(auth=auth) as client:
        await client.get("https://foo.com")
    assert route.calls.last.request.headers["Authorization"] == f"Bearer {test_token}"


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
@pytest.mark.parametrize("headers", [None, {"foo": "bar"}, {"Authorization": "abc"}])
@pytest.mark.parametrize("json", [None, {"abc": "xyz"}])
async def test_user_auth_does_not_mutate_request(test_token_file, method, headers, json) -> None:
    url = "https://foo.com"
    auth = UserAuth(url)

    tokens = _get_test_tokens(test_token_file)
    test_token = tokens["id_token"]

    request = httpx.Request(method, url, headers=headers, json=json)
    orig_headers = request.headers.copy()
    request_gen = auth.async_auth_flow(request)
    request = await request_gen.__anext__()  # TODO: switch to anext(request_gen) when python>=3.10
    # check that authorization header was inserted
    assert request.headers["Authorization"] == f"Bearer {test_token}"

    # check that the rest of the request is the same
    assert request.method == method
    assert request.url == url
    for k, header in orig_headers.items():
        # authorization is one the key that we expect to be mutated (if it was on the original request for some reason)
        if k != "authorization":  # keys are lower case
            assert header == request.headers.get(k)
    if json:
        assert json_lib.loads(request.content) == json


@pytest.mark.asyncio
async def test_user_auth_refresh_request(test_token_file, mock_auth_provider_config) -> None:
    # Note: while this test does not explicitly await anything, the UserAuth class does include an asyncio.Lock
    # therefore, we execute this mark this test for async execution
    url = "https://foo.com"
    auth = UserAuth(url)

    tokens = _get_test_tokens(test_token_file)
    refresh_token = tokens["refresh_token"]

    request = auth._token_handler.refresh_request
    content = dict(item.split("=") for item in request.content.decode("utf-8").split("&"))

    assert request.method == "POST"
    assert request.url.path == "/oauth/token"
    assert content["refresh_token"] == refresh_token


@pytest.mark.asyncio
async def test_user_auth_refreshes_on_401(test_token_file, respx_mock, mock_auth_provider_config) -> None:
    url = "https://foo.com"
    auth = UserAuth(url)

    # orig_tokens = _get_test_tokens(test_token_file)
    new_tokens = {
        "access_token": "akdh83",
        "id_token": "asdjkd7367",
        "refresh_token": "2383478nd",
        "expires_in": 86400,
        "token_type": "Bearer",
    }

    refresh_request = auth._token_handler.refresh_request
    respx_mock.get(url__eq=url).mock(side_effect=[httpx.Response(httpx.codes.UNAUTHORIZED), httpx.Response(httpx.codes.OK)])
    respx_mock.post(refresh_request.url).mock(return_value=httpx.Response(httpx.codes.OK, json=new_tokens))

    async with httpx.AsyncClient(auth=auth) as client:
        result = await client.get(url)
        assert result.status_code == httpx.codes.OK

    updated_tokens = _get_test_tokens(test_token_file)
    assert new_tokens == updated_tokens


@pytest.mark.asyncio
async def test_sync_user_auth_flow_raises(test_token_file) -> None:
    # Note: while this test does not explicitly await anything, the UserAuth class does include an asyncio.Lock
    # therefore, we execute this mark this test for async execution
    url = "https://foo.com"
    auth = UserAuth(url)

    request = httpx.Request("GET", url)
    with pytest.raises(RuntimeError, match="Sync auth flow not implemented yet"):
        auth.sync_auth_flow(request)

    with httpx.Client(auth=auth) as client:
        with pytest.raises(RuntimeError, match="Sync auth flow not implemented yet"):
            client.get(url)


# additional tests to write:
# test that we handle a failure to refresh gracefully


@pytest.mark.asyncio
async def test_retry_on_exception_decorator() -> None:
    @retry_on_exception(ValueError, n=3)
    async def raise_value_error():
        raise ValueError

    # Test that the function raises an exception if it fails 3 times
    with pytest.raises(ValueError):
        await raise_value_error()

    # Test that the function succeeds if it fails fewer than 3 times
    count = 0

    @retry_on_exception(ValueError, n=3)
    async def raise_value_error_then_succeed():
        nonlocal count
        count += 1
        if count < 2:
            raise ValueError
        else:
            return True

    assert await raise_value_error_then_succeed() is True
    assert count == 2

    # test that other errors are raised immediately
    count = 0

    @retry_on_exception(ValueError, n=3)
    async def raise_key_error():
        nonlocal count
        count += 1
        raise KeyError

    with pytest.raises(KeyError):
        await raise_key_error()
    assert count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("exception", [httpx.RemoteProtocolError, httpx.ConnectError])
async def test_retry_request_connection_errors(exception, respx_mock) -> None:
    # regression test for https://github.com/earth-mover/arraylake/issues/514

    mock_url = "https://foo.bar/"
    route = respx_mock.request("POST", mock_url).mock(side_effect=[exception, httpx.Response(200)])
    client = ArraylakeHttpClient(mock_url)
    response = await client._request("POST", "")
    assert response.status_code == 200
    assert route.call_count == 2

    # test that repeated exceptions are passed through
    mock_url = "https://spam.bar/"
    route = respx_mock.request("POST", mock_url).mock(side_effect=5 * [exception])
    client = ArraylakeHttpClient(mock_url)
    with pytest.raises(exception):
        await client._request("POST", "")
    assert route.call_count == 5


@pytest.fixture(name="log_output")
def fixture_log_output():
    return LogCapture()


@pytest.fixture(autouse=True)
def fixture_configure_structlog(log_output):
    structlog.configure(processors=[log_output])


def test_handle_response() -> None:
    mock_request = httpx.Request("POST", "https://earthmover.io/content/foo", params={"a": "b"}, json={"foo": "bar"})
    mock_response = httpx.Response(
        200, request=mock_request, content=json_lib.dumps({"detail": "Not found"}), headers={"Content-Type": "application/json"}
    )
    handle_response(mock_response)


def test_handle_response_error(log_output: LogCapture) -> None:
    mock_request = httpx.Request(
        "POST", "https://earthmover.io/content/foo", params={"a": "b"}, json={"foo": "bar"}, headers={"Authorization": "Bearer foo"}
    )
    mock_response = httpx.Response(
        404,
        request=mock_request,
        content=json_lib.dumps({"detail": "Not found"}),
        headers={"Content-Type": "application/json", "x-request-id": "7eea73c041524f268f804af813f7618f"},
    )
    with pytest.raises(ArraylakeClientError, match="Error response") as exc_info:
        handle_response(mock_response)

    # Verify the exception has the correct properties
    exc = exc_info.value
    assert exc.request_id == "7eea73c041524f268f804af813f7618f"
    assert exc.status_code == 404
    assert "[request-id: 7eea73c041524f268f804af813f7618f]" in str(exc)

    # Verify it's still a ValueError for backward compatibility
    assert isinstance(exc, ValueError)

    entries = log_output.entries[0]
    assert entries["log_level"] == "debug"
    assert entries["url"] == "https://earthmover.io/content/foo?a=b"
    assert json_lib.loads(entries["request_content"]) == {"foo": "bar"}
    assert entries["request_headers"]["authorization"] == "[omitted]"
    assert entries["response_headers"]["content-type"] == "application/json"
    assert entries["response_headers"]["x-request-id"] == "7eea73c041524f268f804af813f7618f"


def test_handle_response_422_validation_error() -> None:
    """Test that 422 responses raise ArraylakeValidationError with correlation ID"""
    mock_request = httpx.Request("POST", "https://foo.smerfmover.io/repos/org/repo")
    mock_response = httpx.Response(
        422,
        request=mock_request,
        content=json_lib.dumps({"detail": "Invalid repository name"}),
        headers={"Content-Type": "application/json", "x-request-id": "validation-error-id"},
    )
    with pytest.raises(ArraylakeValidationError) as exc_info:
        handle_response(mock_response)

    exc = exc_info.value
    assert exc.request_id == "validation-error-id"
    assert exc.status_code == 422
    assert str(exc) == "Invalid repository name [request-id: validation-error-id]"
    assert isinstance(exc, ValueError)  # Backward compatibility


def test_handle_response_422_validation_error_malformed_json() -> None:
    """Test that 422 responses with malformed JSON still include correlation ID"""
    mock_request = httpx.Request("POST", "https://foo.smerfmover.io/repos/org/repo")
    mock_response = httpx.Response(
        422,
        request=mock_request,
        content="Not valid JSON",
        headers={"Content-Type": "text/plain", "x-request-id": "malformed-json-id"},
    )
    with pytest.raises(ArraylakeValidationError) as exc_info:
        handle_response(mock_response)

    exc = exc_info.value
    assert exc.request_id == "malformed-json-id"
    assert exc.status_code == 422
    assert "Validation error while requesting" in str(exc)
    assert "[request-id: malformed-json-id]" in str(exc)


def test_handle_response_500_server_error() -> None:
    """Test that 5xx responses raise ArraylakeServerError with correlation ID"""
    mock_request = httpx.Request("GET", "https://foo.smerfmover.io/repos/org/repo")
    mock_response = httpx.Response(
        500,
        request=mock_request,
        content=json_lib.dumps({"detail": "Internal server error"}),
        headers={"Content-Type": "application/json", "x-request-id": "server-error-id"},
    )
    with pytest.raises(ArraylakeServerError) as exc_info:
        handle_response(mock_response)

    exc = exc_info.value
    assert exc.request_id == "server-error-id"
    assert exc.status_code == 500
    assert "Error response 500" in str(exc)
    assert "[request-id: server-error-id]" in str(exc)
    assert isinstance(exc, ValueError)  # Backward compatibility


def test_handle_response_no_correlation_id() -> None:
    """Test that errors without x-request-id header still work"""
    mock_request = httpx.Request("GET", "https://foo.smerfmover.io/repos/org/repo")
    mock_response = httpx.Response(
        404,
        request=mock_request,
        content=json_lib.dumps({"detail": "Not found"}),
        headers={"Content-Type": "application/json"},  # No x-request-id header
    )
    with pytest.raises(ArraylakeClientError) as exc_info:
        handle_response(mock_response)

    exc = exc_info.value
    assert exc.request_id is None
    assert exc.status_code == 404
    assert "[request-id:" not in str(exc)  # Should not include request-id in message
    assert "Error response 404" in str(exc)


def test_handle_response_request_error() -> None:
    """Test that RequestError includes correlation ID in error message"""
    mock_request = httpx.Request("GET", "https://foo.smerfmover.io/repos/org/repo")
    mock_response = httpx.Response(
        200,  # Use valid status code since we're testing RequestError path
        request=mock_request,
        content="",
        headers={"x-request-id": "request-error-id"},
    )

    # Directly test the RequestError handling path in handle_response
    # by simulating what happens when httpx raises a RequestError
    with pytest.raises(ArraylakeHttpError) as exc_info:
        try:
            raise httpx.RequestError("Connection failed", request=mock_request)
        except httpx.RequestError as exc:
            # This simulates the RequestError handling in handle_response
            request_id = mock_response.headers.get("x-request-id")
            error_msg = f"An error occurred while requesting {exc.request.url!r}. {mock_response}: {mock_response.text}"
            raise ArraylakeHttpError(error_msg, request_id=request_id) from exc

    exc = exc_info.value
    assert exc.request_id == "request-error-id"
    assert "[request-id: request-error-id]" in str(exc)


@pytest.mark.parametrize(
    "status_code,expected_exception_class",
    [
        (400, ArraylakeClientError),
        (401, ArraylakeClientError),
        (403, ArraylakeClientError),
        (404, ArraylakeClientError),
        (422, ArraylakeValidationError),
        (429, ArraylakeClientError),
        (500, ArraylakeServerError),
        (502, ArraylakeServerError),
        (503, ArraylakeServerError),
    ],
)
def test_handle_response_exception_mapping(status_code: int, expected_exception_class: type[ArraylakeHttpError]) -> None:
    """Test that different status codes map to the correct exception classes"""
    mock_request = httpx.Request("GET", "https://foo.smerfmover.io/test")
    mock_response = httpx.Response(
        status_code,
        request=mock_request,
        content=json_lib.dumps({"detail": f"Error {status_code}"}),
        headers={"Content-Type": "application/json", "x-request-id": f"test-{status_code}"},
    )

    with pytest.raises(expected_exception_class) as exc_info:
        handle_response(mock_response)

    exc = exc_info.value
    assert exc.request_id == f"test-{status_code}"
    assert exc.status_code == status_code
    assert isinstance(exc, ValueError)  # All should inherit from ValueError


@pytest.mark.asyncio
@pytest.mark.parametrize("verify_ssl", [True, False])
async def test_config_verify_ssl(respx_mock, verify_ssl):
    import ssl

    mock_url = "https://foo.bar/"
    _route = respx_mock.request("GET", mock_url).mock(side_effect=[httpx.ConnectError, httpx.Response(200)])

    with config.set({"service.ssl.verify": verify_ssl}):
        client = ArraylakeHttpClient(mock_url)

        # This triggers building the client
        _ = await client._request("GET", "")

    verify_mode = ssl.CERT_REQUIRED if verify_ssl else ssl.CERT_NONE
    assert client._get_client()._transport.wrapped_transport._pool._ssl_context.verify_mode == verify_mode


@pytest.mark.asyncio
@pytest.mark.parametrize("cafile", [None, "/path/to/cafile"])
async def test_config_custom_ssl_cert(respx_mock, cafile):
    import ssl

    mock_url = "https://foo.bar/"
    _route = respx_mock.request("GET", mock_url).mock(side_effect=[httpx.ConnectError, httpx.Response(200)])

    with config.set({"service.ssl.cafile": cafile}):
        client = ArraylakeHttpClient(mock_url)

        if not cafile:
            _ = await client._request("GET", "")
            assert client._get_client()._transport.wrapped_transport._pool._ssl_context.verify_mode == ssl.CERT_REQUIRED
        else:
            # This error shwos us the cert was passed through to the ssl context
            # but fails because the cert file does not exist
            with pytest.raises(FileNotFoundError):
                _ = await client._request("GET", "")


def test_separate_loops(respx_mock):
    mock_url = "https://foo.bar/"
    client = ArraylakeHttpClient(mock_url)
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    async def _request():
        return await client._request("GET", "")

    loop1 = asyncio.new_event_loop()
    loop2 = asyncio.new_event_loop()

    loop1.run_until_complete(_request())
    loop1.close()
    loop2.run_until_complete(_request())
    loop2.close()

    # make sure there is one client cached per event loop
    assert len(client._clients) == 2
    assert loop1 in client._clients
    assert loop2 in client._clients


# Proxy functionality tests


def _extract_proxy_url_string(proxy_url) -> str:
    """Helper to extract proxy URL string from httpcore.URL object"""
    return f"{proxy_url.scheme.decode()}://{proxy_url.host.decode()}:{proxy_url.port}"


def test_get_proxy_from_env_https_proxy(monkeypatch) -> None:
    """Test proxy detection prioritizes HTTPS_PROXY"""
    monkeypatch.setenv("HTTPS_PROXY", "https://proxy1.example.com:8080")
    monkeypatch.setenv("HTTP_PROXY", "http://proxy2.example.com:3128")

    proxy = _get_proxy_from_env()
    assert proxy == "https://proxy1.example.com:8080"


def test_get_proxy_from_env_http_proxy_fallback(monkeypatch) -> None:
    """Test proxy detection falls back to HTTP_PROXY"""
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    monkeypatch.setenv("HTTP_PROXY", "http://proxy.example.com:3128")

    proxy = _get_proxy_from_env()
    assert proxy == "http://proxy.example.com:3128"


def test_get_proxy_from_env_lowercase_vars(monkeypatch) -> None:
    """Test proxy detection works with lowercase environment variables"""
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    monkeypatch.delenv("HTTP_PROXY", raising=False)
    monkeypatch.setenv("https_proxy", "https://proxy.example.com:8080")

    proxy = _get_proxy_from_env()
    assert proxy == "https://proxy.example.com:8080"


def test_get_proxy_from_env_all_proxy(monkeypatch) -> None:
    """Test proxy detection falls back to ALL_PROXY"""
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    monkeypatch.delenv("HTTP_PROXY", raising=False)
    monkeypatch.delenv("https_proxy", raising=False)
    monkeypatch.delenv("http_proxy", raising=False)
    monkeypatch.setenv("ALL_PROXY", "http://proxy.example.com:8080")

    proxy = _get_proxy_from_env()
    assert proxy == "http://proxy.example.com:8080"


def test_get_proxy_from_env_no_proxy(monkeypatch) -> None:
    """Test proxy detection returns None when no proxy vars set"""
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    proxy = _get_proxy_from_env()
    assert proxy is None


def test_get_proxy_from_env_strips_whitespace(monkeypatch) -> None:
    """Test proxy detection strips whitespace from proxy URLs"""
    monkeypatch.setenv("HTTPS_PROXY", "  https://proxy.example.com:8080  ")

    proxy = _get_proxy_from_env()
    assert proxy == "https://proxy.example.com:8080"


def test_async_retry_transport_explicit_proxy() -> None:
    """Test AsyncRetryTransport uses explicitly provided proxy"""
    transport = AsyncRetryTransport(proxy="http://explicit.proxy.com:8080")
    # With proxy, the pool should be AsyncHTTPProxy type
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncHTTPProxy"
    # Check the proxy URL is correctly set
    proxy_url = transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url) == "http://explicit.proxy.com:8080"


def test_async_retry_transport_auto_detect_proxy(monkeypatch) -> None:
    """Test AsyncRetryTransport auto-detects proxy from environment"""
    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:3128")

    transport = AsyncRetryTransport()
    # With proxy, the pool should be AsyncHTTPProxy type
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncHTTPProxy"
    # Check the proxy URL is correctly set
    proxy_url = transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url) == "http://env.proxy.com:3128"


def test_async_retry_transport_no_proxy(monkeypatch) -> None:
    """Test AsyncRetryTransport works without proxy"""
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    transport = AsyncRetryTransport()
    # Without proxy, the pool should be AsyncConnectionPool type
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncConnectionPool"


def test_async_retry_transport_explicit_overrides_env(monkeypatch) -> None:
    """Test explicit proxy parameter overrides environment variables"""
    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:3128")

    transport = AsyncRetryTransport(proxy="http://explicit.proxy.com:8080")
    # Check the explicit proxy URL is used, not the environment one
    proxy_url = transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url) == "http://explicit.proxy.com:8080"


def test_async_retry_transport_empty_string_disables_proxy(monkeypatch) -> None:
    """Test empty string proxy parameter disables proxy even with env vars"""
    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:3128")

    transport = AsyncRetryTransport(proxy="")
    # Empty string should disable proxy, resulting in AsyncConnectionPool
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncConnectionPool"


def test_arraylake_http_client_explicit_proxy() -> None:
    """Test ArraylakeHttpClient accepts explicit proxy parameter"""
    client = ArraylakeHttpClient("https://api.example.com", proxy="http://proxy.example.com:8080")
    assert client.proxy == "http://proxy.example.com:8080"


def test_arraylake_http_client_no_proxy() -> None:
    """Test ArraylakeHttpClient works without proxy"""
    client = ArraylakeHttpClient("https://api.example.com")
    assert client.proxy is None


def test_arraylake_http_client_serialization_with_proxy() -> None:
    """Test ArraylakeHttpClient serialization includes proxy"""
    client = ArraylakeHttpClient("https://api.example.com", proxy="http://proxy.example.com:8080")

    # Test serialization
    serialized = client.__getstate__()
    assert "http://proxy.example.com:8080" in serialized

    # Test deserialization
    new_client = ArraylakeHttpClient("https://api.example.com")
    new_client.__setstate__(serialized)
    assert new_client.proxy == "http://proxy.example.com:8080"


@pytest.mark.asyncio
async def test_proxy_passed_to_transport(respx_mock, monkeypatch) -> None:
    """Test that proxy configuration is passed through to the transport layer"""
    # Clear any existing proxy environment variables
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    mock_url = "https://foo.bar/"
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    # Test explicit proxy
    client = ArraylakeHttpClient(mock_url, proxy="http://proxy.example.com:8080")
    response = await client._request("GET", "")
    assert response.status_code == 200

    # Verify the transport was created with the proxy
    transport = client._get_client()._transport
    assert hasattr(transport, "wrapped_transport")
    # The proxy is configured on the underlying HTTPTransport
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncHTTPProxy"
    proxy_url = transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url) == "http://proxy.example.com:8080"


@pytest.mark.asyncio
async def test_proxy_from_environment_integration(respx_mock, monkeypatch) -> None:
    """Test end-to-end proxy configuration from environment variables"""
    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set proxy environment variable
    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:3128")

    mock_url = "https://foo.bar/"
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    # Client should auto-detect proxy from environment
    client = ArraylakeHttpClient(mock_url)
    response = await client._request("GET", "")
    assert response.status_code == 200

    # Verify the transport was created with the proxy from environment
    transport = client._get_client()._transport
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncHTTPProxy"
    proxy_url = transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url) == "http://env.proxy.com:3128"


def test_proxy_authentication_url_format() -> None:
    """Test proxy URL with authentication credentials"""
    client = ArraylakeHttpClient("https://api.example.com", proxy="http://user:pass@proxy.example.com:8080")
    assert client.proxy == "http://user:pass@proxy.example.com:8080"


@pytest.mark.asyncio
async def test_different_proxy_configurations_create_separate_clients(respx_mock) -> None:
    """Test that different proxy configurations result in separate cached clients"""
    mock_url = "https://foo.bar/"
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    # Create clients with different proxy configurations
    client1 = ArraylakeHttpClient(mock_url, proxy="http://proxy1.example.com:8080")
    client2 = ArraylakeHttpClient(mock_url, proxy="http://proxy2.example.com:3128")
    client3 = ArraylakeHttpClient(mock_url)  # no proxy

    # Make requests to initialize clients
    await client1._request("GET", "")
    await client2._request("GET", "")
    await client3._request("GET", "")

    # Verify each has its own cached client
    httpx_client1 = client1._get_client()
    httpx_client2 = client2._get_client()
    httpx_client3 = client3._get_client()

    # All should be different client instances
    assert httpx_client1 is not httpx_client2
    assert httpx_client2 is not httpx_client3
    assert httpx_client1 is not httpx_client3

    # Verify proxy configurations
    proxy_url1 = httpx_client1._transport.wrapped_transport._pool._proxy_url
    proxy_url2 = httpx_client2._transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url1) == "http://proxy1.example.com:8080"
    assert _extract_proxy_url_string(proxy_url2) == "http://proxy2.example.com:3128"
    # Client3 should have no proxy (AsyncConnectionPool)
    assert type(httpx_client3._transport.wrapped_transport._pool).__name__ == "AsyncConnectionPool"


@pytest.mark.asyncio
async def test_same_proxy_configuration_shares_client(respx_mock) -> None:
    """Test that same proxy configuration shares cached client"""
    mock_url = "https://foo.bar/"
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    # Create two clients with same proxy configuration
    client1 = ArraylakeHttpClient(mock_url, proxy="http://proxy.example.com:8080")
    client2 = ArraylakeHttpClient(mock_url, proxy="http://proxy.example.com:8080")

    # Make requests to initialize clients
    await client1._request("GET", "")
    await client2._request("GET", "")

    # Should share the same cached httpx client
    httpx_client1 = client1._get_client()
    httpx_client2 = client2._get_client()

    assert httpx_client1 is httpx_client2


# Config-based proxy detection tests


def test_get_proxy_from_config_priority(monkeypatch) -> None:
    """Test that config proxy takes priority over environment variables"""
    from arraylake.config import config

    # Clear environment variables
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set both config and environment
    config.set({"service.proxy": "http://config.proxy.com:8080"})
    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:3128")

    proxy = _get_proxy_from_env()
    assert proxy == "http://config.proxy.com:8080"

    # Clean up
    config.clear()


def test_get_proxy_from_config_only(monkeypatch) -> None:
    """Test proxy detection from config when no environment variables"""
    from arraylake.config import config

    # Clear environment variables
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set only config
    config.set({"service.proxy": "http://config.proxy.com:8080"})

    proxy = _get_proxy_from_env()
    assert proxy == "http://config.proxy.com:8080"

    # Clean up
    config.clear()


def test_get_proxy_fallback_to_env_when_no_config(monkeypatch) -> None:
    """Test fallback to environment variables when no config proxy"""
    from arraylake.config import config

    # Clear config
    config.clear()

    # Clear environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set environment variable
    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:3128")

    proxy = _get_proxy_from_env()
    assert proxy == "http://env.proxy.com:3128"


def test_get_proxy_config_strips_whitespace() -> None:
    """Test that config proxy URLs are stripped of whitespace"""
    from arraylake.config import config

    config.set({"service.proxy": "  http://config.proxy.com:8080  "})

    proxy = _get_proxy_from_env()
    assert proxy == "http://config.proxy.com:8080"

    # Clean up
    config.clear()


def test_get_proxy_config_empty_string() -> None:
    """Test that empty string in config is treated as no proxy"""
    from arraylake.config import config

    config.set({"service.proxy": ""})

    proxy = _get_proxy_from_env()
    assert proxy is None

    # Clean up
    config.clear()


def test_get_proxy_config_none_value() -> None:
    """Test that None value in config falls back to environment"""
    import os

    from arraylake.config import config

    # Clear environment first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        os.environ.pop(var, None)

    # Set config to None (should fall back to environment)
    config.set({"service.proxy": None})
    os.environ["HTTPS_PROXY"] = "http://env.proxy.com:3128"

    proxy = _get_proxy_from_env()
    assert proxy == "http://env.proxy.com:3128"

    # Clean up
    config.clear()
    os.environ.pop("HTTPS_PROXY", None)


def test_arraylake_http_client_config_proxy() -> None:
    """Test ArraylakeHttpClient uses config proxy when no explicit proxy provided"""
    from arraylake.config import config

    # Set config proxy
    config.set({"service.proxy": "http://config.proxy.com:8080"})

    # Create client without explicit proxy
    client = ArraylakeHttpClient("https://api.example.com")
    assert client.proxy == "http://config.proxy.com:8080"

    # Clean up
    config.clear()


def test_arraylake_http_client_explicit_overrides_config() -> None:
    """Test that explicit proxy parameter overrides config proxy"""
    from arraylake.config import config

    # Set config proxy
    config.set({"service.proxy": "http://config.proxy.com:8080"})

    # Create client with explicit proxy
    client = ArraylakeHttpClient("https://api.example.com", proxy="http://explicit.proxy.com:3128")
    assert client.proxy == "http://explicit.proxy.com:3128"

    # Clean up
    config.clear()


def _ok_response(headers: dict[str, str] | None = None) -> httpx.Response:
    return httpx.Response(200, request=httpx.Request("GET", "https://example.com/api"), headers=headers or {})


def test_deprecation_warnings() -> None:
    import warnings

    _emitted_deprecation_warnings.clear()

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        # no header -> no warning
        handle_response(_ok_response())
        # header -> warning
        handle_response(_ok_response({"X-Deprecation-Warning": "A is deprecated"}))
        # same message again -> deduplicated
        handle_response(_ok_response({"X-Deprecation-Warning": "A is deprecated"}))
        # different message -> new warning
        handle_response(_ok_response({"X-Deprecation-Warning": "B is deprecated"}))

    deprecation_warnings = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert len(deprecation_warnings) == 2
    assert "A is deprecated" in str(deprecation_warnings[0].message)
    assert "B is deprecated" in str(deprecation_warnings[1].message)


@pytest.mark.asyncio
async def test_config_proxy_end_to_end_integration(respx_mock, monkeypatch) -> None:
    """Test end-to-end proxy configuration via arraylake config"""
    from arraylake.config import config

    # Clear environment variables
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set proxy via config
    config.set({"service.proxy": "http://config.proxy.com:8080"})

    mock_url = "https://foo.bar/"
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    # Client should auto-detect proxy from config
    client = ArraylakeHttpClient(mock_url)
    response = await client._request("GET", "")
    assert response.status_code == 200

    # Verify the transport was created with the proxy from config
    transport = client._get_client()._transport
    assert type(transport.wrapped_transport._pool).__name__ == "AsyncHTTPProxy"
    proxy_url = transport.wrapped_transport._pool._proxy_url
    assert _extract_proxy_url_string(proxy_url) == "http://config.proxy.com:8080"

    # Clean up
    config.clear()
