"""Explicit Python representability checks independent of full JSON Schema semantics."""

from collections.abc import Callable
from typing import ClassVar
from urllib.parse import unquote

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schema_codegen.field_type import FieldType
from labqoat.schema_codegen.schema_expression import SchemaExpression
from labqoat.schema_codegen.schema_projection import SchemaProjection
from labqoat.schemas.asset_schema import AssetSchema
from labqoat.schemas.schema_nodes import SchemaNodes


class SchemaTypes:
    """Compile finite scalar, literal, nullable union and homogeneous array field shapes."""

    _TYPES: ClassVar[dict[str, str]] = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "null": "None",
        "asset": "AssetRef",
    }

    def __init__(
        self,
        schema: dict[str, JsonValue],
        record: Callable[[JsonValue, str, int], FieldType],
        projection: SchemaProjection,
    ) -> None:
        """Capture schema positions and local anchors without importing authored modules."""
        self.nodes = dict(SchemaNodes.walk(schema))
        self.record = record
        self.projection = projection
        self.anchors = {
            str(node["$anchor"]): path
            for path, node in self.nodes.items()
            if isinstance(node, dict) and "$anchor" in node
        }

    def locate(self, value: JsonValue, pointer: str, seen: tuple[str, ...] = ()) -> tuple[JsonDocument, str]:
        """Resolve only finite captured references, keeping constraints in the full validator."""
        if not isinstance(value, dict) or "$dynamicRef" in value:
            raise ValueError(f"{pointer}: Python generation requires an explicit finite schema shape")
        if "$ref" not in value:
            return JsonDocument(value), pointer
        target = unquote(JsonDocument.expect_scalar(value["$ref"], str).removeprefix("#"))
        target = self.anchors.get(target, target)
        if target in seen:
            raise ValueError(f"{pointer}/$ref: recursive Python record shapes are unsupported")
        return self.locate(self.nodes[target], target, (*seen, target))

    def field(self, value: JsonValue, pointer: str, depth: int = 0) -> FieldType:
        """Reject unrepresentable structure rather than producing untyped fields."""
        if depth > 16:
            raise ValueError(f"{pointer}: Python field nesting exceeds the supported depth")
        node, location = self.locate(value, pointer)
        for keyword in ("anyOf", "oneOf"):
            if keyword in node:
                return self._union(node[keyword], location + "/" + keyword, depth)
        kinds = self._kinds(node, pointer)
        members = {kind: self._member(kind, node, location, depth, value, pointer) for kind in kinds}
        names = [member.annotation for member in members.values()]
        annotation = self._literal(node, kinds) or " | ".join(names)
        shape = self._shape(kinds, members)
        records = tuple(sorted({name for member in members.values() for name in member.records}))
        return FieldType(annotation, shape, records)

    def _union(self, branches: JsonValue, pointer: str, depth: int) -> FieldType:
        """Generate meaningful alternatives and retain full branch validation for runtime selection."""
        fields = []
        shapes = []
        for index, value in enumerate(JsonDocument.expect_list(branches)):
            location = pointer + "/" + str(index)
            field = self.field(value, location, depth + 1)
            schema = SchemaExpression.render(self.projection.capture(location))
            fields.append(field)
            shapes.append(f"({schema}, {field.shape})")
        annotation = " | ".join(dict.fromkeys(field.annotation for field in fields))
        records = tuple(sorted({name for field in fields for name in field.records}))
        return FieldType(annotation, "ValueUnion((" + ", ".join(shapes) + ",))", records)

    def _member(
        self, kind: str, node: JsonDocument, location: str, depth: int, value: JsonValue, pointer: str
    ) -> FieldType:
        """Construct scalar, array and nested record annotations with their matching decoders."""
        if kind == "array":
            item = self._item(node, location, depth)
            return FieldType(f"list[{item.annotation}]", item.shape, item.records)
        if kind == "object":
            return self.record(value, pointer, depth)
        return FieldType(self._TYPES[kind], "")

    @staticmethod
    def _shape(kinds: tuple[str, ...], members: dict[str, FieldType]) -> str:
        """Emit explicit decoder metadata without importing generated classes during discovery."""
        item = f", item={members['array'].shape}" if "array" in members else ""
        record = f", record={members['object'].annotation}" if "object" in members else ""
        return f"ValueShape({kinds!r}{item}{record})"

    def _item(self, node: JsonDocument, pointer: str, depth: int) -> FieldType:
        """Require homogeneous finite array element types."""
        if node.get("prefixItems"):
            raise ValueError(f"{pointer}/prefixItems: heterogeneous Python tuple generation is unsupported")
        return self.field(node.get("items"), pointer + "/items", depth + 1)

    @classmethod
    def _kinds(cls, node: JsonDocument, pointer: str) -> tuple[str, ...]:
        """Require explicit types whose structural meaning Python can preserve."""
        raw = node.get("type")
        kinds = raw if isinstance(raw, list) else [raw]
        AssetSchema.check(node, pointer)
        if node.get("x-labqoat-type") == "asset":
            kinds = ["asset" if kind == "object" else kind for kind in kinds]
        if not kinds or any(kind not in (*cls._TYPES, "array", "object") for kind in kinds):
            raise ValueError(f"{pointer}/type: expected explicit scalar or homogeneous-array Python types")
        return tuple(sorted((str(kind) for kind in kinds), key=cls._kind_order))

    @staticmethod
    def _kind_order(kind: str) -> tuple[bool, str]:
        """Keep null last and all other union members stable across schema ordering."""
        return kind == "null", kind

    @staticmethod
    def _literal(node: JsonDocument, kinds: tuple[str, ...]) -> str | None:
        """Express representable enum/constant values as Literal while retaining every assertion."""
        values = [node["const"]] if "const" in node else node.get("enum")
        if not isinstance(values, list) or "array" in kinds:
            return None
        if any(type(value) not in (str, int, bool, type(None)) for value in values):
            return None
        if "number" in kinds:
            return None
        return "Literal[" + ", ".join(repr(value) for value in values) + "]"
