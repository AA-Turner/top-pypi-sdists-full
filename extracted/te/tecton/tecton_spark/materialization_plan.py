import datetime
import logging
from typing import Optional

import attrs
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions

import tecton_core.tecton_pendulum as pendulum
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query import builder
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query_consts import anchor_time
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_spark.data_observability import MetricsCollector
from tecton_spark.offline_store import get_offline_store_reader
from tecton_spark.query import translate


MATERIALIZED_RAW_DATA_END_TIME = "_materialized_raw_data_end_time"
logger = logging.getLogger(__name__)


@attrs.define(auto_attribs=True)
class MaterializationPlan:
    """Computes dataframes required for materialization to offline and online stores.

    This class contains `offline_store_data_frame` and `online_store_data_frame`, but both might not always be necessary.

    Both `offline_store_data_frame` and `online_store_data_frame` should be used during batch materialization of BFVs and BWAFVs.
    Only `offline_store_data_frame` should be used during batch materialization of SFVs and SWAFVs.
    Only `online_store_data_frame` should be used during stream materialization of SFVs and SWAFVs.
    """

    _fd: FeatureDefinitionWrapper
    base_data_frame: DataFrame
    count: Optional[int] = None

    @classmethod
    def from_querytree(
        cls, fd: FeatureDefinitionWrapper, query_tree: NodeRef, spark: SparkSession
    ) -> "MaterializationPlan":
        logger.info("Query Plan:")
        logger.info(query_tree.pretty_str())
        # TODO(sanika): Consider adding validation that the expected materialization schema matches the actual materialization schema
        spark_df = translate.spark_convert(query_tree, spark).to_dataframe(spark)
        return cls(fd=fd, base_data_frame=spark_df)

    @classmethod
    def from_parquet(cls, fd: FeatureDefinitionWrapper, path: str, spark: SparkSession) -> "MaterializationPlan":
        return cls(fd=fd, base_data_frame=spark.read.parquet(path))

    @classmethod
    def from_offline_store(
        cls,
        fd: FeatureDefinitionWrapper,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        spark: SparkSession,
    ) -> Optional["MaterializationPlan"]:
        from pyspark.sql.utils import AnalysisException

        try:
            version = fd.get_feature_store_format_version
            offline_store_reader = get_offline_store_reader(spark, fd)
            offline_store_df = offline_store_reader.read(
                # subtract 1us from end time because offline store reader is inclusive on end time
                pendulum.period(start_time, end_time - datetime.timedelta(microseconds=1)),
            )
            start_time_col = convert_timestamp_for_version(start_time, version)
            end_time_col = convert_timestamp_for_version(end_time, version)
            offline_store_df = offline_store_df.filter(
                (functions.col(anchor_time()) >= functions.lit(start_time_col))
                & (functions.col(anchor_time()) < functions.lit(end_time_col))
            )
            return cls(fd=fd, base_data_frame=offline_store_df)
        except AnalysisException as e:
            if "Unable to infer schema for Parquet. It must be specified manually." in str(e):
                logger.warning("Unable to infer Parquet schema; assuming offline store is empty")
                return None
            else:
                raise e

    @property
    def offline_store_data_frame(self) -> DataFrame:
        return self.base_data_frame

    @property
    def online_store_data_frame(self) -> DataFrame:
        online_df = self.base_data_frame

        # batch online and offline df are slightly different
        if not self._fd.compaction_enabled and self._fd.is_temporal and not online_df.isStreaming:
            version = self._fd.get_feature_store_format_version
            batch_mat_schedule = convert_timedelta_for_version(self._fd.batch_materialization_schedule, version)
            online_df = self.base_data_frame.withColumn(
                MATERIALIZED_RAW_DATA_END_TIME, functions.col(anchor_time()) + batch_mat_schedule
            ).drop(anchor_time())
        return online_df

    def cached_count(self):
        if self.count is None:
            self.count = self.base_data_frame.count()
        return self.count


def get_batch_materialization_plan(
    *,
    spark: SparkSession,
    feature_definition: FeatureDefinitionWrapper,
    feature_data_time_limits: Optional[pendulum.Period],
    metrics_collector: Optional[MetricsCollector] = None,
) -> MaterializationPlan:
    """
    NOTE: We rely on Spark's lazy evaluation model to infer partially materialized tile Schema during FeatureView
    creation time without actually performing any materialization.
    Please make sure to not perform any Spark operations under this function's code path that will actually execute
    the Spark query (e.g: df.count(), df.show(), etc.).
    """
    query_tree = builder.build_materialization_querytree(
        Dialect.SPARK,
        ComputeMode.SPARK,
        feature_definition,
        for_stream=False,
        feature_data_time_limits=feature_data_time_limits,
        enable_feature_metrics=(metrics_collector is not None),
    )
    return MaterializationPlan.from_querytree(fd=feature_definition, query_tree=query_tree, spark=spark)


def get_batch_compaction_online_materialization_plan(
    *, spark: SparkSession, feature_definition: FeatureDefinitionWrapper, compaction_job_end_time: datetime.datetime
) -> MaterializationPlan:
    """The materialization plan for compaction jobs to the online store. Only used by feature views with compaction enabled.

    NOTE: We rely on Spark's lazy evaluation model to infer partially materialized tile Schema during FeatureView
    creation time without actually performing any materialization.
    Please make sure to not perform any Spark operations under this function's code path that will actually execute
    the Spark query (e.g: df.count(), df.show(), etc.).
    """
    query_tree = builder.build_compaction_query(
        Dialect.SPARK, ComputeMode.SPARK, feature_definition, compaction_job_end_time
    )
    return MaterializationPlan.from_querytree(fd=feature_definition, query_tree=query_tree, spark=spark)


def get_stream_materialization_plan(
    *,
    spark: SparkSession,
    feature_definition: FeatureDefinitionWrapper,
    metrics_collector: Optional[MetricsCollector] = None,
) -> MaterializationPlan:
    query_tree = builder.build_materialization_querytree(
        Dialect.SPARK,
        ComputeMode.SPARK,
        feature_definition,
        for_stream=True,
        enable_feature_metrics=(metrics_collector is not None),
    )
    return MaterializationPlan.from_querytree(fd=feature_definition, query_tree=query_tree, spark=spark)
