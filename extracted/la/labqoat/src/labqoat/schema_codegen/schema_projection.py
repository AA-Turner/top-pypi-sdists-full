"""Closed schema projections for independently validated generated nested records."""

from urllib.parse import unquote

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.identity import Identity
from labqoat.schemas.schema_document import SchemaDocument
from labqoat.schemas.schema_nodes import SchemaNodes


class SchemaProjection:
    """Retain every assertion and captured reference when selecting a nested schema position."""

    def __init__(self, schema: dict[str, JsonValue]) -> None:
        """Own canonical input separately from the rebased nested-record validation bundle."""
        self.schema = SchemaDocument.capture(schema)
        self.document = JsonDocument.expect_dict(Identity.decode(self.schema.canonical.decode()))
        nodes = dict(SchemaNodes.walk(self.document))
        self.anchors = {
            str(node["$anchor"]): path for path, node in nodes.items() if isinstance(node, dict) and "$anchor" in node
        }
        for path, node in nodes.items():
            if isinstance(node, dict):
                self._rebase(node, path)

    def _rebase(self, node: dict[str, JsonValue], path: str) -> None:
        """Rewrite schema-position references only; instance annotations remain opaque."""
        if "$id" in node or "$dynamicRef" in node:
            raise ValueError(f"{path}: Python generation requires a single static captured reference scope")
        if "$ref" in node:
            target = unquote(JsonDocument.expect_scalar(node["$ref"], str).removeprefix("#"))
            node["$ref"] = "#/$defs/captured" + self.anchors.get(target, target)

    def capture(self, pointer: str) -> SchemaDocument:
        """Use exact root bytes for the public record and a closed bundle for each nested record."""
        if not pointer:
            return self.schema
        return SchemaDocument.capture({"$defs": {"captured": self.document}, "$ref": "#/$defs/captured" + pointer})
