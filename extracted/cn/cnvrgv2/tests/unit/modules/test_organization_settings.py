from cnvrgv2.modules.organization.organization_settings import OrganizationSettings
from cnvrgv2.proxy import Proxy


class TestOrganizationSettings:

    def test_save_organization_settings(self, mocker, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        organization_settings = OrganizationSettings(organization=empty_cnvrg)

        mocked_save = mocker.patch.object(Proxy, 'call_api')
        organization_settings.save()
        assert mocked_save.call_count == 1
