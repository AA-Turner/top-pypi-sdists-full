"""FitBudgetInterval"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.budget_adjustment import BudgetAdjustment
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class FitBudgetInterval:
    """FitBudgetInterval"""

    adjustment: BudgetAdjustment | None
    attempt_id: str
    duration_ms: int
    expires_at: str
    fence: int
    id: str
    reported_ms: int
    starts_at: str
    status: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> FitBudgetInterval:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for FitBudgetInterval")
        return cls(
            adjustment=BudgetAdjustment.from_dict(JsonDocument.expect_dict(values["adjustment"]))
            if values["adjustment"] is not None
            else None,
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            duration_ms=JsonDocument.expect_scalar(values["duration_ms"], int),
            expires_at=JsonDocument.expect_scalar(values["expires_at"], str),
            fence=JsonDocument.expect_scalar(values["fence"], int),
            id=JsonDocument.expect_scalar(values["id"], str),
            reported_ms=JsonDocument.expect_scalar(values["reported_ms"], int),
            starts_at=JsonDocument.expect_scalar(values["starts_at"], str),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("adjustment", True, "BudgetAdjustment", ""),
                ("attempt_id", True, "str", ""),
                ("duration_ms", True, "int", ""),
                ("expires_at", True, "str", ""),
                ("fence", True, "int", ""),
                ("id", True, "str", ""),
                ("reported_ms", True, "int", ""),
                ("starts_at", True, "str", ""),
                ("status", True, "str", ""),
            ],
        )
