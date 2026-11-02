from pydantic import Field

from letschatty.models.base_models.ai_agent_component import AiAgentComponent, AiAgentComponentPreview
from typing import ClassVar


class AiSpecificInstruction(AiAgentComponent):
    """Specific instruction for the AI agent to follow"""

    content: str = Field(..., description="The instruction content for the AI agent")
    is_essential: bool = Field(
        default=True,
        description="Whether this instruction is essential for the AI agent to work",
    )

    preview_class: ClassVar[type[AiAgentComponentPreview]] = AiAgentComponentPreview