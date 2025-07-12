import logging
import tempfile
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union

import pandas
from pyspark.sql.streaming import StreamingQuery

import tecton
import tecton_core.tecton_pendulum as pendulum
from tecton._internals import errors
from tecton._internals import mock_source_utils
from tecton._internals.secret_resolver import LocalDevSecretResolver
from tecton.framework.data_frame import TectonDataFrame
from tecton.run_api_consts import AGGREGATION_LEVEL_DISABLED
from tecton.run_api_consts import AGGREGATION_LEVEL_FULL
from tecton.run_api_consts import AGGREGATION_LEVEL_PARTIAL
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME
from tecton.run_api_consts import SUPPORTED_AGGREGATION_LEVEL_VALUES
from tecton.tecton_context import TectonContext
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.mock_context import MockContext
from tecton_core.pipeline import pipeline_common
from tecton_core.pipeline.pipeline_common import get_all_input_keys
from tecton_core.pipeline.pipeline_common import get_fco_ids_to_input_keys
from tecton_core.pipeline.rtfv_pipeline import RealtimeFeaturePipeline
from tecton_core.query.builder import build_aggregated_time_range_run_query
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.builder import build_pipeline_querytree
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import ConvertEpochToTimestampNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.rewrite import MockDataRewrite
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import window_end_column_name
from tecton_core.realtime_context import RealtimeContext
from tecton_core.schema import Schema
from tecton_core.secret_management import SecretResolver
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.transformation__client_pb2 import TransformationMode
from tecton_proto.common import secret__client_pb2 as secret_pb2
from tecton_spark import materialization_plan
from tecton_spark.partial_aggregations import partial_aggregate_column_renames
from tecton_spark.spark_helper import check_spark_version


DEFAULT_CONTEXT_PARAMETER_NAME = "context"

logger = logging.getLogger(__name__)

MockInputs = Dict[str, Union[Dict[str, Any], pandas.DataFrame, PySparkDataFrame, RealtimeContext, MockContext]]


def maybe_warn_incorrect_time_range_size(
    fd: FeatureDefinitionWrapper, start_time: datetime, end_time: datetime, aggregation_level: Optional[str]
):
    time_range = end_time - start_time
    if fd.is_temporal_aggregate:
        if fd.is_continuous:
            # There should not be any time range warnings for continuous aggregates.
            return
        slide_interval = fd.aggregate_slide_interval.ToTimedelta()
        if aggregation_level == AGGREGATION_LEVEL_FULL:
            if not fd.has_lifetime_aggregate:
                max_aggregation_window = -fd.earliest_window_start
                if time_range < max_aggregation_window:
                    logger.warning(
                        f"Run time range ({start_time}, {end_time}) is smaller than the maximum aggregation size: {max_aggregation_window}. This may lead to incorrect aggregate feature values."
                    )

            if time_range.total_seconds() % slide_interval.total_seconds() != 0:
                logger.warning(
                    f"Run time range ({start_time}, {end_time}) is not a multiple of the aggregation_interval: {slide_interval}. This may lead to incorrect aggregate feature values, since Tecton pre-aggregates data in smaller time windows based on the aggregation_interval size."
                )
        elif aggregation_level == AGGREGATION_LEVEL_PARTIAL:
            if time_range.total_seconds() % slide_interval.total_seconds() != 0:
                logger.warning(
                    f"Run time range ({start_time}, {end_time}) is not a multiple of the aggregation_interval: {slide_interval}. This may lead to incorrect aggregate feature values, since Tecton pre-aggregates data in smaller time windows based on the aggregation_interval size."
                )
    elif fd.is_incremental_backfill and time_range != fd.batch_materialization_schedule:
        logger.warning(
            f"Run time range ({start_time}, {end_time}) is not equivalent to the batch_schedule: {fd.batch_materialization_schedule}. This may lead to incorrect feature values since feature views with incremental_backfills typically implicitly rely on the materialization range being equivalent to the batch_schedule."
        )


def run_batch(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: FeatureDefinitionWrapper,
    feature_start_time: datetime,
    feature_end_time: datetime,
    mock_data_sources: Dict[str, NodeRef],
    aggregation_level: Optional[str],
) -> "tecton.framework.data_frame.TectonDataFrame":
    _print_run_deprecation_message(aggregation_level)

    if not fd.is_rtfv:
        check_spark_version(fd.fv_spec.batch_cluster_config)

    return _querytree_run_batch(
        dialect=dialect,
        compute_mode=compute_mode,
        fd=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        mock_data_sources=mock_data_sources,
        aggregation_level=aggregation_level,
    )


