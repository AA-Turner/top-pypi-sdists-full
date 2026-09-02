"""
Tests for the releases router: CRUD, status transitions, auto released_at,
synthetic release fallback, and ticket join.
"""

import ast
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.organization import (
    Organization,
)
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User, UserRole
from src.routers.tickets import _resolve_release_filter
from src.services.ticket_release import (
    CURRENT_RELEASE,
    ReleaseNotOutstanding,
    resolve_ticket_release,
)
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    engine = build_test_engine()
    return engine


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
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"T{str(uuid4())[:6]}".upper(),
        name="Test Project",
        description="Test project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def user(db_session, org):
    u = User(
        id=str(uuid4()),
        email="test@example.com",
        full_name="Test User",
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


class TestReleaseCreate:
    def test_create_release(self, client, org, project, auth_headers):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "version": "v1.0.0",
                "status": "planned",
                "project_id": project.id,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["version"] == "v1.0.0"
        assert data["status"] == "planned"
        assert data["released_at"] is None
        assert data["project_id"] == project.id

    def test_create_release_writes_timeline_entry(
        self, client, org, project, db_session, auth_headers
    ):
        from src.domain.project_timeline import ProjectTimeline, TimelineEventType

        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v2.0.0", "project_id": project.id},
            headers=auth_headers,
        )
        assert resp.status_code == 201

        entry = db_session.exec(
            select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
        ).first()
        assert entry is not None
        assert entry.event_type == TimelineEventType.RELEASE_CREATED
        assert "v2.0.0" in entry.summary
        assert entry.metadata_json["version"] == "v2.0.0"

    def test_update_release_writes_timeline_entry(
        self, client, org, project, db_session, auth_headers
    ):
        from src.domain.project_timeline import ProjectTimeline, TimelineEventType

        release = Release(
            organization_id=org.id,
            project_id=project.id,
            version="v3.0.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()
        db_session.refresh(release)

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert resp.status_code == 200

        entries = db_session.exec(
            select(ProjectTimeline).where(
                ProjectTimeline.project_id == project.id,
                ProjectTimeline.event_type == TimelineEventType.RELEASE_UPDATED,
            )
        ).all()
        assert len(entries) == 1
        assert "released" in entries[0].summary.lower()

    def test_duplicate_version_returns_409(
        self, client, org, project, db_session, auth_headers
    ):
        db_session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version="v1.0.0",
                status=ReleaseStatus.PLANNED,
            )
        )
        db_session.commit()

        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v1.0.0", "project_id": project.id},
            headers=auth_headers,
        )
        assert resp.status_code == 409

    def test_create_release_persists_summary_and_changelog(
        self, client, org, project, db_session, auth_headers
    ):
        changelog = {
            "repos": [
                {
                    "repo": "innoday",
                    "prs": [
                        {"number": 209, "title": "Fix cascade", "author": "khaviland"}
                    ],
                }
            ]
        }
        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "version": "v1.4.0",
                "summary": "Bug fixes and cascade delete improvements",
                "changelog": changelog,
                "project_id": project.id,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["summary"] == "Bug fixes and cascade delete improvements"
        assert data["changelog"] == changelog

        stored = db_session.exec(
            select(Release).where(
                Release.organization_id == org.id, Release.version == "v1.4.0"
            )
        ).first()
        assert stored.summary == "Bug fixes and cascade delete improvements"
        assert stored.changelog == changelog


class TestReleasePatch:
    def test_patch_notes(self, client, org, project, db_session, auth_headers):
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.1.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"notes": "Fixed critical bug"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["notes"] == "Fixed critical bug"

    def test_status_to_released_sets_released_at(
        self, client, org, project, db_session, auth_headers
    ):
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.2.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "released"
        assert data["released_at"] is not None

    def test_patch_summary_and_changelog(
        self, client, org, project, db_session, auth_headers
    ):
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.4.1",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()

        changelog = {"repos": [{"repo": "innoday", "prs": []}]}
        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"summary": "Patched summary", "changelog": changelog},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] == "Patched summary"
        assert data["changelog"] == changelog

    def test_released_at_not_overwritten_if_already_set(
        self, client, org, project, db_session, auth_headers
    ):
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.3.0",
            status=ReleaseStatus.RELEASED,
            released_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        db_session.add(release)
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"notes": "updated notes"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        # released_at should be unchanged
        assert "2026-01-01" in resp.json()["released_at"]


