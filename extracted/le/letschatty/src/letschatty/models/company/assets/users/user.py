from __future__ import annotations
from typing import Optional, List, Any, ClassVar, Dict
from datetime import datetime
from zoneinfo import ZoneInfo
from letschatty.models.utils import StrObjectId
from pydantic import BaseModel, Field, model_validator, field_validator
from enum import StrEnum
from ....base_models import CompanyAssetModel, ChattyAssetPreview
from ...notifications.notification import Notification, WhatsAppNotifications
from .user_asset_permission import AssetPermission, AgentBusinessAreaAssignment, FunnelAssignment, Permission
from letschatty.models.company.home_widget import HomeWidget
from .permissions import Module, effective_permission as _effective_permission, can as _can
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

class CurrentChatAPBMode(BaseModel):
    chat_id  : StrObjectId = Field(default=None)
    last_activity : datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))

    @classmethod
    def for_chat_id(cls, chat_id:StrObjectId) -> CurrentChatAPBMode:
        return cls(chat_id=chat_id)


class UserPreview(ChattyAssetPreview):
    status: UserStatus
    last_activity_timestamp: datetime
    photo_url: str = Field(default="https://files-chatty.s3.us-east-1.amazonaws.com/Disen%CC%83o+sin+ti%CC%81tulo.png")
    roles: List[UserRole]
    user_type : UserType
    email : Optional[str] = Field(default=None)
    auto_assign_chats: bool = Field(default=False)
    account_ids: Optional[List[StrObjectId]] = Field(default=None, description="WhatsApp accounts this user is limited to; None = all of them (see User.account_ids)")

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
            auto_assign_chats=False
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
        projection["auto_assign_chats"] = 1
        projection["account_ids"] = 1
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
            updated_at=asset.updated_at,
            auto_assign_chats=asset.auto_assign_chats,
            account_ids=asset.account_ids
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
    current_chat_apb_mode : Optional[CurrentChatAPBMode] = Field(default=None, description="The current apb mode for the chat")

    # Status and activity
    status: UserStatus = Field(default=UserStatus.ONLINE)
    last_activity_timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))

    # Roles and permissions
    roles: List[UserRole]
    is_root: bool = Field(default=False, description="If true, root user can't be deleted and has super admin powers")

    # Asset permissions (applies to all users)
    asset_permissions: List[AssetPermission] = Field(default_factory=list, description="Asset permissions for the user")

    # Per-module permission overrides (the "capability flags" layer). Empty for
    # almost every user — the role defaults in ROLE_DEFAULTS apply. When an entry
    # is present it REPLACES the role default for that module (up or down). This is
    # a NEW additive field and does not touch the legacy `asset_permissions`.
    module_permission_overrides: Dict[Module, Permission] = Field(default_factory=dict, description="Per-user, per-module permission overrides that replace the role default")

    # Notifications
    notifications: List[Notification] = Field(default_factory=list)
    whatsapp_notification: WhatsAppNotifications = Field(default_factory=WhatsAppNotifications.default)

    # Agent specific fields
    business_areas: List[AgentBusinessAreaAssignment] = Field(default_factory=list)
    funnels: List[FunnelAssignment] = Field(default_factory=list)
    auto_assign_chats: bool = Field(default=False)
    preview_class: ClassVar[type[UserPreview]] = UserPreview

    # WhatsApp accounts (numbers) this user may work with. Written ONLY by the admin endpoint
    # `PUT /company_workspace/{id}/users/{user_id}/accounts`; never by the self-service user update
    # (`UserUpdateInfo` has no such field), so nobody can widen their own access.
    account_ids: Optional[List[StrObjectId]] = Field(
        default=None,
        description="None (or absent) = all the company's accounts. A list = limited to those accounts. "
                    "An empty list is never written (the endpoint rejects it); if one is found in the data it "
                    "reads as 'no account at all' (fail-closed), never as 'all'. Ignored for the Owner "
                    "(root/super_admin), mega admins and copilot: see `restricted_to_accounts`.",
    )

    # Home layout (frontend 'inicio por rol', spec 2026-10-01)
    home_layout: Optional[List[HomeWidget]] = Field(default=None, description="El inicio que armó el usuario; None = el de su rol")

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

    @property
    def exempt_from_account_limit(self) -> bool:
        """The Owner (root / super_admin), mega admins and copilot always work with every account."""
        return self.is_super_admin or self.is_mega_admin or self.is_copilot

    @property
    def restricted_to_accounts(self) -> bool:
        """True when this user is limited to some accounts. `isinstance(list)` on purpose, not truthiness:
        `[]` is a limit (to nothing) and a MagicMock attribute is not one."""
        return isinstance(self.account_ids, list) and not self.exempt_from_account_limit

    def can_access_account(self, account_id: Optional[str]) -> bool:
        """May this user work with a chat of `account_id`? A chat with no account (`None`) is NOT visible to
        a limited user here: the caller resolves 'no account = the default one' first (see
        `services/whatsapp_accounts/account_floor.py`, the single place that does)."""
        if not self.restricted_to_accounts:
            return True
        return account_id is not None and account_id in (self.account_ids or [])

    def effective_permission(self, module: Module) -> Permission:
        """This user's effective permission on a module (role defaults + overrides)."""
        return _effective_permission(
            [role.value for role in self.roles],
            module,
            self.module_permission_overrides,
            self.is_mega_admin,
        )

    def can(self, module: Module, required: Permission) -> bool:
        """True if this user may perform an action requiring ``required`` on ``module``."""
        return _can(
            [role.value for role in self.roles],
            module,
            required,
            self.module_permission_overrides,
            self.is_mega_admin,
        )


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