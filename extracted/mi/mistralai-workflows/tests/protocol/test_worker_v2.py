import uuid

import pytest
from pydantic import ValidationError

from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_SCOPE_NOT_FOUND_CODE,
    EventRouteClaims,
)


def test_scope_not_found_code_remains_part_of_protocol_surface() -> None:
    assert EVENT_ROUTE_SCOPE_NOT_FOUND_CODE == "EVENT_ROUTE_SCOPE_NOT_FOUND"


def test_event_route_claims_model_dump_is_json_safe_by_default() -> None:
    claims = EventRouteClaims(
        scope_kind="root",
        workflow_owner_customer_id=uuid.uuid4(),
        workflow_owner_workspace_id=uuid.uuid4(),
        execution_owner_customer_id=uuid.uuid4(),
        execution_owner_workspace_id=uuid.uuid4(),
        workflow_id=uuid.uuid4(),
        workflow_name="workflow",
        workflow_exec_id="exec",
        workflow_run_id="run",
        root_workflow_exec_id="root-exec",
    )

    dumped = claims.model_dump()

    assert isinstance(claims.workflow_id, uuid.UUID)
    assert isinstance(dumped["workflow_id"], str)
    assert dumped["workflow_id"] == str(claims.workflow_id)


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("workflow_name", ""),
        ("workflow_exec_id", ""),
        ("workflow_run_id", ""),
        ("root_workflow_exec_id", ""),
        ("parent_workflow_exec_id", ""),
    ],
)
def test_event_route_claims_rejects_empty_string_fields(field_name: str, field_value: str) -> None:
    claims = {
        "scope_kind": "root",
        "workflow_owner_customer_id": uuid.uuid4(),
        "workflow_owner_workspace_id": uuid.uuid4(),
        "execution_owner_customer_id": uuid.uuid4(),
        "execution_owner_workspace_id": uuid.uuid4(),
        "workflow_id": uuid.uuid4(),
        "workflow_name": "workflow",
        "workflow_exec_id": "exec",
        "workflow_run_id": "run",
        "root_workflow_exec_id": "root-exec",
        "parent_workflow_exec_id": "parent-exec",
    }
    claims[field_name] = field_value

    with pytest.raises(ValidationError):
        EventRouteClaims(**claims)
