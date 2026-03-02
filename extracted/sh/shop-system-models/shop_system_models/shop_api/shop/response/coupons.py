import datetime

from pydantic import BaseModel

from shop_system_models.shop_api.shop.request.coupons import CouponModel
from shop_system_models.shop_api.shop.response.products import PartialPaginationResponseModel


class CouponResponseModel(CouponModel):
    id: str
    created_at: datetime.datetime


class CouponListResponseModel(BaseModel):
    coupons: list[CouponResponseModel]
    page_info: PartialPaginationResponseModel
