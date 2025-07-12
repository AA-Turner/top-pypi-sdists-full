import binascii
import os
import re
import zlib
from functools import wraps
from typing import List
from typing import Optional

import pyspark
from google.protobuf.empty_pb2 import Empty

from tecton_core import errors as tecton_core_errors
from tecton_core import function_deserialization
from tecton_core import specs
from tecton_materialization.materialization import _parse_bucket_key_from_uri
from tecton_proto.common import data_type__client_pb2 as data_type_pb2
from tecton_proto.common.schema__client_pb2 import Schema as SchemaProto
from tecton_proto.common.spark_schema__client_pb2 import SparkSchema
from tecton_proto.data.hive_metastore__client_pb2 import ListHiveResult
from tecton_proto.data.remote_spark__client_pb2 import ExecuteRequest
from tecton_proto.data.remote_spark__client_pb2 import ExecuteResult
from tecton_proto.data.remote_spark__client_pb2 import FeatureViewSchemaResponse
from tecton_proto.data.remote_spark__client_pb2 import GetBatchDataSourceFunctionSchema
from tecton_proto.data.remote_spark__client_pb2 import GetFeatureViewSchema
from tecton_proto.data.remote_spark__client_pb2 import GetFileSourceSchema
from tecton_proto.data.remote_spark__client_pb2 import GetHiveTableSchema
from tecton_proto.data.remote_spark__client_pb2 import GetKafkaSourceSchema
from tecton_proto.data.remote_spark__client_pb2 import GetKinesisSourceSchema
from tecton_proto.data.remote_spark__client_pb2 import GetMultipleDataSourceSchemasRequest
from tecton_proto.data.remote_spark__client_pb2 import GetMultipleDataSourceSchemasResponse
from tecton_proto.data.remote_spark__client_pb2 import GetMultipleFeatureViewSchemasRequest
from tecton_proto.data.remote_spark__client_pb2 import GetMultipleFeatureViewSchemasResponse
from tecton_proto.data.remote_spark__client_pb2 import GetQueryPlanInfoForFeatureViewPipeline
from tecton_proto.data.remote_spark__client_pb2 import GetRedshiftTableSchema
from tecton_proto.data.remote_spark__client_pb2 import GetSnowflakeSchema
from tecton_proto.data.remote_spark__client_pb2 import GetStreamDataSourceFunctionSchema
from tecton_proto.data.remote_spark__client_pb2 import GetUnityTableSchema
from tecton_proto.data.remote_spark__client_pb2 import ListHiveDatabases
from tecton_proto.data.remote_spark__client_pb2 import ListHiveTableColumns
from tecton_proto.data.remote_spark__client_pb2 import ListHiveTables
from tecton_proto.data.remote_spark__client_pb2 import QueryPlanInfo
from tecton_proto.data.remote_spark__client_pb2 import SparkSchemas
from tecton_proto.data.virtual_data_source__client_pb2 import VirtualDataSource
from tecton_spark import schema_derivation_utils
from tecton_spark.spark_helper import get_query_plan_info_for_df
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


# Return raw Spark exceptions as strings to avoid py4j wrapping that obfuscates the root cause
def exception_catching_wrapper(func):
    @wraps(func)
    def _exception_catching_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pyspark.sql.utils.CapturedException as e:
            msg = e.desc if e.desc else str(e)
            return msg

    return _exception_catching_wrapper


# TODO(rafael): We should move this to a `fs_utils` module at some point and collect any related functionality there.
def _write_to_path(path: str, content: str) -> None:
    if path.startswith("s3://"):
        import boto3  # import here since this is not always available, but should if path is S3

        # NOTE(rafael): This will inherit whatever default access the current role has.
        s3 = boto3.resource("s3")
        bucket_name, key = _parse_bucket_key_from_uri(path)
        s3.Object(bucket_name, key).put(Body=content)
    elif path.startswith("dbfs:/"):
        path = re.sub("^dbfs:/", "/dbfs/", path)
        # create directory if it does not exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fid:
            fid.write(content)
    else:
        msg = f"'{path}' is not of supported type"
        raise ValueError(msg)


