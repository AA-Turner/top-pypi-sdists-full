"""Enrollment-only authentication for the alexa_media_player auth redesign.

Design: https://github.com/superbeetle1973/alexa-auth-redesign

The user authenticates interactively through Amazon's real login page in
their own browser (paste-URL flow, no proxy) and the pasted redirect URL is
exchanged for durable device credentials. Nothing here ever handles or
stores the account password or a TOTP seed.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import secrets
import time
from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

import aiohttp
from yarl import URL

# Suffix Amazon's iOS Alexa app appends to the serial to form the client
# device id (matches the registration identity used since alexapy 1.25).
# Already hex-encoded; append literally, do not hex-encode it again.
_DEVICE_ID_SUFFIX = "23413249564c5635564d32573831"

_LOCALE_BY_TLD = {
    ".com": "en_US",
    ".co.uk": "en_GB",
    ".de": "de_DE",
    ".fr": "fr_FR",
    ".it": "it_IT",
    ".es": "es_ES",
    ".com.au": "en_AU",
    ".co.jp": "ja_JP",
    ".com.br": "pt_BR",
    ".ca": "en_CA",
    ".com.mx": "es_MX",
    ".in": "en_IN",
}

# Only these Amazon marketplace domains may be used. The domain is interpolated
# into every auth endpoint and the login URL, so an unvalidated value would let
# a mistyped or attacker-supplied domain receive the authorization code and PKCE
# verifier. Reject anything not on this allowlist.
ALLOWED_DOMAINS = frozenset(f"amazon{tld}" for tld in _LOCALE_BY_TLD)


_APP_NAME = "Amazon Alexa"
_CALL_VERSION = "2.2.556530.0"


class EnrollmentError(Exception):
    """Enrollment could not proceed with the provided input."""


class AuthTransientError(Exception):
    """Retryable failure (network, throttling, server error); back off, don't reauth."""


class AuthTerminalError(Exception):
    """The stored credentials are dead — interactive re-enrollment is required."""


