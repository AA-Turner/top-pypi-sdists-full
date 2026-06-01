# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Sentry error tracking integration for airbyte-ops-mcp.

This module provides automatic error tracking via Sentry for the airbyte-ops-mcp
package. Errors during server startup, tool execution, and API interactions are
automatically captured and reported.

The Sentry DSN is embedded in the package since it only allows write access
(sending errors), not read access. This is standard practice for client-side
error tracking.

To disable Sentry tracking, set the environment variable:
    AIRBYTE_DISABLE_SENTRY=1
"""

import logging
import os
from typing import Literal

import sentry_sdk

# Valid Sentry severity levels
SentryLevel = Literal["fatal", "error", "warning", "info", "debug"]

logger = logging.getLogger(__name__)

# Environment variable to disable Sentry tracking
DISABLE_SENTRY_ENV_VAR = "AIRBYTE_DISABLE_SENTRY"

# Sentry DSN for the airbyte-ops-mcp project
# This DSN only allows sending errors to Sentry, not reading data.
# It is safe to embed in client-side code per Sentry's documentation.
# Project: https://airbytehq.sentry.io/projects/internal-ops-app/
_SENTRY_DSN = "https://292842cbf7f632f34c68cff23f2deee3@o1009025.ingest.us.sentry.io/4510746336559104"

_sentry_initialized = False


def _get_package_version() -> str:
    """Get the package version for Sentry release tracking."""
    try:
        from importlib.metadata import version

        return version("airbyte-internal-ops")
    except Exception as exc:
        logger.debug("Failed to get package version for Sentry release", exc_info=exc)
        return "unknown"


def init_sentry_tracking() -> bool:
    """Initialize Sentry error tracking if not already initialized.

    Returns:
        True if Sentry was initialized successfully, False otherwise.
    """
    global _sentry_initialized

    if _sentry_initialized:
        return True

    if os.getenv(DISABLE_SENTRY_ENV_VAR):
        logger.debug("Sentry tracking is disabled via environment variable")
        return False

    try:
        sentry_sdk.init(
            dsn=_SENTRY_DSN,
            release=f"airbyte-ops-mcp@{_get_package_version()}",
            environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
            # Only send errors, not performance data
            traces_sample_rate=0.0,
            # Attach request data for better debugging
            send_default_pii=False,
            # Set server name to help identify the source
            server_name=os.getenv("HOSTNAME", "unknown"),
        )
        _sentry_initialized = True
        logger.debug("Sentry initialized successfully")
        return True
    except Exception as e:
        logger.warning(f"Failed to initialize Sentry: {e}")
        return False


def capture_exception(exception: BaseException) -> None:
    """Capture an exception and send it to Sentry.

    This is a convenience wrapper that ensures Sentry is initialized
    before capturing the exception.
    """
    if init_sentry_tracking():
        sentry_sdk.capture_exception(exception)


def capture_message(message: str, level: SentryLevel = "info") -> None:
    """Capture a message and send it to Sentry.

    This is useful for logging important events that aren't exceptions.
    """
    if init_sentry_tracking():
        sentry_sdk.capture_message(message, level=level)
