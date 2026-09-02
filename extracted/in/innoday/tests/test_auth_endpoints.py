"""Tests for GET /api/v1/auth/me and GET /api/v1/auth/users/{user_id}/organizations.

Both endpoints previously depended on get_current_user_from_api_key, which
requires a Bearer token minted via POST /api-keys into an in-memory
api_keys_store -- wiped on every server restart, and never obtained by any
CLI code path (the CLI only ever sends X-User-ID/X-Team-Secret headers, the
same mechanism every other route uses via get_current_user in
src/middleware/rbac.py). Confirmed live: `innoday config init`'s "which
organizations do you belong to" step always reported "No organizations
found for this user" for a real user with real active memberships, because
the underlying request always 401'd.

Fixed by switching both endpoints to get_current_user (X-User-ID header),
matching every other route in the app.
"""

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
from src.domain.user import User, UserRole
from src.domain.user_identity import IdentityPlatform, UserIdentity
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
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def user_with_orgs(db_engine):
    with Session(db_engine) as session:
        user = User(
            id=str(uuid4()),
            email="karl@example.com",
            full_name="Karl Haviland",
            role=UserRole.MEMBER,
        )
        session.add(user)

        org_a = Organization(id=str(uuid4()), name="Bright Power", alias="bp")
        org_b = Organization(id=str(uuid4()), name="Haviland Software", alias="hs")
        session.add(org_a)
        session.add(org_b)
        session.commit()

        for org in (org_a, org_b):
            session.add(
                OrganizationMembership(
                    id=str(uuid4()),
                    user_id=user.id,
                    organization_id=org.id,
                    role=OrganizationRole.ADMIN,
                    is_active=True,
                )
            )
        session.commit()
        session.refresh(user)
        return user, [org_a, org_b]


