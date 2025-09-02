from pydantic import BaseModel, Field, field_validator
from enum import StrEnum
from ...utils.types.identifier import StrObjectId
from datetime import datetime
from zoneinfo import ZoneInfo
from bson import ObjectId
import json
from typing import Dict, Any
from letschatty.models.utils.types.serializer_type import SerializerType
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode

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


class AssignedAssetToChat(BaseModel):
    id: StrObjectId = Field(frozen=True, default_factory=lambda: str(ObjectId()))
    asset_type: ChatAssetType = Field(frozen=True)
    asset_id: StrObjectId = Field(frozen=True)
    assigned_at: datetime = Field(frozen=True, default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    assigned_by: StrObjectId = Field(frozen=True)

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        serializer = kwargs.pop("serializer", SerializerType.API)
        dumped_json = super().model_dump_json(*args, **kwargs)
        loaded_json = json.loads(dumped_json)
        if serializer == SerializerType.DATABASE:
            loaded_json["assigned_at"] = self.assigned_at
        return loaded_json

    def model_dump(
        self,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        return json.loads(super().model_dump_json(*args, **kwargs))

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