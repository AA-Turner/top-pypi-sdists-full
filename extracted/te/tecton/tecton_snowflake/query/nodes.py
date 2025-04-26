from __future__ import annotations

import typing
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pandas
import pypika
from pypika import terms

import tecton_core.tecton_pendulum as pendulum
from tecton_core import feature_definition_wrapper
from tecton_core import query_consts
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.query import node_interface
from tecton_core.query import nodes
from tecton_core.query.dialect import Dialect
from tecton_core.query.pandas import node as pandas_node
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_proto.common import aggregation_function__client_pb2 as afpb
from tecton_proto.data import feature_view__client_pb2 as feature_view_pb2
from tecton_snowflake import pipeline_helper
from tecton_snowflake.query import aggregation_plans
from tecton_snowflake.query import queries


if typing.TYPE_CHECKING:
    import snowflake.snowpark


@attrs.frozen
class PartialAggSnowflakeNode(nodes.PartialAggNode):
    """
    Using a different implementation for LastN/FirstN aggregation functions for Snowflake
    """

    @classmethod
    def from_query_node(cls, query_node: nodes.PartialAggNode) -> "PartialAggSnowflakeNode":
        return cls(
            dialect=Dialect.SNOWFLAKE,
            compute_mode=ComputeMode.SNOWFLAKE,
            input_node=query_node.input_node,
            fdw=query_node.fdw,
            window_start_column_name=query_node.window_start_column_name,
            aggregation_tile_interval=query_node.aggregation_tile_interval,
            window_end_column_name=query_node.window_end_column_name,
            aggregation_anchor_time=query_node.aggregation_anchor_time,
        )

    def _get_partial_agg_columns_and_names(self) -> List[Tuple[terms.Term, str]]:
        """
        Override PartialAggNode's _get_partial_agg_columns to use the Snowflake implementation
        """
        time_aggregation = self.fdw.trailing_time_window_aggregation()
        agg_cols = []
        output_columns = set()
        for feature in time_aggregation.features:
            aggregation_plan = aggregation_plans.get_aggregation_plan(
                feature.function, feature.function_params, self.fdw.time_key
            )
            agg_query_terms = aggregation_plan.partial_aggregation_query_terms(feature.input_feature_name)
            materialized_column_names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            assert len(agg_query_terms) == len(materialized_column_names)
            for column_name, aggregated_column in zip(
                materialized_column_names,
                agg_query_terms,
            ):
                if column_name in output_columns:
                    continue
                output_columns.add(column_name)
                agg_cols.append((aggregated_column, column_name))
        return agg_cols


