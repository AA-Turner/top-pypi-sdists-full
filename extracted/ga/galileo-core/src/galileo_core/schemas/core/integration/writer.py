from typing import Literal

from pydantic import BaseModel

from galileo_core.schemas.core.integration.integration_type import LLMIntegration


class WriterExtras(BaseModel):
    organization_id: str


class WriterIntegrationCreate(WriterExtras):
    name: Literal[LLMIntegration.writer] = LLMIntegration.writer
    token: str
