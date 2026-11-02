"""String-keyed typed mappings for authored scalar metric results."""

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Generic, TypeVar, cast, get_args

from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.compute.value_codec import ValueCodec

T = TypeVar("T")


@dataclass(frozen=True)
class MappingCodec(Generic[T]):
    """Keep dynamic keys separate from each value's explicit captured schema."""

    value_type: type[T]
    ancestors: tuple[object, ...] = ()

    def schema(self) -> dict[str, JsonValue]:
        """Capture only mappings whose keys have an unambiguous JSON representation."""
        from labqoat.compute.value_codec import ValueCodec

        return {"type": "object", "additionalProperties": ValueCodec(self._item_type(), self.ancestors).schema()}

    def convert(self, value: T) -> JsonValue:
        """Check keys and value types; the enclosing value validates the result once."""
        if not isinstance(value, dict) or any(type(key) is not str for key in value):
            raise TypeError("Expected a string-keyed compute dictionary")
        codec = self._item
        return {key: codec.convert(item) for key, item in value.items()}

    def restore(self, value: JsonValue) -> T:
        """Rebuild the authored dictionary from members its enclosing document already validated."""
        codec = self._item
        return cast(T, {key: codec.restore(item) for key, item in JsonDocument.expect_dict(value).items()})

    @cached_property
    def _item(self) -> "ValueCodec[object]":
        """Resolve the value codec once for every member of every mapping this codec handles."""
        from labqoat.compute.value_codec import ValueCodec

        return ValueCodec(self._item_type())

    def _item_type(self) -> type[object]:
        """Reject omitted annotations and nonstring dictionary keys before publication."""
        arguments = get_args(self.value_type)
        if len(arguments) != 2 or arguments[0] is not str:
            raise TypeError("Compute mappings require dict[str, T]")
        return cast(type[object], arguments[1])
