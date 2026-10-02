"""Identity Service authentication client (RFC 7523 private_key_jwt).

Decodes identity-service client credentials, builds a `client_assertion` JWT,
exchanges it at the identity-service's token endpoint for an access token, and
manages token refresh (proactive, before expiry) with bounded retry/backoff.
`IdentityServiceClient.request` then makes authenticated calls with that token.

This is also the shared floor for the other hand-written Identity Service surfaces: the
request primitives live here so the Identity Service endpoint wrappers can reuse one
implementation. They are hand-written because the Identity Service publishes no OpenAPI
spec and we need precise retry/backoff and 4xx-vs-5xx classification.

The credential format matches the registry service and the agent: a JSON object
`{clientId, keyId, key}` where `key` is a PEM-encoded ECDSA P-384 private
key. The secret may be supplied inline as a base64-encoded JSON blob, or as a
path to a raw JSON credentials file (the format produced by the keypair helpers
in `istari_digital_client._auth.keys`).

`cryptography` and `jwt` are imported lazily inside functions because this
module is reachable from `import istari` (via the
`istari_digital_client._configuration.Configuration`), and importing
cryptography's Rust extension at package-import time crashes under the
pytest-cov subinterpreter (see the note in `istari_digital_client._auth.keys`).
"""

from __future__ import annotations

import base64
import binascii
import json
import logging
import os
import random
import ssl
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar

import urllib3

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey

logger = logging.getLogger("istari_digital_client._auth.identity_service")

_TOKEN_ENDPOINT_PATH = "/oauth2/token"
_CLIENT_ASSERTION_EXPIRATION_SECONDS = 300
_REQUEST_TIMEOUT_SECONDS = 10
# Re-authenticate when the token has less than this many seconds remaining.
_REFRESH_MARGIN_SECONDS = 60
# Proportional jitter applied to backoff intervals when jitter is enabled.
_JITTER_FRACTION = 0.1

# Fallback retry values used when the corresponding Configuration knob is unset.
_DEFAULT_MAX_ATTEMPTS = 3
_DEFAULT_MIN_INTERVAL_MILLIS = 200
_DEFAULT_MAX_INTERVAL_MILLIS = 10_000


class IdentityServiceError(Exception):
    """Raised when identity-service authentication or a request fails.

    Carries the optional structured `code` and HTTP `status` from the
    identity-service's error response so callers can branch on them; both default
    to ``None`` for transport failures and the token-fetch path, which do not
    populate them.
    """

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        status: Optional[int] = None,
    ) -> None:
        """Initialize the error with an optional server `code` and HTTP `status`."""
        super().__init__(message)
        self.code = code
        self.status = status


@dataclass(frozen=True)
class RetryPolicy:
    """Bounded retry/backoff settings for the identity-service token fetch.

    Built by `istari_digital_client._configuration.Configuration` from
    its existing `retry_*` knobs so the token fetch reuses the same retry
    budget as the rest of the SDK.
    """

    enabled: bool = True
    max_attempts: int = _DEFAULT_MAX_ATTEMPTS
    min_interval_millis: int = _DEFAULT_MIN_INTERVAL_MILLIS
    max_interval_millis: int = _DEFAULT_MAX_INTERVAL_MILLIS
    jitter_enabled: bool = True

    @property
    def attempts(self) -> int:
        """Number of token-fetch attempts to make (always at least one)."""
        if not self.enabled:
            return 1
        return max(1, self.max_attempts)


@dataclass
class _Credentials:
    client_id: str
    key_id: str
    private_key: "EllipticCurvePrivateKey"


@dataclass
class _TokenResponse:
    access_token: str
    expires_at: datetime


