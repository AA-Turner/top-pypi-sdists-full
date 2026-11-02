"""Service status; also verifies HTTP Basic credentials."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Status:
    """Service status; also verifies HTTP Basic credentials."""

    links: Mapping[str, JsonValue]
    status: str
    time: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Status:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Status")
        return cls(
            links=JsonDocument.expect_dict(values["links"]),
            status=JsonDocument.expect_scalar(values["status"], str),
            time=JsonDocument.expect_scalar(values["time"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [("links", True, "Mapping[str, JsonValue]", ""), ("status", True, "str", ""), ("time", True, "str", "")],
        )
