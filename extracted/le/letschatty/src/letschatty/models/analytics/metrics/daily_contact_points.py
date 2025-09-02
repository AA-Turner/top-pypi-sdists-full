from pydantic import BaseModel, Field
from datetime import date
from utils.types import ChannelId, StrObjectId, Country, SourceType

class DailyContactPointsMetric(BaseModel):
    """This metric represents the number of of contact points (message originated from a source) in a given day and its quality"""
    date: date
    channel_id: ChannelId
    country: Country
    source_id: StrObjectId
    source_name: str
    source_category: str
    source_type: SourceType
    ad_id: str = Field(default="", description="Meta ad id, only available for Meta ads")
    cp_new_chats_count: int = Field(default=0, description="Number of new chats originated from this source")
    cp_existing_chats_count: int = Field(default=0, description="Number of existing chats that received a message originated from this source")
    cp_total_count: int = Field(default=0, description="Total number of contact points originated from this source")
    good_quality_count : int = Field(default=0, description="Number of chats with good quality that received a message originated from this source")
    neutral_quality_count : int = Field(default=0, description="Number of chats with neutral quality that received a message originated from this source")
    bad_quality_count : int = Field(default=0, description="Number of chats with bad quality that received a message originated from this source")
    sales_count : int = Field(default=0, description="Number of chats that closed a sale that received a message originated from this source")