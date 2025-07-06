import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgError
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.registries import RegistriesClient, Registry, RegistryTypes


class MockRegistry:
    def __init__(self, list=False):
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
        if list:
            self.data = [self.data]

    def response(self, *args, **kwargs):
        return JAF(response={"data": self.data})


class TestRegistriesClient:
    def test_create_registry_with_valid_arguments(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry()
        mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        client = RegistriesClient(empty_cnvrg)
        image = client.create(title=mock_resp.title, url=mock_resp.url, type=mock_resp.type)
        assert isinstance(image, Registry)
        assert image.slug == mock_resp.slug

    def test_create_registry_with_invalid_arguments(self, empty_context, empty_cnvrg):
        url = "docker.io"
        type = RegistryTypes.OTHER
        title = "test-image"

        client = RegistriesClient(empty_cnvrg)
        with pytest.raises(CnvrgError):
            client.create(title=1, url=url, type=type)

        with pytest.raises(CnvrgError):
            client.create(title=title, url=1, type=type)

        with pytest.raises(CnvrgError):
            client.create(title=title, url="badurl", type=type)

        with pytest.raises(CnvrgError):
            client.create(title=title, url=url, type=1)

        with pytest.raises(CnvrgError):
            client.create(title=title, url=url, type="fake")

        with pytest.raises(CnvrgError):
            client.create(title=title, url=url, type=type, username=1)

    def test_list_registries(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry(list=True)
        mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        client = RegistriesClient(empty_cnvrg)

        registries = client.list()
        registries = [registry for registry in registries]

        assert len(registries) == 1
        assert isinstance(registries[0], Registry)
        assert registries[0].slug == mock_resp.slug

    def test_get_registry(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry()
        mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        client = RegistriesClient(empty_cnvrg)
        registry = client.get(mock_resp.slug)

        assert isinstance(registry, Registry)
        assert registry.slug == mock_resp.slug
        assert registry.title == mock_resp.title

    def test_delete_image(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockRegistry()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        client = RegistriesClient(empty_cnvrg)
        client.delete(mock_resp.slug)

        assert mocked_call.call_count == 1
