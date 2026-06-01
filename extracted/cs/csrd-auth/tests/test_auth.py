"""Tests for csrd.auth — JWT authentication system."""

import time
from datetime import UTC, datetime
from unittest.mock import MagicMock

import jwt as pyjwt
import pytest
from fastapi import FastAPI, HTTPException, Request
from pydantic import SecretStr

from csrd.auth import (
    CallbackAuthenticator,
    CallbackKeyProvider,
    ChainedAuthenticator,
    EnvKeyProvider,
    JWTAuthenticator,
    MultiKeyProvider,
    StaticAuthenticator,
    StaticKeyProvider,
    _default_claims_mapper,
    create_bearer_dependency,
    create_jwt_bearer,
)
from csrd.logging import configure_logging
from csrd.models.claims import UserClaims

SECRET = "test-secret-key-for-jwt-testing-32b"


@pytest.fixture(autouse=True)
def _enable_debug_errors():
    """Enable verbose auth error details during tests."""
    configure_logging(debug=True)
    yield
    configure_logging(debug=False)


def _make_token(payload: dict, secret: str = SECRET, algorithm: str = "HS256") -> str:
    return pyjwt.encode(payload, secret, algorithm=algorithm)


def _make_request(app=None) -> Request:
    scope = {"type": "http", "method": "GET", "path": "/", "headers": [], "app": app or FastAPI()}
    return Request(scope)


# ── Key Providers ────────────────────────────────────────────────────────


class TestStaticKeyProvider:
    def test_string_key(self):
        provider = StaticKeyProvider(key="my-secret")
        result = provider({}, None)
        assert result == "my-secret"

    def test_bytes_key(self):
        provider = StaticKeyProvider(key=b"bytes-secret")
        result = provider({}, None)
        assert result == b"bytes-secret"

    def test_secret_str_key(self):
        provider = StaticKeyProvider(key=SecretStr("hidden"))
        result = provider({}, None)
        assert result == "hidden"


class TestEnvKeyProvider:
    def test_from_app_state(self):
        provider = EnvKeyProvider()
        app = MagicMock()
        settings = MagicMock()
        settings.jwt_secret = SecretStr("state-secret")
        app.state._versioning_settings = settings
        result = provider({}, app)
        assert result == "state-secret"

    def test_from_settings_loader(self):
        settings = MagicMock()
        settings.jwt_secret = SecretStr("loader-secret")
        provider = EnvKeyProvider(settings_loader=lambda: settings)
        app = MagicMock()
        app.state = MagicMock(spec=[])  # no _versioning_settings attr
        result = provider({}, app)
        assert result == "loader-secret"

    def test_missing_secret_raises(self):
        provider = EnvKeyProvider()
        app = MagicMock()
        app.state = MagicMock(spec=[])  # no _versioning_settings attr
        with pytest.raises(RuntimeError, match="No JWT secret configured"):
            provider({}, app)


class TestCallbackKeyProvider:
    def test_delegates_to_callback(self):
        cb = MagicMock(return_value="callback-key")
        provider = CallbackKeyProvider(callback=cb)
        result = provider({"alg": "HS256"}, None)
        assert result == "callback-key"
        cb.assert_called_once_with({"alg": "HS256"}, None)


class TestMultiKeyProvider:
    def test_dict_by_kid(self):
        provider = MultiKeyProvider(providers={"key1": "secret1", "key2": "secret2"})
        result = provider({"kid": "key1"}, None)
        assert result == "secret1"

    def test_dict_fallback_tries_all(self):
        provider = MultiKeyProvider(providers={"a": "val_a", "b": "val_b"})
        result = provider({"kid": "unknown"}, None)
        assert result in ("val_a", "val_b")

    def test_list_tries_in_order(self):
        provider = MultiKeyProvider(providers=["first", "second"])
        result = provider({}, None)
        assert result == "first"

    def test_list_empty_raises(self):
        def failing_provider(headers, app):
            raise ValueError("nope")

        provider = MultiKeyProvider(providers=[CallbackKeyProvider(callback=failing_provider)])
        with pytest.raises(ValueError, match="nope"):
            provider({}, None)


# ── Authenticators ───────────────────────────────────────────────────────


