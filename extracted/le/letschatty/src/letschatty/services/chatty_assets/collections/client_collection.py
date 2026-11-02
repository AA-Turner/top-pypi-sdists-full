"""Las personas: la colección `clients`, compartida por los chats de cada persona.

Una persona por teléfono o BSUID dentro de la empresa (índices únicos y parciales
`{company_id, waid}` y `{company_id, user_id}`, declarados en api-chatty). Esta colección es la
única que escribe la preview de la persona en `chats` (fan-out): editar a la persona escribe
`clients` y, en la misma pasada, todos sus chats.

El lock por identidad para el alta (dos webhooks del mismo contacto nuevo a la vez) vive en
api-chatty, como el lock de creación de chats.
"""
import logging
from typing import Sequence, Any, Dict, List, Optional, Union

from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError
from zoneinfo import ZoneInfo

from ..asset_service import AssetCollection
from ....models.chat.chat_client_preview import ChatClientPreview
from ....models.chat.client import Client
from ....models.chat.no_contactar import NoContactar
from ....models.chat.marcas_de_meta import MarcaDeMeta, TipoDeMarca
from ....models.data_base.mongo_connection import MongoConnection
from ....models.utils.custom_exceptions.custom_exceptions import IdentityAlreadyTaken, NotFoundError
from ....models.utils.types.identifier import StrObjectId

logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


#: Así llegan las claves del formulario en los cambios pendientes de la persona (`Chat.set_person_form_value`).
FORM_PREFIX = "lead_form_data."


def _is_path_safe(key: str) -> bool:
    """Una clave que se puede usar como tramo de una ruta de Mongo sin cambiar su significado."""
    return bool(key) and "." not in key and not key.startswith("$")


def person_update(fields: Dict[str, Any], now: datetime) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """El update de `clients` para estos cambios de la persona.

    Las claves del formulario se escriben de a una (`lead_form_data.<clave>`), sin pisar las otras.
    Pero una clave con punto («Nro. de cliente») o que empieza con `$` no se puede usar como
    tramo de ruta: el punto la anidaría y el `$` haría fallar el update. Para esas, el update es
    un pipeline con `$setField`, que trata el nombre como literal (MongoDB ≥ 5.0).
    """
    form = {name[len(FORM_PREFIX):]: value for name, value in fields.items() if name.startswith(FORM_PREFIX)}
    if all(_is_path_safe(key) for key in form):
        return {"$set": {**fields, "updated_at": now}}
    plain = {name: {"$literal": value} for name, value in fields.items() if not name.startswith(FORM_PREFIX)}
    form_expr: Any = {"$ifNull": ["$lead_form_data", {}]}
    for key, value in form.items():
        form_expr = {"$setField": {"field": {"$literal": key}, "input": form_expr, "value": {"$literal": value}}}
    return [{"$set": {**plain, "lead_form_data": form_expr, "updated_at": now}}]


