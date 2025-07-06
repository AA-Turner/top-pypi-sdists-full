import pytest

from cnvrgv2.errors import CnvrgHttpError
from cnvrgv2.modules.organization.organizations_client import OrganizationsClient
from tests.e2e.conftest import call_database


class TestOrganizations:
    @staticmethod
    def cleanup(context_prefix):
        # TODO: This doesnt cleanup all of the organization clusters and stuff.
        delete_user_command = "DELETE FROM organizations WHERE slug LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    def test_create_organization(self, class_context, domain, e2e_user):
        org_name = class_context.generate_name(5)
        oc = OrganizationsClient(domain=domain, token=e2e_user["token"])
        sample_org = oc.create(name=org_name)
        assert sample_org["slug"] == org_name

    def test_create_duplicate_organization(self, class_context, domain, e2e_user):
        org_name = class_context.generate_name(5)
        oc = OrganizationsClient(domain=domain, token=e2e_user["token"])
        sample_org = oc.create(name=org_name)
        assert sample_org["slug"] == org_name

        with pytest.raises(CnvrgHttpError) as exception_info:
            oc.create(name=org_name)

        assert "exists" in str(exception_info.value)

    def test_create_organization_bad_name(self, class_context, domain, e2e_user):
        org_name = class_context.generate_name(5) + "-bad"
        oc = OrganizationsClient(domain=domain, token=e2e_user["token"])

        with pytest.raises(CnvrgHttpError) as exception_info:
            oc.create(name=org_name)

        assert "invalid title" in str(exception_info.value)

    def test_get_organization(self, class_context, domain, e2e_user):
        org_name = class_context.generate_name(5)
        oc = OrganizationsClient(domain=domain, token=e2e_user["token"])
        oc.create(name=org_name)

        sample_org = oc.get(slug=org_name)

        assert sample_org["slug"] == org_name

    def test_get_non_existent_organization(self, class_context, domain, e2e_user):
        org_name = class_context.generate_name(5)
        oc = OrganizationsClient(domain=domain, token=e2e_user["token"])

        with pytest.raises(CnvrgHttpError) as exception_info:
            oc.get(slug=org_name)

        assert "found" in str(exception_info.value)
