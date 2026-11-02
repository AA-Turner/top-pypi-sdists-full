"""BudgetAdjustment"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class BudgetAdjustment:
    """BudgetAdjustment"""

    actor: str
    attempt_id: str
    consumed_delta_ms: int
    evidence_digest: str
    grant_id: str
    id: str
    inserted_at: str
    request: Mapping[str, JsonValue]
    request_key: str
    run_id: str
    uncertain_delta_ms: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> BudgetAdjustment:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for BudgetAdjustment")
        return cls(
            actor=JsonDocument.expect_scalar(values["actor"], str),
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            consumed_delta_ms=JsonDocument.expect_scalar(values["consumed_delta_ms"], int),
            evidence_digest=JsonDocument.expect_scalar(values["evidence_digest"], str),
            grant_id=JsonDocument.expect_scalar(values["grant_id"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            request=JsonDocument.expect_dict(values["request"]),
            request_key=JsonDocument.expect_scalar(values["request_key"], str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            uncertain_delta_ms=JsonDocument.expect_scalar(values["uncertain_delta_ms"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("actor", True, "str", ""),
                ("attempt_id", True, "str", ""),
                ("consumed_delta_ms", True, "int", ""),
                ("evidence_digest", True, "str", ""),
                ("grant_id", True, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("request", True, "Mapping[str, JsonValue]", ""),
                ("request_key", True, "str", ""),
                ("run_id", True, "str", ""),
                ("uncertain_delta_ms", True, "int", ""),
            ],
        )
