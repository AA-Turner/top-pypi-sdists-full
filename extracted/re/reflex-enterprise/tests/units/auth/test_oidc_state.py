"""Unit tests for OIDCAuthState._get_userinfo functionality."""

import time
from collections.abc import Iterator, Mapping
from types import MethodType, TracebackType
from typing import Any
from unittest.mock import AsyncMock

import pytest
import reflex as rx
import wrapt
from joserfc import jwk, jwt

from reflex_enterprise.auth.oidc import utils as oidc_utils
from reflex_enterprise.auth.oidc.state import AccessTokenMetadata, OIDCAuthState
from reflex_enterprise.auth.oidc.types import AsyncHTTPClientProtocol

ISSUER = "https://test-issuer.example.com"
AUDIENCE = "test-client-id"
USERINFO_URL = "https://test-issuer.example.com/userinfo"
TOKEN_URL = "https://test-issuer.example.com/token"
JWKS_URL = "https://test-issuer.example.com/jwks"
AUTHORIZATION_URL = "https://test-issuer.example.com/authorize"


class _RebindingStateProxy(wrapt.ObjectProxy):
    """Minimal stand-in for reflex's ``StateProxy`` used to reproduce ENG-9663.

    Like ``reflex.istate.proxy.StateProxy``, this is a ``wrapt.ObjectProxy`` --
    so ``self.__class__`` resolves to the wrapped state's real class while
    ``type(self)`` is the proxy type -- and it rebinds bound methods so that
    ``self`` inside a handler is the proxy rather than the wrapped instance.
    That combination is exactly what turns a stray
    ``type(self).<event_handler>`` lookup into
    ``AttributeError: type object 'StateProxy' has no attribute ...``.
    """

    def __getattr__(self, name: str) -> Any:
        value = super().__getattr__(name)  # pyright: ignore[reportAttributeAccessIssue]
        if isinstance(value, MethodType) and value.__self__ is self.__wrapped__:
            value = type(value)(value.__func__, self)
        return value


class FakeResponse:
    """Fake HTTP response for OIDC tests."""

    def __init__(self, status: int = 200, json_data: Any = None, text: str = ""):
        self.status = status
        self._json_data = json_data if json_data is not None else {}
        self._text = text

    async def json(self) -> Any:
        return self._json_data

    async def text(self) -> str:
        return self._text


class FakeResponseContext:
    """Async context manager wrapping a FakeResponse."""

    def __init__(self, response: FakeResponse):
        self._response = response

    async def __aenter__(self) -> FakeResponse:
        return self._response

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None


class FakeHTTPClient:
    """Configurable mock HTTP client for OIDC tests.

    OIDC discovery and JWKS URLs are served from ``metadata`` and ``jwks``.
    Other endpoints can be configured via ``get_responses`` / ``post_responses``.
    """

    def __init__(self, metadata: dict | None = None, jwks: dict | None = None):
        self.metadata = metadata or {}
        self.jwks = jwks
        self.get_responses: dict[str, FakeResponse] = {}
        self.post_responses: dict[str, FakeResponse] = {}
        self.get_calls: list[dict[str, Any]] = []
        self.post_calls: list[dict[str, Any]] = []

    def get(
        self, url: str, *, headers: Mapping[str, str] | None = None
    ) -> FakeResponseContext:
        self.get_calls.append(
            {"url": url, "headers": dict(headers) if headers else None}
        )
        if url.endswith("/.well-known/openid-configuration"):
            return FakeResponseContext(FakeResponse(json_data=self.metadata))
        if self.jwks is not None and url == self.metadata.get("jwks_uri"):
            return FakeResponseContext(FakeResponse(json_data=self.jwks))
        if url in self.get_responses:
            return FakeResponseContext(self.get_responses[url])
        return FakeResponseContext(
            FakeResponse(status=404, text=f"unexpected GET {url}")
        )

    def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        data: Any = None,
    ) -> FakeResponseContext:
        self.post_calls.append(
            {
                "url": url,
                "headers": dict(headers) if headers else None,
                "data": data,
            }
        )
        if url in self.post_responses:
            return FakeResponseContext(self.post_responses[url])
        return FakeResponseContext(
            FakeResponse(status=404, text=f"unexpected POST {url}")
        )


