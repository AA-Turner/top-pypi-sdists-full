"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Login class.

This file could not have been written without referencing MIT code from https://github.com/Apollon77/alexa-remote.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

import asyncio
import base64
import contextlib
import datetime
import hashlib
import http.cookiejar
import logging
import os
import pickle
import re
import secrets
import socket
import ssl
import time
import warnings
from binascii import Error
from collections import defaultdict
from collections.abc import Callable
from copy import copy
from http.cookies import BaseCookie, CookieError, Morsel, SimpleCookie
from io import BytesIO, StringIO
from json import JSONDecodeError, dumps, loads
from typing import Any
from urllib.parse import urlencode, urlparse
from uuid import uuid4

import aiofiles
import aiohttp
import certifi
import pyotp
from aiofiles import os as aioos
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar
from yarl import URL

from .const import (
    APP_NAME,
    COOKIE_SERIALIZATION_FORMAT,
    COOKIE_SERIALIZATION_VERSION,
    LOCALE_KEY,
    LOGIN_APP_VERSION,
    LOGIN_BROWSER_USER_AGENT,
    LOGIN_WEBVIEW_USER_AGENT,
    PARENT_DASHBOARD_DNS_RETRY_SECONDS,
    PARENT_DASHBOARD_SUBDOMAIN_DEFAULT,
    PARENT_DASHBOARD_SUBDOMAIN_EXCEPTIONS,
)
from .errors import AlexapyPyotpInvalidKey
from .helpers import (
    _catch_all_exceptions,
    delete_cookie,
    hide_email,
    hide_serial,
)

_LOGGER = logging.getLogger(__name__)

_OAUTH_REFRESH_FAILURE_RETRY_SECONDS = 15 * 60

# Calling code, domestic trunk prefix, and national number length pattern.
# For Italy, the leading zero is part of the international number.
_PHONE_DIALING_PLANS = {
    "amazon.com": ("1", "", r"[2-9][0-9]{9}"),
    "amazon.ca": ("1", "", r"[2-9][0-9]{9}"),
    "amazon.co.uk": ("44", "0", r"[1-9][0-9]{9}"),
    "amazon.de": ("49", "0", r"[1-9][0-9]{4,13}"),
    "amazon.fr": ("33", "0", r"[1-9][0-9]{8}"),
    "amazon.it": ("39", "", r"[0-9]{6,11}"),
    "amazon.es": ("34", "", r"[1-9][0-9]{8}"),
    "amazon.com.au": ("61", "0", r"[1-9][0-9]{8}"),
    "amazon.in": ("91", "0", r"[1-9][0-9]{9}"),
    "amazon.com.in": ("91", "0", r"[1-9][0-9]{9}"),
    "amazon.co.jp": ("81", "0", r"[1-9][0-9]{8,9}"),
    "amazon.com.mx": ("52", "", r"[1-9][0-9]{9}"),
    "amazon.mx": ("52", "", r"[1-9][0-9]{9}"),
    "amazon.com.br": ("55", "", r"[1-9][0-9]{9,10}"),
}


# Ensure http.cookies.Morsel recognizes the Partitioned cookie attribute.
# Older Python releases do not include the "partitioned" attribute.
# Newer releases (Python 3.14+) already support it, so this patch is only
# applied when necessary.
if "partitioned" not in Morsel._reserved:
    _LOGGER.debug("Adding partitioned support to http.cookies.Morsel")
    Morsel._reserved["partitioned"] = "Partitioned"

Morsel._flags.add("partitioned")


def create_alexa_context() -> ssl.SSLContext:
    """Create an SSL context for Alexa."""
    context = ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where()
    )
    return context


_SSL_CONTEXT = create_alexa_context()


def _morsel_attr(morsel: Morsel, attr: str) -> str | bool:
    """Return a morsel attribute without assuming runtime support for newer attrs."""
    try:
        return morsel[attr]
    except KeyError:
        return ""


def _cookie_url(domain: str, path: str = "/", secure: bool = True) -> URL:
    """Build a response URL suitable for aiohttp.CookieJar.update_cookies."""
    clean_domain = (domain or "amazon.com").lstrip(".")
    clean_path = path or "/"
    if not clean_path.startswith("/"):
        clean_path = f"/{clean_path}"
    scheme = "https" if secure else "http"
    return URL.build(scheme=scheme, host=clean_domain, path=clean_path)


def _safe_bool(value: Any) -> bool:
    """Convert cookie flag values to bool."""
    if isinstance(value, bool):
        return value
    return value not in ("", None, "False", "false", "0", 0)


def _strip_wrapping_quotes(value: str) -> str:
    """Strip one pair of extra cookie quotes without altering embedded quotes."""
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def _serialize_morsel(
    name: str,
    morsel: Morsel,
    *,
    fallback_domain: str = "",
    fallback_path: str = "/",
    host_only_cookies: set[tuple[str, str]] | None = None,
    expirations: dict[tuple[str, str, str], Any] | None = None,
) -> dict[str, Any]:
    """Serialize one Morsel to a stable dict."""
    domain = str(_morsel_attr(morsel, "domain") or fallback_domain or "")
    path = str(_morsel_attr(morsel, "path") or fallback_path or "/")
    host_only_cookies = host_only_cookies or set()
    expirations = expirations or {}
    expiration = expirations.get(
        (domain, path, str(name)),
        expirations.get((domain, path.rstrip("/"), str(name))),
    )
    # aiohttp 3.8 uses aware datetimes where later releases use timestamps.
    if isinstance(expiration, datetime.datetime):
        expiration = expiration.timestamp()
    return {
        "name": str(name),
        "value": str(morsel.value),
        "domain": domain,
        "path": path,
        "expires": _morsel_attr(morsel, "expires") or "",
        "max_age": _morsel_attr(morsel, "max-age") or "",
        "secure": _safe_bool(_morsel_attr(morsel, "secure")),
        "httponly": _safe_bool(_morsel_attr(morsel, "httponly")),
        "samesite": _morsel_attr(morsel, "samesite") or "",
        "partitioned": _safe_bool(_morsel_attr(morsel, "partitioned")),
        "host_only": (domain, str(name)) in host_only_cookies,
        "expiration": expiration,
    }


def _serialize_cookie_jar(cookie_jar: aiohttp.CookieJar) -> dict[str, Any]:
    """Persist cookies using an alexapy-owned serialization format.

    aiohttp.CookieJar.save/load serializes private implementation details,
    which have changed across aiohttp/Python releases (for example the
    addition of the "Partitioned" cookie attribute). Using an explicit
    serialization format provides forward compatibility and allows schema
    versioning.
    """
    serialized: dict[str, Any] = {
        "format": COOKIE_SERIALIZATION_FORMAT,
        "version": COOKIE_SERIALIZATION_VERSION,
        "cookies": [],
    }

    cookies: list[dict[str, Any]] = serialized["cookies"]
    host_only_cookies = getattr(cookie_jar, "_host_only_cookies", set())
    expirations = getattr(cookie_jar, "_expirations", {})
    seen: set[tuple[str, str, str]] = set()

    # Preserve aiohttp's domain/path buckets when available. Current aiohttp uses
    # a mapping like {(domain, path): SimpleCookie(...)}; older/newer versions may
    # vary, so this is deliberately defensive.
    jar_cookies = getattr(cookie_jar, "_cookies", {})
    if isinstance(jar_cookies, dict):
        for key, simple_cookie in jar_cookies.items():
            domain = ""
            path = "/"
            if isinstance(key, tuple):
                domain = str(key[0] or "") if len(key) >= 1 else ""
                path = str(key[1] or "/") if len(key) >= 2 else "/"
            elif isinstance(key, str):
                # Some private aiohttp pickles have been observed with a string
                # bucket key. Treat it as a domain, not as a cookie name.
                domain = key

            if not isinstance(simple_cookie, BaseCookie):
                continue

            for name, morsel in simple_cookie.items():
                entry = _serialize_morsel(
                    str(name),
                    morsel,
                    fallback_domain=domain,
                    fallback_path=path,
                    host_only_cookies=host_only_cookies,
                    expirations=expirations,
                )
                cookie_key = (entry["domain"], entry["path"], entry["name"])
                if cookie_key in seen:
                    continue
                seen.add(cookie_key)
                cookies.append(entry)

    # Fallback for aiohttp versions whose internals differ from the above.
    for morsel in cookie_jar:
        entry = _serialize_morsel(morsel.key, morsel)
        cookie_key = (entry["domain"], entry["path"], entry["name"])
        if cookie_key in seen:
            continue
        seen.add(cookie_key)
        cookies.append(entry)

    return serialized


def _deserialize_cookie(  # noqa: PLR0915
    cookie_jar: aiohttp.CookieJar,
    cookie: dict[str, Any],
    *,
    fallback_domain: str = "",
) -> tuple[str, str] | None:
    """Restore a serialized cookie into an aiohttp CookieJar."""
    name = str(cookie.get("name") or "")
    value = cookie.get("value")
    domain = str(cookie.get("domain") or "")
    path = str(cookie.get("path") or "/")
    expires = str(cookie.get("expires") or "")
    max_age = str(cookie.get("max_age") or "")
    secure = _safe_bool(cookie.get("secure", True))
    httponly = _safe_bool(cookie.get("httponly", False))
    samesite = str(cookie.get("samesite") or "")
    partitioned = _safe_bool(cookie.get("partitioned", False))
    host_only = _safe_bool(cookie.get("host_only", False))

    expiration = cookie.get("expiration")
    if isinstance(expiration, (int, float)):
        if expiration <= time.time():
            return None
        expires = http.cookiejar.time2netscape(expiration)
        max_age = ""

    if not name or value is None:
        return None

    if partitioned:
        secure = True

    cookie_value = _strip_wrapping_quotes(str(value))
    raw_cookie = SimpleCookie()
    try:
        raw_cookie[name] = cookie_value
    except CookieError:
        return None
    morsel = raw_cookie[name]

    clean_domain = domain.lstrip(".") or fallback_domain.lstrip(".")
    clean_path = path
    if not clean_path.startswith("/"):
        clean_path = f"/{clean_path}"

    # For host-only cookies, do not set the Domain attribute. The response URL
    # supplies the host scope. Domain cookies keep their explicit Domain attr.
    if clean_domain and not host_only:
        with contextlib.suppress(KeyError):
            morsel["domain"] = clean_domain
    if clean_path:
        with contextlib.suppress(KeyError):
            morsel["path"] = clean_path
    if expires:
        with contextlib.suppress(KeyError):
            morsel["expires"] = expires
    if max_age:
        with contextlib.suppress(KeyError):
            morsel["max-age"] = max_age
    if secure:
        with contextlib.suppress(KeyError):
            morsel["secure"] = True
    if httponly:
        with contextlib.suppress(KeyError):
            morsel["httponly"] = True
    if samesite:
        with contextlib.suppress(KeyError):
            morsel["samesite"] = samesite
    if partitioned:
        with contextlib.suppress(KeyError):
            morsel["partitioned"] = True

    cookie_jar.update_cookies(raw_cookie, _cookie_url(clean_domain, clean_path, secure))
    return name, cookie_value


