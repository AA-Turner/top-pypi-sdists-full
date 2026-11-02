"""Motor implementations of the WhatsApp account ports.

Uniqueness is enforced by the database (indexes declared in api-chatty,
`Database/indexes/whatsapp_accounts_indexes.py`), not by read-then-write checks:
- `whatsapp_numbers._id` = phone_number_id → a number lives in one company.
- `whatsapp_wabas {company_id, waba_id}` and `whatsapp_portfolios {company_id, portfolio_id}` unique.
- `whatsapp_accounts {company_id}` unique where `is_default: true` → one default per company.
"""
from typing import Any, Dict, List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ...models.utils.types.identifier import StrObjectId
from ...models.whatsapp import (
    DefaultAccountExists,
    NumberAlreadyClaimed,
    WhatsAppAccount,
    WhatsAppAccountNotFound,
    WhatsAppAccountStatus,
    WhatsAppBusinessAccount,
    WhatsAppNumber,
    WhatsAppPortfolio,
)
from ...models.whatsapp.time import utc_now

ACCOUNTS = "whatsapp_accounts"
NUMBERS = "whatsapp_numbers"
WABAS = "whatsapp_wabas"
PORTFOLIOS = "whatsapp_portfolios"


class MongoWhatsAppAccountRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[ACCOUNTS]

    async def get(self, account_id: StrObjectId) -> Optional[WhatsAppAccount]:
        document = await self.collection.find_one({"_id": ObjectId(account_id)})
        return WhatsAppAccount.from_document(document) if document else None

    async def get_default(self, company_id: StrObjectId) -> Optional[WhatsAppAccount]:
        document = await self.collection.find_one({"company_id": company_id, "is_default": True})
        return WhatsAppAccount.from_document(document) if document else None

    async def list_by_company(self, company_id: StrObjectId) -> List[WhatsAppAccount]:
        documents = await self.collection.find({"company_id": company_id}).sort("created_at", 1).to_list(None)
        return [WhatsAppAccount.from_document(d) for d in documents]

    async def list_by_waba(self, waba_id: str) -> List[WhatsAppAccount]:
        documents = await self.collection.find({"waba_id": waba_id}).to_list(None)
        return [WhatsAppAccount.from_document(d) for d in documents]

    async def list_additional_connected(self) -> List[WhatsAppAccount]:
        documents = await self.collection.find(
            {"is_default": False, "status": WhatsAppAccountStatus.CONNECTED.value}
        ).to_list(None)
        return [WhatsAppAccount.from_document(d) for d in documents]

    async def insert(self, account: WhatsAppAccount) -> None:
        document = account.to_document()
        document["_id"] = ObjectId(account.id)
        try:
            await self.collection.insert_one(document)
        except DuplicateKeyError as e:
            raise DefaultAccountExists(company_id=str(account.company_id)) from e

    async def delete(self, account_id: StrObjectId) -> None:
        await self.collection.delete_one({"_id": ObjectId(account_id)})

    async def update_fields(self, account_id: StrObjectId, fields: Dict[str, Any]) -> None:
        await self.collection.update_one({"_id": ObjectId(account_id)}, {"$set": {**fields, "updated_at": utc_now()}})

    async def move_waba(self, account_id: StrObjectId, from_waba_id: str, to_waba_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(account_id), "waba_id": from_waba_id},
            {"$set": {"waba_id": to_waba_id, "updated_at": utc_now()}},
        )
        return result.modified_count == 1

    async def set_default(self, company_id: StrObjectId, account_id: StrObjectId) -> None:
        """Unset first: the unique partial index allows a single default per company. Two writes,
        so if the second one does not land the previous default is put back: a company is never
        left without a default account (every request that does not pick a number needs one)."""
        now = utc_now()
        previous = [d["_id"] async for d in self.collection.find(
            {"company_id": company_id, "is_default": True, "_id": {"$ne": ObjectId(account_id)}}, {"_id": 1}
        )]
        if previous:
            await self.collection.update_many({"_id": {"$in": previous}}, {"$set": {"is_default": False, "updated_at": now}})
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(account_id), "company_id": company_id},
                {"$set": {"is_default": True, "updated_at": now}},
            )
            if result.matched_count != 1:
                raise WhatsAppAccountNotFound(f"Account {account_id} is not from company {company_id}", company_id=str(company_id))
        except Exception:
            if previous:
                await self.collection.update_one({"_id": previous[0]}, {"$set": {"is_default": True, "updated_at": utc_now()}})
            raise


class MongoWhatsAppNumberRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[NUMBERS]

    async def get(self, phone_number_id: str) -> Optional[WhatsAppNumber]:
        document = await self.collection.find_one({"_id": phone_number_id})
        return WhatsAppNumber.from_document(document) if document else None

    async def claim(self, number: WhatsAppNumber) -> WhatsAppNumber:
        bound = {
            "company_id": number.company_id,
            "account_id": number.account_id,
            "display_phone_number": number.display_phone_number,
            "digits": number.digits,
            "active": True,
            "since": utc_now(),
            "until": None,
            "taken_down_at": None,
        }
        for _ in range(2):
            # Its own company re-binds it; anyone may take a number that was taken down.
            document = await self.collection.find_one_and_update(
                {"_id": number.phone_number_id, "$or": [{"company_id": number.company_id}, {"taken_down_at": {"$ne": None}}]},
                {"$set": bound},
                return_document=ReturnDocument.AFTER,
            )
            if document is not None:
                return WhatsAppNumber.from_document(document)
            try:
                await self.collection.insert_one({**number.to_document(), **bound})
                return number.model_copy(update=bound)
            except DuplicateKeyError:
                # Someone holds this _id: either another company (reject) or a concurrent claim
                # by this company (the next loop turn binds it).
                holder = await self.collection.find_one({"_id": number.phone_number_id}, {"company_id": 1, "taken_down_at": 1})
                if holder is not None and holder["company_id"] != number.company_id and holder.get("taken_down_at") is None:
                    raise NumberAlreadyClaimed(
                        f"Phone number {number.phone_number_id} belongs to another company",
                        company_id=str(number.company_id),
                    )
        raise NumberAlreadyClaimed(f"Could not claim phone number {number.phone_number_id}", company_id=str(number.company_id))

    async def deactivate(self, phone_number_id: str) -> None:
        await self.collection.update_one({"_id": phone_number_id}, {"$set": {"active": False, "until": utc_now()}})

    async def live_by_digits(self, digits: str) -> List[WhatsAppNumber]:
        documents = await self.collection.find({"digits": digits, "taken_down_at": None}).to_list(None)
        return [WhatsAppNumber.from_document(d) for d in documents]

    async def take_down(self, phone_number_id: str) -> None:
        now = utc_now()
        await self.collection.update_one({"_id": phone_number_id}, {"$set": {"taken_down_at": now, "active": False, "until": now}})

    async def list_by_account(self, account_id: StrObjectId) -> List[WhatsAppNumber]:
        documents = await self.collection.find({"account_id": account_id}).sort("since", 1).to_list(None)
        return [WhatsAppNumber.from_document(d) for d in documents]


class MongoWhatsAppBusinessAccountRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[WABAS]

    async def get(self, company_id: StrObjectId, waba_id: str) -> Optional[WhatsAppBusinessAccount]:
        document = await self.collection.find_one({"company_id": company_id, "waba_id": waba_id})
        return WhatsAppBusinessAccount.from_document(document) if document else None

    async def upsert(self, waba: WhatsAppBusinessAccount) -> WhatsAppBusinessAccount:
        document = waba.to_document()
        document.pop("_id")
        created_at = document.pop("created_at")
        stored = await _upsert(self.collection, {"company_id": waba.company_id, "waba_id": waba.waba_id}, document, created_at, waba.id)
        return WhatsAppBusinessAccount.from_document(stored)

    async def list_by_company(self, company_id: StrObjectId) -> List[WhatsAppBusinessAccount]:
        documents = await self.collection.find({"company_id": company_id}).to_list(None)
        return [WhatsAppBusinessAccount.from_document(d) for d in documents]


class MongoWhatsAppPortfolioRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[PORTFOLIOS]

    async def get(self, company_id: StrObjectId, portfolio_id: str) -> Optional[WhatsAppPortfolio]:
        document = await self.collection.find_one({"company_id": company_id, "portfolio_id": portfolio_id})
        return WhatsAppPortfolio.from_document(document) if document else None

    async def upsert(self, portfolio: WhatsAppPortfolio) -> WhatsAppPortfolio:
        document = portfolio.to_document()
        document.pop("_id")
        created_at = document.pop("created_at")
        stored = await _upsert(
            self.collection, {"company_id": portfolio.company_id, "portfolio_id": portfolio.portfolio_id}, document, created_at, portfolio.id
        )
        return WhatsAppPortfolio.from_document(stored)

    async def list_by_company(self, company_id: StrObjectId) -> List[WhatsAppPortfolio]:
        documents = await self.collection.find({"company_id": company_id}).to_list(None)
        return [WhatsAppPortfolio.from_document(d) for d in documents]


async def _upsert(collection, key: Dict[str, Any], fields: Dict[str, Any], created_at, new_id: str) -> Dict[str, Any]:
    """Upsert by a unique key; a concurrent upsert that loses the race re-reads the winner."""
    update = {"$set": {**fields, "updated_at": utc_now()}, "$setOnInsert": {"_id": ObjectId(new_id), "created_at": created_at}}
    try:
        return await collection.find_one_and_update(key, update, upsert=True, return_document=ReturnDocument.AFTER)
    except DuplicateKeyError:
        return await collection.find_one_and_update(key, {"$set": update["$set"]}, return_document=ReturnDocument.AFTER)
