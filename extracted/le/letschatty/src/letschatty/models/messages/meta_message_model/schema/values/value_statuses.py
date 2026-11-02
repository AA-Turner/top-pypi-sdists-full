from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
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
    # The Status enum is intentionally strict: it constrains what the code has to handle
    # and a status we don't manage fails loudly (ValidationError → 422) rather than being
    # silently accepted. `played` (voice notes, Meta 2026-03-17) is a first-class member;
    # the receiver routes it to Message.played_at, never to Message.status.
    status: Status
    timestamp: datetime
    # `recipient_id` (phone) is OPTIONAL: a status for a message SENT to a BSUID (a phone-less
    # username-adopter) arrives with only `recipient_user_id` and no phone. Keeping it required
    # made pydantic reject the whole webhook (422 → the delivery/read/FAILED receipt is dropped,
    # so a failed BSUID send would look successful forever). Resolve the chat by BSUID when the
    # phone is absent.
    recipient_id: Optional[str] = None
    recipient_user_id: Optional[str] = Field(default=None, description="BSUID of the recipient (e.g. 'CO.xxx') — present when the message was sent to a BSUID; the stable identity when recipient_id (phone) is absent")
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None
    errors: Optional[List[ErrorDetail]] = None

    def get_recipient_id(self) -> Optional[str]:
        return self.recipient_id

    def get_recipient_user_id(self) -> Optional[str]:
        return self.recipient_user_id

    @field_validator('timestamp')
    def ensure_utc(cls, v):
        if isinstance(v, str):
            # Meta sends an epoch string; parse it as UTC (was tz-naive → server-tz-dependent).
            v = datetime.fromtimestamp(int(v), tz=ZoneInfo("UTC"))
        if isinstance(v, datetime):
            return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
        raise ValueError('must be a datetime')