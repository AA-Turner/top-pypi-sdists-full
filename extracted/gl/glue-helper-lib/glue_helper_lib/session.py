from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
import typing


class SparkEnabledSession(typing.Protocol):
    def get_spark_session(self) -> SparkSession:
        ...


class GlueSession(typing.Protocol):
    def get_glue_context(self) -> GlueContext:
        ...


class SparkGlueSession:
    def __init__(self) -> None:
        self._spark_context = SparkContext()
        self._glue_context = GlueContext(self._spark_context)
        self._spark_session: SparkSession = self._glue_context.spark_session

    def get_spark_session(self):
        return self._spark_session

    def get_glue_context(self):
        return self._glue_context
