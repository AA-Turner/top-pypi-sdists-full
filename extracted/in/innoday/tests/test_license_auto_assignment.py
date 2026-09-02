"""
Tests for automatic top-tier license assignment.

Every organization is expected to have an active license at all times --
before this fix, create_organization never created one, so a brand-new org
had can_create_ticket (and every other license-gated action) return False
unconditionally, not "limited tier", just fully blocked. Confirmed live
against the dev database: 4 of 5 real orgs had zero organization_licenses
rows.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.license import LicenseTier
from src.domain.organization import Organization, OrganizationLicense
from src.domain.user import User, UserRole
from src.utils.license_utils import (
    TOP_LICENSE_TIER_NAME,
    LicenseError,
    ensure_top_tier_license,
    is_license_active,
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
def velocity_tier(db_session):
    tier = LicenseTier(
        id=str(uuid4()), name=TOP_LICENSE_TIER_NAME, display_name="Velocity"
    )
    db_session.add(tier)
    db_session.commit()
    db_session.refresh(tier)
    return tier


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def user(db_session):
    u = User(
        id=str(uuid4()),
        email="creator@example.com",
        full_name="Creator User",
        role=UserRole.MEMBER,
        is_platform_member=False,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


class TestEnsureTopTierLicense:
    def test_creates_active_velocity_license_for_org_with_none(
        self, db_session, org, velocity_tier
    ):
        assert not is_license_active(org.id, db_session)

        license_row = ensure_top_tier_license(org.id, db_session)

        assert license_row.status == "ACTIVE"
        assert license_row.license_tier_id == velocity_tier.id
        assert is_license_active(org.id, db_session)

    def test_idempotent_when_org_already_has_active_license(
        self, db_session, org, velocity_tier
    ):
        first = ensure_top_tier_license(org.id, db_session)
        second = ensure_top_tier_license(org.id, db_session)

        assert first.id == second.id
        from sqlmodel import select as sqlmodel_select

        rows = db_session.exec(
            sqlmodel_select(OrganizationLicense).where(
                OrganizationLicense.organization_id == org.id
            )
        ).all()
        assert len(rows) == 1

    def test_raises_if_top_tier_not_seeded(self, db_session, org):
        # No velocity_tier fixture used here -- license_tiers table is empty.
        with pytest.raises(LicenseError):
            ensure_top_tier_license(org.id, db_session)


class TestCreateOrganizationAssignsLicense:
    def test_new_org_gets_active_license_on_creation(
        self, client, velocity_tier, user, db_session
    ):
        resp = client.post(
            "/api/v1/organizations",
            json={"name": "Brand New Org"},
            headers=bearer_for(db_session, user.id),
        )
        assert resp.status_code == 201
        org_id = resp.json()["id"]

        assert is_license_active(org_id, db_session)

    def test_new_org_ticket_creation_not_blocked_by_missing_license(
        self, client, velocity_tier, user, db_session
    ):
        from src.domain.project import Project

        resp = client.post(
            "/api/v1/organizations",
            json={"name": "Org For Ticket Test"},
            headers=bearer_for(db_session, user.id),
        )
        assert resp.status_code == 201
        org_id = resp.json()["id"]

        assert is_license_active(org_id, db_session)

        # Ticket.project_id is a required FK -- create a minimal project in
        # the new org so the ticket-creation request has a valid project_id.
        project = Project(
            id=str(uuid4()),
            organization_id=org_id,
            alias=f"T{str(uuid4())[:6]}".upper(),
            name="Test Project",
            description="Test project",
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        ticket_resp = client.post(
            f"/api/v1/organizations/{org_id}/tickets",
            json={
                "summary": "Should not be blocked by a missing license",
                "project_id": project.id,
            },
            headers=bearer_for(db_session, user.id),
        )
        assert ticket_resp.status_code == 200
