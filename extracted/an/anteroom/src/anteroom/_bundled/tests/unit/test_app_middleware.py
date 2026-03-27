"""Tests for app.py middleware: BearerTokenMiddleware, RateLimitMiddleware, helpers."""

from __future__ import annotations

import hashlib
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from anteroom.app import (
    BearerTokenMiddleware,
    RateLimitMiddleware,
    _normalize_loopback,
    session_id_from_token,
)
from anteroom.config import SessionConfig

# ---------------------------------------------------------------------------
# session_id_from_token
# ---------------------------------------------------------------------------


class TestSessionIdFromToken:
    def test_deterministic(self) -> None:
        sid1 = session_id_from_token("my-token")
        sid2 = session_id_from_token("my-token")
        assert sid1 == sid2

    def test_length(self) -> None:
        assert len(session_id_from_token("tok")) == 32

    def test_different_tokens_different_ids(self) -> None:
        assert session_id_from_token("a") != session_id_from_token("b")


# ---------------------------------------------------------------------------
# _normalize_loopback
# ---------------------------------------------------------------------------


class TestNormalizeLoopback:
    def test_ipv4_loopback(self) -> None:
        assert _normalize_loopback("127.0.0.1") == "127.0.0.1"

    def test_ipv6_loopback(self) -> None:
        assert _normalize_loopback("::1") == "127.0.0.1"

    def test_ipv4_mapped_ipv6(self) -> None:
        assert _normalize_loopback("::ffff:127.0.0.1") == "127.0.0.1"

    def test_non_loopback_ipv4(self) -> None:
        assert _normalize_loopback("192.168.1.1") == "192.168.1.1"

    def test_invalid_ip(self) -> None:
        assert _normalize_loopback("not-an-ip") == "not-an-ip"


# ---------------------------------------------------------------------------
# BearerTokenMiddleware._check_token
# ---------------------------------------------------------------------------


class TestCheckToken:
    def _make_middleware(self, token: str = "secret") -> BearerTokenMiddleware:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        return BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token)

    def test_correct_token(self) -> None:
        mw = self._make_middleware("secret")
        assert mw._check_token("secret") is True

    def test_wrong_token(self) -> None:
        mw = self._make_middleware("secret")
        assert mw._check_token("wrong") is False

    def test_empty_token(self) -> None:
        mw = self._make_middleware("secret")
        assert mw._check_token("") is False


# ---------------------------------------------------------------------------
# BearerTokenMiddleware._check_session
# ---------------------------------------------------------------------------


class TestCheckSession:
    def _make_middleware(
        self,
        idle_timeout: int = 1800,
        absolute_timeout: int = 43200,
    ) -> BearerTokenMiddleware:
        token = "test-token"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        cfg = SessionConfig(idle_timeout=idle_timeout, absolute_timeout=absolute_timeout)
        mw = BearerTokenMiddleware(app, token_hash=token_hash, session_config=cfg)
        # Inject a mock store
        store = MagicMock()
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True
        return mw

    def test_new_session(self) -> None:
        mw = self._make_middleware()
        mw._BearerTokenMiddleware__store.get.return_value = None  # type: ignore[attr-defined]
        assert mw._check_session("sid", "127.0.0.1") == "new"

    def test_valid_session(self) -> None:
        mw = self._make_middleware()
        now = time.time()
        mw._BearerTokenMiddleware__store.get.return_value = {  # type: ignore[attr-defined]
            "created_at": now - 100,
            "last_activity_at": now - 10,
            "ip_address": "127.0.0.1",
        }
        assert mw._check_session("sid", "127.0.0.1") == "valid"

    def test_absolute_timeout_expired(self) -> None:
        mw = self._make_middleware(absolute_timeout=600)
        now = time.time()
        mw._BearerTokenMiddleware__store.get.return_value = {  # type: ignore[attr-defined]
            "created_at": now - 700,
            "last_activity_at": now - 10,
            "ip_address": "127.0.0.1",
        }
        assert mw._check_session("sid", "127.0.0.1") == "expired"

    def test_idle_timeout_expired(self) -> None:
        mw = self._make_middleware(idle_timeout=60)
        now = time.time()
        mw._BearerTokenMiddleware__store.get.return_value = {  # type: ignore[attr-defined]
            "created_at": now - 100,
            "last_activity_at": now - 120,
            "ip_address": "127.0.0.1",
        }
        assert mw._check_session("sid", "127.0.0.1") == "expired"

    def test_ip_mismatch(self) -> None:
        mw = self._make_middleware()
        now = time.time()
        mw._BearerTokenMiddleware__store.get.return_value = {  # type: ignore[attr-defined]
            "created_at": now - 100,
            "last_activity_at": now - 10,
            "ip_address": "10.0.0.1",
        }
        assert mw._check_session("sid", "192.168.1.1") == "ip_mismatch"

    def test_loopback_variants_match(self) -> None:
        mw = self._make_middleware()
        now = time.time()
        mw._BearerTokenMiddleware__store.get.return_value = {  # type: ignore[attr-defined]
            "created_at": now - 100,
            "last_activity_at": now - 10,
            "ip_address": "::1",
        }
        assert mw._check_session("sid", "127.0.0.1") == "valid"


# ---------------------------------------------------------------------------
# BearerTokenMiddleware.dispatch — non-API paths skip auth
# ---------------------------------------------------------------------------


