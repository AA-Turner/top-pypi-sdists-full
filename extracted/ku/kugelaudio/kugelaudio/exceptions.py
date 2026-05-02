"""Exceptions for KugelAudio SDK.

All SDK errors inherit from :class:`KugelAudioError`. Specific subclasses
map to the server's ``error_code`` field (see the server-side ``ErrorCode``
enum) so callers can ``except AuthenticationError`` without matching on
message text.

Each exception carries:

* ``message`` — human-readable, actionable text (includes how to fix when
  possible).
* ``status_code`` — HTTP status if known.
* ``error_code`` — machine-readable code mirrored from the server enum.
* ``request_id`` — correlation ID echoed by the server (when present).
* ``retry_after`` — seconds hint for 429 / 503 (when present).
"""

from __future__ import annotations

from typing import Any, Optional

# Keep in lockstep with tts/src/serving/deployments/errors.py::ErrorCode.
ERROR_CODE_UNAUTHORIZED = "UNAUTHORIZED"
ERROR_CODE_RATE_LIMITED = "RATE_LIMITED"
ERROR_CODE_INSUFFICIENT_CREDITS = "INSUFFICIENT_CREDITS"
ERROR_CODE_MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
ERROR_CODE_EMPTY_AUDIO = "EMPTY_AUDIO"
ERROR_CODE_VALIDATION = "VALIDATION_ERROR"
ERROR_CODE_INTERNAL = "INTERNAL_ERROR"
ERROR_CODE_NOT_FOUND = "NOT_FOUND"

# Server-defined WebSocket close codes.
WS_CLOSE_UNAUTHORIZED = 4001
WS_CLOSE_INSUFFICIENT_CREDITS = 4003
WS_CLOSE_RATE_LIMITED = 4029
WS_CLOSE_MODEL_UNAVAILABLE = 4500

_API_KEYS_URL = "https://app.kugelaudio.com/settings/api-keys"
_BILLING_URL = "https://app.kugelaudio.com/billing"


