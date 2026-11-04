"""The coexistence history import queue («cola del import de historial»): the job and the ports of
`coexistence_import_jobs` and `coexistence_import_chat_leases` (api-chatty `docs/infra/cola-del-import-de-historial.md`).

The `history` webhook stores a JOB per thread (a customer and their raw messages) and answers at once; a worker takes
them one at a time, holds the chat, joins the pending ones of the same chat and writes them. The queue is of every
company (the worker serves them all); a job carries its `company_id`. Without cache: the chat lease is in Mongo on
purpose (Redis evicts keys, and the lease keeps two workers off one chat).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any, Dict, List, Optional, Protocol

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    PENDING = "pending"    # ready to take from `next_attempt_at`
    RUNNING = "running"    # taken by a worker until `lease_until`
    DONE = "done"          # written; expires by itself after 7 days (TTL index)
    FAILED = "failed"      # ran out of retries; never expires, it alerts
    # LEGACY: no longer produced. History that did not fit a chat under the old 12 MB cap. The jobs stored like
    # that are kept, and `QueueStats.overflow` counts them until someone decides what to do with them.
    OVERFLOW = "overflow"


class HistoryImportJob(BaseModel):
    """One thread of a `history` chunk: a customer and their raw messages from Meta."""

    id: Optional[str] = None
    company_id: str
    sync_id: Optional[str] = None
    phone_number_id: Optional[str] = None
    #: The account that owned the number when it was queued. A job queued before has none: it is resolved by the
    #: number, as always. It matters when the number is no longer routed and the batch still has to go to ITS account.
    account_id: Optional[str] = None
    business_waid: str
    chat_key: str = Field(description='"<phone_number_id>|waid:<wa_id>" o "<phone_number_id>|user:<bsuid>" (sin número: sólo la identidad): el hilo de una persona en un número')
    contact: Dict[str, Any] = Field(description="Contact de Meta, serializado")
    raw_messages: List[Dict[str, Any]] = Field(description="Mensajes crudos del hilo")
    n_messages: int
    chunk_key: str = Field(description="La misma clave que usa el tracker del import")
    dedup_key: str = Field(description="sha1(empresa, chat, wamids): un reenvío no duplica")
    status: JobStatus = JobStatus.PENDING
    attempts: int = 0
    next_attempt_at: datetime
    lease_until: Optional[datetime] = None
    worker_id: Optional[str] = None
    last_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    done_at: Optional[datetime] = None
    batch_size: int = 0
    batch_imported: int = 0


@dataclass(frozen=True)
class QueueStats:
    pending: int = 0
    running: int = 0
    failed: int = 0
    overflow: int = 0  # legacy: see JobStatus.OVERFLOW
    oldest_pending_s: Optional[float] = None

    @property
    def active(self) -> int:
        """Work that can still write messages."""
        return self.pending + self.running


class HistoryImportQueue(Protocol):
    async def enqueue(self, jobs: List[HistoryImportJob]) -> int:
        """Stores the jobs; the repeated ones (`dedup_key`) are ignored. Answers how many went in. Raises if the
        database could not store them."""

    async def claim(self, worker_id: str, lease: timedelta) -> Optional[HistoryImportJob]:
        """Takes first a `running` one whose lease expired (its worker died: one more attempt), else the oldest
        ready one."""

    async def claim_more_for_chat(
        self, job: HistoryImportJob, worker_id: str, lease: timedelta, max_messages: int
    ) -> List[HistoryImportJob]:
        """Takes other pending ones of the SAME chat up to `max_messages` messages."""

    async def extend_lease(self, job_ids: List[str], worker_id: str, lease: timedelta) -> None:
        """Renews the lease of the jobs `worker_id` is still processing (heartbeat)."""

    async def release(self, job_ids: List[str], delay: timedelta) -> None:
        """Puts jobs back to `pending` without counting an attempt (the chat was busy)."""

    async def defer_chat(self, company_id: str, chat_key: str, delay: timedelta) -> None:
        """Moves every pending job of a chat another worker is writing to within `delay`."""

    async def complete(self, job_ids: List[str], imported: int, worker_id: str) -> None:
        """Marks jobs as written. `imported` is what the BATCH added to the chat. Only the ones still of
        `worker_id`."""

    async def retry_or_fail(self, job: HistoryImportJob, error: str, delay: Optional[timedelta]) -> None:
        """One more attempt: with `delay` it is rescheduled, with None it goes to `failed`. Only while it is still
        of the worker that took it (`job.worker_id`)."""

    async def stats(self, company_id: Optional[str] = None) -> QueueStats:
        """How many there are in each state, and the age of the oldest pending one."""

    async def has_active(self, company_id: str, sync_id: Optional[str] = None) -> bool:
        """Whether something is `pending` or `running`: of THAT import with `sync_id`, of the company without it."""

    async def top_active_companies(self, limit: int = 5) -> List[Dict[str, Any]]:
        """The companies with most pending work: `company_id`, `jobs`, `oldest`."""


class ChatLeases(Protocol):
    async def acquire(self, key: str, owner: str, ttl: timedelta) -> bool:
        """Takes the chat for `owner`. False if another one has it and it has not expired."""

    async def extend(self, key: str, owner: str, ttl: timedelta) -> bool:
        """Renews the chat of `owner`. False if it is no longer theirs."""

    async def release(self, key: str, owner: str) -> None:
        """Lets the chat go, only if it is still of `owner`."""
