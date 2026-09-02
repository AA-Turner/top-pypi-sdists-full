"""ConversationStore — the client-host persistence seam.

When matrx-ai runs inside a desktop/client host (no Postgres, no matrx-orm
wiring — e.g. matrx-local), the host injects an object implementing this
Protocol via ``matrx_ai.configure(conversation_store=...)``. Every
conversation write the classic execution path makes is then delegated to the
store INSTEAD of the ORM, at the same choke points the 0.1.26
``client_mode.ConversationHandler`` used:

* ``db/conversation_gate.py`` — ``ensure_conversation_exists`` /
  ``ensure_user_request_exists`` / ``create_pending_user_request`` early-return
  into the store; the status-update helpers become no-ops (the store owns
  status transitions through ``persist_completed_request``).
* ``db/persistence.py`` — ``persist_completed_request`` delegates WHOLESALE
  (the store receives the CompletedRequest object and owns the entire turn
  write, exactly like 0.1.26).
* ``tools/logger.py`` — tool-call start/update rows route to
  ``log_tool_call_start`` / ``log_tool_call_update``; ``backfill_message_id``
  is a no-op (the host owns its local storage schema and any message linking).
* the history-read path (``agents/resolver.ConversationResolver``) reads the
  stored config via ``get_conversation_config`` instead of the cx_ tables.

With upstream dispatch at these choke points, no client-host write ever
reaches ``persistence/queue_helpers.py`` or the WriteCoordinator — the
coordinator is a server-lane concept and is always None in a client host.

NOTE (v2 runner): ``orchestrator/conversation_runtime.py``'s
``CxmConversationPersistence`` already takes injected callables
(persist/ensure/queue/data/rebuild) and is NOT covered by this dispatch — a
host driving the v2 conversation runtime injects its store's callables there
directly.

The method signatures are forward-ported 1:1 from 0.1.26's
``ConversationHandler`` (plus ``get_conversation_data`` for the flat-data
read), so a host can port its existing handler with minimal changes. The host
owns the storage mechanism — SQLite, memory, files, or a remote API.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

#: The _ext registry key under which the store is registered.
CONVERSATION_STORE_KEY = "conversation_store"

#: The methods a ConversationStore must implement (used for validation
#: error messages and the runtime_checkable structural check).
CONVERSATION_STORE_METHODS: tuple[str, ...] = (
    "ensure_conversation_exists",
    "create_pending_user_request",
    "persist_completed_request",
    "log_tool_call_start",
    "log_tool_call_update",
    "get_conversation_config",
    "get_conversation_data",
)


@runtime_checkable
class ConversationStore(Protocol):
    """Host-implemented conversation persistence for client-host installs."""

    async def ensure_conversation_exists(
        self,
        conversation_id: str,
        user_id: str,
        parent_conversation_id: str | None = None,
        variables: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> None:
        """Create the conversation record if it does not already exist.

        Idempotent. ``variables`` / ``overrides`` carry the AppContext's
        write-once initial values (may be empty for non-agent calls).
        """
        ...

    async def create_pending_user_request(
        self,
        request_id: str,
        conversation_id: str,
        user_id: str,
    ) -> None:
        """Insert (or confirm) a user-request record with status='pending'.

        Called from BOTH ``create_pending_user_request`` and
        ``ensure_user_request_exists`` gate paths — the store owns idempotency
        (a second call for the same ``request_id`` must be a no-op).
        ``conversation_id`` may be ``""`` when the gate has no conversation in
        context (a user request can legitimately span conversations).
        """
        ...

    async def persist_completed_request(
        self,
        completed: Any,
        conversation_id: str | None = None,
    ) -> dict[str, Any]:
        """Persist all data from a completed AI execution (a
        ``matrx_ai.orchestrator.requests.CompletedRequest``).

        May be called more than once per request (mid-run flush + final);
        the store owns upsert semantics. Must return a dict with keys:
        ``conversation_id``, ``user_request_id``, ``message_ids`` (list),
        ``request_ids`` (list).
        """
        ...

    async def log_tool_call_start(
        self,
        row_id: str,
        data: dict[str, Any],
    ) -> None:
        """Insert a tool-call record. ``data`` carries the full row (id,
        conversation_id, user_request_id, tool_name, call_id, status,
        arguments, timestamps, ...). ``status`` is ``'running'`` for a normal
        start and ``'error'`` for a pre-dispatch rejection (a single terminal
        insert)."""
        ...

    async def log_tool_call_update(
        self,
        row_id: str,
        data: dict[str, Any],
    ) -> None:
        """Update an existing tool-call record (completion or error)."""
        ...

    async def get_conversation_config(
        self,
        conversation_id: str,
    ) -> dict[str, Any]:
        """Return the stored conversation config dict (the shape
        ``UnifiedConfig.from_dict`` accepts, including rebuilt ``messages``).
        Called by ConversationResolver when rebuilding state from local
        storage. Must raise when the conversation does not exist."""
        ...

    async def get_conversation_data(
        self,
        conversation_id: str,
    ) -> dict[str, Any]:
        """Return the flat conversation data dict — at minimum
        ``{"conversation": ..., "messages": [...], "tool_calls": [...],
        "media": [...], "user_requests": [...], "requests": [...]}`` —
        mirroring ``CxManagers.get_conversation_data``."""
        ...


def missing_store_methods(candidate: Any) -> list[str]:
    """Return the ConversationStore method names ``candidate`` lacks."""
    return [
        name
        for name in CONVERSATION_STORE_METHODS
        if not callable(getattr(candidate, name, None))
    ]


__all__ = [
    "CONVERSATION_STORE_KEY",
    "CONVERSATION_STORE_METHODS",
    "ConversationStore",
    "missing_store_methods",
]