def _deserialize_cookie_jar(
    cookie_jar: aiohttp.CookieJar,
    serialized: dict[str, Any],
    *,
    fallback_domain: str = "",
) -> dict[str, str]:
    """Restore a serialized alexapy cookie jar into an aiohttp CookieJar."""
    return_cookies: dict[str, str] = {}
    if serialized.get("format") != COOKIE_SERIALIZATION_FORMAT:
        return return_cookies

    entries = serialized.get("cookies")
    if serialized.get("version") != COOKIE_SERIALIZATION_VERSION or not isinstance(
        entries, list
    ):
        return return_cookies

    cookie_jar.clear()
    for cookie in entries:
        if not isinstance(cookie, dict):
            continue
        restored = _deserialize_cookie(
            cookie_jar,
            cookie,
            fallback_domain=fallback_domain,
        )
        if restored:
            return_cookies[restored[0]] = restored[1]

    return return_cookies


def _legacy_cookie_value(value: Any) -> Any:
    """Extract a value from old aiohttp private-cookie records."""
    if isinstance(value, Morsel):
        return value.value
    if isinstance(value, dict):
        return value.get("value") or value.get("coded_value")
    return value


def _restore_legacy_aiohttp_cookie_mapping(
    cookie_jar: aiohttp.CookieJar,
    cookies: dict[Any, Any],
    *,
    fallback_domain: str = "",
) -> dict[str, str]:
    """Restore old aiohttp.CookieJar.save() mappings.

    This avoids treating bucket keys as cookie names.
    """
    return_cookies: dict[str, str] = {}
    restored_count = 0

    for bucket_key, bucket in cookies.items():
        domain = fallback_domain
        path = "/"
        if isinstance(bucket_key, tuple):
            domain = str(bucket_key[0] or "") if len(bucket_key) >= 1 else ""
            path = str(bucket_key[1] or "/") if len(bucket_key) >= 2 else "/"
        elif isinstance(bucket_key, str):
            # aiohttp private bucket key; do not turn this into a cookie name.
            domain = bucket_key

        if isinstance(bucket, BaseCookie | dict):
            iterator = bucket.items()
        else:
            continue

        for name, stored in iterator:
            cookie_domain = domain
            cookie_path = path
            expires = ""
            max_age = ""
            secure = True
            httponly = False
            samesite = ""
            partitioned = False
            value = _legacy_cookie_value(stored)

            if isinstance(stored, Morsel):
                cookie_domain = str(_morsel_attr(stored, "domain") or domain)
                cookie_path = str(_morsel_attr(stored, "path") or path or "/")
                expires = str(_morsel_attr(stored, "expires") or "")
                max_age = str(_morsel_attr(stored, "max-age") or "")
                secure = _safe_bool(_morsel_attr(stored, "secure"))
                httponly = _safe_bool(_morsel_attr(stored, "httponly"))
                samesite = str(_morsel_attr(stored, "samesite") or "")
                partitioned = _safe_bool(_morsel_attr(stored, "partitioned"))
            elif isinstance(stored, dict):
                cookie_domain = str(stored.get("domain") or domain)
                cookie_path = str(stored.get("path") or path or "/")
                expires = str(stored.get("expires") or "")
                max_age = str(stored.get("max-age") or stored.get("max_age") or "")
                secure = _safe_bool(stored.get("secure", True))
                httponly = _safe_bool(stored.get("httponly", False))
                samesite = str(stored.get("samesite") or "")
                partitioned = _safe_bool(stored.get("partitioned", False))

            restored = _deserialize_cookie(
                cookie_jar,
                {
                    "name": str(name),
                    "value": value,
                    "domain": cookie_domain,
                    "path": cookie_path,
                    "expires": expires,
                    "max_age": max_age,
                    "secure": secure,
                    "httponly": httponly,
                    "samesite": samesite,
                    "partitioned": partitioned,
                },
                fallback_domain=fallback_domain,
            )
            if restored:
                restored_count += 1
                return_cookies[restored[0]] = restored[1]

    if restored_count:
        _LOGGER.debug(
            "Restored %s cookies from legacy aiohttp cookie mapping",
            restored_count,
        )
    return return_cookies


def _is_flat_cookie_dict(cookies: dict[Any, Any]) -> bool:
    """Return True only for a legacy plain name/value cookie dict."""
    return bool(cookies) and all(
        isinstance(key, str)
        and isinstance(value, str)
        and not value.lstrip().startswith("{")
        for key, value in cookies.items()
    )


class _ScopedCookies(dict[str, str]):
    """Compatibility mapping with an independent snapshot of the cookie scopes."""

    def __init__(self, jar: aiohttp.CookieJar) -> None:
        super().__init__((cookie.key, cookie.value) for cookie in jar)
        self.serialized = _serialize_cookie_jar(jar)


class _LegacyCookieUnpickler(pickle.Unpickler):
    """Read the historical cookie formats without allowing arbitrary globals."""

    def find_class(self, module: str, name: str) -> Any:
        allowed = {
            ("builtins", "dict"): dict,
            ("collections", "defaultdict"): defaultdict,
            ("http.cookies", "SimpleCookie"): SimpleCookie,
            ("http.cookies", "Morsel"): Morsel,
            ("http.cookiejar", "Cookie"): http.cookiejar.Cookie,
            ("requests.cookies", "RequestsCookieJar"): RequestsCookieJar,
            (
                "http.cookiejar",
                "DefaultCookiePolicy",
            ): http.cookiejar.DefaultCookiePolicy,
        }
        if (module, name) not in allowed:
            raise pickle.UnpicklingError("Unsupported legacy cookie type")
        return allowed[module, name]


