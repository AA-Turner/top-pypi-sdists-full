"""`ReceptionRepository` on the `recepciones` collection: the whole-document merge (`MongoCatalogById`) plus the dotted
`$set` of an account's block or of the absence and the swap of the blocks (the only place with the dotted paths, the
`$set`/`$unset` operators and the stored form of a value: an `Ausencia` as its JSON dump, a date as its ISO text). Only
Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Union

from ...domain.attention.receptions import ABSENCE_FLAGS, BLOCK_FIELDS, FlowStateWrite, StoredBlocks, StoredFlowStates
from ...models.company.assets.recepcion import Ausencia, Recepcion
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogById


class MongoReceptionRepository(MongoCatalogById[Recepcion]):
    """Reuses the asset collection of the legacy `Recepciones` service, so the stored document keeps its shape
    (cintia-lambdas and copilot may read it straight from Mongo)."""

    async def set_account_block(self, company_id: StrObjectId, reception_id: StrObjectId, account_id: str,
                                fields: Dict[str, Any]) -> None:
        unknown = [name for name in fields if name not in BLOCK_FIELDS]
        if unknown:
            raise ValueError(f"Not fields of an account's block: {unknown}")
        await self.collection.partial_update(
            reception_id, {f"account_receptions.{account_id}.{name}": _stored(value) for name, value in fields.items()})

    async def set_absence(self, company_id: StrObjectId, reception_id: StrObjectId,
                          by_account: Dict[Optional[str], Union[Ausencia, Dict[str, Any]]]) -> None:
        paths: Dict[str, Any] = {}
        for account_id, absence in by_account.items():
            prefix = "ausencia" if account_id is None else f"account_receptions.{account_id}.ausencia"
            if isinstance(absence, Ausencia):
                paths[prefix] = _stored(absence)
                continue
            unknown = [name for name in absence if name not in ABSENCE_FLAGS]
            if unknown:
                raise ValueError(f"Not flags of the absence: {unknown}")
            for name, value in absence.items():
                paths[f"{prefix}.{name}"] = value.isoformat() if hasattr(value, "isoformat") else value
        await self.collection.partial_update(reception_id, paths)

    async def stored_blocks(self, company_id: StrObjectId, fields: Sequence[str]) -> Optional[StoredBlocks]:
        doc = await self.collection.collection.find_one({"company_id": str(company_id), "deleted_at": None})
        if doc is None:
            return None
        return StoredBlocks(reception_id=doc["_id"], base={k: doc[k] for k in fields if k in doc},
                            accounts=doc.get("account_receptions") or {})

    async def flow_states(self, company_id: StrObjectId, *, max_time_ms: int) -> Optional[StoredFlowStates]:
        doc = await self.collection.collection.find_one(
            {"company_id": str(company_id), "deleted_at": None},
            projection={"_id": 0, "atencion_estado": 1, "account_receptions": 1}, max_time_ms=max_time_ms)
        if doc is None:
            return None
        blocks = doc.get("account_receptions")
        accounts = {str(k): v["atencion_estado"] for k, v in blocks.items()
                    if isinstance(v, dict) and "atencion_estado" in v} if isinstance(blocks, dict) else {}
        return StoredFlowStates(base=doc.get("atencion_estado"), accounts=accounts)

    async def set_flow_state(self, company_id: StrObjectId, state: str, *, account_id: Optional[str] = None,
                             only_if_missing: bool = False) -> FlowStateWrite:
        if account_id and (not isinstance(account_id, str) or any(c in account_id for c in ".$ \t\n/\\")):
            # Same rule as the use case (`valid_account_id`): the id must not build another path of the document.
            raise ValueError(f"Id de cuenta inválido: {account_id!r}")
        field = "atencion_estado" if not account_id else f"account_receptions.{account_id}.atencion_estado"
        query: Dict[str, Any] = {"company_id": str(company_id), "deleted_at": None}
        if only_if_missing:
            query["atencion_estado"] = {"$exists": False}
        result = await self.collection.collection.update_one(query, {"$set": {field: state}})
        return FlowStateWrite(matched=int(getattr(result, "matched_count", 0)),
                              modified=int(getattr(result, "modified_count", 0)))

    async def swap_default_block(self, company_id: StrObjectId, reception_id: Any, previous_account_id: str,
                                 to_previous: Dict[str, Any], to_base: Dict[str, Any],
                                 retired_account_id: Optional[str]) -> None:
        previous = {f"account_receptions.{previous_account_id}.{name}": value for name, value in to_previous.items()}
        update: Dict[str, Any] = {"$set": {**previous, **to_base}}
        if retired_account_id is not None:
            update["$unset"] = {f"account_receptions.{retired_account_id}": ""}
        await self.collection.collection.update_one({"_id": reception_id}, update)


def _stored(value: Any) -> Any:
    """How a block value is stored: an `Ausencia` as its JSON dump (dates as ISO text), as `main` wrote it."""
    return value.model_dump(mode="json") if isinstance(value, Ausencia) else value
