from ..base_models.chatty_asset_model import ChattyAssetModel
from ..utils.types import StrObjectId
from pydantic import BaseModel, Field
from typing import Optional
from ..utils.types import MessageSubtype

class Highlight(ChattyAssetModel):
    creator_id: StrObjectId
    title: str
    description: str
    starred: bool
    subtype : MessageSubtype

class HighlightRequestData(BaseModel):
    title: str
    description: str
    starred: bool = Field(default=False)
    subtype : MessageSubtype = Field(frozen=True, default=MessageSubtype.USER_NOTE)
