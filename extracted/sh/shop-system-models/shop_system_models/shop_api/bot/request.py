import enum
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OrderStatusTypes(str, enum.Enum):
    CREATED = "CREATED"
    CANCELLED = "CANCELLED"
    PAID = "PAID"


class OrderStatusModel(BaseModel):
    name: str
    message: str
    in_timeline: bool | None = False
    type: Optional[OrderStatusTypes] = None

    # @field_validator('name', )
    # def validate_name_len(cls, value):
    #     if len(value) > 16:
    #         return value[:16]
    #     return value


class MessagesType(str, Enum):
    admin_order_created = "admin_order_created"
    admin_order_updated = "admin_order_updated"
    user_order_created = "user_order_created"
    user_order_updated = "user_order_updated"


class MessageModel(BaseModel):
    type: MessagesType
    text: str


class ButtonType(str, Enum):
    inline_url = "inline_url"
    inline_payload = "inline_payload"
    app_url = "app_url"


class ButtonModel(BaseModel):
    linked_status: OrderStatusModel | None = None
    type: ButtonType
    name: str
    payload: str | None = ""
