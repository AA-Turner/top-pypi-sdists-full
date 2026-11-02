from __future__ import annotations
import copy
import logging
import re
from collections import OrderedDict
from typing import Any, List, Optional, Tuple, TYPE_CHECKING

from pydantic import model_validator

from .meta_base_notification_json import BaseMetaNotificationJson, Contact

if TYPE_CHECKING:
    from .schema.values.value_messages import Message, HistoryEntry

logger = logging.getLogger("logger")


def _digits_only(value: Optional[str]) -> str:
    """Strip everything but digits so a formatted business number
    ('+54 9 11 3559 5255') compares equal to a bare wa_id ('5491135595255')."""
    return re.sub(r"\D", "", value or "")


class MetaHistoryJson(BaseMetaNotificationJson):
    """WhatsApp Coexistence — `history` webhook.

    When a business connects a coexistence number, Meta backfills the prior
    WhatsApp Business App conversations. Two shapes are observed in production:

    1. THREADS ENVELOPE — `value.history[]` entries carrying chunk metadata
       (`phase`, `chunk_order`, `progress`) plus `threads`, where each thread is
       one customer conversation (`id` = customer wa_id) holding historical
       `Message`s.
    2. FLAT MESSAGES — historical messages delivered directly under
       `value.messages[]` (byte-for-byte the live-message shape), distinguished
       only by the Change-level `field == "history"`. No `value.history`, often no
       `history_context` / chunk metadata. `iter_threads()` synthesizes per-customer
       threads from these.

    This envelope exposes the chunk metadata and a flat thread iterator so the
    api-chatty factory can fan the history out into per-chat imported messages.
    """

    @model_validator(mode="before")
    @classmethod
    def _drop_unparseable_messages(cls, data: Any) -> Any:
        """Isolate a single unparseable historical message so it can't void the WHOLE chunk.

        A `history` webhook packs MANY messages into ONE envelope (flat: value.messages[];
        threads: value.history[].threads[].messages[]), which pydantic validates atomically.
        If any single message fails to parse — a content sub-model stricter than Meta's real
        backfill (e.g. an `order` whose required `text` is absent, metadata-only media missing
        sha256/id), or a future field shape — the strict List[Message] raises ValidationError
        for the entire envelope, silently dropping a whole chunk of otherwise-valid history.
        The receiver's per-message try/except runs AFTER this parse, so it cannot isolate it.

        Here we pre-validate each raw message in its own try/except and DROP (log) the ones
        that fail, leaving the survivors for the strict field validation that follows. This is
        scoped to the history envelope ONLY (the factory routes `field=="history"` here before
        the strict base parse), so the live message path keeps its strict validation. The raw
        webhook is deep-copied first, so this never mutates the caller's payload (the receiver
        still captures the true raw webhook)."""
        if not isinstance(data, dict):
            return data
        from .schema.values.value_messages import Message

        def _keep_parseable(raw_messages: Any) -> Any:
            if not isinstance(raw_messages, list):
                return raw_messages
            kept = []
            for m in raw_messages:
                try:
                    Message.model_validate(m)  # validate only; the field re-parses survivors
                    kept.append(m)
                except Exception as e:  # noqa: BLE001 - any parse failure -> isolate this message
                    logger.warning(
                        "Coexistence history: dropping unparseable message id=%s: %s",
                        (m or {}).get("id", "?") if isinstance(m, dict) else "?",
                        e,
                    )
            return kept

        data = copy.deepcopy(data)
        for entry in data.get("entry", []) or []:
            for change in (entry.get("changes", []) or []) if isinstance(entry, dict) else []:
                value = (change.get("value") or {}) if isinstance(change, dict) else {}
                if "messages" in value:
                    value["messages"] = _keep_parseable(value.get("messages"))
                for h in (value.get("history", []) or []):
                    for thread in (h.get("threads", []) or []) if isinstance(h, dict) else []:
                        if isinstance(thread, dict) and "messages" in thread:
                            thread["messages"] = _keep_parseable(thread.get("messages"))
        return data

    def _first_entry(self) -> Optional[HistoryEntry]:
        history = self.get_value().history
        return history[0] if history else None

    def get_display_phone_number(self) -> str:
        """The coexistence business number whose history this chunk belongs to."""
        return self.get_metadata().display_phone_number

    def get_phase(self) -> Optional[int]:
        """The backfill phase reported by the current chunk, if any (integer)."""
        entry = self._first_entry()
        if entry is None or entry.metadata is None:
            return None
        return entry.metadata.phase

    def get_chunk_order(self) -> Optional[int]:
        """The ordinal position of the current chunk in the backfill sequence."""
        entry = self._first_entry()
        if entry is None or entry.metadata is None:
            return None
        return entry.metadata.chunk_order

    def get_progress(self) -> Optional[float]:
        """The 0-100 completion percentage of the overall history backfill."""
        entry = self._first_entry()
        if entry is None or entry.metadata is None:
            return None
        return entry.metadata.progress

    def iter_thread_identities(self) -> List[Tuple[Contact, List[Message]]]:
        """Flatten the chunk into ``(customer_identity, messages)`` pairs.

        The identity is a `Contact` — the same object the live-message path hands to
        chat resolution — because a history customer is NOT always a phone number.
        A customer who uses a WhatsApp **username** has no phone at all and exists
        only as the opaque `user_id` (BSUID, e.g. `CO.1472426137994571`). Returning
        a bare wa_id string could not express that, so those customers used to be
        dropped; returning the Contact lets the consumer resolve them by BSUID
        exactly as it already does for live messages, statuses, edits and echoes.

        Prefers the THREADS ENVELOPE (`value.history[].threads[]`), walking every
        entry so a multi-entry chunk is fully drained; falls back to the FLAT
        MESSAGES shape when there is no envelope (see `_flat_thread_identities`).

        A thread we cannot identify AT ALL — no phone and no BSUID — is skipped and
        logged, alone: one unidentifiable thread must never cost its neighbours."""
        threads: List[Tuple[Contact, List[Message]]] = []
        saw_envelope_thread = False
        for entry in self.get_value().history:
            for thread in entry.threads:
                saw_envelope_thread = True
                ctx = thread.context
                wa_id = thread.id or (ctx.wa_id if ctx else None)
                user_id = ctx.user_id if ctx else None
                if not wa_id and not user_id:
                    logger.warning(
                        "Coexistence history: skipping unidentifiable thread — no wa_id and "
                        "no BSUID; %d message(s) not imported", len(thread.messages),
                    )
                    continue
                threads.append((
                    Contact(
                        wa_id=wa_id,
                        user_id=user_id,
                        username=ctx.username if ctx else None,
                    ),
                    thread.messages,
                ))
        if saw_envelope_thread:
            # The envelope WAS the shape of this chunk. Even if every thread was
            # skipped, do not fall through to the flat reader — `value.messages` is
            # a different delivery shape, not a backup copy of these threads.
            return threads
        return self._flat_thread_identities()

    def _flat_thread_identities(self) -> List[Tuple[Contact, List[Message]]]:
        """FLAT shape: group `value.messages` into per-customer threads.

        Direction comes from `history_context.from_me` when present (authoritative),
        else a digits-only `from` vs business compare. The customer is then:
        - INCOMING (customer -> business): `from` (phone), else `from_user_id` (BSUID),
        - OUTGOING (business -> customer): `to` (phone), else `to_user_id` (BSUID).

        The BSUID fallbacks are what make a phoneless customer importable here. Real
        history outgoing messages frequently carry NO `to` AND no `to_user_id` (Meta
        omits the recipient for owner-sent history); such a message has no derivable
        customer and is SKIPPED (logged) — a partial import beats a storm.

        Messages are grouped by `wa_id or user_id`: a given customer is consistently
        one or the other within a chunk, and two groups for one customer would still
        converge on a single chat downstream, where identity is resolved against what
        is already stored."""
        business_digits = _digits_only(self.get_metadata().display_phone_number)
        grouped: "OrderedDict[str, Tuple[Contact, List[Message]]]" = OrderedDict()
        for m in self.get_value().messages:
            hist_ctx = getattr(m, "history_context", None)
            from_me = getattr(hist_ctx, "from_me", None) if hist_ctx is not None else None
            if from_me is not None:
                is_incoming = not from_me
            else:
                is_incoming = _digits_only(m.from_) != business_digits
            if is_incoming:
                wa_id, user_id = m.from_, getattr(m, "from_user_id", None)
            else:
                wa_id, user_id = m.to, getattr(m, "to_user_id", None)
            key = wa_id or user_id
            if not key:
                logger.warning(
                    "Coexistence flat history: skipping message id=%s — no phone and no BSUID "
                    "for the customer side, no derivable thread", getattr(m, "id", "?"),
                )
                continue
            if key not in grouped:
                grouped[key] = (Contact(wa_id=wa_id, user_id=user_id), [])
            grouped[key][1].append(m)
        return list(grouped.values())
