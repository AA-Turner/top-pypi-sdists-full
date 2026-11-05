"""`ProfileSnapshotRepository` on `company_whatsapp_profiles`: the same filters and writes that
`company/whatsapp_accounts/profile_snapshots.py` of api-chatty ran (a `find_one` per question, a `$set` per write, an
`insert_one` that the unique partial index `uniq_company_account` turns into «already there»). No cache, as before."""
from __future__ import annotations

from typing import Any, Dict, Optional

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from ...domain.whatsapp.profile_snapshots import CONTENT_FIELDS, ProfileSnapshot

COLLECTION = "company_whatsapp_profiles"
WITHOUT_ACCOUNT = {"$exists": False}


class MongoProfileSnapshotRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def first_of_company(self, company_id: str) -> Optional[ProfileSnapshot]:
        return self._model(await self.collection.find_one({"company_id": company_id}))

    async def of_account(self, company_id: str, account_id: str) -> Optional[ProfileSnapshot]:
        return self._model(await self.collection.find_one({"company_id": company_id, "account_id": account_id}))

    async def without_account(self, company_id: str) -> Optional[ProfileSnapshot]:
        return self._model(await self.collection.find_one({"company_id": company_id, "account_id": WITHOUT_ACCOUNT}))

    async def save_first_of_company(self, company_id: str, snapshot: ProfileSnapshot) -> None:
        await self.collection.update_one(
            {"company_id": company_id}, {"$set": {"company_id": company_id, **self._content(snapshot)}}, upsert=True)

    async def update_of_account(self, company_id: str, snapshot: ProfileSnapshot) -> bool:
        result = await self.collection.update_one(
            {"company_id": company_id, "account_id": snapshot.account_id}, {"$set": self._stamped(company_id, snapshot)})
        return bool(result.matched_count)

    async def adopt_without_account(self, company_id: str, snapshot: ProfileSnapshot) -> bool:
        result = await self.collection.update_one(
            {"company_id": company_id, "account_id": WITHOUT_ACCOUNT}, {"$set": self._stamped(company_id, snapshot)})
        return bool(result.matched_count)

    async def add(self, company_id: str, snapshot: ProfileSnapshot) -> bool:
        document = self._stamped(company_id, snapshot)
        try:
            await self.collection.insert_one(document)
        except DuplicateKeyError:
            return False
        finally:
            # `insert_one` gives the dict its `_id` before sending it, refused or not: the snapshot keeps it.
            if "_id" in document:
                snapshot.id = str(document["_id"])
        return True

    async def stamp_without_account(self, company_id: str, account_id: str, phone_number_id: Optional[str]) -> None:
        await self.collection.update_one(
            {"company_id": company_id, "account_id": WITHOUT_ACCOUNT},
            {"$set": {"account_id": account_id, "phone_number_id": phone_number_id}},
        )

    @staticmethod
    def _content(snapshot: ProfileSnapshot) -> Dict[str, Any]:
        return {field: getattr(snapshot, field) for field in CONTENT_FIELDS}

    @classmethod
    def _stamped(cls, company_id: str, snapshot: ProfileSnapshot) -> Dict[str, Any]:
        """The content, then the identity: the order the refresh stored a new document in. With the id of an earlier
        `add`, the `_id` too: the refresh wrote the dict that `insert_one` had given one."""
        fields = {**cls._content(snapshot), "company_id": company_id, "account_id": snapshot.account_id,
                  "phone_number_id": snapshot.phone_number_id}
        if snapshot.id is not None:
            fields["_id"] = ObjectId(snapshot.id)
        return fields

    @staticmethod
    def _model(doc: Optional[Dict[str, Any]]) -> Optional[ProfileSnapshot]:
        return ProfileSnapshot.model_validate(doc) if doc is not None else None
