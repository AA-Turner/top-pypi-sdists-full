#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import threading
import time
from collections.abc import Callable
from pathlib import Path

from snowflake.snowpark_connect.client.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.config import get_scala_version
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

SPARK_VERSION = "3.5.6"
RESOURCE_PATH = "/snowflake/snowpark_connect/resources"

# On demand Scala UDF jar upload state - separate from general resource initialization
_scala_2_12_jars_uploaded = threading.Event()
_scala_2_12_jars_lock = threading.Lock()
_scala_2_13_jars_uploaded = threading.Event()
_scala_2_13_jars_lock = threading.Lock()

# Define Scala resource names
SPARK_SQL_JAR_212 = f"spark-sql_2.12-{SPARK_VERSION}.jar"
SPARK_CONNECT_CLIENT_JAR_212 = f"spark-connect-client-jvm_2.12-{SPARK_VERSION}.jar"
SPARK_COMMON_UTILS_JAR_212 = f"spark-common-utils_2.12-{SPARK_VERSION}.jar"
SAS_SCALA_UDF_JAR_212 = "sas-scala-udf_2.12-0.2.0.jar"
JSON_4S_JAR_212 = "json4s-ast_2.12-3.7.0-M11.jar"
SCALA_REFLECT_JAR_212 = "scala-reflect-2.12.18.jar"

# Static dependencies for Scala 2.13
SPARK_SQL_JAR_213 = f"spark-sql_2.13-{SPARK_VERSION}.jar"
SPARK_CONNECT_CLIENT_JAR_213 = f"spark-connect-client-jvm_2.13-{SPARK_VERSION}.jar"
SPARK_COMMON_UTILS_JAR_213 = f"spark-common-utils_2.13-{SPARK_VERSION}.jar"
SAS_SCALA_UDF_JAR_213 = "sas-scala-udf_2.13-0.2.0.jar"
JSON_4S_JAR_213 = "json4s-ast_2.13-3.7.0-M11.jar"
SCALA_REFLECT_JAR_213 = "scala-reflect-2.13.16.jar"


def _upload_scala_udf_jars(jar_files: list[str]) -> None:
    """Upload Spark jar files required for creating Scala UDFs.
    This is the internal implementation - use ensure_scala_udf_jars_uploaded() for thread-safe lazy loading."""

    session = get_or_create_snowpark_session()
    stage = session.get_session_stage()
    resource_path = stage + RESOURCE_PATH
    import snowpark_connect_deps_1
    import snowpark_connect_deps_2

    # Path to includes/jars directory
    includes_jars_dir = Path(__file__).parent / "includes" / "jars"

    for jar_name in jar_files:
        jar_path = None

        # First check includes/jars directory
        includes_jar_path = includes_jars_dir / jar_name
        if includes_jar_path.exists():
            jar_path = includes_jar_path
            logger.info(f"Found {jar_name} in includes/jars")
        else:
            # Try to find the JAR in package 1 first, then package 2
            try:
                jar_path = snowpark_connect_deps_1.get_jar_path(jar_name)
            except FileNotFoundError:
                try:
                    jar_path = snowpark_connect_deps_2.get_jar_path(jar_name)
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"JAR {jar_name} not found in includes/jars or either package"
                    )

        try:
            session.file.put(
                str(jar_path),
                resource_path,
                auto_compress=False,
                overwrite=False,
                source_compression="NONE",
            )
        except Exception as e:
            raise RuntimeError(f"Failed to upload JAR {jar_name}: {e}")


def _upload_scala_2_12_jars() -> None:
    scala_2_12_jars = [
        SPARK_SQL_JAR_212,
        SPARK_CONNECT_CLIENT_JAR_212,
        SPARK_COMMON_UTILS_JAR_212,
        SAS_SCALA_UDF_JAR_212,
        JSON_4S_JAR_212,
        SCALA_REFLECT_JAR_212,  # Required for deserializing Scala lambdas
    ]
    _upload_scala_udf_jars(scala_2_12_jars)


def _upload_scala_2_13_jars() -> None:
    scala_2_13_jars = [
        SPARK_SQL_JAR_213,
        SPARK_CONNECT_CLIENT_JAR_213,
        SPARK_COMMON_UTILS_JAR_213,
        SAS_SCALA_UDF_JAR_213,
        JSON_4S_JAR_213,
        SCALA_REFLECT_JAR_213,
    ]
    _upload_scala_udf_jars(scala_2_13_jars)


