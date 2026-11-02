"""RecoveryReason"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RecoveryReason:
    """RecoveryReason"""

    code: str
    remediation: str
    stage: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RecoveryReason:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RecoveryReason")
        return cls(
            code=JsonDocument.expect_scalar(values["code"], str),
            remediation=JsonDocument.expect_scalar(values["remediation"], str),
            stage=JsonDocument.expect_scalar(values["stage"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("code", True, "str", ""), ("remediation", True, "str", ""), ("stage", True, "str", "")]
        )
