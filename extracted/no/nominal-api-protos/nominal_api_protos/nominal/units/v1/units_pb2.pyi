from google.api import annotations_pb2 as _annotations_pb2
from nominal.conjure.v1 import compat_pb2 as _compat_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScoutError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCOUT_ERROR_CANNOT_DESERIALIZE_SEARCH_TOKEN: _ClassVar[ScoutError]
    SCOUT_ERROR_INVALID_RANGE: _ClassVar[ScoutError]
    SCOUT_ERROR_REQUESTED_PAGE_SIZE_TOO_LARGE: _ClassVar[ScoutError]
SCOUT_ERROR_CANNOT_DESERIALIZE_SEARCH_TOKEN: ScoutError
SCOUT_ERROR_INVALID_RANGE: ScoutError
SCOUT_ERROR_REQUESTED_PAGE_SIZE_TOO_LARGE: ScoutError

class GetAllUnitsResponse(_message.Message):
    __slots__ = ("units_by_property",)
    class UnitsByPropertyEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GetAllUnitsResponse.GetUnitsResponseUnitsByPropertyWrapper
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetAllUnitsResponse.GetUnitsResponseUnitsByPropertyWrapper, _Mapping]] = ...) -> None: ...
    class GetUnitsResponseUnitsByPropertyWrapper(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: _containers.RepeatedCompositeFieldContainer[Unit]
        def __init__(self, value: _Optional[_Iterable[_Union[Unit, _Mapping]]] = ...) -> None: ...
    UNITS_BY_PROPERTY_FIELD_NUMBER: _ClassVar[int]
    units_by_property: _containers.MessageMap[str, GetAllUnitsResponse.GetUnitsResponseUnitsByPropertyWrapper]
    def __init__(self, units_by_property: _Optional[_Mapping[str, GetAllUnitsResponse.GetUnitsResponseUnitsByPropertyWrapper]] = ...) -> None: ...

class Unit(_message.Message):
    __slots__ = ("name", "symbol", "property", "dimension", "system")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    property: str
    dimension: UnitDimension
    system: str
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., property: _Optional[str] = ..., dimension: _Optional[_Union[UnitDimension, _Mapping]] = ..., system: _Optional[str] = ...) -> None: ...

class UnitDimension(_message.Message):
    __slots__ = ("base_dimensions",)
    class BaseDimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    BASE_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    base_dimensions: _containers.ScalarMap[str, int]
    def __init__(self, base_dimensions: _Optional[_Mapping[str, int]] = ...) -> None: ...

class GetAllUnitsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUnitRequest(_message.Message):
    __slots__ = ("unit",)
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: str
    def __init__(self, unit: _Optional[str] = ...) -> None: ...

class GetUnitResponse(_message.Message):
    __slots__ = ("unit",)
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: Unit
    def __init__(self, unit: _Optional[_Union[Unit, _Mapping]] = ...) -> None: ...

class GetBatchUnitsRequest(_message.Message):
    __slots__ = ("units",)
    UNITS_FIELD_NUMBER: _ClassVar[int]
    units: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, units: _Optional[_Iterable[str]] = ...) -> None: ...

class GetBatchUnitsResponse(_message.Message):
    __slots__ = ("responses",)
    class ResponsesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Unit
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Unit, _Mapping]] = ...) -> None: ...
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.MessageMap[str, Unit]
    def __init__(self, responses: _Optional[_Mapping[str, Unit]] = ...) -> None: ...

class GetCommensurableUnitsRequest(_message.Message):
    __slots__ = ("unit",)
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: str
    def __init__(self, unit: _Optional[str] = ...) -> None: ...

class GetCommensurableUnitsResponse(_message.Message):
    __slots__ = ("units",)
    UNITS_FIELD_NUMBER: _ClassVar[int]
    units: _containers.RepeatedCompositeFieldContainer[Unit]
    def __init__(self, units: _Optional[_Iterable[_Union[Unit, _Mapping]]] = ...) -> None: ...
