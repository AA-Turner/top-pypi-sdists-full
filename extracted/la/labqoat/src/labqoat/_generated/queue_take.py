"""QueueTake"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueueTake:
    """QueueTake"""

    limit: int | None = None
    partition: str | None = None
    timeout: float | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueueTake:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueueTake")
        return cls(
            limit=JsonDocument.expect_optional_scalar(values.get("limit"), int),
            partition=JsonDocument.expect_optional_scalar(values.get("partition"), str),
            timeout=JsonDocument.expect_optional_scalar(values.get("timeout"), float),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("limit", False, "int", ""), ("partition", False, "str", ""), ("timeout", False, "float", "")]
        )
