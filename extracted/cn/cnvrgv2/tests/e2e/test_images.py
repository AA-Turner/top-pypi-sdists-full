import pytest

from cnvrgv2.errors import CnvrgError
from tests.e2e.conftest import call_database


class TestImages:
    @staticmethod
    def cleanup(context_prefix):
        delete_user_command = "DELETE FROM images WHERE name LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    def test_create_image(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        tag = "v1"
        registry = "docker-hub"

        image = e2e_client.images.create(name=name, tag=tag, registry=registry)
        assert image.slug
        assert image.tag == tag
        assert image.name == name
        assert image.dockerfile == ''
        assert image.registry_slug == registry

    def test_create_custom_image(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        tag = "v1"
        registry = "docker-hub"
        dockerfile = "docker"

        image = e2e_client.images.create(name=name, tag=tag, registry=registry, custom=True, dockerfile=dockerfile)
        assert image.slug
        assert image.tag == tag
        assert image.name == name
        assert image.dockerfile == dockerfile  # Tests dockerfile property as well!

    def test_get_image(self, class_context, e2e_client):
        name = "cnvrg"
        tag = "v5.0"

        # Get image by name and tag
        image = e2e_client.images.get(name="cnvrg", tag=tag)
        assert image.slug
        assert image.tag == tag
        assert image.name == name

        # Get image by slug
        image_by_slug = e2e_client.images.get(slug=image.slug)
        assert image_by_slug.tag == tag
        assert image_by_slug.name == name

    def test_update_image(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        tag = "v1"
        registry = "docker-hub"

        image = e2e_client.images.create(name=name, tag=tag, registry=registry)
        assert image.logo is None
        assert image.readme == ''

        logo = "cnvrg"
        readme = "readme"
        image.update(logo=logo, readme=readme)
        image.reload()
        assert image.logo == logo
        assert image.readme == readme

        image.update(logo=logo, readme=readme + "-new")
        image.reload()
        assert image.logo == logo
        assert image.readme == readme + "-new"

    def test_delete_image(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        tag = "v1"
        registry = "docker-hub"

        image = e2e_client.images.create(name=name, tag=tag, registry=registry)
        assert image.slug

        image.delete()
        with pytest.raises(CnvrgError):
            e2e_client.images.get(slug=image.slug).logo  # Need to call attribute to bypass lazy load

    def test_delete_image_from_client(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        tag = "v1"
        registry = "docker-hub"

        image = e2e_client.images.create(name=name, tag=tag, registry=registry)
        assert image.slug

        e2e_client.images.delete(slug=image.slug)
        with pytest.raises(CnvrgError):
            e2e_client.images.get(slug=image.slug).logo  # Need to call attribute to bypass lazy load
