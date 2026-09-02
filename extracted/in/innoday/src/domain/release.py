"""Release domain model."""

from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import JSON, Column, Date, Index, text
from sqlmodel import Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.organization import Organization
    from src.domain.project import Project


class ReleaseStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    RELEASED = "released"
    ARCHIVED = "archived"


class ReleaseVerdict(str, Enum):
    """How one ticket or pull request stands against a release.

    **These were bare string literals at eight assignment sites**, mirrored by
    hand into a rendering table in `summary_line`, into a TypeScript union in the
    UI, and into the release-review skill's prose. Four copies of one vocabulary,
    none of them authoritative: `verdict_label` deliberately passes an unknown
    state through, `SummaryItemPayload.state` is a bare `Optional[str]`, and the
    only thing that would refuse a new value was a UI typecheck the API never
    consulted. Two verdicts the skill described -- `release_candidate` and
    `unticketed_design` -- existed in no code at all, which is exactly the
    failure a closed set is supposed to make impossible.

    Closed on purpose. A situation that fits none of these is a finding about the
    payload, not grounds for a ninth.
    """

    #: On the release, every pull request merged inside the bounds.
    SHIPPED = "shipped"
    #: On the release, some merged and at least one still open.
    PARTLY_MERGED = "partly_merged"
    #: On the release, has pull requests, none merged.
    NOT_MERGED = "not_merged"
    #: On the release, still backlog or todo.
    NOT_STARTED = "not_started"
    #: On the release, no pull request names it. **Never grounds for dropping a
    #: design ticket** -- design work lands in the design repositories and is
    #: reported apart, so the ticket reads `no_code` while its code sits one
    #: bucket away.
    NO_CODE = "no_code"

    #: Not on the release: code merged inside the bounds, ticket carries no
    #: release. The loudest thing a release report can say.
    SHIPPED_UNTAGGED = "shipped_untagged"
    #: Not on the release: a pull request is open, so somebody is working on it.
    #: Distinct from `STARTED_UNTAGGED`, which has no code in flight at all --
    #: before a release is cut this is a candidate for it, and after one has gone
    #: out the same shape means the work did not make it.
    RELEASE_CANDIDATE = "release_candidate"
    #: Not on the release: started, carries no release, nothing in flight.
    STARTED_UNTAGGED = "started_untagged"
    #: Unfinished, but pointing at a version that has already shipped. Shipping
    #: touches no ticket, so nothing else says one was left behind.
    ON_SHIPPED_RELEASE = "on_shipped_release"

    #: A merged pull request naming no ticket.
    UNTICKETED = "unticketed"
    #: A merged pull request in a **design** repository naming no ticket.
    UNTICKETED_DESIGN = "unticketed_design"
    #: A pull request whose reference resolves, but to a ticket whose owner or
    #: subject disagrees with it. bps-ui-v2 #241 matched BPAI-409 cleanly and
    #: belonged to neither that ticket nor that person.
    CONTESTED = "contested"


