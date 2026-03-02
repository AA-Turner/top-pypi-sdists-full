import enum

from pydantic import BaseModel, field_validator

from shop_system_models.shop_api.shop.request.products import (
    ProductModel,
    SubmitProductCategoriesModel,
)
from shop_system_models.shop_api.shop.response.extra_product_options import (
    ExtraOptionCategoriesResponseModel,
)


class BaseProductResponseModel(ProductModel, SubmitProductCategoriesModel):
    id: str


class ProductCheckoutModes(enum.Enum):
    PAYMENT = "payment"
    BOOKING = "booking"


class ProductResponseModel(BaseProductResponseModel):
    extra_option_choice_required: bool = False
    extra_option_categories: list[ExtraOptionCategoriesResponseModel] = []
    related_products: list["ProductResponseModel"] | None = []
    secret_urls: list[str] = []
    checkout_modes: list[ProductCheckoutModes] = []

    @field_validator("checkout_modes")
    def convert_status(cls, value: list[ProductCheckoutModes]):
        return [v.value for v in value]


class PartialPaginationResponseModel(BaseModel):
    total_rows: int
    is_first_page: bool
    is_last_page: bool


class PaginationResponseModel(PartialPaginationResponseModel):
    page: int
    page_size: int


class ProductListResponseModel(BaseModel):
    products: list[ProductResponseModel]
    page_info: PaginationResponseModel
