from __future__ import annotations

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


def _expr200() -> TypeInfo:
    return class_type("System.SystemException", None, SystemException, class_type("System.Exception"))


class SystemException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


SystemException_reflection = _expr200


def SystemException__ctor_Z721C83C5(message: str) -> SystemException:
    return SystemException(message)


def SystemException__ctor(__unit: None = None) -> SystemException:
    return SystemException__ctor_Z721C83C5(SR_Arg_SystemException)


def _expr201() -> TypeInfo:
    return class_type("System.ApplicationException", None, ApplicationException, class_type("System.Exception"))


class ApplicationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


ApplicationException_reflection = _expr201


def ApplicationException__ctor_Z721C83C5(message: str) -> ApplicationException:
    return ApplicationException(message)


def ApplicationException__ctor(__unit: None = None) -> ApplicationException:
    return ApplicationException__ctor_Z721C83C5(SR_Arg_ApplicationException)


def _expr202() -> TypeInfo:
    return class_type("System.ArithmeticException", None, ArithmeticException, class_type("System.Exception"))


class ArithmeticException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


ArithmeticException_reflection = _expr202


def ArithmeticException__ctor_Z721C83C5(message: str) -> ArithmeticException:
    return ArithmeticException(message)


def ArithmeticException__ctor(__unit: None = None) -> ArithmeticException:
    return ArithmeticException__ctor_Z721C83C5(SR_Arg_ArithmeticException)


def _expr203() -> TypeInfo:
    return class_type("System.DivideByZeroException", None, DivideByZeroException, class_type("System.Exception"))


class DivideByZeroException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


DivideByZeroException_reflection = _expr203


def DivideByZeroException__ctor_Z721C83C5(message: str) -> DivideByZeroException:
    return DivideByZeroException(message)


def DivideByZeroException__ctor(__unit: None = None) -> DivideByZeroException:
    return DivideByZeroException__ctor_Z721C83C5(SR_Arg_DivideByZero)


def _expr204() -> TypeInfo:
    return class_type("System.FormatException", None, FormatException, class_type("System.Exception"))


class FormatException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


FormatException_reflection = _expr204


def FormatException__ctor_Z721C83C5(message: str) -> FormatException:
    return FormatException(message)


def FormatException__ctor(__unit: None = None) -> FormatException:
    return FormatException__ctor_Z721C83C5(SR_Arg_FormatException)


def _expr205() -> TypeInfo:
    return class_type("System.IndexOutOfRangeException", None, IndexOutOfRangeException, class_type("System.Exception"))


class IndexOutOfRangeException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


IndexOutOfRangeException_reflection = _expr205


def IndexOutOfRangeException__ctor_Z721C83C5(message: str) -> IndexOutOfRangeException:
    return IndexOutOfRangeException(message)


def IndexOutOfRangeException__ctor(__unit: None = None) -> IndexOutOfRangeException:
    return IndexOutOfRangeException__ctor_Z721C83C5(SR_Arg_IndexOutOfRangeException)


def _expr207() -> TypeInfo:
    return class_type(
        "System.InvalidOperationException", None, InvalidOperationException, class_type("System.Exception")
    )


class InvalidOperationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


InvalidOperationException_reflection = _expr207


def InvalidOperationException__ctor_Z721C83C5(message: str) -> InvalidOperationException:
    return InvalidOperationException(message)


def InvalidOperationException__ctor(__unit: None = None) -> InvalidOperationException:
    return InvalidOperationException__ctor_Z721C83C5(SR_Arg_InvalidOperationException)


def _expr208() -> TypeInfo:
    return class_type("System.NotFiniteNumberException", None, NotFiniteNumberException, class_type("System.Exception"))


class NotFiniteNumberException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NotFiniteNumberException_reflection = _expr208


def NotFiniteNumberException__ctor_Z721C83C5(message: str) -> NotFiniteNumberException:
    return NotFiniteNumberException(message)


def NotFiniteNumberException__ctor(__unit: None = None) -> NotFiniteNumberException:
    return NotFiniteNumberException__ctor_Z721C83C5(SR_Arg_NotFiniteNumberException)


def _expr209() -> TypeInfo:
    return class_type("System.NotImplementedException", None, NotImplementedException, class_type("System.Exception"))


