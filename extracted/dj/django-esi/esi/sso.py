"""Requests to the EVE SSO: authorization, code exchange, token refresh and JWKS (cached).

Uses one long lived httpx2 client per process, sharing the timeouts and connection
pool settings of the ESI clients, with its own User-Agent and retry/backoff.

No httpx2 exception escapes this module, they are raised as `SSOUnavailableError`.
This keeps them from being retried a second time by the ESI client's retries,
which wrap token refreshes made during an ESI request.
"""
import logging
import os
import secrets
import threading
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import urlencode

import httpx2
from tenacity import (
    RetryCallState, Retrying, before_sleep_log, retry_if_exception, stop_after_attempt, wait_exponential,
)

from django.core.cache import cache

from esi import app_settings

from .errors import IncompleteResponseError, SSOOAuthError, SSOUnavailableError
from .http_utils import build_django_esi_user_agent, build_limits, build_timeout, time_to_expiry, unpack_cache_control

logger = logging.getLogger(__name__)

SSO_RETRY_STATUS_CODES = {429, 502, 503, 504}

JWKS_CACHE_KEY = "esi_sso_jwks"
JWKS_DEFAULT_CACHE_TIME = 60 * 5  # If the SSO doesn't say
JWKS_FORCE_REFRESH_LOCK_KEY = "esi_sso_jwks_force_refresh"
JWKS_FORCE_REFRESH_COOLDOWN = 60

# Errors raised before the request was sent, so always safe to retry.
_NOT_SENT_ERRORS = (httpx2.ConnectError, httpx2.ConnectTimeout, httpx2.PoolTimeout)

_client: httpx2.Client | None = None
_client_pid: int | None = None
_client_lock = threading.Lock()


def sso_user_agent() -> str:
    return app_settings.ESI_SSO_USER_AGENT or build_django_esi_user_agent()


def _build_client(**kwargs) -> httpx2.Client:
    return httpx2.Client(
        headers={"User-Agent": sso_user_agent()},
        timeout=build_timeout(),
        limits=build_limits(),
        http2=True,
        **kwargs
    )


def sso_client() -> httpx2.Client:
    """The shared SSO client for this process.

    Rebuilt after a fork, so prefork celery workers never share connections.
    """
    global _client, _client_pid
    pid = os.getpid()
    if _client is None or _client_pid != pid:
        with _client_lock:
            if _client is None or _client_pid != pid:
                _client = _build_client()
                _client_pid = pid
    return _client


def _retry_after(exc: BaseException) -> float | None:
    """Seconds to wait from a Retry-After header, in either seconds or HTTP-date form."""
    response = getattr(exc, "response", None)
    if response is None:
        return None
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    try:
        return max(float(value), 0.0)
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max((when - datetime.now(timezone.utc)).total_seconds(), 0.0)


def _is_retryable(exc: BaseException, idempotent: bool) -> bool:
    """
    Helper function for SSO Retries, what exceptions and status codes should we retry on.
    A non idempotent request (single use auth code) is only retried
    if it never reached the SSO, or the SSO explicitly refused it.
    """
    if isinstance(exc, httpx2.HTTPStatusError):
        if exc.response.status_code not in SSO_RETRY_STATUS_CODES:
            return False
        retry_after = _retry_after(exc)
        return retry_after is None or retry_after <= app_settings.ESI_SSO_MAX_RETRY_AFTER
    if idempotent:
        return isinstance(exc, httpx2.TransportError)
    return isinstance(exc, _NOT_SENT_ERRORS)