def _parse_token_response(data: bytes) -> _TokenResponse:
    """Parse and validate a 2xx token-endpoint body into a `_TokenResponse`.

    Mapping every failure to `IdentityServiceError` keeps the token fetch on the
    bounded retry path in `_authenticate_with_retry`: a malformed body is
    occasionally transient (a proxy/gateway hiccup), and on a persistently
    broken server the error still surfaces once the retry budget is exhausted.

    The raw body is deliberately never echoed into the error message — a
    partially-valid response could carry a real token, and exception text
    reaches logs.

    :raises IdentityServiceError: If the body is not a JSON object, is missing a
                                 usable `access_token`, or carries a
                                 non-integer `expires_in`.
    """
    try:
        body = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise IdentityServiceError(
            "Identity-router returned a malformed (non-JSON) token response",
        ) from e

    if not isinstance(body, dict):
        raise IdentityServiceError(
            "Identity-router returned a malformed token response (not a JSON object)",
        )

    access_token = body.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise IdentityServiceError(
            "Identity-router token response is missing a usable 'access_token'",
        )

    raw_expires_in = body.get("expires_in", 3600)
    try:
        expires_in = int(raw_expires_in)
    except (TypeError, ValueError) as e:
        raise IdentityServiceError(
            "Identity-router token response has a non-integer 'expires_in'",
        ) from e

    return _TokenResponse(
        access_token=access_token,
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=expires_in),
    )


def _compute_backoff(attempt: int, policy: RetryPolicy) -> float:
    """Return seconds to sleep before the retry following `attempt` (0-indexed).

    Exponential backoff between `min_interval_millis` and
    `max_interval_millis` (`min * 2**attempt`, capped at `max`), with
    proportional jitter applied only when `policy.jitter_enabled`.
    """
    base = policy.min_interval_millis / 1000.0
    cap = policy.max_interval_millis / 1000.0
    wait = min(cap, base * (2**attempt))
    if policy.jitter_enabled:
        wait *= 1 + random.uniform(-_JITTER_FRACTION, _JITTER_FRACTION)
    return max(0.0, wait)


# --- Shared identity-service request primitives --------------------------------
#
# These back both the PAT-to-key exchange (`key_exchange`, authenticated with a
# raw Zitadel PAT) and the authenticated key-management calls (`key_registration`,
# routed through `IdentityServiceClient.request`). They are hand-written for the
# same reasons as the token fetch above: the Identity Service publishes no OpenAPI spec, and we
# need precise retry/backoff and error classification that the generated
# `call_api` machinery does not provide. The token fetch (`_authenticate`)
# deliberately keeps its own request handling — it retries every non-2xx, whereas
# these primitives treat 4xx as permanent.

_T = TypeVar("_T")

# retries=False because `_send_with_retry` does its own bounded retry/backoff;
# we don't want urllib3 to compound it.
_POOL = urllib3.PoolManager(cert_reqs=ssl.CERT_REQUIRED, retries=False)


class PrincipalKind(str, Enum):
    """Principal type, selecting the user vs. agent identity-service route.

    `AGENT` and `USER` map to the agent/user route families in `key_exchange`
    (PAT-to-key exchange) and `key_registration` (key management); the
    server derives the client id from the Zitadel `sub` (agents) or
    `preferred_username` (users) claim.
    """

    AGENT = "agent"
    USER = "user"

    @classmethod
    def from_json(cls, json_str: str) -> "PrincipalKind":
        """Create an instance of PrincipalKind from a JSON string"""
        return cls(json.loads(json_str))


class _HttpError(Exception):
    """Internal base for a classified identity-service request outcome.

    Carries the structured `code` and HTTP `status` parsed from the error body
    (both `None` for transport failures). Subclasses select how `_send_with_retry`
    reacts; they are siblings, not a hierarchy, so catching one never catches
    another.
    """

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        status: Optional[int] = None,
    ) -> None:
        """Initialize the marker with an optional server `code` and HTTP `status`."""
        super().__init__(message)
        self.code = code
        self.status = status


class _TransientHttpError(_HttpError):
    """Internal marker for a transient failure that should be retried.

    Raised for timeouts, connection failures, 5xx responses, and (by the
    caller's parse step) malformed 2xx bodies.
    """


class _UnauthorizedHttpError(_HttpError):
    """Internal marker for a 401 response.

    Drives a single forced token refresh in `_send_with_retry` when an
    `on_unauthorized` hook is supplied (the authenticated key-management path);
    callers without a hook (the PAT exchange) treat it as terminal.
    """


class _PermanentHttpError(_HttpError):
    """Internal marker for a non-retryable 4xx response."""


