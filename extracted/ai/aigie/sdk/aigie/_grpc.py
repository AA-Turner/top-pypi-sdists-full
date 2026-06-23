"""Shared gRPC plumbing used by ``autonomous.control_plane`` and ``ingest``.

Kept deliberately small: only logic that is genuinely duplicated between the
sync (control_plane) and async (ingest) clients lives here.
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

import grpc

# Default port for the gRPC services (ingest gateway + control plane).
_DEFAULT_GRPC_PORT = 50051


def split_host_port(endpoint: str) -> tuple[str, int | None]:
    """Parse an endpoint into ``(host, port_or_None)``.

    Accepts:
      - ``host``                         → (host, None)
      - ``host:port``                    → (host, port)
      - ``scheme://host[:port][/path]``  → (host, port_or_None)
    """
    if "://" in endpoint:
        parsed = urlparse(endpoint)
        return parsed.hostname or "", parsed.port
    host, sep, port_str = endpoint.split("/", 1)[0].partition(":")
    if not sep or not port_str:
        return host, None
    try:
        return host, int(port_str)
    except ValueError:
        return host, None


def grpc_uses_tls(endpoint: str) -> bool:
    """Whether gRPC should use TLS for ``endpoint``.

    An ``https`` platform URL means the SDK reaches the platform through a
    TLS front (e.g. an ALB on :443) rather than the in-cluster plaintext gRPC
    port. In that case gRPC rides the same TLS endpoint and the front
    path-routes the gRPC service to the in-cluster gRPC port.

    URL schemes are case-insensitive (RFC 3986), so this normalizes via
    ``urlparse`` rather than matching a literal ``https://`` prefix.
    """
    return "://" in endpoint and urlparse(endpoint).scheme == "https"


def data_path_grpc_target(endpoint: str, *, default_port: int = _DEFAULT_GRPC_PORT) -> str:
    """gRPC ``host:port`` target for a data-path client (ingest, decision).

    The SDK is configured with an HTTP-style platform URL; the gRPC target is
    derived from its scheme:

    - ``https://host[/path]``  → the URL's ``host:port`` (default **:443**). The
      SDK reaches the platform through a TLS front (e.g. an ALB on :443) that
      path-routes ``/<package>.<Service>/*`` to the in-cluster gRPC port.
    - ``http://host:8000/api`` → the fixed in-cluster ``default_port``. The HTTP
      URL port is the gateway's REST port, so it is never reused for gRPC.

    Returns an empty string when no host can be parsed.
    """
    host, port = split_host_port(endpoint)
    if not host:
        return ""
    if grpc_uses_tls(endpoint):
        return f"{host}:{port or 443}"
    return f"{host}:{default_port}"


def control_plane_grpc_target(endpoint: str) -> str:
    """gRPC ``host:port`` target for the control-plane client (always plaintext).

    Unlike the data path, the control plane may be addressed directly, so:

    - a bare ``host:port`` (no scheme) trusts the given port;
    - otherwise the gRPC port comes from ``AIGIE_GRPC_PORT`` (default
      :data:`_DEFAULT_GRPC_PORT`).

    Returns an empty string when no host can be parsed.
    """
    host, port = split_host_port(endpoint)
    if not host:
        return ""
    if "://" not in endpoint and port:
        return f"{host}:{port}"
    return f"{host}:{int(os.environ.get('AIGIE_GRPC_PORT', _DEFAULT_GRPC_PORT))}"


# Default port for the Decision Orchestrator's EvaluateSpan service
# (Determine Error MVP) — a sibling container in the agent pod, same host as
# the ingest gateway, its own port.
_DEFAULT_DECISION_GRPC_PORT = 50052


def grpc_is_unreachable(error: BaseException) -> bool:
    """Whether a gRPC error means the server could not be reached.

    ``UNAVAILABLE`` (channel can't connect / TLS handshake / route down) and
    ``DEADLINE_EXCEEDED`` (no response in time) indicate a connectivity problem
    worth an actionable warning, as opposed to a server-side rejection.
    """
    code = getattr(error, "code", None)
    status = code() if callable(code) else None
    return status in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED)


def unreachable_hint(*, use_tls: bool, plaintext_port: int) -> str:
    """One-line, actionable hint for a 'cannot reach <service>' warning.

    Names the expected wire path so the operator can check the right thing:
    a TLS front for ``https`` URLs, or the in-cluster plaintext port for
    ``http`` URLs.
    """
    if use_tls:
        return (
            "platform reached over TLS (an https KYTTE_URL routes gRPC to :443 via the "
            "load balancer) — check KYTTE_URL and that the gRPC route/ALB is healthy"
        )
    return (
        f"platform reached in-cluster (an http KYTTE_URL uses plaintext gRPC on :{plaintext_port}) "
        "— check KYTTE_URL and that the gateway is reachable"
    )