def _ensure_configured_scala_jars_uploaded(
    jars_uploaded: threading.Event, lock: threading.Lock, upload_fn: Callable[[], None]
) -> None:
    """
    Ensure Scala UDF jars are uploaded to Snowflake, uploading them lazily if not already done.
    This function is thread-safe and will only upload once even if called from multiple threads.

    Uses the given upload_fn to upload Scala jars if the jars_uploaded event is not set yet.
    """
    # Fast path: if already uploaded, return immediately without acquiring lock
    if jars_uploaded.is_set():
        return

    # Slow path: need to upload, acquire lock to ensure only one thread does it
    with lock:
        # Double-check pattern: another thread might have uploaded while we waited for the lock
        if jars_uploaded.is_set():
            return

        try:
            start_time = time.time()
            logger.info("Uploading Scala UDF jars on-demand...")
            upload_fn()
            jars_uploaded.set()
            logger.info(f"Scala UDF jars uploaded in {time.time() - start_time:.2f}s")
        except Exception as e:
            logger.error(f"Failed to upload Scala UDF jars: {e}")
            raise


def ensure_scala_udf_jars_uploaded() -> None:
    """
    Public function to make sure Scala jars are uploaded and available for imports.
    """
    scala_version = get_scala_version()

    match scala_version:
        case "2.12":
            _ensure_configured_scala_jars_uploaded(
                _scala_2_12_jars_uploaded,
                _scala_2_12_jars_lock,
                _upload_scala_2_12_jars,
            )
        case "2.13":
            _ensure_configured_scala_jars_uploaded(
                _scala_2_13_jars_uploaded,
                _scala_2_13_jars_lock,
                _upload_scala_2_13_jars,
            )
        case _:
            exception = ValueError(
                f"Unsupported Scala version: {scala_version}. Snowpark Connect supports Scala 2.12 and 2.13"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
            raise exception


def initialize_resources() -> None:
    """Initialize all expensive resources. We should initialize what we can here, so that actual rpc calls like
    ExecutePlan are as fast as possible."""
    from snowflake.snowpark import functions as snowpark_fn
    from snowflake.snowpark_connect.expression.map_sql_expression import sql_parser

    session = get_or_create_snowpark_session()

    # This could be merged into the sql_parser call, it is done separately because
    # it introduces additional overhead. This finer grained structuring allows us to make finer grained
    # preloading decisions.
    def warm_sql_parser() -> None:
        parser = sql_parser()
        parser.parseExpression("1 + 1")
        parser.parseExpression("CASE WHEN id > 10 THEN 'large' ELSE 'small' END")

    def initialize_session_stage() -> None:
        _ = session.get_session_stage()

    def initialize_catalog() -> None:
        _ = session.catalog

    def warm_up_sf_connection() -> None:
        df = session.create_dataframe([["a", 3], ["b", 2], ["a", 1]], schema=["x", "y"])
        df = df.select(snowpark_fn.upper(df.x).alias("x"), df.y.alias("y2"))
        df = df.group_by(df.x).agg(snowpark_fn.sum("y2"))
        df.collect()

        session.sql("select 1 as sf_connection_warm_up").collect()

    start_time = time.time()

    resources = [
        ("SQL Parser Init", sql_parser),  # Takes about 0.5s
        ("SQL Parser Warm Up", warm_sql_parser),  # Takes about 0.7s
        ("Initialize Session Stage", initialize_session_stage),  # Takes about 0.3s
        ("Initialize Session Catalog", initialize_catalog),  # Takes about 1.2s
        ("Snowflake Connection Warm Up", warm_up_sf_connection),  # Takes about 1s
    ]

    for name, resource_func in resources:
        resource_start = time.time()
        try:
            resource_func()
            logger.info(f"Initialized {name} in {time.time() - resource_start:.2f}s")
        except Exception as e:
            # We will only log the error if it isn't caused by session being closed. Session
            # closed error happens when the particular run finishes very quickly.
            if str(e).find("because the session has been closed") == -1:
                logger.error(f"Failed to initialize {name}: {e}")

    logger.info(f"All resources initialized in {time.time() - start_time:.2f}s")


def wait_for_resource_initialization() -> None:
    """No-op function retained for backward compatibility.

    This function is kept to maintain backward compatibility with external client code that may call it.
    Previously, this function waited for asynchronous resource initialization to complete.
    Now that resource initialization is synchronous, this function does nothing.
    External callers can safely call this function without any effect.
    """
    pass


def set_upload_jars(upload: bool) -> None:
    """No-op function retained for backward compatibility.
    This function is kept to maintain backward compatibility with external client code that may call it.
    Previously, this function was used to set whether to upload jars required for Scala UDFs.
    Now that Scala UDF jar upload has been moved to lazy on-demand loading via ensure_scala_udf_jars_uploaded(),
    this function does nothing. External callers can safely call this function without any effect.
    """
    pass
