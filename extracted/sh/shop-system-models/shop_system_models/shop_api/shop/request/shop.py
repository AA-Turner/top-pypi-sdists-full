from typing import Any, Dict, List, Optional

from pydantic import Field, validator

from shop_system_models.shop_api import MetaBaseModel


class ShopCreateRequest(MetaBaseModel):
    """Request model for shop creation."""

    name: str
    description: Optional[str] = None
    owner_id: str
    categories: List[str] = Field(default_factory=list)

    @validator("name")
    def validate_name(self, v):
        if not v.strip():
            raise ValueError("Shop name cannot be empty")
        return v


class ShopUpdateRequest(MetaBaseModel):
    """Request model for shop update."""

    shop_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    settings: Optional[Dict[str, Any]] = None
