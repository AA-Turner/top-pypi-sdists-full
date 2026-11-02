"""One bounded page of repository tags."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dataset_tag import DatasetTag
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetTagPage:
    """One bounded page of repository tags."""

    items: list[DatasetTag]
    links: Mapping[str, JsonValue]
    next_cursor: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetTagPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetTagPage")
        return cls(
            items=[
                DatasetTag.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            links=JsonDocument.expect_dict(values["links"]),
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("items", True, "list[DatasetTag]", "DatasetTag"),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("next_cursor", False, "str", ""),
            ],
        )
