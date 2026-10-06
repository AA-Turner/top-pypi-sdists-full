"""Identity API version routing and the warn-once notice for the /api/v1 key operations.

Each operation takes ``api_version``, an `IdentityApiVersion` member or its string.
``"auto"``, the default, uses identity-service's v2 API when the identity API version
in force is ``v2`` and v2 can address the call, and the deprecated v1 routes
otherwise. ``"v1"`` and ``"v2"`` force a route; ``"v2"`` raises ``ConfigurationError``
before any request for a call with no v2 form. A call that reaches a v1 route warns
once per process.
"""

from __future__ import annotations

import os
import sys
import threading
import warnings
from types import FrameType

from istari_digital_client.sdk._identity.auth.identity_service import (
    IdentityApiVersion,
    IdentityServiceClient,
    identity_api_version_message,
)

_warned: set[str] = set()
_lock = threading.Lock()


def _configuration_error() -> type[ValueError]:
    """The ``ConfigurationError`` of this tree, imported late to avoid an import cycle."""
    from istari_digital_client.sdk._configuration import ConfigurationError

    return ConfigurationError


def normalize_api_version(api_version: object) -> IdentityApiVersion:
    """Return ``api_version`` as an `IdentityApiVersion`, reading ``None`` as ``AUTO``.

    :raises ConfigurationError: If the value is not a member or its string.
    """
    if api_version is None:
        return IdentityApiVersion.AUTO
    message = f"api_version must be 'auto', 'v1' or 'v2', got {api_version!r}"
    if not isinstance(api_version, str):
        raise _configuration_error()(message)
    try:
        return IdentityApiVersion(api_version)
    except ValueError:
        raise _configuration_error()(message) from None


def configured_api_version(
    client: IdentityServiceClient | None = None,
) -> IdentityApiVersion:
    """Return the identity API version in force for a call that leaves the choice to ``"auto"``.

    The version the identity-service ``client`` uses (settling an ``"auto"`` client),
    else ``ISTARI_IDENTITY_API_VERSION``, with ``"auto"`` or nothing reading as ``"v2"``.

    :raises ConfigurationError: If the resolved value is neither ``"v1"`` nor ``"v2"``.
    """
    version = getattr(client, "api_version", None) if client is not None else None
    if version is None:
        version = os.environ.get("ISTARI_IDENTITY_API_VERSION") or IdentityApiVersion.AUTO
    try:
        resolved = IdentityApiVersion(version)
    except ValueError:
        raise _configuration_error()(identity_api_version_message(version)) from None
    return IdentityApiVersion.V2 if resolved is IdentityApiVersion.AUTO else resolved


def no_v2_form_message(operation: str, reason: str) -> str:
    """The error text for ``api_version="v2"`` on a call identity-service v2 cannot express."""
    return (
        f"{operation} {reason}; pass api_version='auto' or 'v1' "
        "to use the deprecated identity-service /api/v1 routes"
    )


def warn_v1(operation: str, replacement: str | None) -> None:
    """Warn once per process that ``operation`` used a v1 route, naming its v2 ``replacement``."""
    with _lock:
        first = operation not in _warned
        _warned.add(operation)
    if not first:
        return
    # Point at the caller outside this package; default filters show it when that is __main__.
    stacklevel = 1
    frame: FrameType | None = sys._getframe(0)
    while frame is not None and frame.f_globals.get("__name__", "").startswith(
        "istari_digital_client."
    ):
        stacklevel, frame = stacklevel + 1, frame.f_back
    advice = (
        f"use {replacement} instead"
        if replacement
        else "identity-service has no v2 equivalent"
    )
    warnings.warn(
        f"{operation} calls the frozen /api/v1 identity-service routes, "
        f"which are scheduled for removal; {advice}",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def reset_deprecation_warnings() -> None:
    """Forget which operations have warned. For tests."""
    with _lock:
        _warned.clear()
