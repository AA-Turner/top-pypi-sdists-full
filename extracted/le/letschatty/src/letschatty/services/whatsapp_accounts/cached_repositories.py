"""Redis cache-aside over the account and WABA repositories.

Every inbound webhook and every send builds an `AccountContext`, which reads the account and its
WABA. Both change only when someone connects, reconnects, renames, disconnects, picks the default
or moves the WABA, so they are cached next to the number route, with the same 10-minute expiry
(`ROUTE_TTL_SECONDS`) and the same rules:

- Only what exists is cached: an unknown account or WABA always goes to MongoDB.
- Every write through these repositories deletes the key AFTER writing, even when the write
  raised (it may have landed). A write that does not go through them (a manual edit in Atlas)
  is seen when the key expires, or at once if the key is deleted by hand:
  `whatsapp_accounts:item:<account_id>` / `whatsapp_wabas:item:<company_id>:<waba_id>`.
- The cache only saves reads: if it is down, reads go to MongoDB and a failed delete is logged
  (the stale value expires with its TTL). A cache error never fails the caller.

Wrap the Mongo repositories with these wherever the app writes or reads accounts (api-chatty's
`account_process`, the migration CLI). The account cache holds the token: it is stored as the
account document is, so the same Redis already holding the app's caches holds it.
"""
import json
import logging
from typing import Any, Dict, List, Optional

from ...models.cache.cache_protocol import CacheProtocol
from ...models.utils.types.identifier import StrObjectId
from ...models.whatsapp import WhatsAppAccount, WhatsAppBusinessAccount
from .directory import ROUTE_TTL_SECONDS
from .repositories import WhatsAppAccountRepository, WhatsAppBusinessAccountRepository

logger = logging.getLogger(__name__)

ACCOUNT_TTL_SECONDS = ROUTE_TTL_SECONDS


def account_cache_key(account_id: StrObjectId) -> str:
    return f"whatsapp_accounts:item:{account_id}"


def waba_cache_key(company_id: StrObjectId, waba_id: str) -> str:
    return f"whatsapp_wabas:item:{company_id}:{waba_id}"


async def _read(cache: CacheProtocol, key: str) -> Optional[str]:
    try:
        return await cache.get(key)
    except Exception as e:  # noqa: BLE001
        logger.error("Account cache unavailable reading %s: reading MongoDB (%s)", key, e)
        return None


async def _write(cache: CacheProtocol, key: str, value: str) -> None:
    try:
        await cache.set(key, value, ttl=ACCOUNT_TTL_SECONDS)
    except Exception as e:  # noqa: BLE001
        logger.error("Account cache unavailable writing %s: read from MongoDB anyway (%s)", key, e)


async def invalidate(cache: CacheProtocol, key: str) -> None:
    """Best effort: if the cache is down, the stale value expires with its TTL."""
    try:
        await cache.delete(key)
    except Exception as e:  # noqa: BLE001
        logger.error("Account cache unavailable invalidating %s: it expires in %ss (%s)", key, ACCOUNT_TTL_SECONDS, e)


async def _parsed(cache: CacheProtocol, key: str, parse):
    """A value that does not parse (corrupted, or written by another version of the model during a deploy) is dropped
    and MongoDB is read: a cache problem never fails the caller."""
    cached = await _read(cache, key)
    if not cached:
        return None
    try:
        return parse(cached)
    except Exception as e:  # noqa: BLE001
        logger.error("Unreadable account cache value at %s: reading MongoDB and dropping it (%s)", key, e)
        await invalidate(cache, key)
        return None


def _account_to_json(account: WhatsAppAccount) -> str:
    document = account.model_dump(mode="json", by_alias=True, exclude={"token"})
    document["token"] = account.token.get_secret_value()
    return json.dumps(document)


def _account_from_json(value: str) -> WhatsAppAccount:
    return WhatsAppAccount.from_document(json.loads(value))


def _waba_to_json(waba: WhatsAppBusinessAccount) -> str:
    return json.dumps(waba.model_dump(mode="json", by_alias=True))


