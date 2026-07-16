from __future__ import annotations

from typing import cast

from .global_ import (
    SR_Arg_ApplicationException,
    SR_Arg_ArgumentException,
    SR_Arg_ArgumentOutOfRangeException,
    SR_Arg_ArithmeticException,
    SR_Arg_DivideByZero,
    SR_Arg_FormatException,
    SR_Arg_IndexOutOfRangeException,
    SR_Arg_InvalidOperationException,
    SR_Arg_NotFiniteNumberException,
    SR_Arg_NotImplementedException,
    SR_Arg_NotSupportedException,
    SR_Arg_NullReferenceException,
    SR_Arg_OutOfMemoryException,
    SR_Arg_OverflowException,
    SR_Arg_ParamName_Name,
    SR_Arg_RankException,
    SR_Arg_StackOverflowException,
    SR_Arg_SystemException,
    SR_Arg_TimeoutException,
    SR_ArgumentNull_Generic,
)
from .reflection import TypeInfo, class_type
from .string_ import is_null_or_empty
from .types import ExceptionBase
from .util import UNIT, Unit


def _expr182() -> TypeInfo:
    return class_type("System.SystemException", None, SystemException, class_type("System.Exception"))


class SystemException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


SystemException_reflection = _expr182


def SystemException__ctor_Z721C83C5(message: str) -> SystemException:
    return SystemException(message)


def SystemException__ctor(__unit: Unit = UNIT) -> SystemException:
    return SystemException__ctor_Z721C83C5(SR_Arg_SystemException)


def _expr183() -> TypeInfo:
    return class_type("System.ApplicationException", None, ApplicationException, class_type("System.Exception"))


class ApplicationException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


ApplicationException_reflection = _expr183


def ApplicationException__ctor_Z721C83C5(message: str) -> ApplicationException:
    return ApplicationException(message)


def ApplicationException__ctor(__unit: Unit = UNIT) -> ApplicationException:
    return ApplicationException__ctor_Z721C83C5(SR_Arg_ApplicationException)


def _expr184() -> TypeInfo:
    return class_type("System.ArithmeticException", None, ArithmeticException, class_type("System.Exception"))


class ArithmeticException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


ArithmeticException_reflection = _expr184


def ArithmeticException__ctor_Z721C83C5(message: str) -> ArithmeticException:
    return ArithmeticException(message)


def ArithmeticException__ctor(__unit: Unit = UNIT) -> ArithmeticException:
    return ArithmeticException__ctor_Z721C83C5(SR_Arg_ArithmeticException)


def _expr185() -> TypeInfo:
    return class_type("System.DivideByZeroException", None, DivideByZeroException, class_type("System.Exception"))


class DivideByZeroException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


DivideByZeroException_reflection = _expr185


def DivideByZeroException__ctor_Z721C83C5(message: str) -> DivideByZeroException:
    return DivideByZeroException(message)


def DivideByZeroException__ctor(__unit: Unit = UNIT) -> DivideByZeroException:
    return DivideByZeroException__ctor_Z721C83C5(SR_Arg_DivideByZero)


def _expr186() -> TypeInfo:
    return class_type("System.FormatException", None, FormatException, class_type("System.Exception"))


class FormatException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


FormatException_reflection = _expr186


def FormatException__ctor_Z721C83C5(message: str) -> FormatException:
    return FormatException(message)


def FormatException__ctor(__unit: Unit = UNIT) -> FormatException:
    return FormatException__ctor_Z721C83C5(SR_Arg_FormatException)


def _expr187() -> TypeInfo:
    return class_type("System.IndexOutOfRangeException", None, IndexOutOfRangeException, class_type("System.Exception"))


class IndexOutOfRangeException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


IndexOutOfRangeException_reflection = _expr187


def IndexOutOfRangeException__ctor_Z721C83C5(message: str) -> IndexOutOfRangeException:
    return IndexOutOfRangeException(message)


def IndexOutOfRangeException__ctor(__unit: Unit = UNIT) -> IndexOutOfRangeException:
    return IndexOutOfRangeException__ctor_Z721C83C5(SR_Arg_IndexOutOfRangeException)


def _expr188() -> TypeInfo:
    return class_type(
        "System.InvalidOperationException", None, InvalidOperationException, class_type("System.Exception")
    )


class InvalidOperationException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


InvalidOperationException_reflection = _expr188


def InvalidOperationException__ctor_Z721C83C5(message: str) -> InvalidOperationException:
    return InvalidOperationException(message)


def InvalidOperationException__ctor(__unit: Unit = UNIT) -> InvalidOperationException:
    return InvalidOperationException__ctor_Z721C83C5(SR_Arg_InvalidOperationException)


def _expr189() -> TypeInfo:
    return class_type("System.NotFiniteNumberException", None, NotFiniteNumberException, class_type("System.Exception"))


