"""A fresh login decision must replace warm cached administrator authority."""

import time
from dataclasses import FrozenInstanceError

import httpx
import jwt
import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.session_authority import (
    CurrentSessionDecision,
)

SECRET = "owned-current-admin-test-key-with-32-bytes"
SUBJECT = "00000000-0000-4000-8000-000000000011"
SESSION = "00000000-0000-4000-8000-000000000012"


def bearer():
    return jwt.encode(
        {
            "sub": SUBJECT,
            "session_id": SESSION,
            "aal": "aal2",
            "aud": "authenticated",
            "exp": int(time.time()) + 3600,
        },
        SECRET,
        algorithm="HS256",
    )


@pytest.mark.asyncio
async def test_warm_cache_tracks_role_removal_tier_change_and_mfa_downgrade():
    state = CurrentSessionDecision(True, "super_admin", True, True, "admitted")
    calls = 0

    async def resolve(verified):
        nonlocal calls
        calls += 1
        return state

    async def stale_role(_):
        return "super_admin"

    verifier = AuthMiddleware(
        lambda *_: None,
        jwt_secret=SECRET,
        admin_level_resolver=stale_role,
        resolve_current_session=resolve,
        log_requests=False,
    )
    token = bearer()
    first = await verifier.verify_token_raw(token)
    assert first and first.is_admin and first.admin_level == "super_admin"
    assert verifier._token_cache
    for state, effective in [
        (CurrentSessionDecision(True, "developer", True, True, "admitted"), "developer"),
        (CurrentSessionDecision(True, "super_admin", False, True, "insufficient_aal"), None),
        (CurrentSessionDecision(True, "super_admin", False, False, "support_session"), None),
        (CurrentSessionDecision(True, None, False, True, "not_admin"), None),
    ]:
        current = await verifier.verify_token_raw(token)
        assert current and current.user_id == SUBJECT
        assert current.admin_level == effective
        assert current.is_admin == (effective is not None)
        assert current.session_decision == state
    state = CurrentSessionDecision(False, None, False, True, "session_ended")
    assert await verifier.verify_token_raw(token) is None
    assert calls == 6
    assert first.is_admin and first.admin_level == "super_admin"
    with pytest.raises(FrozenInstanceError):
        first.session_decision.reason = "changed"


@pytest.mark.asyncio
async def test_boolean_login_authority_cannot_preserve_an_admin_grant():
    async def login(_):
        return True

    async def stale_role(_):
        return "super_admin"

    verifier = AuthMiddleware(
        lambda *_: None,
        jwt_secret=SECRET,
        admin_level_resolver=stale_role,
        resolve_current_session=login,
        log_requests=False,
    )
    for _ in range(2):
        result = await verifier.verify_token_raw(bearer())
        assert (
            result
            and result.user_id == SUBJECT
            and not result.is_admin
            and result.admin_level is None
        )
        assert result.session_decision.reason == "login_only"


@pytest.mark.asyncio
async def test_http_keeps_aal1_identity_without_power_and_outage_is_not_logout():
    state = CurrentSessionDecision(True, "super_admin", False, True, "insufficient_aal")

    async def authority(_):
        if state is None:
            raise RuntimeError("private authority detail")
        return state

    async def role(_):
        return "super_admin"

    async def handler(request):
        ctx = request.state.context
        return JSONResponse(
            {
                "user_id": ctx.user_id,
                "authenticated": ctx.is_authenticated,
                "admin": ctx.is_admin,
                "level": ctx.admin_level,
                "admission": ctx.metadata.get("admin_admission"),
            }
        )

    app = AuthMiddleware(
        Starlette(routes=[Route("/health", handler)]),
        jwt_secret=SECRET,
        admin_level_resolver=role,
        resolve_current_session=authority,
        log_requests=False,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health", headers={"Authorization": f"Bearer {bearer()}"})
        assert response.status_code == 200
        assert response.json() == {
            "user_id": SUBJECT,
            "authenticated": True,
            "admin": False,
            "level": None,
            "admission": {
                "admitted": False,
                "mfa_required": True,
                "reason": "insufficient_aal",
                "current_admin_level": "super_admin",
            },
        }
        state = None
        response = await client.get("/health", headers={"Authorization": f"Bearer {bearer()}"})
        assert response.status_code == 503 and response.headers["retry-after"] == "1"
        assert "private" not in response.text


@pytest.mark.parametrize(
    "args",
    [
        (True, None, True, True, "admitted"),
        (False, "super_admin", True, True, "admitted"),
        (True, "super_admin", True, None, "admitted"),
        (True, "invented", True, True, "admitted"),
        (1, None, False, None, "login_only"),
    ],
)
def test_invalid_structured_authority_cannot_be_constructed(args):
    with pytest.raises(ValueError):
        CurrentSessionDecision(*args)


@pytest.mark.asyncio
async def test_role_only_tenant_hook_cannot_restore_refused_human_admin_power():
    calls = []
    state = CurrentSessionDecision(True, "super_admin", False, True, "insufficient_aal")

    async def authority(_):
        return state

    async def hook(*args):
        calls.append(args)
        return True

    async def membership(*args):
        return None

    async def role(_):
        return "super_admin"

    async def handler(request):
        return JSONResponse({"unexpected": True})

    app = AuthMiddleware(
        Starlette(routes=[Route("/private", handler)]),
        jwt_secret=SECRET,
        admin_level_resolver=role,
        resolve_current_session=authority,
        admin_lane_admission=hook,
        resolve_active_organization=membership,
        log_requests=False,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/private",
            headers={
                "Authorization": f"Bearer {bearer()}",
                "x-organization-id": "00000000-0000-4000-8000-000000000013",
                "x-matrx-admin-lane": "1",
            },
        )
        assert response.status_code == 400 and response.json()["code"] == "organization_forbidden"
        assert calls == []
        state = CurrentSessionDecision(True, "super_admin", True, True, "admitted")
        response = await client.get(
            "/private",
            headers={
                "Authorization": f"Bearer {bearer()}",
                "x-organization-id": "00000000-0000-4000-8000-000000000013",
                "x-matrx-admin-lane": "1",
            },
        )
        assert response.status_code == 200
        assert len(calls) == 1
