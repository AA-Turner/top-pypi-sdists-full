from pydantic import BaseModel, Field
from letschatty.models.utils.types.identifier import StrObjectId
from .chatty_ai_mode import ChattyAIMode

class ChattyAIConfigForAutomation(BaseModel):
    mode: ChattyAIMode
    agent_id: StrObjectId
    only_for_new_chats: bool = Field(default=False)

class ChattyAICofnigForChatRequest(BaseModel):
    mode: ChattyAIMode
    agent_id: StrObjectId