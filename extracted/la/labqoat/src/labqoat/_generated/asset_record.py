"""A content-addressed asset with availability."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class AssetRecord:
    """A content-addressed asset with availability."""

    availability: str
    byte_size: int
    id: str
    links: Mapping[str, JsonValue]
    media_type: str
    sha256: str
    storage_key: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> AssetRecord:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for AssetRecord")
        return cls(
            availability=JsonDocument.expect_scalar(values["availability"], str),
            byte_size=JsonDocument.expect_scalar(values["byte_size"], int),
            id=JsonDocument.expect_scalar(values["id"], str),
            links=JsonDocument.expect_dict(values["links"]),
            media_type=JsonDocument.expect_scalar(values["media_type"], str),
            sha256=JsonDocument.expect_scalar(values["sha256"], str),
            storage_key=JsonDocument.expect_scalar(values["storage_key"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("availability", True, "str", ""),
                ("byte_size", True, "int", ""),
                ("id", True, "str", ""),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("media_type", True, "str", ""),
                ("sha256", True, "str", ""),
                ("storage_key", True, "str", ""),
            ],
        )
