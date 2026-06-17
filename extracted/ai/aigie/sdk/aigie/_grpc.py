"""Shared gRPC plumbing used by ``autonomous.control_plane`` and ``ingest``.

Kept deliberately small: only logic that is genuinely duplicated between the
sync (control_plane) and async (ingest) clients lives here.
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

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


def derive_grpc_target(endpoint: str, *, honor_url_port: bool, honor_env_port: bool) -> str:
    """Convert an HTTP-style platform endpoint to a gRPC ``host:port`` target.

    The SDK is configured with an HTTP API endpoint (e.g.
    ``http://kytte-agent:8000/api``). A scheme means the URL port is HTTP's, so
    it is never reused as the gRPC port.

    - ``honor_url_port``: for a bare ``host:port`` input (no scheme), trust the
      given port instead of substituting the gRPC port. The control-plane
      client wants this; the ingest path does not (it always uses the fixed
      in-cluster port).
    - ``honor_env_port``: take the gRPC port from ``AIGIE_GRPC_PORT`` (default
      :data:`_DEFAULT_GRPC_PORT`) rather than the fixed default.

    Returns an empty string when no host can be parsed.
    """
    grpc_port = _DEFAULT_GRPC_PORT
    if honor_env_port:
        grpc_port = int(os.environ.get("AIGIE_GRPC_PORT", _DEFAULT_GRPC_PORT))
    host, port = split_host_port(endpoint)
    if not host:
        return ""
    if honor_url_port and "://" not in endpoint and port:
        return f"{host}:{port}"
    return f"{host}:{grpc_port}"


# Default port for the Decision Orchestrator's EvaluateSpan service
# (Determine Error MVP) — a sibling container in the agent pod, same host as
# the ingest gateway, its own port.
_DEFAULT_DECISION_GRPC_PORT = 50052
