"""Lineage recorded for one immutable dataset revision."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRevisionLineage:
    """Lineage recorded for one immutable dataset revision."""

    lineage: Mapping[str, JsonValue]
    ref: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRevisionLineage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRevisionLineage")
        return cls(
            lineage=JsonDocument.expect_dict(values["lineage"]),
            ref=JsonDocument.expect_scalar(values["ref"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("lineage", True, "Mapping[str, JsonValue]", ""), ("ref", True, "str", "")]
        )
