"""Typed exceptions for use.computer SDK errors that callers should catch by class
rather than by parsing HTTP status codes or response bodies."""

from __future__ import annotations

import httpx


class UseComputerError(Exception):
    """Base class for typed use.computer SDK errors."""


class PlatformNotSupportedError(UseComputerError):
    """Raised when an action is not supported on the sandbox's platform."""

    def __init__(
        self,
        action: str,
        sandbox_type: str,
        hint: str,
        response: httpx.Response | None = None,
    ):
        self.action = action
        self.sandbox_type = sandbox_type
        self.hint = hint
        self.response = response
        super().__init__(f"{action} not supported on {sandbox_type} sandbox: {hint}")


class BillingRequiredError(UseComputerError):
    """Raised when a billable sandbox launch needs prepaid credits."""

    def __init__(self, message: str, response: httpx.Response | None = None):
        self.message = message
        self.response = response
        super().__init__(message or "Add credits to launch this sandbox")


class ReservationRequiredError(UseComputerError):
    """Raised when a macOS launch needs an active Mac Mini reservation."""

    def __init__(self, message: str, response: httpx.Response | None = None):
        self.message = message
        self.response = response
        super().__init__(message or "macOS requires an active Mac Mini reservation")


def _typed_error_from_response(resp: httpx.Response) -> UseComputerError | None:
    try:
        data = resp.json()
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    error_code = data.get("error")
    message = str(data.get("message") or error_code or "")
    if resp.status_code == 402 and error_code == "billing_required":
        return BillingRequiredError(message=message, response=resp)
    if resp.status_code == 409 and error_code == "macos_reservation_required":
        return ReservationRequiredError(message=message, response=resp)
    return None


def _raise_if_unsupported(resp: httpx.Response) -> None:
    """httpx event hook: convert stable gateway error JSON into typed errors.

    httpx hooks run before the body is read on streaming responses, so we
    only touch the body for statuses we own — anything else is left
    untouched for raise_for_status() to handle normally.
    """
    if resp.status_code not in (402, 409):
        return
    try:
        resp.read()
    except Exception:
        return
    err = _typed_error_from_response(resp)
    if err is not None:
        raise err


async def _araise_if_unsupported(resp: httpx.Response) -> None:
    if resp.status_code not in (402, 409):
        return
    try:
        await resp.aread()
    except Exception:
        return
    err = _typed_error_from_response(resp)
    if err is not None:
        raise err