class ClientCollection(AssetCollection[Client, None]):  # type: ignore[type-var]
    def __init__(self, connection: MongoConnection, chats: Optional[AsyncIOMotorCollection] = None):
        super().__init__(
            collection="clients",
            asset_type=Client,
            connection=connection,
            create_instance_method=Client.default_create_instance_method,
            preview_type=None,
        )
        self.chats: AsyncIOMotorCollection = chats if chats is not None else self.db["chats"]

    async def find_by_identity(
        self,
        company_id: StrObjectId,
        waid: Optional[str] = None,
        user_id: Optional[str] = None,
        include_deleted: bool = False,
        parent_bsuid: Optional[str] = None,
        bsuids: Sequence[str] = (),
    ) -> Optional[Client]:
        """La persona por teléfono, después por BSUID y después por BSUID padre. El teléfono gana:
        es la identidad de siempre y es igual en todos los portfolios.

        A BSUID is looked up in the per-portfolio list (`bsuids.bsuid`) and in the legacy scalar
        `user_id` (documents written before the multi-account migration).

        `include_deleted`: los índices únicos no miran `deleted_at`, así que una persona borrada
        que conserva su identidad la sigue ocupando (ver `find_or_insert`)."""
        lookups: List[Dict[str, Any]] = []
        if waid:
            lookups.append({"waid": waid})
        for bsuid in dict.fromkeys(b for b in (user_id, *bsuids) if b):
            # Two lookups, never an `$or`: both indexes are partial, and Mongo cannot use a partial
            # index inside an `$or` — it scanned the whole collection (prod 2026-10-22, ~1.4 s per message).
            lookups.append({"bsuids.bsuid": bsuid})
            lookups.append({"user_id": bsuid})
        if parent_bsuid:
            lookups.append({"parent_bsuids": parent_bsuid})
        for lookup in lookups:
            query: Dict[str, Any] = {"company_id": company_id, **lookup}
            if not include_deleted:
                query["deleted_at"] = None
            document = await self.collection.find_one(query)
            if document is not None:
                return self.create_instance(document)
        return None

    async def find_or_insert(self, person: Client) -> Client:
        """La persona con esa identidad en la empresa; si no hay ninguna, se da de alta `person`.

        Si dos altas de la misma persona corren a la vez, la que pierde contra el índice único
        lee la que ganó: las dos terminan con la misma persona. Si la identidad la ocupa una
        persona BORRADA (los índices no miran `deleted_at`), el contacto volvió: se la restaura
        en vez de fallar para siempre en cada mensaje suyo.
        """
        parent = person.parent_bsuids[0] if person.parent_bsuids else None
        # A person met on an additional account carries its BSUID only in `bsuids` (`user_id` is the
        # default account's): without them a phone-less contact never matched and the insert hit the
        # unique `bsuids.bsuid` index, losing the message (dev 2026-10-12).
        bsuids = [entry.bsuid for entry in person.bsuids]
        existing = await self.find_by_identity(person.company_id, waid=person.waid, user_id=person.user_id, parent_bsuid=parent, bsuids=bsuids)
        if existing is not None:
            return await self._attach_missing_bsuids(existing, person)
        try:
            await self.insert(person)
            return person
        except DuplicateKeyError:
            holder = await self.find_by_identity(person.company_id, waid=person.waid, user_id=person.user_id, include_deleted=True, parent_bsuid=parent, bsuids=bsuids)
            if holder is None:
                raise
            if holder.deleted_at is not None:
                await self.collection.update_one({"_id": ObjectId(holder.id)}, {"$set": {"deleted_at": None, "updated_at": _now()}})
                holder.deleted_at = None
            return await self._attach_missing_bsuids(holder, person)

    async def _attach_missing_bsuids(self, existing: Client, person: Client) -> Client:
        """The person was found (by phone, say) on a number of a portfolio where we did not have
        their BSUID yet: record it. Without it, their next phone-less message to that number
        found nobody and created a second person and a second chat (dev 2026-10-12).
        A BSUID that already belongs to someone else is a merge case: logged, never raised."""
        known = {entry.portfolio_id for entry in existing.bsuids}
        for entry in person.bsuids:
            if entry.portfolio_id in known:
                continue
            try:
                if await self.add_bsuid(existing.id, entry.portfolio_id, entry.bsuid):
                    existing.bsuids.append(entry)
                    known.add(entry.portfolio_id)
            except IdentityAlreadyTaken as error:
                logger.warning("[BSUID] %s (portfolio %s) already belongs to another person; not attached to %s: %s",
                               entry.bsuid, entry.portfolio_id, existing.id, error)
        return existing

    async def get_many(self, client_ids: List[StrObjectId]) -> List[Client]:
        documents = await self.collection.find({"_id": {"$in": [ObjectId(i) for i in client_ids]}}).to_list(None)
        return [self.create_instance(d) for d in documents]

    async def update_person(self, client_id: StrObjectId, fields: Dict[str, Any]) -> List[StrObjectId]:
        """Escribe campos de la persona y hace fan-out de los de la preview a todos sus chats.

        `fields` va con nombres de `Client` (`name`, `email`, `lead_form_data.dni`...).
        Devuelve los ids de los chats tocados, para que el llamador despierte sus workflows y
        emita los eventos.
        """
        if not fields:
            return []
        now = _now()
        try:
            result = await self.collection.update_one({"_id": ObjectId(client_id)}, person_update(fields, now))
        except DuplicateKeyError as error:
            raise IdentityAlreadyTaken(f"El teléfono o el BSUID de {fields} ya es de otra persona (persona {client_id})") from error
        if result.matched_count == 0:
            raise NotFoundError(f"No client {client_id}")
        preview_fields = {f"client.{name}": value for name, value in fields.items() if name in ChatClientPreview.FIELDS}
        chat_ids = await self.chat_ids_of(client_id)
        if preview_fields and chat_ids:
            await self.chats.update_many({"client_id": client_id}, {"$set": {**preview_fields, "updated_at": now}})
        return chat_ids

    async def set_no_contactar(self, client_id: StrObjectId, value: Optional[NoContactar]) -> List[StrObjectId]:
        """Marca (o, con `None`, desmarca) «No contactar» en la persona y en la preview de todos sus
        chats. Desmarcar BORRA la clave en los dos lados: la bandeja filtra «marcado» como
        `client.no_contactar: {$exists: true}`, así que un `null` lo seguiría mostrando marcado.

        Devuelve los ids de los chats tocados (como `update_person`)."""
        now = _now()
        if value is None:
            on_person = {"$unset": {"no_contactar": ""}, "$set": {"updated_at": now}}
            on_chats = {"$unset": {"client.no_contactar": ""}, "$set": {"updated_at": now}}
        else:
            document = value.model_dump()
            on_person = {"$set": {"no_contactar": document, "updated_at": now}}
            on_chats = {"$set": {"client.no_contactar": document, "updated_at": now}}
        result = await self.collection.update_one({"_id": ObjectId(client_id)}, on_person)
        if result.matched_count == 0:
            raise NotFoundError(f"No client {client_id}")
        chat_ids = await self.chat_ids_of(client_id)
        if chat_ids:
            await self.chats.update_many({"client_id": client_id}, on_chats)
        return chat_ids

    async def set_marca_de_meta(self, client_id: StrObjectId, tipo: TipoDeMarca,
                                value: Optional[MarcaDeMeta]) -> List[StrObjectId]:
        """Pone (o, con `None`, saca) una marca de Meta en la persona y en la preview de todos sus chats,
        como `set_no_contactar`. Sacar BORRA la clave en los dos lados. Devuelve los ids de los chats tocados."""
        now = _now()
        clave = f"marcas_de_meta.{TipoDeMarca(tipo).value}"
        if value is None:
            on_person = {"$unset": {clave: ""}, "$set": {"updated_at": now}}
            on_chats = {"$unset": {f"client.{clave}": ""}, "$set": {"updated_at": now}}
        else:
            document = value.model_dump()
            on_person = {"$set": {clave: document, "updated_at": now}}
            on_chats = {"$set": {f"client.{clave}": document, "updated_at": now}}
        result = await self.collection.update_one({"_id": ObjectId(client_id)}, on_person)
        if result.matched_count == 0:
            raise NotFoundError(f"No client {client_id}")
        chat_ids = await self.chat_ids_of(client_id)
        if chat_ids:
            await self.chats.update_many({"client_id": client_id}, on_chats)
        return chat_ids

    async def chat_ids_of(self, client_id: StrObjectId) -> List[StrObjectId]:
        documents = await self.chats.find({"client_id": client_id}, projection={"_id": 1}).to_list(None)
        return [str(d["_id"]) for d in documents]

    async def add_bsuid(self, client_id: StrObjectId, portfolio_id: str, bsuid: str) -> bool:
        """Record the person's BSUID in `portfolio_id` if they have none there yet. Idempotent:
        returns False when the portfolio already had one. Raises `IdentityAlreadyTaken` when that
        BSUID belongs to another person of the company (a merge case)."""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(client_id), "bsuids.portfolio_id": {"$ne": portfolio_id}},
                {"$push": {"bsuids": {"portfolio_id": portfolio_id, "bsuid": bsuid}}, "$set": {"updated_at": _now()}},
            )
        except DuplicateKeyError as error:
            raise IdentityAlreadyTaken(f"BSUID {bsuid} already belongs to another person (person {client_id})") from error
        return result.modified_count == 1

    async def replace_bsuid(self, company_id: StrObjectId, portfolio_id: str, previous: str, new: str) -> List[StrObjectId]:
        """Meta regenerated the person's BSUID in one portfolio (`user_changed_user_id`, sent once
        per portfolio). Updates the person's entry for that portfolio and every chat that used the
        previous BSUID, which by definition are chats of accounts of that portfolio.
        Returns the ids of the chats touched."""
        now = _now()
        try:
            await self.collection.update_one(
                # `bsuids.bsuid` equality next to the `$elemMatch`: the only index on it is PARTIAL
                # (`uniq_company_bsuids`, `bsuids.bsuid $exists`) and the planner can't prove the partial
                # filter from an `$elemMatch` alone, so it fell to a COLLSCAN. The `$elemMatch` stays so
                # portfolio and bsuid must match in the SAME element.
                {"company_id": company_id, "bsuids.bsuid": previous, "bsuids": {"$elemMatch": {"portfolio_id": portfolio_id, "bsuid": previous}}},
                {"$set": {"bsuids.$.bsuid": new, "updated_at": now}},
            )
        except DuplicateKeyError as error:
            raise IdentityAlreadyTaken(f"BSUID {new} already belongs to another person") from error
        documents = await self.chats.find({"company_id": company_id, "bsuid": previous}, projection={"_id": 1}).to_list(None)
        chat_ids = [str(d["_id"]) for d in documents]
        if chat_ids:
            await self.chats.update_many({"_id": {"$in": [ObjectId(i) for i in chat_ids]}}, {"$set": {"bsuid": new, "updated_at": now}})
        return chat_ids

    async def merge(self, keep_id: StrObjectId, drop_id: StrObjectId) -> Client:
        """Une dos personas que resultaron ser la misma (llegó por BSUID y después apareció su
        teléfono, que ya tenía otra). Los chats de `drop` pasan a `keep`, `keep` completa lo que
        le falta con los datos de `drop` (en conflicto gana `keep`) y `drop` se borra.

        Es el único caso en que el `client_id` de un chat cambia.
        """
        keep, drop = await self.get_by_id(keep_id), await self.get_by_id(drop_id)
        merged_form = {**drop.lead_form_data, **keep.lead_form_data}
        filled = {
            name: getattr(drop, name)
            for name in ("waid", "user_id", "user_id_parent", "username", "email", "country", "external_id", "document_id")
            if getattr(keep, name) in (None, "") and getattr(drop, name) not in (None, "")
        }
        identity = _merged_identity(keep, drop)
        # "No contactar" is the PERSON's and anyone marked stays marked: a person merged into another keeps the
        # most recent mark of the two (by `desde`). Without this the mark of `drop` was lost with it.
        mark = _latest_no_contactar(keep, drop)
        if mark is not None and mark is not keep.no_contactar:
            filled["no_contactar"] = mark.model_dump()
        # Meta's marks too: per type, the one with the latest rejection.
        marcas = _merged_marcas(keep, drop)
        if marcas:
            filled["marcas_de_meta"] = {tipo: marca.model_dump() for tipo, marca in marcas.items()}
        now = _now()
        # The dropped person releases every identity first: the unique indexes would reject keep's update otherwise.
        await self.collection.update_one(
            {"_id": ObjectId(drop_id)},
            {"$set": {"deleted_at": now, "updated_at": now}, "$unset": {"waid": "", "user_id": "", "bsuids": "", "parent_bsuids": ""}},
        )
        await self.collection.update_one({"_id": ObjectId(keep_id)}, {"$set": {**filled, **identity, "lead_form_data": merged_form, "updated_at": now}})
        merged = await self.get_by_id(keep_id)
        preview = {f"client.{k}": v for k, v in merged.preview().model_dump().items() if k not in ("no_contactar", "marcas_de_meta")}
        update: Dict[str, Any] = {"$set": {"client_id": keep_id, **preview, "updated_at": now}}
        if merged.no_contactar is not None:
            update["$set"]["client.no_contactar"] = merged.no_contactar.model_dump()
        else:
            # Never a `null`: the inbox counts "marked" as `client.no_contactar: {$exists: true}`.
            update["$unset"] = {"client.no_contactar": ""}
        if merged.marcas_de_meta:
            update["$set"]["client.marcas_de_meta"] = {tipo: marca.model_dump() for tipo, marca in merged.marcas_de_meta.items()}
        else:
            update.setdefault("$unset", {})["client.marcas_de_meta"] = ""
        await self.chats.update_many({"client_id": {"$in": [keep_id, drop_id]}}, update)
        return merged


