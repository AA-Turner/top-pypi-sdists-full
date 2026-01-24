from typing import Literal

from pydantic import BaseModel

from galileo_core.schemas.core.integration.integration_type import LLMIntegration


class VertexAIIntegrationCreate(BaseModel):
    name: Literal[LLMIntegration.vertex_ai] = LLMIntegration.vertex_ai
    token: str
