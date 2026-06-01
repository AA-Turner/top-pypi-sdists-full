from typing import List

from pydantic import BaseModel, Field, field_validator

from shop_system_models.shop_api.shared import ImageMetadata


class SubmitParentCategoryModel(BaseModel):
    parent_category: list[int] = Field(default_factory=list)


class SubmitCategoryModel(BaseModel):
    name: str
    preview_url: str = ""

    @field_validator("name", mode="before")
    def name_validation(cls, value):
        if not value:
            raise ValueError("Name cannot be an empty string.")
        return value


class CategoryModel(SubmitCategoryModel, SubmitParentCategoryModel):
    images: List[ImageMetadata] = []
