"""DictEntries"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dict_entry import DictEntry
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DictEntries:
    """DictEntries"""

    entries: list[DictEntry]
    skip_if_exists: bool | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DictEntries:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DictEntries")
        return cls(
            entries=[
                DictEntry.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("entries", []))
            ],
            skip_if_exists=JsonDocument.expect_optional_scalar(values.get("skip_if_exists"), bool),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("entries", True, "list[DictEntry]", "DictEntry"), ("skip_if_exists", False, "bool", "")]
        )
