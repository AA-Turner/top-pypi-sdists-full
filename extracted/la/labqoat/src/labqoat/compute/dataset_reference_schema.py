"""Closed wire schema for a complete immutable typed dataset revision."""

from typing import cast

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.asset_schema import AssetSchema


class DatasetReferenceSchema:
    """Bind row types and every materialized revision identity without mutable selectors."""

    @staticmethod
    def document(digest: str) -> dict[str, JsonValue]:
        """Keep the descriptor aligned with the service's exact semantic reference schema."""
        identity: dict[str, JsonValue] = {
            "type": "string",
            "minLength": 71,
            "maxLength": 71,
            "pattern": "^sha256:[0-9a-f]{64}",
        }
        identifier = JsonDocument.expect_dict(AssetSchema.document()["properties"])["id"]
        properties: dict[str, JsonValue] = {
            "dataset_id": identifier,
            "repository": {"type": "string", "minLength": 1},
            "revision_id": identifier,
            "schema_digest": {"const": digest},
            "layout_digest": dict(identity),
            "data_manifest_digest": dict(identity),
            "snapshot_ref": {"type": "string", "minLength": 1},
        }
        return {
            "type": "object",
            "x-labqoat-type": "dataset",
            "properties": properties,
            "required": cast(list[JsonValue], sorted(properties)),
            "additionalProperties": False,
        }
