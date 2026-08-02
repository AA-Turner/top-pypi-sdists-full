"""Tests for the Tetra browser session API."""

import httpx
import pytest
from mockito import mock, patch, unstub, when
from test.utils.http_mocks import create_fake_async_post, create_fake_post

from agentql import APIKeyError
from agentql.tools.async_api import CustomProxyConfig, TetraProxyConfig
from agentql.tools.async_api import create_browser_session as async_create_browser_session
from agentql.tools.async_api._tetra import tetra as async_tetra
from agentql.tools.sync_api import BrowserProfile, UserAgentPreset, create_browser_session
from agentql.tools.sync_api._tetra import tetra as sync_tetra


@pytest.fixture(autouse=True)
def clean_mockito():
    """Clean up mockito mocks after each test."""
    yield
    unstub()


@pytest.fixture
def mock_api_key():
    """Mock API key for all tests."""
    patch(sync_tetra.get_api_key, lambda: "test-api-key")


@pytest.fixture
def mock_session_response():
    """Standard browser session response."""
    return {"cdp_url": "ws://browser:9222/session/123", "base_url": "https://browser.example.com"}


def mock_http_success(response_data):
    """Mock successful HTTP response."""
    fake_post, _ = create_fake_post(response_data)
    patch(sync_tetra._http_client.post, fake_post)


# Sync tests


def test_create_browser_session_basic(mock_api_key, mock_session_response):
    """Test basic browser session creation without any presets."""
    mock_http_success(mock_session_response)

    session = create_browser_session()

    assert session.cdp_url == "ws://browser:9222/session/123"
    assert session.get_page_streaming_url(0) == "https://browser.example.com/stream/0"


def test_create_browser_session_with_ua_preset(mock_api_key, mock_session_response):
    """Test browser session creation with user agent preset."""
    mock_http_success(mock_session_response)

    session = create_browser_session(ua_preset=UserAgentPreset.WINDOWS)

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_with_browser_profile(mock_api_key, mock_session_response):
    """Test browser session creation with browser profile."""
    mock_http_success(mock_session_response)

    session = create_browser_session(profile=BrowserProfile.STEALTH)

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_with_both_presets(mock_api_key, mock_session_response):
    """Test browser session creation with both user agent preset and browser profile."""
    mock_http_success(mock_session_response)

    session = create_browser_session(ua_preset=UserAgentPreset.MACOS, profile=BrowserProfile.LIGHT)

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_no_api_key():
    """Test that APIKeyError is raised when no API key is set."""
    patch(sync_tetra.get_api_key, lambda: None)

    with pytest.raises(APIKeyError):
        create_browser_session()


def test_create_browser_session_http_error(mock_api_key):
    """Test that HTTPStatusError is raised on API failure."""
    mock_response = mock(httpx.Response)
    mock_error = httpx.HTTPStatusError("Bad Request", request=mock(), response=mock())
    when(mock_response).raise_for_status().thenRaise(mock_error)
    patch(sync_tetra._http_client.post, lambda *args, **kwargs: mock_response)

    with pytest.raises(httpx.HTTPStatusError):
        create_browser_session()


def test_create_browser_session_stealth_with_ua_preset_error():
    """Test that ValueError is raised when ua_preset is used with STEALTH profile."""
    with pytest.raises(ValueError, match="Invalid configuration: ua_preset cannot be specified with STEALTH profile"):
        create_browser_session(ua_preset=UserAgentPreset.WINDOWS, profile=BrowserProfile.STEALTH)


def test_create_browser_session_with_tf_browser_profile(mock_api_key, mock_session_response):
    """Test browser session creation with TF_BROWSER profile."""
    mock_http_success(mock_session_response)

    session = create_browser_session(profile=BrowserProfile.TF_BROWSER)

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_tf_browser_with_ua_preset_error():
    """Test that ValueError is raised when ua_preset is used with TF_BROWSER profile."""
    with pytest.raises(
        ValueError, match="Invalid configuration: ua_preset cannot be specified with TF_BROWSER profile"
    ):
        create_browser_session(ua_preset=UserAgentPreset.WINDOWS, profile=BrowserProfile.TF_BROWSER)


@pytest.fixture
def mock_async_api_key():
    """Mock async API key."""

    async def mock_get_key():
        return "test-api-key"

    patch(async_tetra.get_api_key_async, mock_get_key)


def mock_async_http_success(response_data):
    """Mock successful async HTTP response."""
    fake_post, _ = create_fake_async_post(response_data)
    patch(async_tetra._http_client.post, fake_post)


@pytest.mark.asyncio
async def test_async_create_browser_session_basic(mock_async_api_key, mock_session_response):
    """Test basic async browser session creation."""
    mock_async_http_success(mock_session_response)

    session = await async_create_browser_session()

    assert session.cdp_url == "ws://browser:9222/session/123"