@dataclass(frozen=True)
class DeviceCredentials:
    """The only durable credential material this design persists."""

    refresh_token: str
    mac_dms: dict[str, Any] = field(default_factory=dict)
    serial: str = ""
    customer_id: str | None = None
    domain: str = "amazon.com"

    def as_dict(self) -> dict[str, Any]:
        """Return the credentials as a plain dict, for storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeviceCredentials:
        """Reconstruct credentials from a dict produced by `as_dict`."""
        return cls(**data)


class EnrollmentFlow:
    """One interactive enrollment attempt.

    Holds the PKCE verifier in memory only; a new flow gets fresh secrets.
    """

    def __init__(
        self,
        domain: str = "amazon.com",
        serial: str | None = None,
        code_verifier: str | None = None,
    ) -> None:
        """Start a new flow, generating fresh PKCE/serial secrets if omitted."""
        if domain not in ALLOWED_DOMAINS:
            raise EnrollmentError(
                f"Unsupported Amazon domain '{domain}'. Supported domains: "
                + ", ".join(sorted(ALLOWED_DOMAINS))
            )
        self.domain = domain
        self.serial = serial if serial else uuid4().hex.upper()
        self.code_verifier: str = (
            code_verifier
            if code_verifier
            else base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
        )

    def to_state(self) -> dict[str, str]:
        """Serialize the flow so another process can complete the exchange.

        Contains the PKCE verifier — persist only to a private, short-lived
        location; delete once enrollment finishes.
        """
        return {
            "domain": self.domain,
            "serial": self.serial,
            "code_verifier": self.code_verifier,
        }

    @classmethod
    def from_state(cls, state: dict[str, Any]) -> EnrollmentFlow:
        """Restore a flow from `to_state`'s output, e.g. in another process."""
        return cls(
            domain=state["domain"],
            serial=state["serial"],
            code_verifier=state["code_verifier"],
        )

    @property
    def code_challenge(self) -> str:
        """Return the S256 PKCE code challenge derived from `code_verifier`."""
        return (
            base64.urlsafe_b64encode(
                hashlib.sha256(self.code_verifier.encode()).digest()
            )
            .rstrip(b"=")
            .decode()
        )

    @property
    def device_id(self) -> str:
        """Return the client device id derived from `serial`."""
        return self.serial.encode().hex() + _DEVICE_ID_SUFFIX

    @property
    def oauth_url(self) -> str:
        """Login URL the user opens in their own browser."""
        tld = self.domain.removeprefix("amazon")
        query = {
            "openid.return_to": f"https://www.{self.domain}/ap/maplanding",
            "openid.assoc_handle": "amzn_dp_project_dee_ios",
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "pageId": "amzn_dp_project_dee_ios",
            "accountStatusPolicy": "P1",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.mode": "checkid_setup",
            "openid.ns.oa2": "http://www.amazon.com/ap/ext/oauth/2",
            "openid.oa2.client_id": f"device:{self.device_id}",
            "openid.ns.pape": "http://specs.openid.net/extensions/pape/1.0",
            "openid.oa2.response_type": "code",
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.pape.max_auth_age": "0",
            "openid.oa2.scope": "device_auth_access offline_access",
            "openid.oa2.code_challenge_method": "S256",
            "openid.oa2.code_challenge": self.code_challenge,
            "language": _LOCALE_BY_TLD.get(tld, "en_US"),
        }
        return str(URL(f"https://www.{self.domain}/ap/register").update_query(query))

    def parse_redirect_url(self, pasted_url: str) -> str:
        """Extract the authorization code from the pasted maplanding URL."""
        try:
            url = URL(pasted_url.strip())
        except (ValueError, TypeError) as ex:
            raise EnrollmentError(f"Could not parse the pasted URL: {ex}") from ex
        if url.scheme != "https":
            raise EnrollmentError("The pasted URL must be an https:// Amazon URL")
        if url.path != "/ap/maplanding":
            raise EnrollmentError(
                "The pasted URL does not look like an Amazon maplanding redirect"
            )
        expected_host = f"www.{self.domain}"
        if url.host != expected_host:
            raise EnrollmentError(
                f"The pasted URL is for {url.host}, but this flow uses the"
                f" {expected_host} domain"
            )
        code = url.query.get("openid.oa2.authorization_code")
        if not code:
            raise EnrollmentError(
                "The pasted URL does not contain an authorization code"
            )
        return code

    async def async_register(
        self, session: aiohttp.ClientSession, authorization_code: str
    ) -> DeviceCredentials:
        """Exchange the authorization code for durable device credentials."""
        frc = base64.b64encode(secrets.token_bytes(313)).decode("ascii").rstrip("=")
        map_md = (
            base64.b64encode(
                json.dumps(
                    {
                        "device_user_dictionary": [],
                        "device_registration_data": {"software_version": "1"},
                        "app_identifier": {
                            "app_version": _CALL_VERSION,
                            "bundle_id": "com.amazon.echo",
                        },
                    }
                ).encode()
            )
            .decode()
            .rstrip("=")
        )
        payload = {
            "requested_extensions": ["device_info", "customer_info"],
            "cookies": {"website_cookies": [], "domain": f".{self.domain}"},
            "registration_data": {
                "domain": "Device",
                "app_version": _CALL_VERSION,
                "device_type": "A2IVLV5VM2W81",
                "device_name": (f"%FIRST_NAME%'s%DUPE_STRATEGY_1ST%{_APP_NAME}"),
                "os_version": "16.6",
                "device_serial": self.serial,
                "device_model": "iPhone",
                "app_name": _APP_NAME,
                "software_version": "1",
            },
            "auth_data": {
                "client_id": self.device_id,
                "authorization_code": authorization_code,
                "code_verifier": self.code_verifier,
                "code_algorithm": "SHA-256",
                "client_domain": "DeviceLegacy",
            },
            "user_context_map": {"frc": frc},
            "requested_token_type": ["bearer", "mac_dms", "website_cookies"],
        }
        try:
            async with session.post(
                f"https://api.{self.domain}/auth/register",
                json=payload,
                headers={"Content-Type": "application/json"},
                cookies={"frc": frc, "map-md": map_md},
            ) as response:
                status = response.status
                try:
                    parsed = await response.json(content_type=None)
                except (json.JSONDecodeError, aiohttp.ClientError, ValueError) as ex:
                    raise EnrollmentError(
                        f"Device registration returned an unreadable response "
                        f"(HTTP {status})"
                    ) from ex
        except (aiohttp.ClientError, TimeoutError) as ex:
            raise EnrollmentError(f"Device registration request failed: {ex}") from ex
        if status != 200:
            raise EnrollmentError(f"Device registration failed with HTTP {status}")
        body = (parsed if isinstance(parsed, dict) else {}).get("response")
        body = body if isinstance(body, dict) else {}
        success = body.get("success")
        if not success:
            error = body.get("error")
            error = error if isinstance(error, dict) else {}
            raise EnrollmentError(
                "Device registration rejected: "
                f"{error.get('code', 'unknown')} — {error.get('message', '')}"
            )
        try:
            refresh_token = success["tokens"]["bearer"]["refresh_token"]
            mac_dms = success["tokens"]["mac_dms"]
        except (KeyError, TypeError) as ex:
            raise EnrollmentError(
                "Device registration response was missing expected tokens"
            ) from ex
        return DeviceCredentials(
            refresh_token=refresh_token,
            mac_dms=mac_dms,
            serial=self.serial,
            customer_id=success.get("extensions", {})
            .get("customer_info", {})
            .get("user_id"),
            domain=self.domain,
        )


_TOKEN_FORM_BASE = {
    "app_name": _APP_NAME,
    "app_version": _CALL_VERSION,
    "di.sdk.version": "6.12.4",
    "package_name": "com.amazon.echo",
    "di.hw.version": "iPhone",
    "platform": "iOS",
    "di.os.name": "iOS",
    "di.os.version": "16.6",
    "current_version": "6.12.4",
    "previous_version": "6.12.4",
}


