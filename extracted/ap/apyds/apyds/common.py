"""Base class for all deductive system wrapper types."""

from __future__ import annotations

__all__ = [
    "Common",
]

import typing
from .buffer_size import buffer_size


class DsProto(typing.Protocol):
    """Protocol for deductive system base types."""

    @classmethod
    def from_string(cls, string: str, capacity: int) -> typing.Self: ...

    @classmethod
    def from_binary(cls, binary: memoryview) -> typing.Self: ...

    @classmethod
    def to_string(cls, value: typing.Self, capacity: int) -> str: ...

    @classmethod
    def to_binary(cls, value: typing.Self) -> bytes: ...

    def data_size(self) -> int: ...

    def clone(self) -> typing.Self: ...


T = typing.TypeVar("T", bound=DsProto)


class Common(typing.Generic[T]):
    """Base class for all deductive system wrapper types.

    Handles initialization, serialization, and common operations.
    """

    _base: type[T]

    def __init__(self, value: Common[T] | T | str | bytes, size: int | None = None) -> None:
        """Creates a new instance.

        Args:
            value: Initial value (can be another instance, base value, string, or memoryview).
            size: Optional buffer capacity for the internal storage.

        Raises:
            ValueError: If initialization fails or invalid arguments are provided.
            TypeError: If value is of an unsupported type.
        """
        self.value: T
        self.capacity: int | None
        if isinstance(value, type(self)):
            self.value = value.value
            self.capacity = value.capacity
            if size is not None:
                raise ValueError("Cannot set capacity when copying from another instance.")
        elif isinstance(value, self._base):
            self.value = value
            self.capacity = size
        elif isinstance(value, str):
            self.capacity = size if size is not None else buffer_size()
            self.value = self._base.from_string(value, self.capacity)
            if self.value is None:
                raise ValueError("Initialization from a string failed.")
        elif isinstance(value, memoryview):
            self.value = self._base.from_binary(value)
            self.capacity = self.size()
            if size is not None:
                raise ValueError("Cannot set capacity when initializing from bytes.")
        else:
            raise TypeError("Unsupported type for initialization.")

    def __str__(self) -> str:
        """Convert the value to a string representation.

        Returns:
            The string representation.

        Raises:
            ValueError: If conversion fails.
        """
        result = self._base.to_string(self.value, buffer_size())
        if result == "":
            raise ValueError("Conversion to string failed.")
        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__}[{self}]"

    def data(self) -> bytes:
        """Get the binary representation of the value.

        Returns:
            The binary data as bytes.
        """
        return self._base.to_binary(self.value)

    def size(self) -> int:
        """Get the size of the data in bytes.

        Returns:
            The data size.
        """
        return self.value.data_size()

    def __copy__(self) -> Common[T]:
        """Create a deep copy of this instance.

        Returns:
            A new instance with cloned value.
        """
        return type(self)(self.value.clone(), self.size())

    def __hash__(self) -> int:
        return hash(self.data())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Common):
            return False
        return self.data() == other.data()
