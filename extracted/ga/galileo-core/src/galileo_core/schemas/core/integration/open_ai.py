from typing import Literal, Optional

from pydantic import BaseModel

from galileo_core.schemas.core.integration.integration_type import LLMIntegration


class OpenAIExtras(BaseModel):
    organization_id: Optional[str] = None


class OpenAIIntegrationCreate(OpenAIExtras):
    name: Literal[LLMIntegration.openai] = LLMIntegration.openai
    token: str