class PysparkRemoteHost(object):
    def __init__(self, spark_session):
        # A way for users to implement custom logic like our built-in schema_uri functionality for datasource-functions.
        os.environ["_TECTON_SCHEMA_DERIVATION"] = "1"
        self.executions_map = {
            "getHiveTableSchema": lambda r: self._getHiveTableSchema(r.getHiveTableSchema),
            "getUnityTableSchema": lambda r: self._getUnityTableSchema(r.getUnityTableSchema),
            "getRedshiftTableSchema": lambda r: self._getRedshiftTableSchema(r.getRedshiftTableSchema),
            "getSnowflakeSchema": lambda r: self._getSnowflakeSchema(r.getSnowflakeSchema),
            "getFileSourceSchema": lambda r: self._getFileDataSourceSchema(r.getFileSourceSchema),
            "getBatchDataSourceFunctionSchema": lambda r: self._getBatchDataSourceFunctionSchema(
                r.getBatchDataSourceFunctionSchema
            ),
            "getStreamDataSourceFunctionSchema": lambda r: self._getStreamDataSourceFunctionSchema(
                r.getStreamDataSourceFunctionSchema
            ),
            "getKinesisSourceSchema": lambda r: self._getKinesisDataSourceSchema(r.getKinesisSourceSchema),
            "getKafkaSourceSchema": lambda r: self._getKafkaDataSourceSchema(r.getKafkaSourceSchema),
            "getFeatureViewSchema": lambda r: self._getFeatureViewSchema(r.getFeatureViewSchema),
            "getMultipleFeatureViewSchemasRequest": lambda r: self._getMultipleFeatureViewSchemasRequest(
                r.getMultipleFeatureViewSchemasRequest
            ),
            "getMultipleDataSourceSchemasRequest": lambda r: self._getMultipleDataSourceSchemasRequest(
                r.getMultipleDataSourceSchemasRequest
            ),
            "getQueryPlanInfoForFeatureViewPipeline": lambda r: self._getQueryPlanInfoForFeatureViewPipeline(
                r.getQueryPlanInfoForFeatureViewPipeline
            ),
            "listHiveDatabases": lambda r: self._listHiveDatabases(r.listHiveDatabases),
            "listHiveTables": lambda r: self._listHiveTables(r.listHiveTables),
            "listHiveTableColumns": lambda r: self._listHiveTableColumns(r.listHiveTableColumns),
        }

        self.spark = spark_session

    def _getHiveTableSchema(self, request: GetHiveTableSchema) -> SparkSchema:
        if request.HasField("rawBatchTranslator"):
            post_processor = function_deserialization.from_proto(
                request.rawBatchTranslator, include_main_variable_in_scope=True
            )
        else:
            post_processor = None

        return schema_derivation_utils.get_hive_table_schema(
            spark=self.spark,
            database=request.database,
            table=request.table,
            post_processor=post_processor,
            timestamp_field=request.timestampColumn,
            timestamp_format=request.timestampFormat,
        )

    def _getUnityTableSchema(self, request: GetUnityTableSchema) -> SparkSchema:
        if request.HasField("rawBatchTranslator"):
            post_processor = function_deserialization.from_proto(
                request.rawBatchTranslator, include_main_variable_in_scope=True
            )
        else:
            post_processor = None

        return schema_derivation_utils.get_unity_table_schema(
            spark=self.spark,
            catalog=request.catalog,
            schema=request.schema,
            table=request.table,
            post_processor=post_processor,
            timestamp_field=request.timestampColumn,
            timestamp_format=request.timestampFormat,
        )

    def _getBatchDataSourceFunctionSchema(self, request: GetBatchDataSourceFunctionSchema) -> SparkSchema:
        data_source_fn = function_deserialization.from_proto(request.function, include_main_variable_in_scope=True)
        return schema_derivation_utils.get_batch_data_source_function_schema(
            spark=self.spark,
            data_source_function=data_source_fn,
            supports_time_filtering=request.supports_time_filtering,
        )

    def _getStreamDataSourceFunctionSchema(self, request: GetStreamDataSourceFunctionSchema) -> SparkSchema:
        data_source_fn = function_deserialization.from_proto(request.function, include_main_variable_in_scope=True)
        return schema_derivation_utils.get_stream_data_source_function_schema(self.spark, data_source_fn)

    def _getRedshiftTableSchema(self, request: GetRedshiftTableSchema) -> SparkSchema:
        assert request.HasField("endpoint") and request.endpoint, "endpoint cannot be None"
        assert request.HasField("temp_s3_dir") and request.temp_s3_dir, "temp_s3_dir cannot be None"

        assert (request.HasField("table") and request.table) or (request.HasField("query") and request.query), (
            "Both table and query cannot be None"
        )
        if request.HasField("rawBatchTranslator"):
            post_processor = function_deserialization.from_proto(
                request.rawBatchTranslator, include_main_variable_in_scope=True
            )
        else:
            post_processor = None
        return schema_derivation_utils.get_redshift_table_schema(
            spark=self.spark,
            endpoint=request.endpoint,
            table=request.table,
            query=request.query,
            temp_s3=request.temp_s3_dir,
            post_processor=post_processor,
        )

    def _getSnowflakeSchema(self, request: GetSnowflakeSchema) -> SparkSchema:
        assert request.HasField("url"), "url cannot be None"
        assert request.HasField("database"), "database cannot be None"
        assert request.HasField("schema"), "schema cannot be None"
        assert request.HasField("warehouse"), "warehouse cannot be None"

        if request.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(
                request.post_processor, include_main_variable_in_scope=True
            )
        else:
            post_processor = None

        return schema_derivation_utils.get_snowflake_schema(
            spark=self.spark,
            url=request.url,
            database=request.database,
            schema=request.schema,
            warehouse=request.warehouse,
            role=request.role if request.HasField("role") else None,
            table=request.table if request.HasField("table") else None,
            query=request.query if request.HasField("query") else None,
            post_processor=post_processor,
        )

    def _getFileDataSourceSchema(self, request: GetFileSourceSchema) -> SparkSchema:
        schema_override = None
        if request.HasField("schemaOverride"):
            schema_override = SparkSchemaWrapper.from_proto(request.schemaOverride)

        post_processor = None
        if request.HasField("rawBatchTranslator"):
            post_processor = function_deserialization.from_proto(
                request.rawBatchTranslator, include_main_variable_in_scope=True
            )

        return schema_derivation_utils.get_file_source_schema(
            spark=self.spark,
            file_format=request.fileFormat,
            file_uri=request.uri,
            convert_to_glue=request.convertToGlueFormat,
            schema_uri=request.schemaUri if request.HasField("schemaUri") else None,
            schema_override=schema_override,
            post_processor=post_processor,
            timestamp_col=request.timestampColumn if request.HasField("timestampColumn") else None,
            timestmap_format=request.timestampFormat if request.HasField("timestampFormat") else None,
        )

    def _getKinesisDataSourceSchema(self, request: GetKinesisSourceSchema) -> SparkSchema:
        translator_fn = function_deserialization.from_proto(
            request.rawStreamTranslator, include_main_variable_in_scope=True
        )
        return schema_derivation_utils.get_kinesis_schema(self.spark, request.streamName, translator_fn)

    def _getKafkaDataSourceSchema(self, request: GetKafkaSourceSchema) -> SparkSchema:
        translator_fn = function_deserialization.from_proto(
            request.rawStreamTranslator, include_main_variable_in_scope=True
        )
        return schema_derivation_utils.get_kafka_schema(self.spark, translator_fn)

    @classmethod
    def deserialize_virtual_data_sources(cls, virtual_data_sources_bin: List[bytes]) -> List[VirtualDataSource]:
        data_sources = []
        for bstr in virtual_data_sources_bin:
            data_source = VirtualDataSource()
            data_source.ParseFromString(bstr)
            data_sources.append(data_source)
        return data_sources

    def _getMultipleDataSourceSchemasRequest(
        self, request: GetMultipleDataSourceSchemasRequest
    ) -> GetMultipleDataSourceSchemasResponse:
        batched_responses = GetMultipleDataSourceSchemasResponse()
        for ds in request.data_source_args:
            response = SparkSchemas()
            # Create a spec to leverage its unified interface. (Usually specs are only created from fully validated args with derived schemas.)
            spec = specs.DataSourceSpec.from_args_proto(
                ds,
                specs.DataSourceSpecArgsSupplement(
                    # The spec constructor expects a non-null schema
                    batch_schema=SparkSchema(),
                    stream_schema=SparkSchema(),
                ),
            )
            if spec.batch_source is not None:
                response.batchSchema.CopyFrom(
                    schema_derivation_utils.derive_batch_schema(
                        self.spark,
                        ds,
                        getattr(spec.batch_source, "post_processor", None),
                        getattr(spec.batch_source, "function", None),
                    )
                )
            if spec.stream_source is not None:
                response.streamSchema.CopyFrom(
                    schema_derivation_utils.derive_stream_schema(
                        self.spark,
                        ds,
                        getattr(spec.stream_source, "post_processor", None),
                        getattr(spec.stream_source, "function", None),
                    )
                )
            batched_responses.data_source_responses[ds.info.name].CopyFrom(response)
        return batched_responses

    def _getMultipleFeatureViewSchemasRequest(
        self, request: GetMultipleFeatureViewSchemasRequest
    ) -> GetMultipleFeatureViewSchemasResponse:
        data_source_specs = [
            specs.DataSourceSpec.from_data_proto(ds, include_main_variables_in_scope=True)
            for ds in request.virtual_data_sources
        ]
        transformation_specs = [
            specs.TransformationSpec.from_data_proto(t, include_main_variables_in_scope=True)
            for t in request.transformations
        ]
        batched_responses = GetMultipleFeatureViewSchemasResponse()
        for fv_request in request.feature_view_requests:
            response = FeatureViewSchemaResponse()
            response.view_schema.CopyFrom(
                schema_derivation_utils.get_feature_view_view_schema(
                    self.spark,
                    fv_request.feature_view,
                    transformation_specs,
                    data_source_specs,
                )
            )
            timestamp_keys = [
                c.name
                for c in response.view_schema.columns
                if c.offline_data_type.type == data_type_pb2.DATA_TYPE_TIMESTAMP
            ]
            if len(timestamp_keys) != 1:
                msg = f"Expected single timestamp column for Feature View {fv_request.feature_view.info.name}. Found {timestamp_keys}"
                raise tecton_core_errors.TectonValidationError(msg)
            else:
                response.timestamp_key = timestamp_keys[0]
            batched_responses.feature_view_responses[fv_request.feature_view.info.name].CopyFrom(response)
        return batched_responses

    def _getFeatureViewSchema(self, request: GetFeatureViewSchema) -> SchemaProto:
        data_source_specs = [
            specs.DataSourceSpec.from_data_proto(ds, include_main_variables_in_scope=True)
            for ds in request.virtual_data_sources
        ]
        transformation_specs = [
            specs.TransformationSpec.from_data_proto(t, include_main_variables_in_scope=True)
            for t in request.transformations
        ]
        return schema_derivation_utils.get_feature_view_view_schema(
            self.spark, request.feature_view, transformation_specs, data_source_specs
        )

    def _getQueryPlanInfoForFeatureViewPipeline(self, request: GetQueryPlanInfoForFeatureViewPipeline) -> QueryPlanInfo:
        data_source_specs = [
            specs.DataSourceSpec.from_data_proto(ds, include_main_variables_in_scope=True)
            for ds in request.virtual_data_sources
        ]
        transformation_specs = [
            specs.TransformationSpec.from_data_proto(t, include_main_variables_in_scope=True)
            for t in request.transformations
        ]
        df = schema_derivation_utils.get_feature_view_empty_view_df(
            self.spark, request.feature_view, transformation_specs, data_source_specs
        )

        query_plan = get_query_plan_info_for_df(df)

        return QueryPlanInfo(
            has_joins=query_plan.has_joins,
            has_aggregations=query_plan.has_aggregations,
        )

    def _listHiveDatabases(self, request: ListHiveDatabases) -> ListHiveResult:
        spark_sql = self.spark.sql("SHOW DATABASES")
        return ListHiveResult(names=[row["databaseName"] for row in spark_sql.collect()])

    def _listHiveTables(self, request: ListHiveTables) -> ListHiveResult:
        spark_sql = self.spark.sql(f"SHOW TABLES FROM `{request.database}`")
        return ListHiveResult(names=[row["tableName"] for row in spark_sql.collect()])

    def _listHiveTableColumns(self, request: ListHiveTableColumns) -> ListHiveResult:
        spark_sql = self.spark.sql(f"DESCRIBE {request.database}.{request.table}")
        return ListHiveResult(names=[row["col_name"] for row in spark_sql.collect()])

    def execute(self, request: str, output_path: Optional[str] = None) -> Optional[str]:
        request_bytes = binascii.unhexlify(request)
        execute_request = ExecuteRequest()
        execute_request.ParseFromString(request_bytes)

        request_type = execute_request.WhichOneof("request")
        if request_type is None:
            execute_result = ExecuteResult()
            execute_result.errorMessage = "Missing request in ExecuteRequest message"
            return str(binascii.b2a_base64(execute_result.SerializeToString()).rstrip())

        try:
            for k, v in execute_request.envVars.items():
                os.environ[k] = v
            handler = self.executions_map[request_type]
            resp = handler(execute_request)
            result = self._serialize_response(resp)
        except tecton_core_errors.TectonValidationError as e:
            result = ExecuteResult()
            result.validationError = str(e)
        except pyspark.sql.utils.CapturedException as e:
            import traceback

            result = ExecuteResult()
            result.uncaughtError = (
                e.desc if e.desc else "".join(traceback.TracebackException.from_exception(e).format())
            )
        except Exception as e:
            import traceback

            result = ExecuteResult()
            result.uncaughtError = "".join(traceback.TracebackException.from_exception(e).format())

        resp = str(binascii.b2a_base64(zlib.compress(result.SerializeToString())).rstrip())
        if output_path is None:
            return resp
        else:
            _write_to_path(path=output_path, content=resp)

    @staticmethod
    def _serialize_response(result) -> ExecuteResult:
        if isinstance(result, Empty):
            return ExecuteResult()
        elif isinstance(result, SparkSchema):
            return ExecuteResult(sparkSchema=result)
        elif isinstance(result, QueryPlanInfo):
            return ExecuteResult(queryPlanInfo=result)
        elif isinstance(result, SchemaProto):
            return ExecuteResult(schema=result)
        elif isinstance(result, ListHiveResult):
            return ExecuteResult(listHiveResult=result)
        elif isinstance(result, GetMultipleFeatureViewSchemasResponse):
            return ExecuteResult(multipleFeatureViewSchemaResponse=result)
        elif isinstance(result, GetMultipleDataSourceSchemasResponse):
            return ExecuteResult(multipleDataSourceSchemaResponse=result)
        msg = f"Unidentified return type: ${type(result)}"
        raise Exception(msg)
