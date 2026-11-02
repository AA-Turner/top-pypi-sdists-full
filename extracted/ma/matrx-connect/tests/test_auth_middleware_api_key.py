"""The API-key admission lane (`Authorization: Bearer mx_...`).

Platform tests for the ONE AuthMiddleware's branch-free API-key lane
(API-KEY-LANE-DESIGN.md, ruling C16). Locked-in behaviors:

* an ``mx_``-prefixed bearer with an injected resolver resolves to a REAL
  service identity: ``auth_type="api_key"``, ``is_authenticated=True``, and the
  key's organization admitted as the request organization
* ``X-Organization-Id`` present and EQUAL → admitted; present and DIFFERENT →
  409 with the exact ``organization_context_mismatch`` envelope; absent → the
  key's org is admitted
* a rejected key (resolver returns None) leaves the request anonymous —
  fail-closed, the route's own auth gate 401s
* a resolver that RAISES is a denied credential, never a 500
* with no resolver configured, ``mx_`` bearers fall through silently exactly
  as before (the sandbox-bridge non-JWT-bearer contract is unchanged)
* JWTs still authenticate normally with the resolver configured — the lane
  claims only ``mx_``-shaped bearers
"""

from __future__ import annotations

import time
import asyncio

import jwt
import pytest
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient
from matrx_connect import AppContext, context_dep, get_app_context, require_organization_context
from matrx_connect.context.app_context import TenantAppContext
from matrx_connect.middleware.auth import (
    ApiKeyIdentity,
    AuthMiddleware,
)

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
SERVICE_USER_ID = "22222222-2222-4222-8222-222222222222"
ORG_ID = "33333333-3333-4333-8333-333333333333"
OTHER_ORG_ID = "44444444-4444-4444-8444-444444444444"
GOOD_KEY = "mx_live_abc123DEF456_" + "s" * 43
JWT_USER_ID = "11111111-1111-4111-8111-111111111111"


async def _good_resolver(token: str) -> ApiKeyIdentity | None:
    if token == GOOD_KEY:
        return ApiKeyIdentity(
            user_id=SERVICE_USER_ID,
            organization_id=ORG_ID,
            key_id="abc123DEF456",
            key_name="ci-key",
        )
    return None


class _App:
    """Terminal ASGI app that records the request context and answers 200."""

    def __init__(self) -> None:
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        state = scope.get("state") or {}
        self.context = state.get("context")
        await send(
            {"type": "http.response.start", "status": 200, "headers": []}
        )
        await send({"type": "http.response.body", "body": b"ok"})


def _scope(headers: dict[str, str]) -> dict:
    return {
        "type": "http",
        "method": "GET",
        "path": "/auth/whoami",
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }


async def _receive() -> dict:
    return {"type": "http.request", "body": b"", "more_body": False}


async def _call(mw: AuthMiddleware, headers: dict[str, str]) -> tuple[int, bytes]:
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    await mw(_scope(headers), _receive, send)
    status = next(m["status"] for m in sent if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    return status, body


def _middleware(app: _App, *, resolver=_good_resolver) -> AuthMiddleware:
    return AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_api_key=resolver,
        log_requests=False,
    )


@pytest.mark.asyncio
async def test_valid_api_key_resolves_service_identity_and_org() -> None:
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(mw, {"authorization": f"Bearer {GOOD_KEY}"})
    assert status == 200
    ctx = app.context
    assert ctx is not None
    assert ctx.is_authenticated is True
    assert ctx.auth_type == "api_key"
    assert ctx.user_id == SERVICE_USER_ID
    assert ctx.organization_id == ORG_ID
    assert ctx.organization_admission == "verified"
    assert ctx.claimed_organization_id == ORG_ID
    assert ctx.is_admin is False
    assert ctx.metadata["api_key_id"] == "abc123DEF456"
    assert ctx.metadata["api_key_name"] == "ci-key"


@pytest.mark.asyncio
async def test_matching_org_header_is_admitted() -> None:
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(
        mw,
        {"authorization": f"Bearer {GOOD_KEY}", "x-organization-id": ORG_ID},
    )
    assert status == 200
    assert app.context.organization_id == ORG_ID