_active_client: FakeHTTPClient | None = None


class UserinfoAuthState(OIDCAuthState, rx.State):
    """OIDCAuthState subclass that delegates to a per-test fake HTTP client."""

    __provider__ = "test_userinfo"

    @classmethod
    def _http_client(cls) -> AsyncHTTPClientProtocol:
        if _active_client is None:
            raise RuntimeError("FakeHTTPClient not active for this test.")
        return _active_client


@pytest.fixture
def signing_key() -> jwk.RSAKey:
    return jwk.RSAKey.generate_key(2048, parameters={"kid": "test-kid"})


@pytest.fixture
def jwks(signing_key: jwk.RSAKey) -> dict:
    return {"keys": [signing_key.as_dict(private=False)]}


@pytest.fixture
def metadata() -> dict:
    return {
        "issuer": ISSUER,
        "jwks_uri": JWKS_URL,
        "userinfo_endpoint": USERINFO_URL,
        "token_endpoint": TOKEN_URL,
        "authorization_endpoint": AUTHORIZATION_URL,
    }


@pytest.fixture
def fake_client(metadata, jwks) -> Iterator[FakeHTTPClient]:
    global _active_client
    _active_client = FakeHTTPClient(metadata=metadata, jwks=jwks)
    yield _active_client
    _active_client = None


@pytest.fixture(autouse=True)
def _clear_oidc_cache():
    oidc_utils._OIDC_CACHE.clear()
    yield
    oidc_utils._OIDC_CACHE.clear()


@pytest.fixture(autouse=True)
def oidc_env(monkeypatch):
    monkeypatch.setenv("OIDC_CLIENT_ID", AUDIENCE)
    monkeypatch.setenv("OIDC_ISSUER_URI", ISSUER)


@pytest.fixture
def stub_call_event_from_computed_var(monkeypatch) -> AsyncMock:
    """Stub `call_event_from_computed_var` so it does not require a running app."""
    stub = AsyncMock(return_value=None)
    monkeypatch.setattr(
        "reflex_enterprise.auth.oidc.state.call_event_from_computed_var",
        stub,
    )
    return stub


@pytest.fixture
def stub_chain_event_out_of_band(monkeypatch) -> AsyncMock:
    """Stub `chain_event_out_of_band` so it does not require a running app."""
    stub = AsyncMock(return_value=None)
    monkeypatch.setattr(
        "reflex_enterprise.auth.oidc.state.chain_event_out_of_band",
        stub,
    )
    return stub


@pytest.fixture(autouse=True)
def stub_event_chaining(
    stub_call_event_from_computed_var: AsyncMock,
    stub_chain_event_out_of_band: AsyncMock,
) -> None:
    """Autouse super-fixture to install both event chaining stubs."""
    return None


@pytest.fixture(autouse=True)
def stub_cookie_sync(monkeypatch):
    """Stub out HTTPCookie.ensure_handlers_registered so we don't need a running app."""
    from reflex_enterprise.auth.cookie import HTTPCookie

    monkeypatch.setattr(
        HTTPCookie, "ensure_handlers_registered", classmethod(lambda cls: None)
    )


def make_id_token(
    signing_key: jwk.RSAKey,
    *,
    iss: str = ISSUER,
    aud: str = AUDIENCE,
    sub: str = "user-1",
    exp_offset: int = 600,
    **extra: Any,
) -> str:
    """Create a signed ID token JWT for tests."""
    now = int(time.time())
    claims = {
        "iss": iss,
        "aud": aud,
        "sub": sub,
        "iat": now,
        "exp": now + exp_offset,
        **extra,
    }
    return jwt.encode({"alg": "RS256", "kid": signing_key.kid}, claims, signing_key)


