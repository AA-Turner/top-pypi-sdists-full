from enum import Enum

from pydantic import BaseModel

from shop_system_models.shop_api.shop.request.baskets import BasketModel, BasketModelV2
from shop_system_models.shop_api.shop.response.products import ProductResponseModel


class BasketResponseModel(BasketModel):
    id: str | None = None


class BasketResponseModelV2(BasketModelV2):
    id: str | None = None


class ProductsInBasket(ProductResponseModel):
    count_in_basket: int = 1


class UserBasketResponseModel(BasketResponseModel):
    products: list[ProductsInBasket] = []


class UserBasketResponseModelV2(BasketResponseModelV2):
    products: list[ProductsInBasket] = []


class ManageOrderAction(Enum):
    create = "create"
    delete = "delete"


class ManageBasketModel(BaseModel):
    message: str
    product_unique_id: str | None = None
    product: ProductResponseModel | None = None