def _parse_error_body(data: bytes) -> tuple[Optional[str], Optional[str]]:
    """Parse the identity-service's `{error, error_description}` body.

    Returns `(code, description)`, each `None` when absent or when the body is
    not a JSON object. Never raises — a malformed error body simply yields
    `(None, None)` so the caller falls back to a status-only message.
    """
    try:
        body = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, None
    if not isinstance(body, dict):
        return None, None
    code = body.get("error")
    desc = body.get("error_description")
    return (
        code if isinstance(code, str) else None,
        desc if isinstance(desc, str) else None,
    )


def _validate_public_key_pem(
    public_key_pem: str,
    *,
    error_cls: Callable[[str], Exception] = ValueError,
) -> None:
    """Validate that `public_key_pem` is an ECDSA P-384 public key.

    Mirrors the curve check `_parse_credentials_json` does for private keys.

    :param error_cls: Exception type raised on failure; callers pass their own
                      public error type (e.g. `ExchangePatError`).
    :raises error_cls: if the PEM is unparseable or not ECDSA P-384.
    """
    # Lazy import; see module docstring.
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import load_pem_public_key

    try:
        key = load_pem_public_key(public_key_pem.encode())
    except (ValueError, TypeError) as e:
        raise error_cls(
            f"public_key_pem is not a valid PEM public key: {e}"
        ) from e
    if not isinstance(key, ec.EllipticCurvePublicKey) or not isinstance(
        key.curve, ec.SECP384R1
    ):
        raise error_cls(
            "public_key_pem must be an ECDSA P-384 (secp384r1) public key"
        )


