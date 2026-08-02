import logging
from typing import Optional

import httpx

from agentql import APIKeyError
from agentql._core._api_constants import BROWSER_SESSIONS_ENDPOINT, SERVICE_URL
from agentql._core._errors import API_KEY_NOT_SET_MESSAGE
from agentql._core._utils import get_api_key_async
from agentql.tools._shared.tetra import (
    BrowserProfile,
    BrowserSession,
    CustomProxyConfig,
    ProxyConfig,
    ShutdownMode,
    TetraProxyConfig,
    UserAgentPreset,
)

log = logging.getLogger("agentql")

_http_client = httpx.AsyncClient()


async def create_browser_session(
    ua_preset: Optional[UserAgentPreset] = None,
    profile: Optional[BrowserProfile] = None,
    inactivity_timeout_seconds: Optional[int] = None,
    proxy: Optional[ProxyConfig] = None,
    shutdown_mode: Optional[ShutdownMode] = None,
) -> BrowserSession:
    """
    Create a new remote browser session via Tetra.

    Parameters:
    -----------
    ua_preset: Optional[UserAgentPreset]
        User Agent preset (windows, macos, linux). Defaults to None.
    profile: Optional[BrowserProfile]
        Browser profile preset (light, stealth, tf-browser). Defaults to None.
    inactivity_timeout_seconds: Optional[int]
        Inactivity timeout in seconds. Defaults to None.
    proxy: Optional[ProxyConfig]
        Proxy configuration. Can be either:
        - TetraProxyConfig: Built-in proxy with optional country_code
        - CustomProxyConfig: Custom proxy with url and optional username/password
        Defaults to None.
    shutdown_mode: Optional[ShutdownMode]
        Controls session teardown on disconnect. Defaults to None (on_disconnect).

    Returns:
    --------
    BrowserSession: A browser session object with cdp_url property for connecting to the browser.

    Raises:
    -------
    ValueError: If ua_preset is specified with STEALTH or TF_BROWSER profile.
    APIKeyError: If the API key is not set or invalid.
    httpx.HTTPStatusError: If the API request fails.
    """
    api_key = await get_api_key_async()

    if not api_key:
        raise APIKeyError(API_KEY_NOT_SET_MESSAGE)

    url = f"{SERVICE_URL}{BROWSER_SESSIONS_ENDPOINT}"
    headers = {"X-API-Key": api_key}

    if profile in (BrowserProfile.STEALTH, BrowserProfile.TF_BROWSER) and ua_preset:
        raise ValueError(
            f"Invalid configuration: ua_preset cannot be specified with {profile.name} profile. "
            f"{profile.name} profile automatically manages user agents for optimal anti-detection."
        )

    # Prepare request body
    body = {}
    if ua_preset:
        body["browser_ua_preset"] = ua_preset.value
    if profile:
        body["browser_profile"] = profile.value
    if inactivity_timeout_seconds is not None:
        body["inactivity_timeout_seconds"] = inactivity_timeout_seconds
    if proxy is not None:
        proxy_dict = proxy.model_dump(exclude_none=True)
        if isinstance(proxy, TetraProxyConfig):
            proxy_dict["type"] = "tetra"
        elif isinstance(proxy, CustomProxyConfig):
            proxy_dict["type"] = "custom"
        body["proxy"] = proxy_dict
    if shutdown_mode is not None:
        body["shutdown_mode"] = shutdown_mode.value

    try:
        response = await _http_client.post(url, headers=headers, json=body)
        response.raise_for_status()
        session_data = response.json()

        browser_session = BrowserSession(session_data=session_data)
        log.info(f"Successfully allocated browser session: {browser_session.cdp_url}")
        return browser_session
    except ValueError as e:
        log.exception(f"Invalid JSON response from server: {e}")
        raise
    except httpx.HTTPStatusError as e:
        log.exception(
            f"Failed to allocate browser session. Status: {e.response.status_code}, Response: {e.response.text}"
        )
        raise
    except Exception as e:
        log.exception(f"Unexpected error during browser allocation: {e}")
        raise
