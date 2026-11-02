from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, JsonValue


class ResolvedDirectiveBase(BaseModel):
    directive_id: UUID
    key: str
    order: int
    version_id: UUID
    version: int
    name: str | None = None
    description: str | None = None
    directive_metadata: JsonValue | None = None
    version_created_at: datetime


class ResolvedSystemPromptDirective(ResolvedDirectiveBase):
    injection: Literal["system_prompt"]
    body: str


class ResolvedSkillDirective(ResolvedDirectiveBase):
    injection: Literal["skill"]
    dss_entry_id: UUID


ResolvedDirective = Annotated[
    ResolvedSystemPromptDirective | ResolvedSkillDirective,
    Field(discriminator="injection"),
]


class DirectiveResolveResponse(BaseModel):
    directives: list[ResolvedDirective]
