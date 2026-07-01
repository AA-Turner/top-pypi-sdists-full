#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Environment variable utilities for Snowpark Connect.
"""

import os

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def get_int_from_env(env_var: str, default: int) -> int:
    """
    Safely get integer value from environment variable with fallback to default.

    Args:
        env_var: Environment variable name
        default: Default integer value if env var is not set or invalid

    Returns:
        Integer value from environment variable or default

    Raises:
        TypeError: If default is not an integer

    Examples:
        >>> get_int_from_env("MAX_WORKERS", 10)
        10
        >>> os.environ["MAX_WORKERS"] = "20"
        >>> get_int_from_env("MAX_WORKERS", 10)
        20
        >>> os.environ["MAX_WORKERS"] = "invalid"
        >>> get_int_from_env("MAX_WORKERS", 10)  # logs warning, returns 10
        10
    """
    # Validate that default is actually an integer
    if not isinstance(default, int):
        exception = TypeError(
            f"Default value must be an integer, got {type(default).__name__}: {default}"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    value = os.getenv(env_var)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        logger.warning(
            f"Invalid integer value for environment variable {env_var}: '{value}', "
            f"using default: {default}"
        )
        return default
