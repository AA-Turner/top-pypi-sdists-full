"""A captured schema and its versioned physical layout shared by all data validation."""

from dataclasses import dataclass

import pyarrow as pa

from labqoat.data_layout.layout_compiler import LayoutCompiler
from labqoat.data_layout.layout_node import LayoutNode
from labqoat.data_layout.layout_value_codec import LayoutValueCodec
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.identity import Identity
from labqoat.schemas.schema_document import SchemaDocument


@dataclass(frozen=True)
class DatasetLayout:
    """Validate every logical row against its schema before lossless Parquet encoding."""

    schema: SchemaDocument
    root: LayoutNode

    @classmethod
    def capture(cls, schema: dict[str, JsonValue] | bool) -> "DatasetLayout":
        """Keep standards validation and physical representability as separate checks."""
        document = SchemaDocument.capture(schema)
        return cls(document, LayoutCompiler.compile(schema))

    @property
    def digest(self) -> str:
        """Bind schema constraints, presence encoding, and layout version in one identity."""
        return Identity.digest({"layout_version": 1, "schema_digest": self.schema.digest, "root": self.root.document()})

    @property
    def arrow_schema(self) -> pa.Schema:
        """Return the exact supported uploaded and materialized Parquet field types."""
        return pa.schema([child.arrow_field(name) for name, child in self.root.children])

    def encode(self, value: JsonValue) -> dict[str, JsonValue]:
        """Reject invalid values before Arrow can perform any implicit conversion."""
        self.schema.validate(value)
        return JsonDocument.expect_dict(LayoutValueCodec.encode(self.root, value))

    def physical(self, value: JsonValue) -> dict[str, JsonValue]:
        """Encode a row for upload without validating it here; the service validates every uploaded file."""
        return JsonDocument.expect_dict(LayoutValueCodec.encode(self.root, value))

    def logical(self, value: JsonValue) -> dict[str, JsonValue]:
        """Unwrap a stored row; published files were validated by the service and are verified by digest."""
        return JsonDocument.expect_dict(LayoutValueCodec.decode(self.root, value))
