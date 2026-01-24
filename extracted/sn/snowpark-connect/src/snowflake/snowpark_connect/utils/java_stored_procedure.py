#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from pyspark.errors import AnalysisException

import snowflake.snowpark.types as snowpark_type
from snowflake.snowpark import Session
from snowflake.snowpark._internal.type_utils import type_string_to_type_object
from snowflake.snowpark_connect.client.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.config import (
    get_scala_version,
    is_java_udf_creator_initialized,
    set_java_udf_creator_initialized_state,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.resources_initializer import (
    RESOURCE_PATH,
    SPARK_COMMON_UTILS_JAR_212,
    SPARK_COMMON_UTILS_JAR_213,
    SPARK_CONNECT_CLIENT_JAR_212,
    SPARK_CONNECT_CLIENT_JAR_213,
    SPARK_SQL_JAR_212,
    SPARK_SQL_JAR_213,
    ensure_scala_udf_jars_uploaded,
)
from snowflake.snowpark_connect.utils.upload_java_jar import upload_java_udf_jar

CREATE_JAVA_UDF_PREFIX = "__SC_JAVA_UDF_"
PROCEDURE_NAME = "__SC_JAVA_SP_CREATE_JAVA_UDF"
SP_TEMPLATE = """
CREATE OR REPLACE TEMPORARY PROCEDURE __SC_JAVA_SP_CREATE_JAVA_UDF(udf_name VARCHAR, udf_class VARCHAR, imports ARRAY(VARCHAR))
RETURNS VARCHAR
LANGUAGE JAVA
RUNTIME_VERSION = 17
PACKAGES = ('com.snowflake:snowpark___scala_version__:latest')
__snowflake_udf_imports__
HANDLER = 'com.snowflake.snowpark_connect.procedures.JavaUDFCreator.process'
EXECUTE AS CALLER
;
"""


class JavaUdf:
    """
    Reference class for Java UDFs, providing similar properties like Python UserDefinedFunction.

    This class serves as a lightweight reference to a Java UDF that has been created
    in Snowflake, storing the essential metadata needed for function calls.
    """

    def __init__(
        self,
        name: str,
        input_types: list[snowpark_type.DataType],
        return_type: snowpark_type.DataType,
    ) -> None:
        """
        Initialize a Java UDF reference.

        Args:
            name: The name of the UDF in Snowflake
            input_types: List of input parameter types
            return_type: The return type of the UDF
        """
        self.name = name
        self._input_types = input_types
        self._return_type = return_type


def _scala_static_imports_for_sproc(stage_resource_path: str) -> set[str]:
    scala_version = get_scala_version()
    if scala_version == "2.12":
        return {
            f"{stage_resource_path}/{SPARK_CONNECT_CLIENT_JAR_212}",
            f"{stage_resource_path}/{SPARK_COMMON_UTILS_JAR_212}",
            f"{stage_resource_path}/{SPARK_SQL_JAR_212}",
        }

    if scala_version == "2.13":
        return {
            f"{stage_resource_path}/{SPARK_CONNECT_CLIENT_JAR_213}",
            f"{stage_resource_path}/{SPARK_COMMON_UTILS_JAR_213}",
            f"{stage_resource_path}/{SPARK_SQL_JAR_213}",
        }

    # invalid Scala version
    exception = ValueError(
        f"Unsupported Scala version: {scala_version}. Snowpark Connect supports Scala 2.12 and 2.13"
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


def get_quoted_imports(session: Session) -> str:
    stage_resource_path = session.get_session_stage() + RESOURCE_PATH
    spark_imports = _scala_static_imports_for_sproc(stage_resource_path) | {
        f"{stage_resource_path}/java_udfs-1.0-SNAPSHOT.jar",
    }

    def quote_single(s: str) -> str:
        """Helper function to wrap strings in single quotes for SQL."""
        return "'" + s + "'"

    from snowflake.snowpark_connect.config import global_config

    config_imports = global_config.get("snowpark.connect.udf.java.imports", "")
    config_imports = (
        {x.strip() for x in config_imports.strip("[] ").split(",") if x.strip()}
        if config_imports
        else set()
    )

    return ", ".join(
        quote_single(x) for x in session._artifact_jars | spark_imports | config_imports
    )


def create_snowflake_imports(session: Session) -> str:
    # Make sure that the resource initializer thread is completed before creating Java UDFs since we depend on the jars
    # uploaded by it.
    ensure_scala_udf_jars_uploaded()

    return f"IMPORTS = ({get_quoted_imports(session)})"


def create_java_udf(session: Session, function_name: str, java_class: str):
    if not is_java_udf_creator_initialized():
        upload_java_udf_jar(session)
        session.sql(
            SP_TEMPLATE.replace(
                "__snowflake_udf_imports__", create_snowflake_imports(session)
            ).replace("__scala_version__", get_scala_version())
        ).collect()
        set_java_udf_creator_initialized_state(True)
    name = CREATE_JAVA_UDF_PREFIX + function_name
    result = session.sql(
        f"CALL {PROCEDURE_NAME}('{name}', '{java_class}', ARRAY_CONSTRUCT({get_quoted_imports(session)})::ARRAY(VARCHAR))"
    ).collect()
    result_value = result[0][0]
    if not result_value:
        raise AnalysisException(f"Can not load class {java_class}")
    types = result_value.split(";")
    input_types = [type_string_to_type_object(t) for t in types[:-1]]
    output_type = types[-1]

    return JavaUdf(
        name,
        input_types,
        type_string_to_type_object(output_type),
    )