class TestReleaseGetByVersion:
    def test_get_existing_release_by_version(
        self, client, org, project, db_session, auth_headers
    ):
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v2.0.0",
            status=ReleaseStatus.RELEASED,
        )
        db_session.add(release)
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases/by-version/v2.0.0",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["version"] == "v2.0.0"

    def test_synthetic_release_returned_when_tickets_exist(
        self, client, org, project, db_session, auth_headers
    ):
        # No Release row, but tickets have this release version
        ticket = Ticket(
            organization_id=org.id,
            project_id=project.id,
            summary="Fix something",
            status=TicketStatus.TODO,
            external_ticket_id="TEST-1",
            release="v3.0.0-beta",
        )
        db_session.add(ticket)
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases/by-version/v3.0.0-beta",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["version"] == "v3.0.0-beta"
        # Synthetic releases have no persisted id
        assert data.get("id") is None or data["id"] == ""

    def test_returns_synthetic_when_no_release_and_no_tickets(
        self, client, org, project, auth_headers
    ):
        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases/by-version/v99.0.0",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["version"] == "v99.0.0"
        assert data["ticket_count"] == 0
        assert data.get("id") == "" or data.get("id") is None


class TestReleaseLeavesTicketsAlone:
    """**Shipping a version no longer closes the work planned into it.**

    It used to set every non-DONE ticket carrying the version to DONE with a
    completion timestamp. Membership in a release is a free-text string somebody
    typed or dragged, not evidence that work happened, so a ticket nobody ever
    started was closed exactly like one that shipped -- destroying the only
    record that it had not been done, writing nothing back to the external board,
    and offering no undo. The dry run could not warn about it either, because
    blastoff never queries tickets.

    Shipping now touches no ticket and records what it found instead.
    """

    def test_shipping_leaves_unfinished_work_unfinished(
        self, client, org, project, db_session, auth_headers
    ):
        """The bug, stated directly: a ticket nobody started stays not-started."""
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.0.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                summary="never started",
                status=TicketStatus.TODO,
                external_ticket_id="T-1",
                release="v4.0.0",
            )
        )
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                summary="half done",
                status=TicketStatus.IN_PROGRESS,
                external_ticket_id="T-2",
                release="v4.0.0",
            )
        )
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert resp.status_code == 200

        tickets = {
            t.external_ticket_id: t
            for t in db_session.exec(
                select(Ticket).where(
                    Ticket.organization_id == org.id, Ticket.release == "v4.0.0"
                )
            ).all()
        }
        assert tickets["T-1"].status == TicketStatus.TODO
        assert tickets["T-2"].status == TicketStatus.IN_PROGRESS
        assert all(t.completed_at is None for t in tickets.values()), (
            "shipping stamped a completion date on work that was never completed"
        )

    def test_shipping_reports_what_was_planned_in(
        self, client, org, project, db_session, auth_headers
    ):
        """The replacement for closing: say what is there, and how much is open.

        The counts come from `_ticket_counts`, the same helper that fills
        `open_ticket_count` on every release response -- so the note and the
        field cannot disagree.
        """
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.1.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        for ref, status in (
            ("T-3", TicketStatus.DONE),
            ("T-4", TicketStatus.DONE),
            ("T-5", TicketStatus.TODO),
        ):
            db_session.add(
                Ticket(
                    organization_id=org.id,
                    project_id=project.id,
                    summary=ref,
                    status=status,
                    external_ticket_id=ref,
                    release="v4.1.0",
                )
            )
        db_session.commit()

        data = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        ).json()

        assert data["notes"] == "Shipped with 3 ticket(s) planned in -- 1 not done."
        assert data["open_ticket_count"] == 1, (
            "shipping zeroed the count that answers 'what never got finished'"
        )

    def test_a_release_with_everything_done_says_so(
        self, client, org, project, db_session, auth_headers
    ):
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.2.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                summary="shipped",
                status=TicketStatus.DONE,
                external_ticket_id="T-6",
                release="v4.2.0",
            )
        )
        db_session.commit()

        data = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        ).json()
        assert data["notes"] == "Shipped with 1 ticket(s) planned in, all done."

    def test_a_release_with_nothing_planned_in_says_so(
        self, client, org, project, db_session, auth_headers
    ):
        """Never a bare "0 tickets", which reads as a failure to look."""
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.3.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()

        data = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        ).json()
        assert data["notes"] == "Shipped with no tickets planned in."

    def test_the_stamp_counts_only_this_project_and_this_version(
        self, client, org, project, db_session, auth_headers
    ):
        """A version string is unique per project, not per org.

        Two projects on `v4.4.0` would otherwise pool their tickets into one
        count -- the same scoping bug the old closer had to avoid, for the same
        reason, and the reason `_ticket_counts` takes a `project_id`.
        """
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.4.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                summary="ours",
                status=TicketStatus.TODO,
                external_ticket_id="T-7",
                release="v4.4.0",
            )
        )
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=str(uuid4()),  # another project, same version string
                summary="theirs",
                status=TicketStatus.TODO,
                external_ticket_id="T-8",
                release="v4.4.0",
            )
        )
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                summary="next release",
                status=TicketStatus.TODO,
                external_ticket_id="T-9",
                release="v4.5.0",
            )
        )
        db_session.commit()

        data = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        ).json()
        assert data["notes"] == "Shipped with 1 ticket(s) planned in -- 1 not done."

    def test_a_plain_patch_does_not_re_stamp(
        self, client, org, project, db_session, auth_headers
    ):
        """The stamp records the act of shipping, not the state of the row.

        Editing an already-released release must not append a second line -- the
        release shipped once.
        """
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.6.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()

        first = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"status": "released"},
            headers=auth_headers,
        ).json()["notes"]
        assert first.count("Shipped with") == 1

        second = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release.id}",
            json={"notes": first},
            headers=auth_headers,
        )
        assert second.status_code == 200
        assert second.json()["notes"].count("Shipped with") == 1

    def test_unreleasing_and_reshipping_stamps_again(
        self, client, org, project, db_session, auth_headers
    ):
        """A second ship is a second event, and the notes are its record."""
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v4.7.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()
        url = f"/api/v1/organizations/{org.id}/releases/{release.id}"

        assert (
            client.patch(url, json={"status": "released"}, headers=auth_headers)
            .json()["notes"]
            .count("Shipped with")
            == 1
        )
        assert (
            client.patch(url, json={"status": "planned"}, headers=auth_headers)
        ).status_code == 200
        assert (
            client.patch(url, json={"status": "released"}, headers=auth_headers)
            .json()["notes"]
            .count("Shipped with")
            == 2
        )

    def test_creating_a_release_already_shipped_also_stamps(
        self, client, org, project, db_session, auth_headers
    ):
        """`create` and `update` are two doors to the same event.

        The old closer was called from both, and a fix applied to one only is how
        the two drifted apart before (`resolve_project_ref` was in `create` and
        not `update`, 300 lines away in the same file).
        """
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                summary="already planned in",
                status=TicketStatus.TODO,
                external_ticket_id="T-10",
                release="v4.8.0",
            )
        )
        db_session.commit()

        data = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "version": "v4.8.0",
                "project_id": project.id,
                "status": "released",
            },
            headers=auth_headers,
        ).json()
        assert data["notes"] == "Shipped with 1 ticket(s) planned in -- 1 not done."

        ticket = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "T-10")
        ).first()
        db_session.refresh(ticket)
        assert ticket.status == TicketStatus.TODO

    def test_release_requires_project_id(self, db_session, org):
        """
        Release.project_id is a required (NOT NULL) column -- a release cannot
        exist without a project, so it can never span every project in an org.
        Constructing one without project_id must fail at the DB layer.
        """
        from sqlalchemy.exc import IntegrityError

        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            version="v4.9.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_ticket_count_scoped_to_release_project_id(
        self, client, org, db_session, auth_headers
    ):
        project_id = str(uuid4())
        release = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project_id,
            version="v4.10.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=project_id,
                summary="In project",
                status=TicketStatus.TODO,
                external_ticket_id="T-13",
                release="v4.10.0",
            )
        )
        db_session.add(
            Ticket(
                organization_id=org.id,
                project_id=str(uuid4()),
                summary="Other project",
                status=TicketStatus.TODO,
                external_ticket_id="T-14",
                release="v4.10.0",
            )
        )
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = next(r for r in resp.json() if r["version"] == "v4.10.0")
        assert data["ticket_count"] == 1
        assert data["open_ticket_count"] == 1


