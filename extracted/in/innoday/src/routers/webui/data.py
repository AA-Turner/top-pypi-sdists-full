"""Read queries behind the dashboard, and the small derivations it needs.

Everything here runs in-process against the database. The pages deliberately do
not call ``/api/v1``: a browser cannot send the ``X-Team-Secret`` header
``TeamSecretMiddleware`` requires, and putting the shared secret into page
JavaScript would leak it to every visitor.

Two values the dashboard shows are **derived, not stored**, and both are
judgment calls worth knowing about:

* *Last synced* -- ``Project`` has no sync column. Boards and repositories each
  have their own, and they are independent jobs that fail independently, so this
  reports the most recent of the two. It answers "is anything here stale?", which
  is the question the column exists to answer.
* *Next launch* -- ``Release`` has no target date, only ``released_at`` (set when
  a version ships). So "next" cannot be ordered by date. It is ordered
  ``IN_PROGRESS`` before ``PLANNED``, then by lowest semantic version.

The scrum panel and the profile page add a third and fourth, both documented at
their own functions: which summary a viewer sees by default, and how a board
handle that was matched by *email* is told apart from one somebody claimed.
"""

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sqlalchemy import func, or_
from sqlmodel import Session, select

from src.domain.board import BoardRegistration
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.project_timeline import ProjectTimeline
from src.domain.release import Release, ReleaseStatus
from src.domain.repository import Repository
from src.domain.repository_pull_request import RepositoryPullRequest
from src.domain.scrum import Scrum, ScrumKind, ScrumTicketVisit
from src.domain.summary import Summary, SummaryItem, SummaryType
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.services.release_planning import (
    latest_release,
    next_release,
    pipeline_options,
    semver_key,
    slot_two,
    suggest_next_version,
)
from src.services.summary_service import ACTIVE_CAP, SummaryService
from src.services.ticket_matching import (
    TicketPullRequest,
    pull_requests_by_ticket,
)

#: The window the panel *prefers*, not the only one it will show. The engine
#: takes any spec; the dashboard asks one question ("what happened lately?") and
#: a picker on a read-only panel would be a control that changes nothing, since
#: generating a summary is a local CLI action by design. `3d` is the CLI's
#: default, so a team that runs `innoday summary` plainly gets what it wrote.
#:
#: A team that summarises **weekly** was the case this got wrong: with only a
#: `week` summary stored, an exact-match lookup found nothing and the panel said
#: "No summary generated yet" beside a summary that existed. `_live_summary`
#: now falls back to the newest live summary of any window, and the heading
#: names the window actually on show rather than asserting this one.
PANEL_WINDOW_SPEC = "3d"

#: How #565 spells a release scope in `window_spec`. Matched case-insensitively
#: here because this only ever *reads* the stored value, and a label is not the
#: place to be strict about a spelling the writer already settled.
RELEASE_WINDOW_PREFIX = "release:"

#: Singular unit names for `window_label`.
_WINDOW_UNIT_NAMES = {"h": "hour", "d": "day", "w": "week"}
_WINDOW_LABEL_RE = re.compile(r"^\s*(\d+)\s*([hdw])\s*$", re.IGNORECASE)


def window_label(spec: Optional[str]) -> str:
    """``'3d'`` -> ``'last 3 days'``, for the panel heading.

    ``''`` is the engine's sentinel for "outside the windowed regime", and says
    so rather than being dressed up as a duration. Anything else unparseable is
    shown verbatim: a heading that repeats what is stored is honest, where one
    that guesses is not.
    """
    raw = (spec or "").strip()
    # A release scope, not a duration. #565 stores `release:<version>` as a
    # window_spec, and the verbatim fallback below would render that as
    # "window release:v1.9.0" -- honest, and reading like a leaked internal key.
    # The version is the whole point of that scope, so it leads.
    if raw.lower().startswith(RELEASE_WINDOW_PREFIX):
        version = raw[len(RELEASE_WINDOW_PREFIX) :].strip()
        return f"release {version}" if version else "a release"

    match = _WINDOW_LABEL_RE.match(spec or "")
    if not match:
        return "no fixed window" if not raw else f"window {spec}"
    amount = int(match.group(1))
    unit = _WINDOW_UNIT_NAMES[match.group(2).lower()]
    return f"last {unit}" if amount == 1 else f"last {amount} {unit}s"


@dataclass
class RepoRow:
    """One repository as the dashboard renders it."""

    id: str
    name: str
    layer: str
    url: Optional[str]
    last_synced_at: Optional[datetime]
    # None means "never counted", which is deliberately different from 0. A repo
    # nobody has synced and a repo with nothing open must not look the same.
    open_pr_count: Optional[int] = None
    #: When the count above was read. Carried separately from `last_synced_at`
    #: because that field is stamped by metadata syncs that never read a pull
    #: request, so it cannot date this number -- see `Repository.open_pr_counted_at`.
    #: None means the age is unknown, which the badge says rather than guessing.
    open_pr_counted_at: Optional[datetime] = None
    # True when the layer came from the project link rather than the repo-wide
    # fallback. The picker writes the link, so this says whether what you see is
    # what you would be editing.
    layer_is_per_project: bool = False
    #: Whether this repository's last sync failed (#499). Per repo rather than
    #: only per project, because "GitHub is broken" and "one repo is broken" are
    #: different problems and the card should be able to name which.
    errored: bool = False


@dataclass
class ProjectCard:
    """One project card: identity, freshness, its repos, and its next release."""

    id: str
    alias: str
    name: str
    last_synced_at: Optional[datetime]
    repos: List[RepoRow] = field(default_factory=list)
    next_release: Optional[Release] = None
    # Work in flight, for the launch panel. `in_test` maps to IN_REVIEW: there is
    # no IN_TEST status in the enum, and inventing one here would misreport rather
    # than reveal. Renamed in the UI to match what the board actually tracks.
    in_progress: int = 0
    in_review: int = 0
    #: Work that exists but has not started: TODO and BACKLOG together. They are
    #: one number on the card because the distinction between them is a board's
    #: internal grooming state, and the card answers "how much is queued".
    planned: int = 0
    #: Shipped. The one count on the card that goes up rather than down, and the
    #: reason the block reads as progress instead of as a to-do list.
    done: int = 0
    #: The same four buckets again, counting **only tickets whose `release`
    #: matches `next_release.version`** -- what the card's "Release tickets"
    #: block renders. All four are 0 when `next_release` is None, and 0 is also
    #: the honest answer when the version simply has nothing attached to it: on
    #: real data most projects have no ticket carrying any version at all.
    #:
    #: Separate fields rather than a redefinition of the four above, because the
    #: project-wide numbers are still read elsewhere -- `routes.py` builds the
    #: project nav's ticket badge from `in_progress + in_review`, and that badge
    #: counts the Tickets tab, which is not release-scoped.
    release_planned: int = 0
    release_in_progress: int = 0
    release_in_review: int = 0
    release_done: int = 0
    next_version_suggestion: Optional[str] = None
    # The newest shipped version. Shown when nothing is upcoming: a project that
    # has plainly released things should say so, not show a dash.
    latest_released: Optional[Release] = None
    # The row this card was built from. Nothing renders it -- it is here so a
    # caller that needs the `Project` (the scrum panel does) can take the one
    # already loaded instead of issuing the identical query a second time.
    project: Optional[Project] = None
    #: Every repository this project has is archived. **Not derivable from
    #: `repos`**, which `_repo_rows_by_project` filters archived rows out of --
    #: so a project whose repos are all archived arrives here with `repos == []`,
    #: identical to a project that has never had one. The two must not render the
    #: same: the first is finished, the second is new.
    archived_only: bool = False
    # What this project is wired to, for the three header icons. All three are
    # derived from rows `project_cards` already reads, so none of them costs a
    # query -- which is the only reason three icons are affordable on a page
    # that renders one card per project.
    #
    # `github_connected` is "repositories are linked", deliberately still not
    # "the last sync succeeded" -- the outcome is carried by `github_errored`
    # below, and `_integration_icon` lets red beat green, so the two do not need
    # to be folded into one field. Keeping them apart is what keeps the three
    # states distinguishable: a dead token over stale repo rows is red, a project
    # with neither repos nor a failure is grey.
    github_connected: bool = False
    # The active board's platform, or None for "no board registered". None is
    # rendered as a greyed fallback glyph rather than omitting the icon: a
    # missing icon and an unconfigured one would be indistinguishable, and the
    # whole point of the row is that you can see what is *not* set up.
    board_platform: Optional[str] = None
    # Whether `Project.project_context` holds anything. Reads grey on every
    # project until issue #498 ships a generator -- nothing writes that column
    # today.
    has_context: bool = False
    # Whether the last attempt to reach each integration failed. Distinct from
    # "not configured": grey means nothing is wired, red means something is and
    # it is broken -- and before #499 there was no way to say the second, so an
    # expired token rendered exactly like a healthy connection.
    github_errored: bool = False
    #: Why the GitHub sync failed, when the project itself recorded it. None for a
    #: per-repo failure -- that path marks the repository, not the project, and
    #: `RepoRow` carries only a bool, so the generic title stands in there.
    #:
    #: Invariant: `github_errored_at` and `github_error_message` are always written
    #: together and always cleared together, which is what lets this be populated
    #: unconditionally at the call site -- see the comment there.
    github_error: Optional[str] = None
    board_errored: bool = False


def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Normalise to timezone-aware UTC. SQLite returns naive, Postgres aware."""
    if value is None:
        return None
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _newest(*values: Optional[datetime]) -> Optional[datetime]:
    present = [v for v in (_as_utc(v) for v in values) if v is not None]
    return max(present) if present else None


def member_organizations(session: Session, user: User) -> List[Organization]:
    """Every org the user can open, ordered by name.

    Platform members see all of them -- the same bypass
    ``rbac.verify_org_membership`` applies, kept consistent so the org switcher
    can never list an org whose dashboard would then 404.
    """
    if user.is_platform_member:
        return list(
            session.exec(
                select(Organization)
                .where(Organization.is_active == True)  # noqa: E712
                .order_by(Organization.name)
            ).all()
        )

    return list(
        session.exec(
            select(Organization)
            .join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            )
            .where(
                OrganizationMembership.user_id == user.id,
                OrganizationMembership.is_active == True,  # noqa: E712
                Organization.is_active == True,  # noqa: E712
            )
            .order_by(Organization.name)
        ).all()
    )


def can_open(session: Session, user: User, organization_id: str) -> bool:
    """Whether the user may see this org's dashboard."""
    if user.is_platform_member:
        return True
    membership = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == user.id,
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.is_active == True,  # noqa: E712
        )
    ).first()
    return membership is not None


def _repo_rows_by_project(
    session: Session, project_ids: List[str]
) -> Dict[str, Tuple[List[RepoRow], Optional[datetime], bool]]:
    """Active repos for every project at once, its newest repo sync, and whether
    it has an archived repo at all.

    One query for all projects rather than one per project -- the board and
    release lookups in ``project_cards`` already batch this way, and a dashboard
    that issues a query per card gets slower exactly as an org grows.
    ``test_repo_lookup_does_not_scale_with_project_count`` holds that at exactly
    one statement touching ``project_repositories``.

    **The archived flag rides along rather than taking a second query**, which is
    why the ``archived`` filter moved out of SQL and into the loop below. The two
    facts come from the same rows: a project whose repos are all archived
    contributes no ``RepoRow`` at all, so "has archived repos" is the only thing
    left that can tell it apart from a project that has never had one -- and
    asking for it separately would have doubled the statement count the test
    exists to pin.
    """
    result: Dict[str, Tuple[List[RepoRow], Optional[datetime], bool]] = {
        pid: ([], None, False) for pid in project_ids
    }
    if not project_ids:
        return result

    links = session.exec(
        select(ProjectRepository, Repository)
        .join(Repository, Repository.id == ProjectRepository.repository_id)
        .where(
            ProjectRepository.project_id.in_(project_ids),  # type: ignore[attr-defined]
            ProjectRepository.is_active == True,  # noqa: E712
            Repository.deleted == False,  # noqa: E712
        )
    ).all()

    for link, repo in links:
        rows, newest, had_archived = result[link.project_id]
        if repo.archived:
            # Counted, never listed. The card is about live work, and an archived
            # repo in the list would be a row nobody can act on.
            result[link.project_id] = (rows, newest, True)
            continue
        link_layer = getattr(link.layer, "value", link.layer)
        rows.append(
            RepoRow(
                id=repo.id,
                name=repo.name,
                layer=_layer_of(link, repo),
                url=repo.github_url or repo.url,
                last_synced_at=_as_utc(repo.last_synced_at),
                open_pr_count=repo.open_pr_count,
                open_pr_counted_at=_as_utc(repo.open_pr_counted_at),
                layer_is_per_project=bool(
                    link_layer and link_layer != RepositoryLayer.UNASSIGNED.value
                ),
                errored=repo.errored_at is not None,
            )
        )
        result[link.project_id] = (
            rows,
            _newest(newest, repo.last_synced_at),
            had_archived,
        )

    for rows, _newest_at, _archived in result.values():
        rows.sort(key=lambda r: r.name.lower())
    return result


