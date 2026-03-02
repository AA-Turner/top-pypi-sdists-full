from pydantic import BaseModel

from shop_system_models.shop_api.shop.request.categories import CategoryModel
from shop_system_models.shop_api.shop.response.products import (
    PaginationResponseModel,
    ProductListResponseModel,
    ProductResponseModel,
)


class CategoryResponseModel(CategoryModel):
    id: int


class SubcatsProdsResponseModel(BaseModel):
    subcategories: list[CategoryResponseModel]
    products: list[ProductResponseModel]


class MainCatIncredProdResponseModel(BaseModel):
    categories: list[CategoryResponseModel]
    products: list[ProductResponseModel]


class CategoryListResponseModel(BaseModel):
    categories: list[CategoryResponseModel]
    page_info: PaginationResponseModel


class CategoriesProductsResponseModel(BaseModel):
    categories: CategoryListResponseModel
    products: ProductListResponseModel
