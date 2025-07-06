import pytest

from cnvrgv2.cnvrg import Cnvrg
from cnvrgv2.errors import CnvrgError, CnvrgHttpError


class TestOrganizationSettings:
    def test_get_settings_success(self, e2e_client):
        assert e2e_client.settings.default_computes
        assert e2e_client.settings.debug_time
        assert e2e_client.settings.max_duration_workspaces

    def test_save_settings_success(self, e2e_client):
        # Test with getattr (that fetches data from server) first
        assert e2e_client.settings.debug_time

        e2e_client.settings.debug_time = 50
        e2e_client.settings.save()

        e2e_client.settings._attributes = {}
        assert e2e_client.settings.debug_time == 50

        # Test without getattr (that fetches data from server) first
        e2e_client.settings._attributes = {}
        e2e_client.settings.debug_time = 60
        e2e_client.settings.save()

        e2e_client.settings._attributes = {}
        assert e2e_client.settings.debug_time == 60

    def test_update_settings_success(self, e2e_client):
        default_computes = ["small", "large"]
        idle_enabled = True
        idle_time = 99

        e2e_client.settings.update(
            default_computes=default_computes,
            idle_enabled=idle_enabled,
            idle_time=idle_time
        )

        assert e2e_client.settings.default_computes == default_computes
        assert e2e_client.settings.idle_enabled == idle_enabled
        assert e2e_client.settings.idle_time == idle_time

    def test_update_non_existing_attribute_fail(self, e2e_client):
        # Fetch original setting value for comparison
        original_setting = e2e_client.settings.email_on_error

        with pytest.raises(CnvrgError):
            e2e_client.settings.update(fake="setting", email_on_error=(not original_setting))

        assert e2e_client.settings.email_on_error == original_setting

    def test_update_unauthorized(self, domain, e2e_client, e2e_data_scientist_user):
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )

        with pytest.raises(CnvrgHttpError) as exception_info:
            client_of_non_admin_user.settings.update(debug_time=666)

        assert 'unauthorized' in str(exception_info.value).lower()
