"""A PERSONAL API key IS its person, and its organization is verified like a sign-in's.

TABLE-API-1 (2026-09-29). A service key's organization is the key's; a personal key only
carries the organization it was configured to work in, and every request's organization goes
through the SAME membership resolver a JWT's does:

* no header → the key's configured organization, verified — admitted when a member;
* a header naming another organization the person belongs to → that one (no 409);
* a header or configured organization the person does NOT belong to → denied, never the
  key's organization substituted;
* the admin tier is never resolved for a key.
"""

from __future__ import annotations

import pytest
from matrx_connect.middleware.auth import ApiKeyIdentity, ApiKeyRefused, AuthMiddleware

PERSON = "55555555-5555-4555-8555-555555555555"
HOME_ORG = "33333333-3333-4333-8333-333333333333"
OTHER_MEMBER_ORG = "66666666-6666-4666-8666-666666666666"
NOT_A_MEMBER_ORG = "44444444-4444-4444-8444-444444444444"
PERSONAL_KEY = "mx_live_personalKey01_" + "p" * 43


REVOKED_KEY = "mx_live_revokedKey01_" + "r" * 43


async def _resolver(token: str) -> ApiKeyIdentity | None:
    if token == REVOKED_KEY:
        raise ApiKeyRefused("This key was revoked 2 hours ago. Make a new one in Settings, API keys.")
    if token == PERSONAL_KEY:
        return ApiKeyIdentity(
            user_id=PERSON, organization_id=HOME_ORG, key_id="personalKey01",
            key_name="tracker", kind="personal",
        )
    return None


async def _membership(user_id: str, claimed: str | None) -> str | None:
    if user_id == PERSON and claimed in (HOME_ORG, OTHER_MEMBER_ORG):
        return claimed
    return None


async def _admin_level(user_id: str) -> str | None:  # a platform admin, on purpose
    return "super_admin"


class _App:
    def __init__(self) -> None:
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


async def _call(mw: AuthMiddleware, headers: dict[str, str]) -> int:
    sent: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        sent.append(message)

    scope = {
        "type": "http", "method": "GET", "path": "/v1/tables", "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 1), "state": {},
    }
    await mw(scope, receive, send)
    return next(m["status"] for m in sent if m["type"] == "http.response.start")


def _mw(app: _App) -> AuthMiddleware:
    return AuthMiddleware(
        app,
        jwt_secret="x" * 64,
        resolve_api_key=_resolver,
        resolve_active_organization=_membership,
        admin_level_resolver=_admin_level,
        log_requests=False,
    )


@pytest.mark.asyncio
async def test_no_header_admits_the_keys_configured_org_after_membership_check() -> None:
    app = _App()
    await _call(_mw(app), {"authorization": f"Bearer {PERSONAL_KEY}"})
    ctx = app.context
    assert ctx.user_id == PERSON
    assert ctx.auth_type == "api_key"
    assert ctx.organization_id == HOME_ORG
    assert ctx.organization_admission == "verified"
    assert ctx.metadata["api_key_kind"] == "personal"


@pytest.mark.asyncio
async def test_header_naming_another_membership_is_used_not_refused() -> None:
    app = _App()
    await _call(_mw(app), {"authorization": f"Bearer {PERSONAL_KEY}", "x-organization-id": OTHER_MEMBER_ORG})
    assert app.context.organization_id == OTHER_MEMBER_ORG
    assert app.context.organization_admission == "verified"


@pytest.mark.asyncio
async def test_header_naming_a_foreign_org_is_denied_never_substituted() -> None:
    app = _App()
    await _call(_mw(app), {"authorization": f"Bearer {PERSONAL_KEY}", "x-organization-id": NOT_A_MEMBER_ORG})
    ctx = app.context
    assert ctx is None or ctx.organization_id != HOME_ORG
    if ctx is not None:
        assert ctx.organization_admission == "denied"


@pytest.mark.asyncio
async def test_a_personal_key_never_carries_the_admin_tier() -> None:
    app = _App()
    await _call(_mw(app), {"authorization": f"Bearer {PERSONAL_KEY}"})
    assert app.context.is_admin is False
    assert app.context.admin_level is None


@pytest.mark.asyncio
async def test_a_revoked_key_reaches_the_route_gate_with_its_reason() -> None:
    """The request stays unauthenticated, and require_authenticated answers the key's own reason."""
    from fastapi import HTTPException
    from matrx_connect.dependencies import require_authenticated
    from types import SimpleNamespace

    app = _App()
    await _call(_mw(app), {"authorization": f"Bearer {REVOKED_KEY}"})
    ctx = app.context
    assert ctx.is_authenticated is False
    with pytest.raises(HTTPException) as refused:
        await require_authenticated(SimpleNamespace(state=SimpleNamespace(context=ctx)))
    assert refused.value.status_code == 401
    assert refused.value.detail["error"] == "api_key_refused"
    assert refused.value.detail["message"].startswith("This key was revoked")

