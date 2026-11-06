"""Redis cache in front of any `ReceptionRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used (`recepciones:all:{company}`, `…:item:{id}`, `…:previews:
{company}` and the global lists): the legacy `Recepciones` service still serves the callers that have not moved, and
the attention state clears the same company. The list read (`list_live`) is the runtime's hot path: one cache read
when it is warm, and Mongo only on a miss. A write clears the item and the lists AFTER the store accepted it.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Union

from ...domain.attention.receptions import FlowStateWrite, StoredBlocks, StoredFlowStates
from ...models.company.assets.recepcion import Ausencia, Recepcion
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogById


class CachedReceptionRepository(CachedCatalogById[Recepcion]):
    prefix = "recepciones"
    item_type = Recepcion

    async def set_account_block(self, company_id: StrObjectId, reception_id: StrObjectId, account_id: str,
                                fields: Dict[str, Any]) -> None:
        await self.inner.set_account_block(company_id, reception_id, account_id, fields)
        await self.assets.invalidate(reception_id, company_id)

    async def set_absence(self, company_id: StrObjectId, reception_id: StrObjectId,
                          by_account: Dict[Optional[str], Union[Ausencia, Dict[str, Any]]]) -> None:
        await self.inner.set_absence(company_id, reception_id, by_account)
        await self.assets.invalidate(reception_id, company_id)

    async def stored_blocks(self, company_id: StrObjectId, fields: Sequence[str]) -> Optional[StoredBlocks]:
        return await self.inner.stored_blocks(company_id, fields)

    async def flow_states(self, company_id: StrObjectId, *, max_time_ms: int) -> Optional[StoredFlowStates]:
        return await self.inner.flow_states(company_id, max_time_ms=max_time_ms)

    async def set_flow_state(self, company_id: StrObjectId, state: str, *, account_id: Optional[str] = None,
                             only_if_missing: bool = False) -> FlowStateWrite:
        # No clear of the item or the lists: the model does not carry `atencion_estado`, and in `main` this write went
        # straight to the collection (the state's own cache is api-chatty's).
        return await self.inner.set_flow_state(company_id, state, account_id=account_id, only_if_missing=only_if_missing)

    async def swap_default_block(self, company_id: StrObjectId, reception_id: Any, previous_account_id: str,
                                 to_previous: Dict[str, Any], to_base: Dict[str, Any],
                                 retired_account_id: Optional[str]) -> None:
        await self.inner.swap_default_block(company_id, reception_id, previous_account_id, to_previous, to_base,
                                            retired_account_id)
        # Not `assets.invalidate`: in `main` this clear was not wrapped, so a Redis that fails here fails the request.
        await self.assets.drop([self.assets.item_key(str(reception_id)), *self.assets.list_keys(str(company_id))],
                               on_failure=None)
