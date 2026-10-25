"""Every relay answer a device-served call can end with, as ONE typed device error.

The relay's ``POST /v1/devices/D/stream`` (matrx-desktop ``relay/src/stream-sink.ts``) answers:

* BEFORE the device's response — an HTTP status with the ``RelayCallResponse`` JSON
  ``{"ok": false, "error": {"code", "message", "retryable", "data"?: {"reason"}}}``: 503 offline,
  504 first-byte timeout, 401/403 auth, 404 ``NOT_FOUND``, 409 ``RESOURCE_BUSY``, 400
  ``INVALID_PARAMS``, 502 otherwise (``RESOURCE_GONE``, ``INTERNAL``…). The openai SDK raises
  ``APIStatusError`` with that body.
* AFTER it, on a ``text/event-stream`` body — one ``event: error`` block,
  ``{"error": {"type": "device_stream_error", "code", "message"}}``. The SDK raises ``APIError``
  with ``body = that error``.
* A body that is cut, idles past the deadline or ends without ``[DONE]`` — the transport raises
  :class:`~matrx_ai.providers.device.errors.DeviceStreamDroppedError` itself.

Every result is a :class:`~matrx_ai.providers.device.errors.DeviceRouteError` subclass with
``is_retryable=False`` and a device ``error_type`` (never ``server_error`` / overload): a device
run is never re-sent and never moved anywhere else (``route_guard.py``).
"""

from __future__ import annotations

import re
from typing import Any

from matrx_ai.providers.device.errors import (
    DeviceAccessDeniedError,
    DeviceAuthExpiredError,
    DeviceContextTooSmallError,
    DeviceFailedError,
    DeviceInvalidRequestError,
    DeviceOfflineError,
    DeviceRouteError,
    DeviceStreamDroppedError,
    DeviceTimeoutError,
    ModelBusyError,
    ModelNotRunningError,
)
from matrx_ai.providers.errors import RetryableError

#: Plain sentences per type (the condition, never an action in progress).
USER_MESSAGES: dict[type[DeviceRouteError], str] = {
    DeviceOfflineError: "Your computer isn't connected right now. Open Matrx 2 on it and try again.",
    DeviceTimeoutError: "The model on your computer didn't start answering in time.",
    ModelNotRunningError: "That model isn't running on your computer. Start it in Matrx 2 › Models.",
    ModelBusyError: "Your computer is busy with another chat right now.",
    DeviceAuthExpiredError: "Your sign-in ended before your computer could answer. Sign in again.",
    DeviceAccessDeniedError: "This account can't use models on that computer.",
    DeviceStreamDroppedError: "The answer from your computer stopped part way.",
    DeviceInvalidRequestError: "The model on your computer couldn't accept this request.",
    DeviceFailedError: "The model on your computer ran into a problem.",
    DeviceContextTooSmallError: (
        "This chat needs more tokens than your computer runs this model with. "
        "Raise it in Matrx 2 › Models › This computer › Options… › Context window."
    ),
}

#: Device codes whose own message is written for people (core/capabilities/python/llm-chat.ts).
_DEVICE_WORDED: frozenset[type[DeviceRouteError]] = frozenset(
    {ModelNotRunningError, ModelBusyError}
)

_CODE_TO_ERROR: dict[str, type[DeviceRouteError]] = {
    "DEVICE_OFFLINE": DeviceOfflineError,
    "TIMEOUT": DeviceTimeoutError,
    "NOT_FOUND": ModelNotRunningError,
    "RESOURCE_GONE": ModelNotRunningError,
    "RESOURCE_BUSY": ModelBusyError,
    "CONFLICT": ModelBusyError,
    "RATE_LIMITED": ModelBusyError,
    "AUTH_REQUIRED": DeviceAuthExpiredError,
    "AUTH_INVALID": DeviceAuthExpiredError,
    "AUTH_EXPIRED": DeviceAuthExpiredError,
    "AUTH_FORBIDDEN": DeviceAccessDeniedError,
    "AUTH_DEVICE_REVOKED": DeviceAccessDeniedError,
    "PERMISSION_DENIED_OS": DeviceAccessDeniedError,
    "INVALID_PARAMS": DeviceInvalidRequestError,
    "UNKNOWN_OPERATION": DeviceInvalidRequestError,
    "PROTOCOL_VERSION_UNSUPPORTED": DeviceInvalidRequestError,
    "PAYLOAD_TOO_LARGE": DeviceInvalidRequestError,
    "PLATFORM_UNSUPPORTED": DeviceInvalidRequestError,
}

_STATUS_TO_ERROR: dict[int, type[DeviceRouteError]] = {
    503: DeviceOfflineError,
    504: DeviceTimeoutError,
    401: DeviceAuthExpiredError,
    403: DeviceAccessDeniedError,
    404: ModelNotRunningError,
    409: ModelBusyError,
    429: ModelBusyError,
    400: DeviceInvalidRequestError,
    413: DeviceInvalidRequestError,
    501: DeviceInvalidRequestError,
}


def make_device_error(
    cls: type[DeviceRouteError],
    message: str,
    *,
    device_message: str | None = None,
    details: dict[str, Any] | None = None,
) -> DeviceRouteError:
    """One typed device error with its plain ``user_message``."""
    user_message = USER_MESSAGES[cls]
    if cls in _DEVICE_WORDED and device_message:
        user_message = device_message[:300]
    return cls(message, user_message=user_message, details=details)


def _busy_chat_name(data: dict[str, Any]) -> str | None:
    """The chat a busy device names (its error ``data``), or None."""
    value = data.get("chat_title")  # the ONE name: apps/shared/desktop-protocol/fixtures/device-model-contract.json
    return value.strip()[:120] if isinstance(value, str) and value.strip() else None