def _layer_of(link: ProjectRepository, repo: Repository) -> str:
    """Resolve a repo's layer: the project's classification wins.

    ``ProjectRepository.layer`` is per-project and authoritative -- the same repo
    can be the UI layer of one project and a library to another.
    ``Repository.layer`` is the org-wide fallback, and ``unassigned`` closes it
    out so the template never has to handle ``None``.
    """
    link_layer = getattr(link.layer, "value", link.layer)
    if link_layer and link_layer != RepositoryLayer.UNASSIGNED.value:
        return str(link_layer)
    if repo.layer:
        return str(repo.layer)
    return RepositoryLayer.UNASSIGNED.value


def _status_key(status: Any) -> str:
    """One canonical spelling for a ticket status read back from a count query.

    The enum's *values* are lowercase with spaces ("in progress") while its
    *names* use underscores, and Postgres stores the names. Normalise both to one
    shape rather than guessing which side a given row came from.
    """
    label = getattr(status, "value", status)
    return str(label).upper().replace(" ", "_").replace("-", "_")


def project_cards(session: Session, organization_id: str) -> List[ProjectCard]:
    """Every project in an org, with its repos, freshness and next release."""
    projects = session.exec(
        select(Project)
        .where(Project.organization_id == organization_id)
        .order_by(Project.alias)
    ).all()
    if not projects:
        return []

    project_ids = [p.id for p in projects]

    board_sync: Dict[str, Optional[datetime]] = {}
    # The platform rides out of the same loop rather than a second query. It is
    # the raw `BoardType` value ("linear", "jira", ...), not an `IdentityPlatform`
    # -- this picks an icon, and a board type with no identity platform still has
    # a board worth showing. `_project_platform` below narrows to identity
    # platforms because it answers a different question (what can you claim a
    # handle against), and that is why the two do not share a helper.
    board_platform: Dict[str, str] = {}
    board_failed: set = set()
    for board in session.exec(
        select(BoardRegistration).where(
            BoardRegistration.project_id.in_(project_ids),  # type: ignore[attr-defined]
            BoardRegistration.is_active == True,  # noqa: E712
        )
    ).all():
        board_sync[board.project_id] = _newest(
            board_sync.get(board.project_id), board.last_sync_at
        )
        board_platform[board.project_id] = str(
            getattr(board.board_type, "value", board.board_type)
        )
        if board.errored_at is not None:
            board_failed.add(board.project_id)

    releases: Dict[str, List[Release]] = {}
    for release in session.exec(
        select(Release).where(
            Release.project_id.in_(project_ids),  # type: ignore[attr-defined]
            Release.deleted_at.is_(None),
        )
    ).all():
        releases.setdefault(release.project_id, []).append(release)

    # The open release per project, resolved **once**. The card's `next_release`
    # and the release-scoped counts below have to name the same version -- calling
    # `next_release` a second time inside the card loop is how the heading and the
    # numbers under it would drift apart.
    upcoming_by_project: Dict[str, Optional[Release]] = {
        project.id: next_release(releases.get(project.id, [])) for project in projects
    }

    repos_by_project = _repo_rows_by_project(session, project_ids)
    # Two different failures, one icon. A per-repo `errored_at` says "part of what
    # you see could not be read" -- one failing repo is enough, because the icon
    # answers "can I trust what this shows". `Project.github_errored_at` says "the
    # sync itself died", and it is the only signal available when the project has
    # no repo rows for a failure to attach to, which is precisely what a sync that
    # died in discovery leaves behind (#640).
    #
    # Free: `projects` rows are already loaded above, so this adds no statement.
    github_failed = {
        p.id
        for p in projects
        if p.github_errored_at is not None
        or any(row.errored for row in repos_by_project[p.id][0])
    }

    # Work in flight per project, one grouped query rather than one per card.
    # `deleted_at IS NULL` because a soft-deleted ticket is not work: without it
    # the card counted rows nothing else on the page will show, and the "done"
    # figure -- which is a claim about delivery -- would have been the worst
    # affected, since deletion is most common on tickets that never shipped.
    counts: Dict[str, Dict[str, int]] = {}
    for project_id, status, total in session.exec(
        select(Ticket.project_id, Ticket.status, func.count())  # type: ignore[arg-type]
        .where(
            Ticket.project_id.in_(project_ids),  # type: ignore[attr-defined]
            Ticket.deleted_at.is_(None),
        )
        .group_by(Ticket.project_id, Ticket.status)
    ).all():
        counts.setdefault(project_id, {})[_status_key(status)] = int(total)

    # The same counts, narrowed to each project's open release. Grouped by release
    # as well as status so one query serves every card; the `project_id` half of
    # the key is load-bearing, since a version string is only unique within a
    # project and two projects on `v1.0.0` would otherwise pool their tickets.
    #
    # `Ticket.release` is matched **byte-exact, with no normalisation**, because
    # every other reader matches it that way (`Ticket.release == release.version`).
    # A count using a looser rule than the release page and the shipped stamp
    # would claim work those two do not agree is in the release.
    open_versions = {r.version for r in upcoming_by_project.values() if r is not None}
    release_counts: Dict[Tuple[str, str], Dict[str, int]] = {}
    if open_versions:
        for project_id, version, status, total in session.exec(
            select(Ticket.project_id, Ticket.release, Ticket.status, func.count())  # type: ignore[arg-type]
            .where(
                Ticket.project_id.in_(project_ids),  # type: ignore[attr-defined]
                Ticket.deleted_at.is_(None),
                Ticket.release.in_(open_versions),  # type: ignore[attr-defined]
            )
            .group_by(Ticket.project_id, Ticket.release, Ticket.status)
        ).all():
            release_counts.setdefault((project_id, version), {})[
                _status_key(status)
            ] = int(total)

    cards: List[ProjectCard] = []
    for project in projects:
        repos, repo_sync, had_archived = repos_by_project[project.id]
        project_releases = releases.get(project.id, [])
        upcoming = upcoming_by_project[project.id]
        by_status = counts.get(project.id, {})
        for_release = (
            release_counts.get((project.id, upcoming.version), {}) if upcoming else {}
        )
        cards.append(
            ProjectCard(
                id=project.id,
                alias=project.alias,
                name=project.name,
                last_synced_at=_newest(board_sync.get(project.id), repo_sync),
                repos=repos,
                next_release=upcoming,
                in_progress=by_status.get("IN_PROGRESS", 0),
                in_review=by_status.get("IN_REVIEW", 0),
                planned=by_status.get("TODO", 0) + by_status.get("BACKLOG", 0),
                done=by_status.get("DONE", 0),
                release_in_progress=for_release.get("IN_PROGRESS", 0),
                release_in_review=for_release.get("IN_REVIEW", 0),
                release_planned=(
                    for_release.get("TODO", 0) + for_release.get("BACKLOG", 0)
                ),
                release_done=for_release.get("DONE", 0),
                next_version_suggestion=(
                    None if upcoming else suggest_next_version(project_releases)
                ),
                latest_released=(
                    None if upcoming else latest_release(project_releases)
                ),
                project=project,
                archived_only=(not repos and had_archived),
                github_connected=bool(repos),
                github_errored=project.id in github_failed,
                # Unconditional, and safe only because of one invariant:
                # `github_errored_at` and `github_error_message` are written
                # together by `_record_project_sync_error` and cleared together by
                # `_clear_project_sync_error`, so a message here always belongs to
                # a failure the icon is currently showing. A change that ever
                # writes one without the other makes this line render the reason
                # for a failure that has already been forgiven -- or drop the
                # reason for one still on screen. Keep the pair, or gate this on
                # `project.github_errored_at`.
                github_error=project.github_error_message,
                board_platform=board_platform.get(project.id),
                board_errored=project.id in board_failed,
                # `.strip()` because a column holding only whitespace is a column
                # nobody wrote anything into, and lighting the icon for it would
                # be the one failure mode this indicator exists to rule out.
                has_context=bool((project.project_context or "").strip()),
            )
        )
    return cards


# --------------------------------------------------------------------------- #
# Scrum summary panel
# --------------------------------------------------------------------------- #


@dataclass
class SummaryRow:
    """One line of a stored summary, as the panel renders it."""

    ticket_id: Optional[int]
    ticket_ref: Optional[str]
    title: Optional[str]
    url: Optional[str]
    owner_label: Optional[str]
    body_markdown: Optional[str]
    repo: Optional[str]
    branch: Optional[str]
    pr_url: Optional[str]
    pr_state: Optional[str]
    occurred_at: Optional[datetime]
    #: How the ticket was judged when the line was written -- `shipped`,
    #: `not_merged`, `no_code` and the rest. **Read from the stored row, never
    #: recomputed:** the verdict belongs to the window the summary covered, and
    #: recomputing it against today's window is what made every ticket on a
    #: freshly cut release read as `no_code`.
    verdict: Optional[str] = None
    #: The pull requests the summary recorded, as stored. `pull_requests` below is
    #: a live *open*-PR join, so a shipped release ticket delivered by two merged
    #: pull requests matched nothing there and rendered as having none -- the
    #: recompute-on-read failure the `verdict` column exists to prevent, applied
    #: to code links.
    prs: List[Dict[str, Any]] = field(default_factory=list)
    #: Everyone credited on the ticket. `owner_label` is the one name the board
    #: carried; a ticket two people delivered has to show both.
    people: List[str] = field(default_factory=list)
    #: Every open pull request naming this ticket, from `pull_requests_by_ticket`.
    #: Distinct from `pr_url` above, which is the single one the summary *item*
    #: recorded at assembly time -- that is one repository's worth, and a ticket
    #: can have work in several.
    pull_requests: List[TicketPullRequest] = field(default_factory=list)


@dataclass
class SummaryPanel:
    """The scrum panel for one project, for one viewer.

    ``summary is None`` is not one state but two, and the panel must say which:
    nobody has generated one, or the viewer has no board identity so nothing
    could be attributed to them. ``identity_mapped`` is what tells them apart.
    """

    project_id: str
    scope: str  # "team" | "yours"
    has_personal: bool
    identity_mapped: bool
    unmapped_count: int
    #: Whether the viewer has a board handle registered *anywhere*. Distinct from
    #: `identity_mapped`, which is about this project, and the distinction is what
    #: decides whether "map your board handle" is advice or noise: identities are
    #: usually registered per project, so someone mapped on two of six projects is
    #: not unmapped -- they are simply absent from this board.
    handles_mapped: bool = False
    summary: Optional[Summary] = None
    active: List[SummaryRow] = field(default_factory=list)
    no_work: List[SummaryRow] = field(default_factory=list)
    unassigned_active: List[SummaryRow] = field(default_factory=list)

    @property
    def window_label(self) -> str:
        """The window the panel is actually showing, for the heading.

        The summary's own spec when there is one, so a `week` summary is not
        captioned "last 3 days". With nothing to show, the preferred window --
        the empty state is about what would appear, and that is what the CLI
        writes by default.
        """
        if self.summary is None:
            return window_label(PANEL_WINDOW_SPEC)
        return window_label(self.summary.window_spec)


