"""RecoveryDiscovery"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.recovery_checkpoint_page import RecoveryCheckpointPage
from labqoat._generated.shard_recovery_plan import ShardRecoveryPlan
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class RecoveryDiscovery:
    """RecoveryDiscovery"""

    actions: list[JsonValue]
    budget: Mapping[str, JsonValue] | None
    capabilities: Mapping[str, JsonValue]
    checkpoints: RecoveryCheckpointPage
    expected_state_version: int
    history: Mapping[str, JsonValue]
    retention: Mapping[str, JsonValue]
    run_id: str
    shard_plan: ShardRecoveryPlan | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> RecoveryDiscovery:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for RecoveryDiscovery")
        return cls(
            actions=list(JsonDocument.expect_list(values.get("actions", []))),
            budget=JsonDocument.expect_optional_dict(values["budget"]),
            capabilities=JsonDocument.expect_dict(values["capabilities"]),
            checkpoints=RecoveryCheckpointPage.from_dict(JsonDocument.expect_dict(values["checkpoints"])),
            expected_state_version=JsonDocument.expect_scalar(values["expected_state_version"], int),
            history=JsonDocument.expect_dict(values["history"]),
            retention=JsonDocument.expect_dict(values["retention"]),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            shard_plan=ShardRecoveryPlan.from_dict(JsonDocument.expect_dict(values.get("shard_plan")))
            if values.get("shard_plan") is not None
            else None,
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("actions", True, "list[JsonValue]", "JsonValue"),
                ("budget", True, "Mapping[str, JsonValue]", ""),
                ("capabilities", True, "Mapping[str, JsonValue]", ""),
                ("checkpoints", True, "RecoveryCheckpointPage", ""),
                ("expected_state_version", True, "int", ""),
                ("history", True, "Mapping[str, JsonValue]", ""),
                ("retention", True, "Mapping[str, JsonValue]", ""),
                ("run_id", True, "str", ""),
                ("shard_plan", False, "ShardRecoveryPlan", ""),
            ],
        )
