"""RecoveryRequest"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RecoveryRequest:
    """RecoveryRequest"""

    expected_state_version: int
    mode: str
    checkpoint: Mapping[str, JsonValue] | None = None
    child_strategy: str | None = None
    include_cancelled: bool | None = None
    reason: str | None = None
    scope: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RecoveryRequest:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RecoveryRequest")
        return cls(
            checkpoint=JsonDocument.expect_optional_dict(values.get("checkpoint")),
            child_strategy=JsonDocument.expect_optional_scalar(values.get("child_strategy"), str),
            expected_state_version=JsonDocument.expect_scalar(values["expected_state_version"], int),
            include_cancelled=JsonDocument.expect_optional_scalar(values.get("include_cancelled"), bool),
            mode=JsonDocument.expect_scalar(values["mode"], str),
            reason=JsonDocument.expect_optional_scalar(values.get("reason"), str),
            scope=JsonDocument.expect_optional_scalar(values.get("scope"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("checkpoint", False, "Mapping[str, JsonValue]", ""),
                ("child_strategy", False, "str", ""),
                ("expected_state_version", True, "int", ""),
                ("include_cancelled", False, "bool", ""),
                ("mode", True, "str", ""),
                ("reason", False, "str", ""),
                ("scope", False, "str", ""),
            ],
        )