class NotFiniteNumberException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NotFiniteNumberException_reflection = _expr189


def NotFiniteNumberException__ctor_Z721C83C5(message: str) -> NotFiniteNumberException:
    return NotFiniteNumberException(message)


def NotFiniteNumberException__ctor(__unit: Unit = UNIT) -> NotFiniteNumberException:
    return NotFiniteNumberException__ctor_Z721C83C5(SR_Arg_NotFiniteNumberException)


def _expr190() -> TypeInfo:
    return class_type("System.NotImplementedException", None, NotImplementedException, class_type("System.Exception"))


class NotImplementedException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NotImplementedException_reflection = _expr190


def NotImplementedException__ctor_Z721C83C5(message: str) -> NotImplementedException:
    return NotImplementedException(message)


def NotImplementedException__ctor(__unit: Unit = UNIT) -> NotImplementedException:
    return NotImplementedException__ctor_Z721C83C5(SR_Arg_NotImplementedException)


def _expr191() -> TypeInfo:
    return class_type("System.NotSupportedException", None, NotSupportedException, class_type("System.Exception"))


class NotSupportedException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NotSupportedException_reflection = _expr191


def NotSupportedException__ctor_Z721C83C5(message: str) -> NotSupportedException:
    return NotSupportedException(message)


def NotSupportedException__ctor(__unit: Unit = UNIT) -> NotSupportedException:
    return NotSupportedException__ctor_Z721C83C5(SR_Arg_NotSupportedException)


def _expr192() -> TypeInfo:
    return class_type("System.NullReferenceException", None, NullReferenceException, class_type("System.Exception"))


class NullReferenceException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NullReferenceException_reflection = _expr192


def NullReferenceException__ctor_Z721C83C5(message: str) -> NullReferenceException:
    return NullReferenceException(message)


def NullReferenceException__ctor(__unit: Unit = UNIT) -> NullReferenceException:
    return NullReferenceException__ctor_Z721C83C5(SR_Arg_NullReferenceException)


def _expr193() -> TypeInfo:
    return class_type("System.OutOfMemoryException", None, OutOfMemoryException, class_type("System.Exception"))


class OutOfMemoryException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


OutOfMemoryException_reflection = _expr193


def OutOfMemoryException__ctor_Z721C83C5(message: str) -> OutOfMemoryException:
    return OutOfMemoryException(message)


def OutOfMemoryException__ctor(__unit: Unit = UNIT) -> OutOfMemoryException:
    return OutOfMemoryException__ctor_Z721C83C5(SR_Arg_OutOfMemoryException)


def _expr194() -> TypeInfo:
    return class_type("System.OverflowException", None, OverflowException, class_type("System.Exception"))


class OverflowException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


OverflowException_reflection = _expr194


def OverflowException__ctor_Z721C83C5(message: str) -> OverflowException:
    return OverflowException(message)


def OverflowException__ctor(__unit: Unit = UNIT) -> OverflowException:
    return OverflowException__ctor_Z721C83C5(SR_Arg_OverflowException)


def _expr195() -> TypeInfo:
    return class_type("System.RankException", None, RankException, class_type("System.Exception"))


class RankException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


RankException_reflection = _expr195


def RankException__ctor_Z721C83C5(message: str) -> RankException:
    return RankException(message)


def RankException__ctor(__unit: Unit = UNIT) -> RankException:
    return RankException__ctor_Z721C83C5(SR_Arg_RankException)


def _expr196() -> TypeInfo:
    return class_type("System.StackOverflowException", None, StackOverflowException, class_type("System.Exception"))


class StackOverflowException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


StackOverflowException_reflection = _expr196


def StackOverflowException__ctor_Z721C83C5(message: str) -> StackOverflowException:
    return StackOverflowException(message)


def StackOverflowException__ctor(__unit: Unit = UNIT) -> StackOverflowException:
    return StackOverflowException__ctor_Z721C83C5(SR_Arg_StackOverflowException)


def _expr197() -> TypeInfo:
    return class_type("System.TimeoutException", None, TimeoutException, class_type("System.Exception"))


class TimeoutException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


TimeoutException_reflection = _expr197


def TimeoutException__ctor_Z721C83C5(message: str) -> TimeoutException:
    return TimeoutException(message)


def TimeoutException__ctor(__unit: Unit = UNIT) -> TimeoutException:
    return TimeoutException__ctor_Z721C83C5(SR_Arg_TimeoutException)


def _expr198() -> TypeInfo:
    return class_type("System.ArgumentException", None, ArgumentException, class_type("System.Exception"))


class ArgumentException(ExceptionBase):
    def __init__(self, message: str, param_name: str, inner_exception: Exception) -> None:
        super().__init__(
            message if is_null_or_empty(param_name) else (((message + SR_Arg_ParamName_Name) + param_name) + "')"),
            inner_exception,
        )
        self.param_name: str = param_name


