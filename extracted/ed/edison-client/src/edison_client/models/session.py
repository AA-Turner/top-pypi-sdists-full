from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SessionType(StrEnum):
    TRAJECTORY = auto()
    PROJECT = auto()
    WORLD_MODEL = auto()
    CONVERSATION = auto()


class Session(BaseModel):
    id: UUID = Field(description="Session identifier")
    type_id: UUID = Field(
        description=(
            "Foreign key into the session's owning resource. For chat "
            "sessions this is the project_id."
        )
    )
    type: SessionType = Field(description="Session type discriminator")
    job_name: str | None = Field(
        default=None, description="Job name associated with the session, if any"
    )
    created_at: datetime | None = Field(
        default=None, description="Timestamp when the session was created"
    )

    model_config = ConfigDict(from_attributes=True)