class TestGetCurrentUserProfile:
    def test_returns_profile_with_organizations_via_x_user_id_header(
        self, client, user_with_orgs, db_engine
    ):
        user, orgs = user_with_orgs

        response = client.get(
            "/api/v1/auth/me", headers=bearer_for_engine(db_engine, user.id)
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "karl@example.com"
        assert len(data["organizations"]) == 2
        assert {o["alias"] for o in data["organizations"]} == {"bp", "hs"}

    def test_missing_x_user_id_header_returns_401(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestGetUserOrganizations:
    def test_returns_real_memberships_via_x_user_id_header(
        self, client, user_with_orgs, db_engine
    ):
        user, orgs = user_with_orgs

        response = client.get(
            f"/api/v1/auth/users/{user.id}/organizations",
            headers=bearer_for_engine(db_engine, user.id),
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert {o["alias"] for o in data} == {"bp", "hs"}
        assert all(o["role"] == OrganizationRole.ADMIN for o in data)

    def test_requesting_another_users_organizations_is_denied(
        self, client, user_with_orgs, db_engine
    ):
        user, _ = user_with_orgs
        other_user_id = str(uuid4())

        response = client.get(
            f"/api/v1/auth/users/{other_user_id}/organizations",
            headers=bearer_for_engine(db_engine, user.id),
        )

        assert response.status_code == 403

    def test_missing_x_user_id_header_returns_401(self, client, user_with_orgs):
        user, _ = user_with_orgs
        response = client.get(f"/api/v1/auth/users/{user.id}/organizations")
        assert response.status_code == 401


class TestProfileIdentities:
    """`/auth/me` reports the caller's board handles (PF-398).

    Added to this route rather than a new one: "which handles are me?" is part
    of who you are, it is only ever asked about yourself, and every client
    already calls `/auth/me` to find that out. `innoday summary` needs it to
    tell a quiet window apart from an unrecognised caller -- two identical
    empty results, only one of which the user can do anything about.
    """

    def test_absent_mappings_are_an_empty_list_not_a_missing_key(
        self, client, user_with_orgs, db_engine
    ):
        user, _ = user_with_orgs
        response = client.get(
            "/api/v1/auth/me", headers=bearer_for_engine(db_engine, user.id)
        )
        assert response.status_code == 200
        assert response.json()["identities"] == []

    def test_reports_platform_handle_and_scope(self, client, user_with_orgs, db_engine):
        user, _ = user_with_orgs
        with Session(db_engine) as session:
            org = session.exec(
                select(Organization).where(Organization.alias == "hs")
            ).one()
            project = Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias="PF",
                name="PixelFuel",
                description="",
            )
            session.add(project)
            session.add(
                UserIdentity(
                    user_id=user.id,
                    project_id=project.id,
                    platform=IdentityPlatform.LINEAR,
                    handle="Karl H",
                )
            )
            session.add(
                UserIdentity(
                    user_id=user.id,
                    platform=IdentityPlatform.GITHUB,
                    handle="havkarl",
                )
            )
            session.commit()

        response = client.get(
            "/api/v1/auth/me", headers=bearer_for_engine(db_engine, user.id)
        )
        identities = {i["handle"]: i for i in response.json()["identities"]}

        assert identities["havkarl"]["platform"] == "github"
        # NULL project_id is the *global* handle, not missing data.
        assert identities["havkarl"]["scope"] == "global"
        assert identities["havkarl"]["project"] is None

        assert identities["Karl H"]["scope"] == "project"
        assert identities["Karl H"]["project"] == "PF"

    def test_only_the_callers_own_mappings_are_returned(
        self, client, user_with_orgs, db_engine
    ):
        user, _ = user_with_orgs
        with Session(db_engine) as session:
            other = User(
                id=str(uuid4()),
                email="someone@example.com",
                full_name="Someone Else",
                role=UserRole.MEMBER,
            )
            session.add(other)
            session.commit()
            session.add(
                UserIdentity(
                    user_id=other.id,
                    platform=IdentityPlatform.GITHUB,
                    handle="not-me",
                )
            )
            session.commit()

        response = client.get(
            "/api/v1/auth/me", headers=bearer_for_engine(db_engine, user.id)
        )
        assert response.json()["identities"] == []


class TestClaimMyIdentity:
    """`PUT /auth/me/identities` — the write half, self-only (PF-398).

    Its whole reason for existing is that a personal summary was unreachable
    without a browser: the only mapping form lived at `/ui/<org>/profile`, so
    the CLI printed a fix it could not perform.
    """

    @staticmethod
    def _project(db_engine, *, org_alias="hs", alias="BPAI", name="Bright Power AI"):
        with Session(db_engine) as session:
            org = session.exec(
                select(Organization).where(Organization.alias == org_alias)
            ).one()
            project = Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias=alias,
                name=name,
                description="",
            )
            session.add(project)
            session.commit()
            return project.id, org.id

    def test_a_project_alias_resolves_the_same_as_its_id(
        self, client, user_with_orgs, db_engine
    ):
        """`--project BPAI` must work, not only `--project <uuid>`.

        The CLI's `--project` takes the alias everywhere else, so a route that
        accepted only a UUID answered "Project not found" for a project the
        caller administers — while the identical command run from inside that
        project's directory succeeded, because the cwd resolves to an id.
        """
        user, _ = user_with_orgs
        self._project(db_engine)

        response = client.put(
            "/api/v1/auth/me/identities",
            headers=bearer_for_engine(db_engine, user.id),
            json={"project_id": "BPAI", "platform": "github", "handle": "havkarl"},
        )

        assert response.status_code == 200
        identities = {i["handle"]: i for i in response.json()["identities"]}
        assert identities["havkarl"]["project"] == "BPAI"
        assert identities["havkarl"]["scope"] == "project"

    def test_a_project_id_still_resolves(self, client, user_with_orgs, db_engine):
        user, _ = user_with_orgs
        project_id, _ = self._project(db_engine)

        response = client.put(
            "/api/v1/auth/me/identities",
            headers=bearer_for_engine(db_engine, user.id),
            json={"project_id": project_id, "platform": "linear", "handle": "Karl H"},
        )

        assert response.status_code == 200

    def test_claiming_replaces_the_callers_previous_handle_on_that_platform(
        self, client, user_with_orgs, db_engine
    ):
        """One handle per person per platform per project — the old one goes.

        Same rule the profile page enforces. Two live handles for one person on
        one board would make the resolver's answer depend on row order.
        """
        user, _ = user_with_orgs
        self._project(db_engine)
        headers = bearer_for_engine(db_engine, user.id)

        client.put(
            "/api/v1/auth/me/identities",
            headers=headers,
            json={"project_id": "BPAI", "platform": "github", "handle": "old-login"},
        )
        response = client.put(
            "/api/v1/auth/me/identities",
            headers=headers,
            json={"project_id": "BPAI", "platform": "github", "handle": "new-login"},
        )

        assert response.status_code == 200
        handles = {
            i["handle"]
            for i in response.json()["identities"]
            if i["platform"] == "github"
        }
        assert handles == {"new-login"}

    def test_a_handle_another_user_holds_is_refused_not_stolen(
        self, client, user_with_orgs, db_engine
    ):
        user, _ = user_with_orgs
        project_id, org_id = self._project(db_engine)
        with Session(db_engine) as session:
            other = User(
                id=str(uuid4()),
                email="them@example.com",
                full_name="Them",
                role=UserRole.MEMBER,
            )
            session.add(other)
            session.commit()
            session.add(
                OrganizationMembership(
                    id=str(uuid4()),
                    user_id=other.id,
                    organization_id=org_id,
                    role=OrganizationRole.MEMBER,
                    is_active=True,
                )
            )
            session.add(
                UserIdentity(
                    user_id=other.id,
                    project_id=project_id,
                    platform=IdentityPlatform.GITHUB,
                    handle="taken",
                )
            )
            session.commit()

        response = client.put(
            "/api/v1/auth/me/identities",
            headers=bearer_for_engine(db_engine, user.id),
            json={"project_id": "BPAI", "platform": "github", "handle": "taken"},
        )

        assert response.status_code == 409

    def test_a_project_in_an_org_the_caller_is_not_in_is_a_404(
        self, client, user_with_orgs, db_engine
    ):
        """404, deliberately, not 403.

        A distinguishable 403 would confirm that another tenant's project
        exists, so an unauthorized project and an absent one must look the
        same from outside.
        """
        user, _ = user_with_orgs
        with Session(db_engine) as session:
            stranger_org = Organization(
                id=str(uuid4()), name="Stranger Co", alias="stranger"
            )
            session.add(stranger_org)
            session.commit()
            session.add(
                Project(
                    id=str(uuid4()),
                    organization_id=stranger_org.id,
                    alias="SECRET",
                    name="Secret Project",
                    description="",
                )
            )
            session.commit()

        response = client.put(
            "/api/v1/auth/me/identities",
            headers=bearer_for_engine(db_engine, user.id),
            json={"project_id": "SECRET", "platform": "github", "handle": "havkarl"},
        )

        assert response.status_code == 404

    def test_an_unknown_platform_is_a_422_that_lists_the_real_ones(
        self, client, user_with_orgs, db_engine
    ):
        user, _ = user_with_orgs
        self._project(db_engine)

        response = client.put(
            "/api/v1/auth/me/identities",
            headers=bearer_for_engine(db_engine, user.id),
            json={"project_id": "BPAI", "platform": "bitbucket", "handle": "x"},
        )

        assert response.status_code == 422
        assert "github" in response.json()["detail"]

    def test_a_blank_handle_is_refused(self, client, user_with_orgs, db_engine):
        user, _ = user_with_orgs
        self._project(db_engine)

        response = client.put(
            "/api/v1/auth/me/identities",
            headers=bearer_for_engine(db_engine, user.id),
            json={"project_id": "BPAI", "platform": "github", "handle": "   "},
        )

        assert response.status_code == 422
