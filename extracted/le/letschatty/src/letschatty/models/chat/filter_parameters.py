from letschatty.models.utils.types import StrObjectId
from letschatty.models.execution.execution import ExecutionContext
from pydantic import BaseModel, Field
from letschatty.models.utils.definitions import Area
from letschatty.models.chat.quality_scoring import QualityScore
from datetime import datetime, timedelta
import logging
from typing import Optional
logger = logging.getLogger("FilterParameters")

class FilterParameters(BaseModel):
    area_status: list[Area] = Field(default=[])
    previews_per_page: int = Field(default=10, ge=1)
    order_desc: int = Field(default=1, ge=0, le=1)
    page_number: int = Field(default=1, ge=1)
    unread: int = Field(default=0, ge=0, le=1)
    starred: int = Field(default=0, ge=0, le=1)
    time_left_order: int = Field(default=0, ge=0, le=1)
    products: list[StrObjectId] = Field(default=[])
    sales_products: list[StrObjectId] = Field(default=[])
    tags: list[StrObjectId] = Field(default=[])
    search_like: str = Field(default="")
    agents: list[StrObjectId] = Field(default=[])
    business_areas: list[StrObjectId] = Field(default=[])
    funnels: list[StrObjectId] = Field(default=[])
    funnel_stages: list[StrObjectId] = Field(default=[])
    time_since_last_message_hours: int = Field(default=0, ge=0)
    sources: list[StrObjectId] = Field(default=[])
    quality_score: list[QualityScore] = Field(default=[])
    messages_count: int = Field(default=0, ge=0)
    search_in_chat: str = Field(default="")
    workflows: list[StrObjectId] = Field(default=[])
    last_message_date_range: Optional[tuple[datetime, datetime]] = Field(default=None)
    sales_date_range: Optional[tuple[datetime, datetime]] = Field(default=None)
    sources_date_range: Optional[tuple[datetime, datetime]] = Field(default=None)
    sent_templates : list[str] = Field(default=[])
    executor_user_id: StrObjectId

    @property
    def is_my_chats(self) -> bool:
        return len(self.agents) == 1 and self.agents[0] == self.executor_user_id and len(self.area_status) == 0

    @property
    def is_direct(self) -> bool:
        if not self.search_in_chat and not self.search_like and not self.sent_templates and not self.products and not self.sales_products and not self.tags and not self.business_areas and not self.funnels and not self.funnel_stages and not self.time_since_last_message_hours and not self.sources and not self.quality_score and not self.messages_count and not self.workflows and not self.last_message_date_range and not self.sales_date_range and not self.sources_date_range and len(self.area_status) <= 1 and (len(self.agents) <= 1 or self.is_my_chats):
            return True
        return False

    @classmethod
    def from_query_params(cls, query_params: dict, execution_context: ExecutionContext) -> "FilterParameters":
        logger.debug(f"Query params: {query_params}")
        processed_params = {}
        processed_params["executor_user_id"] = execution_context.executor.id

        # Handle all list fields
        list_fields = {
            "products": StrObjectId,
            "sales_products": StrObjectId,
            "tags": StrObjectId,
            "agents": StrObjectId,
            "business_areas": StrObjectId,
            "funnels": StrObjectId,
            "funnel_stages": StrObjectId,
            "area_status": Area,
            "sources": StrObjectId,
            "quality_score": QualityScore,
            "workflows": StrObjectId,
            "sent_templates": str
        }

        for field_name, field_type in list_fields.items():
            value = query_params.get(field_name)
            if not value:
                processed_params[field_name] = []
            elif "," in value:
                processed_params[field_name] = [field_type(item) for item in value.split(",")]
            else:
                processed_params[field_name] = [field_type(value)]

        # Process all other fields from query params
        for key, value in query_params.items():
            if key not in list_fields and value:  # Only process if value is not empty
                processed_params[key] = value
        logger.debug(f"Processed params: {processed_params}")
        return cls(**processed_params)