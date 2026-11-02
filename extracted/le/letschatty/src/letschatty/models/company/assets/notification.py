from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from pydantic import Field, field_validator
from typing import Optional, Any, ClassVar, Literal
from ...utils.types import StrObjectId
from datetime import datetime
from enum import Enum


class NotificationLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# Global company ID constant - notifications with this company_id are global
GLOBAL_COMPANY_ID = "000000000000000000000000"


class NotificationPreview(ChattyAssetPreview):
    level: NotificationLevel = Field(default=NotificationLevel.INFO)
    title: str
    dismissed: bool = Field(default=False)
    account_id: Optional[StrObjectId] = None

    @field_validator("account_id", mode="before")
    @classmethod
    def _blank_account_is_none(cls, value):
        """`StrObjectId` rejects the empty string."""
        return value or None

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"level": 1, "title": 1, "dismissed": 1, "account_id": 1}

    @classmethod
    def from_asset(cls, asset: 'Notification') -> 'NotificationPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            level=asset.level,
            title=asset.title,
            dismissed=asset.dismissed,
            account_id=asset.account_id,
            deleted_at=asset.deleted_at
        )


class Notification(CompanyAssetModel):
    name: str = Field(description="Internal name for the notification")
    title: str = Field(description="Display title of the notification")
    description: str = Field(description="Detailed description/content of the notification")
    level: NotificationLevel = Field(default=NotificationLevel.INFO, description="Notification level: info, warning, or error")
    dismissed: bool = Field(default=False, description="User dismissed/closed the notification")
    dismissed_at: Optional[datetime] = Field(default=None, description="UTC time the notification was dismissed")
    account_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "The WhatsApp account (number) this notification is about (a connection or payment problem of one "
            "number). Absent = company-wide, visible to every user. A user limited to some accounts only sees the "
            "notifications of their accounts plus the company-wide ones."
        ),
    )
    preview_class: ClassVar[type[NotificationPreview]] = NotificationPreview

    @field_validator("account_id", mode="before")
    @classmethod
    def _blank_account_is_none(cls, value):
        """`StrObjectId` rejects the empty string."""
        return value or None

    @property
    def is_global(self) -> bool:
        """Check if this notification is global (applies to all companies)"""
        return self.company_id == GLOBAL_COMPANY_ID