def _live_summary(
    session: Session,
    *,
    project_id: str,
    summary_type: SummaryType,
    user_id: Optional[str],
) -> Optional[Summary]:
    """The current summary for one scope: the panel's window, else any window.

    Exact-match-only was wrong for every team that does not summarise on the
    panel's cadence. A team running `innoday summary --window 1w` had its
    summary stored under `week` and the dashboard reported "No summary generated
    yet" -- an empty state that names the wrong cause and offers a command they
    are already running. The preferred window still wins when it exists; the
    fallback is the newest live summary of any window, and the heading says
    which one that turned out to be.
    """
    base = select(Summary).where(
        Summary.project_id == project_id,
        Summary.summary_type == summary_type,
        Summary.superseded_by_id.is_(None),
    )
    base = (
        base.where(Summary.user_id.is_(None))
        if user_id is None
        else base.where(Summary.user_id == user_id)
    )
    newest = base.order_by(Summary.created_at.desc())

    preferred = session.exec(
        newest.where(Summary.window_spec == PANEL_WINDOW_SPEC)
    ).first()
    if preferred is not None:
        return preferred
    return session.exec(newest).first()


def live_summaries_for(
    session: Session,
    project_ids: Sequence[str],
    user_id: str,
) -> Dict[Tuple[str, SummaryType], Summary]:
    """The current PERSONAL and SCRUM summary for many projects, in two queries.

    ``_live_summary`` answers one project at a time and issues two selects to do
    it -- so the dashboard, which calls ``summary_panel`` once per card, paid
    2xN. Its neighbours in that same function (``project_cards``,
    ``unmapped_counts_for``) were both deliberately batched to avoid exactly
    this; the panel reads were simply never given the same treatment (#501).

    Two queries total: one for the viewer's personal summaries, one for the
    team's. **Not one query with an OR** -- `user_id IS NULL` and
    `user_id = :me` select different scopes, and combining them would make the
    per-row "which of these is mine" decision happen in Python over a result set
    that is mostly not.

    The preference inside each scope is the same one ``_live_summary`` applies,
    and is applied here rather than re-queried: ordering by
    ``(window_spec = PANEL_WINDOW_SPEC) DESC, created_at DESC`` and keeping the
    first row per project reproduces "preferred window if it exists, else the
    newest of any window" without a second round trip per project.
    """
    if not project_ids:
        return {}

    found: Dict[Tuple[str, SummaryType], Summary] = {}
    for summary_type, scope in (
        (SummaryType.PERSONAL, user_id),
        (SummaryType.SCRUM, None),
    ):
        base = select(Summary).where(
            Summary.project_id.in_(project_ids),  # type: ignore[attr-defined]
            Summary.summary_type == summary_type,
            Summary.superseded_by_id.is_(None),
        )
        base = (
            base.where(Summary.user_id.is_(None))
            if scope is None
            else base.where(Summary.user_id == scope)
        )
        rows = session.exec(base.order_by(Summary.created_at.desc())).all()
        # Preferred window wins; otherwise the newest of any window. Sorting in
        # Python because the tie-break is a boolean over a value already loaded,
        # and expressing it in SQL would mean a CASE that every backend spells
        # differently -- this runs over one org's summaries, not a table scan.
        rows = sorted(
            rows,
            key=lambda r: (r.window_spec != PANEL_WINDOW_SPEC,),
        )
        for row in rows:
            found.setdefault((row.project_id, summary_type), row)
    return found


def _ticket_ref(ticket: Optional[Ticket]) -> Optional[str]:
    """How to name a ticket in one short token.

    The board's own id when there is one (`PF-398`), because that is what
    people say out loud. Falling back to the internal integer would be a
    reference nobody can look up anywhere else, so it is prefixed to make the
    difference visible rather than passed off as a board key.
    """
    if ticket is None:
        return None
    if ticket.external_ticket_id:
        return ticket.external_ticket_id
    return f"#{ticket.id}"


def _summary_rows(
    session: Session, summary: Summary, *, scrum: bool
) -> Tuple[List[SummaryRow], List[SummaryRow], List[SummaryRow]]:
    """A stored summary's items, sorted into the blocks the panel renders.

    ``SummaryItem`` records no block -- deliberately, since the block is a
    property of how a line was *assembled* and the table stores what was
    *written*. The three enumerated blocks are recoverable from the columns
    that are stored, and each rule is the assembler's own:

    * ``no_work_detected`` is an explicit column, set by the writer.
    * an item with activity (a PR, a repo, a timestamp) but no owner is the
      unassigned-work-happening case -- that block exists precisely because the
      board named nobody while the code had an author.
    * everything else is active.

    Sorted most-recent first on ``occurred_at``, with undated items last: an
    item with no timestamp has no claim to the top of a recency-ordered list.
    """
    items = list(
        session.exec(
            select(SummaryItem)
            .where(SummaryItem.summary_id == summary.id)
            .order_by(SummaryItem.rank)
        ).all()
    )
    ticket_ids = {i.ticket_id for i in items if i.ticket_id is not None}
    tickets: Dict[int, Ticket] = {}
    if ticket_ids:
        tickets = {
            t.id: t
            for t in session.exec(
                select(Ticket).where(Ticket.id.in_(ticket_ids))  # type: ignore[attr-defined]
            ).all()
        }

    def _row(item: SummaryItem) -> SummaryRow:
        ticket = tickets.get(item.ticket_id) if item.ticket_id is not None else None
        return SummaryRow(
            ticket_id=item.ticket_id,
            ticket_ref=_ticket_ref(ticket),
            title=ticket.summary if ticket else None,
            url=ticket.url if ticket else None,
            # `@name` is a team-mode decoration: in a personal summary every
            # line is the viewer's own, and prefixing their own name to all of
            # them is noise. The unmapped marker rides along with it, because
            # it is only ever attached to a name being shown.
            owner_label=_owner_label(item) if scrum else None,
            body_markdown=item.body_markdown,
            repo=item.repo,
            branch=item.branch,
            pr_url=item.pr_url,
            pr_state=item.pr_state,
            occurred_at=_as_utc(item.occurred_at),
            verdict=item.verdict,
            prs=list(item.prs or []),
            # Falls back to the single board name, so a row written before the
            # column existed still shows who it belonged to rather than nobody.
            people=list(item.people or [])
            or ([item.assignee_display] if item.assignee_display else []),
        )

    active: List[SummaryRow] = []
    no_work: List[SummaryRow] = []
    unassigned_active: List[SummaryRow] = []
    for item in items:
        if item.no_work_detected:
            no_work.append(_row(item))
        elif not (item.assignee_display or "").strip() and (
            item.pr_url or item.repo or item.occurred_at
        ):
            unassigned_active.append(_row(item))
        else:
            active.append(_row(item))

    active.sort(
        key=lambda r: (
            r.occurred_at is not None,
            r.occurred_at or datetime.min.replace(tzinfo=timezone.utc),
        ),
        reverse=True,
    )
    return active[:ACTIVE_CAP], no_work, unassigned_active


def _owner_label(item: SummaryItem) -> Optional[str]:
    """``@Name`` -- or ``@Name (unmapped)`` when it maps to no InnoDay user.

    Same rule and the same wording as ``SummaryLine.owner_label`` in the
    engine, so the panel and the CLI never describe one row two ways.
    """
    display = (item.assignee_display or "").strip()
    if not display:
        return None
    if item.assignee_user_id:
        return f"@{display}"
    return f"@{display} (unmapped)"


def viewer_has_identity(session: Session, user: User, project: Project) -> bool:
    """Whether anything on this project could be attributed to the viewer.

    Two ways, and both count -- which is the point. A claimed handle is the
    obvious one. The other is a ticket already resolved to them: on Linear the
    board supplies an email and the resolver matches it without anyone ever
    registering a handle, so a "you have no identity" message keyed only on
    `user_identity` would be wrong for the platform most likely to work.
    """
    claimed = session.exec(
        select(UserIdentity.id).where(
            UserIdentity.user_id == user.id,
            # `IN (project_id, NULL)` would silently never match the global
            # rows: `NULL IN (...)` is NULL, not true, so a person whose only
            # handle is the platform-wide one would be told they have none.
            or_(
                UserIdentity.project_id == project.id,
                UserIdentity.project_id.is_(None),
            ),
        )
    ).first()
    if claimed is not None:
        return True
    assigned = session.exec(
        select(Ticket.id).where(
            Ticket.project_id == project.id,
            Ticket.assigned_to == user.id,
            Ticket.deleted_at.is_(None),
        )
    ).first()
    return assigned is not None


def viewer_has_any_handle(session: Session, user: User) -> bool:
    """Whether this person has registered a board handle anywhere at all.

    Deliberately unscoped -- no project, no organisation. It answers exactly one
    question: is there anything left for them to do on the profile page? Someone
    with a handle on one project has already been there and done it, and telling
    them to go again from every *other* project is advice that cannot be followed.

    ``viewer_has_identity`` remains the project-scoped fact, and the two are used
    together: one decides whether the viewer's work can be shown, the other
    whether they are being asked to fix it.
    """
    found = session.exec(
        select(UserIdentity.id).where(UserIdentity.user_id == user.id)
    ).first()
    return found is not None


def summary_panel(
    session: Session,
    project: Project,
    user: User,
    *,
    prefer_personal: bool = False,
    unmapped_counts: Optional[Dict[str, int]] = None,
    prefetched: Optional[Dict[Tuple[str, SummaryType], Summary]] = None,
) -> SummaryPanel:
    """The scrum panel for one project card.

    **Team by default.** The panel is populated for everyone the moment one
    person runs `innoday summary --scrum`, which is what makes it worth putting
    on a shared dashboard at all; a personal-by-default panel would be empty
    for all but its author. "Yours" is offered only when a personal summary for
    this viewer actually exists -- a toggle that leads to a blank box is worse
    than no toggle.

    ``prefetched`` is ``live_summaries_for``'s output, for a caller rendering
    several cards: without it this issues two selects **per call**, which on the
    dashboard meant 2xN (#501). A single-panel caller omits it and pays two.

    ``unmapped_counts`` lets a caller rendering several cards resolve the
    footer's count for all of them in one query (see
    ``SummaryService.unmapped_assignees_by_project``) instead of once per card.
    Omitted, this asks for its own -- the single-panel case stays a one-liner.
    """
    if prefetched is not None:
        personal = prefetched.get((project.id, SummaryType.PERSONAL))
        team = prefetched.get((project.id, SummaryType.SCRUM))
    else:
        personal = _live_summary(
            session,
            project_id=project.id,
            summary_type=SummaryType.PERSONAL,
            user_id=user.id,
        )
        team = _live_summary(
            session,
            project_id=project.id,
            summary_type=SummaryType.SCRUM,
            user_id=None,
        )

    show_personal = prefer_personal and personal is not None
    chosen = personal if show_personal else team

    unmapped = (
        unmapped_counts.get(project.id, 0)
        if unmapped_counts is not None
        else len(SummaryService(session).unmapped_assignees(project.id))
    )
    panel = SummaryPanel(
        project_id=project.id,
        scope="yours" if show_personal else "team",
        has_personal=personal is not None,
        identity_mapped=viewer_has_identity(session, user, project),
        handles_mapped=viewer_has_any_handle(session, user),
        unmapped_count=unmapped,
        summary=chosen,
    )
    if chosen is None:
        return panel

    active, no_work, unassigned = _summary_rows(
        session, chosen, scrum=not show_personal
    )
    # One join for the panel, not one per row: a ticket's pull requests live in
    # several repositories, and the stored item knows about at most one of them.
    prs = pull_requests_by_ticket(session, project.id)
    for row in (*active, *no_work, *unassigned):
        if row.ticket_id is not None:
            row.pull_requests = prs.get(row.ticket_id, [])
    panel.active = active
    panel.no_work = no_work
    panel.unassigned_active = unassigned
    return panel


def unmapped_counts_for(session: Session, project_ids: Sequence[str]) -> Dict[str, int]:
    """How many unmapped board assignees each project has, in one query."""
    grouped = SummaryService(session).unmapped_assignees_by_project(project_ids)
    return {project_id: len(rows) for project_id, rows in grouped.items()}


