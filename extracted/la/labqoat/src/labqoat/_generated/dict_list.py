"""DictList"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dict_summary import DictSummary
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DictList:
    """DictList"""

    items: list[DictSummary]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DictList:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DictList")
        return cls(
            items=[
                DictSummary.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("items", True, "list[DictSummary]", "DictSummary")])
