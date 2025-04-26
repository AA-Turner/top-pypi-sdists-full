import datetime as dt
import json
from typing import Any, Dict, List, Optional, Union

from google.protobuf import message as proto_message

from chalk._gen.chalk.common.v1 import chalk_error_pb2, online_query_pb2
from chalk.client import ChalkError, ChalkException, ErrorCode, ErrorCodeCategory, OnlineQueryContext, QueryMeta
from chalk.client._internal_models.models import INDEX_COL_NAME, OBSERVED_AT_COL_NAME, PKEY_COL_NAME, TS_COL_NAME
from chalk.client.models import (
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    BulkUploadFeaturesResult,
    FeatureResolutionMeta,
    FeatureResult,
    OnlineQueryManyRequest,
    OnlineQueryRequest,
    OnlineQueryResponse,
    OnlineQueryResultFeather,
)
from chalk.client.serialization.constants import GRPC_RESULT_METADATA_COL_PREFIX
from chalk.features._encoding.converter import PrimitiveFeatureConverter
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.parsed._proto.utils import (
    datetime_to_proto_timestamp,
    proto_duration_to_timedelta,
    proto_value_to_python,
    seconds_to_proto_duration,
    value_to_proto,
)
from chalk.utils.collections import BidirectionalMap
from chalk.utils.df_utils import arrow_ipc_to_record_batch, pa_table_to_pl_df, record_batch_to_arrow_ipc


def check_has_field(proto: proto_message.Message, field: str):
    if not proto.HasField(field):
        raise ValueError(f"Proto is missing expected field '{field}'.")


def get_field_or(proto: proto_message.Message, field_name: str, default_value: Any = None):
    if not proto.HasField(field_name):
        return default_value
    return getattr(proto, field_name)