@attrs.frozen
class AsofJoinFullAggSnowflakeNode(nodes.AsofJoinFullAggNode):
    """
    Asof join full agg rollup, using band joins
    """

    @classmethod
    def from_query_node(cls, query_node: nodes.AsofJoinFullAggNode):
        kwargs = attrs.asdict(query_node, recurse=False)
        del kwargs["node_id"]
        return cls(**kwargs)

    def _to_query(self) -> pypika.Query:
        """
        Snowflake doesn't support RANGE BETWEEN with sliding window as of 07/27/2023, they have it on the roadmap but no ETA.
        This implmentation treat every feature in an aggregation as a separate query, and then join them together.

        :return: Query
        """
        time_aggregation = self.fdw.trailing_time_window_aggregation()
        join_keys = list(self.spine.node.columns)

        # Generate sub queries for each feature
        sub_queries = []
        # Output columns for each sub query
        output_columns = []
        for feature in time_aggregation.features:
            sub_query = self._to_single_feature_aggregate_query(feature)
            sub_queries.append(sub_query)
            output_columns.append([*list(self.spine.node.columns), feature.output_feature_name])

        # Join all sub queries together
        left_columns = output_columns[0]
        result_df = sub_queries[0]
        for right_q, right_columns in zip(sub_queries[1:], output_columns[1:]):
            left_q = result_df
            join_q = queries.SnowflakeQuery().from_(left_q)
            join_q = join_q.inner_join(right_q)
            join_conditions = terms.Criterion.all(
                [
                    terms.Criterion.any(
                        [
                            left_q.field(col) == right_q.field(col),
                            left_q.field(col).isnull() and right_q.field(col).isnull(),
                        ]
                    )
                    for col in join_keys
                ]
            )
            right_nonjoin_cols = set(right_columns) - set(join_keys)
            result_df = join_q.on(join_conditions).select(
                *(left_q.field(col) for col in left_columns), *(right_q.field(col) for col in right_nonjoin_cols)
            )
            left_columns = left_columns + list(right_nonjoin_cols)
        return result_df

    def _to_single_feature_aggregate_query(self, aggregate_feature: feature_view_pb2.Aggregate) -> pypika.Query:
        """
        Helper method to run one aggregate feature. This does not use the Range Between implemention.

        :param aggregate_feature: AggregateFeature data proto
        :return: Query
        """
        left_df = self.spine.node._to_query()
        right_df = self.partial_agg_node.node._to_query()
        join_keys = self.fdw.join_keys
        # When calling ghf() with time range, spine only has _ANCHOR_TIME but not time_key
        timestamp_join_cols = (
            [self.fdw.time_key, query_consts.anchor_time()]
            if self.fdw.time_key in self.spine.node.columns
            else [query_consts.anchor_time()]
        )
        common_cols = join_keys + timestamp_join_cols

        output_columns = list(self.spine.node.columns)

        left_name = self.spine.name

        agg_name = self.partial_agg_node.name

        output_feature_name = query_consts.default_case(aggregate_feature.output_feature_name)
        if aggregate_feature.HasField("window"):
            # This is the legacy way to specify an aggregation window
            window_duration = pendulum.Duration(seconds=aggregate_feature.window.ToSeconds())
        else:
            time_window = create_time_window_spec_from_data_proto(aggregate_feature.time_window)
            window_duration = pendulum.Duration(seconds=time_window.window_duration.total_seconds())
        window = time_utils.convert_timedelta_for_version(window_duration, self.fdw.get_feature_store_format_version)
        aggregation_plan = aggregation_plans.get_aggregation_plan(
            aggregate_feature.function,
            aggregate_feature.function_params,
            f"{agg_name}.{query_consts.anchor_time()}",
        )
        names = aggregation_plan.materialized_column_names(aggregate_feature.input_feature_name)
        agg_columns = [*common_cols, aggregation_plan.full_aggregation_join_query_term(names).as_(output_feature_name)]
        # Join spine and partial agg node
        agg_from = (
            queries.SnowflakeQuery()
            .from_(pypika.AliasedQuery(left_name))
            .inner_join(pypika.AliasedQuery(agg_name))
            .on_field(*join_keys)
        )
        # Flatten the input feature if the aggregation function is last/first non-distinct N
        if aggregate_feature.function in {
            afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
            afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
        }:
            agg_from = agg_from.lateral(pypika.Field(f"FLATTEN(input=>{names[0]})"))
        # Add the condition that spine time is between partial agg time and partial agg time + window, and run the aggregation function
        agg = (
            agg_from.select(*agg_columns)
            .distinct()
            .where(pypika.AliasedQuery(left_name)._ANCHOR_TIME >= pypika.AliasedQuery(agg_name)._ANCHOR_TIME)
            .where(pypika.AliasedQuery(left_name)._ANCHOR_TIME < pypika.AliasedQuery(agg_name)._ANCHOR_TIME + window)
            .groupby(*(pypika.AliasedQuery(left_name).field(column) for column in output_columns))
        )

        output_feature_name = query_consts.default_case(aggregate_feature.output_feature_name)
        spine_name = left_name + "_" + output_feature_name
        right_name = agg_name + "_AGG"
        feature_column = pypika.AliasedQuery(right_name).field(output_feature_name)
        # TODO(TEC-15924): This behavior is not the same as spark. We should consider consolidating this behavior.
        if aggregate_feature.function == afpb.AggregationFunction.AGGREGATION_FUNCTION_COUNT:
            feature_column = queries.ZeroIfNull(feature_column).as_(output_feature_name)
        # Join the result with the spine node
        join_df = (
            queries.SnowflakeQuery()
            .with_(left_df, spine_name)
            .with_(agg, right_name)
            .from_(pypika.AliasedQuery(spine_name))
            .left_join(pypika.AliasedQuery(right_name))
            .on_field(*common_cols)
            .select(*output_columns, feature_column)
        )
        output_columns.append(output_feature_name)

        return (
            queries.SnowflakeQuery()
            .with_(left_df, left_name)
            .with_(right_df, agg_name)
            .from_(join_df)
            .select(*output_columns)
        )


