from pydantic import BaseModel
from shops_payment_processing.models.invoice import ( # type: ignore
    InvoiceWithPaymentLinkMessageModel,  # type: ignore
)

from shop_system_models.shop_api.commands.request import NotificationPayloadModel
from shop_system_models.shop_api.shop.request.orders import (
    InvoiceTGMessageModel,
    InvoiceTONMessageModel,
)
from shop_system_models.shop_api.shop.request.orders import (
    InvoiceWithPaymentLinkMessageModel as InvoiceWithPaymentLinkMessageModelLocal,
)


class SetAdminMessageIdProcess(BaseModel):
    admin_message_id: int | None = None


class SetProcessStatus(BaseModel):
    message: str | None = None
    success: bool | None = None


class ProcessModel(SetAdminMessageIdProcess, SetProcessStatus):
    name: str
    process_key: int
    order_id: str


class ProcessVariables(BaseModel):
    order_id: str
    shop_url: str
    shop_id: str
    shop_api_url: str
    shop_bot_url: str
    user_order_info: NotificationPayloadModel
    admin_order_info: NotificationPayloadModel
    payment_info: (
        InvoiceTGMessageModel
        | InvoiceTONMessageModel
        | InvoiceWithPaymentLinkMessageModel
        | InvoiceWithPaymentLinkMessageModelLocal
        | None
    ) = None
    send_to_admin_dm: bool = False
    shop_language: str
