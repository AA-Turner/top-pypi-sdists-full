from pydantic import BaseModel, Field

class AgentChatsSnapshot(BaseModel):
    agent_unread_chats: int = Field(description="Number of chats unread and assigned to the agent")
    agent_active_chats_4h: int = Field(description="Number of chats agent is handling that have been active in the last 4 hours")
    agent_active_chats_8h: int = Field(description="Number of chats agent is handling that have been active in the last 8 hours")
    agent_active_chats_24h: int = Field(description="Number of chats agent is handling that have been active in the last 24 hours")
