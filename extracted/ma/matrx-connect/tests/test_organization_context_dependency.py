"""Forcing proof for the route-level organization admission boundary."""

from __future__ import annotations

from typing import Annotated

import dataclasses
import asyncio

import pytest
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient
from starlette.requests import Request as StarletteRequest

from matrx_connect import (
    AppContext,
    AuthorizedResourceAdmission,
    TenantAppContext,
    context_dep,
    get_app_context,
    require_organization_context,
    require_tenant_context,
    set_app_context,
    tenant_resource_context,
    tenant_system_context,
)
from matrx_connect.emitters.silent_emitter import SilentEmitter
from matrx_connect.org_hold import (
    MEMBERSHIPS_URL,
    ORGANIZATION_REQUIRED,
    assert_no_default_org_wording,
)

ORGANIZATION_ID = "11111111-1111-4111-8111-111111111111"
OTHER_ORGANIZATION_ID = "22222222-2222-4222-8222-222222222222"


def _context(
    organization_id: str | None,
    *,
    is_admin: bool = False,
    admin_level: str | None = None,
) -> AppContext:
    return AppContext(
        emitter=SilentEmitter(),
        user_id="user-1",
        auth_type="token",
        is_authenticated=True,
        is_admin=is_admin,
        admin_level=admin_level,
        organization_id=organization_id,
        organization_admission="verified" if organization_id else "none",
    )


def _client(ctx: AppContext) -> tuple[TestClient, dict[str, int]]:
    app = FastAPI()
    calls = {"handler": 0}

    @app.middleware("http")
    async def install_context(request: Request, call_next):
        request.state.context = ctx
        token = set_app_context(ctx)
        try:
            return await call_next(request)
        finally:
            from matrx_connect import clear_app_context

            clear_app_context(token)

    router = APIRouter(dependencies=[Depends(require_organization_context)])

    @router.get("/protected")
    async def protected(
        request: Request,
        admitted: Annotated[AppContext, Depends(context_dep)],
    ) -> dict[str, str | bool | None]:
        calls["handler"] += 1
        task_context = await asyncio.create_task(asyncio.sleep(0, result=get_app_context()))
        return {
            "organization_id": admitted.organization_id,
            "is_admin": admitted.is_admin,
            "admin_level": admitted.admin_level,
            "is_tenant": isinstance(admitted, TenantAppContext),
            "same_request_context": admitted is request.state.context,
            "same_ambient_context": admitted is get_app_context(),
            "same_task_context": admitted is task_context,
        }

    app.include_router(router)
    return TestClient(app), calls


def test_openapi_demands_organization_header() -> None:
    client, _ = _client(_context(ORGANIZATION_ID))

    parameters = client.get("/openapi.json").json()["paths"]["/protected"]["get"][
        "parameters"
    ]

    assert {
        "name": "X-Organization-Id",
        "in": "header",
        "required": True,
        "schema": {"type": "string", "title": "X-Organization-Id"},
    } in parameters


def test_missing_header_is_rejected_before_handler() -> None:
    client, calls = _client(_context(ORGANIZATION_ID))

    response = client.get("/protected")

    assert response.status_code == 422
    assert calls["handler"] == 0


def test_malformed_header_is_rejected_before_handler() -> None:
    client, calls = _client(_context(ORGANIZATION_ID))

    response = client.get("/protected", headers={"X-Organization-Id": "not-a-uuid"})

    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "organization_context_invalid"
    assert calls["handler"] == 0


