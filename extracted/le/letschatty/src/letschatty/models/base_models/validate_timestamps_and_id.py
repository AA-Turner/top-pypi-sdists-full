from pydantic import BaseModel, field_validator, model_validator, Field
from .helpers import _normalize_precision
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Optional

import logging

logger = logging.getLogger("TimestampValidationMixin")

class TimestampValidationMixin(BaseModel):
    """Mixin class providing timestamp validation functionality"""
    updated_at: datetime
    created_at: datetime = Field(frozen=True)
    deleted_at: Optional[datetime] = Field(default=None)


    @model_validator(mode='before')
    @classmethod
    def set_timestamps(cls, data: Dict) -> Dict:
        """Handle timestamps before model creation"""
        logger.debug(f"Setting timestamps for {cls.__name__} with data: {data}")
        if isinstance(data, TimestampValidationMixin):
            return data
        has_id = bool(data.get('id') or data.get('_id'))
        now = _normalize_precision(datetime.now(ZoneInfo("UTC")))

        if 'updated_at' not in data or data['updated_at'] is None:
            data['updated_at'] = now

        if has_id and ('created_at' not in data or data['created_at'] is None):
            raise ValueError("created_at is required when id is provided")

        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = now

        return data

    @field_validator('deleted_at', mode='before')
    @classmethod
    def validate_deleted_at(cls, v: datetime | str) -> Optional[datetime | str]:
        if not v:
            return None
        else:
            return v

    @field_validator('created_at', 'updated_at', 'deleted_at', mode="after")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v is None:
            return v
        return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))


    def update_now(self):
        self.updated_at = _normalize_precision(datetime.now(ZoneInfo("UTC")))