class TestMiddlewareDispatch:
    @pytest.mark.asyncio
    async def test_non_api_path_skips_auth(self) -> None:
        token = "tok"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        mw = BearerTokenMiddleware(app, token_hash=token_hash)

        request = MagicMock()
        request.url.path = "/index.html"
        call_next = AsyncMock(return_value=MagicMock(status_code=200))

        await mw.dispatch(request, call_next)
        call_next.assert_awaited_once_with(request)

    @pytest.mark.asyncio
    async def test_api_path_no_auth_returns_401(self) -> None:
        token = "tok"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        mw = BearerTokenMiddleware(app, token_hash=token_hash)

        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "GET"
        request.headers = {}
        request.cookies = {}
        request.client = MagicMock(host="127.0.0.1")
        # Mock app.state for audit
        request.app.state.audit_writer = None

        # Inject store
        store = MagicMock()
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        response = await mw.dispatch(request, AsyncMock())
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_bearer_auth_success(self) -> None:
        token = "my-secret"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        cfg = SessionConfig()
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token, session_config=cfg)

        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "GET"
        request.headers = {"authorization": f"Bearer {token}"}
        request.cookies = {}
        request.client = MagicMock(host="127.0.0.1")
        request.app.state.audit_writer = None

        store = MagicMock()
        store.get.return_value = None
        store.create_if_allowed.return_value = True
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        call_next = AsyncMock(return_value=MagicMock(status_code=200))
        await mw.dispatch(request, call_next)
        call_next.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_csrf_mismatch_returns_403(self) -> None:
        token = "my-secret"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token)

        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "POST"
        request.headers = {"x-csrf-token": "wrong-csrf"}
        request.cookies = {"anteroom_session": token, "anteroom_csrf": "real-csrf"}
        request.client = MagicMock(host="127.0.0.1")
        request.app.state.audit_writer = None

        now = time.time()
        store = MagicMock()
        store.get.return_value = {
            "created_at": now - 10,
            "last_activity_at": now - 5,
            "ip_address": "127.0.0.1",
        }
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        response = await mw.dispatch(request, AsyncMock())
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_csrf_match_allows_post(self) -> None:
        token = "my-secret"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token)

        csrf = "csrf-value-123"
        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "POST"
        request.headers = {"x-csrf-token": csrf}
        request.cookies = {"anteroom_session": token, "anteroom_csrf": csrf}
        request.client = MagicMock(host="127.0.0.1")
        request.app.state.audit_writer = None
        request.app.state._allowed_origins = set()

        now = time.time()
        store = MagicMock()
        store.get.return_value = {
            "created_at": now - 10,
            "last_activity_at": now - 5,
            "ip_address": "127.0.0.1",
        }
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        call_next = AsyncMock(return_value=MagicMock(status_code=200))
        await mw.dispatch(request, call_next)
        call_next.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_origin_not_in_allowlist_returns_403(self) -> None:
        token = "my-secret"
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token)

        csrf = "csrf-123"
        request = MagicMock()
        request.url.path = "/api/config"
        request.method = "PATCH"
        request.headers = {"x-csrf-token": csrf, "origin": "https://evil.com"}
        request.cookies = {"anteroom_session": token, "anteroom_csrf": csrf}
        request.client = MagicMock(host="127.0.0.1")
        request.app.state.audit_writer = None
        request.app.state._allowed_origins = {"https://localhost:8080"}

        now = time.time()
        store = MagicMock()
        store.get.return_value = {
            "created_at": now - 10,
            "last_activity_at": now - 5,
            "ip_address": "127.0.0.1",
        }
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        response = await mw.dispatch(request, AsyncMock())
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# RateLimitMiddleware
# ---------------------------------------------------------------------------


class TestRateLimitMiddleware:
    @pytest.mark.asyncio
    async def test_under_limit_passes(self) -> None:
        app = MagicMock()
        mw = RateLimitMiddleware(app, max_requests=5, window_seconds=60)

        request = MagicMock()
        request.url.path = "/api/chat"
        request.client = MagicMock(host="10.0.0.1")

        call_next = AsyncMock(return_value=MagicMock(status_code=200))
        await mw.dispatch(request, call_next)
        call_next.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_over_limit_returns_429(self) -> None:
        app = MagicMock()
        mw = RateLimitMiddleware(app, max_requests=2, window_seconds=60)

        request = MagicMock()
        request.url.path = "/api/chat"
        request.client = MagicMock(host="10.0.0.1")

        call_next = AsyncMock(return_value=MagicMock(status_code=200))

        # Fill up the limit
        await mw.dispatch(request, call_next)
        await mw.dispatch(request, call_next)

        # Third request should be rate limited
        response = await mw.dispatch(request, call_next)
        assert response.status_code == 429

    @pytest.mark.asyncio
    async def test_exempt_path_skips_rate_limit(self) -> None:
        app = MagicMock()
        mw = RateLimitMiddleware(app, max_requests=1, window_seconds=60, exempt_paths={"/api/events"})

        request = MagicMock()
        request.url.path = "/api/events"

        call_next = AsyncMock(return_value=MagicMock(status_code=200))

        # Even many requests pass through on exempt path
        for _ in range(5):
            await mw.dispatch(request, call_next)
        assert call_next.await_count == 5
