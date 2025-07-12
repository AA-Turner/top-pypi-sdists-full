from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pyspark
from pyspark.sql.column import Column

import tecton_core.tecton_pendulum as pendulum
from tecton_core import query_consts
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.mock_context import MockContext
from tecton_core.query.compaction_utils import AggregationGroup
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.nodes import Repartition
from tecton_core.query_consts import udf_internal
from tecton_core.schema import Schema
from tecton_spark import data_observability
from tecton_spark import partial_aggregations
from tecton_spark.feature_view_spark_utils import validate_df_columns_and_feature_types
from tecton_spark.query.node import SparkExecNode
from tecton_spark.schema_spark_utils import schema_to_spark
from tecton_spark.spark_pipeline import SparkFeaturePipeline
from tecton_spark.spark_rtfv_pipeline import SparkRealtimeFeaturePipeline


@attrs.frozen
class MultiOdfvPipelineSparkNode(SparkExecNode):
    input_node: SparkExecNode
    use_namespace_feature_prefix: bool
    events_df_timestamp_field: str
    feature_definition_namespaces: List[Tuple[FeatureDefinitionWrapper, str]]

    def build_realtime_fv_udf_col(
        self,
        input_df: pyspark.sql.DataFrame,
        fdw: FeatureDefinitionWrapper,
        namespace: str,
    ) -> Tuple[Column, List[Column]]:
        """
        Builds a Spark udf for executing a specific RTFV. This runs an RTFV,
        which outputs a single temporary object (dict/map for python mode, json for
        pandas mode). We then deserialize this to get the feature columns.

        We use this function in two phases in parallel across multiple RTFVs:
        1. Run an RTFV to get the tmp object
        2. Select columns from the tmp object

        To support running these two phases in parallel, we use this method
        to output the column for (1) and the columns for (2), and concat them
        all together.

        :return: select_column (the tmp rtfv output col), output_columns (the
        columns of the tmp rtfv output, which map to the output features of an
        rtfv)
        """
        output_schema = schema_to_spark(fdw.view_schema)
        if namespace is None:
            namespace = fdw.name

        # Pass in only the non-internal fields and udf-internal fields
        # corresponding to this particular rtfv
        udf_args = []
        for input_col in input_df.schema:
            if udf_internal() not in input_col.name or fdw.id in input_col.name:
                udf_args.append(input_col.name)
        udf_arg_idx_map = {}
        for arg_idx in range(len(udf_args)):
            udf_arg_idx_map[udf_args[arg_idx]] = arg_idx
        realtime_pipeline = SparkRealtimeFeaturePipeline(
            name=fdw.name,
            pipeline=fdw.pipeline,
            transformations=fdw.transformations,
            udf_arg_idx_map=udf_arg_idx_map,
            output_schema=output_schema,
            events_df_timestamp_field=self.events_df_timestamp_field,
            fv_id=fdw.id,
            resource_providers=fdw.resource_providers,
        )

        from pyspark.sql.functions import col

        output_columns = []
        rtfv_tmp_output_name = f"_{namespace}_rtfv_output"
        for c in output_schema:
            output_column_name = (
                f"{namespace}{fdw.namespace_separator}{c.name}" if self.use_namespace_feature_prefix else c.name
            )
            output_columns.append(col(f"{rtfv_tmp_output_name}.{c.name}").alias(output_column_name))

        from pyspark.sql.functions import from_json
        from pyspark.sql.functions import pandas_udf
        from pyspark.sql.functions import udf
        from pyspark.sql.types import StringType

        if realtime_pipeline.mode == "python":
            # Python features are output as a single dict / map column, so we
            # map that into individual columns
            _rtfv_udf = udf(realtime_pipeline.py_udf_wrapper, output_schema)
            udf_col = _rtfv_udf(*[f"`{c}`" for c in udf_args]).alias(rtfv_tmp_output_name)
            return udf_col, output_columns
        elif realtime_pipeline.mode == "pandas":
            # Pandas features are output into a single struct, so we deserialize
            # here + cast into multiple columns.
            # Note: from_json will return null in the case of an unparseable
            # string.
            _rtfv_udf = pandas_udf(realtime_pipeline.pandas_udf_wrapper, StringType())
            deserialized_udf_col = from_json(_rtfv_udf(*[f"`{c}`" for c in udf_args]), output_schema)
            return deserialized_udf_col.alias(rtfv_tmp_output_name), output_columns
        elif realtime_pipeline.mode == "no_transformation":
            _rtfv_identity_function = udf(realtime_pipeline.no_transformation_wrapper, output_schema)
            udf_col = _rtfv_identity_function(*[f"`{c}`" for c in udf_args]).alias(rtfv_tmp_output_name)
            return udf_col, output_columns
        else:
            msg = f"Unsupported realtime pipeline mode {realtime_pipeline.mode}"
            raise ValueError(msg)

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        """
        Executes multiple RTFV transformations on the same input dataframe.

        Note: If the user defines their transformation to produce extra columns
        (besides what's specified in output_schema), they will be ignored. If
        there are missing columns they will fail in this function during
        runtime.
        """
        udf_select_columns = []
        rtfv_output_columns = []
        input_df = self.input_node.to_dataframe(spark)
        for fdw, namespace in self.feature_definition_namespaces:
            select_col, output_cols = self.build_realtime_fv_udf_col(input_df, fdw, namespace)
            udf_select_columns.append(select_col)
            rtfv_output_columns.extend(output_cols)

        # Execute rtfvs in parallel, then deserialize outputs into columns
        input_columns = [f"`{c.name}`" for c in input_df.schema]
        rtfv_tmp_outputs = input_df.select(*input_columns, *udf_select_columns)
        return rtfv_tmp_outputs.select(*input_columns, *rtfv_output_columns)


