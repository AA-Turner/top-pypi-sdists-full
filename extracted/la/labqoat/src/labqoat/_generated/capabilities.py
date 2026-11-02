"""Configured environments, usable operations, limits, and versions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Capabilities:
    """Configured environments, usable operations, limits, and versions."""

    contract_version: str
    operations: Mapping[str, JsonValue]
    protocol_version: str
    authentication: Mapping[str, JsonValue] | None = None
    dependencies: Mapping[str, JsonValue] | None = None
    deployment: Mapping[str, JsonValue] | None = None
    environments: list[JsonValue] | None = field(default_factory=list)
    limits: Mapping[str, JsonValue] | None = None
    service: Mapping[str, JsonValue] | None = None
    unavailable: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Capabilities:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Capabilities")
        return cls(
            authentication=JsonDocument.expect_optional_dict(values.get("authentication")),
            contract_version=JsonDocument.expect_scalar(values["contract_version"], str),
            dependencies=JsonDocument.expect_optional_dict(values.get("dependencies")),
            deployment=JsonDocument.expect_optional_dict(values.get("deployment")),
            environments=list(JsonDocument.expect_list(values.get("environments", []))),
            limits=JsonDocument.expect_optional_dict(values.get("limits")),
            operations=JsonDocument.expect_dict(values["operations"]),
            protocol_version=JsonDocument.expect_scalar(values["protocol_version"], str),
            service=JsonDocument.expect_optional_dict(values.get("service")),
            unavailable=list(JsonDocument.expect_list(values.get("unavailable", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("authentication", False, "Mapping[str, JsonValue]", ""),
                ("contract_version", True, "str", ""),
                ("dependencies", False, "Mapping[str, JsonValue]", ""),
                ("deployment", False, "Mapping[str, JsonValue]", ""),
                ("environments", False, "list[JsonValue]", "JsonValue"),
                ("limits", False, "Mapping[str, JsonValue]", ""),
                ("operations", True, "Mapping[str, JsonValue]", ""),
                ("protocol_version", True, "str", ""),
                ("service", False, "Mapping[str, JsonValue]", ""),
                ("unavailable", False, "list[JsonValue]", "JsonValue"),
            ],
        )
