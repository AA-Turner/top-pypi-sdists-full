from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta

from utils.types import ChannelId, StrObjectId, MessageStatus, PhoneNumber, Country

##Unfinished

class SalesRoadmapMetric(BaseModel):
    """This metric shows the complete roadmap a chat followed from the first contact point to the closing of the sale, including templates"""
    chat_id: StrObjectId = Field(description="Id of the chat")
    phone_number: PhoneNumber = Field(description="Phone number of the user that originated the chat")
    date: datetime = Field(description="Date and time when the chat was created")
    source_id: StrObjectId = Field(description="Id of the source that originated the chat")
    source_name: str = Field(description="Name of the source that originated the chat")
    country: Country = Field(description="Country of the user that originated the chat")