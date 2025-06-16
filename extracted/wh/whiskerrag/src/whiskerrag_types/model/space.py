from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from whiskerrag_types.model.timeStampedModel import TimeStampedModel


class SpaceCreate(BaseModel):
    """
    SpaceCreate model for creating space resources.
    Attributes:
        space_name (str): Space name, example: petercat bot group.
        description (str): descrition of the space resource.
        metadata (Dict[str, Any]): metadata of the space resource.such as embedding model name
            and other parameters.
    """

    space_name: str = Field(
        ..., max_length=64, description="name of the space resource"
    )
    space_id: Optional[str] = Field(
        default=None,
        description="id of the space resource (letters, numbers, hyphens and underscores allowed, max 36 chars)",
        pattern=r"^[a-zA-Z0-9\-_]{1,36}$",
    )
    description: str = Field(..., max_length=255, description="descrition of the space")
    metadata: Dict[str, Any] = Field(
        default={},
        description="metadata of the space resource",
    )


class Space(SpaceCreate, TimeStampedModel):
    space_id: str = Field(default_factory=lambda: str(uuid4()), description="space id")
    tenant_id: str = Field(..., description="tenant id")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    def update(self, **kwargs: Dict[str, Any]) -> "Space":
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self

    @model_validator(mode="before")
    def pre_process_data(cls, data: dict) -> dict:
        for field, value in data.items():
            if isinstance(value, UUID):
                data[field] = str(value)
        if isinstance(data, dict) and not data.get("space_id"):
            data["space_id"] = str(uuid4())
        return data


class SpaceResponse(Space):
    """
    SpaceResponse model class that extends Space.
    Attributes:
         (str): Space ID.
        total_size Optional[int]: size of the all kowledge in this space.
        knowledge_size Optional[int]: count of the knowledge in this space.
    """

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    storage_size: Optional[int] = Field(
        default=0, description="size of the all kowledge in this space"
    )
    knowledge_count: Optional[int] = Field(
        default=0, description="count of the knowledge in this space"
    )

    def update(self, **kwargs: Dict[str, Any]) -> "SpaceResponse":
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
