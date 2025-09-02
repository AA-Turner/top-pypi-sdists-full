
from typing import List, Any, Optional
from .chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from pydantic import Field
from ..utils.types.identifier import StrObjectId
from datetime import datetime
from enum import StrEnum

class AiAgentComponentType(StrEnum):
    """Type of the ai agent component"""
    FOLLOW_UP_STRATEGY = "follow_up_strategy"
    CONTEXT = "context"
    CHAT_EXAMPLE = "chat_example"
    FAQ = "faq"

class AiAgentComponentPreview(ChattyAssetPreview):
    """Preview of the AiAgentComponent"""
    start_time: Optional[datetime] = Field(default=None, description="The start time of the component")
    end_time: Optional[datetime] = Field(default=None, description="The end time of the component")
    is_essential: Optional[bool] = Field(default=None, description="Whether the component is essential for the ai agent to work")
    type: AiAgentComponentType = Field(description="The type of the component")
    filter_criteria: List[StrObjectId] = Field(default_factory=list, description="The assets that are related to the component")
    icon: Optional[str] = Field(default=None, description="The icon of the component")

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"type": 1, "start_time": 1, "end_time": 1, "is_essential": 1, "type": 1, "icon": 1, "filter_criteria": 1}

    @classmethod
    def from_asset(cls, asset: 'AiAgentComponent') -> 'ChattyAssetPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            type=asset.type,
            icon=asset.icon,
            filter_criteria=asset.filter_criteria,
            start_time=asset.start_time,
            end_time=asset.end_time,
            is_essential=asset.is_essential
        )


class AiAgentComponent(CompanyAssetModel):
    """Protocol for models that have related chatty assets"""
    name: str = Field(description="The name of the component")
    type: AiAgentComponentType = Field(description="The type of the component")
    filter_criteria: List[StrObjectId] = Field(default_factory=list, description="The assets that are related to the component")
    start_time: Optional[datetime] = Field(default=None, description="The start time of the component")
    end_time: Optional[datetime] = Field(default=None, description="The end time of the component")
    is_essential: Optional[bool] = Field(default=False, description="Whether the component is essential for the ai agent to work")
    icon: Optional[str] = Field(default=None, description="The icon of the component")

    def has_conditional_filters(self) -> bool:
        """Check if the model has assets restrictions"""
        return len(self.filter_criteria) > 0

    def is_always_on(self) -> bool:
        """Check if the model is always on"""
        return len(self.filter_criteria) == 0