from typing import List

from pydantic import BaseModel

from shop_system_models.shop_api.shop.request.orders import DeliveryTypeModel, OrderModel
from shop_system_models.shop_api.shop.response.products import PaginationResponseModel


class OrderResponseModel(OrderModel):
    """Response model for a single order."""

    id: str


class OrderListResponseModel(BaseModel):
    """Response model for a list of orders."""

    orders: List[OrderResponseModel]
    page_info: PaginationResponseModel


class DeliveryTypeResponseModel(DeliveryTypeModel):
    """Response model for a delivery type."""

    id: str
