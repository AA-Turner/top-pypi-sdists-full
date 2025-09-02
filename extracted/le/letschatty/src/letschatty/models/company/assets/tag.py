from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from pydantic import Field
from typing import Optional, Any, ClassVar
from pydantic import BaseModel
from ...utils.types import StrObjectId
from datetime import datetime
from zoneinfo import ZoneInfo

class TagPreview(ChattyAssetPreview):
    color: str = Field(default="#000000")

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"color": 1}

    @classmethod
    def from_asset(cls, asset: 'Tag') -> 'TagPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            color=asset.color,
            updated_at=asset.updated_at
        )

class Tag(CompanyAssetModel):
    name: str
    description: str
    color: str
    is_event: bool
    event_name: Optional[str] = Field(default=None)
    preview_class: ClassVar[type[TagPreview]] = TagPreview

