"""Trusted-proxy client IP resolution with CIDR-based trust model.

When ``TrustedProxyConfig.enabled`` is ``True`` and the socket peer is
within a configured CIDR range, the resolver walks the forwarded-header
chain right-to-left and returns the first IP **not** in the trusted set.

Fail-closed by design:
- Disabled config or empty CIDRs -> socket peer (backward compatible)
- Untrusted socket peer -> socket peer (XFF ignored entirely)
- Malformed IP in chain -> socket peer
- All-trusted chain -> leftmost entry (or socket peer if empty)
"""

from __future__ import annotations

import ipaddress
import logging
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from starlette.requests import Request

    from anteroom.config import TrustedProxyConfig

logger = logging.getLogger(__name__)

# Module-level cache: maps frozenset of CIDR strings to parsed networks.
_cidr_cache: dict[frozenset[str], list[ipaddress.IPv4Network | ipaddress.IPv6Network]] = {}


def _parse_cidrs(
    cidrs: Sequence[str],
) -> list[ipaddress.IPv4Network | ipaddress.IPv6Network]:
    """Parse CIDR strings into network objects, using a module-level cache."""
    key = frozenset(cidrs)
    if key in _cidr_cache:
        return _cidr_cache[key]
    networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
    for entry in cidrs:
        try:
            networks.append(ipaddress.ip_network(entry, strict=False))
        except ValueError:
            logger.warning("Invalid trusted CIDR entry: %s -- skipping", entry)
    _cidr_cache[key] = networks
    return networks


def _is_valid_ip(ip_str: str) -> bool:
    """Return True if *ip_str* is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def _is_trusted(
    ip_str: str,
    networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network],
) -> bool:
    """Return True if *ip_str* falls within any of the *networks*."""
    try:
        addr = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return any(addr in net for net in networks)


def resolve_client_ip(request: Request, config: TrustedProxyConfig | None) -> str:
    """Resolve the real client IP, respecting trusted-proxy configuration.

    Parameters
    ----------
    request:
        The incoming Starlette/FastAPI request.
    config:
        The ``TrustedProxyConfig`` from ``AppConfig``.  ``None`` is safe
        and equivalent to disabled.

    Returns
    -------
    str
        The resolved client IP address.
    """
    socket_ip: str = request.client.host if request.client else "unknown"

    if config is None or not config.enabled or not config.trusted_cidrs:
        return socket_ip

    networks = _parse_cidrs(config.trusted_cidrs)
    if not networks:
        return socket_ip

    # Only process the header if the socket peer itself is trusted
    if not _is_trusted(socket_ip, networks):
        return socket_ip

    header_value = request.headers.get(config.header, "")
    if not header_value:
        return socket_ip

    ips = [ip.strip() for ip in header_value.split(",")]
    for ip in reversed(ips):
        if not _is_valid_ip(ip):
            # Malformed entry -- fail closed.  Truncate the raw header value before
            # logging to prevent log injection / log flooding from attacker-controlled input.
            safe_ip = ip[:64] if len(ip) > 64 else ip
            logger.warning(
                "Malformed IP in %s header: %r -- falling back to socket peer %s",
                config.header,
                safe_ip,
                socket_ip,
            )
            return socket_ip
        if not _is_trusted(ip, networks):
            return ip

    # All IPs in chain are trusted -- fail closed, return socket peer
    logger.warning(
        "All IPs in %s chain are trusted -- falling back to socket peer %s",
        config.header,
        socket_ip,
    )
    return socket_ip
