"""Deterministic physical shape selection, separate from full Draft 2020-12 validation."""

from urllib.parse import unquote

from labqoat.data_layout.layout_node import LayoutNode
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.asset_schema import AssetSchema
from labqoat.schemas.schema_nodes import SchemaNodes


class LayoutCompiler:
    """Reject unrepresentable schemas rather than serializing arbitrary values to strings."""

    def __init__(self, nodes: dict[str, JsonValue]) -> None:
        """Retain the already captured local reference graph."""
        self._nodes = nodes

    @classmethod
    def compile(cls, schema: dict[str, JsonValue] | bool) -> LayoutNode:
        """Require a nonnullable record at the dataset row boundary."""
        nodes = dict(SchemaNodes.walk(schema))
        nodes.update(cls._anchors(nodes))
        root = cls(nodes)._node(schema, "", False, ())
        if root.kind != "object" or root.nullable:
            raise ValueError("/: dataset rows require a nonnullable object layout")
        return root

    @staticmethod
    def _anchors(nodes: dict[str, JsonValue]) -> dict[str, JsonValue]:
        """Resolve ordinary anchors only within captured schema positions."""
        return {
            anchor: node
            for node in nodes.values()
            if isinstance(node, dict) and isinstance(anchor := node.get("$anchor"), str)
        }

    def _node(self, value: JsonValue, pointer: str, optional: bool, seen: tuple[str, ...]) -> LayoutNode:
        """Use explicit declared types; other assertions remain enforced by the validator."""
        if not isinstance(value, dict):
            raise ValueError(f"{pointer}: a physical layout requires an explicit type")
        if "$dynamicRef" in value:
            raise ValueError(f"{pointer}/$dynamicRef: dynamic physical layouts are unsupported")
        if "$ref" in value:
            return self._reference(value, pointer, optional, seen)
        AssetSchema.check(value, pointer)
        kind, nullable = self._kind(value, pointer)
        children: tuple[tuple[str, LayoutNode], ...] = ()
        if kind == "object":
            children = self._object(value, pointer, seen)
        if kind == "array":
            children = self._array(value, pointer, seen)
        return LayoutNode(kind, nullable, optional, children, value.get("x-labqoat-type") == "asset")

    def _reference(
        self, value: dict[str, JsonValue], pointer: str, optional: bool, seen: tuple[str, ...]
    ) -> LayoutNode:
        """Reject recursive shapes while allowing reused, finite local definitions."""
        reference = JsonDocument.expect_scalar(value["$ref"], str)
        target = unquote(reference.removeprefix("#"))
        if target in seen:
            raise ValueError(f"{pointer}/$ref: recursive physical layouts are unsupported")
        return self._node(self._nodes[target], pointer, optional, (*seen, target))

    @staticmethod
    def _kind(value: dict[str, JsonValue], pointer: str) -> tuple[str, bool]:
        """Nullable single-kind unions have one lossless Arrow representation."""
        raw = value.get("type")
        types = raw if isinstance(raw, list) else [raw]
        nonnull = [kind for kind in types if kind != "null"]
        if len(nonnull) != 1 or nonnull[0] not in ("object", "array", "string", "integer", "number", "boolean"):
            raise ValueError(f"{pointer}/type: expected one explicit physical type, optionally unioned with null")
        return str(nonnull[0]), "null" in types

    def _object(
        self, value: dict[str, JsonValue], pointer: str, seen: tuple[str, ...]
    ) -> tuple[tuple[str, LayoutNode], ...]:
        """Closed records retain every declared field; arbitrary keys are not discarded."""
        if value.get("additionalProperties") is not False or value.get("patternProperties"):
            raise ValueError(f"{pointer}: object layouts require additionalProperties=false and fixed properties")
        properties = JsonDocument.expect_dict(value.get("properties", {}))
        if not properties:
            raise ValueError(f"{pointer}/properties: empty physical records are unsupported")
        required = JsonDocument.expect_list(value.get("required", []))
        return tuple(
            (name, self._node(properties[name], self._property(pointer, name), name not in required, seen))
            for name in sorted(properties)
        )

    def _array(
        self, value: dict[str, JsonValue], pointer: str, seen: tuple[str, ...]
    ) -> tuple[tuple[str, LayoutNode], ...]:
        """Represent homogeneous arrays, including nullable nested elements."""
        if value.get("prefixItems"):
            raise ValueError(f"{pointer}/prefixItems: tuple layouts are unsupported")
        return (("element", self._node(value.get("items"), pointer + "/items", False, seen)),)

    @staticmethod
    def _property(pointer: str, name: str) -> str:
        """Preserve schema-source locations for unsupported nested fields."""
        return pointer + "/properties/" + name.replace("~", "~0").replace("/", "~1")
