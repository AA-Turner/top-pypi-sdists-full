"""Coded failure with retry intent."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerFailure:
    """Coded failure with retry intent."""

    retryable: bool
    reason: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerFailure:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerFailure")
        return cls(
            reason=JsonDocument.expect_optional_scalar(values.get("reason"), str),
            retryable=JsonDocument.expect_scalar(values["retryable"], bool),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("reason", False, "str", ""), ("retryable", True, "bool", "")])