# --------------------------------------------------------------------------- #
# Profile page
# --------------------------------------------------------------------------- #


@dataclass
class IdentityRow:
    """One project's board-handle mapping for one person."""

    project_id: str
    project_alias: str
    project_name: str
    #: The board's platform, as an ``IdentityPlatform`` value, or None when the
    #: project has no board -- in which case there is nothing to map yet and
    #: the row says so rather than offering a form that cannot resolve anything.
    platform: Optional[str]
    handle: Optional[str]
    match_source: Optional[str]
    #: True when the handle was never claimed: the board supplied an email and
    #: the resolver matched it. Overridable -- claiming writes a real row.
    matched_by_email: bool
    #: Whether the claimed row is the person's global handle rather than one
    #: scoped to this project. Shown, because editing it here narrows it.
    is_global: bool
    #: Board assignee strings on this project that map to nobody. The primary
    #: way anyone maps themselves -- see ``profile_rows``.
    candidates: List[Dict[str, Any]] = field(default_factory=list)


def _project_platform(session: Session, project_ids: List[str]) -> Dict[str, str]:
    """Each project's board platform, from its active board registration."""
    platforms: Dict[str, str] = {}
    if not project_ids:
        return platforms
    for board in session.exec(
        select(BoardRegistration).where(
            BoardRegistration.project_id.in_(project_ids),  # type: ignore[attr-defined]
            BoardRegistration.is_active == True,  # noqa: E712
            BoardRegistration.deleted_at.is_(None),
        )
    ).all():
        value = getattr(board.board_type, "value", board.board_type)
        try:
            platforms[board.project_id] = IdentityPlatform(str(value)).value
        except ValueError:
            # A board type with no identity platform is not an error -- there
            # is simply nothing to map against, and inventing a platform name
            # would make the claim form write rows the resolver never reads.
            continue
    return platforms


def profile_rows(
    session: Session, user: User, organization_id: str
) -> List[IdentityRow]:
    """One row per project in this org: how the viewer is known to its board.

    The picklist of unmapped assignee strings is the **primary** mapping path,
    not a fallback for when auto-matching fails. Auto-matching needs the board
    to supply an email: Linear reliably does, Jira usually does not (Atlassian
    privacy settings hide it), and Trello never exposes member email at all --
    so on two of the three boards this repo syncs, picking your own name off a
    list is the only way it ever happens. It is fed from the same
    ``unmapped_assignees`` capability behind the summary footer's count, so the
    list and the count can never disagree. Resolved for every project in one
    grouped query rather than once per row -- this page shows every project in
    the org, so per-row was the worst place in the app to pay it.
    """
    projects = list(
        session.exec(
            select(Project)
            .where(Project.organization_id == organization_id)
            .order_by(Project.alias)
        ).all()
    )
    if not projects:
        return []

    project_ids = [p.id for p in projects]
    platforms = _project_platform(session, project_ids)

    identities = list(
        session.exec(
            select(UserIdentity).where(
                UserIdentity.user_id == user.id,
                # Same NULL trap as `viewer_has_identity`: a global row has to
                # be matched with IS NULL, never by putting None in an IN list.
                or_(
                    UserIdentity.project_id.in_(project_ids),  # type: ignore[attr-defined]
                    UserIdentity.project_id.is_(None),
                ),
            )
        ).all()
    )
    scoped = {(i.project_id, i.platform.value): i for i in identities if i.project_id}
    globals_ = {i.platform.value: i for i in identities if i.project_id is None}

    candidates = SummaryService(session).unmapped_assignees_by_project(project_ids)
    rows: List[IdentityRow] = []
    for project in projects:
        platform = platforms.get(project.id)
        row = IdentityRow(
            project_id=project.id,
            project_alias=project.alias,
            project_name=project.name,
            platform=platform,
            handle=None,
            match_source=None,
            matched_by_email=False,
            is_global=False,
            candidates=candidates.get(project.id, []),
        )
        if platform is None:
            rows.append(row)
            continue

        identity = scoped.get((project.id, platform)) or globals_.get(platform)
        if identity is not None:
            row.handle = identity.handle
            row.match_source = identity.match_source.value
            row.is_global = identity.project_id is None
        else:
            # No claimed row, but tickets already resolve to them: the only
            # remaining path is the email match, so name it as one rather than
            # showing "unmapped" beside work that is plainly attributed.
            assignee = session.exec(
                select(Ticket.assignee)
                .where(
                    Ticket.project_id == project.id,
                    Ticket.assigned_to == user.id,
                    Ticket.assignee.is_not(None),
                    Ticket.deleted_at.is_(None),
                )
                .limit(1)
            ).first()
            if assignee:
                row.handle = assignee
                row.match_source = MatchSource.EMAIL.value
                row.matched_by_email = True
        rows.append(row)
    return rows


# --------------------------------------------------------------------------- #
# The viewer's own slice of one project
#
# Three readers, all scoped to one project *and* one person. They exist for the
# project page's "You" tab, which answers "what is my part in this?" -- a
# different question from the dashboard's "what is the state of my projects?",
# and the reason the two pages do not share a query between them.
# --------------------------------------------------------------------------- #

# What counts as still on someone's plate. DRAFT and BACKLOG are excluded: they
# are the board's holding pen, not work in hand, and a list that opened with
# forty backlog items would bury the three things actually moving.
_ACTIVE_TICKET_STATUSES = (
    TicketStatus.TODO,
    TicketStatus.IN_PROGRESS,
    TicketStatus.IN_REVIEW,
)


@dataclass
class MyTicket:
    """One of the viewer's tickets, as the project page renders it."""

    id: str
    ref: Optional[str]
    summary: str
    status: str
    url: Optional[str]
    updated_at: Optional[datetime]


def my_tickets(session: Session, project_id: str, user_id: str) -> List[MyTicket]:
    """Every active ticket on this project assigned to this person.

    **Uncapped, deliberately.** A "your tickets" list that silently stops at ten
    is worse than a long one: the reader cannot tell a short list from a
    truncated one, and the whole value of the block is that it is the complete
    answer to "what is on me here". The status filter is what keeps it bounded --
    a person with forty *active* tickets has a problem the UI should show, not
    hide behind a limit.

    Ordered by `updated_at`, so what moved most recently is at the top.
    """
    rows = session.exec(
        select(Ticket)
        .where(
            Ticket.project_id == project_id,
            Ticket.assigned_to == user_id,
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            Ticket.status.in_(_ACTIVE_TICKET_STATUSES),  # type: ignore[attr-defined]
        )
        .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
    ).all()
    return [
        MyTicket(
            id=row.id,
            # The board's own reference where there is one. An InnoDay-only
            # ticket has no `external_ticket_id`, and inventing a reference for
            # it would produce a label that matches nothing on any board.
            ref=row.external_ticket_id,
            summary=row.summary,
            status=str(getattr(row.status, "value", row.status)),
            url=row.url,
            updated_at=_as_utc(row.updated_at),
        )
        for row in rows
    ]


@dataclass
class ProjectTicketRow:
    """One ticket on the project, for the Tickets tab."""

    id: str
    ref: Optional[str]
    summary: str
    status: str
    url: Optional[str]
    owner: Optional[str]
    updated_at: Optional[datetime]
    # The raw version string off the ticket. Carried so the Releases tab can show
    # *which* version an orphaned ticket points at -- without it, a ticket
    # belonging to no release is indistinguishable from one belonging to none.
    release: Optional[str] = None
    #: Open pull requests whose branch names this ticket, one per repository.
    #: Empty when nothing references it, which is the common case.
    pull_requests: List["TicketPullRequest"] = field(default_factory=list)


#: The order work is read in, closest-to-done first: IN_REVIEW, IN_PROGRESS, TODO,
#: BACKLOG -- then DONE at the bottom. It is the pipeline reversed, because the
#: question a board answers is "what is nearly out" before "what has not started",
#: and finished work is reference rather than a queue.
#:
#: The request for this order described the top of it as "in test". The status is
#: **IN_REVIEW**, and `_work_in_flight` already records why the UI must not rename
#: it: there is no test state on the board, so calling it one would report
#: something the data does not say. The position is what was asked for; the label
#: stays the board's own.
STATUS_ORDER = (
    TicketStatus.IN_REVIEW,
    TicketStatus.IN_PROGRESS,
    TicketStatus.TODO,
    TicketStatus.BACKLOG,
    TicketStatus.DONE,
)

#: Which statuses the Tickets tab shows when nothing is unticked. Everything in
#: `STATUS_ORDER`: a filter that starts with boxes cleared hides work without
#: saying so.
DEFAULT_STATUSES = STATUS_ORDER


def status_rank(status) -> int:
    """Where a status sits in `STATUS_ORDER`. Unknown ones sort last.

    Sorted in Python rather than SQL: the enum's stored form is its *name* while
    its value is lowercase-with-spaces, so a `CASE` expression would have to
    encode that mapping in SQL and drift from the enum the moment one is added.
    A project's ticket list is capped at 200, so the cost is nil.
    """
    try:
        return STATUS_ORDER.index(TicketStatus(str(getattr(status, "value", status))))
    except (ValueError, KeyError):
        return len(STATUS_ORDER)


def project_tickets(
    session: Session,
    project_id: str,
    *,
    limit: int = 200,
    statuses: Optional[Sequence[TicketStatus]] = None,
    release: Optional[str] = None,
) -> List[ProjectTicketRow]:
    """Every live ticket on the project, newest movement first.

    Capped, unlike ``my_tickets``. The distinction is deliberate: "yours" is a
    list you are accountable for and must be complete, while "the project's" can
    run to thousands and is a browse. The cap is stated in the UI so a truncated
    list never reads as the whole board.

    Owner is the board's own assignee string rather than a resolved user: it is
    what the board said, and resolving it here would quietly hide exactly the
    unmapped names the profile page exists to fix.
    """
    wanted = tuple(statuses) if statuses is not None else DEFAULT_STATUSES
    if not wanted:
        # Every box unticked is a legitimate ask with an empty answer, not a
        # reason to fall back to showing everything.
        return []

    statement = select(Ticket).where(
        Ticket.project_id == project_id,
        Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
        Ticket.status.in_(wanted),  # type: ignore[attr-defined]
    )
    if release:
        statement = statement.where(Ticket.release == release)

    rows = list(
        session.exec(
            statement.order_by(Ticket.updated_at.desc()).limit(limit)  # type: ignore[union-attr]
        ).all()
    )
    # Grouped by status in pipeline order, newest movement first inside each
    # group. `sort` is stable, so the `updated_at` ordering above survives.
    rows.sort(key=lambda row: status_rank(row.status))
    return [
        ProjectTicketRow(
            id=row.id,
            ref=row.external_ticket_id,
            summary=row.summary,
            status=str(getattr(row.status, "value", row.status)),
            url=row.url,
            owner=row.assignee,
            updated_at=_as_utc(row.updated_at),
        )
        for row in rows
    ]


def _tickets_capped_per_partition(
    session: Session,
    conditions: Sequence,
    *,
    partition_by: Sequence,
    cap: int,
) -> List[Ticket]:
    """Tickets matching ``conditions``, at most ``cap`` per partition, in one query.

    **This exists because a plain ``ORDER BY updated_at DESC ... LIMIT n`` cannot
    express the cap these callers actually want, and fails silently when it
    matters most.** A single `LIMIT` spends one budget across every project and
    every status at once, so whichever group moved most recently consumes it and
    the rest come back empty -- and "empty" is indistinguishable from "there is
    nothing there". A board sync that touches seventy DONE tickets is enough to
    make three IN_REVIEW tickets vanish from the page, which then states, in
    words, that nothing is in review.

    ``row_number()`` gives each partition its own budget, so no group can spend
    another's. It is chosen over issuing one query per status -- the other way to
    get the same guarantee -- because a per-status loop fixes starvation *between*
    statuses while leaving it intact *within* one: two projects competing for a
    single IN_PROGRESS budget is the same bug wearing a smaller hat. Partitioning
    on ``(project_id, status)`` closes both, and stays one round trip.

    Window functions are available on both backends this schema runs on:
    Postgres, and SQLite from 3.25 (2018) -- the same floor `alembic`'s own
    chain assumes.

    **Each caller's partition/order pair has an index shaped to match it** --
    `ix_ticket_project_status_updated` and `ix_ticket_project_done_unreleased`,
    both on `Ticket`. That is not an optimisation of the same plan, it is a
    different one: a window function cannot be answered from a top-N heap, so
    without an index Postgres sorts every matching row before it can number any
    of them. Change the `partition_by` or the ordering here and the sort comes
    back silently -- the query stays correct and gets slower.
    """
    ranked = (
        select(
            Ticket.id.label("ticket_id"),
            func.row_number()
            .over(
                partition_by=list(partition_by),
                order_by=Ticket.updated_at.desc(),  # type: ignore[union-attr]
            )
            .label("rank"),
        )
        .where(*conditions)
        .subquery()
    )
    return list(
        session.exec(
            select(Ticket)
            .join(ranked, Ticket.id == ranked.c.ticket_id)
            .where(ranked.c.rank <= cap)
            .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
        ).all()
    )


