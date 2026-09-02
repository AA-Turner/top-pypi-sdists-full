"""Adding someone to an organization now makes them a DEVELOPER.

MEMBER was the default everywhere, and MEMBER cannot do the things people are
added in order to do: releases, board sync and ticket writes all require
DEVELOPER or higher. So the default produced accounts that could read everything
and change nothing, and the failure surfaced late and obscurely — `innoday
release` tagged every repository and only then answered "Requires DEVELOPER role
or higher".

MEMBER is still available; it is simply no longer the assumption.
"""

from src.domain.organization import (
    ORGANIZATION_ROLE_RANK,
    OrganizationMembership,
    OrganizationRole,
    role_satisfies,
)
from src.domain.organization_invite import OrganizationInvite
from src.routers.invites import InviteCreate
from src.routers.organizations import MembershipCreate


class TestTheDefaultsAreDeveloper:
    def test_adding_a_member_over_the_api(self):
        assert MembershipCreate(user_id="u").role is OrganizationRole.DEVELOPER

    def test_inviting_someone(self):
        assert InviteCreate(email="a@b.com").role is OrganizationRole.DEVELOPER

    def test_the_invite_row(self):
        assert OrganizationInvite.model_fields["role"].default is (
            OrganizationRole.DEVELOPER
        )

    def test_the_membership_row(self):
        assert OrganizationMembership.model_fields["role"].default is (
            OrganizationRole.DEVELOPER
        )

    def test_the_cli_add_default(self):
        import argparse

        from src.cli.commands.organizations import OrganizationCommands

        parser = argparse.ArgumentParser()
        OrganizationCommands.setup_parser(parser)
        args = parser.parse_args(["members", "--add", "a@b.com"])
        assert args.member_role == "DEVELOPER"

    def test_an_explicit_member_is_still_honoured(self):
        """Read-only people still exist — this is a change of default, not a
        removal of the role."""
        assert (
            MembershipCreate(user_id="u", role=OrganizationRole.MEMBER).role
            is OrganizationRole.MEMBER
        )


class TestTheDefaultActuallyClearsTheGate:
    """A default that still could not cut a release would have fixed nothing."""

    def test_the_new_default_satisfies_the_release_requirement(self):
        assert role_satisfies(
            MembershipCreate(user_id="u").role, OrganizationRole.DEVELOPER
        )

    def test_the_old_default_did_not(self):
        assert not role_satisfies(OrganizationRole.MEMBER, OrganizationRole.DEVELOPER)


class TestWhatDeliberatelyDidNotChange:
    def test_member_still_outranks_nothing_and_is_still_ranked(self):
        """The rank table is not a default — changing it would silently grant
        every existing MEMBER write access rather than changing an assumption."""
        assert ORGANIZATION_ROLE_RANK[OrganizationRole.MEMBER] == 1
        assert ORGANIZATION_ROLE_RANK[OrganizationRole.DEVELOPER] == 2
        assert ORGANIZATION_ROLE_RANK[OrganizationRole.ADMIN] == 3

    def test_member_is_still_an_invitable_role(self):
        assert (
            InviteCreate(email="a@b.com", role=OrganizationRole.MEMBER).role
            is OrganizationRole.MEMBER
        )

    def test_self_registration_is_not_covered_by_this_change(self):
        """Self-registration grants a role to someone adding *themselves* to an
        org that allows it — a different trust boundary from an admin inviting a
        colleague, so it is still MEMBER and left as an explicit decision."""
        import inspect

        from src.routers import invites

        source = inspect.getsource(invites.self_register)
        assert "OrganizationRole.MEMBER" in source
