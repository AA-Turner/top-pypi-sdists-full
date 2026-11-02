"""Machine supply at one location. The pool id is the location id; capacity sums its ready machines and configuration carries the location's offering policy."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Pool:
    """Machine supply at one location. The pool id is the location id; capacity sums its ready machines and configuration carries the location's offering policy."""

    id: str
    name: str
    allocatable: Mapping[str, JsonValue] | None = None
    capacity: Mapping[str, JsonValue] | None = None
    configuration: Mapping[str, JsonValue] | None = None
    environment_id: str | None = None
    provider: str | None = None
    state: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Pool:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Pool")
        return cls(
            allocatable=JsonDocument.expect_optional_dict(values.get("allocatable")),
            capacity=JsonDocument.expect_optional_dict(values.get("capacity")),
            configuration=JsonDocument.expect_optional_dict(values.get("configuration")),
            environment_id=JsonDocument.expect_optional_scalar(values.get("environment_id"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            name=JsonDocument.expect_scalar(values["name"], str),
            provider=JsonDocument.expect_optional_scalar(values.get("provider"), str),
            state=JsonDocument.expect_optional_scalar(values.get("state"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("allocatable", False, "Mapping[str, JsonValue]", ""),
                ("capacity", False, "Mapping[str, JsonValue]", ""),
                ("configuration", False, "Mapping[str, JsonValue]", ""),
                ("environment_id", False, "str", ""),
                ("id", True, "str", ""),
                ("name", True, "str", ""),
                ("provider", False, "str", ""),
                ("state", False, "str", ""),
            ],
        )
