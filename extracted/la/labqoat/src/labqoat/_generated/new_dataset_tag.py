"""Tag move to a revision."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewDatasetTag:
    """Tag move to a revision."""

    repository_ref: str
    revision_ref: str
    tag: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewDatasetTag:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewDatasetTag")
        return cls(
            repository_ref=JsonDocument.expect_scalar(values["repository_ref"], str),
            revision_ref=JsonDocument.expect_scalar(values["revision_ref"], str),
            tag=JsonDocument.expect_scalar(values["tag"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("repository_ref", True, "str", ""), ("revision_ref", True, "str", ""), ("tag", True, "str", "")]
        )
