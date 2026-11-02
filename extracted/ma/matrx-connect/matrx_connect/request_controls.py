from __future__ import annotations

import asyncio
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Literal

# "interrupt" is cancel-with-fork semantics: stop at the next boundary like a
# plain cancel, but the executor additionally HIDES the tail produced after the
# last clean boundary (is_visible_to_user=False + is_visible_to_model=False on
# those messages) so the user's redirect message replies to the last thing they
# actually saw. Costs are unaffected — the in-flight call finishes and bills.
RequestControlAction = Literal["cancel", "interrupt", "retry_now"]


@dataclass(frozen=True)
class RequestControlSignal:
    action: RequestControlAction
    requested_at: float


#: Bound on the request→root links held in memory (oldest dropped first).
_MAX_TREE_LINKS = 100_000


class RequestControlRegistry:
    """In-process stop / interrupt / retry-now signals, keyed on the request TREE.

    Every child agent run owns its own turn id. A child id is LINKED to its tree's
    root (:meth:`link_tree`, done at every fork by ``child_agent_context`` and at every
    run start by the executor), and a signal for ANY id of the tree lands on the root:
    Stop on the parent's turn — or on a helper's — stops the whole tree, and every run
    in the tree polls its own id, which resolves to the root.
    """

    _instance: RequestControlRegistry | None = None

    def __init__(self, ttl_seconds: float = 3600.0) -> None:
        self._signals: dict[str, list[RequestControlSignal]] = {}
        self._roots: OrderedDict[str, str] = OrderedDict()
        self._ttl = ttl_seconds
        self._lock = asyncio.Lock()

    def link_tree(self, request_id: str | None, root_request_id: str | None) -> None:
        """Record that ``request_id`` runs inside ``root_request_id``'s tree."""
        if not request_id or not root_request_id or request_id == root_request_id:
            return
        root = self.root_of(root_request_id)
        if root == request_id:
            return
        self._roots[request_id] = root
        self._roots.move_to_end(request_id)
        while len(self._roots) > _MAX_TREE_LINKS:
            self._roots.popitem(last=False)

    def root_of(self, request_id: str) -> str:
        """The tree root ``request_id`` belongs to (itself when unlinked)."""
        return self._roots.get(request_id, request_id)

    def _tree_ids(self, request_id: str) -> tuple[str, ...]:
        root = self.root_of(request_id)
        return (request_id,) if root == request_id else (request_id, root)

    @classmethod
    def get_instance(cls) -> RequestControlRegistry:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def request(self, request_id: str, action: RequestControlAction) -> None:
        """Signal the TREE ``request_id`` belongs to (its root)."""
        request_id = self.root_of(request_id)
        async with self._lock:
            self._cleanup_locked(time.time())
            self._signals.setdefault(request_id, []).append(
                RequestControlSignal(action=action, requested_at=time.time())
            )

    async def cancel(self, request_id: str) -> None:
        await self.request(request_id, "cancel")

    async def interrupt(self, request_id: str) -> None:
        await self.request(request_id, "interrupt")

    async def retry_now(self, request_id: str) -> None:
        await self.request(request_id, "retry_now")

    def is_cancelled(self, request_id: str) -> bool:
        """True for cancel OR interrupt — an interrupt IS a cancel plus
        tail-hiding; every existing cancel poll honors it automatically."""
        self._cleanup_locked(time.time())
        return any(
            signal.action in ("cancel", "interrupt")
            for key in self._tree_ids(request_id)
            for signal in self._signals.get(key, ())
        )

    def is_interrupted(self, request_id: str) -> bool:
        self._cleanup_locked(time.time())
        return any(
            signal.action == "interrupt"
            for key in self._tree_ids(request_id)
            for signal in self._signals.get(key, ())
        )

    async def consume_retry_now(self, request_id: str) -> bool:
        async with self._lock:
            self._cleanup_locked(time.time())
            for key in self._tree_ids(request_id):
                if self._consume_retry_locked(key):
                    return True
            return False

    def _consume_retry_locked(self, request_id: str) -> bool:
        signals = self._signals.get(request_id)
        if not signals:
            return False
        keep: list[RequestControlSignal] = []
        consumed = False
        for signal in signals:
            if signal.action == "retry_now" and not consumed:
                consumed = True
                continue
            keep.append(signal)
        if keep:
            self._signals[request_id] = keep
        else:
            self._signals.pop(request_id, None)
        return consumed

    async def cleanup_expired(self) -> int:
        async with self._lock:
            before = sum(len(v) for v in self._signals.values())
            self._cleanup_locked(time.time())
            after = sum(len(v) for v in self._signals.values())
            return before - after

    def _cleanup_locked(self, now: float) -> None:
        expired_keys: list[str] = []
        for request_id, signals in self._signals.items():
            fresh = [signal for signal in signals if now - signal.requested_at <= self._ttl]
            if fresh:
                self._signals[request_id] = fresh
            else:
                expired_keys.append(request_id)
        for request_id in expired_keys:
            self._signals.pop(request_id, None)


def register_request_tree(ctx: Any) -> None:
    """Link ``ctx``'s own turn id to its tree root in the control registry (idempotent).

    Called at every fork (``child_agent_context``) and at every run start (the
    executor), so a run rebuilt in another process (resume, deferred work, crash
    recovery) that carries ``root_request_id`` from its row is stoppable by the
    tree's id too."""
    request_id = str(getattr(ctx, "request_id", "") or "")
    root = str(getattr(ctx, "root_request_id", "") or "")
    if request_id and root and request_id != root:
        RequestControlRegistry.get_instance().link_tree(request_id, root)
