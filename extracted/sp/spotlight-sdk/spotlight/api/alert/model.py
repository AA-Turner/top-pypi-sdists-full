from datetime import datetime
from typing import Optional, Set, Union

from pydantic import Field, validator

from spotlight.api.data.model import WhereClause
from spotlight.core.common.base import Base
from spotlight.core.common.enum import IntervalType, NotificationType


class AlertRequest(Base):
    display_name: str
    description: Optional[str] = Field(default=None)
    dataset_id: str
    where_clause: Optional[Union[WhereClause, dict]] = Field(default=None)
    interval_type: IntervalType
    interval: int
    interval_start: datetime
    notification_type: NotificationType
    notification_source: Set[str]

    @validator("interval")
    def _validate_interval(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("interval must be greater than 0")
        return value


class AlertResponse(Base):
    id: str
    display_name: str
    description: Optional[str] = Field(default=None)
    dataset_id: str
    where_clause: Optional[Union[WhereClause, dict]] = Field(default=None)
    interval_type: IntervalType
    interval: int
    interval_start: datetime
    notification_type: NotificationType
    notification_source: Set[str]


class AlertSignal(Base):
    alert_id: str
    alert_name: str
    alert_description: Optional[str] = Field(default=None)
    notification_type: NotificationType
    notification_source: Set[str]
    interval_type: IntervalType
    interval: int
    interval_start_time: datetime
    window_start_time: datetime
    window_end_time: datetime
    where_clause: WhereClause
    dataset_id: str