def access_token_data(access_token: str = "at-1", expires_in: int = 3600) -> str:
    """Create the urlencoded ``_access_token_data`` cookie value."""
    return AccessTokenMetadata.from_exchange(
        {"access_token": access_token, "expires_in": expires_in}
    ).to_cookie_value()


@pytest.fixture
def state():
    """Instantiate the test OIDCAuthState subclass."""
    return UserinfoAuthState()


async def test_get_userinfo_returns_endpoint_response_when_tokens_valid(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """Valid tokens with a userinfo endpoint should return the endpoint response."""
    state._access_token_data = access_token_data("at-1")
    state._id_token = make_id_token(signing_key)
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        json_data={"sub": "user-1", "email": "user@example.com"}
    )

    result = await state._get_userinfo()

    assert result == {"sub": "user-1", "email": "user@example.com"}
    userinfo_call = next(
        call for call in fake_client.get_calls if call["url"] == USERINFO_URL
    )
    assert userinfo_call["headers"] == {"Authorization": "Bearer at-1"}
    stub_call_event_from_computed_var.assert_not_called()


async def test_get_userinfo_falls_back_to_id_token_claims_without_userinfo_endpoint(
    state, fake_client, signing_key, metadata
):
    """Without a userinfo endpoint, the ID token claims should be used."""
    metadata.pop("userinfo_endpoint")
    state._access_token_data = access_token_data("at-1")
    state._id_token = make_id_token(
        signing_key, sub="claims-user", email="c@example.com"
    )

    result = await state._get_userinfo()

    assert result is not None
    assert result["sub"] == "claims-user"
    assert result["email"] == "c@example.com"
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)


async def test_get_userinfo_returns_none_when_userinfo_endpoint_fails(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """A non-2xx userinfo response is swallowed by the error context and yields None."""
    state._access_token_data = access_token_data("at-1")
    state._id_token = make_id_token(signing_key)
    fake_client.get_responses[USERINFO_URL] = FakeResponse(status=500, text="boom")

    result = await state._get_userinfo()

    assert result is None
    # The tokens were valid; reset_auth should not have been triggered.
    stub_call_event_from_computed_var.assert_not_called()
    assert state._last_error_message
    assert "Userinfo request failed" in state._last_error_message


async def test_get_userinfo_resets_auth_when_no_tokens_and_no_refresh_token(
    state, fake_client, stub_call_event_from_computed_var
):
    """With no tokens at all, reset_auth should be called and no refresh attempted."""
    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    assert fake_client.post_calls == []


async def test_get_userinfo_resets_auth_when_invalid_tokens_and_no_refresh_token(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """Invalid tokens without a refresh token should reset immediately."""
    state._access_token_data = access_token_data("at-1")
    state._id_token = make_id_token(signing_key, iss="https://wrong-issuer.example.com")

    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    # No refresh attempt because there is no refresh token.
    assert fake_client.post_calls == []


async def test_get_userinfo_refreshes_then_returns_userinfo(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """Invalid tokens with a refresh token should refresh and then return userinfo."""
    state._access_token_data = access_token_data("expired-at", expires_in=-10)
    state._id_token = make_id_token(signing_key, exp_offset=-10)
    state._refresh_token = "refresh-1"
    new_id_token = make_id_token(signing_key, sub="refreshed-user")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "new-at",
            "id_token": new_id_token,
            "refresh_token": "refresh-2",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "openid email profile",
        }
    )
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        json_data={"sub": "refreshed-user"}
    )

    result = await state._get_userinfo()

    assert result == {"sub": "refreshed-user"}
    # Refresh happened.
    assert any(call["url"] == TOKEN_URL for call in fake_client.post_calls)
    refresh_call = next(
        call for call in fake_client.post_calls if call["url"] == TOKEN_URL
    )
    assert refresh_call["data"]["grant_type"] == "refresh_token"
    assert refresh_call["data"]["refresh_token"] == "refresh-1"
    # New tokens were stored.
    assert state._refresh_token == "refresh-2"
    # reset_auth should not have been called because refresh succeeded.
    stub_call_event_from_computed_var.assert_not_called()
    # Userinfo call used the new access token.
    userinfo_call = next(
        call for call in fake_client.get_calls if call["url"] == USERINFO_URL
    )
    assert userinfo_call["headers"] == {"Authorization": "Bearer new-at"}


