from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from shop_system_models.shop_api import MetaBaseModel
from shop_system_models.shop_api.shared import ImageMetadata


class ExtraAttribute(BaseModel):
    name: str
    description: str


class SubmitProductModel(MetaBaseModel):
    name: str
    description: str = ""
    price: float
    final_price: float = 0
    currency: str
    preview_url: list[str] = []
    stock_qty: int
    orders_qty: int = 0
    extra_attributes: list[ExtraAttribute] = []


class SubmitProductCategoriesModel(MetaBaseModel):
    category: list[int]


class ProductModel(SubmitProductModel):
    created: datetime = datetime.fromtimestamp(0)
    updated: datetime = datetime.fromtimestamp(0)
    images: List[ImageMetadata] = []

    @field_validator("final_price", mode="before")
    def set_final_price(cls, value, values: ValidationInfo):
        if not value:
            return values.data.get("price")
        return value
