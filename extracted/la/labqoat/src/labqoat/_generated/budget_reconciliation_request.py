"""BudgetReconciliationRequest"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class BudgetReconciliationRequest:
    """BudgetReconciliationRequest"""

    consumed_ms: int
    evidence_digest: str
    expected_state_version: int
    reason: str
    operation_key: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> BudgetReconciliationRequest:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for BudgetReconciliationRequest")
        return cls(
            consumed_ms=JsonDocument.expect_scalar(values["consumed_ms"], int),
            evidence_digest=JsonDocument.expect_scalar(values["evidence_digest"], str),
            expected_state_version=JsonDocument.expect_scalar(values["expected_state_version"], int),
            operation_key=JsonDocument.expect_optional_scalar(values.get("operation_key"), str),
            reason=JsonDocument.expect_scalar(values["reason"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("consumed_ms", True, "int", ""),
                ("evidence_digest", True, "str", ""),
                ("expected_state_version", True, "int", ""),
                ("operation_key", False, "str", ""),
                ("reason", True, "str", ""),
            ],
        )
