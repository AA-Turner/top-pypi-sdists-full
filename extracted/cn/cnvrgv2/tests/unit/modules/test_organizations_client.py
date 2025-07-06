import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.organization.organizations_client import OrganizationsClient


class TestOrganizationsClient:
    def test_init_valid_credentials(self):
        organizations_client = OrganizationsClient(domain="fake", token="fake")
        assert organizations_client._proxy

    def test_get_organization_with_slug(self, mocker):
        slug = "test-slug"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "2",
                    "type": "organization",
                    "attributes": {
                        "slug": slug,
                        "created_at": "2020-09-13T15:32:16.671Z",
                        "updated_at": "2020-09-13T15:32:16.671Z"
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        organizations_client = OrganizationsClient(domain="fake", token="fake")
        organizations_client.get(slug)

        # TODO: add attribute checks. added call_count until decided what to check
        assert mocked_api_call.call_count > 0

    def test_get_organization_empty_slug(self, empty_context):
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        with pytest.raises(CnvrgArgumentsError):
            organizations_client.get("")

    def test_get_organization_none_slug(self, empty_context):
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        with pytest.raises(CnvrgArgumentsError):
            organizations_client.get(None)

    def test_get_organization_obj_slug(self, empty_context):
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        with pytest.raises(CnvrgArgumentsError):
            organizations_client.get({"say": "whaaat??"})

    def test_create_organization_with_name(self, mocker, empty_context):
        slug = "test-slug"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "2",
                    "type": "organization",
                    "attributes": {
                        "slug": slug,
                        "created_at": "2020-09-13T15:32:16.671Z",
                        "updated_at": "2020-09-13T15:32:16.671Z"
                    }
                }
            }
            return JAF(response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        organizations_client.create(slug)

        # TODO: add attribute checks. added call_count until decided what to check
        assert mocked_api_call.call_count > 0

    def test_create_organization_empty_name(self, empty_context):
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        with pytest.raises(CnvrgArgumentsError):
            organizations_client.create("")

    def test_create_organization_none_name(self, empty_context):
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        with pytest.raises(CnvrgArgumentsError):
            organizations_client.create(None)

    def test_create_organization_obj_name(self, empty_context):
        organizations_client = OrganizationsClient(empty_context.domain, empty_context.token)
        with pytest.raises(CnvrgArgumentsError):
            organizations_client.create({"say": "whaaat??"})
