import pytest

from tecton import tecton_context
from tecton.repo_utils import get_tecton_objects_skip_validation
from tecton.tecton_test_repo import TestRepo
from tecton_core import conf
from tecton_spark.udf_jar import get_udf_jar_path


def pytest_configure():
    # TECTON_FORCE_FUNCTION_SERIALIZATION will always be set during `tecton test`, however it may not be set when
    # running tests via `tecton plan/apply` or when a user invokes tests directly with pytest. In those cases, default
    # TECTON_FORCE_FUNCTION_SERIALIZATION to true.
    if conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION") is None:
        conf.set("TECTON_FORCE_FUNCTION_SERIALIZATION", "true")


@pytest.fixture(scope="session")
def tecton_pytest_spark_session():
    try:
        from pyspark.sql import SparkSession
    except ImportError:
        pytest.fail("Cannot create a SparkSession if `pyspark` is not installed.")

    active_session = SparkSession.getActiveSession()
    if active_session:
        pytest.fail(
            f"Cannot create SparkSession `tecton_pytest_spark_session` when there is already an active session: {active_session.sparkContext.appName}"
        )

    try:
        spark = (
            SparkSession.builder.appName("tecton_pytest_spark_session")
            .config("spark.jars", get_udf_jar_path())
            # This short-circuit's Spark's attempt to auto-detect a hostname for the master address, which can lead to
            # errors on hosts with "unusual" hostnames that Spark believes are invalid.
            .config("spark.driver.host", "localhost")
            .config("spark.ui.enabled", "false")
            .config("spark.sql.session.timeZone", "UTC")
            # Enable Arrow for PySpark to be compatible with Pandas 2.0. More details, refer to:
            # https://www.notion.so/tecton/mini-RFC-Pandas-2-0-Spark-Compatibility-70687042a6144e60b0bc2a622af65f09?pvs=4#ef8b77bdcc8e4147a224543725ea1936
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )
    except Exception as e:
        # Unfortunately we can't do much better than parsing the error message since Spark raises `Exception` rather than a more specific type.
        if str(e) == "Java gateway process exited before sending its port number":
            pytest.fail(
                "Failed to start Java process for Spark, perhaps Java isn't installed or the 'JAVA_HOME' environment variable is not set?"
            )

        raise e

    try:
        tecton_context.set_tecton_spark_session(spark)
        yield spark
    finally:
        spark.stop()


@pytest.fixture(scope="session")
def repo_fixture():
    tecton_objects, _, _, _ = get_tecton_objects_skip_validation(specified_repo_config=None)
    return TestRepo(tecton_objects)
