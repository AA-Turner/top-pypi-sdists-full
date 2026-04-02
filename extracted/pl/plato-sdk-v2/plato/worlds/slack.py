"""Slack notification helpers for durable stages.

.. deprecated::
    Slack notifications are now handled server-side by Chronos when stage
    events are reported. This module provides backward-compatible aliases
    for ``enable_stage_tracking`` / ``disable_stage_tracking``.
"""

from __future__ import annotations

import contextvars
import logging
from typing import Any

from plato.worlds.stage_tracking import (
    StageTrackingContext,
    disable_stage_tracking,
    enable_stage_tracking,
)

logger = logging.getLogger(__name__)


def enable_slack_notifications(
    api_key: str | None = None,
    base_url: str | None = None,
    formatter: Any = None,
    session_id: str = "",
    chronos_url: str = "",
) -> contextvars.Token[StageTrackingContext | None]:
    """Enable stage tracking (and server-side Slack notifications).

    This is a backward-compatible alias for :func:`enable_stage_tracking`.
    The ``formatter`` parameter is accepted but ignored — message formatting
    is now handled by the Chronos backend.
    """
    return enable_stage_tracking(
        session_id=session_id,
        base_url=base_url or chronos_url or None,
        api_key=api_key,
    )


def disable_slack_notifications(
    token: contextvars.Token[StageTrackingContext | None],
) -> None:
    """Disable stage tracking. Backward-compatible alias."""
    disable_stage_tracking(token)
