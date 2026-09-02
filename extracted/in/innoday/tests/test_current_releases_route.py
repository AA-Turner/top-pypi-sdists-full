"""`GET /organizations/{org}/releases/current` — one row per project, no counts.

The dashboard used to answer this by asking for every release the organization
had and re-deriving `next_release` in TypeScript. These tests pin the two things
that made that wrong: the rule (a `planned` row below the high-water mark is
history, not a plan) and the shape (a project cutting nothing is absent, not
null).
"""

from datetime import datetime, timezone
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.user import User, UserRole
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    return build_test_engine()


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def auth_headers(db_session, org):
    u = User(
        id=str(uuid4()),
        email="dash@example.com",
        full_name="Dash Reader",
        role=UserRole.MEMBER,
        is_platform_member=True,
    )
    db_session.add(u)
    db_session.commit()
    return bearer_for(db_session, u.id)


def make_project(db_session, org, alias):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=alias,
        name=f"Project {alias}",
        description="x",
    )
    db_session.add(p)
    db_session.commit()
    return p


def make_release(db_session, org, project, version, status):
    r = Release(
        organization_id=org.id,
        project_id=project.id,
        version=version,
        status=status,
        released_at=(
            datetime.now(timezone.utc) if status == ReleaseStatus.RELEASED else None
        ),
    )
    db_session.add(r)
    db_session.commit()
    return r


def get(client, org, headers):
    resp = client.get(
        f"/api/v1/organizations/{org.id}/releases/current", headers=headers
    )
    assert resp.status_code == 200, resp.text
    return {row["project_alias"]: row for row in resp.json()}


class TestCurrentReleases:
    def test_one_row_per_project_with_something_upcoming(
        self, client, db_session, org, auth_headers
    ):
        one = make_project(db_session, org, "ONE")
        two = make_project(db_session, org, "TWO")
        make_release(db_session, org, one, "v1.0.0", ReleaseStatus.RELEASED)
        make_release(db_session, org, one, "v1.1.0", ReleaseStatus.IN_PROGRESS)
        make_release(db_session, org, two, "v3.0.0", ReleaseStatus.IN_PROGRESS)

        rows = get(client, org, auth_headers)
        assert rows["ONE"]["version"] == "v1.1.0"
        assert rows["ONE"]["status"] == "in_progress"
        assert rows["TWO"]["version"] == "v3.0.0"

    def test_a_project_cutting_nothing_is_absent_rather_than_null(
        self, client, db_session, org, auth_headers
    ):
        # A null row would have to be filtered by every caller, and the first one
        # to forget renders an empty badge.
        quiet = make_project(db_session, org, "QUIET")
        make_release(db_session, org, quiet, "v1.0.0", ReleaseStatus.RELEASED)

        assert get(client, org, auth_headers) == {}

    def test_a_planned_version_below_what_shipped_is_history_not_a_plan(
        self, client, db_session, org, auth_headers
    ):
        # BPAI accumulates PLANNED rows from board sync -- forty-odd, most of them
        # `v0.1.x-beta` from a repo on a different versioning line. Taking the
        # lowest upcoming version outright picked one of those as the next launch
        # for a project that had already shipped v1.9.0.
        p = make_project(db_session, org, "DRIFT")
        make_release(db_session, org, p, "v1.9.0", ReleaseStatus.RELEASED)
        make_release(db_session, org, p, "v0.1.1", ReleaseStatus.PLANNED)
        make_release(db_session, org, p, "v2.0.0", ReleaseStatus.PLANNED)

        assert get(client, org, auth_headers)["DRIFT"]["version"] == "v2.0.0"

    def test_a_planned_release_counts_when_nothing_is_in_progress(
        self, client, db_session, org, auth_headers
    ):
        # The project page shows this version, so the dashboard must too --
        # disagreeing about it is the bug this route was added to end.
        p = make_project(db_session, org, "NEXT")
        make_release(db_session, org, p, "v1.0.0", ReleaseStatus.RELEASED)
        make_release(db_session, org, p, "v1.1.0", ReleaseStatus.PLANNED)

        row = get(client, org, auth_headers)["NEXT"]
        assert row["version"] == "v1.1.0"
        assert row["status"] == "planned"

    def test_in_progress_is_preferred_over_a_lower_planned_version(
        self, client, db_session, org, auth_headers
    ):
        p = make_project(db_session, org, "BOTH")
        make_release(db_session, org, p, "v2.0.0", ReleaseStatus.PLANNED)
        make_release(db_session, org, p, "v2.1.0", ReleaseStatus.IN_PROGRESS)

        assert get(client, org, auth_headers)["BOTH"]["version"] == "v2.1.0"

    def test_another_organizations_releases_are_not_reported(
        self, client, db_session, org, auth_headers
    ):
        other = Organization(id=str(uuid4()), name="Someone Else")
        db_session.add(other)
        db_session.commit()
        theirs = make_project(db_session, other, "THEIRS")
        make_release(db_session, org, theirs, "v9.9.9", ReleaseStatus.IN_PROGRESS)

        # The row is scoped by organization even though the project is not ours.
        rows = get(client, other, auth_headers)
        assert rows == {}

    def test_the_route_is_not_read_as_a_release_id(
        self, client, db_session, org, auth_headers
    ):
        # `/releases/{release_id}` would capture "current" if it were registered
        # first, and the failure would be a 404 that looks like missing data.
        make_project(db_session, org, "ORDER")
        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases/current", headers=auth_headers
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
