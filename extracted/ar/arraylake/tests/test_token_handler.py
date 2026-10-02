import asyncio
import json as json_lib
from pathlib import Path

import httpx
import pytest
import respx
from pydantic import SecretStr

from arraylake.api_utils import UserAuth
from arraylake.config import config
from arraylake.token import AuthException, TokenHandler, resolve_token_path
from arraylake.types import AuthProviderConfig, OauthTokens


def test_token_handler_init(test_token_file, helpers) -> None:
    test_tokens = helpers.oauth_tokens_from_file(test_token_file)
    url = "https://foo.com"
    token_handler = TokenHandler(api_endpoint=url)
    assert url == token_handler.api_endpoint
    assert test_token_file == token_handler.token_path
    assert token_handler.tokens == test_tokens


def test_token_handler_init_when_not_logged_in(tmp_path) -> None:
    bad_token_file = tmp_path / "tokens.json"
    with config.set({"service.token_path": str(bad_token_file)}):
        handler = TokenHandler()
        assert handler.token_path == bad_token_file
        assert handler.tokens is None


def test_resolve_token_path_default_endpoint_uses_legacy_path() -> None:
    legacy = Path("~/.arraylake/token.json").expanduser()
    with config.set({"service.token_path": None}):
        assert resolve_token_path("https://api.earthmover.io") == legacy
        assert resolve_token_path("https://api.earthmover.io/") == legacy


def test_resolve_token_path_non_default_endpoint_is_per_environment() -> None:
    with config.set({"service.token_path": None}):
        assert resolve_token_path("http://localhost:8000") == Path("~/.arraylake/tokens/localhost_8000.json").expanduser()
        assert resolve_token_path("https://api.dev.earthmover.io") == Path("~/.arraylake/tokens/api.dev.earthmover.io.json").expanduser()


def test_resolve_token_path_explicit_config_wins(tmp_path) -> None:
    explicit = tmp_path / "custom-token.json"
    with config.set({"service.token_path": str(explicit)}):
        assert resolve_token_path("http://localhost:8000") == explicit
        assert resolve_token_path("https://api.earthmover.io") == explicit


def test_resolve_token_path_environments_are_isolated() -> None:
    with config.set({"service.token_path": None}):
        paths = {
            resolve_token_path("https://api.earthmover.io"),
            resolve_token_path("https://api.dev.earthmover.io"),
            resolve_token_path("http://localhost:8000"),
        }
        assert len(paths) == 3


def test_cache_creates_per_environment_directory(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    with config.set({"service.token_path": None}):
        handler = TokenHandler(api_endpoint="http://localhost:8000")
        assert handler.tokens is None
        handler.tokens = OauthTokens(access_token="a", id_token="b", refresh_token="c", expires_in=300, token_type="Bearer")
        handler.cache()

    expected = tmp_path / ".arraylake" / "tokens" / "localhost_8000.json"
    assert expected.is_file()
    assert expected.stat().st_mode == 0o100600


@pytest.mark.parametrize(
    "contents,match", [("", ".* malformed auth tokens.*"), ("not a valid json", ".* malformed auth tokens.*"), ('{"token": "abc"}', None)]
)
def test_malformed_tokens_raise(tmp_path, contents, match) -> None:
    bad_token_file = tmp_path / "tokens.json"
    with bad_token_file.open(mode="w") as f:
        f.write(contents)
    with config.set({"service.token_path": str(bad_token_file)}):
        with pytest.raises(AuthException, match=r".* malformed auth tokens.*"):
            TokenHandler(raise_if_not_logged_in=True)


def test_token_model_roundtrips(tmp_path, helpers) -> None:
    tokens_dict = dict(
        access_token="test_access_token_response",
        id_token="test_id_token_response",
        refresh_token="test_refresh_token_response",
        expires_in=3600,
        token_type="Bearer",
    )

    tokens = OauthTokens(**tokens_dict)
    token_file = tmp_path / "tokens.json"
    with token_file.open(mode="w") as f:
        f.write(tokens.model_dump_json())

    tokens2 = helpers.oauth_tokens_from_file(token_file)
    assert tokens_dict == tokens2.model_dump()
    assert tokens.model_dump() == tokens2.model_dump()
    assert tokens.model_dump_json() == tokens2.model_dump_json()


def test_token_model_does_not_show_secrets() -> None:
    tokens_dict = dict(
        access_token="test_access_token_response",
        id_token="test_id_token_response",
        refresh_token="test_refresh_token_response",
        expires_in=3600,
        token_type="Bearer",
    )

    tokens = OauthTokens(**tokens_dict)

    assert tokens.dict() == tokens_dict
    assert "test_refresh_token_response" not in repr(tokens)
    assert "test_refresh_token_response" not in str(tokens)
    assert "test_refresh_token_response" in tokens.model_dump_json()


@pytest.mark.asyncio
async def test_token_handler_login_auth_flow(test_token_file, respx_mock, helpers) -> None:
    test_tokens = helpers.oauth_tokens_from_file(test_token_file)
    test_tokens_data = test_tokens.model_dump()

    # we test the refresh flow, which yields a new set of id+access tokens
    # this object is what we expect our handler token state to look like after refresh
    refreshed_test_tokens = test_tokens.model_copy(
        update={"id_token": SecretStr("new-id-token"), "access_token": SecretStr("new-access-token")}
    )
    refreshed_test_tokens_data = refreshed_test_tokens.model_dump()

    test_token_file.unlink()  # start "logged out"
    api_url = "https://foo.com"
    auth_domain = "foo.us.auth0.com"
    client_id = "abcDEF123456789"
    scopes = ["email", "openid", "profile", "offline_access"]
    device_code = "def456789"

    provider_info_route = respx_mock.get(f"{api_url}/auth/config", params={"target": "client"}).mock(
        return_value=httpx.Response(httpx.codes.OK, json={"domain": auth_domain, "client_id": client_id})
    )

    # json={"client_id": client_id, "scope": " ".join(scopes)}
    device_code_route = respx_mock.post(f"https://{auth_domain}/oauth/device/code").mock(
        return_value=httpx.Response(
            httpx.codes.OK,
            json={
                "verification_uri_complete": "https://foo.com/token",
                "user_code": "ABC-123",
                "device_code": device_code,
                "interval": 1,
                "expires_in": 3600,
            },
        )
    )

    # json={"grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    #       "device_code": device_code,
    #       "client_id": client_id,
    #       }
    token_route = respx_mock.post(f"https://{auth_domain}/oauth/token")
    token_route.side_effect = [
        httpx.Response(httpx.codes.TOO_MANY_REQUESTS, json={"error": "authorization_pending"}),
        httpx.Response(httpx.codes.TOO_MANY_REQUESTS, json={"error": "slow_down"}),
        httpx.Response(  # successful login
            httpx.codes.OK,
            json=test_tokens_data,
        ),
        httpx.Response(  # refresh
            httpx.codes.OK,
            json=refreshed_test_tokens_data,
        ),
    ]

    user_info = {"id": "2eb77e18-884a-4b01-b85c-46ad169ad39f", "first_name": "John", "last_name": "Doe", "email": "jQqzH@example.com"}

    user_route = respx_mock.request("GET", f"{api_url}/user").mock(return_value=httpx.Response(httpx.codes.OK, json=user_info))

    respx_mock.request("POST", f"{api_url}/auth/update-user").mock(return_value=httpx.Response(httpx.codes.OK, json=user_info))

    logout_route = respx_mock.request("GET", f"https://{auth_domain}/v2/logout").mock(return_value=httpx.Response(httpx.codes.OK))

    handler = TokenHandler(api_endpoint=api_url, scopes=scopes, raise_if_not_logged_in=False)
    assert handler.tokens is None
    with pytest.raises(AuthException):
        UserAuth(api_url)

    # login
    await handler.login(browser=False)
    auth = UserAuth(api_url)
    handler.tokens == test_tokens

    # refresh
    await handler.refresh_token()
    handler.tokens.model_dump() == refreshed_test_tokens

    # logout
    assert test_token_file.exists()
    await handler.logout()
    assert handler.tokens is None
    assert not test_token_file.exists()
    with pytest.raises(AuthException):
        UserAuth(api_url)


def test_token_handler_update_tokens(test_token_file, helpers) -> None:
    test_token_file.unlink()
    test_tokens1 = OauthTokens(access_token="abcdef", id_token="123456", refresh_token="abc123", expires_in=300, token_type="Bearer")
    handler = TokenHandler()

    assert handler.tokens == None
    assert not test_token_file.exists()

    handler.update(new_token_data=test_tokens1.model_dump())

    assert handler.tokens == test_tokens1
    assert test_token_file.exists()
    assert helpers.oauth_tokens_from_file(test_token_file) == test_tokens1

    test_tokens2 = OauthTokens(
        access_token="abcdef-234", id_token="123456-abc", refresh_token="abc123-dkdk", expires_in=500, token_type="Bearer"
    )
    handler.update(new_token_data=test_tokens2.model_dump())
    assert handler.tokens == test_tokens2
    assert test_token_file.exists()
    assert helpers.oauth_tokens_from_file(test_token_file) == test_tokens2


@pytest.mark.asyncio
async def test_token_handler_get_authorize_config_raises(test_token_file, respx_mock) -> None:
    api_url = "https://foo.com"
    login_url = "https://foo.com/auth/config"
    login_route = respx_mock.get(login_url, params={"target": "client"}).mock(return_value=httpx.Response(httpx.codes.NOT_FOUND))

    handler = TokenHandler(api_url)
    with pytest.raises(AuthException, match="Error getting auth configuration"):
        await handler.login(browser=False)


@pytest.mark.asyncio
async def test_token_handler_get_token_raises(test_token_file, respx_mock) -> None:
    api_url = "https://foo.com"
    auth_domain = "bar.com"
    provider_info_route = respx_mock.get(api_url + "/auth/config", params={"target": "client"}).mock(
        return_value=httpx.Response(httpx.codes.OK, json={"domain": auth_domain, "client_id": "123"})
    )
    token_route = respx_mock.post(f"https://{auth_domain}/oauth/token").mock(return_value=httpx.Response(httpx.codes.NOT_FOUND))

    handler = TokenHandler(api_url)
    with pytest.raises(AuthException, match="Error getting token"):
        await handler.get_token("test-token-1234567890", interval=5, expires_in=10)


@pytest.mark.asyncio
async def test_get_auth_provider_config_is_cached(test_token_file, respx_mock) -> None:
    api_url = "https://foo.com"
    auth_domain = "bar.auth0.com"
    route = respx_mock.get(api_url + "/auth/config", params={"target": "client"}).mock(
        return_value=httpx.Response(httpx.codes.OK, json={"domain": auth_domain, "client_id": "123"})
    )

    handler = TokenHandler(api_url)
    config = await handler.get_auth_provider_config()
    assert config.domain == auth_domain

    config_again = await handler.get_auth_provider_config()
    assert config_again is config
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_get_auth_provider_config_coalesces_concurrent_calls(test_token_file) -> None:
    handler = TokenHandler("https://foo.com")
    fetches = 0

    async def _fetch() -> AuthProviderConfig:
        nonlocal fetches
        fetches += 1
        await asyncio.sleep(0.05)
        return AuthProviderConfig(domain="bar.auth0.com", client_id="123")

    handler._fetch_auth_provider_config = _fetch  # type: ignore[method-assign]

    results = await asyncio.gather(*[handler.get_auth_provider_config() for _ in range(5)])
    assert fetches == 1
    assert all(result is results[0] for result in results)


@pytest.mark.parametrize("exc", [httpx.ConnectError("boom"), httpx.ConnectTimeout("boom")])
@pytest.mark.asyncio
async def test_get_auth_provider_config_connect_errors_raise_auth_exception(test_token_file, respx_mock, exc) -> None:
    api_url = "https://foo.com"
    respx_mock.get(api_url + "/auth/config", params={"target": "client"}).mock(side_effect=exc)

    handler = TokenHandler(api_url)
    with pytest.raises(AuthException, match="Could not connect"):
        await handler.get_auth_provider_config()


@pytest.mark.asyncio
async def test_refresh_token_raises_on_error_status(test_token_file, respx_mock, mock_auth_provider_config) -> None:
    handler = TokenHandler("https://foo.com")
    respx_mock.post(f"https://{mock_auth_provider_config.domain}/oauth/token").mock(
        return_value=httpx.Response(httpx.codes.FORBIDDEN, json={"error": "invalid_grant"})
    )
    with pytest.raises(AuthException, match="Error getting refresh token"):
        await handler.refresh_token()


def test_token_handler_cache(test_token_file, helpers) -> None:
    tokens = helpers.oauth_tokens_from_file(test_token_file)
    test_token_file.unlink()
    handler = TokenHandler()
    assert handler.tokens is None
    with pytest.raises(ValueError, match="Error saving tokens, no tokens to cache"):
        handler.cache()

    handler.tokens = tokens

    handler.cache()
    assert test_token_file.is_file()
    assert test_token_file.stat().st_mode == 0o100600  # -rw-------

    # check that we successfully round tripped the tokens
    helpers.oauth_tokens_from_file(test_token_file) == tokens


# Proxy configuration tests for login flow
def test_token_handler_proxy_from_environment(monkeypatch, tmp_path):
    """Test TokenHandler detects proxy from environment variables"""
    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set environment proxy
    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:8080")

    bad_token_file = tmp_path / "tokens.json"
    with config.set({"service.token_path": str(bad_token_file)}):
        handler = TokenHandler()
        assert handler.proxy == "http://env.proxy.com:8080"


def test_token_handler_proxy_from_config(monkeypatch, tmp_path):
    """Test TokenHandler uses config proxy with priority over environment"""
    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set both environment and config proxy
    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:8080")

    bad_token_file = tmp_path / "tokens.json"
    with config.set({"service.token_path": str(bad_token_file), "service.proxy": "http://config.proxy.com:3128"}):
        handler = TokenHandler()
        assert handler.proxy == "http://config.proxy.com:3128"


def test_token_handler_no_proxy(monkeypatch, tmp_path):
    """Test TokenHandler works with no proxy configuration"""
    # Clear any existing proxy environment variables
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    bad_token_file = tmp_path / "tokens.json"
    with config.set({"service.token_path": str(bad_token_file)}):
        handler = TokenHandler()
        assert handler.proxy is None


@pytest.mark.parametrize(
    "env_proxy,config_proxy,expected_proxy",
    [
        ("http://test.proxy.com:8080", None, "http://test.proxy.com:8080"),
        (None, None, None),
        ("http://env.proxy.com:8080", "http://config.proxy.com:3128", "http://config.proxy.com:3128"),
    ],
)
def test_token_handler_create_async_client_proxy(monkeypatch, tmp_path, env_proxy, config_proxy, expected_proxy):
    """_create_async_client honors config proxy over environment proxy over none."""
    from unittest.mock import MagicMock, patch

    for var in ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]:
        monkeypatch.delenv(var, raising=False)
    if env_proxy is not None:
        monkeypatch.setenv("HTTPS_PROXY", env_proxy)

    settings = {"service.token_path": str(tmp_path / "tokens.json")}
    if config_proxy is not None:
        settings["service.proxy"] = config_proxy

    with config.set(settings):
        handler = TokenHandler()
        assert handler.proxy == expected_proxy

        with patch("httpx.AsyncClient") as mock_async_client_class:
            mock_async_client_class.return_value = MagicMock()
            handler._create_async_client()

            mock_async_client_class.assert_called_once()
            call_kwargs = mock_async_client_class.call_args.kwargs
            assert call_kwargs["verify"] == handler.verify_ssl
            assert call_kwargs["cert"] == handler.ssl_cafile

            if expected_proxy is None:
                assert "proxy" not in call_kwargs
            else:
                proxy_arg = call_kwargs["proxy"]
                assert (str(proxy_arg.url) if hasattr(proxy_arg, "url") else proxy_arg) == expected_proxy
