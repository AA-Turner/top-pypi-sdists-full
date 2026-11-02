"""Files materialized by one immutable dataset revision."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.materialized_dataset_file import MaterializedDatasetFile
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRevisionFiles:
    """Files materialized by one immutable dataset revision."""

    data_manifest: Mapping[str, JsonValue]
    data_manifest_digest: str
    files: list[MaterializedDatasetFile]
    layout: Mapping[str, JsonValue]
    layout_digest: str
    revision_id: str
    schema: Mapping[str, JsonValue]
    schema_digest: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRevisionFiles:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRevisionFiles")
        return cls(
            data_manifest=JsonDocument.expect_dict(values["data_manifest"]),
            data_manifest_digest=JsonDocument.expect_scalar(values["data_manifest_digest"], str),
            files=[
                MaterializedDatasetFile.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("files", []))
            ],
            layout=JsonDocument.expect_dict(values["layout"]),
            layout_digest=JsonDocument.expect_scalar(values["layout_digest"], str),
            revision_id=JsonDocument.expect_scalar(values["revision_id"], str),
            schema=JsonDocument.expect_dict(values["schema"]),
            schema_digest=JsonDocument.expect_scalar(values["schema_digest"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("data_manifest", True, "Mapping[str, JsonValue]", ""),
                ("data_manifest_digest", True, "str", ""),
                ("files", True, "list[MaterializedDatasetFile]", "MaterializedDatasetFile"),
                ("layout", True, "Mapping[str, JsonValue]", ""),
                ("layout_digest", True, "str", ""),
                ("revision_id", True, "str", ""),
                ("schema", True, "Mapping[str, JsonValue]", ""),
                ("schema_digest", True, "str", ""),
            ],
        )