class Recommendation(str, Enum):
    """The single move a reviewed row wants, or `NONE` when it wants nothing.

    Emitted only where it follows from the verdict. Whether an unticketed pull
    request pairs with an existing ticket, joins a proposed grouping, or gets one
    of its own is a judgement about what two pieces of English mean, and this
    service states facts it can defend -- so those rows carry no recommendation
    and the narrator proposes one.

    One per row. A row that genuinely wants two is really two rows.
    """

    #: It is where it belongs.
    NONE = "none"
    #: The code is inside these bounds; put the ticket on the release.
    ATTACH_TICKET_TO_RELEASE = "attach_ticket_to_release"
    #: An existing ticket plainly covers this pull request.
    #: **Narrator-only.** Whether an existing ticket covers a pull request is
    #: a judgement about what two pieces of English mean; the service reports
    #: the unticketed pull request and proposes nothing.
    ATTACH_PR_TO_TICKET = "attach_pr_to_ticket"
    #: Nothing existing covers it.
    #: **Narrator-only**, for the same reason as `ATTACH_PR_TO_TICKET`: the
    #: service cannot know that nothing existing covers the work.
    CREATE_TICKET = "create_ticket"
    #: The work belongs to a different release.
    MOVE_TO_RELEASE = "move_to_release"
    #: On the release, no code, not being finished, and not a design ticket.
    #: **Never emitted by the service** -- `no_code` cannot be told from a design
    #: ticket awaiting its design pull requests, so this is a reviewer's
    #: conclusion after checking `design.unticketed`, not a derivation.
    DROP_FROM_RELEASE = "drop_from_release"
    #: Part done. Say what is unfinished; a person decides where it goes.
    SPLIT = "split"
    #: The work has to reach a line that already shipped, which a minor cannot
    #: carry backwards.
    #: **Narrator-only.** Whether stranded work goes forward onto the release
    #: being cut or backwards onto the line that shipped is a decision about
    #: cost, not a derivation.
    CUT_HOTFIX = "cut_hotfix"


#: The name of the uniqueness rule below, written once — referenced by the
#: migration that creates it and by the test that asserts a duplicate is refused.
PROJECT_VERSION_INDEX = "uq_release_project_version"

#: What makes that index partial, and the whole point of soft-deleting a release.
#:
#: A plain ``UniqueConstraint(project_id, version)`` held the version string
#: forever, whatever the row's status. So "undoing" a release by archiving it
#: looked right and left the number permanently spent: `releases create v1.0.0`
#: answered "already exists" against an archived row nobody could see the point
#: of, and there was no way to free it. Excluding soft-deleted rows is what makes
#: a delete an actual undo.
#:
#: **Archived and deleted are deliberately different**, and the difference is
#: visibility and usage: an archived release is history you can still see and its
#: version stays spent; a deleted one is gone from every view and gives the
#: number back.
#:
#: Written **character for character** the same in the migration that creates it:
#: `alembic check` compares the two as text, so a difference in spacing or quoting
#: reads as a changed index and emits a spurious drop-and-recreate on every run.
#: Same convention, and same reason, as `Scrum.UPDATE_DAY_INDEX`.
_LIVE_ONLY = "deleted_at IS NULL"