#: llama-server's own refusal: "request (9851 tokens) exceeds the available context size (4096
#: tokens)" — carried verbatim in the device's INVALID_PARAMS message or the SSE error block.
_CONTEXT_TOO_SMALL = re.compile(
    r"request \((\d+) tokens\) exceeds the available context size \((\d+) tokens\)", re.I
)


def context_too_small(message: str) -> DeviceRouteError | None:
    """llama's context refusal in ``message`` as the typed error (N needed, W window), or None."""
    match = _CONTEXT_TOO_SMALL.search(message or "")
    if match is None:
        return None
    needed, window = int(match.group(1)), int(match.group(2))
    return DeviceContextTooSmallError(
        f"the device's model window is {window} tokens; the request needs {needed}: {message[:300]}",
        user_message=(
            f"This chat needs about {needed} tokens; your computer runs this model with a "
            f"{window}-token window. Raise it in Matrx 2 › Models › This computer › Options… › Context window."
        ),
        details={"needed_tokens": needed, "window_tokens": window, "reason": "context_too_small"},
    )


def _relay_error_body(body: Any) -> dict[str, Any]:
    """The protocol error inside a relay answer (``{"ok": false, "error": {...}}``) or an SSE
    error block's ``error`` object; ``{}`` when neither."""
    if isinstance(body, dict):
        inner = body.get("error")
        if isinstance(inner, dict):
            return inner
        if "code" in body:
            return body
    return {}


def _typed_in_chain(exc: BaseException) -> DeviceRouteError | None:
    """A typed device error raised by the transport (the openai SDK wraps a transport exception
    in ``APIConnectionError``; the original rides ``__cause__``)."""
    seen: set[int] = set()
    cur: BaseException | None = exc
    while cur is not None and id(cur) not in seen:
        if isinstance(cur, DeviceRouteError):
            return cur
        seen.add(id(cur))
        cur = cur.__cause__ or cur.__context__
    return None


def device_error_for(exc: BaseException) -> DeviceRouteError:
    """``exc`` (anything a device call raised) as ONE typed device error."""
    typed = _typed_in_chain(exc)
    if typed is not None:
        return typed

    import openai

    if isinstance(exc, openai.APIStatusError):
        status = int(exc.status_code)
        err = _relay_error_body(exc.body)
        code = str(err.get("code") or "")
        relay_message = str(err.get("message") or "")
        data = err.get("data") if isinstance(err.get("data"), dict) else {}
        too_small = context_too_small(relay_message)
        if too_small is not None:
            return too_small
        cls = _STATUS_TO_ERROR.get(status) or _CODE_TO_ERROR.get(code) or DeviceFailedError
        # A device error before the response: its code decides when the status is the
        # catch-all 502 (RESOURCE_GONE → model_not_running) or 503 is not DEVICE_OFFLINE.
        if code in _CODE_TO_ERROR and status in (200, 502):
            cls = _CODE_TO_ERROR[code]
        details: dict[str, Any] = {
            "relay_status": status,
            "relay_code": code or None,
            "reason": (data or {}).get("reason"),
            "phase": "before_response",
        }
        device_message = relay_message
        if cls is ModelBusyError:
            # RESOURCE_BUSY means "busy with another chat" (the device switches an idle
            # model itself under start_if_stopped); the device names that chat.
            busy_with = _busy_chat_name(data or {})
            details["busy_with"] = busy_with
            details["device_message"] = relay_message or None
            if not relay_message and busy_with:
                device_message = f"Your computer is busy with another chat ({busy_with})."
        return make_device_error(
            cls,
            f"relay answered {status} {code or '-'}: {relay_message or exc.message}",
            device_message=device_message,
            details=details,
        )

    if isinstance(exc, openai.APITimeoutError):
        return make_device_error(DeviceTimeoutError, f"relay hop timed out: {exc}")
    if isinstance(exc, openai.APIConnectionError):
        return make_device_error(
            DeviceOfflineError,
            f"the relay could not be reached: {exc}",
            details={"reason": "relay_unreachable"},
        )
    if isinstance(exc, openai.APIError):
        # No status: an SSE ``event: error`` block after content started (stream-sink.ts).
        err = _relay_error_body(exc.body)
        code = str(err.get("code") or getattr(exc, "code", None) or "")
        too_small = context_too_small(str(err.get("message") or exc.message or ""))
        if too_small is not None:
            return too_small
        return make_device_error(
            DeviceStreamDroppedError,
            f"the device stream ended with an error after it started: {code or '-'}: "
            f"{err.get('message') or exc.message}",
            details={
                "relay_code": code or None,
                "error_kind": err.get("type"),
                "phase": "mid_stream",
            },
        )

    import httpx

    if isinstance(exc, httpx.TimeoutException):
        return make_device_error(DeviceTimeoutError, f"relay hop timed out: {type(exc).__name__}")
    if isinstance(exc, httpx.ConnectError):
        return make_device_error(
            DeviceOfflineError,
            f"the relay could not be reached: {type(exc).__name__}: {exc}",
            details={"reason": "relay_unreachable"},
        )
    if isinstance(exc, httpx.TransportError):
        return make_device_error(
            DeviceStreamDroppedError, f"the relay hop broke: {type(exc).__name__}: {exc}"
        )
    return make_device_error(DeviceFailedError, f"device call failed: {type(exc).__name__}: {exc}")


def classify_device_error(exception: Exception) -> RetryableError:
    """The ``_PROVIDER_CLASSIFIERS["device"]`` entry: never retryable, never overload-class."""
    return device_error_for(exception).error_info


__all__ = ["USER_MESSAGES", "classify_device_error", "device_error_for", "make_device_error"]
