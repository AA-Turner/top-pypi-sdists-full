"""A durable dataset revision with captured schema and data-publication state."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetPublication:
    """A durable dataset revision with captured schema and data-publication state."""

    data_manifest: Mapping[str, JsonValue] | None
    data_manifest_digest: str | None
    dataset: str
    dataset_id: str
    deadline: str
    failure: Mapping[str, JsonValue] | None
    id: str
    inputs: list[JsonValue]
    intent_digest: str
    layout: Mapping[str, JsonValue]
    progress: Mapping[str, JsonValue]
    requested_tag: str | None
    revision_number: int
    schema: Mapping[str, JsonValue]
    schema_digest: str
    snapshot_metadata: Mapping[str, JsonValue]
    snapshot_ref: str | None
    status: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetPublication:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetPublication")
        return cls(
            data_manifest=JsonDocument.expect_optional_dict(values["data_manifest"]),
            data_manifest_digest=JsonDocument.expect_optional_scalar(values.get("data_manifest_digest"), str),
            dataset=JsonDocument.expect_scalar(values["dataset"], str),
            dataset_id=JsonDocument.expect_scalar(values["dataset_id"], str),
            deadline=JsonDocument.expect_scalar(values["deadline"], str),
            failure=JsonDocument.expect_optional_dict(values["failure"]),
            id=JsonDocument.expect_scalar(values["id"], str),
            inputs=list(JsonDocument.expect_list(values.get("inputs", []))),
            intent_digest=JsonDocument.expect_scalar(values["intent_digest"], str),
            layout=JsonDocument.expect_dict(values["layout"]),
            progress=JsonDocument.expect_dict(values["progress"]),
            requested_tag=JsonDocument.expect_optional_scalar(values.get("requested_tag"), str),
            revision_number=JsonDocument.expect_scalar(values["revision_number"], int),
            schema=JsonDocument.expect_dict(values["schema"]),
            schema_digest=JsonDocument.expect_scalar(values["schema_digest"], str),
            snapshot_metadata=JsonDocument.expect_dict(values["snapshot_metadata"]),
            snapshot_ref=JsonDocument.expect_optional_scalar(values.get("snapshot_ref"), str),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("data_manifest", True, "Mapping[str, JsonValue]", ""),
                ("data_manifest_digest", True, "str", ""),
                ("dataset", True, "str", ""),
                ("dataset_id", True, "str", ""),
                ("deadline", True, "str", ""),
                ("failure", True, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("inputs", True, "list[JsonValue]", "JsonValue"),
                ("intent_digest", True, "str", ""),
                ("layout", True, "Mapping[str, JsonValue]", ""),
                ("progress", True, "Mapping[str, JsonValue]", ""),
                ("requested_tag", True, "str", ""),
                ("revision_number", True, "int", ""),
                ("schema", True, "Mapping[str, JsonValue]", ""),
                ("schema_digest", True, "str", ""),
                ("snapshot_metadata", True, "Mapping[str, JsonValue]", ""),
                ("snapshot_ref", True, "str", ""),
                ("status", True, "str", ""),
            ],
        )
