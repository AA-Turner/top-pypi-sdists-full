from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from awsglue.context import GlueContext  # type: ignore


class HudiGlueSession:
    def __init__(self) -> None:
        self._spark_session: SparkSession = self._set_spark()
        self._spark_context = self._spark_session.sparkContext
        self._glue_context = GlueContext(self._spark_context)

    def get_spark_session(self):
        return self._spark_session

    def _set_spark(self) -> SparkSession:
        conf_list = self._get_conf_list()
        spark_conf = SparkConf().setAll(conf_list)
        return (
            SparkSession.builder.config(conf=spark_conf)
            .enableHiveSupport()
            .getOrCreate()
        )

    def _get_conf_list(self):
        return [
            ("spark.serializer", "org.apache.spark.serializer.KryoSerializer"),
            (
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.hudi.catalog.HoodieCatalog",
            ),
            (
                "spark.sql.extensions",
                "org.apache.spark.sql.hudi.HoodieSparkSessionExtension",
            ),
        ]
