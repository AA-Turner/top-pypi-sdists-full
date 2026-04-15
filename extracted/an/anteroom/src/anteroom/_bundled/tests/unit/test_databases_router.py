"""Tests for routers/databases.py (#689)."""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from anteroom.config import TrustedProxyConfig
from anteroom.routers.databases import (
    _AUTH_MAX_ATTEMPTS,
    _auth_attempts,
    _check_auth_rate_limit,
    _validate_db_name,
    router,
)


def _make_app() -> tuple[FastAPI, MagicMock]:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    mock_mgr = MagicMock()
    app.state.db_manager = mock_mgr
    app.state.config = MagicMock()
    app.state.config.app.tls = False
    return app, mock_mgr


class TestValidateDbName:
    def test_valid_name(self) -> None:
        assert _validate_db_name("my-db_01") == "my-db_01"

    def test_invalid_name_raises(self) -> None:
        import pytest
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            _validate_db_name("bad name!")
        assert exc_info.value.status_code == 400

    def test_empty_name_raises(self) -> None:
        import pytest
        from fastapi import HTTPException

        with pytest.raises(HTTPException):
            _validate_db_name("")


class TestCheckAuthRateLimit:
    def setup_method(self) -> None:
        _auth_attempts.clear()

    def test_allows_under_limit(self) -> None:
        for _ in range(_AUTH_MAX_ATTEMPTS - 1):
            _check_auth_rate_limit("10.0.0.1")

    def test_blocks_at_limit(self) -> None:
        import pytest
        from fastapi import HTTPException

        for _ in range(_AUTH_MAX_ATTEMPTS):
            _check_auth_rate_limit("10.0.0.2")
        with pytest.raises(HTTPException) as exc_info:
            _check_auth_rate_limit("10.0.0.2")
        assert exc_info.value.status_code == 429

    def test_expired_attempts_cleared(self) -> None:
        _auth_attempts["10.0.0.3"] = [time.time() - 120] * _AUTH_MAX_ATTEMPTS
        _check_auth_rate_limit("10.0.0.3")

    def test_evicts_oldest_when_full(self) -> None:
        for i in range(1100):
            _auth_attempts[f"ip-{i}"] = [time.time()]
        _check_auth_rate_limit("new-ip")
        assert len(_auth_attempts) <= 1001


class TestListDatabases:
    def test_returns_databases(self) -> None:
        app, mock_mgr = _make_app()
        mock_mgr.list_databases.return_value = [
            {"name": "personal", "requires_auth": "false"},
            {"name": "shared", "requires_auth": "true"},
        ]
        client = TestClient(app)
        resp = client.get("/api/databases")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_no_db_manager_returns_empty(self) -> None:
        app = FastAPI()
        app.include_router(router, prefix="/api")
        client = TestClient(app)
        resp = client.get("/api/databases")
        assert resp.status_code == 200
        assert resp.json() == []