async def test_get_userinfo_resets_auth_when_refresh_http_request_fails(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """If the refresh endpoint returns an HTTP error, reset_auth should be called."""
    state._access_token_data = access_token_data("expired-at", expires_in=-10)
    state._id_token = make_id_token(signing_key, exp_offset=-10)
    state._refresh_token = "refresh-1"
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        status=400, text='{"error":"invalid_grant"}'
    )

    result = await state._get_userinfo()

    assert result is None
    assert any(call["url"] == TOKEN_URL for call in fake_client.post_calls)
    stub_call_event_from_computed_var.assert_awaited()
    # No userinfo call should have been issued.
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)


async def test_get_userinfo_refreshes_without_existing_access_token(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """A refresh token alone (no access token cookie) should still trigger refresh."""
    state._refresh_token = "refresh-1"
    new_id_token = make_id_token(signing_key, sub="no-at-user")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "fresh-at",
            "id_token": new_id_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        json_data={"sub": "no-at-user"}
    )

    result = await state._get_userinfo()

    assert result == {"sub": "no-at-user"}
    assert any(call["url"] == TOKEN_URL for call in fake_client.post_calls)
    stub_call_event_from_computed_var.assert_not_called()


async def test_get_userinfo_resets_auth_when_refresh_succeeds_but_tokens_still_invalid(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """Refresh succeeds but returns tokens that still fail validation."""
    state._access_token_data = access_token_data("expired-at", expires_in=-10)
    state._id_token = make_id_token(signing_key, exp_offset=-10)
    state._refresh_token = "refresh-1"
    # New id_token has wrong issuer so re-validation will fail.
    bad_id_token = make_id_token(signing_key, iss="https://other-issuer.example.com")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "new-at",
            "id_token": bad_id_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )

    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited()
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)


async def test_get_userinfo_retries_after_userinfo_fetch_fails_with_refresh_token(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """If the userinfo endpoint rejects the access token, refresh and retry."""
    state._access_token_data = access_token_data("stale-at")
    state._id_token = make_id_token(signing_key)
    state._refresh_token = "refresh-1"
    new_id_token = make_id_token(signing_key, sub="retried-user")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "fresh-at",
            "id_token": new_id_token,
            "refresh_token": "refresh-2",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )
    # First call returns 401, second call succeeds. Track call count to
    # return a different response each time.
    call_count = {"n": 0}

    def userinfo_response_for_call():
        call_count["n"] += 1
        if call_count["n"] == 1:
            return FakeResponse(status=401, text="invalid_token")
        return FakeResponse(json_data={"sub": "retried-user"})

    original_get = fake_client.get

    def dynamic_get(url, *, headers=None):
        if url == USERINFO_URL:
            return FakeResponseContext(userinfo_response_for_call())
        return original_get(url, headers=headers)

    fake_client.get = dynamic_get

    result = await state._get_userinfo()

    assert result == {"sub": "retried-user"}
    assert call_count["n"] == 2
    # Refresh was performed exactly once.
    assert sum(1 for c in fake_client.post_calls if c["url"] == TOKEN_URL) == 1
    # New tokens are persisted.
    assert state._refresh_token == "refresh-2"
    stub_call_event_from_computed_var.assert_not_called()


async def test_get_userinfo_does_not_retry_userinfo_fetch_without_refresh_token(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """A userinfo fetch failure without a refresh token should not be retried."""
    state._access_token_data = access_token_data("stale-at")
    state._id_token = make_id_token(signing_key)
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        status=401, text="invalid_token"
    )

    result = await state._get_userinfo()

    assert result is None
    # Exactly one userinfo call, no refresh attempt.
    assert sum(1 for c in fake_client.get_calls if c["url"] == USERINFO_URL) == 1
    assert fake_client.post_calls == []
    stub_call_event_from_computed_var.assert_not_called()
    assert "Userinfo request failed" in state._last_error_message