def _waba_from_json(value: str) -> WhatsAppBusinessAccount:
    return WhatsAppBusinessAccount.from_document(json.loads(value))


class CachedWhatsAppAccountRepository:
    """`WhatsAppAccountRepository` that caches `get` and deletes the key on every write."""

    def __init__(self, inner: WhatsAppAccountRepository, cache: CacheProtocol):
        self.inner = inner
        self.cache = cache

    async def get(self, account_id: StrObjectId) -> Optional[WhatsAppAccount]:
        key = account_cache_key(account_id)
        cached = await _parsed(self.cache, key, _account_from_json)
        if cached is not None:
            return cached
        account = await self.inner.get(account_id)
        if account is not None:
            await _write(self.cache, key, _account_to_json(account))
        return account

    async def get_default(self, company_id: StrObjectId) -> Optional[WhatsAppAccount]:
        return await self.inner.get_default(company_id)

    async def list_by_company(self, company_id: StrObjectId) -> List[WhatsAppAccount]:
        return await self.inner.list_by_company(company_id)

    async def list_by_waba(self, waba_id: str) -> List[WhatsAppAccount]:
        return await self.inner.list_by_waba(waba_id)

    async def list_additional_connected(self) -> List[WhatsAppAccount]:
        return await self.inner.list_additional_connected()

    async def insert(self, account: WhatsAppAccount) -> None:
        try:
            await self.inner.insert(account)
        finally:
            await invalidate(self.cache, account_cache_key(account.id))

    async def delete(self, account_id: StrObjectId) -> None:
        try:
            await self.inner.delete(account_id)
        finally:
            await invalidate(self.cache, account_cache_key(account_id))

    async def update_fields(self, account_id: StrObjectId, fields: Dict[str, Any]) -> None:
        try:
            await self.inner.update_fields(account_id, fields)
        finally:
            await invalidate(self.cache, account_cache_key(account_id))

    async def move_waba(self, account_id: StrObjectId, from_waba_id: str, to_waba_id: str) -> bool:
        try:
            return await self.inner.move_waba(account_id, from_waba_id, to_waba_id)
        finally:
            await invalidate(self.cache, account_cache_key(account_id))

    async def set_default(self, company_id: StrObjectId, account_id: StrObjectId) -> None:
        """Every account of the company is deleted after the write, not only the new and the previous default: two
        concurrent calls un-default an account neither of them read before writing. Picking the default is rare."""
        try:
            await self.inner.set_default(company_id, account_id)
        finally:
            await invalidate(self.cache, account_cache_key(account_id))
            try:
                company_accounts = await self.inner.list_by_company(company_id)
            except Exception as e:  # noqa: BLE001
                logger.error("Could not list the accounts of company %s to invalidate them: they expire in %ss (%s)",
                             company_id, ACCOUNT_TTL_SECONDS, e)
                company_accounts = []
            for account in company_accounts:
                await invalidate(self.cache, account_cache_key(account.id))


class CachedWhatsAppBusinessAccountRepository:
    """`WhatsAppBusinessAccountRepository` that caches `get` and deletes the key on every write."""

    def __init__(self, inner: WhatsAppBusinessAccountRepository, cache: CacheProtocol):
        self.inner = inner
        self.cache = cache

    async def get(self, company_id: StrObjectId, waba_id: str) -> Optional[WhatsAppBusinessAccount]:
        key = waba_cache_key(company_id, waba_id)
        cached = await _parsed(self.cache, key, _waba_from_json)
        if cached is not None:
            return cached
        waba = await self.inner.get(company_id, waba_id)
        if waba is not None:
            await _write(self.cache, key, _waba_to_json(waba))
        return waba

    async def upsert(self, waba: WhatsAppBusinessAccount) -> WhatsAppBusinessAccount:
        try:
            return await self.inner.upsert(waba)
        finally:
            await invalidate(self.cache, waba_cache_key(waba.company_id, waba.waba_id))

    async def list_by_company(self, company_id: StrObjectId) -> List[WhatsAppBusinessAccount]:
        return await self.inner.list_by_company(company_id)
