"""Scrums: one timed walk of a project's board, recorded while it happens.

A `Scrum` is the *event*, not a report of it. It opens when someone starts the
walk, and it is written to again at every ticket -- one `ScrumTicketVisit` per
stop, as the stop ends. Nothing is batched at the finish, because a scrum that
is interrupted half way through is the normal case, not the exceptional one: a
call drops, a conversation runs long, someone closes the tab. Batching would
mean those runs left no trace at all, which is exactly the runs whose record is
most worth having.

**A scrum is not a summary.** `Summary` (see `summary.py`) owns the prose --
what happened over a window, generated and superseded. A scrum owns the
*meeting*: who ran it, how long it took, which tickets were visited in what
order, and what was said at each one. The two are linked in one direction only:
`initial_summary_id` records the summary the room read at the start and
`updated_summary_id` the one regenerated at the end. Both are nullable, because
a scrum can be run without either -- there may be no summary for today yet, and
nobody is obliged to regenerate one afterwards.

`total_seconds` is stored rather than derived from `started_at`/`ended_at`,
which measure wall-clock elapsed time and therefore include the gap when the
tab sat open through lunch. The clock the page actually runs is the one worth
comparing week to week, so it is the one recorded.

**A scrum has a kind, and there are two.** A team walk (`ScrumKind.SCRUM`) is a
meeting: one person drives it, everyone attends, and its minutes are final once
written. A personal update (`ScrumKind.UPDATE`) is one person's daily form on the
same project -- what they want brought back and what they are taking on -- and it
is theirs to correct until the day ends. They share this table because they share
every field that decides whether a write is allowed (see
`services/scrum_service.py`); they are told apart by `kind` because without it
*the same row* serves both, and somebody with a half-walked stand-up who opened
their own update wrote their picks onto the meeting's record with nothing on
screen to notice.

**`day` is what makes a record findable again**, and it is *derived* -- always
`started_at.date()`, never a date the caller states. Never from `created_at`
either, which `TimestampMixin` makes *aware* while `started_at` is naive; a
replayed run would land on the day it was uploaded. It is set on **every** row,
both kinds, because it is a fact about the row and cheap to read; what differs is
whether anything is constrained by it.

**One surface can influence it, and that is deliberate rather than a hole.** The
workflow page sends no timestamp at all -- `POST /ui/{org}/scrums` forwards only
`kind` -- so nothing a browser does can move its own day, which is the case that
matters: a tab in UTC+13 filing tomorrow's update. `POST /api/v1/.../scrums` does
accept `started_at`, for a client replaying a run it recorded offline, and that
run's day follows the timestamp it asserts. That is the correct answer for a
replay -- the day the run happened, not the day it was uploaded -- and it is why
the rule is "derived from `started_at`" rather than the flatter "never from a
client", which would be true of one surface and read as true of both.

**The uniqueness rule is partial, and the partiality is the design.** See
`UPDATE_DAY_INDEX`: ``UNIQUE(project_id, run_by_user_id, day) WHERE kind =
'update'``. An update is a *form* -- there is exactly one per person per project
per day, and re-entering it means correcting the one that exists. A scrum is an
*event*, and a team can legitimately hold two in a day: a call that dropped and
was restarted, a session split across a break, two halves of a team in different
timezones. Putting `kind` inside a whole-table unique key would have made the
second meeting impossible, which is a capability nobody asked to lose.

So the two kinds are keyed differently on purpose, and `scrum_service.open_scrum`
says which is which: an update resumes the day's row whether it is closed or not,
a scrum resumes only its own un-ended row and otherwise starts a new one.

**Several columns are NULL for an update, and that is the honest record.** An
update has no clock and walks no board, so `total_seconds` and `lingering_count`
are NULL; it feeds no prose, so `initial_summary_id` and `updated_summary_id` are
too. **Anything that aggregates scrum duration must therefore filter on `kind`** --
averaging over both kinds averages a number against rows that never had one.

All datetimes here are **naive UTC**, like the rest of this schema -- see
CLAUDE.md and `summary.notes_updated_at` for why a single aware column in a
naive table is a trap rather than a nicety.
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, Date, ForeignKey, Index, Integer, Text, text
from sqlmodel import Field
from sqlmodel.sql.sqltypes import AutoString

from src.domain._base import TimestampMixin


class ScrumKind(str, Enum):
    """What was recorded: a team walk, or one person's daily update.

    Stored as its **value**, not its name -- the column is a plain string rather
    than a database enum, so adding a third kind later is a code change and not a
    migration on every backend. `TicketStatus` is the same shape for the same
    reason.
    """

    SCRUM = "scrum"
    UPDATE = "update"


#: The name of the rule below, written once. It is referenced by the migration that
#: creates it and by the test that asserts the database refuses a duplicate, and a
#: name spelled twice is a name that gets spelled two ways.
UPDATE_DAY_INDEX = "uq_scrums_update_per_runner_day"

#: The predicate that makes the index partial. Written **character for character**
#: the same in the migration that creates it: `alembic check` compares the two as
#: text, so a difference in spacing or quoting reads to it as a changed index and
#: it emits a spurious drop-and-recreate on every run. Same convention, and same
#: reason, as `Ticket.__table_args__`'s two partial indexes.
_UPDATES_ONLY = "kind = 'update'"


class Scrum(TimestampMixin, table=True):
    """One run of the scrum workflow over one project's board."""

    __tablename__ = "scrums"

    #: One personal update per person per project per day -- and **only** for the
    #: personal update, which is why this is a partial `Index(unique=True)` rather
    #: than a `UniqueConstraint`. A constraint cannot carry a predicate, and a
    #: whole-table one including `kind` would forbid a second *team scrum* in a
    #: day, which is a thing teams legitimately do (see the module docstring).
    #:
    #: Stated in the schema rather than left to `open_scrum`'s lookup, because that
    #: lookup is a read followed by a write and two concurrent requests both pass
    #: it -- which is precisely the case a dropped response and a retry produce.
    __table_args__ = (
        Index(
            UPDATE_DAY_INDEX,
            "project_id",
            "run_by_user_id",
            "day",
            unique=True,
            postgresql_where=text(_UPDATES_ONLY),
            sqlite_where=text(_UPDATES_ONLY),
        ),
    )

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    # ------------------------------------------------------------------ scope
    organization_id: str = Field(foreign_key="organizations.id", index=True)
    project_id: str = Field(foreign_key="projects.id", index=True)
    run_by_user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Who ran the walk. Never null -- a scrum has a driver.",
    )

    # ------------------------------------------------------------------- kind
    kind: str = Field(
        default=ScrumKind.SCRUM.value,
        sa_column=Column(
            AutoString(20),
            nullable=False,
            # Correct by construction for every row that already exists: the team
            # walk is the only kind that has ever been recorded, so the backfill
            # is not a guess about history, it is a statement of it.
            server_default=ScrumKind.SCRUM.value,
        ),
        description="`ScrumKind` value: 'scrum' for a team walk, 'update' for a person's day.",
    )

    # ------------------------------------------------------------------ clock
    started_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Naive UTC. Stamped server-side when the walk opens.",
    )
    day: date = Field(
        # A factory rather than a required argument, so a `Scrum()` built with a
        # defaulted `started_at` cannot end up with a day from a different one.
        # Every real caller goes through `scrum_service.open_scrum`, which passes
        # `started_at.date()` explicitly -- the two readings agree because both
        # read the same clock in the same call.
        default_factory=lambda: datetime.utcnow().date(),
        sa_column=Column(Date, nullable=False, index=True),
        description=(
            "The UTC calendar date of `started_at`, always derived and never "
            "stated by a caller. The boundary is UTC midnight, matching "
            "`scrum_service.todays_scrum_summary`: there is no timezone column on "
            "`users`, so anything else would invent one."
        ),
    )
    ended_at: Optional[datetime] = Field(
        default=None,
        description=(
            "Naive UTC. NULL while the scrum is still open -- and it stays NULL "
            "for a run that was abandoned, which is how an abandoned run is told "
            "apart from a finished one."
        ),
    )
    total_seconds: Optional[int] = Field(
        default=None,
        description=(
            "The page's own clock, not `ended_at - started_at`: the latter "
            "counts the tab sitting open through an interruption. **NULL for "
            "every `kind='update'` row** -- a form has no clock -- so anything "
            "aggregating this must filter on `kind`."
        ),
    )

    # --------------------------------------------------------------- summaries
    initial_summary_id: Optional[str] = Field(
        default=None,
        foreign_key="summaries.id",
        index=True,
        description="The summary the room read at the start, when one existed.",
    )
    updated_summary_id: Optional[str] = Field(
        default=None,
        foreign_key="summaries.id",
        index=True,
        description="The summary regenerated at the end, when one was.",
    )

    # ----------------------------------------------------------------- outputs
    transcript_url: Optional[str] = Field(default=None, max_length=1000)
    lingering_count: Optional[int] = Field(
        default=None,
        description=(
            "How many tickets were still sitting where they were at the last "
            "scrum. Recorded at wrap-up, so NULL means 'not yet counted' rather "
            "than zero."
        ),
    )
    notes_markdown: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="What a person typed at wrap-up, kept out of the summary prose.",
    )


