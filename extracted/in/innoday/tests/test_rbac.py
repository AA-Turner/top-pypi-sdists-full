"""
Tests for RBAC middleware: resolve_organization, get_current_user, verify_org_membership.
"""

from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.user import User, UserRole
from src.middleware.rbac import resolve_organization, verify_org_membership
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_session():
    engine = build_test_engine()
    with Session(engine) as session:
        yield session


@pytest.fixture
def org(db_session):
    o = Organization(
        id=str(uuid4()),
        name="Example Org",
        alias="ex",
    )
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def user(db_session):
    u = User(
        id=str(uuid4()),
        email="karl@example.com",
        full_name="Karl H",
        role=UserRole.MEMBER,
        is_platform_member=False,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def platform_user(db_session):
    u = User(
        id=str(uuid4()),
        email="admin@innoday.io",
        full_name="Platform Admin",
        role=UserRole.ADMIN,
        is_platform_member=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


class TestResolveOrganization:
    def test_resolve_by_uuid(self, db_session, org):
        result = resolve_organization(org.id, db_session)
        assert result.id == org.id

    def test_resolve_by_alias(self, db_session, org):
        result = resolve_organization("ex", db_session)
        assert result.id == org.id

    def test_raises_404_for_unknown_ref(self, db_session):
        with pytest.raises(HTTPException) as exc_info:
            resolve_organization("nonexistent", db_session)
        assert exc_info.value.status_code == 404


class TestVerifyOrgMembership:
    def test_active_member_passes(self, db_session, org, user):
        membership = OrganizationMembership(
            user_id=user.id,
            organization_id=org.id,
            role=OrganizationRole.MEMBER,
            is_active=True,
        )
        db_session.add(membership)
        db_session.commit()

        result = verify_org_membership(user.id, org.id, db_session)
        assert result.user_id == user.id

    def test_non_member_raises_403(self, db_session, org, user):
        with pytest.raises(HTTPException) as exc_info:
            verify_org_membership(user.id, org.id, db_session)
        assert exc_info.value.status_code == 403

    def test_inactive_member_raises_403(self, db_session, org, user):
        membership = OrganizationMembership(
            user_id=user.id,
            organization_id=org.id,
            role=OrganizationRole.MEMBER,
            is_active=False,
        )
        db_session.add(membership)
        db_session.commit()

        with pytest.raises(HTTPException) as exc_info:
            verify_org_membership(user.id, org.id, db_session)
        assert exc_info.value.status_code == 403

    def test_platform_member_bypasses_membership_check(
        self, db_session, org, platform_user
    ):
        # No membership row exists — platform member should still get synthesized ADMIN membership
        result = verify_org_membership(platform_user.id, org.id, db_session)
        assert result.role == OrganizationRole.ADMIN
        assert result.is_active is True

    def test_platform_member_bypass_on_any_org(self, db_session, platform_user):
        # Even for orgs the platform member has never interacted with
        other_org_id = str(uuid4())
        result = verify_org_membership(platform_user.id, other_org_id, db_session)
        assert result.role == OrganizationRole.ADMIN

    def test_role_check_passes_for_correct_role(self, db_session, org, user):
        membership = OrganizationMembership(
            user_id=user.id,
            organization_id=org.id,
            role=OrganizationRole.ADMIN,
            is_active=True,
        )
        db_session.add(membership)
        db_session.commit()

        result = verify_org_membership(
            user.id, org.id, db_session, required_role=OrganizationRole.ADMIN
        )
        assert result.role == OrganizationRole.ADMIN

    def test_role_check_raises_403_for_wrong_role(self, db_session, org, user):
        membership = OrganizationMembership(
            user_id=user.id,
            organization_id=org.id,
            role=OrganizationRole.MEMBER,
            is_active=True,
        )
        db_session.add(membership)
        db_session.commit()

        with pytest.raises(HTTPException) as exc_info:
            verify_org_membership(
                user.id, org.id, db_session, required_role=OrganizationRole.ADMIN
            )
        assert exc_info.value.status_code == 403
