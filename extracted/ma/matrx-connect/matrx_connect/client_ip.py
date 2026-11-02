"""The ONE answer to "what IP address is this request from?".

The server runs behind Cloudflare -> AWS ALB -> uvicorn. uvicorn's proxy-header
trust (``FORWARDED_ALLOW_IPS``) covers only the ALB, so ``request.client.host``
is the Cloudflare EDGE that forwarded the request, never the person: on
2026-09-30, 90% of ``ops.api_request_log`` addresses were Cloudflare edges.

Rule: when the immediate peer is inside Cloudflare's published ranges, the
client is Cloudflare's ``CF-Connecting-IP`` header (validated as an IP);
otherwise the client is the peer itself. A ``CF-Connecting-IP`` sent by anyone
who is NOT Cloudflare is ignored (the origin is reachable directly, so the
header is attacker-controlled there). The left-most ``X-Forwarded-For`` entry
is never read: every hop appends to it, so its first entry is whatever the
caller typed.

Never derive a client IP any other way — call :func:`client_ip`.
"""

from __future__ import annotations

import ipaddress
from collections.abc import Mapping
from typing import Protocol

#: Cloudflare's published edge ranges. Source: https://www.cloudflare.com/ips-v4
#: and https://www.cloudflare.com/ips-v6, fetched 2026-09-30. Cloudflare changes
#: these rarely and announces it; refresh by replacing this tuple wholesale from
#: those two URLs (and bump the date).
CLOUDFLARE_IP_RANGES_FETCHED = "2026-09-30"
CLOUDFLARE_IP_RANGES: tuple[str, ...] = (
    # ips-v4
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
    # ips-v6
    "2400:cb00::/32",
    "2606:4700::/32",
    "2803:f800::/32",
    "2405:b500::/32",
    "2405:8100::/32",
    "2a06:98c0::/29",
    "2c0f:f248::/32",
)

_CLOUDFLARE_NETWORKS = tuple(ipaddress.ip_network(cidr) for cidr in CLOUDFLARE_IP_RANGES)

CF_CONNECTING_IP_HEADER = "cf-connecting-ip"


class _Peer(Protocol):
    host: str


class _HasClient(Protocol):
    @property
    def client(self) -> _Peer | None: ...

    @property
    def headers(self) -> Mapping[str, str]: ...


def _parse_ip(value: str | None) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    if not value:
        return None
    try:
        address = ipaddress.ip_address(value.strip())
    except ValueError:
        return None
    # An IPv4-mapped IPv6 peer ("::ffff:1.2.3.4") is the IPv4 address.
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        return address.ipv4_mapped
    return address


def is_cloudflare_ip(value: str | None) -> bool:
    """True when ``value`` is an address inside Cloudflare's published ranges."""
    address = _parse_ip(value)
    if address is None:
        return False
    return any(address in network for network in _CLOUDFLARE_NETWORKS)


def resolve_client_ip(peer_host: str | None, headers: Mapping[str, str]) -> str | None:
    """Client IP from the immediate peer and the request headers.

    ``headers`` must be case-insensitive (Starlette ``Headers``) or lower-cased.
    """
    if peer_host and is_cloudflare_ip(peer_host):
        forwarded = _parse_ip(headers.get(CF_CONNECTING_IP_HEADER))
        if forwarded is not None:
            return str(forwarded)
    return peer_host or None


def client_ip(request: _HasClient) -> str | None:
    """The requesting client's IP for a Starlette ``Request``/``WebSocket``/``HTTPConnection``."""
    peer = request.client
    return resolve_client_ip(peer.host if peer else None, request.headers)


__all__ = [
    "CF_CONNECTING_IP_HEADER",
    "CLOUDFLARE_IP_RANGES",
    "CLOUDFLARE_IP_RANGES_FETCHED",
    "client_ip",
    "is_cloudflare_ip",
    "resolve_client_ip",
]
