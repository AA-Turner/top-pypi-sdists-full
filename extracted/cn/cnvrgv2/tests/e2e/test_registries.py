import pytest

from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.registries import RegistryTypes
from tests.e2e.conftest import call_database


class TestRegistries:
    @staticmethod
    def cleanup(context_prefix):
        delete_user_command = "DELETE FROM registries WHERE slug LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    def test_create_registry(self, class_context, e2e_client):
        title = class_context.generate_name(5)
        url = "docker.io"

        registry = e2e_client.registries.create(title=title, url=url)
        assert registry.slug
        assert registry.url == url
        assert registry.title == title
        assert registry.registry_type == RegistryTypes.OTHER

    def test_get_registry(self, class_context, e2e_client):
        registry = e2e_client.registries.get(slug="cnvrg")
        assert registry.url == "docker.io/cnvrg"
        assert registry.title == "cnvrg"

    def test_get_registry_images(self, class_context, e2e_client):
        registry = e2e_client.registries.get(slug="cnvrg")
        for image in registry.images:
            assert image.tag
            assert image.name
            assert image.registry_slug == 'cnvrg'
            assert image.registry_url == 'docker.io/cnvrg'

    def test_list_registries(self, class_context, e2e_client):
        registries = e2e_client.registries.list()
        cnvrg_registry = [registry for registry in registries if registry.slug == "cnvrg"][0]
        assert cnvrg_registry.url == "docker.io/cnvrg"
        assert cnvrg_registry.title == "cnvrg"

    def test_update_registry(self, class_context, e2e_client):
        title = class_context.generate_name(5)
        url = "docker.io"

        registry = e2e_client.registries.create(title=title, url=url)
        assert registry.url == url
        assert registry.title == title

        new_url = "good-url.io"
        registry.update(url=new_url)
        registry.reload()
        assert registry.url == new_url
        assert registry.title == title

    def test_delete_registry(self, class_context, e2e_client):
        title = class_context.generate_name(5)
        url = "docker.io"

        registry = e2e_client.registries.create(title=title, url=url)
        assert registry.slug

        registry.delete()
        with pytest.raises(CnvrgError):
            e2e_client.registries.get(slug=registry.slug).url  # Need to call attribute to bypass lazy load

    def test_delete_registry_from_client(self, class_context, e2e_client):
        title = class_context.generate_name(5)
        url = "docker.io"

        registry = e2e_client.registries.create(title=title, url=url)
        assert registry.slug

        e2e_client.registries.delete(slug=registry.slug)
        with pytest.raises(CnvrgError):
            e2e_client.registries.get(slug=registry.slug).url  # Need to call attribute to bypass lazy load
