"""THE ADMIN LANE reads as the lane even when the admin is a MEMBER of the platform tenant.

The break this catches (2026-10-08): admin-reach doors ask
``organization_admitted_by == "admin_lane"`` (``admin_lane_active``). The middleware
set that marker only when membership REFUSED the claimed organization, so a platform
admin who is also a member of the platform tenant was admitted by membership, the
marker was never set, and every admin door refused them on an admin page. Now a
membership-admitted request that carries ``x-matrx-admin-lane: 1`` still asks the
host's lane hook (which re-verifies tenant + admin registry and audits); a yes marks
the lane, a no or no header leaves plain membership — never a demotion.
"""

from __future__ import annotations

import time

import jwt
import pytest
from matrx_connect.context.app_context import admin_lane_active, try_get_app_context
from matrx_connect.middleware.auth import AuthMiddleware

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
USER_ID = "11111111-1111-4111-8111-111111111111"
TENANT = "39c38960-d30c-4840-b0c1-c9960de95582"


class _App:
    def __init__(self) -> None:
        self.ctx = None

    async def __call__(self, scope, receive, send) -> None:
        self.ctx = try_get_app_context()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def _token() -> str:
    return jwt.encode(
        {"sub": USER_ID, "aud": "authenticated", "exp": int(time.time()) + 3600},
        JWT_SECRET,
        algorithm="HS256",
    )


async def _member_of_tenant(user_id: str, claimed: str | None) -> str | None:
    return TENANT if claimed == TENANT else None


async def _is_admin(user_id: str) -> bool:
    return True


def _mw(app: _App, verdict: bool, calls: list[str]) -> AuthMiddleware:
    async def _lane(user_id: str, organization_id: str) -> bool:
        calls.append(organization_id)
        return verdict

    return AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        resolve_active_organization=_member_of_tenant,
        admin_lane_admission=_lane,
        log_requests=False,
    )


async def _call(mw: AuthMiddleware, *, lane_header: bool) -> None:
    headers = {"authorization": f"Bearer {_token()}", "x-organization-id": TENANT}
    if lane_header:
        headers["x-matrx-admin-lane"] = "1"

    async def send(message: dict) -> None:
        return None

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/ai/runs",
        "query_string": b"",
        "headers": [(k.encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }
    await mw(scope, receive, send)


@pytest.mark.asyncio
async def test_a_tenant_member_admin_on_the_lane_reads_as_the_lane() -> None:
    app, calls = _App(), []
    await _call(_mw(app, True, calls), lane_header=True)
    assert calls == [TENANT]
    assert app.ctx is not None
    assert app.ctx.organization_id == TENANT
    assert app.ctx.metadata.get("organization_admitted_by") == "admin_lane"
    assert admin_lane_active(app.ctx, user_id=USER_ID) is True


@pytest.mark.asyncio
async def test_no_header_is_plain_membership_and_never_asks_the_hook() -> None:
    app, calls = _App(), []
    await _call(_mw(app, True, calls), lane_header=False)
    assert calls == []
    assert app.ctx.organization_id == TENANT
    assert "organization_admitted_by" not in (app.ctx.metadata or {})
    assert admin_lane_active(app.ctx, user_id=USER_ID) is False


@pytest.mark.asyncio
async def test_a_refused_lane_leaves_membership_untouched() -> None:
    app, calls = _App(), []
    await _call(_mw(app, False, calls), lane_header=True)
    assert calls == [TENANT]
    assert app.ctx.organization_id == TENANT
    assert app.ctx.organization_admission == "verified"
    assert admin_lane_active(app.ctx, user_id=USER_ID) is False
