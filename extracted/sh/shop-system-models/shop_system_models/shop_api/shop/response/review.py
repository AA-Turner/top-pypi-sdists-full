from pydantic import BaseModel

from shop_system_models.shop_api.shop.request.review import ReviewModel
from shop_system_models.shop_api.shop.response.products import PaginationResponseModel
from shop_system_models.shop_api.shop.response.users import UserResponseModel


class ReviewResponseModel(ReviewModel):
    id: str
    user: UserResponseModel | None = None


class ReviewListResponseModel(BaseModel):
    reviews: list[ReviewResponseModel]
    page_info: PaginationResponseModel
