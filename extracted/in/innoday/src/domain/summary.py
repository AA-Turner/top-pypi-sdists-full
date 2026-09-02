"""Summaries: one write-up of what happened, scoped and windowed (PF-398).

This was `board_summaries` -- a blob of AI prose hanging off a board
registration, with no notion of *whose* work it described or *what stretch of
time* it covered. Two summaries of the same board were only distinguishable by
`created_at`, so nothing could ask "do we already have this week's summary for
Alex?" and nothing could show the per-ticket breakdown behind the prose.

Three ideas carry the widened model:

**Scope.** A summary belongs to a project (`project_id`, NOT NULL) and
optionally to one person (`user_id`). ``user_id IS NULL`` is not missing data --
it is the *team* summary, the scrum-style roll-up over everyone. A board
registration is still recorded when the summary came from one, but it is no
longer the thing a summary hangs off, so `board_registration_id` is nullable.

**Window.** `window_spec` is the literal spec the caller asked for -- `"3d"`,
`"1w"` -- and it, not a timestamp, is the cache key. Asking twice for "the last
3 days" is the same question both times; asking with two timestamps that happen
to be 3 days apart is not obviously the same question to a database. The
resolved `period_start`/`period_end` are recorded as metadata, so a reader can
see which days were actually covered, but they are deliberately *not* identity.

**Supersession.** Re-running a summary does not overwrite the old one. The old
row gets `superseded_by_id` pointing at the new one, so the history survives and
"the current summary" is expressible as `superseded_by_id IS NULL`. That is what
makes the uniqueness rule below a rule about *live* rows rather than about every
row that ever existed.

**Two kinds of prose, kept apart.** `body_markdown` is what the narrator
generated; `notes_markdown` is what a person wrote to go with it. They are
separate columns rather than one appended blob because they answer to different
authors and have different lifetimes: the generated half is rewritten on every
re-run, the human half is not. Merging them would mean the next regeneration
either destroyed someone's note or had to parse it back out of its own output.

That difference is why supersession **carries the note forward**: a replacement
that says nothing about notes inherits the superseded row's, so re-running the
summary at 16:00 does not silently discard what someone typed at 09:00. Clearing
one is possible but has to be asked for explicitly (`notes_markdown=""`), never
implied by omission -- see `SummaryService.persist`.

Writing a replacement therefore has one correct order -- **update the old row
first, then insert the new one**. The unique indexes are checked immediately, so
inserting first would put two live rows in the same slot for the length of a
statement and be refused. The self-FK is `DEFERRABLE INITIALLY DEFERRED` so that
the update may name a row that does not exist yet; both checks settle at
COMMIT.

Two partial unique indexes enforce "at most one live summary per scope+window",
and it takes two because `user_id` is nullable: in Postgres two NULLs never
compare equal, so a single `UNIQUE(project_id, user_id, summary_type,
window_spec)` would happily accept a second *team* summary for the same project,
type and window -- exactly the trap `user_identity` hit with its global handles.
The team case therefore gets its own index with `user_id` dropped from the
column list and `user_id IS NULL` moved into the predicate, where NULL is a
condition rather than a value.

Both predicates also exclude ``window_spec = ''``. That empty string is NOT
"unknown" -- it is the explicit marker for a summary written outside the
windowed regime, which today means the board-scoped
`POST .../boards/{id}/summaries` path that has always been free to append as
many status summaries to a board as it likes. Those rows are a history log, not
cache entries, and there is nothing for a uniqueness rule to key them on. The
column stays NOT NULL so the distinction is a value in the data and a condition
in the index, never a NULL that quietly opts a row out of a constraint.

`SummaryItem` is the per-ticket breakdown. Its `assignee_display` and
`attribution` exist because **a ticket with no assignee is a first-class case**,
not an error: the board may name nobody while the commits and PRs in the window
carry a real author. `attribution` records where the ownership on the row
actually came from -- `board` (the board said so), `code` (the commit/PR author
did), or `none` (nobody is attributable).
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:  # forward refs for the Relationship() strings below
    from .board import BoardRegistration
    from .organization import Organization


class SummaryType(str, Enum):
    """Types of summaries that can be generated."""

    STATUS = "status"  # Current status overview
    DAILY = "daily"  # Daily standup format
    SPRINT = "sprint"  # Sprint health metrics
    WEEKLY = "weekly"  # Weekly roundup
    RELEASE = "release"  # Release summary with commit history since a tag
    CUSTOM = "custom"  # Custom user-defined
    SCRUM = "scrum"  # Team stand-up roll-up (user_id IS NULL)
    PERSONAL = "personal"  # One person's work over the window


class GeneratedBy(str, Enum):
    """Who wrote the prose in `body_markdown`."""

    AGENT = "agent"  # written unattended by an agent
    HUMAN = "human"  # typed by a person
    HYBRID = "hybrid"  # agent draft, edited by a person


class Attribution(str, Enum):
    """Why a summary item is attributed to the person it names."""

    BOARD = "board"  # the board's own assignee field said so
    CODE = "code"  # the commit/PR author said so; the board named nobody
    NONE = "none"  # nobody is attributable to this item


class Summary(SQLModel, table=True):
    """One summary of a project's work over one named window.

    Every column that passes an explicit `sa_column` states `nullable=`, because
    SQLAlchemy defaults to nullable=True regardless of the annotation and the
    test fixtures build their schema from this metadata -- see CLAUDE.md,
    "sa_column= silently drops NOT NULL".
    """

    __tablename__ = "summaries"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )

    # ------------------------------------------------------------------ scope
    organization_id: str = Field(
        sa_column=Column(
            String, ForeignKey("organizations.id"), nullable=False, index=True
        )
    )
    project_id: str = Field(
        sa_column=Column(String, ForeignKey("projects.id"), nullable=False, index=True),
        description="The project the summary covers. Every summary has one.",
    )
    board_registration_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String, ForeignKey("board_registrations.id"), nullable=True, index=True
        ),
        description=(
            "The board this summary was assembled from, when it came from one. "
            "Nullable: a project/user summary need not involve a board at all."
        ),
    )
    user_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String, ForeignKey("users.id"), nullable=True, index=True),
        description="Whose work this summarises. NULL = the team/scrum summary.",
    )

    # ----------------------------------------------------------------- window
    window_spec: str = Field(
        # Deliberately no default. `''` is a *sentinel* -- "written outside the
        # windowed regime" -- and it is the one value both live-uniqueness
        # indexes exempt. A default would hand that exemption to any caller who
        # merely forgot the kwarg, silently, with no error: the row would be
        # exempt from both unique indexes and nothing would say so. Without one,
        # omission is a NOT NULL violation at insert. The two board call sites
        # that genuinely mean the sentinel pass `window_spec=""` explicitly.
        sa_column=Column(String(64), nullable=False),
        description=(
            "The literal window spec asked for, e.g. '3d'. This is the cache "
            "key -- deliberately the spec and not a timestamp. '' means the "
            "summary was written outside the windowed regime (the board-scoped "
            "append path) and is exempt from the live-uniqueness indexes."
        ),
    )
    period_start: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True),
        description="Resolved start of the window. Recorded metadata, not identity.",
    )
    period_end: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True),
        description="Resolved end of the window. Recorded metadata, not identity.",
    )

    # ---------------------------------------------------------------- content
    summary_type: SummaryType
    body_markdown: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="The summary prose itself (was `summary_content`).",
    )
    notes_markdown: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description=(
            "A person's own words, kept beside the generated prose rather than "
            "merged into it. NULL means nobody has written any."
        ),
    )
    notes_updated_at: Optional[datetime] = Field(
        default=None,
        # **Naive UTC, like every sibling on this table.** It shipped aware and
        # was the only such column here; a single aware column in a naive table
        # means Postgres refuses the first obvious comparison somebody writes
        # against it. See 20260810_090000 for the measurement (99 naive : 7
        # aware) and why it was cheap to correct immediately.
        sa_column=Column(DateTime(), nullable=True),
        description=(
            "When the note last actually changed -- never restamped by a "
            "regeneration that merely inherited it. A note outlives the prose "
            "it was written against, so this is what tells a reader whether it "
            "is current."
        ),
    )
    summary_data: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    ticket_stats: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    highlights: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    concerns: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    motivational_quote: str = Field(max_length=500)

    # --------------------------------------------------------------- lineage
    # There is deliberately no `release_id`. One was added with the table and
    # never written by anything -- no writer in `persist`, none in
    # `CreateSummaryRequest`, none in the release router -- so every row had it
    # NULL while the FK and its docstring implied a supported lineage link.
    # Dropped in 20260806_140000. `SummaryType.RELEASE` remains; whoever builds
    # release summaries should re-add the column together with its writer.
    source_fingerprint: Dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=True),
        description=(
            "What the summary was built from (ticket ids, commit shas, ...), so a "
            "re-run can tell whether anything actually changed."
        ),
    )
    generated_by: GeneratedBy = Field(
        default=GeneratedBy.AGENT,
        sa_column=Column(SAEnum(GeneratedBy), nullable=False),
    )
    superseded_by_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String,
            # DEFERRABLE INITIALLY DEFERRED, because the only correct write
            # order fails an immediate check: the old row has to leave the live
            # index *before* the new row enters it, so the UPDATE that points it
            # at the replacement necessarily runs while the replacement does not
            # exist yet. Deferring lets both statements share one transaction.
            ForeignKey("summaries.id", deferrable=True, initially="DEFERRED"),
            nullable=True,
        ),
        description=(
            "The summary that replaced this one. NULL = this is the live one; a "
            "re-run supersedes rather than overwrites."
        ),
    )

    # --------------------------------------------------------------- metadata
    token_usage: int = Field(default=0)
    generation_time_ms: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("users.id"), nullable=True)
    )

    board_registration: Optional["BoardRegistration"] = Relationship()
    organization: Optional["Organization"] = Relationship()

    __table_args__ = (
        # At most one *live* summary per scope and window. Two indexes, not one,
        # because `user_id` is nullable and NULLs never collide in a plain
        # UNIQUE -- see the module docstring, which also explains why
        # `window_spec = ''` is excluded.
        Index(
            "uq_summaries_live_user",
            "project_id",
            "user_id",
            "summary_type",
            "window_spec",
            unique=True,
            postgresql_where=text(
                "superseded_by_id IS NULL AND user_id IS NOT NULL AND window_spec <> ''"
            ),
            sqlite_where=text(
                "superseded_by_id IS NULL AND user_id IS NOT NULL AND window_spec <> ''"
            ),
        ),
        Index(
            "uq_summaries_live_team",
            "project_id",
            "summary_type",
            "window_spec",
            unique=True,
            postgresql_where=text(
                "superseded_by_id IS NULL AND user_id IS NULL AND window_spec <> ''"
            ),
            sqlite_where=text(
                "superseded_by_id IS NULL AND user_id IS NULL AND window_spec <> ''"
            ),
        ),
        # Every read path orders by recency within a scope.
        Index("ix_summaries_created_at", "created_at"),
        # A row that supersedes itself is never live -- `superseded_by_id IS
        # NULL` is what "live" means -- so it empties its own scope+window slot
        # while still existing. The deferred self-FK accepts it happily; only
        # this says no. One hop only; see the migration for why cycles are not
        # covered.
        CheckConstraint(
            "superseded_by_id IS NULL OR superseded_by_id <> id",
            name="ck_summaries_no_self_supersede",
        ),
    )

    def to_dict(self) -> Dict:
        """Convert summary to dictionary for API responses.

        The board-scoped endpoints have returned this exact shape since the
        table was called `board_summaries`; the widened columns are appended
        rather than replacing anything, so existing consumers are unaffected.
        """
        return {
            "id": self.id,
            "board_registration_id": self.board_registration_id,
            "organization_id": self.organization_id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "window_spec": self.window_spec,
            "summary_type": self.summary_type,
            "summary": self.body_markdown,
            # Beside `summary`, never folded into it: the two have different
            # authors, and a client that merged them could not tell whose words
            # it was showing.
            #
            # Published under **both** names on purpose. This shape predates
            # the note and calls the prose `summary`, so `notes` is the pair
            # that reads correctly here; but `summary-data` -- which the skill
            # and the MCP guide both point agents at -- calls it
            # `notes_markdown`. An agent that saved a note and checked the
            # response for the documented key found nothing. Two keys, one
            # value, is cheaper than teaching every reader which endpoint it
            # came from.
            "notes": self.notes_markdown,
            "notes_markdown": self.notes_markdown,
            "notes_updated_at": (
                self.notes_updated_at.isoformat() if self.notes_updated_at else None
            ),
            "stats": self.ticket_stats,
            "highlights": self.highlights,
            "concerns": self.concerns,
            "motivational_message": self.motivational_quote,
            "created_at": self.created_at.isoformat(),
            "generation_time_ms": self.generation_time_ms,
        }


class SummaryItem(SQLModel, table=True):
    """One line of a summary: usually a ticket, always a unit of work.

    A row may carry no `ticket_id` at all -- code activity on a branch nobody
    opened a ticket for is still work that happened in the window.
    """

    __tablename__ = "summary_items"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    summary_id: str = Field(
        sa_column=Column(String, ForeignKey("summaries.id"), nullable=False, index=True)
    )
    ticket_id: Optional[int] = Field(
        default=None,
        # `ticket.id` is an autoincrement integer, not a string UUID -- unlike
        # nearly every other primary key in this schema.
        sa_column=Column(Integer, ForeignKey("ticket.id"), nullable=True, index=True),
        description=(
            "Indexed: per-ticket history -- 'show me every summary that "
            "mentioned this ticket' -- is a primary read path, not a rare one."
        ),
    )

    # -------------------------------------------------------------- ownership
    assignee_user_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String, ForeignKey("users.id"), nullable=True, index=True),
        description="The resolved InnoDay user, when the handle could be mapped.",
    )
    assignee_display: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255), nullable=True),
        description=(
            "The raw string the board used, kept for assignees that could not "
            "be mapped to a user -- losing it would lose the only record of who "
            "the board thought owned this."
        ),
    )
    attribution: Attribution = Field(
        default=Attribution.NONE,
        sa_column=Column(SAEnum(Attribution), nullable=False),
        description="Where the ownership on this row came from.",
    )

    # ------------------------------------------------------------------- code
    repo: Optional[str] = Field(
        default=None, sa_column=Column(String(255), nullable=True)
    )
    branch: Optional[str] = Field(
        default=None, sa_column=Column(String(255), nullable=True)
    )
    pr_url: Optional[str] = Field(
        default=None, sa_column=Column(String(500), nullable=True)
    )
    pr_state: Optional[str] = Field(
        default=None, sa_column=Column(String(50), nullable=True)
    )

    # --------------------------------------------------------------- verdict
    verdict: Optional[str] = Field(
        default=None,
        sa_column=Column(String(32), nullable=True),
        description=(
            "How this ticket was judged when the summary was written: shipped, "
            "partly_merged, not_merged, not_started, no_code, or one of the "
            "off-release pair. The same vocabulary `releases content` returns "
            "as `state`, deliberately -- one set of words, not two."
        ),
    )
    prs: Optional[List[Dict]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description=(
            "Every pull request that delivered this ticket -- `repo`, `number`, "
            "`url`, `merged`. `pr_url`/`pr_state` above hold the single one a "
            "stand-up line shows; a release line names them all, because a "
            "ticket delivered across the API and the UI is two links and "
            "showing one of them understates what shipped."
        ),
    )
    people: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description=(
            "Everyone credited on this ticket. `assignee_user_id` holds the one "
            "the board named; this holds all of them, which is what a release "
            "line has to show -- a ticket delivered by two people stored only "
            "the first, and the second's work disappeared from the record."
        ),
    )

    # ---------------------------------------------------------------- content
    body_markdown: Optional[str] = Field(
        default=None, sa_column=Column(Text, nullable=True)
    )
    occurred_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=True)
    )
    rank: int = Field(
        default=0,
        sa_column=Column(Integer, nullable=False),
        description="Display order within the summary; lower sorts first.",
    )
    no_work_detected: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False),
        description=(
            "The window was searched for this ticket/person and nothing was "
            "found. An explicit 'nothing happened', not an absent row."
        ),
    )