def project_tickets_for(
    session: Session,
    project_ids: Sequence[str],
    *,
    per_status: int = 25,
    statuses: Optional[Sequence[TicketStatus]] = None,
) -> Dict[str, List[ProjectTicketRow]]:
    """``project_tickets`` for several projects at once, in one query.

    The workflow page carries every project's work in a single payload, because
    switching projects in its rail must not cost a round trip. Calling
    `project_tickets` once per project to build that would be one query per
    project -- the exact shape `_render_dashboard` batched away in #501, and
    worse here, since the rail exists to make switching free.

    **The cap is per project *and per status*, applied in SQL by a window
    function.** See `_tickets_capped_per_partition` for why: a shared
    ``LIMIT`` let one busy status starve every other one, and the page renders
    that starvation as the sentence "Nothing is in test or in progress on this
    board" -- a false statement rather than a truncated list.

    **25 per status, because that is more than the page can display.** The
    workflow page renders at most `workflow.WALK_CAP` (20) tickets of any one
    status -- the walk's own cap -- and `workflow.PICK_CAP` (8) everywhere else,
    and it computes no total from these rows, so nothing it shows changes above
    25. The number matters because this payload is built for *every* project in
    the org at once: at 60 it was up to 300 rows per project, and an org with
    fifteen populated projects instantiated up to 4,500 ORM objects to render one
    page. 25 keeps the same guarantee (no status or project can starve another)
    at a fifth of the cost, with headroom over what is drawn.

    **Re-examined once `ix_ticket_project_status_updated` landed, and kept at
    25 -- but for only one of the two reasons it was lowered for.** The drop
    from 60 was a stopgap taken while the query had no index, and half of its
    justification has since evaporated: measured at 60,000 tickets over fifteen
    projects, 25 and 60 now cost the same in SQL (~20ms, 1,397 buffers, the same
    plan). They must, because the index-only scan walks every matching entry
    either way and `cap` only decides how many survive the window's run
    condition -- so *nothing* is bought back by keeping the number small there.
    What the index does not touch is the other half: 1,725 `Ticket` objects
    hydrated per page against 4,140. That cost is in Python, scales linearly in
    `cap`, and is paid on every load. It alone still decides the number, and it
    still says 25 -- which is above everything the page can draw, so raising it
    would buy rows nobody reads.

    **Not reconciled with `project_tickets`, which caps at 200 across all
    statuses, and does not need to be.** The two caps answer different questions:
    that one bounds a single project's browse, where a truncated list is visible
    and stated in the UI; this one bounds what a page holding every project's
    work carries at once. Neither is a correctness boundary.
    """
    ids = [pid for pid in project_ids if pid]
    if not ids:
        return {}

    wanted = tuple(statuses) if statuses is not None else DEFAULT_STATUSES
    if not wanted:
        # Same contract as `project_tickets`: every box unticked is a real ask
        # with an empty answer, not a reason to show everything.
        return {}

    rows = _tickets_capped_per_partition(
        session,
        (
            Ticket.project_id.in_(ids),  # type: ignore[attr-defined]
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            Ticket.status.in_(wanted),  # type: ignore[attr-defined]
        ),
        partition_by=(Ticket.project_id, Ticket.status),
        cap=per_status,
    )

    grouped: Dict[str, List[ProjectTicketRow]] = {pid: [] for pid in ids}
    for row in rows:
        bucket = grouped.get(row.project_id)
        if bucket is None:
            continue
        bucket.append(
            ProjectTicketRow(
                id=row.id,
                ref=row.external_ticket_id,
                summary=row.summary,
                status=str(getattr(row.status, "value", row.status)),
                url=row.url,
                owner=row.assignee,
                updated_at=_as_utc(row.updated_at),
                release=row.release,
            )
        )
    # Pipeline order inside each project, newest movement first within a status.
    # `sort` is stable, so the `updated_at` ordering above survives -- same
    # reasoning as `project_tickets`.
    for bucket in grouped.values():
        bucket.sort(key=lambda row: status_rank(row.status))
    return grouped


def _done_unreleased_conditions(project_ids: Sequence[str]) -> tuple:
    """What "finished and not in a release" means, in one place.

    Written once because two callers ask the same question and must get the same
    answer: `done_unreleased_for` for the rows and `done_unreleased_totals_for`
    for how many there are. A count derived from a different predicate than the
    rows is worse than no count -- it disagrees with what is on the screen.

    It is also the predicate `ix_ticket_project_done_unreleased` is partial on,
    so changing it here silently stops that index applying.
    """
    return (
        Ticket.project_id.in_(list(project_ids)),  # type: ignore[attr-defined]
        Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
        Ticket.status == TicketStatus.DONE,
        or_(
            Ticket.release.is_(None),  # type: ignore[union-attr]
            Ticket.release == "",
        ),
    )


def done_unreleased_totals_for(
    session: Session, project_ids: Sequence[str]
) -> Dict[str, int]:
    """How many finished-and-unreleased tickets each project has. **All of them.**

    The sibling below returns at most ``per_project`` rows, which is the right
    shape for a picker and the wrong one for a sentence: the workflow page was
    rendering ``len(rows)`` as "N finished tickets with no release", so a project
    with 300 of them said 60, and its "52 more not shown" was short by 240.

    A separate ``COUNT`` rather than an unbounded fetch, and cheap for the same
    reason the sibling is: `ix_ticket_project_done_unreleased` is partial on
    exactly this predicate, so the count is answered from the index without
    touching a heap page or hydrating a single ORM object.

    One query for every project, grouped -- the same rule as every other read on
    that page. Projects with none are present with ``0``, so an absent key means
    "not asked about", never "none".
    """
    ids = [pid for pid in project_ids if pid]
    if not ids:
        return {}

    totals: Dict[str, int] = {pid: 0 for pid in ids}
    rows = session.exec(
        select(Ticket.project_id, func.count())  # type: ignore[call-overload]
        .where(*_done_unreleased_conditions(ids))
        .group_by(Ticket.project_id)  # type: ignore[arg-type]
    ).all()
    for project_id, count in rows:
        if project_id in totals:
            totals[project_id] = int(count)
    return totals


def done_unreleased_for(
    session: Session,
    project_ids: Sequence[str],
    *,
    per_project: int = 60,
) -> Dict[str, List[ProjectTicketRow]]:
    """Finished tickets attached to no release, for several projects at once.

    The same question `ReleaseBoard.done_unreleased` answers for one project --
    work that completed before anyone recorded where it was going -- batched for
    the workflow page's "Organize the release" step, which offers it for
    whichever project the rail has selected.

    ``release`` is empty **or** NULL: the column is free text with no foreign
    key, and both spellings of "no release" occur in the wild.

    Capped per project by the same window function as `project_tickets_for`, and
    for the same reason: one project with a busy release cycle must not be able
    to spend a budget the others need. Only one status is involved here, so the
    partition is the project alone.

    **The cap means ``len()`` of what comes back is not a total**, and a caller
    that needs one must ask `done_unreleased_totals_for` rather than count these
    rows. The workflow page counted them and printed the answer as a total, so a
    project with 300 unreleased tickets reported 60. `project_tickets_for`
    defends its own cap with "it computes no total from these rows"; that is now
    true of this one too, because there is a total to ask for instead.

    Served by `ix_ticket_project_done_unreleased`, which is partial on this
    exact filter. It has its own index rather than sharing
    `project_tickets_for`'s because that one cannot screen on `release`: it would
    have to walk every DONE ticket to find the unreleased ones, and measured that
    way it lost to the sequential scan it was meant to replace. The cost of the
    narrower index is that these two conditions are now duplicated in the
    schema -- change either the status or the release test here and the index
    stops applying, again silently.
    """
    ids = [pid for pid in project_ids if pid]
    if not ids:
        return {}

    rows = _tickets_capped_per_partition(
        session,
        _done_unreleased_conditions(ids),
        partition_by=(Ticket.project_id,),
        cap=per_project,
    )

    grouped: Dict[str, List[ProjectTicketRow]] = {pid: [] for pid in ids}
    for row in rows:
        bucket = grouped.get(row.project_id)
        if bucket is None:
            continue
        bucket.append(
            ProjectTicketRow(
                id=row.id,
                ref=row.external_ticket_id,
                summary=row.summary,
                status=str(getattr(row.status, "value", row.status)),
                url=row.url,
                owner=row.assignee,
                updated_at=_as_utc(row.updated_at),
                release=row.release,
            )
        )
    return grouped


# --------------------------------------------------------------------------- #
# Today's scrum activity, and the work a person might bring back
# --------------------------------------------------------------------------- #


@dataclass
class ScrumSubmitter:
    """One person who submitted their daily update on a project today.

    Carried as ``name``/``email`` because that is what `render._bubbles` reads --
    the avatar group is the next change's job, and shaping the payload for it now
    is what stops the tick and the avatars being answered by two different
    queries that can disagree.
    """

    user_id: str
    name: str
    email: str


@dataclass
class ScrumActivity:
    """What has already been recorded on one project today.

    Three questions with three different scopes, which is the whole reason they
    are one dataclass rather than three booleans passed around separately:

    * ``my_update_submitted`` is **the viewer's**. Their daily update is theirs;
      somebody else's does not answer it.
    * ``scrum_ran`` is **the project's**. A stand-up is one meeting, so a second
      person seeing an empty box would go and run it again.
    * ``my_update_scrum_id`` is **the row to resume**, so re-entry costs no extra
      round trip.

    ``submitters`` holds everyone whose update is in for the day, in name order.
    Nothing renders it yet.
    """

    my_update_scrum_id: Optional[str] = None
    my_update_submitted: bool = False
    my_update_notes: Optional[str] = None
    scrum_ran: bool = False
    submitters: List[ScrumSubmitter] = field(default_factory=list)
    #: Ticket id -> the status the viewer asked for it, from their own update's
    #: visits. Empty unless there is something to resume.
    my_picks: Dict[int, str] = field(default_factory=dict)
    #: The picked tickets themselves, as the picker renders them, **and the
    #: status each was at when it was picked**.
    #:
    #: Needed because submitting now *applies* the move: a ticket brought back
    #: from DONE is IN_PROGRESS afterwards, so `my_done_recently_for` no longer
    #: returns it and `unowned_todo_for` never did. Without these rows a resumed
    #: picker shows nothing, and pressing through re-posts an empty selection --
    #: which `replace_picks` faithfully interprets as "remove everything I
    #: recorded". The day's record would be wiped by re-entering to look at it.
    #:
    #: ``status_at_visit`` is what says *which* picker a resumed row belongs
    #: under: "done" came from "bring anything back", anything else from "take
    #: anything on". It is the visit's own historical observation, so the row
    #: goes back where the person put it rather than where its current status
    #: would suggest.
    my_pick_rows: List["ProjectTicketRow"] = field(default_factory=list)
    my_pick_status_at_visit: Dict[int, str] = field(default_factory=dict)
    #: Ticket id -> what the viewer typed about it on their own update. Empty
    #: unless there is something to resume.
    #:
    #: Carried on the *same* row and the *same* query as the pick itself, because
    #: a comment and the box it belongs to are one answer: re-entering to correct
    #: a pick re-posts the whole selection, and a comment fetched separately could
    #: arrive from a read taken at a different moment and be written back over a
    #: newer one. Rendered into a `<textarea>` **text node**, never a `value=`
    #: attribute -- a newline is not representable in one.
    my_pick_comments: Dict[int, str] = field(default_factory=dict)


