"""The fail-open client kind, version and device headers: telemetry, never authorization identity.

One bounded wire shape for the CLI sender and the hosted MCP receiver.
"""

from __future__ import annotations

import contextvars
import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager

CLIENT_KIND_HEADER = "X-Probe-Client"
CLIENT_VERSION_HEADER = "X-Probe-Client-Version"
#: The MACHINE a request came from: attribution only, never authorization. Matched inside the
#: authenticated user and team, so a forged value picks one of the caller's own devices or nothing.
DEVICE_HEADER = "X-Probe-Device"

#: Mirrors the server's `parse_device_instance_id` and the CHECKs in control/028 and
#: experiment/0182: all four must agree, or one layer rejects what another accepts.
_DEVICE_INSTANCE_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


def device_headers(device_instance_id: object) -> dict[str, str]:
    """A validated device header, or none: malformed input sends NO header, never a rejected
    request (an unreadable identity file reads as a client predating device identity)."""
    if not isinstance(device_instance_id, str):
        return {}
    if not _DEVICE_INSTANCE_RE.fullmatch(device_instance_id):
        return {}
    return {DEVICE_HEADER: device_instance_id}

#: Add a kind to the server (`app/client_version/models.py::ClientKind`, the CHECK on
#: `client_version_observations.client_kind`) and dashboard first, here last. DESIGN.md.
_CLIENT_KINDS = frozenset({"cli", "plugin", "sdk", "tap"})
_MAX_VERSION_LENGTH = 64
_VERSION_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def client_version_headers(kind: object, version: object) -> dict[str, str]:
    """A validated kind/version pair, or none on malformed input. Strict SemVer, as the backend
    compares: PEP 440-only ``0.8.0rc1`` and the source-tree ``0.0.0.dev0`` send nothing; whitespace,
    control characters, header delimiters and unbounded values are rejected, never normalized.
    """

    if (
        not isinstance(kind, str)
        or kind not in _CLIENT_KINDS
        or not isinstance(version, str)
    ):
        return {}
    if not 1 <= len(version) <= _MAX_VERSION_LENGTH:
        return {}
    match = _VERSION_RE.fullmatch(version)
    if match is None:
        return {}
    prerelease = match.group(4)
    if prerelease is not None and any(
        identifier.isdigit()
        and len(identifier) > 1
        and identifier.startswith("0")
        for identifier in prerelease.split(".")
    ):
        return {}
    return {
        CLIENT_KIND_HEADER: kind,
        CLIENT_VERSION_HEADER: version,
    }


# Per-request client-identity override, for the hosted MCP only (DESIGN.md (request_identity.py)).
# None: use the Transport's own; an EMPTY dict: this caller reported nothing (no fallback to ours).
_outbound_client_headers: contextvars.ContextVar[dict[str, str] | None] = contextvars.ContextVar(
    "probe_outbound_client_headers", default=None
)


def current_client_headers() -> dict[str, str] | None:
    """The per-request client-identity override, or None when unset."""
    return _outbound_client_headers.get()


@contextmanager
def client_headers_scope(headers: Mapping[str, str] | None) -> Iterator[None]:
    """Bind ``headers`` as the outbound client identity for the duration of the block.

    Scoped to the calling context, so concurrent requests in the hosted server
    never see each other's caller version.
    """
    token = _outbound_client_headers.set(None if headers is None else dict(headers))
    try:
        yield
    finally:
        _outbound_client_headers.reset(token)
