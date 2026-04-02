from __future__ import annotations

from typing import Any

from .array_ import Array
from .bases import StringableBase
from .core import float64, int32
from .exceptions import to_string
from .reflection import TypeInfo, class_type
from .string_ import format, get_length, is_null_or_empty, join, replace, replicate, substring
from .util import UNIT, Unit, clear, range, string_hash, to_enumerable


def _expr250() -> TypeInfo:
    return class_type("System.Text.StringBuilder", None, StringBuilder)


class StringBuilder(StringableBase):
    def __init__(self, value: str, capacity: int32) -> None:
        self.buf: list[str] = []
        if not is_null_or_empty(value):
            (self.buf.append(value))

    def ToString(self, __unit: Unit = UNIT) -> str:
        _: StringBuilder = self
        return join("", to_enumerable(_.buf))

    def Equals(self, other: Any = None) -> bool:
        x: StringBuilder = self
        return (to_string(x) == to_string(other)) if isinstance(other, StringBuilder) else False

    def GetHashCode(self, __unit: Unit = UNIT) -> int32:
        x: StringBuilder = self
        return string_hash(to_string(x))


StringBuilder_reflection = _expr250


def StringBuilder__ctor_Z18115A39(value: str, capacity: int32) -> StringBuilder:
    return StringBuilder(value, capacity)


def StringBuilder__ctor_Z524259A4(capacity: int32) -> StringBuilder:
    return StringBuilder__ctor_Z18115A39("", capacity)


def StringBuilder__ctor_Z721C83C5(value: str) -> StringBuilder:
    return StringBuilder__ctor_Z18115A39(value, int32.SIXTEEN)


def StringBuilder__ctor(__unit: Unit = UNIT) -> StringBuilder:
    return StringBuilder__ctor_Z18115A39("", int32.SIXTEEN)


def StringBuilder__Append_Z721C83C5(x: StringBuilder, s: str) -> StringBuilder:
    (x.buf.append(s))
    return x


def StringBuilder__Append_487EF8FB(x: StringBuilder, s: str, start_index: int32, count: int32) -> StringBuilder:
    (x.buf.append(substring(s, start_index, count)))
    return x


def StringBuilder__Append_244C7CD6(x: StringBuilder, c: str) -> StringBuilder:
    (x.buf.append(c))
    return x


def StringBuilder__Append_61B1CA(x: StringBuilder, c: str, repeat_count: int32) -> StringBuilder:
    s: str = replicate(repeat_count, c)
    (x.buf.append(s))
    return x


def StringBuilder__Append_Z524259A4(x: StringBuilder, o: int32) -> StringBuilder:
    (x.buf.append(int32(o).to_string()))
    return x


def StringBuilder__Append_5E38073B(x: StringBuilder, o: float64) -> StringBuilder:
    (x.buf.append(to_string(o)))
    return x


def StringBuilder__Append_Z1FBCCD16(x: StringBuilder, o: bool) -> StringBuilder:
    (x.buf.append(to_string(o)))
    return x


def StringBuilder__Append_4E60E31B(x: StringBuilder, o: Any = None) -> StringBuilder:
    (x.buf.append(to_string(o)))
    return x


def StringBuilder__Append_Z372E4D23(x: StringBuilder, cs: Array[str]) -> StringBuilder:
    (x.buf.append("".join(cs)))
    return x


def StringBuilder__Append_43A65C09(x: StringBuilder, s: StringBuilder) -> StringBuilder:
    (x.buf.append(to_string(s)))
    return x


def StringBuilder__AppendFormat_433E080(x: StringBuilder, fmt: str, o: Any = None) -> StringBuilder:
    (x.buf.append(format(fmt, o)))
    return x


def StringBuilder__AppendFormat_Z3B30EC65(x: StringBuilder, fmt: str, o1: Any = None, o2: Any = None) -> StringBuilder:
    (x.buf.append(format(fmt, o1, o2)))
    return x


def StringBuilder__AppendFormat_10D165E0(
    x: StringBuilder, fmt: str, o1: Any = None, o2: Any = None, o3: Any = None
) -> StringBuilder:
    (x.buf.append(format(fmt, o1, o2, o3)))
    return x


def StringBuilder__AppendFormat_Z17053F5(x: StringBuilder, fmt: str, arr: Array[Any]) -> StringBuilder:
    (x.buf.append(format(fmt, *arr)))
    return x


def StringBuilder__AppendFormat_Z696D8D1B(x: StringBuilder, provider: Any, fmt: str, o: Any = None) -> StringBuilder:
    (x.buf.append(format(provider, fmt, o)))
    return x


def StringBuilder__AppendFormat_26802C9E(
    x: StringBuilder, provider: Any, fmt: str, o1: Any = None, o2: Any = None
) -> StringBuilder:
    (x.buf.append(format(provider, fmt, o1, o2)))
    return x


