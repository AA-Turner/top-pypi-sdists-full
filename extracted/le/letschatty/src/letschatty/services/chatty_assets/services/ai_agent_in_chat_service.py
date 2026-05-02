"""AI Agent In Chat Service - Pre-configured AssetService for CRUD operations only"""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from ..asset_service import AssetService, CacheConfig
from ..collections.ai_agent_in_chat_collection import AIAgentInChatCollection
from ....models.company.assets.ai_agents_v2.chatty_ai_agent_in_chat import ChattyAIAgentInChat
from ....models.data_base.mongo_connection import MongoConnection
from ....models.utils.types.identifier import StrObjectId
import logging

logger = logging.getLogger(__name__)


class AIAgentInChatService(AssetService[ChattyAIAgentInChat, ChattyAIAgentInChat]):
    """
    Pre-configured service for AI Agent In Chat CRUD operations.

    For business logic operations (set_to_processing, escalate, etc.),
    use AIAgentInChatEditor instead.

    No events needed - this is operational state, not a business asset.
    """

    def __init__(
        self,
        connection: MongoConnection,
        cache_config: CacheConfig = None,
    ):
        collection = AIAgentInChatCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

    collection: AIAgentInChatCollection  # Type annotation for better type checking

    async def get_by_chat_id(self, chat_id: StrObjectId) -> Optional[ChattyAIAgentInChat]:
        """Get AI agent state for a chat"""
        return await self.collection.get_by_chat_id(chat_id)

    async def update(self, ai_agent_in_chat: ChattyAIAgentInChat) -> ChattyAIAgentInChat:
        """Update AI agent state"""
        ai_agent_in_chat.updated_at = datetime.now(ZoneInfo("UTC"))
        ai_agent_dict = ai_agent_in_chat.model_dump(by_alias=True, exclude_none=False)
        # Remove _id field as it's immutable in MongoDB
        ai_agent_dict.pop('_id', None)
        result = await self.collection.collection.update_one(
            {"chat_id": ai_agent_in_chat.chat_id},
            {"$set": ai_agent_dict}
        )
        if result.matched_count == 0:
            raise ValueError(f"AI agent state for chat {ai_agent_in_chat.chat_id} not found")
        return ai_agent_in_chat

    async def create(self, ai_agent_in_chat: ChattyAIAgentInChat) -> ChattyAIAgentInChat:
        """Create new AI agent state"""
        ai_agent_dict = ai_agent_in_chat.model_dump(by_alias=True, exclude_none=False)
        result = await self.collection.collection.insert_one(ai_agent_dict)
        if not result.inserted_id:
            raise Exception(f"Failed to create AI agent state for chat {ai_agent_in_chat.chat_id}")
        return ai_agent_in_chat

    async def delete(self, chat_id: StrObjectId) -> None:
        """Delete AI agent state"""
        result = await self.collection.collection.delete_one({"chat_id": chat_id})
        if result.deleted_count == 0:
            raise ValueError(f"AI agent state for chat {chat_id} not found")

