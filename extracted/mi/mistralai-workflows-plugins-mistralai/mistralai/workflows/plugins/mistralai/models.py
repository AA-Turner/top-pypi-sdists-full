from typing import List

from pydantic import BaseModel, Field

from mistralai.client import models as mistralai_models


class ContentChunk(BaseModel):
    type: str = "text"
    text: str


class ChatStreamState(BaseModel):
    contentChunks: List[ContentChunk] = Field(default_factory=list)


class ConversationStreamState(BaseModel):
    contentChunks: List[ContentChunk] = Field(default_factory=list)


class ConversationAppendRequest(mistralai_models.ConversationAppendRequest):
    conversation_id: str


class AgentUpdateRequest(mistralai_models.UpdateAgentRequest):
    agent_id: str
