"""Host-supplied metadata for a turn's ``chat.request_snapshot`` row.

A host stages a JSON-safe dict on ``AppContext.metadata[REQUEST_SNAPSHOT_METADATA_KEY]`` while it
prepares a turn; the executor writes it into the snapshot's ``metadata`` column on the turn's
first iteration only (one copy per turn, never per tool round). aidream uses it to keep what the
``context`` tool returns for each on-request value of the turn — text that is, by definition, not
in the provider request — so its context viewer can serve it later (common-docs
context-delivery RULES.md §5b).
"""

from __future__ import annotations

from typing import Any

REQUEST_SNAPSHOT_METADATA_KEY = "request_snapshot_metadata"


def snapshot_metadata_for(exec_ctx: Any, iteration: int) -> dict[str, Any] | None:
    """The staged metadata for this snapshot, or None (later iterations, nothing staged)."""
    if iteration != 1:
        return None
    metadata = getattr(exec_ctx, "metadata", None)
    if not isinstance(metadata, dict):
        return None
    staged = metadata.get(REQUEST_SNAPSHOT_METADATA_KEY)
    return dict(staged) if isinstance(staged, dict) and staged else None


__all__ = ["REQUEST_SNAPSHOT_METADATA_KEY", "snapshot_metadata_for"]
