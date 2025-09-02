from enum import StrEnum
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from letschatty.models.base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from letschatty.models.utils.types.identifier import StrObjectId

class AttributeType(StrEnum):
    """This class represents the type of an item.
    It is used to represent the type of an item in a related asset or filter condition.
    """
    QUALITY_SCORE = "quality_score"
    BUSINESS_AREAS = "business_areas"
    FUNNELS = "funnels"
    PRODUCTS = "products"
    SALES = "sales"
    TAGS = "tags"
    SOURCES = "sources"
    FILTER_CRITERIA = "filter_criteria"


class Attribute(BaseModel):
    """This class is used to represent the id and type of an item.
    It is used to represent the id and type of an item in a related asset or filter condition.
    """
    attribute_id: StrObjectId | str = Field(frozen=True, description="The id of the item, could either be an object id if it's a chatty asset, or a string if it's a member of a string enum as quality score")
    attribute_type : AttributeType = Field(frozen=True, description="The type of the item")

    model_config = ConfigDict(
        extra = "ignore"
    )


class FilterCriteriaPreview(ChattyAssetPreview):
    """Preview of the filter criteria"""

    icon: Optional[str] = Field(default=None, description="The icon of the filter criteria")
    is_global: bool = Field(default=False, description="Whether the filter criteria is global")

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"icon": 1, "is_global": 1}

class FilterCriteria(CompanyAssetModel):
    """This class represents the combination of AND and OR filters.
    Inner arrays represent OR conditions, outer array represents AND conditions.
    Example: [[A, B], [C]] means (A OR B) AND (C)
    """
    name: str = Field(description="The name of the filter criteria")
    filters: List[List[Attribute]] = Field(default_factory=list)
    is_global: bool = Field(default=False, description="Whether the filter criteria is global")
    icon: str = Field(default="", description="The icon of the filter criteria")

    model_config = ConfigDict(
        extra = "ignore"
    )