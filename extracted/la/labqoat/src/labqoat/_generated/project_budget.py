"""ProjectBudget"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.project_budget_limits import ProjectBudgetLimits
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ProjectBudget:
    """ProjectBudget"""

    calculated_at: str
    currency: str
    elapsed_hours: float | None
    hints: list[JsonValue]
    limits: ProjectBudgetLimits
    project: str
    spent: float | None
    spent_last_hour: float | None
    started_at: str | None
    spend_rate: float | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ProjectBudget:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ProjectBudget")
        return cls(
            calculated_at=JsonDocument.expect_scalar(values["calculated_at"], str),
            currency=JsonDocument.expect_scalar(values["currency"], str),
            elapsed_hours=JsonDocument.expect_optional_scalar(values.get("elapsed_hours"), float),
            hints=list(JsonDocument.expect_list(values.get("hints", []))),
            limits=ProjectBudgetLimits.from_dict(JsonDocument.expect_dict(values["limits"])),
            project=JsonDocument.expect_scalar(values["project"], str),
            spend_rate=JsonDocument.expect_optional_scalar(values.get("spend_rate"), float),
            spent=JsonDocument.expect_optional_scalar(values.get("spent"), float),
            spent_last_hour=JsonDocument.expect_optional_scalar(values.get("spent_last_hour"), float),
            started_at=JsonDocument.expect_optional_scalar(values.get("started_at"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("calculated_at", True, "str", ""),
                ("currency", True, "str", ""),
                ("elapsed_hours", True, "float", ""),
                ("hints", True, "list[JsonValue]", "JsonValue"),
                ("limits", True, "ProjectBudgetLimits", ""),
                ("project", True, "str", ""),
                ("spend_rate", False, "float", ""),
                ("spent", True, "float", ""),
                ("spent_last_hour", True, "float", ""),
                ("started_at", True, "str", ""),
            ],
        )
