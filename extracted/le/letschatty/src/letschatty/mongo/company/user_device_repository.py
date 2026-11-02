"""`UserDeviceRepository` on the `user_devices` collection. Not a catalog (ADR-010 of api-chatty): rows are upserted
by their natural key, never read or written by id, and nothing is cached. Every write is one atomic Mongo operation,
the same ones the asset service ran, because notifications-lambda writes the same rows directly
(`last_push_sent_at`, `token_status`, `invalidated_at`, `last_push_error_at`)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ...domain.company.user_devices import DeviceKey, RegisteredDevice
from ...models.push_notifications import DeviceStatus, TokenStatus, UserDevice


class MongoUserDeviceRepository:
    """Reuses the asset collection of the legacy service (its Motor collection), so the stored row keeps its shape."""

    def __init__(self, collection):
        self.collection = collection

    @property
    def _rows(self):
        return self.collection.collection

    @staticmethod
    def _query(key: DeviceKey) -> Dict[str, Any]:
        return {"company_id": key.company_id, "user_id": key.user_id, "installation_id": key.installation_id}

    async def register(self, key: DeviceKey, *, platform: str, fcm_token: str, app_version: Optional[str],
                       now: datetime) -> RegisteredDevice:
        """⚠️ The UNIQUE index on the key (`uniq_company_user_installation`) is what makes this safe, not the upsert:
        without it two concurrent upserts that both match nothing BOTH insert. With it the loser gets
        `DuplicateKeyError` and retries into the winner.

        Everything that says "this installation is live" goes in `$set`, so a device coming back from logout — or from
        a soft delete — is fully reactivated. Only immutable identity and `created_at` may be `$setOnInsert`; putting
        `is_active` or `deleted_at` there would leave a re-registered install permanently invisible to the sender."""
        query = self._query(key)
        update = {
            "$set": {
                "fcm_token": fcm_token,
                "platform": platform,
                "app_version": app_version,
                "token_status": TokenStatus.VALID,
                "status": DeviceStatus.ACTIVE,
                "is_active": True,
                "deleted_at": None,
                "online": True,
                "updated_at": now,
                # A fresh token is not a dead token: clear what the sender stamped when it gave up on the previous one.
                "invalidated_at": None,
                "last_push_error_at": None,
                "last_push_error_code": None,
            },
            "$setOnInsert": query | {"created_at": now, "last_seen_at": None},
        }
        try:
            doc = await self._rows.find_one_and_update(query, update, upsert=True,
                                                       return_document=ReturnDocument.AFTER)
        except DuplicateKeyError:
            # Lost the insert race: the winner exists now, so the same update without upsert lands on it.
            doc = await self._rows.find_one_and_update(query, update, return_document=ReturnDocument.AFTER)
            if doc is None:
                raise
        return RegisteredDevice(UserDevice.model_validate(doc), doc["_id"])

    async def retire_others_with_token(self, fcm_token: str, keep: RegisteredDevice, now: datetime) -> int:
        """No unique index can hold this — `fcm_token` is nullable and legitimately repeats across retired rows — so
        the invariant is enforced here, on write."""
        result = await self._rows.update_many(
            {"fcm_token": fcm_token, "_id": {"$ne": keep.stored_id}, "is_active": True,
             "status": DeviceStatus.ACTIVE},
            {"$set": {"status": DeviceStatus.LOGGED_OUT, "is_active": False, "online": False, "updated_at": now}},
        )
        return result.modified_count

    async def touch(self, key: DeviceKey, now: datetime) -> Optional[UserDevice]:
        return await self._set(key, {"last_seen_at": now, "online": True, "updated_at": now})

    async def log_out(self, key: DeviceKey, now: datetime) -> Optional[UserDevice]:
        """`is_active` moves with `status`: the sender checks both."""
        return await self._set(key, {"status": DeviceStatus.LOGGED_OUT, "is_active": False, "online": False,
                                     "updated_at": now})

    async def find(self, key: DeviceKey) -> Optional[UserDevice]:
        doc = await self._rows.find_one(self._query(key))
        return None if doc is None else UserDevice.model_validate(doc)

    async def _set(self, key: DeviceKey, fields: Dict[str, Any]) -> Optional[UserDevice]:
        doc = await self._rows.find_one_and_update(self._query(key), {"$set": fields},
                                                   return_document=ReturnDocument.AFTER)
        return None if doc is None else UserDevice.model_validate(doc)