def scrum_activity_today(
    session: Session,
    project_ids: Sequence[str],
    user_id: str,
    *,
    day: date,
) -> Dict[str, ScrumActivity]:
    """Every project's scrum activity for one UTC day, for one viewer.

    **Org-wide and batched, never per project.** The workflow launcher carries
    every project's payload at once because its rail switches project in the
    browser with no round trip, so a per-project read here would grow the page's
    query count with the org -- and
    `test_workflow_page_query_count_grows_with_project_count` pins the route at
    under four extra SELECTs per project, which it already spends.

    ``day`` is passed in rather than read from the clock. The caller owns "which
    day is it" -- there is exactly one boundary (UTC midnight, see
    `domain.scrum`) and a function that read `utcnow()` itself could not be
    tested at one.

    **Three scalar columns off `users`, never the `User` entity.** ``users`` has
    two ``json`` columns and ``json`` has no equality operator in Postgres, so an
    entity in the select list is a query that dies the moment anything needs to
    compare rows -- the bug that 500'd ``/ui/bp``, recorded at
    `contributors_by_project`. Nothing here needs more than the id, name and
    email a `ScrumSubmitter` carries.

    **Two statements, and the second cannot be folded into the first.** The join
    below answers the ticks and the avatars together, which is the point: a tick
    and an avatar group derived from separate queries can disagree about who
    submitted. The resumed picks then need the ids that query just found, so they
    are a second round trip by construction -- and it is skipped entirely when
    there is nothing to resume. Both are constant in the project count, which is
    the property the page needs.
    """
    ids = [pid for pid in project_ids if pid]
    if not ids:
        return {}

    found: Dict[str, ScrumActivity] = {pid: ScrumActivity() for pid in ids}
    by_project_submitters: Dict[str, Dict[str, ScrumSubmitter]] = {
        pid: {} for pid in ids
    }

    rows = session.exec(
        select(
            Scrum.project_id,
            Scrum.id,
            Scrum.kind,
            Scrum.run_by_user_id,
            Scrum.ended_at,
            Scrum.notes_markdown,
            User.full_name,
            User.email,
        )
        .join(User, User.id == Scrum.run_by_user_id)
        .where(
            Scrum.project_id.in_(ids),  # type: ignore[attr-defined]
            Scrum.day == day,
        )
    ).all()

    for pid, scrum_id, kind, runner, ended_at, notes, full_name, email in rows:
        activity = found.get(pid)
        if activity is None:
            continue
        submitted = ended_at is not None
        if kind == ScrumKind.UPDATE.value:
            if runner == user_id:
                activity.my_update_scrum_id = scrum_id
                activity.my_update_submitted = submitted
                activity.my_update_notes = notes
            if submitted:
                by_project_submitters[pid].setdefault(
                    runner,
                    ScrumSubmitter(
                        user_id=runner,
                        name=full_name or email or "",
                        email=email or "",
                    ),
                )
        # An abandoned walk is not a scrum that ran -- `ended_at` NULL is how
        # `domain.scrum` spells "somebody walked out of this", and the tick's
        # whole job is to stop a second person running the meeting again.
        elif kind == ScrumKind.SCRUM.value and submitted:
            activity.scrum_ran = True

    for pid, people in by_project_submitters.items():
        found[pid].submitters = sorted(people.values(), key=lambda p: p.name.lower())

    resumable = {
        activity.my_update_scrum_id: pid
        for pid, activity in found.items()
        if activity.my_update_scrum_id
    }
    if resumable:
        # Joined to `ticket` rather than read separately: the picker has to render
        # the row, and a resumed pick's ticket may be in neither of the two lists
        # the page builds for those steps (submitting moves it out of both). This
        # is the same round trip either way -- the join adds columns, not a query,
        # so the page's constant-in-project-count shape is unchanged.
        #
        # Scalar columns only, never the `Ticket` entity: see the note above about
        # `json` columns having no equality operator in Postgres.
        for row in session.exec(
            select(
                ScrumTicketVisit.scrum_id,
                ScrumTicketVisit.ticket_id,
                ScrumTicketVisit.moved_to,
                ScrumTicketVisit.status_at_visit,
                ScrumTicketVisit.comment,
                Ticket.project_id,
                Ticket.external_ticket_id,
                Ticket.summary,
                Ticket.status,
                Ticket.url,
                Ticket.assignee,
                Ticket.updated_at,
            )
            .join(Ticket, Ticket.id == ScrumTicketVisit.ticket_id)
            .where(
                ScrumTicketVisit.scrum_id.in_(list(resumable)),  # type: ignore[attr-defined]
                # **A withdrawn pick is not resumed.** Its row survives only to
                # remember whether the board ever got its comment
                # (`ScrumTicketVisit.withdrawn_at`); rendering it would put a
                # ticked box and a typed note back in front of somebody who had
                # explicitly taken them off their update, and the next submit
                # would then re-apply what they withdrew.
                ScrumTicketVisit.withdrawn_at.is_(None),  # type: ignore[union-attr]
                # **`deleted_at IS NULL`, like every other ticket read here.**
                # Without it a ticket soft-deleted between recording and
                # submitting -- which is how a cleared board keeps its rows for
                # audit -- was re-rendered as a live, pre-ticked pick and then
                # moved and pushed to a board that no longer tracks it.
                Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
                # And only tickets still on a project this page is showing. A
                # ticket that moved projects is refused by `replace_picks`
                # (`ticket.project_id != scrum.project_id`), so rendering it
                # pre-ticked produced a 404 on the whole post with nothing on
                # screen saying which row caused it.
                Ticket.project_id.in_(ids),  # type: ignore[attr-defined]
            )
        ).all():
            (
                scrum_id,
                ticket_id,
                moved_to,
                status_at_visit,
                comment,
                ticket_project_id,
                ref,
                summary,
                status,
                url,
                assignee,
                updated_at,
            ) = row
            pid = resumable.get(scrum_id)
            if not pid or not moved_to:
                continue
            if ticket_project_id != pid:
                # The record belongs to one project and the ticket now belongs to
                # another. `replace_picks` refuses that pair, so offering it back
                # would render a box whose only effect is to 404 the next post.
                continue
            activity = found[pid]
            activity.my_picks[int(ticket_id)] = str(moved_to)
            activity.my_pick_status_at_visit[int(ticket_id)] = str(status_at_visit)
            if comment:
                activity.my_pick_comments[int(ticket_id)] = str(comment)
            activity.my_pick_rows.append(
                ProjectTicketRow(
                    # The int the column holds, matching `unowned_todo_for` and
                    # `my_done_recently_for` -- the annotation says `str` and every
                    # builder disagrees with it; `_pick_rows` calls `int()` either
                    # way. Not a place to start a second convention.
                    id=ticket_id,
                    ref=ref,
                    summary=summary,
                    status=str(getattr(status, "value", status)),
                    url=url,
                    owner=assignee,
                    updated_at=_as_utc(updated_at),
                )
            )

    return found


def my_done_recently_for(
    session: Session,
    project_ids: Sequence[str],
    user_id: str,
    *,
    since: datetime,
) -> Dict[str, List[ProjectTicketRow]]:
    """The viewer's own finished work, per project, completed at or after ``since``.

    **It cannot ride `project_tickets_for`.** That one caps DONE at 25 per project
    ordered by ``updated_at DESC``, and a board sync bumps ``updated_at`` on
    everything it touches -- so the ticket somebody finished yesterday can be
    ranked out by twenty-five tickets that merely got re-synced. Its
    `ProjectTicketRow`s also carry neither ``completed_at`` nor ``assigned_to``,
    which are the two columns this question is actually about.

    **``completed_at``, with no fallback to ``updated_at``.** A DONE ticket whose
    ``completed_at`` is NULL is simply not offered, and the page says so. The
    fallback is tempting and wrong: ``updated_at`` moves on every sync, so a
    ticket finished six months ago that a sync touched this morning would be
    offered as "you finished this yesterday". Not offering it is a visible gap
    somebody can act on; offering the wrong thing is not.

    ``since`` is naive UTC, like the column. It is passed in rather than derived
    here for the same reason `scrum_activity_today`'s ``day`` is: the window is
    the caller's decision (`workflow.REOPEN_WINDOW_DAYS`) and a function reading
    its own clock cannot be tested at a boundary.

    **Uncapped, deliberately** -- the same reasoning as `my_tickets`. This is one
    person's finished work inside a one-week window, and the filter is what bounds
    it; a silent cap on a list this small would hide a ticket while looking
    complete. The page caps what it *draws* at `workflow.PICK_CAP` and says how
    many it left out.

    Ordered by ``completed_at`` descending: most recently finished first, which is
    the one most likely to be coming back.

    One query for every project, grouped. Projects with none are present with an
    empty list, so an absent key means "not asked about", never "none".
    """
    ids = [pid for pid in project_ids if pid]
    if not ids:
        return {}

    grouped: Dict[str, List[ProjectTicketRow]] = {pid: [] for pid in ids}
    rows = session.exec(
        select(Ticket)
        .where(
            Ticket.project_id.in_(ids),  # type: ignore[attr-defined]
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            Ticket.status == TicketStatus.DONE,
            Ticket.assigned_to == user_id,
            Ticket.completed_at.is_not(None),  # type: ignore[union-attr]
            Ticket.completed_at >= since,  # type: ignore[operator]
        )
        .order_by(Ticket.completed_at.desc())  # type: ignore[union-attr]
    ).all()
    for row in rows:
        bucket = grouped.get(row.project_id)
        if bucket is None:
            continue
        bucket.append(
            ProjectTicketRow(
                id=row.id,
                ref=row.external_ticket_id,
                summary=row.summary,
                status=str(getattr(row.status, "value", row.status)),
                url=row.url,
                owner=row.assignee,
                updated_at=_as_utc(row.updated_at),
                release=row.release,
            )
        )
    return grouped


def unowned_todo_for(
    session: Session,
    project_ids: Sequence[str],
    *,
    cap: int = 25,
) -> Dict[str, List[ProjectTicketRow]]:
    """Queued work nobody owns, per project, **oldest first**.

    **Oldest first is the whole value of the list.** The question it answers is
    "what has been sitting here", and a newest-first ordering buries exactly that
    -- so this orders by ``created_at``, which is the only column that means "how
    long has this been waiting". ``updated_at`` would not do: a board sync bumps it
    on everything it touches, so the ticket that has waited longest is routinely
    the one with the freshest ``updated_at``.

    **It cannot ride `project_tickets_for`** for the same reason. That helper caps
    TODO at 25 per project *ordered by ``updated_at DESC``*, so the page it returns
    is the 25 most recently synced TODOs -- and re-sorting that page by age gives
    the oldest of the 25 newest, which is a different ticket and looks like an
    answer. Its `ProjectTicketRow`s also carry neither ``assigned_to`` nor
    ``created_at``.

    **"Unowned" means both columns, not one.** ``assigned_to`` is the FK every
    InnoDay reader uses; ``assignee`` is the board's display mirror and is what
    `ProjectTicketRow.owner` renders on screen. A ticket with only the latter set
    belongs to somebody on the board whose handle InnoDay has not resolved -- it
    shows an owner in the UI, and offering it as unowned is precisely the "nobody
    can silently take a colleague's ticket" case this list is filtered for. So both
    have to be empty.

    ``TODO`` only, not ``BACKLOG``. The backlog is a holding area rather than a
    queue: offering it here would turn "take something on" into "start anything
    ever written down", and the queue is what the team has already agreed is next.

    Capped in Python after one query, because the cap is a rendering decision (the
    page shows 25 and says how many it left out) while the ordering is the query's.
    One query for every project, grouped; projects with none are present with an
    empty list.
    """
    ids = [pid for pid in project_ids if pid]
    if not ids:
        return {}

    grouped: Dict[str, List[ProjectTicketRow]] = {pid: [] for pid in ids}
    rows = session.exec(
        select(Ticket)
        .where(
            Ticket.project_id.in_(ids),  # type: ignore[attr-defined]
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            Ticket.status == TicketStatus.TODO,
            Ticket.assigned_to.is_(None),  # type: ignore[union-attr]
            or_(
                Ticket.assignee.is_(None),  # type: ignore[union-attr]
                Ticket.assignee == "",
            ),
        )
        .order_by(Ticket.created_at.asc())  # type: ignore[union-attr]
    ).all()
    for row in rows:
        bucket = grouped.get(row.project_id)
        if bucket is None or len(bucket) >= cap:
            continue
        bucket.append(
            ProjectTicketRow(
                id=row.id,
                ref=row.external_ticket_id,
                summary=row.summary,
                status=str(getattr(row.status, "value", row.status)),
                url=row.url,
                owner=row.assignee,
                updated_at=_as_utc(row.updated_at),
                release=row.release,
            )
        )
    return grouped


