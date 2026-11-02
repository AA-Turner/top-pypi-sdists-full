"""DatasetImportEvent"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dataset_import import DatasetImport
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetImportEvent:
    """DatasetImportEvent"""

    data: DatasetImport
    event: str
    id: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetImportEvent:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetImportEvent")
        return cls(
            data=DatasetImport.from_dict(JsonDocument.expect_dict(values["data"])),
            event=JsonDocument.expect_scalar(values["event"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("data", True, "DatasetImport", ""), ("event", True, "str", ""), ("id", True, "str", "")]
        )
