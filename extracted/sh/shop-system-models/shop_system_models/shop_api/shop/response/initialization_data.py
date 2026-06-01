from typing import Optional

from pydantic import BaseModel

from shop_system_models.shop_api.bot.response import OrderStatusResponseModel
from shop_system_models.shop_api.links import LinkBlocksModel
from shop_system_models.shop_api.shop.response.orders import DeliveryTypeResponseModel
from shop_system_models.shop_api.shop.response.payment_methods import PaymentMethodDBResponseModel
from shop_system_models.shop_api.shop.response.users import UserResponseModel


class ContentDataResponseModel(BaseModel):
    blocks: LinkBlocksModel | None
    delivery_types: list[DeliveryTypeResponseModel] | None
    payment_methods: list[PaymentMethodDBResponseModel] | None


class InitializationDataResponseModel(ContentDataResponseModel):
    web_app_url: str
    user: UserResponseModel
    search_enabled: Optional[bool] = False
    orders_statuses: list[OrderStatusResponseModel] | None
