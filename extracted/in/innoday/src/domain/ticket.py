from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint, text
from sqlmodel import Column, Field, Relationship, SQLModel

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.board import BoardRegistration
    from src.domain.organization import Organization
    from src.domain.project import Project
    from src.domain.user import User


class TicketStatus(str, Enum):
    DRAFT = "draft"
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in progress"
    IN_REVIEW = "in review"
    DONE = "done"
    CANCELLED = "cancelled"

    @classmethod
    def _missing_(cls, value: object) -> Optional["TicketStatus"]:
        """Accept the spellings clients actually send, not just the canonical one.

        **The member NAMES and the member VALUES are spelled differently, and
        every client had been sending the names.** ``IN_REVIEW`` is the name;
        ``"in review"`` is the value, and only the value matched. So a caller
        following the vocabulary printed in `innoday tickets update --help`
        (``DRAFT, BACKLOG, TODO, IN_PROGRESS, ...``) got a 422 listing the
        lowercase values back at it.

        The CLI had papered over this in its own HTTP client
        (``status.lower().replace("_", " ")``), which is why the CLI worked and
        the MCP server -- posting to the identical endpoint, documenting the
        identical vocabulary -- did not. Normalising here fixes both, and every
        future client, instead of asking each one to remember.

        Case, underscores and hyphens are the whole of it: ``"In Progress"``,
        ``"in-progress"``, ``"IN_PROGRESS"`` and ``"in progress"`` are one
        status to a human and are now one status here.

        **Deliberately no synonym tier.** Mapping unknown words onto members is
        how ``"done"`` reaches ``CANCELLED``; an unrecognised status must still
        fail loudly rather than silently become somebody else's.
        """
        if not isinstance(value, str):
            return None
        normalised = " ".join(
            value.strip().lower().replace("_", " ").replace("-", " ").split()
        )
        for member in cls:
            if member.value == normalised:
                return member
        return None


