"""
Tests for LicenseTier canonical product names (PF-160).

Covers the LicenseTier model and /tiers endpoints for the four canonical
tier names: guidance, spark, sprint, velocity.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.license import LicenseTier
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
def license_tiers(db_session):
    """Seed the four canonical license tiers."""
    guidance = LicenseTier(
        id=str(uuid4()),
        name="guidance",
        display_name="Guidance",
        max_users=2,
        max_boards=1,
        daily_ticket_limit=25,
        api_rate_limit=60,
    )
    spark = LicenseTier(
        id=str(uuid4()),
        name="spark",
        display_name="Spark",
        max_users=5,
        max_boards=1,
        daily_ticket_limit=100,
        api_rate_limit=300,
    )
    sprint = LicenseTier(
        id=str(uuid4()),
        name="sprint",
        display_name="Sprint",
        max_users=15,
        max_boards=5,
        daily_ticket_limit=500,
        api_rate_limit=1000,
    )
    velocity = LicenseTier(
        id=str(uuid4()),
        name="velocity",
        display_name="Velocity",
        max_users=None,
        max_boards=None,
        daily_ticket_limit=None,
        api_rate_limit=None,
    )

    for tier in (guidance, spark, sprint, velocity):
        db_session.add(tier)
    db_session.commit()

    for tier in (guidance, spark, sprint, velocity):
        db_session.refresh(tier)

    return {
        "guidance": guidance,
        "spark": spark,
        "sprint": sprint,
        "velocity": velocity,
    }


class TestLicenseTierModel:
    def test_license_tier_model_accepts_new_names(self, db_session, license_tiers):
        for name in ("guidance", "spark", "sprint", "velocity"):
            assert license_tiers[name].name == name

    def test_get_limit_helper_reflects_seeded_values(self, license_tiers):
        assert license_tiers["guidance"].get_limit("users") == 2
        assert license_tiers["spark"].get_limit("daily_tickets") == 100
        assert license_tiers["sprint"].get_limit("boards") == 5
        assert license_tiers["velocity"].get_limit("api_calls") is None


class TestLicenseTierEndpoints:
    def test_tiers_endpoint_returns_new_names(self, client, license_tiers):
        response = client.get("/tiers")

        assert response.status_code == 200
        names = {tier["name"] for tier in response.json()}
        assert names == {"guidance", "spark", "sprint", "velocity"}

    def test_get_tier_by_name(self, client, license_tiers):
        response = client.get("/tiers/velocity")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "velocity"
        assert data["display_name"] == "Velocity"
        assert data["max_users"] is None

    @pytest.mark.parametrize(
        "old_name,expected_new_name",
        [("pro", "spark"), ("max", "sprint"), ("unlimited", "velocity")],
    )
    def test_get_tier_by_old_name_resolves_via_alias(
        self, client, license_tiers, old_name, expected_new_name
    ):
        """Legacy tier names are aliased -- they should return 200 with the mapped tier."""
        response = client.get(f"/tiers/{old_name}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == expected_new_name
