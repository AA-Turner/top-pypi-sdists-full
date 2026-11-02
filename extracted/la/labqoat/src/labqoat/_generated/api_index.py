"""Entry point advertising collections, status, and contract links."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ApiIndex:
    """Entry point advertising collections, status, and contract links."""

    links: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ApiIndex:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ApiIndex")
        return cls(
            links=JsonDocument.expect_dict(values["links"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("links", True, "Mapping[str, JsonValue]", "")])
