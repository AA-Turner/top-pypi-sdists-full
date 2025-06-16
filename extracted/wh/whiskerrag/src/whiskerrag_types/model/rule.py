from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from whiskerrag_types.model.language import LanguageEnum
from whiskerrag_types.model.timeStampedModel import TimeStampedModel


class RuleCreate(BaseModel):
    content: str = Field(..., description="rule content")
    space_id: Optional[str] = Field(
        default=None, description="space id. GlobalRule do not need set"
    )
    language: LanguageEnum = Field(
        default=LanguageEnum.zh, description="rule content language, ISO 639-1 code"
    )


class Rule(TimeStampedModel):
    content: str = Field(description="rule content")
    language: LanguageEnum = Field(
        default=LanguageEnum.zh, description="rule content language, ISO 639-1 code"
    )
    tenant_id: str = Field(description="tenant id")
    space_id: Optional[str] = Field(default=None, description="space id")

    is_active: bool = Field(default=True)

    def update(self, **kwargs: Dict[str, Any]) -> "Rule":
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self

    @field_validator("is_active", mode="before")
    @classmethod
    def convert_tinyint_to_bool(cls, v: Any) -> bool:
        return bool(v)


class GlobalRule(Rule):
    @model_validator(mode="after")
    def validate_space_id_is_none(self) -> "GlobalRule":
        if self.space_id is not None:
            raise ValueError("space_id must be None for GlobalRule")
        return self


class SpaceRule(Rule):
    space_id: str = Field(description="space id")
