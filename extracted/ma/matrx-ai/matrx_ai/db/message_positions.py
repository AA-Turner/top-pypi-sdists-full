"""Database-owned message-position allocation contract.

Normal append writers send this sentinel instead of guessing a transcript
coordinate from a model-visible list. The database trigger installed by
``0174_cx_message_atomic_position_allocator.sql`` serializes writers per
conversation and replaces the sentinel with ``max(live position) + 1``.

Explicit-position operations such as fork and compaction deliberately do not
use this value; their non-negative positions pass through the trigger intact.
"""

APPEND_MESSAGE_POSITION = -1

__all__ = ["APPEND_MESSAGE_POSITION"]
