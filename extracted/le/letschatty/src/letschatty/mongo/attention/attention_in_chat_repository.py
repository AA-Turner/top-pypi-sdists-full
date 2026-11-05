"""`AttentionInChatRepository` on `atencion_en_chat`: the same filters, updates, upserts, projections, `return_document`
and time limits that `AtencionEnChat` of api-chatty ran (`company/…/atencion/en_chat.py` in `main`), and the only
place that knows the stored shape (`document_of` / `attention_of`).

The stored names are Spanish and never change (cintia-lambdas reads the collection). A closed value
(`asignar_al_escalar` among them) is written in the order `main`'s producers wrote it; a payload (`ia`,
`ia.resultado`) and a `StoredAsIs` as they come."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ...domain.attention.attention_in_chat import (ABSENT, REASON_CHANGES_KEPT, UNCHANGED, AiFollowUps, AiOnReason,
                                                   AiResult, AssignOnEscalation, AttentionInChat, EscalationMark,
                                                   FixedFollowUpChain, FollowUpsCut, HandOverMessageMark, Payload,
                                                   PersonRequest, ReasonChange, ReasonReplyMark, StoredAsIs)
from ...domain.attention.states import AI_ACTIVE, AI_FINISHED

COLLECTION = "atencion_en_chat"
REASON_CHANGES = "cambios_de_motivo_por_ia"
# The writes of the follow-ups and of the AI's marks die on the server (`update_one` takes no `maxTimeMS`).
MAX_TIME_MS = 2000
# The page of a company when the beta is switched off.
MAX_TIME_MS_PAGE = 10000
MAX_TIME_MS_SWEEP = 5000

# The closed values: their stored names in the order `main` writes them, and the model's field for each.
_CLOSED: Dict[type, Tuple[Tuple[str, str], ...]] = {
    # The dump of the reason's `Asignacion` (letschatty `models/company/assets/atencion/al_responder.py`), in its order.
    AssignOnEscalation: (("modo", "mode"), ("user_id", "user_id"), ("business_area_id", "business_area_id")),
    ReasonReplyMark: (("clave", "key"), ("motivo_id", "reason_id"), ("desde", "since"), ("vence_at", "expires_at"),
                      ("aplicado_at", "applied_at")),
    PersonRequest: (("por", "by"), ("at", "at")),
    AiFollowUps: (("follow_up_strategy_id", "follow_up_strategy_id"), ("clave", "key"), ("propios", "own"),
                  ("agente_id", "agent_id")),
    # The rebuild adds both marks in one `$set`: Mongo appends new fields in alphabetical order.
    FixedFollowUpChain: (("clave", "key"), ("motivo_id", "reason_id"), ("rearmada_at", "rebuilt_at"),
                         ("rearmada_por", "rebuilt_by")),
    FollowUpsCut: (("por", "by"), ("user_id", "user_id"), ("at", "at")),
    EscalationMark: (("modo", "mode"), ("user_id", "user_id"), ("at", "at")),
    HandOverMessageMark: (("clave", "key"), ("at", "at")),
    ReasonChange: (("at", "at"), ("de", "from_reason_id"), ("a", "to_reason_id"), ("turno_id", "turn_id")),
}

# The document: stored name → field, and how each value is read.
_FIELDS: Tuple[Tuple[str, str, Any], ...] = (
    ("_id", "id", None),
    ("chat_id", "chat_id", None),
    ("company_id", "company_id", None),
    ("motivo_id", "reason_id", None),
    ("entrada_at", "entered_at", None),
    ("creado_at", "created_at", None),
    ("actualizado_at", "updated_at", None),
    ("asignar_al_escalar", "assign_on_escalation", AssignOnEscalation),
    ("ia", "ai", AiOnReason),
    ("si_responde_motivo", "reason_reply", ReasonReplyMark),
    ("pide_persona", "person_request", PersonRequest),
    ("seguimientos_ia", "ai_follow_ups", AiFollowUps),
    ("seguimientos_fijos", "fixed_chain", FixedFollowUpChain),
    ("cortados", "cut", FollowUpsCut),
    ("al_escalar", "escalation", EscalationMark),
    ("mensaje_al_derivar_enviado", "hand_over_message", HandOverMessageMark),
    (REASON_CHANGES, "reason_changes", list),
    ("si_responde_seguimiento_id", "follow_up_reply_id", None),
    ("si_responde_at", "follow_up_reply_at", None),
)
_STORED = {stored for stored, _, _ in _FIELDS}
_READ_ORDER = "_mongo_read_order"


def value_of(kind: Any, stored: Any) -> Any:
    """A stored value as the model: `None` stays `None`; a shape `main` never writes is `StoredAsIs`."""
    if stored is None or kind is None:
        return stored
    if kind is list:
        if not isinstance(stored, list):
            return StoredAsIs(stored)
        return tuple(value_of(ReasonChange, item) for item in stored)
    if isinstance(kind, type) and issubclass(kind, Payload):
        return kind(stored) if isinstance(stored, Mapping) else StoredAsIs(stored)
    if not isinstance(stored, Mapping):
        return StoredAsIs(stored)
    names = [name for name, _ in _CLOSED[kind]]
    keys = list(stored)
    if any(key not in names for key in keys) or keys != sorted(keys, key=names.index):
        return StoredAsIs(stored)
    return kind(**{attr: stored.get(name, ABSENT) for name, attr in _CLOSED[kind]})


def stored_of(value: Any) -> Any:
    """A model value as it is stored (the inverse of `value_of`)."""
    if value is None:
        return None
    if isinstance(value, StoredAsIs):
        return value.value
    if isinstance(value, Payload):
        return value.as_dict()
    if isinstance(value, tuple):
        return [stored_of(item) for item in value]
    if type(value) in _CLOSED:
        return {name: getattr(value, attr) for name, attr in _CLOSED[type(value)]
                if getattr(value, attr) is not ABSENT}
    return value


def attention_of(document: Optional[Mapping[str, Any]]) -> Optional[AttentionInChat]:
    """A stored document (whole or projected) as the model; None stays None."""
    if document is None:
        return None
    values = {attr: value_of(kind, document[stored]) for stored, attr, kind in _FIELDS if stored in document}
    others = {key: value for key, value in document.items() if key not in _STORED}
    attention = AttentionInChat(**values, others=others)
    # The order Mongo gave the fields in, for `document_of`: a storage detail, so it is not a field of the model.
    object.__setattr__(attention, _READ_ORDER, tuple(document))
    return attention


def document_of(attention: Optional[AttentionInChat]) -> Optional[Dict[str, Any]]:
    """The model as Mongo answered it to `main`: only what was read, by its stored names."""
    if attention is None:
        return None
    document = {stored: stored_of(getattr(attention, attr)) for stored, attr, _ in _FIELDS
                if getattr(attention, attr) is not ABSENT}
    document.update(attention.others)
    # In the order Mongo gave it (what `main` handed its callers); what was not read keeps the codec's order.
    order = [key for key in getattr(attention, _READ_ORDER, ()) if key in document]
    return {**{key: document[key] for key in order}, **{k: v for k, v in document.items() if k not in order}}


class MongoAttentionInChatRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def record_entry(self, company_id: str, chat_id: str, *, reason_id: Optional[str],
                           assign_on_escalation: Optional[AssignOnEscalation], ai: Optional[AiOnReason],
                           now: datetime, clear_reason_reply: bool = True) -> None:
        sets: Dict[str, Any] = {
            "company_id": str(company_id),
            "motivo_id": str(reason_id) if reason_id else None,
            "entrada_at": now,
            "asignar_al_escalar": stored_of(assign_on_escalation),
            "ia": stored_of(ai),
            "actualizado_at": now,
        }
        if clear_reason_reply:
            sets["si_responde_motivo"] = None
        await self.collection.update_one(
            {"chat_id": str(chat_id)},
            {"$set": sets, "$setOnInsert": {"chat_id": str(chat_id), "creado_at": now}},
            upsert=True,
        )

    async def mark_reason_reply(self, company_id: str, chat_id: str, mark: Optional[ReasonReplyMark],
                                now: datetime) -> None:
        changes: Dict[str, Any] = {"$set": {"company_id": str(company_id), "si_responde_motivo": stored_of(mark),
                                            "actualizado_at": now}}
        if mark is not None:
            changes["$setOnInsert"] = {"chat_id": str(chat_id), "creado_at": now}
        await self.collection.find_one_and_update(
            {"chat_id": str(chat_id)}, changes, projection={"_id": 1}, upsert=mark is not None, maxTimeMS=MAX_TIME_MS,
        )

    async def claim_reason_reply(self, chat_id: str, *, arrived_at: datetime, last_outgoing_at: datetime,
                                 now: datetime) -> Union[ReasonReplyMark, StoredAsIs, None]:
        before = await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "si_responde_motivo.clave": {"$type": "string"},
             "si_responde_motivo.aplicado_at": None,
             "si_responde_motivo.desde": {"$lt": last_outgoing_at},
             "si_responde_motivo.vence_at": {"$gte": arrived_at}},
            {"$set": {"si_responde_motivo.aplicado_at": now}},
            projection={"_id": 0, "si_responde_motivo": 1}, return_document=ReturnDocument.BEFORE,
            maxTimeMS=MAX_TIME_MS,
        )
        return value_of(ReasonReplyMark, (before or {}).get("si_responde_motivo"))

    async def hand_over_ai(self, chat_id: str, turn_id: str, new: AiOnReason, *, now: datetime
                           ) -> Optional[AttentionInChat]:
        return attention_of(await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "ia.estado": AI_ACTIVE, "ia.turno_id": turn_id},
            {"$set": {"ia": stored_of(new), "actualizado_at": now}},
            projection={"_id": 1}, return_document=ReturnDocument.BEFORE, maxTimeMS=MAX_TIME_MS,
        ))

    async def mark_person_request(self, company_id: str, chat_id: str, *, by: str, now: datetime) -> None:
        await self.collection.update_one(
            {"chat_id": str(chat_id)},
            {"$set": {"company_id": str(company_id), "pide_persona": {"por": str(by), "at": now},
                      "actualizado_at": now},
             "$setOnInsert": {"chat_id": str(chat_id), "creado_at": now}},
            upsert=True,
        )

    async def put_ai(self, chat_id: str, *, ai: Optional[AiOnReason],
                     assign_on_escalation: Optional[AssignOnEscalation], now: datetime) -> None:
        await self.collection.update_one(
            {"chat_id": str(chat_id)},
            {"$set": {"ia": stored_of(ai), "asignar_al_escalar": stored_of(assign_on_escalation),
                      "actualizado_at": now}},
        )

    async def of_the_company(self, company_id: str, since: datetime, limit: int,
                             until: Optional[datetime] = None) -> List[AttentionInChat]:
        window: Dict[str, Any] = {"$gte": since}
        if until is not None:
            window["$lt"] = until
        cursor = self.collection.find(
            {"company_id": str(company_id), "actualizado_at": window},
            projection={"_id": 0, "chat_id": 1, "ia": 1, "seguimientos_ia": 1, "actualizado_at": 1},
        ).sort("actualizado_at", -1).limit(int(limit)).max_time_ms(MAX_TIME_MS_PAGE)
        return [attention_of(doc) for doc in await cursor.to_list(length=int(limit))]

    async def read(self, chat_id: str) -> Optional[AttentionInChat]:
        return attention_of(await self.collection.find_one({"chat_id": str(chat_id)}))

    async def current_ai(self, company_id: str, chat_id: str, turn_id: str) -> Optional[AttentionInChat]:
        return attention_of(await self.collection.find_one(
            {"chat_id": str(chat_id), "company_id": str(company_id), "ia.estado": AI_ACTIVE, "ia.turno_id": turn_id}
        ))

    async def close_ai(self, chat_id: str, turn_id: str, *, now: datetime, result: Optional[AiResult] = None,
                       clear_assignment: bool = False) -> Optional[AttentionInChat]:
        changes: Dict[str, Any] = {"ia.estado": AI_FINISHED, "ia.resultado": stored_of(result), "ia.terminada_at": now,
                                   "actualizado_at": now}
        if clear_assignment:
            changes["asignar_al_escalar"] = None
        return attention_of(await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "ia.estado": AI_ACTIVE, "ia.turno_id": turn_id},
            {"$set": changes},
            return_document=ReturnDocument.BEFORE,
        ))

    async def claim_reason_change(self, company_id: str, chat_id: str, turn_id: str, *, from_reason_id: Optional[str],
                                  to_reason_id: str, now: datetime, limit: int, since: datetime
                                  ) -> Optional[AttentionInChat]:
        recent = {"$size": {"$filter": {
            "input": {"$ifNull": [f"${REASON_CHANGES}", []]}, "as": "c", "cond": {"$gte": ["$$c.at", since]},
        }}}
        change = stored_of(ReasonChange(at=now, from_reason_id=str(from_reason_id) if from_reason_id else None,
                                        to_reason_id=str(to_reason_id), turn_id=turn_id))
        return attention_of(await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "company_id": str(company_id), "ia.estado": AI_ACTIVE, "ia.turno_id": turn_id,
             "$expr": {"$lt": [recent, int(limit)]}},
            {"$set": {"ia.estado": AI_FINISHED, "ia.terminada_at": now, "actualizado_at": now,
                      "ia.resultado": {"por": "cambio_de_motivo", "a": str(to_reason_id)}},
             "$push": {REASON_CHANGES: {"$each": [change], "$slice": -REASON_CHANGES_KEPT}}},
            projection={"_id": 1, "motivo_id": 1}, return_document=ReturnDocument.BEFORE, maxTimeMS=MAX_TIME_MS,
        ))

    async def set_ai_follow_ups(self, company_id: str, chat_id: str, value: Optional[AiFollowUps], now: datetime, *,
                                fixed_chain: Any = UNCHANGED) -> Union[AiFollowUps, StoredAsIs, None]:
        sets: Dict[str, Any] = {"company_id": str(company_id), "seguimientos_ia": stored_of(value),
                                "actualizado_at": now}
        if fixed_chain is not UNCHANGED:
            sets["seguimientos_fijos"] = stored_of(fixed_chain)
        changes: Dict[str, Any] = {"$set": sets}
        # Clearing a chat that never had a document does not create it.
        create = value is not None or (fixed_chain is not UNCHANGED and fixed_chain is not None)
        if create:
            changes["$setOnInsert"] = {"chat_id": str(chat_id), "creado_at": now}
        before = await self.collection.find_one_and_update(
            {"chat_id": str(chat_id)}, changes,
            projection={"_id": 0, "seguimientos_ia": 1}, upsert=create, return_document=ReturnDocument.BEFORE,
            maxTimeMS=MAX_TIME_MS,
        )
        return value_of(AiFollowUps, (before or {}).get("seguimientos_ia"))

    async def claim_follow_up_reply(self, company_id: str, chat_id: str, follow_up_id: str, now: datetime) -> bool:
        try:
            # `find_one_and_update` and not `update_one`: Motor's `update_one` takes no `maxTimeMS`. What it answers
            # does not matter: winning is not colliding with the unique index.
            await self.collection.find_one_and_update(
                {"chat_id": str(chat_id), "si_responde_seguimiento_id": {"$ne": str(follow_up_id)}},
                {"$set": {"si_responde_seguimiento_id": str(follow_up_id), "si_responde_at": now},
                 "$setOnInsert": {"company_id": str(company_id), "creado_at": now}},
                projection={"_id": 1}, upsert=True, maxTimeMS=MAX_TIME_MS,
            )
        except DuplicateKeyError:
            return False
        return True

    async def ai_follow_ups(self, chat_id: str) -> Union[AiFollowUps, StoredAsIs, None]:
        doc = await self.collection.find_one(
            {"chat_id": str(chat_id)}, projection={"_id": 0, "seguimientos_ia": 1}, max_time_ms=MAX_TIME_MS
        )
        return value_of(AiFollowUps, (doc or {}).get("seguimientos_ia"))

    async def fixed_chain(self, chat_id: str) -> Union[FixedFollowUpChain, StoredAsIs, None]:
        doc = await self.collection.find_one(
            {"chat_id": str(chat_id)}, projection={"_id": 0, "seguimientos_fijos": 1}, max_time_ms=MAX_TIME_MS,
        )
        return value_of(FixedFollowUpChain, (doc or {}).get("seguimientos_fijos"))

    async def claim_rebuild(self, chat_id: str, incoming_id: str, now: datetime) -> bool:
        before = await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "seguimientos_fijos.clave": {"$type": "string"},
             "seguimientos_fijos.rearmada_por": {"$ne": str(incoming_id)}},
            {"$set": {"seguimientos_fijos.rearmada_por": str(incoming_id), "seguimientos_fijos.rearmada_at": now}},
            projection={"_id": 1}, maxTimeMS=MAX_TIME_MS,
        )
        return before is not None

    async def drop_fixed_chain(self, chat_id: str, now: datetime) -> None:
        await self.collection.find_one_and_update(
            {"chat_id": str(chat_id)}, {"$set": {"seguimientos_fijos": None, "actualizado_at": now}},
            projection={"_id": 1}, maxTimeMS=MAX_TIME_MS,
        )

    async def mark_cut(self, company_id: str, chat_id: str, *, by: str, user_id: Optional[str], now: datetime) -> None:
        await self.collection.find_one_and_update(
            {"chat_id": str(chat_id)},
            {"$set": {"cortados": stored_of(FollowUpsCut(by=str(by), user_id=str(user_id) if user_id else None,
                                                         at=now)),
                      "actualizado_at": now}},
            projection={"_id": 1}, maxTimeMS=MAX_TIME_MS,
        )

    async def drop_fixed_chains_of_the_company(self, company_id: str) -> int:
        result = await self.collection.update_many(
            {"company_id": str(company_id), "seguimientos_fijos": {"$ne": None}},
            {"$set": {"seguimientos_fijos": None}},
        )
        return int(getattr(result, "modified_count", 0) or 0)

    async def mark_escalation(self, chat_id: str, mark: EscalationMark) -> None:
        await self.collection.find_one_and_update(
            {"chat_id": str(chat_id)}, {"$set": {"al_escalar": stored_of(mark)}},
            projection={"_id": 1}, maxTimeMS=MAX_TIME_MS,
        )

    async def claim_hand_over_message(self, chat_id: str, key: str, now: datetime) -> Optional[bool]:
        doc = await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "mensaje_al_derivar_enviado.clave": {"$ne": str(key)}},
            {"$set": {"mensaje_al_derivar_enviado": stored_of(HandOverMessageMark(key=str(key), at=now))}},
            projection={"_id": 1}, maxTimeMS=MAX_TIME_MS,
        )
        if doc is not None:
            return True
        exists = await self.collection.find_one(
            {"chat_id": str(chat_id)}, projection={"_id": 1}, max_time_ms=MAX_TIME_MS
        )
        return False if exists is not None else None

    async def release_hand_over_message(self, chat_id: str, key: str) -> None:
        await self.collection.update_one(
            {"chat_id": str(chat_id), "mensaje_al_derivar_enviado.clave": str(key)},
            {"$unset": {"mensaje_al_derivar_enviado": ""}},
        )

    async def escalation(self, chat_id: str) -> Union[EscalationMark, StoredAsIs, None]:
        doc = await self.collection.find_one(
            {"chat_id": str(chat_id)}, projection={"_id": 0, "al_escalar": 1}, max_time_ms=MAX_TIME_MS
        )
        return value_of(EscalationMark, (doc or {}).get("al_escalar"))

    async def clear_assignment(self, chat_id: str, now: datetime) -> Union[AiFollowUps, StoredAsIs, None]:
        before = await self.collection.find_one_and_update(
            {"chat_id": str(chat_id)},
            {"$set": {"asignar_al_escalar": None, "seguimientos_ia": None, "actualizado_at": now}},
            projection={"_id": 0, "seguimientos_ia": 1}, return_document=ReturnDocument.BEFORE,
            maxTimeMS=MAX_TIME_MS,
        )
        return value_of(AiFollowUps, (before or {}).get("seguimientos_ia"))

    async def mark_after_turn(self, chat_id: str, turn_id: str, *, done: Mapping[str, Any], complete: bool,
                              now: datetime) -> None:
        changes: Dict[str, Any] = {f"ia.{key}": value for key, value in done.items()}
        if complete:
            changes["ia.pendiente"] = False
        changes["actualizado_at"] = now
        await self.collection.update_one(
            {"chat_id": str(chat_id), "ia.turno_id": turn_id, "ia.pendiente": True}, {"$set": changes}
        )

    async def pending_after_turn(self, cutoff: datetime, limit: int) -> List[AttentionInChat]:
        cursor = (
            self.collection.find(
                {"ia.pendiente": True, "ia.estado": AI_ACTIVE, "ia.creado_at": {"$lte": cutoff}},
                projection={"_id": 0, "chat_id": 1, "company_id": 1, "ia": 1},
            )
            .sort("ia.creado_at", 1)
            .limit(limit)
            .max_time_ms(MAX_TIME_MS_SWEEP)
        )
        return [attention_of(doc) for doc in await cursor.to_list(length=limit)]

    async def take_for_sweep(self, chat_id: str, turn_id: str, *, attempts_seen: int, now: datetime
                             ) -> Optional[AttentionInChat]:
        return attention_of(await self.collection.find_one_and_update(
            {"chat_id": str(chat_id), "ia.turno_id": turn_id, "ia.estado": AI_ACTIVE, "ia.pendiente": True,
             "ia.barrido_intentos": int(attempts_seen)},
            {"$inc": {"ia.barrido_intentos": 1}, "$set": {"ia.barrido_at": now, "actualizado_at": now}},
            return_document=ReturnDocument.AFTER,
        ))
