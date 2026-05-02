from pydantic import BaseModel, Field

class CompanyChatsSnapshot(BaseModel):
    company_unread_chats: int = Field(description="Company queue size waiting for agent and unread")
    company_active_chats_4h: int = Field(description="Number of chats agent is handling that have been active in the last 4 hours")
    company_active_chats_8h: int = Field(description="Number of chats agent is handling that have been active in the last 8 hours")
    company_active_chats_24h: int = Field(description="Number of chats agent is handling that have been active in the last 24 hours")
    company_online_agents: int = Field(description="Total available agents at the moment")
