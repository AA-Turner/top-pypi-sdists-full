from abc import abstractmethod
from typing import Any, Protocol

from .types import int32


class IGenericAdder_1[T](Protocol):
    @abstractmethod
    def Add(self, __arg0: T, __arg1: T) -> T: ...

    @abstractmethod
    def GetZero(self) -> T: ...


class IGenericAverager_1[T](Protocol):
    @abstractmethod
    def Add(self, __arg0: T, __arg1: T) -> T: ...

    @abstractmethod
    def DivideByInt(self, __arg0: T, __arg1: int32) -> T: ...

    @abstractmethod
    def GetZero(self) -> T: ...


class Symbol_wellknown(Protocol):
    @property
    @abstractmethod
    def Symbol_toStringTag(self) -> str: ...


class IJsonSerializable(Protocol):
    @abstractmethod
    def to_json(self) -> Any: ...


SR_indexOutOfBounds: str = "The index was outside the range of elements in the collection."

SR_inputWasEmpty: str = "Collection was empty."

SR_inputMustBeNonNegative: str = "The input must be non-negative."

SR_inputSequenceEmpty: str = "The input sequence was empty."

SR_inputSequenceTooLong: str = "The input sequence contains more than one element."

SR_keyNotFoundAlt: str = "An index satisfying the predicate was not found in the collection."

SR_differentLengths: str = "The collections had different lengths."

SR_notEnoughElements: str = "The input sequence has an insufficient number of elements."

SR_Arg_ApplicationException: str = "Error in the application."

SR_Arg_ArgumentException: str = "Value does not fall within the expected range."

SR_Arg_ArgumentOutOfRangeException: str = "Specified argument was out of the range of valid values."

SR_ArgumentNull_Generic: str = "Value cannot be null."

SR_Arg_ParamName_Name: str = " (Parameter '"

SR_Arg_ArithmeticException: str = "Overflow or underflow in the arithmetic operation."

SR_Arg_DivideByZero: str = "Attempted to divide by zero."

SR_Arg_FormatException: str = "One of the identified items was in an invalid format."

SR_Arg_IndexOutOfRangeException: str = "Index was outside the bounds of the array."

SR_Arg_InvalidOperationException: str = "Operation is not valid due to the current state of the object."

SR_Arg_KeyNotFound: str = "The given key was not present in the dictionary."

SR_Arg_NotFiniteNumberException: str = "Number encountered was not a finite quantity."

SR_Arg_NotImplementedException: str = "The method or operation is not implemented."

SR_Arg_NotSupportedException: str = "Specified method is not supported."

SR_Arg_NullReferenceException: str = "Object reference not set to an instance of an object."

SR_Arg_OutOfMemoryException: str = "Insufficient memory to continue the execution of the program."

SR_Arg_OverflowException: str = "Arithmetic operation resulted in an overflow."

SR_Arg_RankException: str = "Attempted to operate on an array with the incorrect number of dimensions."

SR_Arg_StackOverflowException: str = "Operation caused a stack overflow."

SR_Arg_SystemException: str = "System error."

SR_Arg_TimeoutException: str = "The operation has timed out."

__all__ = [
    "SR_indexOutOfBounds",
    "SR_inputWasEmpty",
    "SR_inputMustBeNonNegative",
    "SR_inputSequenceEmpty",
    "SR_inputSequenceTooLong",
    "SR_keyNotFoundAlt",
    "SR_differentLengths",
    "SR_notEnoughElements",
    "SR_Arg_ApplicationException",
    "SR_Arg_ArgumentException",
    "SR_Arg_ArgumentOutOfRangeException",
    "SR_ArgumentNull_Generic",
    "SR_Arg_ParamName_Name",
    "SR_Arg_ArithmeticException",
    "SR_Arg_DivideByZero",
    "SR_Arg_FormatException",
    "SR_Arg_IndexOutOfRangeException",
    "SR_Arg_InvalidOperationException",
    "SR_Arg_KeyNotFound",
    "SR_Arg_NotFiniteNumberException",
    "SR_Arg_NotImplementedException",
    "SR_Arg_NotSupportedException",
    "SR_Arg_NullReferenceException",
    "SR_Arg_OutOfMemoryException",
    "SR_Arg_OverflowException",
    "SR_Arg_RankException",
    "SR_Arg_StackOverflowException",
    "SR_Arg_SystemException",
    "SR_Arg_TimeoutException",
]
