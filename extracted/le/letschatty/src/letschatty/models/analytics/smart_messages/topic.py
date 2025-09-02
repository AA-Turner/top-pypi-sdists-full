from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, List, ClassVar, Dict, Any
from bson.objectid import ObjectId
from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from ...utils.types.serializer_type import SerializerType
from pydantic import Field, field_validator, model_validator

from ...utils.types import StrObjectId
from .topic_message import MessageTopic

class Topic(CompanyAssetModel):
    name: str
    default_source_id: StrObjectId = Field(default_factory=lambda: str(ObjectId()))
    messages: List[MessageTopic] = Field(default_factory=list)
    lock_duration: timedelta = Field(default=timedelta(seconds=30))
    preview_class: ClassVar[type[ChattyAssetPreview]] = ChattyAssetPreview
    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"default_source_id", "messages", "lock_duration"}
    }

    def model_dump(self, *args, **kwargs) -> dict:
        kwargs["by_alias"] = True
        dump = super().model_dump(*args, **kwargs)
        dump["lock_duration"] = int(self.lock_duration.total_seconds())
        return dump

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["by_alias"] = True
        dump = super().model_dump_json(*args, **kwargs)
        dump["lock_duration"] = int(self.lock_duration.total_seconds())
        return dump

    @model_validator(mode='after')
    def validate_messages_and_duration(self):
        """Validate messages have a default and lock_duration is correct"""
        if self.messages and not any(m.is_default for m in self.messages):
            self.messages[0].is_default = True

        return self

    @field_validator('lock_duration', mode='before')
    def validate_lock_duration(cls, v: int | timedelta) -> timedelta:
        if isinstance(v, int):
            return timedelta(seconds=v)
        elif isinstance(v, timedelta):
            return v
        else:
            raise ValueError("lock_duration must be a timedelta or an int")
