"""
Tests for GitHubConnectService.sync_project_repositories' reconciliation
behavior (soft-delete on topic loss, reactivation) and
remove_project_repository (removes the GitHub topic, then soft-deletes).
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import httpx
import pytest
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.api.github_api import GitHubAPIError
from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository
from src.domain.repository import Repository
from src.routers.webui.data import project_cards
from src.services.github_connect_service import (
    _UNEXPECTED_SYNC_ERROR,
    GitHubConnectService,
)
from tests.db_helpers import build_test_engine


@pytest.fixture
def session():
    engine = build_test_engine()
    with Session(engine) as s:
        yield s


@pytest.fixture
def org(session):
    o = Organization(id=str(uuid4()), name="Test Org", alias="testorg")
    session.add(o)
    session.commit()
    session.refresh(o)
    return o


@pytest.fixture
def project(session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias="MYPROJ",
        name="My Project",
        description="Test project",
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


#: Sync now confirms with GitHub before retiring a repo: "the search did not
#: return it" and "the tag was removed" are different statements, and only the
#: second justifies deactivation. These tests simulate a repo that genuinely lost
#: the topic, so the per-repo lookup must agree with the search and report no
#: matching topic. Without this the service (correctly) refuses to deactivate.
def _topics_gone():
    return patch(
        "src.api.github_api.GitHubAPI.get_repository_topics",
        new=AsyncMock(return_value=[]),
    )


def _validation_error(payload: str) -> ValidationError:
    """A real `pydantic.ValidationError` -- a `ValueError` subclass whose `str()`
    quotes back the value it was handed. Built rather than faked, because the
    property under test is pydantic's own formatting."""

    class _Port(BaseModel):
        port: int

    with pytest.raises(ValidationError) as caught:
        _Port(port=payload)
    return caught.value


def _raw_repo(github_id: str, name: str) -> dict:
    return {
        "id": int(github_id),
        "name": name,
        "full_name": f"acme/{name}",
        "html_url": f"https://github.com/acme/{name}",
        "description": None,
        "language": "Python",
        "topics": ["my-project"],
        "archived": False,
        "private": False,
    }


