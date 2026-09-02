"""Assembling a summary: three gates, then the work (PF-398).

**Assembly is server-side; narration is not.** This service returns structured,
assembled data -- which tickets moved, who owns them, what code touched them --
and any prose it already had cached. It never writes prose and never calls an
LLM. The calling Claude session writes the words and posts them back through
``POST .../projects/{p}/summaries``, exactly the split
``get_board_summary_data`` / ``save_board_summary`` already uses for boards.

Three gates run in order, each an escape hatch. Work only reaches assembly when
all three decline to short-circuit:

**1. Freshness.** If the project's boards were *successfully* synced less than an
hour ago, do not sync at all -- a summary is a read, and making every read
trigger a board sync would turn a cheap question into an expensive one. Older
than that, one sync runs, scoped to the window via `options["since"]`, and
bounded by `SYNC_TIMEOUT_SECONDS`: a board pull inside a synchronous GET is a
plausible gateway timeout, and a 504 would kill the request before the soft-fail
path could return anything. On timeout the engine summarises what is on disk.
This changes nothing about how sync behaves anywhere else -- `since` is only
sent when a caller supplies it, and no other caller does.

**2. Cache.** A live summary (`superseded_by_id IS NULL`) for the same
``(project, user, type, window_spec)`` written under an hour ago is returned
verbatim.

*The key is ``window_spec``, never a computed timestamp.* "The last 3 days"
asked twice is the same question; the two resolved `period_start`s are ~30
minutes apart and would never compare equal, so a cache keyed on them would miss
every single time while looking like it worked. This was caught in design
review, and `src/domain/summary.py` is built around the same distinction.

**3. Fingerprint.** `source_fingerprint` covers commit SHAs, every
``(ticket_id, status, updated_at)`` tuple, **and** every open PR's
``(url, state, updated_at)``. All three are load-bearing:

* commits alone miss a ticket that moved TODO → IN REVIEW with no new code, and
  would answer "nothing changed" to a question whose answer just changed;
* tickets alone miss a day of pushes to an open branch;
* and commits are read from the **default branch only**, so an unmerged PR
  contributes no SHAs at all -- without the PR's own timestamp a week of work on
  a live branch is invisible to this gate.

A ticket with zero commits would also have a permanently empty fingerprint and
so be permanently "unchanged" -- also caught in review. Matching the last run
means the stored `body_markdown` is reused and the window is restamped; nothing
is regenerated and no new row is written, because nothing about the *content*
changed and superseding a row with a byte-identical copy is churn, not history.

Only past all three does assembly run, and only the *narrated* result is
persisted -- by superseding the previous live row, never overwriting it, and
recording a `ProjectTimeline` entry alongside.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
)

from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.adapters.board_assignee import BoardAssignee
from src.domain.board import BoardRegistration, BoardSyncHistory, SyncStatus
from src.domain.organization import OrganizationMembership
from src.domain.project import Project, ProjectRepository
from src.domain.project_timeline import TimelineEventType
from src.domain.release import Release
from src.domain.repository import Repository
from src.domain.repository_pull_request import RepositoryPullRequest
from src.domain.summary import (
    Attribution,
    GeneratedBy,
    Summary,
    SummaryItem,
    SummaryType,
)
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, UserIdentity
from src.services.code_activity import CodeActivity, CodeActivityFetcher
from src.services.identity_resolution import IdentityResolutionService
from src.services.project_timeline_writer import upsert_daily_timeline_entry
from src.services.ticket_matching import (
    tickets_by_ref,
)
from src.utils.time_windows import (
    WINDOW_ALIASES,
    WINDOW_GRAMMAR_HINT,
    as_utc,
    normalize_window,
    parse_window,
)

logger = logging.getLogger(__name__)

#: How recently the boards must have synced for gate 1 to skip syncing.
SYNC_FRESHNESS = timedelta(hours=1)
#: How recently a live summary must have been written for gate 2 to reuse it.
CACHE_TTL = timedelta(hours=1)
#: Active items shown before the rest are rolled into the footer count.
ACTIVE_CAP = 5
#: Items shown in every other enumerated block before it, too, is rolled into a
#: count. Capping only the active list left `no_work_detected` and
#: `unassigned_work_happening` unbounded, so a project with 400 open assigned
#: tickets answered a "what happened this week?" question with 400 lines.
BLOCK_CAP = 20
#: How long gate 1 waits for its sync before giving up and using stale data.
#: A board pull inside a synchronous GET is a plausible gateway timeout, and a
#: 504 kills the request before the soft-fail path can return anything at all --
#: so the engine bounds the wait itself rather than letting a proxy do it.
SYNC_TIMEOUT_SECONDS = 25.0

#: A ticket in one of these is finished; it is not "idle work" and never
#: belongs in the no-work or unassigned-idle blocks, however long ago it moved.
TERMINAL_STATUSES = {TicketStatus.DONE, TicketStatus.CANCELLED}

#: What marks a `window_spec` as a **release scope** rather than a duration.
#:
#: A release scope narrows the ticket universe, so it is a different question
#: from "the last three days" and must not share its cache entry -- and
#: `window_spec` *is* the cache key. It also has to be **stable**: the spec this
#: replaced was "days since the last release", which minted `5d` on Monday and
#: `6d` on Tuesday, so every morning missed the cache and orphaned the previous
#: day's note. A release names itself, so the key can stand still while the
#: calendar moves.
#:
#: `''` is not available for this: it is the board-scoped append path's sentinel
#: and the one value both live-uniqueness indexes exempt (`src/domain/summary.py`).
RELEASE_SPEC_PREFIX = "release:"
#: How far back a release-scoped run's activity window may reach.
#:
#: The window is measured from when the release row was opened, which for a
#: stale one is months ago -- and `period_start` is what bounds both the board
#: sync and the per-repo GitHub fetches inside a synchronous GET. BPAI carries
#: ~40 rows board sync invented from version labels years old, so this is not
#: hypothetical.
RELEASE_SPAN_CAP = timedelta(days=90)
#: The window a release-scoped run uses when the version matches no release row
#: at all. `Ticket.release` is free text a board wrote, so a legitimate scope may
#: name a version InnoDay has no row for; that is a query with an answer, not an
#: error.
RELEASE_SPAN_FALLBACK = timedelta(days=28)
#: `summaries.window_spec` is `String(64)`; a spec longer than that is a
#: DataError at INSERT rather than a validation failure at the door.
_WINDOW_SPEC_MAX = 64


class InvalidWindowSpec(ValueError):
    """The caller asked for a window nobody can resolve."""


def is_release_spec(spec: Optional[str]) -> bool:
    """Whether this `window_spec` names a release rather than a duration."""
    return str(spec or "").strip().lower().startswith(RELEASE_SPEC_PREFIX)


def release_spec(version: str) -> str:
    """``'v1.9.0'`` → ``'release:v1.9.0'``, the spec such a summary is keyed on."""
    return f"{RELEASE_SPEC_PREFIX}{str(version or '').strip()}"


def release_spec_version(spec: str) -> str:
    """The version out of a release spec, **byte-exact**.

    Sliced rather than lowercased: ``Ticket.release`` is matched by string
    equality and nothing normalises either side, so folding `V1.10.0` to
    `v1.10.0` here would name a release whose tickets are invisible to the very
    filter the spec exists to express.
    """
    return str(spec or "").strip()[len(RELEASE_SPEC_PREFIX) :].strip()


def parse_window_spec(spec: str) -> timedelta:
    """``'3d'`` → 3 days. Raises `InvalidWindowSpec` on anything else.

    The grammar itself lives in `src/utils/time_windows.py`, shared with the
    CLI's `--since`: it used to be declared twice, byte for byte, in modules
    that do not import each other. Only the exception type is local -- the
    engine's callers catch `InvalidWindowSpec` and answer 422.

    Accepts the aliases too, so a caller that says `day` gets 1 day rather than
    a 422 that reads like the window is unsupported.

    A **release** spec is refused rather than given a stand-in duration: it is
    anchored to when the release opened, not to a length, and inventing a length
    here would hand every caller a period that quietly disagreed with the one
    `resolve_scope` uses. Ask `resolve_scope` instead -- it answers for both
    kinds of scope.
    """
    if is_release_spec(spec):
        raise InvalidWindowSpec(
            f"{spec!r} is a release scope, not a duration — resolve it with "
            "SummaryService.resolve_scope"
        )
    try:
        window = parse_window(WINDOW_ALIASES.get(str(spec or "").strip().lower(), spec))
    except ValueError:
        raise InvalidWindowSpec("window_spec must cover at least one unit")
    if window is None:
        raise InvalidWindowSpec(
            f"window_spec must be {WINDOW_GRAMMAR_HINT}; got {spec!r}"
        )
    return window


def canonical_window_spec(spec: str) -> str:
    """The spec as the engine should *store* it, or `InvalidWindowSpec`.

    Separate from `parse_window_spec` because the two answer different
    questions: that one asks "how long is this window", this one asks "what is
    this window called". Both matter, and only the second one is a cache key --
    persisting the caller's spelling is what let `'3d'`, `'3D'` and `'day'`
    become three cache entries covering the same three days.

    A release scope is canonical too, and canonical here means **the prefix
    normalised and the version left exactly as given** -- see
    `release_spec_version` for why the version must not be folded.
    """
    if is_release_spec(spec):
        version = release_spec_version(spec)
        if not version:
            raise InvalidWindowSpec(
                "a release scope must name a version, e.g. 'release:v1.9.0'"
            )
        canonical_release = release_spec(version)
        if len(canonical_release) > _WINDOW_SPEC_MAX:
            # `summaries.window_spec` is String(64) while `Ticket.release` allows
            # 100, so a long enough version would be a DataError at INSERT --
            # after the prose was written, and only on Postgres.
            raise InvalidWindowSpec(
                f"release version too long for a window spec (max "
                f"{_WINDOW_SPEC_MAX - len(RELEASE_SPEC_PREFIX)} characters)"
            )
        return canonical_release
    try:
        canonical = normalize_window(spec)
    except ValueError:
        # `0d` and friends: parses as a window, covers nothing. Raised bare by
        # `normalize_window`, and the routers only catch `InvalidWindowSpec` --
        # so letting it through would be a 500 where a 422 belongs.
        raise InvalidWindowSpec("window_spec must cover at least one unit")
    if canonical is None:
        raise InvalidWindowSpec(
            f"window_spec must be {WINDOW_GRAMMAR_HINT}; got {spec!r}"
        )
    return canonical


class SummaryOutcome(str, Enum):
    """Which gate answered, or that none did."""

    CACHED = "cached"  # gate 2: a live summary under an hour old
    UNCHANGED = "unchanged"  # gate 3: same fingerprint, prose reused
    ASSEMBLED = "assembled"  # assembled fresh; needs narrating


class Block(str, Enum):
    """Which part of the summary a line belongs to.

    There is deliberately no `UNASSIGNED_IDLE` member. One existed and nothing
    ever produced it: `_assemble` *counts* the unassigned backlog
    (`unassigned_idle_count`) and never builds a line for it, because
    enumerating it would drown everything above it. An enum member with no
    writer reads as a block a caller might receive, and would have been
    accepted by `SummaryItemPayload.block` from a caller that invented it.
    """

    ACTIVE = "active"
    NO_WORK = "no_work_detected"
    UNASSIGNED_ACTIVE = "unassigned_work_happening"
    UP_NEXT = "up_next"


#: Which block wins when one ticket was echoed back under several of them.
#: Ordered by how much the row says that nothing else records:
#: an active line carries the code anchor; `no_work_detected` is an explicit
#: "nothing happened" with no other home; `up_next` is re-derivable from the
#: ticket's assignment plus the absence of activity, so it yields.
_BLOCK_PRECEDENCE: Dict[str, int] = {
    Block.ACTIVE.value: 0,
    Block.UNASSIGNED_ACTIVE.value: 1,
    Block.NO_WORK.value: 2,
    Block.UP_NEXT.value: 3,
}


def mirror_release_notes(
    session: Session,
    *,
    organization_id: str,
    project_id: str,
    window_spec: str,
    body_markdown: Optional[str],
) -> Optional[str]:
    """A release-scoped summary *is* that release's notes. Keep the row in step.

    **One artifact, two doors.** A release's notes and a release-scoped stand-up
    were two stores of the same prose: `release.summary`, written at tag time,
    and a `Summary` row, written by the narrator. Whichever door somebody came
    through, they saw the other one's absence -- and the team could not tell it
    was one system.

    The `Summary` row is canonical, because it is the one with items, a
    fingerprint, an author and a history. `Release.summary` is a mirror of it,
    kept because the release card and the release API read it.

    Returns the version it mirrored onto, or `None` when the spec was not a
    release or no such release exists. Never raises: a summary is worth storing
    even when the mirror cannot be written.
    """
    # `is_release_spec`, not a raw `startswith`: every other reader of a window
    # spec strips and lowercases, and `persist` canonicalises internally -- so
    # `Release:v1.11.0` was stored as a release summary while this gate said no,
    # and the release card went on reading "nothing written yet".
    if not is_release_spec(window_spec):
        return None
    version = release_spec_version(str(window_spec or "").strip())
    if not version or not body_markdown:
        return None
    try:
        release = session.exec(
            select(Release).where(
                Release.organization_id == organization_id,
                Release.project_id == project_id,
                Release.version == version,
                Release.deleted_at.is_(None),
            )
        ).first()
    except SQLAlchemyError:
        logger.warning("Could not read release %s to mirror its notes", version)
        return None
    if release is None:
        return None
    release.summary = body_markdown
    release.touch()
    session.add(release)
    return version


def _people(item: Dict[str, Any]) -> Optional[List[str]]:
    """Everyone credited on a line, or `None` when nobody was.

    A single string is accepted and wrapped: a caller with one name should not
    have to know this is a list, and a bare string stored as a JSON list of
    characters is the failure that shape invites.

    `None` rather than `[]` for the empty case -- an unattributed line is a
    different thing from a line somebody deliberately credited to nobody, and
    the column has to be able to say which.
    """
    people = item.get("people")
    if people is None:
        display = item.get("assignee_display")
        return [display] if display else None
    if isinstance(people, str):
        return [people] if people else None
    cleaned = [str(p) for p in people if p]
    return cleaned or None


#: What a stored pull request keeps. Everything else on an assembled PR -- the
#: title, the branch, the author, `matched_by` -- belongs to the window the
#: release was assembled over, and a release line does not show it.
_PR_KEYS = ("repo", "number", "url", "merged")


def _prs(item: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Every pull request on a line, trimmed to what the line renders.

    Trimmed rather than stored whole: an assembled pull request carries a
    description, and freezing prose from GitHub inside a summary row means two
    copies of it drifting apart.

    Falls back to the single `pr_url` a stand-up line carries, so one shape comes
    out of the column whether the row arrived from a release or a stand-up.
    """
    prs = item.get("prs")
    if not prs:
        url = item.get("pr_url")
        if not url:
            return None
        return [
            {
                "repo": item.get("repo"),
                "number": None,
                "url": url,
                "merged": (item.get("pr_state") or "").lower() == "merged",
            }
        ]
    trimmed = [
        {key: pr.get(key) for key in _PR_KEYS} for pr in prs if isinstance(pr, dict)
    ]
    return trimmed or None


