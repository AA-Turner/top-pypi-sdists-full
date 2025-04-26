from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import aws_credentials__client_pb2 as _aws_credentials__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.offlinestore.delta import metadata__client_pb2 as _metadata__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddFile(_message.Message):
    __slots__ = ["partition_values", "stats", "tags", "uri"]
    class PartitionValuesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PARTITION_VALUES_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    partition_values: _containers.ScalarMap[str, str]
    stats: str
    tags: _containers.ScalarMap[str, str]
    uri: str
    def __init__(self, uri: _Optional[str] = ..., partition_values: _Optional[_Mapping[str, str]] = ..., tags: _Optional[_Mapping[str, str]] = ..., stats: _Optional[str] = ...) -> None: ...

class CrossAccountRoleConfig(_message.Message):
    __slots__ = ["dynamo_cross_account_role", "s3_cross_account_role"]
    DYNAMO_CROSS_ACCOUNT_ROLE_FIELD_NUMBER: _ClassVar[int]
    S3_CROSS_ACCOUNT_ROLE_FIELD_NUMBER: _ClassVar[int]
    dynamo_cross_account_role: _aws_credentials__client_pb2.AwsIamRole
    s3_cross_account_role: _aws_credentials__client_pb2.AwsIamRole
    def __init__(self, s3_cross_account_role: _Optional[_Union[_aws_credentials__client_pb2.AwsIamRole, _Mapping]] = ..., dynamo_cross_account_role: _Optional[_Union[_aws_credentials__client_pb2.AwsIamRole, _Mapping]] = ...) -> None: ...

class Expression(_message.Message):
    __slots__ = ["binary", "column", "literal"]
    class Binary(_message.Message):
        __slots__ = ["left", "op", "right"]
        class Op(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        LEFT_FIELD_NUMBER: _ClassVar[int]
        OP_AND: Expression.Binary.Op
        OP_EQ: Expression.Binary.Op
        OP_FIELD_NUMBER: _ClassVar[int]
        OP_LE: Expression.Binary.Op
        OP_LT: Expression.Binary.Op
        OP_OR: Expression.Binary.Op
        OP_UNSPECIFIED: Expression.Binary.Op
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        left: Expression
        op: Expression.Binary.Op
        right: Expression
        def __init__(self, op: _Optional[_Union[Expression.Binary.Op, str]] = ..., left: _Optional[_Union[Expression, _Mapping]] = ..., right: _Optional[_Union[Expression, _Mapping]] = ...) -> None: ...
    class Literal(_message.Message):
        __slots__ = ["bool", "int64", "str", "timestamp"]
        BOOL_FIELD_NUMBER: _ClassVar[int]
        INT64_FIELD_NUMBER: _ClassVar[int]
        STR_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        bool: bool
        int64: int
        str: str
        timestamp: _timestamp_pb2.Timestamp
        def __init__(self, str: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., int64: _Optional[int] = ..., bool: bool = ...) -> None: ...
    BINARY_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    binary: Expression.Binary
    column: _schema__client_pb2.Column
    literal: Expression.Literal
    def __init__(self, column: _Optional[_Union[_schema__client_pb2.Column, _Mapping]] = ..., literal: _Optional[_Union[Expression.Literal, _Mapping]] = ..., binary: _Optional[_Union[Expression.Binary, _Mapping]] = ...) -> None: ...

class GetPartitionsArgs(_message.Message):
    __slots__ = ["tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.ScalarMap[str, str]
    def __init__(self, tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetPartitionsResult(_message.Message):
    __slots__ = ["partitions"]
    class Partition(_message.Message):
        __slots__ = ["values"]
        class ValuesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.ScalarMap[str, str]
        def __init__(self, values: _Optional[_Mapping[str, str]] = ...) -> None: ...
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    partitions: _containers.RepeatedCompositeFieldContainer[GetPartitionsResult.Partition]
    def __init__(self, partitions: _Optional[_Iterable[_Union[GetPartitionsResult.Partition, _Mapping]]] = ...) -> None: ...

class InitializeArgs(_message.Message):
    __slots__ = ["cross_account_role_configs", "description", "dynamodb_log_table_name", "dynamodb_log_table_region", "id", "kms_key_arn", "name", "partition_columns", "path", "schema"]
    CROSS_ACCOUNT_ROLE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_LOG_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_LOG_TABLE_REGION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ARN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    cross_account_role_configs: CrossAccountRoleConfig
    description: str
    dynamodb_log_table_name: str
    dynamodb_log_table_region: str
    id: str
    kms_key_arn: str
    name: str
    partition_columns: _containers.RepeatedScalarFieldContainer[str]
    path: str
    schema: _schema__client_pb2.Schema
    def __init__(self, path: _Optional[str] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., partition_columns: _Optional[_Iterable[str]] = ..., dynamodb_log_table_name: _Optional[str] = ..., dynamodb_log_table_region: _Optional[str] = ..., cross_account_role_configs: _Optional[_Union[CrossAccountRoleConfig, _Mapping]] = ..., kms_key_arn: _Optional[str] = ...) -> None: ...

class ReadForUpdateArgs(_message.Message):
    __slots__ = ["read_predicate"]
    READ_PREDICATE_FIELD_NUMBER: _ClassVar[int]
    read_predicate: Expression
    def __init__(self, read_predicate: _Optional[_Union[Expression, _Mapping]] = ...) -> None: ...

class ReadForUpdateResult(_message.Message):
    __slots__ = ["uris"]
    URIS_FIELD_NUMBER: _ClassVar[int]
    uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uris: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateArgs(_message.Message):
    __slots__ = ["add_files", "delete_uris", "user_metadata"]
    ADD_FILES_FIELD_NUMBER: _ClassVar[int]
    DELETE_URIS_FIELD_NUMBER: _ClassVar[int]
    USER_METADATA_FIELD_NUMBER: _ClassVar[int]
    add_files: _containers.RepeatedCompositeFieldContainer[AddFile]
    delete_uris: _containers.RepeatedScalarFieldContainer[str]
    user_metadata: _metadata__client_pb2.TectonDeltaMetadata
    def __init__(self, add_files: _Optional[_Iterable[_Union[AddFile, _Mapping]]] = ..., user_metadata: _Optional[_Union[_metadata__client_pb2.TectonDeltaMetadata, _Mapping]] = ..., delete_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateResult(_message.Message):
    __slots__ = ["committed_version", "error_message", "error_type"]
    class ErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    COMMITTED_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONCURRENT_APPEND_ERROR: UpdateResult.ErrorType
    CONCURRENT_DELETE_DELETE_ERROR: UpdateResult.ErrorType
    CONCURRENT_DELETE_READ_ERROR: UpdateResult.ErrorType
    CONCURRENT_TRANSACTION_ERROR: UpdateResult.ErrorType
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_UNKNOWN: UpdateResult.ErrorType
    ERROR_UNSPECIFIED: UpdateResult.ErrorType
    METADATA_CHANGED_ERROR: UpdateResult.ErrorType
    PROTOCOL_CHANGED_ERROR: UpdateResult.ErrorType
    committed_version: int
    error_message: str
    error_type: UpdateResult.ErrorType
    def __init__(self, committed_version: _Optional[int] = ..., error_type: _Optional[_Union[UpdateResult.ErrorType, str]] = ..., error_message: _Optional[str] = ...) -> None: ...
