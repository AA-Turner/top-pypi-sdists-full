from typing import overload
from enum import IntEnum
import typing

import System
import System.Numerics.Colors

System_Numerics_Colors_Argb = typing.Any
System_Numerics_Colors_Rgba = typing.Any

System_Numerics_Colors_Argb_T = typing.TypeVar("System_Numerics_Colors_Argb_T")
System_Numerics_Colors_Rgba_T = typing.TypeVar("System_Numerics_Colors_Rgba_T")


class Argb(typing.Generic[System_Numerics_Colors_Argb_T], System.IEquatable[System_Numerics_Colors_Argb]):
    """This class has no documentation."""

    @property
    def a(self) -> System_Numerics_Colors_Argb_T:
        ...

    @property
    def r(self) -> System_Numerics_Colors_Argb_T:
        ...

    @property
    def g(self) -> System_Numerics_Colors_Argb_T:
        ...

    @property
    def b(self) -> System_Numerics_Colors_Argb_T:
        ...

    @overload
    def __init__(self, a: System_Numerics_Colors_Argb_T, r: System_Numerics_Colors_Argb_T, g: System_Numerics_Colors_Argb_T, b: System_Numerics_Colors_Argb_T) -> None:
        ...

    @overload
    def __init__(self, values: System.ReadOnlySpan[System_Numerics_Colors_Argb_T]) -> None:
        ...

    def copy_to(self, destination: System.Span[System_Numerics_Colors_Argb_T]) -> None:
        ...

    @staticmethod
    def create_big_endian(color: int) -> System.Numerics.Colors.Argb[int]:
        ...

    @staticmethod
    def create_little_endian(color: int) -> System.Numerics.Colors.Argb[int]:
        ...

    @overload
    def equals(self, other: System.Numerics.Colors.Argb[System_Numerics_Colors_Argb_T]) -> bool:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    def get_hash_code(self) -> int:
        ...

    def to_rgba(self) -> System.Numerics.Colors.Rgba[System_Numerics_Colors_Argb_T]:
        ...

    def to_string(self) -> str:
        ...

    @staticmethod
    def to_u_int_32_big_endian(color: System.Numerics.Colors.Argb[int]) -> int:
        ...

    @staticmethod
    def to_u_int_32_little_endian(color: System.Numerics.Colors.Argb[int]) -> int:
        ...


class Rgba(typing.Generic[System_Numerics_Colors_Rgba_T], System.IEquatable[System_Numerics_Colors_Rgba]):
    """This class has no documentation."""

    @property
    def r(self) -> System_Numerics_Colors_Rgba_T:
        ...

    @property
    def g(self) -> System_Numerics_Colors_Rgba_T:
        ...

    @property
    def b(self) -> System_Numerics_Colors_Rgba_T:
        ...

    @property
    def a(self) -> System_Numerics_Colors_Rgba_T:
        ...

    @overload
    def __init__(self, r: System_Numerics_Colors_Rgba_T, g: System_Numerics_Colors_Rgba_T, b: System_Numerics_Colors_Rgba_T, a: System_Numerics_Colors_Rgba_T) -> None:
        ...

    @overload
    def __init__(self, values: System.ReadOnlySpan[System_Numerics_Colors_Rgba_T]) -> None:
        ...

    def copy_to(self, destination: System.Span[System_Numerics_Colors_Rgba_T]) -> None:
        ...

    @staticmethod
    def create_big_endian(color: int) -> System.Numerics.Colors.Rgba[int]:
        ...

    @staticmethod
    def create_little_endian(color: int) -> System.Numerics.Colors.Rgba[int]:
        ...

    @overload
    def equals(self, other: System.Numerics.Colors.Rgba[System_Numerics_Colors_Rgba_T]) -> bool:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    def get_hash_code(self) -> int:
        ...

    def to_argb(self) -> System.Numerics.Colors.Argb[System_Numerics_Colors_Rgba_T]:
        ...

    def to_string(self) -> str:
        ...

    @staticmethod
    def to_u_int_32_big_endian(color: System.Numerics.Colors.Rgba[int]) -> int:
        ...

    @staticmethod
    def to_u_int_32_little_endian(color: System.Numerics.Colors.Rgba[int]) -> int:
        ...


