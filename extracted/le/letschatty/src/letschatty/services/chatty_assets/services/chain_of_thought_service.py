"""Chain Of Thought Service - Pre-configured AssetService for CRUD operations only"""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Optional
from ..asset_service import AssetService, CacheConfig
from ..collections.chain_of_thought_collection import ChainOfThoughtCollection
from ....models.company.assets.ai_agents_v2.chain_of_thought_in_chat import ChainOfThoughtInChat
from ....models.data_base.mongo_connection import MongoConnection
from ....models.utils.types.identifier import StrObjectId
from ....models.utils.types.serializer_type import SerializerType
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class ChainOfThoughtService(AssetService[ChainOfThoughtInChat, ChainOfThoughtInChat]):
    """
    Pre-configured service for Chain Of Thought CRUD operations.

    For business logic operations (create for N8N, set as failed, etc.),
    use ChainOfThoughtsEditor instead.

    No events needed - this is execution state, not a business asset.
    """

    def __init__(
        self,
        connection: MongoConnection,
        cache_config: CacheConfig = CacheConfig()
    ):
        collection = ChainOfThoughtCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

    collection: ChainOfThoughtCollection  # Type annotation for better type checking

    async def get_by_chat_id(self, chat_id: StrObjectId, skip: int = 0, limit: int = 10) -> List[ChainOfThoughtInChat]:
        """Get chain of thoughts by chat ID, sorted by created_at (newest first)"""
        return await self.collection.get_by_chat_id(chat_id=chat_id, skip=skip, limit=limit)

    async def get_by_id(self, cot_id: StrObjectId) -> Optional[ChainOfThoughtInChat]:
        """Get chain of thought by ID"""
        return await self.collection.get_by_id(cot_id)

    async def create(self, cot: ChainOfThoughtInChat) -> ChainOfThoughtInChat:
        """Create new chain of thought"""
        cot_dict = cot.model_dump(by_alias=True, exclude_none=False)
        result = await self.collection.collection.insert_one(cot_dict)
        if not result.inserted_id:
            raise Exception(f"Failed to create chain of thought {cot.id}")
        return cot

    async def update(self, cot: ChainOfThoughtInChat) -> ChainOfThoughtInChat:
        """Update chain of thought"""
        cot.updated_at = datetime.now(ZoneInfo("UTC"))
        cot_dict = cot.model_dump(by_alias=True, exclude_none=False)
        result = await self.collection.collection.update_one(
            {"_id": cot.id},
            {"$set": cot_dict}
        )
        if result.matched_count == 0:
            raise ValueError(f"Chain of thought {cot.id} not found")
        return cot
