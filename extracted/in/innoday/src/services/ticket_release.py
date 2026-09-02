"""Which release a ticket may be assigned to, and what a submitted value means.

``Ticket.release`` is a **validated free-text string**, not a foreign key, and
that is deliberate: board sync writes whatever an external board names -- a Jira
``fixVersions`` entry, a semver-shaped Linear label -- and a rejecting constraint
would either fail the sync or silently drop the value. So the constraint lives
here, on the interactive write paths, and sync (which writes through the session
and never reaches a router) is structurally untouched by it.

**The match is byte-exact, so the validation must be too.** Every reader of
this column -- ``_ticket_counts``, the Releases tab's ``release_board``, the
``?release=`` filter -- compares ``Ticket.release == release.version`` with
nothing normalising either side. Admit ``V1.10.0`` for a ``v1.10.0`` row and the
ticket belongs to no release anywhere: it shows in no slot, is counted in no
release, and appears instead in the orphaned list. That is precisely the state
this validation exists to prevent, and it would have been created by the code
meant to prevent it. Only surrounding whitespace is stripped, and what gets
stored is the release row's own version string rather than the caller's, so the
two cannot differ by a character.

Session-aware, hence not in :mod:`src.services.release_planning`, whose whole
contract is pure functions over a list of releases; and not in
:mod:`src.services.release_pipeline`, which is the *writing* half of release
management. This module only reads.
"""

from typing import List, Optional

from sqlmodel import Session, select

from src.domain.project import Project
from src.domain.release import Release
from src.services.release_planning import next_release, outstanding_releases

#: The value ``release`` takes to mean "whatever this project is cutting now"
#: rather than a literal version string.
#:
#: A reserved word in a value is usually a wart -- a release genuinely versioned
#: "current" would become unreachable. Here it cannot happen: the pipeline only
#: ever opens semver versions, and ``ensure_pipeline`` closes any open release
#: whose version is not semver, so "current" can never be a live version on any
#: project.
#:
#: Shared with the ``?release=`` query filter (``src/routers/tickets.py``,
#: ``src/routers/summaries.py``) and with the CLI's ``--window release``
#: (``src/cli/commands/summary.py``) on purpose -- one sentinel resolved by one
#: helper (:func:`current_release_version`), so a filter and a write can never
#: disagree about which version is current. Import it; a re-declared copy of the
#: literal is two values that must stay equal with nothing pinning them.
CURRENT_RELEASE = "current"

#: What a **read**-path 404 says when :data:`CURRENT_RELEASE` has no answer.
#: Shared by the ``?release=`` ticket filter and the project summary routes so
#: two routes cannot tell a caller different things about the same state.
#:
#: The write path's message is deliberately *not* this one: it is a 422 about a
#: body field that cannot be satisfied, names the project by alias and quotes the
#: sentinel, and lives in :func:`resolve_ticket_release`.
NO_CURRENT_RELEASE_DETAIL = (
    "Project {project} has no current release. One opens when something ships "
    "or on the next repository sync."
)


class ReleaseNotOutstanding(ValueError):
    """A submitted version is not one this project is planning into.

    Carries the message the API turns into a 422 ``detail`` verbatim -- a plain
    string, because the CLI f-strings ``detail`` and the MCP server hands the raw
    body to an agent to read. A dict would print as one.
    """


def _project_releases(
    session: Session, organization_id: str, project_id: str
) -> List[Release]:
    """Every release row for one project.

    **All of them, filtered in Python by the caller** -- never
    ``WHERE status IN (...)``. Not an oversight and not worth "optimising": enum
    storage in this schema is genuinely inconsistent (values are lowercase, the
    column holds NAMEs, and routers disagree on which they accept), so a status
    comparison in SQL is a bet on which side it lands. The same shape is already
    used by ``_advance_release_pipeline``. A project has a handful of releases,
    not thousands.
    """
    return list(
        session.exec(
            select(Release).where(
                Release.organization_id == organization_id,
                Release.project_id == project_id,
                Release.deleted_at.is_(None),
            )
        ).all()
    )


