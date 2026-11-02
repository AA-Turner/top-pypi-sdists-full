from pydantic import Field
from typing import List
from letschatty.models.base_models.chatty_asset_model import ChattyAssetModel

class N8NAgentsInfo(ChattyAssetModel):
    """N8N agents info"""
    webhook_url: str = Field(..., description="N8N webhook URL")
    name : str = Field(..., description="N8N agent name")
    tools : List[str] = Field(..., description="N8N agent tools")