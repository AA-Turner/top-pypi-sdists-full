from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from ....utils.types.identifier import StrObjectId
from .....models.utils.definitions import Area
from ....chat.quality_scoring import QualityScore
class FunnelStageContext(BaseModel):
    funnel_stage_id: StrObjectId
    funnel_id: StrObjectId
    time_in_funnel_stage_seconds: int

class ChatContext(BaseModel):
    # Core identifiers
    chat_id: StrObjectId
    company_id: StrObjectId
    is_read: bool
    is_starred: bool

    # Core context elements
    active_funnel_stages: List[FunnelStageContext] = Field(default_factory=list)
    previous_funnel_stages: List[FunnelStageContext] = Field(default_factory=list)
    products_of_interest: List[StrObjectId] = Field(default_factory=list)
    purchased_products: List[StrObjectId] = Field(default_factory=list)
    sales_count: int = 0
    sales_amount_by_currency: Dict[str, float] = Field(default_factory=dict, description="A dictionary of currency code and the amount of money spent on them")
    active_tags: List[StrObjectId] = Field(default_factory=list)
    all_sources: List[StrObjectId] = Field(default_factory=list)

    # Assignment information
    agent_id: Optional[StrObjectId] = None
    area: Optional[Area] = None

    # Conversation metrics
    incoming_messages_count: int = 0
    outgoing_messages_count: int = 0

    # Activity metrics
    fast_answers_sent: List[StrObjectId] = Field(default_factory=list)
    templates_sent: List[str] = Field(default_factory=list)
    executed_workflows: List[StrObjectId] = Field(default_factory=list)
    active_workflows: List[StrObjectId] = Field(default_factory=list)

    # Quality metrics
    quality_score: Optional[QualityScore] = None
    time_since_last_incoming_message_seconds: Optional[int] = None
    time_since_last_outgoing_message_seconds: Optional[int] = None
    time_to_qualify_seconds: Optional[int] = None
    time_to_first_sale_seconds: Optional[int] = None
    time_since_last_sale_seconds: Optional[int] = None
    average_user_response_time_seconds: Optional[int] = None
    average_company_response_time_seconds: Optional[int] = None
    # Timestamps
    created_at: datetime