def _build_run_batch_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: FeatureDefinitionWrapper,
    feature_end_time: datetime,
    feature_time_limits_aligned: pendulum.Period,
    aggregation_level: Optional[str],
) -> NodeRef:
    """Build run_batch query tree

    This assumes that inputs are validated already and is general (should not
    handle mocking data). Using mock data is considered a query tree rewrite.

    Any extra querytree nodes in this function should simply be a display-level
    modification (like field rename, type change, etc).
    """
    if fd.is_temporal:
        qt = build_materialization_querytree(
            dialect, compute_mode, fd, for_stream=False, feature_data_time_limits=feature_time_limits_aligned
        )
        # For a BFV, the materialization querytree is an `AddAnchorTimeNode` wrapped around exactly what we want, so we
        # just extract the input node.
        assert isinstance(qt.node, AddAnchorTimeNode)
        return qt.node.inputs[0]
    elif fd.is_temporal_aggregate:
        if aggregation_level == AGGREGATION_LEVEL_PARTIAL:
            qt = build_materialization_querytree(
                dialect,
                compute_mode,
                fd,
                for_stream=False,
                feature_data_time_limits=feature_time_limits_aligned,
                include_window_end_time=True,
                aggregation_anchor_time=feature_end_time,
            )
            if fd.is_continuous:
                renames = {
                    **partial_aggregate_column_renames(
                        slide_interval_string=fd.get_aggregate_slide_interval_string,
                        trailing_time_window_aggregation=fd.trailing_time_window_aggregation(),
                    ),
                }
                drop = [anchor_time()]
            else:
                # The `PartialAggNode` returned by `build_materialization_querytree` converts timestamps to epochs. We convert back
                # from epochs to timestamps since timestamps are more readable.
                qt = ConvertEpochToTimestampNode(
                    dialect,
                    compute_mode,
                    qt,
                    dict.fromkeys((anchor_time(), window_end_column_name()), fd.get_feature_store_format_version),
                ).as_ref()
                renames = {
                    anchor_time(): DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME,
                    window_end_column_name(): DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME,
                    **partial_aggregate_column_renames(
                        slide_interval_string=fd.get_aggregate_slide_interval_string,
                        trailing_time_window_aggregation=fd.trailing_time_window_aggregation(),
                    ),
                }
                drop = []
            return RenameColsNode(dialect, compute_mode, qt, mapping=renames, drop=drop).as_ref()
        elif aggregation_level == AGGREGATION_LEVEL_DISABLED:
            return build_pipeline_querytree(
                dialect, compute_mode, fd, for_stream=False, feature_data_time_limits=feature_time_limits_aligned
            )
        elif aggregation_level == AGGREGATION_LEVEL_FULL:
            qt = build_aggregated_time_range_run_query(
                dialect,
                compute_mode,
                fd,
                feature_data_time_limits=feature_time_limits_aligned,
                aggregation_anchor_time=feature_end_time,
            )
            return qt

    msg = "Unsupported batch query tree"
    raise Exception(msg)


def _querytree_run_batch(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: FeatureDefinitionWrapper,
    feature_start_time: datetime,
    feature_end_time: datetime,
    mock_data_sources: Dict[str, NodeRef],
    aggregation_level: Optional[str],
) -> "tecton.framework.data_frame.DataFrame":
    feature_time_limits_aligned = pendulum.period(feature_start_time, feature_end_time)

    qt = _build_run_batch_querytree(
        dialect, compute_mode, fd, feature_end_time, feature_time_limits_aligned, aggregation_level
    )

    MockDataRewrite(mock_data_sources).rewrite(qt)

    return TectonDataFrame._create(qt)


def run_stream(
    fd: FeatureDefinitionWrapper,
    output_temp_table: str,
    checkpoint_dir: Optional[str],
) -> StreamingQuery:
    check_spark_version(fd.fv_spec.stream_cluster_config)
    plan = materialization_plan.get_stream_materialization_plan(
        spark=TectonContext.get_instance()._spark,
        feature_definition=fd,
    )
    spark_df = plan.online_store_data_frame
    with tempfile.TemporaryDirectory(dir=checkpoint_dir) as d:
        return (
            spark_df.writeStream.format("memory")
            .queryName(output_temp_table)
            .option("checkpointLocation", d)
            .outputMode("update")
            .start()
        )


