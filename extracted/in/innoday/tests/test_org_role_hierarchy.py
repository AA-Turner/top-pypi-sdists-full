"""Org roles rank, so a required role is a minimum rather than an exact match.

`verify_org_membership` compared `membership.role != required_role`. Because
`OrganizationRole` is an unordered str Enum, a route asking for DEVELOPER **refused an
ADMIN** — 9 routes (7 board, 2 release) locked org admins out of board sync, while six
ticket routes hand-rolled `if membership.role not in (DEVELOPER, ADMIN)` because
equality could not express "either".

These tests pin the ranking so a future edit to the enum can't silently change access.
"""

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from src.domain.organization import (
    OrganizationMembership,
    OrganizationRole,
    role_satisfies,
)
from src.domain.user import User
from src.middleware.rbac import verify_org_membership

ALL_ROLES = [
    OrganizationRole.MEMBER,
    OrganizationRole.DEVELOPER,
    OrganizationRole.ADMIN,
]


class TestRoleSatisfies:
    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_a_role_satisfies_itself(self, role):
        assert role_satisfies(role, role)

    def test_admin_outranks_developer_and_member(self):
        assert role_satisfies(OrganizationRole.ADMIN, OrganizationRole.DEVELOPER)
        assert role_satisfies(OrganizationRole.ADMIN, OrganizationRole.MEMBER)

    def test_developer_outranks_member_but_not_admin(self):
        assert role_satisfies(OrganizationRole.DEVELOPER, OrganizationRole.MEMBER)
        assert not role_satisfies(OrganizationRole.DEVELOPER, OrganizationRole.ADMIN)

    def test_member_outranks_nothing(self):
        assert not role_satisfies(OrganizationRole.MEMBER, OrganizationRole.DEVELOPER)
        assert not role_satisfies(OrganizationRole.MEMBER, OrganizationRole.ADMIN)

    def test_ranking_is_declared_not_inherited_from_enum_order(self):
        """The enum declares MEMBER, ADMIN, DEVELOPER — deliberately not the ranking.

        If the rank were derived from definition order, DEVELOPER would outrank ADMIN.
        """
        from src.domain.organization import ORGANIZATION_ROLE_RANK

        assert (
            ORGANIZATION_ROLE_RANK[OrganizationRole.ADMIN]
            > ORGANIZATION_ROLE_RANK[OrganizationRole.DEVELOPER]
        )
        assert list(OrganizationRole) != sorted(
            OrganizationRole, key=lambda r: ORGANIZATION_ROLE_RANK[r]
        )


def _member(session: Session, org, role: OrganizationRole) -> User:
    user = User(email=f"{role.value.lower()}@example.com", full_name=role.value)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.add(
        OrganizationMembership(
            user_id=user.id, organization_id=org.id, role=role, is_active=True
        )
    )
    session.commit()
    return user


class TestVerifyOrgMembershipUsesTheRanking:
    """The regression that matters: an ADMIN must pass a DEVELOPER gate."""

    def test_admin_passes_a_developer_gate(self, db_session, org):
        admin = _member(db_session, org, OrganizationRole.ADMIN)
        m = verify_org_membership(
            admin.id, org.id, db_session, required_role=OrganizationRole.DEVELOPER
        )
        assert m.role == OrganizationRole.ADMIN

    def test_developer_passes_a_developer_gate(self, db_session, org):
        dev = _member(db_session, org, OrganizationRole.DEVELOPER)
        assert verify_org_membership(
            dev.id, org.id, db_session, required_role=OrganizationRole.DEVELOPER
        )

    def test_member_is_refused_a_developer_gate(self, db_session, org):
        plain = _member(db_session, org, OrganizationRole.MEMBER)
        with pytest.raises(HTTPException) as exc:
            verify_org_membership(
                plain.id, org.id, db_session, required_role=OrganizationRole.DEVELOPER
            )
        assert exc.value.status_code == 403
        assert "or higher" in exc.value.detail

    def test_developer_is_refused_an_admin_gate(self, db_session, org):
        """The ranking must not collapse into "any member will do"."""
        dev = _member(db_session, org, OrganizationRole.DEVELOPER)
        with pytest.raises(HTTPException) as exc:
            verify_org_membership(
                dev.id, org.id, db_session, required_role=OrganizationRole.ADMIN
            )
        assert exc.value.status_code == 403

    def test_no_required_role_admits_any_member(self, db_session, org):
        plain = _member(db_session, org, OrganizationRole.MEMBER)
        assert verify_org_membership(plain.id, org.id, db_session)

    def test_non_member_is_still_refused(self, db_session, org):
        outsider = User(email="outsider@example.com", full_name="Outsider")
        db_session.add(outsider)
        db_session.commit()
        db_session.refresh(outsider)
        with pytest.raises(HTTPException) as exc:
            verify_org_membership(outsider.id, org.id, db_session)
        assert exc.value.status_code == 403
        assert "not a member" in exc.value.detail

    def test_platform_member_still_bypasses_entirely(self, db_session, org):
        """Platform staff get a synthesised ADMIN membership with no row at all."""
        staff = User(
            email="staff@havilandsoftware.com",
            full_name="Staff",
            is_platform_member=True,
        )
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)

        m = verify_org_membership(
            staff.id, org.id, db_session, required_role=OrganizationRole.ADMIN
        )
        assert m.role == OrganizationRole.ADMIN
        assert m.organization_id == org.id
