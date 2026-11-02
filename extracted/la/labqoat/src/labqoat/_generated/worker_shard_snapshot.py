"""WorkerShardSnapshot"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.shard_recovery_plan import ShardRecoveryPlan
from labqoat._generated.worker_shard_state import WorkerShardState
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerShardSnapshot:
    """WorkerShardSnapshot"""

    attempt_id: str
    fence: int
    protocol_version: int
    run_id: str
    shards: list[WorkerShardState]
    recovery: ShardRecoveryPlan | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerShardSnapshot:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerShardSnapshot")
        return cls(
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            fence=JsonDocument.expect_scalar(values["fence"], int),
            protocol_version=JsonDocument.expect_scalar(values["protocol_version"], int),
            recovery=ShardRecoveryPlan.from_dict(JsonDocument.expect_dict(values.get("recovery")))
            if values.get("recovery") is not None
            else None,
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            shards=[
                WorkerShardState.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("shards", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("fence", True, "int", ""),
                ("protocol_version", True, "int", ""),
                ("recovery", False, "ShardRecoveryPlan", ""),
                ("run_id", True, "str", ""),
                ("shards", True, "list[WorkerShardState]", "WorkerShardState"),
            ],
        )
