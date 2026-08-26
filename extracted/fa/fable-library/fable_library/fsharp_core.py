from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from .choice import Choice1Of2, Choice2Of2, FSharpChoice_2
from .fsharp_collections import ComparisonIdentity_Structural, HashIdentity_Structural
from .option import value as value_1
from .protocols import IComparer_1, IDisposable, IEqualityComparer, IEqualityComparer_1
from .system import ArgumentNullException__ctor_Z721C83C5, NullReferenceException__ctor
from .system_text import StringBuilder__Append_Z721C83C5
from .types import ExceptionBase
from .util import UNIT, Unit, dispose, equals, ignore, structural_hash


class ObjectExpr5(IEqualityComparer):
    def Equals(self, x: Any = None, y: Any = None) -> bool:
        return equals(x, y)

    def GetHashCode(self, x_1: Any = None) -> int:
        return structural_hash(x_1)


LanguagePrimitives_GenericEqualityComparer: IEqualityComparer = ObjectExpr5()


class ObjectExpr6(IEqualityComparer):
    def Equals(self, x: Any = None, y: Any = None) -> bool:
        return equals(x, y)

    def GetHashCode(self, x_1: Any = None) -> int:
        return structural_hash(x_1)


LanguagePrimitives_GenericEqualityERComparer: IEqualityComparer = ObjectExpr6()


def LanguagePrimitives_FastGenericComparer[T](__unit: Unit = UNIT) -> IComparer_1[T]:
    return ComparisonIdentity_Structural()


def LanguagePrimitives_FastGenericComparerFromTable[T](__unit: Unit = UNIT) -> IComparer_1[T]:
    return ComparisonIdentity_Structural()


def LanguagePrimitives_FastGenericEqualityComparer[T](__unit: Unit = UNIT) -> IEqualityComparer_1[Any]:
    return HashIdentity_Structural()


def LanguagePrimitives_FastGenericEqualityComparerFromTable[T](__unit: Unit = UNIT) -> IEqualityComparer_1[Any]:
    return HashIdentity_Structural()


def Operators_Failure(message: str) -> Exception:
    return ExceptionBase(message)


def Operators_FailurePattern(exn: Exception) -> str | None:
    return str(exn)


def Operators_NullArg[_A](argument_name: str) -> _A:
    raise ArgumentNullException__ctor_Z721C83C5(argument_name)


def Operators_Using[T: IDisposable, R](resource: T, action: Callable[[T], R]) -> R:
    try:
        return action(resource)

    finally:
        if equals(resource, cast(Any, None)):
            pass

        else:
            copy_of_struct: Any = resource
            dispose(copy_of_struct)


def Operators_Lock[_A, _B](_lockObj: _A, action: Callable[[], _B]) -> _B:
    return action()


def Operators_IsNull[T](value: T = UNIT) -> bool:
    if equals(value, cast(Any, None)):
        return True

    else:
        return False


def Operators_IsNotNull[T](value: T = UNIT) -> bool:
    if equals(value, cast(Any, None)):
        return False

    else:
        return True


def Operators_IsNullV[T: Any](value: T | None) -> bool:
    return not (value is not None)


def Operators_NonNull[T](value: T = UNIT) -> T:
    if equals(value, cast(Any, None)):
        raise NullReferenceException__ctor()

    else:
        return value


def Operators_NonNullV[T: Any](value: T | None) -> T:
    if value is not None:
        return value_1(value)

    else:
        raise NullReferenceException__ctor()


def Operators_NullMatchPattern[T](value: T = UNIT) -> FSharpChoice_2[None, T]:
    if equals(value, cast(Any, None)):
        return Choice1Of2(None)

    else:
        return Choice2Of2(value)


def Operators_NullValueMatchPattern[T: Any](value: T | None) -> FSharpChoice_2[None, T]:
    if value is not None:
        return Choice2Of2(value_1(value))

    else:
        return Choice1Of2(None)


def Operators_NonNullQuickPattern[T](value: T = UNIT) -> T:
    if equals(value, cast(Any, None)):
        raise NullReferenceException__ctor()

    else:
        return value


def Operators_NonNullQuickValuePattern[T: Any](value: T | None) -> T:
    if value is not None:
        return value_1(value)

    else:
        raise NullReferenceException__ctor()


def Operators_WithNull[T](value: T = UNIT) -> T:
    return value


def Operators_WithNullV[T: Any](value: T = UNIT) -> T:
    return value


def Operators_NullV[T: Any](__unit: Unit = UNIT) -> T | None:
    return cast(Any | None, None)


def Operators_NullArgCheck[T](argument_name: str, value: T) -> T:
    if equals(value, cast(Any, None)):
        raise ArgumentNullException__ctor_Z721C83C5(argument_name)

    else:
        return value


def ExtraTopLevelOperators_LazyPattern[_A](input: Any) -> _A:
    return input.Value


def PrintfModule_PrintFormatToStringBuilderThen[_A, _B](
    continuation: Callable[[], _A], builder: Any, format: Any
) -> _B:
    def append(s: str, continuation: Any = continuation, builder: Any = builder) -> _A:
        ignore(StringBuilder__Append_Z721C83C5(builder, s))
        return continuation()

    return format.cont(append)


def PrintfModule_PrintFormatToStringBuilder[_A](builder: Any, format: Any) -> _A:
    def _arrow7(__unit: Unit = UNIT) -> None:
        ignore(None)

    return PrintfModule_PrintFormatToStringBuilderThen(_arrow7, builder, format)


__all__ = [
    "ExtraTopLevelOperators_LazyPattern",
    "LanguagePrimitives_FastGenericComparer",
    "LanguagePrimitives_FastGenericComparerFromTable",
    "LanguagePrimitives_FastGenericEqualityComparer",
    "LanguagePrimitives_FastGenericEqualityComparerFromTable",
    "LanguagePrimitives_GenericEqualityComparer",
    "LanguagePrimitives_GenericEqualityERComparer",
    "Operators_Failure",
    "Operators_FailurePattern",
    "Operators_IsNotNull",
    "Operators_IsNull",
    "Operators_IsNullV",
    "Operators_Lock",
    "Operators_NonNull",
    "Operators_NonNullQuickPattern",
    "Operators_NonNullQuickValuePattern",
    "Operators_NonNullV",
    "Operators_NullArg",
    "Operators_NullArgCheck",
    "Operators_NullMatchPattern",
    "Operators_NullV",
    "Operators_NullValueMatchPattern",
    "Operators_Using",
    "Operators_WithNull",
    "Operators_WithNullV",
    "PrintfModule_PrintFormatToStringBuilder",
    "PrintfModule_PrintFormatToStringBuilderThen",
]
