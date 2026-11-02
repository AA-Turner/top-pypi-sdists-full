"""AutomaticRecoveryPolicy"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class AutomaticRecoveryPolicy:
    """AutomaticRecoveryPolicy"""

    backoff_ms: int
    deadline_seconds: int
    failure_classes: list[JsonValue]
    jitter_percent: int
    max_backoff_ms: int
    repeated_failure_limit: int
    restart_fallback: bool
    strategy: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> AutomaticRecoveryPolicy:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for AutomaticRecoveryPolicy")
        return cls(
            backoff_ms=JsonDocument.expect_scalar(values["backoff_ms"], int),
            deadline_seconds=JsonDocument.expect_scalar(values["deadline_seconds"], int),
            failure_classes=list(JsonDocument.expect_list(values.get("failure_classes", []))),
            jitter_percent=JsonDocument.expect_scalar(values["jitter_percent"], int),
            max_backoff_ms=JsonDocument.expect_scalar(values["max_backoff_ms"], int),
            repeated_failure_limit=JsonDocument.expect_scalar(values["repeated_failure_limit"], int),
            restart_fallback=JsonDocument.expect_scalar(values["restart_fallback"], bool),
            strategy=JsonDocument.expect_scalar(values["strategy"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("backoff_ms", True, "int", ""),
                ("deadline_seconds", True, "int", ""),
                ("failure_classes", True, "list[JsonValue]", "JsonValue"),
                ("jitter_percent", True, "int", ""),
                ("max_backoff_ms", True, "int", ""),
                ("repeated_failure_limit", True, "int", ""),
                ("restart_fallback", True, "bool", ""),
                ("strategy", True, "str", ""),
            ],
        )
