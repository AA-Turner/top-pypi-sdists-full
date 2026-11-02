"""Forcing proof for isolated authorized resource-operation contexts."""

from __future__ import annotations

import asyncio
import dataclasses
from contextvars import ContextVar

import pytest

from matrx_connect import (
    AppContext,
    AuthorizedResourceAdmission,
    OrganizationFreeAppContext,
    TenantAppContext,
    authorized_guest_resource_operation,
    authorized_resource_operation,
    get_app_context,
    set_app_context,
    tenant_resource_context,
)
from matrx_connect.emitters.silent_emitter import SilentEmitter

ORG_A = "11111111-1111-4111-8111-111111111111"
ORG_B = "22222222-2222-4222-8222-222222222222"
RESOURCE_ID = "33333333-3333-4333-8333-333333333333"


def _parent(**overrides: object) -> AppContext:
    fields: dict[str, object] = {
        "emitter": SilentEmitter(),
        "user_id": "principal-a",
        "email": "person@example.test",
        "auth_type": "token",
        "is_authenticated": True,
        "is_admin": True,
        "admin_level": "super_admin",
        "is_minor": True,
        "fingerprint_id": "fingerprint-a",
        "ip_address": "127.0.0.1",
        "user_agent": "test-agent",
        "token": "token-a",
        "request_id": "request-a",
        "operation_id": "parent-operation",
        "route": "/virtual/notes/id",
        "source_app": "notes",
        "source_feature": "virtual-files",
        "organization_id": ORG_A,
        "organization_admission": "verified",
        "claimed_organization_id": ORG_A,
        "project_id": "project-a",
        "task_id": "task-a",
        "execution_kind": "workflow_run",
        "execution_id": "44444444-4444-4444-8444-444444444444",
        "metadata": {"unsafe": "metadata"},
        "api_keys": {"provider": "secret"},
        "conversation_id": "conversation-a",
        "parent_conversation_id": "conversation-parent",
        "parent_request_id": "parent-request",
        "is_internal_agent": True,
        "conversation_type": "workflow",
        "initial_variables": {"unsafe": "variables"},
        "initial_overrides": {"unsafe": "overrides"},
        "agent_id": "agent-a",
        "agent_version_id": "agent-version-a",
        "workflow_definition_version_id": "workflow-version-a",
        "client_tools": ["tool-a"],
        "block_mode": True,
        "snapshot": True,
        "memory_enabled": True,
        "memory_model": "memory-model",
        "memory_scope": "organization",
        "origin_class": "human",
        "store": False,
        "system_run": True,
        "debug": True,
    }
    fields.update(overrides)
    return AppContext(**fields)  # type: ignore[arg-type]


def _admission(**overrides: object) -> AuthorizedResourceAdmission:
    fields: dict[str, object] = {
        "principal": "principal-a",
        "organization_id": ORG_B,
        "resource_token": "note",
        "resource_id": RESOURCE_ID,
        "operation": "write",
        "access_level": "editor",
        "adapter_id": "workbench.notes",
    }
    fields.update(overrides)
    return AuthorizedResourceAdmission(**fields)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_operation_uses_only_the_identity_allowlist_and_fresh_tenant() -> None:
    parent = _parent()
    unrelated: ContextVar[object] = ContextVar("unrelated_resource_operation", default=object())
    unrelated_value = object()
    unrelated_token = unrelated.set(unrelated_value)
    ambient_token = set_app_context(parent)
    try:
        async with authorized_resource_operation(parent, _admission(), expected_organization_id=ORG_B) as resource:
            assert get_app_context() is resource
            assert resource.organization_id == ORG_B
            assert resource.operation_id != parent.operation_id
            assert resource.request_id == parent.request_id
            assert resource.metadata == {"resource_operation_parent_operation_id": parent.operation_id}
            assert resource.metadata is not parent.metadata
            assert unrelated.get() is unrelated_value
            for field in (
                "emitter", "user_id", "email", "auth_type", "is_admin", "admin_level", "is_minor",
                "fingerprint_id", "ip_address", "user_agent", "token", "route", "source_app", "source_feature",
            ):
                assert getattr(resource, field) == getattr(parent, field)
            assert resource.project_id is None and resource.task_id is None
            assert resource.execution_kind is None and resource.execution_id is None
            assert resource.conversation_id is None and resource.parent_conversation_id is None
            assert resource.parent_request_id is None and resource.agent_id is None
            assert resource.agent_version_id is None and resource.workflow_definition_version_id is None
            assert resource.api_keys == {} and resource.initial_variables == {} and resource.initial_overrides == {}
            assert resource.client_tools == [] and resource.origin_class == ""
            assert resource.api_keys is not parent.api_keys
            assert resource.initial_variables is not parent.initial_variables
            assert resource.initial_overrides is not parent.initial_overrides
            assert resource.client_tools is not parent.client_tools
            resource.api_keys["new"] = "value"
            resource.initial_variables["new"] = "value"
            resource.initial_overrides["new"] = "value"
            resource.client_tools.append("new")
            assert parent.api_keys == {"provider": "secret"}
            assert parent.initial_variables == {"unsafe": "variables"}
            assert parent.initial_overrides == {"unsafe": "overrides"}
            assert parent.client_tools == ["tool-a"]
            assert resource.store is True and resource.system_run is False
            assert resource.snapshot is None and resource.memory_enabled is False and resource.memory_model is None
            assert resource.memory_scope == "thread" and resource.block_mode is False and resource.debug is False
            resource.metadata["changed"] = True
            assert "changed" not in parent.metadata
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(ambient_token)
        unrelated.reset(unrelated_token)
    assert unrelated.get() is not unrelated_value