class TestReleaseList:
    def test_list_releases(self, client, org, project, db_session, auth_headers):
        for v in ["v1.0.0", "v1.1.0", "v1.2.0"]:
            db_session.add(
                Release(
                    organization_id=org.id,
                    project_id=project.id,
                    version=v,
                    status=ReleaseStatus.PLANNED,
                )
            )
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3

    def test_filter_by_status(self, client, org, project, db_session, auth_headers):
        db_session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version="v1.0.0",
                status=ReleaseStatus.PLANNED,
            )
        )
        db_session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version="v1.1.0",
                status=ReleaseStatus.RELEASED,
            )
        )
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases?status=released",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert all(r["status"] == "released" for r in data)


class TestPipelineRotation:
    """Shipping a version rotates the project's two forward slots.

    Slot 1 is IN_PROGRESS (what blastoff cuts) and slot 2 is PLANNED (what
    tickets are planned into). This hangs off "a release became RELEASED"
    rather than off the command that caused it, so every path rotates -- the
    CLI proxy, the blast_off MCP tool, GitHub sync, and a person in the UI.
    """

    def _pipeline(self, db_engine, project_id):
        """Read the pipeline from a brand-new session.

        Not the test's own `db_session`: the request ran in a different session,
        so the test session's identity map holds the rows as they were before the
        rotation. Expiring would do, but a fresh session is unambiguous -- it can
        only report what is actually committed to the database.
        """
        with Session(db_engine) as fresh:
            rows = fresh.exec(
                select(Release).where(Release.project_id == project_id)
            ).all()
            return {r.version: r.status for r in rows}

    def test_patching_to_released_promotes_slot_two_and_opens_a_new_one(
        self, client, org, project, db_session, db_engine, auth_headers
    ):
        shipping = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.9.0",
            status=ReleaseStatus.IN_PROGRESS,
        )
        db_session.add(shipping)
        db_session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                version="v1.10.0",
                status=ReleaseStatus.PLANNED,
            )
        )
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{shipping.id}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert resp.status_code == 200

        assert self._pipeline(db_engine, project.id) == {
            "v1.9.0": ReleaseStatus.RELEASED,
            "v1.10.0": ReleaseStatus.IN_PROGRESS,
            "v1.11.0": ReleaseStatus.PLANNED,
        }

    def test_creating_a_released_version_opens_the_pipeline_above_it(
        self, client, org, project, db_session, db_engine, auth_headers
    ):
        """This is the blastoff path: `record_release` POSTs a RELEASED row for a
        project that may have had no pipeline at all."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "project_id": project.id,
                "version": "v1.9.0",
                "status": "released",
            },
            headers=auth_headers,
        )
        assert resp.status_code in (200, 201)

        assert self._pipeline(db_engine, project.id) == {
            "v1.9.0": ReleaseStatus.RELEASED,
            "v1.10.0": ReleaseStatus.IN_PROGRESS,
            "v1.11.0": ReleaseStatus.PLANNED,
        }

    def test_rotation_is_idempotent_across_a_repeated_release(
        self, client, org, project, db_session, db_engine, auth_headers
    ):
        """`record_release` re-runs on a retried `innoday release`. Rotating twice
        must not skip a version -- a pipeline that advanced on every replay would
        leave a gap in the versions nobody ever shipped."""
        shipping = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.9.0",
            status=ReleaseStatus.IN_PROGRESS,
        )
        db_session.add(shipping)
        db_session.commit()

        for _ in range(2):
            resp = client.patch(
                f"/api/v1/organizations/{org.id}/releases/{shipping.id}",
                json={"status": "released"},
                headers=auth_headers,
            )
            assert resp.status_code == 200

        assert self._pipeline(db_engine, project.id) == {
            "v1.9.0": ReleaseStatus.RELEASED,
            "v1.10.0": ReleaseStatus.IN_PROGRESS,
            "v1.11.0": ReleaseStatus.PLANNED,
        }

    def test_a_released_version_and_its_pipeline_commit_together(
        self, client, org, project, db_session, db_engine, auth_headers
    ):
        """The rotation shares the release's transaction, so a project can never
        be observed shipped-but-not-rotated by a concurrent reader."""
        ticket = Ticket(
            summary="in the release",
            organization_id=org.id,
            project_id=project.id,
            status=TicketStatus.IN_PROGRESS,
            release="v1.9.0",
        )
        db_session.add(ticket)
        shipping = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version="v1.9.0",
            status=ReleaseStatus.IN_PROGRESS,
        )
        db_session.add(shipping)
        db_session.commit()

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{shipping.id}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # The pipeline advanced, and the ticket was left exactly as it was --
        # shipping rotates the slots, it does not finish anybody's work.
        db_session.expire_all()
        untouched = db_session.exec(
            select(Ticket).where(Ticket.id == ticket.id)
        ).first()
        assert untouched.status == TicketStatus.IN_PROGRESS
        assert untouched.completed_at is None
        assert self._pipeline(db_engine, project.id)["v1.10.0"] == (
            ReleaseStatus.IN_PROGRESS
        )

    def test_a_project_shipping_a_non_semver_tag_gets_no_invented_pipeline(
        self, client, org, project, db_session, db_engine, auth_headers
    ):
        """`rancher-FINAL` has no successor. Bootstrapping this project to v0.1.0
        would put it on a versioning line nobody chose."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "project_id": project.id,
                "version": "rancher-FINAL",
                "status": "released",
            },
            headers=auth_headers,
        )
        assert resp.status_code in (200, 201)
        assert self._pipeline(db_engine, project.id) == {
            "rancher-FINAL": ReleaseStatus.RELEASED
        }


