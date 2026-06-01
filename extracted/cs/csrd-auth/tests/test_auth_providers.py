"""Tests for JWKSKeyProvider and RemoteAuthenticator (mocked HTTP)."""

import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from csrd.auth import JWKSKeyProvider, RemoteAuthenticator
from csrd.logging import configure_logging
from csrd.models.claims import UserClaims


@pytest.fixture(autouse=True)
def _enable_debug_errors():
    """Enable verbose auth error details during tests."""
    configure_logging(debug=True)
    yield
    configure_logging(debug=False)


# ── Helpers ──────────────────────────────────────────────────────────────


def _mock_response(*, status_code=200, json_data=None, text="", raise_for_status=None):
    """Build a mock httpx.Response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.json.return_value = json_data
    if raise_for_status:
        resp.raise_for_status.side_effect = raise_for_status
    else:
        resp.raise_for_status.return_value = None
    return resp


def _mock_request(app_state=None):
    """Build a mock FastAPI Request with optional app.state."""
    request = MagicMock()
    request.app = MagicMock()
    if app_state:
        for k, v in app_state.items():
            setattr(request.app.state, k, v)
    return request


# ── JWKSKeyProvider ──────────────────────────────────────────────────────


class TestJWKSKeyProvider:
    @pytest.mark.asyncio
    async def test_raises_401_when_no_keys_and_fetch_fails(self):
        provider = JWKSKeyProvider(url="https://auth.example.com/.well-known/jwks.json")

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.get.side_effect = Exception("connection refused")
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with pytest.raises(HTTPException) as exc_info:
                await provider({"kid": "key-1", "alg": "RS256"}, None)
            assert exc_info.value.status_code == 401
            assert "Unable to fetch" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_raises_401_when_kid_not_found(self):
        provider = JWKSKeyProvider(url="https://auth.example.com/.well-known/jwks.json")

        # Simulate a successful JWKS fetch with no matching kid
        mock_jwk = MagicMock()
        mock_jwk.key_id = "other-key"
        mock_jwk.key = "the-key"

        mock_jwk_set = MagicMock()
        mock_jwk_set.keys = [mock_jwk]

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(json_data={"keys": []})
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with patch("jwt.PyJWKSet.from_dict", return_value=mock_jwk_set):
                with pytest.raises(HTTPException) as exc_info:
                    await provider({"kid": "nonexistent", "alg": "RS256"}, None)
                assert exc_info.value.status_code == 401
                assert exc_info.value.detail == "No matching key found in JWKS (kid=nonexistent)"

    @pytest.mark.asyncio
    async def test_returns_key_on_match(self):
        provider = JWKSKeyProvider(url="https://auth.example.com/.well-known/jwks.json")

        mock_jwk = MagicMock()
        mock_jwk.key_id = "key-1"
        mock_jwk.key = "resolved-public-key"

        mock_jwk_set = MagicMock()
        mock_jwk_set.keys = [mock_jwk]

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(json_data={"keys": []})
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with patch("jwt.PyJWKSet.from_dict", return_value=mock_jwk_set):
                key = await provider({"kid": "key-1", "alg": "RS256"}, None)
                assert key == "resolved-public-key"

    @pytest.mark.asyncio
    async def test_cache_ttl_prevents_refetch(self):
        provider = JWKSKeyProvider(
            url="https://auth.example.com/.well-known/jwks.json",
            cache_ttl=300.0,
        )

        mock_jwk = MagicMock()
        mock_jwk.key_id = "key-1"
        mock_jwk.key = "the-key"

        mock_jwk_set = MagicMock()
        mock_jwk_set.keys = [mock_jwk]

        # Manually populate cache
        provider._jwk_set = mock_jwk_set
        provider._fetched_at = time.monotonic()

        # Should return cached key without any HTTP call
        key = await provider({"kid": "key-1", "alg": "RS256"}, None)
        assert key == "the-key"

    @pytest.mark.asyncio
    async def test_expired_cache_triggers_refresh(self):
        provider = JWKSKeyProvider(
            url="https://auth.example.com/.well-known/jwks.json",
            cache_ttl=300.0,
        )

        mock_jwk_old = MagicMock()
        mock_jwk_old.key_id = "key-1"
        mock_jwk_old.key = "old-key"

        mock_jwk_set_old = MagicMock()
        mock_jwk_set_old.keys = [mock_jwk_old]

        # Populate cache as expired (fetched_at far enough in the past to exceed TTL)
        provider._jwk_set = mock_jwk_set_old
        provider._fetched_at = time.monotonic() - 600.0  # 600s ago, well past 300s TTL

        new_jwk = MagicMock()
        new_jwk.key_id = "key-1"
        new_jwk.key = "new-key"

        new_jwk_set = MagicMock()
        new_jwk_set.keys = [new_jwk]

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(json_data={"keys": []})
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with patch("jwt.PyJWKSet.from_dict", return_value=new_jwk_set):
                key = await provider({"kid": "key-1", "alg": "RS256"}, None)
                assert key == "new-key"


# ── RemoteAuthenticator ──────────────────────────────────────────────────


class TestRemoteAuthenticator:
    @pytest.mark.asyncio
    async def test_success_returns_claims(self):
        auth = RemoteAuthenticator(url="https://auth.example.com/userinfo")
        request = _mock_request()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(
                json_data={"sub": "user-123", "user_name": "alice", "authorities": ["admin"]}
            )
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            claims = await auth(request, "valid-token")
            assert isinstance(claims, UserClaims)
            assert claims.sub == "user-123"

    @pytest.mark.asyncio
    async def test_401_on_http_error(self):
        import httpx

        auth = RemoteAuthenticator(url="https://auth.example.com/userinfo")
        request = _mock_request()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(side_effect=httpx.ConnectError("refused"))
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with pytest.raises(HTTPException) as exc_info:
                await auth(request, "token")
            assert exc_info.value.status_code == 401
            assert "unavailable" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_401_on_upstream_rejection(self):
        auth = RemoteAuthenticator(url="https://auth.example.com/userinfo")
        request = _mock_request()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(status_code=403, text="Forbidden")
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with pytest.raises(HTTPException) as exc_info:
                await auth(request, "bad-token")
            assert exc_info.value.status_code == 401
            assert "rejected" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_401_on_non_json_response(self):
        auth = RemoteAuthenticator(url="https://auth.example.com/userinfo")
        request = _mock_request()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(status_code=200, text="not json")
            mock_resp.json.side_effect = ValueError("not json")
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with pytest.raises(HTTPException) as exc_info:
                await auth(request, "token")
            assert exc_info.value.status_code == 401
            assert "Invalid response" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_401_on_inactive_token(self):
        auth = RemoteAuthenticator(url="https://auth.example.com/introspect")
        request = _mock_request()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(json_data={"active": False})
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            with pytest.raises(HTTPException) as exc_info:
                await auth(request, "expired-token")
            assert exc_info.value.status_code == 401
            assert "not active" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_custom_claims_mapper(self):
        def custom_mapper(payload):
            return UserClaims(sub=payload["id"], user_name=payload["email"])

        auth = RemoteAuthenticator(
            url="https://auth.example.com/userinfo",
            claims_mapper=custom_mapper,
        )
        request = _mock_request()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_resp = _mock_response(json_data={"id": "u-1", "email": "bob@example.com"})
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_resp)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            claims = await auth(request, "token")
            assert claims.sub == "u-1"
            assert claims.user_name == "bob@example.com"

    @pytest.mark.asyncio
    async def test_uses_injected_client(self):
        mock_client = AsyncMock()
        mock_resp = _mock_response(json_data={"sub": "injected", "user_name": "test"})
        mock_client.request = AsyncMock(return_value=mock_resp)

        auth = RemoteAuthenticator(
            url="https://auth.example.com/userinfo",
            client=mock_client,
        )
        request = _mock_request()

        claims = await auth(request, "token")
        assert claims.sub == "injected"
        mock_client.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_sends_correct_auth_header(self):
        mock_client = AsyncMock()
        mock_resp = _mock_response(json_data={"sub": "u", "user_name": "u"})
        mock_client.request = AsyncMock(return_value=mock_resp)

        auth = RemoteAuthenticator(
            url="https://auth.example.com/userinfo",
            client=mock_client,
            token_header="X-Auth-Token",
            token_prefix="Token ",
        )
        request = _mock_request()

        await auth(request, "my-token")
        call_kwargs = mock_client.request.call_args
        assert call_kwargs.kwargs["headers"]["X-Auth-Token"] == "Token my-token"
