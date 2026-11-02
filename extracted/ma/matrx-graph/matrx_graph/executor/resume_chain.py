"""The loop chain of a RESUMED leg — from the change that started the run (lane 11 round 5).

A fresh leg reads its chain from its ``trigger`` input (built by the host's verified store
fire from the outbox row). A resumed leg has no such input in memory, and the run's persisted
input/metadata are owner-writable, so the host injects a resolver that reads the change from
the store's outbox through the server. Unconfigured, or when the host finds no change, the
leg is a root of its own (depth 1) — said in the log, not guessed silently.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

logger = logging.getLogger(__name__)

ResumeChainResolver = Callable[[str], Awaitable[Mapping[str, Any] | None]]
_resolver: ResumeChainResolver | None = None


def configure_resume_chain_resolver(resolver: ResumeChainResolver | None) -> None:
    global _resolver
    _resolver = resolver


async def resumed_chain_cause(run_id: str) -> Mapping[str, Any] | None:
    if _resolver is None:
        return None
    try:
        return await _resolver(str(run_id))
    except Exception:  # noqa: BLE001 — a chain read must never stop a resume; said
        logger.warning("resume chain: could not read the starting change of run %s", run_id,
                       exc_info=True)
        return None


__all__ = ["ResumeChainResolver", "configure_resume_chain_resolver", "resumed_chain_cause"]