class TestCurrentReleaseTickets:
    """One call that answers "what is in the release we're cutting".

    The point is that a summary can be generated from this route and nothing else,
    so the tests are about it needing no filters and never disagreeing with the UI.
    """

    def _url(self, org_id, project_id):
        return (
            f"/api/v1/organizations/{org_id}/releases/current/tickets"
            f"?project_id={project_id}"
        )

    def _seed(self, db_session, org, project):
        for version, status_ in (
            ("v1.8.0", ReleaseStatus.RELEASED),
            ("v1.9.0", ReleaseStatus.IN_PROGRESS),
            ("v1.10.0", ReleaseStatus.PLANNED),
        ):
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=status_,
                )
            )
        for summary, status_, release in (
            ("in the current release", TicketStatus.IN_PROGRESS, "v1.9.0"),
            ("already done in it", TicketStatus.DONE, "v1.9.0"),
            ("deferred to the next one", TicketStatus.TODO, "v1.10.0"),
            ("no version at all", TicketStatus.TODO, None),
        ):
            db_session.add(
                Ticket(
                    summary=summary,
                    organization_id=org.id,
                    project_id=project.id,
                    status=status_,
                    release=release,
                )
            )
        db_session.commit()

    def test_returns_the_in_progress_release_and_only_its_tickets(
        self, client, org, project, db_session, auth_headers
    ):
        self._seed(db_session, org, project)

        r = client.get(self._url(org.id, project.id), headers=auth_headers)
        assert r.status_code == 200
        data = r.json()

        assert data["version"] == "v1.9.0"
        assert data["status"] == "in_progress"

        summaries = {t["summary"] for t in data["tickets"]}
        assert summaries == {"in the current release", "already done in it"}
        # DONE work is in the release; the counts say so separately.
        assert data["ticket_count"] == 2
        assert data["open_ticket_count"] == 1

    def test_it_needs_nothing_but_the_project(
        self, client, org, project, db_session, auth_headers
    ):
        """No version, no status filter, no date window. A caller that had to pick
        those could pick differently from the next caller."""
        self._seed(db_session, org, project)
        r = client.get(self._url(org.id, project.id), headers=auth_headers)
        assert r.status_code == 200

    def test_it_names_the_same_version_the_page_does(
        self, client, org, project, db_session, auth_headers
    ):
        """Both go through `next_release`. A route that resolved "current" its own
        way could disagree with the Releases tab, which is the class of bug the
        pipeline work exists to remove."""
        from src.services.release_planning import next_release

        self._seed(db_session, org, project)

        releases = db_session.exec(
            select(Release).where(Release.project_id == project.id)
        ).all()
        r = client.get(self._url(org.id, project.id), headers=auth_headers)

        assert r.json()["version"] == next_release(list(releases)).version

    def test_a_project_with_no_upcoming_release_404s(
        self, client, org, project, db_session, auth_headers
    ):
        """A real state -- never shipped, never synced. Answering 200 with an empty
        release would read as "the current release is empty" instead."""
        r = client.get(self._url(org.id, project.id), headers=auth_headers)
        assert r.status_code == 404
        assert "no current release" in r.json()["detail"].lower()

    def test_a_stale_version_string_belongs_to_no_release(
        self, client, org, project, db_session, auth_headers
    ):
        """The join is free text with no FK, so this is reachable. Such a ticket is
        in no release's list -- documented on the tool, and surfaced on the
        Releases tab rather than silently folded in here."""
        self._seed(db_session, org, project)
        db_session.add(
            Ticket(
                summary="points at nothing",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.TODO,
                release="v9.9.9",
            )
        )
        db_session.commit()

        r = client.get(self._url(org.id, project.id), headers=auth_headers)
        assert "points at nothing" not in {t["summary"] for t in r.json()["tickets"]}


