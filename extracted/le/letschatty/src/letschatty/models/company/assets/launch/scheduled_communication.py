from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft
from letschatty.models.company.assets.ai_agents_v2.ai_agent_message_draft import AIAgentMessageDraft


class LaunchScheduledCommunication(BaseModel):
    """
    Scheduled communication for pre/post launch.
    Can be AI-adapted or literal messages.
    """
    id: str = Field(description="Unique identifier for the communication")
    name: str = Field(description="Name of the communication (e.g., '5 dias antes', '2 horas antes')")
    delta_minutes: int = Field(
        description="Minutes relative to the launch (negative=before, positive=after, 0=welcome kit)"
    )

    # Content - one or the other
    ai_communication: Optional[AIAgentMessageDraft] = Field(
        default=None,
        description="AI adapted communication content and instructions"
    )
    literal_messages: Optional[List[MessageDraft]] = Field(
        default=None,
        description="Literal messages to be sent without AI adaptation"
    )

    # State
    sent_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when this communication was sent globally for the launch"
    )

    @property
    def requires_ai(self) -> bool:
        """Check if this communication requires AI adaptation"""
        return self.ai_communication is not None

    @property
    def is_sent(self) -> bool:
        """Check if this communication has been sent"""
        return self.sent_at is not None

