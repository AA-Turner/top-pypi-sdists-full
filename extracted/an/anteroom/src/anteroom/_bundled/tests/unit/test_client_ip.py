"""Tests for trusted-proxy client IP resolution."""

from __future__ import annotations

from dataclasses import dataclass, field
from unittest.mock import MagicMock

from anteroom.services.client_ip import (
    _cidr_cache,
    _is_trusted,
    _is_valid_ip,
    _parse_cidrs,
    resolve_client_ip,
)


@dataclass
class FakeTrustedProxyConfig:
    enabled: bool = False
    trusted_cidrs: list[str] = field(default_factory=list)
    header: str = "X-Forwarded-For"


def _make_request(
    client_host: str | None = "10.0.0.1",
    headers: dict[str, str] | None = None,
) -> MagicMock:
    """Build a minimal mock Request with client and headers."""
    request = MagicMock()
    if client_host is not None:
        request.client = MagicMock()
        request.client.host = client_host
    else:
        request.client = None
    request.headers = headers or {}
    return request


class TestDisabledPassthrough:
    def test_disabled_returns_socket_ip(self) -> None:
        config = FakeTrustedProxyConfig(enabled=False, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("192.168.1.1")
        assert resolve_client_ip(request, config) == "192.168.1.1"

    def test_no_config_returns_socket_ip(self) -> None:
        request = _make_request("192.168.1.1")
        assert resolve_client_ip(request, None) == "192.168.1.1"

    def test_empty_cidrs_returns_socket_ip(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=[])
        request = _make_request("192.168.1.1")
        assert resolve_client_ip(request, config) == "192.168.1.1"


class TestUntrustedSocket:
    def test_untrusted_socket_ignores_xff(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("192.168.1.1", {"X-Forwarded-For": "1.2.3.4"})
        assert resolve_client_ip(request, config) == "192.168.1.1"


class TestTrustedSocketExtraction:
    def test_trusted_socket_extracts_client_ip(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "203.0.113.50"})
        assert resolve_client_ip(request, config) == "203.0.113.50"

    def test_single_hop_xff(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "1.2.3.4"})
        assert resolve_client_ip(request, config) == "1.2.3.4"

    def test_multi_hop_xff_rightmost_untrusted(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8", "172.16.0.0/12"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "spoofed.by.client, 203.0.113.50, 172.16.0.5"})
        assert resolve_client_ip(request, config) == "203.0.113.50"

    def test_all_trusted_falls_back_to_socket_peer(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8", "172.16.0.0/12"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "10.0.0.5, 172.16.0.1, 10.0.0.3"})
        # All IPs in chain are trusted -- fail closed, return socket peer
        assert resolve_client_ip(request, config) == "10.0.0.1"


class TestEdgeCases:
    def test_empty_xff_returns_socket(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": ""})
        assert resolve_client_ip(request, config) == "10.0.0.1"

    def test_no_xff_header_returns_socket(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("10.0.0.1", {})
        assert resolve_client_ip(request, config) == "10.0.0.1"

    def test_malformed_ip_fails_closed(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "203.0.113.50, not-an-ip, 10.0.0.2"})
        assert resolve_client_ip(request, config) == "10.0.0.1"

    def test_no_request_client_returns_unknown(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request(client_host=None)
        assert resolve_client_ip(request, config) == "unknown"

    def test_whitespace_in_xff_stripped(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "  203.0.113.50 , 10.0.0.2  "})
        assert resolve_client_ip(request, config) == "203.0.113.50"


class TestCustomHeader:
    def test_custom_header(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"], header="CF-Connecting-IP")
        request = _make_request("10.0.0.1", {"CF-Connecting-IP": "198.51.100.1"})
        assert resolve_client_ip(request, config) == "198.51.100.1"

    def test_custom_header_missing_returns_socket(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"], header="CF-Connecting-IP")
        request = _make_request("10.0.0.1", {"X-Forwarded-For": "203.0.113.50"})
        assert resolve_client_ip(request, config) == "10.0.0.1"


class TestCidrMatching:
    def test_cidr_match_ipv4(self) -> None:
        networks = _parse_cidrs(["10.0.0.0/8"])
        assert _is_trusted("10.255.0.1", networks) is True
        assert _is_trusted("11.0.0.1", networks) is False

    def test_cidr_match_ipv6(self) -> None:
        networks = _parse_cidrs(["fd00::/8"])
        assert _is_trusted("fd12::1", networks) is True
        assert _is_trusted("fe80::1", networks) is False

    def test_mixed_ipv4_ipv6_cidrs(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8", "fd00::/8"])
        # IPv4 trusted socket with XFF
        req4 = _make_request("10.0.0.1", {"X-Forwarded-For": "203.0.113.1"})
        assert resolve_client_ip(req4, config) == "203.0.113.1"
        # IPv6 trusted socket with XFF
        req6 = _make_request("fd00::1", {"X-Forwarded-For": "2001:db8::1"})
        assert resolve_client_ip(req6, config) == "2001:db8::1"

    def test_loopback_trusted(self) -> None:
        config = FakeTrustedProxyConfig(enabled=True, trusted_cidrs=["127.0.0.0/8"])
        request = _make_request("127.0.0.1", {"X-Forwarded-For": "203.0.113.50"})
        assert resolve_client_ip(request, config) == "203.0.113.50"


class TestParseCidrsCaching:
    def test_parse_cidrs_caches(self) -> None:
        _cidr_cache.clear()
        cidrs = ["192.168.0.0/16"]
        result1 = _parse_cidrs(cidrs)
        result2 = _parse_cidrs(cidrs)
        assert result1 is result2

    def test_parse_cidrs_invalid_entry_skipped(self) -> None:
        _cidr_cache.clear()
        result = _parse_cidrs(["10.0.0.0/8", "not-a-cidr"])
        assert len(result) == 1


class TestHelpers:
    def test_is_valid_ip_v4(self) -> None:
        assert _is_valid_ip("10.0.0.1") is True

    def test_is_valid_ip_v6(self) -> None:
        assert _is_valid_ip("::1") is True

    def test_is_valid_ip_invalid(self) -> None:
        assert _is_valid_ip("not-an-ip") is False

    def test_is_valid_ip_empty(self) -> None:
        assert _is_valid_ip("") is False