class KugelAudioError(Exception):
    """Base exception for KugelAudio SDK."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        request_id: Optional[str] = None,
        retry_after: Optional[int] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.request_id = request_id
        self.retry_after = retry_after
        super().__init__(self._format())

    def _format(self) -> str:
        if self.request_id:
            return f"{self.message} (request_id: {self.request_id})"
        return self.message


class AuthenticationError(KugelAudioError):
    """API key was missing, malformed, or rejected by the server."""

    def __init__(self, message: Optional[str] = None, **kw: Any) -> None:
        if message is None:
            message = (
                f"KugelAudio rejected the API key. Check it is current at "
                f"{_API_KEYS_URL}."
            )
        kw.setdefault("status_code", 401)
        kw.setdefault("error_code", ERROR_CODE_UNAUTHORIZED)
        super().__init__(message, **kw)


class RateLimitError(KugelAudioError):
    """Request was rejected by the per-org rate limiter."""

    def __init__(self, message: Optional[str] = None, **kw: Any) -> None:
        kw.setdefault("status_code", 429)
        kw.setdefault("error_code", ERROR_CODE_RATE_LIMITED)
        if message is None:
            retry = kw.get("retry_after")
            if retry:
                message = f"KugelAudio rate limit hit; retry after {retry}s."
            else:
                message = "KugelAudio rate limit hit; retry shortly."
        super().__init__(message, **kw)


class InsufficientCreditsError(KugelAudioError):
    """Account is out of TTS credits."""

    def __init__(self, message: Optional[str] = None, **kw: Any) -> None:
        if message is None:
            message = (
                f"Your KugelAudio account is out of credits. Top up at "
                f"{_BILLING_URL}."
            )
        kw.setdefault("status_code", 402)
        kw.setdefault("error_code", ERROR_CODE_INSUFFICIENT_CREDITS)
        super().__init__(message, **kw)


class ValidationError(KugelAudioError):
    """Request was rejected as invalid (bad params, missing fields, etc.)."""

    def __init__(self, message: str, **kw: Any) -> None:
        kw.setdefault("status_code", 400)
        kw.setdefault("error_code", ERROR_CODE_VALIDATION)
        super().__init__(message, **kw)


class ConnectionError(KugelAudioError):  # noqa: A001 - intentional shadow
    """The SDK could not reach KugelAudio (network error, server down,
    or model deployment temporarily unavailable)."""

    def __init__(self, message: str, **kw: Any) -> None:
        kw.setdefault("status_code", 503)
        super().__init__(message, **kw)


# ---------------------------------------------------------------------------
# Classifiers
# ---------------------------------------------------------------------------


def _build(
    status: Optional[int],
    error_code: Optional[str],
    message: str,
    *,
    request_id: Optional[str] = None,
    retry_after: Optional[int] = None,
) -> KugelAudioError:
    """Pick the right subclass for a given status/error_code pair."""
    # Only seed keys whose value we actually know. Leaving them out lets the
    # subclass's setdefault fill in the canonical value (401/402/429/... and
    # the matching error_code). `dict.setdefault` is a no-op when the key
    # exists with value None, so we must not seed `None` for status_code or
    # error_code.
    kw: dict[str, Any] = {
        "request_id": request_id,
        "retry_after": retry_after,
    }
    if status is not None:
        kw["status_code"] = status
    if error_code is not None:
        kw["error_code"] = error_code

    if error_code == ERROR_CODE_UNAUTHORIZED or status == 401:
        # Keep default actionable message when the server gave us no detail.
        auth_msg = message if message else None
        return AuthenticationError(auth_msg, **kw)
    if error_code == ERROR_CODE_INSUFFICIENT_CREDITS or status == 402:
        credits_msg = message if message else None
        return InsufficientCreditsError(credits_msg, **kw)
    if error_code == ERROR_CODE_RATE_LIMITED or status == 429:
        rl_msg = message if message else None
        return RateLimitError(rl_msg, **kw)
    if error_code == ERROR_CODE_VALIDATION or status == 400:
        return ValidationError(message or "Request validation failed.", **kw)
    if error_code == ERROR_CODE_MODEL_UNAVAILABLE or status == 503:
        detail = message or "service temporarily unavailable"
        return ConnectionError(
            f"KugelAudio is temporarily unavailable: {detail}. Retry shortly.",
            **kw,
        )
    if error_code == ERROR_CODE_NOT_FOUND or status == 404:
        return KugelAudioError(message or "Not found.", **kw)
    return KugelAudioError(message or f"HTTP {status}", **kw)


def classify_http_response(response: Any) -> KugelAudioError:
    """Build the appropriate :class:`KugelAudioError` for an httpx response.

    Reads the structured ``{error, error_code, retry_after}`` body emitted
    by the server, falls back to FastAPI's ``detail`` field, and finally
    to the raw response text.
    """
    error_code: Optional[str] = None
    message: Optional[str] = None
    retry_after: Optional[int] = None

    try:
        body = response.json()
    except Exception:
        body = None

    if isinstance(body, dict):
        error_code = body.get("error_code")
        message = body.get("error") or body.get("detail")
        if isinstance(message, list):
            message = "; ".join(str(m) for m in message)
        ra = body.get("retry_after")
        if isinstance(ra, int):
            retry_after = ra

    if retry_after is None:
        header = response.headers.get("Retry-After") or response.headers.get(
            "retry-after"
        )
        if header:
            try:
                retry_after = int(header)
            except (TypeError, ValueError):
                pass

    request_id = response.headers.get("x-request-id") or response.headers.get(
        "X-Request-Id"
    )

    if not message:
        message = (getattr(response, "text", None) or "").strip()

    return _build(
        response.status_code,
        error_code,
        message or "",
        request_id=request_id,
        retry_after=retry_after,
    )


def classify_ws_frame(data: dict) -> KugelAudioError:
    """Build a :class:`KugelAudioError` from a server-sent WebSocket
    error frame (``{error, error_code, retry_after}``)."""
    error_code = data.get("error_code")
    message = data.get("error") or "Server reported an error."
    retry_after = data.get("retry_after")
    if not isinstance(retry_after, int):
        retry_after = None
    return _build(None, error_code, message, retry_after=retry_after)


def ws_handshake_error_types(_websockets_mod: Any = None) -> tuple:
    """Return the tuple of handshake-rejection exception classes for the
    installed ``websockets`` version.

    ``websockets`` >= 14 uses ``InvalidStatus`` (with a ``.response`` attr);
    older versions use ``InvalidStatusCode`` (with a ``.status_code`` attr).
    Both may be present during the deprecation window; return everything we
    find so callers can catch all variants with one clause.

    The ``_websockets_mod`` argument is accepted for backward compatibility
    but ignored — we import ``websockets.exceptions`` explicitly because the
    v14+ lazy-imports shim does not expose it as a bare attribute.
    """
    import importlib
    import warnings

    exc_mod = importlib.import_module("websockets.exceptions")
    candidates: list = []
    # Suppress the v14+ DeprecationWarning emitted when probing the legacy
    # `InvalidStatusCode` attribute — we only read it to stay compatible.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        for name in ("InvalidStatus", "InvalidStatusCode"):
            cls = getattr(exc_mod, name, None)
            if isinstance(cls, type):
                candidates.append(cls)
    return tuple(candidates) if candidates else (Exception,)


def classify_ws_handshake_error(exc: BaseException) -> Optional[KugelAudioError]:
    """Classify a ``websockets`` handshake failure by HTTP status.

    The ``websockets`` library exposes the rejected HTTP status differently
    across versions:

    * ``websockets.exceptions.InvalidStatus`` (v14+): ``exc.response.status_code``
    * ``websockets.exceptions.InvalidStatusCode`` (pre-v14): ``exc.status_code``

    Returns a typed :class:`KugelAudioError` (``AuthenticationError`` on
    401/403, ``InsufficientCreditsError`` on 402, ``RateLimitError`` on 429,
    etc.) or ``None`` if ``exc`` is not a recognized handshake exception.

    Note: the TTS server rejects WS upgrades with a bare API key using
    HTTP 403 (not 401), so ``403`` during a WS handshake is classified as
    :class:`AuthenticationError`. In the HTTP API path, 403 keeps its
    generic semantics via :func:`classify_http_response`.
    """
    status: Optional[int] = None
    response = getattr(exc, "response", None)
    if response is not None:
        status = getattr(response, "status_code", None)
    if status is None:
        status = getattr(exc, "status_code", None)
    if not isinstance(status, int):
        return None
    if status == 403:
        return AuthenticationError()
    return _build(status, None, str(exc))


def classify_ws_close(
    code: Optional[int], reason: Optional[str] = None
) -> KugelAudioError:
    """Build a :class:`KugelAudioError` from a WebSocket close code +
    reason string."""
    reason_txt = (reason or "").strip()
    if code == WS_CLOSE_UNAUTHORIZED:
        msg = (
            "KugelAudio rejected the API key. "
            f"Check it is current at {_API_KEYS_URL}."
        )
        if reason_txt:
            msg = f"{msg} ({reason_txt})"
        return AuthenticationError(msg)
    if code == WS_CLOSE_INSUFFICIENT_CREDITS:
        return InsufficientCreditsError()
    if code == WS_CLOSE_RATE_LIMITED:
        return RateLimitError()
    if code == WS_CLOSE_MODEL_UNAVAILABLE:
        return ConnectionError(
            "KugelAudio model is temporarily unavailable. Retry shortly."
            + (f" ({reason_txt})" if reason_txt else "")
        )
    # Generic close
    detail = reason_txt or "no reason given"
    code_str = f" (code {code})" if code is not None else ""
    return ConnectionError(
        f"KugelAudio WebSocket closed by server: {detail}{code_str}."
    )