class TestSyncProjectRepositoriesReconciliation:
    @pytest.mark.asyncio
    async def test_repo_losing_topic_is_soft_deleted_not_hard_deleted(
        self, session, org, project
    ):
        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("111", "repo-a")]),
            ),
            _topics_gone(),
        ):
            result1 = await service.sync_project_repositories(org.id, project.id)
        assert result1["changes"]["new_repositories"][0]["name"] == "repo-a"

        link = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).first()
        assert link.is_active is True
        assert link.removed_at is None

        # Second sync: GitHub search no longer returns repo-a (lost the topic)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[]),
            ),
            _topics_gone(),
        ):
            result2 = await service.sync_project_repositories(org.id, project.id)

        assert result2["changes"]["deactivated_repositories"] == 1
        assert "repo-a" in result2["changes"]["deactivated_repository_names"]

        session.refresh(link)
        assert link.is_active is False
        assert link.removed_at is not None

        # Row still exists (soft delete, not hard delete)
        still_there = session.exec(
            select(ProjectRepository).where(ProjectRepository.id == link.id)
        ).first()
        assert still_there is not None

    @pytest.mark.asyncio
    async def test_repo_regaining_topic_reactivates_same_row_not_duplicate(
        self, session, org, project
    ):
        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("222", "repo-b")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        # Lose the topic
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        # Regain the topic
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("222", "repo-b")]),
            ),
            _topics_gone(),
        ):
            result = await service.sync_project_repositories(org.id, project.id)

        assert result["changes"]["reactivated_repositories"] == 1
        assert result["changes"]["new_repositories"] == []

        links = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).all()
        assert len(links) == 1  # reactivated, not duplicated
        assert links[0].is_active is True
        assert links[0].removed_at is None

    @pytest.mark.asyncio
    async def test_only_one_primary_across_multiple_syncs(self, session, org, project):
        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("333", "repo-c")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        # A second sync discovers a brand new repo -- must not also be primary
        with patch(
            "src.api.github_api.GitHubAPI.search_organization_repositories",
            new=AsyncMock(
                return_value=[_raw_repo("333", "repo-c"), _raw_repo("444", "repo-d")]
            ),
        ):
            await service.sync_project_repositories(org.id, project.id)

        links = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).all()
        primaries = [link for link in links if link.is_primary]
        assert len(primaries) == 1

    @pytest.mark.asyncio
    async def test_primary_reelected_when_primary_repo_is_deactivated(
        self, session, org, project
    ):
        """
        Regression test: deactivating the current primary repo (it lost the
        topic label) must promote a replacement in the same sync call, not
        leave the project with zero active primaries.
        """
        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with patch(
            "src.api.github_api.GitHubAPI.search_organization_repositories",
            new=AsyncMock(
                return_value=[
                    _raw_repo("501", "repo-primary"),
                    _raw_repo("502", "repo-other"),
                ]
            ),
        ):
            await service.sync_project_repositories(org.id, project.id)

        links = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).all()
        primary_link = next(link for link in links if link.is_primary)
        assert primary_link.repository_id == "501"  # first discovered is primary

        # repo-primary loses the topic label; repo-other keeps it
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("502", "repo-other")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        links = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).all()
        active_primaries = [
            link for link in links if link.is_active and link.is_primary
        ]
        assert len(active_primaries) == 1
        assert active_primaries[0].repository_id == "502"

        deactivated = next(link for link in links if link.repository_id == "501")
        assert deactivated.is_active is False
        assert deactivated.is_primary is False  # cleared, not left stale

    @pytest.mark.asyncio
    async def test_reactivation_preserves_manually_set_layer(
        self, session, org, project
    ):
        """
        Regression test: an admin's manual layer reclassification must
        survive a deactivate/reactivate cycle, not get silently reverted to
        GitHub's auto-detected layer on reactivation.
        """
        from src.domain.project import RepositoryLayer

        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("601", "repo-f")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        # Admin manually reclassifies the layer
        link = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).first()
        link.layer = RepositoryLayer.DATA
        session.add(link)
        session.commit()

        # Repo loses the topic, then regains it
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("601", "repo-f")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        session.refresh(link)
        assert link.is_active is True
        assert link.layer == RepositoryLayer.DATA  # manual override preserved

    @pytest.mark.asyncio
    async def test_sync_writes_timeline_entry(self, session, org, project):
        from src.domain.project_timeline import ProjectTimeline, TimelineEventType

        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("701", "repo-g")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        entry = session.exec(
            select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
        ).first()
        assert entry is not None
        assert entry.event_type == TimelineEventType.REPO_ADDED
        assert "repo-g" in entry.summary

    @pytest.mark.asyncio
    async def test_noop_sync_writes_no_timeline_entry(self, session, org, project):
        from src.domain.project_timeline import ProjectTimeline

        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        entries = session.exec(
            select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
        ).all()
        assert entries == []


class TestRemoveProjectRepository:
    @pytest.mark.asyncio
    async def test_remove_repository_removes_topic_and_soft_deletes(
        self, session, org, project
    ):
        repo = Repository(
            id="555",
            organization_id=org.id,
            name="repo-e",
            full_name="acme/repo-e",
            url="https://github.com/acme/repo-e",
        )
        session.add(repo)
        link = ProjectRepository(
            project_id=project.id, repository_id=repo.id, is_active=True
        )
        session.add(link)
        session.commit()

        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with patch(
            "src.api.github_api.GitHubAPI.remove_repository_topic",
            new=AsyncMock(return_value=[]),
        ) as mock_remove_topic:
            result = await service.remove_project_repository(
                org.id, project.id, repo.id
            )

        # Topic is derived from the project alias (lowercased), not a slug.
        mock_remove_topic.assert_called_once_with("acme", "repo-e", "myproj")
        assert result["removed_topic"] == "myproj"

        session.refresh(link)
        assert link.is_active is False
        assert link.removed_at is not None

        from src.domain.project_timeline import ProjectTimeline, TimelineEventType

        entry = session.exec(
            select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
        ).first()
        assert entry is not None
        assert entry.event_type == TimelineEventType.REPO_REMOVED
        assert "repo-e" in entry.summary

    @pytest.mark.asyncio
    async def test_remove_nonexistent_repository_raises(self, session, org, project):
        service = GitHubConnectService(session)

        with pytest.raises(ValueError, match="not found"):
            await service.remove_project_repository(org.id, project.id, "nonexistent")


