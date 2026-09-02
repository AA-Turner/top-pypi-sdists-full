from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import JSON, ForeignKey, Index, String, UniqueConstraint, text
from sqlmodel import Column, Field, Relationship, SQLModel

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.organization import Organization
    from src.domain.project import Project
    from src.domain.ticket import Ticket
    from src.domain.user import User


class BoardType(str, Enum):
    """Supported board types for synchronization"""

    TRELLO = "trello"
    JIRA = "jira"
    NOTION = "notion"
    LINEAR = "linear"


class SyncStatus(str, Enum):
    """Status of board synchronization operations"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class BoardRegistration(TimestampMixin, table=True):
    """
    Board registrations linking users, clients, and external boards.

    This model manages the relationship between InnoDay clients and external
    project management boards (Trello/Jira). Each registration represents
    a user's authorization to sync tickets from a specific board to a client.

    Security Note:
    - This model does NOT store API tokens or sensitive credentials
    - Tokens are managed by the CLI and passed during sync operations
    - Only public board metadata and configuration is stored
    """

    __tablename__ = "board_registrations"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    user_id: str = Field(sa_column=Column(String, ForeignKey("users.id")))

    # Organization reference
    organization_id: str = Field(
        sa_column=Column(String, ForeignKey("organizations.id"))
    )

    # Project reference -- REQUIRED. A board must belong to a project; there
    # is no supported "org-only" board. This is the canonical, one-directional
    # FK (Project no longer holds a reverse pointer -- that deprecated
    # transition field, Project.board_registration_id, has been removed).
    # At most one *live* board per project is enforced by a PARTIAL unique
    # index (WHERE deleted_at IS NULL) declared in __table_args__ below -- not
    # by an unconditional unique= on this column. That soft-delete-awareness
    # is load-bearing: a soft-deleted board keeps its project_id for audit, so
    # an unconditional unique constraint would block re-registering a new board
    # for the same project (the Jira->Linear migration flow). index=True still
    # keeps a plain index on the column for FK lookups.
    project_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("projects.id"),
            nullable=False,
            index=True,
        )
    )

    # Board identification
    board_name: str = Field(max_length=255)
    board_url: str = Field(max_length=500)
    board_type: BoardType
    board_external_id: str = Field(
        max_length=255
    )  # Trello board ID or Jira project key

    # Configuration
    is_active: bool = Field(default=True)
    auto_sync_enabled: bool = Field(default=False)
    sync_frequency_hours: Optional[int] = Field(default=None)  # For future auto-sync

    last_sync_at: Optional[datetime] = Field(default=None)

    # Whether the last sync of this board failed, and when. `last_sync_at` alone
    # could not answer that: it records that an attempt *happened*, so a board
    # whose credential expired three days ago still looked freshly synced. See
    # #499. `BoardSyncHistory` holds the same facts per attempt, but that is an
    # audit log -- this is current state, which is what a status icon can read
    # without walking history on every page load.
    errored_at: Optional[datetime] = Field(default=None)
    error_message: Optional[str] = Field(default=None, max_length=500)

    # Logical-delete marker for the board registration. NULL = live. A deleted
    # board keeps its row (and its tickets' rows) for audit.
    deleted_at: Optional[datetime] = Field(default=None, index=True)

    # Relationships
    user: Optional["User"] = Relationship()
    organization: Optional["Organization"] = Relationship(
        back_populates="board_registrations"
    )
    project: Optional["Project"] = Relationship(
        back_populates="boards",
        sa_relationship_kwargs={"foreign_keys": "[BoardRegistration.project_id]"},
    )
    sync_history: List["BoardSyncHistory"] = Relationship(
        back_populates="board_registration"
    )
    board_metadata: Optional["BoardMetadata"] = Relationship(
        back_populates="board_registration"
    )
    tickets: List["Ticket"] = Relationship(back_populates="board_registration")

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "board_external_id",
            "board_type",
            name="uq_organization_board_type",
        ),
        # At most one LIVE board per project. Partial unique index so that a
        # soft-deleted board (deleted_at IS NOT NULL) does not block
        # re-registering a new board for the same project. Both dialect
        # predicates are given so Postgres (prod) and SQLite (tests) each emit
        # a real partial unique index and stay consistent. Same name as the
        # unconditional constraint it replaces (uq_board_registrations_project_id).
        Index(
            "uq_board_registrations_project_id",
            "project_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
            sqlite_where=text("deleted_at IS NULL"),
        ),
    )

    def get_organization_id(self) -> str:
        """Get organization ID."""
        return self.organization_id

    def get_organization(self) -> Optional["Organization"]:
        """Get organization object."""
        return self.organization


class BoardSyncHistory(SQLModel, table=True):
    """
    Sync history for audit trail and monitoring.

    Tracks each synchronization operation for debugging, monitoring,
    and providing users with sync status information.
    """

    __tablename__ = "board_sync_history"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    board_registration_id: str = Field(
        sa_column=Column(String, ForeignKey("board_registrations.id"))
    )

    # Sync status and results
    sync_status: SyncStatus = Field(default=SyncStatus.PENDING)
    #: Whether this run was a preview that wrote nothing.
    #:
    #: **Three readers need to know, and none of them could.** A dry run recorded a
    #: row indistinguishable from a real sync -- `completed_at` set, counts
    #: populated -- so `board sync-status` reported "Last sync completed
    #: successfully · 38 created" for a run that created nothing; the
    #: already-in-progress guard could be tripped by an abandoned preview; and
    #: worst, `SummaryService.latest_sync` read it as evidence of freshness, so
    #: gate 1 skipped a *real* sync for the freshness window. A dry run therefore
    #: suppressed the very sync it was meant to preview.
    dry_run: bool = Field(default=False, nullable=False)
    tickets_found: int = Field(default=0)
    tickets_created: int = Field(default=0)
    tickets_updated: int = Field(default=0)
    tickets_skipped: int = Field(default=0)

    # Error handling
    error_message: Optional[str] = Field(default=None)
    error_code: Optional[str] = Field(default=None)

    # Timestamps
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # User tracking
    synced_by: str = Field(sa_column=Column(String, ForeignKey("users.id")))

    # Relationships
    board_registration: Optional["BoardRegistration"] = Relationship(
        back_populates="sync_history"
    )
    synced_by_user: Optional["User"] = Relationship()

    @property
    def duration_seconds(self) -> Optional[int]:
        """Calculate sync duration in seconds"""
        if self.completed_at and self.started_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None

    def mark_completed(
        self, status: SyncStatus, error_message: Optional[str] = None
    ) -> None:
        """Mark the sync as completed with given status"""
        self.sync_status = status
        self.completed_at = datetime.now(timezone.utc)
        if error_message:
            self.error_message = error_message


class BoardMetadata(SQLModel, table=True):
    """
    Board metadata cache for non-sensitive board information.

    Stores cached information about the board structure and activity
    to improve sync performance and provide users with board insights.
    """

    __tablename__ = "board_metadata"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    board_registration_id: str = Field(
        sa_column=Column(
            String, ForeignKey("board_registrations.id", ondelete="CASCADE")
        )
    )

    # Board statistics
    last_activity_date: Optional[datetime] = Field(default=None)
    member_count: Optional[int] = Field(default=None)
    list_count: Optional[int] = Field(default=None)  # Trello lists or Jira statuses
    total_cards: Optional[int] = Field(default=None)

    # Cached metadata (non-sensitive)
    board_description: Optional[str] = Field(default=None)
    board_visibility: Optional[str] = Field(default=None)  # public, private, team
    labels: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, sa_column=Column(JSON)
    )
    custom_fields: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, sa_column=Column(JSON)
    )

    # Update tracking
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    board_registration: Optional["BoardRegistration"] = Relationship(
        back_populates="board_metadata"
    )

    def update_from_api(self, api_data: Dict[str, Any]) -> None:
        """Update metadata from API response"""
        self.updated_at = datetime.now(timezone.utc)

        # Update common fields based on board type
        if "desc" in api_data:  # Trello
            self.board_description = api_data.get("desc")
        elif "description" in api_data:  # Jira
            self.board_description = api_data.get("description")

        if "prefs" in api_data:  # Trello preferences
            prefs = api_data["prefs"]
            self.board_visibility = prefs.get("permissionLevel")

        # Update activity and member info
        if "dateLastActivity" in api_data:
            try:
                self.last_activity_date = datetime.fromisoformat(
                    api_data["dateLastActivity"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        if "memberships" in api_data:
            self.member_count = len(api_data["memberships"])
        elif "members" in api_data:
            self.member_count = len(api_data["members"])
