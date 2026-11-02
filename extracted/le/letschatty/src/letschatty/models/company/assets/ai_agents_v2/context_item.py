from datetime import datetime
from pydantic import Field, BaseModel
from letschatty.models.base_models.ai_agent_component import AiAgentComponent
from letschatty.models.company.assets.embeddable import build_chunks

class ContextItem(AiAgentComponent):
    """Individual context item with title and content"""
    content: str = Field(..., description="The content of the context item")
    is_essential: bool = Field(default=False, description="Whether the example is essential for the ai agent to work")

    def embedding_chunks(self) -> list[dict[str, str]]:
        return build_chunks("context", {"name": self.name, "content": self.content})

