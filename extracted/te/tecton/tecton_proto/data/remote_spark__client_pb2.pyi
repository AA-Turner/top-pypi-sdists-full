from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2_1
from tecton_proto.data import hive_metastore__client_pb2 as _hive_metastore__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteRequest(_message.Message):
    __slots__ = ["envVars", "getBatchDataSourceFunctionSchema", "getFeatureViewSchema", "getFileSourceSchema", "getHiveTableSchema", "getKafkaSourceSchema", "getKinesisSourceSchema", "getMultipleDataSourceSchemasRequest", "getMultipleFeatureViewSchemasRequest", "getQueryPlanInfoForFeatureViewPipeline", "getRedshiftTableSchema", "getSnowflakeSchema", "getStreamDataSourceFunctionSchema", "getUnityTableSchema", "listHiveDatabases", "listHiveTableColumns", "listHiveTables"]
    class EnvVarsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENVVARS_FIELD_NUMBER: _ClassVar[int]
    GETBATCHDATASOURCEFUNCTIONSCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETFEATUREVIEWSCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETFILESOURCESCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETHIVETABLESCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETKAFKASOURCESCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETKINESISSOURCESCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETMULTIPLEDATASOURCESCHEMASREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETMULTIPLEFEATUREVIEWSCHEMASREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETQUERYPLANINFOFORFEATUREVIEWPIPELINE_FIELD_NUMBER: _ClassVar[int]
    GETREDSHIFTTABLESCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETSNOWFLAKESCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETSTREAMDATASOURCEFUNCTIONSCHEMA_FIELD_NUMBER: _ClassVar[int]
    GETUNITYTABLESCHEMA_FIELD_NUMBER: _ClassVar[int]
    LISTHIVEDATABASES_FIELD_NUMBER: _ClassVar[int]
    LISTHIVETABLECOLUMNS_FIELD_NUMBER: _ClassVar[int]
    LISTHIVETABLES_FIELD_NUMBER: _ClassVar[int]
    envVars: _containers.ScalarMap[str, str]
    getBatchDataSourceFunctionSchema: GetBatchDataSourceFunctionSchema
    getFeatureViewSchema: GetFeatureViewSchema
    getFileSourceSchema: GetFileSourceSchema
    getHiveTableSchema: GetHiveTableSchema
    getKafkaSourceSchema: GetKafkaSourceSchema
    getKinesisSourceSchema: GetKinesisSourceSchema
    getMultipleDataSourceSchemasRequest: GetMultipleDataSourceSchemasRequest
    getMultipleFeatureViewSchemasRequest: GetMultipleFeatureViewSchemasRequest
    getQueryPlanInfoForFeatureViewPipeline: GetQueryPlanInfoForFeatureViewPipeline
    getRedshiftTableSchema: GetRedshiftTableSchema
    getSnowflakeSchema: GetSnowflakeSchema
    getStreamDataSourceFunctionSchema: GetStreamDataSourceFunctionSchema
    getUnityTableSchema: GetUnityTableSchema
    listHiveDatabases: ListHiveDatabases
    listHiveTableColumns: ListHiveTableColumns
    listHiveTables: ListHiveTables
    def __init__(self, getMultipleFeatureViewSchemasRequest: _Optional[_Union[GetMultipleFeatureViewSchemasRequest, _Mapping]] = ..., getMultipleDataSourceSchemasRequest: _Optional[_Union[GetMultipleDataSourceSchemasRequest, _Mapping]] = ..., getHiveTableSchema: _Optional[_Union[GetHiveTableSchema, _Mapping]] = ..., getRedshiftTableSchema: _Optional[_Union[GetRedshiftTableSchema, _Mapping]] = ..., getFileSourceSchema: _Optional[_Union[GetFileSourceSchema, _Mapping]] = ..., getKinesisSourceSchema: _Optional[_Union[GetKinesisSourceSchema, _Mapping]] = ..., getKafkaSourceSchema: _Optional[_Union[GetKafkaSourceSchema, _Mapping]] = ..., getFeatureViewSchema: _Optional[_Union[GetFeatureViewSchema, _Mapping]] = ..., getSnowflakeSchema: _Optional[_Union[GetSnowflakeSchema, _Mapping]] = ..., getBatchDataSourceFunctionSchema: _Optional[_Union[GetBatchDataSourceFunctionSchema, _Mapping]] = ..., getStreamDataSourceFunctionSchema: _Optional[_Union[GetStreamDataSourceFunctionSchema, _Mapping]] = ..., getUnityTableSchema: _Optional[_Union[GetUnityTableSchema, _Mapping]] = ..., listHiveDatabases: _Optional[_Union[ListHiveDatabases, _Mapping]] = ..., listHiveTables: _Optional[_Union[ListHiveTables, _Mapping]] = ..., listHiveTableColumns: _Optional[_Union[ListHiveTableColumns, _Mapping]] = ..., getQueryPlanInfoForFeatureViewPipeline: _Optional[_Union[GetQueryPlanInfoForFeatureViewPipeline, _Mapping]] = ..., envVars: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ExecuteResult(_message.Message):
    __slots__ = ["listHiveResult", "multipleDataSourceSchemaResponse", "multipleFeatureViewSchemaResponse", "queryPlanInfo", "schema", "sparkSchema", "uncaughtError", "validationError"]
    LISTHIVERESULT_FIELD_NUMBER: _ClassVar[int]
    MULTIPLEDATASOURCESCHEMARESPONSE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLEFEATUREVIEWSCHEMARESPONSE_FIELD_NUMBER: _ClassVar[int]
    QUERYPLANINFO_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SPARKSCHEMA_FIELD_NUMBER: _ClassVar[int]
    UNCAUGHTERROR_FIELD_NUMBER: _ClassVar[int]
    VALIDATIONERROR_FIELD_NUMBER: _ClassVar[int]
    listHiveResult: _hive_metastore__client_pb2.ListHiveResult
    multipleDataSourceSchemaResponse: GetMultipleDataSourceSchemasResponse
    multipleFeatureViewSchemaResponse: GetMultipleFeatureViewSchemasResponse
    queryPlanInfo: QueryPlanInfo
    schema: _schema__client_pb2.Schema
    sparkSchema: _spark_schema__client_pb2.SparkSchema
    uncaughtError: str
    validationError: str
    def __init__(self, uncaughtError: _Optional[str] = ..., validationError: _Optional[str] = ..., sparkSchema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., queryPlanInfo: _Optional[_Union[QueryPlanInfo, _Mapping]] = ..., schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., listHiveResult: _Optional[_Union[_hive_metastore__client_pb2.ListHiveResult, _Mapping]] = ..., multipleFeatureViewSchemaResponse: _Optional[_Union[GetMultipleFeatureViewSchemasResponse, _Mapping]] = ..., multipleDataSourceSchemaResponse: _Optional[_Union[GetMultipleDataSourceSchemasResponse, _Mapping]] = ...) -> None: ...

class FeatureViewSchemaRequest(_message.Message):
    __slots__ = ["feature_view", "join_keys", "temporal_aggregate"]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    TEMPORAL_AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    temporal_aggregate: _feature_view__client_pb2_1.TemporalAggregate
    def __init__(self, feature_view: _Optional[_Union[_feature_view__client_pb2.FeatureViewArgs, _Mapping]] = ..., join_keys: _Optional[_Iterable[str]] = ..., temporal_aggregate: _Optional[_Union[_feature_view__client_pb2_1.TemporalAggregate, _Mapping]] = ...) -> None: ...

class FeatureViewSchemaResponse(_message.Message):
    __slots__ = ["timestamp_key", "view_schema"]
    TIMESTAMP_KEY_FIELD_NUMBER: _ClassVar[int]
    VIEW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    timestamp_key: str
    view_schema: _schema__client_pb2.Schema
    def __init__(self, view_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., timestamp_key: _Optional[str] = ...) -> None: ...

class GetBatchDataSourceFunctionSchema(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class GetFeatureViewSchema(_message.Message):
    __slots__ = ["feature_view", "transformations", "virtual_data_sources"]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2_1.VirtualDataSource]
    def __init__(self, virtual_data_sources: _Optional[_Iterable[_Union[_virtual_data_source__client_pb2_1.VirtualDataSource, _Mapping]]] = ..., transformations: _Optional[_Iterable[_Union[_transformation__client_pb2.Transformation, _Mapping]]] = ..., feature_view: _Optional[_Union[_feature_view__client_pb2.FeatureViewArgs, _Mapping]] = ...) -> None: ...

class GetFileSourceSchema(_message.Message):
    __slots__ = ["convertToGlueFormat", "fileFormat", "rawBatchTranslator", "schemaOverride", "schemaUri", "timestampColumn", "timestampFormat", "uri"]
    CONVERTTOGLUEFORMAT_FIELD_NUMBER: _ClassVar[int]
    FILEFORMAT_FIELD_NUMBER: _ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    SCHEMAOVERRIDE_FIELD_NUMBER: _ClassVar[int]
    SCHEMAURI_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPCOLUMN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFORMAT_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    convertToGlueFormat: bool
    fileFormat: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    schemaOverride: _spark_schema__client_pb2.SparkSchema
    schemaUri: str
    timestampColumn: str
    timestampFormat: str
    uri: str
    def __init__(self, uri: _Optional[str] = ..., fileFormat: _Optional[str] = ..., convertToGlueFormat: bool = ..., rawBatchTranslator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., schemaUri: _Optional[str] = ..., timestampColumn: _Optional[str] = ..., timestampFormat: _Optional[str] = ..., schemaOverride: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...

class GetHiveTableSchema(_message.Message):
    __slots__ = ["database", "rawBatchTranslator", "table", "timestampColumn", "timestampFormat"]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPCOLUMN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFORMAT_FIELD_NUMBER: _ClassVar[int]
    database: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    table: str
    timestampColumn: str
    timestampFormat: str
    def __init__(self, database: _Optional[str] = ..., table: _Optional[str] = ..., timestampColumn: _Optional[str] = ..., timestampFormat: _Optional[str] = ..., rawBatchTranslator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class GetKafkaSourceSchema(_message.Message):
    __slots__ = ["rawStreamTranslator", "ssl_keystore_location", "ssl_keystore_password_secret_id"]
    RAWSTREAMTRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    rawStreamTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    ssl_keystore_location: str
    ssl_keystore_password_secret_id: str
    def __init__(self, rawStreamTranslator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., ssl_keystore_location: _Optional[str] = ..., ssl_keystore_password_secret_id: _Optional[str] = ...) -> None: ...

class GetKinesisSourceSchema(_message.Message):
    __slots__ = ["rawStreamTranslator", "streamName"]
    RAWSTREAMTRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    STREAMNAME_FIELD_NUMBER: _ClassVar[int]
    rawStreamTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    streamName: str
    def __init__(self, streamName: _Optional[str] = ..., rawStreamTranslator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class GetMultipleDataSourceSchemasRequest(_message.Message):
    __slots__ = ["data_source_args"]
    DATA_SOURCE_ARGS_FIELD_NUMBER: _ClassVar[int]
    data_source_args: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSourceArgs]
    def __init__(self, data_source_args: _Optional[_Iterable[_Union[_virtual_data_source__client_pb2.VirtualDataSourceArgs, _Mapping]]] = ...) -> None: ...

class GetMultipleDataSourceSchemasResponse(_message.Message):
    __slots__ = ["data_source_responses"]
    class DataSourceResponsesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SparkSchemas
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SparkSchemas, _Mapping]] = ...) -> None: ...
    DATA_SOURCE_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    data_source_responses: _containers.MessageMap[str, SparkSchemas]
    def __init__(self, data_source_responses: _Optional[_Mapping[str, SparkSchemas]] = ...) -> None: ...

