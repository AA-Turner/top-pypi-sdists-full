from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .choice import FSharpChoice_2
from .fsharp_collections import ComparisonIdentity_Structural, HashIdentity_Structural
from .option import value as value_1
from .system import ArgumentNullException__ctor_Z721C83C5, NullReferenceException__ctor
from .system_text import StringBuilder__Append_Z721C83C5
from .types import int32
from .util import IComparer_1, IEqualityComparer, IEqualityComparer_1, dispose, equals, ignore, structural_hash
from .util import int32 as int32_1


class ObjectExpr5(IEqualityComparer):
    def Equals(self, x: Any = None, y: Any = None) -> bool:
        return equals(x, y)

    def GetHashCode(self, x_1: Any = None) -> int32:
        return structural_hash(x_1)


LanguagePrimitives_GenericEqualityComparer: IEqualityComparer = ObjectExpr5()


class ObjectExpr6(IEqualityComparer):
    def Equals(self, x: Any = None, y: Any = None) -> bool:
        return equals(x, y)

    def GetHashCode(self, x_1: Any = None) -> int32:
        return structural_hash(x_1)


LanguagePrimitives_GenericEqualityERComparer: IEqualityComparer = ObjectExpr6()


def LanguagePrimitives_FastGenericComparer[T](__unit: None = None) -> IComparer_1[Any]:
    return ComparisonIdentity_Structural()


def LanguagePrimitives_FastGenericComparerFromTable[T](__unit: None = None) -> IComparer_1[Any]:
    return ComparisonIdentity_Structural()


def LanguagePrimitives_FastGenericEqualityComparer[T](__unit: None = None) -> IEqualityComparer_1[Any]:
    return HashIdentity_Structural()


def LanguagePrimitives_FastGenericEqualityComparerFromTable[T](__unit: None = None) -> IEqualityComparer_1[Any]:
    return HashIdentity_Structural()


def Operators_Failure(message: str) -> Exception:
    return Exception(message)


def Operators_FailurePattern(exn: Exception) -> str | None:
    return str(exn)


def Operators_NullArg[_A](argument_name: str) -> Any:
    raise ArgumentNullException__ctor_Z721C83C5(argument_name)


def Operators_Using[R, T](resource: T, action: Callable[[T], R]) -> R:
    try:
        return action(resource)

    finally:
        if equals(resource, None):
            pass

        else:
            copy_of_struct: T = resource
            dispose(copy_of_struct)


def Operators_Lock[_A, _B](_lockObj: Any, action: Callable[[], _B]) -> _B:
    return action()


def Operators_IsNull[T](value: Any | None = None) -> bool:
    if equals(value, None):
        return True

    else:
        return False


def Operators_IsNotNull[T](value: Any | None = None) -> bool:
    if equals(value, None):
        return False

    else:
        return True


def Operators_IsNullV[T](value: Any | None) -> bool:
    return not (value is not None)


def Operators_NonNull[T](value: T | None = None) -> T | None:
    if equals(value, None):
        raise NullReferenceException__ctor()

    else:
        return value


def Operators_NonNullV[T](value: T | None) -> T:
    if value is not None:
        return value_1(value)

    else:
        raise NullReferenceException__ctor()


def Operators_NullMatchPattern[T](value: T | None = None) -> Any:
    if equals(value, None):
        return FSharpChoice_2(int32_1(0), None)

    else:
        return FSharpChoice_2(int32_1(1), value)


def Operators_NullValueMatchPattern[T](value: T | None) -> Any:
    if value is not None:
        return FSharpChoice_2(int32_1(1), value_1(value))

    else:
        return FSharpChoice_2(int32_1(0), None)


def Operators_NonNullQuickPattern[T](value: T | None = None) -> T | None:
    if equals(value, None):
        raise NullReferenceException__ctor()

    else:
        return value


def Operators_NonNullQuickValuePattern[T](value: T | None) -> T:
    if value is not None:
        return value_1(value)

    else:
        raise NullReferenceException__ctor()


def Operators_WithNull[T](value: T | None = None) -> T | None:
    return value


def Operators_WithNullV[T](value: T | None = None) -> T | None:
    return value


def Operators_NullV[T](__unit: None = None) -> Any | None:
    return None


def Operators_NullArgCheck[T](argument_name: str, value: T) -> T:
    if equals(value, None):
        raise ArgumentNullException__ctor_Z721C83C5(argument_name)

    else:
        return value


def ExtraTopLevelOperators_LazyPattern[_A](input: Any) -> _A:
    return input.Value


def PrintfModule_PrintFormatToStringBuilderThen[_A, _B](
    continuation: Callable[[], _A], builder: Any, format: Any
) -> _B:
    def append(s: str, continuation: Any = continuation, builder: Any = builder, format: Any = format) -> _A:
        ignore(StringBuilder__Append_Z721C83C5(builder, s))
        return continuation()

    return format.cont(append)


def PrintfModule_PrintFormatToStringBuilder[_A](builder: Any, format: Any) -> _A:
    def _arrow7(__unit: None = None, builder: Any = builder, format: Any = format) -> None:
        ignore(None)

    return PrintfModule_PrintFormatToStringBuilderThen(_arrow7, builder, format)


__all__ = [
    "LanguagePrimitives_GenericEqualityComparer",
    "LanguagePrimitives_GenericEqualityERComparer",
    "LanguagePrimitives_FastGenericComparer",
    "LanguagePrimitives_FastGenericComparerFromTable",
    "LanguagePrimitives_FastGenericEqualityComparer",
    "LanguagePrimitives_FastGenericEqualityComparerFromTable",
    "Operators_Failure",
    "Operators_FailurePattern",
    "Operators_NullArg",
    "Operators_Using",
    "Operators_Lock",
    "Operators_IsNull",
    "Operators_IsNotNull",
    "Operators_IsNullV",
    "Operators_NonNull",
    "Operators_NonNullV",
    "Operators_NullMatchPattern",
    "Operators_NullValueMatchPattern",
    "Operators_NonNullQuickPattern",
    "Operators_NonNullQuickValuePattern",
    "Operators_WithNull",
    "Operators_WithNullV",
    "Operators_NullV",
    "Operators_NullArgCheck",
    "ExtraTopLevelOperators_LazyPattern",
    "PrintfModule_PrintFormatToStringBuilderThen",
    "PrintfModule_PrintFormatToStringBuilder",
]
