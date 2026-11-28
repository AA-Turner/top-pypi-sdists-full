"""Request profiles for Alexa's cookie and OAuth APIs."""

import logging
from enum import Enum, auto

from aiohttp import ClientResponse, ClientSession, ClientTimeout
from multidict import CIMultiDict
from yarl import URL

from .alexalogin import AlexaLogin
from .const import (
    DEFAULT_ACCEPT_LANGUAGE,
    LOGIN_BROWSER_USER_AGENT,
    LOGIN_WEBVIEW_USER_AGENT,
    PITANGUI_API_USER_AGENT,
)

_LOGGER = logging.getLogger(__name__)
_KNOWN_USER_AGENTS = {
    LOGIN_BROWSER_USER_AGENT,
    LOGIN_WEBVIEW_USER_AGENT,
    PITANGUI_API_USER_AGENT,
}


class RequestProfile(Enum):
    """Keep request identity and authentication scoped to the endpoint."""

    WEB_API = auto()
    AUXILIARY_API = auto()
    DISCOVERY = auto()
    NOTIFICATIONS_PITANGUI = auto()
    ALARMS = auto()
    SYRUP_LISTS = auto()


def build_headers(
    login: AlexaLogin,
    profile: RequestProfile,
    overrides: dict[str, str] | None = None,
) -> CIMultiDict[str]:
    """Build case-insensitive request headers without mutating login state."""
    if profile is RequestProfile.ALARMS:
        return CIMultiDict(
            {
                "authorization": login.access_token,
                "Accept": "application/json",
                "Content-Type": "application/json; charset=UTF-8",
                "User-Agent": PITANGUI_API_USER_AGENT,
            }
        )

    if profile is RequestProfile.SYRUP_LISTS:
        # Preserve the existing list identity: the Android Syrup bytecode
        # establishes token and metadata headers, not a PitanguiBridge UA.
        headers = CIMultiDict(
            {
                "x-amz-access-token": login.access_token,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": LOGIN_WEBVIEW_USER_AGENT,
            }
        )
        for name, value in (overrides or {}).items():
            headers[name] = value
        return headers

    base = CIMultiDict(getattr(login, "_headers", {}) or {})
    if profile is RequestProfile.NOTIFICATIONS_PITANGUI:
        headers = CIMultiDict(
            {
                "User-Agent": PITANGUI_API_USER_AGENT,
                "Accept-Language": DEFAULT_ACCEPT_LANGUAGE,
                "Accept": "application/json",
                "Connection": "keep-alive",
            }
        )
        for name in ("Cookie", "Referer"):
            if base.get(name):
                headers[name] = base[name]
        csrf = (
            base.get("anti-csrftoken-a2z")
            or base.get("csrf")
            or base.get("x-amzn-csrf")
        )
        if csrf:
            name = "anti-csrftoken-a2z" if "anti-csrftoken-a2z" in base else "csrf"
            headers[name] = csrf
        return headers

    if profile is RequestProfile.DISCOVERY:
        base.setdefault("Accept", "application/json")
    if profile in (RequestProfile.WEB_API, RequestProfile.DISCOVERY):
        base["User-Agent"] = PITANGUI_API_USER_AGENT
    for name, value in (overrides or {}).items():
        base[name] = value
    return base


async def send_request(
    session: ClientSession,
    method: str,
    url: URL,
    login: AlexaLogin,
    profile: RequestProfile,
    *,
    data: dict | None = None,
    overrides: dict[str, str] | None = None,
    allow_redirects: bool = True,
    timeout: ClientTimeout | None = None,
) -> ClientResponse:
    """Send one request and log the identity recorded by aiohttp."""
    if profile is RequestProfile.SYRUP_LISTS:
        allow_redirects = False
    options = {}
    if not allow_redirects:
        options["allow_redirects"] = False
    if timeout is not None:
        options["timeout"] = timeout
    response = await getattr(session, method)(
        url,
        json=data,
        headers=build_headers(login, profile, overrides),
        ssl=login._ssl,
        **options,
    )
    if _LOGGER.isEnabledFor(logging.DEBUG) and isinstance(response, ClientResponse):
        for hop in (*response.history, response):
            request = hop.request_info
            user_agent = request.headers.get("User-Agent")
            _LOGGER.debug(
                "Alexa API profile=%s method=%s status=%s User-Agent=%s",
                profile.name,
                request.method,
                hop.status,
                user_agent if user_agent in _KNOWN_USER_AGENTS else "<unset or custom>",
            )
    return response
