"""Secret"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Secret:
    """Secret"""

    created_at: str
    keys: list[JsonValue]
    name: str
    updated_at: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Secret:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Secret")
        return cls(
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            keys=list(JsonDocument.expect_list(values.get("keys", []))),
            name=JsonDocument.expect_scalar(values["name"], str),
            updated_at=JsonDocument.expect_scalar(values["updated_at"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("created_at", True, "str", ""),
                ("keys", True, "list[JsonValue]", "JsonValue"),
                ("name", True, "str", ""),
                ("updated_at", True, "str", ""),
            ],
        )
