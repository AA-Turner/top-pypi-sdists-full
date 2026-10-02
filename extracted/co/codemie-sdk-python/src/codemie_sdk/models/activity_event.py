"""Models for activity event data structures."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ActivityEventListItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    domain: str
    event_type: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    actor_id: Optional[str] = None
    actor_email: Optional[str] = None
    actor_name: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    created_at: datetime


class ActivityEventPagination(BaseModel):
    model_config = ConfigDict(extra="ignore")

    total: int
    page: int = 0
    per_page: int
    pages: int = 1


class PaginatedActivityEventResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    data: List[ActivityEventListItem]
    pagination: ActivityEventPagination


class ActivityEventFilterOptions(BaseModel):
    model_config = ConfigDict(extra="ignore")

    domains: List[str]
    event_types: List[str]
    entity_types: List[str]