@pytest.mark.asyncio
async def test_async_create_browser_session_with_presets(mock_async_api_key, mock_session_response):
    """Test async browser session creation with both presets."""
    mock_async_http_success(mock_session_response)

    session = await async_create_browser_session(ua_preset=UserAgentPreset.LINUX, profile=BrowserProfile.LIGHT)

    assert session.cdp_url == "ws://browser:9222/session/123"


@pytest.mark.asyncio
async def test_async_create_browser_session_stealth_with_ua_preset_error():
    """Test that ValueError is raised when ua_preset is used with STEALTH profile."""
    with pytest.raises(ValueError, match="Invalid configuration: ua_preset cannot be specified with STEALTH profile"):
        await async_create_browser_session(ua_preset=UserAgentPreset.WINDOWS, profile=BrowserProfile.STEALTH)


@pytest.mark.asyncio
async def test_async_create_browser_session_with_tf_browser_profile(mock_async_api_key, mock_session_response):
    """Test async browser session creation with TF_BROWSER profile."""
    mock_async_http_success(mock_session_response)

    session = await async_create_browser_session(profile=BrowserProfile.TF_BROWSER)

    assert session.cdp_url == "ws://browser:9222/session/123"


@pytest.mark.asyncio
async def test_async_create_browser_session_tf_browser_with_ua_preset_error():
    """Test that ValueError is raised when ua_preset is used with TF_BROWSER profile."""
    with pytest.raises(
        ValueError, match="Invalid configuration: ua_preset cannot be specified with TF_BROWSER profile"
    ):
        await async_create_browser_session(ua_preset=UserAgentPreset.WINDOWS, profile=BrowserProfile.TF_BROWSER)


# Proxy tests


def test_create_browser_session_with_tetra_proxy(mock_api_key, mock_session_response):
    """Test browser session creation with Tetra proxy (default country)."""
    mock_http_success(mock_session_response)

    session = create_browser_session(proxy=TetraProxyConfig())

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_with_tetra_proxy_country(mock_api_key, mock_session_response):
    """Test browser session creation with Tetra proxy (custom country code)."""
    mock_http_success(mock_session_response)

    session = create_browser_session(proxy=TetraProxyConfig(country_code="us"))

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_with_custom_proxy(mock_api_key, mock_session_response):
    """Test browser session creation with custom proxy."""
    mock_http_success(mock_session_response)

    session = create_browser_session(proxy=CustomProxyConfig(url="http://proxy.example.com:8080"))

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_with_custom_proxy_auth(mock_api_key, mock_session_response):
    """Test browser session creation with custom proxy including authentication."""
    mock_http_success(mock_session_response)

    session = create_browser_session(
        proxy=CustomProxyConfig(url="http://proxy.example.com:8080", username="user", password="pass")
    )

    assert session.cdp_url == "ws://browser:9222/session/123"


def test_create_browser_session_tetra_proxy_with_url_error():
    """Test that ValidationError is raised when Tetra proxy has url field."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        TetraProxyConfig(url="http://proxy.example.com")  # type: ignore


def test_create_browser_session_tetra_proxy_with_username_error():
    """Test that ValidationError is raised when Tetra proxy has username field."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        TetraProxyConfig(username="user")  # type: ignore


def test_create_browser_session_tetra_proxy_with_password_error():
    """Test that ValidationError is raised when Tetra proxy has password field."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        TetraProxyConfig(password="pass")  # type: ignore


def test_create_browser_session_custom_proxy_without_url_error():
    """Test that ValidationError is raised when custom proxy doesn't have url."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        CustomProxyConfig()  # type: ignore


def test_create_browser_session_custom_proxy_with_country_code_error():
    """Test that ValidationError is raised when custom proxy has country_code field."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        CustomProxyConfig(url="http://proxy.example.com", country_code="us")  # type: ignore


@pytest.mark.asyncio
async def test_async_create_browser_session_with_tetra_proxy(mock_async_api_key, mock_session_response):
    """Test async browser session creation with Tetra proxy."""
    mock_async_http_success(mock_session_response)

    session = await async_create_browser_session(proxy=TetraProxyConfig(country_code="uk"))

    assert session.cdp_url == "ws://browser:9222/session/123"


@pytest.mark.asyncio
async def test_async_create_browser_session_with_custom_proxy(mock_async_api_key, mock_session_response):
    """Test async browser session creation with custom proxy."""
    mock_async_http_success(mock_session_response)

    session = await async_create_browser_session(
        proxy=CustomProxyConfig(url="http://proxy.example.com:8080", username="user", password="pass")
    )

    assert session.cdp_url == "ws://browser:9222/session/123"


@pytest.mark.asyncio
async def test_async_create_browser_session_custom_proxy_without_url_error():
    """Test that ValidationError is raised when custom proxy doesn't have url in async."""
    with pytest.raises(Exception):
        CustomProxyConfig()  # type: ignore
