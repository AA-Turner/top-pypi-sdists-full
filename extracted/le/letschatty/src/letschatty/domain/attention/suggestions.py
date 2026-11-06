"""Reason suggestions («sugerencias de motivos»): the port of `sugerencias_de_motivos` (api-chatty
`docs/atencion/migracion-a-entradas.md`).

A request asks the classifier's lambda for up to five reasons from the company's chats. One document per request; it
expires 10 minutes after it was asked (`expires_at`) and is deleted 7 days after (`delete_at`, the TTL). The result
only enters a request that is still `pending` and not expired, and of the company the route says: the content is built
by N8N, which has no secret.

The port speaks of `ReasonSuggestionRequest` with English names; only the Mongo adapter knows the stored shape (Spanish
keys, `_id` as an `ObjectId`). `reasons` is the lambda's cleaned result, stored and returned as it is (ADR-013,
«Excepciones»). Without cache.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

__all__ = ["ReasonSuggestionRepository", "ReasonSuggestionRequest"]


@dataclass(frozen=True)
class ReasonSuggestionRequest:
    """A request as stored. `error` is None when the document has no `error` key."""
    id: Optional[str] = None
    company_id: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    delete_at: Optional[datetime] = None
    reasons: List[Dict[str, Any]] = field(default_factory=list)
    analyzed: int = 0
    error: Optional[str] = None


class ReasonSuggestionRepository(Protocol):
    async def add(self, request: ReasonSuggestionRequest) -> None:
        """Stores the request as it was built (with its id)."""
        ...

    async def fail_if_pending(self, request_id: str, error: str) -> None:
        """If the request is still `pending`, it becomes `error` with that text."""
        ...

    async def of_company(self, company_id: str, request_id: str) -> Optional[ReasonSuggestionRequest]:
        """The request of that company, or None; an id that is not one reads nothing."""
        ...

    async def resolve_if_pending(self, company_id: str, request_id: str, now: datetime, *, error: Optional[str] = None,
                                 reasons: Optional[List[Dict[str, Any]]] = None, analyzed: int = 0) -> bool:
        """If the request is of the company, `pending` and expires after `now`: with `error` it becomes `error`, else
        `ready` with `reasons` (and `analyzed` if it is not zero), noting `now` as received; whether it matched."""
        ...
