from pydantic import BaseModel

from shop_system_models.shop_api import MetaBaseModel


class ExtraOptionResponseModel(BaseModel):
    id: str
    name: str
    description: str = ""
    price: float = 0
    preview_url: list[str] = []


class ExtraOptionCategoriesResponseModel(MetaBaseModel):
    id: str
    name: str
    description: str = ""
    choice_count: int = 0  # How many options user can select from this category, 0 means no limit
    is_required: bool | None = (
        False  # If true, user must select at least one option from this category
    )
    options: list[ExtraOptionResponseModel] = []
