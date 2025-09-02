from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta

from utils.types import ChannelId, StrObjectId, MessageStatus, PhoneNumber

class SentTemplatesMetric(BaseModel):
    """This metric shows the complete lifecycle of a template that was sent to a user"""
    date: datetime
    channel_id: ChannelId
    chat_id: StrObjectId = Field(description="Chat id of the chat that received the template")
    phone_number: PhoneNumber = Field(description="Phone number of the user that received the template")
    template_status: MessageStatus = Field(description="Status of the template that was sent")
    message_id: str = Field(description="Id of the message in which the template that was sent")
    template_name: str = Field(description="Name of the template that was sent")
    campaign_name: str = Field(default="Individual", description="Name of the template campaign that sent the template")
    answered: bool = Field(default=False, description="Whether the template was answered")
    answered_message: str = Field(default="", description="The message that was sent in response to the template")
    answered_at_date: datetime | None = Field(default=None, description="Date and time when the answered message was sent")
    time_to_answer: timedelta | None = Field(default=None, description="Time elapsed between the template being sent and the answered message being sent")