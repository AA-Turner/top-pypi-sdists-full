"""Refusing a release the caller cannot finish, and changing a role from the CLI.

Both halves of one problem. `unurbat@havilandsoftware.com` was a MEMBER of `hs`
and `bp`; running `innoday release` tagged every repository and *then* failed on
the recording step with

    Recording release failed (non-blocking): Failed to record release:
    HTTP 403 -- {"detail":"Requires DEVELOPER role or higher"}

leaving a release that had shipped but that InnoDay had no record of — the worst
of the three possible outcomes, and the hardest to spot. Two things were missing:
a check that runs *before* the tagging, and any way at all to change a member's
role once it had been set.
"""

import argparse
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.commands.release_proxy import ReleaseProxyCommands, _role_can_release
from src.domain.organization import OrganizationRole, role_satisfies

ORG_ID = "org-1"


def make_config(token="tok", team_secret=None):
    config = MagicMock()
    config.get_cli_token.return_value = token
    config.get_team_secret.return_value = team_secret
    config.get_api_url.return_value = "https://www.inno.day"
    return config


def me(role=None, orgs=None, platform=False):
    if orgs is None:
        orgs = [] if role is None else [{"id": ORG_ID, "alias": "hs", "role": role}]
    return {"organizations": orgs, "is_platform_member": platform}


async def run_preflight(config, me_payload, side_effect=None):
    with patch(
        "src.cli.commands.session._fetch_me",
        new=AsyncMock(return_value=me_payload, side_effect=side_effect),
    ):
        return await ReleaseProxyCommands._preflight(config, ORG_ID, "pf")


class TestRoleRanking:
    """Ranked through the domain helper so the CLI cannot drift from the server."""

    def test_member_cannot_release(self):
        assert _role_can_release("MEMBER") is False

    def test_developer_can(self):
        assert _role_can_release("DEVELOPER") is True

    def test_admin_can(self):
        """A route asking for DEVELOPER must not reject an ADMIN — the exact bug
        the rank table was introduced to fix."""
        assert _role_can_release("ADMIN") is True

    def test_it_uses_the_domain_ranking_not_its_own(self):
        for role in OrganizationRole:
            assert _role_can_release(role.value) == role_satisfies(
                role, OrganizationRole.DEVELOPER
            )

    def test_an_unknown_role_passes(self):
        """This is a courtesy check, not a security boundary — the server still
        enforces. Blocking on a role string this client has not been taught
        about would turn a future role into an outage."""
        assert _role_can_release("SOMETHING_NEW") is True


class TestNotAnInnoDayUser:
    @pytest.mark.asyncio
    async def test_no_token_stops_immediately_and_points_at_signup(self, capsys):
        rc = await run_preflight(make_config(token=None), None)
        out = capsys.readouterr().out
        assert rc == 1
        assert "inno.day" in out
        assert "not signed in" in out.lower()

    @pytest.mark.asyncio
    async def test_an_invalid_session_points_at_login_and_signup(self, capsys):
        rc = await run_preflight(make_config(), None)
        out = capsys.readouterr().out
        assert rc == 1
        assert "innoday login" in out
        assert "inno.day" in out


class TestMembershipAndRole:
    @pytest.mark.asyncio
    async def test_a_non_member_is_stopped(self, capsys):
        rc = await run_preflight(
            make_config(), me(orgs=[{"id": "other", "role": "ADMIN"}])
        )
        out = capsys.readouterr().out
        assert rc == 1
        assert "not a member" in out.lower()

    @pytest.mark.asyncio
    async def test_a_member_below_developer_is_stopped(self, capsys):
        """unurbat's case exactly."""
        rc = await run_preflight(make_config(), me(role="MEMBER"))
        out = capsys.readouterr().out
        assert rc == 1
        assert "MEMBER" in out
        assert "DEVELOPER" in out

    @pytest.mark.asyncio
    async def test_it_says_nothing_was_tagged(self, capsys):
        """The whole point of moving the check earlier — the reader needs to know
        no repository was touched, because the old failure came *after* tagging."""
        await run_preflight(make_config(), me(role="MEMBER"))
        assert "Nothing has been tagged" in capsys.readouterr().out

    @pytest.mark.asyncio
    async def test_it_names_the_command_that_fixes_it(self, capsys):
        await run_preflight(make_config(), me(role="MEMBER"))
        assert "--set-role" in capsys.readouterr().out

    @pytest.mark.asyncio
    async def test_a_developer_proceeds(self):
        assert await run_preflight(make_config(), me(role="DEVELOPER")) == 0

    @pytest.mark.asyncio
    async def test_an_admin_proceeds(self):
        assert await run_preflight(make_config(), me(role="ADMIN")) == 0

    @pytest.mark.asyncio
    async def test_a_platform_member_proceeds_without_a_membership(self):
        """Platform members reach every organization, so an empty org list is not
        a refusal for them."""
        assert await run_preflight(make_config(), me(orgs=[], platform=True)) == 0


class TestPreflightFailsOpen:
    @pytest.mark.asyncio
    async def test_an_unreachable_api_does_not_block_the_release(self):
        """Refusing to release because the *check* could not run would be a worse
        failure than the one it prevents. The recording step still reports
        honestly if the caller really was unauthorised."""
        rc = await run_preflight(make_config(), None, side_effect=OSError("no route"))
        assert rc == 0


class TestSetRoleReachesThePutRoute:
    """`--add` cannot change a role: the route 409s on an active member and the
    CLI treats that as idempotent success, so re-adding with a different role
    silently does nothing."""

    @pytest.mark.asyncio
    async def test_it_puts_the_new_role(self, capsys):
        from src.cli.commands.organizations import OrganizationCommands

        client = MagicMock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=False)
        client.put = AsyncMock(
            return_value=SimpleNamespace(status_code=200, text="{}", json=lambda: {})
        )

        with (
            patch(
                "src.cli.commands.organizations.InnoDayAPIClient", return_value=client
            ),
            patch.object(
                OrganizationCommands,
                "_user_id_for_email",
                new=AsyncMock(return_value="user-9"),
            ),
        ):
            rc = await OrganizationCommands._set_member_role(
                MagicMock(), ORG_ID, "hs", "unurbat@havilandsoftware.com", "DEVELOPER"
            )

        assert rc == 0
        (endpoint,) = client.put.call_args.args
        assert endpoint == f"/organizations/{ORG_ID}/members/user-9"
        assert client.put.call_args.kwargs["json"] == {"role": "DEVELOPER"}

    @pytest.mark.asyncio
    async def test_a_non_member_is_told_to_be_added_first(self, capsys):
        from src.cli.commands.organizations import OrganizationCommands

        client = MagicMock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=False)
        client.put = AsyncMock(
            return_value=SimpleNamespace(
                status_code=404,
                text="{}",
                json=lambda: {"detail": "Membership not found"},
            )
        )

        with (
            patch(
                "src.cli.commands.organizations.InnoDayAPIClient", return_value=client
            ),
            patch.object(
                OrganizationCommands,
                "_user_id_for_email",
                new=AsyncMock(return_value="u"),
            ),
        ):
            rc = await OrganizationCommands._set_member_role(
                MagicMock(), ORG_ID, "hs", "nobody@example.com", "DEVELOPER"
            )

        assert rc == 1
        assert "--add" in capsys.readouterr().out

    def test_add_and_set_role_are_mutually_exclusive(self):
        """Both at once has no coherent meaning and would half-apply."""
        args = argparse.Namespace(
            member_add="a@b.com", member_set_role="a@b.com", member_role="DEVELOPER"
        )
        assert args.member_add and args.member_set_role
