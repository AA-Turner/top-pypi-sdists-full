"""AI Agent Collection - Pre-configured AssetCollection for AI Agents"""

from ..asset_service import AssetCollection
from ....models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent, ChattyAIAgentPreview
from ....models.data_base.mongo_connection import MongoConnection


class AiAgentCollection(AssetCollection[ChattyAIAgent, ChattyAIAgentPreview]):
    """Pre-configured collection for AI Agent assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="ai_agents",
            asset_type=ChattyAIAgent,
            connection=connection,
            create_instance_method=ChattyAIAgent.default_create_instance_method,
            preview_type=ChattyAIAgentPreview
        )

