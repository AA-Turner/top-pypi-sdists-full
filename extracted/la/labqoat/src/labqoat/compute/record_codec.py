"""Closed inline schemas and transport for ordinary authored dataclasses."""

from dataclasses import dataclass, fields, is_dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Generic, TypeVar, get_type_hints

from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.compute.value_codec import ValueCodec

T = TypeVar("T")


@dataclass(frozen=True)
class RecordCodec(Generic[T]):
    """Reconstruct declared Python rows while preserving nested reference positions."""

    value_type: type[T]
    ancestors: tuple[object, ...] = ()

    def schema(self) -> dict[str, JsonValue]:
        """Capture constructor fields inline and reject recursive or non-constructor state."""
        from labqoat.compute.value_codec import ValueCodec

        if self.value_type in self.ancestors or not is_dataclass(self.value_type):
            raise TypeError("Compute records must be nonrecursive dataclasses")
        declared = fields(self.value_type)
        if any(not item.init for item in declared):
            raise TypeError("Compute record fields must participate in construction")
        annotations = get_type_hints(self.value_type)
        ancestry = (*self.ancestors, self.value_type)
        properties: dict[str, JsonValue] = {
            item.name: ValueCodec(annotations[item.name], ancestry).schema() for item in declared
        }
        return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}

    def convert(self, value: T) -> JsonValue:
        """Check the record and field types; the enclosing value validates the result once."""
        if type(value) is not self.value_type:
            raise TypeError(f"Expected {self.value_type.__name__}")
        return {name: codec.convert(getattr(value, name)) for name, codec in self._members}

    def restore(self, value: JsonValue) -> T:
        """Invoke the real constructor with fields their enclosing document already validated."""
        values = JsonDocument.expect_dict(value)
        return self.value_type(**{name: codec.restore(values[name]) for name, codec in self._members})

    @cached_property
    def _members(self) -> "tuple[tuple[str, ValueCodec[object]], ...]":
        """Resolve each declared field's codec once for every record this codec handles."""
        from labqoat.compute.value_codec import ValueCodec

        annotations = get_type_hints(self.value_type)
        return tuple((item.name, ValueCodec(annotations[item.name])) for item in fields(self.value_type))  # type: ignore[arg-type]