class TestProjectTicketsFilteredByRelease:
    """Release filters live on the **project** route, and only there.

    A version string means something only inside a project -- PF's v1.9.0 and
    BPAI's v1.9.0 are unrelated releases that happen to share a name. Filtering an
    organization-wide collection by version would merge two different answers, so
    the project is a path segment and the meaningless form cannot be expressed.
    """

    def _seed(self, db_session, org, project):
        for version, status_ in (
            ("v1.8.0", ReleaseStatus.RELEASED),
            ("v1.9.0", ReleaseStatus.IN_PROGRESS),
            ("v1.10.0", ReleaseStatus.PLANNED),
        ):
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=status_,
                )
            )
        for summary, release in (
            ("in the current release", "v1.9.0"),
            ("deferred", "v1.10.0"),
            ("unversioned", None),
            ("points at nothing", "v9.9.9"),
        ):
            db_session.add(
                Ticket(
                    summary=summary,
                    organization_id=org.id,
                    project_id=project.id,
                    status=TicketStatus.TODO,
                    release=release,
                )
            )
        db_session.commit()

    def _base(self, org, project):
        return f"/api/v1/organizations/{org.id}/projects/{project.id}/tickets"

    def test_release_current_filters_to_the_in_progress_version(
        self, client, org, project, db_session, auth_headers
    ):
        self._seed(db_session, org, project)
        r = client.get(
            self._base(org, project) + "?release=current", headers=auth_headers
        )
        assert r.status_code == 200
        assert {t["summary"] for t in r.json()} == {"in the current release"}

    def test_an_explicit_version_works_too(
        self, client, org, project, db_session, auth_headers
    ):
        self._seed(db_session, org, project)
        r = client.get(
            self._base(org, project) + "?release=v1.10.0", headers=auth_headers
        )
        assert {t["summary"] for t in r.json()} == {"deferred"}

    def test_a_version_nothing_carries_matches_nothing_rather_than_erroring(
        self, client, org, project, db_session, auth_headers
    ):
        """The join is free text with no FK, so an unknown version is a legitimate
        query with an empty answer -- not a 404."""
        self._seed(db_session, org, project)
        r = client.get(
            self._base(org, project) + "?release=v42.0.0", headers=auth_headers
        )
        assert r.status_code == 200 and r.json() == []

    def test_the_organization_collection_has_no_release_filter(
        self, client, org, project, db_session, auth_headers
    ):
        """Passing one must not silently filter. FastAPI ignores unknown query
        params, so the org route returns everything -- which is the honest answer
        for a question that has no organization-wide meaning."""
        self._seed(db_session, org, project)
        r = client.get(
            f"/api/v1/organizations/{org.id}/tickets?release=v1.9.0",
            headers=auth_headers,
        )
        assert r.status_code == 200
        # All four seeded tickets, not just the one on v1.9.0.
        assert len(r.json()) == 4

    def test_the_first_class_route_matches_the_filter(
        self, client, org, project, db_session, auth_headers
    ):
        """Same answer, no query string. Both org and project are path segments,
        so there is no parameter to get wrong."""
        self._seed(db_session, org, project)
        direct = client.get(
            self._base(org, project) + "/current-release", headers=auth_headers
        )
        filtered = client.get(
            self._base(org, project) + "?release=current", headers=auth_headers
        )
        assert direct.status_code == 200
        assert {t["summary"] for t in direct.json()} == {
            t["summary"] for t in filtered.json()
        }

    def test_no_current_release_is_a_404_on_both(
        self, client, org, project, db_session, auth_headers
    ):
        for url in (
            self._base(org, project) + "?release=current",
            self._base(org, project) + "/current-release",
        ):
            assert client.get(url, headers=auth_headers).status_code == 404

    def test_another_organizations_project_is_refused(
        self, client, org, project, db_session, auth_headers
    ):
        """The project route already checks ownership; the new route must too, or
        it would be a way around it."""
        self._seed(db_session, org, project)
        other = Organization(id=str(uuid4()), name="Other Org")
        db_session.add(other)
        db_session.commit()

        r = client.get(
            f"/api/v1/organizations/{other.id}/projects/{project.id}/tickets"
            "/current-release",
            headers=auth_headers,
        )
        assert r.status_code in (403, 404)


