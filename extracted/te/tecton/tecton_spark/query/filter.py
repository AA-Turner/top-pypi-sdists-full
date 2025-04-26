import logging
import operator
from datetime import datetime
from functools import reduce
from typing import Any
from typing import List
from typing import Optional
from typing import Union

import attrs
import pyspark
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import TimestampType

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core.query_consts import valid_from
from tecton_core.query_consts import valid_to
from tecton_proto.data.feature_view__client_pb2 import MaterializationTimeRangePolicy
from tecton_spark.jars.class_loader import get_or_create_udf_jar_class_loader
from tecton_spark.query.node import SparkExecNode


TECTON_FEATURE_TIMESTAMP_VALIDATOR = "_tecton_feature_timestamp_validator"
SKIP_FEATURE_TIMESTAMP_VALIDATION_ENV = "SKIP_FEATURE_TIMESTAMP_VALIDATION"
TIMESTAMP_VALIDATOR_UDF_REGISTERED = False

logger = logging.getLogger(__name__)


def _apply_or_check_feature_data_time_limits(
    spark: SparkSession,
    feature_df: DataFrame,
    time_range_policy: MaterializationTimeRangePolicy,
    feature_data_time_limits: Optional[pendulum.Period],
    start_timestamp_key: str,
    end_timestamp_key: str,
) -> DataFrame:
    if time_range_policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE:
        return _validate_feature_timestamps(spark, feature_df, feature_data_time_limits, start_timestamp_key)
    elif time_range_policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE:
        return _filter_to_feature_data_time_limits(
            feature_df,
            feature_data_time_limits,
            start_timestamp_key=start_timestamp_key,
            end_timestamp_key=end_timestamp_key,
        )
    else:
        msg = f"Unhandled time range policy: {time_range_policy}"
        raise ValueError(msg)


def _filter_to_feature_data_time_limits(
    feature_df: DataFrame,
    feature_data_time_limits: Optional[pendulum.Period],
    start_timestamp_key: str,
    end_timestamp_key: str,
) -> DataFrame:
    if not feature_data_time_limits:
        return feature_df

    return feature_df.filter(
        (feature_df[end_timestamp_key] >= feature_data_time_limits.start)
        & (feature_df[start_timestamp_key] < feature_data_time_limits.end)
    )


def _ensure_timestamp_validation_udf_registered(spark):
    """
    Register the Spark UDF that is contained in the JAR files and that is part of passed Spark session.
    If the UDF was already registered by the previous calls, do nothing. This is to avoid calling the JVM
    registration code repeatedly, which can be flaky due to Spark. We cannot use `SHOW USER FUNCTIONS` because
    there is a bug in the AWS Glue Catalog implementation that omits the catalog ID.

    Jars are included the following way into the Spark session:
     - For materialization jobs scheduled by Orchestrator, they are included in the Job submission API.
       In this case, we always use the default Spark session of the spun-up Spark cluster.
     - For interactive execution (or remote over db-connect / livy), we always construct Spark session
       manually and include appropriate JARs ourselves.
    """
    global TIMESTAMP_VALIDATOR_UDF_REGISTERED
    if not TIMESTAMP_VALIDATOR_UDF_REGISTERED:
        udf_generator = (
            get_or_create_udf_jar_class_loader()
            .load_class(spark.sparkContext, "com.tecton.udfs.spark3.RegisterFeatureTimestampValidator")
            .newInstance()
        )
        udf_generator.register(TECTON_FEATURE_TIMESTAMP_VALIDATOR)
        TIMESTAMP_VALIDATOR_UDF_REGISTERED = True


def _validate_feature_timestamps(
    spark: SparkSession,
    feature_df: DataFrame,
    feature_data_time_limits: Optional[pendulum.Period],
    timestamp_key: Optional[str],
) -> DataFrame:
    if conf.get_or_none(SKIP_FEATURE_TIMESTAMP_VALIDATION_ENV) is True:
        logger.info(
            "Note: skipping the feature timestamp validation step because `SKIP_FEATURE_TIMESTAMP_VALIDATION` is set to true."
        )
        return feature_df

    if feature_data_time_limits:
        _ensure_timestamp_validation_udf_registered(spark)

        start_time_expr = f"to_timestamp('{feature_data_time_limits.start}')"
        # Registered feature timestamp validation UDF checks that each timestamp is within *closed* time interval: [start_time, end_time].
        # So we subtract 1 microsecond here, before passing time limits to the UDF.
        end_time_expr = f"to_timestamp('{feature_data_time_limits.end - pendulum.duration(microseconds=1)}')"
        filter_expr = f"{TECTON_FEATURE_TIMESTAMP_VALIDATOR}({timestamp_key}, {start_time_expr}, {end_time_expr}, '{timestamp_key}')"

        # Force the output of the UDF to be filtered on, so the UDF cannot be optimized away.
        feature_df = feature_df.where(filter_expr)

    return feature_df


@attrs.frozen
class CustomFilterSparkNode(SparkExecNode):
    input_node: SparkExecNode
    filter_str: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.filter(self.filter_str)