@attrs.frozen
class PipelineEvalSparkNode(SparkExecNode):
    inputs_map: Dict[str, SparkExecNode]
    feature_definition_wrapper: FeatureDefinitionWrapper

    # Needed for correct behavior by tecton_sliding_window udf if it exists in the pipeline
    feature_time_limits: Optional[pendulum.Period]

    check_view_schema: bool

    # Not implemented for Spark yet
    mock_context: Optional[MockContext] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        spark_pipeline = SparkFeaturePipeline(
            spark,
            self.feature_definition_wrapper.pipeline,
            transformations=self.feature_definition_wrapper.transformations,
            materialization_context_limits=self.feature_time_limits,
            schedule_interval=self.feature_definition_wrapper.batch_materialization_schedule,
            data_source_inputs={k: self.inputs_map[k].to_dataframe(spark) for k in self.inputs_map},
            output_schema=schema_to_spark(self.feature_definition_wrapper.view_schema),
        )
        df = spark_pipeline.get_dataframe()
        if self.feature_time_limits is None and self.feature_definition_wrapper.materialization_start_timestamp:
            df = df.filter(
                df[self.feature_definition_wrapper.timestamp_key]
                >= self.feature_definition_wrapper.materialization_start_timestamp
            )

        if self.check_view_schema:
            validate_df_columns_and_feature_types(
                df, self.feature_definition_wrapper.view_schema, allow_extraneous_columns=True
            )

        return df


@attrs.frozen
class PartialAggSparkNode(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    window_start_column_name: str
    aggregation_tile_interval: pendulum.Duration
    window_end_column_name: Optional[str] = None
    aggregation_anchor_time: Optional[datetime] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = partial_aggregations.construct_partial_time_aggregation_df(
            self.input_node.to_dataframe(spark),
            self.fdw.partial_aggregate_group_by_columns,
            self.fdw.trailing_time_window_aggregation(aggregation_slide_period=self.aggregation_tile_interval),
            self.fdw.get_feature_store_format_version,
            self.fdw.view_schema,
            window_start_column_name=self.window_start_column_name,
            window_end_column_name=self.window_end_column_name,
            aggregation_anchor_time=self.aggregation_anchor_time,
        )
        return df


@attrs.frozen
class OnlinePartialAggSparkNodeV2(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    aggregation_groups: Tuple[AggregationGroup, ...]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = partial_aggregations.construct_online_partial_agg_v2_df(
            self.input_node.to_dataframe(spark),
            [
                *self.fdw.base_partial_aggregate_group_by_columns,
                query_consts.aggregation_tile_id(),
                query_consts.aggregation_group_id(),
            ],
            self.aggregation_groups,
            time_key=self.fdw.trailing_time_window_aggregation().time_key,
            view_schema=self.fdw.view_schema,
            is_continuous=self.fdw.is_continuous,
        )
        return df


@attrs.frozen
class OnlineListAggSparkNode(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    aggregation_groups: Tuple[AggregationGroup, ...]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = partial_aggregations.construct_partial_agg_lists_for_online_df(
            self.input_node.to_dataframe(spark),
            [*self.fdw.base_partial_aggregate_group_by_columns, query_consts.aggregation_group_id()],
            self.aggregation_groups,
        )
        return df


@attrs.frozen
class MetricsCollectorSparkNode(SparkExecNode):
    input_node: SparkExecNode
    metrics_collector: data_observability.MetricsCollector = attrs.field(
        factory=data_observability.get_active_metrics_collector
    )

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.metrics_collector.observe(self.input_node.to_dataframe(spark))


@attrs.frozen
class StagingSparkNode(SparkExecNode):
    input_node: SparkExecNode
    staging_table_name: str
    checkpoint: bool = False
    repartition: Optional[Repartition] = None
    query_tree_step: Optional[QueryTreeStep] = None
    stage_description: Optional[str] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        # TODO(danny): consider implementing this in Spark, but for now this is unnecessary and is a passthrough
        return self.input_node.to_dataframe(spark)


@attrs.frozen
class PythonDataSparkNode(SparkExecNode):
    columns: Tuple[str, ...]
    data: Tuple[Tuple[Any, ...]]
    schema: Optional[Schema] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        if self.schema:
            spark_schema = schema_to_spark(self.schema)
            return spark.createDataFrame(self.data, spark_schema)
        return spark.createDataFrame(self.data, self.columns)