class Ticket(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    summary: str
    description: Optional[str] = None
    assignee: Optional[str] = None  # Keep for backward compatibility

    # Organization reference
    organization_id: str = Field(
        sa_column=Column(String, ForeignKey("organizations.id"), nullable=False)
    )

    # Project-scoped sequential reference number (1, 2, 3…) set on first
    # sync/create. Scoped to the project, not the org: `Project.alias` is
    # documented as "short uppercase code used as ticket prefix", and an
    # org-scoped number cannot follow a project that moves between orgs -- every
    # number in the destination org's sequence collides with it.
    project_ref_number: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
        description="Project-scoped sequential number for display (e.g. 42 → 'BPAI-42')",
    )

    status: TicketStatus = Field(default=TicketStatus.BACKLOG)
    completed_at: Optional[datetime] = Field(
        default=None
    )  # When ticket was marked as DONE
    # Version/release: Jira fixVersions or a semver-shaped Linear label.
    #
    # **100 is a deliberate ceiling, not an oversight, and shrinking it buys
    # nothing.** Postgres `varchar(n)` is variable-length -- `n` is a constraint,
    # not an allocation -- so `varchar(100)` and `varchar(50)` occupy byte-for-byte
    # identical space (measured: 2,637,824 bytes each for 50k rows). There is no
    # storage or speed win to collect here.
    #
    # The cost of tightening it is real, though. This field holds whatever a board
    # labelled the work with, and Jira's `fixVersions[].name` is free text -- a
    # legitimate "2026 Q3 Compliance Release" is 26 characters. Postgres *errors*
    # on an overlong value rather than truncating, so too tight a limit turns a
    # board label into a failed sync.
    #
    # And it could not be caught before production: SQLite ignores `varchar`
    # limits entirely (it stores 200 characters in a `varchar(10)`), and the suite
    # runs on SQLite unless INNODAY_TEST_POSTGRES_URL is set.
    #
    # **Keep this equal to `Release.version`'s max_length.** They are the two
    # halves of the join; shrinking one alone creates versions that can exist as a
    # Release row but cannot be stored on a ticket -- unjoinable, silently.
    release: Optional[str] = Field(default=None, max_length=100)
    url: Optional[str] = None

    # Project reference — denormalized from board→project at sync/create time.
    # Required: a board always belongs to exactly one project (see
    # BoardRegistration.project_id), so a ticket synced from a board always
    # has a resolvable project; manually-created tickets must specify one.
    project_id: str = Field(
        sa_column=Column(String, ForeignKey("projects.id"), nullable=False)
    )

    # Board synchronization fields
    board_registration_id: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("board_registrations.id"))
    )
    external_ticket_id: Optional[str] = Field(default=None, max_length=255)

    # Cross-platform enrichment fields
    source_platform: Optional[str] = Field(
        default=None,
        description="Denormalized board_type value (trello|jira|notion|linear). Populated on sync.",
    )
    priority: Optional[str] = Field(
        default=None,
        description="Normalized priority: no_priority|urgent|high|medium|low.",
    )
    parent_external_id: Optional[str] = Field(
        default=None,
        description="External ID of parent issue (Linear parent, Jira epic link).",
    )

    # Logical-delete marker. NULL = live. Set by board clear/delete; cleared on
    # re-sync if the ticket still exists at source. Tickets are never hard-deleted.
    deleted_at: Optional[datetime] = Field(default=None, index=True)

    # User tracking fields
    created_by: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("users.id"))
    )
    assigned_to: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("users.id"))
    )

    # Relationships
    organization: "Organization" = Relationship(back_populates="tickets")
    project: Optional["Project"] = Relationship(back_populates="tickets")
    board_registration: Optional["BoardRegistration"] = Relationship(
        back_populates="tickets"
    )
    creator: Optional["User"] = Relationship(
        back_populates="tickets_created",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.created_by]"},
    )
    assignee_user: Optional["User"] = Relationship(
        back_populates="tickets_assigned",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to]"},
    )

    # Relationship for comments
    comments: List["TicketComment"] = Relationship(back_populates="ticket")

    # Constraints - simple unique constraint for board registration + external ID
    __table_args__ = (
        UniqueConstraint(
            "board_registration_id",
            "external_ticket_id",
            name="uq_ticket_board_external",
        ),
        # project_ref_number is user-facing ("BPAI-42"), so a collision means two
        # tickets display as the same id. It was assigned by
        # read-max-then-insert with no lock, so two concurrent syncs -- each on
        # its own Session -- both read max=41 and both wrote 42. The constraint
        # is what makes that race impossible; BoardSyncService retries on
        # violation. NULLs don't collide in Postgres or SQLite, so tickets
        # created outside sync (no ref) are unaffected.
        #
        # Scoped by project, not organization. An org-scoped number cannot
        # survive a project moving between orgs: the destination org has its own
        # 1..n sequence, so every moved ticket collides at once. Per-project
        # numbering makes the move a no-op for this constraint.
        UniqueConstraint(
            "project_id",
            "project_ref_number",
            name="uq_ticket_project_ref_number",
        ),
        # The workflow page's two window queries, each given the index that
        # removes its sort. See `_tickets_capped_per_partition`: both rank rows
        # with `row_number() OVER (PARTITION BY … ORDER BY updated_at DESC)`,
        # and a window function cannot be answered from a top-N heap -- Postgres
        # must produce the *whole* partition in order before it can number it.
        # Unindexed that meant sorting every matching row on each page load.
        #
        # Three details do the work, and each was measured to matter (60k
        # tickets across 15 projects, the shape board sync produces -- ~70% DONE
        # with the freshest `updated_at`):
        #
        #   `updated_at DESC`, not ASC. ASC still groups the partitions, but the
        #   planner then bolts an Incremental Sort on top to flip the ordering
        #   inside each one: 34-42ms against 19-25ms.
        #
        #   `INCLUDE (id)` -- the only column the ranking subquery selects. It
        #   is what makes the scan *Index Only*: without it the same plan reads
        #   53,659 buffers fetching `id` from the heap row by row, with it 363.
        #   That is the difference between a page that is fast on a warm cache
        #   and one that is fast at all.
        #
        #   `WHERE deleted_at IS NULL` -- not for size (95% of rows are live, so
        #   it saves almost nothing) but because an index-only scan cannot
        #   consult a column it does not carry. Without the predicate the filter
        #   forces a heap visit per row and the Index Only Scan degrades to a
        #   plain Index Scan, which is the 53,659-buffer case above. Carrying
        #   `deleted_at` as another INCLUDE column would also work; the
        #   predicate is smaller and states the intent.
        Index(
            "ix_ticket_project_status_updated",
            "project_id",
            "status",
            text("updated_at DESC"),
            postgresql_include=["id"],
            postgresql_where=text("deleted_at IS NULL"),
            sqlite_where=text("deleted_at IS NULL"),
        ),
        # `done_unreleased_for` needs its own index rather than riding the one
        # above, and this was checked rather than assumed: forced onto
        # `ix_ticket_project_status_updated` the query got *slower* than the
        # seq scan it replaced (28ms against 26ms), because that index cannot
        # screen on `release` -- it walks all 42,000 DONE rows to keep 10,800.
        # The planner declines it for exactly that reason and is right to.
        #
        # Folding the whole predicate into a partial index instead leaves 900
        # index entries to scan (448 kB total) and no sort: 26-34ms -> 8-9ms,
        # and the window's buffer count drops 1,034 -> 56. `status` and
        # `release` are equality/emptiness tests here, so moving them into the
        # predicate costs nothing in generality -- this index answers one
        # question, which is the only one asked of it.
        Index(
            "ix_ticket_project_done_unreleased",
            "project_id",
            text("updated_at DESC"),
            postgresql_include=["id"],
            postgresql_where=text(
                "deleted_at IS NULL AND status = 'DONE' AND (release IS NULL OR release = '')"
            ),
            sqlite_where=text(
                "deleted_at IS NULL AND status = 'DONE' AND (release IS NULL OR release = '')"
            ),
        ),
    )

    def get_organization_id(self) -> str:
        """Get organization ID."""
        return self.organization_id

    def get_organization(self) -> "Organization":
        """Get organization object."""
        return self.organization


class TicketComment(SQLModel, table=True):
    __tablename__ = "ticket_comment"

    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.id")
    # User IDs are UUID strings (see User.id); the column was mistakenly created
    # as an integer, which 500s on every comment/cancel write. FK to users.id.
    commenter_id: str = Field(foreign_key="users.id")
    comment: str
    parent_comment_id: Optional[int] = Field(
        default=None, foreign_key="ticket_comment.id"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    ticket: Ticket = Relationship(back_populates="comments")
    parent_comment: Optional["TicketComment"] = Relationship(
        sa_relationship_kwargs={"remote_side": "TicketComment.id"}
    )
    child_comments: List["TicketComment"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "overlaps": "parent_comment",
        }
    )
