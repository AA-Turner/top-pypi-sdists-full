from datetime import datetime
from pydantic import Field, BaseModel
from letschatty.models.base_models.ai_agent_component import AiAgentComponent

class ContextItem(AiAgentComponent):
    """Individual context item with title and content"""
    content: str = Field(..., description="The content of the context item")
    is_essential: bool = Field(default=False, description="Whether the example is essential for the ai agent to work")

