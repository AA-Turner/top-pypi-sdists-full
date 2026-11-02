"""NewDatasetImport"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.hugging_face_source import HuggingFaceSource
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewDatasetImport:
    """NewDatasetImport"""

    dataset: str
    source: HuggingFaceSource
    tag: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewDatasetImport:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewDatasetImport")
        return cls(
            dataset=JsonDocument.expect_scalar(values["dataset"], str),
            source=HuggingFaceSource.from_dict(JsonDocument.expect_dict(values["source"])),
            tag=JsonDocument.expect_optional_scalar(values.get("tag"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("dataset", True, "str", ""), ("source", True, "HuggingFaceSource", ""), ("tag", False, "str", "")]
        )
