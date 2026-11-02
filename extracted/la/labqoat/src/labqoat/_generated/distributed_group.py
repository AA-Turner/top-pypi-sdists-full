"""DistributedGroup"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DistributedGroup:
    """DistributedGroup"""

    attempt_id: str
    backend: str
    checkpoint_id: str
    fence: int
    phase: str
    restored_count: int
    run_id: str
    topology: str
    world_size: int
    deadline_at: str | None = None
    failed_at: str | None = None
    failed_rank: int | None = None
    failure: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DistributedGroup:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DistributedGroup")
        return cls(
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            backend=JsonDocument.expect_scalar(values["backend"], str),
            checkpoint_id=JsonDocument.expect_scalar(values["checkpoint_id"], str),
            deadline_at=JsonDocument.expect_optional_scalar(values.get("deadline_at"), str),
            failed_at=JsonDocument.expect_optional_scalar(values.get("failed_at"), str),
            failed_rank=JsonDocument.expect_optional_scalar(values.get("failed_rank"), int),
            failure=JsonDocument.expect_optional_dict(values.get("failure")),
            fence=JsonDocument.expect_scalar(values["fence"], int),
            phase=JsonDocument.expect_scalar(values["phase"], str),
            restored_count=JsonDocument.expect_scalar(values["restored_count"], int),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            topology=JsonDocument.expect_scalar(values["topology"], str),
            world_size=JsonDocument.expect_scalar(values["world_size"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("backend", True, "str", ""),
                ("checkpoint_id", True, "str", ""),
                ("deadline_at", False, "str", ""),
                ("failed_at", False, "str", ""),
                ("failed_rank", False, "int", ""),
                ("failure", False, "Mapping[str, JsonValue]", ""),
                ("fence", True, "int", ""),
                ("phase", True, "str", ""),
                ("restored_count", True, "int", ""),
                ("run_id", True, "str", ""),
                ("topology", True, "str", ""),
                ("world_size", True, "int", ""),
            ],
        )
