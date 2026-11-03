"""`ChainOfThoughtRepository` on the standalone `chain_of_thoughts` collection: one `find_one` by `_id`.

Not a simple catalog (ADR-010): only a read by id, not async, no previews, no cache, no writes.

ENG-126, kept as in `main` (`ChainOfThoughts.get_by_id` over `mongo_mgr`): `collection` is Motor's, whose `find_one`
hands back a Future that nobody awaits. So the read is sent, `doc` is never a document, and building the chain raises
`TypeError` («… argument after ** must be a mapping, not _asyncio.Future»), whether the chain exists or not.
"""
from __future__ import annotations

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ...models.company.assets.ai_agents_v2.chain_of_thought_in_chat import ChainOfThoughtInChat
from ...models.utils.custom_exceptions import NotFoundError
from ...models.utils.types import StrObjectId


class MongoChainOfThoughtRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    def get(self, chain_of_thought_id: StrObjectId) -> ChainOfThoughtInChat:
        doc = self.collection.find_one({"_id": ObjectId(chain_of_thought_id)})  # not awaited: ENG-126
        if not doc:
            raise NotFoundError(f"Chain of thought {chain_of_thought_id} not found")
        return ChainOfThoughtInChat(**doc)
