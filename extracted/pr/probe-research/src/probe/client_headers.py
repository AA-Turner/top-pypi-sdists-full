"""Small, fail-open client-version header contract.

These headers are telemetry, never identity or authorization.  Keeping their
validation here gives the CLI sender and hosted MCP receiver the same bounded
wire shape without teaching the generic SDK that it is always a CLI.
"""

from __future__ import annotations

import contextvars
import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager

CLIENT_KIND_HEADER = "X-Probe-Client"
CLIENT_VERSION_HEADER = "X-Probe-Client-Version"
#: The MACHINE this request came from. Telemetry-shaped like the two above and
#: subject to the same rule: it is never identity for AUTHORIZATION, only for
#: attribution. The server matches it inside the already-authenticated user and
#: team, so a forged value selects one of the caller's own devices or nothing.
DEVICE_HEADER = "X-Probe-Device"

#: Mirrors the server's `parse_device_instance_id` and the CHECK constraints in
#: control/028 and experiment/0182. All four must agree, or a value this sends is
#: accepted by one layer and rejected by another.
_DEVICE_INSTANCE_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


def device_headers(device_instance_id: object) -> dict[str, str]:
    """A validated device header, or nothing at all.

    Same posture as `client_version_headers`: malformed input produces NO header
    rather than a rejected request. A machine whose identity file is unreadable
    still works, it just reports as a client that predates device identity.
    """
    if not isinstance(device_instance_id, str):
        return {}
    if not _DEVICE_INSTANCE_RE.fullmatch(device_instance_id):
        return {}
    return {DEVICE_HEADER: device_instance_id}

#: Must stay in step with `app/client_version/models.py::ClientKind` and the
#: database CHECK on `client_version_observations.client_kind`. A kind sent from
#: here that the server has not learned yet is rejected by that CHECK -- and one
#: the DASHBOARD has not learned is dropped by its parser with no error at all,
#: so the version simply never appears. Server and dashboard first, sender last.
#:
#: `sdk` reports the SAME number as `cli` -- both ship in the one `probe-research`
#: distribution -- and is a separate kind only so the surface is legible: a
#: training script that never opens a terminal is exactly the install a CLI-shaped
#: view of the fleet cannot see.
_CLIENT_KINDS = frozenset({"cli", "plugin", "sdk", "tap"})
_MAX_VERSION_LENGTH = 64
_VERSION_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def client_version_headers(kind: object, version: object) -> dict[str, str]:
    """Return a validated kind/version pair, or no telemetry on malformed input.

    The backend compares strict SemVer, so PEP 440-only forms such as
    ``0.8.0rc1`` and the source-tree fallback ``0.0.0.dev0`` intentionally
    produce no telemetry. Whitespace, control characters, header delimiters,
    and unbounded values are rejected rather than normalized.
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


# Per-request override for the client identity on outbound backend requests.
#
# It exists for ONE case: the hosted MCP. `_client_for_token` is shared by the
# local (stdio) server and the hosted one, and its Transport is memoized per
# token, so the version fixed at construction is this PROCESS's package version.
# That is the right answer locally -- the stdio server IS the user's install --
# and the wrong one when hosted, where it would report OUR deployed version as
# every caller's client version and make the whole fleet look evenly upgraded.
#
# So: unset (the default) means "no override, use what the Transport was built
# with". An EMPTY mapping is a real value and means "this caller reported
# nothing", which is why the type is `| None` and not just a dict -- the hosted
# wrapper must be able to say "no telemetry" without falling back to ours.
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
