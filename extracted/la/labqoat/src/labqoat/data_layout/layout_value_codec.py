"""Presence-aware value encoding and strict physical-value decoding."""

from labqoat.data_layout.layout_node import LayoutNode
from labqoat.json_document import JsonDocument, JsonValue


class LayoutValueCodec:
    """Bridge validated logical records and physical records without lossy casts."""

    @classmethod
    def encode(cls, node: LayoutNode, value: JsonValue, pointer: str = "") -> JsonValue:
        """Encode a schema-validated value and enforce physical integer boundaries."""
        if value is None:
            return None
        if node.kind == "object":
            return cls._encode_object(node, JsonDocument.expect_dict(value), pointer)
        if node.kind == "array":
            return cls._encode_array(node.children[0][1], JsonDocument.expect_list(value), pointer)
        if node.kind == "integer":
            return cls._integer(value, pointer)
        return value

    @classmethod
    def _encode_array(cls, child: LayoutNode, items: list[JsonValue], pointer: str) -> list[JsonValue]:
        """Pass plain scalar elements through together; name an element's position only where it is needed."""
        if child.kind in ("string", "number", "boolean"):
            return items
        if child.kind == "integer" and all(type(item) is int and abs(item) <= 9_007_199_254_740_991 for item in items):
            return items
        return [cls.encode(child, item, f"{pointer}/{index}") for index, item in enumerate(items)]

    @staticmethod
    def _integer(value: JsonValue, pointer: str) -> int:
        """JSON integers use the canonical interoperable safe-integer domain."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{pointer}: expected an integer")
        if value != int(value) or abs(value) > 9_007_199_254_740_991:
            raise ValueError(f"{pointer}: integer is outside the lossless safe-integer range")
        return int(value)

    @classmethod
    def _encode_object(cls, node: LayoutNode, value: dict[str, JsonValue], pointer: str) -> dict[str, JsonValue]:
        """Capture optional presence before Arrow supplies missing values as nulls."""
        result: dict[str, JsonValue] = {}
        for name, child in node.children:
            encoded = cls.encode(child, value.get(name), cls._pointer(pointer, name))
            result[name] = {"present": name in value, "value": encoded} if child.optional else encoded
        return result

    @classmethod
    def decode(cls, node: LayoutNode, value: JsonValue, pointer: str = "") -> JsonValue:
        """Decode physical values and their integer bounds; full schema validation follows at the row boundary."""
        if value is None:
            return None
        if node.kind == "object":
            return cls._decode_object(node, JsonDocument.expect_dict(value), pointer)
        if node.kind == "array":
            return cls._decode_array(node.children[0][1], JsonDocument.expect_list(value), pointer)
        if node.kind == "integer":
            return cls._integer(value, pointer)
        return value

    @classmethod
    def _decode_array(cls, child: LayoutNode, items: list[JsonValue], pointer: str) -> list[JsonValue]:
        """Pass plain scalar elements through together; name an element's position only where it is needed."""
        if child.kind == "integer":
            limit = 9_007_199_254_740_991
            if all(type(item) is int and -limit <= item <= limit for item in items):
                return items
        elif child.kind not in ("object", "array"):
            return items
        return [cls.decode(child, item, f"{pointer}/{index}") for index, item in enumerate(items)]

    @classmethod
    def _decode_object(cls, node: LayoutNode, value: dict[str, JsonValue], pointer: str) -> dict[str, JsonValue]:
        """Do not let an uploaded file hide a value behind a forged presence flag."""
        result: dict[str, JsonValue] = {}
        for name, child in node.children:
            path = cls._pointer(pointer, name)
            item = value[name]
            if child.optional:
                present, item = cls._presence(item, path)
                if not present:
                    continue
            result[name] = cls.decode(child, item, path)
        return result

    @staticmethod
    def _presence(value: JsonValue, pointer: str) -> tuple[bool, JsonValue]:
        """Validate physical presence records rather than trusting their metadata."""
        if not isinstance(value, dict) or type(value.get("present")) is not bool:
            raise ValueError(f"{pointer}: invalid optional presence wrapper")
        if not value["present"] and value["value"] is not None:
            raise ValueError(f"{pointer}: absent field carries a physical value")
        return bool(value["present"]), value["value"]

    @staticmethod
    def _pointer(parent: str, name: str) -> str:
        """Locate physical errors in the logical JSON record, not the storage wrapper."""
        return parent + "/" + name.replace("~", "~0").replace("/", "~1")
