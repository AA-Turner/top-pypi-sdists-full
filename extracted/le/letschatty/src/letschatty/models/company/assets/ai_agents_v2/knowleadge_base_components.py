from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo
from datetime import datetime
from letschatty.models.base_models.ai_agent_component import AiAgentComponentType
from letschatty.models.utils.types.identifier import StrObjectId

class KnowleadgeBaseComponent(BaseModel):
    """Knowleadge base component"""
    name: str = Field(description="The name of the component")
    type: AiAgentComponentType = Field(description="The type of the component")
    timestamp: datetime = Field(description="The timestamp of usage of the component", default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    id : StrObjectId = Field(description="The id of the component")