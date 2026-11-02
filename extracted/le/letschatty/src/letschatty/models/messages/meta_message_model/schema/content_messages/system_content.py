from pydantic import BaseModel, field_validator
from enum import StrEnum
from typing import Optional
from pydantic import Field

class MetaSystemTypeMessage(StrEnum):
    CUSTOMER_CHANGED_NUMBER = "customer_changed_number"
    CUSTOMER_IDENTITY_CHANGED = "customer_identity_changed"
    USER_CHANGED_NUMBER = "user_changed_number"
    # El usuario cambió de número y Meta le regeneró el BSUID. Ver
    # https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids/
    USER_CHANGED_USER_ID = "user_changed_user_id"
    # Cualquier tipo que Meta agregue y todavía no conozcamos. Sin este valor, un tipo
    # nuevo hacía rechazar el webhook entero con un 422 (es lo que pasó con
    # USER_CHANGED_USER_ID): mismo criterio que `Message.coerce_unknown_type`.
    UNKNOWN = "unknown"

    @classmethod
    def values(cls) -> set[str]:
        return {member.value for member in cls}

class MetaSystemContent(BaseModel):
    """When messages type is set to system, a customer has updated their phone number or profile information, this object is included in the messages object. System objects have the following properties:
    body – String. Describes the change to the customer's identity or phone number.
    identity – String. Hash for the identity fetched from server.
    new_wa_id – String. New WhatsApp ID for the customer when their phone number is updated. Available on webhook versions v11.0 and earlier.
    wa_id – String. New WhatsApp ID for the customer when their phone number is updated. Available on webhook versions v12.0 and later.
        Omitted on `user_changed_user_id` when the user adopted a username and Meta can't share the phone.
    user_id – String. `user_changed_user_id` only: the NEW BSUID.
    previous_user_id – String. `user_changed_user_id` only: the BSUID being replaced. Meta's example payload
        doesn't show it, but every real webhook we received carries it (10 of 10, Sept 2026).
    parent_user_id – String. `user_changed_user_id` only: the new parent BSUID, when the portfolio has one.
    type – String. Type of system update. Will be one of the following:.
    customer_changed_number – A customer changed their phone number.
    customer_identity_changed – A customer changed their profile information.
    user_changed_user_id – A user changed their phone number, so their BSUID was regenerated.
    customer – String. The WhatsApp ID for the customer prior to the update."""
    body: str
    identity: Optional[str] = Field(default=None)
    wa_id: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    previous_user_id: Optional[str] = Field(default=None)
    parent_user_id: Optional[str] = Field(default=None)
    type: MetaSystemTypeMessage
    customer: Optional[str] = Field(default=None)

    @field_validator("type", mode="before")
    @classmethod
    def coerce_unknown_type(cls, v):
        if isinstance(v, str) and v not in MetaSystemTypeMessage.values():
            return MetaSystemTypeMessage.UNKNOWN
        return v

    def is_user_id_change(self) -> bool:
        return self.type == MetaSystemTypeMessage.USER_CHANGED_USER_ID