def _validate_run_transformation_input_types(
    input_data: MockInputs,
    transformation_mode: TransformationMode,
):
    for key, value in input_data.items():
        if isinstance(value, (RealtimeContext, MockContext)):
            continue
        if transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            if not isinstance(value, pandas.DataFrame) and not is_pyspark_df(value):
                msg = f"Expected input of type DataFrame for key '{key}' in 'pandas' mode, got {type(value).__name__}."
                raise errors.TectonValidationError(msg)
        elif transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            if not isinstance(value, Dict):
                msg = f"Expected input of type Dict for key '{key}' in 'python' mode, got {type(value).__name__}."
                raise errors.TectonValidationError(msg)


def _enrich_realtime_context(
    input_data: MockInputs,
    transformation_mode: TransformationMode,
    request_timestamp: Optional[datetime] = None,
    context_parameter_name: Optional[str] = None,
):
    mock_context = next(
        (data for data in input_data.values() if isinstance(data, (MockContext, RealtimeContext))), None
    )
    key = context_parameter_name or DEFAULT_CONTEXT_PARAMETER_NAME

    if mock_context:
        if isinstance(mock_context, MockContext):
            mock_context = RealtimeContext(secrets=mock_context.secrets, resources=mock_context.resources)
        mock_context.set_request_timestamp(request_timestamp)
        input_data[key] = mock_context
    else:
        input_data[key] = RealtimeContext(request_timestamp=request_timestamp)

    input_data[key].set_mode(transformation_mode)


def run_realtime(
    fd: FeatureDefinitionWrapper,
    fv_name: str,
    mock_inputs: MockInputs,
    transformation_mode: TransformationMode,
    request_timestamp: Optional[datetime] = None,
) -> Union[Dict[str, Any], "tecton.framework.data_frame.TectonDataFrame"]:
    if fd.uses_realtime_context:
        _enrich_realtime_context(mock_inputs, transformation_mode, request_timestamp, fd.context_parameter_name)

    _validate_run_transformation_input_types(mock_inputs, transformation_mode)
    _validate_realtime_mock_inputs_match_expected_shape(mock_inputs, fd.pipeline, fd)
    for key in mock_inputs:
        if is_pyspark_df(mock_inputs[key]):
            mock_inputs[key] = mock_inputs[key].toPandas()

    # Execute ODFV pipeline to get output DataFrame.
    output = run_mock_rtfv_pipeline(
        pipeline=fd.pipeline,
        transformations=fd.transformations,
        name=fv_name,
        mock_inputs=mock_inputs,
        context_parameter_name=fd.context_parameter_name or DEFAULT_CONTEXT_PARAMETER_NAME,
        secret_references=fd.secrets,
        resource_providers=fd.resource_providers,
        secret_resolver=LocalDevSecretResolver(),
    )
    if isinstance(output, pandas.DataFrame):
        output = TectonDataFrame._create(output)

    return output


def run_mock_rtfv_pipeline(
    pipeline: Pipeline,
    transformations: List[specs.TransformationSpec],
    name: str,
    mock_inputs: MockInputs,
    context_parameter_name: str,
    resource_providers: Optional[Mapping[str, specs.ResourceProviderSpec]] = None,
    secret_references: Optional[Mapping[str, secret_pb2.SecretReference]] = None,
    secret_resolver: Optional[SecretResolver] = None,
) -> Union[Dict[str, Any], pandas.DataFrame]:
    return RealtimeFeaturePipeline(
        name=name,
        pipeline=pipeline,
        transformations=transformations,
        pipeline_inputs=mock_inputs,
        resource_providers=resource_providers,
        secret_references=secret_references,
        secret_resolver=secret_resolver,
        context_parameter_name=context_parameter_name,
    ).to_dataframe()


def validate_and_get_aggregation_level(fd: FeatureDefinitionWrapper, aggregation_level: Optional[str]) -> str:
    # Set default aggregation_level value.
    if aggregation_level is None:
        if fd.is_temporal_aggregate:
            aggregation_level = AGGREGATION_LEVEL_FULL
        else:
            aggregation_level = AGGREGATION_LEVEL_DISABLED

    if aggregation_level not in SUPPORTED_AGGREGATION_LEVEL_VALUES:
        msg = "aggregation_level"
        raise errors.FV_INVALID_ARG_VALUE(msg, str(aggregation_level), str(SUPPORTED_AGGREGATION_LEVEL_VALUES))

    return aggregation_level


def _print_run_deprecation_message(aggregation_level: Optional[str]):
    if aggregation_level == AGGREGATION_LEVEL_FULL:
        logger.warning(errors.RUN_DEPRECATED_FULL_AGG)
    elif aggregation_level == AGGREGATION_LEVEL_DISABLED:
        logger.warning(errors.RUN_DEPRECATED_TRANSFORMATION)
    elif aggregation_level == AGGREGATION_LEVEL_PARTIAL:
        logger.warning(errors.RUN_DEPRECATED_PARTIAL_AGGS)


