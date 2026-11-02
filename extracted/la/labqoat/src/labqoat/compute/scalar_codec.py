"""Portable scalar type capture and validated JSON transport."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

from labqoat.json_document import JsonValue
from labqoat.schemas.schema_document import SchemaDocument

T = TypeVar("T")


@dataclass(frozen=True)
class ScalarCodec(Generic[T]):
    """Capture the scalar types used by the first callable and host entrypoints."""

    value_type: type[T]

    def schema(self) -> dict[str, JsonValue]:
        """Reject unsupported transport types before publishing source or accepting work."""
        if self.value_type is int:
            return {"type": "integer", "minimum": -(2**53 - 1), "maximum": 2**53 - 1}
        kinds = {str: "string", bool: "boolean", float: "number", type(None): "null"}
        if self.value_type not in kinds:
            raise TypeError(
                f"Unsupported compute transport type: {self.value_type}. Annotate parameters and results as int, "
                "float, str, bool, None, Literal[...], T | None, list[T], tuple[T, ...], dict[str, T], a dataclass "
                "of these, Artifact, Dataset[Row] or Checkpoint[Metadata]; a bare dict or list needs element types."
            )
        return {"type": kinds[self.value_type]}

    def encode(self, value: T) -> JsonValue:
        """Enforce the declared Python type and canonical finite JSON bounds."""
        encoded = self.convert(value)
        SchemaDocument.capture(self.schema()).validate(encoded)
        return encoded

    def convert(self, value: T) -> JsonValue:
        """Enforce the declared Python type; the enclosing value validates bounds once for all its parts."""
        if type(value) is self.value_type:
            return cast(JsonValue, value)
        if self.value_type in (str, float, int) and self.widens(value):
            declared = cast(Callable[[object], JsonValue], self.value_type)
            return declared(value)
        expected = getattr(self.value_type, "__name__", str(self.value_type))
        hint = ""
        if type(value).__name__ in {"ResourceId", "Sha256", "AssetRef", "CheckpointRef", "UUID"}:
            hint = "; annotate the field as Artifact, Dataset or Checkpoint, or pass str(value)"
        raise TypeError(f"Expected {expected}, received {type(value).__name__}{hint}")

    def widens(self, value: object) -> bool:
        """Whether `value` is the declared type in all but name: a subclass of it, or an int where float is declared."""
        if isinstance(value, bool):
            return False
        if self.value_type is float and isinstance(value, int):
            return True
        return isinstance(value, self.value_type)

    def decode(self, value: JsonValue) -> T:
        """Validate the captured shape before restoring Python numeric identity."""
        SchemaDocument.capture(self.schema()).validate(value)
        return self.restore(value)

    def restore(self, value: JsonValue) -> T:
        """Restore Python numeric identity for a value its enclosing document already validated."""
        if self.value_type is int and isinstance(value, (int, float)):
            return cast(T, int(value))
        if self.value_type is float and isinstance(value, (int, float)):
            return cast(T, float(value))
        return cast(T, value)
