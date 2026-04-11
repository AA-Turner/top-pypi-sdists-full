#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import logging
import os
from collections.abc import Sequence
from typing import Any

from snowflake import snowpark
from snowflake.connector.description import PLATFORM
from snowflake.snowpark.exceptions import SnowparkClientException, SnowparkSQLException
from snowflake.snowpark.session import _get_active_session
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.describe_query_cache import (
    instrument_session_for_describe_cache,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import (
    init_spark_session_cache_registry,
)
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
    session._sprocs = set()

    # built-in udf cache
    init_builtin_udf_cache(session)
    init_spark_session_cache_registry(session)

    # file format cache
    session._file_formats = set()

    # Set experimental parameters (warnings globally suppressed)
    session.ast_enabled = False
    session.eliminate_numeric_sql_value_cast_enabled = False
    session.reduce_describe_query_enabled = True

    session._join_alias_fix = True
    session.connection.arrow_number_to_decimal_setter = True
    session.custom_package_usage_config["enabled"] = True

    # TODO(SNOW-3122222): Remove this once 10.6 is fully rolled out
    session._has_structured_try_cast = False

    # Scoped temp objects may not be accessible in stored procedure and cause "object does not exist" error. So disable
    # _use_scoped_temp_objects here and use temp table instead.
    session._use_scoped_temp_objects = False

    # Configure CTE optimization based on session configuration
    cte_optimization_enabled = get_cte_optimization_enabled()
    session.cte_optimization_enabled = cte_optimization_enabled
    logger.debug(f"CTE optimization enabled: {cte_optimization_enabled}")

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

    # SNOW-3316643: Enable SCOS feature flag on CI (Jenkins sfctest0/qa6/preprod6) only.
    # Phase 2: enable by default once the GS-side public session parameter fix lands.
    _conn_param_file = os.environ.get("CONN_PARAM_FILE", "")
    if "SAS_DAILY_JENKINS" in os.environ or any(
        env in _conn_param_file for env in ("sfctest0", "preprod", "qa")
    ):
        session_params["ENABLE_SCOS_FEATURE"] = "true"

    # SNOW-2245971: Stored procedures inside Native Apps run as Execute As Owner and hence cannot set session params.
    if not SKIP_SESSION_CONFIGURATION:
        session.sql(
            f"ALTER SESSION SET {', '.join([f'{k} = {v}' for k, v in session_params.items()])}"
        ).collect()
        # TODO(SNOW-3122222): Move this to the `session_params` dict and remove the session variable
        # once 10.6 is fully rolled out
        try:
            result = session.sql(
                "ALTER SESSION SET ENABLE_TRY_CAST_STRUCTURED_TYPES = true"
            ).collect()
            session._has_structured_try_cast = (
                len(result) == 1
                and hasattr(result[0], "status")
                and result[0].status == "Statement executed successfully."
            )
        except SnowparkSQLException:
            # If the query failed, that means the parameter is not available, and we cannot use TRY_CAST
            # in JSON casting operations.
            pass
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
    snowpark connect code should use this function to create or get snowpark session.

    Connection resolution (when not in SPCS):
    1. Use 'spark-connect' connection if it exists (backwards compatible)
    2. Use SNOWFLAKE_DEFAULT_CONNECTION_NAME env var if set
    3. Use default_connection_name from connections.toml if set
    4. Use 'default' connection if it exists
    5. If no connections.toml exists (e.g., Snowflake Notebooks), use existing session
    6. Error if connections.toml exists but no valid connection is configured
    """
    # Fast path: if a session already exists and no custom configs are requested,
    # return it immediately without running the connection resolver.
    # This avoids repeatedly reading connections.toml on every request.
    if custom_configs is None:
        existing_session = _get_current_snowpark_session()
        if existing_session is not None:
            return existing_session

    session_configs = {}
    if _is_running_in_SPCS():
        # Running in SPCS, use environment variables injected by SPCS run time
        # We don't use connections.toml file created by SPCS because of the 0600 permissions issue
        session_configs = _get_session_configs_from_ENV()
    elif not (custom_configs and "connection_name" in custom_configs):
        # Only resolve connection name if not explicitly provided in custom_configs.
        # Uses our custom resolver which properly handles default_connection_name
        # from connections.toml (Snowpark's built-in resolution has issues)
        from snowflake.snowpark_connect.utils.connection_resolver import (
            resolve_connection_name,
        )

        resolved_connection = resolve_connection_name()
        if resolved_connection is not None:
            session_configs["connection_name"] = resolved_connection
        # If None, don't set connection_name - let Snowpark use existing session or defaults

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
