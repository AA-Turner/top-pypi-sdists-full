"""HuggingFaceSource"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class HuggingFaceSource:
    """HuggingFaceSource"""

    repository: str
    splits: list[JsonValue]
    columns: Mapping[str, JsonValue] | None = None
    configuration: str | None = None
    revision: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> HuggingFaceSource:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for HuggingFaceSource")
        return cls(
            columns=JsonDocument.expect_optional_dict(values.get("columns")),
            configuration=JsonDocument.expect_optional_scalar(values.get("configuration"), str),
            repository=JsonDocument.expect_scalar(values["repository"], str),
            revision=JsonDocument.expect_optional_scalar(values.get("revision"), str),
            splits=list(JsonDocument.expect_list(values.get("splits", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("columns", False, "Mapping[str, JsonValue]", ""),
                ("configuration", False, "str", ""),
                ("repository", True, "str", ""),
                ("revision", False, "str", ""),
                ("splits", True, "list[JsonValue]", "JsonValue"),
            ],
        )