def _required_org_client() -> tuple[TestClient, dict[str, int]]:
    app = FastAPI()
    calls = {"handler": 0}
    router = APIRouter(dependencies=[Depends(require_organization_context)])

    @router.get("/required")
    async def required(
        request: Request, ctx: AppContext = Depends(context_dep)
    ) -> dict[str, bool | str]:
        calls["handler"] += 1
        task_ctx = await asyncio.create_task(asyncio.sleep(0, result=get_app_context()))
        return {
            "organization_id": ctx.organization_id,
            "tenant": isinstance(ctx, TenantAppContext),
            "same_request": ctx is request.state.context,
            "same_ambient": ctx is get_app_context(),
            "same_task": ctx is task_ctx,
        }

    app.include_router(router)
    app.add_middleware(
        AuthMiddleware,
        jwt_secret=JWT_SECRET,
        resolve_api_key=_good_resolver,
        log_requests=False,
    )
    return TestClient(app), calls


def test_api_key_required_org_router_promotes_one_shared_tenant_context() -> None:
    client, calls = _required_org_client()

    response = client.get(
        "/required",
        headers={"Authorization": f"Bearer {GOOD_KEY}", "X-Organization-Id": ORG_ID},
    )

    assert response.status_code == 200
    assert response.json() == {
        "organization_id": ORG_ID,
        "tenant": True,
        "same_request": True,
        "same_ambient": True,
        "same_task": True,
    }
    assert calls["handler"] == 1


def test_api_key_required_org_router_still_requires_the_header() -> None:
    client, calls = _required_org_client()

    response = client.get("/required", headers={"Authorization": f"Bearer {GOOD_KEY}"})

    assert response.status_code == 422
    assert calls["handler"] == 0


def test_api_key_required_org_router_preserves_mismatch_refusal() -> None:
    client, calls = _required_org_client()

    response = client.get(
        "/required",
        headers={
            "Authorization": f"Bearer {GOOD_KEY}",
            "X-Organization-Id": OTHER_ORG_ID,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"]["error"] == "organization_context_mismatch"
    assert calls["handler"] == 0


@pytest.mark.asyncio
async def test_mismatched_org_header_is_409_conflict() -> None:
    app = _App()
    mw = _middleware(app)
    status, body = await _call(
        mw,
        {"authorization": f"Bearer {GOOD_KEY}", "x-organization-id": OTHER_ORG_ID},
    )
    assert status == 409
    assert b"organization_context_mismatch" in body
    # The handler must never have run.
    assert app.context is None


@pytest.mark.asyncio
async def test_rejected_key_leaves_request_anonymous() -> None:
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(mw, {"authorization": "Bearer mx_live_nope_wrongsecret"})
    assert status == 200  # the demo app has no auth gate; the CONTEXT is what matters
    ctx = app.context
    assert ctx.is_authenticated is False
    assert ctx.user_id in (None, "")
    assert ctx.auth_type != "api_key"


@pytest.mark.asyncio
async def test_raising_resolver_is_denied_credential_not_500() -> None:
    async def _boom(token: str) -> ApiKeyIdentity | None:
        raise RuntimeError("db down")

    app = _App()
    mw = _middleware(app, resolver=_boom)
    status, _ = await _call(mw, {"authorization": f"Bearer {GOOD_KEY}"})
    assert status == 200
    assert app.context.is_authenticated is False


@pytest.mark.asyncio
async def test_no_resolver_falls_through_silently(capsys) -> None:
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, log_requests=False)
    status, _ = await _call(mw, {"authorization": f"Bearer {GOOD_KEY}"})
    assert status == 200
    assert app.context.is_authenticated is False
    captured = capsys.readouterr()
    assert "JWT validation FAILED" not in captured.out
    assert "JWT validation FAILED" not in captured.err


@pytest.mark.asyncio
async def test_jwt_lane_untouched_when_resolver_configured() -> None:
    token = jwt.encode(
        {
            "sub": JWT_USER_ID,
            "email": "user@example.com",
            "aud": "authenticated",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    app = _App()
    mw = _middleware(app)
    status, _ = await _call(mw, {"authorization": f"Bearer {token}"})
    assert status == 200
    ctx = app.context
    assert ctx.is_authenticated is True
    assert ctx.auth_type == "token"
    assert ctx.user_id == JWT_USER_ID
