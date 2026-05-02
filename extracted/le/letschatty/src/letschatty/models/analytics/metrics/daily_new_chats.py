from pydantic import BaseModel
from datetime import date
from utils.types import Country, ChannelId

class DailyNewChatsMetric(BaseModel):
    """This metric represents the number of new chats in a given day"""
    date: date
    country: Country
    channel_id: ChannelId
    inbound: int
    outbound: int
    total: int