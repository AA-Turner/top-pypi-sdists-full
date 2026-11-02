"""Nullable authored values retain the complete non-null transport contract."""

from dataclasses import dataclass
from functools import cached_property
from types import UnionType
from typing import TYPE_CHECKING, Generic, TypeVar, Union, cast, get_args, get_origin

from labqoat.json_document import JsonValue

if TYPE_CHECKING:
    from labqoat.compute.value_codec import ValueCodec

T = TypeVar("T")


@dataclass(frozen=True)
class OptionalCodec(Generic[T]):
    """Support exactly one value type plus None, including immutable reference inputs."""

    value_type: type[T]
    ancestors: tuple[object, ...] = ()

    @staticmethod
    def matches(value_type: object) -> bool:
        """Distinguish nullable values from ambiguous multi-type unions."""
        members = get_args(value_type)
        return get_origin(value_type) in (UnionType, Union) and len(members) == 2 and type(None) in members

    def schema(self) -> dict[str, JsonValue]:
        """Keep the reference descriptor intact inside an unambiguous nullable branch."""
        from labqoat.compute.value_codec import ValueCodec

        return {"anyOf": [ValueCodec(self.member(), self.ancestors).schema(), {"type": "null"}]}

    def convert(self, value: T) -> JsonValue:
        """Check a present value's type; the enclosing value validates the result once."""
        return None if value is None else self._present.convert(value)

    def restore(self, value: JsonValue) -> T:
        """Rebuild a present value its enclosing document already validated."""
        return cast(T, None) if value is None else self._present.restore(value)

    @cached_property
    def _present(self) -> "ValueCodec[T]":
        """Resolve the non-null codec once for every value this codec handles."""
        from labqoat.compute.value_codec import ValueCodec

        return ValueCodec(self.member(), self.ancestors)

    def member(self) -> type[T]:
        """Return the non-null type from an already selected optional annotation."""
        return cast(type[T], next(member for member in get_args(self.value_type) if member is not type(None)))
