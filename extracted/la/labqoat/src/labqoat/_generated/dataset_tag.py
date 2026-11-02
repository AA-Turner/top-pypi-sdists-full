"""A mutable pointer to a revision."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetTag:
    """A mutable pointer to a revision."""

    id: str
    repository_id: str
    revision_id: str
    tag: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetTag:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetTag")
        return cls(
            id=JsonDocument.expect_scalar(values["id"], str),
            repository_id=JsonDocument.expect_scalar(values["repository_id"], str),
            revision_id=JsonDocument.expect_scalar(values["revision_id"], str),
            tag=JsonDocument.expect_scalar(values["tag"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("id", True, "str", ""),
                ("repository_id", True, "str", ""),
                ("revision_id", True, "str", ""),
                ("tag", True, "str", ""),
            ],
        )