# Validate that mock_inputs keys are exact match with expected inputs.
def _validate_realtime_mock_inputs_match_expected_shape(
    mock_inputs: MockInputs,
    pipeline: pipeline_pb2.Pipeline,
    rtfv_fd: Optional[FeatureDefinitionWrapper] = None,
):
    """Validate the mock_inputs for `run_transformation` matches expected input

    If a feature definition is passed, this will additionally check inputs against batch feature view schemas.
    """
    expected_input_names = get_all_input_keys(pipeline.root)
    mock_inputs_keys = set(mock_inputs.keys())
    if mock_inputs_keys != expected_input_names:
        raise errors.FV_INVALID_MOCK_INPUTS(list(mock_inputs_keys), list(expected_input_names))

    _validate_request_context_mock_inputs(mock_inputs, pipeline)
    # Get num row for all FV mock_inputs with DF types, to validate that they match.
    input_df_row_counts = set()
    for input in mock_inputs.values():
        if isinstance(input, pandas.DataFrame):
            input_df_row_counts.add(len(input.index))
    if len(input_df_row_counts) > 1:
        raise errors.FV_INVALID_MOCK_INPUTS_NUM_ROWS(input_df_row_counts)

    _validate_mock_bfv_inputs_to_odfv(mock_inputs, rtfv_fd)


def _validate_request_context_mock_inputs(
    mock_inputs: MockInputs,
    pipeline: pipeline_pb2.Pipeline,
):
    rc_node = pipeline_common.get_request_context_node(pipeline)
    if not rc_node:
        return

    expected_rc_schema = Schema(rc_node.request_context.tecton_schema)
    expected_cols = set(expected_rc_schema.column_names())
    actual_rc_inputs = mock_inputs[rc_node.input_name]

    # Python mode
    if isinstance(actual_rc_inputs, dict):
        actual_cols = set(actual_rc_inputs.keys())
    # Pandas mode
    elif isinstance(actual_rc_inputs, pandas.DataFrame):
        actual_cols = set(actual_rc_inputs.columns)

    if not actual_cols.issubset(expected_cols):
        raise errors.UNDEFINED_REQUEST_SOURCE_INPUT(list(actual_cols - expected_cols), list(expected_cols))


def _validate_mock_bfv_inputs_to_odfv(mock_inputs: MockInputs, odfv_fd: FeatureDefinitionWrapper):
    """Validate the mock data used to represent batch feature view materialized data for `run()` and `test_run()`.

    Unlike other mock data checks, because there's no way for us to easily identify what features are needed in the
    ODFV, we expect all features in the upstream BFV to be present.
    """
    from tecton_core import feature_set_config

    # Extract input names (from pipeline) and map to feature view schemas (from FDW)
    dependent_fvs = feature_set_config.find_dependent_feature_set_items(
        odfv_fd.fco_container, odfv_fd.pipeline.root, visited_inputs={}, fv_id=odfv_fd.id
    )
    fv_ids_to_fvs = {fv.feature_definition.id: fv for fv in dependent_fvs}
    fco_ids_to_input_keys = get_fco_ids_to_input_keys(odfv_fd.pipeline.root)
    input_name_to_features = {}
    for fv_id, fv in fv_ids_to_fvs.items():
        input_name = fco_ids_to_input_keys[fv_id]
        input_name_to_features[input_name] = fv.features

    # Validate some required fields in the mock data schemas.
    for key, mock_df in mock_inputs.items():
        if key not in input_name_to_features:
            continue
        input_columns = mock_source_utils.get_pandas_or_spark_df_or_dict_columns(mock_df)
        # Check columns match BFV
        dependent_columns = input_name_to_features[key]
        unexpected_columns = [col for col in input_columns if col not in dependent_columns]
        if len(unexpected_columns) > 0:
            msg = f"Unexpected columns: {unexpected_columns} found in mock inputs. Expected columns from the Feature View {key}, such as: '{dependent_columns}'"
            raise TectonValidationError(msg)
        missing_columns = [col for col in dependent_columns if col not in input_columns]
        if len(missing_columns) > 0:
            logger.warning(
                f"ODFV {odfv_fd.name} has a dependency on the Feature View {key}. Features '{missing_columns}' of this "
                f"Feature View are not found. Available columns: '{input_columns}'"
            )
