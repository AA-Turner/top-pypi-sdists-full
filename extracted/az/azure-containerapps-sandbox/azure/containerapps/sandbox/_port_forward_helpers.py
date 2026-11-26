"""Shared validation and wire protocol for ACA Sandboxes TCP tunnels."""

from __future__ import annotations

import ipaddress
import json
import logging
import math
import re
from typing import Any
from urllib.parse import quote, urlencode, urlsplit, urlunsplit

from azure.core.exceptions import AzureError

from azure.containerapps.sandbox._helpers import SDK_MONIKER, _validate_segment


class PortForwardError(AzureError):
    """The WebSocket upgrade, TCP handshake, or port-forward stream failed."""


# WebSocket debug logs include the Authorization header and tunneled payloads.
# Keep this logger private rather than changing application logging settings.
_WIRE_LOGGER = logging.Logger(__name__, level=logging.CRITICAL + 1)
_WIRE_LOGGER.disabled = True
_WIRE_LOGGER.propagate = False

_CONTROL_CHARACTERS = re.compile(r"[\x00-\x20\x7f]")
_DNS_LABEL = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")


def _validate_timeout(value: float, name: str) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError(f"{name} must be a positive finite number of seconds.")


def _port_forward_url(
    endpoint: str,
    subscription_id: str,
    resource_group: str,
    sandbox_group: str,
    sandbox_id: str,
    api_version: str,
    port: int,
    container_name: str | None,
    *,
    connect_timeout: float,
    handshake_timeout: float,
    close_timeout: float,
) -> str:
    """Validate all inputs before obtaining a credential or opening a socket."""
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("port must be an integer between 1 and 65535.")
    for value, name in (
        (connect_timeout, "connect_timeout"),
        (handshake_timeout, "handshake_timeout"),
        (close_timeout, "close_timeout"),
    ):
        _validate_timeout(value, name)

    if not isinstance(endpoint, str) or _CONTROL_CHARACTERS.search(endpoint) or "\\" in endpoint:
        raise ValueError("endpoint must be a valid HTTPS management endpoint.")
    try:
        parsed = urlsplit(endpoint)
        hostname = parsed.hostname
        endpoint_port = parsed.port
    except ValueError as exc:
        raise ValueError("endpoint must be a valid HTTPS management endpoint.") from exc
    if (
        parsed.scheme != "https"
        or not hostname
        or hostname.rstrip(".") == "management.azure.com"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in ("", "/")
        or "?" in endpoint
        or "#" in endpoint
        or (endpoint_port is not None and not 1 <= endpoint_port <= 65535)
        or parsed.netloc.endswith(":")
    ):
        raise ValueError(
            "endpoint must be an HTTPS data-plane origin (not management.azure.com) "
            "without credentials, path, query, or fragment."
        )
    if ":" in hostname:
        if not re.fullmatch(r"\[[0-9A-Fa-f:.]+\](?::[0-9]+)?", parsed.netloc):
            raise ValueError("endpoint contains an invalid host.")
        try:
            ipaddress.IPv6Address(hostname)
        except ValueError as exc:
            raise ValueError("endpoint contains an invalid host.") from exc
    elif len(hostname) > 253 or any(
        not _DNS_LABEL.fullmatch(label) for label in hostname.rstrip(".").split(".")
    ):
        raise ValueError("endpoint contains an invalid host.")

    segments: list[str] = []
    for segment, name in (
        (subscription_id, "subscription_id"),
        (resource_group, "resource_group"),
        (sandbox_group, "sandbox_group"),
        (sandbox_id, "sandbox_id"),
    ):
        if (
            not isinstance(segment, str)
            or segment == "."
            or "%" in segment
            or any(ord(character) < 32 or ord(character) == 127 for character in segment)
        ):
            raise ValueError(f"Invalid {name}: expected a safe URL path segment.")
        _validate_segment(segment, name)
        segments.append(quote(segment, safe=""))
    if not isinstance(api_version, str) or not api_version:
        raise ValueError("api_version must be a nonempty string.")
    if container_name is not None and not isinstance(container_name, str):
        raise ValueError("container_name must be a string or None.")
    query = {"api-version": api_version}
    if container_name is not None:
        query["containerName"] = container_name
    subscription, resource, group, sandbox = segments
    path = (
        f"/subscriptions/{subscription}/resourceGroups/{resource}"
        f"/sandboxGroups/{group}/sandboxes/{sandbox}/portforward/stream"
    )
    return urlunsplit(("wss", parsed.netloc, path, urlencode(query, quote_via=quote), ""))


def _connection_options(
    token: str,
    *,
    connect_timeout: float,
    close_timeout: float,
) -> dict[str, Any]:
    return {
        "additional_headers": {"Authorization": f"Bearer {token}"},
        "user_agent_header": SDK_MONIKER,
        "open_timeout": connect_timeout,
        "close_timeout": close_timeout,
        "compression": None,
        "max_size": 1024 * 1024,
        "max_queue": 16,
        "logger": _WIRE_LOGGER,
    }


def _start_message(port: int) -> str:
    return json.dumps({"type": "start", "port": port}, separators=(",", ":"))


def _check_control_message(message: str | bytes, *, handshake: bool) -> None:
    if not isinstance(message, str):
        raise PortForwardError("Expected a JSON text connected response, received binary data.")
    try:
        payload = json.loads(message)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise PortForwardError("Invalid JSON in port-forward response.") from exc
    if not isinstance(payload, dict):
        raise PortForwardError("Port-forward response must be a JSON object.")
    if payload.get("type") == "error":
        detail = payload.get("data")
        if not isinstance(detail, str):
            raise PortForwardError("Malformed port-forward error response.")
        raise PortForwardError(f"Port-forward server error: {detail}")
    if handshake and payload.get("type") == "connected":
        return
    raise PortForwardError("Unexpected port-forward control response.")


def _binary_payload(data: bytes | bytearray | memoryview) -> bytes:
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("Port-forward writes require bytes, bytearray, or memoryview.")
    return bytes(data)