class ScrumTicketVisit(TimestampMixin, table=True):
    """One stop on the walk: a ticket, how long it took, and what was decided.

    Written as the stop ends, not collected at the finish -- see the module
    docstring. `position` therefore records the order the walk actually took,
    which need not match the order the board was in when it started.
    """

    __tablename__ = "scrum_ticket_visits"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    scrum_id: str = Field(foreign_key="scrums.id", index=True)
    ticket_id: int = Field(
        # `ticket.id` is an autoincrement integer on a singular table name --
        # unlike nearly every other primary key in this schema, which is a
        # string UUID. Same note as `SummaryItem.ticket_id`.
        sa_column=Column(Integer, ForeignKey("ticket.id"), nullable=False, index=True),
    )

    position: int = Field(
        description="0-based order this ticket was reached in, within the scrum."
    )
    seconds: int = Field(description="How long the room spent on this ticket.")
    status_at_visit: str = Field(
        max_length=50,
        description=(
            "The ticket's status when it was reached, as a plain string rather "
            "than the enum: this is a historical observation, and re-labelling "
            "or retiring a status later must not rewrite what was true then."
        ),
    )
    comment: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="What was said. NULL means nothing was typed, not nothing said.",
    )
    moved_to: Optional[str] = Field(
        default=None,
        max_length=50,
        description="The status it was moved to during the stop, if it moved.",
    )
    push_error: Optional[str] = Field(
        default=None,
        max_length=500,
        description=(
            "Why the board never got this move, when the local write succeeded "
            "and the outbound push did not. NULL is the ordinary case and means "
            "'nothing outstanding' -- both 'pushed cleanly' and 'there was "
            "nothing to push to', which are the same thing to a reader.\n\n"
            "**A column rather than a return value**, because the failure has to "
            "outlive the response that reported it: the answer is painted once "
            "and then the tab is closed, while the board stays out of step until "
            "somebody acts. 500 characters, matching "
            "`BoardRegistration.error_message`.\n\n"
            "**What is stored here is read by every member of the org**, so it is "
            "a *classified* message and never `str(exc)` -- a DBAPI error "
            "stringifies to SQL with its bound parameters, and a connection error "
            "to host, port and user. See `services/ticket_status_service.py`.\n\n"
            "Deliberately **not** `BoardRegistration.errored_at`: that means 'the "
            "last sync of this board failed' and the dashboard's status icon "
            "reads it, so one ticket's push failure reddening the whole board "
            "would misreport."
        ),
    )
    withdrawn_at: Optional[datetime] = Field(
        default=None,
        description=(
            "When this pick was taken back off the update, or NULL while it is "
            "part of it.\n\n"
            "**A withdrawn visit is kept, not deleted, and that is a correctness "
            "requirement rather than tidiness.** The row carries `comment_id` and "
            "`comment_error` -- the only record that a comment reached the "
            "board, or that it did not -- and a withdrawal cannot un-say a "
            "sentence a client's board has already been given. Deleting the row "
            "threw that evidence away, so a board that was down when the comment "
            "was first sent, followed by a withdrawal and a re-tick, ended with "
            "the board never having the comment and the page reporting no error "
            "at all. Silent non-delivery is the worst outcome this path has, and "
            "it was reachable by somebody changing their mind twice.\n\n"
            "A withdrawn visit is **not part of the update**, and here is the "
            "complete list of the places that have to know it -- every query "
            "over this table in `src/`, because a new lifecycle state's defining "
            "hazard is leaking into a reader nobody edited (one of these was "
            "missed exactly that way, and served withdrawn picks over `/api/v1` "
            "while `visit_count` in the same payload excluded them):\n\n"
            "* `scrum_service.apply_recorded_moves` -- it moves nothing;\n"
            "* `scrum_service.visit_count` -- it is not counted;\n"
            "* `scrum_service.replace_picks` -- it is not returned as held;\n"
            "* `routers.webui.data.scrum_activity_today` -- it is not resumed or "
            "rendered;\n"
            "* `routers.scrums.get_scrum` -- it is not served by the API.\n\n"
            "Two queries deliberately do **not** filter it out, and both then "
            "check the flag themselves: `replace_picks`' own lookup, which needs "
            "to find the row in order to revive it, and "
            "`deliver_recorded_comments`, for the one thing that still happens to "
            "a withdrawn visit -- an outstanding `comment_error` is still "
            "retried, because the board is still out of step and this row is what "
            "says so.\n\n"
            "Re-ticking the same ticket **revives this row** rather than "
            "inserting a second one, which is what keeps the memory continuous."
        ),
    )
    comment_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer, ForeignKey("ticket_comment.id"), nullable=True, index=True
        ),
        description=(
            "The `TicketComment` this visit's `comment` was delivered as, or NULL "
            "when it has not been delivered.\n\n"
            "**The idempotence marker, and it has to be durable.** A personal "
            "update is re-enterable and re-closable all day, so submitting is not "
            "a once-only event; without a record of what was already delivered, "
            "every re-submit would post the same sentence to the board again. It "
            "points at the local row rather than holding a copy of the text, so "
            "'has this changed since?' is answered against the thing that was "
            "actually sent.\n\n"
            "An **edited** comment is a new comment: the text no longer matches "
            "what this points at, so a fresh `TicketComment` is written and "
            "pushed. A board comment cannot be edited through `add_comment`, and "
            "silently keeping the old one on the board while showing the new one "
            "here is the disagreement this whole path exists to avoid."
        ),
    )
    comment_error: Optional[str] = Field(
        default=None,
        max_length=500,
        description=(
            "Why the board never got this visit's comment, when the local write "
            "succeeded and the outbound push did not. Same shape, same ceiling "
            "and the same classification rule as `push_error` -- and **separate "
            "from it on purpose**: the two pushes fail independently, and one "
            "column would let a clean status push clear a still-true comment "
            "failure (or the reverse), which is exactly the erasure PR 2's review "
            "found on `push_error` itself.\n\n"
            "NULL means nothing outstanding. That covers 'delivered', 'nothing to "
            "deliver to', and 'this board type has no comments' -- the last of "
            "which is a capability fact rather than a failure, so recording it "
            "here would make it permanent and ask for a retry forever."
        ),
    )
