"""Redis cache in front of any `GlobalBetasRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Not `AssetCache` (ADR-006 of api-chatty): the global betas never went through the asset service. This does what
api-chatty's legacy `BetasGlobales` did, with its key, value, TTL, logger and texts:

- the key `plataforma:betas_globales` holds the cleaned list as JSON, for 60 s (short on purpose: a switch the staff
  flips has to hold within a minute even if the clear did not reach Redis);
- the cache is built by `cache_factory` on each use, where the legacy service built it: before a read, outside its
  `try` (an error building it goes up), and inside the `try` of the clear after a write (a WARNING);
- a read: the cache first; a failed cache read is a WARNING and a miss; a cached value that is not a JSON list (or is
  empty) is a silent miss; on a miss, the store, and the result is cached (a failed cache write is a WARNING);
- a switch: the store first (its error goes up and nothing is cleared), then the key is deleted (a failed delete is a
  WARNING: the old value expires alone).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Callable, List, Optional

from ...domain.company.global_betas import GlobalBetasRepository, clean_global_betas

logger = logging.getLogger("BetasGlobales")

KEY = "plataforma:betas_globales"
TTL = 60


class CachedGlobalBetasRepository:
    def __init__(self, inner: GlobalBetasRepository, cache_factory: Callable[[], Any]):
        self.inner, self.cache_factory = inner, cache_factory

    async def enabled(self) -> List[str]:
        cache = self.cache_factory()
        try:
            cached = await cache.get(KEY)
        except Exception as e:
            logger.warning("betas globales: no pude leer la caché: %s", e)
            cached = None
        if cached:
            try:
                value = json.loads(cached)
                if isinstance(value, list):
                    return clean_global_betas(value)
            except ValueError:
                pass
        betas = await self.inner.enabled()
        try:
            await cache.set(KEY, json.dumps(betas), ttl=TTL)
        except Exception as e:
            logger.warning("betas globales: no pude escribir la caché: %s", e)
        return betas

    async def switch(self, beta: str, on: bool, *, updated_by: Optional[str], updated_at: datetime) -> List[str]:
        betas = await self.inner.switch(beta, on, updated_by=updated_by, updated_at=updated_at)
        try:
            await self.cache_factory().delete(KEY)
        except Exception as e:
            logger.warning("betas globales: no pude invalidar la caché: %s", e)
        return betas
