"""Repeatable receipt for a retired or deleted resource."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DeletionReceipt:
    """Repeatable receipt for a retired or deleted resource."""

    ref: str
    status: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DeletionReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DeletionReceipt")
        return cls(
            ref=JsonDocument.expect_scalar(values["ref"], str),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("ref", True, "str", ""), ("status", True, "str", "")])
