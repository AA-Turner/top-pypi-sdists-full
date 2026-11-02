"""An immutable revision owning its schema, layout and data manifest."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRevision:
    """An immutable revision owning its schema, layout and data manifest."""

    data_manifest: Mapping[str, JsonValue] | None
    data_manifest_digest: str | None
    id: str
    layout: Mapping[str, JsonValue]
    links: Mapping[str, JsonValue]
    repository_id: str
    revision_number: int
    schema: Mapping[str, JsonValue]
    schema_digest: str
    status: str
    storage_prefix: str
    lineage: Mapping[str, JsonValue] | None = None
    manifest: Mapping[str, JsonValue] | None = None
    snapshot_ref: str | None = None
    validation: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRevision:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRevision")
        return cls(
            data_manifest=JsonDocument.expect_optional_dict(values["data_manifest"]),
            data_manifest_digest=JsonDocument.expect_optional_scalar(values.get("data_manifest_digest"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            layout=JsonDocument.expect_dict(values["layout"]),
            lineage=JsonDocument.expect_optional_dict(values.get("lineage")),
            links=JsonDocument.expect_dict(values["links"]),
            manifest=JsonDocument.expect_optional_dict(values.get("manifest")),
            repository_id=JsonDocument.expect_scalar(values["repository_id"], str),
            revision_number=JsonDocument.expect_scalar(values["revision_number"], int),
            schema=JsonDocument.expect_dict(values["schema"]),
            schema_digest=JsonDocument.expect_scalar(values["schema_digest"], str),
            snapshot_ref=JsonDocument.expect_optional_scalar(values.get("snapshot_ref"), str),
            status=JsonDocument.expect_scalar(values["status"], str),
            storage_prefix=JsonDocument.expect_scalar(values["storage_prefix"], str),
            validation=JsonDocument.expect_optional_dict(values.get("validation")),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("data_manifest", True, "Mapping[str, JsonValue]", ""),
                ("data_manifest_digest", True, "str", ""),
                ("id", True, "str", ""),
                ("layout", True, "Mapping[str, JsonValue]", ""),
                ("lineage", False, "Mapping[str, JsonValue]", ""),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("manifest", False, "Mapping[str, JsonValue]", ""),
                ("repository_id", True, "str", ""),
                ("revision_number", True, "int", ""),
                ("schema", True, "Mapping[str, JsonValue]", ""),
                ("schema_digest", True, "str", ""),
                ("snapshot_ref", False, "str", ""),
                ("status", True, "str", ""),
                ("storage_prefix", True, "str", ""),
                ("validation", False, "Mapping[str, JsonValue]", ""),
            ],
        )
