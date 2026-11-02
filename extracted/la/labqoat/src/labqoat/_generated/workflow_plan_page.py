"""WorkflowPlanPage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.workflow_node import WorkflowNode
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkflowPlanPage:
    """WorkflowPlanPage"""

    active: bool
    items: list[WorkflowNode]
    next_cursor: str | None
    operation_id: str
    plan_id: str
    run_id: str
    status: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkflowPlanPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkflowPlanPage")
        return cls(
            active=JsonDocument.expect_scalar(values["active"], bool),
            items=[
                WorkflowNode.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
            operation_id=JsonDocument.expect_scalar(values["operation_id"], str),
            plan_id=JsonDocument.expect_scalar(values["plan_id"], str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("active", True, "bool", ""),
                ("items", True, "list[WorkflowNode]", "WorkflowNode"),
                ("next_cursor", True, "str", ""),
                ("operation_id", True, "str", ""),
                ("plan_id", True, "str", ""),
                ("run_id", True, "str", ""),
                ("status", True, "str", ""),
            ],
        )
