"""DatasetImport"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetImport:
    """DatasetImport"""

    dataset: str
    failure: Mapping[str, JsonValue] | None
    id: str
    revision_id: str | None
    source: Mapping[str, JsonValue] | None
    status: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetImport:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetImport")
        return cls(
            dataset=JsonDocument.expect_scalar(values["dataset"], str),
            failure=JsonDocument.expect_optional_dict(values["failure"]),
            id=JsonDocument.expect_scalar(values["id"], str),
            revision_id=JsonDocument.expect_optional_scalar(values.get("revision_id"), str),
            source=JsonDocument.expect_optional_dict(values["source"]),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("dataset", True, "str", ""),
                ("failure", True, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("revision_id", True, "str", ""),
                ("source", True, "Mapping[str, JsonValue]", ""),
                ("status", True, "str", ""),
            ],
        )
