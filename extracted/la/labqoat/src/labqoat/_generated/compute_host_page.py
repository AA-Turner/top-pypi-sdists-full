"""ComputeHostPage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.compute_host import ComputeHost
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeHostPage:
    """ComputeHostPage"""

    items: list[ComputeHost]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeHostPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeHostPage")
        return cls(
            items=[
                ComputeHost.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("items", True, "list[ComputeHost]", "ComputeHost")])
