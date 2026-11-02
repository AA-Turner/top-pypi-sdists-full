"""FitBudgetIntervals"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.fit_budget_interval import FitBudgetInterval
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class FitBudgetIntervals:
    """FitBudgetIntervals"""

    items: list[FitBudgetInterval]
    next_cursor: str | None
    run_id: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> FitBudgetIntervals:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for FitBudgetIntervals")
        return cls(
            items=[
                FitBudgetInterval.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("items", True, "list[FitBudgetInterval]", "FitBudgetInterval"),
                ("next_cursor", True, "str", ""),
                ("run_id", True, "str", ""),
            ],
        )
