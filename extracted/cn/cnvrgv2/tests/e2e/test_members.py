import pytest

from cnvrgv2.cnvrg import Cnvrg
from cnvrgv2.errors import CnvrgHttpError
from cnvrgv2.modules.organization.organizations_client import OrganizationsClient
from cnvrgv2.modules.users import ROLES


class TestMembers:

    def test_revoke_last_member_in_organization_fail(self, e2e_user, domain, e2e_client):
        org_client = OrganizationsClient(domain=domain, token=e2e_client._context.token)
        org = org_client.get(e2e_client._context.organization)
        # run the test if there is only one member in the organization
        if len(org["memberships"]) == 1:
            email = org["memberships"][0]['email'] or org["memberships"][0]['invite_email']
            with pytest.raises(CnvrgHttpError):
                e2e_client.members.get(email).revoke()

    def test_add_membership_for_non_existent_user_success(self, e2e_user, domain, e2e_client):
        email = "nonexistent@user.com"
        e2e_client.members.add(email, ROLES.MANAGER)
        org_client = OrganizationsClient(domain=domain, token=e2e_client._context.token)
        org = org_client.get(e2e_client._context.organization)
        assert not any(user["email"] == email for user in org["memberships"])
        assert any(member["invite_email"] == email for member in org["memberships"])

    def test_add_membership_for_existent_member_fail(self, e2e_user, domain, e2e_client):
        email = "nonexistent2@user.com"
        e2e_client.members.add(email, ROLES.MANAGER)
        # add membership once again for the same user
        with pytest.raises(CnvrgHttpError):
            e2e_client.members.add(email, ROLES.MANAGER)

    def test_get_members(self, domain, e2e_client):
        org_client = OrganizationsClient(domain=domain, token=e2e_client._context.token)
        org = org_client.get(e2e_client._context.organization)
        members = org["memberships"]
        assert len(members) >= 1

    def test_add_member_unauthorized(self, domain, e2e_client, e2e_data_scientist_user):
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )
        email = "nonexistent@user.com"
        with pytest.raises(CnvrgHttpError):
            client_of_non_admin_user.members.add(email, ROLES.MANAGER)

    def test_revoke_member_success(self, e2e_user, domain, e2e_client, e2e_data_scientist_user):
        org_client = OrganizationsClient(domain=domain, token=e2e_client._context.token)
        e2e_client.members.get(e2e_data_scientist_user["email"]).revoke()
        org = org_client.get(e2e_client._context.organization)
        assert not any(user["email"] == e2e_data_scientist_user["email"] for user in org["memberships"])

    def test_revoke_non_existent_member_fail(self, e2e_user, e2e_client):
        with pytest.raises(CnvrgHttpError):
            e2e_client.members.get("nonexistent3@user.com").revoke()
