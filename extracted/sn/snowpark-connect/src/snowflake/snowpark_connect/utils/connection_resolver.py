#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Connection resolution utilities for Snowpark Connect.

This module provides connection name resolution from connections.toml,
following the standard Snowflake connection resolution behavior.

Why this module exists:
    Snowpark's Session.builder.getOrCreate() does NOT properly honor the
    `default_connection_name` setting from connections.toml. When no connection_name
    is specified, Snowpark looks for a connection literally named 'default' rather
    than using the value of `default_connection_name`.

    This module correctly reads `default_connection_name` from CONFIG_MANAGER["connections"]
    and resolves to the appropriate connection name before passing it to Snowpark.
"""

import os

from snowflake.snowpark_connect.constants import DEFAULT_CONNECTION_NAME
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def resolve_connection_name() -> str:
    """
    Resolve the connection name to use from connections.toml.

    Resolution priority:
    1. If "spark-connect" connection exists, use it (backwards compatible)
    2. Use SNOWFLAKE_DEFAULT_CONNECTION_NAME env var if set
    3. Use default_connection_name from connections.toml/config.toml
    4. If a connection named "default" exists, use it
    5. Otherwise, raise an error

    Returns:
        The resolved connection name to use, or None if no connections.toml exists
        (e.g., in Snowflake Notebook environments where a session already exists).

    Raises:
        RuntimeError: If connections.toml exists but no valid connection can be resolved.
    """
    try:
        from snowflake.connector.config_manager import CONFIG_MANAGER

        # Access connections using bracket notation (CONFIG_MANAGER is a special object)
        try:
            connections = CONFIG_MANAGER["connections"]
        except KeyError:
            # No connections.toml - this is OK in environments like Snowflake Notebooks
            # where a session already exists. Return None to let Snowpark handle it.
            logger.debug(
                "No connections.toml found. Will use existing session or Snowpark defaults."
            )
            return None

        # Get the list of available connection names
        # Filter out 'default_connection_name' as it's a setting, not a connection
        if hasattr(connections, "keys"):
            available_connections = [
                k for k in connections.keys() if k != "default_connection_name"
            ]
        else:
            # Fallback if connections is not dict-like
            available_connections = []

        if not available_connections:
            # connections.toml exists but has no connections - same as no file
            logger.debug(
                "No connections found in connections.toml. "
                "Will use existing session or Snowpark defaults."
            )
            return None

        # Priority 1: Use "spark-connect" if it exists (backwards compatible)
        if DEFAULT_CONNECTION_NAME in available_connections:
            logger.debug(
                f"Using connection '{DEFAULT_CONNECTION_NAME}' from connections.toml"
            )
            return DEFAULT_CONNECTION_NAME

        # Priority 2: Check SNOWFLAKE_DEFAULT_CONNECTION_NAME env var
        env_default = os.environ.get("SNOWFLAKE_DEFAULT_CONNECTION_NAME")
        if env_default and env_default in available_connections:
            logger.debug(
                f"Using connection '{env_default}' from SNOWFLAKE_DEFAULT_CONNECTION_NAME env var"
            )
            return env_default

        # Priority 3: Use default_connection_name from connections.toml
        # In connections.toml format, default_connection_name is inside the connections dict
        default_conn_name = None
        if hasattr(connections, "get"):
            default_conn_name = connections.get("default_connection_name")

        if default_conn_name and default_conn_name in available_connections:
            logger.debug(
                f"Using default connection '{default_conn_name}' from connections.toml"
            )
            return default_conn_name

        # Priority 4: Use connection named "default" if it exists
        if "default" in available_connections:
            logger.debug("Using connection 'default' from connections.toml")
            return "default"

        # Priority 5: Error - no valid default found
        raise RuntimeError(
            "No 'spark-connect' connection found and no default connection is configured. "
            "Please either:\n"
            "  1. Create a connection named 'spark-connect', or\n"
            "  2. Set 'default_connection_name' in your connections.toml, or\n"
            "  3. Set SNOWFLAKE_DEFAULT_CONNECTION_NAME environment variable, or\n"
            "  4. Create a connection named 'default'"
        )

    except ImportError:
        # If CONFIG_MANAGER is not available, fall back to default
        logger.warning(
            "Could not import CONFIG_MANAGER. Falling back to default connection name."
        )
        return DEFAULT_CONNECTION_NAME
    except RuntimeError:
        # Re-raise RuntimeError (our custom errors about no connections)
        raise
    except Exception as e:
        # Log unexpected errors and re-raise to let session creation handle it
        logger.error(f"Unexpected error resolving connection name: {e}")
        raise
