"""Pending out of hours notices («aviso fuera de horario con IA»): the port of `ausencia_pendiente` (api-chatty
`docs/atencion/aviso-fuera-de-horario.md`).

Outside the hours, with an autonomous AI in the chat, the business chooses when the closed notice goes out
(`Recepcion.ausencia.con_ia_autonoma`). Two options send it AFTER: the entry leaves a pending notice (one per chat,
valid until the next opening) and a hook after the AI's first reply or after its hand over takes it, once. Its stored
form (Spanish names, as in `main`) is the Mongo adapter's (`letschatty/mongo/attention/pending_notice_repository.py`):
the port takes fields and answers the model below. Without cache, list, edit or events: every operation is by the
chat's id, and the document is deleted when it is taken or by a TTL when it expires.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol

__all__ = ["PendingNotice", "PendingNoticeRepository"]


@dataclass(frozen=True)
class PendingNotice:
    """A notice as taking it answers. `account_id` is the account of the chat when it had one (the hours of the notice
    are the account's); a stored value that is not text is kept as it is (`raw_account_id`), and `main` read it as «no
    account»: `account_id` answers None then."""
    chat_id: str
    company_id: Optional[str]
    option: str
    raw_account_id: Any = None

    @property
    def account_id(self) -> Optional[str]:
        return self.raw_account_id if isinstance(self.raw_account_id, str) else None


class PendingNoticeRepository(Protocol):
    async def register(self, company_id: str, *, chat_id: str, option: str, expires_at: datetime, now: datetime,
                       account_id: Optional[str] = None) -> None:
        """Leaves the chat's pending notice (an upsert by the chat's id): `company_id`, `option`, `expires_at` (a time
        without a zone is UTC) and `now` as its creation time; `account_id` only if there is one. Another notice of the
        chat is overwritten in those fields and keeps an `account_id` it had."""
        ...

    async def option(self, chat_id: str, now: datetime) -> Optional[str]:
        """The option of the chat's notice if it is still valid at `now`, or None. By the chat's id only (ADR-010 §3:
        the chat already comes from the company)."""
        ...

    async def take(self, chat_id: str, option: str, now: datetime) -> Optional[PendingNotice]:
        """Atomic, for one caller: deletes and answers the chat's notice if it has that option and is valid at `now`,
        or None. By the chat's id only (ADR-010 §3)."""
        ...