async def test_get_userinfo_returns_none_when_userinfo_retry_also_fails(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """If the retried userinfo fetch also fails, the error context returns None."""
    state._access_token_data = access_token_data("stale-at")
    state._id_token = make_id_token(signing_key)
    state._refresh_token = "refresh-1"
    new_id_token = make_id_token(signing_key, sub="user-1")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "fresh-at",
            "id_token": new_id_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )
    # Userinfo keeps returning 401 even after refresh.
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        status=401, text="invalid_token"
    )

    result = await state._get_userinfo()

    assert result is None
    # Two userinfo attempts, one refresh.
    assert sum(1 for c in fake_client.get_calls if c["url"] == USERINFO_URL) == 2
    assert sum(1 for c in fake_client.post_calls if c["url"] == TOKEN_URL) == 1
    # No explicit reset_auth event because validation passed after refresh.
    stub_call_event_from_computed_var.assert_not_called()


async def test_get_userinfo_returns_none_when_userinfo_fails_and_refresh_invalidates_tokens(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """Userinfo fetch fails; refresh succeeds but new tokens fail validation."""
    state._access_token_data = access_token_data("stale-at")
    state._id_token = make_id_token(signing_key)
    state._refresh_token = "refresh-1"
    bad_id_token = make_id_token(signing_key, iss="https://other-issuer.example.com")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "new-at",
            "id_token": bad_id_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        status=401, text="invalid_token"
    )

    result = await state._get_userinfo()

    assert result is None
    # Only the initial userinfo attempt is made; retry is skipped because
    # validation fails after refresh.
    assert sum(1 for c in fake_client.get_calls if c["url"] == USERINFO_URL) == 1
    assert sum(1 for c in fake_client.post_calls if c["url"] == TOKEN_URL) == 1
    # reset_auth is triggered now that tokens are no longer valid.
    stub_call_event_from_computed_var.assert_awaited()


async def test_get_userinfo_invalid_when_only_id_token_present(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """An ID token without an access token should fail validation immediately."""
    state._id_token = make_id_token(signing_key)

    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    # No userinfo call, no refresh attempt.
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)
    assert fake_client.post_calls == []


async def test_get_userinfo_invalid_when_only_access_token_present(
    state, fake_client, stub_call_event_from_computed_var
):
    """An access token without an ID token should fail validation immediately."""
    state._access_token_data = access_token_data("at-1")

    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)
    assert fake_client.post_calls == []


async def test_get_userinfo_invalid_when_access_token_data_is_malformed(
    state, fake_client, signing_key, stub_call_event_from_computed_var
):
    """A malformed access_token_data cookie should be treated as no access token."""
    state._access_token_data = "this is not a valid query string=&&&"
    state._id_token = make_id_token(signing_key)

    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)


async def test_get_userinfo_id_token_signed_by_wrong_key_is_rejected(
    state, fake_client, stub_call_event_from_computed_var
):
    """An ID token signed by a key not present in the JWKS should be rejected."""
    other_key = jwk.RSAKey.generate_key(2048, parameters={"kid": "other-kid"})
    state._access_token_data = access_token_data("at-1")
    state._id_token = make_id_token(other_key)

    result = await state._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    assert all(call["url"] != USERINFO_URL for call in fake_client.get_calls)


async def test_get_userinfo_uses_id_token_claims_after_refresh_when_no_userinfo_endpoint(
    state, fake_client, signing_key, metadata, stub_call_event_from_computed_var
):
    """Without a userinfo endpoint, refresh-then-claims should still work."""
    metadata.pop("userinfo_endpoint")
    state._access_token_data = access_token_data("expired-at", expires_in=-10)
    state._id_token = make_id_token(signing_key, exp_offset=-10)
    state._refresh_token = "refresh-1"
    new_id_token = make_id_token(signing_key, sub="claims-after-refresh")
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "new-at",
            "id_token": new_id_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )

    result = await state._get_userinfo()

    assert result is not None
    assert result["sub"] == "claims-after-refresh"
    stub_call_event_from_computed_var.assert_not_called()


