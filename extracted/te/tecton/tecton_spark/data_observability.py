from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


if TYPE_CHECKING:
    from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


_active_metrics_collector = None


def get_active_metrics_collector():
    if _active_metrics_collector is None:
        return NoopMetricsCollector()

    return _active_metrics_collector


class MetricsCollector:
    def observe(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError


class NoopMetricsCollector(MetricsCollector):
    def observe(self, df: DataFrame) -> DataFrame:
        return df

    def publish(self):
        pass


class SparkMetricsCollector(MetricsCollector):
    def __init__(self, jvm_collector):
        self._jvm_collector = jvm_collector

    def observe(self, df: DataFrame) -> DataFrame:
        new_jdf = self._jvm_collector.observe(df._jdf)
        return DataFrame(new_jdf, df.sql_ctx)

    def publish(self):
        self._jvm_collector.publish()


def create_feature_metrics_collector(
    spark: SparkSession,
    params: "MaterializationTaskParams",
    feature_start_time: Optional[datetime] = None,
    feature_end_time: Optional[datetime] = None,
) -> MetricsCollector:
    global _active_metrics_collector

    if not params.HasField("data_observability_config"):
        return NoopMetricsCollector()

    config = params.data_observability_config
    if not config.enabled:
        return NoopMetricsCollector()

    # TODO(dataobs): it seems we always used the default datetime for FT ingestion, which is 0
    # if it's intentional, it should be more explicit
    feature_start_time = feature_start_time or datetime.fromtimestamp(0)
    feature_end_time = feature_end_time or datetime.fromtimestamp(0)

    jvm_collector = spark._jvm.com.tecton.dataobs.spark.MetricsCollector.fromMaterializationTaskParams(
        params.SerializeToString(),
        int(feature_start_time.timestamp()),
        int(feature_end_time.timestamp()),
        spark._jsparkSession,
    )
    _active_metrics_collector = SparkMetricsCollector(jvm_collector)
    return _active_metrics_collector