def current_release_version(
    session: Session, *, organization_id: str, project_id: str
) -> Optional[str]:
    """The version :data:`CURRENT_RELEASE` names for this project, or ``None``.

    **The one resolver for the sentinel.** Two callers ask this question and they
    differ only in what they do with "there isn't one": the ``?release=`` read
    filter answers 404 (``src/routers/tickets.py``, ``src/routers/summaries.py``)
    and a submitted ``release`` answers 422 (:func:`resolve_ticket_release`).
    Each of those used to run its own ``select`` + ``next_release``, which is a
    rule stated twice -- and a rule stated twice is a rule that can change once.

    **Raises nothing, and returns ``None`` rather than an exception, on purpose.**
    Any exception type chosen here would belong to one of the two callers and be
    wrong for the other, which is precisely what made each keep a copy. The
    answer lives here; the error stays with whoever is answering.
    """
    current = next_release(_project_releases(session, organization_id, project_id))
    return None if current is None else current.version


def outstanding_choices(
    session: Session, *, organization_id: str, project_id: str
) -> List[Release]:
    """The project's outstanding releases, best-first -- the vocabulary a picker
    offers and the list an error message names."""
    return outstanding_releases(_project_releases(session, organization_id, project_id))


def _project_label(session: Session, project_id: str) -> str:
    """What to call the project in an error message -- its alias if it has one.

    A bare uuid tells the reader nothing about which project rejected their
    version, and on the CLI they may well be looking at two.
    """
    project = session.get(Project, project_id)
    return project.alias if project and project.alias else project_id


def _options_sentence(options: List[Release]) -> str:
    return ", ".join(f"{r.version} ({r.status.value})" for r in options)


def resolve_ticket_release(
    session: Session,
    *,
    organization_id: str,
    project_id: Optional[str],
    value: Optional[str],
) -> Optional[str]:
    """The version string to store for a submitted ``release`` value.

    Only ever called when the caller actually supplied one. Validation keys off
    the **payload**, never off the row already stored: a ticket carrying an
    unmatched value board sync wrote (``2026.08-hotfix``) must stay editable, and
    checking the row would make every such ticket impossible to touch at all.

    ``""`` means "take this ticket out of its release" and is stored as-is,
    unvalidated -- removing a ticket from a release cannot reasonably require
    naming a valid one.

    Raises :class:`ReleaseNotOutstanding` for anything else the project is not
    planning into. The message distinguishes *unknown* from *closed*: telling
    someone their released version is "unknown" sends them off to create a
    duplicate release row.
    """
    if value is None:
        return None

    wanted = value.strip()
    if not wanted:
        return ""

    if not project_id:
        # Unreachable today -- `Ticket.project_id` is NOT NULL, `POST /tickets`
        # 400s without one and the board-scoped create takes it from the board.
        # Reject rather than skip anyway: accepting unvalidated would manufacture
        # the orphan case, and skipping silently would make the rule conditional
        # on a state that cannot occur, which is how it stops being a rule.
        raise ReleaseNotOutstanding(
            "A release version can only be validated inside a project; "
            "this ticket has none."
        )

    label = _project_label(session, project_id)

    if wanted == CURRENT_RELEASE:
        # Through the shared resolver, so the write path and the `?release=`
        # filter cannot answer "which version is current" differently. Only the
        # error below is this path's own.
        version = current_release_version(
            session, organization_id=organization_id, project_id=project_id
        )
        if version is None:
            # 422 rather than 404 at the router: this is a body field that cannot
            # be satisfied, not a missing resource.
            raise ReleaseNotOutstanding(
                f"Project {label} has no current release for "
                f"'{CURRENT_RELEASE}' to mean. One opens when something ships or "
                "on the next repository sync."
            )
        return version

    # One read, filtered three ways below -- so the "is it outstanding?" and "is
    # it merely closed?" questions cannot be answered by two different
    # comparisons (one in Python, one in SQL) that disagree about case. The
    # sentinel returned above, so this is still one read per call.
    releases = _project_releases(session, organization_id, project_id)
    options = outstanding_releases(releases)

    for release in options:
        if wanted == release.version:
            # The row's own string, not the caller's: what is stored is then
            # exactly what every reader of this column matches on.
            return release.version

    if not options:
        raise ReleaseNotOutstanding(
            f"Project {label} has no outstanding releases, so '{wanted}' cannot "
            f"be one. Create it first, or use '{CURRENT_RELEASE}' once the "
            "project has a version in progress."
        )

    for release in releases:
        if wanted == release.version:
            raise ReleaseNotOutstanding(
                f"Release '{wanted}' is {release.status.value} on project "
                f"{label}, not outstanding. Outstanding releases: "
                f"{_options_sentence(options)}."
            )

    raise ReleaseNotOutstanding(
        f"'{wanted}' is not an outstanding release on project {label}. "
        f"Outstanding releases: {_options_sentence(options)}. Pass one of those, "
        f"or '{CURRENT_RELEASE}' for the version being cut."
    )