class GetMultipleFeatureViewSchemasRequest(_message.Message):
    __slots__ = ["feature_view_requests", "transformations", "virtual_data_sources"]
    FEATURE_VIEW_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    feature_view_requests: _containers.RepeatedCompositeFieldContainer[FeatureViewSchemaRequest]
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2_1.VirtualDataSource]
    def __init__(self, virtual_data_sources: _Optional[_Iterable[_Union[_virtual_data_source__client_pb2_1.VirtualDataSource, _Mapping]]] = ..., transformations: _Optional[_Iterable[_Union[_transformation__client_pb2.Transformation, _Mapping]]] = ..., feature_view_requests: _Optional[_Iterable[_Union[FeatureViewSchemaRequest, _Mapping]]] = ...) -> None: ...

class GetMultipleFeatureViewSchemasResponse(_message.Message):
    __slots__ = ["feature_view_responses"]
    class FeatureViewResponsesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FeatureViewSchemaResponse
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FeatureViewSchemaResponse, _Mapping]] = ...) -> None: ...
    FEATURE_VIEW_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    feature_view_responses: _containers.MessageMap[str, FeatureViewSchemaResponse]
    def __init__(self, feature_view_responses: _Optional[_Mapping[str, FeatureViewSchemaResponse]] = ...) -> None: ...

