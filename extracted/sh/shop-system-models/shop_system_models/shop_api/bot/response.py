from pydantic import BaseModel

from shop_system_models.shop_api.bot.request import OrderStatusModel


class OrderStatusResponseModel(OrderStatusModel):
    id: str


class OrderStatusResponseModelWithShopName(BaseModel):
    shop_name: str
    order_statuses: list[OrderStatusResponseModel]
