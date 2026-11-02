"""AI Agent Service - Pre-configured AssetService for AI Agents"""

from ..asset_service import AssetService, CacheConfig
from ..collections import AiAgentCollection
from ....models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent, ChattyAIAgentPreview
from ....models.data_base.mongo_connection import MongoConnection


class AiAgentService(AssetService[ChattyAIAgent, ChattyAIAgentPreview]):
    """Pre-configured service for AI Agent assets with sensible defaults"""

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = AiAgentCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

