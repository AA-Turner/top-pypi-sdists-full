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
from anteroom.config import SessionConfig, TrustedProxyConfig

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

    @pytest.mark.asyncio
    async def test_trusted_proxy_xff_used_for_rate_limit_key(self) -> None:
        """Rate limiting MUST key on the resolved client IP, not the proxy socket IP.

        When a trusted proxy forwards requests, repeated requests from the same
        real client (same XFF IP) should be rate-limited together, even if they
        arrive on the same socket peer.
        """
        proxy_ip = "10.0.0.1"
        real_client_ip = "203.0.113.42"
        # Header name must match TrustedProxyConfig.header (default "X-Forwarded-For")
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])

        app = MagicMock()
        mw = RateLimitMiddleware(app, max_requests=2, window_seconds=60)

        def _make_request(xff: str) -> MagicMock:
            request = MagicMock()
            request.url.path = "/api/chat"
            request.client = MagicMock(host=proxy_ip)
            # Use a case-insensitive Starlette Headers object so header lookup works
            from starlette.datastructures import Headers

            request.headers = Headers(raw=[(b"x-forwarded-for", xff.encode())])
            # Attach trusted_proxy config via app.state.config
            state_cfg = MagicMock()
            state_cfg.trusted_proxy = trusted_cfg
            request.app.state.config = state_cfg
            return request

        call_next = AsyncMock(return_value=MagicMock(status_code=200))

        # Two requests from the same real client IP exhaust the limit
        await mw.dispatch(_make_request(real_client_ip), call_next)
        await mw.dispatch(_make_request(real_client_ip), call_next)

        # Third request from the SAME real client should be rate-limited
        response = await mw.dispatch(_make_request(real_client_ip), call_next)
        assert response.status_code == 429

    @pytest.mark.asyncio
    async def test_trusted_proxy_different_clients_independent_limits(self) -> None:
        """Two different real clients behind the same proxy have independent rate-limit buckets."""
        proxy_ip = "10.0.0.1"
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])

        app = MagicMock()
        mw = RateLimitMiddleware(app, max_requests=2, window_seconds=60)

        def _make_request(real_ip: str) -> MagicMock:
            from starlette.datastructures import Headers

            request = MagicMock()
            request.url.path = "/api/chat"
            request.client = MagicMock(host=proxy_ip)
            request.headers = Headers(raw=[(b"x-forwarded-for", real_ip.encode())])
            state_cfg = MagicMock()
            state_cfg.trusted_proxy = trusted_cfg
            request.app.state.config = state_cfg
            return request

        call_next = AsyncMock(return_value=MagicMock(status_code=200))

        # Fill up client A's bucket
        await mw.dispatch(_make_request("203.0.113.10"), call_next)
        await mw.dispatch(_make_request("203.0.113.10"), call_next)
        limited = await mw.dispatch(_make_request("203.0.113.10"), call_next)
        assert limited.status_code == 429

        # Client B has a separate bucket and should still pass
        response_b = await mw.dispatch(_make_request("203.0.113.20"), call_next)
        assert response_b.status_code == 200

    @pytest.mark.asyncio
    async def test_untrusted_proxy_socket_ip_used_for_rate_limit(self) -> None:
        """When the socket peer is NOT in trusted CIDRs, XFF is ignored and socket IP is keyed."""
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])

        app = MagicMock()
        mw = RateLimitMiddleware(app, max_requests=2, window_seconds=60)

        def _make_request(socket_ip: str, xff: str) -> MagicMock:
            from starlette.datastructures import Headers

            request = MagicMock()
            request.url.path = "/api/chat"
            request.client = MagicMock(host=socket_ip)
            request.headers = Headers(raw=[(b"x-forwarded-for", xff.encode())])
            state_cfg = MagicMock()
            state_cfg.trusted_proxy = trusted_cfg
            request.app.state.config = state_cfg
            return request

        call_next = AsyncMock(return_value=MagicMock(status_code=200))
        untrusted_peer = "192.168.99.1"
        spoofed_xff = "1.2.3.4"

        # Fill up the untrusted socket peer's bucket (keyed on 192.168.99.1, not spoofed XFF)
        await mw.dispatch(_make_request(untrusted_peer, spoofed_xff), call_next)
        await mw.dispatch(_make_request(untrusted_peer, spoofed_xff), call_next)
        limited = await mw.dispatch(_make_request(untrusted_peer, spoofed_xff), call_next)
        assert limited.status_code == 429


# ---------------------------------------------------------------------------
# BearerTokenMiddleware — trusted-proxy IP resolution
# ---------------------------------------------------------------------------


