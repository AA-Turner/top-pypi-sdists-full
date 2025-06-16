from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator

from whiskerrag_types.model.utils import parse_datetime


class TimeStampedModel(BaseModel):
    """Base class for models with timestamp fields."""

    created_at: Optional[datetime] = Field(
        default=None, alias="gmt_create", description="creation time"
    )
    updated_at: Optional[datetime] = Field(
        default=None, alias="gmt_modified", description="update time"
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_validator(mode="before")
    def pre_process_timestamps(cls, data: dict) -> dict:
        field_mappings = {"created_at": "gmt_create", "updated_at": "gmt_modified"}
        for field, alias_name in field_mappings.items():
            val = data.get(field) or data.get(alias_name)
            if val is None:
                continue

            if isinstance(val, str):
                dt = parse_datetime(val)
            else:
                dt = val

            if dt and dt.tzinfo:
                dt = dt.astimezone(timezone.utc)
            elif dt:
                dt = dt.replace(tzinfo=timezone.utc)

            data[field] = dt
            data[alias_name] = dt

        return data

    @model_validator(mode="after")
    def set_timestamp_defaults(self) -> "TimeStampedModel":
        now = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
        return self

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
