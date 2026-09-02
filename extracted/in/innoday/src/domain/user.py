from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.container_execution import ContainerExecution
    from src.domain.organization import Organization, OrganizationMembership
    from src.domain.ticket import Ticket


class UserRole(str, Enum):
    """User role for access control and permissions."""

    MEMBER = "MEMBER"
    DEVELOPER = "DEVELOPER"
    ADMIN = "ADMIN"


class User(TimestampMixin, table=True):
    """
    User model for InnoDay platform with secure profile management.

    This model represents user accounts in the InnoDay system and manages:
    - Basic profile information (email, username, full name, etc.)
    - Integration status with external services (GitHub, Trello, Jira)
    - User preferences and settings stored as JSON
    - Relationships to tickets (created and assigned)
    - Default client association for multi-tenant support

    INTEGRATION NOTES FOR CLI ONBOARDING:
    ====================================

    1. TOKEN STORAGE EXPECTATIONS:
       - This model does NOT store sensitive tokens/API keys
       - CLI integration should use external secure token storage
       - Integration status fields only track connection state and metadata
       - Expected CLI integration pattern:
         a) CLI stores tokens securely (keyring, encrypted files, etc.)
         b) CLI calls PUT /api/v1/users/{id}/integrations to update connection status
         c) Agent uses this status to determine available integrations per user

    2. CLI ONBOARDING WORKFLOW INTEGRATION POINTS:
       - POST /api/v1/users: Create initial user profile from CLI
       - PUT /api/v1/users/{id}/integrations: Update service connections
       - GET /api/v1/users/{id}: Retrieve profile for CLI display
       - Preferences fields can store CLI-specific settings as JSON

    3. AGENT INTEGRATION EXPECTATIONS:
       - Agent should check user.github_connected before GitHub operations
       - Agent should use user.jira_instance_url for Jira API calls
       - Agent can store user-specific AI preferences in ui_preferences JSON
       - Agent should update user.last_login_at for session tracking

    4. SECURITY DESIGN:
       - No passwords stored (assumes external auth like OAuth, LDAP, etc.)
       - Integration tokens stored outside this model (CLI responsibility)
       - Only connection status and public metadata stored here
       - All API responses exclude sensitive data via UserResponse model
    """

    __tablename__ = "users"

    # Identity
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=100)

    # Supabase Auth linkage (the IdP's auth.users id == the JWT `sub` claim).
    # Nullable during the auth migration so pre-existing header-only users still
    # resolve; populated on first authenticated login (lazy mirror). This becomes
    # the real identity key once Supabase JWT auth is the norm. NOT the primary
    # key -- we keep our own UUID `id` and reference the IdP id here.
    supabase_user_id: Optional[str] = Field(
        default=None,
        unique=True,
        index=True,
        max_length=255,
        description="Supabase auth.users id (JWT sub). Null until first login.",
    )

    # When the IdP confirmed the user controls this email address (mirrors
    # Supabase's auth.users.email_confirmed_at). NULL = never verified, which is
    # the honest state for every user created before the invite flow existed.
    # A CLI token belonging to an unverified user must not authenticate -- see
    # src/middleware/token_auth.py.
    email_verified_at: Optional[datetime] = Field(
        default=None,
        description="When the IdP confirmed this email. Null until verified.",
    )

    # The user's default/home organization -- set during registration/onboarding
    # to the org they created or joined. Previously queried by license_utils but
    # never defined on the model (latent AttributeError); added here.
    default_organization_id: Optional[str] = Field(
        default=None,
        foreign_key="organizations.id",
        index=True,
        description="The user's primary organization (set at registration).",
    )

    # Profile Information
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    bio: Optional[str] = Field(default=None, max_length=1000)
    timezone: str = Field(default="UTC", max_length=50)
    language: str = Field(default="en", max_length=10)

    # Team member information (merged from Teammate model)
    # NOTE: first_name and last_name are kept for display name logic
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)

    # Access control and permissions
    role: UserRole = Field(default=UserRole.MEMBER)

    # Platform member flag (Phase 1: Deprecate Client Concept)
    is_platform_member: bool = Field(
        default=False, description="Platform employee with cross-organization access"
    )

    # Preferences (stored as JSON)
    notification_preferences: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON)
    )
    ui_preferences: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Organization memberships replace the deprecated client association

    # Integration Status (non-sensitive metadata only)
    github_connected: bool = Field(default=False)
    github_username: Optional[str] = Field(default=None, max_length=100)
    jira_connected: bool = Field(default=False)
    jira_instance_url: Optional[str] = Field(default=None, max_length=500)
    jira_email: Optional[str] = Field(default=None, max_length=255)

    # Developer License (Bring Your Own License - BYOL)
    # NOTE: Claude license keys/tokens are stored in initialization config, NOT in database
    # Developers must configure their Claude API keys in the deployment configuration
    # The system will validate licenses at runtime via external API calls

    last_login_at: Optional[datetime] = Field(default=None)

    # Relationships
    organization_memberships: List["OrganizationMembership"] = Relationship(
        back_populates="user"
    )
    tickets_created: List["Ticket"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.created_by]"},
    )
    tickets_assigned: List["Ticket"] = Relationship(
        back_populates="assignee_user",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to]"},
    )
    container_executions: List["ContainerExecution"] = Relationship(
        back_populates="user"
    )

    def update_last_login(self) -> None:
        """Update the last login timestamp"""
        self.last_login_at = datetime.now(timezone.utc)

    def update_integration_status(
        self,
        service: str,
        connected: bool,
        username: Optional[str] = None,
        instance_url: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        """
        Update integration connection status for external services.

        This method is called by both CLI and API endpoints to track which
        external services are connected for this user. It does NOT store
        sensitive tokens - those should be managed by the CLI/calling system.

        CLI Integration Notes:
        - CLI should call this after successfully connecting to a service
        - CLI should set connected=False when tokens expire or are revoked
        - Agent will use these flags to determine available operations

        Args:
            service: Service name ('github', 'trello', 'jira')
            connected: Whether the service is currently connected
            username: Public username/identifier for the service
            instance_url: For Jira, the instance URL (e.g., company.atlassian.net)
            email: For Jira, the email associated with the account
        """
        if service == "github":
            self.github_connected = connected
            if username:
                self.github_username = username
        elif service == "jira":
            self.jira_connected = connected
            if instance_url:
                self.jira_instance_url = instance_url
            if email:
                self.jira_email = email

        self.touch()

    def get_integration_status(self) -> Dict[str, Dict[str, Any]]:
        """Get all integration statuses"""
        return {
            "github": {
                "connected": self.github_connected,
                "username": self.github_username,
            },
            "jira": {
                "connected": self.jira_connected,
                "instance_url": self.jira_instance_url,
                "email": self.jira_email,
            },
        }

    def get_display_name(self) -> str:
        """Get the display name for the user, preferring first/last name over full_name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.full_name:
            return self.full_name
        else:
            return self.email.split("@")[0]

    def get_short_name(self) -> str:
        """ "Alex Y." -- a name for a credit line beside a ticket.

        A release summary credits several people per line, so a full name for
        each is too heavy and a GitHub handle is not a person. First name plus
        last initial reads as a human being and stays short.

        **`first_name`/`last_name` are usually empty**, so the `full_name` split
        is the path that actually runs: every user in the live org has a
        populated `full_name` and neither component. Splitting on whitespace and
        taking the last token as the surname handles "Alex Yu" and also
        "Jasminder pal singh". A single-token name ("Ken") gets no initial --
        "Ken K." would be an invention.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name[0]}."
        if self.first_name:
            return self.first_name
        if self.full_name:
            parts = self.full_name.split()
            if len(parts) > 1:
                return f"{parts[0]} {parts[-1][0].upper()}."
            if parts:
                return parts[0]
        return self.email.split("@")[0]

    def update_name_from_components(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ) -> None:
        """Update name fields and sync full_name if needed."""
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name

        # Update full_name if both components are available
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"

        self.touch()

    # User-level role methods (platform-wide permissions)
    def is_admin(self) -> bool:
        """Check if the user has admin privileges."""
        return self.role == UserRole.ADMIN

    def is_member(self) -> bool:
        """Check if the user has member privileges."""
        return self.role == UserRole.MEMBER

    def promote_to_admin(self) -> None:
        """Promote user to admin role."""
        self.role = UserRole.ADMIN
        self.touch()

    def demote_to_member(self) -> None:
        """Demote user to member role."""
        self.role = UserRole.MEMBER
        self.touch()

    @property
    def email_verified(self) -> bool:
        """True once the IdP confirmed the user controls this email address."""
        return self.email_verified_at is not None

    def mark_email_verified(self, when: Optional[datetime] = None) -> None:
        """Record IdP email confirmation. Idempotent — keeps the first timestamp."""
        if self.email_verified_at is None:
            self.email_verified_at = when or datetime.utcnow()
            self.touch()

    # Platform member management (Phase 1: Deprecate Client Concept)
    def promote_to_platform_member(self) -> None:
        """Promote user to platform member with cross-organization access."""
        self.is_platform_member = True
        self.touch()

    def demote_from_platform_member(self) -> None:
        """Remove platform member privileges."""
        self.is_platform_member = False
        self.touch()

    def has_cross_organization_access(self) -> bool:
        """Check if user has access across all organizations."""
        return self.is_platform_member

    # Organization-level role methods (organization-specific permissions)
    def get_primary_organization(self) -> Optional["Organization"]:
        """Get the user's primary/first organization."""
        active_memberships = [m for m in self.organization_memberships if m.is_active]
        return active_memberships[0].organization if active_memberships else None

    def is_org_admin(self, organization_id: str) -> bool:
        """Check if user is admin/owner of specific organization.

        Platform members are admins of EVERY organization -- consistent with the
        request-time bypass in verify_org_membership (they get cross-org access
        without any membership row). Without this short-circuit, admin-gated
        actions (e.g. sending invites) would wrongly reject platform staff.
        """
        if self.is_platform_member:
            return True
        membership = next(
            (
                m
                for m in self.organization_memberships
                if m.organization_id == organization_id and m.is_active
            ),
            None,
        )
        return membership.is_admin_or_owner() if membership else False

    def is_org_owner(self, organization_id: str) -> bool:
        """Check if user is owner of specific organization.

        Platform members are treated as owners everywhere, mirroring the
        cross-org bypass (see is_org_admin).
        """
        if self.is_platform_member:
            return True
        membership = next(
            (
                m
                for m in self.organization_memberships
                if m.organization_id == organization_id and m.is_active
            ),
            None,
        )
        return membership.is_owner if membership else False

    def get_organization_role(self, organization_id: str) -> Optional[str]:
        """Get user's role in specific organization."""
        membership = next(
            (
                m
                for m in self.organization_memberships
                if m.organization_id == organization_id and m.is_active
            ),
            None,
        )
        return membership.role if membership else None

    def get_organizations(self) -> List["Organization"]:
        """Get all organizations this user belongs to."""
        return [
            m.organization
            for m in self.organization_memberships
            if m.is_active and m.organization
        ]

    # Role-based access methods
    def is_developer(self) -> bool:
        """Check if user has developer role."""
        return self.role == UserRole.DEVELOPER

    def is_admin_or_developer(self) -> bool:
        """Check if user is admin or developer (for repository access)."""
        return self.role in [UserRole.ADMIN, UserRole.DEVELOPER]

    def can_access_repositories(self) -> bool:
        """Check if user can access GitHub repositories."""
        return self.is_admin_or_developer()

    def can_manage_users(self) -> bool:
        """Check if user can manage other users."""
        return self.is_admin()

    def promote_to_developer(self) -> None:
        """Promote user to developer role."""
        self.role = UserRole.DEVELOPER
        self.touch()

    # Developer License (BYOL) Methods
