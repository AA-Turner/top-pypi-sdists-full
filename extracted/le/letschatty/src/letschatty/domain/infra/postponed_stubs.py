"""Postponed first-message stubs («stubs postergados»): the port of `postponed_stubs` (api-chatty
`docs/infra/stubs-postergados.md`).

A contact's first message often comes twice from Meta with the same wamid: an `errors` stub without content and,
a moment later, the real copy. The webhook of the stub is stored and replayed a few seconds later. One document per
stub wamid: `{_id, wamid, phone_number_id, payload, code, due_at, next_at, state, open, attempts, created_at}`, plus
`claimed_at`/`lease_until` once claimed and `done_at`/`error` once closed. `open` is true while pending or running;
`next_at` is the due time while pending and the end of the lease while running. Of every company: there is no
`company_id` (the stub is stored before its company is known). Without cache.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"


class PostponedStubRepository(Protocol):
    async def add(self, *, wamid: str, phone_number_id: Optional[str], payload: Dict[str, Any], code: int,
                  due_at: datetime, now: datetime) -> Optional[str]:
        """Stores a pending stub due at `due_at` and answers its id; None if its wamid was already stored."""
        ...

    async def claim(self, item_id: str, *, due_by: datetime, now: datetime,
                    lease_until: datetime) -> Optional[Dict[str, Any]]:
        """Atomic, for one caller: an open stub that is pending and due by `due_by`, or running with a lease that
        ended before `now`, becomes running until `lease_until` with one more attempt. Answers it as stored after
        the claim, or None."""
        ...

    async def close(self, item_id: str, *, state: str, now: datetime, error: Optional[str]) -> None:
        """Closes it in `state` (`done_at` = `now`; `error` only if given): it is no longer open."""
        ...

    async def due(self, *, until: datetime, limit: int) -> List[Dict[str, Any]]:
        """The open ones whose `next_at` is by `until`, up to `limit`: `{_id, next_at}` each."""
        ...