class NotImplementedException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NotImplementedException_reflection = _expr209


def NotImplementedException__ctor_Z721C83C5(message: str) -> NotImplementedException:
    return NotImplementedException(message)


def NotImplementedException__ctor(__unit: None = None) -> NotImplementedException:
    return NotImplementedException__ctor_Z721C83C5(SR_Arg_NotImplementedException)


def _expr210() -> TypeInfo:
    return class_type("System.NotSupportedException", None, NotSupportedException, class_type("System.Exception"))


class NotSupportedException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NotSupportedException_reflection = _expr210


def NotSupportedException__ctor_Z721C83C5(message: str) -> NotSupportedException:
    return NotSupportedException(message)


def NotSupportedException__ctor(__unit: None = None) -> NotSupportedException:
    return NotSupportedException__ctor_Z721C83C5(SR_Arg_NotSupportedException)


def _expr211() -> TypeInfo:
    return class_type("System.NullReferenceException", None, NullReferenceException, class_type("System.Exception"))


class NullReferenceException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


NullReferenceException_reflection = _expr211


def NullReferenceException__ctor_Z721C83C5(message: str) -> NullReferenceException:
    return NullReferenceException(message)


def NullReferenceException__ctor(__unit: None = None) -> NullReferenceException:
    return NullReferenceException__ctor_Z721C83C5(SR_Arg_NullReferenceException)


def _expr212() -> TypeInfo:
    return class_type("System.OutOfMemoryException", None, OutOfMemoryException, class_type("System.Exception"))


class OutOfMemoryException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


OutOfMemoryException_reflection = _expr212


def OutOfMemoryException__ctor_Z721C83C5(message: str) -> OutOfMemoryException:
    return OutOfMemoryException(message)


def OutOfMemoryException__ctor(__unit: None = None) -> OutOfMemoryException:
    return OutOfMemoryException__ctor_Z721C83C5(SR_Arg_OutOfMemoryException)


def _expr213() -> TypeInfo:
    return class_type("System.OverflowException", None, OverflowException, class_type("System.Exception"))


class OverflowException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


OverflowException_reflection = _expr213


def OverflowException__ctor_Z721C83C5(message: str) -> OverflowException:
    return OverflowException(message)


def OverflowException__ctor(__unit: None = None) -> OverflowException:
    return OverflowException__ctor_Z721C83C5(SR_Arg_OverflowException)


def _expr214() -> TypeInfo:
    return class_type("System.RankException", None, RankException, class_type("System.Exception"))


class RankException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


RankException_reflection = _expr214


def RankException__ctor_Z721C83C5(message: str) -> RankException:
    return RankException(message)


def RankException__ctor(__unit: None = None) -> RankException:
    return RankException__ctor_Z721C83C5(SR_Arg_RankException)


def _expr215() -> TypeInfo:
    return class_type("System.StackOverflowException", None, StackOverflowException, class_type("System.Exception"))


class StackOverflowException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


StackOverflowException_reflection = _expr215


def StackOverflowException__ctor_Z721C83C5(message: str) -> StackOverflowException:
    return StackOverflowException(message)


def StackOverflowException__ctor(__unit: None = None) -> StackOverflowException:
    return StackOverflowException__ctor_Z721C83C5(SR_Arg_StackOverflowException)


def _expr216() -> TypeInfo:
    return class_type("System.TimeoutException", None, TimeoutException, class_type("System.Exception"))


class TimeoutException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


TimeoutException_reflection = _expr216


def TimeoutException__ctor_Z721C83C5(message: str) -> TimeoutException:
    return TimeoutException(message)


def TimeoutException__ctor(__unit: None = None) -> TimeoutException:
    return TimeoutException__ctor_Z721C83C5(SR_Arg_TimeoutException)


def _expr217() -> TypeInfo:
    return class_type("System.ArgumentException", None, ArgumentException, class_type("System.Exception"))


class ArgumentException(Exception):
    def __init__(self, message: str, param_name: str) -> None:
        super().__init__(
            message if is_null_or_empty(param_name) else (((message + SR_Arg_ParamName_Name) + param_name) + "')")
        )
        self.param_name: str = param_name


