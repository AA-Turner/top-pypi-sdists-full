"""FitBudgetHistory"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class FitBudgetHistory:
    """FitBudgetHistory"""

    allowance_ms: int
    consumed_ms: int
    history: Mapping[str, JsonValue]
    history_known: bool
    overshoot_ms: int
    remaining_ms: int | None
    reserved_ms: int
    run_id: str
    uncertain_ms: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> FitBudgetHistory:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for FitBudgetHistory")
        return cls(
            allowance_ms=JsonDocument.expect_scalar(values["allowance_ms"], int),
            consumed_ms=JsonDocument.expect_scalar(values["consumed_ms"], int),
            history=JsonDocument.expect_dict(values["history"]),
            history_known=JsonDocument.expect_scalar(values["history_known"], bool),
            overshoot_ms=JsonDocument.expect_scalar(values["overshoot_ms"], int),
            remaining_ms=JsonDocument.expect_optional_scalar(values.get("remaining_ms"), int),
            reserved_ms=JsonDocument.expect_scalar(values["reserved_ms"], int),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            uncertain_ms=JsonDocument.expect_scalar(values["uncertain_ms"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("allowance_ms", True, "int", ""),
                ("consumed_ms", True, "int", ""),
                ("history", True, "Mapping[str, JsonValue]", ""),
                ("history_known", True, "bool", ""),
                ("overshoot_ms", True, "int", ""),
                ("remaining_ms", True, "int", ""),
                ("reserved_ms", True, "int", ""),
                ("run_id", True, "str", ""),
                ("uncertain_ms", True, "int", ""),
            ],
        )
