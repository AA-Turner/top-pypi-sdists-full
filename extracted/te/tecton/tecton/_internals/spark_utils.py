import importlib.util
import logging
import os
import sys

from tecton_core import conf
from tecton_core import spark_type_annotations
from tecton_spark.udf_jar import get_udf_jar_path


# Environment variables to propagate to the executor
EXECUTOR_ENV_VARIABLES = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "HIVE_METASTORE_HOST",
    "HIVE_METASTORE_PORT",
    "HIVE_METASTORE_USERNAME",
    "HIVE_METASTORE_DATABASE",
    "HIVE_METASTORE_PASSWORD",
]


logger = logging.getLogger(__name__)


def _is_spark_connect_configured():
    # When Spark Connect is configured on the cluster the "SPARK_REMOTE" env var will be set.
    # See more info here https://spark.apache.org/docs/3.5.4/spark-connect-overview.html
    return "SPARK_REMOTE" in os.environ


def _get_basic_spark_session_builder():
    if _is_spark_connect_configured():
        from pyspark.sql.connect.session import SparkSession as DefaultSparkSession
    else:
        from pyspark.sql import SparkSession as DefaultSparkSession

    builder = DefaultSparkSession.builder

    if conf.get_or_none("AWS_ACCESS_KEY_ID") is not None:
        builder = builder.config("spark.hadoop.fs.s3a.access.key", conf.get_or_none("AWS_ACCESS_KEY_ID"))
        builder = builder.config("spark.hadoop.fs.s3a.secret.key", conf.get_or_none("AWS_SECRET_ACCESS_KEY"))
    if conf.get_or_none("HIVE_METASTORE_HOST") is not None:
        builder = (
            builder.enableHiveSupport()
            .config(
                "spark.hadoop.javax.jdo.option.ConnectionURL",
                f"jdbc:mysql://{conf.get_or_none('HIVE_METASTORE_HOST')}:{conf.get_or_none('HIVE_METASTORE_PORT')}/{conf.get_or_none('HIVE_METASTORE_DATABASE')}",
            )
            .config("spark.hadoop.javax.jdo.option.ConnectionDriverName", "com.mysql.cj.jdbc.Driver")
            .config("spark.hadoop.javax.jdo.option.ConnectionUserName", conf.get_or_none("HIVE_METASTORE_USERNAME"))
            .config("spark.hadoop.javax.jdo.option.ConnectionPassword", conf.get_or_none("HIVE_METASTORE_PASSWORD"))
        )
    for v in EXECUTOR_ENV_VARIABLES:
        if conf.get_or_none(v) is not None:
            builder = builder.config(f"spark.executorEnv.{v}", conf.get_or_none(v))
    return builder


def get_or_create_spark_session(custom_spark_options=None):
    logger.debug("Creating Apache Spark Context")
    builder = _get_basic_spark_session_builder()

    if conf.get_or_none("SPARK_DRIVER_LOCAL_IP"):
        # Sadly, Spark will always attempt to retrieve the driver's local IP
        # even if the "spark.driver.host" conf is set. This will
        # result in an error if Spark's code is unable to retrieve the local IP
        # (which happens in the case of SageMaker notebooks). The only way to override Spark's
        # behavior is by setting the SPARK_LOCAL_IP env variable
        os.environ["SPARK_LOCAL_IP"] = conf.get_or_none("SPARK_DRIVER_LOCAL_IP")

    # Databricks 14.3 Shared Access Mode has `Spark_REMOTE` set by defaut, which is conflict with master("local")
    # config.
    if _is_spark_connect_configured():
        builder = builder.master("local")

    builder = builder.config("spark.jars", get_udf_jar_path())

    # For some reason using the property spark.pyspark.python does not
    # work for this like it should
    os.environ["PYSPARK_PYTHON"] = sys.executable

    if custom_spark_options:
        for k, v in custom_spark_options.items():
            builder.config(k, v)

    return builder.getOrCreate()


def log_spark_env(spark: spark_type_annotations.PySparkSession):
    spark_version = spark.version
    has_dbutils = importlib.util.find_spec("dbutils")
    if has_dbutils:
        dbr_version = (
            os.environ.get("DATABRICKS_RUNTIME_VERSION") if "DATABRICKS_RUNTIME_VERSION" in os.environ else "unknown"
        )
        logger.debug(f"Running on Databricks with spark-{spark_version} and dbr-{dbr_version}")
    elif "EMR_CLUSTER_ID" in os.environ:
        emr_cluster_id = os.environ.get("EMR_CLUSTER_ID")
        logger.debug(f"Running on EMR cluster {emr_cluster_id} with spark-{spark_version}")
    else:
        logger.debug(f"Running locally with spark-{spark_version}")
