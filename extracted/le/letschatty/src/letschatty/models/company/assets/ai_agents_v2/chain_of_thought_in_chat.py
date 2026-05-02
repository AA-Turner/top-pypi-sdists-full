from pydantic import ConfigDict, Field, BaseModel, model_validator
from typing import Optional, List
from ....base_models import CompanyAssetModel
from ....utils.types.identifier import StrObjectId
from enum import StrEnum
from .chatty_ai_agent import ChattyAIAgent
from ....base_models.chatty_asset_model import ChattyAssetPreview
from typing import ClassVar, Type, Any, Dict
from datetime import datetime
from zoneinfo import ZoneInfo
from bson import ObjectId

class ChainOfThoughtInChatTrigger(StrEnum):
    """Trigger for the chain of thought in chat"""
    USER_MESSAGE = "user_message"
    FOLLOW_UP = "follow_up"
    MANUAL_TRIGGER = "manual_trigger"
    AUTOMATIC_TAGGING = "automatic_tagging"
    RETRY_CALL = "retry_call"
    DOUBLE_CHECKER = "double_checker"

class ChainOfThoughtInChatStatus(StrEnum):
    """Status for the chain of thought in chat"""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"



class ChainOfThoughtInChatRequest(BaseModel):
    """Request for the chain of thought in chat"""
    id: StrObjectId = Field(description="The id of the chain of thought")
    trigger: ChainOfThoughtInChatTrigger
    # trigger_id removed - trigger info is in: incoming_message_ids for user_message,
    # triggered_by_user_id for manual_trigger, smart_follow_up_id for follow_up
    chatty_ai_agent_id : str = Field(description="The chatty ai agent at the moment of triggering the chain of thought")
    chain_of_thought : Optional[str] = Field(default=None, description="The chain of thought")
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Confidence score for the response reasoning, normalized between 0 and 100"
    )
    name: str = Field(description="A title for the chain of thought", alias="title")

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        arbitrary_types_allowed=True
                )

    @model_validator(mode='before')
    @classmethod
    def auto_generate_id_for_tagger(cls, data: Any) -> Any:
        """
        Auto-generate id for tagger executions (AUTOMATIC_TAGGING trigger).
        This ensures tagger callbacks always have an id even if not provided.
        Other triggers must provide the id explicitly (since it was previously generated when the get chat with prompt was called)
        """
        if isinstance(data, dict):
            trigger = data.get('trigger')
            # Only auto-generate for AUTOMATIC_TAGGING trigger if id is missing
            if (trigger == ChainOfThoughtInChatTrigger.AUTOMATIC_TAGGING or
                trigger == ChainOfThoughtInChatTrigger.AUTOMATIC_TAGGING.value) and not data.get('id'):
                data['id'] = str(ObjectId())
        return data

    @classmethod
    def example(cls) -> dict:
        return {
            "trigger": "user_message",
            "chatty_ai_agent_id": "456",
            "chain_of_thought": "The user's not from the jurisdiction of the law firm, so we need to offer a consultation service with extra fees",
            "confidence": 86,
            "name": "Out of jurisdiction - consultation service"
        }

    @property
    def obtained_chain_of_thought(self) -> str:
        if self.chain_of_thought is None:
            raise ValueError("Chain of thought is not set")
        return self.chain_of_thought



class ChainOfThoughtInChatPreview(ChattyAssetPreview):
    """Preview of the chain of thought in chat"""
    chat_id : StrObjectId
    trigger: ChainOfThoughtInChatTrigger
    # trigger_id removed - trigger info is in: incoming_message_ids for user_message,
    # triggered_by_user_id for manual_trigger, smart_follow_up_id for follow_up
    chain_of_thought : Optional[str] = Field(default=None, description="The chain of thought")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Confidence score between 0 and 100")
    status: Optional[ChainOfThoughtInChatStatus] = Field(default=None, description="The status of the chain of thought")
    name: str = Field(description="A title for the chain of thought")

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"chat_id": 1, "trigger": 1, "chain_of_thought": 1, "confidence": 1, "name": 1, "status": 1}

    @classmethod
    def from_dict(cls, data: dict) -> 'ChainOfThoughtInChatPreview':
        return cls(**data)

    @classmethod
    def from_asset(cls, asset: 'ChainOfThoughtInChat') -> 'ChainOfThoughtInChatPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            chat_id=asset.chat_id,
            trigger=asset.trigger,
            chain_of_thought=asset.chain_of_thought,
            confidence=asset.confidence,
            status=asset.status,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at
        )


class ChainOfThoughtInChat(CompanyAssetModel):
    """Chain of thought in chat"""
    chat_id : StrObjectId
    trigger: ChainOfThoughtInChatTrigger = Field(description="The trigger of the chain of thought")
    # trigger_id removed - trigger info is in: incoming_message_ids for user_message,
    # triggered_by_user_id for manual_trigger, smart_follow_up_id for follow_up
    status: ChainOfThoughtInChatStatus = Field(default=ChainOfThoughtInChatStatus.PROCESSING, description="The status of the chain of thought")
    chatty_ai_agent_id : StrObjectId = Field(description="The chatty ai agent id")
    chatty_ai_agent : Dict[str, Any] = Field(description="The chatty ai agent at the moment of triggering the chain of thought", exclude=True,default_factory=dict)
    chain_of_thought : Optional[str] = Field(default=None, description="The chain of thought")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Confidence score between 0 and 100")
    name: str = Field(description="A title for the chain of thought", alias="title")
    preview_class: ClassVar[Type[ChattyAssetPreview]] = ChainOfThoughtInChatPreview

    def add_cot_to_existing_cot_if_exists(self, cot: str) -> None:
        if self.chain_of_thought is None:
            self.chain_of_thought = cot
        else:
            self.chain_of_thought += f"\n{cot}"