class GetQueryPlanInfoForFeatureViewPipeline(_message.Message):
    __slots__ = ["feature_view", "transformations", "virtual_data_sources"]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2_1.VirtualDataSource]
    def __init__(self, virtual_data_sources: _Optional[_Iterable[_Union[_virtual_data_source__client_pb2_1.VirtualDataSource, _Mapping]]] = ..., transformations: _Optional[_Iterable[_Union[_transformation__client_pb2.Transformation, _Mapping]]] = ..., feature_view: _Optional[_Union[_feature_view__client_pb2.FeatureViewArgs, _Mapping]] = ...) -> None: ...

class GetRedshiftTableSchema(_message.Message):
    __slots__ = ["endpoint", "query", "rawBatchTranslator", "table", "temp_s3_dir"]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TEMP_S3_DIR_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    query: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    table: str
    temp_s3_dir: str
    def __init__(self, endpoint: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., rawBatchTranslator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., temp_s3_dir: _Optional[str] = ...) -> None: ...

class GetSnowflakeSchema(_message.Message):
    __slots__ = ["database", "post_processor", "query", "role", "schema", "table", "url", "warehouse"]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    database: str
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    query: str
    role: str
    schema: str
    table: str
    url: str
    warehouse: str
    def __init__(self, url: _Optional[str] = ..., role: _Optional[str] = ..., database: _Optional[str] = ..., schema: _Optional[str] = ..., warehouse: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., post_processor: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class GetStreamDataSourceFunctionSchema(_message.Message):
    __slots__ = ["function"]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    def __init__(self, function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class GetUnityTableSchema(_message.Message):
    __slots__ = ["catalog", "rawBatchTranslator", "schema", "table", "timestampColumn", "timestampFormat"]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    RAWBATCHTRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPCOLUMN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPFORMAT_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    rawBatchTranslator: _user_defined_function__client_pb2.UserDefinedFunction
    schema: str
    table: str
    timestampColumn: str
    timestampFormat: str
    def __init__(self, catalog: _Optional[str] = ..., schema: _Optional[str] = ..., table: _Optional[str] = ..., timestampColumn: _Optional[str] = ..., timestampFormat: _Optional[str] = ..., rawBatchTranslator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class ListHiveDatabases(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListHiveTableColumns(_message.Message):
    __slots__ = ["database", "table"]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    database: str
    table: str
    def __init__(self, database: _Optional[str] = ..., table: _Optional[str] = ...) -> None: ...

class ListHiveTables(_message.Message):
    __slots__ = ["database"]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    database: str
    def __init__(self, database: _Optional[str] = ...) -> None: ...

class QueryPlanInfo(_message.Message):
    __slots__ = ["has_aggregations", "has_joins"]
    HAS_AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    HAS_JOINS_FIELD_NUMBER: _ClassVar[int]
    has_aggregations: bool
    has_joins: bool
    def __init__(self, has_joins: bool = ..., has_aggregations: bool = ...) -> None: ...

class SparkSchemas(_message.Message):
    __slots__ = ["batchSchema", "streamSchema"]
    BATCHSCHEMA_FIELD_NUMBER: _ClassVar[int]
    STREAMSCHEMA_FIELD_NUMBER: _ClassVar[int]
    batchSchema: _spark_schema__client_pb2.SparkSchema
    streamSchema: _spark_schema__client_pb2.SparkSchema
    def __init__(self, batchSchema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., streamSchema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...
