from pydantic import BaseModel, Field
from letschatty.models import StrObjectId
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent import N8NWorkspaceAgentType

class SmartFollowUpN8NPayload(BaseModel):
    action: str = Field(default="follow_up")
    chat_id: StrObjectId = Field(description="The id of the chat")
    company_id: StrObjectId = Field(description="The id of the company")

class ManualTriggerN8NPayload(BaseModel):
    chat_id: StrObjectId = Field(description="The id of the chat")
    company_id: StrObjectId = Field(description="The id of the company")
    n8n_agent_type: N8NWorkspaceAgentType = Field(description="The type of agent to redirect the message to")