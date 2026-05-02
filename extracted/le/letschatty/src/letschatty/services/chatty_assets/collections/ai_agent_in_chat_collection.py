"""AI Agent In Chat Collection - Pre-configured AssetCollection for AI Agent state in chats"""

from ..asset_service import AssetCollection
from ....models.company.assets.ai_agents_v2.chatty_ai_agent_in_chat import ChattyAIAgentInChat
from ....models.data_base.mongo_connection import MongoConnection
from typing import Optional


class AIAgentInChatCollection(AssetCollection[ChattyAIAgentInChat, ChattyAIAgentInChat]):
    """
    Pre-configured collection for AI Agent In Chat state.

    This is a standalone collection (not embedded in Chat) that allows Lambda to
    manage AI agent state independently without loading entire chat documents.
    """

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="chatty_ai_agents_in_chat",
            asset_type=ChattyAIAgentInChat,
            connection=connection,
            create_instance_method=lambda doc: ChattyAIAgentInChat(**doc),
            preview_type=ChattyAIAgentInChat  # No separate preview type needed
        )

    async def get_by_chat_id(self, chat_id: str) -> Optional[ChattyAIAgentInChat]:
        """Get AI agent state by chat ID, or None if not found"""
        doc = await self.collection.find_one({"chat_id": chat_id, "deleted_at": None})
        if not doc:
            return None
        return self.create_instance(doc)