class Release(TimestampMixin, table=True):
    """
    Tracks a release (version) within a project.

    A version string (e.g. "v1.0.0") is unique per project, not per org --
    the same version can exist as two entirely separate releases in two
    different projects under the same org (different repos, different
    changelogs). blastoff operates at the project level (one GitHub topic
    per run), matching this.

    Linked to tickets via the loose join: ticket.release == release.version
    AND ticket.project_id == release.project_id.

    A project runs a **two-slot pipeline**: exactly one IN_PROGRESS release (the
    version blastoff cuts next) and one PLANNED release above it (the version
    tickets are being planned into), conventionally the next two minor versions.
    Shipping the first rotates the pair — the second is promoted and a new one
    opens above it. **Two is a cap, not just a floor**: anything open beyond them
    is moved to ARCHIVED, so the plan stays readable. Closed history below the
    high-water mark is unbounded — past versions are a record, not a queue. The
    rules live in
    ``src/services/release_planning.py``; ``ensure_pipeline`` is what maintains
    them, from the release router when a version ships and from repository sync
    as the repair path.

    Rows are therefore created two ways: by the release engine (blastoff /
    github-ops) when a version is cut, and by ``ensure_pipeline`` opening the
    next slot. Both converge on the same (project_id, version) row.

    **The ticket link is deliberately not a foreign key.** ``ticket.release`` is a
    free-text version string (``Optional[str]``, 100 chars, no FK anywhere), so a
    board can label work with whatever it likes and InnoDay still records it. That
    flexibility is the point: the board owns the label, InnoDay owns the release
    process. The cost is that the join is exact string equality — see
    ``release_pipeline.retarget`` for why renaming a version has to rewrite every
    ticket pointing at it in the same transaction.

    **Board sync no longer creates releases.** It used to open a PLANNED row
    whenever a synced ticket carried a version (Jira fixVersions, or a
    semver-shaped Linear label), which let a label on anyone's ticket invent a
    version — BPAI accumulated forty-odd rows that way, on versioning lines it
    had long left. The version string still lands on ``ticket.release``; it just
    no longer becomes a release.
    """

    __tablename__ = "releases"
    __table_args__ = (
        Index(
            PROJECT_VERSION_INDEX,
            "project_id",
            "version",
            unique=True,
            postgresql_where=text(_LIVE_ONLY),
            sqlite_where=text(_LIVE_ONLY),
        ),
    )

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    organization_id: str = Field(
        sa_column_kwargs={"nullable": False},
        foreign_key="organizations.id",
        index=True,
    )
    project_id: str = Field(
        foreign_key="projects.id",
        index=True,
    )

    # The version string — must match ticket.release to join (e.g. "v1.4.0").
    #
    # **max_length must stay equal to `Ticket.release`'s** (see the reasoning
    # recorded there): these are the two halves of the join, and a version that
    # fits here but not there is a release no ticket can point at.
    version: str = Field(max_length=100, index=True)

    # Human-readable name, optional (e.g. "Navigate Permissions Release")
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)

    status: ReleaseStatus = Field(default=ReleaseStatus.PLANNED)

    #: Set when a release is withdrawn rather than shipped. Soft, not a row
    #: deletion, for the reason every other soft delete here is soft: a release
    #: is joined to by version string from `ticket.release`, and vaporising the
    #: row would leave those tickets pointing at nothing with no way to tell
    #: what they had pointed at.
    #:
    #: Readers must filter `deleted_at IS NULL` — the same contract as
    #: `Ticket.deleted_at`. It frees the version for reuse via the partial index
    #: above, so a version that was cut by mistake can be cut again properly.
    deleted_at: Optional[datetime] = Field(default=None, index=True)

    # Narrative summary generated by github-ops at release time (Claude-compiled)
    notes: Optional[str] = Field(default=None)

    # Human-readable bulleted narrative for client/executive audience
    summary: Optional[str] = Field(default=None)

    # Structured per-repo PR inventory: [{repo: str, prs: [{number, title, author}]}]
    changelog: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    #: When this release is *aimed* at, as opposed to when it shipped. A plain
    #: calendar date, not a timestamp: a ship date is agreed as "the 14th", it is
    #: the same day for everyone reading the page, and storing it as a datetime
    #: would invent a time nobody chose and then shift it across time zones.
    #:
    #: Nullable, and stays null unless somebody sets it by hand. Nothing derives
    #: it -- not the pipeline, not sync, not blastoff -- because a guessed date on
    #: a page is read as a commitment. The absence is honest and is rendered as
    #: "no date set".
    target_date: Optional[date] = Field(default=None, sa_column=Column(Date))

    released_at: Optional[datetime] = Field(default=None)

    #: The repositories this release actually covered, recorded when it shipped.
    #:
    #: **Nothing else remembers.** A release's repository set is read live from
    #: the project links every time, so once it ships there is no record of what
    #: it contained -- and the next release cannot tell whether covering fewer
    #: repositories is a deliberate change or a fault.
    #:
    #: It is not hypothetical. A BPAI release covered six repositories instead
    #: of seven, dropped thirteen merged pull requests, and reported the smaller
    #: number with no warning at all, because a sync had deactivated one link
    #: seven minutes earlier. Every figure in that report was internally
    #: consistent.
    #:
    #: Written only when a release is marked RELEASED, and never rewritten: it
    #: is what shipped, not what the project links happen to say today.
    repo_names: Optional[List[str]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )

    # Relationships
    organization: Optional["Organization"] = Relationship(back_populates="releases")
    project: Optional["Project"] = Relationship(back_populates="releases")
