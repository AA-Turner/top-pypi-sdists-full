from pydantic import BaseModel, Field
from datetime import date, timedelta

from utils.types import ChannelId

class DailySentTemplatesGroupedMetric(BaseModel):
    """This metric represents the number of templates sent (and its current status) in a given day grouped by template name and campaign name"""
    date: date
    channel_id: ChannelId
    template_name: str = Field(description="Name of the template that was sent")
    campaign_name: str = Field(default="Individual", description="Name of the template campaign that sent the template")
    failed: int = Field(default=0, description="Templates that failed to be sent")
    sent: int = Field(default=0, description="Templates that were sent to the user, but couldn't be delivered")
    delivered: int = Field(default=0, description="Templates that were delivered to the user, but not read")
    read: int = Field(default=0, description="Templates that were read by the user, but not answered")
    answered: int = Field(default=0, description="Templates answered by the user in a 48hs window")
    lost: int = Field(default=0, description="Templates which request were succesfull but no state update was received from META")
    saved_by_chatty: int = Field(default=0, description="Templates that Chatty avoided to send as templates because the conversation was open so were send as messages")
    time_to_answer: timedelta = Field(default=timedelta(), description="Average time to answer")
    sales_count: int = Field(default=0, description="Number of sales that were closed after the template was sent")