def test_unadmitted_context_is_HELD_with_the_one_envelope_not_a_bespoke_string() -> None:
    """The auth boundary speaks the ONE hold vocabulary, not its own.

    Before 2026-09-19 this door answered `organization_context_unresolved`, a
    string only this package used, while aidream answered the typed hold — so
    which refusal a caller got depended on which door it came through, and
    neither told the person what to choose. This asserts the envelope, so a
    regression to a bespoke string fails here by name.
    """
    client, calls = _client(_context(None))

    response = client.get(
        "/protected", headers={"X-Organization-Id": ORGANIZATION_ID}
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error"] == ORGANIZATION_REQUIRED
    assert detail["code"] == ORGANIZATION_REQUIRED
    assert detail["details"]["hold"] == ORGANIZATION_REQUIRED
    assert detail["details"]["can_choose"] is True
    assert detail["details"]["set_on"] == "request"
    assert detail["details"]["memberships_url"] == MEMBERSHIPS_URL
    # The remedy is "choose one", NEVER "set a default organization".
    assert_no_default_org_wording(detail["details"]["remedy"])
    assert_no_default_org_wording(detail["message"])
    assert_no_default_org_wording(detail["user_message"])
    assert calls["handler"] == 0


def test_mismatched_context_is_rejected_before_handler() -> None:
    client, calls = _client(_context(OTHER_ORGANIZATION_ID))

    response = client.get(
        "/protected", headers={"X-Organization-Id": ORGANIZATION_ID}
    )

    assert response.status_code == 409
    assert response.json()["detail"]["error"] == "organization_context_mismatch"
    assert calls["handler"] == 0


def test_matching_context_reaches_handler() -> None:
    client, calls = _client(_context(ORGANIZATION_ID))

    response = client.get(
        "/protected", headers={"X-Organization-Id": ORGANIZATION_ID}
    )

    assert response.status_code == 200
    assert response.json()["organization_id"] == ORGANIZATION_ID
    assert response.json()["is_tenant"] is True
    assert response.json()["same_request_context"] is True
    assert response.json()["same_ambient_context"] is True
    assert response.json()["same_task_context"] is True
    assert calls["handler"] == 1


def test_admin_uses_same_target_org_contract_and_keeps_admin_identity() -> None:
    client, calls = _client(
        _context(ORGANIZATION_ID, is_admin=True, admin_level="super_admin")
    )

    response = client.get(
        "/protected", headers={"X-Organization-Id": ORGANIZATION_ID}
    )

    assert response.status_code == 200
    assert response.json() == {
        "organization_id": ORGANIZATION_ID,
        "is_admin": True,
        "admin_level": "super_admin",
        "is_tenant": True,
        "same_request_context": True,
        "same_ambient_context": True,
        "same_task_context": True,
    }
    assert calls["handler"] == 1


def test_tenant_context_seals_every_replace_path() -> None:
    admitted = require_tenant_context(_context(ORGANIZATION_ID))

    assert admitted.organization_id == ORGANIZATION_ID
    assert admitted.with_overrides(source_feature="test").organization_id == ORGANIZATION_ID
    assert admitted.with_execution_attribution(
        "workflow_run", "33333333-3333-4333-8333-333333333333"
    ).organization_id == ORGANIZATION_ID
    assert admitted.fork_for_child_agent("44444444-4444-4444-8444-444444444444").organization_id == ORGANIZATION_ID
    assert admitted.fork_for_workflow_step("55555555-5555-4555-8555-555555555555").organization_id == ORGANIZATION_ID
    with pytest.raises(ValueError, match="cannot be replaced"):
        dataclasses.replace(admitted, organization_id=OTHER_ORGANIZATION_ID)
    with pytest.raises(ValueError, match="organization_id"):
        dataclasses.replace(admitted, organization_id=None)
    with pytest.raises(ValueError, match="provenance"):
        dataclasses.replace(admitted, organization_admission="none")
    with pytest.raises(ValueError, match="cannot be replaced"):
        admitted.with_overrides(organization_id=OTHER_ORGANIZATION_ID)
    with pytest.raises(ValueError, match="provenance"):
        admitted.with_overrides(organization_admission="none")
    with pytest.raises(AttributeError, match="not overrideable"):
        admitted.with_overrides(_organization_admission_binding=None)


def test_unverified_and_organization_free_contexts_cannot_be_promoted() -> None:
    with pytest.raises(ValueError, match="verified organization admission"):
        require_tenant_context(
            AppContext(
                emitter=SilentEmitter(),
                organization_id=ORGANIZATION_ID,
                organization_admission="unknown",
            )
        )


def test_membership_dependency_rejects_system_and_resource_tenant_provenance() -> None:
    async def mint_system() -> TenantAppContext:
        async with tenant_system_context("worker", user_id="user-1", organization_id=ORGANIZATION_ID) as ctx:
            return ctx

    system_tenant = asyncio.run(mint_system())
    resource_tenant = tenant_resource_context(
        _context(None),
        AuthorizedResourceAdmission(
            principal="user-1",
            organization_id=ORGANIZATION_ID,
            resource_token="note",
            resource_id="33333333-3333-4333-8333-333333333333",
            operation="read",
            access_level="viewer",
            adapter_id="workbench.notes",
        ),
    )
    for tenant in (system_tenant, resource_tenant):
        client, calls = _client(tenant)
        response = client.get("/protected", headers={"X-Organization-Id": ORGANIZATION_ID})
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert detail["error"] == ORGANIZATION_REQUIRED
        assert detail["details"]["hold"] == ORGANIZATION_REQUIRED
        assert calls["handler"] == 0


@pytest.mark.asyncio
async def test_admission_generator_restores_request_and_ambient_context_after_error() -> None:
    base = _context(ORGANIZATION_ID)
    request = StarletteRequest(
        {"type": "http", "method": "GET", "path": "/protected", "headers": []}
    )
    request.state.context = base
    root_token = set_app_context(base)
    dependency = require_organization_context(request, ORGANIZATION_ID)
    try:
        admitted = await anext(dependency)
        assert request.state.context is admitted
        assert get_app_context() is admitted
        await dependency.athrow(ValueError("handler failed"))
    except ValueError as exc:
        assert str(exc) == "handler failed"
    finally:
        assert request.state.context is base
        assert get_app_context() is base
        from matrx_connect import clear_app_context

        clear_app_context(root_token)
