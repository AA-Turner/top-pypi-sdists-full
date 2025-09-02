from __future__ import annotations

from typing import Callable, Generic, TypeVar, cast

T = TypeVar("T")


class CommandValueHandler(Generic[T]):
    def __init__(
        self, validator_function: Callable[[T], bool] | None = None, none_equivalent: bytes | None = None
    ) -> None:
        if none_equivalent is not None and not self._validate_byte_value(none_equivalent):
            raise ValueError("none_equivalent can only be bytes of length 1")

        self._validator_function = validator_function
        self._none_equivalent = none_equivalent

    def byte2native(self, byte_value: bytes) -> T | None:
        if not self._validate_byte_value(byte_value):
            raise ValueError("given value is not a single byte")

        if self._none_equivalent is not None and byte_value == self._none_equivalent:
            return None

        native_type = self.__orig_class__.__args__[0]  # type: ignore
        return cast(T, native_type(ord(byte_value)))

    def native2byte(self, native_value: T) -> bytes:
        if native_value is None:
            if self._none_equivalent is not None:
                return self._none_equivalent
            else:
                raise ValueError("None not a supported value")

        if not self._validate_native_value(native_value):
            raise ValueError("value not allowed by validator function")

        if isinstance(native_value, bool):
            return b"\x01" if native_value else b"\x00"
        elif isinstance(native_value, int):
            return bytes([native_value])
        else:
            raise ValueError(f"not a supported value type: {str(type(native_value))}")

    def _validate_native_value(self, native_value: T) -> bool:
        if self._validator_function is None:
            return True
        return self._validator_function(native_value)

    @staticmethod
    def _validate_byte_value(byte_value: bytes) -> bool:
        if not isinstance(byte_value, bytes):
            return False
        return len(byte_value) == 1

    @classmethod
    def chr2int(cls, v: bytes) -> int:
        if not cls._validate_byte_value(v):
            raise ValueError("not bytes of length 1")
        return v[0]

    @staticmethod
    def int2chr(v: int) -> bytes:
        if not 0 <= v <= 255:
            raise ValueError("given value must be >= 0 and <= 255")
        return v.to_bytes(1, byteorder="big")
