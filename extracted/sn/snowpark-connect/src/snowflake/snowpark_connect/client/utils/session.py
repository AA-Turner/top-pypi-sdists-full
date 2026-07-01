#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Minimal session utilities for Snowpark Connect Client.

This is a simplified version that doesn't require heavy dependencies
like config, telemetry, UDF caches, etc.
"""

import os

from snowflake import snowpark
from snowflake.snowpark.exceptions import SnowparkClientException
from snowflake.snowpark.session import _get_active_session
from snowflake.snowpark_connect.constants import DEFAULT_CONNECTION_NAME
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def _get_current_snowpark_session() -> snowpark.Session | None:
    """Get the current active Snowpark session if one exists."""
    try:
        session = _get_active_session()
        return session
    except SnowparkClientException as ex:
        if ex.error_code == "1403":  # No session
            return None
        raise


def _is_running_in_SPCS():
    """Check if running in Snowpark Container Services."""
    return (
        os.path.exists("/snowflake/session/token")
        and os.getenv("SNOWFLAKE_ACCOUNT") is not None
        and os.getenv("SNOWFLAKE_HOST") is not None
    )


def _get_session_configs_from_ENV() -> dict:
    """Get session configuration from environment variables (for SPCS)."""
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
    Get or create a Snowpark session for the client.

    This is a simplified version that doesn't configure all the SAS-specific
    settings (telemetry, UDF caches, etc.) since the client doesn't need them.
    """
    session_configs = {}
    if _is_running_in_SPCS():
        session_configs = _get_session_configs_from_ENV()
    else:
        session_configs["connection_name"] = DEFAULT_CONNECTION_NAME

    if os.getenv("SNOWFLAKE_DATABASE") is not None:
        session_configs["database"] = os.getenv("SNOWFLAKE_DATABASE")

    if os.getenv("SNOWFLAKE_SCHEMA") is not None:
        session_configs["schema"] = os.getenv("SNOWFLAKE_SCHEMA")

    if os.getenv("SNOWFLAKE_WAREHOUSE") is not None:
        session_configs["warehouse"] = os.getenv("SNOWFLAKE_WAREHOUSE")

    if custom_configs:
        session_configs.update(custom_configs)

    session = snowpark.Session.builder.configs(session_configs).getOrCreate()
    logger.info(f"Created Snowpark session: {session.session_id}")

    return session