class AlexaLogin:
    """Class to handle login connection to Alexa. This class will not reconnect.

    Args:
    url (string): Localized Amazon domain (e.g., amazon.com)
    email (string): Amazon login account
    password (string): Password for Amazon login account
    outputpath (function): Local path with write access for storing files
    debug (boolean): Enable additional debugging including debug file creation
    otp_secret (string): TOTP Secret key for automatic 2FA filling
    uuid: (string): Unique 32 char hex to serve as app serial number for registration

    """

    def __init__(  # noqa: PLR0913, PLR0915
        self,
        url: str,
        email: str,
        password: str,
        outputpath: Callable[[str], str],
        debug: bool = False,
        otp_secret: str = "",
        oauth: dict[Any, Any] | None = None,
        uuid: str | None = None,
        oauth_login: bool = True,
        *,
        experimental_api_user_agent: bool | None = None,
        experimental_notifications: bool | None = None,
    ) -> None:
        """Set up initial connection and log in.

        The two experimental keyword arguments are deprecated and ignored.
        """
        oauth = oauth or {}

        self.reported_account_domain: str | None = None
        self._hass_domain: str = "alexa_media"
        self._prefix: str = "https://alexa."
        self._url: str = url
        self._email: str = email
        self._password: str = password
        self._session: aiohttp.ClientSession | None = None
        self._ssl = _SSL_CONTEXT
        self._headers: dict[str, str] = {}
        self._data: dict[str, str] | None = None
        self.status: dict[str, str | bool] | None = {}
        self.stats: dict[str, str | int | datetime.datetime] | None = {
            "login_timestamp": datetime.datetime(1, 1, 1),
            "api_calls": 0,
        }
        self._outputpath = outputpath
        self._cookiefile: list[str] = [
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.cookies"),
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.pickle"),
            self._outputpath(f"{self._hass_domain}.{self.email}.pickle"),
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.txt"),
        ]
        self._debugpost: str = outputpath(f"{self._hass_domain}{email}post.html")
        self._debugget: str = outputpath(f"{self._hass_domain}{email}get.html")
        self._lastreq: aiohttp.ClientResponse | None = None
        self._debug: bool = debug
        self._links: dict[str, tuple[str, str]] | None = {}
        self._options: dict[str, str] | None = {}
        self._site: str | None = None
        self._close_requested = False
        self._customer_id: str | None = None
        self._totp: pyotp.TOTP | None = None
        self.set_totp(otp_secret.replace(" ", ""))
        self.access_token: str | None = oauth.get("access_token")
        self.refresh_token: str | None = oauth.get("refresh_token")
        self.mac_dms: str | None = oauth.get("mac_dms")
        self.expires_in: float | None = oauth.get("expires_in")
        self._oauth_lock: asyncio.Lock = asyncio.Lock()
        self._oauth_retry_at = 0.0
        self._oauth_refresh_task: asyncio.Task[None] | None = None
        self._pending_cookies: dict[str, str] | None = None
        self._defer_cookie_save = False
        self._form_lock = asyncio.Lock()
        self._credential_login: AlexaLogin | None = None
        self._credential_previous_status: dict[str, str | bool] | None = None
        self._parent_dashboard_host: str | None = None
        self._parent_dashboard_checked = False
        self._parent_dashboard_retry_at = float("inf")
        self._parent_dashboard_lock = asyncio.Lock()
        self.uuid = (
            uuid if uuid else uuid4().hex.upper()
        )  # needed to be unique but repeateable for device registration
        self.deviceid: str = self.uuid.encode().hex() + "23413249564c5635564d32573831"
        self.code_verifier: str = oauth.get(
            "code_verifier",
            base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode(),
        )
        self.code_challenge: str = oauth.get(
            "code_challenge",
            base64.urlsafe_b64encode(
                hashlib.sha256(self.code_verifier.encode()).digest()
            )
            .rstrip(b"=")
            .decode(),
        )
        self.authorization_code: str | None = oauth.get("authorization_code")
        self.oauth_login: bool = oauth_login
        self.csrf_token: str | None = None
        self.csrf_token_created_at: int | None = None
        self.proxy_url: str = ""
        _LOGGER.debug(
            "Login created for %s - %s",
            hide_email(self.email),
            self.url,
        )
        self._create_session()

    @property
    def email(self) -> str:
        """Return email or mobile account for this Login."""
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        """Set email."""
        self._email = value

    @property
    def password(self) -> str:
        """Return password for this Login."""
        return self._password

    @password.setter
    def password(self, value: str | None) -> None:
        """Set password."""
        self._password = value

    @property
    def customer_id(self) -> str | None:
        """Return customer_id for this Login."""
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: str | None) -> None:
        self._customer_id = value

    @property
    def session(self) -> aiohttp.ClientSession | None:
        """Return session for this Login."""
        return self._session

    @property
    def url(self) -> str:
        """Return url for this Login."""
        return self._url

    @property
    def start_url(self) -> URL:
        """Return start url for this Login."""
        if self.oauth_login:
            site: URL = URL("https://www.amazon.com/ap/signin")
            query = {
                "openid.return_to": "https://www.amazon.com/ap/maplanding",
                "openid.assoc_handle": "amzn_dp_project_dee_ios",
                "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
                "pageId": "amzn_dp_project_dee_ios",
                "accountStatusPolicy": "P1",
                "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
                "openid.mode": "checkid_setup",
                "openid.ns.oa2": "http://www.amazon.com/ap/ext/oauth/2",
                "openid.oa2.client_id": f"device:{self.deviceid}",
                "openid.ns.pape": "http://specs.openid.net/extensions/pape/1.0",
                "openid.oa2.response_type": "code",
                "openid.ns": "http://specs.openid.net/auth/2.0",
                "openid.pape.max_auth_age": "0",
                "openid.oa2.scope": "device_auth_access offline_access",
                "openid.oa2.code_challenge_method": "S256",
                "openid.oa2.code_challenge": self.code_challenge,
                "language": (
                    LOCALE_KEY.get(self.url.replace("amazon", ""))
                    if LOCALE_KEY.get(self.url.replace("amazon", ""))
                    else "en_US"
                ),
            }
            site = site.update_query(query)
            _LOGGER.debug("Attempting oauth login to %s", site)
        else:
            site: URL = URL(self._prefix + self.url)
            self._headers["authority"] = f"www.{self._url}"
        return site

    @property
    def lastreq(self) -> aiohttp.ClientResponse | None:
        """Return last response for last request for this Login."""
        return self._lastreq

    @property
    def close_requested(self) -> bool:
        """Return whether this Login has been asked to close."""
        return self._close_requested

    @property
    def links(self) -> str:
        """Return string list of links from last page for this Login."""
        result = ""
        assert self._links is not None
        for key, value in self._links.items():
            result += f"link{key}:{value[0]}\n"
        return result

    def set_totp(self, otp_secret: str) -> pyotp.TOTP | None:
        """Enable a TOTP generator for the login.

        Args
            otp_secret (Text): Secret. If blank, it will remove the TOTP entry.

        Returns
            Optional[pyotp.TOTP]: The pyotp TOTP object

        """
        if otp_secret:
            _LOGGER.debug(
                "Creating TOTP with authenticator app key %s",
                hide_serial(otp_secret),
            )
            try:
                self._totp = pyotp.TOTP(otp_secret)
                self.get_totp_token()
            except Error as ex:
                self._totp = None
                _LOGGER.warning(
                    "Error creating TOTP; %s likely invalid", hide_serial(otp_secret)
                )
                raise AlexapyPyotpInvalidKey(ex) from ex
            except AttributeError:
                self._totp = None
                _LOGGER.warning(
                    "Error creating TOTP; pyotp version likely outdated",
                )
        else:
            self._totp = None
        return self._totp

    def get_totp_token(self) -> str:
        """Generate Timed based OTP token.

        Returns
            Text: OTP for current time.

        """
        if self._totp:
            token: str = self._totp.now()
            _LOGGER.debug(
                "Generated OTP: %s",
                token[:2] + "**" + token[4:],
            )
            return token
        _LOGGER.debug("Unable to generate OTP; 2FA app key not configured")
        return ""

    async def load_cookie(self, cookies_txt: str = "") -> dict[str, str]:
        """Stage imported or saved cookies for validation before adopting them."""
        self._pending_cookies = None
        if cookies_txt:
            cookies = self._load_cookie_data(self._parse_netscape_cookies(cookies_txt))
            self._pending_cookies = cookies or None
            return cookies

        for cookiefile in self._cookiefile:
            try:
                async with aiofiles.open(cookiefile, "rb") as source:
                    raw = await source.read()
                if cookiefile.endswith(".txt"):
                    cookies = self._parse_netscape_cookies(raw.decode())
                else:
                    try:
                        cookies = loads(raw)
                    except (UnicodeError, JSONDecodeError):
                        if not cookiefile.endswith(".pickle"):
                            raise
                        cookies = _LegacyCookieUnpickler(BytesIO(raw)).load()
                restored = self._load_cookie_data(cookies)
            except (
                OSError,
                EOFError,
                ValueError,
                TypeError,
                AttributeError,
                pickle.UnpicklingError,
            ):
                _LOGGER.debug("Could not read saved Alexa cookies")
                continue
            if restored:
                self._pending_cookies = restored
                return restored
        return {}

    def _take_loaded_cookies(
        self, cookies: dict[str, str] | None
    ) -> dict[str, str] | None:
        staged = self._pending_cookies
        self._pending_cookies = None
        return staged if cookies is None else cookies

    @staticmethod
    def _parse_netscape_cookies(content: str) -> http.cookiejar.MozillaCookieJar:
        jar = http.cookiejar.MozillaCookieJar()
        with warnings.catch_warnings(), contextlib.suppress(http.cookiejar.LoadError):
            # The standard parser can include malformed cookie data in warnings.
            warnings.simplefilter("ignore", UserWarning)
            jar._really_load(StringIO(content), "<cookie import>", True, False)
            return jar
        return http.cookiejar.MozillaCookieJar()

    def _load_cookie_data(self, cookies: Any) -> dict[str, str]:
        """Decode storage formats to a candidate jar with the original scope."""
        jar = aiohttp.CookieJar()
        if isinstance(cookies, http.cookiejar.CookieJar):
            for cookie in cookies:
                _deserialize_cookie(
                    jar,
                    {
                        "name": cookie.name,
                        "value": cookie.value,
                        "domain": cookie.domain,
                        "path": cookie.path,
                        "secure": cookie.secure,
                        "expiration": cookie.expires,
                        "host_only": not cookie.domain_specified,
                        "httponly": cookie.has_nonstandard_attr("HTTPOnly"),
                    },
                    fallback_domain=self.url,
                )
        elif isinstance(cookies, dict):
            if cookies.get("format") == COOKIE_SERIALIZATION_FORMAT:
                _deserialize_cookie_jar(jar, cookies, fallback_domain=self.url)
            elif _is_flat_cookie_dict(cookies):
                self._seed_unscoped_cookies(jar, cookies)
            else:
                _restore_legacy_aiohttp_cookie_mapping(
                    jar, cookies, fallback_domain=self.url
                )
        return _ScopedCookies(jar) if len(jar) else {}

    def _seed_unscoped_cookies(
        self, jar: aiohttp.CookieJar, cookies: dict[str, str]
    ) -> None:
        """Hydrate legacy flat cookies within the configured marketplace only."""
        for name, value in cookies.items():
            _deserialize_cookie(
                jar,
                {"name": name, "value": value, "domain": self.url},
                fallback_domain=self.url,
            )

    def _parent_dashboard_cache_valid(self) -> bool:
        """Return whether the cached discovery result can still be used."""
        return (
            self._parent_dashboard_checked
            and time.monotonic() < self._parent_dashboard_retry_at
        )

    async def resolve_parent_dashboard_host(self) -> str | None:
        """Discover the dashboard lazily and cache the DNS result.

        A resolved host and a definitive "no such host" answer are cached for the
        lifetime of this login instance, so a marketplace without a Kids dashboard
        is looked up only once. A timeout or other resolver error says nothing about
        whether the host exists, so it is cached only for
        ``PARENT_DASHBOARD_DNS_RETRY_SECONDS`` and then looked up again; a brief
        network problem at startup therefore cannot disable the dashboard until
        restart. HTTP failures do not affect this cache.
        """
        if self._parent_dashboard_cache_valid():
            return self._parent_dashboard_host
        async with self._parent_dashboard_lock:
            if not self._parent_dashboard_cache_valid():
                domain = self.url.lower()
                subdomain = PARENT_DASHBOARD_SUBDOMAIN_EXCEPTIONS.get(
                    domain, PARENT_DASHBOARD_SUBDOMAIN_DEFAULT
                )
                host = f"{subdomain}.{domain}"
                self._parent_dashboard_host = None
                try:
                    await asyncio.wait_for(
                        asyncio.get_running_loop().getaddrinfo(
                            host, 443, type=socket.SOCK_STREAM
                        ),
                        timeout=5,
                    )
                except socket.gaierror as ex:
                    # EAI_NONAME/EAI_NODATA: the name does not exist. Anything else
                    # (EAI_AGAIN, EAI_FAIL, ...) is a resolver problem, retried later.
                    definitive = ex.errno in {
                        socket.EAI_NONAME,
                        getattr(socket, "EAI_NODATA", socket.EAI_NONAME),
                    }
                    self._parent_dashboard_retry_at = (
                        float("inf")
                        if definitive
                        else time.monotonic() + PARENT_DASHBOARD_DNS_RETRY_SECONDS
                    )
                    _LOGGER.debug(
                        "Parent dashboard DNS unavailable for %s: %s", host, ex
                    )
                except (OSError, TimeoutError) as ex:
                    self._parent_dashboard_retry_at = (
                        time.monotonic() + PARENT_DASHBOARD_DNS_RETRY_SECONDS
                    )
                    _LOGGER.debug(
                        "Parent dashboard DNS unavailable for %s: %s", host, ex
                    )
                else:
                    self._parent_dashboard_host = host
                    self._parent_dashboard_retry_at = float("inf")
                self._parent_dashboard_checked = True
        return self._parent_dashboard_host

    async def close(self) -> None:
        """Close connection for login."""
        self._close_requested = True
        if task := self._oauth_refresh_task:
            self._oauth_refresh_task = None
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        if self._credential_login:
            await self._credential_login.close()
            self._credential_login = None
            self._credential_previous_status = None
        if self._session and not self._session.closed:
            await self._session.close()

    async def reset(self, *, clear_cookies: bool = False) -> None:
        """Reset runtime login state, optionally removing all saved cookie formats."""
        _LOGGER.debug("Resetting Login for %s - %s", hide_email(self.email), self.url)
        await self.close()
        self._session = None
        self._data = None
        self._lastreq = None
        self.status = {}
        self._links = {}
        self._options = {}
        self._site = None
        self.csrf_token = None
        self.csrf_token_created_at = None
        self._pending_cookies = None
        self._credential_previous_status = None
        self._oauth_retry_at = 0.0
        self._create_session()
        self._close_requested = False

        if clear_cookies:
            await self.delete_cookiefile()

    @classmethod
    def get_inputs(cls, soup: BeautifulSoup, searchfield=None) -> dict[str, str]:
        """Parse soup for form with searchfield."""
        searchfield = searchfield or {"name": "signIn"}
        data = {}
        form = soup.find("form", searchfield)
        if not form:
            form = soup.find("form")
        for field in form.find_all("input"):
            try:
                data[field["name"]] = ""
                if field["type"] and field["type"] == "hidden":
                    data[field["name"]] = field["value"]
            except BaseException:
                pass
        return data

    async def test_loggedin(
        self,
        cookies: dict[str, str] | None = None,
        *,
        rebuild_session: bool = True,
    ) -> bool:
        """Verify identity and API cookies before adopting a login session."""
        async with self._oauth_lock:
            cookies = self._take_loaded_cookies(cookies)
            if (
                cookies is None
                and rebuild_session
                and (
                    self.authorization_code
                    or (self.access_token and not self.refresh_token)
                )
                and await self._try_login(register=True)
            ):
                return True
            if await self._try_login(cookies=cookies):
                return True
            return bool(
                rebuild_session
                and self.refresh_token
                and await self._try_login(refresh=True)
            )

    async def _try_login(  # noqa: PLR0911
        self,
        *,
        cookies: dict[str, str] | None = None,
        refresh: bool = False,
        register: bool = False,
    ) -> bool:
        """Attempt authentication in a private jar under the caller's login lock."""
        original = self._session
        candidate = copy(self)
        candidate._headers = {
            name: value
            for name, value in self._headers.items()
            if name.lower() not in {"authorization", "cookie", "csrf", "referer"}
        }
        jar = aiohttp.CookieJar()
        if isinstance(cookies, _ScopedCookies):
            _deserialize_cookie_jar(jar, cookies.serialized, fallback_domain=self.url)
        elif not refresh and cookies is None and original and not original.closed:
            _deserialize_cookie_jar(
                jar,
                _serialize_cookie_jar(original.cookie_jar),
                fallback_domain=self.url,
            )
        if cookies and not isinstance(cookies, _ScopedCookies):
            self._seed_unscoped_cookies(jar, cookies)

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(
            headers=candidate._headers,
            cookie_jar=jar,
            timeout=timeout,
        ) as session:
            candidate._session = session
            try:
                if refresh and not (
                    await candidate.refresh_access_token()
                    and await candidate.exchange_token_for_cookies()
                ):
                    return False
                if register and await candidate.get_tokens():
                    await candidate.register_capabilities()
                    await candidate.exchange_token_for_cookies()

                customer = await candidate._validate_cookie_identity()
                if customer is None:
                    return False
                if not candidate._api_csrf():
                    if not await candidate.get_csrf():
                        return False
                    # Discovery can also receive Set-Cookie. Verify the resulting jar.
                    customer = await candidate._validate_cookie_identity()
                    if customer is None:
                        return False
                csrf = candidate._api_csrf()
                if not csrf or not candidate._has_api_cookies():
                    return False
            except (
                aiohttp.ClientError,
                TimeoutError,
                ValueError,
                KeyError,
                TypeError,
                AttributeError,
                CookieError,
            ):
                _LOGGER.debug("Alexa authentication attempt failed")
                return False

            if self._close_requested or self._session is not original:
                return False
            if not original or original.closed:
                self._create_session(force=True)
            assert self._session
            _deserialize_cookie_jar(
                self._session.cookie_jar,
                _serialize_cookie_jar(jar),
                fallback_domain=self.url,
            )
            self._adopt_oauth(candidate)
            if not (register or refresh):
                self._oauth_retry_at = time.monotonic() + 60
            self.customer_id = customer["id"]
            domain = self._reported_marketplace(customer)
            if domain:
                self.reported_account_domain = domain
            if domain and domain != self.url:
                _LOGGER.warning(
                    "Configured Alexa domain %s differs from the account domain %s",
                    self.url,
                    domain,
                )
            self._headers["csrf"] = csrf
            self._headers["Referer"] = f"{self._prefix}{self.url}/spa/index.html"
            if self.stats is not None and not (
                refresh and self.status and self.status.get("login_successful")
            ):
                self.stats["login_timestamp"] = datetime.datetime.now()
                self.stats["api_calls"] = 0
            await self.finalize_login()
            return True

    def _adopt_oauth(self, candidate: "AlexaLogin") -> None:
        self.access_token = candidate.access_token
        self.refresh_token = candidate.refresh_token
        self.mac_dms = candidate.mac_dms
        self.expires_in = candidate.expires_in
        self.authorization_code = candidate.authorization_code

    async def _refresh_session_if_expired(self) -> None:
        """Schedule one proactive refresh without delaying cookie-based requests."""
        if (
            self._close_requested
            or self._oauth_lock.locked()
            or self._form_lock.locked()
            or self._credential_login is not None
            or (self._oauth_refresh_task and not self._oauth_refresh_task.done())
            or not self.refresh_token
            or not self.expires_in
            or self.expires_in > time.time()
            or time.monotonic() < self._oauth_retry_at
        ):
            return
        self._oauth_refresh_task = asyncio.create_task(self._run_oauth_refresh())

    async def _run_oauth_refresh(self) -> None:
        async with self._oauth_lock:
            if (
                self._close_requested
                or self._form_lock.locked()
                or not self.expires_in
                or self.expires_in > time.time()
                or time.monotonic() < self._oauth_retry_at
            ):
                return
            try:
                if await self._try_login(refresh=True):
                    return
            except Exception:
                _LOGGER.debug("Proactive Alexa OAuth refresh failed")
            self._oauth_retry_at = (
                time.monotonic() + _OAUTH_REFRESH_FAILURE_RETRY_SECONDS
            )

    async def _validate_cookie_identity(self) -> dict[str, Any] | None:  # noqa: PLR0911
        """Probe the regional Alexa endpoint and use bootstrap for compatibility."""
        assert self._session
        regional = f"{self._prefix}{self.url}"
        hosts = [regional]
        if self.url.lower() != "amazon.com":
            hosts.append(f"{self._prefix}amazon.com")
        regional_customer_id = None
        for host in hosts:
            if host != regional and not regional_customer_id:
                # US identity alone cannot identify a separately scoped regional jar.
                return None
            for endpoint in (
                f"/api/users/me?platform=ios&version={LOGIN_APP_VERSION}",
                "/api/bootstrap",
            ):
                path = URL(host + endpoint)
                if not self._session.cookie_jar.filter_cookies(path):
                    continue
                try:
                    async with self._session.get(
                        path, ssl=self._ssl, allow_redirects=False
                    ) as response:
                        if response.status != 200 or response.history:
                            if response.status in (301, 302, 303, 307, 308, 401, 404):
                                continue
                            return None
                        payload = await response.json()
                except (aiohttp.ContentTypeError, ValueError):
                    continue
                except (aiohttp.ClientError, TimeoutError):
                    return None
                if not isinstance(payload, dict):
                    continue
                if endpoint == "/api/bootstrap":
                    auth = payload.get("authentication")
                    if (
                        not isinstance(auth, dict)
                        or auth.get("authenticated") is not True
                    ):
                        break
                    payload = {
                        **auth,
                        "id": auth.get("customerId"),
                        "email": auth.get("customerEmail"),
                    }
                customer_id = payload.get("id")
                if not isinstance(customer_id, str) or not customer_id.strip():
                    continue
                if regional_customer_id and customer_id != regional_customer_id:
                    return None
                if self._matches_customer(payload):
                    return payload
                if self.customer_id and customer_id != self.customer_id:
                    return None
                if self._has_identity_claim(payload):
                    return None
                if host == regional:
                    regional_customer_id = customer_id
        return None

    @staticmethod
    def _reported_marketplace(customer: dict[str, Any]) -> str | None:
        name = customer.get("marketPlaceDomainName")
        if not isinstance(name, str):
            return None
        if "://" not in name:
            name = f"https://{name}"
        with contextlib.suppress(ValueError):
            host = URL(name).host
            if host:
                return host.removeprefix("www.")
        return None

    def _matches_customer(self, customer: dict[str, Any]) -> bool:
        customer_id = customer.get("id")
        if not isinstance(customer_id, str) or not customer_id.strip():
            return False
        if self.customer_id and customer_id != self.customer_id:
            return False
        email = customer.get("email")
        if "@" in self.email:
            return isinstance(email, str) and email.casefold() == self.email.casefold()
        expected = self._normalize_phone(self.email)
        returned = self._customer_phones(customer)
        return expected is not None and (
            expected in returned or (not returned and customer_id == self.customer_id)
        )

    def _has_identity_claim(self, customer: dict[str, Any]) -> bool:
        if "@" in self.email:
            return bool(customer.get("email"))
        return bool(self._customer_phones(customer))

    def _customer_phones(self, customer: dict[str, Any]) -> set[str]:
        return {
            normalized
            for field in ("phoneNumber", "mobilePhoneNumber", "email")
            if isinstance(phone := customer.get(field), str)
            and (normalized := self._normalize_phone(phone)) is not None
        }

    def _normalize_phone(self, number: str) -> str | None:
        digits = re.sub(r"[().\s-]", "", number)
        if not re.fullmatch(r"\+?[0-9]{6,15}", digits):
            return None
        if digits.startswith(("+", "00")):
            international = digits[1:] if digits.startswith("+") else digits[2:]
            return (
                international
                if re.fullmatch(r"[1-9][0-9]{5,14}", international)
                else None
            )

        plan = _PHONE_DIALING_PLANS.get(self.url.lower())
        if plan:
            code, trunk, pattern = plan
            national = digits.removeprefix(trunk)
            if re.fullmatch(pattern, national):
                return code + national
        return digits

    def _api_csrf(self) -> str | None:
        cookie = self._get_cookies_from_session(f"alexa.{self.url}").get("csrf")
        return cookie.value if cookie and cookie.value else None

    def _has_api_cookies(self) -> bool:
        assert self._session
        api = URL(f"{self._prefix}{self.url}/api/behaviors/preview")
        return any(
            name != "csrf" for name in self._session.cookie_jar.filter_cookies(api)
        )

    async def get_csrf_token(self) -> str | None:
        """Get an anti-CSRF token from an Amazon webpage."""
        _LOGGER.debug("Getting CSRF token for %s", self._url)
        resp = await self._session.get(
            f"https://www.{self._url}/alexa-privacy/apd/rvh",
            headers=self._headers,
            ssl=self._ssl,
        )
        t = await resp.text()
        bso = BeautifulSoup(t, "html.parser")
        meta_tag = bso.find("meta", attrs={"name": "csrf-token"})
        if meta_tag and "content" in meta_tag.attrs:
            token = meta_tag["content"]
            _LOGGER.debug("CSRF token found for %s", self._url)
            self.csrf_token = token
            self.csrf_token_created_at = int(datetime.datetime.now().timestamp())
            return token
        _LOGGER.debug("No CSRF token found for %s", self._url)
        return None

    def _create_session(self, force=False) -> None:
        if not self._session or self._session.closed or force:
            self._headers = {
                "User-Agent": (
                    LOGIN_WEBVIEW_USER_AGENT
                    if self.oauth_login
                    else LOGIN_BROWSER_USER_AGENT
                ),
                "Accept": "*/*",
                "Accept-Language": "*",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
            }
            #  initiate session
            self._session = aiohttp.ClientSession(headers=self._headers)

    def _get_cookies_from_session(self, site: str = "") -> "BaseCookie[str]":
        """Return cookies from aiohttp session."""
        assert self._session
        if not site:
            site = f"alexa.{self.url}"
        cookies = {}
        cookie_jar = self._session.cookie_jar
        cookies = cookie_jar.filter_cookies(URL(f"https://{site}"))
        return cookies

    @_catch_all_exceptions
    async def login(
        self,
        cookies: dict[str, str] | None = None,
        data: dict[str, str | None] | None = None,
    ) -> None:
        """Login to Amazon."""
        async with self._form_lock:
            await self._login_with_fallback(cookies, data or {})

    async def _login_with_fallback(
        self, cookies: dict[str, str] | None, data: dict[str, str | None]
    ) -> None:
        # An ongoing form challenge owns a separate session and its form fields.
        if self._credential_login is None and not self._site:
            async with self._oauth_lock:
                cookies = self._take_loaded_cookies(cookies)
                saved = cookies is not None or (
                    self._session
                    and not self._session.closed
                    and len(self._session.cookie_jar)
                )
                if saved and await self._try_login(cookies=cookies):
                    return
                if self.refresh_token and await self._try_login(refresh=True):
                    return
                if saved or self.refresh_token:
                    self._credential_login = self._new_credential_login()
                    if self.status and self.status.get("login_successful"):
                        self._credential_previous_status = self.status

        candidate = self._credential_login
        if candidate is None:
            await self._login_with_credentials(data)
            return

        candidate.password = self.password
        candidate._totp = self._totp
        try:
            await candidate._login_with_credentials(data)
        except (Exception, asyncio.CancelledError):
            await self._discard_credential_login(candidate)
            raise
        if self._close_requested:
            return
        self.status = candidate.status
        self._links = candidate._links
        if candidate.status and candidate.status.get("login_successful"):
            if not self._session or self._session.closed:
                self._create_session(force=True)
            assert self._session and candidate._session
            _deserialize_cookie_jar(
                self._session.cookie_jar,
                _serialize_cookie_jar(candidate._session.cookie_jar),
                fallback_domain=self.url,
            )
            self._adopt_oauth(candidate)
            self.customer_id = candidate.customer_id
            self.reported_account_domain = candidate.reported_account_domain
            self._headers = candidate._headers
            self.stats = candidate.stats
            self._credential_previous_status = None
            await self._discard_credential_login(candidate)
            await self.save_cookiefile()
        elif candidate.status and candidate.status.get("login_failed"):
            # Keep the failure visible: the cookie and refresh-token attempts
            # already failed, so restoring the old login_successful status
            # would hide a dead session from the caller.
            self._credential_previous_status = None
            await self._discard_credential_login(candidate)

    async def _discard_credential_login(self, candidate: "AlexaLogin") -> None:
        if self._credential_previous_status is not None:
            self.status = self._credential_previous_status
        self._credential_previous_status = None
        self._credential_login = None
        await candidate.close()

    def _new_credential_login(self) -> "AlexaLogin":
        candidate = copy(self)
        candidate._session = None
        candidate._oauth_lock = asyncio.Lock()
        candidate._oauth_refresh_task = None
        candidate._pending_cookies = None
        candidate._defer_cookie_save = True
        candidate.status = {}
        candidate._links = {}
        candidate._options = {}
        candidate.stats = dict(self.stats) if self.stats is not None else None
        candidate._data = None
        candidate._lastreq = None
        candidate.access_token = None
        candidate.refresh_token = None
        candidate.authorization_code = None
        candidate.mac_dms = None
        candidate.expires_in = None
        candidate._create_session()
        return candidate

    @_catch_all_exceptions
    async def _login_with_credentials(  # noqa: PLR0915
        self, data: dict[str, str | None]
    ) -> None:
        _LOGGER.debug("Using credentials to log in")
        if not self._site:
            site: URL = self.start_url
        else:
            site = self._site
        if not self._session or self._session.closed:
            self._create_session()
        #  This will process links which is used for debug only to force going
        #  to other links.  Warning, chrome will cache any link parameters
        #  breaking the configuration flow until refresh on browser.
        digit = None
        for datum, value in data.items():
            if (
                value
                and str(value).startswith("link")
                and len(value) > 4
                and value[4:].isdigit()
            ):
                digit = str(value[4:])
                _LOGGER.debug("Found link selection %s in %s ", digit, datum)
                assert self._links is not None
                if self._links.get(digit):
                    _, site = self._links[digit]
                    data[datum] = None
                    _LOGGER.debug("Following selected sign-in link")
                    _LOGGER.debug("%s reset to %s ", datum, data[datum])
        if not digit and self._lastreq is not None:
            assert self._lastreq is not None
            site = str(self._lastreq.url)
            _LOGGER.debug("Reusing the previous sign-in response")
            resp = self._lastreq
        else:
            resp = await self._session.get(
                site, headers=self._headers, ssl=self._ssl, params=self._data
            )
            self._lastreq = resp
            site = await self._process_resp(resp)
        html: str = await resp.text()
        if self._debug:
            async with aiofiles.open(self._debugget, mode="wb") as localfile:
                await localfile.write(await resp.read())
        # This commented block can be used to read a file directly to process.
        # async with aiofiles.open(
        #     "/config/anti-automation-js.html", "rb"
        #     "/config/Amazon-Password-Assistance.html", "rb"
        #     "/config/password_reset_required.html", "rb"
        # ) as myfile:
        #     html = await myfile.read()
        site = await self._process_page(html, site)
        if site is None:
            return
        if not self.status.get("ap_error"):
            missing_params = self._populate_data(site, data)
            if self._debug:
                if missing_params:
                    _LOGGER.debug(
                        "WARNING: Detected missing params: %s",
                        [k for (k, v) in self._data.items() if v == ""],
                    )
                _LOGGER.debug("Submitting Amazon sign-in form")

            # submit post request with username/password and other needed info
            post_resp = None
            if self.status.get("force_get"):
                if not self.status.get("approval") and not self.status.get(
                    "action_required"
                ):
                    post_resp = await self._session.get(
                        site,
                        params=self._data,
                        headers=self._headers,
                        ssl=self._ssl,
                    )
            else:
                # POSTs to Amazon sometimes return redirects
                # (e.g. /verify -> /mybusiness/verify). aiohttp may convert
                # POST->GET for 301/302/303 when auto-following redirects, which
                # can drop the form body and break the flow. Disable auto-redirects
                # and follow once manually while preserving method/body semantics.
                post_resp = await self._session.post(
                    site,
                    data=self._data,
                    headers=self._headers,
                    ssl=self._ssl,
                    allow_redirects=False,
                )

                if post_resp is not None and post_resp.status in (
                    301,
                    302,
                    303,
                    307,
                    308,
                ):
                    location = post_resp.headers.get("Location")
                    if location:
                        # Resolve relative redirects safely against the response URL.
                        target = URL(str(post_resp.url)).join(URL(location))

                        _LOGGER.debug(
                            "POST redirect %s -> %s (status=%s); replaying request",
                            site,
                            str(target),
                            post_resp.status,
                        )

                        # Preserve referer for the follow-up request.
                        headers = dict(self._headers)
                        headers["Referer"] = str(post_resp.url)

                        # Release the prior response before replaying
                        # to avoid connector leaks.
                        with contextlib.suppress(Exception):
                            await post_resp.release()
                        if post_resp.status == 303:
                            # "See Other" becomes a GET.
                            post_resp = await self._session.get(
                                str(target),
                                params=self._data,
                                headers=headers,
                                ssl=self._ssl,
                            )
                        elif post_resp.status in (307, 308):
                            # 307/308 must preserve method and body.
                            post_resp = await self._session.post(
                                str(target),
                                data=self._data,
                                headers=headers,
                                ssl=self._ssl,
                            )
                        else:
                            # For 301/302, preserve POST+body
                            # (Amazon does this for some endpoints).
                            post_resp = await self._session.post(
                                str(target),
                                data=self._data,
                                headers=headers,
                                ssl=self._ssl,
                                allow_redirects=False,
                            )

            # headers need to be submitted to have the referer
            if post_resp:
                if self._debug:
                    async with aiofiles.open(self._debugpost, mode="wb") as localfile:
                        await localfile.write(await post_resp.read())
                self._lastreq = post_resp
                site = await self._process_resp(post_resp)
                self._site = await self._process_page(await post_resp.text(), site)

    async def save_cookiefile(self) -> None:
        """Atomically persist a verified session before removing legacy files."""
        if (
            not self._session
            or not self.status
            or not self.status.get("login_successful")
            or not self._api_csrf()
            or not self._has_api_cookies()
        ):
            return
        jar = self._session.cookie_jar
        destination = self._cookiefile[0]
        temporary = f"{destination}.{uuid4().hex}.tmp"
        try:
            serialized = dumps(_serialize_cookie_jar(jar))
            descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as localfile:
                localfile.write(serialized)
                localfile.flush()
                await asyncio.to_thread(os.fsync, localfile.fileno())
            # No cancellation point between the atomic replacement and its result.
            os.replace(temporary, destination)
        except (OSError, TypeError, ValueError):
            _LOGGER.debug("Could not save Alexa cookies")
            return
        finally:
            with contextlib.suppress(OSError):
                os.unlink(temporary)
        for legacy in self._cookiefile[1:]:
            if await aioos.path.exists(legacy):
                await delete_cookie(legacy)

    async def delete_cookiefile(self) -> None:
        """Explicitly remove all saved cookie formats for the account."""
        for cookiefile in self._cookiefile:
            if await aioos.path.exists(cookiefile):
                await delete_cookie(cookiefile)

    async def get_tokens(self) -> bool:
        """Get access and refresh tokens after registering device using cookies.

        Returns:
            bool: True if successful.
        """
        frc = base64.b64encode(secrets.token_bytes(313)).decode("ascii").rstrip("=")
        map_md_raw = {
            "device_user_dictionary": [],
            "device_registration_data": {"software_version": "1"},
            "app_identifier": {
                "app_version": LOGIN_APP_VERSION,
                "bundle_id": "com.amazon.echo",
            },
        }
        map_md = base64.b64encode(dumps(map_md_raw).encode()).decode().rstrip("=")

        if self.url.lower() != "amazon.com":
            urls = [self.url, "amazon.com"]
        else:
            urls = [self.url]
        registered = False
        for url in urls:
            cookies = self._get_cookies_from_session(url)
            cookies["frc"] = frc
            cookies["map-md"] = map_md
            headers = {
                "Content-Type": "application/json",
            }
            cookies_list = []
            data = {
                "requested_extensions": ["device_info", "customer_info"],
                "cookies": {"website_cookies": cookies_list, "domain": f".{url}"},
                "registration_data": {
                    "domain": "Device",
                    "app_version": LOGIN_APP_VERSION,
                    "device_type": "A2IVLV5VM2W81",
                    "device_name": f"%FIRST_NAME%\u0027s%DUPE_STRATEGY_1ST%{APP_NAME}",
                    "os_version": "16.6",
                    "device_serial": self.uuid,
                    "device_model": "iPhone",
                    "app_name": APP_NAME,
                    "software_version": "1",
                },
                "auth_data": {},
                "user_context_map": {"frc": frc},
                "requested_token_type": ["bearer", "mac_dms", "website_cookies"],
            }
            if self.access_token:
                data["auth_data"] = {"access_token": self.access_token}
            elif self.code_verifier and self.authorization_code:
                data["auth_data"] = {
                    "client_id": self.deviceid,
                    "authorization_code": self.authorization_code,
                    "code_verifier": self.code_verifier,
                    "code_algorithm": "SHA-256",
                    "client_domain": "DeviceLegacy",
                }
            _LOGGER.debug("Attempting to register with %s", url)
            try:
                response = await self._session.post(
                    "https://api." + url + "/auth/register",
                    json=data,
                    headers=headers,
                    allow_redirects=False,
                )
            except aiohttp.ClientConnectorError:
                _LOGGER.debug("Fallback attempt to register with api.amazon.com")
                response = await self._session.post(
                    "https://api.amazon.com/auth/register",
                    json=data,
                    headers=headers,
                    allow_redirects=False,
                )
            if response.status == 200:
                registered = True
                break
        if not registered:
            _LOGGER.debug("Unable to register with %s", urls)
            return False
        response = (await response.json()).get("response")
        if response.get("success"):
            _LOGGER.debug(
                "Successfully registered %s device with Amazon",
                response["success"]["extensions"]["device_info"]["device_name"],
            )
            self.refresh_token = response["success"]["tokens"]["bearer"][
                "refresh_token"
            ]
            self.mac_dms = response["success"]["tokens"]["mac_dms"]
            old = self.access_token
            self.access_token = response["success"]["tokens"]["bearer"]["access_token"]
            self.expires_in = datetime.datetime.now().timestamp() + int(
                response["success"]["tokens"]["bearer"]["expires_in"]
            )
            if old != self.access_token:
                _LOGGER.debug(
                    "New access token(%s) received which expires at %s in %s",
                    len(self.access_token),
                    datetime.datetime.fromtimestamp(self.expires_in),
                    datetime.datetime.fromtimestamp(self.expires_in)
                    - datetime.datetime.now(),
                )
            return True
        return False

    async def register_capabilities(self) -> bool:
        """Register capabilities of virtual device.

        Required for HTTP2/Push.
        https://developer.amazon.com/en-US/docs/alexa/alexa-voice-service/capabilities-api.html

        Returns
            bool: Return True if successful.

        """
        data = {
            "legacyFlags": {
                "SUPPORTS_COMMS": True,
                "SUPPORTS_ARBITRATION": True,
                "SCREEN_WIDTH": 1170,
                "SUPPORTS_SCRUBBING": True,
                "SPEECH_SYNTH_SUPPORTS_TTS_URLS": False,
                "SUPPORTS_HOME_AUTOMATION": True,
                "SUPPORTS_DROPIN_OUTBOUND": True,
                "FRIENDLY_NAME_TEMPLATE": "VOX",
                "SUPPORTS_SIP_OUTBOUND_CALLING": True,
                "VOICE_PROFILE_SWITCHING_DISABLED": True,
                "SUPPORTS_LYRICS_IN_CARD": False,
                "SUPPORTS_DATAMART_NAMESPACE": "Vox",
                "SUPPORTS_VIDEO_CALLING": True,
                "SUPPORTS_PFM_CHANGED": True,
                "SUPPORTS_TARGET_PLATFORM": "TABLET",
                "SUPPORTS_SECURE_LOCKSCREEN": False,
                "AUDIO_PLAYER_SUPPORTS_TTS_URLS": False,
                "SUPPORTS_KEYS_IN_HEADER": False,
                "SUPPORTS_MIXING_BEHAVIOR_FOR_AUDIO_PLAYER": False,
                "AXON_SUPPORT": True,
                "SUPPORTS_TTS_SPEECHMARKS": True,
            },
            "envelopeVersion": "20160207",
            "capabilities": [
                {
                    "version": "0.1",
                    "interface": "CardRenderer",
                    "type": "AlexaInterface",
                },
                {"interface": "Navigation", "type": "AlexaInterface", "version": "1.1"},
                {
                    "type": "AlexaInterface",
                    "version": "2.0",
                    "interface": "Alexa.Comms.PhoneCallController",
                },
                {
                    "type": "AlexaInterface",
                    "version": "1.1",
                    "interface": "ExternalMediaPlayer",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alerts",
                    "configurations": {
                        "maximumAlerts": {"timers": 2, "overall": 99, "alarms": 2}
                    },
                    "version": "1.3",
                },
                {
                    "version": "1.0",
                    "interface": "Alexa.Display.Window",
                    "type": "AlexaInterface",
                    "configurations": {
                        "templates": [
                            {
                                "type": "STANDARD",
                                "id": "app_window_template",
                                "configuration": {
                                    "sizes": [
                                        {
                                            "id": "fullscreen",
                                            "type": "DISCRETE",
                                            "value": {
                                                "value": {
                                                    "height": 1440,
                                                    "width": 3200,
                                                },
                                                "unit": "PIXEL",
                                            },
                                        }
                                    ],
                                    "interactionModes": ["mobile_mode", "auto_mode"],
                                },
                            }
                        ]
                    },
                },
                {
                    "type": "AlexaInterface",
                    "interface": "AccessoryKit",
                    "version": "0.1",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.AudioSignal.ActiveNoiseControl",
                    "version": "1.0",
                    "configurations": {
                        "ambientSoundProcessingModes": [
                            {"name": "ACTIVE_NOISE_CONTROL"},
                            {"name": "PASSTHROUGH"},
                        ]
                    },
                },
                {
                    "interface": "PlaybackController",
                    "type": "AlexaInterface",
                    "version": "1.0",
                },
                {"version": "1.0", "interface": "Speaker", "type": "AlexaInterface"},
                {
                    "version": "1.0",
                    "interface": "SpeechSynthesizer",
                    "type": "AlexaInterface",
                },
                {
                    "version": "1.0",
                    "interface": "AudioActivityTracker",
                    "type": "AlexaInterface",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.Camera.LiveViewController",
                    "version": "1.0",
                },
                {
                    "type": "AlexaInterface",
                    "version": "1.0",
                    "interface": "Alexa.Input.Text",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.PlaybackStateReporter",
                    "version": "1.0",
                },
                {
                    "version": "1.1",
                    "interface": "Geolocation",
                    "type": "AlexaInterface",
                },
                {
                    "interface": "Alexa.Health.Fitness",
                    "version": "1.0",
                    "type": "AlexaInterface",
                },
                {"interface": "Settings", "type": "AlexaInterface", "version": "1.0"},
                {
                    "configurations": {
                        "interactionModes": [
                            {
                                "dialog": "SUPPORTED",
                                "interactionDistance": {"value": 18, "unit": "INCHES"},
                                "video": "SUPPORTED",
                                "keyboard": "SUPPORTED",
                                "id": "mobile_mode",
                                "uiMode": "MOBILE",
                                "touch": "SUPPORTED",
                            },
                            {
                                "video": "UNSUPPORTED",
                                "dialog": "SUPPORTED",
                                "interactionDistance": {"value": 36, "unit": "INCHES"},
                                "uiMode": "AUTO",
                                "touch": "SUPPORTED",
                                "id": "auto_mode",
                                "keyboard": "UNSUPPORTED",
                            },
                        ]
                    },
                    "type": "AlexaInterface",
                    "interface": "Alexa.InteractionMode",
                    "version": "1.0",
                },
                {
                    "type": "AlexaInterface",
                    "configurations": {
                        "catalogs": [
                            {
                                "type": "IOS_APP_STORE",
                                "identifierTypes": [
                                    "URI_HTTP_SCHEME",
                                    "URI_CUSTOM_SCHEME",
                                ],
                            }
                        ]
                    },
                    "version": "0.2",
                    "interface": "Alexa.Launcher",
                },
                {"interface": "System", "version": "1.0", "type": "AlexaInterface"},
                {
                    "interface": "Alexa.IOComponents",
                    "type": "AlexaInterface",
                    "version": "1.4",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.FavoritesController",
                    "version": "1.0",
                },
                {
                    "version": "1.0",
                    "type": "AlexaInterface",
                    "interface": "Alexa.Mobile.Push",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "InteractionModel",
                    "version": "1.1",
                },
                {
                    "interface": "Alexa.PlaylistController",
                    "type": "AlexaInterface",
                    "version": "1.0",
                },
                {
                    "interface": "SpeechRecognizer",
                    "type": "AlexaInterface",
                    "version": "2.1",
                },
                {
                    "interface": "AudioPlayer",
                    "type": "AlexaInterface",
                    "version": "1.3",
                },
                {
                    "type": "AlexaInterface",
                    "version": "3.1",
                    "interface": "Alexa.RTCSessionController",
                },
                {
                    "interface": "VisualActivityTracker",
                    "version": "1.1",
                    "type": "AlexaInterface",
                },
                {
                    "interface": "Alexa.PlaybackController",
                    "version": "1.0",
                    "type": "AlexaInterface",
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.SeekController",
                    "version": "1.0",
                },
                {
                    "interface": "Alexa.Comms.MessagingController",
                    "type": "AlexaInterface",
                    "version": "1.0",
                },
            ],
        }
        headers = {
            "User-Agent": LOGIN_WEBVIEW_USER_AGENT,
            "Accept-Language": "en-US",
            "Accept-Charset": "utf-8",
            "Connection": "keep-alive",
            "Content-type": "application/json; charset=UTF-8",
            "authorization": f"Bearer {self.access_token}",
        }

        async with self._session.put(
            "https://api.amazonalexa.com/v1/devices/@self/capabilities",
            json=data,
            headers=headers,
            allow_redirects=False,
        ) as response:
            _LOGGER.debug("Amazon capability registration returned %s", response.status)
            return response.status == 204

    async def refresh_access_token(self) -> bool:
        """Refresh access token and expires in using refresh token.

        Returns
            bool: Return true if successful.

        """
        if not self.refresh_token:
            _LOGGER.debug("No refresh token found to get access_token")
            return False
        data = {
            "app_name": APP_NAME,
            "app_version": LOGIN_APP_VERSION,
            "di.sdk.version": "6.12.4",
            "source_token": self.refresh_token,
            "package_name": "com.amazon.echo",
            "di.hw.version": "iPhone",
            "platform": "iOS",
            "requested_token_type": "access_token",
            "source_token_type": "refresh_token",
            "di.os.name": "iOS",
            "di.os.version": "16.6",
            "current_version": "6.12.4",
            "previous_version": "6.12.4",
        }
        # Ensure data dictionary is compiled...
        try:
            # Check explicitly if the session was closed outside of our scope
            if self._session is None or self._session.closed:
                _LOGGER.debug(
                    "Detected a closed or missing ClientSession. "
                    "Initializing a new session."
                )
                self._session = aiohttp.ClientSession()

            response = await self._session.post(
                "https://api." + self.url + "/auth/token",
                data=data,
                allow_redirects=False,
            )
        except (aiohttp.ClientConnectionError, RuntimeError) as e:
            # Catch the "Session is closed" RuntimeError explicitly
            if isinstance(e, RuntimeError) and "Session is closed" not in str(e):
                raise

            _LOGGER.debug(
                "Fallback attempt to refresh access token with api.amazon.com due to "
                "connection error or closed session."
            )

            # Safe fallback: create a brand new session context if it completely died
            if self._session is None or self._session.closed:
                self._session = aiohttp.ClientSession()

            try:
                response = await self._session.post(
                    "https://api.amazon.com/auth/token",
                    data=data,
                    allow_redirects=False,
                )
            except RuntimeError as fallback_err:
                if "Session is closed" in str(fallback_err):
                    # Raise an exception that the caller can safely intercept
                    raise ValueError(
                        "Alexa API ClientSession is closed and unrecoverable."
                    ) from fallback_err
                raise

        _LOGGER.debug("Amazon token refresh returned %s", response.status)
        if response.status != 200:
            return False
        response = await response.json()
        if response.get("access_token"):
            self.access_token = response.get("access_token")
            self.expires_in = datetime.datetime.now().timestamp() + int(
                response.get("expires_in")
            )
            _LOGGER.debug(
                "Successfully refreshed access_token(%s) which expires at %s in %s",
                len(self.access_token),
                datetime.datetime.fromtimestamp(self.expires_in),
                datetime.datetime.fromtimestamp(self.expires_in)
                - datetime.datetime.now(),
            )
            return True
        return False

    async def exchange_token_for_cookies(self) -> bool:
        """Generate new session cookies using refresh token.

        Returns
            bool: True if successful

        """
        if not self.refresh_token:
            _LOGGER.debug("No refresh token found to get access token")
            return False
        data = {
            "app_name": APP_NAME,
            "app_version": LOGIN_APP_VERSION,
            "di.sdk.version": "6.12.4",
            "domain": f".{self.url}",
            "source_token": self.refresh_token,
            "package_name": "com.amazon.echo",
            "di.hw.version": "iPhone",
            "platform": "iOS",
            "requested_token_type": "auth_cookies",
            "source_token_type": "refresh_token",
            "di.os.name": "iOS",
            "di.os.version": "16.6",
            "current_version": "6.12.4",
            "previous_version": "6.12.4",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            response = await self._session.post(
                "https://www." + self.url + "/ap/exchangetoken/cookies",
                data=data,
                headers=headers,
                allow_redirects=False,
            )
        except aiohttp.ClientConnectorError:
            _LOGGER.debug("Fallback attempt to exchange tokens with www.amazon.com")
            response = await self._session.post(
                "https://www.amazon.com/ap/exchangetoken/cookies",
                data=data,
                headers=headers,
                allow_redirects=False,
            )
        if response.status != 200:
            _LOGGER.debug("Amazon cookie exchange returned %s", response.status)
            return False
        response = (await response.json()).get("response")
        success = False
        for domain, cookies in response["tokens"]["cookies"].items():
            for item in cookies:
                raw_cookie = SimpleCookie()
                cookie_name = item["Name"]
                cookie_value = item["Value"]
                raw_cookie[cookie_name] = (
                    cookie_value
                    if not (cookie_value.startswith('"') and cookie_value.endswith('"'))
                    # Strings are returned within quotations, strip them
                    else cookie_value[1:-1]
                )
                raw_cookie[cookie_name]["domain"] = domain
                raw_cookie[cookie_name]["path"] = item["Path"]
                raw_cookie[cookie_name]["secure"] = item["Secure"]
                raw_cookie[cookie_name]["expires"] = item["Expires"]
                raw_cookie[cookie_name]["httpOnly"] = item["HttpOnly"]
                self._session.cookie_jar.update_cookies(raw_cookie, _cookie_url(domain))
            _LOGGER.info(
                "Exchanged refresh token for %s %s cookies: %s",
                len(cookies),
                domain,
                [c["Name"] for c in cookies],
            )
            success = True
        return success

    async def get_csrf(self) -> bool:
        """Generate csrf if missing.

        Returns
            bool: True if csrf is found

        """
        if self._api_csrf():
            return True
        assert self._session
        for path in (
            "/spa/index.html",
            "/api/language",
            "/api/devices-v2/device?cached=false",
            "/templates/oobe/d-device-pick.handlebars",
            "/api/strings",
        ):
            try:
                async with self._session.get(
                    f"{self._prefix}{self.url}{path}",
                    ssl=self._ssl,
                    allow_redirects=False,
                ) as response:
                    if response.status in (403, 429) or response.status >= 500:
                        return False
                    if response.status == 200 and self._api_csrf():
                        return True
            except (aiohttp.ClientError, TimeoutError):
                return False
        return False

    async def check_domain(self) -> bool:
        """Check whether logged into appropriate login domain.

        Returns
            bool: True if in correct domain

        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Charset": "utf-8",
            "x-amzn-identity-auth-domain": f"api.{self.url}",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": LOGIN_WEBVIEW_USER_AGENT,
            "Accept-Language": "en-US",
        }
        response = await self._session.get(
            f"{self._prefix}{self.url}/api/users/me?platform=ios&version={LOGIN_APP_VERSION}",
            headers=headers,
        )

        if response.status != 200:
            _LOGGER.debug("Amazon marketplace lookup was unavailable")
            return True

        try:
            response = await response.json(content_type=None)
        except (JSONDecodeError, ValueError):
            _LOGGER.debug("Amazon marketplace lookup was unavailable")
            return True

        domain = (
            self._reported_marketplace(response) if isinstance(response, dict) else None
        )
        if not domain:
            return True
        self.reported_account_domain = domain

        if self.url != domain:
            _LOGGER.warning(
                "Domain %s does not match reported account domain %s; "
                "functionality is not likely to work, please fix",
                self.url,
                domain,
            )
            return False

        _LOGGER.debug("Domain %s matches reported account domain: %s", self.url, domain)
        return True

    async def _process_resp(self, resp) -> str:
        if resp.history:
            for item in resp.history:
                _LOGGER.debug(
                    "%s: redirected from\n%s", item.method, item.url.with_query(None)
                )
            self._headers["Referer"] = str(resp.url)
        url = str(resp.request_info.url)
        method = resp.request_info.method
        status = resp.status
        _LOGGER.debug("%s %s returned %s", method, URL(url).with_query(None), status)
        self._headers["Referer"] = str(url)
        return url

    async def _process_page(self, html: str, site: str) -> str | None:  # noqa: PLR0915
        """Process html to set login.status and find form post url."""

        def find_links() -> None:
            links = {}
            index = 0
            if links_tag:
                for link in links_tag:
                    if not link.string:
                        continue
                    string = link.string.strip()
                    href = link["href"]
                    # _LOGGER.debug("Found link: %s <%s>",
                    #               string,
                    #               href)
                    if href.startswith("/"):
                        links[str(index)] = (string, (self._prefix + self.url + href))
                        index += 1
                    elif href.startswith("http"):
                        links[str(index)] = (string, href)
                        index += 1
            if forms_tag:
                for form in forms_tag:
                    if (
                        form.get("method")
                        and form.get("method") == "get"
                        and form.get("action")
                    ):
                        string = form.get("id")
                        action = form.get("action")
                        params = {}
                        inputs = form.findAll("input")
                        for item in inputs:
                            if (
                                item
                                and item.get("type")
                                and item.get("type") == "hidden"
                            ):
                                params[item.get("name")] = item.get("value")
                        href = f"{self._prefix}{self.url}{action}?{urlencode(params)}"
                        links[str(index)] = (string, href)
                        index += 1
            if links:
                _LOGGER.debug("Found %s sign-in links", len(links))
            self._links = links

        _LOGGER.debug("Processing Amazon sign-in response")
        site_url = URL(site)
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

        status: dict[str, str | bool] = {}

        #  Find tags to determine which path
        login_tag = soup.find("form", {"name": "signIn"})
        captcha_tag = soup.find(id="auth-captcha-image")
        securitycode_tag = soup.find(id="auth-mfa-otpcode")
        errorbox = (
            soup.find(id="auth-error-message-box")
            if soup.find(id="auth-error-message-box")
            else soup.find(id="auth-warning-message-box")
        )
        claimspicker_tag = soup.find("form", {"name": "claimspicker"})
        authselect_tag = soup.find("form", {"id": "auth-select-device-form"})
        verificationcode_tag = soup.find("form", {"action": "verify"})
        verification_captcha_tag = soup.find("img", {"alt": "captcha"})
        javascript_authentication_tag = soup.find("form", {"id": "pollingForm"})
        links_tag = soup.findAll("a", href=True)
        forms_tag = soup.findAll("form")
        form_tag = soup.find("form")
        missingcookies_tag = soup.find(id="ap_error_return_home")
        forgotpassword_tag = soup.find("form", {"name": "forgotPassword"})
        polling_tag = soup.find(id="updatedChannelDetails")
        if self._debug:
            find_links()

        # pull out Amazon error message

        if errorbox:
            error_message = errorbox.find("h4").string
            if error_message is None:
                error_message = "unknown"
            for list_item in errorbox.findAll("li"):
                span_text = list_item.find("span").text
                if span_text:
                    error_message += span_text
            _LOGGER.debug("Error message: %s", error_message)
            status["error_message"] = error_message

        if login_tag and not captcha_tag:
            _LOGGER.debug("Found standard login page")
            #  scrape login page to get all the inputs required for login
            self._data = self.get_inputs(soup, {"name": "signIn"})
        elif captcha_tag is not None:
            _LOGGER.debug("Captcha requested")
            status["captcha_required"] = True
            status["captcha_image_url"] = captcha_tag.get("src")
            self._data = self.get_inputs(soup)

        elif securitycode_tag is not None:
            _LOGGER.debug("2FA requested")
            status["securitycode_required"] = True
            self._data = self.get_inputs(soup, {"id": "auth-mfa-form"})

        elif claimspicker_tag is not None:
            self._options = {}
            index = 0
            claims_message = ""
            options_message = ""
            for div in claimspicker_tag.findAll("div", "a-row"):
                claims_message += f"{div.text}\n"
            for label in claimspicker_tag.findAll("label"):
                value = (
                    (label.find("input")["value"]).strip()
                    if label.find("input")
                    else ""
                )
                message = (
                    (label.find("span").string).strip() if label.find("span") else ""
                )
                valuemessage = (
                    (f"* **`{index}`**:\t `{value} - {message}`.\n")
                    if value != ""
                    else ""
                )
                options_message += valuemessage
                if value:
                    self._options[str(index)] = value
                    index += 1
            _LOGGER.debug(
                "Verification method requested: %s, %s", claims_message, options_message
            )
            status["claimspicker_required"] = True
            status["claimspicker_message"] = options_message
            self._data = self.get_inputs(soup, {"name": "claimspicker"})
        elif authselect_tag is not None:
            self._options = {}
            index = 0
            authselect_message = ""
            authoptions_message = ""
            for div in soup.findAll("div", "a-box-inner"):
                if div.find("p"):
                    authselect_message += f"{div.find('p').string}\n"
            for label in authselect_tag.findAll("label"):
                value = (
                    (label.find("input")["value"]).strip()
                    if label.find("input")
                    else ""
                )
                message = (
                    (label.find("span").string).strip() if label.find("span") else ""
                )
                valuemessage = (f"{index}:\t{message}\n") if value != "" else ""
                authoptions_message += valuemessage
                if value:
                    self._options[str(index)] = value
                    index += 1
            _LOGGER.debug(
                "OTP method requested: %s%s", authselect_message, authoptions_message
            )
            status["authselect_required"] = True
            status["authselect_message"] = authoptions_message
            self._data = self.get_inputs(soup, {"id": "auth-select-device-form"})
        elif verification_captcha_tag is not None:
            _LOGGER.debug("Verification captcha code requested:")
            status["captcha_required"] = True
            status["captcha_image_url"] = verification_captcha_tag.get("src")
            status["verification_captcha_required"] = True
            self._data = self.get_inputs(soup, {"action": "verify"})
        elif verificationcode_tag is not None:
            _LOGGER.debug("Verification code requested:")
            status["verificationcode_required"] = True
            self._data = self.get_inputs(soup, {"action": "verify"})
        elif missingcookies_tag is not None and site_url.path != "/ap/maplanding":
            _LOGGER.debug("Error page detected:")
            href = ""
            links = missingcookies_tag.findAll("a", href=True)
            for link in links:
                href = link["href"]
            status["ap_error"] = True
            status["force_get"] = True
            status["ap_error_href"] = href
        elif javascript_authentication_tag:
            message: str = ""

            message = soup.find("span").getText()
            for div in soup.findAll("div", {"id": "channelDetails"}):
                message += div.getText()
            status["force_get"] = True
            status["message"] = re.sub("(\\s)+", "\\1", message)
            status["action_required"] = True
            _LOGGER.debug("Javascript Authentication page detected: %s", message)
        elif forgotpassword_tag or soup.find("input", {"name": "OTPChallengeOptions"}):
            status["message"] = (
                "Forgot password page detected; "
                "Amazon has detected too many failed logins. "
                "Please check to see if Amazon requires any further action. "
                "You may have to wait before retrying."
            )
            status["ap_error"] = True
            _LOGGER.warning(status["message"])
            status["login_failed"] = "forgot_password"
        elif polling_tag:
            status["force_get"] = True
            status["message"] = self.status["message"]
            approval_status = soup.find("input", {"id": "transactionApprovalStatus"})
            _LOGGER.debug(
                "Polling page detected: %s with %s", polling_tag, approval_status
            )
            status["approval_status"] = approval_status.get("value")
        else:
            _LOGGER.debug("Captcha/2FA not requested; confirming login.")
            query = site_url.query
            original_token, original_code = self.access_token, self.authorization_code
            self.access_token = query.get("openid.oa2.access_token")
            self.authorization_code = query.get("openid.oa2.authorization_code")
            verified = False
            try:
                verified = await self.test_loggedin()
                if verified:
                    return
            finally:
                if not verified:
                    self.access_token, self.authorization_code = (
                        original_token,
                        original_code,
                    )
            _LOGGER.debug("Login failed; check credentials")
            status["login_failed"] = "login_failed"
            if self._data and "" in self._data.values():
                missing = [k for (k, v) in self._data.items() if v == ""]
                _LOGGER.debug(
                    "If credentials correct, please report these missing values: %s",
                    missing,
                )
        self.status = status
        # determine post url if not logged in
        if status.get("approval_status") == "TransactionCompleted":
            site = self._data.get("openid.return_to")
        elif form_tag and "login_successful" not in status:
            formsite: str = form_tag.get("action")
            if self._debug:
                _LOGGER.debug("Found an Amazon sign-in form")
            if formsite and formsite == "verify":
                search_results = re.search(r"(.+)/(.*)", str(site))
                assert search_results is not None
                site = search_results.groups()[0] + "/verify"
                _LOGGER.debug("Found sign-in verification form")
            elif formsite and formsite == "get":
                if "ap_error" in status and status.get("ap_error_href"):
                    assert isinstance(status["ap_error_href"], str)
                    site = status["ap_error_href"]
                elif self._headers.get("Referer"):
                    site = self._headers["Referer"]
                else:
                    site = self.start_url
                _LOGGER.debug("Found sign-in continuation")
                self._lastreq = None
            elif formsite and formsite == "/ap/cvf/approval/poll":
                self._data = self.get_inputs(soup, {"id": "pollingForm"})
                url = urlparse(site)
                site = f"{url.scheme}://{url.netloc}{formsite}"
                # site = form_tag.find("input", {"name": "openid.return_to"}).get("value")  # noqa: E501
                _LOGGER.debug("Found sign-in approval page")
            elif formsite and forgotpassword_tag:
                site = self.start_url
                _LOGGER.debug("Restarting sign-in")
            elif formsite:
                site = site_url.join(URL(formsite))
                _LOGGER.debug("Found sign-in form destination")
        return str(site)

    def _populate_data(self, site: str, data: dict[str, str | None]) -> bool:
        """Populate self._data with info from data."""
        _LOGGER.debug("Preparing Amazon sign-in form submission")
        # pull data from configurator
        password: str | None = data.get("password", "")
        captcha: str | None = data.get("captcha", "")
        if data.get("otp_secret"):
            self.set_totp(data.get("otp_secret", ""))
        securitycode: str | None = data.get("securitycode", "")
        if not securitycode and self._totp:
            _LOGGER.debug("No 2FA code supplied but will generate.")
            securitycode = self.get_totp_token()
        claimsoption: str | None = data.get("claimsoption", "")
        authopt: str | None = data.get("authselectoption", "")
        verificationcode: str | None = data.get("verificationcode", "")

        #  add username and password to self._data for post request
        #  self._data is scraped from the form page in _process_page
        #  check if there is an input field
        if self._data:
            if "email" in self._data and self._data["email"] == "":
                self._data["email"] = self._email
                # add the otp to the password if available
            self._data["password"] = (
                self._password + securitycode
                if not password
                else password + securitycode
                if securitycode
                else password
            )
            if "rememberMe" in self._data:
                self._data["rememberMe"] = "true"
            if captcha is not None and "guess" in self._data:
                self._data["guess"] = captcha
            if captcha is not None and "cvf_captcha_input" in self._data:
                self._data["cvf_captcha_input"] = captcha
                self._data["cvf_captcha_captcha_action"] = "verifyCaptcha"
            if securitycode is not None and "otpCode" in self._data:
                self._data["otpCode"] = securitycode
                self._data["rememberDevice"] = "true"
            if claimsoption is not None and "option" in self._data:
                try:
                    self._data["option"] = self._options[str(claimsoption)]
                except KeyError:
                    _LOGGER.debug(
                        "Selected claimspicker option %s not in %s",
                        str(claimsoption),
                        self._options,
                    )
            if authopt is not None and "otpDeviceContext" in self._data:
                try:
                    self._data["otpDeviceContext"] = self._options[str(authopt)]
                except KeyError:
                    _LOGGER.debug(
                        "Selected OTP option %s not in %s",
                        str(authopt),
                        self._options,
                    )
            if verificationcode is not None and "code" in self._data:
                self._data["code"] = verificationcode
            self._data.pop("", None)  # remove '' key
            return "" in self._data.values()  # test if unfilled values
        return False

    async def finalize_login(self) -> None:
        """Perform final steps after successful login."""
        _LOGGER.debug(
            "Login confirmed for %s - %s; saving cookie to %s",
            hide_email(self.email),
            self.url,
            self._cookiefile[0].replace(self.email, hide_email(self.email)),
        )
        if self._session:
            csrf = self._api_csrf()
            if csrf:
                self._headers["csrf"] = csrf
        self.status = {"login_successful": True}
        if not self._defer_cookie_save:
            await self.save_cookiefile()
        #  remove extraneous Content-Type to avoid 500 errors
        self._headers.pop("Content-Type", None)
