"""The one writer of the `company_routing:*` keys (api-chatty `docs/empresa/repositorio.md`, REQ-EMR-010, REQ-EMR-011).

Not `AssetCache` (ADR-006 of api-chatty): these keys never went through the asset service. Their value is the whole
company, their TTL 24 h, and a failure writing or clearing them is a WARNING of the `Companies` logger: a routing key
that is stale or missing falls back to Mongo. Only dropping the keys read before a change lets its failure through.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import List, Sequence

from ...models.cache import CacheProtocol
from ...models.company.empresa import EmpresaModel
from .company_keys import ROUTING_KEY_TTL, is_deleted, routing_keys_of

logger = logging.getLogger("Companies")


class RedisRoutingIndex:
    def __init__(self, cache: CacheProtocol):
        self.cache = cache

    def keys_of(self, company: EmpresaModel) -> List[str]:
        return routing_keys_of(company)

    async def index(self, company: EmpresaModel) -> None:
        if not company.active_for_messaging:
            return
        try:
            t0 = time.perf_counter()
            value = json.dumps(company.model_dump(by_alias=True, mode='json'))
            t1 = time.perf_counter()
            keys = routing_keys_of(company)
            if is_deleted(company):
                # A deleted company keeps its aliases and origins, often the same ones as the company that replaced
                # it: writing those keys would hand them back to it. Its number still routes to it (see
                # docs/ruteo-sin-empresas-borradas.md), so that key is kept.
                keys = [k for k in keys if k.startswith("company_routing:phone:")]
            await asyncio.gather(*[self.cache.set(key, value, ttl=ROUTING_KEY_TTL) for key in keys])
            t2 = time.perf_counter()
            logger.debug("[routing_keys] company=%s serialize=%.0fms redis_sets=%d sets=%.0fms total=%.0fms",
                         company.id, (t1 - t0) * 1000, len(keys), (t2 - t1) * 1000, (t2 - t0) * 1000)
        except Exception as e:
            logger.warning("Failed to set routing keys for company %s: %s", company.id, e)

    async def drop(self, company: EmpresaModel) -> None:
        try:
            keys = routing_keys_of(company)
            if keys:
                await self.cache.delete_many(keys)
        except Exception as e:
            logger.warning("Failed to clear routing keys for company %s: %s", company.id, e)

    async def drop_previous(self, keys: Sequence[str]) -> None:
        await self.cache.delete_many(keys)