ArgumentException_reflection = _expr198


def ArgumentException__ctor_Z60A2B367(message: str, param_name: str, inner_exception: Exception) -> ArgumentException:
    return ArgumentException(message, param_name, inner_exception)


def ArgumentException__ctor(__unit: Unit = UNIT) -> ArgumentException:
    return ArgumentException__ctor_Z60A2B367(SR_Arg_ArgumentException, "", cast(Exception, None))


def ArgumentException__ctor_Z721C83C5(message: str) -> ArgumentException:
    return ArgumentException__ctor_Z60A2B367(message, "", cast(Exception, None))


def ArgumentException__ctor_Z384F8060(message: str, param_name: str) -> ArgumentException:
    return ArgumentException__ctor_Z60A2B367(message, param_name, cast(Exception, None))


def ArgumentException__ctor_68CE3CA2(message: str, inner_exception: Exception) -> ArgumentException:
    return ArgumentException__ctor_Z60A2B367(message, "", inner_exception)


def ArgumentException__get_ParamName(_: ArgumentException) -> str:
    return _.param_name


def _expr200() -> TypeInfo:
    return class_type("System.ArgumentNullException", None, ArgumentNullException, ArgumentException_reflection())


class ArgumentNullException(ArgumentException):
    def __init__(self, param_name: str, message: str) -> None:
        super().__init__(message, param_name, cast(Exception, None))
        pass


ArgumentNullException_reflection = _expr200


def ArgumentNullException__ctor_Z384F8060(param_name: str, message: str) -> ArgumentNullException:
    return ArgumentNullException(param_name, message)


def ArgumentNullException__ctor_Z721C83C5(param_name: str) -> ArgumentNullException:
    return ArgumentNullException__ctor_Z384F8060(param_name, SR_ArgumentNull_Generic)


def ArgumentNullException__ctor(__unit: Unit = UNIT) -> ArgumentNullException:
    return ArgumentNullException__ctor_Z721C83C5("")


def _expr201() -> TypeInfo:
    return class_type(
        "System.ArgumentOutOfRangeException", None, ArgumentOutOfRangeException, ArgumentException_reflection()
    )


class ArgumentOutOfRangeException(ArgumentException):
    def __init__(self, param_name: str, message: str) -> None:
        super().__init__(message, param_name, cast(Exception, None))
        pass


ArgumentOutOfRangeException_reflection = _expr201


def ArgumentOutOfRangeException__ctor_Z384F8060(param_name: str, message: str) -> ArgumentOutOfRangeException:
    return ArgumentOutOfRangeException(param_name, message)


def ArgumentOutOfRangeException__ctor_Z721C83C5(param_name: str) -> ArgumentOutOfRangeException:
    return ArgumentOutOfRangeException__ctor_Z384F8060(param_name, SR_Arg_ArgumentOutOfRangeException)


def ArgumentOutOfRangeException__ctor(__unit: Unit = UNIT) -> ArgumentOutOfRangeException:
    return ArgumentOutOfRangeException__ctor_Z721C83C5("")


__all__ = [
    "ApplicationException__ctor",
    "ApplicationException_reflection",
    "ArgumentException__ctor",
    "ArgumentException__ctor_68CE3CA2",
    "ArgumentException__ctor_Z384F8060",
    "ArgumentException__ctor_Z721C83C5",
    "ArgumentException__get_ParamName",
    "ArgumentException_reflection",
    "ArgumentNullException__ctor",
    "ArgumentNullException__ctor_Z721C83C5",
    "ArgumentNullException_reflection",
    "ArgumentOutOfRangeException__ctor",
    "ArgumentOutOfRangeException__ctor_Z721C83C5",
    "ArgumentOutOfRangeException_reflection",
    "ArithmeticException__ctor",
    "ArithmeticException_reflection",
    "DivideByZeroException__ctor",
    "DivideByZeroException_reflection",
    "FormatException__ctor",
    "FormatException_reflection",
    "IndexOutOfRangeException__ctor",
    "IndexOutOfRangeException_reflection",
    "InvalidOperationException__ctor",
    "InvalidOperationException_reflection",
    "NotFiniteNumberException__ctor",
    "NotFiniteNumberException_reflection",
    "NotImplementedException__ctor",
    "NotImplementedException_reflection",
    "NotSupportedException__ctor",
    "NotSupportedException_reflection",
    "NullReferenceException__ctor",
    "NullReferenceException_reflection",
    "OutOfMemoryException__ctor",
    "OutOfMemoryException_reflection",
    "OverflowException__ctor",
    "OverflowException_reflection",
    "RankException__ctor",
    "RankException_reflection",
    "StackOverflowException__ctor",
    "StackOverflowException_reflection",
    "SystemException__ctor",
    "SystemException_reflection",
    "TimeoutException__ctor",
    "TimeoutException_reflection",
]
