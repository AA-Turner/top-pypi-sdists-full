from letschatty.models.utils.types.identifier import StrObjectId
from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from typing import Dict, Any, Optional, ClassVar
from pydantic import Field, field_validator, BaseModel
import pycountry
from datetime import datetime
from zoneinfo import ZoneInfo
import json

class ProductPreview(ChattyAssetPreview):
    color: str = Field(default="#000000")
    price: Optional[Dict[str, float]] = Field(default=None)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"color": 1, "description": 1, "price": 1}

    @classmethod
    def from_asset(cls, asset: 'Product') -> 'ProductPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            color=asset.color,
            updated_at=asset.updated_at
        )

class Product(CompanyAssetModel):
    name: str
    price: Optional[Dict[str, float]] = Field(default=None)
    parameters: Optional[Dict[str, Any]] = Field(default=None)
    external_id: Optional[str] = Field(default=None)
    preview_class: ClassVar[type[ProductPreview]] = ProductPreview
    color: str = Field(default="#000000")

    @field_validator('price', mode='before')
    def validate_price(cls, v: Dict[str, float]):
        if v is None:
            return v
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                # Handle Python dict string format (single quotes)
                import ast
                v = ast.literal_eval(v)
        for currency, amount in v.items():
            try:
                pycountry.currencies.get(alpha_3=currency)
            except KeyError:
                raise ValueError(f"Invalid currency code: {currency}. Must be a valid ISO 4217 currency code.")
            if amount < 0:
                raise ValueError(f"Price amount must be non-negative for currency {currency}")

        return v

class ProductToDelete(BaseModel):
    id: Optional[StrObjectId] = Field(default=None)
    company_id: StrObjectId
    external_id: Optional[str] = Field(default=None)
    deleted_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    class ConfigDict:
        arbitrary_types_allowed = True


