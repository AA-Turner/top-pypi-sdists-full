"""Typed failures of a device-served call — never a cloud fallback, never retried.

Every error here carries a ``RetryableError`` with ``is_retryable=False`` on ``error_info``: the
executor reads it as-is (``orchestrator/executor.py`` takes an attached ``error_info`` over the
vendor classifier), so a device failure is surfaced to the person and nothing else is dispatched.

The transport's own failures (``device_offline``, ``model_not_running``, ``model_busy``,
``auth_expired``, ``stream_dropped``, ``device_invalid_request``) are classified by the transport
(L5 builder B2) with the same base class; their type names are declared here once.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.providers.errors import RetryableError

MODEL_NOT_ON_DEVICE = "model_not_on_device"
DEVICE_ROUTE_MOVE_REFUSED = "device_route_move_refused"
DEVICE_TRANSPORT_NOT_BUILT = "device_transport_not_built"
DEVICE_PIN_UNSUPPORTED = "device_pin_unsupported"
# The transport's types (providers/device/relay_transport.py, classified by classify.py).
DEVICE_OFFLINE = "device_offline"
DEVICE_TIMEOUT = "device_timeout"
MODEL_NOT_RUNNING = "model_not_running"
MODEL_BUSY = "model_busy"
AUTH_EXPIRED = "auth_expired"
DEVICE_ACCESS_DENIED = "device_access_denied"
STREAM_DROPPED = "stream_dropped"
DEVICE_INVALID_REQUEST = "device_invalid_request"
DEVICE_FAILED = "device_failed"
DEVICE_CONTEXT_TOO_SMALL = "device_context_too_small"

#: Every error type a device-served call can end with (R1). None is overload-class or retryable.
DEVICE_ERROR_TYPES: frozenset[str] = frozenset(
    {
        DEVICE_OFFLINE,
        DEVICE_TIMEOUT,
        MODEL_NOT_RUNNING,
        MODEL_BUSY,
        AUTH_EXPIRED,
        DEVICE_ACCESS_DENIED,
        STREAM_DROPPED,
        DEVICE_INVALID_REQUEST,
        DEVICE_FAILED,
        DEVICE_CONTEXT_TOO_SMALL,
        MODEL_NOT_ON_DEVICE,
        DEVICE_ROUTE_MOVE_REFUSED,
        DEVICE_TRANSPORT_NOT_BUILT,
        DEVICE_PIN_UNSUPPORTED,
    }
)


def _with_code(error_type: str, details: dict[str, Any] | None) -> dict[str, Any]:
    """``details`` with ``error``/``provider`` and ``code`` = WHY (the placement refusal code,
    the transport reason, the relay's code — else the type itself), so every consumer reads
    one key (the error event's ``details.code``)."""
    out: dict[str, Any] = {"error": error_type, "provider": "device", **(details or {})}
    if not out.get("code"):
        out["code"] = out.get("reason") or out.get("relay_code") or error_type
    return out


class DeviceRouteError(Exception):
    """Base of every device-served failure: typed, plain-worded, never retried.

    ``is_caller_refusal`` marks the PERSON'S STATE (computer off, model not running or not
    there, another model loaded, sign-in ended): an expected outcome shown to the person,
    never filed as a platform failure (no ``provider_request_failed`` row — the executor's
    caller-refusal path). A dropped stream or an unexpected device failure still files.
    """

    error_type = "device_error"
    http_status = 409
    is_caller_refusal = False

    def __init__(self, message: str, *, user_message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.user_message = user_message
        self.code = self.error_type
        self.error_info = RetryableError(
            error_type=self.error_type,
            message=message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=user_message,
            details=_with_code(self.error_type, details),
        )
        super().__init__(message)

    def envelope(self) -> dict[str, Any]:
        """The HTTP answer for a refusal decided before the stream (the same typed error_type,
        code and details the stream's error event carries)."""
        return {
            "error": self.error_type,
            "code": self.error_type,
            "error_type": self.error_type,
            "message": self.message,
            "user_message": self.user_message,
            "details": dict(self.error_info.details or {}),
        }


class ModelNotOnDeviceError(DeviceRouteError):
    """The picked device does not hold that model (or variant / own file) installed."""

    error_type = MODEL_NOT_ON_DEVICE
    http_status = 404
    is_caller_refusal = True


class DeviceRouteMoveRefusedError(DeviceRouteError):
    """Something tried to move a device run to another model or route; it is refused instead."""

    error_type = DEVICE_ROUTE_MOVE_REFUSED
    http_status = 403


class DeviceTransportNotBuiltError(DeviceRouteError):
    """The device transport is not built yet — nothing was sent anywhere."""

    error_type = DEVICE_TRANSPORT_NOT_BUILT
    http_status = 501


class DevicePinUnsupportedError(DeviceRouteError):
    """A device pin on a call that is not a chat turn (speech-to-text, extraction, media)."""

    error_type = DEVICE_PIN_UNSUPPORTED
    http_status = 400


class DeviceOfflineError(DeviceRouteError):
    """The relay answered 503: the computer is not connected (or the relay is unreachable)."""

    error_type = DEVICE_OFFLINE
    http_status = 503
    is_caller_refusal = True


class DeviceTimeoutError(DeviceRouteError):
    """No answer before the first-byte deadline (relay 504): the model never started answering."""

    error_type = DEVICE_TIMEOUT
    http_status = 504


class ModelNotRunningError(DeviceRouteError):
    """The device has no model server for this model (NOT_FOUND / RESOURCE_GONE)."""

    error_type = MODEL_NOT_RUNNING
    http_status = 404
    is_caller_refusal = True


class ModelBusyError(DeviceRouteError):
    """Another model runs on the device (RESOURCE_BUSY / CONFLICT / RATE_LIMITED)."""

    error_type = MODEL_BUSY
    http_status = 409
    is_caller_refusal = True


class DeviceAuthExpiredError(DeviceRouteError):
    """The relay refused the credential (401): the person's sign-in ended."""

    error_type = AUTH_EXPIRED
    http_status = 401
    is_caller_refusal = True


class DeviceAccessDeniedError(DeviceRouteError):
    """The relay refused this account on this device (403: not the owner, removed device)."""

    error_type = DEVICE_ACCESS_DENIED
    http_status = 403


class DeviceStreamDroppedError(DeviceRouteError):
    """The answer started and then stopped: SSE ``event: error``, a cut body, no ``[DONE]``."""

    error_type = STREAM_DROPPED
    http_status = 502


class DeviceInvalidRequestError(DeviceRouteError):
    """The device or relay refused the request itself (INVALID_PARAMS and kin)."""

    error_type = DEVICE_INVALID_REQUEST
    http_status = 400


class DeviceContextTooSmallError(DeviceRouteError):
    """llama-server refused: the request needs more tokens than the window the computer runs the
    model with (``details.needed_tokens`` / ``details.window_tokens``). The person's setting."""

    error_type = DEVICE_CONTEXT_TOO_SMALL
    http_status = 413
    is_caller_refusal = True


class DeviceFailedError(DeviceRouteError):
    """The device side failed for another reason (INTERNAL, PROTOCOL_ERROR, an unknown code)."""

    error_type = DEVICE_FAILED
    http_status = 502


__all__ = [
    "AUTH_EXPIRED",
    "DEVICE_ACCESS_DENIED",
    "DEVICE_CONTEXT_TOO_SMALL",
    "DeviceContextTooSmallError",
    "DEVICE_FAILED",
    "DEVICE_INVALID_REQUEST",
    "DEVICE_OFFLINE",
    "DEVICE_TIMEOUT",
    "MODEL_BUSY",
    "MODEL_NOT_RUNNING",
    "STREAM_DROPPED",
    "DeviceAccessDeniedError",
    "DeviceAuthExpiredError",
    "DeviceFailedError",
    "DeviceInvalidRequestError",
    "DeviceOfflineError",
    "DeviceStreamDroppedError",
    "DeviceTimeoutError",
    "ModelBusyError",
    "ModelNotRunningError",
    "DEVICE_ERROR_TYPES",
    "DEVICE_PIN_UNSUPPORTED",
    "DEVICE_ROUTE_MOVE_REFUSED",
    "DEVICE_TRANSPORT_NOT_BUILT",
    "MODEL_NOT_ON_DEVICE",
    "DevicePinUnsupportedError",
    "DeviceRouteError",
    "DeviceRouteMoveRefusedError",
    "DeviceTransportNotBuiltError",
    "ModelNotOnDeviceError",
]
