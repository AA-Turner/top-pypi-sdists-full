"""AI Component Collection - Pre-configured AssetCollection for AI Components"""

from typing import Any
from ..asset_service import AssetCollection
from ....models.base_models.ai_agent_component import AiAgentComponent, AiAgentComponentPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.ai_components_service import AiComponentsService


class AiComponentCollection(AssetCollection[AiAgentComponent, AiAgentComponentPreview]):
    """Pre-configured collection for AI Component assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="ai_components",
            asset_type=AiAgentComponent,
            connection=connection,
            create_instance_method=AiComponentsService.instantiate_component,
            preview_type=AiAgentComponentPreview
        )

