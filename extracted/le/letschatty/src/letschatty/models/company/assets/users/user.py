from typing import Optional, List, Any, ClassVar, Dict
from datetime import datetime
from zoneinfo import ZoneInfo
from letschatty.models.utils import StrObjectId
from pydantic import BaseModel, Field, model_validator, field_validator
from enum import StrEnum
from ....base_models import CompanyAssetModel, ChattyAssetPreview
from ...notifications.notification import Notification, WhatsAppNotifications
from .user_asset_permission import AssetPermission, AgentBusinessAreaAssignment, FunnelAssignment
import logging
logger = logging.getLogger("User")

class UserRole(StrEnum):
    AGENT = "agent"           # Can handle chats at a specific business area and funnel
    SUPER_AGENT = "super_agent" # Can handle chats at any business area and funnel
    OVERVIEWER = "overviewer" # Can view all company assets
    MARKETER = "marketer"     # Can manage certain assets
    ADMIN = "admin"           # Can administer users and assets
    SUPER_ADMIN = "super_admin" # Can administer everything
    COPILOT = "copilot" #It's a super agent for all companies
    MEGA_ADMIN = "mega_admin" #Can administer everything in all companies

    @classmethod
    def get_all_roles(cls) -> List["UserRole"]:
        return [
            UserRole.AGENT,
            UserRole.SUPER_AGENT,
            UserRole.OVERVIEWER,
            UserRole.MARKETER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        ]

    @classmethod
    def get_roles_and_description(cls) -> Dict["UserRole", str]:
        return {
            UserRole.AGENT: "Can act on chats at a specific business area and funnel",
            UserRole.SUPER_AGENT: "Can handle chats at any business area and funnel and view other agents' chats",
            UserRole.OVERVIEWER: "Can view all company assets, no edit.",
            UserRole.MARKETER: "Can manage certain assets, like sources and topics",
            UserRole.ADMIN: "Can administer users and assets",
            UserRole.SUPER_ADMIN: "Can administer everything"
        }

class UserType(StrEnum):
    HUMAN = "human"
    INTEGRATION = "integration"

    @classmethod
    def get_all_types(cls) -> List["UserType"]:
        return [
            UserType.HUMAN,
            UserType.INTEGRATION
        ]

class UserStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"

class UserPreview(ChattyAssetPreview):
    status: UserStatus
    last_activity_timestamp: datetime
    photo_url: str = Field(default="https://files-chatty.s3.us-east-1.amazonaws.com/Disen%CC%83o+sin+ti%CC%81tulo.png")
    roles: List[UserRole]
    user_type : UserType
    email : Optional[str] = Field(default=None)

    @classmethod
    def not_found(cls, id: StrObjectId, company_id: StrObjectId) -> 'UserPreview':
        #if id is not a valid object id, we return a not found preview
        return cls(
            _id=id,
            name=f"Not found {id}",
            company_id=company_id,
            created_at=datetime.now(tz=ZoneInfo("UTC")),
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
            status=UserStatus.OFFLINE,
            last_activity_timestamp=datetime.now(tz=ZoneInfo("UTC")),
            photo_url="https://files-chatty.s3.us-east-1.amazonaws.com/Disen%CC%83o+sin+ti%CC%81tulo.png",
            roles=[],
            user_type=UserType.HUMAN,
        )

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        projection = super().get_projection()
        projection["status"] = 1
        projection["last_activity_timestamp"] = 1
        projection["photo_url"] = 1
        projection["roles"] = 1
        projection["email"] = 1
        projection["user_type"] = 1
        projection["api_key_expires_at"] = 1
        return projection

    @classmethod
    def from_asset(cls, asset: 'User') -> 'UserPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            status=asset.status,
            last_activity_timestamp=asset.last_activity_timestamp,
            photo_url=asset.photo_url,
            roles=asset.roles,
            user_type=asset.user_type,
            email=asset.email,
            updated_at=asset.updated_at
        )

