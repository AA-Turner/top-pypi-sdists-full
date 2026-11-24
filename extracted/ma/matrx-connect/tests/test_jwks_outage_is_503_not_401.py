"""A JWKS outage is a retryable 503, never a 401 that signs a good token out.

Incident 2026-11-06 08:07-08:11 UTC: 21 agent-mail wake sessions holding valid tokens got 401
while the signing-key endpoint was unreachable. A failed key fetch (and the cooldown that follows
it) said nothing about the token, so it must surface as the retryable credential-unavailable 503.
A genuinely unknown kid, after a SUCCESSFUL fetch, stays a rejection (anonymous -> the route's 401).
"""

from __future__ import annotations

import json

import jwt
import pytest

from matrx_connect.middleware.auth import AuthMiddleware
from tests.test_auth_middleware import (
    _StubSigningKey,
    _generate_rsa_keypair,
    _make_rs256_jwt,
)
from tests.test_auth_middleware_organization_admission import _App, _call

URL = "https://example.invalid/.well-known/jwks.json"


class _DownClient:
    calls = 0

    def get_signing_keys(self, refresh: bool = False):
        self.calls += 1
        raise jwt.PyJWKClientConnectionError("Fail to fetch data from the url, err: timed out")


class _UpClient:
    def __init__(self, public_key):
        self._public_key = public_key

    def get_signing_keys(self, refresh: bool = False):
        return [_StubSigningKey(self._public_key, kid="good-kid")]


def _mw(client):
    mw = AuthMiddleware(_App(), jwt_secret="", jwks_url=URL, jwt_algorithms=("RS256",), log_requests=False)
    mw._jwks_client = client
    return mw


@pytest.mark.asyncio
async def test_failed_jwks_fetch_and_its_cooldown_are_503_not_401() -> None:
    private_key, _ = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key, kid="good-kid")
    mw = _mw(_DownClient())
    for _ in range(2):  # first = the failed fetch, second = the cooldown after it
        status, body = await _call(mw, "/ai/x", {"authorization": f"Bearer {token}"})
        assert status == 503, "a JWKS outage must not read as an invalid token"
        assert json.loads(body)["retryable"] is True


@pytest.mark.asyncio
async def test_unknown_kid_after_a_successful_fetch_is_still_401() -> None:
    private_key, public_key = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key, kid="some-other-kid")
    mw = _mw(_UpClient(public_key))
    status, _ = await _call(mw, "/ai/x", {"authorization": f"Bearer {token}"})
    # Rejected token = anonymous request; the route's own gate answers 401.
    assert status == 200
    assert mw.app.context.is_authenticated is False
