"""Verified credential expiry must survive admission, including warm JWT caches."""

import time

import httpx
import jwt
import pytest
from matrx_connect.middleware.auth import ApiKeyIdentity, AuthMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

SECRET = "synthetic-source-expiry-test-key-not-a-real-secret"
USER = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"
ORG = "00000000-0000-4000-8000-000000000003"


async def _request(middleware, credential, **headers):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=middleware), base_url="http://test"
    ) as client:
        return await client.get(
            "/health", headers={"Authorization": f"Bearer {credential}", **headers}
        )


async def _provenance(request):
    ctx = request.state.context
    return JSONResponse({"auth_type": ctx.auth_type, "metadata": ctx.metadata})


@pytest.mark.asyncio
async def test_cold_and_warm_jwt_admission_preserve_verified_expiry_not_request_header():
    expiry = int(time.time()) + 3600
    bearer = jwt.encode(
        {"sub": USER, "session_id": SESSION, "aud": "authenticated", "exp": expiry},
        SECRET,
        algorithm="HS256",
    )
    middleware = AuthMiddleware(
        Starlette(routes=[Route("/health", _provenance)]), jwt_secret=SECRET, log_requests=False
    )
    for _ in range(2):
        response = await _request(middleware, bearer, **{"X-JWT-Expires-At": "9999999999"})
        assert response.status_code == 200
        metadata = response.json()["metadata"]
        assert metadata["jwt_claims"]["session_id"] == SESSION
        assert "exp" not in metadata["jwt_claims"]
        assert metadata["jwt_expires_at"] == expiry
    assert middleware._token_cache


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["service", "personal"])
@pytest.mark.parametrize("expiry", [None, 2_000_000_000])
async def test_both_key_lanes_carry_resolver_expiry_without_accepting_header_override(kind, expiry):
    async def resolve(raw):
        assert raw == "mx_live_syntheticKey_secret"
        return ApiKeyIdentity(USER, ORG, key_id="syntheticKey", kind=kind, expires_at=expiry)

    async def membership(user, claimed):
        return ORG

    middleware = AuthMiddleware(
        Starlette(routes=[Route("/health", _provenance)]),
        jwt_secret=SECRET,
        resolve_api_key=resolve,
        resolve_active_organization=membership,
        log_requests=False,
    )
    response = await _request(
        middleware, "mx_live_syntheticKey_secret", **{"X-API-Key-Expires-At": "9999999999"}
    )
    assert response.status_code == 200
    assert response.json()["auth_type"] == "api_key"
    assert response.json()["metadata"]["api_key_expires_at"] == expiry
    assert response.json()["metadata"]["api_key_id"] == "syntheticKey"