async def test_redirect_to_login_does_not_toast_when_userinfo_fetch_fails(
    state, fake_client, signing_key, stub_call_event_from_computed_var, monkeypatch
):
    """When userinfo cannot be fetched, redirect_to_login should not toast "logged in"."""
    state._access_token_data = access_token_data("at-1")
    state._id_token = make_id_token(signing_key)
    fake_client.get_responses[USERINFO_URL] = FakeResponse(
        status=401, text="invalid_token"
    )

    async def _no_popup(self):
        return False

    monkeypatch.setattr(UserinfoAuthState, "_use_popup_flow", _no_popup)

    result = await state.redirect_to_login()

    # No "You are logged in" toast should appear in the result.
    assert "You are logged in" not in repr(result)
    # The authorization-request branch should still build a redirect to the
    # provider's authorize endpoint — otherwise a silent failure there would
    # let this test pass with result=None.
    assert result is not None
    assert AUTHORIZATION_URL in repr(result)
    # Tokens were present but userinfo failed, so reset_auth must be queued.
    stub_call_event_from_computed_var.assert_awaited()
    reset_targets = [
        call.args[1]
        for call in stub_call_event_from_computed_var.await_args_list
        if len(call.args) >= 2
    ]
    assert any(target is UserinfoAuthState.reset_auth for target in reset_targets), (
        reset_targets
    )


async def test_get_userinfo_refresh_sends_expected_token_request(
    state, fake_client, signing_key
):
    """Verify the refresh token POST contains the expected payload."""
    state._access_token_data = access_token_data("expired-at", expires_in=-10)
    state._id_token = make_id_token(signing_key, exp_offset=-10)
    state._refresh_token = "refresh-original"
    new_id_token = make_id_token(signing_key)
    fake_client.post_responses[TOKEN_URL] = FakeResponse(
        json_data={
            "access_token": "new-at",
            "id_token": new_id_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }
    )
    fake_client.get_responses[USERINFO_URL] = FakeResponse(json_data={"sub": "user-1"})

    await state._get_userinfo()

    refresh_calls = [c for c in fake_client.post_calls if c["url"] == TOKEN_URL]
    assert len(refresh_calls) == 1
    payload = refresh_calls[0]["data"]
    assert payload["grant_type"] == "refresh_token"
    assert payload["refresh_token"] == "refresh-original"
    assert payload["client_id"] == AUDIENCE
    headers = refresh_calls[0]["headers"]
    assert headers["Content-Type"] == "application/x-www-form-urlencoded"


async def test_get_userinfo_resets_auth_through_state_proxy(
    state, fake_client, stub_call_event_from_computed_var
):
    """Regression test for ENG-9663.

    When the state is reached through a ``StateProxy`` (e.g. from a background
    task), ``type(self)`` is the proxy class, which has no event handlers, so
    ``type(self).reset_auth`` raised ``AttributeError``. The handlers must use
    ``self.__class__`` so the lookup resolves through the proxy to the wrapped
    state's real class. This exercises ``_get_userinfo`` (the path in the
    original traceback) with ``self`` wrapped in such a proxy.
    """
    proxy = _RebindingStateProxy(state)
    # Sanity check that the proxy actually reproduces the failure condition:
    # the bare proxy type has no event handler, but self.__class__ does.
    assert type(proxy) is _RebindingStateProxy
    assert proxy.__class__ is type(state)
    assert not hasattr(type(proxy), "reset_auth")
    assert hasattr(proxy.__class__, "reset_auth")

    # No tokens -> reset_auth must be resolved and chained without raising
    # AttributeError on the proxy type.
    result = await proxy._get_userinfo()

    assert result is None
    stub_call_event_from_computed_var.assert_awaited_once()
    # reset_auth was resolved via self.__class__ to the real state class.
    passed_self, passed_handler = stub_call_event_from_computed_var.call_args.args
    assert passed_self is proxy
    assert passed_handler is type(state).reset_auth
