"""Check schema ownership and exact captured requirements inside static manifests."""

from typing import ClassVar

from labqoat.json_document import JsonDocument
from labqoat.schemas.schema_document import SchemaDocument


class ManifestSchemas:
    """Keep embedded-schema validation distinct from the REST or manifest envelope."""

    schema_fields: ClassVar[tuple[str, ...]] = ("schema",)

    @classmethod
    def validate(cls, kind: str, document: JsonDocument) -> None:
        """Reject schema drift and invalid checkpoint metadata before capture."""
        cls._fields(document, "")
        if kind == "checkpoint":
            schema = cls._schema(document, "schema")
            schema.validate(document["metadata"])

    @classmethod
    def _fields(cls, document: JsonDocument, pointer: str) -> None:
        """Validate complete schema semantics and any adjacent digest binding."""
        for field in cls.schema_fields:
            if field in document:
                schema = cls._schema(document, field)
                cls._digest(document, field, schema, pointer)

    @staticmethod
    def _schema(document: JsonDocument, field: str) -> SchemaDocument:
        """Capture a schema shape already checked by the versioned envelope."""
        value = document[field]
        schema = value if isinstance(value, bool) else JsonDocument.expect_dict(value)
        return SchemaDocument.capture(schema)

    @staticmethod
    def _digest(document: JsonDocument, field: str, schema: SchemaDocument, pointer: str) -> None:
        """Compare exact identities rather than guessing schema compatibility."""
        if field == "schema" and "schema_digest" in document and schema.digest != document["schema_digest"]:
            raise ValueError(f"{pointer}/schema_digest: schema digest mismatch")
