"""Classification requests («pedidos de clasificación»): the port of `clasificaciones_de_motivo` (api-chatty
`docs/atencion/pedidos-de-clasificacion.md`).

A request is the state of the classification of a chat's reason, ONE active per chat (a unique partial index on
`chat_id` among `activo: true`). It is a state machine (`states.py`): every transition is conditional on the state —
and, when given, on the call (`call_id`) and on still being expired — so of two paths that move the same request (the
model's result and the sweep; two retries of the same result) only one wins and the other gets None.

The port speaks of `ClassificationRequest`, with English field names; only the Mongo adapter knows the stored shape
(Spanish keys, `_id` as an `ObjectId`). A request carries exactly the fields its document has: a field the document
lacks is not set (`model_fields_set`), which is not the same as a field stored as null. The nested subdocuments
(`result`, `source`, `source_hint`, `removed_ai_config`, `correction`, `last_result`) are the classifier's and travel
as mappings. Without cache.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional, Protocol, Sequence

from pydantic import BaseModel, ConfigDict, Field


class ClassificationRequest(BaseModel):
    """A request, or the fields a transition writes (`changes`): only the fields it was built with count.

    Strict: a value of another type is refused, never converted. `other_fields` are stored fields this model does not
    name (none in prod on 2026-11-03): they are carried back untouched, by their stored name."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: Optional[str] = None
    company_id: Optional[str] = None
    chat_id: Optional[str] = None
    state: Optional[str] = None
    active: Optional[bool] = None
    round: Optional[int] = None
    calls: Optional[int] = None
    call_id: Optional[str] = None
    new_messages: Optional[bool] = None
    can_ask: Optional[bool] = None
    entry: Optional[str] = None
    is_new: Optional[bool] = None
    is_first_message: Optional[bool] = None
    since: Optional[datetime] = None
    welcome_fast_answer_id: Optional[str] = None
    notice_sent: Optional[bool] = None
    source: Optional[Dict[str, Any]] = None
    text: Optional[str] = None
    question: Optional[str] = None
    options: Optional[List[Any]] = None
    original_phrase: Optional[str] = None
    asked_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    source_hint: Optional[Dict[str, Any]] = None
    dispatch_at: Optional[datetime] = None
    cap_at: Optional[datetime] = None
    correctable_at: Optional[datetime] = None
    applied_reason_id: Optional[str] = None
    applied_origin: Optional[str] = None
    correctable_by: Optional[str] = None
    source_candidates: Optional[List[Any]] = None
    ai_removed: Optional[bool] = None
    removed_ai_config: Optional[Dict[str, Any]] = None
    new_content: Optional[bool] = None
    last_result: Optional[Dict[str, Any]] = None
    base_calls: Optional[int] = None
    correcting: Optional[bool] = None
    reclassifications: Optional[int] = None
    general_inquiry_applied: Optional[bool] = None
    general_inquiry_at: Optional[datetime] = None
    correction: Optional[Dict[str, Any]] = None
    other_fields: Dict[str, Any] = Field(default_factory=dict)


class ClassificationRequestRepository(Protocol):
    async def open(self, request: ClassificationRequest) -> str:
        """Stores the request as it was built (with its id) and answers its id. A second active one of the same chat
        raises the store's duplicate-key error (the unique partial index)."""
        ...

    async def replace_active(self, chat_id: str, *, now: datetime) -> None:
        """Every active request of the chat becomes `replaced`, inactive, updated at `now` (by chat only, as in
        `main`: a chat id is unique across companies)."""
        ...

    async def active_of(self, chat_id: str) -> Optional[ClassificationRequest]:
        """The chat's active request, or None."""
        ...

    async def get(self, request_id: str) -> Optional[ClassificationRequest]:
        """The request with that id (any state, any company), or None; an id that is not one reads nothing."""
        ...

    async def is_current(self, company_id: str, request_id: str, *, chat_id: str, call_id: str) -> bool:
        """Does this request wait for THIS result? Active, classifying, of that company and chat, with that call.
        An id that is not one reads nothing."""
        ...

    async def transition(self, request_id: str, *, from_states: Sequence[str], changes: ClassificationRequest,
                         call_id: Optional[str] = None, expired_by: Optional[datetime] = None,
                         increment: Optional[Mapping[str, int]] = None) -> Optional[ClassificationRequest]:
        """Atomic: if the request is active, in one of `from_states` (and, when given, with that call and still
        expired by `expired_by`), writes the fields `changes` was built with and adds `increment` (field name →
        amount); answers the request AFTER the change, or None. An id that is not one reads nothing."""
        ...

    async def mark_new_messages(self, request_id: str, *, now: datetime, content: bool) -> None:
        """While classifying: a message came (`new_messages`, `updated_at`), and with `content` it says something of
        its own (`new_content`). An id that is not one writes nothing."""
        ...

    async def expired(self, *, now: datetime, limit: int) -> List[ClassificationRequest]:
        """The active requests of every company expired by `now`, the oldest first, up to `limit`."""
        ...
