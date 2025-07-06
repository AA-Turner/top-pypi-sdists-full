import pytest

from cnvrgv2.cnvrg import Cnvrg
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.organization.organizations_client import OrganizationsClient
from cnvrgv2.modules.users import ROLES
from cnvrgv2.modules.users.users_client import UsersClient
from tests.e2e.conftest import call_database


class TestCnvrg:
    @staticmethod
    def cleanup(context_prefix):
        delete_user_command = "DELETE FROM organizations WHERE slug LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    def test_me(self, domain, e2e_client):
        user_mail = e2e_client._context.user
        ret_user = e2e_client.me()
        assert ret_user.email == user_mail

    def test_switch_organizations(self, class_context, domain, e2e_client):
        alter_org = class_context.generate_name(5)
        original_org_proj = class_context.prefix + "orig-proj"
        alter_org_proj = class_context.prefix + "alter-proj"

        oc = OrganizationsClient(domain=domain, token=e2e_client._context.token)
        oc.create(alter_org)

        e2e_client.projects.create(name=original_org_proj)
        assert e2e_client.projects.get(original_org_proj).slug == original_org_proj

        e2e_client.set_organization(alter_org)
        e2e_client.projects.create(alter_org_proj)

        assert e2e_client._context.organization == alter_org
        assert e2e_client.projects.get(alter_org_proj).slug == alter_org_proj

    def test_get_users(self, domain, e2e_client, class_context):
        # e2e_client has at least 2 users here: 1 added when its created,
        # 2nd is created in this test
        username = class_context.generate_name(5)
        email = username + "@cnvrg.io"
        password = "qwe123"
        uc = UsersClient(domain=domain)
        uc.register(username=username, email=email, password=password)
        e2e_client.members.add(email=email, role=ROLES.MEMBER)
        users = e2e_client.get_users()
        assert len(users) > 1

    def test_get_users_unauthorized(self, domain, e2e_client, e2e_data_scientist_user):
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )
        with pytest.raises(CnvrgError) as exception_info:
            client_of_non_admin_user.get_users()

        assert 'unauthorized' in str(exception_info.value).lower()