def _block_rank(item: Dict[str, Any]) -> int:
    block = item.get("block")
    return _BLOCK_PRECEDENCE.get(getattr(block, "value", block), 99)


def _no_work(item: Dict[str, Any]) -> bool:
    """Whether a written line is a "no work detected" one.

    **The block and the boolean are two spellings of the same fact, and only
    one of them survives a round trip.** `SummaryLine.to_dict` emits
    `"block": "no_work_detected"`; `SummaryItem` records a `no_work_detected`
    boolean and no block at all. A caller posting an assembler line back
    verbatim -- which is exactly what the write path is for -- therefore stored
    `False`, pydantic having dropped the key it did not know, and the panel then
    let idle rows compete for the five active slots. The suite missed it because
    every test set the boolean by hand.

    Either spelling is accepted, and neither overrides an explicit True.
    """
    if bool(item.get("no_work_detected", False)):
        return True
    block = item.get("block")
    return getattr(block, "value", block) == Block.NO_WORK.value


def _looks_like_email(value: str) -> bool:
    """Whether a board's word for a person is an address rather than a name.

    Deliberately not a validator -- nothing here rejects anything, so the only
    question is which field to offer the resolver, and `a@b` is enough to answer
    it. Guards against a display name containing an `@` (`@karl`, a Slack-style
    handle) being compared against `users.email`.
    """
    local, _, domain = value.partition("@")
    return bool(local) and "." in domain and " " not in value


@dataclass
class SummaryLine:
    """One assembled line, shaped to become a `SummaryItem` unchanged."""

    block: Block
    ticket_id: Optional[int] = None
    ticket_ref: Optional[str] = None
    ticket_summary: Optional[str] = None
    status: Optional[str] = None
    assignee_user_id: Optional[str] = None
    assignee_display: Optional[str] = None
    assignee_unmapped: bool = False
    attribution: Attribution = Attribution.NONE
    repo: Optional[str] = None
    branch: Optional[str] = None
    pr_url: Optional[str] = None
    pr_state: Optional[str] = None
    occurred_at: Optional[datetime] = None
    commit_count: int = 0
    rank: int = 0

    @property
    def owner_label(self) -> Optional[str]:
        """How to render the owner, including the unmapped case.

        The raw board string is kept in `assignee_display` (that is the model's
        contract -- losing it would lose the only record of who the board
        thought owned this); the decoration lives here, in the view.
        """
        if self.assignee_unmapped and self.assignee_display:
            return f"@{self.assignee_display} (unmapped)"
        if self.assignee_display:
            return self.assignee_display
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block": self.block.value,
            "ticket_id": self.ticket_id,
            "ticket_ref": self.ticket_ref,
            "summary": self.ticket_summary,
            "status": self.status,
            "assignee_user_id": self.assignee_user_id,
            "assignee_display": self.assignee_display,
            "assignee_unmapped": self.assignee_unmapped,
            "owner_label": self.owner_label,
            "attribution": self.attribution.value,
            "repo": self.repo,
            "branch": self.branch,
            "pr_url": self.pr_url,
            "pr_state": self.pr_state,
            "occurred_at": (self.occurred_at.isoformat() if self.occurred_at else None),
            "commit_count": self.commit_count,
            "rank": self.rank,
        }


@dataclass
class SummaryAssembly:
    """What the engine hands back: structured data, and any cached prose."""

    outcome: SummaryOutcome
    window_spec: str
    period_start: datetime
    period_end: datetime
    summary_type: SummaryType
    user_id: Optional[str] = None
    synced: bool = False
    #: Why gate 1's sync did not land, when it did not. `synced=False` alone
    #: cannot be acted on -- "there is no board" and "the board's OAuth consent
    #: was revoked" are the same flag and very different problems, and only one
    #: of them means every figure below is measured against stale tickets.
    sync_error: Optional[str] = None

    active: List[SummaryLine] = field(default_factory=list)
    active_total: int = 0
    no_work_detected: List[SummaryLine] = field(default_factory=list)
    no_work_total: int = 0
    unassigned_active: List[SummaryLine] = field(default_factory=list)
    unassigned_active_total: int = 0
    unassigned_idle_count: int = 0
    up_next: List[SummaryLine] = field(default_factory=list)
    up_next_total: int = 0

    unmapped_assignee_count: int = 0
    #: The release this summary is scoped to, or None when it covers the whole
    #: project. Everything below -- the blocks, the counts, the fingerprint -- is
    #: measured inside that scope, so a reader that ignores this field would read
    #: a slice as the whole.
    release: Optional[str] = None
    #: How many of the project's tickets are on this release.
    #: **None, not 0**, when there is no release scope: "not a release summary"
    #: and "a release with nothing on it" are different facts and the caller must
    #: not have to guess which it got. Same for the field below.
    release_ticket_count: Optional[int] = None
    #: How many of the project's tickets are on **no** release at all -- the size
    #: of what a release-scoped summary leaves out. `Ticket.release` is only set
    #: by sync from a `fixVersions`/label or an explicit `tickets update
    #: --release`, so on most projects this is nearly all of them: a release
    #: summary is a slice, and one that does not say so is a subset reported as
    #: the whole.
    tickets_without_release_count: Optional[int] = None
    source_fingerprint: Dict[str, Any] = field(default_factory=dict)
    summary: Optional[Summary] = None
    body_markdown: Optional[str] = None
    #: A person's note on this summary, carried through so a caller rendering a
    #: cached result shows the human half as well as the generated one.
    notes_markdown: Optional[str] = None
    #: When that note last changed, so a reader can tell a fresh one from a
    #: month-old one that nobody has cleared.
    notes_updated_at: Optional[datetime] = None

    @property
    def footer(self) -> str:
        return f"{len(self.active)} of {self.active_total} active shown"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "summary_type": self.summary_type.value,
            "window_spec": self.window_spec,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "user_id": self.user_id,
            "synced": self.synced,
            "sync_error": self.sync_error,
            "active": [line.to_dict() for line in self.active],
            "active_total": self.active_total,
            "no_work_detected": [line.to_dict() for line in self.no_work_detected],
            "no_work_total": self.no_work_total,
            "unassigned_work_happening": [
                line.to_dict() for line in self.unassigned_active
            ],
            "unassigned_work_happening_total": self.unassigned_active_total,
            "unassigned_idle_count": self.unassigned_idle_count,
            "up_next": [line.to_dict() for line in self.up_next],
            "up_next_total": self.up_next_total,
            "footer": self.footer,
            "release": self.release,
            "release_ticket_count": self.release_ticket_count,
            "tickets_without_release_count": self.tickets_without_release_count,
            "unmapped_assignee_count": self.unmapped_assignee_count,
            "source_fingerprint": self.source_fingerprint,
            "body_markdown": self.body_markdown,
            "notes_markdown": self.notes_markdown,
            "notes_updated_at": (
                self.notes_updated_at.isoformat() if self.notes_updated_at else None
            ),
            "summary_id": self.summary.id if self.summary else None,
        }


class ReleaseCounts(NamedTuple):
    """The boundary a release-scoped summary reports, or ``(None, None)``.

    Named once, in one place, because these are exactly the two extra keys
    :meth:`SummaryService.compute_fingerprint` writes under a release scope -- and
    the key *set* is what gate 3 compares with ``==``. A third boundary count
    added here reaches the fingerprint without a call site to remember.
    """

    release_ticket_count: Optional[int]
    tickets_without_release_count: Optional[int]


@dataclass
class FingerprintInputs:
    """A fingerprint, and everything it was computed from.

    The inputs come back with it because ``assemble`` goes on to build the summary
    from the same rows it fingerprinted. Re-reading them would mean the prose and
    the fingerprint stored beside it describe two different moments.
    """

    fingerprint: Dict[str, Any]
    tickets: List[Ticket]
    activities: List[CodeActivity]
    window_spec: Optional[str]
    release: Optional[str]
    period_start: datetime
    counts: ReleaseCounts


