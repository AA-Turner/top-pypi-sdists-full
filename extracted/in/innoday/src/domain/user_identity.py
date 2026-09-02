"""Mapping from an external board handle to an InnoDay user.

Boards record an assignee as a display name (`Ticket.assignee`), which is the
board's own truth and stays that way. This table is the bridge that lets
`Ticket.assigned_to` — a real FK to `users.id` — be populated from it.

Two kinds of row, distinguished only by `project_id`:

* ``project_id IS NULL`` — a **global** handle for this platform, and the pool
  auto-matching draws from. "Wherever a Linear board says `A. Lice`, that is
  this user."
* ``project_id`` set — the same person's handle **on one project's board**.
  Checked first, so a project row shadows the global one.

`project_id` is *not* a way to give one handle to two people. Within one
organisation a handle already linked to someone is refused for anyone else, in
every project — see `IdentityResolutionService.claim_identity`. (An earlier
version of this docstring described exactly that as the field's purpose; the
claim rule has always made it unreachable, and the rule is the one that is
right: one handle identifies one human, or the global fallback is ambiguous.)
What the field buys is the opposite case — one person appearing under different
handles on different clients' boards, and a project row taking precedence over
a stale or generic global one.

The rule stops at the organisation boundary, and deliberately: two unrelated
tenants both having a `Sam Patel` on their boards is two people with the same
name, not a collision, and refusing the second was letting whoever claimed a
common name first squat it platform-wide.

Two constraints hold the rule up:

* `UNIQUE(project_id, platform, handle)` — one row per handle per scope.
* `UNIQUE(platform, handle) WHERE project_id IS NULL` — one *global* owner per
  handle. The first cannot express this: in Postgres two NULL `project_id`
  rows never collide, so without it a second global row naming a different
  user commits with no error, and the resolver picks between them arbitrarily.
"""

from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.project import Project
    from src.domain.user import User


class IdentityPlatform(str, Enum):
    """External system a handle belongs to."""

    GITHUB = "github"
    LINEAR = "linear"
    JIRA = "jira"
    TRELLO = "trello"
    NOTION = "notion"


class MatchSource(str, Enum):
    """How the link between handle and user was established.

    Two of these describe a *row* in this table and are what the column holds;
    the other two only ever describe a live ``IdentityResolutionService.resolve``
    answer. ``GITHUB_USERNAME`` is the second kind and cannot be anything else —
    a row for a login is precisely the thing it is not.

    **Why the column match has its own value.** It used to report as ``HANDLE``,
    the same value a registered ``user_identity`` row answers with. That was
    survivable while the column was read first and the row was a fallback; #593
    reversed the precedence deliberately (an automatic value must not shadow one
    a person wrote), which makes "did the deliberate override fire, or did the
    generic column answer?" the question the provenance now exists to answer —
    and one value for both made it unanswerable. Both still name the same human,
    so nothing but the label distinguishes them.
    """

    EMAIL = "email"  # the board supplied an address matching users.email
    HANDLE = "handle"  # matched a registered user_identity.handle
    GITHUB_USERNAME = "github_username"  # matched the users.github_username column
    MANUAL = "manual"  # a person claimed it


class UserIdentity(TimestampMixin, table=True):
    """One (project, platform, handle) → user mapping."""

    __tablename__ = "user_identity"

    # Every column below passes an explicit sa_column, which hands column
    # construction to SQLAlchemy -- whose default is nullable=True regardless
    # of the annotation. `nullable=` is therefore stated on every one of them,
    # so the schema the test fixtures build with create_all matches the
    # migration rather than being quietly more permissive. See CLAUDE.md,
    # "sa_column= silently drops NOT NULL".
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String, primary_key=True),
    )
    user_id: str = Field(
        sa_column=Column(String, ForeignKey("users.id"), nullable=False, index=True)
    )
    project_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String, ForeignKey("projects.id"), nullable=True),
        description=(
            "NULL = this user's global handle for the platform; set = the same "
            "user's handle on one project's board, which takes precedence"
        ),
    )
    platform: IdentityPlatform = Field(
        sa_column=Column(SAEnum(IdentityPlatform), nullable=False)
    )
    handle: str = Field(
        sa_column=Column(String(255), nullable=False),
        description="The board's own identifier for the person -- usually the display name",
    )
    board_user_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255), nullable=True),
        description=(
            "The board's stable user id, recorded for reference; not matched "
            "on. Written by the Linear and Jira adapters via "
            "`claim_identity`; nothing reads it yet, and that is the point -- "
            "`handle` is a display name a board can change, so the stable id "
            "is the only way a later migration could re-link a renamed person, "
            "and it can only be captured at sync time. Not an orphan: it has "
            "writers, and adding them later would recover nothing."
        ),
    )
    match_source: MatchSource = Field(
        default=MatchSource.MANUAL,
        sa_column=Column(SAEnum(MatchSource), nullable=False),
        description=(
            "How this row came to exist. In practice always MANUAL -- every "
            "writer is somebody saying who a handle is. `GITHUB_USERNAME` "
            "cannot appear here by construction (it names the *other* store), "
            "but it is in the type because `SAEnum(MatchSource)` is generated "
            "from the enum, and a type the migration and `create_all` disagree "
            "about is drift whether or not anything writes the value -- see the "
            "migration that adds it."
        ),
    )

    user: Optional["User"] = Relationship()
    project: Optional["Project"] = Relationship()

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "platform",
            "handle",
            name="uq_user_identity_project_platform_handle",
        ),
        # One global row per (platform, handle) -- the constraint the plain
        # UNIQUE above cannot express, because NULL `project_id`s never collide
        # with each other. Without it two rows naming *different* users as the
        # global owner of one handle commit happily, and the resolver then has
        # to pick between them.
        #
        # This one *is* platform-wide, unlike the claim rule above, because a
        # global row is by definition unscoped -- there is no organisation to
        # key it on. Nothing user-facing writes global rows (the profile page
        # always passes a `project_id`), so it is not a path one tenant can use
        # to block another; a future feature that does write them would have to
        # decide what a global handle means across tenants first.
        Index(
            "uq_user_identity_global_platform_handle",
            "platform",
            "handle",
            unique=True,
            postgresql_where=text("project_id IS NULL"),
            sqlite_where=text("project_id IS NULL"),
        ),
        # Both the resolver and the claim check look a handle up by
        # (platform, handle) before they know which project scope wins.
        Index("ix_user_identity_platform_handle", "platform", "handle"),
    )
