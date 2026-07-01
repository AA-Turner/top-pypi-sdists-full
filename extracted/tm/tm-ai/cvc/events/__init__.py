"""CVC Event Spine — append-only ledger of every interaction.

See ``spine.py`` for the implementation. This package init just re-exports
the public API for convenience::

    from cvc.events import capture, query, capture_block, spine_info
    from cvc.events.chat_capture import ChatCapture
"""
from __future__ import annotations

from cvc.events.chat_capture import ChatCapture
from cvc.events.spine import (
    capture,
    capture_block,
    count,
    init,
    purge_older_than,
    query,
    rotate_if_needed,
    spine_info,
    stats_by_channel,
    stats_by_day,
    stats_by_kind,
)

__all__ = [
    "capture",
    "capture_block",
    "ChatCapture",
    "count",
    "init",
    "purge_older_than",
    "query",
    "rotate_if_needed",
    "spine_info",
    "stats_by_channel",
    "stats_by_day",
    "stats_by_kind",
]