#: ``(project, since, now, requested_by) -> did a sync run``
SyncRunner = Callable[[Project, datetime, datetime, Optional[str]], Awaitable[bool]]


class SummaryService:
    """The three gates, the assembly, and the supersede-on-write."""

    def __init__(
        self,
        session: Session,
        *,
        activity_fetcher: Optional[CodeActivityFetcher] = None,
        sync_runner: Optional[SyncRunner] = None,
    ) -> None:
        self.session = session
        self.activity_fetcher = activity_fetcher or CodeActivityFetcher(session)
        self._sync_runner = sync_runner or self._run_board_sync
        #: Why the last gate-1 sync did not land. Set by `_run_board_sync`;
        #: an injected `sync_runner` simply leaves it None, which reads as
        #: "no reason recorded" rather than as a false all-clear.
        self.last_sync_error: Optional[str] = None
        # Keyed on (org, project, handle), not the handle alone: identity
        # resolution is scoped to both, so a bare-handle key would hand one
        # project's answer to another if an instance is ever reused.
        self._identity_cache: Dict[Tuple[str, str, str], Optional[str]] = {}
        # `assemble` and the route both want this list on every request, and it
        # is a GROUP BY over the project's tickets. Memoised per instance, which
        # is per request -- nothing in a request writes `Ticket.assignee`.
        self._unmapped_cache: Dict[str, List[Dict[str, Any]]] = {}

    # ================================================================= gate 1

    def latest_sync(self, project_id: str) -> Optional[BoardSyncHistory]:
        """The most recent *finished* sync of any board on this project.

        **A dry run is not evidence either, and that one bit hardest.** A preview
        recorded a completed row with counts, so this returned it, gate 1 read the
        board as fresh and skipped the real sync for the whole freshness window --
        a dry run suppressed the very sync it was meant to preview. Excluded here
        rather than at the call site, because every reader of "when did this
        project last sync" wants the same answer.

        A pending or in-progress run is not evidence of anything, so
        `completed_at IS NULL` rows are excluded rather than ordered last --
        **the exclusion, not the ordering, is what does the work.** On Postgres
        `ORDER BY completed_at DESC` puts NULLs *first*, so without the filter a
        run that started two minutes ago would outrank a genuinely fresh
        completed one and force a needless whole-board pull on every read.
        """
        return self.session.exec(
            select(BoardSyncHistory)
            .join(
                BoardRegistration,
                BoardRegistration.id == BoardSyncHistory.board_registration_id,
            )
            .where(
                BoardRegistration.project_id == project_id,
                BoardSyncHistory.completed_at.is_not(None),
                BoardSyncHistory.dry_run.is_(False),  # type: ignore[union-attr]
            )
            .order_by(BoardSyncHistory.completed_at.desc())
        ).first()

    def running_syncs(self, project_id: str) -> List[BoardSyncHistory]:
        """Every board sync on this project that has started and not reported.

        The exact complement of :meth:`latest_sync`, and deliberately a separate
        method rather than a flag on it. That one answers "is the data fresh",
        for which an unfinished run is no evidence at all and is excluded. This
        one answers "is something happening right now", for which an unfinished
        run is the *only* evidence -- so a single query serving both would have
        to return rows one caller must never see.

        Dry runs are excluded here as they are there: a preview writes nothing,
        so it is not work anybody needs to wait for.

        Ordered oldest first, because a run that has been going for twenty
        minutes is the one worth naming when several are open -- it is the one
        most likely to be a process that died without reporting.
        """
        return list(
            self.session.exec(
                select(BoardSyncHistory)
                .join(
                    BoardRegistration,
                    BoardRegistration.id == BoardSyncHistory.board_registration_id,
                )
                .where(
                    BoardRegistration.project_id == project_id,
                    BoardSyncHistory.completed_at.is_(None),  # type: ignore[union-attr]
                    BoardSyncHistory.dry_run.is_(False),  # type: ignore[union-attr]
                )
                .order_by(BoardSyncHistory.started_at.asc())
            ).all()
        )

    def sync_is_fresh(self, project_id: str, now: datetime) -> bool:
        """Whether the tickets on disk were actually refreshed inside the TTL.

        A **failed** run is not freshness either, and it does carry a
        `completed_at` (see `sync_board_tickets`' error path), so the status is
        checked as well as the timestamp -- otherwise a board whose credential
        expired would report fresh for an hour after every failure.
        """
        last = self.latest_sync(project_id)
        if last is None or last.sync_status != SyncStatus.COMPLETED:
            return False
        completed = as_utc(last.completed_at)
        return completed is not None and completed >= now - SYNC_FRESHNESS

    async def _run_board_sync(
        self,
        project: Project,
        since: datetime,
        now: datetime,
        requested_by: Optional[str],
    ) -> bool:
        """One sync of the project's board, scoped to the window.

        Awaited rather than backgrounded: the summary is being assembled from
        the result, so returning before it lands would hand back exactly the
        stale data gate 1 just decided was too old.

        Returns False -- never raises -- when there is no board, no credential,
        or the sync itself fails. A summary over slightly stale tickets is worth
        far more than a 500.

        **`sync_board_tickets` reports failure by returning, not by raising.**
        It catches everything, writes FAILED to the history row and hands back
        ``{"success": False, "error_message": ...}``. Ignoring that return
        made every call here answer True, so `synced` said "fresh" on top of
        data that was months old -- for Linear, every scoped sync had been
        failing on a GraphQL validation error and nothing surfaced it. The
        `except` below still matters (a raise is possible), but it was never
        the path that actually fired. Whatever went wrong is recorded on
        `self.last_sync_error` for the payload.

        Cancellation (gate 1's `asyncio.wait_for` giving up) is caught only to
        close out the `BoardSyncHistory` row, then re-raised: a PENDING row left
        behind is not merely untidy, it is the row the *next* freshness check
        would otherwise have to reason about.
        """
        from src.services.board_credential_service import (
            get_board_credential_payload,
            payload_to_legacy_token,
        )
        from src.services.board_sync_service import board_sync_service

        board = self.session.exec(
            select(BoardRegistration).where(
                BoardRegistration.project_id == project.id,
                BoardRegistration.deleted_at.is_(None),
            )
        ).first()
        if board is None or not board.is_active:
            self.last_sync_error = (
                None if board is None else f"Board {board.board_name} is not active"
            )
            return False

        payload = get_board_credential_payload(self.session, board.id)
        if not payload:
            logger.info("No board credential for %s; summary skips sync", board.id)
            self.last_sync_error = (
                f"No stored credential for board {board.board_name} — reconnect it"
            )
            return False
        token = payload_to_legacy_token(board.board_type, payload)

        history = BoardSyncHistory(
            board_registration_id=board.id,
            sync_status=SyncStatus.PENDING,
            started_at=now,
            synced_by=requested_by or board.user_id,
        )
        self.session.add(history)
        self.session.commit()

        try:
            result = await board_sync_service.sync_board_tickets(
                registration_id=board.id,
                sync_history_id=history.id,
                token=token,
                # Scoped to the window: a summary needs what moved inside it,
                # not a full re-pull of the board's whole history. `since` is
                # advisory -- an adapter that cannot express the filter answers
                # in full -- but Linear, the board this path actually runs
                # against, pushes it down to `updatedAt`.
                #
                # `full_sync` is deliberately absent: `sync_board_tickets` has
                # never read it, and passing a key that does nothing while the
                # comment claims a scoped pull is how this stayed a full pull
                # for as long as it did.
                options={"since": since.isoformat()},
            )
        except asyncio.CancelledError:
            self._close_out_sync(history, "Summary sync timed out")
            raise
        except Exception as exc:  # noqa: BLE001 - a stale summary beats no summary
            logger.warning("Summary-triggered sync failed for %s: %s", board.id, exc)
            self._close_out_sync(history, str(exc)[:500])
            self.last_sync_error = str(exc)[:500]
            return False

        if not (result or {}).get("success"):
            reason = str((result or {}).get("error_message") or "unknown error")[:500]
            logger.warning("Summary-triggered sync failed for %s: %s", board.id, reason)
            self.last_sync_error = reason
            return False

        self.last_sync_error = None
        return True

    def _close_out_sync(self, history: BoardSyncHistory, reason: str) -> None:
        """Mark an abandoned sync FAILED so it is not left PENDING forever."""
        try:
            history.sync_status = SyncStatus.FAILED
            history.completed_at = datetime.now(timezone.utc)
            history.error_message = reason
            self.session.add(history)
            self.session.commit()
        except Exception as exc:  # noqa: BLE001 - best effort, never the failure
            logger.warning("Could not close out sync history %s: %s", history.id, exc)

    # ================================================================= gate 2

    def live_summary(
        self,
        *,
        project_id: str,
        user_id: Optional[str],
        summary_type: SummaryType,
        window_spec: str,
    ) -> Optional[Summary]:
        """The current summary for this scope and window, if there is one.

        Keyed on `window_spec` -- the literal spec asked for -- and never on the
        resolved timestamps. See the module docstring.

        Read inside a SAVEPOINT: on Postgres a failed statement aborts the whole
        transaction, so a `summaries` table that does not exist yet (an image
        live ahead of `alembic upgrade head`) would not merely miss the cache,
        it would poison the caller's session and turn its COMMIT into a silent
        ROLLBACK. The same trap slice 1 shipped -- see `_resolve_assigned_user_id`
        in `board_sync_service.py`.
        """
        try:
            with self.session.begin_nested():
                query = select(Summary).where(
                    Summary.project_id == project_id,
                    Summary.summary_type == summary_type,
                    Summary.window_spec == window_spec,
                    Summary.superseded_by_id.is_(None),
                )
                query = (
                    query.where(Summary.user_id.is_(None))
                    if user_id is None
                    else query.where(Summary.user_id == user_id)
                )
                return self.session.exec(
                    query.order_by(Summary.created_at.desc())
                ).first()
        except Exception as exc:  # noqa: BLE001 - a cache miss, never a failure
            logger.warning("Live-summary lookup failed: %s", exc)
            return None

    def _latest_live_summary(
        self,
        *,
        project_id: str,
        user_id: Optional[str],
        summary_type: SummaryType,
    ) -> Optional[Summary]:
        """The newest live summary for this scope, whatever window it used.

        Only `persist` wants this, and only to find a note to inherit. Windows
        are not stable identifiers over time -- someone reads `3d` on Monday and
        `1w` on Friday, and `--window release` used to mint a new spec every
        single day -- so a note keyed strictly on `window_spec` is lost the moment
        the window drifts. Scope (project, type, and team-vs-person) is stable, so
        that is what a note follows. (A release scope no longer drifts: it is
        `release:<version>`. Durations still do, so this stands.)

        Windowless rows (`window_spec = ''`, the board-scoped append path) are
        excluded: they are a history log rather than a live slot, and a note
        must not be inherited from something that was never one.

        Same SAVEPOINT reasoning as `live_summary`.
        """
        try:
            with self.session.begin_nested():
                query = select(Summary).where(
                    Summary.project_id == project_id,
                    Summary.summary_type == summary_type,
                    Summary.window_spec != "",
                    Summary.superseded_by_id.is_(None),
                )
                query = (
                    query.where(Summary.user_id.is_(None))
                    if user_id is None
                    else query.where(Summary.user_id == user_id)
                )
                return self.session.exec(
                    query.order_by(Summary.created_at.desc())
                ).first()
        except Exception as exc:  # noqa: BLE001 - no note to inherit, not a failure
            logger.warning("Latest-live-summary lookup failed: %s", exc)
            return None

    # ================================================================= gate 3

    @staticmethod
    def compute_fingerprint(
        tickets: Sequence[Ticket],
        activities: Sequence[CodeActivity],
        *,
        release_ticket_count: Optional[int] = None,
        tickets_without_release_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """What this summary was built from, in a comparable shape.

        Three parts, each covering a blind spot in the others:

        * **commits** -- pushes. Alone they call a status change with no new code
          "unchanged", and a ticket that never had a commit would carry an empty
          list forever and so never look changed at all.
        * **tickets** -- ``(id, status, updated_at)``. Alone it misses a day of
          pushes to an open branch.
        * **prs** -- ``(url, state, updated_at)``. Load-bearing because
          `get_commits` answers on the **default branch only**: for an open PR
          `commit_shas` is empty, so without this a week of work on an unmerged
          branch is invisible to the gate and the stale prose is served back.
          The PR's own `updated_at` moves on every push, review and title edit,
          which is enough to detect the change even with no SHAs at all.

        Plus, **under a release scope only**, the two boundary counts. They are
        part of what such a summary *says* -- the narrator states the release and
        the number of project tickets it excludes -- and the three parts above
        are built from the release-filtered rows, so they cannot see a change
        outside the scope. A ticket created on no release moves
        `tickets_without_release_count` and nothing else: without these keys gate
        3 answers "unchanged", re-serves prose carrying yesterday's excluded
        count, and the CLI prints its own freshly-recomputed boundary line
        underneath it -- one output disagreeing with itself.

        `release_ticket_count` is belt-and-braces: under a release scope it
        equals `len(tickets)` today, since `count_release_tickets` and
        `_project_tickets` apply the same predicate. It is here so that if those
        two ever diverge, the gate notices rather than the reader.

        Omitted entirely when there is no release scope, rather than stored as
        `null`: the comparison is `==` against a stored dict, so adding keys to
        the unscoped shape would make every fingerprint written before this
        change compare unequal and re-narrate once, for nothing.

        Sorted, and built from JSON-native types only, because the stored value
        round-trips through a JSON column and is compared with ``==``.
        """
        commits = sorted({sha for a in activities for sha in a.commit_shas})
        ticket_state = sorted(
            [
                str(t.id),
                t.status.value if isinstance(t.status, TicketStatus) else str(t.status),
                as_utc(t.updated_at).isoformat() if t.updated_at else "",
            ]
            for t in tickets
        )
        pr_state = sorted(
            {
                (
                    a.pr_url,
                    a.pr_state or "",
                    as_utc(a.occurred_at).isoformat() if a.occurred_at else "",
                )
                for a in activities
                if a.pr_url
            }
        )
        fingerprint: Dict[str, Any] = {
            "commits": commits,
            "tickets": ticket_state,
            "prs": [list(row) for row in pr_state],
        }
        if (
            release_ticket_count is not None
            or tickets_without_release_count is not None
        ):
            fingerprint["release_ticket_count"] = release_ticket_count
            fingerprint["tickets_without_release_count"] = tickets_without_release_count
        return fingerprint

    # ================================================================== scope

    def resolve_scope(
        self,
        *,
        project: Project,
        window_spec: str,
        release: Optional[str] = None,
        now: datetime,
    ) -> Tuple[str, Optional[str], datetime]:
        """``(window_spec, release version or None, period_start)``.

        The one place either kind of scope is turned into the three things the
        gates need, so the read path and the write path's fingerprint cannot
        disagree about what a spec means.

        **A release scope wins over a duration and replaces it**, rather than the
        two composing: a release narrows *which tickets exist* for this summary,
        which is a different question from "what moved in the last three days",
        and a key that carried both would drift daily with the duration. A
        release spec arriving as `window_spec` is the same scope by another door
        -- that is what the narrator echoes back on save and what the next read
        looks the row up by, so it has to round-trip.

        `period_start` for a release is anchored to **when that release opened**,
        capped at :data:`RELEASE_SPAN_CAP`: it bounds the board sync and the
        per-repo GitHub fetches, and an unbounded one on a years-old row is a
        timed-out GET rather than a longer summary.
        """
        if release is None and is_release_spec(window_spec):
            release = release_spec_version(window_spec)
        if not release:
            # Canonical before the gates, because all three key on it: gate 2
            # looks up `Summary.window_spec ==`, so reading `'day'` while
            # `persist` wrote `'1d'` is a permanent cache miss that looks
            # exactly like the cache working correctly on a cold row.
            spec = canonical_window_spec(window_spec)
            return spec, None, now - parse_window_spec(spec)

        spec = canonical_window_spec(release_spec(release))
        version = release_spec_version(spec)
        return spec, version, self._release_period_start(project, version, now)

    def _release_period_start(
        self, project: Project, version: str, now: datetime
    ) -> datetime:
        """When to start looking for activity on this release.

        **This is a decision, not a requirement.** #563 fixed *which tickets* a
        release scope covers and said nothing about the period; the rule below is
        this change's own choice, written down here because nothing else states
        it. In full: the release row's `created_at`, floored at
        :data:`RELEASE_SPAN_CAP` back from now, and :data:`RELEASE_SPAN_FALLBACK`
        when the version has no row at all -- `Ticket.release` is free text a
        board wrote, so a scope InnoDay has no release row for is a legitimate
        question rather than an error.

        **Why "since the release was opened".** A duration answers "what moved
        lately"; a release scope asks "where has this version got to", and that
        question has its own start date -- the pipeline opens a version's slot as
        soon as the one below it ships, so `created_at` is when work on it could
        first have happened. Any fixed duration would be arbitrary against it:
        `3d` on a six-week release reports a fraction of it as the whole, and
        `6w` on a release cut yesterday reaches back into the previous one's work
        and attributes it here.

        **The hazard it carries, and why the cap and the fallback both exist.**
        `period_start` is what `_activity_at` measures activity against, so a
        window shorter than the work it is asking about *manufactures absence* --
        tickets land in `no_work_detected` because of where the window starts,
        not because nothing happened. The fallback is 28 days rather than the 3-day
        default for that reason: an unmatched version gets a window wide enough to
        contain a normal release, not a narrow one that reports silence. The cap
        bounds the other end, and is a resource limit rather than an editorial
        one -- `period_start` also bounds the board sync and the per-repo GitHub
        fetches inside a *synchronous* GET, and BPAI carries ~40 release rows board
        sync invented from years-old version labels.

        **The residual, stated rather than fixed:** a slot opened minutes ago
        yields a minutes-long window, so every ticket already tagged with that
        version reads as no-work on ship day. That is a truthful answer to "what
        has moved on v1.10.0 since it opened", and the skill's wording says
        "nothing moved on v1.10.0" rather than "nothing moved", so it does not
        read as a stalled team. There is deliberately **no minimum floor**: one
        would make `period_start` reach back before the release existed, into the
        previous release's work, which is the failure this scope exists to
        prevent. If a floor is wanted later it needs to be an explicit decision
        about attributing pre-release work, not a default.
        """
        row = self.session.exec(
            select(Release).where(
                Release.organization_id == project.organization_id,
                Release.project_id == project.id,
                Release.version == version,
                Release.deleted_at.is_(None),
            )
        ).first()
        opened = as_utc(row.created_at) if row is not None else None
        if opened is None or opened > now:
            return now - RELEASE_SPAN_FALLBACK
        return max(opened, now - RELEASE_SPAN_CAP)

    # ==================================================== fingerprint inputs

    def release_counts(self, project_id: str, release: Optional[str]) -> ReleaseCounts:
        """The two boundary counts, or both ``None`` when nothing is scoped.

        One place decides "is this release-scoped, and if so what does it leave
        out", so the fingerprint's key *set* cannot depend on which caller asked.
        """
        if release is None:
            return ReleaseCounts(None, None)
        return ReleaseCounts(
            release_ticket_count=self.count_release_tickets(project_id, release),
            tickets_without_release_count=self.count_tickets_without_release(
                project_id
            ),
        )

    async def fingerprint_for(
        self,
        *,
        project: Project,
        window_spec: Optional[str] = None,
        release: Optional[str] = None,
        period_start: Optional[datetime] = None,
        counts: Optional[ReleaseCounts] = None,
        now: datetime,
    ) -> FingerprintInputs:
        """Gather what a fingerprint is computed from, then compute it.

        **The gather is the part that has to be shared, not `compute_fingerprint`.**
        That was always single-sourced. What was duplicated is the five steps
        around it -- resolve the scope, read the scoped tickets, fetch the code
        activity, count the release boundary, call it with the right kwargs -- once
        in `assemble` and once in the summary router's save path. The two have to
        pass an **identical** kwarg set or their fingerprints never compare equal
        and gate 3 re-narrates every summary, every morning.

        That has already misfired twice, both times silently:

        * the router parsed the window spec as a *duration*, which raises for
          `release:v1.9.0`, and its broad `except` turned that into `{}` -- a
          summary that could never be `UNCHANGED`;
        * the two boundary counts had to be back-filled into the router after
          `assemble` gained them.

        A third input added in one site and not the other fails the same way, and
        the failure is invisible: a fingerprint that never matches looks exactly
        like a cache working correctly. So there is one gather, and no second site
        to forget.

        **This method raises.** The router's `_compute_fingerprint` degrades to
        `{}` rather than failing a write someone is waiting on; that swallow stays
        at the router on purpose, because moving it in here would hide a bug in
        this method from `assemble` as well.

        Passing `period_start` says the caller has already resolved its scope --
        `assemble` has, and resolving it twice is a second answer to a settled
        question. Passing `window_spec` alone resolves it here.
        """
        if period_start is None:
            if window_spec is None:
                raise ValueError(
                    "fingerprint_for needs a window_spec to resolve, or an "
                    "already-resolved period_start"
                )
            window_spec, release, period_start = self.resolve_scope(
                project=project, window_spec=window_spec, release=release, now=now
            )
        if counts is None:
            counts = self.release_counts(project.id, release)

        tickets = self._project_tickets(project.id, release=release)
        activities = await self.activity_fetcher.fetch(
            project=project, since=period_start, until=now
        )
        return FingerprintInputs(
            # Splatted from `ReleaseCounts` rather than named again here: the
            # boundary keys are declared once, so this call cannot fall behind it.
            fingerprint=self.compute_fingerprint(
                tickets, activities, **counts._asdict()
            ),
            tickets=tickets,
            activities=activities,
            window_spec=window_spec,
            release=release,
            period_start=period_start,
            counts=counts,
        )

    # ============================================================== assembly

    async def assemble(
        self,
        *,
        project: Project,
        summary_type: SummaryType,
        window_spec: str,
        release: Optional[str] = None,
        user_id: Optional[str] = None,
        requested_by: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> SummaryAssembly:
        """Run the gates, and assemble only if all three decline.

        `release` narrows the ticket universe to one version. Out of release
        means **not assembled** -- not assembled and then filtered by whoever
        narrates it: handing a narrator tickets it must be instructed to ignore
        is how a summary comes to describe work that is not in its scope. It must
        be a concrete version by the time it gets here; the `current` sentinel is
        resolved at the route, by the resolver the `?release=` ticket filter
        already uses.
        """
        now = now or datetime.now(timezone.utc)
        window_spec, release, period_start = self.resolve_scope(
            project=project, window_spec=window_spec, release=release, now=now
        )
        # Both counts are needed on **every** outcome, cached ones included: the
        # boundary line is part of what a release-scoped summary means, and a
        # cached read that dropped it would report a subset as the whole. Computed
        # once here and handed to `fingerprint_for` below, so the shell and the
        # fingerprint report the same boundary and neither re-reads it.
        counts = self.release_counts(project.id, release)

        # --- gate 1 ------------------------------------------------------
        synced = False
        self.last_sync_error = None
        if not self.sync_is_fresh(project.id, now):
            try:
                synced = await asyncio.wait_for(
                    self._sync_runner(project, period_start, now, requested_by),
                    timeout=SYNC_TIMEOUT_SECONDS,
                )
            except asyncio.TimeoutError:
                self.last_sync_error = (
                    f"Board sync exceeded {SYNC_TIMEOUT_SECONDS}s and was abandoned"
                )
                # Fall through to whatever is already on disk. The alternative
                # is not "a fresher summary", it is a 504 from the proxy in
                # front of this GET and no summary at all.
                logger.warning(
                    "Board sync for project %s exceeded %ss; summarising stale "
                    "data instead",
                    project.id,
                    SYNC_TIMEOUT_SECONDS,
                )

        # **The count is `len()` of the list the same payload carries**, not a
        # separately-derived number that happens to usually agree. It used to be
        # counted over the assembled lines, which made it a different question
        # wearing the same name: assembly-scoped (a personal summary counted
        # only that user's candidates, and a terminal-status ticket never became
        # a line at all) against `unmapped_assignees()`, which is project-wide
        # and unfiltered. Worse, on a CACHED or UNCHANGED outcome no lines are
        # built, so the count was 0 beside a non-empty list -- the CLI footer
        # dropped the "N assignees unmapped" hint precisely on cached reads,
        # which are the common case.
        unmapped_count = len(self.unmapped_assignees(project.id))

        def _shell(outcome: SummaryOutcome, **kw) -> SummaryAssembly:
            return SummaryAssembly(
                outcome=outcome,
                window_spec=window_spec,
                period_start=period_start,
                period_end=now,
                summary_type=summary_type,
                user_id=user_id,
                synced=synced,
                sync_error=None if synced else self.last_sync_error,
                unmapped_assignee_count=unmapped_count,
                release=release,
                release_ticket_count=counts.release_ticket_count,
                tickets_without_release_count=counts.tickets_without_release_count,
                **kw,
            )

        cached = self.live_summary(
            project_id=project.id,
            user_id=user_id,
            summary_type=summary_type,
            window_spec=window_spec,
        )

        # --- gate 2 ------------------------------------------------------
        if cached is not None:
            written = as_utc(cached.created_at)
            if written is not None and written >= now - CACHE_TTL:
                return _shell(
                    SummaryOutcome.CACHED,
                    summary=cached,
                    body_markdown=cached.body_markdown,
                    notes_markdown=cached.notes_markdown,
                    notes_updated_at=cached.notes_updated_at,
                    source_fingerprint=cached.source_fingerprint or {},
                )

        # The same gather the save path uses -- see `fingerprint_for` for why the
        # two cannot be allowed to read the inputs separately. The scope is already
        # resolved here, so it is passed in rather than worked out again.
        gathered = await self.fingerprint_for(
            project=project,
            window_spec=window_spec,
            release=release,
            period_start=period_start,
            counts=counts,
            now=now,
        )
        tickets = gathered.tickets
        activities = gathered.activities
        fingerprint = gathered.fingerprint

        # --- gate 3 ------------------------------------------------------
        if cached is not None and (cached.source_fingerprint or {}) == fingerprint:
            # Restamped in place, not superseded: the *content* is unchanged, so
            # a new row would be a byte-identical copy and the supersession
            # chain would record churn instead of history. `created_at` is left
            # alone -- it is when the prose was written, and gate 2 reads it.
            cached.period_start = period_start
            cached.period_end = now
            self.session.add(cached)
            return _shell(
                SummaryOutcome.UNCHANGED,
                summary=cached,
                body_markdown=cached.body_markdown,
                notes_markdown=cached.notes_markdown,
                notes_updated_at=cached.notes_updated_at,
                source_fingerprint=fingerprint,
            )

        # --- assembly ----------------------------------------------------
        assembly = self._assemble(
            project=project,
            tickets=tickets,
            activities=activities,
            summary_type=summary_type,
            user_id=user_id,
            period_start=period_start,
            now=now,
            window_spec=window_spec,
            synced=synced,
            previous_statuses=self._previous_statuses(
                cached.source_fingerprint if cached is not None else None
            ),
        )
        assembly.source_fingerprint = fingerprint
        assembly.unmapped_assignee_count = unmapped_count
        assembly.release = release
        assembly.release_ticket_count = counts.release_ticket_count
        assembly.tickets_without_release_count = counts.tickets_without_release_count
        assembly.sync_error = None if synced else self.last_sync_error
        # **The note survives assembly.** It belongs to the live summary, not to
        # the prose that gets regenerated, so it has to travel on *every*
        # outcome -- and `assembled` is the one that matters most: it fires
        # precisely when something moved, which is when anyone is reading. Only
        # the two short-circuit shells carried it at first, so the note vanished
        # from the CLI and from the narrating agent on every non-quiet day while
        # the dashboard -- which reads the row directly -- still showed it.
        assembly.notes_markdown = cached.notes_markdown if cached is not None else None
        assembly.notes_updated_at = (
            cached.notes_updated_at if cached is not None else None
        )
        # **A release's notes are this summary's prose.** Notes written at tag
        # time land on `Release.summary`; a release-scoped read that ignored them
        # reported "nothing written yet" about a release whose notes were sitting
        # one table away. Only as a fallback -- a narrated `Summary` row is
        # canonical, because it is the one with items, a fingerprint and a
        # history, and the mirror on the save path keeps the two in step from
        # then on.
        if assembly.body_markdown is None and release:
            assembly.body_markdown = self._release_notes(project, release)
        return assembly

    def _release_notes(self, project: Project, version: str) -> Optional[str]:
        """The prose stored on a release row, if any. Never raises."""
        try:
            row = self.session.exec(
                select(Release).where(
                    Release.project_id == project.id,
                    Release.version == version,
                    Release.deleted_at.is_(None),
                )
            ).first()
        except SQLAlchemyError:
            logger.warning("Could not read notes for release %s", version)
            return None
        return (row.summary or None) if row is not None else None

    def _project_tickets(
        self, project_id: str, *, release: Optional[str] = None
    ) -> List[Ticket]:
        """Every non-deleted ticket on the project -- deliberately unwindowed.

        A window filter here would be wrong, not merely conservative: two of the
        blocks are defined by the *absence* of activity in the window
        (`no_work_detected`, `unassigned_idle_count`), so the tickets that fill
        them are exactly the ones a window filter removes. The fingerprint has
        the same requirement -- a ticket dropped from it reads as "unchanged".
        The output volume is bounded on the way out instead, by `ACTIVE_CAP` and
        `BLOCK_CAP`.

        `release` is the **one** predicate that does belong here, and it is not a
        window: it says which tickets exist for this summary at all, so the
        absence blocks and the fingerprint have to be measured inside it or they
        report the project's silence as the release's. Matched byte-exact, like
        every other reader of this free-text column (`_ticket_counts`,
        `release_board`).
        """
        statement = select(Ticket).where(
            Ticket.project_id == project_id,
            Ticket.deleted_at.is_(None),
        )
        if release is not None:
            statement = statement.where(Ticket.release == release)
        return list(self.session.exec(statement).all())

    def count_release_tickets(self, project_id: str, release: str) -> int:
        """How many of the project's tickets are on this release.

        Counted rather than `len()`-ed off the assembled list because a cached
        read never builds one, and the boundary line is not optional on a cached
        read -- see `assemble`.
        """
        return int(
            self.session.exec(
                select(func.count())
                .select_from(Ticket)
                .where(
                    Ticket.project_id == project_id,
                    Ticket.deleted_at.is_(None),
                    Ticket.release == release,
                )
            ).one()
            or 0
        )

    def count_tickets_without_release(self, project_id: str) -> int:
        """How many of the project's tickets are on no release at all.

        The size of what a release-scoped summary leaves out. A NULL and an
        emptied-out string are the same fact here: `''` is what `tickets update
        --release ""` stores to take a ticket *out* of a release
        (`src/services/ticket_release.py`), so counting only NULLs would
        understate the excluded set by exactly the tickets somebody removed by
        hand.
        """
        return int(
            self.session.exec(
                select(func.count())
                .select_from(Ticket)
                .where(
                    Ticket.project_id == project_id,
                    Ticket.deleted_at.is_(None),
                    func.coalesce(func.trim(Ticket.release), "") == "",
                )
            ).one()
            or 0
        )

    # ------------------------------------------------------------ internals

    def _resolve_handle(
        self, organization_id: str, project_id: str, handle: Optional[str]
    ) -> Optional[str]:
        """A GitHub login → an InnoDay user id, or None. Memoised per request.

        Same SAVEPOINT reasoning as `live_summary`: the resolver reads
        `user_identity`, and a failed read there must not abort the caller's
        transaction.
        """
        if not handle:
            return None
        key = (organization_id, project_id, handle)
        if key in self._identity_cache:
            return self._identity_cache[key]
        resolved: Optional[str] = None
        try:
            with self.session.begin_nested():
                match = IdentityResolutionService.resolve(
                    self.session,
                    organization_id=organization_id,
                    project_id=project_id,
                    platform=IdentityPlatform.GITHUB,
                    assignee=BoardAssignee(display_name=handle),
                )
                resolved = match.user.id if match else None
        except Exception as exc:  # noqa: BLE001 - unmatched is a valid answer
            logger.warning("GitHub handle %r could not be resolved: %s", handle, exc)
        self._identity_cache[key] = resolved
        return resolved

    def _project_alias(self, project: Project) -> str:
        """The project's alias -- the prefix `project_ref_number` displays under.

        `Project.alias` is documented as the ticket prefix, and the number is
        unique per ``(project_id, project_ref_number)``, so ``{project
        alias}-42`` names exactly one ticket.

        This used to be the *organisation's* alias, because the number was
        org-scoped and a project-prefixed rendering would have collided across
        every project in the org. Numbering is per-project now, so the project
        alias is the correct -- and unambiguous -- prefix.
        """
        return project.alias or ""

    def _display_ref(self, project: Project, ticket: Ticket) -> Optional[str]:
        """What to call this ticket: the board's key, else the display number."""
        if ticket.external_ticket_id:
            return ticket.external_ticket_id
        if ticket.project_ref_number is None:
            return None
        alias = self._project_alias(project)
        return f"{alias}-{ticket.project_ref_number}" if alias else None

    def _tickets_by_ref(
        self, project: Project, tickets: Sequence[Ticket]
    ) -> Dict[str, Ticket]:
        """Instance shim for :func:`tickets_by_ref`. See it for the rule."""
        return tickets_by_ref(self._project_alias(project), tickets)

    def _index_activity(
        self,
        project: Project,
        tickets: Sequence[Ticket],
        activities: Sequence[CodeActivity],
    ) -> Dict[int, List[CodeActivity]]:
        """Ticket id → the code activity referencing it."""
        by_ref = self._tickets_by_ref(project, tickets)

        linked: Dict[int, List[CodeActivity]] = {}
        for activity in activities:
            if not activity.ticket_ref:
                continue
            ticket = by_ref.get(activity.ticket_ref.upper())
            if ticket is None or ticket.id is None:
                continue
            linked.setdefault(ticket.id, []).append(activity)
        return linked

    def _attribute(
        self,
        project: Project,
        ticket: Ticket,
        activities: Sequence[CodeActivity],
    ) -> Tuple[Optional[str], Optional[str], Attribution, bool]:
        """Effective owner of a ticket: `(user_id, display, attribution, unmapped)`.

        The order is `assigned_to`, then the resolved author of code activity in
        the window, then nobody.

        **The id and the display always name the same person.** They did not:
        when the board named someone unmappable *and* the code author resolved,
        this returned the code author's `user_id` beside the board's display
        string, so `SummaryItem` stored a row asserting user X while rendering
        name Y -- and the profile page, or anything joining on the id, drew the
        wrong person. The old comment justified it as the only surviving record
        of who the board thought owned the ticket; that is not so. `Ticket.
        assignee` holds it, and is exactly what `unmapped_assignees()` reads to
        build the profile picklist. So when the code author wins *and* resolves,
        the display is the code author's handle.

        The board's string is still preferred when nothing resolves -- then no
        id is being asserted, so there is nothing for it to contradict.
        """
        board_display = (ticket.assignee or "").strip() or None
        unmapped = bool(board_display and not ticket.assigned_to)

        if ticket.assigned_to:
            return ticket.assigned_to, board_display, Attribution.BOARD, False

        author = next(
            (a.author_handle for a in activities if a.author_handle),
            None,
        )
        if author:
            resolved = self._resolve_handle(project.organization_id, project.id, author)
            if resolved is not None:
                return resolved, author, Attribution.CODE, False
            return None, board_display or author, Attribution.CODE, unmapped
        if board_display:
            return None, board_display, Attribution.BOARD, True
        return None, None, Attribution.NONE, False

    @staticmethod
    def _previous_statuses(fingerprint: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """``{ticket id: status}`` as the last summary recorded it.

        Read back out of the stored `source_fingerprint`, whose ticket rows are
        `[id, status, updated_at]` (see `compute_fingerprint`). This is the only
        record of a ticket's *previous* state anywhere -- there is no status
        history table -- and it is what lets a genuine board transition be told
        apart from a timestamp that merely moved.
        """
        rows = (fingerprint or {}).get("tickets") or []
        previous: Dict[str, str] = {}
        for row in rows:
            if isinstance(row, (list, tuple)) and len(row) >= 2:
                previous[str(row[0])] = str(row[1])
        return previous

    @staticmethod
    def _activity_at(
        ticket: Ticket,
        activities: Sequence[CodeActivity],
        period_start: datetime,
        previous_statuses: Dict[str, str],
    ) -> Optional[datetime]:
        """When this ticket demonstrably moved inside the window, or None.

        **Deliberately not `updated_at`.** That column is the wrong witness: it
        is written by whatever last touched the row, and board sync used to
        write it for every ticket it saw whether or not anything changed. One
        no-op sync therefore reported an entire stale board as active work --
        `no_work_detected` emptied, the unassigned backlog got *enumerated*
        instead of counted, and the active cap was filled by whichever five rows
        an unordered SELECT happened to return. Measured on a fixture of 2 real
        + 30 idle tickets: `active_total` 22, `no_work_detected` 0.

        The restamp is fixed at source (`board_sync_service._create_or_update_ticket`
        now compares before it writes), but a signal that inverts every block
        when one unrelated line regresses is the wrong signal regardless. So
        activity is read from things that mean something on their own:

        * **code in the window** -- a commit or PR the fetcher linked here;
        * **`completed_at` in the window** -- a real terminal transition, and a
          value the board supplies rather than one `now()` writes;
        * **a status different from the last summary's** -- a board move, from
          the only prior state on record.

        A pure board move with no prior summary to compare against is therefore
        *not* activity, and such a ticket lands in `no_work_detected` for one
        cycle. That is the deliberate trade: under-reporting one transition is
        recoverable, inverting every block is not. Gate 3 still sees it -- the
        fingerprint carries status -- so the prose is regenerated either way.
        """
        stamps = [
            stamp
            for stamp in (as_utc(a.occurred_at) for a in activities)
            if stamp is not None
        ]
        if activities and not stamps:
            # Linked code with no usable timestamp is still code. The fetcher
            # bounds its own results to the window, so its mere presence is the
            # evidence; `period_start` is the earliest it could have happened.
            stamps.append(period_start)

        completed = as_utc(ticket.completed_at)
        if completed is not None and completed >= period_start:
            stamps.append(completed)

        key = str(ticket.id)
        current = (
            ticket.status.value
            if isinstance(ticket.status, TicketStatus)
            else str(ticket.status)
        )
        if key in previous_statuses and previous_statuses[key] != current:
            updated = as_utc(ticket.updated_at)
            stamps.append(
                updated
                if updated is not None and updated >= period_start
                else period_start
            )

        return max(stamps) if stamps else None

    def _line(
        self,
        project: Project,
        ticket: Ticket,
        activities: Sequence[CodeActivity],
        block: Block,
        occurred_at: Optional[datetime],
    ) -> SummaryLine:
        user_id, display, attribution, unmapped = self._attribute(
            project, ticket, activities
        )
        newest_pr = next((a for a in activities if a.pr_url), None)
        anchor = newest_pr or (activities[0] if activities else None)
        return SummaryLine(
            block=block,
            ticket_id=ticket.id,
            ticket_ref=self._display_ref(project, ticket),
            ticket_summary=ticket.summary,
            status=(
                ticket.status.value
                if isinstance(ticket.status, TicketStatus)
                else str(ticket.status)
            ),
            assignee_user_id=user_id,
            assignee_display=display,
            assignee_unmapped=unmapped,
            attribution=attribution,
            repo=anchor.repo if anchor else None,
            branch=anchor.branch if anchor else None,
            pr_url=newest_pr.pr_url if newest_pr else None,
            pr_state=newest_pr.pr_state if newest_pr else None,
            occurred_at=occurred_at,
            commit_count=sum(len(a.commit_shas) for a in activities),
        )

    def _assemble(
        self,
        *,
        project: Project,
        tickets: Sequence[Ticket],
        activities: Sequence[CodeActivity],
        summary_type: SummaryType,
        user_id: Optional[str],
        period_start: datetime,
        now: datetime,
        window_spec: str,
        synced: bool,
        previous_statuses: Optional[Dict[str, str]] = None,
    ) -> SummaryAssembly:
        """Group by ticket, cap **every** block, and file the rest as counts.

        A ticket assigned to the requester with no activity appears in *both*
        `no_work_detected` and `up_next`, and that is intended: the two blocks
        answer different questions of the same fact -- "nothing has happened on
        this" and "this is what you have queued" -- and a personal summary that
        reported the first without the second would read as a complaint with no
        next step.
        """
        previous_statuses = previous_statuses or {}
        linked = self._index_activity(project, tickets, activities)

        candidates: List[Ticket] = []
        for ticket in tickets:
            if user_id is None:
                candidates.append(ticket)
                continue
            # Personal: assigned to them, **or** they wrote the code. Authorship
            # counts because a ticket the board never assigned is still their
            # work once their commits are on it.
            if ticket.assigned_to == user_id:
                candidates.append(ticket)
                continue
            authors = {
                self._resolve_handle(
                    project.organization_id, project.id, a.author_handle
                )
                for a in linked.get(ticket.id or -1, [])
            }
            if user_id in authors:
                candidates.append(ticket)

        active: List[Tuple[datetime, SummaryLine]] = []
        no_work: List[SummaryLine] = []
        unassigned_active: List[SummaryLine] = []
        unassigned_idle = 0
        up_next: List[SummaryLine] = []

        for ticket in candidates:
            ticket_activity = linked.get(ticket.id or -1, [])
            occurred_at = self._activity_at(
                ticket, ticket_activity, period_start, previous_statuses
            )
            has_activity = occurred_at is not None
            board_assigned = bool((ticket.assignee or "").strip())
            # A finished ticket is not idle work. Without this every DONE ticket
            # the project ever closed would sit in the no-work block forever and
            # make it unreadable.
            open_ticket = ticket.status not in TERMINAL_STATUSES

            if has_activity and board_assigned:
                active.append(
                    (
                        occurred_at,
                        self._line(
                            project, ticket, ticket_activity, Block.ACTIVE, occurred_at
                        ),
                    )
                )
            elif has_activity:
                unassigned_active.append(
                    self._line(
                        project,
                        ticket,
                        ticket_activity,
                        Block.UNASSIGNED_ACTIVE,
                        occurred_at,
                    )
                )
            elif board_assigned and open_ticket:
                line = self._line(project, ticket, ticket_activity, Block.NO_WORK, None)
                no_work.append(line)
                # "Up next" is board-assignment-only: authorship records what
                # someone did, and cannot predict what they have queued.
                if user_id is not None and ticket.assigned_to == user_id:
                    queued = self._line(
                        project, ticket, ticket_activity, Block.UP_NEXT, None
                    )
                    up_next.append(queued)
            elif open_ticket:
                # Counted, never enumerated -- an unassigned backlog is large
                # and listing it would drown everything above it.
                unassigned_idle += 1

        active.sort(key=lambda pair: pair[0], reverse=True)
        shown = [line for _, line in active[:ACTIVE_CAP]]
        for rank, line in enumerate(shown):
            line.rank = rank

        # `unmapped_assignee_count` is deliberately **not** derived here.
        # Counting the assembled lines made it a different question from the
        # `unmapped_assignees` list shipped in the same payload, and gave no
        # answer at all when a gate short-circuited before assembly. `assemble`
        # sets it from that list; see the comment there.

        # Every enumerated block is capped, for the same reason the active list
        # is: a project with 400 open assigned tickets answered "what happened
        # this week?" with 400 lines. The totals are kept so the caller can say
        # "12 of 380 shown" rather than quietly dropping the rest.
        return SummaryAssembly(
            outcome=SummaryOutcome.ASSEMBLED,
            window_spec=window_spec,
            period_start=period_start,
            period_end=now,
            summary_type=summary_type,
            user_id=user_id,
            synced=synced,
            active=shown,
            active_total=len(active),
            no_work_detected=no_work[:BLOCK_CAP],
            no_work_total=len(no_work),
            unassigned_active=unassigned_active[:BLOCK_CAP],
            unassigned_active_total=len(unassigned_active),
            unassigned_idle_count=unassigned_idle,
            up_next=up_next[:BLOCK_CAP],
            up_next_total=len(up_next),
        )

    # ============================================================== persistence

    def persist(
        self,
        *,
        organization_id: str,
        project: Project,
        summary_type: SummaryType,
        window_spec: str,
        body_markdown: str,
        items: Sequence[Dict[str, Any]],
        notes_markdown: Optional[str] = None,
        generated_by: GeneratedBy = GeneratedBy.AGENT,
        source_fingerprint: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
        created_by: Optional[str] = None,
        motivational_quote: str = "",
        highlights: Optional[List[str]] = None,
        concerns: Optional[List[str]] = None,
        ticket_stats: Optional[Dict[str, Any]] = None,
    ) -> Summary:
        """Write a narrated summary by superseding the live one.

        The write order is the only one the live-uniqueness indexes permit: the
        old row leaves the live set *before* the new one enters it, which means
        the UPDATE names an id that does not exist yet. That is what the
        deferred self-FK on `summaries.superseded_by_id` is for -- both checks
        settle at COMMIT. Inserting first fails immediately. See
        `src/domain/summary.py`.

        Does not commit: the caller owns the transaction, so the summary, its
        items and the timeline entry all land together or not at all.
        """
        # `''` is the board-scoped append path's sentinel for "outside the
        # windowed regime", not a window that failed to parse -- canonicalising
        # it would raise on a legitimate caller. Everything else is normalised
        # so the row is written under the spelling `assemble` will look up.
        if window_spec:
            window_spec = canonical_window_spec(window_spec)

        # Read before building, so the replacement can inherit from it. The
        # *write* order below is unchanged and still the only permitted one.
        previous = self.live_summary(
            project_id=project.id,
            user_id=user_id,
            summary_type=summary_type,
            window_spec=window_spec,
        )

        # **Omission inherits; clearing must be asked for.** `notes_markdown`
        # is the one field on a summary a *person* wrote, and it is the one
        # field regeneration must not destroy: re-running the stand-up at 16:00
        # would otherwise silently drop what someone typed at 09:00, and they
        # would have no way to know it had happened. So `None` means "leave it
        # as it was" and an empty string means "delete it" -- a distinction that
        # only exists because the two are genuinely different intentions here,
        # and collapsing them costs someone their words.
        #
        # **A note belongs to a scope, not to a window.** Inheriting only from
        # the identical `window_spec` looked right and quietly lost notes: the
        # CLI's `--window release` used to resolve to "days since the last
        # release", a *different string every day* (`5d`, then `6d`, ...) --
        # a release scope is `release:<version>` now and stable, but any two
        # runs at different windows still differ, so the model stands.
        # A note written on Monday's release run was orphaned on Tuesday --
        # left live in a slot nothing would ask for again, invisible and
        # un-inheritable. Falling back to the newest live summary for the same
        # (project, type, user) fixes that, and is the more defensible model
        # anyway: "short week, read the numbers accordingly" is a fact about
        # the project, not about a three-day lens on it. Scope is still
        # respected -- a team note never reaches a personal summary.
        note_source = (
            previous
            if previous is not None
            else self._latest_live_summary(
                project_id=project.id, user_id=user_id, summary_type=summary_type
            )
        )
        previous_notes = note_source.notes_markdown if note_source is not None else None

        resolved_notes = notes_markdown
        if resolved_notes is None:
            resolved_notes = previous_notes

        # **Stamped whenever the caller supplied the text, inherited otherwise.**
        # Not "whenever the text differs": re-sending an identical note is a
        # person deliberately reconfirming it, and dating that as the original
        # writing makes a still-true note look stale. But a regeneration that
        # merely inherits must never restamp, or the date says "written today"
        # about something typed a month ago -- worse than no date, because it
        # reads as confirmation. The two are told apart by whether the caller
        # said anything about notes at all, which is exactly what `None` means.
        if notes_markdown is not None:
            notes_updated_at = (
                # Naive UTC to match the column -- see `Summary.notes_updated_at`.
                datetime.now(timezone.utc).replace(tzinfo=None)
                if resolved_notes
                else None
            )
        else:
            notes_updated_at = (
                note_source.notes_updated_at if note_source is not None else None
            )

        replacement = Summary(
            organization_id=organization_id,
            project_id=project.id,
            user_id=user_id,
            # Always explicit. `window_spec` has no default on purpose: '' is
            # the sentinel that exempts a row from both uniqueness indexes, and
            # handing that exemption to a forgotten kwarg is exactly the silent
            # failure the missing default prevents.
            window_spec=window_spec,
            period_start=period_start,
            period_end=period_end,
            summary_type=summary_type,
            body_markdown=body_markdown,
            notes_markdown=resolved_notes,
            notes_updated_at=notes_updated_at,
            # The human-amended distinction is a design goal, and until this
            # was accepted every row was AGENT with no writer for the other
            # two -- while the skill instructed callers to record it.
            generated_by=generated_by,
            source_fingerprint=source_fingerprint or {},
            highlights=highlights or [],
            concerns=concerns or [],
            ticket_stats=ticket_stats or {},
            motivational_quote=motivational_quote,
            created_by=created_by,
        )

        if previous is not None:
            previous.superseded_by_id = replacement.id
            self.session.add(previous)
            self.session.flush()

        self.session.add(replacement)
        self.session.flush()

        items = self._dedupe_items(items)
        for rank, item in enumerate(items):
            self.session.add(
                self._summary_item(replacement.id, item, default_rank=rank)
            )

        # **Only the team roll-up reaches the project timeline, and only once a
        # day.** Two separate corrections, both about what the timeline is for:
        #
        # A personal summary is one person's read of their own work. Filing it
        # on the shared feed put every teammate's morning write-up in front of
        # everyone -- and filed it as `SCRUM_SUMMARY`, so the feed also could
        # not tell the two apart. It is still stored, superseded and readable as
        # a `Summary` row; it simply is not a project event.
        #
        # And a scrum summary is a *snapshot*, not an occurrence: running it
        # again at 16:00 does not mean the team stood up twice. Appending made
        # a busy day read as several stand-ups, so the day's entry is rewritten
        # in place instead. See `upsert_daily_timeline_entry`.
        if user_id is None:
            upsert_daily_timeline_entry(
                self.session,
                organization_id=organization_id,
                project_id=project.id,
                event_type=TimelineEventType.SCRUM_SUMMARY,
                title=f"{summary_type.value.title()} summary ({window_spec})",
                summary=(
                    f"A {summary_type.value} summary covering the last "
                    f"{window_spec} was written for {project.name}, listing "
                    f"{len(items)} item(s) of work."
                ),
                created_by=created_by or "agent",
                metadata={
                    "summary_id": replacement.id,
                    "window_spec": window_spec,
                    "user_id": user_id,
                    "item_count": len(items),
                    "superseded_summary_id": previous.id if previous else None,
                },
            )
        return replacement

    @staticmethod
    def _dedupe_items(items: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """One row per ticket, keeping the block that says the most.

        `_assemble` deliberately files one ticket under *both* `no_work_detected`
        and `up_next` -- the two blocks answer different questions of the same
        fact, and that is documented and intended for display. Nothing on the
        write path knew it, so echoing every block back (exactly what the skill
        instructs) stored the same `(summary_id, ticket_id)` twice, and
        `tickets show --with-summaries` printed the ticket's history twice over.

        Deduplication belongs here rather than in `_assemble`, because the
        duplication in the assembly is correct and the duplication in the table
        is not. Precedence is `_BLOCK_PRECEDENCE`; ties keep the first
        occurrence, so a caller's own ordering survives.

        Lines with **no** `ticket_id` are never merged: code activity on a
        branch nobody opened a ticket for is a real, distinct unit of work, and
        collapsing those to one row would lose most of them.
        """
        best: Dict[int, int] = {}  # ticket_id -> index into `kept`
        kept: List[Dict[str, Any]] = []
        for item in items:
            ticket_id = item.get("ticket_id")
            if ticket_id is None:
                kept.append(item)
                continue
            existing = best.get(ticket_id)
            if existing is None:
                best[ticket_id] = len(kept)
                kept.append(item)
            elif _block_rank(item) < _block_rank(kept[existing]):
                kept[existing] = item
        return kept

    @staticmethod
    def _summary_item(
        summary_id: str, item: Dict[str, Any], *, default_rank: int
    ) -> SummaryItem:
        attribution = item.get("attribution") or Attribution.NONE
        if isinstance(attribution, str):
            attribution = Attribution(attribution)
        occurred_at = item.get("occurred_at")
        if isinstance(occurred_at, str):
            try:
                occurred_at = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
            except ValueError:
                occurred_at = None
        return SummaryItem(
            summary_id=summary_id,
            ticket_id=item.get("ticket_id"),
            assignee_user_id=item.get("assignee_user_id"),
            assignee_display=item.get("assignee_display"),
            attribution=attribution,
            repo=item.get("repo"),
            branch=item.get("branch"),
            pr_url=item.get("pr_url"),
            pr_state=item.get("pr_state"),
            # **The verdict is copied, never recomputed.** `releases content`
            # spells it `state`; frozen onto a row it is a verdict -- a judgment
            # made against one window, at one moment. Recomputing it on read is
            # what turned seven shipped tickets into `no_code` the hour v1.11.0
            # was cut.
            verdict=item.get("verdict") or item.get("state"),
            people=_people(item),
            prs=_prs(item),
            body_markdown=item.get("body_markdown"),
            occurred_at=occurred_at,
            # `.get("rank", default)` is wrong here: the request model carries an
            # explicit `rank: None` when the caller omits it, so the key exists
            # and the default never applies -- and `rank` is NOT NULL.
            rank=default_rank if item.get("rank") is None else item["rank"],
            no_work_detected=_no_work(item),
        )

    # ================================================= the narrated write path

    def resolve_narrated_items(
        self, project: Project, items: Sequence[Any]
    ) -> Tuple[int, int]:
        """Recover the ids a narrator dropped. Returns `(tickets, owners)` filled.

        `get_scrum_summary` hands a narrator every field it would need to echo --
        `ticket_id`, `ticket_ref`, `assignee_user_id`. In practice a model asked
        to narrate echoes the *prose* and drops the identifiers, and until this
        existed the row it produced stored a line about a ticket it had not named
        and a person it had not identified. Both gaps are visible on the page and
        neither reads as missing data:

        * `ticket_id IS NULL` -- the title lives on the ticket, so the line
          rendered as **"Untitled"**.
        * `assignee_user_id IS NULL` beside a display name *is* the definition of
          unmapped (`SummaryItem.assignee_unmapped`), so every line in every
          narrated summary marked its owner **"(unmapped)"** -- including people
          whose tickets resolve perfectly, which is most of them.

        Recovering the ids here rather than demanding them keeps the tool
        forgiving in the direction that matters: a narrator that echoes them is
        unaffected, and one that forgets no longer poisons the record.

        **Ids the caller did send are never overwritten.** They are its claim
        about its own assembly, they are tenancy-checked immediately after this
        runs, and re-deriving them would make one request mean two different
        things depending on our matching.
        """
        if not items:
            return (0, 0)

        tickets = self._project_tickets(project.id)
        by_ref = self._tickets_by_ref(project, tickets)
        by_id = {t.id: t for t in tickets if t.id is not None}

        tickets_filled = owners_filled = 0
        for item in items:
            ticket = self._narrated_ticket(item, by_ref, by_id)
            if ticket is not None and getattr(item, "ticket_id", None) is None:
                item.ticket_id = ticket.id
                tickets_filled += 1
            if getattr(item, "assignee_user_id", None) is None:
                owner = self._narrated_owner(project, item, ticket)
                if owner is not None:
                    item.assignee_user_id = owner
                    owners_filled += 1
        return (tickets_filled, owners_filled)

    @staticmethod
    def _narrated_ticket(
        item: Any,
        by_ref: Dict[str, Ticket],
        by_id: Dict[int, Ticket],
    ) -> Optional[Ticket]:
        """Which ticket a narrated line is about, by id or by reference.

        The id branch matters as much as the reference one: a line that named its
        ticket still needs the row itself, because that is where an owner this
        project has already resolved can be read from.
        """
        ticket_id = getattr(item, "ticket_id", None)
        if ticket_id is not None:
            return by_id.get(ticket_id)
        ref = (getattr(item, "ticket_ref", None) or "").strip()
        return by_ref.get(ref.upper()) if ref else None

    def _narrated_owner(
        self, project: Project, item: Any, ticket: Optional[Ticket]
    ) -> Optional[str]:
        """Who a narrated line belongs to, without ever guessing.

        **The ticket's own `assigned_to` comes first**, and it is the branch that
        does the work. Board sync resolves an assignee at the moment it has the
        board's full identity -- a Linear or Jira ticket carries an *email* that
        never reaches `Ticket.assignee`, which stores the display name -- so the
        row is better resolved than anything a display string could achieve
        later. Preferring it also means one person is described identically here
        and on the ticket, which is the whole point of an id.

        Failing that, the display string itself, through the same resolver board
        sync uses. It is genuinely useful because a narrator often writes an
        address (`george@havilandsoftware.com`) where the board wrote a name.
        """
        if ticket is not None and ticket.assigned_to:
            return ticket.assigned_to
        display = (getattr(item, "assignee_display", None) or "").strip()
        if not display:
            return None
        return self._resolve_board_person(project.organization_id, project.id, display)

    def _resolve_board_person(
        self, organization_id: str, project_id: str, display: str
    ) -> Optional[str]:
        """A board's own word for a person → an InnoDay user id, or None.

        Two shapes arrive here and the resolver treats them differently, so both
        are offered: an address matches `users.email` (or `jira_email`) directly,
        and a display name matches a registered handle.

        **Every platform is tried, not just the project's board.** Within one
        organisation a handle already belongs to at most one person -- that is
        `claim_identity`'s rule and two unique constraints hold it up -- so
        widening the search cannot mis-attribute, and narrowing it would fail the
        common case of somebody whose handle was registered against a different
        board than the one that named them.

        Same SAVEPOINT reasoning as `_resolve_handle`: a failed read of
        `user_identity` must not abort the caller's transaction, and unmatched is
        a valid answer rather than an error.
        """
        key = (organization_id, project_id, display)
        if key in self._identity_cache:
            return self._identity_cache[key]
        assignee = BoardAssignee(
            display_name=display,
            # Only when it really is one. A display name in the email slot would
            # be compared against `users.email` for every platform in turn --
            # harmless, but it makes the query say something untrue.
            email=display if _looks_like_email(display) else None,
        )
        resolved: Optional[str] = None
        try:
            with self.session.begin_nested():
                for platform in IdentityPlatform:
                    match = IdentityResolutionService.resolve(
                        self.session,
                        organization_id=organization_id,
                        project_id=project_id,
                        platform=platform,
                        assignee=assignee,
                    )
                    if match:
                        resolved = match.user.id
                        break
        except Exception as exc:  # noqa: BLE001 - unmatched is a valid answer
            logger.warning("Board person %r could not be resolved: %s", display, exc)
        self._identity_cache[key] = resolved
        return resolved

    # ============================================================== reporting

    def unmapped_assignees(self, project_id: str) -> List[Dict[str, Any]]:
        """Board assignee strings on this project that map to no InnoDay user.

        Powers the footer's one-line "N assignees unmapped" hint, and the
        profile picklist. Grouped by handle rather than listed per ticket: the
        point is "these people need mapping", said once.

        `SummaryAssembly.unmapped_assignee_count` is `len()` of exactly this,
        by construction -- see `assemble`.
        """
        if project_id not in self._unmapped_cache:
            self._unmapped_cache[project_id] = self.unmapped_assignees_by_project(
                [project_id]
            ).get(project_id, [])
        return self._unmapped_cache[project_id]

    def unmapped_assignees_by_project(
        self, project_ids: Sequence[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """The same, for a set of projects, in one query.

        **The grouping belongs in SQL.** This used to `select(Ticket)` and count
        in Python, which meant SQLAlchemy hydrating one full `Ticket` object per
        matching row to produce a number -- and both callers run it once per
        project, so the dashboard paid it once per card and the profile page
        paid it again. Measured on 10 projects of 200 tickets it built 2,000
        ORM instances to compute a `GROUP BY`. The columns and the grouping are
        the whole answer; nothing here ever needed a `Ticket`.

        Keyed by project id, with an entry for every id asked about -- a project
        with nobody unmapped answers `[]`, which is a different fact from "not
        looked at" and the caller should not have to guess which it got.
        """
        wanted = [pid for pid in dict.fromkeys(project_ids) if pid]
        grouped: Dict[str, Dict[str, int]] = {pid: {} for pid in wanted}
        if not wanted:
            return {}

        # `trim` in the group key, matching the `.strip()` this replaced: a
        # board that pads a name must not file " Bob" and "Bob" as two people.
        handle = func.trim(Ticket.assignee)
        rows = self.session.exec(
            select(Ticket.project_id, handle, func.count())  # type: ignore[call-overload]
            .where(
                Ticket.project_id.in_(wanted),  # type: ignore[attr-defined]
                Ticket.deleted_at.is_(None),
                Ticket.assigned_to.is_(None),
                Ticket.assignee.is_not(None),
                handle != "",
            )
            .group_by(Ticket.project_id, handle)
        ).all()
        for project_id, assignee, count in rows:
            grouped.setdefault(project_id, {})[str(assignee)] = int(count)

        return {
            project_id: [
                {
                    "assignee": name,
                    "ticket_count": count,
                    "display": f"@{name} (unmapped)",
                }
                # Most-mapped-first, then alphabetical -- the tiebreak is there
                # so two calls on the same data cannot answer in two orders.
                for name, count in sorted(
                    counts.items(), key=lambda kv: (-kv[1], kv[0])
                )
            ]
            for project_id, counts in grouped.items()
        }

    def resolve_user(self, user_ref: str, organization_id: str) -> Optional[User]:
        """A user by id or email **within this organisation**, or None.

        `organization_id` used to be accepted and ignored, which made
        ``?user_id=<someone@else.com>`` a platform-wide account-existence oracle:
        200 for an email with an account anywhere, 404 for one without, readable
        by any authenticated member of any org. The lookup is now joined to an
        active `OrganizationMembership`, so a user outside the org is
        indistinguishable from a user who does not exist.

        Platform members are **not** exempted here, unlike `verify_org_membership`.
        The question this answers is "whose work in this project should I
        summarise?", and someone with no membership has no work in it -- so the
        bypass would buy nothing and cost the property above.
        """
        base = (
            select(User)
            .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
            .where(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.is_active.is_(True),
            )
        )
        by_id = self.session.exec(base.where(User.id == user_ref)).first()
        if by_id is not None:
            return by_id
        return self.session.exec(base.where(User.email == user_ref)).first()


# --------------------------------------------------------------------------- #
# Who still needs mapping
#
# Lived in `src/routers/webui/data.py` until #598's review: the Team page was
# its only caller, so it was written where that page reads from. `GET
# /api/v1/organizations/{org_id}/identities?unmapped=true` made it a second
# caller and the only `src.routers.webui.*` import from outside that package --
# an API router depending on the throwaway UI, which the retirement would then
# have had to route around. `tests/test_webui_is_not_imported_outside_webui.py`
# keeps the edge from coming back.
#
# It sits in this module rather than `identity_resolution` because half of it
# *is* `SummaryService.unmapped_assignees_by_project`; importing SummaryService
# into the resolver would be a cycle, since the resolver is what SummaryService
# attributes with.
# --------------------------------------------------------------------------- #


@dataclass
class UnmappedHandle:
    """A handle seen in someone else's system that maps to nobody here."""

    kind: str  # "board" | "commit"
    handle: str
    detail: str


def unmapped_handles(
    session: Session, organization_id: str, project_ids: Sequence[str]
) -> List[UnmappedHandle]:
    """Handles appearing on this org's work that match no InnoDay user.

    Two sources, one list, because the question is the same either way: *who is
    this?*

    * **Board** assignee strings, from ``SummaryService.unmapped_assignees`` --
      the same capability behind the profile picklist, so the two can never
      disagree about who still needs mapping.
    * **Commit** logins, from pull-request authors. This became answerable only
      once #500 kept the PR objects the sync had been discarding; before that
      there was nothing to match *from*, only a column to match *into*.

    **Resolution is the authority for what counts as mapped, and the commit half
    used to disagree with it in both directions.**

    Too narrow: it tested a login against ``users.github_username`` alone. Since
    #593 an explicit ``user_identity`` row *beats* that column in ``resolve``, so
    a login mapped by a row with the column left NULL resolved to a real person
    and was still listed here as unmapped -- one endpoint answering both ways in
    the same request cycle, with ``POST .../identities`` then refusing the
    mapping the listing had just asked for (409, naming nobody). Reachable
    without a hand-written row: ``POST /ui/{org_ref}/profile/identities`` and the
    auth claim route both accept ``github``.

    Too wide: that query carried no organization filter at all, so *any*
    tenant's ``github_username`` suppressed a row here while ``resolve``, which
    requires active membership, answered ``None`` for the same login. It hid
    rather than leaked, but another tenant's data decided what this one was
    shown -- and shared contractors are exactly the population this list is for.

    ``organization_id`` is what fixes both, and it was an unused parameter until
    it did. The mapped set is now, for this org only: active members'
    ``github_username`` (case-insensitively, as the column path matches), plus
    the github handles of ``user_identity`` rows that belong here -- an active
    member's row, scoped to one of this org's projects or global
    (``project_id IS NULL``). Membership alone is *not* the tenancy boundary:
    ``verify_org_membership`` synthesises ADMIN for any platform member, so the
    row reaches its org through ``Project.organization_id``, the same derivation
    ``_org_scoped_rows`` makes on the mapping listing.

    Registered handles are matched **exactly**, because that is how ``resolve``
    matches them; only the column path is case-insensitive. A row is org-scoped
    rather than project-scoped here, so a handle mapped in one of this org's
    projects stops being listed for all of them -- the list answers "who in this
    org is unidentified?", and somebody has already answered it for that name.
    """
    out: List[UnmappedHandle] = []
    if not project_ids:
        return out

    grouped = SummaryService(session).unmapped_assignees_by_project(list(project_ids))
    for _pid, rows in grouped.items():
        for row in rows:
            handle = row.get("handle") or row.get("assignee")
            if handle:
                out.append(
                    UnmappedHandle(
                        kind="board",
                        handle=str(handle),
                        detail=f"{row.get('ticket_count', 0)} tickets",
                    )
                )

    known_logins = {
        (u or "").lower()
        for u in session.exec(
            select(User.github_username)
            .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
            .where(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.is_active.is_(True),
                User.github_username.is_not(None),  # type: ignore[union-attr]
            )
        ).all()
        if u
    }
    registered_handles = {
        h
        for h in session.exec(
            select(UserIdentity.handle)
            .join(
                OrganizationMembership,
                OrganizationMembership.user_id == UserIdentity.user_id,
            )
            .join(Project, Project.id == UserIdentity.project_id, isouter=True)
            .where(
                UserIdentity.platform == IdentityPlatform.GITHUB,
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.is_active.is_(True),
                or_(
                    UserIdentity.project_id.is_(None),
                    Project.organization_id == organization_id,
                ),
            )
        ).all()
        if h
    }
    counts: Dict[str, int] = {}
    # `for login in`, not `for (login,) in`. `session.exec()` on a single-column
    # select yields **scalars**, not 1-tuples, so unpacking tries to destructure the
    # string itself -- "too many values to unpack" for any login longer than one
    # character. The two sets above iterate the identical query shape correctly,
    # which is how they came to disagree inside one function.
    #
    # Every existing test reached this loop with zero pull-request rows, so the body
    # never ran. It took a fixture with a PR in it to fire.
    for login in session.exec(
        select(RepositoryPullRequest.author_login)
        .join(Repository, Repository.id == RepositoryPullRequest.repository_id)
        .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
        .where(
            ProjectRepository.project_id.in_(project_ids),  # type: ignore[attr-defined]
            RepositoryPullRequest.author_login.is_not(None),  # type: ignore[union-attr]
        )
    ).all():
        if not login:
            continue
        if login.lower() in known_logins or login in registered_handles:
            continue
        counts[login] = counts.get(login, 0) + 1
    for login, n in sorted(counts.items()):
        out.append(
            UnmappedHandle(
                kind="commit",
                handle=login,
                detail=f"{n} open pull request{'s' if n != 1 else ''}",
            )
        )

    # Deduplicate: the same person often appears under both, and one row per
    # (kind, handle) keeps "these people need mapping" said once.
    seen = set()
    unique = []
    for row in out:
        key = (row.kind, row.handle.lower())
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique
