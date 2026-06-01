import json as json_lib
from pathlib import Path

import httpx
import pytest
import respx
from pydantic import SecretStr

from arraylake.api_utils import UserAuth
from arraylake.config import config
from arraylake.token import AuthException, TokenHandler
from arraylake.types import OauthTokens


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


def test_token_handler_create_client_with_proxy(monkeypatch, tmp_path):
    """Test that TokenHandler creates httpx clients with proper proxy configuration"""
    from unittest.mock import MagicMock, patch

    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set environment proxy
    monkeypatch.setenv("HTTPS_PROXY", "http://test.proxy.com:8080")

    bad_token_file = tmp_path / "tokens.json"
    with config.set({"service.token_path": str(bad_token_file)}):
        handler = TokenHandler()
        assert handler.proxy == "http://test.proxy.com:8080"

        # Test sync client creation with proxy
        with patch("httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Create a sync client
            client = handler._create_client()

            # Verify httpx.Client was called with proxy configuration
            mock_client_class.assert_called_once()
            call_kwargs = mock_client_class.call_args.kwargs

            # Verify proxy is passed correctly (either string or httpx.Proxy object)
            assert "proxy" in call_kwargs
            proxy_arg = call_kwargs["proxy"]
            assert proxy_arg is not None
            # The proxy should be cast for httpx version compatibility
            # It's either the original string or an httpx.Proxy object
            if hasattr(proxy_arg, "url"):
                # It's an httpx.Proxy object
                assert str(proxy_arg.url) == "http://test.proxy.com:8080"
            else:
                # It's a string
                assert proxy_arg == "http://test.proxy.com:8080"

            # Verify SSL settings are also passed
            assert call_kwargs["verify"] == handler.verify_ssl
            assert call_kwargs["cert"] == handler.ssl_cafile

        # Test async client creation with proxy
        with patch("httpx.AsyncClient") as mock_async_client_class:
            mock_async_client = MagicMock()
            mock_async_client_class.return_value = mock_async_client

            # Create an async client
            async_client = handler._create_async_client()

            # Verify httpx.AsyncClient was called with proxy configuration
            mock_async_client_class.assert_called_once()
            call_kwargs = mock_async_client_class.call_args.kwargs

            # Verify proxy is passed correctly (either string or httpx.Proxy object)
            assert "proxy" in call_kwargs
            proxy_arg = call_kwargs["proxy"]
            assert proxy_arg is not None
            # The proxy should be cast for httpx version compatibility
            if hasattr(proxy_arg, "url"):
                # It's an httpx.Proxy object
                assert str(proxy_arg.url) == "http://test.proxy.com:8080"
            else:
                # It's a string
                assert proxy_arg == "http://test.proxy.com:8080"

            # Verify SSL settings are also passed
            assert call_kwargs["verify"] == handler.verify_ssl
            assert call_kwargs["cert"] == handler.ssl_cafile


def test_token_handler_create_client_no_proxy(monkeypatch, tmp_path):
    """Test that TokenHandler creates httpx clients without proxy when not configured"""
    from unittest.mock import MagicMock, patch

    # Clear any existing proxy environment variables
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    bad_token_file = tmp_path / "tokens.json"
    with config.set({"service.token_path": str(bad_token_file)}):
        handler = TokenHandler()
        assert handler.proxy is None

        # Test sync client creation without proxy
        with patch("httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            client = handler._create_client()

            # Verify httpx.Client was called without proxy
            mock_client_class.assert_called_once()
            call_kwargs = mock_client_class.call_args.kwargs

            # Proxy should not be in kwargs when not configured
            assert "proxy" not in call_kwargs

        # Test async client creation without proxy
        with patch("httpx.AsyncClient") as mock_async_client_class:
            mock_async_client = MagicMock()
            mock_async_client_class.return_value = mock_async_client

            async_client = handler._create_async_client()

            # Verify httpx.AsyncClient was called without proxy
            mock_async_client_class.assert_called_once()
            call_kwargs = mock_async_client_class.call_args.kwargs

            # Proxy should not be in kwargs when not configured
            assert "proxy" not in call_kwargs


def test_token_handler_create_client_with_config_proxy(monkeypatch, tmp_path):
    """Test that TokenHandler creates httpx clients with config-based proxy"""
    from unittest.mock import MagicMock, patch

    # Clear any existing proxy environment variables first
    proxy_vars = ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
    for var in proxy_vars:
        monkeypatch.delenv(var, raising=False)

    # Set both environment and config proxy (config should take priority)
    monkeypatch.setenv("HTTPS_PROXY", "http://env.proxy.com:8080")

    bad_token_file = tmp_path / "tokens.json"
    config_proxy = "http://config.proxy.com:3128"
    with config.set({"service.token_path": str(bad_token_file), "service.proxy": config_proxy}):
        handler = TokenHandler()
        assert handler.proxy == config_proxy

        # Test that the config proxy is used in client creation
        with patch("httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            client = handler._create_client()

            mock_client_class.assert_called_once()
            call_kwargs = mock_client_class.call_args.kwargs

            assert "proxy" in call_kwargs
            proxy_arg = call_kwargs["proxy"]
            assert proxy_arg is not None

            # Verify the config proxy is used (not the environment one)
            if hasattr(proxy_arg, "url"):
                assert str(proxy_arg.url) == config_proxy
            else:
                assert proxy_arg == config_proxy