ArgumentException_reflection = _expr217


def ArgumentException__ctor_Z384F8060(message: str, param_name: str) -> ArgumentException:
    return ArgumentException(message, param_name)


def ArgumentException__ctor(__unit: None = None) -> ArgumentException:
    return ArgumentException__ctor_Z384F8060(SR_Arg_ArgumentException, "")


def ArgumentException__ctor_Z721C83C5(message: str) -> ArgumentException:
    return ArgumentException__ctor_Z384F8060(message, "")


def ArgumentException__get_ParamName(_: ArgumentException) -> str:
    return _.param_name


def _expr218() -> TypeInfo:
    return class_type("System.ArgumentNullException", None, ArgumentNullException, ArgumentException_reflection())


class ArgumentNullException(ArgumentException):
    def __init__(self, param_name: str, message: str) -> None:
        super().__init__(message, param_name)
        pass


ArgumentNullException_reflection = _expr218


def ArgumentNullException__ctor_Z384F8060(param_name: str, message: str) -> ArgumentNullException:
    return ArgumentNullException(param_name, message)


def ArgumentNullException__ctor_Z721C83C5(param_name: str) -> ArgumentNullException:
    return ArgumentNullException__ctor_Z384F8060(param_name, SR_ArgumentNull_Generic)


def ArgumentNullException__ctor(__unit: None = None) -> ArgumentNullException:
    return ArgumentNullException__ctor_Z721C83C5("")


def _expr219() -> TypeInfo:
    return class_type(
        "System.ArgumentOutOfRangeException", None, ArgumentOutOfRangeException, ArgumentException_reflection()
    )


class ArgumentOutOfRangeException(ArgumentException):
    def __init__(self, param_name: str, message: str) -> None:
        super().__init__(message, param_name)
        pass


ArgumentOutOfRangeException_reflection = _expr219


def ArgumentOutOfRangeException__ctor_Z384F8060(param_name: str, message: str) -> ArgumentOutOfRangeException:
    return ArgumentOutOfRangeException(param_name, message)


def ArgumentOutOfRangeException__ctor_Z721C83C5(param_name: str) -> ArgumentOutOfRangeException:
    return ArgumentOutOfRangeException__ctor_Z384F8060(param_name, SR_Arg_ArgumentOutOfRangeException)


def ArgumentOutOfRangeException__ctor(__unit: None = None) -> ArgumentOutOfRangeException:
    return ArgumentOutOfRangeException__ctor_Z721C83C5("")


__all__ = [
    "SystemException_reflection",
    "SystemException__ctor",
    "ApplicationException_reflection",
    "ApplicationException__ctor",
    "ArithmeticException_reflection",
    "ArithmeticException__ctor",
    "DivideByZeroException_reflection",
    "DivideByZeroException__ctor",
    "FormatException_reflection",
    "FormatException__ctor",
    "IndexOutOfRangeException_reflection",
    "IndexOutOfRangeException__ctor",
    "InvalidOperationException_reflection",
    "InvalidOperationException__ctor",
    "NotFiniteNumberException_reflection",
    "NotFiniteNumberException__ctor",
    "NotImplementedException_reflection",
    "NotImplementedException__ctor",
    "NotSupportedException_reflection",
    "NotSupportedException__ctor",
    "NullReferenceException_reflection",
    "NullReferenceException__ctor",
    "OutOfMemoryException_reflection",
    "OutOfMemoryException__ctor",
    "OverflowException_reflection",
    "OverflowException__ctor",
    "RankException_reflection",
    "RankException__ctor",
    "StackOverflowException_reflection",
    "StackOverflowException__ctor",
    "TimeoutException_reflection",
    "TimeoutException__ctor",
    "ArgumentException_reflection",
    "ArgumentException__ctor",
    "ArgumentException__ctor_Z721C83C5",
    "ArgumentException__get_ParamName",
    "ArgumentNullException_reflection",
    "ArgumentNullException__ctor_Z721C83C5",
    "ArgumentNullException__ctor",
    "ArgumentOutOfRangeException_reflection",
    "ArgumentOutOfRangeException__ctor_Z721C83C5",
    "ArgumentOutOfRangeException__ctor",
]
