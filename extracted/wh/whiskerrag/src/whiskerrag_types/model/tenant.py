import json
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import Field, field_validator, model_validator

from whiskerrag_types.model.timeStampedModel import TimeStampedModel


class Tenant(TimeStampedModel):
    tenant_id: str = Field(
        default_factory=lambda: str(uuid4()), description="tenant id"
    )
    tenant_name: str = Field("", description="tenant name")
    email: str = Field(..., description="email")
    secret_key: str = Field("", description="secret_key")
    is_active: bool = Field(True, description="is active")
    metadata: Optional[dict] = Field(
        None, description="Metadata for the tenant", alias="metadata"
    )

    def update(self, **kwargs: Any) -> "Tenant":
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self

    @field_validator("is_active", mode="before")
    @classmethod
    def convert_tinyint_to_bool(cls, v: Any) -> bool:
        return bool(v)

    @model_validator(mode="before")
    def pre_process_data(cls, data: dict) -> dict:
        for field, value in data.items():
            if isinstance(value, UUID):
                data[field] = str(value)
            if field == "metadata" and isinstance(value, str):
                data[field] = json.loads(value)
        return data
