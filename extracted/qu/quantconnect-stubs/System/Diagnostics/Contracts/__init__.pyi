from typing import overload
from enum import IntEnum
import typing
import warnings

import System
import System.Collections.Generic
import System.Diagnostics.Contracts
import System.Runtime.Serialization

System_Diagnostics_Contracts__EventContainer_Callable = typing.TypeVar("System_Diagnostics_Contracts__EventContainer_Callable")
System_Diagnostics_Contracts__EventContainer_ReturnType = typing.TypeVar("System_Diagnostics_Contracts__EventContainer_ReturnType")
System_Diagnostics_Contracts_Contract_Requires_TException = typing.TypeVar("System_Diagnostics_Contracts_Contract_Requires_TException")
System_Diagnostics_Contracts_Contract_EnsuresOnThrow_TException = typing.TypeVar("System_Diagnostics_Contracts_Contract_EnsuresOnThrow_TException")
System_Diagnostics_Contracts_Contract_Result_T = typing.TypeVar("System_Diagnostics_Contracts_Contract_Result_T")
System_Diagnostics_Contracts_Contract_ValueAtReturn_T = typing.TypeVar("System_Diagnostics_Contracts_Contract_ValueAtReturn_T")
System_Diagnostics_Contracts_Contract_OldValue_T = typing.TypeVar("System_Diagnostics_Contracts_Contract_OldValue_T")
System_Diagnostics_Contracts_Contract_ForAll_T = typing.TypeVar("System_Diagnostics_Contracts_Contract_ForAll_T")
System_Diagnostics_Contracts_Contract_Exists_T = typing.TypeVar("System_Diagnostics_Contracts_Contract_Exists_T")


class PureAttribute(System.Attribute):
    """This class has no documentation."""


class ContractClassAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def type_containing_contracts(self) -> typing.Type:
        ...

    def __init__(self, type_containing_contracts: typing.Type) -> None:
        ...


class ContractClassForAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def type_contracts_are_for(self) -> typing.Type:
        ...

    def __init__(self, type_contracts_are_for: typing.Type) -> None:
        ...


class ContractInvariantMethodAttribute(System.Attribute):
    """This class has no documentation."""


class ContractReferenceAssemblyAttribute(System.Attribute):
    """This class has no documentation."""


class ContractRuntimeIgnoredAttribute(System.Attribute):
    """This class has no documentation."""


class ContractVerificationAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> bool:
        ...

    def __init__(self, value: bool) -> None:
        ...


class ContractPublicPropertyNameAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def name(self) -> str:
        ...

    def __init__(self, name: str) -> None:
        ...


class ContractArgumentValidatorAttribute(System.Attribute):
    """This class has no documentation."""


class ContractAbbreviatorAttribute(System.Attribute):
    """This class has no documentation."""


class ContractOptionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def category(self) -> str:
        ...

    @property
    def setting(self) -> str:
        ...

    @property
    def enabled(self) -> bool:
        ...

    @property
    def value(self) -> str:
        ...

    @overload
    def __init__(self, category: str, setting: str, enabled: bool) -> None:
        ...

    @overload
    def __init__(self, category: str, setting: str, value: str) -> None:
        ...


class _Typed_Contract_Requires(typing.Generic[System_Diagnostics_Contracts_Contract_Requires_TException]):
    """"""

    @overload
    def __call__(self, condition: bool) -> None:
        ...

    @overload
    def __call__(self, condition: bool, user_message: str) -> None:
        ...


class _Contract_Requires:
    """"""

    @overload
    def __call__(self, condition: bool) -> None:
        ...

    @overload
    def __call__(self, condition: bool, user_message: str) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_Requires_TException]) -> System.Diagnostics.Contracts._Typed_Contract_Requires[System_Diagnostics_Contracts_Contract_Requires_TException]:
        ...


class _Typed_Contract_EnsuresOnThrow(typing.Generic[System_Diagnostics_Contracts_Contract_EnsuresOnThrow_TException]):
    """"""

    @overload
    def __call__(self, condition: bool) -> None:
        ...

    @overload
    def __call__(self, condition: bool, user_message: str) -> None:
        ...


class _Contract_EnsuresOnThrow:
    """"""

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_EnsuresOnThrow_TException]) -> System.Diagnostics.Contracts._Typed_Contract_EnsuresOnThrow[System_Diagnostics_Contracts_Contract_EnsuresOnThrow_TException]:
        ...


class _Typed_Contract_Result(typing.Generic[System_Diagnostics_Contracts_Contract_Result_T]):
    """"""

    @overload
    def __call__(self) -> System_Diagnostics_Contracts_Contract_Result_T:
        ...


class _Contract_Result:
    """"""

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_Result_T]) -> System.Diagnostics.Contracts._Typed_Contract_Result[System_Diagnostics_Contracts_Contract_Result_T]:
        ...


class _Typed_Contract_ValueAtReturn(typing.Generic[System_Diagnostics_Contracts_Contract_ValueAtReturn_T]):
    """"""

    @overload
    def __call__(self, value: typing.Optional[System_Diagnostics_Contracts_Contract_ValueAtReturn_T]) -> typing.Tuple[System_Diagnostics_Contracts_Contract_ValueAtReturn_T, System_Diagnostics_Contracts_Contract_ValueAtReturn_T]:
        ...


class _Contract_ValueAtReturn:
    """"""

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_ValueAtReturn_T]) -> System.Diagnostics.Contracts._Typed_Contract_ValueAtReturn[System_Diagnostics_Contracts_Contract_ValueAtReturn_T]:
        ...


