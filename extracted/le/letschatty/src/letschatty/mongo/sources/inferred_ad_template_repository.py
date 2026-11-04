"""`InferredAdTemplateRepository` on the `inferred_ad_templates` collection: the same Mongo operations the legacy
`InferredAdTemplateStore` of api-chatty ran (`find_one_and_update` with upsert or without, `update_one`), with the same
filters and the same update documents, field by field and in the same order."""
from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from pymongo import ReturnDocument

from ...domain.sources.inferred_ad_templates import day_key


def _identity(company_id: str, account_id: Optional[str], normalized_body: str) -> dict:
    """The filter of ONE template: no account key when there is no account (`{"account_id": None}` in an upsert would
    WRITE a null)."""
    identity = {"company_id": str(company_id), "normalized_body": normalized_body}
    if account_id:
        identity["account_id"] = str(account_id)
    return identity


class MongoInferredAdTemplateRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def record_labeled(self, company_id: str, account_id: Optional[str], normalized_body: str, *,
                             body_sample: str, template_hash: str, hll_base: Optional[str], ad_source_id: str,
                             ad_id: str, at: datetime, stale_days: Sequence[datetime]) -> Optional[dict]:
        prefix = f"linked_ads.{ad_source_id}"
        on_insert = {
            "company_id": str(company_id),
            "normalized_body": normalized_body,
            "body_sample": body_sample,
            "template_hash": template_hash,
            "status": "learning",
            "created_at": at,
        }
        if account_id:
            on_insert["account_id"] = str(account_id)
            on_insert["hll_base"] = hll_base
        update = {
            "$setOnInsert": on_insert,
            "$inc": {f"{prefix}.days.{day_key(at)}": 1, f"{prefix}.total": 1},
            "$set": {
                f"{prefix}.ad_id": ad_id,
                f"{prefix}.last_seen_at": at,
                "updated_at": at,
            },
            "$unset": {f"{prefix}.days.{day_key(day)}": "" for day in stale_days},
        }
        return await self.collection.find_one_and_update(
            _identity(company_id, account_id, normalized_body),
            update, upsert=True, return_document=ReturnDocument.AFTER,
        )

    async def drop_linked_ad(self, company_id: str, account_id: Optional[str], normalized_body: str,
                             ad_source_id: str) -> None:
        await self.collection.update_one(
            _identity(company_id, account_id, normalized_body),
            {"$unset": {f"linked_ads.{ad_source_id}": ""}},
        )

    async def record_orphan(self, company_id: str, account_id: Optional[str], normalized_body: str) -> Optional[dict]:
        return await self.collection.find_one_and_update(
            _identity(company_id, account_id, normalized_body),
            {"$inc": {"orphan_msgs": 1}},
            return_document=ReturnDocument.AFTER,
        )

    async def set_status(self, company_id: str, account_id: Optional[str], normalized_body: str, status: str, *,
                         updated_at: datetime, activated_at: Optional[datetime]) -> None:
        update = {"$set": {"status": status, "updated_at": updated_at}}
        if activated_at is not None:
            update["$set"]["activated_at"] = activated_at
        await self.collection.update_one(_identity(company_id, account_id, normalized_body), update)

    async def record_decision(self, company_id: str, account_id: Optional[str], template_hash: str, kind: str) -> None:
        # The same text is a template on every account (same hash): the decision counts on the given account's.
        identity = {"company_id": str(company_id), "template_hash": template_hash}
        if account_id:
            identity["account_id"] = str(account_id)
        await self.collection.update_one(identity, {"$inc": {"decisions.total": 1, f"decisions.{kind}": 1}})
