from typing import Literal

from pydantic import BaseModel

from galileo_core.schemas.core.integration.integration_type import LLMIntegration


class AnthropicIntegrationCreate(BaseModel):
    name: Literal[LLMIntegration.anthropic] = LLMIntegration.anthropic
    token: str
