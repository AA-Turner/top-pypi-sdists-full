"""#650: a GitHub sync leaves a record, and an empty PR list is checked.

Two halves of the same complaint. `github_sync_history` had a full column set and
no rows ever, so "did a sync run, and did it fail?" had no answer; and
`_store_pull_requests` deleted every stored pull request GitHub did not return,
treating `200 []` as "they all closed" on the strength of the fetch having
succeeded -- which a token that has lost access to a repository also does.

The aborted-transaction half of the history write is **not** testable here: SQLite
has no aborted state, so a row written into one is not lost and a test asserting it
survived would pass against a recorder with no rollback at all. That test lives in
`tests/test_postgres_only.py`.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository
from src.domain.repository import GitHubSyncHistory, Repository
from src.domain.repository_pull_request import RepositoryPullRequest
from src.services.github_connect_service import GitHubConnectService
from tests.db_helpers import build_test_engine


@pytest.fixture
def session():
    engine = build_test_engine()
    with Session(engine) as s:
        yield s


@pytest.fixture
def org(session):
    o = Organization(id=str(uuid4()), name="Hist Org", alias="historg")
    session.add(o)
    session.commit()
    return o


@pytest.fixture
def project(session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias="HIST",
        name="History Project",
        description="d",
    )
    session.add(p)
    session.commit()
    return p


def _service(session):
    service = GitHubConnectService(session)
    service._get_github_credentials = lambda *a, **k: {
        "token": "tok",
        "github_org": "acme",
    }
    return service


def _raw_repo(github_id: str, name: str) -> dict:
    return {
        "id": int(github_id),
        "name": name,
        "full_name": f"acme/{name}",
        "html_url": f"https://github.com/acme/{name}",
        "description": None,
        "language": "Python",
        "topics": ["hist"],
        "archived": False,
        "private": False,
    }


def _topics_gone():
    """Sync confirms a repo really lost the topic before retiring it."""
    return patch(
        "src.api.github_api.GitHubAPI.get_repository_topics",
        new=AsyncMock(return_value=[]),
    )


def _history(session, project_id):
    return session.exec(
        select(GitHubSyncHistory).where(GitHubSyncHistory.project_id == project_id)
    ).all()


# --------------------------------------------------------------------------- #
# github_sync_history
# --------------------------------------------------------------------------- #


class TestSyncHistoryIsWritten:
    @pytest.mark.asyncio
    async def test_a_successful_sync_leaves_a_completed_row(
        self, session, org, project
    ):
        """The table's first row, ever.

        Asserted through the columns a reader would actually ask -- when it ran,
        whether it worked, how many repositories -- rather than merely that a row
        exists, because "a row exists" would pass for a row full of zeros.
        """
        service = _service(session)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("1001", "repo-a")]),
            ),
            patch.object(
                service, "_refresh_open_pr_counts", new=AsyncMock(return_value=(1, 0))
            ),
            patch.object(service, "_discover_releases", new=AsyncMock(return_value=0)),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        rows = _history(session, project.id)
        assert len(rows) == 1, "one row per attempt"
        row = rows[0]
        assert row.status == "completed"
        assert row.organization_id == org.id
        assert row.repositories_synced == 1
        assert row.repositories_created == 1
        assert row.repositories_failed == 0
        assert row.error_message is None
        assert row.completed_at is not None
        assert row.started_at <= row.completed_at
        assert row.duration_seconds is not None and row.duration_seconds >= 0
        # Naive UTC, like every other datetime column in this schema. An aware
        # value here would raise the moment anything compared it to a sibling.
        assert row.started_at.tzinfo is None
        assert row.completed_at.tzinfo is None
        # Not measured, so not claimed. Nothing counts GitHub requests, and a
        # plausible integer here would be exactly the kind of unsubstantiated
        # number #650 is about.
        assert row.api_calls_made is None

    @pytest.mark.asyncio
    async def test_a_failed_sync_leaves_a_failed_row(self, session, org, project):
        """The path that was worth having a table for.

        A sync that dies raises to its caller and reds the project icon; before
        #650 nothing recorded that the attempt had happened, so an operator asking
        "has this been failing all week or did it break just now?" had no way to
        tell.
        """
        service = _service(session)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("1002", "repo-b")]),
            ),
            patch(
                "src.services.github_connect_service.add_timeline_entry",
                side_effect=RuntimeError("timeline write blew up"),
            ),
            _topics_gone(),
        ):
            with pytest.raises(RuntimeError):
                await service.sync_project_repositories(org.id, project.id)

        rows = _history(session, project.id)
        assert len(rows) == 1
        row = rows[0]
        assert row.status == "failed"
        assert row.organization_id == org.id
        assert row.completed_at is not None
        # What had been discovered before it died, not a zero that would read as
        # "found nothing".
        assert row.repositories_synced == 1

    @pytest.mark.asyncio
    async def test_an_unexpected_failure_is_not_quoted_verbatim(
        self, session, org, project
    ):
        """`error_message` is narrowed by `_reportable_sync_error`, `error_details`
        names the type only.

        Nothing renders either column today, and that is precisely why: the row
        outlives the decision not to show it. `RuntimeError`'s text here stands in
        for the real cases -- an `IntegrityError` stringifies to the failing SQL
        plus its bound parameters, an `OperationalError` to connection detail.
        """
        service = _service(session)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("1003", "repo-c")]),
            ),
            patch(
                "src.services.github_connect_service.add_timeline_entry",
                side_effect=RuntimeError("internal detail nobody should read"),
            ),
            _topics_gone(),
        ):
            with pytest.raises(RuntimeError):
                await service.sync_project_repositories(org.id, project.id)

        row = _history(session, project.id)[0]
        assert "internal detail nobody should read" not in (row.error_message or "")
        assert row.error_message == (
            "The sync failed unexpectedly — check the server logs"
        )
        assert row.error_details == "RuntimeError — full detail in the server log"

    @pytest.mark.asyncio
    async def test_a_deliberate_refusal_is_reported_as_written(
        self, session, org, project
    ):
        """The other side: a message written *for* a reader passes through whole.

        A narrowing that dropped everything would be no better than the empty
        table -- "it failed" with no reason is not an answer either.
        """
        service = _service(session)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(side_effect=ValueError("no GitHub credential stored")),
            ),
            _topics_gone(),
        ):
            with pytest.raises(ValueError):
                await service.sync_project_repositories(org.id, project.id)

        row = _history(session, project.id)[0]
        assert row.status == "failed"
        assert "no GitHub credential stored" in row.error_message

    @pytest.mark.asyncio
    async def test_a_broken_recorder_does_not_break_a_working_sync(
        self, session, org, project
    ):
        """An audit row must never become the outcome it was recording.

        The success call sits outside the `try` *and* the recorder swallows its own
        errors; either alone would do, and both are cheap. Inside the try with no
        internal guard, a database fault while writing this row would be caught by
        the failure handler and reported as a failed sync -- turning the record of a
        success into the destruction of one.

        The call count is asserted first, and it is what keeps this test honest: a
        sync that never tries to write a history row satisfies every claim below
        vacuously, which is precisely how the pre-#650 code behaves.
        """
        service = _service(session)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("1005", "repo-e")]),
            ),
            patch.object(
                service, "_refresh_open_pr_counts", new=AsyncMock(return_value=(1, 0))
            ),
            patch.object(service, "_discover_releases", new=AsyncMock(return_value=0)),
            patch.object(
                GitHubSyncHistory,
                "__init__",
                side_effect=RuntimeError("history row blew up"),
            ) as broken,
            _topics_gone(),
        ):
            result = await service.sync_project_repositories(org.id, project.id)

        assert broken.call_count == 1, "the sync must have tried to record itself"
        assert result["status"] == "completed"
        assert _history(session, project.id) == []
        session.refresh(project)
        assert project.github_errored_at is None, (
            "a failure to write the audit row must not red the project icon"
        )


# --------------------------------------------------------------------------- #
# the empty-list hazard
# --------------------------------------------------------------------------- #


def _attach_repo_with_stored_prs(session, org, project, *, numbers):
    repo = Repository(
        id="2001",
        organization_id=org.id,
        name="repo-prs",
        full_name="acme/repo-prs",
        url="https://github.com/acme/repo-prs",
        layer="api",
        open_pr_count=len(numbers),
        last_synced_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    session.add(repo)
    session.add(
        ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id=repo.id,
            is_active=True,
        )
    )
    for number in numbers:
        session.add(
            RepositoryPullRequest(
                repository_id=repo.id,
                number=number,
                title=f"PR {number}",
                url=f"https://github.com/acme/repo-prs/pull/{number}",
            )
        )
    session.commit()
    return repo


class TestEmptyPullRequestList:
    """`200 []` is acted on when it is honest and refused when it is not.

    Both directions are asserted, because either one alone is satisfiable by a
    wrong implementation: a blanket "never delete on empty" passes the second test
    and leaves merged work on the dashboard forever, and the pre-#650 code passes
    the first.
    """

    @pytest.mark.asyncio
    async def test_an_honest_empty_list_deletes_the_stored_rows(
        self, session, org, project
    ):
        """The last open pull request closing is an ordinary event.

        GitHub returns nothing, and the one stored pull request the check probes is
        genuinely closed -- so the list is consistent with GitHub's own answer and
        is acted on.
        """
        repo = _attach_repo_with_stored_prs(session, org, project, numbers=[7, 8])
        service = _service(session)

        with (
            patch(
                "src.api.github_api.GitHubAPI.list_open_pull_requests",
                new=AsyncMock(return_value=[]),
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_pull_request_state",
                new=AsyncMock(return_value="closed"),
            ) as probe,
        ):
            counted, failed = await service._refresh_open_pr_counts(org.id, project.id)

        assert (counted, failed) == (1, 0)
        # The newest stored number is probed: it is the one most likely to still be
        # open, so it is the one that can detect a lying list. Probing the oldest
        # would wave most of them through.
        assert probe.await_args.args[2] == 8
        # `_refresh_open_pr_counts` leaves its writes pending -- the real caller
        # commits them -- so commit here rather than `refresh`, which would
        # re-read the row and discard exactly what is under test.
        session.commit()
        assert repo.open_pr_count == 0
        assert repo.errored_at is None

        # **Marked closed, not deleted.** This asserted the rows were *gone*, which
        # was the behaviour that severed a ticket's link to the pull requests that
        # shipped it -- `head_ref` is the only field naming a ticket, and it went
        # with the row. Acting on the empty list still means "none of these are
        # open"; it no longer means "forget they existed".
        rows = session.exec(
            select(RepositoryPullRequest).where(
                RepositoryPullRequest.repository_id == repo.id
            )
        ).all()
        assert {r.number for r in rows} == {7, 8}, "the rows must survive"
        assert {r.state for r in rows} == {"closed"}, (
            "a confirmed-empty list is acted on -- none of these are open"
        )

    @pytest.mark.asyncio
    async def test_a_lying_empty_list_keeps_the_rows_and_records_the_repo(
        self, session, org, project
    ):
        """A fetch can succeed and be wrong.

        A token that has lost access to a repository receives HTTP 200 and `[]` --
        byte-for-byte what a repository with nothing open returns. Asking about one
        stored pull request separates them: it answers "open", so the empty list
        contradicts GitHub itself and must not be acted on.
        """
        repo = _attach_repo_with_stored_prs(session, org, project, numbers=[7, 8])
        service = _service(session)

        with (
            patch(
                "src.api.github_api.GitHubAPI.list_open_pull_requests",
                new=AsyncMock(return_value=[]),
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_pull_request_state",
                new=AsyncMock(return_value="open"),
            ),
        ):
            counted, failed = await service._refresh_open_pr_counts(org.id, project.id)

        # The rows first: they are the point, and the counters only describe what
        # was done to them.
        session.commit()
        kept = session.exec(
            select(RepositoryPullRequest).where(
                RepositoryPullRequest.repository_id == repo.id
            )
        ).all()
        assert sorted(row.number for row in kept) == [7, 8], (
            "an empty list that contradicts GitHub's own answer must not delete "
            "anybody's work"
        )
        assert repo.open_pr_count == 2, "and the count must not be zeroed either"
        assert repo.errored_at is not None
        assert "#8 is still open" in repo.error_message
        assert (counted, failed) == (0, 1)

    @pytest.mark.asyncio
    async def test_an_unanswerable_probe_also_keeps_the_rows(
        self, session, org, project
    ):
        """No answer is not a "closed".

        This is the shape the lapsed-grant case actually makes: a token that cannot
        see the repository cannot answer about one of its pull requests either. A
        probe that returns `None` and is read as confirmation would delete
        everything in exactly the case the check exists for.
        """
        repo = _attach_repo_with_stored_prs(session, org, project, numbers=[7])
        service = _service(session)

        with (
            patch(
                "src.api.github_api.GitHubAPI.list_open_pull_requests",
                new=AsyncMock(return_value=[]),
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_pull_request_state",
                new=AsyncMock(return_value=None),
            ),
        ):
            counted, failed = await service._refresh_open_pr_counts(org.id, project.id)

        assert (counted, failed) == (0, 1)
        assert (
            len(
                session.exec(
                    select(RepositoryPullRequest).where(
                        RepositoryPullRequest.repository_id == repo.id
                    )
                ).all()
            )
            == 1
        )
        session.commit()
        assert repo.errored_at is not None

    @pytest.mark.asyncio
    async def test_an_empty_list_costs_no_extra_request_with_nothing_stored(
        self, session, org, project
    ):
        """The check is paid for only when there is something to lose.

        A repository with no stored pull requests has nothing an empty list could
        delete, so it is believed without a probe -- which is what keeps this from
        being a second request per repository per sync.
        """
        repo = Repository(
            id="2002",
            organization_id=org.id,
            name="repo-fresh",
            full_name="acme/repo-fresh",
            url="https://github.com/acme/repo-fresh",
            layer="api",
            last_synced_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(repo)
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=repo.id,
                is_active=True,
            )
        )
        session.commit()
        service = _service(session)

        with (
            patch(
                "src.api.github_api.GitHubAPI.list_open_pull_requests",
                new=AsyncMock(return_value=[]),
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_pull_request_state",
                new=AsyncMock(return_value="closed"),
            ) as probe,
        ):
            counted, failed = await service._refresh_open_pr_counts(org.id, project.id)

        assert (counted, failed) == (1, 0)
        assert probe.await_count == 0
        session.commit()
        assert repo.open_pr_count == 0

    @pytest.mark.asyncio
    async def test_a_non_empty_list_is_never_probed(self, session, org, project):
        """The ordinary path is untouched.

        A list with contents states which pull requests are open; there is nothing
        for a probe to add, and adding one would put a request on every repository
        of every sync.
        """
        repo = _attach_repo_with_stored_prs(session, org, project, numbers=[7, 8])
        service = _service(session)

        with (
            patch(
                "src.api.github_api.GitHubAPI.list_open_pull_requests",
                new=AsyncMock(
                    return_value=[
                        {
                            "number": 8,
                            "title": "Still open",
                            "html_url": "https://github.com/acme/repo-prs/pull/8",
                            "user": {"login": "someone"},
                            "head": {"ref": "HS-650-branch"},
                            "assignees": [],
                            "draft": False,
                            "created_at": "2026-08-01T00:00:00Z",
                            "updated_at": "2026-08-02T00:00:00Z",
                        }
                    ]
                ),
            ),
            patch(
                "src.api.github_api.GitHubAPI.get_pull_request_state",
                new=AsyncMock(return_value="closed"),
            ) as probe,
        ):
            counted, failed = await service._refresh_open_pr_counts(org.id, project.id)

        assert (counted, failed) == (1, 0)
        assert probe.await_count == 0
        session.commit()
        assert repo.open_pr_count == 1
        kept = {
            row.number: row
            for row in session.exec(
                select(RepositoryPullRequest).where(
                    RepositoryPullRequest.repository_id == repo.id
                )
            ).all()
        }
        # #7 is genuinely gone from the open list -- and is now recorded as closed
        # rather than deleted, so the ticket it names keeps its link to it.
        assert kept[8].state == "open"
        assert kept[7].state == "closed"
        assert repo.open_pr_count == 1, "the count follows the list, not the rows"


# --------------------------------------------------------------------------- #
# the cascade the new columns pulled into scope
# --------------------------------------------------------------------------- #


def test_deleting_an_organization_removes_its_project_sync_history(
    session, org, project
):
    """A row keyed on `organization_id` must go with the organization.

    `delete_organization_cascade` matched `github_sync_history` on the registration
    FK alone, which was the table's only key until #650. Every row the project sync
    writes had that column NULL, so they would all have survived -- and on Postgres
    their `organization_id` FK then refuses the `organizations` delete two levels
    later, failing an org delete with an integrity error naming a table nobody would
    look at. #658 dropped the registration column entirely, so `organization_id` is
    now the only thing the cascade can match on and this is the only shape of row
    there is.

    Asserted as a deleted row rather than as a successful delete on purpose: SQLite
    has foreign keys off (`tests/db_helpers.build_test_engine`), so a test that only
    checked the delete did not raise would pass against the orphan too.
    """
    from src.services.organization_cascade import delete_organization_cascade

    session.add(
        GitHubSyncHistory(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            started_at=datetime.now(timezone.utc).replace(tzinfo=None),
            completed_at=datetime.now(timezone.utc).replace(tzinfo=None),
            status="completed",
        )
    )
    session.commit()
    assert len(_history(session, project.id)) == 1

    delete_organization_cascade(session, org.id)
    session.commit()

    assert (
        session.exec(
            select(GitHubSyncHistory).where(GitHubSyncHistory.organization_id == org.id)
        ).all()
        == []
    )
