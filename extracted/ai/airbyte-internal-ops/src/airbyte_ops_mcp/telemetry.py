# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Telemetry module for tracking usage analytics.

This module provides utilities for tracking usage of various Airbyte operations
using Segment analytics. The tracking is optional and can be disabled via
environment variables.

Based on the legacy connector_live_tests/commons/segment_tracking.py implementation.
"""

from __future__ import annotations

import logging
import os
from typing import Any

try:
    from segment import analytics  # type: ignore[import-untyped]

    SEGMENT_AVAILABLE = True
except ImportError:
    analytics = None  # type: ignore[assignment]
    SEGMENT_AVAILABLE = False

logger = logging.getLogger(__name__)

# Environment variable to disable tracking
DISABLE_TRACKING_ENV_VAR = "AIRBYTE_DISABLE_TELEMETRY"
# Legacy env var for backward compatibility
LEGACY_DISABLE_TRACKING_ENV_VAR = "REGRESSION_TEST_DISABLE_TRACKING"
# Environment variable to enable debug mode
DEBUG_SEGMENT_ENV_VAR = "DEBUG_SEGMENT"

# Segment write key environment variable name
# The write key can be provided via environment variable or uses the default
# public key for the Airbyte analytics project. Segment write keys are designed
# to be embedded in client-side code for analytics tracking.
SEGMENT_WRITE_KEY_ENV_VAR = "SEGMENT_WRITE_KEY"
_DEFAULT_SEGMENT_WRITE_KEY = "hnWfMdEtXNKBjvmJ258F72wShsLmcsZ8"


def _is_tracking_enabled() -> bool:
    """Check if tracking is enabled based on environment variables."""
    if os.getenv(DISABLE_TRACKING_ENV_VAR) is not None:
        return False
    return os.getenv(LEGACY_DISABLE_TRACKING_ENV_VAR) is None


def _on_error(error: Exception, items: Any) -> None:
    """Handle Segment tracking errors."""
    logger.warning("An error occurred in Segment Tracking", exc_info=error)


def _initialize_analytics() -> bool:
    """Initialize Segment analytics if available and enabled.

    Returns:
        True if analytics was initialized successfully, False otherwise.
    """
    if not SEGMENT_AVAILABLE:
        logger.debug("Segment analytics not available (package not installed)")
        return False

    if not _is_tracking_enabled():
        logger.debug("Telemetry tracking is disabled via environment variable")
        return False

    # Use environment variable if set, otherwise use default public key
    write_key = os.getenv(SEGMENT_WRITE_KEY_ENV_VAR, _DEFAULT_SEGMENT_WRITE_KEY)
    analytics.write_key = write_key
    analytics.send = True
    analytics.debug = os.getenv(DEBUG_SEGMENT_ENV_VAR) is not None
    analytics.on_error = _on_error
    return True


def track_regression_test(
    user_id: str | None,
    connector_image: str,
    command: str,
    target_version: str,
    control_version: str | None = None,
    additional_properties: dict[str, Any] | None = None,
) -> None:
    """Track a regression test execution.

    Args:
        user_id: The user ID to associate with the event. If None, uses "airbyte-ci".
        connector_image: The connector image being tested.
        command: The Airbyte command being run (spec, check, discover, read).
        target_version: The target connector version being tested.
        control_version: The control connector version (for comparison mode).
        additional_properties: Additional properties to include in the event.
    """
    if not _initialize_analytics():
        return

    if not user_id:
        user_id = "airbyte-ci"

    analytics.identify(user_id)

    properties: dict[str, Any] = {
        "connector_image": connector_image,
        "command": command,
        "target_version": target_version,
    }

    if control_version:
        properties["control_version"] = control_version
        properties["test_mode"] = "comparison"
    else:
        properties["test_mode"] = "single_version"

    if additional_properties:
        properties.update(additional_properties)

    try:
        from importlib.metadata import version

        properties["package_version"] = version("airbyte-ops-mcp")
    except Exception:
        properties["package_version"] = "unknown"

    analytics.track(user_id, "regression_test_start", properties)
    logger.debug(f"Tracked regression_test_start event for user {user_id}")


def track_event(
    user_id: str | None,
    event_name: str,
    properties: dict[str, Any] | None = None,
) -> None:
    """Track a generic event.

    This is a general-purpose tracking function for events that don't fit
    into the more specific tracking functions.

    Args:
        user_id: The user ID to associate with the event. If None, uses "airbyte-ci".
        event_name: The name of the event to track.
        properties: Properties to include in the event.
    """
    if not _initialize_analytics():
        return

    if not user_id:
        user_id = "airbyte-ci"

    analytics.identify(user_id)

    event_properties = properties or {}

    try:
        from importlib.metadata import version

        event_properties["package_version"] = version("airbyte-ops-mcp")
    except Exception:
        event_properties["package_version"] = "unknown"

    analytics.track(user_id, event_name, event_properties)
    logger.debug(f"Tracked {event_name} event for user {user_id}")
