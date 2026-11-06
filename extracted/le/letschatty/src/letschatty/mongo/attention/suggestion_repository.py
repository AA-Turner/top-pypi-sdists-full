"""`ReasonSuggestionRepository` on `sugerencias_de_motivos`: the `insert_one`, the `update_one` conditional on `pendiente`
(the dispatch's error), the `find_one` by id and company and the `update_one` of the result, conditional on the company,
`pendiente` and `vence_at`, that `Sugerencias` of api-chatty ran. The stored shape is known only here."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional

from bson import ObjectId
from bson.errors import InvalidId

from ...domain.attention.states import SUGGESTION_ERROR, SUGGESTION_PENDING, SUGGESTION_READY
from ...domain.attention.suggestions import ReasonSuggestionRequest

COLLECTION = "sugerencias_de_motivos"


def _oid(request_id: Any) -> Optional[ObjectId]:
    try:
        return ObjectId(str(request_id))
    except (InvalidId, TypeError):
        return None


def suggestion_of(document: Mapping[str, Any]) -> ReasonSuggestionRequest:
    return ReasonSuggestionRequest(
        id=str(document["_id"]) if document.get("_id") is not None else None, company_id=document.get("company_id"),
        state=document.get("estado"), created_at=document.get("creado_at"), expires_at=document.get("vence_at"),
        delete_at=document.get("borrar_at"), reasons=document.get("motivos") or [],
        analyzed=int(document.get("analizados") or 0), error=document.get("error"))


def document_of(request: ReasonSuggestionRequest) -> Dict[str, Any]:
    """The stored shape of a request just built, with the keys in the order `main` inserted them."""
    document: Dict[str, Any] = {
        "_id": ObjectId(request.id), "company_id": request.company_id, "estado": request.state,
        "creado_at": request.created_at, "vence_at": request.expires_at, "borrar_at": request.delete_at,
        "motivos": list(request.reasons), "analizados": request.analyzed}
    if request.error is not None:
        document["error"] = request.error
    return document


class MongoReasonSuggestionRepository:
    def __init__(self, collection):
        self.collection = collection

    async def add(self, request: ReasonSuggestionRequest) -> None:
        await self.collection.insert_one(document_of(request))

    async def fail_if_pending(self, request_id: str, error: str) -> None:
        await self.collection.update_one({"_id": _oid(request_id), "estado": SUGGESTION_PENDING},
                                         {"$set": {"estado": SUGGESTION_ERROR, "error": error}})

    async def of_company(self, company_id: str, request_id: str) -> Optional[ReasonSuggestionRequest]:
        oid = _oid(request_id)
        if oid is None:
            return None
        document = await self.collection.find_one({"_id": oid, "company_id": str(company_id)})
        return None if document is None else suggestion_of(document)

    async def resolve_if_pending(self, company_id: str, request_id: str, now: datetime, *, error: Optional[str] = None,
                                 reasons: Optional[List[Dict[str, Any]]] = None, analyzed: int = 0) -> bool:
        if error is not None:
            changes: Dict[str, Any] = {"estado": SUGGESTION_ERROR, "error": error, "recibido_at": now}
        else:
            changes = {"estado": SUGGESTION_READY, "motivos": reasons or [], "recibido_at": now}
            if analyzed:
                changes["analizados"] = analyzed
        result = await self.collection.update_one(
            {"_id": _oid(request_id), "company_id": str(company_id), "estado": SUGGESTION_PENDING,
             "vence_at": {"$gt": now}}, {"$set": changes})
        return bool(getattr(result, "matched_count", 0))
