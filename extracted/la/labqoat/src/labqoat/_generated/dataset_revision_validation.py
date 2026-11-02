"""Validation evidence recorded for one immutable dataset revision."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRevisionValidation:
    """Validation evidence recorded for one immutable dataset revision."""

    ref: str
    validation: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRevisionValidation:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRevisionValidation")
        return cls(
            ref=JsonDocument.expect_scalar(values["ref"], str),
            validation=JsonDocument.expect_dict(values["validation"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("ref", True, "str", ""), ("validation", True, "Mapping[str, JsonValue]", "")]
        )
