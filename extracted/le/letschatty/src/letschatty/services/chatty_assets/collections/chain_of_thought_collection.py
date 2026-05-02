"""Chain of Thought Collection - Pre-configured AssetCollection for Chain of Thoughts"""

from typing import Any, List, Dict

from letschatty.models.utils.types.serializer_type import SerializerType
from ..asset_service import AssetCollection, StrObjectId
from ....models.company.assets.ai_agents_v2.chain_of_thought_in_chat import (
    ChainOfThoughtInChat,
    ChainOfThoughtInChatPreview
)
from ....models.data_base.mongo_connection import MongoConnection


class ChainOfThoughtCollection(AssetCollection[ChainOfThoughtInChat, ChainOfThoughtInChatPreview]):
    """Pre-configured collection for Chain of Thought"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="chain_of_thoughts",
            asset_type=ChainOfThoughtInChat,
            connection=connection,
            create_instance_method=lambda doc: ChainOfThoughtInChat(**doc),
            preview_type=ChainOfThoughtInChatPreview
        )

    async def get_by_chat_id(self, chat_id: StrObjectId, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get chain of thoughts by chat ID, sorted by created_at (newest first)"""
        cursor = self.collection.find({"chat_id": chat_id, "deleted_at": None}).sort("created_at", -1).skip(skip).limit(limit)
        cot_docs = await cursor.to_list(length=None)
        return [self.create_instance(cot_doc).model_dump_json(serializer=SerializerType.FRONTEND) for cot_doc in cot_docs]
