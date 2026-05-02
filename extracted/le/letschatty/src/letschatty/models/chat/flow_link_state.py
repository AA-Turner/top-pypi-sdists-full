from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from typing import Optional, Self, Dict, Any, TYPE_CHECKING
import logging
from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.utils.types.serializer_type import SerializerType
from letschatty.models.copilot.links import LinkItem
from pydantic import BaseModel, ConfigDict, Field
from zoneinfo import ZoneInfo
from letschatty.models.company.assets.flow import FlowPreview
from letschatty.models.company.assets.chat_assets import AssignedAssetToChat, ChatAssetType

logger = logging.getLogger("FlowStateAssignedToChat")

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
    FIRST_OF_NEXT_CALL_OR_CHAT_UPDATE = "first_of_next_call_or_chat_update"

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
    total_followups_sent: int = Field(default=0)
    consecutive_count: int = Field(default=0)
    execution_attempts: int = Field(default=0)
    max_total_follow_ups_reached: bool = Field(default=False, description="If true, the total follow ups sent reached the maximum limit. This won't change once its set to true.")
    max_consecutive_follow_ups_reached: bool = Field(default=False, description="If true, the consecutive follow ups reached the maximum limit. This resets each time the user sends a message.")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_by_name=True,
        validate_by_alias=True
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
    def from_link(link: LinkItem, execution_context: ExecutionContext, description: str, last_incoming_message_id: Optional[str] = None, next_call: Optional[datetime] = None, is_smart_follow_up: bool = False, trigger: Optional[StateTrigger] = None) -> FlowStateAssignedToChat:
        kwargs: Dict[str, Any] = dict(
            flow_id=link.flow_id,
            chat_id=link.chat_id,
            company_id=link.company_id,
            asset_type=ChatAssetType.WORKFLOW,
            assigned_by=execution_context.executor.id,
            description=description,
            last_incoming_message_id=last_incoming_message_id,
            next_call=next_call if next_call else datetime.now(ZoneInfo("UTC")),
            is_smart_follow_up=is_smart_follow_up,
        )
        if trigger is not None:
            kwargs["trigger"] = trigger
        return FlowStateAssignedToChat(**kwargs)

    @classmethod
    def from_json(cls, json: dict) -> FlowStateAssignedToChat:
        logger.debug(f"json: {json}")
        if isinstance(json, FlowStateAssignedToChat):
            logger.debug(f"json is instance of  {type(json)}")
            return json
        return FlowStateAssignedToChat(**json)


    @classmethod
    def from_chat(cls, chat: dict) -> list[FlowStateAssignedToChat]:
        if "flow_states" not in chat:
            return []
        states = []
        utc = ZoneInfo("UTC")
        current_time = datetime.now(utc)

        def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
            if value is None:
                return None
            if getattr(value, "tzinfo", None) is None:
                return value.replace(tzinfo=utc)
            return value.astimezone(utc)

        chat_updated_at = _as_utc(chat.get("updated_at"))

        for flow_state in chat["flow_states"]:
            next_call = _as_utc(flow_state.get("next_call")) or current_time
            trigger = flow_state.get("trigger", StateTrigger.NEXT_CALL)
            last_call = _as_utc(flow_state.get("last_call")) or datetime.min.replace(tzinfo=utc)
            chat_updated_since_last_call = (
                chat_updated_at is not None and chat_updated_at > last_call
            )

            if trigger == StateTrigger.NEXT_CALL:
                should_execute = next_call <= current_time
            elif trigger == StateTrigger.CHAT_UPDATE:
                should_execute = next_call <= current_time and chat_updated_since_last_call
            elif trigger == StateTrigger.FIRST_OF_NEXT_CALL_OR_CHAT_UPDATE:
                should_execute = next_call <= current_time or chat_updated_since_last_call
            else:
                should_execute = False

            state_class = cls.from_json(flow_state)
            state_class.should_execute = should_execute
            states.append(state_class)

        return states

class FullState(FlowStateAssignedToChat):
    title: str = Field(default="")
    description: str = Field(default="")

    @staticmethod
    def from_state(state: FlowStateAssignedToChat, flow_preview: FlowPreview) -> FullState:
        full_state = FullState(**state.__dict__, title=flow_preview.title, description=flow_preview.description if flow_preview.description else "")
        return full_state

class SmartFollowUpState(FlowStateAssignedToChat):
    """Smart follow-up workflow state with tracking"""
    logger.warning("SmartFollowUpState is deprecated")
    pass