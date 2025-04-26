from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class FeatherBodyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATHER_BODY_TYPE_UNSPECIFIED: _ClassVar[FeatherBodyType]
    FEATHER_BODY_TYPE_TABLE: _ClassVar[FeatherBodyType]
    FEATHER_BODY_TYPE_RECORD_BATCHES: _ClassVar[FeatherBodyType]

FEATHER_BODY_TYPE_UNSPECIFIED: FeatherBodyType
FEATHER_BODY_TYPE_TABLE: FeatherBodyType
FEATHER_BODY_TYPE_RECORD_BATCHES: FeatherBodyType

class OnlineQueryRequest(_message.Message):
    __slots__ = ("inputs", "outputs", "now", "staleness", "context", "response_options")
    class InputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class StalenessEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    NOW_FIELD_NUMBER: _ClassVar[int]
    STALENESS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.MessageMap[str, _struct_pb2.Value]
    outputs: _containers.RepeatedCompositeFieldContainer[OutputExpr]
    now: _timestamp_pb2.Timestamp
    staleness: _containers.ScalarMap[str, str]
    context: OnlineQueryContext
    response_options: OnlineQueryResponseOptions
    def __init__(
        self,
        inputs: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        outputs: _Optional[_Iterable[_Union[OutputExpr, _Mapping]]] = ...,
        now: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        staleness: _Optional[_Mapping[str, str]] = ...,
        context: _Optional[_Union[OnlineQueryContext, _Mapping]] = ...,
        response_options: _Optional[_Union[OnlineQueryResponseOptions, _Mapping]] = ...,
    ) -> None: ...

class OnlineQueryBulkRequest(_message.Message):
    __slots__ = ("inputs_feather", "outputs", "now", "staleness", "context", "response_options", "body_type")
    class StalenessEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    INPUTS_FEATHER_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    NOW_FIELD_NUMBER: _ClassVar[int]
    STALENESS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    BODY_TYPE_FIELD_NUMBER: _ClassVar[int]
    inputs_feather: bytes
    outputs: _containers.RepeatedCompositeFieldContainer[OutputExpr]
    now: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    staleness: _containers.ScalarMap[str, str]
    context: OnlineQueryContext
    response_options: OnlineQueryResponseOptions
    body_type: FeatherBodyType
    def __init__(
        self,
        inputs_feather: _Optional[bytes] = ...,
        outputs: _Optional[_Iterable[_Union[OutputExpr, _Mapping]]] = ...,
        now: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...,
        staleness: _Optional[_Mapping[str, str]] = ...,
        context: _Optional[_Union[OnlineQueryContext, _Mapping]] = ...,
        response_options: _Optional[_Union[OnlineQueryResponseOptions, _Mapping]] = ...,
        body_type: _Optional[_Union[FeatherBodyType, str]] = ...,
    ) -> None: ...

class GenericSingleQuery(_message.Message):
    __slots__ = ("single_request", "bulk_request")
    SINGLE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    BULK_REQUEST_FIELD_NUMBER: _ClassVar[int]
    single_request: OnlineQueryRequest
    bulk_request: OnlineQueryBulkRequest
    def __init__(
        self,
        single_request: _Optional[_Union[OnlineQueryRequest, _Mapping]] = ...,
        bulk_request: _Optional[_Union[OnlineQueryBulkRequest, _Mapping]] = ...,
    ) -> None: ...

class OnlineQueryMultiRequest(_message.Message):
    __slots__ = ("queries",)
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedCompositeFieldContainer[GenericSingleQuery]
    def __init__(self, queries: _Optional[_Iterable[_Union[GenericSingleQuery, _Mapping]]] = ...) -> None: ...