class TestTheCurrentSentinelHasOneDefinition:
    """One literal and one resolver for ``current``, both pinned by construction.

    Both halves have diverged once already, in the same shape twice. The CLI used
    to compute its own answer from ``max(released_at)`` and send back a day count;
    then, smaller but identical in kind, ``src/cli/commands/summary.py``
    re-declared ``CURRENT_RELEASE = "current"`` while
    ``src/cli/commands/tickets.py`` imported the real one -- two literals that had
    to stay equal with nothing pinning them.

    The resolver went the same way: the read filter and the write path each ran
    their own ``select(Release)`` + ``next_release``, which is one rule written
    twice and therefore one rule that can be changed once. They are *supposed* to
    differ about the error (404 for a filter, 422 for a body field) and about
    everything a non-sentinel value means -- so this asserts they agree on the
    version and disagree only on the failure.
    """

    SRC = Path(__file__).resolve().parents[1] / "src"

    def _modules_assigning(self, name: str):
        found = []
        for path in sorted(self.SRC.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                targets = (
                    node.targets
                    if isinstance(node, ast.Assign)
                    else [node.target]
                    if isinstance(node, ast.AnnAssign)
                    else []
                )
                if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                    found.append(path.relative_to(self.SRC).as_posix())
        return found

    def test_current_release_is_assigned_in_exactly_one_module(self):
        assert self._modules_assigning("CURRENT_RELEASE") == [
            "services/ticket_release.py"
        ]

    def test_the_read_filter_and_the_write_path_name_the_same_version(
        self, db_session, org, project
    ):
        db_session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version="v1.9.0",
                name="v1.9.0",
                status=ReleaseStatus.IN_PROGRESS,
            )
        )
        db_session.commit()

        assert (
            _resolve_release_filter(CURRENT_RELEASE, org.id, project.id, db_session)
            == "v1.9.0"
        )
        assert (
            resolve_ticket_release(
                db_session,
                organization_id=org.id,
                project_id=project.id,
                value=CURRENT_RELEASE,
            )
            == "v1.9.0"
        )

    def test_they_differ_only_in_how_they_report_having_no_answer(
        self, db_session, org, project
    ):
        with pytest.raises(HTTPException) as read:
            _resolve_release_filter(CURRENT_RELEASE, org.id, project.id, db_session)
        assert read.value.status_code == 404

        with pytest.raises(ReleaseNotOutstanding):
            resolve_ticket_release(
                db_session,
                organization_id=org.id,
                project_id=project.id,
                value=CURRENT_RELEASE,
            )

    def test_an_unknown_version_is_still_read_verbatim_and_refused_on_write(
        self, db_session, org, project
    ):
        """The halves the consolidation deliberately left apart.

        A filter passes an unmatched version through (a legitimate query with an
        empty answer); a write refuses it, because what is stored has to match
        ``_bulk_close_tickets_for_release`` byte-for-byte.
        """
        assert (
            _resolve_release_filter("v42.0.0", org.id, project.id, db_session)
            == "v42.0.0"
        )
        with pytest.raises(ReleaseNotOutstanding):
            resolve_ticket_release(
                db_session,
                organization_id=org.id,
                project_id=project.id,
                value="v42.0.0",
            )


