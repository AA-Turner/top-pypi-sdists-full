import pytest
from pydantic import BaseModel

from mistralai.workflows.protocol.v1.events import BaseEvent, JSONPatchPayload, JSONPayload

# Workflow clients and servers roll out independently. A new required event field
# prevents newer clients from parsing events emitted by older servers.
_REQUIRED_EVENT_FIELDS = {
    "attributes",
    "event_id",
    "event_timestamp",
    "event_type",
    "parent_workflow_exec_id",
    "root_workflow_exec_id",
    "workflow_exec_id",
    "workflow_name",
    "workflow_run_id",
}


def _required_schema_fields(model: type[BaseModel]) -> set[str]:
    schema = model.model_json_schema(mode="serialization")
    return set(schema.get("required", []))


@pytest.mark.parametrize("event_model", BaseEvent.__subclasses__())
def test_event_serialization_schema_does_not_add_required_fields(
    event_model: type[BaseEvent],
) -> None:
    required_fields = _required_schema_fields(event_model)

    assert required_fields == _REQUIRED_EVENT_FIELDS


@pytest.mark.parametrize("payload_model", [JSONPayload, JSONPatchPayload])
def test_payload_serialization_schema_keeps_encoding_options_optional(
    payload_model: type[BaseModel],
) -> None:
    required_fields = _required_schema_fields(payload_model)

    assert "type" in required_fields
    assert "encoding_options" not in required_fields
