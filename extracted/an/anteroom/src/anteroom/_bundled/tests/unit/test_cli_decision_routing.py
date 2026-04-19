"""Unit tests for ``cli._decision_routing`` (#925).

The plan v7 failure-mode taxonomy is the load-bearing contract for
tamper evidence in CLI mode. Every row of that table has a dedicated
test below: misclassifying a non-loopback ECONNREFUSED as
``ServerNotRunningError`` would silently let CLI local writes form a
parallel HMAC chain while the real server is up elsewhere.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from anteroom.cli._decision_routing import (
    ServerHttpError,
    ServerNotRunningError,
    _target_is_loopback,
    call_decision_endpoint,
)

# ---------------------------------------------------------------------------
# Lightweight config fixture (mirrors the AppConfig surface we touch)
# ---------------------------------------------------------------------------


_TEST_PEM = "-----BEGIN PRIVATE KEY-----\nfaketestkey\n-----END PRIVATE KEY-----"


@dataclass
class _Tls:
    enabled: bool = False


@dataclass
class _AppCfg:
    host: str = "127.0.0.1"
    port: int = 8080
    tls: Any = None

    def __post_init__(self) -> None:
        if self.tls is None:
            self.tls = _Tls()


@dataclass
class _IdentityCfg:
    private_key: str = _TEST_PEM


@dataclass
class _Config:
    app: _AppCfg
    identity: _IdentityCfg


def _config(host: str = "127.0.0.1", port: int = 8080) -> _Config:
    return _Config(app=_AppCfg(host=host, port=port), identity=_IdentityCfg())


# ---------------------------------------------------------------------------
# _target_is_loopback
# ---------------------------------------------------------------------------


class TestTargetIsLoopback:
    def test_ipv4_loopback_literal(self) -> None:
        assert _target_is_loopback("127.0.0.1") is True

    def test_ipv4_loopback_range(self) -> None:
        assert _target_is_loopback("127.0.0.5") is True

    def test_ipv6_loopback_literal(self) -> None:
        assert _target_is_loopback("::1") is True

    def test_ipv4_non_loopback_literal(self) -> None:
        assert _target_is_loopback("192.168.1.10") is False

    def test_ipv4_zero_address_is_not_loopback(self) -> None:
        # 0.0.0.0 is a bind address, not a connect target — must NOT authorise fallback.
        assert _target_is_loopback("0.0.0.0") is False

    def test_empty_host_is_not_loopback(self) -> None:
        assert _target_is_loopback("") is False

    def test_hostname_resolving_to_loopback(self) -> None:
        with patch(
            "anteroom.cli._decision_routing.socket.getaddrinfo",
            return_value=[(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.1", 0))],
        ):
            assert _target_is_loopback("localhost") is True

    def test_hostname_resolving_to_non_loopback(self) -> None:
        with patch(
            "anteroom.cli._decision_routing.socket.getaddrinfo",
            return_value=[(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("203.0.113.5", 0))],
        ):
            assert _target_is_loopback("example.internal") is False

    def test_hostname_dns_failure_is_conservative_false(self) -> None:
        with patch(
            "anteroom.cli._decision_routing.socket.getaddrinfo",
            side_effect=socket.gaierror("nope"),
        ):
            assert _target_is_loopback("nonexistent.invalid") is False

    def test_hostname_mixed_loopback_and_remote_is_false(self) -> None:
        # Defence in depth: if any resolution maps to non-loopback, decline.
        with patch(
            "anteroom.cli._decision_routing.socket.getaddrinfo",
            return_value=[
                (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.1", 0)),
                (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("203.0.113.5", 0)),
            ],
        ):
            assert _target_is_loopback("dual.example") is False


# ---------------------------------------------------------------------------
# Helpers for taxonomy tests
# ---------------------------------------------------------------------------


def _make_connection_refused() -> httpx.ConnectError:
    """Construct a ConnectError whose chain contains ConnectionRefusedError."""
    inner = ConnectionRefusedError("ECONNREFUSED")
    err = httpx.ConnectError("connection refused")
    err.__cause__ = inner
    return err


def _make_connect_error(message: str) -> httpx.ConnectError:
    """ConnectError NOT caused by ConnectionRefusedError (TLS, DNS, etc.)."""
    inner = OSError(message)  # generic OSError, not ECONNREFUSED
    err = httpx.ConnectError(message)
    err.__cause__ = inner
    return err


def _make_connection_refused_via_context() -> httpx.ConnectError:
    """Construct a ConnectError whose chain has ConnectionRefusedError only in ``__context__``.

    On py3.14 + httpx 0.28+, the real-world chain is:

        ConnectError (outer)
            __context__ -> ConnectError (inner httpcore)
                __context__ -> ConnectionRefusedError

    ``__cause__`` is ``None`` throughout — the chain is set up via
    implicit nesting, not ``raise X from Y``.  Mirrors that shape.
    See #1444.
    """
    refused = ConnectionRefusedError("ECONNREFUSED")
    try:
        raise refused
    except ConnectionRefusedError:
        try:
            raise httpx.ConnectError("inner connect error")
        except httpx.ConnectError as inner:
            try:
                raise httpx.ConnectError("outer connect error") from None
            except httpx.ConnectError as outer:
                # Manually chain via __context__, not __cause__.
                outer.__context__ = inner
                outer.__cause__ = None
                return outer


# ---------------------------------------------------------------------------
# Failure-mode taxonomy
# ---------------------------------------------------------------------------


class TestRoutingTaxonomy:
    def test_2xx_returns_parsed_json(self) -> None:
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "approved", "run_id": "r1"}
        with patch("httpx.request", return_value=mock_response) as req:
            result = call_decision_endpoint(cfg, "POST", "/api/workflow-runs/r1/approve")
        assert result == {"status": "approved", "run_id": "r1"}
        # Bearer header was attached.
        called_headers = req.call_args.kwargs["headers"]
        assert called_headers["Authorization"].startswith("Bearer ")

    def test_econnrefused_loopback_raises_server_not_running(self) -> None:
        cfg = _config(host="127.0.0.1")
        with patch("httpx.request", side_effect=_make_connection_refused()):
            with pytest.raises(ServerNotRunningError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_econnrefused_via_context_chain_raises_server_not_running(self) -> None:
        """Regression for #1444: py3.14 + httpx 0.28+ put ``ConnectionRefusedError``
        in ``__context__``, not ``__cause__``.  The classifier must walk
        both chains so loopback ECONNREFUSED still maps to
        ``ServerNotRunningError``.
        """
        cfg = _config(host="127.0.0.1")
        with patch("httpx.request", side_effect=_make_connection_refused_via_context()):
            with pytest.raises(ServerNotRunningError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_econnrefused_loopback_ipv6_raises_server_not_running(self) -> None:
        cfg = _config(host="::1")
        with patch("httpx.request", side_effect=_make_connection_refused()):
            with pytest.raises(ServerNotRunningError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_econnrefused_non_loopback_ip_raises_server_http_error(self) -> None:
        cfg = _config(host="192.168.1.10")
        with patch("httpx.request", side_effect=_make_connection_refused()):
            with pytest.raises(ServerHttpError) as exc_info:
                call_decision_endpoint(cfg, "POST", "/api/x")
        assert "non-loopback" in str(exc_info.value)

    def test_econnrefused_non_loopback_hostname_raises_server_http_error(self) -> None:
        cfg = _config(host="example.internal")
        with patch(
            "anteroom.cli._decision_routing.socket.getaddrinfo",
            return_value=[(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("203.0.113.5", 0))],
        ):
            with patch("httpx.request", side_effect=_make_connection_refused()):
                with pytest.raises(ServerHttpError):
                    call_decision_endpoint(cfg, "POST", "/api/x")

    def test_econnrefused_dns_failure_raises_server_http_error(self) -> None:
        cfg = _config(host="nonexistent.invalid")
        with patch(
            "anteroom.cli._decision_routing.socket.getaddrinfo",
            side_effect=socket.gaierror("nope"),
        ):
            with patch("httpx.request", side_effect=_make_connection_refused()):
                with pytest.raises(ServerHttpError):
                    call_decision_endpoint(cfg, "POST", "/api/x")

    def test_connect_timeout_raises_server_http_error(self) -> None:
        cfg = _config()
        with patch("httpx.request", side_effect=httpx.ConnectTimeout("connect timeout")):
            with pytest.raises(ServerHttpError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_read_timeout_raises_server_http_error(self) -> None:
        cfg = _config()
        with patch("httpx.request", side_effect=httpx.ReadTimeout("read timeout")):
            with pytest.raises(ServerHttpError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_tls_handshake_error_raises_server_http_error(self) -> None:
        # TLS handshake failures bubble up as a generic ConnectError without
        # ConnectionRefusedError in the cause chain.
        cfg = _config()
        with patch("httpx.request", side_effect=_make_connect_error("tls handshake failed")):
            with pytest.raises(ServerHttpError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_network_unreachable_raises_server_http_error(self) -> None:
        cfg = _config()
        with patch("httpx.request", side_effect=_make_connect_error("network unreachable")):
            with pytest.raises(ServerHttpError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_401_raises_server_http_error(self) -> None:
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "unauthorized"
        with patch("httpx.request", return_value=mock_response):
            with pytest.raises(ServerHttpError) as exc_info:
                call_decision_endpoint(cfg, "POST", "/api/x")
        assert exc_info.value.status_code == 401

    def test_403_raises_server_http_error(self) -> None:
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = "forbidden"
        with patch("httpx.request", return_value=mock_response):
            with pytest.raises(ServerHttpError) as exc_info:
                call_decision_endpoint(cfg, "POST", "/api/x")
        assert exc_info.value.status_code == 403

    def test_404_raises_server_http_error(self) -> None:
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "not found"
        with patch("httpx.request", return_value=mock_response):
            with pytest.raises(ServerHttpError) as exc_info:
                call_decision_endpoint(cfg, "POST", "/api/x")
        assert exc_info.value.status_code == 404

    def test_500_raises_server_http_error(self) -> None:
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "boom"
        with patch("httpx.request", return_value=mock_response):
            with pytest.raises(ServerHttpError) as exc_info:
                call_decision_endpoint(cfg, "POST", "/api/x")
        assert exc_info.value.status_code == 500

    def test_no_identity_raises_server_http_error(self) -> None:
        # No PEM available — cannot derive bearer; surface as HTTP error
        # (NOT ServerNotRunningError, which would license a fallback that
        # would also lack a chain key).
        cfg = _Config(app=_AppCfg(), identity=_IdentityCfg(private_key=""))
        with pytest.raises(ServerHttpError):
            call_decision_endpoint(cfg, "POST", "/api/x")


# ---------------------------------------------------------------------------
# Cold-start race + crash mid-call sequencing (v7 risks section)
# ---------------------------------------------------------------------------


class TestRoutingEdgeCases:
    def test_slow_start_returns_5xx_not_econnrefused(self) -> None:
        """Cold-start race: TCP handshake completes, app not ready → 5xx, not ECONNREFUSED.

        The kernel only emits ECONNREFUSED when no socket is bound to the
        port. As long as the server is bound (even pre-app-ready), we get
        either an HTTP response or a higher-layer error — never
        ECONNREFUSED. So no spurious local fallback can fire.
        """
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.text = "starting up"
        with patch("httpx.request", return_value=mock_response):
            with pytest.raises(ServerHttpError):
                call_decision_endpoint(cfg, "POST", "/api/x")

    def test_unsupported_method_raises_value_error(self) -> None:
        cfg = _config()
        with pytest.raises(ValueError):
            call_decision_endpoint(cfg, "BREW", "/api/x")

    def test_2xx_with_invalid_json_raises_server_http_error(self) -> None:
        cfg = _config()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("invalid JSON")
        with patch("httpx.request", return_value=mock_response):
            with pytest.raises(ServerHttpError):
                call_decision_endpoint(cfg, "POST", "/api/x")
