"""`GET /api/v1/public/impact` — counts for the public front page, and no names.

The route is unauthenticated, so the test that matters most is the one about
what it does *not* say. The rest pin the ways a count like this goes wrong
quietly: a status comparison that guesses the wrong spelling and answers zero,
and a queue counted as work in progress.
"""

from datetime import datetime, timezone
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

import src.routers.public as public_router
from src.api.app import app
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from tests.db_helpers import build_test_engine


@pytest.fixture(autouse=True)
def clear_cache():
    # Module-level and deliberately so; a test that inherits another's numbers
    # passes for the wrong reason.
    public_router._impact_cache = None
    yield
    public_router._impact_cache = None


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
def seeded(db_session):
    """One org, two projects, and a version string both projects use."""
    org = Organization(id=str(uuid4()), name="Org")
    db_session.add(org)

    one = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias="ONE",
        name="One",
        description="x",
    )
    two = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias="TWO",
        name="Two",
        description="x",
    )
    db_session.add(one)
    db_session.add(two)
    db_session.commit()

    # ONE shipped v1.0.0 and is cutting v1.1.0.
    db_session.add(
        Release(
            organization_id=org.id,
            project_id=one.id,
            version="v1.0.0",
            status=ReleaseStatus.RELEASED,
            released_at=datetime.now(timezone.utc),
        )
    )
    db_session.add(
        Release(
            organization_id=org.id,
            project_id=one.id,
            version="v1.1.0",
            status=ReleaseStatus.IN_PROGRESS,
        )
    )
    db_session.commit()

    def ticket(project, status, release):
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                ref_number=int(str(uuid4().int)[:6]),
                summary="t",
                status=status,
                release=release,
            )
        )

    ticket(one, TicketStatus.IN_PROGRESS, None)  # being built
    ticket(one, TicketStatus.IN_REVIEW, "v1.1.0")  # being built
    ticket(one, TicketStatus.TODO, None)  # queued, not being built
    ticket(one, TicketStatus.BACKLOG, None)  # not even queued
    ticket(one, TicketStatus.DONE, "v1.0.0")  # finished
    ticket(two, TicketStatus.IN_PROGRESS, None)  # being built, other project
    ticket(two, TicketStatus.CANCELLED, None)  # never going anywhere
    db_session.commit()
    return org


class TestImpactNumbers:
    def test_counts_projects_releases_and_what_is_being_built(self, client, seeded):
        body = client.get("/api/v1/public/impact").json()
        assert body["projects"] == 2
        # Only the release that actually went out.
        assert body["releases"] == 1
        # In progress and in review, across both projects. Nothing else.
        assert body["features"] == 3

    def test_a_queue_is_not_work_in_progress(self, client, seeded):
        # TODO and BACKLOG are things nobody has started. Counting them as work
        # being built inflates the figure with a wish list, which is the quiet
        # way a number on a front page stops being true.
        assert client.get("/api/v1/public/impact").json()["features"] == 3

    def test_finished_and_cancelled_work_is_not_being_built(self, client, seeded):
        assert client.get("/api/v1/public/impact").json()["features"] == 3

    def test_says_nothing_about_who(self, client, seeded):
        body = client.get("/api/v1/public/impact").json()
        assert set(body) == {"projects", "releases", "features", "counted_at"}
        printed = str(body)
        for secret in ("Org", "ONE", "TWO", "One", "Two", "v1.0.0", "v1.1.0"):
            assert secret not in printed

    def test_needs_no_credential(self, client, seeded):
        # It is the product's front page. A sign-in wall on the number is a
        # number nobody reads.
        assert client.get("/api/v1/public/impact").status_code == 200

    def test_serves_the_cached_answer_rather_than_asking_again(
        self, client, seeded, db_session
    ):
        first = client.get("/api/v1/public/impact").json()

        org_id = seeded.id
        project = Project(
            id=str(uuid4()),
            organization_id=org_id,
            alias="THREE",
            name="Three",
            description="x",
        )
        db_session.add(project)
        db_session.commit()

        assert (
            client.get("/api/v1/public/impact").json()["projects"] == first["projects"]
        )

    def test_answers_503_rather_than_zero_when_it_cannot_count(self, client):
        # "Nothing has shipped" is a statement, and it must never be made by
        # accident on a page that exists to say the opposite.
        with patch.object(
            public_router, "_count_impact", side_effect=RuntimeError("db down")
        ):
            assert client.get("/api/v1/public/impact").status_code == 503

    def test_serves_a_stale_answer_over_no_answer(self, client, seeded):
        client.get("/api/v1/public/impact")
        # Age the cache past its TTL so the route tries the database again.
        counted_at, cached = public_router._impact_cache
        public_router._impact_cache = (
            datetime.fromtimestamp(0, tz=timezone.utc),
            cached,
        )
        with patch.object(
            public_router, "_count_impact", side_effect=RuntimeError("db down")
        ):
            resp = client.get("/api/v1/public/impact")
        assert resp.status_code == 200
        assert resp.json()["projects"] == 2
