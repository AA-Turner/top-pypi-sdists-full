"""ComputeOfferingPage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.compute_offering import ComputeOffering
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeOfferingPage:
    """ComputeOfferingPage"""

    items: list[ComputeOffering]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeOfferingPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeOfferingPage")
        return cls(
            items=[
                ComputeOffering.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("items", True, "list[ComputeOffering]", "ComputeOffering")])
