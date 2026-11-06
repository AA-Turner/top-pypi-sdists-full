"""`MetaEpisodeRepository` on `meta_problemas_de_pago` or `meta_numeros_limitados`: the same operations api-chatty's
`ProblemaDePagoService` ran, filter by filter (`find_one_and_update` on the open one; the upsert filtered by
`estado != abierto`, whose `DuplicateKeyError` adds the rejection with an `update_one`; the banner stored only if
`abierto_at` matches; the close by `find_one_and_update`, which returns the document as it was before; the `find`s of
the sweep and of the open set, which read only `_id`; and the three reads of Chatty Health).

The stored shape is known only here: `{_id, estado, company_id, company_name, display_phone_number, waba_id,
portfolio_id, account_id, account_name, abierto_at, ultimo_rechazo_at, rechazos, detalle, banner_notification_id,
cerrado_at, cerrado_por}`; the episodes stored before the accounts lack `waba_id`, `account_id`, `account_name` and
`portfolio_id`. No cache."""
from __future__ import annotations

from datetime import datetime
from typing import Any, AsyncIterator, List, Mapping, Optional

from pymongo.errors import DuplicateKeyError

from ...domain.whatsapp.meta_episodes import CLOSED, CLOSED_BY_SILENCE, OPEN, EpisodeKey, MetaEpisode

PAYMENT_PROBLEMS = "meta_problemas_de_pago"
LIMITED_NUMBERS = "meta_numeros_limitados"

#: Stored field → field of `MetaEpisode`.
_FIELDS = {
    "estado": "status", "company_id": "company_id", "company_name": "company_name",
    "display_phone_number": "display_phone_number", "waba_id": "waba_id", "portfolio_id": "portfolio_id",
    "account_id": "account_id", "account_name": "account_name", "abierto_at": "opened_at",
    "ultimo_rechazo_at": "last_rejection_at", "rechazos": "rejections", "detalle": "detail",
    "banner_notification_id": "banner_notification_id", "cerrado_at": "closed_at", "cerrado_por": "closed_by",
}


def episode_of(document: Mapping[str, Any]) -> MetaEpisode:
    """Only the stored fields: a missing one keeps the model's default (a missing `rechazos` is 0)."""
    values = {field: document[stored] for stored, field in _FIELDS.items() if stored in document}
    return MetaEpisode(id=str(document["_id"]), **values)


class MongoMetaEpisodeRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def add_rejection(self, company_id: str, key: EpisodeKey, at: datetime) -> bool:
        return await self.collection.find_one_and_update({"_id": key.id, "estado": OPEN}, _added(at)) is not None

    async def open(self, company_id: str, episode: MetaEpisode) -> bool:
        try:
            await self.collection.find_one_and_update(
                {"_id": episode.id, "estado": {"$ne": OPEN}},
                {
                    "$set": {
                        "estado": OPEN,
                        "company_id": episode.company_id,
                        "company_name": episode.company_name,
                        "display_phone_number": episode.display_phone_number,
                        "waba_id": episode.waba_id,
                        "portfolio_id": episode.portfolio_id,
                        "account_id": episode.account_id,
                        "account_name": episode.account_name,
                        "abierto_at": episode.opened_at,
                        "ultimo_rechazo_at": episode.last_rejection_at,
                        "rechazos": 1,
                        "detalle": episode.detail,
                        "banner_notification_id": None,
                    },
                    "$unset": {"cerrado_at": "", "cerrado_por": ""},
                },
                upsert=True,
            )
        except DuplicateKeyError:
            # Another worker opened it between the two writes: this rejection is part of theirs.
            await self.collection.update_one({"_id": episode.id, "estado": OPEN}, _added(episode.last_rejection_at))
            return False
        return True

    async def set_banner(self, company_id: str, key: EpisodeKey, opened_at: datetime, notification_id: str) -> None:
        await self.collection.update_one(
            {"_id": key.id, "estado": OPEN, "abierto_at": opened_at},
            {"$set": {"banner_notification_id": notification_id}},
        )

    async def close(self, company_id: str, key: EpisodeKey, *, at: datetime, by: str,
                    last_rejection_before: datetime) -> Optional[MetaEpisode]:
        before = {"$lt": last_rejection_before}
        # The sweep's filter was its `find`'s plus the `_id`; the delivery's started by the `_id`.
        query = ({"estado": OPEN, "ultimo_rechazo_at": before, "_id": key.id} if by == CLOSED_BY_SILENCE
                 else {"_id": key.id, "estado": OPEN, "ultimo_rechazo_at": before})
        document = await self.collection.find_one_and_update(
            query, {"$set": {"estado": CLOSED, "cerrado_at": at, "cerrado_por": by}},
        )
        return None if document is None else episode_of(document)

    async def due(self, last_rejection_before: datetime) -> AsyncIterator[EpisodeKey]:
        async for document in self.collection.find(
                {"estado": OPEN, "ultimo_rechazo_at": {"$lt": last_rejection_before}}, {"_id": 1}):
            yield EpisodeKey.from_id(str(document["_id"]))

    async def open_keys(self) -> List[EpisodeKey]:
        keys = []
        async for document in self.collection.find({"estado": OPEN}, {"_id": 1}):
            keys.append(EpisodeKey.from_id(str(document["_id"])))
        return keys

    async def companies_with_open(self) -> List[Optional[str]]:
        return await self.collection.distinct("company_id", {"estado": OPEN})

    async def count_closed_since(self, since: datetime) -> int:
        return await self.collection.count_documents({"estado": CLOSED, "cerrado_at": {"$gte": since}})

    async def oldest_open(self, limit: int) -> List[MetaEpisode]:
        return [episode_of(d) async for d in self.collection.find({"estado": OPEN}).sort("abierto_at", 1).limit(limit)]


def _added(at: datetime) -> dict:
    return {"$inc": {"rechazos": 1}, "$set": {"ultimo_rechazo_at": at}}
