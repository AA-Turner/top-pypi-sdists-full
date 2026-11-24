"""Database-owned message-position allocation contract.

Normal append writers send this sentinel instead of guessing a transcript
coordinate from a model-visible list. The database trigger installed by
``0174_cx_message_atomic_position_allocator.sql`` serializes writers per
conversation and replaces the sentinel with one past the highest position the conversation
has ever used (deleted rows included; positions are never reused).

Explicit-position operations such as fork and compaction deliberately do not
use this value; their non-negative positions pass through the trigger intact.
"""

APPEND_MESSAGE_POSITION = -1

# The sentinel is a request, not a value: an exact comparison of a landed row
# (replay, immutable verify) must accept whatever position the trigger chose.
# matrx-orm is imported lazily-safe here: it is absent only in a client host
# with no ORM, where no exact comparison runs.
try:
    from matrx_orm import declare_db_assigned_sentinel
except ImportError:  # pragma: no cover — client host without matrx-orm
    pass
else:
    declare_db_assigned_sentinel("chat.message", "position", APPEND_MESSAGE_POSITION)

__all__ = ["APPEND_MESSAGE_POSITION"]