@dataclass
class ShippedRelease:
    """One release that has gone out, for the history section."""

    version: str
    name: Optional[str]
    released_at: Optional[datetime]
    summary: Optional[str]
    # Per-repo PR counts read off `Release.changelog`, which the release engine
    # writes as `[{repo, prs: [...]}]`. Rendered as "3 repos · 14 PRs" rather
    # than the inventory itself: the summary is the thing worth reading, and the
    # changelog is long enough to bury it.
    repo_count: int = 0
    pr_count: int = 0


@dataclass
class PipelineOption:
    """One choice of bump, and the pair of versions it would produce."""

    part: str
    #: What slot 1 would become.
    version: str
    #: What slot 2 would become.
    planned: str
    #: Whether the pipeline already sits here.
    current: bool


@dataclass
class Slot:
    """One of the project's two forward releases, and what is in it."""

    release: Release
    # Every ticket carrying this version, whatever its status -- including DONE.
    # The list answers "what is in this release", and finished work is
    # emphatically in it.
    tickets: List[ProjectTicketRow] = field(default_factory=list)


@dataclass
class ReleaseBoard:
    """The Releases tab's whole payload: both slots, the pool, and the history.

    `current` and `planned` are the pipeline's two forward slots, and they are
    separate fields rather than a list because they are different things to a
    reader: one is being cut and is closing out, the other is being filled. A
    single "next release" had to be both, which is what this replaced.
    """

    #: Slot 1 -- IN_PROGRESS, the version blastoff cuts next.
    current: Optional[Slot] = None
    #: Slot 2 -- PLANNED, the version work is being planned into.
    planned: Optional[Slot] = None
    # Live tickets carrying no version at all: the pool a planner would drag
    # from. Capped, because an old project's backlog is unbounded.
    backlog: List[ProjectTicketRow] = field(default_factory=list)
    backlog_limit: int = 100
    history: List[ShippedRelease] = field(default_factory=list)
    #: What slot 1 could be moved to. Empty when there is nothing to move --
    #: no pipeline, or one on a version that cannot be bumped.
    options: List[PipelineOption] = field(default_factory=list)
    #: Live tickets whose `release` names a version this project does not have --
    #: a typo, or a version that was renamed or archived out from under them.
    #: They belong in no slot and no release will ship them, so without this they
    #: are simply absent from the board. Each carries the string it points at.
    orphaned: List[ProjectTicketRow] = field(default_factory=list)
    #: Tickets marked DONE that were never attached to any release.
    #:
    #: **Work that finished before anyone recorded where it was going.** The
    #: planning pool is deliberately limited to `_PLANNABLE`, which excludes DONE
    #: -- right for planning, because you do not plan finished work. But it also
    #: made this case invisible: a ticket completed before the release process
    #: caught up appears in no slot, in no pool, and in no release, so the one
    #: page that exists to answer "what is in this release" could not show that
    #: it was missing something. It has to be attachable *after* the fact, which
    #: is why these carry the same plan controls as the pool.
    #:
    #: Capped like the pool, but the **total** is carried separately: unlike the
    #: backlog, hitting the cap here is the normal case rather than the edge (219
    #: on one project at the time of writing), so a list of 100 with no total
    #: would understate the size of the problem by more than half.
    done_unreleased: List[ProjectTicketRow] = field(default_factory=list)
    done_unreleased_total: int = 0


#: Statuses that can still be planned into a release. Applied to the *unassigned*
#: pool only -- work already carrying a version is in that release whatever its
#: status, including DONE, so `assigned` filters nothing but cancellation.
#:
#: Deliberately **not** `_ACTIVE_TICKET_STATUSES`, which the "You" tab uses: that
#: one excludes BACKLOG because a personal to-do list buried under forty backlog
#: items is useless. Here the backlog is precisely the thing being planned from,
#: and a planning pool that cannot see it cannot plan. DRAFT stays out either
#: way -- an unfinished ticket is not yet a candidate for anything.
_PLANNABLE = (
    TicketStatus.BACKLOG,
    TicketStatus.TODO,
    TicketStatus.IN_PROGRESS,
    TicketStatus.IN_REVIEW,
)


def _changelog_totals(changelog) -> Tuple[int, int]:
    """Repo and PR counts from a release's changelog, defensively.

    **The shape that actually arrives is ``{"repos": [...]}``, not a bare list**,
    and this function used to accept only the list -- so every release recorded
    by the release engine would have rendered "0 repos · 0 PRs" on the one page
    that shows what a release contained.

    `Release.changelog` is a `dict` column and `ReleaseCreate.changelog` is
    `Optional[dict]`, so a bare list cannot even reach the row through the API;
    `InnoDayVersionStore._wrap_changelog` exists precisely to wrap blastoff's
    list into that dict. The list branch below is kept for a row written straight
    through the ORM (the fixtures do this) and for anything hand-authored, but
    the wrapped form is the canonical one.

    Nothing caught it because each side was tested against its own idea of the
    shape and the two were never run end to end -- `test_release_changelog_round_trip`
    is that missing test, and it drives the real writer into the real reader.

    Anything else -- a scalar, a dict without `repos`, JSON `null` (which is what
    most existing rows hold) -- counts as zero rather than taking the page down.
    """
    if isinstance(changelog, dict):
        changelog = changelog.get("repos")
    if not isinstance(changelog, list):
        return (0, 0)
    repos = 0
    prs = 0
    for entry in changelog:
        if not isinstance(entry, dict):
            continue
        repos += 1
        pull_requests = entry.get("prs")
        if isinstance(pull_requests, list):
            prs += len(pull_requests)
    return (repos, prs)


def _release_ticket_rows(rows: Sequence[Ticket]) -> List[ProjectTicketRow]:
    """Ticket rows in the shape the Tickets tab already renders."""
    return [
        ProjectTicketRow(
            id=row.id,
            ref=row.external_ticket_id,
            summary=row.summary,
            status=str(getattr(row.status, "value", row.status)),
            url=row.url,
            owner=row.assignee,
            updated_at=_as_utc(row.updated_at),
            release=row.release,
        )
        for row in rows
    ]


def release_board(
    session: Session,
    project_id: str,
    *,
    backlog_limit: int = 100,
    history_limit: int = 10,
) -> ReleaseBoard:
    """What this project is heading toward, and the last few things it shipped.

    Reads the project's releases once and derives both halves from that list --
    ``next_release`` applies the high-water-mark rule documented in
    ``release_planning``, so the "upcoming" release here is the same one the
    dashboard card calls the next launch. Two renderings that could disagree
    about which release is next would be worse than either one alone.

    The ticket join is the loose one ``Release`` documents: ``ticket.release``
    is free text matched against ``release.version``. There is no foreign key,
    so a typo'd version silently belongs to no release -- which is the honest
    behaviour, and the reason the backlog side is defined as "no version at all"
    rather than "not this version".
    """
    releases = session.exec(
        select(Release).where(
            Release.project_id == project_id,
            Release.deleted_at.is_(None),
        )
    ).all()

    current_release = next_release(list(releases))

    # Slot 2 is the lowest PLANNED row above slot 1 -- the same rule
    # `release_pipeline.retarget` applies, so what this page shows is what moving
    # the version line would move.
    planned_release = slot_two(list(releases), current_release)

    def _slot(release) -> Optional[Slot]:
        if release is None:
            return None
        rows = list(
            session.exec(
                select(Ticket)
                .where(
                    Ticket.project_id == project_id,
                    Ticket.release == release.version,
                    Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
                    Ticket.status != TicketStatus.CANCELLED,
                )
                .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
            ).all()
        )
        # The Tickets tab's order, applied here too: status rank, then newest
        # movement inside each. `sort` is stable, so the SQL ordering survives.
        # Two surfaces listing the same tickets in different orders would each
        # claim a different thing is at the top.
        rows.sort(key=lambda row: status_rank(row.status))
        return Slot(release=release, tickets=_release_ticket_rows(rows))

    # Live work whose version matches no release row on this project. The join is
    # free text with no foreign key, so this is a state the schema permits: a
    # typo, or a version renamed or archived after the ticket was labelled. Such
    # a ticket looks planned and is not -- no slot holds it, and no release will
    # ever count it, because there is no release to count it. Surfacing it beside
    # the unassigned pool is the only way it is ever seen again.
    known_versions = {release.version for release in releases}
    orphaned = _release_ticket_rows(
        row
        for row in session.exec(
            select(Ticket)
            .where(
                Ticket.project_id == project_id,
                Ticket.release.is_not(None),  # type: ignore[union-attr]
                Ticket.release != "",
                Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
                Ticket.status.in_(_PLANNABLE),  # type: ignore[attr-defined]
            )
            .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
            .limit(backlog_limit)
        ).all()
        if row.release not in known_versions
    )

    backlog = _release_ticket_rows(
        session.exec(
            select(Ticket)
            .where(
                Ticket.project_id == project_id,
                # `or_` rather than `is_(None)`: board sync writes an empty
                # string when a ticket carries no version label, so testing only
                # for NULL would file those under "planned into nothing named",
                # which is not a distinction anyone means.
                or_(Ticket.release.is_(None), Ticket.release == ""),  # type: ignore[union-attr]
                Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
                Ticket.status.in_(_PLANNABLE),  # type: ignore[attr-defined]
            )
            .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
            .limit(backlog_limit)
        ).all()
    )
    backlog.sort(key=lambda row: status_rank(row.status))

    # Finished work that never carried a version. Newest movement first and no
    # status sort: they are all DONE, so the only useful order is "most recently
    # finished", which is also the most likely to belong in the release being cut.
    _done_unreleased = (
        Ticket.project_id == project_id,
        or_(Ticket.release.is_(None), Ticket.release == ""),  # type: ignore[union-attr]
        Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
        Ticket.status == TicketStatus.DONE,
    )
    done_unreleased = _release_ticket_rows(
        session.exec(
            select(Ticket)
            .where(*_done_unreleased)
            .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
            .limit(backlog_limit)
        ).all()
    )
    # The total, not `len()` of the capped list. CANCELLED is excluded by the
    # status filter above rather than lumped in: cancelled work never shipped, so
    # attaching it to a release would misreport what that release contained.
    done_unreleased_total = int(
        session.exec(
            select(func.count()).select_from(Ticket).where(*_done_unreleased)
        ).one()
        or 0
    )

    # Newest first. `released_at` is the real ordering, but it is nullable even
    # on a RELEASED row (board sync can mark a version shipped without a date),
    # so version order breaks the tie rather than letting an undated release
    # sink to the bottom of the list arbitrarily.
    shipped = [r for r in releases if r.status == ReleaseStatus.RELEASED]
    shipped.sort(
        key=lambda r: (
            _as_utc(r.released_at) or datetime.min.replace(tzinfo=timezone.utc),
            semver_key(r.version),
        ),
        reverse=True,
    )
    history = []
    for release in shipped[:history_limit]:
        repo_count, pr_count = _changelog_totals(release.changelog)
        history.append(
            ShippedRelease(
                version=release.version,
                name=release.name,
                released_at=_as_utc(release.released_at),
                summary=release.summary or release.notes,
                repo_count=repo_count,
                pr_count=pr_count,
            )
        )

    options = []
    if current_release is not None:
        # Named `one`/`two` rather than `slot_one`/`slot_two`: a loop target called
        # `slot_two` would make the imported function local to this whole function
        # and turn the call above into an UnboundLocalError.
        for part, one, two in pipeline_options(list(releases)):
            options.append(
                PipelineOption(
                    part=part,
                    version=one,
                    planned=two,
                    current=one == current_release.version,
                )
            )

    return ReleaseBoard(
        current=_slot(current_release),
        planned=_slot(planned_release),
        done_unreleased=done_unreleased,
        done_unreleased_total=done_unreleased_total,
        backlog=backlog,
        backlog_limit=backlog_limit,
        history=history,
        options=options,
        orphaned=orphaned,
    )


