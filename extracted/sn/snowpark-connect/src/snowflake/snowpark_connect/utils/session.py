#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import logging
import os
import threading
from collections.abc import Sequence
from typing import Any

from snowflake import snowpark
from snowflake.connector.description import PLATFORM
from snowflake.snowpark.exceptions import SnowparkClientException
from snowflake.snowpark.session import _get_active_session
from snowflake.snowpark_connect.constants import DEFAULT_CONNECTION_NAME
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.describe_query_cache import (
    instrument_session_for_describe_cache,
)
from snowflake.snowpark_connect.utils.external_udxf_cache import (
    init_external_udxf_cache,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import telemetry
from snowflake.snowpark_connect.utils.udf_cache import init_builtin_udf_cache

SKIP_SESSION_CONFIGURATION = False


def skip_session_configuration(skip: bool):
    global SKIP_SESSION_CONFIGURATION
    SKIP_SESSION_CONFIGURATION = skip


# Suppress experimental warnings from snowflake.snowpark logger
def _filter_experimental_warnings(record):
    """Filter function to suppress experimental warnings."""
    message = record.getMessage()
    return not (
        "is experimental since" in message and "Do not use it in production" in message
    )


logging.getLogger("snowflake.snowpark").addFilter(_filter_experimental_warnings)


def _get_current_snowpark_session() -> snowpark.Session | None:
    # TODO: this is a temporary solution to get the current session, it would be better to add a function in snowpark
    try:
        session = _get_active_session()
        # if session._conn._conn.expired:
        #     _remove_session(session)
        #     return self.create()
        return session
    except SnowparkClientException as ex:
        if ex.error_code == "1403":  # No session
            return None
        raise


def configure_snowpark_session(session: snowpark.Session):
    """Configure a snowpark session with required parameters and settings."""
    from snowflake.snowpark_connect.config import (
        get_cte_optimization_enabled,
        global_config,
    )

    global SKIP_SESSION_CONFIGURATION

    logger.info(f"Configuring session {session}")

    telemetry.initialize(session)
    # custom udfs
    session._udfs = {}
    session._udtfs = {}
    session._sprocs = set()

    # custom udf imports
    session._python_files = set()
    session._import_files = set()
    session._artifact_jars = set()

    # custom artifact attributes
    # track current chunk
    # key: session_id, value: dict of (name, num_chunks, current_chunk_index)
    session._current_chunk: dict[str, dict] = {}
    # Use thread-safe access when modifying current chunk dictionary
    session._current_chunk_lock = threading.RLock()

    # track filenames to be uploaded to stage
    # key: session_id, value: dict of (name, filename)
    session._filenames: dict[str, dict[str, str]] = {}
    # Use thread-safe access when modifying filenames dictionary
    session._filenames_lock = threading.RLock()

    # built-in udf cache
    init_builtin_udf_cache(session)
    init_external_udxf_cache(session)

    # file format cache
    session._file_formats = set()

    # Set experimental parameters (warnings globally suppressed)
    session.ast_enabled = False
    session.eliminate_numeric_sql_value_cast_enabled = False
    session.reduce_describe_query_enabled = True

    session._join_alias_fix = True
    session.connection.arrow_number_to_decimal_setter = True
    session.custom_package_usage_config["enabled"] = True

    # Scoped temp objects may not be accessible in stored procedure and cause "object does not exist" error. So disable
    # _use_scoped_temp_objects here and use temp table instead.
    session._use_scoped_temp_objects = False

    # Configure CTE optimization based on session configuration
    cte_optimization_enabled = get_cte_optimization_enabled()
    session.cte_optimization_enabled = cte_optimization_enabled
    logger.info(f"CTE optimization enabled: {cte_optimization_enabled}")

    # Default query tag to be used unless overridden by user using AppName or spark.addTag()
    query_tag = "SNOWPARK_CONNECT_QUERY"

    default_fallback_timezone = "UTC"
    if global_config.spark_sql_session_timeZone is None:
        try:
            result = session.sql("SHOW PARAMETERS LIKE 'TIMEZONE'").collect()
            if result and len(result) > 0:
                value = result[0]["value"]
                logger.warning(
                    f"Using Snowflake session timezone parameter as fallback: {value}"
                )
            else:
                value = default_fallback_timezone
                logger.warning(
                    f"Could not determine timezone from parameters, defaulting to {default_fallback_timezone}"
                )
        except Exception as e:
            value = default_fallback_timezone
            logger.warning(
                f"Could not query Snowflake timezone parameter ({e}), defaulting to {default_fallback_timezone}"
            )
        global_config.spark_sql_session_timeZone = value

    session_params = {
        "TIMESTAMP_TYPE_MAPPING": "TIMESTAMP_LTZ",
        "TIMEZONE": f"'{global_config.spark_sql_session_timeZone}'",
        "QUOTED_IDENTIFIERS_IGNORE_CASE": "false",
        "PYTHON_SNOWPARK_ENABLE_THREAD_SAFE_SESSION": "true",
        "ENABLE_STRUCTURED_TYPES_IN_SNOWPARK_CONNECT_RESPONSE": "true",
        "QUERY_TAG": f"'{query_tag}'",
    }

    # SNOW-2245971: Stored procedures inside Native Apps run as Execute As Owner and hence cannot set session params.
    if not SKIP_SESSION_CONFIGURATION:
        session.sql(
            f"ALTER SESSION SET {', '.join([f'{k} = {v}' for k, v in session_params.items()])}"
        ).collect()
    else:
        session_param_names = ", ".join(session_params.keys())
        logger.info(
            f"Skipping Snowpark Connect session configuration as requested. Please make sure following session parameters are set correctly: {session_param_names}"
        )

    # Instrument the snowpark session to use a cache for describe queries.
    instrument_session_for_describe_cache(session)


def _is_running_in_SPCS():
    return (
        os.path.exists("/snowflake/session/token")
        and os.getenv("SNOWFLAKE_ACCOUNT") is not None
        and os.getenv("SNOWFLAKE_HOST") is not None
    )


def _is_running_in_stored_procedure_or_notebook():
    return PLATFORM == "XP"


def _get_session_configs_from_ENV() -> dict[str, Any]:
    session_configs = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "protocol": "https",
        "host": os.getenv("SNOWFLAKE_HOST"),
        "port": os.getenv("SNOWFLAKE_PORT", 443),
        "authenticator": "oauth",
        "token_file_path": "/snowflake/session/token",
        "client_session_keep_alive": True,
    }
    return session_configs


