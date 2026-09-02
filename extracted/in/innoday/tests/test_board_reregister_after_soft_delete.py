"""Regression tests for C1: a soft-deleted board must NOT block registering a
new board for the same project.

The flagship migration flow is: soft-delete a project's old board (e.g. Jira)
for audit, then register a NEW board (e.g. Linear) for the SAME project. The
one-board-per-project uniqueness is enforced by a PARTIAL unique index
(WHERE deleted_at IS NULL), so a soft-deleted board no longer occupies the
project's single live slot -- but two LIVE boards for one project still fail.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.user import User, UserRole
from src.services.board_clear_service import soft_delete_board
from tests.auth_helpers import bearer_for_engine
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
    """Seed org, a platform-member user (bypasses org-membership RBAC), a
    project, and one live Jira board attached to that project."""
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
            board_name="Old Jira Board",
            board_url="https://x.atlassian.net/jira/software/projects/OLD/boards/1",
            board_type=BoardType.JIRA,
            board_external_id="OLD",
        )
        s.add_all([org, user, proj, board])
        s.commit()
        return {
            "org": org.id,
            "user": user.id,
            "project": proj.id,
            "old_board": board.id,
        }


def _register_new_board(client, seeded, db_engine):
    """Register a fresh Linear board for the same project, bypassing the
    external-network validation/resolution steps register_board performs (we
    are exercising the DB uniqueness rule, not Linear connectivity)."""
    body = {
        "project_id": seeded["project"],
        "board_name": "New Linear Board",
        "board_url": "https://linear.app/acme/team/NEW/all",
        "board_type": "linear",
    }
    with (
        patch("src.routers.boards.extract_board_id", return_value="NEW-team-uuid"),
        patch("src.routers.boards.is_uuid", return_value=True),
        patch("src.routers.boards.validate_board_access", return_value=True),
    ):
        return client.post(
            f"/api/v1/organizations/{seeded['org']}/boards",
            json=body,
            headers={
                **bearer_for_engine(db_engine, seeded["user"]),
                "X-Integration-Token": "tok",
            },
        )


def test_reregister_after_soft_delete_succeeds(client, db_engine, seeded):
    # Soft-delete the old board (Jira) -- keeps its row + project_id for audit.
    with Session(db_engine) as s:
        old = s.get(BoardRegistration, seeded["old_board"])
        soft_delete_board(s, old)
        s.commit()

    # Registering a NEW board for the SAME project must now succeed (no 500 /
    # IntegrityError from the old unconditional unique constraint).
    r = _register_new_board(client, seeded, db_engine)
    assert r.status_code in (200, 201), r.text

    with Session(db_engine) as s:
        boards = s.exec(
            select(BoardRegistration).where(
                BoardRegistration.project_id == seeded["project"]
            )
        ).all()
        # Both rows exist: the audit-preserved old one + the new active one.
        assert len(boards) == 2
        old = next(b for b in boards if b.id == seeded["old_board"])
        new = next(b for b in boards if b.id != seeded["old_board"])
        assert old.deleted_at is not None  # audit preserved
        assert old.is_active is False
        assert new.deleted_at is None  # new board is the live one
        assert new.is_active is True
        assert new.board_type == BoardType.LINEAR


def test_second_live_board_for_same_project_still_fails(db_engine, seeded):
    """The partial unique index must still forbid TWO live boards for one
    project (only soft-deleted ones are exempt)."""
    with Session(db_engine) as s:
        dup = BoardRegistration(
            id=str(uuid4()),
            user_id=seeded["user"],
            organization_id=seeded["org"],
            project_id=seeded["project"],  # same project, old board still LIVE
            board_name="Second Live Board",
            board_url="https://linear.app/acme/team/DUP/all",
            board_type=BoardType.LINEAR,
            board_external_id="DUP",
        )
        s.add(dup)
        with pytest.raises(IntegrityError):
            s.commit()
