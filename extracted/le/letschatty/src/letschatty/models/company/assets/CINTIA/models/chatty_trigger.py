"""ChattyTrigger — a reusable trigger phrase linked to one or more company assets."""

from datetime import datetime
from typing import List, Optional

from letschatty.models.company.assets.company_assets import CompanyAssetType
from letschatty.models.utils.types.identifier import StrObjectId
from pydantic import BaseModel, Field


class AssetReference(BaseModel):
    id: str
    type: CompanyAssetType


class ChattyTrigger(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    company_id: StrObjectId
    ai_agent_id: Optional[str] = None
    name: str
    phrase: str
    embedding: Optional[List[float]] = None
    assets: List[AssetReference]
    embedded_at: Optional[datetime] = None

    model_config = {"populate_by_name": True}
