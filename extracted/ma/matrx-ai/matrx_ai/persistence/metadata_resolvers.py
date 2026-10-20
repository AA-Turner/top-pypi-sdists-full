"""Turn-end resolvers for keys inside ``chat.conversation.metadata``.

A feature that keeps a record in the conversation's metadata and lets the PERSON edit it while a turn runs
has a race: the turn's queued copy was read before the edit, and the flush writes the queued copy whole, so
an edit made after the turn's last write of that key was put back to the old text when the turn ended
(Agent Studio workspace, 2026-10-18). The key's owner registers ONE resolver; the coordinator calls it for
every queued metadata op that carries the key, right before the flush, with the queued value and gets the
value to write. Resolvers are bounded and never fail a flush: a resolver that raises or times out leaves the
queued value as it was, and says so.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_ai.persistence.registry import get_model

logger = logging.getLogger(__name__)

#: ``(conversation_id, queued_value) -> value to write``
MetadataResolver = Callable[[str, Any], Awaitable[Any]]

_RESOLVERS: dict[str, MetadataResolver] = {}


def register_conversation_metadata_resolver(key: str, resolver: MetadataResolver) -> None:
    """Register (or replace) the turn-end resolver for ``metadata[key]``."""
    _RESOLVERS[key] = resolver


async def resolve_pending_conversation_metadata(session: Any) -> None:
    """Rewrite each queued conversation metadata op's registered keys through their resolver, in place."""
    if not _RESOLVERS:
        return
    # A resolver may not outlast the commit's own bound.
    from matrx_ai.persistence.coordinator import _COMMIT_HARD_DEADLINE_SECONDS

    try:
        ops = session.pending_ops_for(get_model("chat.conversation"))
    except Exception as exc:  # noqa: BLE001 — never fail the flush, but never be silent about it
        logger.error("conversation metadata resolvers skipped: no pending view (%s: %s)", type(exc).__name__, exc)
        return
    for op in ops:
        if getattr(op, "op_type", None) == "delete":
            continue
        meta = (getattr(op, "payload", None) or {}).get("metadata")
        if not isinstance(meta, dict):
            continue
        for key, resolver in _RESOLVERS.items():
            if key not in meta:
                continue
            try:
                meta[key] = await asyncio.wait_for(
                    resolver(str(getattr(op, "pk_value", "")), meta[key]), _COMMIT_HARD_DEADLINE_SECONDS
                )
            except Exception as exc:  # noqa: BLE001 — a resolver never fails the flush
                logger.error(
                    "conversation metadata resolver for %r failed on %s (%s: %s) — the queued value is written as it was",
                    key, getattr(op, "pk_value", "?"), type(exc).__name__, exc,
                )