class TestJWTAuthenticator:
    @pytest.mark.asyncio
    async def test_valid_token(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        token = _make_token({"sub": "user1", "user_name": "alice"})
        request = _make_request()
        claims = await auth(request, token)
        assert isinstance(claims, UserClaims)
        assert claims.sub == "user1"

    @pytest.mark.asyncio
    async def test_expired_token(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        token = _make_token({"sub": "user1", "exp": int(time.time()) - 3600})
        request = _make_request()
        with pytest.raises(HTTPException) as exc_info:
            await auth(request, token)
        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_invalid_token(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        request = _make_request()
        with pytest.raises(HTTPException) as exc_info:
            await auth(request, "not.a.valid.token")
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_malformed_token(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        request = _make_request()
        with pytest.raises(HTTPException) as exc_info:
            await auth(request, "completely-invalid")
        assert exc_info.value.status_code == 401
        assert "malformed" in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_wrong_key(self):
        auth = JWTAuthenticator(key="wrong-key", algorithms=["HS256"])
        token = _make_token({"sub": "user1"})
        request = _make_request()
        with pytest.raises(HTTPException) as exc_info:
            await auth(request, token)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_custom_claims_mapper(self):
        def mapper(payload):
            return UserClaims(sub=payload["sub"], user_name="custom", authorities=["ADMIN"])

        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"], claims_mapper=mapper)
        token = _make_token({"sub": "user1"})
        request = _make_request()
        claims = await auth(request, token)
        assert claims.user_name == "custom"
        assert claims.authorities == ["ADMIN"]

    @pytest.mark.asyncio
    async def test_audience_validation(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"], audience="my-api")
        token = _make_token({"sub": "user1", "aud": "my-api"})
        claims = await auth(_make_request(), token)
        assert claims.sub == "user1"

    @pytest.mark.asyncio
    async def test_audience_mismatch(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"], audience="my-api")
        token = _make_token({"sub": "user1", "aud": "other-api"})
        with pytest.raises(HTTPException) as exc_info:
            await auth(_make_request(), token)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_verify_token_without_request(self):
        """verify_token works without a Request object (middleware use-case)."""
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        token = _make_token({"sub": "user1", "user_name": "alice"})
        claims = await auth.verify_token(token)
        assert isinstance(claims, UserClaims)
        assert claims.sub == "user1"

    @pytest.mark.asyncio
    async def test_verify_token_with_app(self):
        """verify_token accepts an optional app argument for key providers."""
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        token = _make_token({"sub": "user1"})
        claims = await auth.verify_token(token, app=FastAPI())
        assert claims.sub == "user1"

    @pytest.mark.asyncio
    async def test_verify_token_expired(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        token = _make_token({"sub": "user1", "exp": int(time.time()) - 3600})
        with pytest.raises(HTTPException) as exc_info:
            await auth.verify_token(token)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_verify_token_malformed(self):
        auth = JWTAuthenticator(key=SECRET, algorithms=["HS256"])
        with pytest.raises(HTTPException) as exc_info:
            await auth.verify_token("completely-invalid")
        assert exc_info.value.status_code == 401


class TestStaticAuthenticator:
    @pytest.mark.asyncio
    async def test_valid_token(self):
        claims = UserClaims(sub="static-user")
        auth = StaticAuthenticator(token="secret-token", claims=claims)
        result = await auth(_make_request(), "secret-token")
        assert result.sub == "static-user"

    @pytest.mark.asyncio
    async def test_invalid_token(self):
        auth = StaticAuthenticator(token="secret-token")
        with pytest.raises(HTTPException) as exc_info:
            await auth(_make_request(), "wrong-token")
        assert exc_info.value.status_code == 401


class TestCallbackAuthenticator:
    @pytest.mark.asyncio
    async def test_sync_callback(self):
        def my_auth(request, token):
            return UserClaims(sub=f"cb-{token[:5]}")

        auth = CallbackAuthenticator(callback=my_auth)
        result = await auth(_make_request(), "abcde12345")
        assert result.sub == "cb-abcde"

    @pytest.mark.asyncio
    async def test_async_callback(self):
        async def my_auth(request, token):
            return UserClaims(sub="async-user")

        auth = CallbackAuthenticator(callback=my_auth)
        result = await auth(_make_request(), "token")
        assert result.sub == "async-user"

    @pytest.mark.asyncio
    async def test_callback_exception_wrapped(self):
        def bad_auth(request, token):
            raise ValueError("oops")

        auth = CallbackAuthenticator(callback=bad_auth)
        with pytest.raises(HTTPException) as exc_info:
            await auth(_make_request(), "token")
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_callback_wrong_return_type(self):
        def bad_return(request, token):
            return {"not": "UserClaims"}

        auth = CallbackAuthenticator(callback=bad_return)
        with pytest.raises(TypeError, match="UserClaims"):
            await auth(_make_request(), "token")


class TestChainedAuthenticator:
    @pytest.mark.asyncio
    async def test_first_success_wins(self):
        auth1 = StaticAuthenticator(token="t1", claims=UserClaims(sub="first"))
        auth2 = StaticAuthenticator(token="t2", claims=UserClaims(sub="second"))
        chained = ChainedAuthenticator(authenticators=[auth1, auth2])
        result = await chained(_make_request(), "t1")
        assert result.sub == "first"

    @pytest.mark.asyncio
    async def test_fallback_to_second(self):
        auth1 = StaticAuthenticator(token="t1", claims=UserClaims(sub="first"))
        auth2 = StaticAuthenticator(token="t2", claims=UserClaims(sub="second"))
        chained = ChainedAuthenticator(authenticators=[auth1, auth2])
        result = await chained(_make_request(), "t2")
        assert result.sub == "second"

    @pytest.mark.asyncio
    async def test_all_fail(self):
        auth1 = StaticAuthenticator(token="t1")
        auth2 = StaticAuthenticator(token="t2")
        chained = ChainedAuthenticator(authenticators=[auth1, auth2])
        with pytest.raises(HTTPException) as exc_info:
            await chained(_make_request(), "wrong")
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_empty_chain(self):
        chained = ChainedAuthenticator(authenticators=[])
        with pytest.raises(HTTPException):
            await chained(_make_request(), "any")


# ── Claims Mapper ────────────────────────────────────────────────────────


class TestDefaultClaimsMapper:
    def test_basic_mapping(self):
        payload = {"sub": "user1", "user_name": "alice", "authorities": ["ROLE_USER"]}
        claims = _default_claims_mapper(payload)
        assert claims.sub == "user1"
        assert claims.user_name == "alice"
        assert claims.authorities == ["ROLE_USER"]

    def test_preferred_username_fallback(self):
        payload = {"sub": "user1", "preferred_username": "bob"}
        claims = _default_claims_mapper(payload)
        assert claims.user_name == "bob"

    def test_email_fallback(self):
        payload = {"sub": "user1", "email": "carol@example.com"}
        claims = _default_claims_mapper(payload)
        assert claims.user_name == "carol@example.com"

    def test_sub_fallback_for_user_name(self):
        payload = {"sub": "user-from-sub"}
        claims = _default_claims_mapper(payload)
        assert claims.user_name == "user-from-sub"

    def test_roles_fallback(self):
        payload = {"sub": "user1", "roles": ["ADMIN"]}
        claims = _default_claims_mapper(payload)
        assert claims.authorities == ["ADMIN"]

    def test_authorities_prefer_over_roles(self):
        payload = {"sub": "user1", "authorities": ["ROLE_USER"], "roles": ["ADMIN"]}
        claims = _default_claims_mapper(payload)
        assert claims.authorities == ["ROLE_USER"]

    def test_string_authorities_split(self):
        payload = {"sub": "user1", "authorities": "ROLE_A ROLE_B"}
        claims = _default_claims_mapper(payload)
        assert claims.authorities == ["ROLE_A", "ROLE_B"]

    def test_empty_payload(self):
        claims = _default_claims_mapper({})
        assert claims.sub == ""
        assert claims.user_name == ""
        assert claims.authorities == []

    def test_iat_unix_timestamp_mapping(self):
        """Test that iat (issued at) Unix timestamp is correctly converted to datetime."""
        now_timestamp = int(time.time())
        payload = {"sub": "user1", "iat": now_timestamp}
        claims = _default_claims_mapper(payload)
        assert claims.iat is not None
        # Allow 1-second tolerance for timestamp conversion
        assert abs((claims.iat - datetime.fromtimestamp(now_timestamp, tz=UTC)).total_seconds()) < 1

    def test_exp_unix_timestamp_mapping(self):
        """Test that exp (expiration) Unix timestamp is correctly converted to datetime."""
        exp_timestamp = int(time.time()) + 3600  # 1 hour from now
        payload = {"sub": "user1", "exp": exp_timestamp}
        claims = _default_claims_mapper(payload)
        assert claims.exp is not None
        # Allow 1-second tolerance for timestamp conversion
        assert abs((claims.exp - datetime.fromtimestamp(exp_timestamp, tz=UTC)).total_seconds()) < 1

    def test_iat_and_exp_together(self):
        """Test that both iat and exp are correctly mapped together."""
        iat_timestamp = int(time.time())
        exp_timestamp = iat_timestamp + 3600
        payload = {
            "sub": "user1",
            "user_name": "alice",
            "iat": iat_timestamp,
            "exp": exp_timestamp,
        }
        claims = _default_claims_mapper(payload)
        assert claims.iat is not None
        assert claims.exp is not None
        # Verify the relationship is preserved (exp should be ~1 hour after iat)
        assert abs((claims.exp - claims.iat).total_seconds() - 3600) < 1

    def test_iat_float_timestamp(self):
        """Test that float Unix timestamps are handled correctly."""
        now_timestamp = time.time()  # Float with fractional seconds
        payload = {"sub": "user1", "iat": now_timestamp}
        claims = _default_claims_mapper(payload)
        assert claims.iat is not None
        expected_iat = datetime.fromtimestamp(now_timestamp, tz=UTC)
        assert abs((claims.iat - expected_iat).total_seconds()) < 1

    def test_invalid_iat_falls_back_to_default(self):
        """Test that invalid iat values fall back to UserClaims default."""
        payload = {"sub": "user1", "iat": "not-a-number"}
        claims = _default_claims_mapper(payload)
        # Should have a default iat value (current time)
        assert claims.iat is not None
        # iat should be approximately now (not the invalid value)
        assert abs((datetime.now(UTC) - claims.iat).total_seconds()) < 5

    def test_invalid_exp_falls_back_to_default(self):
        """Test that invalid exp values fall back to UserClaims default."""
        payload = {"sub": "user1", "exp": "not-a-number"}
        claims = _default_claims_mapper(payload)
        # Should have a default exp value (iat + 1 hour)
        assert claims.exp is not None
        expected_diff = 3600
        actual_diff = (claims.exp - claims.iat).total_seconds()
        assert abs(actual_diff - expected_diff) < 5

    def test_missing_iat_and_exp_use_defaults(self):
        """Test that missing iat/exp fields use UserClaims defaults."""
        payload = {"sub": "user1", "user_name": "alice"}
        claims = _default_claims_mapper(payload)
        # Should have default iat (now) and exp (iat + 1h)
        assert claims.iat is not None
        assert claims.exp is not None
        assert abs((datetime.now(UTC) - claims.iat).total_seconds()) < 5
        assert abs((claims.exp - claims.iat).total_seconds() - 3600) < 5


# ── Factory Functions ─────────────────────────────────────────────────────


class TestCreateBearerDependency:
    def test_wraps_callback(self):
        def my_auth(request, token):
            return UserClaims(sub="test")

        dep = create_bearer_dependency(my_auth, token_finder=lambda: "tok")
        assert callable(dep)

    def test_wraps_authenticator(self):
        auth = StaticAuthenticator(token="t", claims=UserClaims(sub="s"))
        dep = create_bearer_dependency(auth, token_finder=lambda: "t")
        assert callable(dep)

    def test_works_without_token_finder(self):
        auth = StaticAuthenticator(token="t", claims=UserClaims(sub="s"))
        dep = create_bearer_dependency(auth)
        # Should still be callable — token extracted from request at call time
        assert callable(dep)


class TestCreateJwtBearer:
    def test_returns_callable(self):
        dep = create_jwt_bearer(key=SECRET, token_finder=lambda: "tok")
        assert callable(dep)
