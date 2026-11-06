"""Redis cache in front of any `CompanyRepository` (ADR-001: the cache is a decorator, not part of Mongo).

The order of `forget` is the rule of api-chatty's `docs/empresa-en-memoria.md`: the asset, the settings, the betas, the
routing keys and, in a `finally`, the version. AFTER clearing the cache: if the version changed before, another worker
could reload the old model (still in Redis) and keep the new version, that is, old forever.

- a change: the store writes and reads the company back; that fresh copy goes through the asset's own read (it is
  written back to its key, as `get_by_id(ignore_cache=True)` always did) and is the one forgotten, so the routing keys
  cleared are the ones of the number the company has NOW; a failure forgetting it is a WARNING.
- `create`, `soft_delete`, `restore`: `forget`, whose failure on the settings or the betas goes up, with the write done.
- a failed version mark never raises: a write already done in Mongo cannot fail because of it.
"""
from __future__ import annotations

import logging
import uuid
from typing import List, Optional, Sequence

from ...domain.company.company import CompanyRepository, RoutingIndex
from ...models.cache import CacheProtocol
from ...models.company.empresa import EmpresaModel
from ...services.chatty_assets.base_container_with_collection import CacheConfig
from ..asset_cache import AssetCache
from .company_keys import betas_key, settings_key, version_key

logger = logging.getLogger("Companies")


class CachedCompanyRepository:
    def __init__(self, inner: CompanyRepository, cache: CacheProtocol, routing: RoutingIndex,
                 config: Optional[CacheConfig] = None):
        self.inner, self.cache, self.routing = inner, cache, routing
        self.assets = AssetCache[EmpresaModel]("empresas", EmpresaModel, cache, config)

    async def get(self, company_id: str, *, ignore_cache: bool = False) -> EmpresaModel:
        return await self.assets.item(company_id, lambda: self.inner.get(company_id), ignore_cache=ignore_cache)

    async def live(self, *, ignore_cache: bool = False) -> List[EmpresaModel]:
        return await self.assets.all(None, self.inner.live, ignore_cache=ignore_cache)

    async def deleted(self) -> List[EmpresaModel]:
        return await self.inner.deleted()

    async def by_shopify_domain(self, shop_domain: str) -> Optional[EmpresaModel]:
        return await self.inner.by_shopify_domain(shop_domain)

    async def create(self, company: EmpresaModel) -> None:
        await self.inner.create(company)
        await self.forget(company)

    async def soft_delete(self, company: EmpresaModel) -> None:
        await self.inner.soft_delete(company)
        await self.forget(company)

    async def restore(self, company_id: str) -> EmpresaModel:
        company = await self.inner.restore(company_id)
        await self.forget(company)
        return company

    async def forget(self, company: EmpresaModel) -> None:
        try:
            await self.assets.invalidate(company.id, getattr(company, "company_id", None))
            await self.assets.drop_key(settings_key(company.id), on_failure=None)
            await self.assets.drop_key(betas_key(company.id), on_failure=None)
            await self.routing.drop(company)
        finally:
            await self._mark_version(company.id)

    async def forget_quietly(self, company: EmpresaModel) -> None:
        try:
            await self.forget(company)
            logger.debug("Cache busted for company %s", company.id)
        except Exception as e:
            logger.warning("bust_cache failed for company %s: %s", company.id, e)

    async def version(self, company_id: str) -> Optional[str]:
        return await self.cache.get(version_key(company_id))

    async def _mark_version(self, company_id: str) -> None:
        """A random value and not a counter: it only has to be different (`CacheProtocol` has no INCR). No TTL: if the
        key is lost, each worker reloads once and that is it."""
        try:
            await self.cache.set(version_key(company_id), uuid.uuid4().hex)
        except Exception as e:
            logger.warning("No se pudo marcar la versión de la empresa %s: %s", company_id, e)

    async def _changed(self, company_id: str, fresh: EmpresaModel) -> EmpresaModel:
        async def the_fresh_copy() -> EmpresaModel:
            return fresh
        await self.assets.item(company_id, the_fresh_copy, ignore_cache=True)
        await self.forget_quietly(fresh)
        return fresh

    async def save_name(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_name(company))

    async def save_test_group(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_test_group(company))

    async def save_organization(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_organization(company))

    async def save_internal_use(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_internal_use(company))

    async def save_executive_chatty(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_executive_chatty(company))

    async def save_chattyless(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_chattyless(company))

    async def save_hammer_credentials(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_hammer_credentials(company))

    async def save_messaging_settings(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_messaging_settings(company))

    async def save_display_phone_number(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_display_phone_number(company))

    async def save_friendly_aliases(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_friendly_aliases(company))

    async def save_allowed_origins(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_allowed_origins(company))

    async def save_cc_template_name(self, company: EmpresaModel) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_cc_template_name(company))

    async def save_registration_extras(self, company: EmpresaModel, *, display_phone_number: bool,
                                       industry: bool) -> EmpresaModel:
        fresh = await self.inner.save_registration_extras(company, display_phone_number=display_phone_number,
                                                          industry=industry)
        return await self._changed(company.id, fresh)

    async def save_integration(self, company: EmpresaModel, field: str) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_integration(company, field))

    async def save_connection(self, company: EmpresaModel, *, waba: bool, display_phone_number: bool,
                              executive_chatty: bool) -> EmpresaModel:
        fresh = await self.inner.save_connection(company, waba=waba, display_phone_number=display_phone_number,
                                                 executive_chatty=executive_chatty)
        return await self._changed(company.id, fresh)

    async def save_resolved_waba(self, company: EmpresaModel, *, only_if_phone: str) -> EmpresaModel:
        return await self._changed(company.id, await self.inner.save_resolved_waba(company, only_if_phone=only_if_phone))

    async def save_meta_profile(self, company: EmpresaModel, fields: Sequence[str], *,
                                only_if_phone: str) -> EmpresaModel:
        fresh = await self.inner.save_meta_profile(company, fields, only_if_phone=only_if_phone)
        return await self._changed(company.id, fresh)

    async def add_beta(self, company_id: str, beta: str) -> EmpresaModel:
        return await self._changed(company_id, await self.inner.add_beta(company_id, beta))

    async def remove_beta(self, company_id: str, beta: str) -> EmpresaModel:
        return await self._changed(company_id, await self.inner.remove_beta(company_id, beta))
