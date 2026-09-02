"""Backend half of the workflow homepage (#626).

Covers the five scrum routes, the promoted `.../tickets/unreleased` endpoint,
the corrected `get_project_overview` counts, and the membership column the
migration adds.

The overview tests are the ones worth reading first: `test_counts_are_not_all_zero`
and its siblings fail against the code as it stood, because that code compared
`Ticket.status` against `"IN_PROGRESS"`/`"DONE"`/`"OPEN"` while `TicketStatus`'s
values are lowercase and two of those names do not exist at all. Every comparison
was False, so three of the four counts were permanently 0 while `total` looked
right -- which is exactly why nobody noticed.
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.scrum import Scrum, ScrumTicketVisit
from src.domain.summary import GeneratedBy, Summary, SummaryType
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User, UserRole
from src.services.project_service import ProjectService
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
    o = Organization(id=str(uuid4()), name="Scrum Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


def _make_project(session, org, alias=None) -> Project:
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=(alias or f"S{str(uuid4())[:6]}").upper(),
        name=f"Project {alias or 'X'}",
        description="A project",
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@pytest.fixture
def project(db_session, org):
    return _make_project(db_session, org, "SCR")


@pytest.fixture
def user(db_session):
    u = User(
        id=str(uuid4()),
        email=f"{uuid4()}@example.com",
        full_name="Scrum Runner",
        role=UserRole.MEMBER,
        is_platform_member=True,  # bypass membership checks
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def auth_headers(user, db_session):
    return bearer_for(db_session, user.id)


def _make_ticket(
    session, org, project, *, status=TicketStatus.TODO, **kwargs
) -> Ticket:
    t = Ticket(
        summary=kwargs.pop("summary", "A ticket"),
        organization_id=org.id,
        project_id=project.id,
        status=status,
        **kwargs,
    )
    session.add(t)
    session.commit()
    session.refresh(t)
    return t


def _make_summary(session, org, project, *, created_at=None) -> Summary:
    s = Summary(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        window_spec="1d",
        summary_type=SummaryType.SCRUM,
        body_markdown="Yesterday we shipped.",
        motivational_quote="Onward.",
        generated_by=GeneratedBy.AGENT,
        created_at=created_at or datetime.utcnow(),
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


def _start(client, org, project, headers, **body):
    return client.post(
        f"/api/v1/organizations/{org.id}/projects/{project.id}/scrums",
        json=body,
        headers=headers,
    )


# ---------------------------------------------------------------------------
# POST .../projects/{id}/scrums -- start
# ---------------------------------------------------------------------------


class TestStartScrum:
    def test_stamps_runner_and_start_time(
        self, client, org, project, auth_headers, user
    ):
        resp = _start(client, org, project, auth_headers)
        assert resp.status_code == 201, resp.text

        body = resp.json()
        assert body["run_by_user_id"] == user.id
        assert body["project_id"] == project.id
        assert body["organization_id"] == org.id
        assert body["started_at"] is not None
        assert body["ended_at"] is None
        assert body["visit_count"] == 0

    def test_links_todays_scrum_summary(
        self, client, org, project, auth_headers, db_session
    ):
        summary = _make_summary(db_session, org, project)

        body = _start(client, org, project, auth_headers).json()
        assert body["initial_summary_id"] == summary.id

    def test_no_summary_today_is_not_an_error(
        self, client, org, project, auth_headers, db_session
    ):
        """A scrum can be run before anyone has generated a summary."""
        # Yesterday's summary is real, and deliberately not today's.
        _make_summary(
            db_session, org, project, created_at=datetime.utcnow() - timedelta(days=2)
        )

        resp = _start(client, org, project, auth_headers)
        assert resp.status_code == 201
        assert resp.json()["initial_summary_id"] is None

    def test_another_projects_summary_is_not_linked(
        self, client, org, project, auth_headers, db_session
    ):
        other = _make_project(db_session, org, "OTH")
        _make_summary(db_session, org, other)

        assert (
            _start(client, org, project, auth_headers).json()["initial_summary_id"]
            is None
        )

    def test_explicit_started_at_with_offset_is_converted_not_stripped(
        self, client, org, project, auth_headers
    ):
        """`parse_iso_naive` converts to UTC. Stripping the offset would store 09:00."""
        body = _start(
            client, org, project, auth_headers, started_at="2026-08-15T09:00:00+02:00"
        ).json()
        assert body["started_at"].startswith("2026-08-15T07:00:00")

    def test_unknown_project_404s(self, client, org, auth_headers):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/projects/{uuid4()}/scrums",
            json={},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_opening_twice_returns_the_run_that_is_already_open(
        self, client, org, project, auth_headers, db_session
    ):
        """**Opening is idempotent.** A dropped response must not split a meeting.

        The open commits, the answer is lost in transit, the client retries --
        and a second row meant every later visit landed on a scrum the first half
        of the walk was not in. The finish path has refused its own double-submit
        from the start; this is the same guarantee at the other end.
        """
        first = _start(client, org, project, auth_headers).json()["id"]
        again = _start(client, org, project, auth_headers)
        assert again.status_code == 201, again.text
        assert again.json()["id"] == first

        assert (
            len(
                db_session.exec(
                    select(Scrum).where(Scrum.project_id == project.id)
                ).all()
            )
            == 1
        )

        # Closed, and the next walk is a new meeting rather than this one again.
        client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{first}",
            json={"ended_at": "2026-08-15T10:30:00Z"},
            headers=auth_headers,
        )
        assert _start(client, org, project, auth_headers).json()["id"] != first

    def test_an_explicit_started_at_still_opens_its_own_run(
        self, client, org, project, auth_headers
    ):
        """A replayed run asserts *which* run it is, so it is never folded into another.

        `started_at` exists for a client replaying a walk it recorded offline.
        Attaching that assertion to whatever row happens to be open would be the
        same quiet substitution `open_scrum` refuses when the timestamp will not
        parse.
        """
        live = _start(client, org, project, auth_headers).json()["id"]
        replayed = _start(
            client, org, project, auth_headers, started_at="2026-08-01T09:00:00Z"
        )
        assert replayed.status_code == 201, replayed.text
        assert replayed.json()["id"] != live

    def test_another_person_walking_the_same_board_gets_their_own_run(
        self, client, org, project, auth_headers, db_session
    ):
        """Reuse is per runner. Two people's stand-ups are two meetings.

        `require_runner` already refuses cross-writes, so folding a second
        person into somebody else's open scrum would hand them a row every one
        of their own writes is then rejected against.
        """
        mine = _start(client, org, project, auth_headers).json()["id"]

        other = User(
            id=str(uuid4()),
            email=f"{uuid4()}@example.com",
            full_name="Somebody Else",
            role=UserRole.MEMBER,
            is_platform_member=True,
        )
        db_session.add(other)
        db_session.commit()
        theirs = _start(client, org, project, bearer_for(db_session, other.id))
        assert theirs.status_code == 201, theirs.text
        assert theirs.json()["id"] != mine

    def test_requires_authentication(self, client, org, project):
        assert _start(client, org, project, {}).status_code == 401


# ---------------------------------------------------------------------------
# POST .../scrums/{id}/visits -- one stop at a time
# ---------------------------------------------------------------------------


class TestRecordVisit:
    def test_records_one_visit(self, client, org, project, auth_headers, db_session):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        ticket = _make_ticket(db_session, org, project, status=TicketStatus.IN_REVIEW)

        resp = client.post(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
            json={
                "ticket_id": ticket.id,
                "position": 0,
                "seconds": 47,
                "status_at_visit": TicketStatus.IN_REVIEW.value,
                "comment": "Waiting on review.",
                "moved_to": TicketStatus.DONE.value,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201, resp.text

        body = resp.json()
        assert body["ticket_id"] == ticket.id
        assert body["seconds"] == 47
        assert body["status_at_visit"] == "in review"
        assert body["moved_to"] == "done"

        stored = db_session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).all()
        assert len(stored) == 1

    def test_visits_accumulate_one_call_at_a_time(
        self, client, org, project, auth_headers, db_session
    ):
        """The walk is recorded as it happens, so an abandoned run keeps its stops."""
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        for i in range(3):
            ticket = _make_ticket(db_session, org, project, summary=f"T{i}")
            client.post(
                f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
                json={
                    "ticket_id": ticket.id,
                    "position": i,
                    "seconds": 10,
                    "status_at_visit": "todo",
                },
                headers=auth_headers,
            )

        detail = client.get(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}", headers=auth_headers
        ).json()
        # Never finished -- and the three stops are still there.
        assert detail["ended_at"] is None
        assert detail["visit_count"] == 3

    def test_ticket_from_another_project_404s(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        other = _make_project(db_session, org, "OTH")
        foreign = _make_ticket(db_session, org, other)

        resp = client.post(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
            json={
                "ticket_id": foreign.id,
                "position": 0,
                "seconds": 5,
                "status_at_visit": "todo",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_unknown_scrum_404s(self, client, org, project, auth_headers, db_session):
        ticket = _make_ticket(db_session, org, project)
        resp = client.post(
            f"/api/v1/organizations/{org.id}/scrums/{uuid4()}/visits",
            json={
                "ticket_id": ticket.id,
                "position": 0,
                "seconds": 5,
                "status_at_visit": "todo",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PATCH .../scrums/{id} -- wrap up
# ---------------------------------------------------------------------------


class TestFinishScrum:
    def test_writes_the_wrap_up_fields(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        summary = _make_summary(db_session, org, project)

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={
                "ended_at": "2026-08-15T10:30:00Z",
                "total_seconds": 900,
                "transcript_url": "https://example.com/t/1",
                "updated_summary_id": summary.id,
                "lingering_count": 2,
                "notes_markdown": "Two tickets have not moved in a week.",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 200, resp.text

        body = resp.json()
        assert body["ended_at"].startswith("2026-08-15T10:30:00")
        assert body["total_seconds"] == 900
        assert body["transcript_url"] == "https://example.com/t/1"
        assert body["updated_summary_id"] == summary.id
        assert body["lingering_count"] == 2
        assert body["notes_markdown"].startswith("Two tickets")

    def test_omitted_fields_are_left_alone(self, client, org, project, auth_headers):
        """A second PATCH that only adds notes must not blank the transcript."""
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"transcript_url": "https://example.com/t/2", "total_seconds": 60},
            headers=auth_headers,
        )

        body = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"notes_markdown": "Added later."},
            headers=auth_headers,
        ).json()
        assert body["transcript_url"] == "https://example.com/t/2"
        assert body["total_seconds"] == 60
        assert body["notes_markdown"] == "Added later."

    def test_ended_at_offset_is_converted_not_stripped(
        self, client, org, project, auth_headers
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        body = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"ended_at": "2026-08-15T11:00:00+03:00"},
            headers=auth_headers,
        ).json()
        assert body["ended_at"].startswith("2026-08-15T08:00:00")

    def test_a_malformed_ended_at_is_422_not_a_silent_none(
        self, client, org, project, auth_headers, db_session
    ):
        """**NULL is not a neutral outcome on this column.**

        `parse_iso_naive` never raises -- it reads third-party sync payloads,
        where one junk field must not take down a sync -- so a body of
        ``{"ended_at": "15/08/2026 10:30"}`` used to answer 200 with the column
        left NULL. `Scrum.ended_at` documents NULL as how an *abandoned* run is
        told from a finished one, so a client date-format bug would have marked
        every completed scrum abandoned, silently and in bulk.
        """
        scrum_id = _start(client, org, project, auth_headers).json()["id"]

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"ended_at": "15/08/2026 10:30", "total_seconds": 900},
            headers=auth_headers,
        )
        assert resp.status_code == 422, resp.text

        db_session.expire_all()
        row = db_session.get(Scrum, scrum_id)
        assert row.ended_at is None
        # Refused whole: the valid field beside it is not written either.
        assert row.total_seconds is None

    def test_a_transcript_url_is_validated_on_write(
        self, client, org, project, auth_headers, db_session
    ):
        """A stored `javascript:` URL is a payload for every later reader.

        There is no CSP on this app, and the renderer refusing to make it
        clickable is one consumer defending itself -- not the value being
        rejected. It round-tripped through this endpoint before.
        """
        scrum_id = _start(client, org, project, auth_headers).json()["id"]

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"transcript_url": "javascript:alert(1)"},
            headers=auth_headers,
        )
        assert resp.status_code == 422, resp.text

        db_session.expire_all()
        assert db_session.get(Scrum, scrum_id).transcript_url is None

        ok = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"transcript_url": "https://example.com/rec"},
            headers=auth_headers,
        )
        assert ok.status_code == 200
        assert ok.json()["transcript_url"] == "https://example.com/rec"

    def test_a_summary_from_another_org_cannot_be_linked(
        self, client, org, project, auth_headers, db_session
    ):
        """`updated_summary_id` is checked the way `record_visit` checks a ticket.

        It was `setattr` with no ownership check at all, so a scrum in one org
        accepted a `Summary.id` belonging to another and linked the two.
        """
        scrum_id = _start(client, org, project, auth_headers).json()["id"]

        elsewhere = Organization(id=str(uuid4()), name="Elsewhere")
        db_session.add(elsewhere)
        db_session.commit()
        stranger_project = _make_project(db_session, elsewhere, "ELS")
        stranger_summary = _make_summary(db_session, elsewhere, stranger_project)

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"updated_summary_id": stranger_summary.id},
            headers=auth_headers,
        )
        assert resp.status_code == 404, resp.text

        db_session.expire_all()
        assert db_session.get(Scrum, scrum_id).updated_summary_id is None

    def test_someone_else_cannot_write_your_scrum(
        self, client, org, project, auth_headers, db_session
    ):
        """Whose row, not what role.

        The MEMBER gate on these routes is about *what* may be written and stays.
        This is about whose: a second person, or a stale tab, would otherwise
        blank the notes and transcript of a meeting somebody else ran.
        """
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"notes_markdown": "the real minutes"},
            headers=auth_headers,
        )

        other = User(
            id=str(uuid4()),
            email=f"{uuid4()}@example.com",
            full_name="Somebody Else",
            role=UserRole.MEMBER,
            is_platform_member=True,
        )
        db_session.add(other)
        db_session.commit()
        other_headers = bearer_for(db_session, other.id)

        ticket = _make_ticket(db_session, org, project, status=TicketStatus.IN_REVIEW)
        visit = client.post(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
            json={
                "ticket_id": ticket.id,
                "position": 0,
                "seconds": 5,
                "status_at_visit": "in review",
            },
            headers=other_headers,
        )
        assert visit.status_code == 403, visit.text

        wrap = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"notes_markdown": ""},
            headers=other_headers,
        )
        assert wrap.status_code == 403, wrap.text

        db_session.expire_all()
        assert db_session.get(Scrum, scrum_id).notes_markdown == "the real minutes"

    def test_a_closed_scrum_refuses_a_second_close(
        self, client, org, project, auth_headers, db_session
    ):
        """Closing is once. A stale tab must not rewrite minutes already final."""
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        first = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"ended_at": "2026-08-15T10:30:00Z", "notes_markdown": "final"},
            headers=auth_headers,
        )
        assert first.status_code == 200

        again = client.patch(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}",
            json={"ended_at": "2026-08-15T18:00:00Z", "notes_markdown": ""},
            headers=auth_headers,
        )
        assert again.status_code == 409, again.text

        db_session.expire_all()
        row = db_session.get(Scrum, scrum_id)
        assert row.notes_markdown == "final"
        assert row.ended_at.hour == 10

    def test_scrum_from_another_org_404s(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        other_org = Organization(id=str(uuid4()), name="Elsewhere")
        db_session.add(other_org)
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{other_org.id}/scrums/{scrum_id}",
            json={"total_seconds": 1},
            headers=auth_headers,
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# The two surfaces, on identical bytes
# ---------------------------------------------------------------------------


class TestBothSurfacesAgree:
    """**`/api/v1` and `/ui` must refuse the same body.**

    `scrum_service` exists to be the single authority on what a scrum write may
    contain, because the ``/ui`` routes have no model in front of them at all.
    The models here undercut it: they validated *first*, and lax pydantic
    coerces -- so ``seconds: true`` became ``1`` and was stored as a stop that
    lasted a second, while the byte-identical body on ``/ui`` was refused with
    the service's own words. ``"5"`` and ``5.0`` went the same way, and
    ``ge=0``/``max_length`` were a second copy of limits the service already
    holds.

    The models are now strict and unconstrained: nothing is coerced, nothing is
    re-stated, and the service decides. The ``/ui`` twin of this class is
    `tests/test_webui_pages.py::test_the_two_surfaces_refuse_the_same_scrum_body`
    -- the pair is the assertion; either alone proves only that one surface has
    an opinion.
    """

    def _visit(self, client, org, scrum_id, ticket, headers, **overrides):
        body = {
            "ticket_id": ticket.id,
            "position": 0,
            "seconds": 5,
            "status_at_visit": "in review",
        }
        body.update(overrides)
        return client.post(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
            json=body,
            headers=headers,
        )

    def test_a_bool_is_not_a_number_of_seconds(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        ticket = _make_ticket(db_session, org, project, status=TicketStatus.IN_REVIEW)

        resp = self._visit(client, org, scrum_id, ticket, auth_headers, seconds=True)
        assert resp.status_code == 422, resp.text
        # Nothing was written -- this used to be a 201 storing `seconds = 1`.
        assert (
            db_session.exec(
                select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
            ).all()
            == []
        )

    def test_a_numeric_string_is_not_a_number(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        ticket = _make_ticket(db_session, org, project, status=TicketStatus.IN_REVIEW)
        assert (
            self._visit(
                client, org, scrum_id, ticket, auth_headers, seconds="5"
            ).status_code
            == 422
        )

    def test_the_service_still_refuses_what_the_constraints_used_to(
        self, client, org, project, auth_headers, db_session
    ):
        """The `ge=0`/`max_length` removals cost nothing: the service holds them."""
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        ticket = _make_ticket(db_session, org, project, status=TicketStatus.IN_REVIEW)

        assert (
            self._visit(
                client, org, scrum_id, ticket, auth_headers, position=-1
            ).status_code
            == 422
        )
        assert (
            self._visit(
                client, org, scrum_id, ticket, auth_headers, seconds=-1
            ).status_code
            == 422
        )
        assert (
            self._visit(
                client,
                org,
                scrum_id,
                ticket,
                auth_headers,
                status_at_visit="x" * 51,
            ).status_code
            == 422
        )
        assert (
            self._visit(
                client, org, scrum_id, ticket, auth_headers, moved_to="x" * 51
            ).status_code
            == 422
        )

    def test_the_wrap_up_refuses_the_same_values(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        url = f"/api/v1/organizations/{org.id}/scrums/{scrum_id}"

        for body in (
            {"total_seconds": True},
            {"total_seconds": -1},
            {"lingering_count": -1},
            {"transcript_url": "https://e.com/" + "x" * 1000},
        ):
            assert (
                client.patch(url, json=body, headers=auth_headers).status_code == 422
            ), body

        db_session.expire_all()
        assert db_session.get(Scrum, scrum_id).ended_at is None


# ---------------------------------------------------------------------------
# GET list + detail
# ---------------------------------------------------------------------------


class TestReadScrums:
    def test_list_is_most_recent_first_and_project_scoped(
        self, client, org, project, auth_headers, db_session
    ):
        older = _start(
            client, org, project, auth_headers, started_at="2026-08-01T09:00:00Z"
        ).json()
        newer = _start(
            client, org, project, auth_headers, started_at="2026-08-10T09:00:00Z"
        ).json()

        other = _make_project(db_session, org, "OTH")
        _start(client, org, other, auth_headers)

        rows = client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.id}/scrums",
            headers=auth_headers,
        ).json()
        assert [r["id"] for r in rows] == [newer["id"], older["id"]]

    def test_detail_nests_visits_in_walk_order(
        self, client, org, project, auth_headers, db_session
    ):
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        tickets = [
            _make_ticket(db_session, org, project, summary=f"T{i}") for i in range(3)
        ]

        # Posted out of order on purpose -- `position` is what the walk meant.
        for pos in (2, 0, 1):
            client.post(
                f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
                json={
                    "ticket_id": tickets[pos].id,
                    "position": pos,
                    "seconds": pos * 10,
                    "status_at_visit": "todo",
                },
                headers=auth_headers,
            )

        detail = client.get(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}", headers=auth_headers
        ).json()
        assert [v["position"] for v in detail["visits"]] == [0, 1, 2]
        assert [v["ticket_id"] for v in detail["visits"]] == [t.id for t in tickets]
        assert detail["visit_count"] == 3

    def test_detail_does_not_serve_a_withdrawn_pick(
        self, client, org, project, auth_headers, db_session
    ):
        """**The fourth reader of `withdrawn_at`, in the router that never changed.**

        A personal update's withdrawn pick keeps its row -- it is the only record
        of whether the board ever got that ticket's comment. That state was added
        for `/ui`, and the readers updated alongside it were the three in the
        files that change was already touching. This one was not, so it served
        withdrawn picks *and* their comment text while `visit_count` in the
        **same payload** excluded them: `visits: 2, visit_count: 1`. A response
        that contradicts itself is worse than either answer alone, and
        `VisitResponse` carries no `withdrawn_at`, so a consumer could not have
        filtered it either.

        Written here rather than beside the `/ui` tests on purpose: this is the
        API's contract, and the defect was precisely that the API was reasoned
        about from another surface's diff.
        """
        scrum_id = _start(client, org, project, auth_headers).json()["id"]
        kept = _make_ticket(db_session, org, project, summary="kept")
        gone = _make_ticket(db_session, org, project, summary="taken back")

        for position, ticket in ((0, kept), (1, gone)):
            client.post(
                f"/api/v1/organizations/{org.id}/scrums/{scrum_id}/visits",
                json={
                    "ticket_id": ticket.id,
                    "position": position,
                    "seconds": 5,
                    "status_at_visit": "todo",
                    "comment": "a note the author took back"
                    if ticket is gone
                    else "kept note",
                },
                headers=auth_headers,
            )

        # Withdraw the second one the way `replace_picks` does.
        with Session(db_session.get_bind()) as session:
            visit = session.exec(
                select(ScrumTicketVisit).where(
                    ScrumTicketVisit.scrum_id == scrum_id,
                    ScrumTicketVisit.ticket_id == gone.id,
                )
            ).one()
            visit.withdrawn_at = datetime.utcnow()
            visit.moved_to = None
            session.add(visit)
            session.commit()

        detail = client.get(
            f"/api/v1/organizations/{org.id}/scrums/{scrum_id}", headers=auth_headers
        )
        assert detail.status_code == 200, detail.text
        body = detail.json()

        assert [v["ticket_id"] for v in body["visits"]] == [kept.id], (
            "the API served a withdrawn pick"
        )
        # The two halves of one payload have to agree with each other.
        assert body["visit_count"] == len(body["visits"]) == 1
        assert "a note the author took back" not in detail.text, (
            "a withdrawn pick's comment text was served as part of the record"
        )

    def test_detail_of_unknown_scrum_404s(self, client, org, auth_headers):
        resp = client.get(
            f"/api/v1/organizations/{org.id}/scrums/{uuid4()}", headers=auth_headers
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET .../projects/{id}/tickets/unreleased
# ---------------------------------------------------------------------------


class TestUnreleasedTickets:
    def _get(self, client, org, project, headers):
        return client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.id}/tickets/unreleased",
            headers=headers,
        )

    def test_includes_done_with_null_and_empty_release(
        self, client, org, project, auth_headers, db_session
    ):
        """Board sync writes `''`, not NULL, when a ticket carries no version."""
        null_release = _make_ticket(
            db_session,
            org,
            project,
            status=TicketStatus.DONE,
            summary="null",
            release=None,
        )
        empty_release = _make_ticket(
            db_session,
            org,
            project,
            status=TicketStatus.DONE,
            summary="empty",
            release="",
        )

        ids = {t["id"] for t in self._get(client, org, project, auth_headers).json()}
        assert ids == {null_release.id, empty_release.id}

    def test_excludes_released_unfinished_deleted_and_other_projects(
        self, client, org, project, auth_headers, db_session
    ):
        keep = _make_ticket(
            db_session, org, project, status=TicketStatus.DONE, summary="keep"
        )
        _make_ticket(
            db_session,
            org,
            project,
            status=TicketStatus.DONE,
            summary="shipped",
            release="v1.2.0",
        )
        _make_ticket(
            db_session, org, project, status=TicketStatus.IN_PROGRESS, summary="wip"
        )
        # CANCELLED never shipped, so it is not a release-note candidate.
        _make_ticket(
            db_session, org, project, status=TicketStatus.CANCELLED, summary="dropped"
        )
        _make_ticket(
            db_session,
            org,
            project,
            status=TicketStatus.DONE,
            summary="deleted",
            deleted_at=datetime.utcnow(),
        )
        other = _make_project(db_session, org, "OTH")
        _make_ticket(
            db_session, org, other, status=TicketStatus.DONE, summary="elsewhere"
        )

        ids = {t["id"] for t in self._get(client, org, project, auth_headers).json()}
        assert ids == {keep.id}

    def test_project_in_another_org_is_403(self, client, org, auth_headers, db_session):
        other_org = Organization(id=str(uuid4()), name="Elsewhere")
        db_session.add(other_org)
        db_session.commit()
        foreign = _make_project(db_session, other_org, "FGN")

        resp = client.get(
            f"/api/v1/organizations/{org.id}/projects/{foreign.id}/tickets/unreleased",
            headers=auth_headers,
        )
        assert resp.status_code == 403

    def test_the_project_may_be_named_by_alias_like_every_scrum_route(
        self, client, org, project, auth_headers, db_session
    ):
        """`resolve_project`, not `session.get` -- so an alias is a valid spelling.

        Every scrum route beside this one accepts a UUID, an alias or a name.
        This one took the UUID alone, so ``.../projects/pf/tickets/unreleased``
        404d while ``.../projects/pf/scrums`` worked -- a difference nothing in
        the URLs could have predicted.
        """
        keep = _make_ticket(
            db_session, org, project, status=TicketStatus.DONE, summary="keep"
        )
        resp = client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.alias}/tickets/unreleased",
            headers=auth_headers,
        )
        assert resp.status_code == 200, resp.text
        assert {t["id"] for t in resp.json()} == {keep.id}

    def test_route_is_not_shadowed_by_a_ticket_id_route(
        self, client, org, project, auth_headers
    ):
        """`unreleased` is a literal segment, not a ticket id -- so this is a 200,

        not a 422 from a route expecting an integer id.
        """
        assert self._get(client, org, project, auth_headers).status_code == 200


# ---------------------------------------------------------------------------
# get_project_overview -- the counts that were always zero
# ---------------------------------------------------------------------------


class TestProjectOverviewCounts:
    """Regression tests for the uppercase/lowercase status comparison.

    Each of these fails against the previous implementation: it compared
    `Ticket.status` (values `"todo"`, `"in progress"`, `"done"`) against
    `"OPEN"`/`"TODO"`/`"IN_PROGRESS"`/`"DONE"`/`"COMPLETED"`/`"CLOSED"`, so the
    only bucket that could ever be non-zero was `total`.
    """

    async def _overview(self, db_session, project):
        return await ProjectService(db_session).get_project_overview(project.id)

    async def test_counts_are_not_all_zero(self, db_session, org, project):
        _make_ticket(db_session, org, project, status=TicketStatus.TODO)
        _make_ticket(db_session, org, project, status=TicketStatus.BACKLOG)
        _make_ticket(db_session, org, project, status=TicketStatus.IN_PROGRESS)
        _make_ticket(db_session, org, project, status=TicketStatus.IN_REVIEW)
        _make_ticket(db_session, org, project, status=TicketStatus.DONE)

        stats = (await self._overview(db_session, project))["tickets"]
        assert stats["total"] == 5
        assert stats["open"] == 2  # todo + backlog
        assert stats["in_progress"] == 2  # in progress + in review
        assert stats["completed"] == 1

    async def test_boardless_project_still_reports_counts(
        self, db_session, org, project
    ):
        """No board registered. The counts used to be `{}` -- absent, not zero."""
        _make_ticket(db_session, org, project, status=TicketStatus.DONE)

        overview = await self._overview(db_session, project)
        assert overview["board"] is None
        assert overview["tickets"]["completed"] == 1

    async def test_scoped_by_project_not_by_board(self, db_session, org, project):
        """A ticket created in InnoDay carries no `board_registration_id`."""
        _make_ticket(db_session, org, project, status=TicketStatus.DONE)
        other = _make_project(db_session, org, "OTH")
        _make_ticket(db_session, org, other, status=TicketStatus.DONE)

        assert (await self._overview(db_session, project))["tickets"]["total"] == 1

    async def test_deleted_tickets_are_excluded(self, db_session, org, project):
        _make_ticket(db_session, org, project, status=TicketStatus.DONE)
        _make_ticket(
            db_session,
            org,
            project,
            status=TicketStatus.DONE,
            deleted_at=datetime.utcnow(),
        )

        assert (await self._overview(db_session, project))["tickets"]["total"] == 1

    async def test_cancelled_counts_in_total_and_no_bucket(
        self, db_session, org, project
    ):
        _make_ticket(db_session, org, project, status=TicketStatus.CANCELLED)

        stats = (await self._overview(db_session, project))["tickets"]
        assert stats["total"] == 1
        assert (stats["open"], stats["in_progress"], stats["completed"]) == (0, 0, 0)

    def test_no_uppercase_status_literals_remain(self):
        """The literals are the bug. Pin their absence, not just the counts."""
        source = Path("src/services/project_service.py").read_text()
        for literal in ('"OPEN"', '"IN_PROGRESS"', '"COMPLETED"', '"CLOSED"'):
            # They survive in the module's explanatory comment; what must not
            # come back is a comparison against one.
            assert f"t.status in [{literal}" not in source
            assert f"t.status == {literal}" not in source


# ---------------------------------------------------------------------------
# organization_memberships.default_project_id
# ---------------------------------------------------------------------------


class TestMembershipDefaultProject:
    def test_column_exists_on_the_model(self):
        assert "default_project_id" in OrganizationMembership.__table__.columns
        column = OrganizationMembership.__table__.columns["default_project_id"]
        assert column.nullable is True
        assert {fk.target_fullname for fk in column.foreign_keys} == {"projects.id"}

    def test_a_migration_adds_the_column(self):
        """The model alone proves nothing about a deployed database.

        `alembic check` catches model-vs-migration drift in CI; this pins that
        the migration exists at all, so the column cannot be introduced by the
        models with no DDL behind it.
        """
        versions = Path("alembic/versions")
        adds = [
            path.name
            for path in versions.glob("*.py")
            if re.search(
                r"add_column\(\s*[\"']organization_memberships[\"'].*default_project_id",
                path.read_text(),
                re.S,
            )
        ]
        assert adds, "no migration adds organization_memberships.default_project_id"

    async def test_first_project_seeds_every_membership(self, db_session, org):
        members = []
        for i in range(2):
            u = User(
                id=str(uuid4()),
                email=f"m{i}-{uuid4()}@example.com",
                full_name=f"Member {i}",
                role=UserRole.MEMBER,
            )
            db_session.add(u)
            m = OrganizationMembership(
                user_id=u.id,
                organization_id=org.id,
                role=OrganizationRole.DEVELOPER,
            )
            db_session.add(m)
            members.append(m)
        db_session.commit()
        assert all(m.default_project_id is None for m in members)

        created = await ProjectService(db_session).create_project(
            organization_id=org.id,
            name="First",
            description="The org's first project",
            alias="FIRST",
        )

        for m in members:
            db_session.refresh(m)
            assert m.default_project_id == created.id

    async def test_a_later_project_does_not_move_anyone(self, db_session, org):
        u = User(
            id=str(uuid4()),
            email=f"{uuid4()}@example.com",
            full_name="Member",
            role=UserRole.MEMBER,
        )
        db_session.add(u)
        membership = OrganizationMembership(
            user_id=u.id, organization_id=org.id, role=OrganizationRole.DEVELOPER
        )
        db_session.add(membership)
        db_session.commit()

        service = ProjectService(db_session)
        first = await service.create_project(
            organization_id=org.id, name="First", description="d", alias="ONE"
        )
        await service.create_project(
            organization_id=org.id, name="Second", description="d", alias="TWO"
        )

        db_session.refresh(membership)
        assert membership.default_project_id == first.id

    async def test_a_project_in_another_org_seeds_nobody_here(self, db_session, org):
        u = User(
            id=str(uuid4()),
            email=f"{uuid4()}@example.com",
            full_name="Member",
            role=UserRole.MEMBER,
        )
        db_session.add(u)
        membership = OrganizationMembership(
            user_id=u.id, organization_id=org.id, role=OrganizationRole.DEVELOPER
        )
        other_org = Organization(id=str(uuid4()), name="Elsewhere")
        db_session.add_all([membership, other_org])
        db_session.commit()

        await ProjectService(db_session).create_project(
            organization_id=other_org.id, name="Theirs", description="d", alias="THR"
        )

        db_session.refresh(membership)
        assert membership.default_project_id is None


def test_scrum_visit_ticket_fk_is_an_integer_on_the_singular_table():
    """`ticket.id` is an autoincrement int, unlike this schema's UUID keys."""
    column = ScrumTicketVisit.__table__.columns["ticket_id"]
    assert {fk.target_fullname for fk in column.foreign_keys} == {"ticket.id"}
    assert column.nullable is False


def test_scrum_datetime_columns_are_naive():
    """House convention: naive UTC. An aware column here would not compare."""
    for name in ("started_at", "ended_at"):
        assert Scrum.__table__.columns[name].type.timezone is False
