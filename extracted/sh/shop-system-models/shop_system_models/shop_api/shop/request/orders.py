from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from shop_system_models.shop_api import MetaBaseModel
from shop_system_models.shop_api.shop.response.baskets import UserBasketResponseModelV2
from shop_system_models.shop_api.shop.response.products import ProductResponseModel


class ExtraFieldPayload(MetaBaseModel):
    """Model for extra field data in orders."""

    name: str
    value: str


class OrderDeliveryTypeModel(BaseModel):
    """Model for order delivery details."""

    name: str
    address: Optional[str] = ""
    amount: Optional[float] = 0.0
    extra_fields_payload: Optional[List[ExtraFieldPayload]] = Field(default_factory=lambda: [])


class Coordinates(MetaBaseModel):
    """Geographic coordinates."""

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AddressModel(MetaBaseModel):
    """Address model with optional coordinates."""

    coordinates: Optional[Coordinates] = None
    address: Optional[str] = None


class ExtraField(MetaBaseModel):
    """Model for defining extra fields."""

    name: str
    description: str
    is_required: Optional[bool] = None


class DeliveryTypeModel(MetaBaseModel):
    """Delivery type configuration model."""

    name: str
    amount: float = 0.0
    is_address_required: Optional[bool] = False
    address_hint: Optional[str] = ""
    extra_fields: List[ExtraField] = Field(default_factory=list)
    is_timepicker_required: bool = False
    details: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None  # ISO format, ex.: RU, KZ, BY...
    city: Optional[str] = None
    delivery_location: Optional[Coordinates] = None
    delivery_radius: Optional[int] = None
    delivery_min_hour: Optional[int] = None
    delivery_max_hour: Optional[int] = None
    delivery_minutes_interval: Optional[int] = None
    delivery_min_day: Optional[int] = None
    delivery_max_day: Optional[int] = None


class BookingOrderModel(MetaBaseModel):
    """Details for a booking order."""

    booking_id: str
    from_date: datetime
    till_date: datetime
    item_id: str


class CreateOrderModel(MetaBaseModel):
    """Model for creating a new order."""

    delivery: Optional[OrderDeliveryTypeModel] = None
    delivery_date_from: datetime = Field(default_factory=lambda: datetime.now())
    comment: Optional[str] = None
    user_contact_number: Optional[str] = None
    payment_type_id: Optional[str] = None
    booking_details: Optional[BookingOrderModel] = None
    preview_url: Optional[str] = ""


class ProductsInBasket(ProductResponseModel):
    count_in_basket: int = 1


class OrderPaymentDetails(BaseModel):
    title: str
    description: str
    expires_at: datetime
    link: str


# This depends on UserBasketResponseModelV2 which we'll define in a separate file
# For now, we'll create a placeholder class that can be updated later
class OrderModel(CreateOrderModel):
    """Complete order model."""

    basket: UserBasketResponseModelV2  # This will be implemented in basket models
    user_id: Optional[str] = None
    basket_id: Optional[str] = None
    status: Optional[str] = None
    client_coordinates: Optional[AddressModel] = None
    created: datetime = Field(default_factory=lambda: datetime.now())
    updated: datetime = Field(default_factory=lambda: datetime.now())
    order_number: str = "#0001"
    process_key: Optional[int] = None
    coupon: Optional[str] = None
    admin_message_id: str | None = None
    payment_data: OrderPaymentDetails | None = None


class LabeledPrice(BaseModel):
    label: str
    amount: int


class InvoiceBaseModel(BaseModel):
    chat_id: int
    order_id: str
    order_number: str  # order_number
    payload: str  # <basket_id>_<order_id>_<order_number> from OrderResponseModel --> its subscription key
    amount: float
    currency: str  # fiat
    payment_address: str
    payment_timeout: int | None = None


class InvoiceTGMessageModel(InvoiceBaseModel):
    description: str  # order_products
    provider_data: str | None = None
    prices: list[LabeledPrice]  # label and amount in coins!
    need_name: bool | None = False
    need_phone_number: bool | None = False
    need_email: bool | None = False
    send_phone_number_to_provider: bool | None = False
    send_email_to_provider: bool | None = False
    is_flexible: bool | None = False
    reply_markup: bool | None = None


class InvoiceWithPaymentLinkMessageModel(InvoiceBaseModel):
    payment_link: str


class InvoiceTONMessageModel(InvoiceBaseModel):
    approved_addresses: list[str] = []
    ton_amount: float


class PaidContentMessage(BaseModel):
    message: str
