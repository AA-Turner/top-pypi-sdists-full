"""ForkRequest"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.new_compute_run import NewComputeRun
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ForkRequest:
    """ForkRequest"""

    expected_state_version: int
    reason: str
    submission: NewComputeRun
    checkpoint_id: str | None = None
    operation_key: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ForkRequest:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ForkRequest")
        return cls(
            checkpoint_id=JsonDocument.expect_optional_scalar(values.get("checkpoint_id"), str),
            expected_state_version=JsonDocument.expect_scalar(values["expected_state_version"], int),
            operation_key=JsonDocument.expect_optional_scalar(values.get("operation_key"), str),
            reason=JsonDocument.expect_scalar(values["reason"], str),
            submission=NewComputeRun.from_dict(JsonDocument.expect_dict(values["submission"])),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("checkpoint_id", False, "str", ""),
                ("expected_state_version", True, "int", ""),
                ("operation_key", False, "str", ""),
                ("reason", True, "str", ""),
                ("submission", True, "NewComputeRun", ""),
            ],
        )
