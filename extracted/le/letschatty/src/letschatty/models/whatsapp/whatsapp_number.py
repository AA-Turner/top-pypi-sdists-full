"""The routing record of a Meta phone number.

`_id` is the `phone_number_id`, so a number can belong to only one account in all of Chatty:
the database rejects a second claim. A number an account stopped using stays here, inactive,
so late webhooks (statuses, a message to the old number) still reach its account.

`digits` is the visible number: Meta gives a number a NEW `phone_number_id` when it moves to
another WABA, so «is this number already in Chatty» is answered by the digits. A number taken
down in Meta (`taken_down_at`, deregistered) is free: any company can connect it again.
"""
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..utils.types.identifier import StrObjectId
from .time import utc_now


#: `Empresa.display_phone_number`'s default: what a company shows before Meta gives its real number (a coexistence
#: signup can finish without it). It is nobody's number, so it never answers «is this number already in Chatty».
PLACEHOLDER_DIGITS = "33333333333333"


def phone_digits(value: Any) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def known_number_digits(value: Any) -> str:
    """The digits of a real number, or "" when it is the placeholder (or has none)."""
    digits = phone_digits(value)
    return "" if digits == PLACEHOLDER_DIGITS else digits


class WhatsAppNumber(BaseModel):
    phone_number_id: str = Field(alias="_id")
    company_id: StrObjectId
    account_id: StrObjectId
    display_phone_number: str
    active: bool = True
    since: datetime = Field(default_factory=utc_now)
    until: Optional[datetime] = None
    digits: Optional[str] = None
    taken_down_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @model_validator(mode="after")
    def _digits_from_display(self) -> "WhatsAppNumber":
        # A previous number recorded by the migration carries its id as display, and a number Meta has not named yet
        # carries the placeholder: no digits known for either.
        if not self.digits and self.display_phone_number and self.display_phone_number != self.phone_number_id:
            self.digits = known_number_digits(self.display_phone_number) or None
        return self

    @property
    def is_live(self) -> bool:
        """Still Chatty's (current or previous): nobody else may connect it."""
        return self.taken_down_at is None

    def to_document(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "WhatsAppNumber":
        return cls(**document)
