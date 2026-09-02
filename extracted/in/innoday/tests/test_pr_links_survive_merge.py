"""A ticket's link to the pull requests that shipped it must outlive the merge.

`head_ref` -- the branch name -- is the only field on a pull request that names a
ticket. `repository_pull_requests` held only what GitHub currently reported as
*open*, and the sync deleted every row it no longer saw, so that link existed for
exactly as long as the pull request was unmerged. "Which pull requests shipped
PF-1268?" was answerable right up until the day it was worth asking.

Rows are marked now, not removed.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.repository_pull_request import RepositoryPullRequest


def _pr(number, **kw):
    """A GitHub payload as `list_open_pull_requests` returns it."""
    payload = {
        "number": number,
        "title": f"PR {number}",
        "html_url": f"https://github.com/o/r/pull/{number}",
        "user": {"login": "havkarl"},
        "head": {"ref": f"PF-{number}-branch"},
        "assignees": [],
        "draft": False,
        "created_at": "2026-08-01T00:00:00Z",
        "updated_at": "2026-08-02T00:00:00Z",
    }
    payload.update(kw)
    return payload


def _service(db_engine):
    from src.services.github_connect_service import GitHubConnectService

    service = GitHubConnectService.__new__(GitHubConnectService)
    service.session = Session(db_engine)
    return service


def _repo_row(db_engine, org):
    from src.domain.repository import Repository

    with Session(db_engine) as session:
        repo = Repository(
            id=str(uuid4()),
            organization_id=org.id,
            name="innoday",
            full_name="havilandsoftware/innoday",
            url="https://github.com/havilandsoftware/innoday",
        )
        session.add(repo)
        session.commit()
        return repo.id


def _rows(db_engine, repo_id):
    with Session(db_engine) as session:
        return {
            row.number: row
            for row in session.exec(
                select(RepositoryPullRequest).where(
                    RepositoryPullRequest.repository_id == repo_id
                )
            ).all()
        }


class TestAMergedPullRequestIsKept:
    @pytest.mark.asyncio
    async def test_it_is_marked_rather_than_deleted(self, db_engine, org):
        """The bug, stated directly."""
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        api = MagicMock()
        api.get_pull_request_outcome = AsyncMock(
            return_value={"state": "closed", "merged_at": "2026-08-10T12:00:00Z"}
        )

        await service._store_pull_requests(repo, [_pr(1)], api, "o", "r")
        service.session.commit()
        await service._store_pull_requests(repo, [], api, "o", "r")
        service.session.commit()

        rows = _rows(db_engine, repo_id)
        assert 1 in rows, "the row was deleted -- the ticket link is gone"
        assert rows[1].state == "closed"
        assert rows[1].merged_at is not None
        assert rows[1].head_ref == "PF-1-branch", "the link itself must survive"

    @pytest.mark.asyncio
    async def test_an_abandoned_one_is_kept_but_not_marked_merged(self, db_engine, org):
        """Closed and merged are different answers. An abandoned pull request
        shipped nothing and must not read as though it had."""
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        api = MagicMock()
        api.get_pull_request_outcome = AsyncMock(
            return_value={"state": "closed", "merged_at": None}
        )

        await service._store_pull_requests(repo, [_pr(2)], api, "o", "r")
        service.session.commit()
        await service._store_pull_requests(repo, [], api, "o", "r")
        service.session.commit()

        row = _rows(db_engine, repo_id)[2]
        assert row.state == "closed"
        assert row.merged_at is None

    @pytest.mark.asyncio
    async def test_an_unanswered_probe_does_not_claim_a_merge(self, db_engine, org):
        """Claiming a merge we could not confirm would put work in a release
        that never had it. Unknown reads as did-not-ship."""
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        api = MagicMock()
        api.get_pull_request_outcome = AsyncMock(return_value=None)

        await service._store_pull_requests(repo, [_pr(3)], api, "o", "r")
        service.session.commit()
        await service._store_pull_requests(repo, [], api, "o", "r")
        service.session.commit()

        row = _rows(db_engine, repo_id)[3]
        assert row.state == "closed"
        assert row.merged_at is None

    @pytest.mark.asyncio
    async def test_a_closed_row_is_not_re_probed_every_sync(self, db_engine, org):
        """One request per *departure*, not per sync forever. Otherwise every
        sync costs one call for every pull request the repo has ever had."""
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        api = MagicMock()
        api.get_pull_request_outcome = AsyncMock(
            return_value={"state": "closed", "merged_at": "2026-08-10T12:00:00Z"}
        )

        await service._store_pull_requests(repo, [_pr(4)], api, "o", "r")
        service.session.commit()
        for _ in range(3):
            await service._store_pull_requests(repo, [], api, "o", "r")
            service.session.commit()

        assert api.get_pull_request_outcome.await_count == 1

    @pytest.mark.asyncio
    async def test_a_reopened_pull_request_goes_back_to_open(self, db_engine, org):
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        api = MagicMock()
        api.get_pull_request_outcome = AsyncMock(
            return_value={"state": "closed", "merged_at": None}
        )

        await service._store_pull_requests(repo, [_pr(5)], api, "o", "r")
        service.session.commit()
        await service._store_pull_requests(repo, [], api, "o", "r")
        service.session.commit()
        await service._store_pull_requests(repo, [_pr(5)], api, "o", "r")
        service.session.commit()

        row = _rows(db_engine, repo_id)[5]
        assert (row.state, row.merged_at, row.closed_seen_at) == ("open", None, None)


class TestTheEmptyListGuardStillGuards:
    """**The interaction that would have failed silently.**

    `_empty_pr_list_is_believable` probes the highest stored number and treats a
    "closed" answer as proof the empty list is honest. Keeping closed rows means
    an unfiltered probe would soon pick one of *them* -- always answering closed,
    always believing the list, and never saying so.
    """

    @pytest.mark.asyncio
    async def test_it_probes_an_open_row_not_the_highest_number(self, db_engine, org):
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        with Session(db_engine) as session:
            session.add(
                RepositoryPullRequest(
                    repository_id=repo_id,
                    number=99,
                    title="merged",
                    url="u",
                    state="closed",
                    merged_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
                )
            )
            session.add(
                RepositoryPullRequest(
                    repository_id=repo_id,
                    number=7,
                    title="open",
                    url="u",
                    state="open",
                )
            )
            session.commit()

        api = MagicMock()
        api.get_pull_request_state = AsyncMock(return_value="open")

        ok, why = await service._empty_pr_list_is_believable(api, "o", "r", repo)

        api.get_pull_request_state.assert_awaited_once()
        assert api.get_pull_request_state.await_args[0][2] == 7, (
            "probed the closed #99 instead of the open #7 -- the guard would "
            "believe every empty list from now on"
        )
        assert ok is False, why

    @pytest.mark.asyncio
    async def test_only_closed_rows_means_nothing_to_protect(self, db_engine, org):
        """No open rows is not the same as no rows. Nothing can be lost, so the
        empty list needs no checking -- and must not cost a request."""
        repo_id = _repo_row(db_engine, org)
        service = _service(db_engine)
        from src.domain.repository import Repository

        repo = service.session.get(Repository, repo_id)

        with Session(db_engine) as session:
            session.add(
                RepositoryPullRequest(
                    repository_id=repo_id,
                    number=42,
                    title="merged",
                    url="u",
                    state="closed",
                )
            )
            session.commit()

        api = MagicMock()
        api.get_pull_request_state = AsyncMock(return_value="closed")

        ok, _why = await service._empty_pr_list_is_believable(api, "o", "r", repo)

        assert ok is True
        api.get_pull_request_state.assert_not_awaited()
