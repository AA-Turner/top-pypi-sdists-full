"""WorkflowPreview"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.workflow_node import WorkflowNode
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkflowPreview:
    """WorkflowPreview"""

    expected_state_version: int
    items: list[WorkflowNode]
    next_cursor: str | None
    parent_id: str
    root: WorkflowNode
    run_id: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkflowPreview:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkflowPreview")
        return cls(
            expected_state_version=JsonDocument.expect_scalar(values["expected_state_version"], int),
            items=[
                WorkflowNode.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
            parent_id=JsonDocument.expect_scalar(values["parent_id"], str),
            root=WorkflowNode.from_dict(JsonDocument.expect_dict(values["root"])),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("expected_state_version", True, "int", ""),
                ("items", True, "list[WorkflowNode]", "WorkflowNode"),
                ("next_cursor", True, "str", ""),
                ("parent_id", True, "str", ""),
                ("root", True, "WorkflowNode", ""),
                ("run_id", True, "str", ""),
            ],
        )
