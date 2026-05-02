from pydantic import Field
from letschatty.models.base_models.ai_agent_component import AiAgentComponent, AiAgentComponentPreview
from letschatty.models.company.assets.embeddable import build_chunks
from typing import ClassVar


class Instruction(AiAgentComponent):
    """A standalone instruction component for the AI agent to follow."""

    content: str = Field(..., description="The instruction content for the AI agent")
    is_essential: bool = Field(
        default=False,
        description="Whether this instruction is essential for the AI agent to work",
    )

    preview_class: ClassVar[type[AiAgentComponentPreview]] = AiAgentComponentPreview

    def embedding_chunks(self) -> list[dict[str, str]]:
        return build_chunks("instruction", {"name": self.name, "content": self.content})