# SnowparkExecNodes are responsible for taking in a snowpark dataframe, performing some snowpark operation and outputting a
# snowpark dataframe
@attrs.frozen
class SnowparkExecNode:
    columns: List[str]
    input_node: SnowparkExecNode
    column_name_updater: Optional[Callable[[str], str]]  # Snowflake uses this method to uppercase all column names
    session: "snowflake.snowpark.Session"

    @classmethod
    def from_node_inputs(
        cls,
        query_node: node_interface.QueryNode,
        input_node: SnowparkExecNode,
        session: "snowflake.snowpark.Session",
        column_name_updater: Optional[Callable[[str], str]] = lambda x: x,
    ) -> "SnowparkExecNode":
        kwargs = attrs.asdict(query_node, recurse=False)
        kwargs["input_node"] = input_node
        kwargs["columns"] = query_node.columns
        kwargs["column_name_updater"] = column_name_updater
        kwargs["session"] = session
        del kwargs["dialect"]
        del kwargs["compute_mode"]
        del kwargs["func"]
        del kwargs["node_id"]
        return cls(**kwargs)

    def to_dataframe(self) -> pandas.Dataframe:
        return self.to_snowpark().toPandas()

    def to_snowpark(self) -> "snowflake.snowpark.DataFrame":
        df = self._to_snowpark()
        return df

    @abstractmethod
    def _to_snowpark(self) -> "snowflake.snowpark.DataFrame":
        raise NotImplementedError


@attrs.frozen
class SnowparkMultiOdfvPipelineNode(SnowparkExecNode):
    input_node: Union[SnowparkExecNode, pandas_node.SqlExecNode]
    feature_definition_namespaces: List[Tuple[feature_definition_wrapper.FeatureDefinitionWrapper, str]]
    use_namespace_feature_prefix: bool
    events_df_timestamp_field: str

    def _to_snowpark(self) -> "snowflake.snowpark.DataFrame":
        """
        Executes multiple ODFV transformations on the same input dataframe.

        Note: If the user defines their transformation to produce extra columns
        (besides what's specified in output_schema), they will be ignored. If
        there are missing columns they will fail in this function during
        runtime.
        """
        output_df = self.input_node.to_snowpark()

        # Apply ODFV to input df one by one
        for fd, namespace in self.feature_definition_namespaces:
            if fd.is_rtfv:
                schema_dict = fd.view_schema.to_dict()
                output_df = pipeline_helper.pipeline_to_df_with_input(
                    session=self.session,
                    input_df=output_df,
                    pipeline=fd.pipeline,
                    transformations=fd.transformations,
                    output_schema=schema_dict,
                    name=fd.name,
                    fv_id=fd.id,
                    namespace=namespace,
                    append_prefix=self.use_namespace_feature_prefix,
                )
        columns_to_drop = [column for column in output_df.columns if query_consts.udf_internal() in column]
        if len(columns_to_drop) > 0:
            output_df = output_df.drop(*columns_to_drop)
        return output_df


@attrs.frozen
class SnowparkRenameColsNode(SnowparkExecNode):
    input_node: Union[SnowparkExecNode, pandas_node.SqlExecNode]
    mapping: Optional[Dict[str, str]]
    drop: Optional[List[str]]

    def _to_snowpark(self) -> "snowflake.snowpark.DataFrame":
        input_df = self.input_node.to_snowpark()
        output_df = input_df
        if self.drop:
            output_df = input_df.drop(*self.drop)
        if self.mapping:
            from snowflake.snowpark.functions import col

            select_columns = []
            for column_name in output_df.columns:
                if column_name not in self.mapping:
                    select_columns.append(col(column_name))
                else:
                    select_columns.append(col(column_name).alias(self.mapping[column_name]))
            output_df = input_df.select(*select_columns)
        return output_df
