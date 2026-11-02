"""Portable homogeneous list and tuple transport for authored compute results."""

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Generic, TypeVar, cast, get_args, get_origin

from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.compute.value_codec import ValueCodec

T = TypeVar("T")


@dataclass(frozen=True)
class SequenceCodec(Generic[T]):
    """Preserve explicit element schemas and restore the authored collection type."""

    value_type: type[T]
    ancestors: tuple[object, ...] = ()

    def schema(self) -> dict[str, JsonValue]:
        """Keep element reference positions explicit for service-owned input and output pins."""
        from labqoat.compute.value_codec import ValueCodec

        return {"type": "array", "items": ValueCodec(self._item_type(), self.ancestors).schema()}

    def convert(self, value: T) -> JsonValue:
        """Check the collection and item types; the enclosing value validates the result once."""
        if type(value) is not get_origin(self.value_type):
            raise TypeError("Expected the declared compute sequence type")
        codec = self._item
        return [codec.convert(item) for item in cast(list[object] | tuple[object, ...], value)]

    def restore(self, value: JsonValue) -> T:
        """Rebuild the authored collection from items its enclosing document already validated."""
        codec = self._item
        decoded = [codec.restore(item) for item in JsonDocument.expect_list(value)]
        return cast(T, tuple(decoded) if get_origin(self.value_type) is tuple else decoded)

    @cached_property
    def _item(self) -> "ValueCodec[object]":
        """Resolve the item codec once for every element of every sequence this codec handles."""
        from labqoat.compute.value_codec import ValueCodec

        return ValueCodec(self._item_type())

    def _item_type(self) -> type[object]:
        """Require typed lists or homogeneous variadic tuples rather than ambiguous positional tuples."""
        arguments = get_args(self.value_type)
        expected = 2 if get_origin(self.value_type) is tuple else 1
        if len(arguments) != expected or (expected == 2 and arguments[1] is not Ellipsis):
            raise TypeError("Compute sequences require list[T] or tuple[T, ...]")
        return cast(type[object], arguments[0])
