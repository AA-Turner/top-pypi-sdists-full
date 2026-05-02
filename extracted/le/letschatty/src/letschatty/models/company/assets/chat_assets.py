from pydantic import BaseModel, Field, field_validator
from enum import StrEnum

from pydantic_core.core_schema import str_schema

from letschatty.models.company.assets.ai_agents_v2.chain_of_thought_in_chat import ChainOfThoughtInChatTrigger
from ...utils.types.identifier import StrObjectId
from datetime import datetime
from zoneinfo import ZoneInfo
from bson import ObjectId
import json
from typing import Dict, Any, Optional
from letschatty.models.utils.types.serializer_type import SerializerType
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode

import logging
logger = logging.getLogger("AssignedAssetToChat")

class ChatAssetType(StrEnum):
    PRODUCT = "product"
    SALE = "sale"
    TAG = "tag"
    HIGHLIGHT = "highlight"
    CONTACT_POINT = "contact_point"
    CONTINUOUS_CONVERSATION = "continuous_conversation"
    BUSINESS_AREA = "business_area"
    FUNNEL = "funnel"
    WORKFLOW = "workflow"
    CHATTY_AI_AGENT = "chatty_ai_agent"


class DataCollectionStatus(StrEnum):
    COLLECTING = "collecting"
    MANDATORY_COMPLETED = "mandatory_completed"
    ALL_COMPLETED = "all_completed"
    CANCELLED = "cancelled"


class AssignedAssetToChat(BaseModel):
    id: StrObjectId = Field(frozen=True, default_factory=lambda: str(ObjectId()))
    asset_type: ChatAssetType = Field(frozen=True)
    asset_id: StrObjectId = Field(frozen=True)
    assigned_at: datetime = Field(frozen=True, default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    assigned_by: StrObjectId = Field(frozen=True)

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        serializer = kwargs.pop("serializer", SerializerType.API)
        kwargs.pop("mode", None)  # model_dump_json has no mode param
        dumped_json = super().model_dump_json(*args, **kwargs)
        loaded_json = json.loads(dumped_json)
        if serializer == SerializerType.DATABASE:
            loaded_json["assigned_at"] = self.assigned_at
        return loaded_json

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        serializer = kwargs.pop("serializer", SerializerType.API)
        kwargs.pop("mode", None)  # model_dump_json has no mode param
        dumped_json = super().model_dump_json(*args, **kwargs)
        loaded_json = json.loads(dumped_json)
        if serializer == SerializerType.DATABASE:
            loaded_json["assigned_at"] = self.assigned_at
        return loaded_json

    def __lt__(self, other: 'AssignedAssetToChat') -> bool:
        return self.assigned_at < other.assigned_at

    def __gt__(self, other: 'AssignedAssetToChat') -> bool:
        return self.assigned_at > other.assigned_at

    @field_validator('assigned_at', mode="after")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v is None:
            return v
        return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))


class SaleAssignedToChat(AssignedAssetToChat):
    product_id: StrObjectId = Field(frozen=True)

class ContactPointAssignedToChat(AssignedAssetToChat):
    source_id: StrObjectId = Field(frozen=True)

