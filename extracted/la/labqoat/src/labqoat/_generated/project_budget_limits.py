"""ProjectBudgetLimits"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ProjectBudgetLimits:
    """ProjectBudgetLimits"""

    already_hours: float | None = None
    already_spent: float | None = None
    hours: float | None = None
    spend: float | None = None
    spend_per_hour: float | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ProjectBudgetLimits:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ProjectBudgetLimits")
        return cls(
            already_hours=JsonDocument.expect_optional_scalar(values.get("already_hours"), float),
            already_spent=JsonDocument.expect_optional_scalar(values.get("already_spent"), float),
            hours=JsonDocument.expect_optional_scalar(values.get("hours"), float),
            spend=JsonDocument.expect_optional_scalar(values.get("spend"), float),
            spend_per_hour=JsonDocument.expect_optional_scalar(values.get("spend_per_hour"), float),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("already_hours", False, "float", ""),
                ("already_spent", False, "float", ""),
                ("hours", False, "float", ""),
                ("spend", False, "float", ""),
                ("spend_per_hour", False, "float", ""),
            ],
        )
