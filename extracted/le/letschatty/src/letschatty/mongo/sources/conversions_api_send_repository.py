"""`ConversionsApiSendRepository` on `meta_notification_logs`: the one read api-chatty's `main` sent (`find` by the
company as text with five fields, sorted by `created_at` desc as the prod index `company_id_1_created_at_-1`, capped).

Not a simple catalog (ADR-010 of api-chatty): another service writes it, and it is only read by company, newest first.
"""
from __future__ import annotations

from typing import Any, List, Optional

_FIELDS = {"event_type": 1, "response_status": 1, "response_body": 1, "created_at": 1, "payload": 1}


class StoredConversionsApiSend:
    """A send as `meta_notification_logs` stores it, each field read when it is asked for, with `main`'s expressions:
    a missing or empty `payload`, `data` or `user_data` reads as none, and one that is not an object raises."""

    def __init__(self, document: dict):
        self._document = document

    def _user_data(self) -> Any:
        event = ((self._document.get("payload") or {}).get("data") or [{}])[0]
        return event.get("user_data") or {}

    def _response(self) -> Any:
        return self._document.get("response_body") or {}

    @property
    def ctwa_clid(self) -> Optional[str]:
        return self._user_data().get("ctwa_clid")

    @property
    def external_id(self) -> Optional[str]:
        return self._user_data().get("external_id")

    @property
    def event_type(self) -> Any:
        return self._document.get("event_type")

    @property
    def response_status(self) -> Any:
        return self._document.get("response_status")

    @property
    def created_at(self) -> Any:
        return self._document.get("created_at")

    @property
    def fbtrace_id(self) -> Any:
        return self._response().get("fbtrace_id")

    @property
    def events_received(self) -> Any:
        return self._response().get("events_received")

    @property
    def warnings(self) -> List[Any]:
        return self._response().get("messages") or []


class MongoConversionsApiSendRepository:
    """On a Motor collection, resolved by whoever wires it (api-chatty, when its legacy service is built)."""

    def __init__(self, collection):
        self.collection = collection

    async def latest_of_company(self, company_id: str, limit: int) -> List[StoredConversionsApiSend]:
        documents = await self.collection.find(
            {"company_id": str(company_id)}, _FIELDS).sort("created_at", -1).to_list(length=limit)
        return [StoredConversionsApiSend(document) for document in documents]
