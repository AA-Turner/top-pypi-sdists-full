# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Admin authentication and validation for internal Airbyte operations.

This module provides functions for validating internal admin access for privileged
operations. General Cloud authentication is handled by PyAirbyte's airbyte.cloud.auth module.
"""

from __future__ import annotations

import os

from airbyte import constants as airbyte_constants

from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.constants import (
    ENV_AIRBYTE_INTERNAL_ADMIN_FLAG,
    ENV_AIRBYTE_INTERNAL_ADMIN_USER,
    EXPECTED_ADMIN_EMAIL_DOMAIN,
    EXPECTED_ADMIN_FLAG_VALUE,
)


class CloudAuthError(Exception):
    """Raised when admin authentication validation fails."""

    pass


def check_internal_admin_flag() -> bool:
    """Check if internal admin flag is properly configured.

    This validates that both AIRBYTE_INTERNAL_ADMIN_FLAG and
    AIRBYTE_INTERNAL_ADMIN_USER are set correctly for admin operations.

    Returns:
        True if both environment variables are set correctly, False otherwise
    """
    admin_flag = os.environ.get(ENV_AIRBYTE_INTERNAL_ADMIN_FLAG)
    admin_user = os.environ.get(ENV_AIRBYTE_INTERNAL_ADMIN_USER)

    if admin_flag != EXPECTED_ADMIN_FLAG_VALUE:
        return False

    return bool(admin_user and EXPECTED_ADMIN_EMAIL_DOMAIN in admin_user)


def check_internal_admin_flag_only() -> bool:
    """Check if internal admin flag is set (without requiring user email env var).

    This is a lighter check that only validates AIRBYTE_INTERNAL_ADMIN_FLAG,
    allowing the admin user email to be provided as a parameter instead of
    an environment variable.

    Returns:
        True if AIRBYTE_INTERNAL_ADMIN_FLAG is set correctly, False otherwise
    """
    admin_flag = os.environ.get(ENV_AIRBYTE_INTERNAL_ADMIN_FLAG)
    return admin_flag == EXPECTED_ADMIN_FLAG_VALUE


def require_internal_admin() -> None:
    """Require internal admin access for the current operation.

    This function validates that the user has proper admin credentials
    configured via environment variables.

    Raises:
        CloudAuthError: If admin credentials are not properly configured
    """
    if not check_internal_admin_flag():
        raise CloudAuthError(
            "This operation requires internal admin access. "
            f"Set {ENV_AIRBYTE_INTERNAL_ADMIN_FLAG}={EXPECTED_ADMIN_FLAG_VALUE} and "
            f"{ENV_AIRBYTE_INTERNAL_ADMIN_USER}=<your-email{EXPECTED_ADMIN_EMAIL_DOMAIN}> "
            "environment variables."
        )


def require_internal_admin_flag_only() -> None:
    """Require internal admin flag for the current operation.

    This is a lighter check that only validates AIRBYTE_INTERNAL_ADMIN_FLAG,
    allowing the admin user email to be provided as a parameter instead of
    an environment variable.

    Raises:
        CloudAuthError: If AIRBYTE_INTERNAL_ADMIN_FLAG is not properly configured
    """
    if not check_internal_admin_flag_only():
        raise CloudAuthError(
            "This operation requires internal admin access. "
            f"Set {ENV_AIRBYTE_INTERNAL_ADMIN_FLAG}={EXPECTED_ADMIN_FLAG_VALUE} "
            "environment variable."
        )


def get_admin_user_email() -> str:
    """Get the admin user email from environment.

    This function validates admin access and returns the configured
    admin user email address.

    Returns:
        The admin user email address

    Raises:
        CloudAuthError: If admin credentials are not properly configured
    """
    require_internal_admin()
    admin_user = os.environ.get(ENV_AIRBYTE_INTERNAL_ADMIN_USER)
    if not admin_user:
        # This should never happen after require_internal_admin(), but be defensive
        raise CloudAuthError(f"{ENV_AIRBYTE_INTERNAL_ADMIN_USER} is not set")
    return admin_user


def get_admin_user_id(
    *,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> str:
    """Resolve the admin user UUID from the `AIRBYTE_INTERNAL_ADMIN_USER` env var.

    Combines `get_admin_user_email` with `api_client.get_user_id_by_email` to
    look up the UUID for the configured admin email address. The inner
    `get_user_id_by_email` call is LRU-cached, so repeated invocations
    within the same process avoid redundant API round-trips.
    """
    admin_email = get_admin_user_email()
    return api_client.get_user_id_by_email(
        email=admin_email,
        config_api_root=airbyte_constants.CLOUD_CONFIG_API_ROOT,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )
