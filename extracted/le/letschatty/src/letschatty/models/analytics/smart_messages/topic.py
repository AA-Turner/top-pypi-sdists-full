from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, List, ClassVar, Dict, Any
from bson.objectid import ObjectId
from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from ...utils.types.serializer_type import SerializerType
from pydantic import Field, field_validator, model_validator

from ...utils.types import StrObjectId
from .topic_message import MessageTopic

class TopicPreview(ChattyAssetPreview):
    """What the topic list shows: the topic's account too, so the screen can filter and label by number."""
    account_id: Optional[StrObjectId] = None

    @field_validator("account_id", mode="before")
    @classmethod
    def _blank_is_none(cls, value: Any) -> Any:
        return value or None

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"account_id": 1}

    @classmethod
    def from_asset(cls, asset: "Topic") -> "TopicPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            account_id=asset.account_id,
        )


class Topic(CompanyAssetModel):
    name: str
    account_id: Optional[StrObjectId] = Field(
        default=None,
        frozen=True,
        description=(
            "The WhatsApp account (number) this topic opens: the link and the pixel button of a topic always "
            "open ITS number, and an incoming message is matched only against the topics of the chat's account. "
            "Fixed for the life of the topic (frozen: no update moves it; to use the same texts on another number "
            "the topic is duplicated). Without it (topics from before accounts) it is the company's default "
            "account's; the migration stamps every existing topic."
        ),
    )
    default_source_id: StrObjectId = Field(default_factory=lambda: str(ObjectId()))
    messages: List[MessageTopic] = Field(default_factory=list)
    lock_duration: timedelta = Field(default=timedelta(seconds=30))
    preview_class: ClassVar[type[ChattyAssetPreview]] = TopicPreview
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

    @field_validator("account_id", mode="before")
    @classmethod
    def validate_account_id(cls, value: Any) -> Any:
        """`StrObjectId` rejects the empty string, which is what a form without the field sends."""
        return value or None

    @field_validator('lock_duration', mode='before')
    def validate_lock_duration(cls, v: int | timedelta) -> timedelta:
        if isinstance(v, int):
            return timedelta(seconds=v)
        elif isinstance(v, timedelta):
            return v
        else:
            raise ValueError("lock_duration must be a timedelta or an int")
