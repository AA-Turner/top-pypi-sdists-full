"""HuggingFacePreview"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class HuggingFacePreview:
    """HuggingFacePreview"""

    files: list[JsonValue]
    preview: list[JsonValue]
    rows: int
    schema: Mapping[str, JsonValue]
    source: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> HuggingFacePreview:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for HuggingFacePreview")
        return cls(
            files=list(JsonDocument.expect_list(values.get("files", []))),
            preview=list(JsonDocument.expect_list(values.get("preview", []))),
            rows=JsonDocument.expect_scalar(values["rows"], int),
            schema=JsonDocument.expect_dict(values["schema"]),
            source=JsonDocument.expect_dict(values["source"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("files", True, "list[JsonValue]", "JsonValue"),
                ("preview", True, "list[JsonValue]", "JsonValue"),
                ("rows", True, "int", ""),
                ("schema", True, "Mapping[str, JsonValue]", ""),
                ("source", True, "Mapping[str, JsonValue]", ""),
            ],
        )