def _send_once(
    method: str,
    url: str,
    token: str,
    *,
    body: Optional[bytes] = None,
    timeout: int = _REQUEST_TIMEOUT_SECONDS,
) -> Optional[bytes]:
    """Perform one bearer-authenticated request and return the raw 2xx body.

    Returns `None` for a 204 (or any empty 2xx body). The bearer `token` may be
    a raw Zitadel PAT (exchange) or an identity-service JWT (key management); it
    is never echoed into an error message.

    :raises _UnauthorizedHttpError: on a 401.
    :raises _TransientHttpError: on timeout, connection failure, or 5xx.
    :raises _PermanentHttpError: on any other 4xx (permanent; not retried).
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    try:
        resp = _POOL.request(
            method,
            url,
            body=body,
            headers=headers,
            timeout=urllib3.Timeout(total=timeout),
        )
    except urllib3.exceptions.TimeoutError as e:
        raise _TransientHttpError(
            f"Identity-router request timed out: {e}"
        ) from e
    except urllib3.exceptions.HTTPError as e:
        # Base urllib3 error: connection refused, DNS failure, etc.
        raise _TransientHttpError(
            f"Identity-router is unreachable at {url}: {e}"
        ) from e

    if 200 <= resp.status <= 299:
        return resp.data or None

    code, desc = _parse_error_body(resp.data)
    if code or desc:
        message = f"Identity-router request failed: HTTP {resp.status} ({code}): {desc}"
    else:
        message = f"Identity-router request failed: HTTP {resp.status}"

    if resp.status == 401:
        raise _UnauthorizedHttpError(message, code=code, status=resp.status)
    if resp.status >= 500:
        raise _TransientHttpError(message, code=code, status=resp.status)
    # 4xx (400/403/404/409 and friends) — permanent; do not retry.
    raise _PermanentHttpError(message, code=code, status=resp.status)


def _send_with_retry(
    do: Callable[[], _T],
    policy: RetryPolicy,
    error_cls: Callable[..., Exception],
    *,
    on_unauthorized: Optional[Callable[[], None]] = None,
    label: str = "Identity-router request",
) -> _T:
    """Drive `do` with bounded retry, mapping terminal failures to `error_cls`.

    `do` performs one `_send_once` plus its parse step, signalling outcomes via
    the internal `_TransientHttpError` hierarchy. Transient failures (5xx,
    connection errors, malformed bodies via the parse step) are retried with
    exponential backoff until the attempt budget is exhausted. On a 401: if
    `on_unauthorized` is supplied it is invoked once and the request retried
    immediately (this does not consume the transient-retry budget); a second 401
    — or any 401 without a hook — is terminal. `_PermanentHttpError` is terminal.

    Terminal failures are re-raised as `error_cls(message, code=..., status=...)`
    so callers surface their own public exception type carrying the server code
    and HTTP status.
    """
    attempts = policy.attempts
    refreshed_on_401 = False
    attempt = 0
    while True:
        try:
            return do()
        except _UnauthorizedHttpError as e:
            if on_unauthorized is None or refreshed_on_401:
                raise error_cls(str(e), code=e.code, status=e.status) from e
            # Cached token may have expired between fetch and use; refresh once
            # and retry before giving up.
            refreshed_on_401 = True
            on_unauthorized()
            continue
        except _PermanentHttpError as e:
            raise error_cls(str(e), code=e.code, status=e.status) from e
        except _TransientHttpError as e:
            if attempt >= attempts - 1:
                raise error_cls(str(e), code=e.code, status=e.status) from e
            backoff = _compute_backoff(attempt, policy)
            logger.warning(
                "%s attempt %d/%d failed (%s); retrying in %.2fs",
                label,
                attempt + 1,
                attempts,
                e,
                backoff,
            )
            attempt += 1
            time.sleep(backoff)


class IdentityServiceClient:
    """Authenticates with the identity-service via RFC 7523 `private_key_jwt`.

    Maintains a cached access token, refreshing it proactively before expiry
    (or on demand via `force_refresh`). Token fetches are wrapped in a bounded
    retry loop with exponential backoff so a transient identity-service outage
    does not immediately surface to callers.
    """

    def __init__(
        self,
        identity_service_url: str,
        secret: str,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> None:
        """Initialize the client.

        :param identity_service_url: Base URL of the identity-service (e.g. http://localhost:8888).
        :param secret: Either a base64-encoded JSON credentials blob, or a file
                       path to a raw JSON credentials file.
        :param retry_policy: Bounded retry/backoff settings for the token fetch.
        """
        self._identity_service_url = identity_service_url.rstrip("/")
        self._token_endpoint = self._identity_service_url + _TOKEN_ENDPOINT_PATH
        self._credentials = _load_credentials(secret)
        self._retry_policy = retry_policy or RetryPolicy()
        self._token: Optional[_TokenResponse] = None
        # retries=False because _authenticate_with_retry does its own bounded
        # retry/backoff; we don't want urllib3 to compound it.
        self._pool = urllib3.PoolManager(cert_reqs=ssl.CERT_REQUIRED, retries=False)
        # serializes _authenticate so concurrent callers share one HTTP exchange
        # and never observe a half-written self._token
        self._lock = threading.Lock()

    @property
    def identity_service_url(self) -> str:
        """The identity-service base URL this client authenticates against (no trailing slash)."""
        return self._identity_service_url

    @property
    def client_id(self) -> str:
        """The client id this client authenticates as (the JWT `sub`/`iss`)."""
        return self._credentials.client_id

    def get_token(self, force_refresh: bool = False) -> str:
        """Return a valid identity-service JWT, refreshing if needed.

        :param force_refresh: Re-authenticate even if the cached token is unexpired.
        :return: The access token string.
        :raises IdentityServiceError: If authentication fails after exhausting retries.
        """
        with self._lock:
            if force_refresh or self._token is None or self._is_expired():
                self._authenticate_with_retry()
            assert self._token is not None
            return self._token.access_token

    def invalidate(self) -> None:
        """Drop the cached token so the next `get_token()` re-authenticates."""
        with self._lock:
            self._token = None

    def request(
        self,
        method: str,
        path: str,
        parse: Callable[[Optional[bytes]], _T],
        *,
        body: Optional[bytes] = None,
        error_cls: Callable[..., Exception] = IdentityServiceError,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> _T:
        """Make an authenticated identity-service request with bounded retry.

        Injects the bearer token from `get_token()`, drives `_send_with_retry`,
        and on a 401 invalidates the cached token and retries once with a fresh
        one before surfacing the failure (the cached token may have expired
        between fetch and use). The 2xx body is handed to `parse` inside the
        retry loop, so a malformed body (which `parse` signals by raising
        `_TransientHttpError`) is retried like any other transient failure.

        :param method: HTTP method (GET/POST/DELETE/…).
        :param path: Request path relative to this client's identity-service base URL.
        :param parse: Maps the raw 2xx body (``None`` for 204) to the return
                      value; should raise `_TransientHttpError` on a malformed body.
        :param body: Optional JSON request body (already encoded to bytes).
        :param error_cls: Public exception type terminal failures are raised as;
                          must accept ``(message, *, code, status)``.
        :param retry_policy: Bounded retry/backoff; defaults to this client's
                             configured policy.
        :return: Whatever `parse` returns.
        """
        policy = retry_policy or self._retry_policy
        # Ensure proper URL joining - add leading slash if path doesn't have one
        if path and not path.startswith("/"):
            path = "/" + path
        url = self._identity_service_url.rstrip("/") + path

        def do() -> _T:
            return parse(_send_once(method, url, self.get_token(), body=body))

        return _send_with_retry(
            do,
            policy,
            error_cls,
            on_unauthorized=self.invalidate,
            label="Key operation",
        )

    def _is_expired(self) -> bool:
        """Return whether the cached token is missing or within the refresh margin."""
        if self._token is None:
            return True
        margin = timedelta(seconds=_REFRESH_MARGIN_SECONDS)
        return datetime.now(timezone.utc) >= (self._token.expires_at - margin)

    def _authenticate_with_retry(self) -> None:
        """Authenticate, retrying transient failures with exponential backoff.

        Re-raises the last `IdentityServiceError` once the configured
        attempt budget is exhausted, so a persistent outage still surfaces.
        """
        attempts = self._retry_policy.attempts
        for attempt in range(attempts):
            try:
                self._authenticate()
                return
            except IdentityServiceError as e:
                if attempt == attempts - 1:
                    raise
                backoff = _compute_backoff(attempt, self._retry_policy)
                logger.warning(
                    "Identity-router authentication attempt %d/%d failed (%s); "
                    "retrying in %.2fs",
                    attempt + 1,
                    attempts,
                    e,
                    backoff,
                )
                time.sleep(backoff)

    def _authenticate(self) -> None:
        """Perform a single token exchange and cache the result."""
        assertion = _build_client_assertion(self._credentials, self._token_endpoint)
        try:
            resp = self._pool.request(
                "POST",
                self._token_endpoint,
                fields={
                    "grant_type": "client_credentials",
                    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                    "client_assertion": assertion,
                },
                encode_multipart=False,  # send as application/x-www-form-urlencoded
                timeout=urllib3.Timeout(total=_REQUEST_TIMEOUT_SECONDS),
            )
        except urllib3.exceptions.TimeoutError as e:
            raise IdentityServiceError(
                f"Identity-router request timed out: {e}",
            ) from e
        except urllib3.exceptions.HTTPError as e:
            # Base urllib3 error: connection refused, DNS failure, max retries, etc.
            raise IdentityServiceError(
                f"Identity-router is unreachable at {self._token_endpoint}: {e}",
            ) from e

        # urllib3 does not raise on 4xx/5xx; check the status ourselves.
        if not 200 <= resp.status <= 299:
            raise IdentityServiceError(
                f"Identity-router authentication failed: HTTP {resp.status}",
            )

        self._token = _parse_token_response(resp.data)
        logger.info(
            "Authenticated with identity-service (client_id=%s, token expires at %s)",
            self._credentials.client_id,
            self._token.expires_at.isoformat(),
        )


def _get_required_str(data: dict[str, Any], field_name: str, source: str) -> str:
    """Return `data[field_name]` asserting it is a non-empty string."""
    value = data.get(field_name)
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"Identity-router credentials at {source} must contain "
            f"'{field_name}' as a non-empty string",
        )

    return value


def _parse_credentials_json(json_bytes: bytes, source: str) -> _Credentials:
    """Parse and validate Identity Service credentials from raw JSON bytes.

    :param json_bytes: The raw JSON bytes.
    :param source: Human-readable description of where the bytes came from
                   (file path or "inline secret"), used in error messages.
    :raises ValueError: If the JSON is malformed, missing required fields,
                        contains non-string field values, or carries an
                        unparseable PEM key.
    :raises TypeError: If the PEM key is not an ECDSA P-384 key.
    """
    # Lazy import; see module docstring.
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    try:
        data = json.loads(json_bytes)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(
            f"Identity-router credentials at {source} are not valid JSON: {e}",
        ) from e

    if not isinstance(data, dict):
        raise ValueError(
            f"Identity-router credentials at {source} must be a JSON object",
        )

    client_id = _get_required_str(data, "clientId", source)
    key_id = _get_required_str(data, "keyId", source)
    key_pem = _get_required_str(data, "key", source)

    try:
        private_key = load_pem_private_key(key_pem.encode(), password=None)
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Identity-router credentials at {source} have an invalid PEM key: {e}",
        ) from e

    if not isinstance(private_key, EllipticCurvePrivateKey):
        raise TypeError(
            f"Identity-router credentials at {source} key is not an ECDSA P-384 key",
        )
    if not isinstance(private_key.curve, ec.SECP384R1):
        raise TypeError(
            f"Identity-router credentials at {source} key uses curve "
            f"{private_key.curve.name}; ECDSA P-384 (secp384r1) is required",
        )

    return _Credentials(client_id=client_id, key_id=key_id, private_key=private_key)


def validate_credentials_file(file_path: Path) -> None:
    """Validate that an Identity Service credentials file is readable and well-formed.

    :raises ValueError: If the file is missing, unreadable, malformed, or contains
                        an invalid PEM key.
    :raises TypeError: If the PEM key is not an ECDSA P-384 key.
    """
    if not file_path.is_file():
        raise ValueError(
            f"Identity-router credentials file not found or not a regular file: {file_path}",
        )
    try:
        json_bytes = file_path.read_bytes()
    except OSError as e:
        raise ValueError(
            f"Cannot read identity-service credentials file at {file_path}: {e}",
        ) from e

    _parse_credentials_json(json_bytes, source=str(file_path))


def validate_inline_credentials(secret_blob: str) -> None:
    """Validate that an inline (base64-encoded JSON) Identity Service credentials secret is well-formed.

    :raises ValueError: If the blob is not valid base64, the JSON is malformed,
                        required fields are missing, or the PEM key is invalid.
    :raises TypeError: If the PEM key is not an ECDSA P-384 key.
    """
    try:
        json_bytes = base64.b64decode(secret_blob, validate=True)
    except (binascii.Error, ValueError) as e:
        raise ValueError(
            f"Identity-router inline secret is not valid base64: {e}",
        ) from e

    _parse_credentials_json(json_bytes, source="inline secret")


def _load_credentials(secret: str) -> _Credentials:
    """Load credentials from a base64 blob or a file path to raw JSON."""
    if os.path.isfile(secret):
        try:
            json_bytes = Path(secret).read_bytes()
        except OSError as e:
            raise ValueError(
                f"Cannot read identity-service credentials file at {secret}: {e}",
            ) from e
        source = secret
    else:
        try:
            json_bytes = base64.b64decode(secret, validate=True)
        except Exception as e:
            raise ValueError(
                f"Identity-router secret is not a valid file path or base64 string: {e}",
            ) from e
        source = "inline secret"

    return _parse_credentials_json(json_bytes, source=source)


def _build_client_assertion(creds: _Credentials, token_endpoint: str) -> str:
    """Build an RFC 7523 `client_assertion` JWT signed with the ECDSA P-384 key."""
    # Lazy import; see module docstring.
    import jwt

    now = int(datetime.now(timezone.utc).timestamp())
    payload = {
        "iss": creds.client_id,
        "sub": creds.client_id,
        "aud": token_endpoint,
        "exp": now + _CLIENT_ASSERTION_EXPIRATION_SECONDS,
        "iat": now,
        "jti": str(uuid.uuid4()),
    }
    headers = {"kid": creds.key_id}

    return jwt.encode(payload, creds.private_key, algorithm="ES384", headers=headers)
