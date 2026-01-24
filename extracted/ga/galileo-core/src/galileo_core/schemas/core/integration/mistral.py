from typing import Literal

from pydantic import BaseModel

from galileo_core.schemas.core.integration.integration_type import LLMIntegration


class MistralIntegrationCreate(BaseModel):
    name: Literal[LLMIntegration.mistral] = LLMIntegration.mistral
    token: str