class TestSyncStampsRepoFreshness:
    """A sync must record that it synced.

    `repositories.last_synced_at` was never written, so it stayed NULL forever and
    the dashboard's project freshness fell back to the *board's* last sync.
    Pressing "sync now" succeeded and the pill still read "58 days ago" --
    indistinguishable from the button doing nothing.
    """

    @pytest.mark.asyncio
    async def test_sync_stamps_last_synced_at(self, session, org, project):
        from src.domain.repository import Repository

        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: {
            "token": "tok",
            "github_org": "acme",
        }

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("111", "repo-a")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        created = session.exec(select(Repository)).all()
        assert created, "the sync should have produced a repository"
        assert all(r.last_synced_at is not None for r in created), (
            "a repo discovered by this sync has a sync time of now, not never"
        )

        # A second sync updates rather than leaves the first stamp in place.
        first = created[0].last_synced_at
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("111", "repo-a")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        refreshed = session.exec(select(Repository)).first()
        assert refreshed.last_synced_at >= first


class TestSyncRecordsItsOwnOutcome:
    """A sync that dies has to say so somewhere (#640).

    Before this, only a *partial* failure was recorded: `_record_repo_error`
    marks one repo whose open-PR read failed, and that step runs only after
    discovery has already succeeded. A sync that died outright -- dead token, no
    credential at all, a refusal -- raised a 400 to the caller and wrote nothing,
    so the dashboard's GitHub icon stayed green over a token that had not worked
    for weeks. The icon means "the token is connected and working", which needs a
    per-project record of the last attempt's outcome.
    """

    def _service(self, session, creds=None):
        service = GitHubConnectService(session)
        service._get_github_credentials = lambda *a, **k: creds
        return service

    @pytest.mark.asyncio
    async def test_a_dead_token_is_recorded_on_the_project(self, session, org, project):
        """No credential at all: the case the icon exists for."""
        service = self._service(session, creds=None)

        with pytest.raises(ValueError):
            await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None
        assert "connection" in (project.github_error_message or "").lower()

    @pytest.mark.asyncio
    async def test_a_failure_inside_discovery_is_recorded(self, session, org, project):
        """A token GitHub rejects. The message has to carry *why*, or the icon
        sends the reader to the logs to find out.

        Injected as `GitHubAPIError` because that is what a rejected token really
        raises -- `github_api` turns any non-200 into one. Only GitHub's own errors
        are quotable, so a stand-in of some other type would be pinning the
        *generic* message here while reading as though it pinned this one.
        """
        service = self._service(
            session, creds={"token": "expired", "github_org": "acme"}
        )

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(side_effect=GitHubAPIError("401 Bad credentials")),
            ),
            _topics_gone(),
        ):
            with pytest.raises(ValueError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None
        assert "401" in (project.github_error_message or "")

    @pytest.mark.asyncio
    async def test_a_later_success_clears_the_flag(self, session, org, project):
        """The half that makes the flag mean anything: a mark that is only ever
        set is a permanent red for one bad afternoon (#499)."""
        project.github_errored_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
        project.github_error_message = "401 Bad credentials"
        session.add(project)
        session.commit()

        service = self._service(session, creds={"token": "tok", "github_org": "acme"})
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("111", "repo-a")]),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is None
        assert project.github_error_message is None

    @pytest.mark.asyncio
    async def test_the_refusal_guards_are_recorded_too(self, session, org, project):
        """A refusal reds the icon. Nothing synced, and the cause is a
        resolution/scope problem -- exactly what the icon is for. Reading a
        refusal as "fine, nothing to do" is how BPAI's wrong-org sync stayed
        invisible."""
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(
                    return_value=[
                        _raw_repo("111", "repo-a"),
                        _raw_repo("222", "repo-b"),
                        _raw_repo("333", "repo-c"),
                        _raw_repo("444", "repo-d"),
                    ]
                ),
            ),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is None, "the first sync succeeded"

        # Now the search finds only one of the four -- a wrong-org resolution
        # looks exactly like this, so the sync refuses.
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("111", "repo-a")]),
            ),
            _topics_gone(),
        ):
            with pytest.raises(ValueError, match="Refusing to sync"):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None
        assert "Refusing to sync" in (project.github_error_message or "")

    @pytest.mark.asyncio
    async def test_one_projects_failure_does_not_red_a_sibling(self, session, org):
        """Why this is on `projects` and not on `github_org_registrations`.

        The credential is org-level, but the *outcome* is not: a project whose
        topic resolves to a renamed org fails while its siblings sync fine.
        Recorded org-wide, one project's bad override would red every card in
        the org and the icon would stop meaning anything per project.
        """
        failing = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="AAA",
            name="Fails",
            description="d",
        )
        healthy = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BBB",
            name="Syncs fine",
            description="d",
        )
        session.add(failing)
        session.add(healthy)
        session.commit()

        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        # The two post-commit steps are stubbed because they reach GitHub for real
        # with this fixture's fake token, and a failed open-PR read marks the
        # *repository* errored -- which reds the healthy project's card through the
        # per-repo half of `github_errored` and would mask what is asserted below.
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("555", "repo-e")]),
            ),
            patch.object(
                service, "_refresh_open_pr_counts", new=AsyncMock(return_value=(0, 0))
            ),
            patch.object(service, "_discover_releases", new=AsyncMock(return_value=0)),
            _topics_gone(),
        ):
            await service.sync_project_repositories(org.id, healthy.id)

        # `GitHubAPIError` for the same reason as above: a rejected token arrives
        # as one, and discovery relabels only that type.
        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(side_effect=GitHubAPIError("401 Bad credentials")),
            ),
            _topics_gone(),
        ):
            with pytest.raises(ValueError):
                await service.sync_project_repositories(org.id, failing.id)

        session.refresh(failing)
        session.refresh(healthy)
        assert failing.github_errored_at is not None
        assert healthy.github_errored_at is None, (
            "a sibling project's sync outcome is its own -- the shared token "
            "is not what this column records"
        )

        # And assert it through the render path, not only the column. Pinning
        # storage alone does not guard the mistake this test exists for: a change
        # that kept these columns on `Project` but *also* ORed
        # `GitHubOrgRegistration.last_error` into `github_errored` would satisfy
        # both assertions above while every sibling card in the org went red.
        cards = {card.project.alias: card for card in project_cards(session, org.id)}
        assert cards["AAA"].github_errored is True
        assert cards["BBB"].github_errored is False, (
            "the sibling's card must render green -- the icon is per project"
        )

    @pytest.mark.asyncio
    async def test_writes_still_pending_when_a_sync_fails_are_discarded(
        self, session, org, project
    ):
        """The recorder rolls back before it writes, and that discards whatever the
        failed sync had **not yet committed** along with it.

        Safe *because* everything pending belongs to a sync that failed. It is
        also required: on Postgres a failed statement aborts the transaction, so
        a flag written into it is silently thrown away by a COMMIT that reports
        success.

        **This is not atomicity, and the boundary is the commit in
        `sync_project_repositories` that ends the reconciliation block.** The
        failure injected here lands at `add_timeline_entry`, before that commit, so
        this sync's links are still pending and go with the rollback. A failure
        *after* it -- `_refresh_open_pr_counts`, `_discover_releases` -- leaves the
        links durably in place and records only the error flag; that case is pinned
        by the test below. Nothing here licenses a retry path that assumes a failed
        sync left the project as it found it.
        """
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("666", "repo-f")]),
            ),
            patch(
                "src.services.github_connect_service.add_timeline_entry",
                side_effect=RuntimeError("timeline write blew up"),
            ),
            _topics_gone(),
        ):
            with pytest.raises(RuntimeError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None
        assert (
            session.exec(
                select(ProjectRepository).where(
                    ProjectRepository.project_id == project.id
                )
            ).all()
            == []
        ), "the failed sync's links must not survive the rollback that records it"

    @pytest.mark.asyncio
    async def test_links_committed_before_the_late_steps_survive_a_later_failure(
        self, session, org, project
    ):
        """The other side of the boundary, stated so nobody has to assume it.

        `sync_project_repositories` commits the reconciled links, *then* refreshes
        open-PR counts and discovers releases. A failure in either of those late
        steps reds the icon but cannot un-attach what is already committed -- the
        recorder's rollback has nothing of this sync's left to discard.

        Pinned deliberately rather than fixed: making the whole sync atomic is a
        larger change than #640. What must not happen is code written against a
        guarantee of atomicity that was never there -- a retry that assumes it
        starts from an empty slate would double-count, and a caller that reads
        "errored" as "nothing was written" would be wrong.
        """
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("999", "repo-i")]),
            ),
            patch.object(
                service, "_refresh_open_pr_counts", new=AsyncMock(return_value=(0, 0))
            ),
            patch.object(
                service,
                "_discover_releases",
                new=AsyncMock(side_effect=RuntimeError("release discovery blew up")),
            ),
            _topics_gone(),
        ):
            with pytest.raises(RuntimeError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None, "the icon still has to red"
        links = session.exec(
            select(ProjectRepository).where(ProjectRepository.project_id == project.id)
        ).all()
        assert [link.repository_id for link in links] == ["999"], (
            "the link was committed before the failing step and stays attached"
        )
        assert links[0].is_active is True

    @pytest.mark.asyncio
    async def test_a_broken_recorder_does_not_mask_the_original_failure(
        self, session, org, project
    ):
        """Reporting a failure must never become the failure the caller sees.

        The recorder issues three statements of its own, and a connection that
        died behind the session (pooler restart, failover) makes any of them raise
        `OperationalError`/`PendingRollbackError`. Escaping, that would *replace*
        the real exception: `routers/projects.py` matches `except ValueError`, so
        the caller would get a 500 carrying a database error instead of a 400.
        """
        service = self._service(session, creds=None)

        with patch.object(
            service,
            "_record_project_sync_error",
            side_effect=RuntimeError("the pooler went away mid-rollback"),
        ):
            with pytest.raises(ValueError) as excinfo:
                await service.sync_project_repositories(org.id, project.id)

        assert "connection" in str(excinfo.value).lower(), (
            "the caller must still see the sync's own failure, not the recorder's"
        )
        assert "pooler" not in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_an_unexpected_failure_reports_nothing_internal(
        self, session, org, project
    ):
        """What is stored is rendered to every member of the org, so a message
        nobody wrote for a reader does not get persisted.

        `IntegrityError` stringifies to the full SQL plus its bound parameters; the
        same class of leak covers `OperationalError` (psycopg2 host/port/user) and
        `TypeError` (which blames GitHub for a bug of ours). The real exception is
        logged instead.
        """
        leaky = IntegrityError(
            "INSERT INTO project_repositories (project_id, repository_id) "
            "VALUES (?, ?)",
            {"project_id": project.id, "repository_id": "777"},
            Exception("UNIQUE constraint failed"),
        )
        assert "INSERT INTO project_repositories" in str(leaky), (
            "premise of this test: this exception type stringifies to its SQL"
        )
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("777", "repo-g")]),
            ),
            patch(
                "src.services.github_connect_service.add_timeline_entry",
                side_effect=leaky,
            ),
            _topics_gone(),
        ):
            with pytest.raises(IntegrityError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None, "the icon still has to red"
        message = project.github_error_message or ""
        assert "INSERT INTO" not in message
        assert project.id not in message
        assert message == _UNEXPECTED_SYNC_ERROR

    @pytest.mark.asyncio
    async def test_a_transport_failure_during_discovery_reports_nothing_internal(
        self, session, org, project
    ):
        """The same guarantee, on the path the test above cannot reach.

        That one injects at `add_timeline_entry`, which runs *after* discovery --
        so it never crosses `discover_project_repositories`' own `except`. That wrap
        caught **everything** and re-raised `ValueError(f"...{e}")`, and a
        `ValueError` is reported verbatim: any failure reaching it became a
        reportable one whatever it was carrying. `github_api` calls httpx directly,
        so a proxy, DNS or TLS failure is not a `GitHubAPIError` and went straight
        through there.

        The exception type is asserted too: relabelling an arbitrary failure as
        `ValueError` also tells `routers/projects.py` to answer 400, i.e. "your
        request was wrong", for something that was never the caller's doing.
        """
        detail = "NOT-A-SECRET-egress-detail-placeholder"
        leaky = httpx.ConnectError(f"connection refused reaching {detail}")
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with patch(
            "src.api.github_api.GitHubAPI.search_organization_repositories",
            new=AsyncMock(side_effect=leaky),
        ):
            with pytest.raises(httpx.ConnectError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None, "the icon still has to red"
        message = project.github_error_message or ""
        assert detail not in message
        assert message == _UNEXPECTED_SYNC_ERROR

    @pytest.mark.asyncio
    async def test_a_value_error_subclass_is_not_reported_verbatim(
        self, session, org, project
    ):
        """Being a `ValueError` is not the same as having been written for a reader.

        `pydantic.ValidationError` inherits from `ValueError` and stringifies to the
        **input value** that failed validation, so a model fed anything sensitive
        reports it; `json.JSONDecodeError` and `UnicodeDecodeError` are `ValueError`s
        describing a payload too. An `isinstance` check trusts all of them.
        """
        payload = "NOT-A-SECRET-input-value-placeholder"
        leaky = _validation_error(payload)
        assert payload in str(leaky), (
            "premise of this test: this exception type stringifies to its input"
        )
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with patch(
            "src.api.github_api.GitHubAPI.search_organization_repositories",
            new=AsyncMock(side_effect=leaky),
        ):
            with pytest.raises(ValidationError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_errored_at is not None, "the icon still has to red"
        message = project.github_error_message or ""
        assert payload not in message
        assert message == _UNEXPECTED_SYNC_ERROR

    @pytest.mark.asyncio
    async def test_a_github_api_error_from_discovery_is_still_reported_verbatim(
        self, session, org, project
    ):
        """Narrowing that wrap must not silence the failures it exists to explain.

        A dead token, a lost org scope and a rate limit all arrive as
        `GitHubAPIError` from the search itself, and those are the messages the
        person pressing Sync can act on -- so discovery still relabels *those* and
        the reader still gets GitHub's own words.
        """
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with patch(
            "src.api.github_api.GitHubAPI.search_organization_repositories",
            new=AsyncMock(side_effect=GitHubAPIError("401 Bad credentials")),
        ):
            with pytest.raises(ValueError, match="Failed to fetch repositories"):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert "401 Bad credentials" in (project.github_error_message or "")

    @pytest.mark.asyncio
    async def test_a_github_api_error_is_reported_verbatim(self, session, org, project):
        """The other half of the classification: `GitHubAPIError` carries GitHub's
        own words, which is exactly what the reader needs to act on -- narrowing it
        to the generic string would send them to the logs for nothing."""
        service = self._service(session, creds={"token": "tok", "github_org": "acme"})

        with (
            patch(
                "src.api.github_api.GitHubAPI.search_organization_repositories",
                new=AsyncMock(return_value=[_raw_repo("888", "repo-h")]),
            ),
            patch(
                "src.services.github_connect_service.add_timeline_entry",
                side_effect=GitHubAPIError("403 API rate limit exceeded"),
            ),
            _topics_gone(),
        ):
            with pytest.raises(GitHubAPIError):
                await service.sync_project_repositories(org.id, project.id)

        session.refresh(project)
        assert project.github_error_message == "403 API rate limit exceeded"
