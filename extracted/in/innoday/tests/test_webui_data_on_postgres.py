"""Every dashboard query, run against Postgres.

**Why this file exists.** `test_webui_pages.py` -- 100-odd tests covering every
page -- runs entirely on SQLite, and SQLite cannot see a whole class of Postgres
error. `/ui/bp` returned a 500 for exactly that reason: `contributors_by_project`
selected a full `User` row under `DISTINCT`, and Postgres has no equality operator
for `json` (`users` has two `json` columns). Every test passed; the page was down.

Rendering cannot fail this way -- it is pure Python string building. The risk lives
entirely in the queries, so this covers the queries: each one is called against a
migrated Postgres with rows that actually exercise it.

These are **smoke tests, not behaviour tests**. What they assert is "this query is
valid SQL against the real engine, with real rows". The behaviour of each function
is covered on SQLite where it is faster to set up and where behaviour is identical.
Keep it that way: adding behaviour assertions here would duplicate that suite and
slow the one thing this file is for.

`pg_engine` skips when Postgres is unreachable, so this is silent locally and real
in CI. That is the same bargain `test_summary_storage.py` makes.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session as SQLSession

from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.project_timeline import ProjectTimeline, TimelineEventType
from src.domain.release import Release, ReleaseStatus
from src.domain.repository import Repository
from src.domain.repository_pull_request import RepositoryPullRequest
from src.domain.scrum import Scrum, ScrumKind
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, UserIdentity
from src.routers.webui import data
from src.services import ticket_matching

# Not a dashboard query any more: `unmapped_handles` moved to `src/services/`
# in #598 when the identities API became its second caller. It stays in this
# file because the Team page is still one of those callers and the query is
# what this file exists to run against a real engine -- it is also the only
# one here that joins `user_identity` through `project` to an organization.
from src.services.summary_service import unmapped_handles

NOW = datetime.now(timezone.utc)


@pytest.fixture(scope="module")
def world(pg_engine):
    """One org with everything a dashboard query can touch.

    Deliberately *populated*: an empty database makes every query trivially valid
    and would have let the `DISTINCT`-over-`json` bug through, since Postgres only
    raises when it has rows to compare. Each row here exists to make some query do
    real work.

    Unique aliases and emails throughout -- `organizations.alias` and
    `users.email` are uniquely indexed, and this database persists across runs, so
    fixed values pass once and then fail forever on a duplicate key. That is how a
    regression test stops testing anything.
    """
    tag = str(uuid4())[:8]
    with SQLSession(pg_engine) as session:
        org = Organization(id=str(uuid4()), name=f"Smoke {tag}", alias=f"smoke{tag}")
        user = User(
            id=str(uuid4()),
            email=f"smoke-{tag}@example.com",
            full_name="Ada Lovelace",
            github_username=f"ada{tag}",
            # The two `json` columns that broke `/ui/bp`. Non-empty on purpose:
            # Postgres only needs an equality operator when there is something to
            # compare.
            notification_preferences={"email": True},
            ui_preferences={"theme": "dark"},
        )
        session.add_all([org, user])
        session.commit()

        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=user.id,
                role=OrganizationRole.ADMIN,
                is_active=True,
            )
        )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias=f"S{tag[:6]}".upper(),
            name=f"Smoke Project {tag}",
            description="d",
        )
        session.add(project)
        session.commit()

        repo = Repository(
            id=str(uuid4()),
            name=f"repo-{tag}",
            full_name=f"acme/repo-{tag}",
            url=f"https://github.com/acme/repo-{tag}",
            organization_id=org.id,
            layer=RepositoryLayer.API,
            last_synced_at=NOW - timedelta(minutes=5),
        )
        session.add(repo)
        session.commit()
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=repo.id,
                layer=RepositoryLayer.API,
                is_active=True,
            )
        )
        session.add(
            RepositoryPullRequest(
                id=str(uuid4()),
                repository_id=repo.id,
                number=1,
                title="an open PR",
                url=f"https://github.com/acme/repo-{tag}/pull/1",
                author_login=f"ada{tag}",
                assignee_logins=[f"ada{tag}"],
                is_draft=False,
                last_synced_at=NOW,
            )
        )

        # A two-slot pipeline plus shipped history, so `release_board` has all
        # three of its sections to build.
        for version, status_ in (
            ("v1.8.0", ReleaseStatus.RELEASED),
            ("v1.9.0", ReleaseStatus.IN_PROGRESS),
            ("v1.10.0", ReleaseStatus.PLANNED),
        ):
            session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=status_,
                    released_at=NOW - timedelta(days=3)
                    if status_ == ReleaseStatus.RELEASED
                    else None,
                    summary="shipped things"
                    if status_ == ReleaseStatus.RELEASED
                    else None,
                    changelog=[{"repo": f"repo-{tag}", "prs": [{"number": 1}]}]
                    if status_ == ReleaseStatus.RELEASED
                    else None,
                )
            )

        # Two tickets assigned to the same person: `contributors_by_project` uses
        # DISTINCT, and one row would never have needed to deduplicate.
        for n, release in enumerate((None, "v1.9.0")):
            session.add(
                Ticket(
                    summary=f"ticket {n}",
                    organization_id=org.id,
                    project_id=project.id,
                    status=TicketStatus.IN_PROGRESS,
                    assignee="Ada L.",
                    assigned_to=user.id,
                    release=release,
                )
            )
        # Finished, the viewer's, and stamped -- so `my_done_recently_for` has a
        # row to return rather than being trivially valid.
        session.add(
            Ticket(
                summary="finished yesterday",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.DONE,
                assignee="Ada L.",
                assigned_to=user.id,
                completed_at=(NOW - timedelta(days=1)).replace(tzinfo=None),
            )
        )
        # A submitted personal update and a submitted team scrum on the same day,
        # so `scrum_activity_today`'s join to `users` has both kinds to resolve.
        for kind in (ScrumKind.UPDATE.value, ScrumKind.SCRUM.value):
            session.add(
                Scrum(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    run_by_user_id=user.id,
                    started_at=NOW.replace(tzinfo=None),
                    ended_at=NOW.replace(tzinfo=None),
                    kind=kind,
                    day=NOW.date(),
                )
            )
        # An unmapped board assignee -- nothing resolves this name to a user.
        session.add(
            Ticket(
                summary="someone else's",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.TODO,
                assignee="Nobody Known",
            )
        )
        session.add(
            UserIdentity(
                id=str(uuid4()),
                user_id=user.id,
                organization_id=org.id,
                project_id=project.id,
                platform=IdentityPlatform.LINEAR,
                handle="ada",
            )
        )
        session.add(
            ProjectTimeline(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                event_type=TimelineEventType.RELEASE_CREATED,
                title="Release v1.9.0 created",
                # NOT NULL in Postgres, despite reading as optional on the model.
                summary="v1.9.0 opened",
                created_by=user.id,
            )
        )
        session.commit()

        yield {"org": org, "user": user, "project": project, "engine": pg_engine}


def _call(session, world, name):
    """Invoke one data-layer function with arguments that make it do work."""
    org, user, project = world["org"], world["user"], world["project"]
    pids = [project.id]
    return {
        "member_organizations": lambda: data.member_organizations(session, user),
        "can_open": lambda: data.can_open(session, user, org.id),
        "project_cards": lambda: data.project_cards(session, org.id),
        "live_summaries_for": lambda: data.live_summaries_for(session, pids, user.id),
        "viewer_has_identity": lambda: data.viewer_has_identity(session, user, project),
        "viewer_has_any_handle": lambda: data.viewer_has_any_handle(session, user),
        "summary_panel": lambda: data.summary_panel(session, project, user),
        "summary_panel_personal": lambda: data.summary_panel(
            session, project, user, prefer_personal=True
        ),
        "unmapped_counts_for": lambda: data.unmapped_counts_for(session, pids),
        "profile_rows": lambda: data.profile_rows(session, user, org.id),
        "my_tickets": lambda: data.my_tickets(session, project.id, user.id),
        "my_pull_requests": lambda: data.my_pull_requests(session, project.id, user),
        "project_tickets": lambda: data.project_tickets(session, project.id),
        # The batched twins the workflow page uses. Worth their own rows
        # rather than trusting the single-project versions: `IN (...)` plus
        # the enum tuple is exactly the shape this file exists to catch, and
        # `or_(release IS NULL, release = '')` is Postgres-sensitive in a way
        # SQLite does not reproduce.
        "project_tickets_for": lambda: data.project_tickets_for(session, pids),
        "done_unreleased_for": lambda: data.done_unreleased_for(session, pids),
        # Same predicate as the line above, answered as a COUNT with a GROUP BY.
        # It has to run here for the same reason its sibling does: the enum
        # comparison and `or_(release IS NULL, release = '')` behave differently
        # on Postgres than on SQLite.
        "done_unreleased_totals_for": lambda: data.done_unreleased_totals_for(
            session, pids
        ),
        # The workflow launcher's two org-wide scrum reads. `scrum_activity_today`
        # joins `scrums` to `users` and is exactly the shape this file exists to
        # catch: the join that broke `/ui/bp` selected a `User` entity under
        # DISTINCT, and `users` has two `json` columns Postgres cannot compare.
        "scrum_activity_today": lambda: data.scrum_activity_today(
            session, pids, user.id, day=NOW.date()
        ),
        "my_done_recently_for": lambda: data.my_done_recently_for(
            session, pids, user.id, since=NOW.replace(tzinfo=None) - timedelta(days=7)
        ),
        # `or_(assignee IS NULL, assignee = '')` beside an enum comparison, which
        # is the pairing that behaves differently here than on SQLite.
        "unowned_todo_for": lambda: data.unowned_todo_for(session, pids),
        "project_timeline": lambda: data.project_timeline(session, project.id, user.id),
        "release_board": lambda: data.release_board(session, project.id),
        # These two moved to `services.ticket_matching` -- the branch-to-ticket
        # join is needed by the release path too, and lived somewhere only the
        # web UI could reach. Still exercised here: they are the queries whose
        # Postgres behaviour matters most, and the coverage check below now
        # ignores them because it filters on the defining module.
        "pull_requests_by_ticket": lambda: ticket_matching.pull_requests_by_ticket(
            session, project.id
        ),
        "merged_pull_requests_by_ticket": (
            lambda: ticket_matching.merged_pull_requests_by_ticket(session, project.id)
        ),
        "contributors_by_project": lambda: data.contributors_by_project(session, pids),
        "team_members": lambda: data.team_members(session, org.id, user),
        "admin_count": lambda: data.admin_count(session, org.id),
        "unmapped_handles": lambda: unmapped_handles(session, org.id, pids),
        "alias_is_available": lambda: data.alias_is_available(session, org.id, "ZZZ"),
    }[name]()


QUERIES = [
    "member_organizations",
    "can_open",
    "project_cards",
    "live_summaries_for",
    "viewer_has_identity",
    "viewer_has_any_handle",
    "summary_panel",
    "summary_panel_personal",
    "unmapped_counts_for",
    "profile_rows",
    "my_tickets",
    "my_pull_requests",
    "project_tickets",
    "project_tickets_for",
    "done_unreleased_for",
    "done_unreleased_totals_for",
    "scrum_activity_today",
    "my_done_recently_for",
    "unowned_todo_for",
    "project_timeline",
    "release_board",
    "pull_requests_by_ticket",
    "merged_pull_requests_by_ticket",
    "contributors_by_project",
    "team_members",
    "admin_count",
    "unmapped_handles",
    "alias_is_available",
]


@pytest.mark.parametrize("name", QUERIES)
def test_query_is_valid_against_postgres(world, name):
    """One test per query, so a failure names the offending function.

    A single test calling all twenty would stop at the first break and hide the
    rest -- which matters here, because the failures this file exists to catch
    (`json` under DISTINCT, enum casing, JSON operators) tend to arrive in
    clusters rather than alone.
    """
    with SQLSession(world["engine"]) as session:
        _call(session, world, name)


def test_every_public_query_in_data_is_covered():
    """The list above has to keep up with `data.py`, or this file quietly stops
    covering the function someone just added -- which is the failure mode of every
    hand-maintained inventory."""
    import inspect

    public = {
        name
        for name, obj in inspect.getmembers(data, inspect.isfunction)
        if not name.startswith("_")
        and obj.__module__ == data.__name__
        and "session" in inspect.signature(obj).parameters
    }
    covered = {n.removesuffix("_personal") for n in QUERIES}
    assert not (public - covered), (
        f"not exercised against Postgres: {sorted(public - covered)}"
    )