class ChalkErrorConverter:
    _error_code_map: "BidirectionalMap[ErrorCode, chalk_error_pb2.ErrorCode]" = BidirectionalMap(
        [
            (ErrorCode.INTERNAL_SERVER_ERROR, chalk_error_pb2.ERROR_CODE_INTERNAL_SERVER_ERROR_UNSPECIFIED),
            (ErrorCode.PARSE_FAILED, chalk_error_pb2.ERROR_CODE_PARSE_FAILED),
            (ErrorCode.RESOLVER_NOT_FOUND, chalk_error_pb2.ERROR_CODE_RESOLVER_NOT_FOUND),
            (ErrorCode.INVALID_QUERY, chalk_error_pb2.ERROR_CODE_INVALID_QUERY),
            (ErrorCode.VALIDATION_FAILED, chalk_error_pb2.ERROR_CODE_VALIDATION_FAILED),
            (ErrorCode.RESOLVER_FAILED, chalk_error_pb2.ERROR_CODE_RESOLVER_FAILED),
            (ErrorCode.RESOLVER_TIMED_OUT, chalk_error_pb2.ERROR_CODE_RESOLVER_TIMED_OUT),
            (ErrorCode.UPSTREAM_FAILED, chalk_error_pb2.ERROR_CODE_UPSTREAM_FAILED),
            (ErrorCode.UNAUTHENTICATED, chalk_error_pb2.ERROR_CODE_UNAUTHENTICATED),
            (ErrorCode.UNAUTHORIZED, chalk_error_pb2.ERROR_CODE_UNAUTHORIZED),
            (ErrorCode.CANCELLED, chalk_error_pb2.ERROR_CODE_CANCELLED),
            (ErrorCode.DEADLINE_EXCEEDED, chalk_error_pb2.ERROR_CODE_DEADLINE_EXCEEDED),
        ]
    )

    _error_category_map: "BidirectionalMap[ErrorCodeCategory, chalk_error_pb2.ErrorCodeCategory]" = BidirectionalMap(
        [
            (ErrorCodeCategory.NETWORK, chalk_error_pb2.ERROR_CODE_CATEGORY_NETWORK_UNSPECIFIED),
            (ErrorCodeCategory.FIELD, chalk_error_pb2.ERROR_CODE_CATEGORY_FIELD),
            (ErrorCodeCategory.REQUEST, chalk_error_pb2.ERROR_CODE_CATEGORY_REQUEST),
        ]
    )

    @staticmethod
    def _chalk_error_code_encode(
        error_code: ErrorCode,
    ) -> chalk_error_pb2.ErrorCode:
        code_proto: Optional[chalk_error_pb2.ErrorCode] = ChalkErrorConverter._error_code_map.get(error_code)
        if code_proto is None:
            raise ValueError(f"Unrecognized error code: {error_code}")
        else:
            return code_proto

    @staticmethod
    def _chalk_error_code_decode(
        error_code_proto: chalk_error_pb2.ErrorCode,
    ) -> ErrorCode:
        code_py: Optional[ErrorCode] = ChalkErrorConverter._error_code_map.get_reverse(error_code_proto)
        if code_py is None:
            raise ValueError(f"Unrecognized error code protobuf: {error_code_proto}")
        else:
            return code_py

    @staticmethod
    def _chalk_error_code_category_encode(
        category_py: ErrorCodeCategory,
    ) -> chalk_error_pb2.ErrorCodeCategory:
        category_proto: Optional[chalk_error_pb2.ErrorCodeCategory] = ChalkErrorConverter._error_category_map.get(
            category_py
        )
        if category_proto is None:
            raise ValueError(f"Unrecognized error code: {category_proto}")
        else:
            return category_proto

    @staticmethod
    def _chalk_error_code_category_decode(
        category_proto: chalk_error_pb2.ErrorCodeCategory,
    ) -> ErrorCodeCategory:
        category_py: Optional[ErrorCodeCategory] = ChalkErrorConverter._error_category_map.get_reverse(category_proto)
        if category_py is None:
            raise ValueError(f"Unrecognized error code: {category_proto}")
        else:
            return category_py

    @staticmethod
    def chalk_exception_encode(
        exception: ChalkException,
    ) -> chalk_error_pb2.ChalkException:
        proto_exception = chalk_error_pb2.ChalkException()
        proto_exception.kind = exception.kind
        proto_exception.message = exception.message
        proto_exception.stacktrace = exception.stacktrace
        if exception.internal_stacktrace is not None:
            proto_exception.internal_stacktrace = exception.internal_stacktrace
        return proto_exception

    @staticmethod
    def chalk_exception_decode(exception_proto: chalk_error_pb2.ChalkException) -> ChalkException:
        return ChalkException(
            kind=exception_proto.kind,
            message=exception_proto.message,
            stacktrace=exception_proto.stacktrace,
            internal_stacktrace=exception_proto.internal_stacktrace or None,
        )

    @staticmethod
    def chalk_error_encode(
        error: ChalkError,
    ) -> chalk_error_pb2.ChalkError:
        proto_error = chalk_error_pb2.ChalkError()
        proto_error.code = ChalkErrorConverter._chalk_error_code_encode(error.code)
        proto_error.category = ChalkErrorConverter._chalk_error_code_category_encode(error.category)
        proto_error.message = error.message
        if error.display_primary_key:
            proto_error.display_primary_key = error.display_primary_key
        if error.display_primary_key_fqn:
            proto_error.display_primary_key_fqn = error.display_primary_key_fqn
        if error.exception:
            proto_error.exception.CopyFrom(ChalkErrorConverter.chalk_exception_encode(error.exception))
        if error.feature:
            proto_error.feature = error.feature
        if error.resolver:
            proto_error.resolver = error.resolver
        return proto_error

    @staticmethod
    def chalk_error_decode(
        error_proto: chalk_error_pb2.ChalkError,
    ) -> ChalkError:
        if error_proto.HasField("exception"):
            chalk_exception = ChalkErrorConverter.chalk_exception_decode(error_proto.exception)
        else:
            chalk_exception = None
        return ChalkError(
            code=ChalkErrorConverter._chalk_error_code_decode(error_proto.code),
            category=ChalkErrorConverter._chalk_error_code_category_decode(error_proto.category),
            message=error_proto.message,
            display_primary_key=get_field_or(error_proto, "display_primary_key", None),
            display_primary_key_fqn=get_field_or(error_proto, "display_primary_key_fqn", None),
            exception=chalk_exception,
            feature=get_field_or(error_proto, "feature", None),
            resolver=get_field_or(error_proto, "resolver", None),
        )


