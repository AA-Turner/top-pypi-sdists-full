from datetime import datetime
from typing import Optional, List

from pydantic import Field

from spotlight.api.data.model import WhereClause
from spotlight.core.common.base import Base
from spotlight.core.common.enum import IntervalType, NotificationType


class AlertRequest(Base):
    display_name: str
    description: Optional[str] = Field(default=None)
    data_rule_id: str
    interval_type: IntervalType
    interval: int
    interval_start: Optional[datetime] = Field(default=None)
    notification_type: NotificationType
    notification_source: List[str]


class AlertResponse(Base):
    id: str
    display_name: str
    description: Optional[str]
    data_rule_id: str
    interval_type: IntervalType
    interval: int
    interval_start: Optional[datetime]
    notification_type: NotificationType
    notification_source: List[str]
    created_by: str
    created_at: datetime
    updated_by: Optional[str]
    updated_at: Optional[int]


class AlertSignal(Base):
    alert_id: str
    alert_name: str
    alert_description: Optional[str]
    notification_type: NotificationType
    notification_source: List[str]
    interval_type: IntervalType
    interval: int
    interval_start_time: datetime
    window_start_time: datetime
    window_end_time: datetime
    where_clause: WhereClause
    dataset_id: str
