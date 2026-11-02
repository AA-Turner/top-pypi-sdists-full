from enum import StrEnum
from pydantic import field_validator, ValidationInfo, Field
from ....utils.types.identifier import StrObjectId
from typing import Optional, ClassVar
from ....utils.types.executor_types import ExecutorType
from ..base import Event, EventType, EventData
import json



class UserStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"

class UserEventData(EventData):
    user_id: StrObjectId
    company_id: StrObjectId
    new_status: Optional[UserStatus] = Field(default=None)
    business_area_id: Optional[StrObjectId] = Field(default=None)
    funnel_id:Optional[StrObjectId] = Field(default=None)
    executor_type: ExecutorType
    executor_id: StrObjectId

    @property
    def message_group_id(self) -> str:
        return f"user-{self.user_id}"

class UserEvent(Event):
    data: UserEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.USER_LOGGED_IN,
        EventType.USER_CREATED,
        EventType.USER_UPDATED,
        EventType.USER_DELETED,
        EventType.USER_LOGGED_OUT,
        EventType.USER_STATUS_UPDATED,
        EventType.USER_ASSIGNED_AREA,
        EventType.USER_UNASSIGNED_AREA,
        EventType.USER_ASSIGNED_FUNNEL,
        EventType.USER_UNASSIGNED_FUNNEL
    }

    @field_validator('data')
    def validate_data_fields(cls, v: UserEventData, info: ValidationInfo):
        if info.data.get('type') == EventType.USER_STATUS_UPDATED and not v.new_status:
            raise ValueError("new_status must be set for USER_STATUS_UPDATED events")
        if info.data.get('type') == EventType.USER_ASSIGNED_AREA and not v.business_area_id:
            raise ValueError("business_area_id must be set for USER_ASSIGNED_AREA events")
        if info.data.get('type') == EventType.USER_UNASSIGNED_AREA and not v.business_area_id:
            raise ValueError("business_area_id must be set for USER_UNASSIGNED_AREA events")
        if info.data.get('type') == EventType.USER_ASSIGNED_FUNNEL and not v.funnel_id:
            raise ValueError("funnel_id must be set for USER_ASSIGNED_FUNNEL events")
        if info.data.get('type') == EventType.USER_UNASSIGNED_FUNNEL and not v.funnel_id:
            raise ValueError("funnel_id must be set for USER_UNASSIGNED_FUNNEL events")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump