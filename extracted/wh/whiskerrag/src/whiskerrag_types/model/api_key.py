import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import (
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from whiskerrag_types.model.permission import Permission
from whiskerrag_types.model.timeStampedModel import TimeStampedModel


class APIKey(TimeStampedModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    key_id: str = Field(default_factory=lambda: str(uuid4()), description="key id")
    tenant_id: str = Field(description="tenant id")
    key_name: str = Field(default="", description="key name")
    key_value: str = Field(description="key value")
    permissions: List[Permission] = Field(
        default_factory=list, description="permissions config"
    )
    rate_limit: int = Field(default=0, ge=0, description="rate limit per minute")
    expires_at: Optional[datetime] = Field(
        default=None, description="expire time (UTC)"
    )
    is_active: bool = Field(default=True, description="key status")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="key metadata")

    @model_validator(mode="before")
    @classmethod
    def validate_permissions(cls, data: Any) -> Any:
        for field, value in data.items():
            if isinstance(value, UUID):
                data[field] = str(value)
        if isinstance(data, dict) and not data.get("key_id"):
            data["key_id"] = str(uuid4())
        if isinstance(data, dict) and "permissions" in data:
            perms = data["permissions"]
            if isinstance(perms, str):
                try:
                    data["permissions"] = json.loads(perms)
                except json.JSONDecodeError:
                    data["permissions"] = {}
        return data

    @model_validator(mode="after")
    def validate_expires(self) -> "APIKey":
        if self.expires_at:
            now = datetime.now(timezone.utc)
            if self.expires_at.tzinfo is None:
                self.expires_at = self.expires_at.replace(tzinfo=timezone.utc)

            if self.expires_at < now:
                raise ValueError("expires_at must be future time (UTC)")
        return self

    @field_validator("is_active", mode="before")
    @classmethod
    def convert_tinyint_to_bool(cls, v: Any) -> bool:
        return bool(v)

    @field_serializer("expires_at")
    def serialize_expires_at(self, dt: Union[datetime, None]) -> Optional[str]:
        if dt:
            return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return None
