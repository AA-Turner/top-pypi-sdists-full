"""DictEntryListing"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.encoded_value import EncodedValue
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DictEntryListing:
    """DictEntryListing"""

    key: str
    value: EncodedValue | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DictEntryListing:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DictEntryListing")
        return cls(
            key=JsonDocument.expect_scalar(values["key"], str),
            value=EncodedValue.from_dict(JsonDocument.expect_dict(values.get("value")))
            if values.get("value") is not None
            else None,
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("key", True, "str", ""), ("value", False, "EncodedValue", "")])
