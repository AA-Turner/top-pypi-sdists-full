"""The in-memory client-tool handoff of an UNSAVED (``store=False``) run.

A saved run parks a delegated call on its ``chat.tool_call`` row and resumes from it (RESUME-AND-RECOVERY
section 1). An unsaved run has no row, so the same ``tool_delegated`` event is emitted and the turn WAITS, in
this process, on a future keyed by the call id; the result-post route resolves it. Nothing here is durable by
design: a restart loses the waiter, and the late post is answered plainly (the chat was not saved).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any


@dataclass
class _Waiter:
    future: asyncio.Future[dict[str, Any]]
    user_id: str
    conversation_id: str


_WAITERS: dict[str, _Waiter] = {}  # call_id -> waiter


def register(call_id: str, *, user_id: str, conversation_id: str) -> asyncio.Future[dict[str, Any]]:
    future: asyncio.Future[dict[str, Any]] = asyncio.get_running_loop().create_future()
    _WAITERS[call_id] = _Waiter(future, str(user_id or ""), str(conversation_id or ""))
    return future


def forget(call_id: str) -> None:
    _WAITERS.pop(call_id, None)


def has_waiter(call_id: str) -> bool:
    waiter = _WAITERS.get(call_id)
    return waiter is not None and not waiter.future.done()


def deliver(call_id: str, *, user_id: str, conversation_id: str, answer: dict[str, Any]) -> bool:
    """Hand the client's answer to the waiting turn. False when nobody waits (restart, timeout, other person)."""
    waiter = _WAITERS.get(call_id)
    if waiter is None or waiter.future.done():
        return False
    if waiter.user_id != str(user_id or "") or waiter.conversation_id != str(conversation_id or ""):
        return False
    waiter.future.set_result(answer)
    return True
