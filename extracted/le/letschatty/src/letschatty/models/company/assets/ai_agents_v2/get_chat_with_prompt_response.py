from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from letschatty.models.chat.chat import Chat
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode
import logging

logger = logging.getLogger("AiAgentContextService")

class GetChatWithPromptResponse(BaseModel):
    mode: ChattyAIMode
    context: str
    messages: str
    chatty_ai_agent: Optional[ChattyAIAgent] = Field(default=None)
    chat: Optional[Chat] = Field(default=None)


    def to_dict(self) -> Dict[str, Any]:
        logger.debug(f"Chatty AI agent: {self.chatty_ai_agent}")
        output = {
            "mode": self.mode.value,
            "context": self.context,
            "messages": self.messages,
            "n8n_agent_type": self.chatty_ai_agent.n8n_workspace_agent_type.value if self.chatty_ai_agent else None,
            "n8n_agent_type_parameters": self.chatty_ai_agent.n8n_workspace_agent_type_parameteres.model_dump() if self.chatty_ai_agent else None,
            "phone_number": self.chat.client.get_waid() if self.chat else None
        }
        return output