class TestAuthenticateDatabase:
    def setup_method(self) -> None:
        _auth_attempts.clear()

    def test_invalid_db_name(self) -> None:
        app, _ = _make_app()
        client = TestClient(app)
        resp = client.post("/api/databases/bad name!/auth", json={"passphrase": "x"})
        assert resp.status_code == 400

    def test_no_db_manager(self) -> None:
        app = FastAPI()
        app.include_router(router, prefix="/api")
        client = TestClient(app)
        resp = client.post("/api/databases/mydb/auth", json={"passphrase": "x"})
        assert resp.status_code == 400

    def test_no_passphrase_required(self) -> None:
        app, mock_mgr = _make_app()
        mock_mgr.get_passphrase_hash.return_value = None
        client = TestClient(app)
        resp = client.post("/api/databases/mydb/auth", json={"passphrase": "x"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    @patch("anteroom.routers.databases.verify_passphrase", create=True)
    def test_correct_passphrase(self, mock_verify: MagicMock) -> None:
        app, mock_mgr = _make_app()
        mock_mgr.get_passphrase_hash.return_value = "hashed"
        with patch("anteroom.services.db_auth.verify_passphrase", return_value=True):
            client = TestClient(app)
            resp = client.post("/api/databases/mydb/auth", json={"passphrase": "correct"})
        assert resp.status_code == 200
        assert "anteroom_db_auth_mydb" in resp.headers.get("set-cookie", "")

    def test_wrong_passphrase(self) -> None:
        app, mock_mgr = _make_app()
        mock_mgr.get_passphrase_hash.return_value = "hashed"
        with patch("anteroom.services.db_auth.verify_passphrase", return_value=False):
            client = TestClient(app)
            resp = client.post("/api/databases/mydb/auth", json={"passphrase": "wrong"})
        assert resp.status_code == 401

    def test_rate_limit_enforced(self) -> None:
        app, mock_mgr = _make_app()
        mock_mgr.get_passphrase_hash.return_value = "hashed"
        with patch("anteroom.services.db_auth.verify_passphrase", return_value=False):
            client = TestClient(app)
            for _ in range(_AUTH_MAX_ATTEMPTS):
                client.post("/api/databases/mydb/auth", json={"passphrase": "wrong"})
            resp = client.post("/api/databases/mydb/auth", json={"passphrase": "wrong"})
        assert resp.status_code == 429


class TestAuthenticateDatabaseTrustedProxy:
    """Verify that database auth rate limiting keys on the resolved client IP.

    When a trusted proxy is configured, repeated failed auth attempts from the
    same real client (same XFF IP) must be tracked together, regardless of the
    proxy socket peer.
    """

    def setup_method(self) -> None:
        _auth_attempts.clear()

    def _make_app_with_trusted_proxy(self) -> tuple[FastAPI, MagicMock]:
        app, mock_mgr = _make_app()
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])
        cfg = MagicMock()
        cfg.trusted_proxy = trusted_cfg
        app.state.config = cfg
        return app, mock_mgr

    def test_rate_limit_keyed_on_xff_real_client_not_proxy(self) -> None:
        """Auth rate limit applies to resolved real client IP, not the proxy socket IP.

        TestClient is configured with a socket peer in the trusted CIDR (10.0.0.1)
        so XFF resolution activates and the real client IP is used as the rate-limit key.
        """
        app, mock_mgr = self._make_app_with_trusted_proxy()
        mock_mgr.get_passphrase_hash.return_value = "hashed"

        with patch("anteroom.services.db_auth.verify_passphrase", return_value=False):
            # Socket peer is in trusted CIDR, so XFF is resolved
            client = TestClient(app, client=("10.0.0.1", 50000))
            headers = {"X-Forwarded-For": "203.0.113.55"}
            for _ in range(_AUTH_MAX_ATTEMPTS):
                client.post(
                    "/api/databases/mydb/auth",
                    json={"passphrase": "wrong"},
                    headers=headers,
                )
            # Next request from same real client should be rate-limited
            resp = client.post(
                "/api/databases/mydb/auth",
                json={"passphrase": "wrong"},
                headers=headers,
            )
        assert resp.status_code == 429

    def test_different_real_clients_independent_rate_limits(self) -> None:
        """Two different real clients behind the same proxy have separate rate-limit buckets."""
        app, mock_mgr = self._make_app_with_trusted_proxy()
        mock_mgr.get_passphrase_hash.return_value = "hashed"

        with patch("anteroom.services.db_auth.verify_passphrase", return_value=False):
            # Socket peer is in trusted CIDR, so XFF is resolved per-request
            client = TestClient(app, client=("10.0.0.1", 50000))

            # Exhaust client A's bucket
            headers_a = {"X-Forwarded-For": "203.0.113.10"}
            for _ in range(_AUTH_MAX_ATTEMPTS):
                client.post(
                    "/api/databases/mydb/auth",
                    json={"passphrase": "wrong"},
                    headers=headers_a,
                )
            resp_a = client.post(
                "/api/databases/mydb/auth",
                json={"passphrase": "wrong"},
                headers=headers_a,
            )
            assert resp_a.status_code == 429

            # Client B has an independent bucket and should return 401 (not 429)
            headers_b = {"X-Forwarded-For": "203.0.113.20"}
            resp_b = client.post(
                "/api/databases/mydb/auth",
                json={"passphrase": "wrong"},
                headers=headers_b,
            )
            assert resp_b.status_code == 401
