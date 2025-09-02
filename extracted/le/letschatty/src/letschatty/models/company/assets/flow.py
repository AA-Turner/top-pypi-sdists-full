from pydantic import BaseModel
from typing import Dict, Any
from ...base_models.chatty_asset_model import CompanyAssetModel
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import Field
import logging
from letschatty.models.utils import StrObjectId
logger = logging.getLogger("logger")

class FlowPreview(CompanyAssetModel):
    """This class is only used to preview the workflow. It is not used to create or update the flow."""
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    company_id: StrObjectId = Field(alias="companyId")
    visible: bool = Field(default=True)

    @property
    def is_smart_follow_up(self) -> bool:
        """Check if the flow is a smart follow up"""
        return self.title.lower() == "smart follow up"

    @classmethod
    def default_create_instance_method(cls, dict_data: Dict[str, Any]) -> 'FlowPreview':

        return cls(created_at=dict_data.get("created_at", datetime.now(tz=ZoneInfo("UTC"))), updated_at=dict_data.get("updated_at", datetime.now(tz=ZoneInfo("UTC"))), **dict_data)