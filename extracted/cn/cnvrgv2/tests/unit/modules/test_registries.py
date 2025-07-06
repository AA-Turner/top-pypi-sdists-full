import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgError
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.registries import Registry, RegistryTypes


class MockRegistry:
    def __init__(self):
        self.slug = "test-slug"
        self.url = "doker.io"
        self.type = RegistryTypes.OTHER
        self.title = "my-registry"
        self.username = "username"

        self.data = {
            "id": "17",
            "type": "registry",
            "attributes": {
                "slug": self.slug,
                "url": self.url,
                "title": self.title,
                "private": True,
                "username": self.username,
                "registry_type": self.type
            }
        }

    def response(self, *args, **kwargs):
        return JAF(response={"data": self.data})


class TestImage:
    def test_registry_attributes(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        registry = Registry(empty_cnvrg, mock_resp.slug)
        assert registry.slug == mock_resp.slug
        assert registry.url == mock_resp.url
        assert registry.title == mock_resp.title
        assert registry.registry_type == mock_resp.type

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'GET'

    def test_delete_registry(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        registry = Registry(empty_cnvrg, mock_resp.slug)
        registry.delete()

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'DELETE'

    def test_update_registry(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        registry = Registry(empty_cnvrg, mock_resp.slug)
        registry.update(url="new.url")

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'PUT'

    def test_update_registry_invalid_arguments(self, empty_context, empty_cnvrg):
        registry = Registry(empty_cnvrg, "slug")

        with pytest.raises(CnvrgError):
            registry.update(url=1)

        with pytest.raises(CnvrgError):
            registry.update(title=1)

        with pytest.raises(CnvrgError):
            registry.update(username=1)
