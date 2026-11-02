"""Forcing proof for package-only resource-origin tenant contexts."""

from __future__ import annotations

import dataclasses

import pytest

from matrx_connect import (
    AppContext,
    AuthorizedResourceAdmission,
    OrganizationFreeAppContext,
    require_tenant_context,
    tenant_resource_context,
)
from matrx_connect.emitters.silent_emitter import SilentEmitter

ORG_ID = "11111111-1111-4111-8111-111111111111"
OTHER_ORG_ID = "22222222-2222-4222-8222-222222222222"
RESOURCE_ID = "33333333-3333-4333-8333-333333333333"


def _base(**overrides: object) -> AppContext:
    fields: dict[str, object] = {
        "emitter": SilentEmitter(),
        "user_id": "principal-a",
        "auth_type": "token",
        "is_authenticated": True,
        "request_id": "request-a",
        "operation_id": "operation-a",
        "metadata": {"source": "base"},
        "api_keys": {"key": "value"},
        "initial_variables": {"variable": "value"},
        "initial_overrides": {"override": "value"},
        "client_tools": ["tool"],
    }
    fields.update(overrides)
    return AppContext(**fields)  # type: ignore[arg-type]


def _admission(**overrides: object) -> AuthorizedResourceAdmission:
    fields: dict[str, object] = {
        "principal": "principal-a",
        "organization_id": ORG_ID,
        "resource_token": "note",
        "resource_id": RESOURCE_ID,
        "operation": "write",
        "access_level": "editor",
        "adapter_id": "workbench.notes",
    }
    fields.update(overrides)
    return AuthorizedResourceAdmission(**fields)  # type: ignore[arg-type]


def test_resource_factory_mints_distinct_sealed_operation_and_copies_mutables() -> None:
    base = _base(organization_id=ORG_ID, claimed_organization_id=ORG_ID)
    resource = tenant_resource_context(base, _admission(), organization_id=ORG_ID)

    assert resource.organization_id == ORG_ID
    assert resource.organization_admission == "none"
    assert resource.user_id == "principal-a"
    assert resource.request_id == base.request_id
    assert resource.operation_id != base.operation_id
    assert resource.metadata is not base.metadata
    assert resource.api_keys is not base.api_keys
    assert resource.initial_variables is not base.initial_variables
    assert resource.initial_overrides is not base.initial_overrides
    assert resource.client_tools is not base.client_tools
    resource.metadata["changed"] = True
    assert "changed" not in base.metadata
    assert resource.fork_for_child_agent(RESOURCE_ID)._tenant_context_seal is resource._tenant_context_seal
    assert resource.fork_for_workflow_step(RESOURCE_ID)._tenant_context_seal is resource._tenant_context_seal
    assert resource.with_execution_attribution("workflow_run", RESOURCE_ID)._tenant_provenance is resource._tenant_provenance

    with pytest.raises(ValueError, match="provenance does not match"):
        dataclasses.replace(resource, user_id="principal-b")
    with pytest.raises(ValueError, match="private binding"):
        dataclasses.replace(resource, _tenant_context_seal=None)
    with pytest.raises(ValueError, match="typed admitted provenance"):
        type(resource)(**dataclasses.asdict(resource))


@pytest.mark.parametrize(
    "changes",
    [
        {"organization_id": OTHER_ORG_ID},
        {"principal": "principal-b"},
        {"resource_token": "note_folder"},
        {"resource_id": "44444444-4444-4444-8444-444444444444"},
        {"operation": "read", "access_level": "viewer"},
        {"adapter_id": "code.files"},
    ],
)
def test_resource_seal_rejects_each_provenance_field_substitution(changes: dict[str, object]) -> None:
    resource = tenant_resource_context(_base(), _admission())
    provenance = resource._tenant_provenance
    assert provenance is not None
    replacement = type(provenance)(dataclasses.replace(provenance.admission, **changes))
    with pytest.raises(ValueError, match="tenant provenance does not match|private binding"):
        dataclasses.replace(resource, _tenant_provenance=replacement)


@pytest.mark.parametrize(
    ("base", "admission", "organization_id", "error"),
    [
        (_base(user_id=""), _admission(), None, "authenticated principal"),
        (_base(), _admission(principal="principal-b"), None, "does not match"),
        (_base(organization_id=OTHER_ORG_ID), _admission(), None, "does not match"),
        (_base(claimed_organization_id=OTHER_ORG_ID), _admission(), None, "does not match"),
        (_base(organization_admission="malformed"), _admission(), None, "malformed"),
        (_base(), _admission(), OTHER_ORG_ID, "does not match"),
        (_base(is_authenticated=False), _admission(), None, "authenticated base"),
    ],
)
def test_resource_factory_refuses_identity_and_claim_mismatches(
    base: AppContext,
    admission: AuthorizedResourceAdmission,
    organization_id: str | None,
    error: str,
) -> None:
    with pytest.raises(ValueError, match=error):
        tenant_resource_context(base, admission, organization_id=organization_id)


def test_resource_factory_refuses_other_admission_paths_and_membership_dependency_stays_specific() -> None:
    resource = tenant_resource_context(_base(), _admission())
    with pytest.raises(ValueError, match="retargeted"):
        tenant_resource_context(resource, _admission())
    free = OrganizationFreeAppContext(emitter=SilentEmitter(), user_id="principal-a")
    with pytest.raises(ValueError, match="organization-free"):
        tenant_resource_context(free, _admission())
    with pytest.raises(ValueError, match="verified organization admission"):
        require_tenant_context(_base(organization_id=ORG_ID, organization_admission="none"))


@pytest.mark.parametrize(
    "fields",
    [
        {"resource_token": "Note"},
        {"resource_id": "not-a-uuid"},
        {"operation": "create"},
        {"operation": "delete", "access_level": "editor"},
        {"adapter_id": ""},
        {"principal": ""},
    ],
)
def test_resource_admission_is_closed_and_typed(fields: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        _admission(**fields)
    with pytest.raises(ValueError, match="typed"):
        tenant_resource_context(_base(), {"organization_id": ORG_ID})  # type: ignore[arg-type]
