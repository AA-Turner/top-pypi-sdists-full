"""ChattyAssetEmbedding — persisted vector embedding for a company asset."""

from datetime import datetime
from typing import List, Optional

from letschatty.models.company.assets.company_assets import CompanyAssetType
from letschatty.models.utils.types.identifier import StrObjectId
from pydantic import BaseModel, Field


class ChattyAssetEmbedding(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    asset_id: StrObjectId
    asset_type: CompanyAssetType
    embedded_at: datetime
    embedding: List[float]
    company_id: StrObjectId

    model_config = {"populate_by_name": True}
