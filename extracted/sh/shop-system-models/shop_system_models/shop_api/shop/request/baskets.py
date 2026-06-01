from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel
from typing_extensions import Doc


class DBProductInBasket(BaseModel):
    id: str  # ID продукта
    count: int  # его кол-во


class BasketModel(BaseModel):
    user_id: str | None = None  # Not uses in request
    order_id: str | None = None  # Not uses in request
    products_id: list[DBProductInBasket] = []
    amount: float | None = 0  # Not uses in request
    preview_url: str = ""


class DBProductInBasketV2(BaseModel):
    id: str  # product ID
    unique_id: str  # unique product ID in the basket, used it for product deleting
    extra_option_ids: list[str] = []


class BasketModelV2(BaseModel):
    user_id: str | None = None
    order_id: str | None = None
    products_id: list[DBProductInBasketV2] = []
    coupon: str | None = None
    coupon_discount: Annotated[
        float, Doc("The amount of discount from attached coupon, if any.")
    ] = 0
    amount: Annotated[float, Ge(0)] = 0  # this amount already includes discount
    preview_url: str = ""


class CouponInputData(BaseModel):
    code: str
