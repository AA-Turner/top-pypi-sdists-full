from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Affinity(_message.Message):
    __slots__ = ["selectors"]
    SELECTORS_FIELD_NUMBER: _ClassVar[int]
    selectors: _containers.RepeatedCompositeFieldContainer[Selector]
    def __init__(self, selectors: _Optional[_Iterable[_Union[Selector, _Mapping]]] = ...) -> None: ...

class ClusterAssignment(_message.Message):
    __slots__ = ["affinity", "toleration"]
    AFFINITY_FIELD_NUMBER: _ClassVar[int]
    TOLERATION_FIELD_NUMBER: _ClassVar[int]
    affinity: Affinity
    toleration: Toleration
    def __init__(self, affinity: _Optional[_Union[Affinity, _Mapping]] = ..., toleration: _Optional[_Union[Toleration, _Mapping]] = ...) -> None: ...

class Selector(_message.Message):
    __slots__ = ["key", "operator", "value"]
    class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    EQUALS: Selector.Operator
    EXISTS: Selector.Operator
    IN: Selector.Operator
    KEY_FIELD_NUMBER: _ClassVar[int]
    NOT_EQUALS: Selector.Operator
    NOT_IN: Selector.Operator
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    operator: Selector.Operator
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Iterable[str]] = ..., operator: _Optional[_Union[Selector.Operator, str]] = ...) -> None: ...

class Toleration(_message.Message):
    __slots__ = ["selectors"]
    SELECTORS_FIELD_NUMBER: _ClassVar[int]
    selectors: _containers.RepeatedCompositeFieldContainer[Selector]
    def __init__(self, selectors: _Optional[_Iterable[_Union[Selector, _Mapping]]] = ...) -> None: ...