def StringBuilder__AppendFormat_Z471ADCBB(
    x: StringBuilder, provider: Any, fmt: str, o1: Any = None, o2: Any = None, o3: Any = None
) -> StringBuilder:
    (x.buf.append(format(provider, fmt, o1, o2, o3)))
    return x


def StringBuilder__AppendFormat_6C2E3E6E(x: StringBuilder, provider: Any, fmt: str, arr: Array[Any]) -> StringBuilder:
    (x.buf.append(format(provider, fmt, *arr)))
    return x


def StringBuilder__AppendLine(x: StringBuilder) -> StringBuilder:
    (x.buf.append("\n"))
    return x


def StringBuilder__AppendLine_Z721C83C5(x: StringBuilder, s: str) -> StringBuilder:
    (x.buf.append(s))
    (x.buf.append("\n"))
    return x


def StringBuilder__Clear(x: StringBuilder) -> StringBuilder:
    clear(x.buf)
    return x


def StringBuilder__get_Chars_Z524259A4(x: StringBuilder, index: int32) -> str:
    len_1: int32 = int32.ZERO
    i: int32 = int32.ZERO
    while ((len_1 + get_length(x.buf[i])) <= index) if (i < int32(len(x.buf))) else False:
        len_1 = len_1 + get_length(x.buf[i])
        i = i + int32.ONE
    if True if (index < int32.ZERO) else (i >= int32(len(x.buf))):
        raise Exception("Index was outside the bounds of the array")

    else:
        pos: int32 = index - len_1
        return x.buf[i][pos]


def StringBuilder__set_Chars_413E0D0A(x: StringBuilder, index: int32, value: str) -> None:
    len_1: int32 = int32.ZERO
    i: int32 = int32.ZERO
    while ((len_1 + get_length(x.buf[i])) <= index) if (i < int32(len(x.buf))) else False:
        len_1 = len_1 + get_length(x.buf[i])
        i = i + int32.ONE
    if True if (index < int32.ZERO) else (i >= int32(len(x.buf))):
        raise Exception("Index was outside the bounds of the array")

    else:
        pos: int32 = index - len_1
        x.buf[i] = (x.buf[i][int32.ZERO : (pos - int32.ONE) + int32.ONE] + value) + x.buf[i][
            pos + int32.ONE : len(x.buf[i])
        ]


def StringBuilder__Replace_Z766F94C0(x: StringBuilder, old_value: str, new_value: str) -> StringBuilder:
    for i in range(int32(len(x.buf)) - int32.ONE, int32.ZERO, -1):
        x.buf[i] = replace(x.buf[i], old_value, new_value)
    return x


def StringBuilder__Replace_Z384F8060(x: StringBuilder, old_value: str, new_value: str) -> StringBuilder:
    str_1: str = replace(to_string(x), old_value, new_value)
    return StringBuilder__Append_Z721C83C5(StringBuilder__Clear(x), str_1)


def StringBuilder__get_Length(x: StringBuilder) -> int32:
    len_1: int32 = int32.ZERO
    for i in range(int32(len(x.buf)) - int32.ONE, int32.ZERO, -1):
        len_1 = len_1 + get_length(x.buf[i])
    return len_1


def StringBuilder__ToString_Z37302880(x: StringBuilder, first_index: int32, length: int32) -> str:
    return substring(to_string(x), first_index, length)


__all__ = [
    "StringBuilder__AppendFormat_10D165E0",
    "StringBuilder__AppendFormat_26802C9E",
    "StringBuilder__AppendFormat_433E080",
    "StringBuilder__AppendFormat_6C2E3E6E",
    "StringBuilder__AppendFormat_Z17053F5",
    "StringBuilder__AppendFormat_Z3B30EC65",
    "StringBuilder__AppendFormat_Z471ADCBB",
    "StringBuilder__AppendFormat_Z696D8D1B",
    "StringBuilder__AppendLine",
    "StringBuilder__AppendLine_Z721C83C5",
    "StringBuilder__Append_244C7CD6",
    "StringBuilder__Append_43A65C09",
    "StringBuilder__Append_487EF8FB",
    "StringBuilder__Append_4E60E31B",
    "StringBuilder__Append_5E38073B",
    "StringBuilder__Append_61B1CA",
    "StringBuilder__Append_Z1FBCCD16",
    "StringBuilder__Append_Z372E4D23",
    "StringBuilder__Append_Z524259A4",
    "StringBuilder__Append_Z721C83C5",
    "StringBuilder__Clear",
    "StringBuilder__Replace_Z384F8060",
    "StringBuilder__Replace_Z766F94C0",
    "StringBuilder__ToString_Z37302880",
    "StringBuilder__ctor",
    "StringBuilder__ctor_Z524259A4",
    "StringBuilder__ctor_Z721C83C5",
    "StringBuilder__get_Chars_Z524259A4",
    "StringBuilder__get_Length",
    "StringBuilder__set_Chars_413E0D0A",
    "StringBuilder_reflection",
]
