"""RecoveryOperation"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.recovery_request import RecoveryRequest
from labqoat._generated.shard_recovery_plan import ShardRecoveryPlan
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RecoveryOperation:
    """RecoveryOperation"""

    actor: str
    attempt_id: str | None
    checkpoint_digest: str | None
    checkpoint_id: str | None
    cycle_id: str | None
    deadline_at: str
    execution_ended_at: str | None
    execution_outcome: str | None
    failure: Mapping[str, JsonValue]
    id: str
    inserted_at: str
    mode: str
    phase: str
    request: RecoveryRequest
    run_id: str
    scope: str
    updated_at: str
    decision: Mapping[str, JsonValue] | None = None
    not_before: str | None = None
    shard_plan: ShardRecoveryPlan | None = None
    trigger: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RecoveryOperation:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RecoveryOperation")
        return cls(
            actor=JsonDocument.expect_scalar(values["actor"], str),
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            checkpoint_digest=JsonDocument.expect_optional_scalar(values.get("checkpoint_digest"), str),
            checkpoint_id=JsonDocument.expect_optional_scalar(values.get("checkpoint_id"), str),
            cycle_id=JsonDocument.expect_optional_scalar(values.get("cycle_id"), str),
            deadline_at=JsonDocument.expect_scalar(values["deadline_at"], str),
            decision=JsonDocument.expect_optional_dict(values.get("decision")),
            execution_ended_at=JsonDocument.expect_optional_scalar(values.get("execution_ended_at"), str),
            execution_outcome=JsonDocument.expect_optional_scalar(values.get("execution_outcome"), str),
            failure=JsonDocument.expect_dict(values["failure"]),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            mode=JsonDocument.expect_scalar(values["mode"], str),
            not_before=JsonDocument.expect_optional_scalar(values.get("not_before"), str),
            phase=JsonDocument.expect_scalar(values["phase"], str),
            request=RecoveryRequest.from_dict(JsonDocument.expect_dict(values["request"])),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            scope=JsonDocument.expect_scalar(values["scope"], str),
            shard_plan=ShardRecoveryPlan.from_dict(JsonDocument.expect_dict(values.get("shard_plan")))
            if values.get("shard_plan") is not None
            else None,
            trigger=JsonDocument.expect_optional_scalar(values.get("trigger"), str),
            updated_at=JsonDocument.expect_scalar(values["updated_at"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("actor", True, "str", ""),
                ("attempt_id", True, "str", ""),
                ("checkpoint_digest", True, "str", ""),
                ("checkpoint_id", True, "str", ""),
                ("cycle_id", True, "str", ""),
                ("deadline_at", True, "str", ""),
                ("decision", False, "Mapping[str, JsonValue]", ""),
                ("execution_ended_at", True, "str", ""),
                ("execution_outcome", True, "str", ""),
                ("failure", True, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("mode", True, "str", ""),
                ("not_before", False, "str", ""),
                ("phase", True, "str", ""),
                ("request", True, "RecoveryRequest", ""),
                ("run_id", True, "str", ""),
                ("scope", True, "str", ""),
                ("shard_plan", False, "ShardRecoveryPlan", ""),
                ("trigger", False, "str", ""),
                ("updated_at", True, "str", ""),
            ],
        )
