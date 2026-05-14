from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class TySet(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: Ty
    def __init__(self, items: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

class TyList(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: Ty
    def __init__(self, items: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

class TyIterable(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: Ty
    def __init__(self, items: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

class TyGenerator(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: Ty
    def __init__(self, items: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

class TyDatetime(_message.Message):
    __slots__ = ("tz",)
    TZ_FIELD_NUMBER: _ClassVar[int]
    tz: str
    def __init__(self, tz: _Optional[str] = ...) -> None: ...

class TyDict(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: Ty
    value: Ty
    def __init__(
        self, key: _Optional[_Union[Ty, _Mapping]] = ..., value: _Optional[_Union[Ty, _Mapping]] = ...
    ) -> None: ...

class TyTuple(_message.Message):
    __slots__ = ("fixed", "is_variable")
    FIXED_FIELD_NUMBER: _ClassVar[int]
    IS_VARIABLE_FIELD_NUMBER: _ClassVar[int]
    fixed: _containers.RepeatedCompositeFieldContainer[Ty]
    is_variable: bool
    def __init__(self, fixed: _Optional[_Iterable[_Union[Ty, _Mapping]]] = ..., is_variable: bool = ...) -> None: ...

class StringTyPair(_message.Message):
    __slots__ = ("key", "ty")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TY_FIELD_NUMBER: _ClassVar[int]
    key: str
    ty: Ty
    def __init__(self, key: _Optional[str] = ..., ty: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

class TyLogicalStruct(_message.Message):
    __slots__ = ("fields", "ordered_fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Ty
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

    FIELDS_FIELD_NUMBER: _ClassVar[int]
    ORDERED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.MessageMap[str, Ty]
    ordered_fields: _containers.RepeatedCompositeFieldContainer[StringTyPair]
    def __init__(
        self,
        fields: _Optional[_Mapping[str, Ty]] = ...,
        ordered_fields: _Optional[_Iterable[_Union[StringTyPair, _Mapping]]] = ...,
    ) -> None: ...

class TyFeatureClass(_message.Message):
    __slots__ = ("constructor_namespace", "assigned_fields", "ordered_assigned_fields")
    class AssignedFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Ty
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Ty, _Mapping]] = ...) -> None: ...

    CONSTRUCTOR_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    ORDERED_ASSIGNED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    constructor_namespace: str
    assigned_fields: _containers.MessageMap[str, Ty]
    ordered_assigned_fields: _containers.RepeatedCompositeFieldContainer[StringTyPair]
    def __init__(
        self,
        constructor_namespace: _Optional[str] = ...,
        assigned_fields: _Optional[_Mapping[str, Ty]] = ...,
        ordered_assigned_fields: _Optional[_Iterable[_Union[StringTyPair, _Mapping]]] = ...,
    ) -> None: ...

class TyEnum(_message.Message):
    __slots__ = ("module", "name", "bases", "ty")
    MODULE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASES_FIELD_NUMBER: _ClassVar[int]
    TY_FIELD_NUMBER: _ClassVar[int]
    module: str
    name: str
    bases: _containers.RepeatedCompositeFieldContainer[Ty]
    ty: Ty
    def __init__(
        self,
        module: _Optional[str] = ...,
        name: _Optional[str] = ...,
        bases: _Optional[_Iterable[_Union[Ty, _Mapping]]] = ...,
        ty: _Optional[_Union[Ty, _Mapping]] = ...,
    ) -> None: ...

class Ty(_message.Message):
    __slots__ = (
        "nullable",
        "int",
        "str",
        "bool",
        "float",
        "list",
        "set",
        "none",
        "any",
        "iterable",
        "datetime",
        "timedelta",
        "date",
        "tuple",
        "dict",
        "bytes",
        "logical_struct",
        "feature_class",
        "enum",
        "sequence_matcher",
        "generator",
        "never",
        "requests_http_response",
    )
    NULLABLE_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    STR_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    NONE_FIELD_NUMBER: _ClassVar[int]
    ANY_FIELD_NUMBER: _ClassVar[int]
    ITERABLE_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    TIMEDELTA_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    DICT_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_STRUCT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_CLASS_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_MATCHER_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_FIELD_NUMBER: _ClassVar[int]
    NEVER_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_HTTP_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    nullable: bool
    int: EmptyMessage
    str: EmptyMessage
    bool: EmptyMessage
    float: EmptyMessage
    list: TyList
    set: TySet
    none: EmptyMessage
    any: EmptyMessage
    iterable: TyIterable
    datetime: TyDatetime
    timedelta: EmptyMessage
    date: EmptyMessage
    tuple: TyTuple
    dict: TyDict
    bytes: EmptyMessage
    logical_struct: TyLogicalStruct
    feature_class: TyFeatureClass
    enum: TyEnum
    sequence_matcher: EmptyMessage
    generator: TyGenerator
    never: EmptyMessage
    requests_http_response: EmptyMessage
    def __init__(
        self,
        nullable: bool = ...,
        int: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        str: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        bool: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        float: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        list: _Optional[_Union[TyList, _Mapping]] = ...,
        set: _Optional[_Union[TySet, _Mapping]] = ...,
        none: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        any: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        iterable: _Optional[_Union[TyIterable, _Mapping]] = ...,
        datetime: _Optional[_Union[TyDatetime, _Mapping]] = ...,
        timedelta: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        date: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        tuple: _Optional[_Union[TyTuple, _Mapping]] = ...,
        dict: _Optional[_Union[TyDict, _Mapping]] = ...,
        bytes: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        logical_struct: _Optional[_Union[TyLogicalStruct, _Mapping]] = ...,
        feature_class: _Optional[_Union[TyFeatureClass, _Mapping]] = ...,
        enum: _Optional[_Union[TyEnum, _Mapping]] = ...,
        sequence_matcher: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        generator: _Optional[_Union[TyGenerator, _Mapping]] = ...,
        never: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        requests_http_response: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
    ) -> None: ...

class EmptyMessage(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SymbolicConst(_message.Message):
    __slots__ = ("ty", "value")
    TY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ty: Ty
    value: _arrow_pb2.ScalarValue
    def __init__(
        self,
        ty: _Optional[_Union[Ty, _Mapping]] = ...,
        value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
    ) -> None: ...

class CodeVariable(_message.Message):
    __slots__ = ("name", "module")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    name: str
    module: str
    def __init__(self, name: _Optional[str] = ..., module: _Optional[str] = ...) -> None: ...

class CodeVariableValue(_message.Message):
    __slots__ = ("variable", "value")
    VARIABLE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    variable: CodeVariable
    value: SymbolicConst
    def __init__(
        self,
        variable: _Optional[_Union[CodeVariable, _Mapping]] = ...,
        value: _Optional[_Union[SymbolicConst, _Mapping]] = ...,
    ) -> None: ...

class GlobalVariablesInfo(_message.Message):
    __slots__ = ("code_variables", "environment_variables")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    CODE_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    code_variables: _containers.RepeatedCompositeFieldContainer[CodeVariableValue]
    environment_variables: _containers.ScalarMap[str, str]
    def __init__(
        self,
        code_variables: _Optional[_Iterable[_Union[CodeVariableValue, _Mapping]]] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...