class ChattyAIAgentAssignedToChat(AssignedAssetToChat):
    mode: ChattyAIMode = Field(default=ChattyAIMode.OFF)
    requires_human_intervention: bool = Field(default=False)
    is_processing: bool = Field(default=False)
    last_call_started_at: Optional[datetime] = Field(default=None, description="The timestamp of the get chat with prompt (the moment n8n started processing the call)")
    trigger_timestamp: Optional[datetime] = Field(default=None, description="The timestamp of the trigger that started the call, if it's a manual trigger, it will be the timestamp of the manual trigger, if it's a follow up, it will be the timestamp of the follow up, if it's a user message, it will be the timestamp of the user message")
    last_call_cot_id: Optional[StrObjectId] = Field(default=None)
    trigger: Optional[ChainOfThoughtInChatTrigger] = Field(default=None, description="The trigger that started the call, if it's a manual trigger, it will be ChainOfThoughtInChatTrigger.MANUAL_TRIGGER, if it's a follow up, it will be ChainOfThoughtInChatTrigger.FOLLOW_UP, if it's a user message, it will be ChainOfThoughtInChatTrigger.USER_MESSAGE")
    incoming_message_id_trigger: Optional[str] = Field(default=None, description="If the trigger is a user message, this will be the id of the incoming message that triggered the call")

    def new_incoming_message_trigger(self, trigger_timestamp: datetime, incoming_message_id: str) -> None:
        if self.is_processing:
            self.end_call()
        self.is_processing = True
        self.trigger = ChainOfThoughtInChatTrigger.USER_MESSAGE
        self.incoming_message_id_trigger = incoming_message_id
        self.trigger_timestamp = trigger_timestamp

    def new_call(self, cot_id: StrObjectId, trigger: ChainOfThoughtInChatTrigger) -> Optional[StrObjectId]:
        logger.debug(f"Starting a new call for chat | ai agent {self.asset_id} | cot id {cot_id} | trigger {trigger}")
        if not trigger == ChainOfThoughtInChatTrigger.USER_MESSAGE:
            self.incoming_message_id_trigger = None
        last_call_cot_id = self.last_call_cot_id
        self.is_processing = True
        self.last_call_started_at = datetime.now(ZoneInfo("UTC"))
        self.last_call_cot_id = cot_id
        self.trigger = trigger
        return last_call_cot_id

    def is_call_valid(self, cot_id: StrObjectId) -> bool:
        return self.last_call_cot_id == cot_id and self.is_processing

    def manual_trigger(self, cot_id: StrObjectId) -> None:
        self.is_processing = True
        self.trigger = ChainOfThoughtInChatTrigger.MANUAL_TRIGGER
        self.trigger_timestamp = datetime.now(ZoneInfo("UTC"))
        logger.debug(f"Starting a manual trigger for chat | ai agent {self.asset_id} | cot id {cot_id}")

    def end_call(self) -> Optional[StrObjectId]:
        logger.debug(f"Ending a call for chat | ai agent {self.asset_id}")
        if not self.is_processing:
            raise ValueError(f"Chatty AI Agent is not processing, so it can't be ended")
        self.incoming_message_id_trigger = None
        cot_id = self.last_call_cot_id
        self.is_processing = False
        self.last_call_started_at = None
        self.last_call_cot_id = None
        self.trigger = None
        self.trigger_timestamp = None
        logger.debug(f"Ended a call for chat | ai agent {self.asset_id} | cot id {cot_id}")
        return cot_id

    @property
    def is_call_in_progress(self) -> bool:
        return self.is_processing and self.last_call_started_at is not None and self.last_call_cot_id is not None

    @property
    def is_waiting_for_call_to_start_after_incoming_message(self) -> bool:
        return self.is_processing and self.trigger == ChainOfThoughtInChatTrigger.USER_MESSAGE and self.trigger_timestamp is not None

    @property
    def is_waiting_for_call_after_manual_trigger(self) -> bool:
        return self.is_processing and self.trigger == ChainOfThoughtInChatTrigger.MANUAL_TRIGGER and self.trigger_timestamp is not None

    @property
    def current_call_cot_id(self) -> StrObjectId:
        if not self.last_call_cot_id:
            raise ValueError(f"Chatty AI Agent is not processing, so it doesn't have a current call cot id")
        return self.last_call_cot_id

    def re_run_call(self, cot_id: StrObjectId) -> Optional[StrObjectId]:
        if not self.is_call_in_progress:
            if not self.is_waiting_for_call_to_start_after_incoming_message:
                raise ValueError(f"Chatty AI Agent is not processing, so it can't be re-run, and it's not waiting for a call to start after an incoming message")
            else:
                logger.debug(f"Chatty AI Agent is still waiting for the n8n call to start after an incoming message, so there's no COT to cancel")
        cot_id_to_cancel = self.end_call()
        self.new_call(cot_id=cot_id, trigger=ChainOfThoughtInChatTrigger.RETRY_CALL)
        return cot_id_to_cancel
