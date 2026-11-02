"""The record of a WhatsApp Coexistence history import («registro del import de coexistence»): one per company and
`phone_number_id`, the durable bookmark of the backfill Meta sends once per onboarding of each number. The port every
store of it implements, and the pure rules about it.

The entity is `letschatty.models.chat.coexistence_import_sync.CoexistenceImportSync`, unchanged. It is not a catalog
(ADR-010 of api-chatty): nobody creates, edits or lists it by hand; chunks fold into it with atomic Mongo operators,
because they arrive concurrently and are redelivered (at-least-once webhooks), and the end is a conditional flip that
exactly one caller wins.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional, Protocol

from ...models.chat.coexistence_import_sync import CoexistenceImportSync
from ...models.utils.types import StrObjectId

# Meta's progress of a finished backfill.
TERMINAL_PROGRESS = 100.0


def chunk_key(phase, chunk_order) -> str:
    """The key a chunk is counted once under (`history:3`, `state_sync:0`; `None:None` is a key too)."""
    return f"{phase}:{chunk_order}"


def is_terminal(progress: Optional[float]) -> bool:
    """Meta says the backfill is complete."""
    return progress is not None and progress >= TERMINAL_PROGRESS


def newest(records: Iterable[CoexistenceImportSync]) -> CoexistenceImportSync:
    """The most recently created; the first of the given order on a tie."""
    return max(records, key=lambda r: r.created_at)


class CoexistenceImportSyncRepository(Protocol):
    async def of_company(self, company_id: StrObjectId) -> List[CoexistenceImportSync]:
        """Every record of the company (any status and number), in the store's order. The company is compared as
        stored text."""
        ...

    async def of_number(self, company_id: StrObjectId, phone_number_id: Optional[str]) -> List[CoexistenceImportSync]:
        """The records of the company with that `phone_number_id`; None means the ones stored without a number."""
        ...

    async def adopt(self, sync_id: StrObjectId, phone_number_id: str) -> bool:
        """Gives the number to a record that still has none; False if another caller gave it one first."""
        ...

    async def add(self, item: CoexistenceImportSync) -> None:
        ...

    async def get(self, sync_id: StrObjectId) -> CoexistenceImportSync:
        """Raises `NotFoundError` if there is none."""
        ...

    async def apply_chunk(self, sync_id: StrObjectId, *, key: str, messages_delta: int, threads_delta: int,
                          contacts_delta: int, progress: Optional[float]) -> None:
        """Counts messages and threads once per `key`; adds contacts and keeps the furthest progress every time."""
        ...

    async def add_imported(self, sync_id: StrObjectId, *, messages_delta: int, threads_delta: int) -> None:
        """Adds what the queue worker wrote, without the chunk key."""
        ...

    async def touch_last_chunk(self, sync_id: StrObjectId, when: datetime) -> None:
        """The quiescence clock."""
        ...

    async def reopen_if_completed(self, sync_id: StrObjectId) -> Optional[CoexistenceImportSync]:
        """Completed → in progress; the record if THIS call flipped it, else None."""
        ...

    async def complete_if_pending(self, sync_id: StrObjectId) -> Optional[CoexistenceImportSync]:
        """→ completed; the record if THIS call flipped it, else None (exactly one caller wins)."""
        ...

    async def stale_in_progress(self, older_than: datetime) -> List[CoexistenceImportSync]:
        """In progress with a `last_chunk_at` older than `older_than`, of every company."""
        ...

    async def set_notification_id(self, sync_id: StrObjectId, notification_id: str) -> None:
        ...
