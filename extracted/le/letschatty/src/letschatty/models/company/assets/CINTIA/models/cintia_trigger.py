from pydantic import BaseModel, Field
from enum import StrEnum

from letschatty.models.analytics.events.chat_based_events.message import MessageEvent
from .....utils.types.identifier import StrObjectId
from typing import Any, Literal
from datetime import datetime
from zoneinfo import ZoneInfo

class CintiaTriggerType(StrEnum):
    USER_MESSAGE = "user_message"
    SMART_FOLLOW_UP = "smart_follow_up"
    MANUAL_TRIGGER = "manual_trigger"

class CintiaTrigger(BaseModel):
    type: CintiaTriggerType = Field(description="The type of the trigger")
    data: Any = Field(description="The data of the trigger")

class IncomingMessageTrigger(BaseModel):
    type : Literal[CintiaTriggerType.USER_MESSAGE] = CintiaTriggerType.USER_MESSAGE
    data: MessageEvent = Field(description="The message event that triggered the cintia execution")


class FollowUpTriggerData(BaseModel):
    chat_id: StrObjectId

class FollowUpTrigger(BaseModel):
    type : Literal[CintiaTriggerType.SMART_FOLLOW_UP] = CintiaTriggerType.SMART_FOLLOW_UP
    data : FollowUpTriggerData = Field(description="The smart follow up data that triggered the cintia execution")

class ManualTriggerEventData(BaseModel):
    chat_id: StrObjectId
    triggered_by_user_id: StrObjectId
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")), description="The timestamp of the manual trigger")

class ManualTrigger(BaseModel):
    type : Literal[CintiaTriggerType.MANUAL_TRIGGER] = CintiaTriggerType.MANUAL_TRIGGER
    data : ManualTriggerEventData = Field(description="The manual trigger event that triggered the cintia execution")