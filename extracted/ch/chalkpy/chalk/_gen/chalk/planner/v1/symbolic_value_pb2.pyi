from chalk._gen.chalk.python.v1 import types_pb2 as _types_pb2
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

class SymbolicValue(_message.Message):
    __slots__ = (
        "ty",
        "symbolic_parameter",
        "symbolic_const",
        "symbolic_func_call",
        "symbolic_branch",
        "symbolic_struct_class_constructor",
        "symbolic_feature_class_constructor",
        "symbolic_confluent_kafka_serialization_context",
        "symbolic_lambda_parameter",
        "symbolic_lambda_function",
        "symbolic_struct_field",
        "symbolic_struct_pack",
        "symbolic_slice",
        "symbolic_tuple",
        "symbolic_dict",
        "sequence_matcher_symbolic_value",
        "symbolic_protobuf_message_class",
        "symbolic_proto_enum",
        "symbolic_value_ref",
        "this_ref",
    )
    TY_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_CONST_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_FUNC_CALL_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_BRANCH_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_STRUCT_CLASS_CONSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_FEATURE_CLASS_CONSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_CONFLUENT_KAFKA_SERIALIZATION_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_LAMBDA_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_LAMBDA_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_STRUCT_FIELD_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_STRUCT_PACK_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_SLICE_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_TUPLE_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_DICT_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_MATCHER_SYMBOLIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_PROTOBUF_MESSAGE_CLASS_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_PROTO_ENUM_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_VALUE_REF_FIELD_NUMBER: _ClassVar[int]
    THIS_REF_FIELD_NUMBER: _ClassVar[int]
    ty: _types_pb2.Ty
    symbolic_parameter: SymbolicParameter
    symbolic_const: _types_pb2.SymbolicConst
    symbolic_func_call: SymbolicFuncCall
    symbolic_branch: SymbolicBranch
    symbolic_struct_class_constructor: SymbolicStructClassConstructor
    symbolic_feature_class_constructor: SymbolicFeatureClassConstructor
    symbolic_confluent_kafka_serialization_context: SymbolicConfluentKafkaSerializationContext
    symbolic_lambda_parameter: SymbolicLambdaParameter
    symbolic_lambda_function: SymbolicLambdaFunction
    symbolic_struct_field: SymbolicStructField
    symbolic_struct_pack: SymbolicStructPack
    symbolic_slice: SymbolicSlice
    symbolic_tuple: SymbolicTuple
    symbolic_dict: SymbolicDict
    sequence_matcher_symbolic_value: SequenceMatcherSymbolicValue
    symbolic_protobuf_message_class: SymbolicProtobufMessageClass
    symbolic_proto_enum: SymbolicProtoEnum
    symbolic_value_ref: EmptyMessage
    this_ref: SymbolicValueRef
    def __init__(
        self,
        ty: _Optional[_Union[_types_pb2.Ty, _Mapping]] = ...,
        symbolic_parameter: _Optional[_Union[SymbolicParameter, _Mapping]] = ...,
        symbolic_const: _Optional[_Union[_types_pb2.SymbolicConst, _Mapping]] = ...,
        symbolic_func_call: _Optional[_Union[SymbolicFuncCall, _Mapping]] = ...,
        symbolic_branch: _Optional[_Union[SymbolicBranch, _Mapping]] = ...,
        symbolic_struct_class_constructor: _Optional[_Union[SymbolicStructClassConstructor, _Mapping]] = ...,
        symbolic_feature_class_constructor: _Optional[_Union[SymbolicFeatureClassConstructor, _Mapping]] = ...,
        symbolic_confluent_kafka_serialization_context: _Optional[
            _Union[SymbolicConfluentKafkaSerializationContext, _Mapping]
        ] = ...,
        symbolic_lambda_parameter: _Optional[_Union[SymbolicLambdaParameter, _Mapping]] = ...,
        symbolic_lambda_function: _Optional[_Union[SymbolicLambdaFunction, _Mapping]] = ...,
        symbolic_struct_field: _Optional[_Union[SymbolicStructField, _Mapping]] = ...,
        symbolic_struct_pack: _Optional[_Union[SymbolicStructPack, _Mapping]] = ...,
        symbolic_slice: _Optional[_Union[SymbolicSlice, _Mapping]] = ...,
        symbolic_tuple: _Optional[_Union[SymbolicTuple, _Mapping]] = ...,
        symbolic_dict: _Optional[_Union[SymbolicDict, _Mapping]] = ...,
        sequence_matcher_symbolic_value: _Optional[_Union[SequenceMatcherSymbolicValue, _Mapping]] = ...,
        symbolic_protobuf_message_class: _Optional[_Union[SymbolicProtobufMessageClass, _Mapping]] = ...,
        symbolic_proto_enum: _Optional[_Union[SymbolicProtoEnum, _Mapping]] = ...,
        symbolic_value_ref: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        this_ref: _Optional[_Union[SymbolicValueRef, _Mapping]] = ...,
    ) -> None: ...

class EmptyMessage(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SymbolicValueRef(_message.Message):
    __slots__ = ("ref_id",)
    REF_ID_FIELD_NUMBER: _ClassVar[int]
    ref_id: int
    def __init__(self, ref_id: _Optional[int] = ...) -> None: ...

class SymbolicParameter(_message.Message):
    __slots__ = ("name", "index")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    name: str
    index: int
    def __init__(self, name: _Optional[str] = ..., index: _Optional[int] = ...) -> None: ...

class SymbolicFuncCall(_message.Message):
    __slots__ = ("function_name", "args")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    args: _containers.RepeatedCompositeFieldContainer[SymbolicValue]
    def __init__(
        self, function_name: _Optional[str] = ..., args: _Optional[_Iterable[_Union[SymbolicValue, _Mapping]]] = ...
    ) -> None: ...

class SymbolicBranch(_message.Message):
    __slots__ = ("condition", "if_true", "if_false")
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    IF_TRUE_FIELD_NUMBER: _ClassVar[int]
    IF_FALSE_FIELD_NUMBER: _ClassVar[int]
    condition: SymbolicValue
    if_true: SymbolicValue
    if_false: SymbolicValue
    def __init__(
        self,
        condition: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
        if_true: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
        if_false: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
    ) -> None: ...

class StringSymbolicValuePair(_message.Message):
    __slots__ = ("key", "symbolic_value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    symbolic_value: SymbolicValue
    def __init__(
        self, key: _Optional[str] = ..., symbolic_value: _Optional[_Union[SymbolicValue, _Mapping]] = ...
    ) -> None: ...

class SymbolicStructClassConstructor(_message.Message):
    __slots__ = ("struct_name", "fields", "ordered_fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SymbolicValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[SymbolicValue, _Mapping]] = ...
        ) -> None: ...

    STRUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    ORDERED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    struct_name: str
    fields: _containers.MessageMap[str, SymbolicValue]
    ordered_fields: _containers.RepeatedCompositeFieldContainer[StringSymbolicValuePair]
    def __init__(
        self,
        struct_name: _Optional[str] = ...,
        fields: _Optional[_Mapping[str, SymbolicValue]] = ...,
        ordered_fields: _Optional[_Iterable[_Union[StringSymbolicValuePair, _Mapping]]] = ...,
    ) -> None: ...

class SymbolicFeatureClassConstructor(_message.Message):
    __slots__ = ("constructor_namespace", "fields", "ordered_fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SymbolicValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[SymbolicValue, _Mapping]] = ...
        ) -> None: ...

    CONSTRUCTOR_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    ORDERED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    constructor_namespace: str
    fields: _containers.MessageMap[str, SymbolicValue]
    ordered_fields: _containers.RepeatedCompositeFieldContainer[StringSymbolicValuePair]
    def __init__(
        self,
        constructor_namespace: _Optional[str] = ...,
        fields: _Optional[_Mapping[str, SymbolicValue]] = ...,
        ordered_fields: _Optional[_Iterable[_Union[StringSymbolicValuePair, _Mapping]]] = ...,
    ) -> None: ...

class SymbolicConfluentKafkaSerializationContext(_message.Message):
    __slots__ = ("topic", "message_field")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_FIELD_NUMBER: _ClassVar[int]
    topic: SymbolicValue
    message_field: SymbolicValue
    def __init__(
        self,
        topic: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
        message_field: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
    ) -> None: ...

class SymbolicLambdaParameter(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SymbolicLambdaFunction(_message.Message):
    __slots__ = ("parameters", "body")
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[SymbolicValue]
    body: SymbolicValue
    def __init__(
        self,
        parameters: _Optional[_Iterable[_Union[SymbolicValue, _Mapping]]] = ...,
        body: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
    ) -> None: ...

class SymbolicStructField(_message.Message):
    __slots__ = ("struct", "field_name_str", "field_name_int")
    STRUCT_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_STR_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_INT_FIELD_NUMBER: _ClassVar[int]
    struct: SymbolicValue
    field_name_str: str
    field_name_int: int
    def __init__(
        self,
        struct: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
        field_name_str: _Optional[str] = ...,
        field_name_int: _Optional[int] = ...,
    ) -> None: ...

class SymbolicStructPack(_message.Message):
    __slots__ = ("fields", "ordered_fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SymbolicValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[SymbolicValue, _Mapping]] = ...
        ) -> None: ...

    FIELDS_FIELD_NUMBER: _ClassVar[int]
    ORDERED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.MessageMap[str, SymbolicValue]
    ordered_fields: _containers.RepeatedCompositeFieldContainer[StringSymbolicValuePair]
    def __init__(
        self,
        fields: _Optional[_Mapping[str, SymbolicValue]] = ...,
        ordered_fields: _Optional[_Iterable[_Union[StringSymbolicValuePair, _Mapping]]] = ...,
    ) -> None: ...

class SymbolicSlice(_message.Message):
    __slots__ = ("lower", "upper", "step")
    LOWER_FIELD_NUMBER: _ClassVar[int]
    UPPER_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    lower: SymbolicValue
    upper: SymbolicValue
    step: SymbolicValue
    def __init__(
        self,
        lower: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
        upper: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
        step: _Optional[_Union[SymbolicValue, _Mapping]] = ...,
    ) -> None: ...

class SymbolicTuple(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[SymbolicValue]
    def __init__(self, values: _Optional[_Iterable[_Union[SymbolicValue, _Mapping]]] = ...) -> None: ...

class SymbolicDict(_message.Message):
    __slots__ = ("values_keys", "values_values")
    VALUES_KEYS_FIELD_NUMBER: _ClassVar[int]
    VALUES_VALUES_FIELD_NUMBER: _ClassVar[int]
    values_keys: _containers.RepeatedCompositeFieldContainer[SymbolicValue]
    values_values: _containers.RepeatedCompositeFieldContainer[SymbolicValue]
    def __init__(
        self,
        values_keys: _Optional[_Iterable[_Union[SymbolicValue, _Mapping]]] = ...,
        values_values: _Optional[_Iterable[_Union[SymbolicValue, _Mapping]]] = ...,
    ) -> None: ...

class SequenceMatcherSymbolicValue(_message.Message):
    __slots__ = ("a", "b")
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    a: SymbolicValue
    b: SymbolicValue
    def __init__(
        self, a: _Optional[_Union[SymbolicValue, _Mapping]] = ..., b: _Optional[_Union[SymbolicValue, _Mapping]] = ...
    ) -> None: ...

class SymbolicProtobufMessageClass(_message.Message):
    __slots__ = ("class_name", "module_name")
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    module_name: str
    def __init__(self, class_name: _Optional[str] = ..., module_name: _Optional[str] = ...) -> None: ...

class SymbolicProtoEnum(_message.Message):
    __slots__ = ("class_name", "module_name", "full_qualified_name", "value_to_name_map")
    class ValueToNameMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...

    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    FULL_QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_TO_NAME_MAP_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    module_name: str
    full_qualified_name: str
    value_to_name_map: _containers.ScalarMap[int, str]
    def __init__(
        self,
        class_name: _Optional[str] = ...,
        module_name: _Optional[str] = ...,
        full_qualified_name: _Optional[str] = ...,
        value_to_name_map: _Optional[_Mapping[int, str]] = ...,
    ) -> None: ...
