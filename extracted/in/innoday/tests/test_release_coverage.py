"""A release that covers less than the last one has to say so.

A BPAI release covered six repositories instead of seven, dropped thirteen
merged pull requests, and reported the smaller number in silence — a sync had
deactivated one project link seven minutes earlier. Every figure in that report
was internally consistent, which is why nothing caught it.

The repository set is read live from the project links, so once a release ships
nothing remembers what it contained. `repo_names` is that memory, written at the
moment of shipping and never rewritten.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.services.release_content import ReleaseContentService
from tests.db_helpers import build_test_engine

SHIPPED = datetime(2026, 8, 12, tzinfo=timezone.utc)


@pytest.fixture
def world():
    engine = build_test_engine()
    with Session(engine) as session:
        org = Organization(id=str(uuid4()), name="Acme", alias=f"a{str(uuid4())[:5]}")
        session.add(org)
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPAI",
            name="Bright Power AI",
            description="d",
        )
        session.add(project)
        session.commit()
        yield session, org, project


def _released(session, org, project, version, repo_names):
    session.add(
        Release(
            organization_id=org.id,
            project_id=project.id,
            version=version,
            status=ReleaseStatus.RELEASED,
            released_at=SHIPPED,
            repo_names=repo_names,
        )
    )
    session.commit()


def _warn(session, org, project, covering, previous="v1.10.0"):
    return ReleaseContentService(session).coverage_warning(
        project_id=project.id,
        organization_id=org.id,
        covering=covering,
        previous_version=previous,
    )


class TestItNamesWhatWentMissing:
    def test_a_smaller_release_warns(self, world):
        session, org, project = world
        _released(session, org, project, "v1.10.0", ["a", "b", "bps-ui-demo"])
        warning = _warn(session, org, project, ["a", "b"])
        assert warning is not None
        assert "bps-ui-demo" in warning

    def test_it_names_them_rather_than_counting_them(self, world):
        """A number says the release is short; a name says where to look."""
        session, org, project = world
        _released(session, org, project, "v1.10.0", ["a", "b", "c"])
        warning = _warn(session, org, project, ["a"])
        assert "b, c" in warning

    def test_it_says_what_to_check(self, world):
        session, org, project = world
        _released(session, org, project, "v1.10.0", ["a", "b"])
        assert "repository links" in _warn(session, org, project, ["a"])


class TestItStaysQuietWhenItShould:
    def test_the_same_set_is_silent(self, world):
        session, org, project = world
        _released(session, org, project, "v1.10.0", ["a", "b"])
        assert _warn(session, org, project, ["b", "a"]) is None

    def test_growing_is_not_a_warning(self, world):
        """A repository joining a project is ordinary. Warning about it would
        train people to ignore the warning that matters."""
        session, org, project = world
        _released(session, org, project, "v1.10.0", ["a"])
        assert _warn(session, org, project, ["a", "b"]) is None

    def test_a_release_predating_the_column_is_silent(self, world):
        """Every release shipped before `repo_names` existed has none.

        Reconstructing it from today's links would manufacture the agreement
        this check exists to test.
        """
        session, org, project = world
        _released(session, org, project, "v1.10.0", None)
        assert _warn(session, org, project, ["a"]) is None

    def test_no_previous_version_is_silent(self, world):
        session, org, project = world
        assert _warn(session, org, project, ["a"], previous=None) is None


class TestShippingRecordsWhatItCovered:
    """The write half. Without it the warning has nothing to compare against.

    A first pass tested only the comparison, and deleting the write left every
    one of those tests green — the check was intact and permanently blind.
    """

    def _repo(self, session, org, project, name, archived=False):
        from uuid import uuid4 as u

        from src.domain.project import ProjectRepository, RepositoryLayer
        from src.domain.repository import Repository

        repo = Repository(
            id=str(u()),
            organization_id=org.id,
            name=name,
            full_name=f"acme/{name}",
            url=f"https://github.com/acme/{name}",
            archived=archived,
        )
        session.add(repo)
        session.add(
            ProjectRepository(
                id=str(u()),
                project_id=project.id,
                repository_id=repo.id,
                layer=RepositoryLayer.UNASSIGNED,
            )
        )
        session.commit()

    def _ship(self, session, org, project, version="v1.11.0"):
        import asyncio
        from uuid import uuid4 as u

        from src.domain.user import User
        from src.routers.releases import ReleaseUpdate, update_release

        actor = User(id=str(u()), email=f"{u()}@x.com", full_name="A Person")
        session.add(actor)
        session.commit()

        release = Release(
            organization_id=org.id,
            project_id=project.id,
            version=version,
            status=ReleaseStatus.IN_PROGRESS,
        )
        session.add(release)
        session.commit()
        session.refresh(release)
        asyncio.run(
            update_release(
                org_id=org.id,
                release_id=release.id,
                body=ReleaseUpdate(status=ReleaseStatus.RELEASED),
                current_user=actor,
                session=session,
                _org=org,
            )
        )
        session.refresh(release)
        return release

    def test_marking_it_released_records_the_repositories(self, world):
        session, org, project = world
        self._repo(session, org, project, "bps-api")
        self._repo(session, org, project, "bps-ui-v2")
        assert self._ship(session, org, project).repo_names == ["bps-api", "bps-ui-v2"]

    def test_an_archived_repository_is_not_recorded(self, world):
        """It is not tagged, so recording it would report a shrink the moment
        somebody archives one."""
        session, org, project = world
        self._repo(session, org, project, "bps-api")
        self._repo(session, org, project, "old-thing", archived=True)
        assert self._ship(session, org, project).repo_names == ["bps-api"]

    def test_the_record_survives_the_round_trip(self, world):
        """A JSON column that does not read back is the same as no column."""
        session, org, project = world
        self._repo(session, org, project, "bps-api")
        release = self._ship(session, org, project)
        session.expire_all()
        stored = session.get(Release, release.id)
        assert stored.repo_names == ["bps-api"]
