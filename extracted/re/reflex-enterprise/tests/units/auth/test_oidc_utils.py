"""Unit tests for reflex_enterprise.auth.oidc.utils.verify_jwt."""

import time

import pytest
from joserfc import jwk, jwt
from joserfc.errors import InvalidClaimError

from reflex_enterprise.auth.oidc import utils as oidc_utils
from reflex_enterprise.auth.oidc.utils import verify_jwt

ISSUER_COMMON = "https://login.microsoftonline.com/common/v2.0"
ISSUER_TENANT = (
    "https://login.microsoftonline.com/11111111-2222-3333-4444-555555555555/v2.0"
)
AUDIENCE = "test-client-id"


@pytest.fixture
def signing_key() -> jwk.RSAKey:
    return jwk.RSAKey.generate_key(2048, parameters={"kid": "test-kid"})


@pytest.fixture
def jwks(signing_key: jwk.RSAKey) -> dict:
    return {"keys": [signing_key.as_dict(private=False)]}


@pytest.fixture
def fake_http_client(jwks: dict):
    class _FakeResponse:
        def __init__(self, payload: dict):
            self._payload = payload
            self.status = 200

        async def json(self):
            return self._payload

        async def text(self):
            return ""

    class _FakeCtx:
        def __init__(self, payload: dict):
            self._payload = payload

        async def __aenter__(self):
            return _FakeResponse(self._payload)

        async def __aexit__(self, *args):
            return None

    class _FakeClient:
        def __init__(self):
            self.jwks_uri = "https://example/jwks"

        def get(self, url, *, headers=None):
            if url.endswith("/.well-known/openid-configuration"):
                return _FakeCtx({"jwks_uri": self.jwks_uri})
            if url == self.jwks_uri:
                return _FakeCtx(jwks)
            raise AssertionError(f"unexpected GET {url}")

        def post(self, url, *, headers=None, data=None):
            raise AssertionError("unexpected POST")

    return _FakeClient()


@pytest.fixture(autouse=True)
def _clear_oidc_cache():
    oidc_utils._OIDC_CACHE.clear()
    yield
    oidc_utils._OIDC_CACHE.clear()


def _make_token(signing_key: jwk.RSAKey, *, iss: str, aud: str = AUDIENCE) -> str:
    now = int(time.time())
    claims = {
        "iss": iss,
        "aud": aud,
        "sub": "user-1",
        "iat": now,
        "exp": now + 600,
    }
    return jwt.encode({"alg": "RS256", "kid": signing_key.kid}, claims, signing_key)


async def test_verify_jwt_default_accepts_matching_iss(signing_key, fake_http_client):
    token = _make_token(signing_key, iss=ISSUER_COMMON)
    result = await verify_jwt(
        token, issuer=ISSUER_COMMON, audience=AUDIENCE, client=fake_http_client
    )
    assert result.claims["iss"] == ISSUER_COMMON


async def test_verify_jwt_default_accepts_trailing_slash_iss(
    signing_key, fake_http_client
):
    token = _make_token(signing_key, iss=ISSUER_COMMON + "/")
    result = await verify_jwt(
        token, issuer=ISSUER_COMMON, audience=AUDIENCE, client=fake_http_client
    )
    assert result.claims["iss"] == ISSUER_COMMON + "/"


async def test_verify_jwt_default_rejects_mismatched_iss(signing_key, fake_http_client):
    token = _make_token(signing_key, iss=ISSUER_TENANT)
    with pytest.raises(InvalidClaimError):
        await verify_jwt(
            token, issuer=ISSUER_COMMON, audience=AUDIENCE, client=fake_http_client
        )


async def test_verify_jwt_valid_issuers_accepts_tenant_token(
    signing_key, fake_http_client
):
    token = _make_token(signing_key, iss=ISSUER_TENANT)
    result = await verify_jwt(
        token,
        issuer=ISSUER_COMMON,
        audience=AUDIENCE,
        client=fake_http_client,
        valid_issuers=[ISSUER_TENANT],
    )
    assert result.claims["iss"] == ISSUER_TENANT


async def test_verify_jwt_valid_issuers_rejects_non_listed_iss(
    signing_key, fake_http_client
):
    bad_iss = (
        "https://login.microsoftonline.com/00000000-0000-0000-0000-000000000000/v2.0"
    )
    token = _make_token(signing_key, iss=bad_iss)
    with pytest.raises(InvalidClaimError):
        await verify_jwt(
            token,
            issuer=ISSUER_COMMON,
            audience=AUDIENCE,
            client=fake_http_client,
            valid_issuers=[ISSUER_TENANT],
        )
