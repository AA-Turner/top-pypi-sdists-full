# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Admin authentication and validation for internal Airbyte operations.

This module provides functions for validating internal admin access for privileged
operations. General Cloud authentication is handled by PyAirbyte's airbyte.cloud.auth module.
"""

from __future__ import annotations

import logging
import os

from airbyte import constants as airbyte_constants
from fastmcp.server.dependencies import get_access_token

from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.constants import (
    ENV_AIRBYTE_INTERNAL_ADMIN_FLAG,
    ENV_AIRBYTE_INTERNAL_ADMIN_USER,
    EXPECTED_ADMIN_EMAIL_DOMAIN,
    EXPECTED_ADMIN_FLAG_VALUE,
)

logger = logging.getLogger(__name__)


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


def _resolve_oidc_user_email() -> str | None:
    """Extract the authenticated user's email from the OIDC access token.

    In hosted mode (OIDCProxy via Keycloak), the upstream access token
    contains JWT claims including `email`. This function retrieves that
    claim so admin tools can identify the logged-in user without requiring
    the `AIRBYTE_INTERNAL_ADMIN_USER` env var.

    Returns `None` when no OIDC session is active (e.g. stdio mode) or
    when the token has no `email` claim.
    """
    access_token = get_access_token()
    if access_token is None:
        return None

    claims: dict[str, object] = getattr(access_token, "claims", {})
    email = claims.get("email")
    if isinstance(email, str) and email.strip():
        return email.strip()

    return None


def get_admin_user_email() -> str:
    """Get the admin user email, resolving from OIDC token or environment.

    Resolution order:
    1. `AIRBYTE_INTERNAL_ADMIN_USER` env var (local/stdio mode)
    2. OIDC access token `email` claim (hosted mode via Keycloak)

    When the email comes from OIDC, only `AIRBYTE_INTERNAL_ADMIN_FLAG` is
    required (not the full `require_internal_admin` check which also demands
    the env var).

    Returns:
        The admin user email address.

    Raises:
        CloudAuthError: If admin credentials are not properly configured.
    """
    # Path 1: env var is set — use the existing full admin check
    admin_user = os.environ.get(ENV_AIRBYTE_INTERNAL_ADMIN_USER)
    if admin_user:
        require_internal_admin()
        return admin_user

    # Path 2: no env var — try OIDC token email (hosted mode)
    require_internal_admin_flag_only()
    oidc_email = _resolve_oidc_user_email()
    if oidc_email:
        if EXPECTED_ADMIN_EMAIL_DOMAIN not in oidc_email:
            raise CloudAuthError(
                f"OIDC user email '{oidc_email}' is not an "
                f"{EXPECTED_ADMIN_EMAIL_DOMAIN} address."
            )
        logger.info("Resolved admin user email from OIDC token: %s", oidc_email)
        return oidc_email

    raise CloudAuthError(
        f"{ENV_AIRBYTE_INTERNAL_ADMIN_USER} is not set and no OIDC session is active. "
        f"Set {ENV_AIRBYTE_INTERNAL_ADMIN_USER}=<your-email{EXPECTED_ADMIN_EMAIL_DOMAIN}> "
        f"or authenticate via OIDC."
    )


def get_admin_user_id(
    *,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> str:
    """Resolve the admin user UUID from env var or OIDC token.

    Combines `get_admin_user_email` with `api_client.get_user_id_by_email` to
    look up the UUID for the admin email address. The inner
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
