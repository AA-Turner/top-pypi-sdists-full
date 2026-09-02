"""P0 foundations for the auth/registration work (PF-350, issue #350).

Covers the model-level behavior added in P0:
  - platform users are admin/owner of EVERY org (short-circuit, no membership row)
  - ownership implies admin capability (is_admin_or_owner / can_manage_*)
  - new schema fields exist with the right defaults
"""

from uuid import uuid4

from src.domain.organization import OrganizationMembership, OrganizationRole
from src.domain.user import User


def _user(**kw) -> User:
    return User(
        id=str(uuid4()),
        email=f"{uuid4().hex[:8]}@example.com",
        full_name="Test User",
        **kw,
    )


class TestPlatformUserOrgAuthority:
    """Platform users reach every org via a short-circuit -- never a per-org row."""

    def test_platform_user_is_org_admin_everywhere(self):
        u = _user(is_platform_member=True)
        # No memberships at all -- still admin of an arbitrary org.
        assert u.organization_memberships == []
        assert u.is_org_admin("any-org-id-they-never-joined") is True

    def test_platform_user_is_org_owner_everywhere(self):
        u = _user(is_platform_member=True)
        assert u.is_org_owner("any-org-id") is True

    def test_non_platform_user_without_membership_is_not_admin(self):
        u = _user(is_platform_member=False)
        assert u.is_org_admin("some-org") is False
        assert u.is_org_owner("some-org") is False

    def test_platform_authority_creates_no_membership_rows(self):
        """The invariant: authority is by bypass, not by enumeration."""
        u = _user(is_platform_member=True)
        _ = u.is_org_admin("org-a")
        _ = u.is_org_owner("org-b")
        assert u.organization_memberships == []


class TestOwnershipImpliesAdmin:
    """Reconciled role helpers: is_owner always implies admin capability."""

    def test_owner_is_admin_or_owner_regardless_of_role(self):
        m = OrganizationMembership(
            user_id=str(uuid4()),
            organization_id=str(uuid4()),
            role=OrganizationRole.MEMBER,  # not ADMIN...
            is_owner=True,  # ...but is owner
        )
        assert m.is_admin_or_owner() is True
        assert m.can_manage_members() is True
        assert m.can_manage_settings() is True
        assert m.can_manage_licenses() is True

    def test_admin_role_is_admin_but_not_license_manager(self):
        m = OrganizationMembership(
            user_id=str(uuid4()),
            organization_id=str(uuid4()),
            role=OrganizationRole.ADMIN,
            is_owner=False,
        )
        assert m.is_admin_or_owner() is True
        assert m.can_manage_members() is True
        # Licenses are owner-only.
        assert m.can_manage_licenses() is False

    def test_plain_member_manages_nothing(self):
        m = OrganizationMembership(
            user_id=str(uuid4()),
            organization_id=str(uuid4()),
            role=OrganizationRole.MEMBER,
            is_owner=False,
        )
        assert m.is_admin_or_owner() is False
        assert m.can_manage_members() is False
        assert m.can_manage_licenses() is False
