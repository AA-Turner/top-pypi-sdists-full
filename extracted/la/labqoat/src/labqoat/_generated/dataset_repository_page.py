"""One bounded page of repositories."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.dataset_repository import DatasetRepository
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRepositoryPage:
    """One bounded page of repositories."""

    items: list[DatasetRepository]
    links: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRepositoryPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRepositoryPage")
        return cls(
            items=[
                DatasetRepository.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            links=JsonDocument.expect_dict(values["links"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("items", True, "list[DatasetRepository]", "DatasetRepository"),
                ("links", True, "Mapping[str, JsonValue]", ""),
            ],
        )
