"""QueueList"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.queue_summary import QueueSummary
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueueList:
    """QueueList"""

    items: list[QueueSummary]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueueList:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueueList")
        return cls(
            items=[
                QueueSummary.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("items", True, "list[QueueSummary]", "QueueSummary")])