class TokenManager:
    """Runtime token lifecycle for a set of stored device credentials.

    Serializes refresh attempts; classifies failures into transient
    (AuthTransientError — caller backs off and retries) vs terminal
    (AuthTerminalError — caller escalates to interactive re-enrollment).
    """

    def __init__(self, credentials: DeviceCredentials) -> None:
        """Create a manager for the given (already-enrolled) device credentials."""
        self.credentials = credentials
        self.access_token: str | None = None
        self.expires_at: float = 0.0
        self._refresh_lock = asyncio.Lock()

    async def async_refresh_access_token(self, session: aiohttp.ClientSession) -> str:
        """Mint a fresh access token from the refresh token."""
        form = dict(
            _TOKEN_FORM_BASE,
            source_token=self.credentials.refresh_token,
            requested_token_type="access_token",
            source_token_type="refresh_token",
        )
        async with self._refresh_lock:
            try:
                async with session.post(
                    f"https://api.{self.credentials.domain}/auth/token", data=form
                ) as response:
                    status = response.status
                    try:
                        body = await response.json(content_type=None)
                    except (json.JSONDecodeError, aiohttp.ClientError):
                        body = {}
                    body = body if isinstance(body, dict) else {}
            except (aiohttp.ClientError, TimeoutError) as ex:
                raise AuthTransientError(f"Token refresh failed: {ex}") from ex
            if status == 200 and body.get("access_token"):
                self.access_token = body["access_token"]
                self.expires_at = time.time() + int(body.get("expires_in") or 0)
                return self.access_token
            error = body.get("error")
            if status in (400, 401) and error in (
                "invalid_grant",
                "invalid_token",
                "unauthorized_client",
            ):
                raise AuthTerminalError(
                    f"Refresh token rejected ({error}): "
                    f"{body.get('error_description', '')}"
                )
            raise AuthTransientError(
                f"Token refresh failed with HTTP {status}"
                + (f" ({error})" if error else "")
            )

    async def async_exchange_cookies(
        self, session: aiohttp.ClientSession
    ) -> dict[str, dict[str, str]]:
        """Re-mint session cookies from the refresh token, per domain."""
        form = dict(
            _TOKEN_FORM_BASE,
            domain=f".{self.credentials.domain}",
            source_token=self.credentials.refresh_token,
            requested_token_type="auth_cookies",
            source_token_type="refresh_token",
        )
        try:
            async with session.post(
                f"https://www.{self.credentials.domain}/ap/exchangetoken/cookies",
                data=form,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            ) as response:
                if response.status != 200:
                    raise AuthTransientError(
                        f"Cookie exchange failed with HTTP {response.status}"
                    )
                try:
                    parsed = await response.json(content_type=None)
                except (json.JSONDecodeError, aiohttp.ClientError, ValueError) as ex:
                    raise AuthTransientError(
                        f"Cookie exchange returned an unreadable response: {ex}"
                    ) from ex
        except (aiohttp.ClientError, TimeoutError) as ex:
            raise AuthTransientError(f"Cookie exchange failed: {ex}") from ex
        # Walk the response defensively: any shape that isn't the expected
        # nested dict/list structure (null response, list body, non-string
        # cookie value, etc.) is a malformed response, not a usable session, so
        # map it to a retryable error rather than letting an AttributeError or
        # TypeError escape into the caller.
        cookies: dict[str, dict[str, str]] = {}
        try:
            body = (parsed or {}).get("response") or {}
            cookie_map = ((body.get("tokens") or {}).get("cookies")) or {}
            for domain, items in cookie_map.items():
                cookies[domain] = {}
                for item in items or []:
                    value = item["Value"]
                    name = item["Name"]
                    if not isinstance(value, str) or not isinstance(name, str):
                        raise TypeError("cookie Name/Value must be strings")
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    cookies[domain][name] = value
        except (AttributeError, TypeError, KeyError, ValueError) as ex:
            raise AuthTransientError(
                f"Cookie exchange returned a malformed response: {ex}"
            ) from ex
        # A 200 with no cookies for the requested domain is not a usable session;
        # treat it as retryable rather than silently "succeeding" and letting
        # callers persist/keep credentials that never minted a session.
        expected = f".{self.credentials.domain}"
        if not cookies.get(expected):
            raise AuthTransientError(
                f"Cookie exchange returned no cookies for {expected}"
            )
        return cookies

    async def async_deregister(self, session: aiohttp.ClientSession) -> bool:
        """Best-effort device deregistration; never raises."""
        if not self.access_token:
            return False
        try:
            async with session.post(
                f"https://api.{self.credentials.domain}/auth/deregister",
                json={"requested_deregister_type": "deregister_device"},
                headers={"Authorization": f"Bearer {self.access_token}"},
            ) as response:
                return response.status == 200
        except (aiohttp.ClientError, TimeoutError):
            return False
