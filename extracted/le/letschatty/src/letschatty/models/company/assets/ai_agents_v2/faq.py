from typing import Any, ClassVar
from pydantic import Field
from letschatty.models.base_models.ai_agent_component import AiAgentComponent

class FAQ(AiAgentComponent):
    """FAQ item with question and answer"""
    question: str = Field(..., description="The question")
    answer: str = Field(..., description="The answer to the question")
    is_essential: bool = Field(default=False, description="Whether the faq is essential for the ai agent to work")