class User(CompanyAssetModel):
    """
    Unified user model combining multiple possible roles.
    Different fields become relevant based on the roles a user has.
    """
    # Basic info
    user_type: UserType = Field(default=UserType.HUMAN)
    name: str
    email: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    photo_url: str = Field(default="https://files-chatty.s3.us-east-1.amazonaws.com/Disen%CC%83o+sin+ti%CC%81tulo.png")

    # Status and activity
    status: UserStatus = Field(default=UserStatus.ONLINE)
    last_activity_timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))

    # Roles and permissions
    roles: List[UserRole]
    is_root: bool = Field(default=False, description="If true, root user can't be deleted and has super admin powers")

    # Asset permissions (applies to all users)
    asset_permissions: List[AssetPermission] = Field(default_factory=list, description="Asset permissions for the user")

    # Notifications
    notifications: List[Notification] = Field(default_factory=list)
    whatsapp_notification: WhatsAppNotifications = Field(default_factory=WhatsAppNotifications.default)

    # Agent specific fields
    business_areas: List[AgentBusinessAreaAssignment] = Field(default_factory=list)
    funnels: List[FunnelAssignment] = Field(default_factory=list)
    auto_assign_chats: bool = Field(default=False)
    preview_class: ClassVar[type[UserPreview]] = UserPreview

    # API key fields
    api_key_hash: Optional[str] = Field(default=None)  # Stored hashed, not plaintext
    api_key_created_at: Optional[datetime] = Field(default=None)
    api_key_expires_at: Optional[datetime] = Field(default=None)
    api_key_last_used_at: Optional[datetime] = Field(default=None)
    api_key_description: Optional[str] = Field(default=None)

    @property
    def is_copilot(self) -> bool:
        return UserRole.COPILOT in self.roles

    @property
    def is_mega_admin(self) -> bool:
        return UserRole.MEGA_ADMIN in self.roles and self.company_id == "000000000000000000000000"

    @property
    def is_admin(self) -> bool:
        return UserRole.ADMIN in self.roles or UserRole.SUPER_ADMIN in self.roles or self.is_root

    @property
    def is_super_admin(self) -> bool:
        return UserRole.SUPER_ADMIN in self.roles or self.is_root

    @property
    def is_agent(self) -> bool:
        return UserRole.AGENT in self.roles

    @property
    def is_marketer(self) -> bool:
        return UserRole.MARKETER in self.roles

    @property
    def is_overviewer(self) -> bool:
        return UserRole.OVERVIEWER in self.roles

    @property
    def is_integration(self) -> bool:
        return self.user_type == UserType.INTEGRATION

    @property
    def is_super_agent(self) -> bool:
        return UserRole.SUPER_AGENT in self.roles

    @property
    def can_see_all_agents_chats(self) -> bool:
        return self.is_overviewer or self.is_super_admin or self.is_admin or self.is_super_agent


    @model_validator(mode="before")
    @classmethod
    def validate_email(cls, data: Any) -> Any:
        if data.get("user_type") == UserType.HUMAN and not data.get("email"):
            raise ValueError("Email is required for human users")
        return data

    @field_validator("api_key_expires_at", mode="after")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v is None:
            return v
        return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))

    @model_validator(mode="before")
    @classmethod
    def ensure_mail_if_human(cls, data: Any) -> Any:
        logger.debug(f"Ensuring email for human user: {data}")
        if data.get("user_type") == UserType.HUMAN and not data.get("email"):
            raise ValueError("Email is required for human users")
        elif not data.get("user_type") and not data.get("email"):
            raise ValueError("Email is required for human users")
        return data

    @model_validator(mode="before")
    @classmethod
    def ensure_roles(cls, data: Any) -> Any:
        logger.debug(f"Ensuring roles for user: {data}")
        if not data.get("roles"):
            raise ValueError("At least one role is required")
        return data

class UserUpdateInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    photo_url: Optional[str] = None
    notifications: Optional[List[Notification]] = None
    auto_assign_chats: Optional[bool] = None