@pytest.mark.asyncio
async def test_operation_restores_nested_success_error_and_cancellation_contexts() -> None:
    parent = _parent()
    parent_token = set_app_context(parent)
    try:
        async with authorized_resource_operation(parent, _admission()) as outer:
            assert get_app_context() is outer
            async with authorized_resource_operation(outer, _admission()) as inner:
                assert get_app_context() is inner
                assert inner.operation_id != outer.operation_id
            assert get_app_context() is outer
            with pytest.raises(RuntimeError, match="boom"):
                async with authorized_resource_operation(outer, _admission()):
                    raise RuntimeError("boom")
            assert get_app_context() is outer

            entered = asyncio.Event()

            async def cancelled_operation() -> None:
                async with authorized_resource_operation(outer, _admission()):
                    entered.set()
                    await asyncio.Event().wait()

            task = asyncio.create_task(cancelled_operation())
            await entered.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert get_app_context() is outer
    finally:
        from matrx_connect import clear_app_context

        clear_app_context(parent_token)


@pytest.mark.asyncio
async def test_operations_are_concurrent_and_do_not_leak_ambient_context() -> None:
    parent = _parent()

    async def run(number: int) -> tuple[str, str]:
        async with authorized_resource_operation(parent, _admission()) as resource:
            before = resource.operation_id
            await asyncio.sleep(0)
            return before, get_app_context().operation_id

    results = await asyncio.gather(*(run(index) for index in range(10)))
    operation_ids = {before for before, after in results if before == after}
    assert len(operation_ids) == len(results)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("parent", "admission", "expected", "error"),
    [
        (_parent(is_authenticated=False), _admission(), None, "authenticated parent"),
        (_parent(user_id="principal-b"), _admission(), None, "does not match"),
        (_parent(organization_admission="malformed"), _admission(), None, "malformed"),
        (_parent(), _admission(), ORG_A, "expected_organization_id does not match"),
    ],
)
async def test_operation_refuses_bad_identity_or_new_resource_claim(
    parent: AppContext,
    admission: AuthorizedResourceAdmission,
    expected: str | None,
    error: str,
) -> None:
    with pytest.raises(ValueError, match=error):
        async with authorized_resource_operation(parent, admission, expected_organization_id=expected):
            pass


@pytest.mark.asyncio
async def test_operation_accepts_sealed_parent_from_a_different_tenant() -> None:
    sealed_parent = tenant_resource_context(
        _parent(organization_id=None, organization_admission="none", claimed_organization_id=None),
        _admission(organization_id=ORG_A),
    )
    async with authorized_resource_operation(sealed_parent, _admission(), expected_organization_id=ORG_B) as resource:
        assert isinstance(resource, TenantAppContext)
        assert sealed_parent.organization_id == ORG_A
        assert resource.organization_id == ORG_B


@pytest.mark.asyncio
async def test_operation_rejects_organization_free_untyped_and_forged_tenant_inputs() -> None:
    free = OrganizationFreeAppContext(emitter=SilentEmitter(), user_id="principal-a", is_authenticated=True)
    with pytest.raises(ValueError, match="organization-free"):
        async with authorized_resource_operation(free, _admission()):
            pass
    with pytest.raises(ValueError, match="parent_context"):
        async with authorized_resource_operation(object(), _admission()):  # type: ignore[arg-type]
            pass

    sealed = tenant_resource_context(
        _parent(organization_id=None, organization_admission="none", claimed_organization_id=None),
        _admission(organization_id=ORG_A),
    )
    with pytest.raises(ValueError, match="private binding"):
        dataclasses.replace(sealed, _tenant_context_seal=None)
    with pytest.raises(ValueError, match="typed admitted provenance"):
        TenantAppContext(**dataclasses.asdict(sealed))


def _guest_parent(**overrides: object) -> AppContext:
    fields: dict[str, object] = {
        "emitter": SilentEmitter(),
        "user_id": "principal-a",
        "auth_type": "fingerprint",
        "is_authenticated": False,
        "fingerprint_id": "fingerprint-a",
        "request_id": "guest-request",
        "operation_id": "guest-operation",
        "route": "/seo/public/runs/id/rejoin",
    }
    fields.update(overrides)
    return AppContext(**fields)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_guest_operation_seals_only_host_authorized_resource_tenancy() -> None:
    parent = _guest_parent()
    async with authorized_guest_resource_operation(parent, _admission()) as resource:
        assert isinstance(resource, TenantAppContext)
        assert resource.auth_type == "fingerprint"
        assert resource.is_authenticated is False
        assert resource.organization_id == ORG_B
        assert resource.user_id == parent.user_id
        assert resource.operation_id != parent.operation_id
        assert resource.metadata == {"resource_operation_parent_operation_id": parent.operation_id}
        assert resource.project_id is None and resource.task_id is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("parent", "admission", "error"),
    [
        (_guest_parent(auth_type="anonymous"), _admission(), "fingerprint guest"),
        (_guest_parent(is_authenticated=True), _admission(), "fingerprint guest"),
        (_guest_parent(organization_id=ORG_A, organization_admission="verified"), _admission(), "must not carry"),
        (_guest_parent(user_id="principal-b"), _admission(), "does not match"),
    ],
)
async def test_guest_operation_refuses_non_guest_claims_and_cross_principal_admission(
    parent: AppContext, admission: AuthorizedResourceAdmission, error: str
) -> None:
    with pytest.raises(ValueError, match=error):
        async with authorized_guest_resource_operation(parent, admission):
            pass