class FeatureExpression(_message.Message):
    __slots__ = ("output_column_name", "namespace", "expr")
    OUTPUT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    output_column_name: str
    namespace: str
    expr: _expression_pb2.LogicalExprNode
    def __init__(
        self,
        output_column_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        expr: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class OutputExpr(_message.Message):
    __slots__ = ("feature_fqn", "feature_expression")
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    FEATURE_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    feature_expression: FeatureExpression
    def __init__(
        self,
        feature_fqn: _Optional[str] = ...,
        feature_expression: _Optional[_Union[FeatureExpression, _Mapping]] = ...,
    ) -> None: ...

class OnlineQueryContext(_message.Message):
    __slots__ = (
        "environment",
        "tags",
        "required_resolver_tags",
        "deployment_id",
        "branch_id",
        "correlation_id",
        "query_name",
        "query_name_version",
        "options",
        "value_metrics_tag_by_features",
        "query_context",
    )
    class OptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class QueryContextEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_RESOLVER_TAGS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_VERSION_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    VALUE_METRICS_TAG_BY_FEATURES_FIELD_NUMBER: _ClassVar[int]
    QUERY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    environment: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    required_resolver_tags: _containers.RepeatedScalarFieldContainer[str]
    deployment_id: str
    branch_id: str
    correlation_id: str
    query_name: str
    query_name_version: str
    options: _containers.MessageMap[str, _struct_pb2.Value]
    value_metrics_tag_by_features: _containers.RepeatedCompositeFieldContainer[OutputExpr]
    query_context: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        environment: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        required_resolver_tags: _Optional[_Iterable[str]] = ...,
        deployment_id: _Optional[str] = ...,
        branch_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        query_name_version: _Optional[str] = ...,
        options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        value_metrics_tag_by_features: _Optional[_Iterable[_Union[OutputExpr, _Mapping]]] = ...,
        query_context: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class OnlineQueryResponseOptions(_message.Message):
    __slots__ = ("include_meta", "explain", "encoding_options", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    INCLUDE_META_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    ENCODING_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    include_meta: bool
    explain: ExplainOptions
    encoding_options: FeatureEncodingOptions
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        include_meta: bool = ...,
        explain: _Optional[_Union[ExplainOptions, _Mapping]] = ...,
        encoding_options: _Optional[_Union[FeatureEncodingOptions, _Mapping]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ExplainOptions(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FeatureEncodingOptions(_message.Message):
    __slots__ = ("encode_structs_as_objects",)
    ENCODE_STRUCTS_AS_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    encode_structs_as_objects: bool
    def __init__(self, encode_structs_as_objects: bool = ...) -> None: ...

class OnlineQueryResponse(_message.Message):
    __slots__ = ("data", "errors", "response_meta")
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_META_FIELD_NUMBER: _ClassVar[int]
    data: OnlineQueryResult
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    response_meta: OnlineQueryMetadata
    def __init__(
        self,
        data: _Optional[_Union[OnlineQueryResult, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        response_meta: _Optional[_Union[OnlineQueryMetadata, _Mapping]] = ...,
    ) -> None: ...

class OnlineQueryBulkResponse(_message.Message):
    __slots__ = ("scalars_data", "groups_data", "errors", "response_meta")
    class GroupsDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...

    SCALARS_DATA_FIELD_NUMBER: _ClassVar[int]
    GROUPS_DATA_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_META_FIELD_NUMBER: _ClassVar[int]
    scalars_data: bytes
    groups_data: _containers.ScalarMap[str, bytes]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    response_meta: OnlineQueryMetadata
    def __init__(
        self,
        scalars_data: _Optional[bytes] = ...,
        groups_data: _Optional[_Mapping[str, bytes]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        response_meta: _Optional[_Union[OnlineQueryMetadata, _Mapping]] = ...,
    ) -> None: ...

class GenericSingleResponse(_message.Message):
    __slots__ = ("single_response", "bulk_response")
    SINGLE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    BULK_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    single_response: OnlineQueryResponse
    bulk_response: OnlineQueryBulkResponse
    def __init__(
        self,
        single_response: _Optional[_Union[OnlineQueryResponse, _Mapping]] = ...,
        bulk_response: _Optional[_Union[OnlineQueryBulkResponse, _Mapping]] = ...,
    ) -> None: ...

class OnlineQueryMultiResponse(_message.Message):
    __slots__ = ("responses", "errors")
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[GenericSingleResponse]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        responses: _Optional[_Iterable[_Union[GenericSingleResponse, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class OnlineQueryResult(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[FeatureResult]
    def __init__(self, results: _Optional[_Iterable[_Union[FeatureResult, _Mapping]]] = ...) -> None: ...

class FeatureResult(_message.Message):
    __slots__ = ("field", "pkey", "value", "error", "ts", "meta")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    PKEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    field: str
    pkey: _struct_pb2.Value
    value: _struct_pb2.Value
    error: _chalk_error_pb2.ChalkError
    ts: _timestamp_pb2.Timestamp
    meta: FeatureMeta
    def __init__(
        self,
        field: _Optional[str] = ...,
        pkey: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        meta: _Optional[_Union[FeatureMeta, _Mapping]] = ...,
    ) -> None: ...

class FeatureMeta(_message.Message):
    __slots__ = ("chosen_resolver_fqn", "cache_hit", "primitive_type", "version")
    CHOSEN_RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    CACHE_HIT_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    chosen_resolver_fqn: str
    cache_hit: bool
    primitive_type: str
    version: int
    def __init__(
        self,
        chosen_resolver_fqn: _Optional[str] = ...,
        cache_hit: bool = ...,
        primitive_type: _Optional[str] = ...,
        version: _Optional[int] = ...,
    ) -> None: ...

class OnlineQueryMetadata(_message.Message):
    __slots__ = (
        "execution_duration",
        "deployment_id",
        "environment_id",
        "environment_name",
        "query_id",
        "query_timestamp",
        "query_hash",
        "explain_output",
        "metadata",
        "additional_metadata",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class AdditionalMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    EXECUTION_DURATION_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    QUERY_HASH_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    execution_duration: _duration_pb2.Duration
    deployment_id: str
    environment_id: str
    environment_name: str
    query_id: str
    query_timestamp: _timestamp_pb2.Timestamp
    query_hash: str
    explain_output: QueryExplainInfo
    metadata: _containers.ScalarMap[str, str]
    additional_metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        execution_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        deployment_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        environment_name: _Optional[str] = ...,
        query_id: _Optional[str] = ...,
        query_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_hash: _Optional[str] = ...,
        explain_output: _Optional[_Union[QueryExplainInfo, _Mapping]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        additional_metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class QueryExplainInfo(_message.Message):
    __slots__ = ("plan_string",)
    PLAN_STRING_FIELD_NUMBER: _ClassVar[int]
    plan_string: str
    def __init__(self, plan_string: _Optional[str] = ...) -> None: ...

class UploadFeaturesBulkRequest(_message.Message):
    __slots__ = ("inputs_feather", "body_type")
    INPUTS_FEATHER_FIELD_NUMBER: _ClassVar[int]
    BODY_TYPE_FIELD_NUMBER: _ClassVar[int]
    inputs_feather: bytes
    body_type: FeatherBodyType
    def __init__(
        self, inputs_feather: _Optional[bytes] = ..., body_type: _Optional[_Union[FeatherBodyType, str]] = ...
    ) -> None: ...

class UploadFeaturesBulkResponse(_message.Message):
    __slots__ = ("errors",)
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(self, errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...) -> None: ...
