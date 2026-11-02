"""One bounded page of revision history."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dataset_revision import DatasetRevision
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRevisionPage:
    """One bounded page of revision history."""

    items: list[DatasetRevision]
    links: Mapping[str, JsonValue]
    next_cursor: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRevisionPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRevisionPage")
        return cls(
            items=[
                DatasetRevision.from_dict(JsonDocument.expect_dict(v))
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
                ("items", True, "list[DatasetRevision]", "DatasetRevision"),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("next_cursor", False, "str", ""),
            ],
        )
