from datetime import datetime, timezone
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User, UserRole
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    engine = build_test_engine()
    return engine


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
def seeded(db_engine):
    with Session(db_engine) as s:
        org = Organization(id=str(uuid4()), name="Org")
        user = User(
            id=str(uuid4()),
            email="t@e.com",
            full_name="T",
            role=UserRole.MEMBER,
            is_platform_member=True,
        )
        proj = Project(
            id=str(uuid4()),
            name="P",
            alias="P",
            description="d",
            organization_id=org.id,
        )
        board = BoardRegistration(
            id=str(uuid4()),
            user_id=user.id,
            organization_id=org.id,
            project_id=proj.id,
            board_name="B",
            board_url="https://x",
            board_type=BoardType.JIRA,
            board_external_id="ext-1",
        )
        s.add_all([org, user, proj, board])
        s.commit()
        live = Ticket(
            summary="live",
            organization_id=org.id,
            project_id=proj.id,
            board_registration_id=board.id,
            external_ticket_id="E-1",
            status=TicketStatus.TODO,
        )
        dead = Ticket(
            summary="dead",
            organization_id=org.id,
            project_id=proj.id,
            board_registration_id=board.id,
            external_ticket_id="E-2",
            status=TicketStatus.TODO,
            deleted_at=datetime.now(timezone.utc),
        )
        s.add_all([live, dead])
        s.commit()
        return {
            "org": org.id,
            "user": user.id,
            "project": proj.id,
            "board": board.id,
            "auth": bearer_for(s, user.id),
        }


def _summaries(resp):
    return {t["summary"] for t in resp.json()}


def test_org_ticket_list_excludes_deleted(client, seeded):
    r = client.get(
        f"/api/v1/organizations/{seeded['org']}/tickets",
        headers=seeded["auth"],
    )
    assert r.status_code == 200
    assert _summaries(r) == {"live"}


def test_project_ticket_list_excludes_deleted(client, seeded):
    r = client.get(
        f"/api/v1/organizations/{seeded['org']}/projects/{seeded['project']}/tickets",
        headers=seeded["auth"],
    )
    assert r.status_code == 200
    assert _summaries(r) == {"live"}


def test_board_ticket_list_excludes_deleted(client, seeded):
    r = client.get(
        f"/api/v1/organizations/{seeded['org']}/boards/{seeded['board']}/tickets",
        headers=seeded["auth"],
    )
    assert r.status_code == 200
    assert _summaries(r) == {"live"}
