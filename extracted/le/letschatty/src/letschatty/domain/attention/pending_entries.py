"""Delayed entries («entradas demoradas»): the port of `entradas_pendientes` (api-chatty
`docs/atencion/entrada-demorada.md`).

The entry of a NEW chat (welcome, reason, automations, AI, `message.received`) runs `Recepcion.bienvenida_demora_s`
seconds later. One document per waiting entry: `{_id, company_id, chat_id, mensajes: [message_id…], procesados:
[message_id…], contact_points: {message_id: contact_point_id|None}, trazas: {message_id: trace_id|None}, demora_s,
due_at, proximo_at, estado, abierta, intentos, creada_at}`, plus `lease_until`/`reclamada_at`/`reclamada_por` once
claimed and `hecha_at`/`error` once closed. `abierta` is true while pending or sending (one open per chat, unique
partial index); `proximo_at` is the due time while pending and the end of the lease while sending. The stored names
and values are Spanish, as in `main`. Without cache.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

PENDING = "pendiente"
SENDING = "enviando"
DONE = "hecha"
FAILED = "fallida"


class PendingEntryRepository(Protocol):
    async def open(self, company_id: str, *, chat_id: str, message_id: str, contact_point_id: Optional[str],
                   trace_id: Optional[str], delay_s: int, due_at: datetime, now: datetime) -> Optional[str]:
        """Stores a pending entry of the chat with this first message, due at `due_at`, and answers its id; None if
        the chat already had an open one."""
        ...

    async def add_message(self, chat_id: str, message_id: str, contact_point_id: Optional[str],
                          trace_id: Optional[str]) -> bool:
        """Adds the message at the end of the chat's open entry (once), with its contact point and trace under
        `contact_points.<message_id>` / `trazas.<message_id>`; True if the chat had an open entry."""
        ...

    async def claim(self, item_id: str, *, due_by: datetime, now: datetime, lease_until: datetime,
                    claimed_by: str) -> Optional[Dict[str, Any]]:
        """Atomic, for one caller: an open entry that is pending and due by `due_by`, or sending with a lease that
        ended before `now`, becomes sending until `lease_until` with one more attempt. Answers it as stored after the
        claim, or None."""
        ...

    async def read(self, item_id: str) -> Optional[Dict[str, Any]]:
        """`{_id, mensajes, procesados, contact_points, trazas, estado, company_id, chat_id, intentos, due_at,
        demora_s}`, or None."""
        ...

    async def mark_processed(self, item_id: str, message_id: str, *, lease_until: datetime) -> None:
        """The message ran: it is not run again; the lease lasts until `lease_until`."""
        ...

    async def close(self, item_id: str, *, messages: int, now: datetime) -> bool:
        """Done, only if it is sending and still has `messages` messages (nobody added one); True if it closed."""
        ...

    async def fail(self, item_id: str, *, now: datetime, error: str) -> None:
        """Closes it failed with `error`: it is no longer open."""
        ...

    async def due(self, *, until: datetime, limit: int) -> List[Dict[str, Any]]:
        """The open ones whose `proximo_at` is by `until`, up to `limit`: `{_id, company_id, chat_id, proximo_at}`."""
        ...
