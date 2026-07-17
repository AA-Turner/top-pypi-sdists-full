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
    is_native_app_mode,
    qualify_temp_object_name_str,
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
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache
from snowflake.snowpark_connect.utils.sql_quoting import quote_single
from snowflake.snowpark_connect.utils.upload_java_jar import (
    JAVA_UDFS_JAR_NAME,
    upload_java_udf_jar,
)

CREATE_JAVA_UDF_PREFIX = "__SC_JAVA_UDF_"
PROCEDURE_NAME = "__SC_JAVA_SP_CREATE_JAVA_UDF"
# Versioned schema SCOS creates at runtime in native app mode.
# Must be versioned so EXECUTE AS OWNER procs are allowed (093043 blocks them
# in non-versioned schemas).  Relative IMPORTS resolve against the app's version
# stage root, so the app provider must bundle the SCOS JARs there.
NATIVE_APP_VERSIONED_SCHEMA = "__SCOS_JAVA_RUNTIME"
# Normal path: TEMPORARY makes the proc session-scoped (auto-cleaned, no privileges needed).
SP_TEMPLATE = """
CREATE OR REPLACE TEMPORARY PROCEDURE __procedure_name__(udf_name VARCHAR, udf_class VARCHAR, imports ARRAY(VARCHAR))
RETURNS VARCHAR
LANGUAGE JAVA
RUNTIME_VERSION = 17
PACKAGES = ('com.snowflake:snowpark___scala_version__:latest')
__snowflake_udf_imports__
HANDLER = 'com.snowflake.snowpark_connect.procedures.JavaUDFCreator.process'
EXECUTE AS CALLER
;
"""
# Native app path: proc lives in a persistent versioned schema (not TEMPORARY).
# TEMPORARY is incompatible with a fully-qualified 3-part name in a versioned schema,
# and the proc must survive across sessions (the is_java_udf_creator_initialized flag
# is per-process, not per-session, so a fresh execute_jar process always re-creates it —
# but keeping it persistent is still safer than relying on TEMPORARY semantics here).
# EXECUTE AS OWNER is required: versioned schemas allow it; non-versioned schemas don't (093043).
NATIVE_APP_SP_TEMPLATE = """
CREATE OR REPLACE PROCEDURE __procedure_name__(udf_name VARCHAR, udf_class VARCHAR, imports ARRAY(VARCHAR))
RETURNS VARCHAR
LANGUAGE JAVA
RUNTIME_VERSION = 17
PACKAGES = ('com.snowflake:snowpark___scala_version__:latest')
__snowflake_udf_imports__
HANDLER = 'com.snowflake.snowpark_connect.procedures.JavaUDFCreator.process'
EXECUTE AS OWNER
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

    from snowflake.snowpark_connect.config import global_config

    config_imports = global_config.get("snowpark.connect.udf.java.imports", "")
    config_imports = (
        {x.strip() for x in config_imports.strip("[] ").split(",") if x.strip()}
        if config_imports
        else set()
    )

    artifacts_store = get_spark_session_cache().artifacts_store

    return ", ".join(
        quote_single(x)
        for x in artifacts_store.get_jars() | spark_imports | config_imports
    )


def create_snowflake_imports(session: Session) -> str:
    # Make sure that the resource initializer thread is completed before creating Java UDFs since we depend on the jars
    # uploaded by it.
    ensure_scala_udf_jars_uploaded()

    return f"IMPORTS = ({get_quoted_imports(session)})"


# ── Native App helpers ───────────────────────────────────────────────────────
# In native app mode the helper proc lives in a runtime-created versioned schema
# with relative IMPORTS paths that resolve against the app's version stage root.
# The app provider must place the SCOS JARs there at install time.
# addArtifact JARs are silently ignored in native app mode — they are not included in IMPORTS.


def _native_app_static_jar_paths() -> set[str]:
    """Relative JAR paths for SCOS JARs bundled in the app's version stage.

    Single source of truth for both create_native_app_snowflake_imports (proc
    creation) and get_relative_quoted_imports (CALL time).
    """
    scala_version = get_scala_version()
    if scala_version == "2.12":
        client_jar, utils_jar, sql_jar = (
            SPARK_CONNECT_CLIENT_JAR_212,
            SPARK_COMMON_UTILS_JAR_212,
            SPARK_SQL_JAR_212,
        )
    elif scala_version == "2.13":
        client_jar, utils_jar, sql_jar = (
            SPARK_CONNECT_CLIENT_JAR_213,
            SPARK_COMMON_UTILS_JAR_213,
            SPARK_SQL_JAR_213,
        )
    else:
        exception = ValueError(
            f"Unsupported Scala version: {scala_version}. Snowpark Connect supports Scala 2.12 and 2.13"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception
    return {
        f"{RESOURCE_PATH}/{client_jar}",
        f"{RESOURCE_PATH}/{utils_jar}",
        f"{RESOURCE_PATH}/{sql_jar}",
        f"{RESOURCE_PATH}/{JAVA_UDFS_JAR_NAME}",
    }


def _native_app_user_config_imports() -> set[str]:
    """User-supplied JAR paths from snowpark.connect.udf.java.imports."""
    from snowflake.snowpark_connect.config import global_config

    raw = global_config.get("snowpark.connect.udf.java.imports", "")
    if not raw:
        return set()
    # TODO: strip surrounding quotes from each entry so users who write
    # ['/my.jar'] (quoted inside the config value) get a clear validation error
    # instead of a confusing "path must start with '/'" message when the path
    # is actually '/my.jar' with a leading quote.  x.strip().strip("'\"") is
    # the one-liner fix.
    paths = {x.strip() for x in raw.strip("[] ").split(",") if x.strip()}
    bad = {p for p in paths if not p.startswith("/")}
    if bad:
        exception = ValueError(
            f"Native app mode requires version-stage relative paths starting with '/'. "
            f"Invalid snowpark.connect.udf.java.imports entries: {sorted(bad)}"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception
    return paths


def get_relative_quoted_imports() -> str:
    """IMPORTS entries for a CALL in native app mode (relative paths only).

    addArtifact JARs are excluded — they live on the session stage and cannot
    be expressed as version-stage relative paths.
    """
    all_imports = _native_app_static_jar_paths() | _native_app_user_config_imports()
    return ", ".join(quote_single(x) for x in all_imports)


def create_native_app_snowflake_imports() -> str:
    """IMPORTS clause for the helper proc in native app mode (relative paths only).

    Includes user JARs so JavaUDFCreator can load customer classes via
    reflection at proc-creation time.
    """
    all_imports = _native_app_static_jar_paths() | _native_app_user_config_imports()
    return f"IMPORTS = ({', '.join(quote_single(p) for p in all_imports)})"


def _ensure_native_app_schema(session: Session) -> None:
    session.sql(
        f"CREATE OR ALTER VERSIONED SCHEMA {NATIVE_APP_VERSIONED_SCHEMA}"
    ).collect()


def create_java_udf(session: Session, function_name: str, java_class: str):
    # TODO: is_java_udf_creator_initialized is a process-global flag, not tied to
    # the native_app_mode setting.  Toggling native_app_mode mid-process (rare, but
    # possible in tests) after a proc has been created will skip re-creation on the
    # switched path — the wrong proc gets called.  Fix: track initialization state
    # per-mode (two flags, or a mode-keyed dict).
    if is_native_app_mode():
        return _create_java_udf_native_app(session, function_name, java_class)
    return _create_java_udf_normal(session, function_name, java_class)


def _create_java_udf_normal(session: Session, function_name: str, java_class: str):
    qualified_proc_name = qualify_temp_object_name_str(session, PROCEDURE_NAME)

    if not is_java_udf_creator_initialized():
        upload_java_udf_jar(session)
        session.sql(
            SP_TEMPLATE.replace("__procedure_name__", qualified_proc_name)
            .replace("__snowflake_udf_imports__", create_snowflake_imports(session))
            .replace("__scala_version__", get_scala_version())
        ).collect()
        set_java_udf_creator_initialized_state(True)
    session_id = get_spark_session_id()
    session_suffix = f"_{session_id.replace('-','_')}" if session_id else ""
    udf_base = CREATE_JAVA_UDF_PREFIX + function_name + session_suffix
    # qualify_temp_object_name_str is a no-op when temp_object_schema is unset.
    name = qualify_temp_object_name_str(session, udf_base)
    result = session.sql(
        f"CALL {qualified_proc_name}('{name}', '{java_class}', ARRAY_CONSTRUCT({get_quoted_imports(session)})::ARRAY(VARCHAR))"
    ).collect()
    result_value = result[0][0]
    if not result_value:
        raise AnalysisException(f"Can not load class {java_class}")
    types = result_value.split(";")
    input_types = [type_string_to_type_object(t) for t in types[:-1]]
    output_type = types[-1]
    return JavaUdf(name, input_types, type_string_to_type_object(output_type))


def _create_java_udf_native_app(session: Session, function_name: str, java_class: str):
    """Native app mode: helper proc lives in a runtime versioned schema with relative IMPORTS.

    The version stage must contain the SCOS JARs at the relative paths returned by
    create_native_app_snowflake_imports().  UDF JARs must be bundled in the app's version
    stage and referenced via snowpark.connect.udf.java.imports as relative paths.
    addArtifact JARs are silently ignored — they are not included in IMPORTS for this path.
    """
    db = session.get_current_database()
    if not db:
        raise ValueError("A current database must be set when using native app mode")
    qualified_proc_name = f"{db}.{NATIVE_APP_VERSIONED_SCHEMA}.{PROCEDURE_NAME}"

    if not is_java_udf_creator_initialized():
        _ensure_native_app_schema(session)
        # Skip upload_java_udf_jar and ensure_scala_udf_jars_uploaded — JARs are
        # already in the app's version stage.
        session.sql(
            NATIVE_APP_SP_TEMPLATE.replace("__procedure_name__", qualified_proc_name)
            .replace("__snowflake_udf_imports__", create_native_app_snowflake_imports())
            .replace("__scala_version__", get_scala_version())
        ).collect()
        set_java_udf_creator_initialized_state(True)

    session_id = get_spark_session_id()
    session_suffix = f"_{session_id.replace('-','_')}" if session_id else ""
    udf_base = CREATE_JAVA_UDF_PREFIX + function_name + session_suffix
    # Fully qualify the UDF name so it resolves from any session schema.
    name = f"{db}.{NATIVE_APP_VERSIONED_SCHEMA}.{udf_base}"
    result = session.sql(
        f"CALL {qualified_proc_name}('{name}', '{java_class}', ARRAY_CONSTRUCT({get_relative_quoted_imports()})::ARRAY(VARCHAR))"
    ).collect()
    result_value = result[0][0]
    if not result_value:
        raise AnalysisException(f"Can not load class {java_class}")
    types = result_value.split(";")
    input_types = [type_string_to_type_object(t) for t in types[:-1]]
    output_type = types[-1]
    return JavaUdf(name, input_types, type_string_to_type_object(output_type))
