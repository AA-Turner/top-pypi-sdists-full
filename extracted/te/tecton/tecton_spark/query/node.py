from abc import abstractmethod
from typing import List

import attrs
import pandas
import pyspark

from tecton_core.pandas_compat import pandas_to_spark
from tecton_core.query import node_interface
from tecton_core.query.nodes import PandasDataframeWrapper
from tecton_core.query.nodes import exclude_query_node_params
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_core.spark_type_annotations import PySparkSession
from tecton_spark.query import translate


@attrs.frozen
class SparkExecNode:
    columns: List[str]

    @classmethod
    def from_query_node(cls, query_node: node_interface.QueryNode) -> "SparkExecNode":
        kwargs = attrs.asdict(
            query_node,
            value_serializer=translate.attrs_spark_converter,
            recurse=False,
            filter=exclude_query_node_params,
        )
        kwargs["columns"] = query_node.columns
        del kwargs["dialect"]
        del kwargs["compute_mode"]
        del kwargs["func"]
        del kwargs["node_id"]
        return cls(**kwargs)

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = self._to_dataframe(spark)
        if {c.lower() for c in df.columns} != {c.lower() for c in self.columns}:
            pass
            # Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
            # cached. This is problematic but will require separate solution; don't fail for now
            # raise RuntimeError(f"Returned mismatch of columns: received: {df.columns}, expected: {self.columns}")
        return df

    @abstractmethod
    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        raise NotImplementedError


class SparkPandasDataframeWrapper(PandasDataframeWrapper):
    def __init__(self, dataframe: pandas.DataFrame, spark: PySparkSession) -> None:
        super().__init__(dataframe)
        self._spark = spark

    def to_spark(self) -> PySparkDataFrame:
        return pandas_to_spark(self._spark, self._dataframe)
