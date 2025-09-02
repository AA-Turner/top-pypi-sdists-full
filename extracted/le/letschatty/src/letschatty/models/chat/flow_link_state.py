from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from typing import Optional, Self, Dict, Any, TYPE_CHECKING

from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.utils.types.serializer_type import SerializerType
from letschatty.models.copilot.links import LinkItem
from pydantic import BaseModel, ConfigDict, Field
from zoneinfo import ZoneInfo
from letschatty.models.company.assets.flow import FlowPreview
from letschatty.models.company.assets.chat_assets import AssignedAssetToChat, ChatAssetType

if TYPE_CHECKING:
    from letschatty.models.execution.execution import ExecutionContext

class ExecutionResult(StrEnum):
    EXECUTED = "executed"
    FAILED = "failed"
    POSTPONED_FOR_LATER = "postponed_for_later"
    NOT_EXECUTED = "not_executed"

class StateTrigger(StrEnum):
    NEXT_CALL = "next_call"
    CHAT_UPDATE = "chat_update"

class FlowStateAssignedToChat(AssignedAssetToChat):
    company_id: StrObjectId
    asset_id: StrObjectId = Field(alias="flow_id")
    chat_id: StrObjectId = Field()
    next_call: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    last_call: Optional[datetime] = Field(default=None)
    description: str = Field(default="", description="Usefull for AI follow ups where we wanta a specific prompt for the follow up")
    executed_step: int = Field(default=0)
    repeat_step: int = Field(default=0)
    trigger: StateTrigger = Field(default=StateTrigger.NEXT_CALL)
    should_execute: bool = Field(default=True)
    execution_result: ExecutionResult = Field(default=ExecutionResult.NOT_EXECUTED)
    execution_time_seconds: Optional[float] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    last_incoming_message_id: Optional[str] = Field(default=None)
    is_smart_follow_up: bool = Field(default=False)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        serializer = kwargs.get("serializer", SerializerType.API)
        loaded_json = super().model_dump_json(*args, **kwargs)
        if serializer == SerializerType.DATABASE:
            loaded_json["next_call"] = datetime.fromisoformat(loaded_json["next_call"])
            loaded_json["last_call"] = datetime.fromisoformat(loaded_json["last_call"]) if loaded_json["last_call"] else None
        return loaded_json

    @property
    def flow_id(self) -> StrObjectId:
        return self.asset_id

    def __eq__(self, other: Self) -> bool:
        return self.flow_id == other.flow_id and self.chat_id == other.chat_id

    @staticmethod
    def from_link(link: LinkItem, execution_context: ExecutionContext, description: str, last_incoming_message_id: Optional[str] = None, next_call: Optional[datetime] = None, is_smart_follow_up: bool = False) -> FlowStateAssignedToChat:
        if is_smart_follow_up:
            return SmartFollowUpState(
                flow_id=link.flow_id,
                chat_id=link.chat_id,
                company_id=link.company_id,
                asset_type=ChatAssetType.WORKFLOW,
                assigned_by=execution_context.executor.id,
                description=description,
                last_incoming_message_id=last_incoming_message_id,
                next_call=next_call if next_call else datetime.now(ZoneInfo("UTC")),
                is_smart_follow_up=is_smart_follow_up
            )
        else:
            return FlowStateAssignedToChat(
                flow_id=link.flow_id,
                chat_id=link.chat_id,
                company_id=link.company_id,
                asset_type=ChatAssetType.WORKFLOW,
                assigned_by=execution_context.executor.id,
                description=description,
                last_incoming_message_id=last_incoming_message_id,
                next_call=next_call if next_call else datetime.now(ZoneInfo("UTC")),
                is_smart_follow_up=is_smart_follow_up
            )

    @classmethod
    def from_json(cls, json: dict) -> FlowStateAssignedToChat | SmartFollowUpState:
        if json.get("is_smart_follow_up", False):
            return SmartFollowUpState(**json)
        else:
            return cls(**json)


    @classmethod
    def from_chat(cls, chat: dict) -> list[FlowStateAssignedToChat]:
        if "flow_states" not in chat:
            return []
        states = []
        current_time = datetime.now(ZoneInfo("UTC"))

        for flow_state in chat["flow_states"]:
            next_call = flow_state["next_call"].replace(tzinfo=ZoneInfo("UTC"))
            trigger = flow_state.get("trigger", StateTrigger.NEXT_CALL)

            should_execute = (
                next_call <= current_time and
                (trigger == StateTrigger.NEXT_CALL or
                (trigger == StateTrigger.CHAT_UPDATE and
                chat["updated_at"] > flow_state.get("last_call", datetime.min.replace(tzinfo=ZoneInfo("UTC")))))
            )

            state_class = cls.from_json(flow_state)
            state_class.should_execute = should_execute
            states.append(state_class)

        return states

class FullState(FlowStateAssignedToChat):
    title: str = Field(default="")
    description: str = Field(default="")

    @staticmethod
    def from_state(state: FlowStateAssignedToChat, flow_preview: FlowPreview) -> FullState:
        full_state = FullState(**state.__dict__, title=flow_preview.title, description=flow_preview.description)
        return full_state

class SmartFollowUpState(FlowStateAssignedToChat):
    """Smart follow-up workflow state with tracking"""
    # Follow-up strategy and tracking
    total_followups_sent: int = Field(default=0)
    consecutive_count: int = Field(default=0)