def _merged_marcas(keep: Client, drop: Client) -> Dict[str, MarcaDeMeta]:
    """Meta's marks of two persons: per type, the one with the latest rejection (`keep` wins a tie)."""
    merged: Dict[str, MarcaDeMeta] = dict(drop.marcas_de_meta)
    for tipo, marca in keep.marcas_de_meta.items():
        if tipo not in merged or marca.ultimo_rechazo >= merged[tipo].ultimo_rechazo:
            merged[tipo] = marca
    return merged


def _latest_no_contactar(keep: Client, drop: Client) -> Optional[NoContactar]:
    """The more recent "No contactar" of two persons (`keep` wins a tie), or None if neither is marked."""
    marks = [m for m in (keep.no_contactar, drop.no_contactar) if m is not None]
    return max(marks, key=lambda m: m.desde) if marks else None


def _merged_identity(keep: Client, drop: Client) -> Dict[str, Any]:
    """The per-portfolio identities of a merge: keep's BSUID wins in a portfolio both have."""
    bsuids = {entry.portfolio_id: entry for entry in drop.bsuids}
    bsuids.update({entry.portfolio_id: entry for entry in keep.bsuids})
    parents = list(dict.fromkeys([*keep.parent_bsuids, *drop.parent_bsuids]))
    identity: Dict[str, Any] = {}
    if bsuids:
        identity["bsuids"] = [entry.model_dump() for entry in bsuids.values()]
    if parents:
        identity["parent_bsuids"] = parents
    return identity