class TestBearerTokenMiddlewareTrustedProxy:
    def _make_middleware(self, token: str = "secret") -> BearerTokenMiddleware:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        cfg = SessionConfig()
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token, session_config=cfg)
        store = MagicMock()
        store.get.return_value = None
        store.create_if_allowed.return_value = True
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True
        return mw

    @pytest.mark.asyncio
    async def test_ip_allowlist_uses_resolved_ip_not_socket_peer(self) -> None:
        """IP allowlist check MUST use the resolved client IP from trusted proxy, not the socket peer.

        When the session config restricts allowed_ips, the check should apply
        to the real client IP resolved from XFF, not the proxy's socket address.
        """
        from starlette.datastructures import Headers

        token = "secret"
        proxy_ip = "10.0.0.1"
        real_client_ip = "203.0.113.50"
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])

        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        # Allow only the real client IP
        cfg = SessionConfig(allowed_ips=[real_client_ip])
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token, session_config=cfg)
        store = MagicMock()
        store.get.return_value = None
        store.create_if_allowed.return_value = True
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "GET"
        request.headers = Headers(
            raw=[
                (b"authorization", f"Bearer {token}".encode()),
                (b"x-forwarded-for", real_client_ip.encode()),
            ]
        )
        request.cookies = {}
        request.client = MagicMock(host=proxy_ip)
        request.app.state.audit_writer = None
        state_cfg = MagicMock()
        state_cfg.trusted_proxy = trusted_cfg
        request.app.state.config = state_cfg

        call_next = AsyncMock(return_value=MagicMock(status_code=200))
        response = await mw.dispatch(request, call_next)
        # Real client IP is in the allowlist, so request should pass
        assert response.status_code == 200
        call_next.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_ip_allowlist_blocks_real_client_not_in_allowlist(self) -> None:
        """Resolved real client IP blocked when not in allowlist, even if proxy IP would pass."""
        from starlette.datastructures import Headers

        token = "secret"
        proxy_ip = "10.0.0.1"
        blocked_real_ip = "198.51.100.99"
        allowed_ip = "203.0.113.1"
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])

        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        cfg = SessionConfig(allowed_ips=[allowed_ip])
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token, session_config=cfg)
        store = MagicMock()
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "GET"
        request.headers = Headers(
            raw=[
                (b"authorization", f"Bearer {token}".encode()),
                (b"x-forwarded-for", blocked_real_ip.encode()),
            ]
        )
        request.cookies = {}
        request.client = MagicMock(host=proxy_ip)
        request.app.state.audit_writer = None
        state_cfg = MagicMock()
        state_cfg.trusted_proxy = trusted_cfg
        request.app.state.config = state_cfg

        response = await mw.dispatch(request, AsyncMock())
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_session_binding_uses_resolved_ip(self) -> None:
        """Session IP binding records and validates against the resolved client IP.

        A session created from real_client_ip should be considered valid when the
        next request also resolves to real_client_ip via XFF, regardless of the
        proxy socket IP.
        """
        from starlette.datastructures import Headers

        token = "secret"
        proxy_ip = "10.0.0.1"
        real_client_ip = "203.0.113.77"
        trusted_cfg = TrustedProxyConfig(enabled=True, trusted_cidrs=["10.0.0.0/8"])

        token_hash = hashlib.sha256(token.encode()).hexdigest()
        app = MagicMock()
        cfg = SessionConfig()
        mw = BearerTokenMiddleware(app, token_hash=token_hash, auth_token=token, session_config=cfg)
        now = time.time()
        store = MagicMock()
        # Session was created with the real client IP
        store.get.return_value = {
            "created_at": now - 100,
            "last_activity_at": now - 10,
            "ip_address": real_client_ip,
        }
        mw._BearerTokenMiddleware__store = store  # type: ignore[attr-defined]
        mw._store_initialized = True

        request = MagicMock()
        request.url.path = "/api/chat"
        request.method = "GET"
        request.headers = Headers(
            raw=[
                (b"authorization", f"Bearer {token}".encode()),
                (b"x-forwarded-for", real_client_ip.encode()),
            ]
        )
        request.cookies = {}
        request.client = MagicMock(host=proxy_ip)
        request.app.state.audit_writer = None
        state_cfg = MagicMock()
        state_cfg.trusted_proxy = trusted_cfg
        request.app.state.config = state_cfg

        call_next = AsyncMock(return_value=MagicMock(status_code=200))
        response = await mw.dispatch(request, call_next)
        # Session IP matches resolved real client IP, so request should succeed
        assert response.status_code == 200
        call_next.assert_awaited_once()