class _Typed_Contract_OldValue(typing.Generic[System_Diagnostics_Contracts_Contract_OldValue_T]):
    """"""

    @overload
    def __call__(self, value: System_Diagnostics_Contracts_Contract_OldValue_T) -> System_Diagnostics_Contracts_Contract_OldValue_T:
        ...


class _Contract_OldValue:
    """"""

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_OldValue_T]) -> System.Diagnostics.Contracts._Typed_Contract_OldValue[System_Diagnostics_Contracts_Contract_OldValue_T]:
        ...


class _Typed_Contract_ForAll(typing.Generic[System_Diagnostics_Contracts_Contract_ForAll_T]):
    """"""

    @overload
    def __call__(self, collection: System.Collections.Generic.IEnumerable[System_Diagnostics_Contracts_Contract_ForAll_T], predicate: typing.Callable[[System_Diagnostics_Contracts_Contract_ForAll_T], bool]) -> bool:
        ...


class _Contract_ForAll:
    """"""

    @overload
    def __call__(self, from_inclusive: int, to_exclusive: int, predicate: typing.Callable[[int], bool]) -> bool:
        ...

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_ForAll_T]) -> System.Diagnostics.Contracts._Typed_Contract_ForAll[System_Diagnostics_Contracts_Contract_ForAll_T]:
        ...


class _Typed_Contract_Exists(typing.Generic[System_Diagnostics_Contracts_Contract_Exists_T]):
    """"""

    @overload
    def __call__(self, collection: System.Collections.Generic.IEnumerable[System_Diagnostics_Contracts_Contract_Exists_T], predicate: typing.Callable[[System_Diagnostics_Contracts_Contract_Exists_T], bool]) -> bool:
        ...


class _Contract_Exists:
    """"""

    @overload
    def __call__(self, from_inclusive: int, to_exclusive: int, predicate: typing.Callable[[int], bool]) -> bool:
        ...

    def __getitem__(self, type: typing.Type[System_Diagnostics_Contracts_Contract_Exists_T]) -> System.Diagnostics.Contracts._Typed_Contract_Exists[System_Diagnostics_Contracts_Contract_Exists_T]:
        ...


class ContractFailureKind(IntEnum):
    """This class has no documentation."""

    PRECONDITION = 0

    POSTCONDITION = 1

    POSTCONDITION_ON_EXCEPTION = 2

    INVARIANT = 3

    ASSERT = 4

    ASSUME = 5


class ContractFailedEventArgs(System.EventArgs):
    """This class has no documentation."""

    @property
    def message(self) -> str:
        ...

    @property
    def condition(self) -> str:
        ...

    @property
    def failure_kind(self) -> System.Diagnostics.Contracts.ContractFailureKind:
        ...

    @property
    def original_exception(self) -> System.Exception:
        ...

    @property
    def handled(self) -> bool:
        ...

    @property
    def unwind(self) -> bool:
        ...

    def __init__(self, failure_kind: System.Diagnostics.Contracts.ContractFailureKind, message: str, condition: str, original_exception: System.Exception) -> None:
        ...

    def set_handled(self) -> None:
        ...

    def set_unwind(self) -> None:
        ...


class Contract(System.Object):
    """This class has no documentation."""

    contract_failed: _EventContainer[typing.Callable[[System.Object, System.Diagnostics.Contracts.ContractFailedEventArgs], typing.Any], typing.Any]

    requires: System.Diagnostics.Contracts._Contract_Requires

    ensures_on_throw: System.Diagnostics.Contracts._Contract_EnsuresOnThrow

    result: System.Diagnostics.Contracts._Contract_Result

    value_at_return: System.Diagnostics.Contracts._Contract_ValueAtReturn

    old_value: System.Diagnostics.Contracts._Contract_OldValue

    for_all: System.Diagnostics.Contracts._Contract_ForAll

    exists: System.Diagnostics.Contracts._Contract_Exists

    @staticmethod
    @overload
    def Assert(condition: bool) -> None:
        ...

    @staticmethod
    @overload
    def Assert(condition: bool, userMessage: str) -> None:
        ...

    @staticmethod
    @overload
    def assume(condition: bool) -> None:
        ...

    @staticmethod
    @overload
    def assume(condition: bool, user_message: str) -> None:
        ...

    @staticmethod
    def end_contract_block() -> None:
        ...

    @staticmethod
    @overload
    def ensures(condition: bool) -> None:
        ...

    @staticmethod
    @overload
    def ensures(condition: bool, user_message: str) -> None:
        ...

    @staticmethod
    @overload
    def invariant(condition: bool) -> None:
        ...

    @staticmethod
    @overload
    def invariant(condition: bool, user_message: str) -> None:
        ...


class ContractException(System.Exception):
    """This class has no documentation."""

    @property
    def kind(self) -> System.Diagnostics.Contracts.ContractFailureKind:
        ...

    @property
    def failure(self) -> str:
        ...

    @property
    def user_message(self) -> str:
        ...

    @property
    def condition(self) -> str:
        ...

    def __init__(self, kind: System.Diagnostics.Contracts.ContractFailureKind, failure: str, user_message: str, condition: str, inner_exception: System.Exception) -> None:
        ...

    def get_object_data(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class _EventContainer(typing.Generic[System_Diagnostics_Contracts__EventContainer_Callable, System_Diagnostics_Contracts__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Diagnostics_Contracts__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Diagnostics_Contracts__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Diagnostics_Contracts__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