@attrs.frozen
class TrimValidityPeriodSparkNode(SparkExecNode):
    input_node: SparkExecNode
    start: Any
    end: Any

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = self.input_node.to_dataframe(spark)

        start_time_lit = functions.lit(self.start)
        end_time_lit = functions.lit(self.end)

        # Update valid_to if it's null or greater than end_time
        df = df.withColumn(
            valid_to(),
            functions.when(
                (functions.col(valid_to()).isNull()) | (functions.col(valid_to()) > end_time_lit),
                end_time_lit,
            ).otherwise(functions.col(valid_to())),
        )

        # Update valid_from if it's less than start_time
        df = df.withColumn(
            valid_from(),
            functions.when(functions.col(valid_from()) < start_time_lit, start_time_lit).otherwise(
                functions.col(valid_from())
            ),
        )

        # Filter out rows where valid_from >= end_time or valid_to <= start_time
        df = df.filter(~((functions.col(valid_from()) >= end_time_lit) | (functions.col(valid_to()) <= start_time_lit)))

        return df


@attrs.frozen
class FeatureTimeFilterSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_data_time_limits: pendulum.Period
    policy: MaterializationTimeRangePolicy
    start_timestamp_field: str
    # TODO (ajeya): Can go back to using just one column name for filtering since we don't use this for validity
    #  filtering any more
    end_timestamp_field: str
    is_timestamp_format: bool = True
    feature_store_format_version: Optional[int] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        if not self.is_timestamp_format:
            error_msg = "Only timestamp format is supported for FeatureTimeFilterSparkNode"
            raise NotImplementedError(error_msg)
        input_df = self.input_node.to_dataframe(spark)
        return _apply_or_check_feature_data_time_limits(
            spark,
            input_df,
            self.policy,
            self.feature_data_time_limits,
            start_timestamp_key=self.start_timestamp_field,
            end_timestamp_key=self.end_timestamp_field,
        )


@attrs.frozen
class EntityFilterSparkNode(SparkExecNode):
    feature_data: SparkExecNode
    entities: SparkExecNode
    entity_cols: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        feature_df = self.feature_data.to_dataframe(spark)
        entities_df = self.entities.to_dataframe(spark)
        if entities_df:
            # Apply range filter during the Delta read to prune parquet files
            agg_exprs = [
                expr
                for column in entities_df.columns
                for expr in [
                    functions.min(functions.col(column)).alias(f"min_{column}"),
                    functions.max(functions.col(column)).alias(f"max_{column}"),
                ]
            ]
            agg_result = entities_df.agg(*agg_exprs)
            agg_values = agg_result.collect()[0]

            range_filters = []
            for col in entities_df.columns:
                min_value = agg_values[f"min_{col}"]
                max_value = agg_values[f"max_{col}"]
                if min_value is not None and max_value is not None:
                    # Create a filter that allows nulls
                    range_filter = (
                        (functions.col(col) >= min_value) & (functions.col(col) <= max_value)
                    ) | functions.col(col).isNull()
                    range_filters.append(range_filter)
            if len(range_filters) > 0:
                combined_filter = reduce(lambda x, y: x & y, range_filters)
                feature_df = feature_df.filter(combined_filter)

        join_condition = reduce(
            operator.and_, [feature_df[col].eqNullSafe(entities_df[col]) for col in self.entity_cols]
        )
        return feature_df.join(entities_df.hint("broadcast"), how="inner", on=join_condition).select(
            *(feature_df[col] for col in feature_df.columns)
        )


@attrs.frozen
class RespectFeatureStartTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    retrieval_time_col: str
    feature_start_time: Union[pendulum.datetime, int]
    features: List[str]
    feature_store_format_version: int

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)

        ts_col_datatype = ret.schema[self.retrieval_time_col].dataType
        if isinstance(self.feature_start_time, int):
            if not (isinstance(ts_col_datatype, (IntegerType, LongType))):
                msg = f"Invalid feature_start_time column type, expected LongType but got: {ts_col_datatype}"
                raise RuntimeError(msg)
        elif isinstance(self.feature_start_time, datetime):
            if not isinstance(ts_col_datatype, TimestampType):
                msg = f"Invalid feature_start_time column type, expected TimestampType but got: {ts_col_datatype}"
                raise RuntimeError(msg)
        else:
            msg = f"Invalid feature_start_time type: {type(self.feature_start_time)}"
            raise RuntimeError(msg)

        cond = functions.col(self.retrieval_time_col) >= functions.lit(self.feature_start_time)
        # select all non-feature cols, and null out any features outside of feature start time
        project_list = [col for col in ret.columns if col not in self.features]
        for c in self.features:
            newcol = functions.when(cond, functions.col(f"`{c}`")).otherwise(functions.lit(None)).alias(c)
            project_list.append(newcol)
        return ret.select(project_list)


@attrs.frozen
class RespectTTLSparkNode(SparkExecNode):
    input_node: SparkExecNode
    retrieval_time_col: str
    expiration_time_col: str
    features: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        cond = functions.col(self.retrieval_time_col) < functions.col(self.expiration_time_col)
        # select all non-feature cols, and null out any features outside of ttl
        project_list = [col for col in ret.columns if col not in self.features]
        for c in self.features:
            newcol = functions.when(cond, functions.col(c)).otherwise(functions.lit(None)).alias(c)
            project_list.append(newcol)
        return ret.select(project_list)


@attrs.frozen
class StreamWatermarkSparkNode(SparkExecNode):
    input_node: SparkExecNode
    time_column: str
    stream_watermark: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        return ret.withWatermark(self.time_column, self.stream_watermark)