def sso_retry(idempotent: bool = True) -> Retrying:
    exponential = wait_exponential(multiplier=app_settings.ESI_SSO_WAIT_EXPONENT, min=1, max=10)

    def wait(retry_state: RetryCallState) -> float:
        retry_after = _retry_after(retry_state.outcome.exception())
        if retry_after is not None:
            return retry_after
        return exponential(retry_state)

    return Retrying(
        retry=retry_if_exception(lambda exc: _is_retryable(exc, idempotent)),
        wait=wait,
        stop=stop_after_attempt(app_settings.ESI_SSO_MAX_RETRIES),
        sleep=time.sleep,
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


def _request(method: str, url: str, idempotent: bool = True, **kwargs) -> httpx2.Response:
    """Send a request to the SSO with retries.

    Raises:
        SSOUnavailableError: SSO unreachable, or still failing after retries
    """
    def send() -> httpx2.Response:
        response = sso_client().request(method, url, **kwargs)
        if response.status_code in SSO_RETRY_STATUS_CODES:
            response.raise_for_status()
        return response

    try:
        return sso_retry(idempotent)(send)
    except httpx2.HTTPError as e:
        logger.warning("SSO request %s %s failed: %r", method, url, e)
        raise SSOUnavailableError(str(e)) from e


def _token_request(data: dict[str, str], idempotent: bool) -> dict[str, Any]:
    """POST to the SSO token endpoint, authenticated as this application.

    Raises:
        SSOOAuthError: SSO rejected the request, eg `invalid_grant`
        IncompleteResponseError: Success response without an access token
        SSOUnavailableError: SSO unreachable or returned an unexpected response
    """
    response = _request(
        "POST",
        app_settings.ESI_TOKEN_URL,
        idempotent=idempotent,
        data=data,
        auth=(app_settings.ESI_SSO_CLIENT_ID, app_settings.ESI_SSO_CLIENT_SECRET),
        headers={"Accept": "application/json"},
    )
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if response.is_success:
        if not isinstance(payload, dict) or "access_token" not in payload:
            logger.info("SSO token response missing access token")
            raise IncompleteResponseError()
        return payload

    if isinstance(payload, dict) and "error" in payload:
        raise SSOOAuthError(payload["error"], payload.get("error_description"))

    logger.warning("Unexpected %s response from SSO token endpoint", response.status_code)
    raise SSOUnavailableError(f"Unexpected {response.status_code} response from SSO")


def authorization_url(scopes: list[str] | None = None) -> tuple[str, str]:
    """Build the SSO login URL to redirect a user to.

    Returns:
        (url, state)
    """
    state = secrets.token_urlsafe(24)
    params = {
        "response_type": "code",
        "client_id": app_settings.ESI_SSO_CLIENT_ID,
        "redirect_uri": app_settings.ESI_SSO_CALLBACK_URL,
        "state": state,
    }
    if scopes:
        params["scope"] = " ".join(scopes)
    return f"{app_settings.ESI_OAUTH_LOGIN_URL}?{urlencode(params)}", state


def exchange_code(code: str) -> dict[str, Any]:
    """Exchange an authorization code for a token.

    Codes are single use, so this is only retried if the request never reached the SSO.
    """
    return _token_request(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": app_settings.ESI_SSO_CALLBACK_URL,
        },
        idempotent=False,
    )


def refresh_token(refresh_token: str) -> dict[str, Any]:
    """Get a new access token using a refresh token."""
    token = _token_request(
        {"grant_type": "refresh_token", "refresh_token": refresh_token},
        idempotent=True,
    )
    # Not every response rotates the refresh token
    token.setdefault("refresh_token", refresh_token)
    return token


def _jwks_cache_ttl(response: httpx2.Response) -> int:
    """How long the SSO says its JWKS response stays fresh.

    The SSO sits behind a CDN, so the time a response has already spent in the
    CDN's cache (Age header) is taken off. If Date is the origin's time rather than
    the CDN's this undercounts the ttl, which only means refetching sooner.
    """
    headers = response.headers
    if "cache-control" in headers:
        ttl = unpack_cache_control(headers)
    elif "expires" in headers:
        ttl = time_to_expiry(headers["expires"])
    else:
        return JWKS_DEFAULT_CACHE_TIME
    try:
        age = int(headers.get("age", 0))
    except ValueError:
        age = 0
    return max(ttl - age, 0)


def _fetch_jwks() -> tuple[dict[str, Any], int]:
    response = _request("GET", app_settings.ESI_TOKEN_JWK_SET_URL)
    try:
        response.raise_for_status()
        return response.json(), _jwks_cache_ttl(response)
    except (httpx2.HTTPStatusError, ValueError) as e:
        logger.warning("Failed to fetch JWKS from SSO: %r", e)
        raise SSOUnavailableError(str(e)) from e


def get_jwks(force_refresh: bool = False) -> dict[str, Any]:
    """The SSO's JSON Web Key Set, for validating access tokens.

    Cached for as long as the SSO says it is fresh.

    Args:
        force_refresh: Skip the cache, eg when a token is signed by a key that isn't cached.
            Limited to once per JWKS_FORCE_REFRESH_COOLDOWN, otherwise the cached keys are returned.
    """
    if force_refresh and not cache.add(JWKS_FORCE_REFRESH_LOCK_KEY, True, JWKS_FORCE_REFRESH_COOLDOWN):
        logger.debug("JWKS force refresh on cooldown, using cached keys")
        force_refresh = False
    if not force_refresh:
        jwks = cache.get(JWKS_CACHE_KEY)
        if jwks is not None:
            return jwks

    jwks, ttl = _fetch_jwks()
    if ttl > 0 and isinstance(jwks, dict) and isinstance(jwks.get("keys"), list):
        cache.set(JWKS_CACHE_KEY, jwks, ttl)
    return jwks