@dataclass
class TimelineRow:
    """One timeline entry, for the Timeline tab."""

    id: str
    event_type: str
    title: str
    summary: Optional[str]
    occurred_at: Optional[datetime]
    is_yours: bool


def project_timeline(
    session: Session, project_id: str, viewer_id: str, *, limit: int = 100
) -> List[TimelineRow]:
    """The project's whole timeline, with the viewer's own entries marked.

    Everyone's, not just yours -- this is the project's record. ``is_yours`` lets
    the page distinguish without a second query, and without the page having to
    claim someone else's entry is the viewer's.
    """
    rows = session.exec(
        select(ProjectTimeline)
        .where(ProjectTimeline.project_id == project_id)
        .order_by(ProjectTimeline.occurred_at.desc())  # type: ignore[union-attr]
        .limit(limit)
    ).all()
    return [
        TimelineRow(
            id=row.id,
            event_type=str(getattr(row.event_type, "value", row.event_type)),
            title=row.title,
            summary=row.summary,
            occurred_at=_as_utc(row.occurred_at),
            is_yours=row.created_by == viewer_id,
        )
        for row in rows
    ]


# --------------------------------------------------------------------------- #
# Creating a project
# --------------------------------------------------------------------------- #

# How many extra topics a project may carry beyond its alias. Three is a limit
# on the *form*, not the data model: `settings['github_topics']` is a free
# comma-separated string. It exists because every topic is another GitHub search
# on every discovery run, and because a project that needs more than three
# probably wants to be two projects.
MAX_EXTRA_TOPICS = 3


@dataclass
class TopicOption:
    """One selectable GitHub topic, with the repos that carry it."""

    name: str
    repos: List[str]
    #: True for the project's own alias, which is always searched and therefore
    #: cannot be deselected. Rendering it as a choice would let someone turn off
    #: a topic that still applies, and the preview beside it would then be a lie.
    locked: bool = False


@dataclass
class TopicPreview:
    """What a set of topic choices would actually pull in."""

    options: List[TopicOption]
    included: List[str]
    #: Repos matching a chosen topic but archived on GitHub. Shown struck
    #: through rather than dropped: the count someone sees when creating must
    #: match the count they get, and sync skips archived repos.
    archived: List[str]


def topic_preview(
    repos: Sequence[Dict[str, Any]], alias: str, chosen: Sequence[str]
) -> TopicPreview:
    """Build the topic picker and its repo preview from one listing of org repos.

    Pure: it takes GitHub's repo dicts and returns what to draw. That is what
    makes it testable without a network call, and it is the reason the caller
    fetches once rather than querying per topic -- GitHub's org listing already
    returns each repo's `topics`, so one request answers the whole form.

    ``alias`` is always included and always locked. `WorkspaceOnboardService.
    github_topics()` adds `settings['github_topics']` **to** the lowercased alias
    rather than replacing it, so the alias is not a default anyone can turn off.
    """
    alias_topic = (alias or "").strip().lower()
    picked = {t.strip().lower() for t in chosen if t and t.strip()}
    picked.discard(alias_topic)

    by_topic: Dict[str, List[str]] = {}
    archived_names = set()
    for repo in repos:
        name = repo.get("name") or ""
        if not name:
            continue
        if repo.get("archived"):
            archived_names.add(name)
        for topic in repo.get("topics") or []:
            by_topic.setdefault(str(topic).lower(), []).append(name)

    options = []
    if alias_topic:
        options.append(
            TopicOption(
                name=alias_topic,
                repos=sorted(by_topic.get(alias_topic, [])),
                locked=True,
            )
        )
    for topic in sorted(by_topic):
        if topic != alias_topic:
            options.append(TopicOption(name=topic, repos=sorted(by_topic[topic])))

    searched = ({alias_topic} if alias_topic else set()) | picked
    matched = {name for topic in searched for name in by_topic.get(topic, [])}
    return TopicPreview(
        options=options,
        included=sorted(n for n in matched if n not in archived_names),
        archived=sorted(n for n in matched if n in archived_names),
    )


def alias_is_available(session: Session, organization_id: str, alias: str) -> bool:
    """Whether this alias is free within the org.

    Per-organization, matching `uq_project_org_alias` -- two orgs may each have a
    project aliased "PF". Case-insensitive, because the alias is stored uppercase
    as a ticket prefix and lowercased in URLs, so "pf" and "PF" are the same
    project by every route that resolves one.
    """
    existing = session.exec(
        select(Project.id).where(
            Project.organization_id == organization_id,
            func.lower(Project.alias) == alias.strip().lower(),
        )
    ).first()
    return existing is None


@dataclass
class MyPullRequest:
    """One of the viewer's open pull requests, as the project page renders it."""

    repo: str
    number: int
    title: str
    url: Optional[str]
    is_draft: bool
    updated_at: Optional[datetime]


def my_pull_requests(
    session: Session, project_id: str, user: User
) -> Optional[List[MyPullRequest]]:
    """The viewer's open PRs across this project's repositories.

    ``None`` -- not ``[]`` -- when the viewer has no GitHub username on file.
    The two say different things: an empty list claims "you have nothing open",
    which would be wrong for anyone who simply has not told us their handle, and
    a page cannot tell the difference without being told. The caller renders the
    two states separately for exactly that reason.

    "Theirs" means authored **or** assigned. GitHub allows several assignees and
    the author is often not among them, so keying on either alone drops real
    work off someone's list.
    """
    handle = (user.github_username or "").strip().lower()
    if not handle:
        return None

    rows = session.exec(
        select(RepositoryPullRequest, Repository)
        .join(Repository, Repository.id == RepositoryPullRequest.repository_id)
        .join(
            ProjectRepository,
            ProjectRepository.repository_id == Repository.id,
        )
        .where(
            ProjectRepository.project_id == project_id,
            ProjectRepository.is_active == True,  # noqa: E712
        )
        .order_by(RepositoryPullRequest.github_updated_at.desc())  # type: ignore[union-attr]
    ).all()

    mine = []
    for pr, repo in rows:
        logins = {
            str(login).lower()
            for login in ([pr.author_login] + list(pr.assignee_logins or []))
            if login
        }
        if handle not in logins:
            continue
        mine.append(
            MyPullRequest(
                repo=repo.name,
                number=pr.number,
                title=pr.title,
                url=pr.url,
                is_draft=pr.is_draft,
                updated_at=_as_utc(pr.github_updated_at),
            )
        )
    return mine


# --------------------------------------------------------------------------- #
# Team
#
# Two different notions of "team", deliberately not conflated:
#
# * **Contributors** -- who is actually working on one project. Derived from
#   tickets and identities, never stored, because `OrganizationMembership` has no
#   project column. A literal member list on a project card would render
#   identically on every project in the org, which is not a team for *that*
#   project.
# * **Members** -- the org roster, which is what the model actually holds and
#   what an admin manages.
#
# The card shows the first; the team page manages the second, and says which.
# --------------------------------------------------------------------------- #


@dataclass
class Contributor:
    """One person visibly working on a project."""

    user_id: str
    name: str
    email: str


def contributors_by_project(
    session: Session, project_ids: Sequence[str]
) -> Dict[str, List[Contributor]]:
    """Who is working on each project, resolved for all of them at once.

    Two queries regardless of project count, for the same reason
    ``project_cards`` and ``unmapped_counts_for`` beside it are batched: this
    renders once per card, and a per-card query is a dashboard that slows down
    exactly as an org grows (#501 was the last one of those).

    "Working on it" means an assigned ticket **or** a project-scoped identity.
    Assignment alone would miss someone who has mapped their board handle but
    has nothing open right now, and a card that dropped them the moment their
    last ticket closed would read as them having left.
    """
    found: Dict[str, Dict[str, Contributor]] = {pid: {} for pid in project_ids}
    if not project_ids:
        return {}

    def _add(pid: str, user_id: str, full_name: Optional[str], email: Optional[str]):
        if not user_id or pid not in found:
            return
        found[pid].setdefault(
            user_id,
            Contributor(
                user_id=user_id,
                name=full_name or email or "",
                email=email or "",
            ),
        )

    # Three scalar columns, **never the whole `User` entity.** Selecting the entity
    # under DISTINCT makes Postgres compare every column of it, and `users` has two
    # `json` columns (`notification_preferences`, `ui_preferences`). `json` has no
    # equality operator in Postgres -- only `jsonb` does -- so the query dies with:
    #
    #     could not identify an equality operator for type json
    #
    # SQLite has no such restriction, so this passed every test and 500'd the
    # dashboard of the first org whose tickets had assignees. Nothing here ever
    # needed more than the id, name and email that `Contributor` carries.
    for pid, user_id, full_name, email in session.exec(
        select(Ticket.project_id, User.id, User.full_name, User.email)
        .join(User, User.id == Ticket.assigned_to)
        .where(
            Ticket.project_id.in_(project_ids),  # type: ignore[attr-defined]
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
        )
        .distinct()
    ).all():
        _add(pid, user_id, full_name, email)

    for pid, user_id, full_name, email in session.exec(
        select(UserIdentity.project_id, User.id, User.full_name, User.email)
        .join(User, User.id == UserIdentity.user_id)
        .where(UserIdentity.project_id.in_(project_ids))  # type: ignore[attr-defined]
        .distinct()
    ).all():
        _add(pid, user_id, full_name, email)

    return {
        pid: sorted(people.values(), key=lambda c: c.name.lower())
        for pid, people in found.items()
    }


@dataclass
class TeamMember:
    """One org member, as the team page renders them."""

    user_id: str
    name: str
    email: str
    role: str
    github_username: Optional[str]
    board_handles: List[str]
    is_you: bool


def team_members(
    session: Session, organization_id: str, viewer: User
) -> List[TeamMember]:
    """The org's roster, with each person's handles.

    Only **active** memberships. Removal here deactivates rather than deletes, so
    the row survives for audit and their tickets keep resolving -- an inactive
    membership is a former member, not a missing one.
    """
    rows = session.exec(
        select(OrganizationMembership, User)
        .join(User, User.id == OrganizationMembership.user_id)
        .where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.is_active == True,  # noqa: E712
        )
    ).all()

    handles: Dict[str, List[str]] = {}
    for identity in session.exec(
        select(UserIdentity).where(
            UserIdentity.user_id.in_([u.id for _m, u in rows] or [""])  # type: ignore[attr-defined]
        )
    ).all():
        if identity.handle:
            handles.setdefault(identity.user_id, []).append(identity.handle)

    members = [
        TeamMember(
            user_id=user.id,
            name=user.full_name or user.email or "",
            email=user.email or "",
            role=str(getattr(m.role, "value", m.role)),
            github_username=user.github_username,
            board_handles=sorted(set(handles.get(user.id, []))),
            is_you=user.id == viewer.id,
        )
        for m, user in rows
    ]
    return sorted(members, key=lambda m: m.name.lower())


def admin_count(session: Session, organization_id: str) -> int:
    """How many active admins the org has.

    Read before any demotion or removal: an org with no admin is an org nobody
    can add one to, and that is not recoverable from the UI. Enforced
    server-side rather than by hiding a button -- the button is a courtesy, the
    check is the guarantee.
    """
    return len(
        session.exec(
            select(OrganizationMembership.id).where(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.is_active == True,  # noqa: E712
                OrganizationMembership.role == OrganizationRole.ADMIN,
            )
        ).all()
    )