class UploadFeaturesBulkConverter:
    @staticmethod
    def upload_features_bulk_response_decode(
        response_proto: online_query_pb2.UploadFeaturesBulkResponse, trace_id: Optional[str]
    ) -> BulkUploadFeaturesResult:
        return BulkUploadFeaturesResult(
            errors=[ChalkErrorConverter.chalk_error_decode(e) for e in response_proto.errors],
            trace_id=trace_id,
        )


class OnlineQueryConverter:
    @staticmethod
    def _options_bool_field(online_query_context: online_query_pb2.OnlineQueryContext, field: str) -> Optional[bool]:
        unacceptable_has_fields = ("number_value", "string_value", "struct_value", "list_value")
        value = online_query_context.options[field]
        if value.HasField("null_value"):
            return None
        for fieldx in unacceptable_has_fields:
            if value.HasField(fieldx):
                raise ValueError(f"Expected bool_value in online_query_context.options.{field}, got {fieldx}")
        return value.bool_value

    @staticmethod
    def _online_query_context_decode(
        online_query_context: online_query_pb2.OnlineQueryContext,
    ) -> OnlineQueryContext:
        # Note that the proto online query context tends to differ from the python model. This function needs
        # frequent updates as more stuff gets moved into the python OnlineQueryContext
        return OnlineQueryContext(
            environment=online_query_context.environment,
            tags=[tag for tag in online_query_context.tags],
            required_resolver_tags=[tag for tag in online_query_context.required_resolver_tags],
        )

    @staticmethod
    def _feature_encoding_options_decode(
        feature_encoding_options: online_query_pb2.FeatureEncodingOptions,
    ) -> FeatureEncodingOptions:
        return FeatureEncodingOptions(
            encode_structs_as_objects=feature_encoding_options.encode_structs_as_objects,
        )

    @staticmethod
    def _query_meta_encode(query_meta: QueryMeta) -> online_query_pb2.OnlineQueryMetadata:
        proto_metadata = online_query_pb2.OnlineQueryMetadata()
        proto_metadata.execution_duration.CopyFrom(seconds_to_proto_duration(query_meta.execution_duration_s))
        if query_meta.deployment_id is not None:
            proto_metadata.deployment_id = query_meta.deployment_id
        if query_meta.environment_id is not None:
            proto_metadata.environment_id = query_meta.environment_id
        if query_meta.environment_name is not None:
            proto_metadata.environment_name = query_meta.environment_name
        if query_meta.query_id is not None:
            proto_metadata.query_id = query_meta.query_id
        if query_meta.query_timestamp is not None:
            proto_metadata.query_timestamp.CopyFrom(datetime_to_proto_timestamp(query_meta.query_timestamp))
        if query_meta.query_hash is not None:
            proto_metadata.query_hash = query_meta.query_hash
        if query_meta.explain_output is not None:
            proto_metadata.explain_output.CopyFrom(
                online_query_pb2.QueryExplainInfo(plan_string=query_meta.explain_output)
            )
        return proto_metadata

    @staticmethod
    def _query_meta_decode(meta_proto: online_query_pb2.OnlineQueryMetadata) -> QueryMeta:
        check_has_field(meta_proto, "execution_duration")
        execution_duration = proto_duration_to_timedelta(meta_proto.execution_duration)
        return QueryMeta(
            execution_duration_s=execution_duration.total_seconds(),
            deployment_id=meta_proto.deployment_id,
            environment_id=meta_proto.environment_id,
            environment_name=meta_proto.environment_name,
            query_id=meta_proto.query_id,
            query_timestamp=meta_proto.query_timestamp.ToDatetime(tzinfo=dt.timezone.utc)
            if meta_proto.HasField("query_timestamp")
            else None,
            query_hash=meta_proto.query_hash,
            explain_output=get_field_or(meta_proto.explain_output, "plan_string"),
        )

    @staticmethod
    def online_query_request_decode(
        online_query_request: online_query_pb2.OnlineQueryRequest,
    ) -> OnlineQueryRequest:
        now_str: Optional[str] = None
        if online_query_request.HasField("now"):
            now_dt: dt.datetime = online_query_request.now.ToDatetime()
            now_str = now_dt.astimezone(tz=dt.timezone.utc).isoformat()
        return OnlineQueryRequest(
            inputs={k: proto_value_to_python(v) for k, v in online_query_request.inputs.items()},
            outputs=[output_expr.feature_fqn for output_expr in online_query_request.outputs],
            now=now_str,
            staleness={k: v for k, v in online_query_request.staleness.items()},
            context=OnlineQueryConverter._online_query_context_decode(online_query_request.context),
            include_meta=online_query_request.response_options.include_meta,
            explain=online_query_request.response_options.HasField("explain"),
            skip_online_storage=OnlineQueryConverter._options_bool_field(
                online_query_request.context, "skip_online_storage"
            ),
            skip_offline_storage=OnlineQueryConverter._options_bool_field(
                online_query_request.context, "skip_offline_storage"
            ),
            skip_metrics_storage=OnlineQueryConverter._options_bool_field(
                online_query_request.context, "skip_metrics_storage"
            ),
            correlation_id=online_query_request.context.correlation_id,
            query_name=online_query_request.context.query_name,
            query_name_version=online_query_request.context.query_name_version,
            deployment_id=online_query_request.context.deployment_id,
            branch_id=online_query_request.context.branch_id,
            meta={k: v for k, v in online_query_request.response_options.metadata.items()},
            store_plan_stages=OnlineQueryConverter._options_bool_field(
                online_query_request.context, "store_plan_stages"
            )
            or False,
            encoding_options=OnlineQueryConverter._feature_encoding_options_decode(
                online_query_request.response_options.encoding_options
            ),
            planner_options=None,  # for now
        )

    @staticmethod
    def online_query_context_encode(
        request: Union[OnlineQueryRequest, OnlineQueryManyRequest], options: Dict[str, Any]
    ):
        if request.context is None:
            raise ValueError("Given request object has no OnlineQueryContext.")
        context_options_proto = {k: value_to_proto(v) for k, v in options.items()}
        return online_query_pb2.OnlineQueryContext(
            environment=request.context.environment,
            tags=request.context.tags,
            required_resolver_tags=request.context.required_resolver_tags,
            deployment_id=request.deployment_id,
            branch_id=request.branch_id,
            correlation_id=request.correlation_id,
            query_name=request.query_name,
            query_name_version=request.query_name_version,
            options=context_options_proto,
        )

    @staticmethod
    def online_query_request_encode(request: OnlineQueryRequest) -> online_query_pb2.OnlineQueryRequest:
        inputs_proto = {k: value_to_proto(v) for k, v in request.inputs.items()}
        # TODO -- eventually we'll have more complex structured output expressions
        outputs_proto = [online_query_pb2.OutputExpr(feature_fqn=o) for o in request.outputs]
        now_proto = None
        if request.now is not None:
            now_proto = datetime_to_proto_timestamp(dt.datetime.fromisoformat(request.now))
        context_options_dict: Dict[str, Any] = {
            "skip_online_storage": request.skip_online_storage,
            "skip_offline_storage": request.skip_offline_storage,
            "skip_metrics_storage": request.skip_metrics_storage,
            "store_plan_stages": request.store_plan_stages,
        }
        context_options_dict.update(**(request.planner_options or {}))
        context_proto = OnlineQueryConverter.online_query_context_encode(request, options=context_options_dict)
        return online_query_pb2.OnlineQueryRequest(
            inputs=inputs_proto,
            outputs=outputs_proto,
            staleness=request.staleness,
            now=now_proto,
            context=context_proto,
            response_options=online_query_pb2.OnlineQueryResponseOptions(
                include_meta=request.include_meta,
                explain=online_query_pb2.ExplainOptions() if request.explain else None,
                encoding_options=online_query_pb2.FeatureEncodingOptions(
                    encode_structs_as_objects=request.encoding_options.encode_structs_as_objects
                ),
                metadata=request.meta,
            ),
        )

    @staticmethod
    def online_query_request_feather_encode(
        request: OnlineQueryManyRequest,
    ) -> online_query_pb2.OnlineQueryBulkRequest:
        import pyarrow as pa

        rb = pa.RecordBatch.from_pydict(request.inputs)
        inputs_bytes = record_batch_to_arrow_ipc(rb)
        outputs = [online_query_pb2.OutputExpr(feature_fqn=o) for o in request.outputs]
        now_proto = None
        if request.now is not None:
            now_proto = [datetime_to_proto_timestamp(dt.datetime.fromisoformat(n)) for n in request.now]
        context_options_dict = {
            "skip_online_storage": request.skip_online_storage,
            "skip_offline_storage": request.skip_offline_storage,
            "skip_metrics_storage": request.skip_metrics_storage,
            "store_plan_stages": request.store_plan_stages,
            "planner_version": "2",  # TODO remove this
        }
        context_proto = OnlineQueryConverter.online_query_context_encode(request, options=context_options_dict)
        return online_query_pb2.OnlineQueryBulkRequest(
            inputs_feather=inputs_bytes,
            outputs=outputs,
            staleness=request.staleness,
            now=now_proto,
            context=context_proto,
            response_options=online_query_pb2.OnlineQueryResponseOptions(
                include_meta=request.include_meta,
                explain=online_query_pb2.ExplainOptions() if request.explain else None,
                encoding_options=online_query_pb2.FeatureEncodingOptions(
                    encode_structs_as_objects=request.encoding_options.encode_structs_as_objects
                ),
                metadata=request.meta,
            ),
        )

    @staticmethod
    def _feature_meta_encode(feature_meta: FeatureResolutionMeta) -> online_query_pb2.FeatureMeta:
        return online_query_pb2.FeatureMeta(
            chosen_resolver_fqn=feature_meta.chosen_resolver_fqn,
            cache_hit=feature_meta.cache_hit,
            primitive_type=feature_meta.primitive_type,
            version=feature_meta.version,
        )

    @staticmethod
    def _feature_result_encode(feature_result: FeatureResult) -> online_query_pb2.FeatureResult:
        feature_result_proto = online_query_pb2.FeatureResult(
            field=feature_result.field,
        )
        feature_result_proto.value.CopyFrom(value_to_proto(feature_result.value))
        if feature_result.error:
            feature_result_proto.error.CopyFrom(ChalkErrorConverter.chalk_error_encode(feature_result.error))
        if feature_result.ts:
            feature_result_proto.ts.CopyFrom(datetime_to_proto_timestamp(feature_result.ts))
        if feature_result.meta:
            feature_result_proto.meta.CopyFrom(OnlineQueryConverter._feature_meta_encode(feature_result.meta))
        return feature_result_proto

    @staticmethod
    def _feature_result_decode(proto: online_query_pb2.FeatureResult) -> FeatureResult:
        return FeatureResult(
            field=proto.field,
            value=proto_value_to_python(proto.value),
            pkey=proto_value_to_python(proto.pkey),
            error=ChalkErrorConverter.chalk_error_decode(proto.error) if proto.HasField("error") else None,
            ts=proto.ts.ToDatetime(tzinfo=dt.timezone.utc) if proto.HasField("ts") else None,
            meta=FeatureResolutionMeta(
                chosen_resolver_fqn=proto.meta.chosen_resolver_fqn,
                cache_hit=proto.meta.cache_hit,
                primitive_type=proto.meta.primitive_type,
                version=proto.meta.version,
            )
            if proto.HasField("meta")
            else None,
        )

    @staticmethod
    def _online_query_result_decode(result_proto: online_query_pb2.OnlineQueryResult) -> List[FeatureResult]:
        results_py = []
        for fr_proto in result_proto.results:
            results_py.append(OnlineQueryConverter._feature_result_decode(fr_proto))
        return results_py

    @staticmethod
    def online_query_response_encode(
        online_query_result: OnlineQueryResponse,
    ) -> online_query_pb2.OnlineQueryResponse:
        proto_response = online_query_pb2.OnlineQueryResponse()
        proto_response.data.results.extend(
            [OnlineQueryConverter._feature_result_encode(fr) for fr in online_query_result.data]
        )
        if online_query_result.errors:
            proto_response.errors.extend(
                [ChalkErrorConverter.chalk_error_encode(e) for e in online_query_result.errors]
            )
        if online_query_result.meta:
            proto_response.response_meta.CopyFrom(OnlineQueryConverter._query_meta_encode(online_query_result.meta))
        return proto_response

    @staticmethod
    def online_query_response_decode(response_proto: online_query_pb2.OnlineQueryResponse) -> OnlineQueryResponse:
        data = []
        errors = []
        meta = None
        if response_proto.HasField("data"):
            data = OnlineQueryConverter._online_query_result_decode(response_proto.data)
        for err_proto in response_proto.errors:
            errors.append(ChalkErrorConverter.chalk_error_decode(err_proto))
        if response_proto.HasField("response_meta"):
            meta = OnlineQueryConverter._query_meta_decode(response_proto.response_meta)
        return OnlineQueryResponse(
            data=data,
            errors=errors,
            meta=meta,
        )

    @staticmethod
    def online_query_bulk_response_decode_to_single(
        response_proto: online_query_pb2.OnlineQueryBulkResponse,
    ) -> OnlineQueryResponse:
        import pyarrow as pa

        oat_prefix = ".__chalk_observed_at__"
        res: List[FeatureResult] = []

        if len(response_proto.scalars_data) > 0:
            root_ts: Optional[dt.datetime] = None
            pkey: Any = None
            batch: pa.RecordBatch = arrow_ipc_to_record_batch(response_proto.scalars_data)

            if len(batch) != 1:
                raise ValueError(f"Expected exactly one scalar data row in response, found {len(batch)}")

            for col_name in batch.schema.names:
                if col_name.endswith(oat_prefix):
                    root_ts = batch[col_name][0].as_py()
                    break
                if col_name == PKEY_COL_NAME:
                    pkey = batch[col_name][0].as_py()

            for col_name in batch.schema.names:
                if (
                    col_name.startswith("__chalk__.__metadata__.")
                    or col_name.startswith(GRPC_RESULT_METADATA_COL_PREFIX)
                    or col_name.endswith(oat_prefix)
                    or col_name in (TS_COL_NAME, INDEX_COL_NAME, PKEY_COL_NAME, OBSERVED_AT_COL_NAME)
                ):
                    continue

                col_field = batch.schema.field(col_name)
                converter = PrimitiveFeatureConverter(
                    name=col_name,
                    is_nullable=col_field.nullable,
                    pyarrow_dtype=col_field.type,
                )
                scoped_ts_fqn = (col_field.metadata or {}).get(b"ts_fqn")
                if scoped_ts_fqn is not None and scoped_ts_fqn in batch.schema.names:
                    scoped_ts_val = batch[scoped_ts_fqn][0].as_py()
                else:
                    scoped_ts_val = root_ts
                converted_col = converter.from_pyarrow_to_primitive(batch[col_name])
                assert (
                    len(converted_col) == 1
                ), f"Expected exactly one element in column {col_name}, found {len(converted_col)}"
                result = FeatureResult(field=col_name, value=converted_col[0], ts=scoped_ts_val, pkey=pkey)
                metadata_col_name = GRPC_RESULT_METADATA_COL_PREFIX + col_name
                if metadata_col_name in batch.schema.names:
                    metadata_col: pa.StructArray = batch[metadata_col_name]
                    result.valid = metadata_col[0].is_valid
                    if result.valid:
                        assert isinstance(metadata_col, pa.StructArray)
                        source_id_field = metadata_col.field("source_id")  # pyright: ignore
                        source_id: str | None = source_id_field[0].as_py()
                        source_type_field = metadata_col.field("source_type")  # pyright: ignore
                        source_type: str | None = source_type_field[0].as_py()
                        is_cache_hit = source_type in ["online_store", "offline_store"]
                        resolver_fqn = source_id or "unknown"
                        result.meta = FeatureResolutionMeta(
                            chosen_resolver_fqn=resolver_fqn,
                            cache_hit=is_cache_hit,
                            #    version=1
                        )

                res.append(result)

        for output_name, output_bytes in response_proto.groups_data.items():
            values = []
            namespace_ts: Optional[dt.datetime] = None
            batch = pa.Table.from_batches([arrow_ipc_to_record_batch(output_bytes)])

            for col_name in batch.schema.names:
                if col_name.endswith(oat_prefix):
                    namespace_ts = batch[col_name][0].as_py()
                    break

            for col_name in batch.schema.names:
                converter = PrimitiveFeatureConverter(
                    name=col_name,
                    is_nullable=batch.schema.field(col_name).nullable,
                    pyarrow_dtype=batch.schema.field(col_name).type,
                )
                values.append(converter.from_pyarrow_to_primitive(batch[col_name]))

            res.append(
                FeatureResult(
                    field=output_name,
                    value={
                        "columns": batch.schema.names,
                        "values": values,
                    },
                    ts=namespace_ts,
                )
            )

        return OnlineQueryResponse(
            data=res,
            meta=OnlineQueryConverter._query_meta_decode(response_proto.response_meta)
            if response_proto.HasField("response_meta")
            else None,
            errors=[ChalkErrorConverter.chalk_error_decode(e) for e in response_proto.errors],
        )

    @staticmethod
    def online_query_result_feather_encode(
        online_query_result_feather: OnlineQueryResultFeather,
    ) -> online_query_pb2.OnlineQueryBulkResponse:
        proto_response = online_query_pb2.OnlineQueryBulkResponse()
        proto_response.scalars_data = online_query_result_feather.scalar_data
        for k, v in online_query_result_feather.groups_data.items():
            # v should already be bytes at this point
            proto_response.groups_data[k] = v
        if online_query_result_feather.errors:
            for error in online_query_result_feather.errors:
                json_error = json.loads(error)
                chalk_error = ChalkError(**json_error)
                chalk_error_proto = chalk_error_pb2.ChalkError()
                chalk_error_proto.CopyFrom(ChalkErrorConverter.chalk_error_encode(chalk_error))
                proto_response.errors.append(chalk_error_proto)
        if online_query_result_feather.meta:
            meta_json = json.loads(online_query_result_feather.meta)
            query_meta = QueryMeta(**meta_json)
            proto_response.response_meta.CopyFrom(OnlineQueryConverter._query_meta_encode(query_meta))
        return proto_response

    @staticmethod
    def online_query_bulk_response_decode(
        response_proto: online_query_pb2.OnlineQueryBulkResponse, trace_id: Optional[str]
    ) -> BulkOnlineQueryResult:
        import polars as pl
        import pyarrow as pa

        scalars: Optional[pl.DataFrame] = None
        groups: Dict[str, pl.DataFrame] = {}
        errors = []
        meta = None
        if len(response_proto.scalars_data) > 0:
            scalars_batch = arrow_ipc_to_record_batch(response_proto.scalars_data)
            scalars = pa_table_to_pl_df(pa.Table.from_batches([scalars_batch]))
        for output_name, output_bytes in response_proto.groups_data.items():
            group_batch = arrow_ipc_to_record_batch(output_bytes)
            groups[output_name] = pa_table_to_pl_df(pa.Table.from_batches([group_batch]))
        for err_proto in response_proto.errors:
            errors.append(ChalkErrorConverter.chalk_error_decode(err_proto))
        if response_proto.HasField("response_meta"):
            meta = OnlineQueryConverter._query_meta_decode(response_proto.response_meta)
        return BulkOnlineQueryResult(scalars_df=scalars, groups_dfs=groups, meta=meta, errors=errors, trace_id=trace_id)

    @staticmethod
    def online_query_multi_response_decode(
        response_proto: online_query_pb2.OnlineQueryMultiResponse, trace_id: Optional[str]
    ) -> BulkOnlineQueryResponse:
        results = []
        for result_proto in response_proto.responses:
            if result_proto.HasField("single_response"):
                results.append(OnlineQueryConverter.online_query_response_decode(result_proto.single_response))
            elif result_proto.HasField("bulk_response"):
                # Add trace ID to sub-query result objects for clarity
                results.append(
                    OnlineQueryConverter.online_query_bulk_response_decode(
                        result_proto.bulk_response, trace_id=trace_id
                    )
                )
        global_errors = [ChalkErrorConverter.chalk_error_decode(e) for e in response_proto.errors]
        return BulkOnlineQueryResponse(results=results, global_errors=global_errors, trace_id=trace_id)