def get_or_create_snowpark_session(
    custom_configs: dict | None = None,
) -> snowpark.Session:
    """
    snowpark connect code should use this function to create or get snowpark session
    """
    session_configs = {}
    if _is_running_in_SPCS():
        # Running in SPCS, use environment variables injected by SPCS run time
        # We don't use connections.toml file created by SPCS because of the 0600 permissions issue
        session_configs = _get_session_configs_from_ENV()
    else:
        session_configs["connection_name"] = DEFAULT_CONNECTION_NAME

    if os.getenv("SNOWFLAKE_DATABASE") is not None:
        session_configs["database"] = os.getenv("SNOWFLAKE_DATABASE")

    if os.getenv("SNOWFLAKE_SCHEMA") is not None:
        session_configs["schema"] = os.getenv("SNOWFLAKE_SCHEMA")

    if os.getenv("SNOWFLAKE_WAREHOUSE") is not None:
        session_configs["warehouse"] = os.getenv("SNOWFLAKE_WAREHOUSE")

    # add custom session configs
    if custom_configs:
        session_configs.update(custom_configs)

    old_session = _get_current_snowpark_session()
    new_session = snowpark.Session.builder.configs(session_configs).getOrCreate()
    if old_session is None or old_session.session_id != new_session.session_id:
        # every new session needs to be configured
        configure_snowpark_session(new_session)

    return new_session


def set_query_tags(spark_tags: Sequence[str]) -> None:
    """Sets Snowpark session query_tag value to the tag from the Spark request."""

    if any("," in tag for tag in spark_tags):
        exception = ValueError("Tags cannot contain ','.")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # TODO: Tags might not be set correctly in parallel workloads or multi-threaded code.
    snowpark_session = get_or_create_snowpark_session()
    spark_tags_str = ",".join(sorted(spark_tags)) if spark_tags else None

    if spark_tags_str and spark_tags_str != snowpark_session.query_tag:
        snowpark_session.query_tag = spark_tags_str
