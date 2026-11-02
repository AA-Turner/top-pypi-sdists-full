"""One bounded page of nodes."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.node import Node
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NodePage:
    """One bounded page of nodes."""

    items: list[Node]
    next_cursor: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NodePage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NodePage")
        return cls(
            items=[
                Node.from_dict(JsonDocument.expect_dict(v)) for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[Node]", "Node"), ("next_cursor", False, "str", "")]
        )
