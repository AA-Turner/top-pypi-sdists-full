from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator
from zoneinfo import ZoneInfo
from enum import StrEnum
from .value_errors import ERROR_CODE_DETAILS
from .....utils.types import Status

class MetaConversationOriginType(StrEnum):
    authentication = "authentication"
    marketing = "marketing"
    utility = "utility"
    service = "service"
    referral_conversion = "referral_conversion"

class Origin(BaseModel):
    type: MetaConversationOriginType

class Conversation(BaseModel):
    id: str
    expiration_timestamp: Optional[str] = None
    origin: Optional[Origin] = None

class Pricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str

class ErrorData(BaseModel):
    details: str

class ErrorDetail(BaseModel):
    code: int
    title: str
    message: Optional[str] = None
    error_data: Optional[ErrorData] = None
    href: Optional[str] = None

    def get_error_details(self) -> str:
        if self.error_data is not None:
            return self.error_data.details
        else:
            return ""

    def get_more_info(self) -> str:
        details= ERROR_CODE_DETAILS.get(self.code, {})
        if details:
            details_str = f"Error: {details.get('description')}\nSolucion: {details.get('solution')}"
            return details_str
        else:
            return ""


class StatusNotification(BaseModel):
    id: str
    status: Status
    timestamp: datetime
    recipient_id: str
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None
    errors: Optional[List[ErrorDetail]] = None

    @field_validator('timestamp')
    def ensure_utc(cls, v):
        if isinstance(v, str):
            v = datetime.fromtimestamp(int(v))
        if isinstance(v, datetime):
            return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
        raise ValueError('must be a datetime')