class TestWithdrawingAReleaseFreesItsVersion:
    """Archiving a release read like undoing it and quietly spent the version
    for good.

    `UniqueConstraint(project_id, version)` ignored status, so an archived
    v1.0.0 still owned the string: `releases create v1.0.0` answered "already
    exists" against a row nobody could see the point of, and no command could
    give it back. Measured on S4C, whose v1.0.0 was archived and then unusable.

    Deleted and archived are now different, and the difference is visibility and
    usage — archived stays visible and keeps the version; deleted disappears and
    hands the number back.
    """

    def _make(self, client, org, project, auth_headers, version="v1.0.0", **kw):
        body = {"version": version, "project_id": project.id, **kw}
        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json=body,
            headers=auth_headers,
        )
        assert resp.status_code in (200, 201), resp.text
        return resp.json()

    def test_archiving_does_not_free_the_version(
        self, client, org, project, auth_headers
    ):
        """The trap this whole change exists to remove — pinned so nobody
        'simplifies' archive and delete back into one thing."""
        made = self._make(client, org, project, auth_headers)
        client.patch(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            json={"status": "archived"},
            headers=auth_headers,
        )
        again = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v1.0.0", "project_id": project.id},
            headers=auth_headers,
        )
        assert again.status_code == 409, again.text

    def test_deleting_frees_the_version(self, client, org, project, auth_headers):
        made = self._make(client, org, project, auth_headers)
        gone = client.delete(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        assert gone.status_code == 204, gone.text

        again = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v1.0.0", "project_id": project.id},
            headers=auth_headers,
        )
        assert again.status_code in (200, 201), again.text
        assert again.json()["id"] != made["id"], "reused the withdrawn row"

    def test_a_withdrawn_release_is_invisible(
        self, client, org, project, auth_headers, db_session
    ):
        made = self._make(client, org, project, auth_headers)
        client.delete(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        listed = client.get(
            f"/api/v1/organizations/{org.id}/releases",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        assert made["id"] not in [r["id"] for r in listed.json()]

        fetched = client.get(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        assert fetched.status_code == 404

    def test_the_row_survives_so_the_record_does(
        self, client, org, project, auth_headers, db_session
    ):
        """Soft, because tickets join a release by version string — dropping the
        row would leave them pointing at a version nothing can explain."""
        made = self._make(client, org, project, auth_headers)
        client.delete(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        row = db_session.exec(select(Release).where(Release.id == made["id"])).first()
        assert row is not None, "the record was destroyed, not withdrawn"
        assert row.deleted_at is not None

    def test_withdrawing_leaves_the_tickets_alone(
        self, client, org, project, auth_headers, db_session
    ):
        made = self._make(client, org, project, auth_headers)
        t = Ticket(
            id=99321,
            organization_id=org.id,
            project_id=project.id,
            summary="On the withdrawn release",
            status=TicketStatus.TODO,
            release="v1.0.0",
        )
        db_session.add(t)
        db_session.commit()

        client.delete(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        db_session.expire_all()
        still = db_session.exec(select(Ticket).where(Ticket.id == 99321)).first()
        assert still is not None
        assert still.release == "v1.0.0"

    def test_withdrawing_twice_is_not_an_error(
        self, client, org, project, auth_headers
    ):
        """The caller asked for it to be gone, and it is."""
        made = self._make(client, org, project, auth_headers)
        first = client.delete(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        second = client.delete(
            f"/api/v1/organizations/{org.id}/releases/{made['id']}",
            headers=auth_headers,
        )
        assert first.status_code == 204
        assert second.status_code == 204
