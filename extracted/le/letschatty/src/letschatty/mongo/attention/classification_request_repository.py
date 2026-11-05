"""`ClassificationRequestRepository` on `clasificaciones_de_motivo`: the same operations, filters and updates that
`atencion/pedidos.py` of api-chatty ran (`PedidosDeClasificacion`): an `insert_one`, an `update_many` that replaces the
chat's active ones, `find_one`s (the active one by chat, one by id, the projected «is it current?»), the conditional
`find_one_and_update` of every transition (`AFTER`), an `update_one` while classifying and the sorted `find` of the
sweep. An id that is not an `ObjectId` reads and writes nothing.

The stored shape is known only here: the Spanish keys of `STORED_NAMES`, `_id` as an `ObjectId`, the stored values
untouched. A request read from a document (or built from the classifier's dict) gives its keys back in that document's
order, as `main` handed them to its callers; one built without a document, in the order of `STORED_NAMES`, then the
ones the model does not name.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional, Sequence

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import ValidationError
from pymongo import ReturnDocument

from ...domain.attention.classification_requests import ClassificationRequest
from ...domain.attention.states import CLASSIFYING, REPLACED

COLLECTION = "clasificaciones_de_motivo"

#: Model field → stored key. `id` is `_id`, an `ObjectId`.
STORED_NAMES: Dict[str, str] = {
    "id": "_id", "company_id": "company_id", "chat_id": "chat_id", "state": "estado", "active": "activo",
    "round": "ronda", "calls": "llamadas", "call_id": "llamada_id", "new_messages": "mensajes_nuevos",
    "can_ask": "puede_preguntar", "entry": "entrada", "is_new": "es_nuevo", "is_first_message": "es_primer_mensaje",
    "since": "desde", "welcome_fast_answer_id": "bienvenida_fast_answer_id", "notice_sent": "aviso_enviado",
    "source": "fuente", "text": "texto", "question": "pregunta", "options": "opciones",
    "original_phrase": "frase_original", "asked_at": "pregunta_at", "created_at": "creado_at",
    "updated_at": "actualizado_at", "expires_at": "vence_at", "result": "resultado", "source_hint": "pista_de_fuente",
    "dispatch_at": "despachar_at", "cap_at": "tope_at", "correctable_at": "corregible_at",
    "applied_reason_id": "motivo_aplicado_id", "applied_origin": "origen_aplicado", "correctable_by": "corregible_por",
    "source_candidates": "candidatos_de_la_fuente", "ai_removed": "ia_quitada", "removed_ai_config": "ia_quitada_config",
    "new_content": "contenido_nuevo", "last_result": "ultimo_resultado", "base_calls": "llamadas_base",
    "correcting": "corrigiendo", "reclassifications": "reclasificaciones",
    "general_inquiry_applied": "consulta_general_aplicada", "general_inquiry_at": "consulta_general_at",
    "correction": "correccion",
}
_FIELD_OF = {stored: field for field, stored in STORED_NAMES.items()}
_READ_ORDER = "_mongo_read_order"


def _oid(request_id: Any) -> Optional[ObjectId]:
    if isinstance(request_id, ObjectId):
        return request_id
    try:
        return ObjectId(str(request_id))
    except (InvalidId, TypeError):
        return None


def request_of(document: Mapping[str, Any]) -> ClassificationRequest:
    """The request a stored document (or the stored keys of a change) holds: exactly its fields."""
    fields: Dict[str, Any] = {}
    other: Dict[str, Any] = {}
    for key, value in document.items():
        name = _FIELD_OF.get(key)
        if name is None or (name == "id" and not isinstance(value, ObjectId)):
            # An `_id` that is not an `ObjectId` (none in prod) comes back as stored, not converted.
            other[key] = value
        else:
            fields[name] = str(value) if name == "id" else value
    while True:
        try:
            request = ClassificationRequest(**fields, **({"other_fields": other} if other else {}))
            # The order of the document, for `document_of`: a storage detail, so it is not a field of the model.
            object.__setattr__(request, _READ_ORDER, tuple(document))
            return request
        except ValidationError as error:
            # A stored value of another type (none in prod) is carried untouched by its stored name, as `main`
            # passed it through: one odd document never breaks a read (the sweep reads a batch).
            refused = {e["loc"][0] for e in error.errors() if e["loc"] and e["loc"][0] in fields}
            if not refused:
                raise
            for name in refused:
                other[STORED_NAMES[name]] = document[STORED_NAMES[name]]
                del fields[name]


def document_of(request: ClassificationRequest) -> Dict[str, Any]:
    """The stored shape of the fields the request was built with (`_id` back to an `ObjectId`). In the order of the
    document it was read from, if any; otherwise each in the place `STORED_NAMES` gives it, also a value carried in
    `other_fields` under a name of `STORED_NAMES`, and the keys the model does not name go last, in their order."""
    built = request.model_fields_set
    other = request.other_fields
    document: Dict[str, Any] = {}
    for name, stored in STORED_NAMES.items():
        if name in built:
            value = getattr(request, name)
            document[stored] = ObjectId(value) if name == "id" and value is not None else value
        elif stored in other:
            document[stored] = other[stored]
    document.update({key: value for key, value in other.items() if key not in document})
    order = [key for key in getattr(request, _READ_ORDER, ()) if key in document]
    return {**{key: document[key] for key in order}, **{k: v for k, v in document.items() if k not in order}}


class MongoClassificationRequestRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def open(self, request: ClassificationRequest) -> str:
        document = document_of(request)
        await self.collection.insert_one(document)
        return str(document["_id"])

    async def replace_active(self, chat_id: str, *, now: datetime) -> None:
        await self.collection.update_many(
            {"chat_id": str(chat_id), "activo": True},
            {"$set": {"activo": False, "estado": REPLACED, "actualizado_at": now}},
        )

    async def active_of(self, chat_id: str) -> Optional[ClassificationRequest]:
        document = await self.collection.find_one({"chat_id": str(chat_id), "activo": True})
        return None if document is None else request_of(document)

    async def get(self, request_id: str) -> Optional[ClassificationRequest]:
        oid = _oid(request_id)
        if oid is None:
            return None
        document = await self.collection.find_one({"_id": oid})
        return None if document is None else request_of(document)

    async def is_current(self, company_id: str, request_id: str, *, chat_id: str, call_id: str) -> bool:
        oid = _oid(request_id)
        if oid is None:
            return False
        query = {"_id": oid, "company_id": str(company_id), "chat_id": str(chat_id), "activo": True,
                 "estado": CLASSIFYING, "llamada_id": str(call_id)}
        return await self.collection.find_one(query, {"_id": 1}) is not None

    async def transition(self, request_id: str, *, from_states: Sequence[str], changes: ClassificationRequest,
                         call_id: Optional[str] = None, expired_by: Optional[datetime] = None,
                         increment: Optional[Mapping[str, int]] = None) -> Optional[ClassificationRequest]:
        oid = _oid(request_id)
        if oid is None:
            return None
        query: Dict[str, Any] = {"_id": oid, "activo": True, "estado": {"$in": list(from_states)}}
        if call_id is not None:
            query["llamada_id"] = call_id
        if expired_by is not None:
            query["vence_at"] = {"$lte": expired_by}
        update: Dict[str, Any] = {"$set": document_of(changes)}
        if increment:
            update["$inc"] = {STORED_NAMES.get(name, name): amount for name, amount in increment.items()}
        document = await self.collection.find_one_and_update(query, update, return_document=ReturnDocument.AFTER)
        return None if document is None else request_of(document)

    async def mark_new_messages(self, request_id: str, *, now: datetime, content: bool) -> None:
        oid = _oid(request_id)
        if oid is None:
            return
        fields: Dict[str, Any] = {"mensajes_nuevos": True, "actualizado_at": now}
        if content:
            fields["contenido_nuevo"] = True
        await self.collection.update_one({"_id": oid, "activo": True, "estado": CLASSIFYING}, {"$set": fields})

    async def expired(self, *, now: datetime, limit: int) -> List[ClassificationRequest]:
        cursor = self.collection.find({"activo": True, "vence_at": {"$lte": now}}).sort("vence_at", 1).limit(limit)
        return [request_of(document) async for document in cursor]
