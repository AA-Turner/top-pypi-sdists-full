import logging
from datetime import datetime
from typing import Dict
from typing import Optional

import attrs
import pyspark

import tecton_core.tecton_pendulum as pendulum
from tecton_core import specs
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.offline_store import PartitionType
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query_consts import valid_to
from tecton_core.skew_config import SkewConfig
from tecton_proto.args.pipeline__client_pb2 import DataSourceNode
from tecton_proto.data.saved_feature_data_frame__client_pb2 import SavedFeatureDataFrame
from tecton_spark import data_source_helper
from tecton_spark import offline_store
from tecton_spark.query.node import SparkExecNode


logger = logging.getLogger(__name__)


@attrs.frozen
class UserSpecifiedDataSparkNode(SparkExecNode):
    data: DataframeWrapper
    metadata: Optional[Dict[str, any]]
    row_id_column: Optional[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.data.to_spark()


@attrs.frozen
class DataSparkNode(SparkExecNode):
    data: DataframeWrapper
    metadata: Optional[Dict[str, any]]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.data.to_spark()


@attrs.frozen
class MockDataSourceScanSparkNode(SparkExecNode):
    data: SparkExecNode
    ds: specs.DataSourceSpec
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    skew_config: Optional[SkewConfig] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = self.data.to_dataframe(spark)
        if self.start_time or self.end_time:
            df = data_source_helper.apply_partition_and_timestamp_filter(
                df, self.ds.batch_source, self.start_time, self.end_time
            )
        return df


@attrs.frozen
class DataSourceScanSparkNode(SparkExecNode):
    ds: specs.DataSourceSpec
    is_stream: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    ds_node: Optional[DataSourceNode]
    skew_config: Optional[SkewConfig]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = data_source_helper.get_ds_dataframe(
            spark,
            self.ds,
            consume_streaming_data_source=self.is_stream,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        return df


# This is used for debugging method.
@attrs.frozen
class RawDataSourceScanSparkNode(SparkExecNode):
    ds: specs.DataSourceSpec

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = data_source_helper.get_non_dsf_raw_dataframe(spark, self.ds.batch_source)
        return df


@attrs.frozen
class OfflineStoreScanSparkNode(SparkExecNode):
    feature_definition_wrapper: FeatureDefinitionWrapper
    partition_time_filter: Optional[pendulum.Period]
    # TODO: pushdown join keys filter based on the provided spine (currently this is not used by Spark implementation)
    entity_filter: Optional[NodeRef] = None
    skew_config: Optional[SkewConfig] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        offline_reader = offline_store.get_offline_store_reader(spark, self.feature_definition_wrapper)
        try:
            # None implies no timestamp filtering. When we implement time filter pushdown, it will go here
            df = offline_reader.read(self.partition_time_filter)
            return df
        except pyspark.sql.utils.AnalysisException as e:
            error_message = f"Failed to read from the Offline Store. Please ensure that materialization backfills have completed for Feature View '{self.feature_definition_wrapper.name}' before investigating further."
            raise TectonInternalError(error_message) from e


@attrs.frozen
class DatasetScanSparkNode(SparkExecNode):
    dataset: SavedFeatureDataFrame
    time_filter: Optional[pendulum.Period] = None

    @property
    def _timestamp_column_name(self) -> str:
        if self.dataset.HasField("logged_dataset"):
            return self.dataset.logged_dataset.timestamp_column_name
        elif self.dataset.HasField("saved_dataset"):
            return self.dataset.saved_dataset.timestamp_column_name
        elif self.dataset.HasField("timestamp_column_name"):  # Legacy fallback
            return self.dataset.timestamp_column_name
        else:
            error_msg = "Dataset must have either logged_dataset or saved_dataset defined."
            raise ValueError(error_msg)

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        reader = offline_store.DeltaReader(
            spark,
            self.dataset.dataframe_location,
            partition_size=None,
            partition_type=PartitionType.NONE,
            feature_store_format_version=0,  # is not relevant for PartitionType.DATE_STR
        )
        try:
            df = reader.read(partition_time_limits=None)
            if self.time_filter is not None:
                timestamp_column_name = self._timestamp_column_name

                # if timestamp_column_name is not in the dataframe, it's a gfir case so use valid_to() instead
                if timestamp_column_name not in df.columns:
                    timestamp_column_name = valid_to()

                start_date = pyspark.sql.functions.lit(self.time_filter.start)
                end_date = pyspark.sql.functions.lit(self.time_filter.end)
                timestamp_col = pyspark.sql.functions.col(timestamp_column_name)
                df = df.filter((timestamp_col >= start_date) & (timestamp_col < end_date))
            return df
        except pyspark.sql.utils.AnalysisException as e:
            error_message = "Failed to read from the Dataset storage. Please ensure that the dataset job has completed before investigating further."
            raise TectonInternalError(error_message) from e
