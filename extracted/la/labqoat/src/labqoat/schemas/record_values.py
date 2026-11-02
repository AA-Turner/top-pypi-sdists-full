"""Explicit JSON encoding for schema records and structured immutable asset identities."""

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.references import AssetRef
from labqoat.schemas.schema_record import SchemaRecord


class RecordValues:
    """Serialize schema-owned values without reflecting on arbitrary dataclasses or coercing inputs."""

    @staticmethod
    def encode(value: object) -> JsonValue:
        """Preserve JSON primitives and only the explicitly supported typed value boundaries."""
        if isinstance(value, SchemaRecord):
            return value.to_dict()
        if isinstance(value, AssetRef):
            return {
                "id": str(value.id),
                "blob_sha256": str(value.blob_sha256),
                "byte_size": value.byte_size,
                "media_type": value.media_type,
            }
        if isinstance(value, dict):
            return {JsonDocument.expect_scalar(name, str): RecordValues.encode(item) for name, item in value.items()}
        if isinstance(value, list):
            return [RecordValues.encode(item) for item in value]
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        raise ValueError(f"Unsupported schema record value: {type(value).__name__}")
