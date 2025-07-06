import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgError
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.images import Image, ImageLogos


class MockImage:
    def __init__(self):
        self.slug = "test-slug"
        self.name = "test-image"
        self.tag = "v1"
        self.registry = "docker-hub"

        self.data = {
            "id": "17",
            "type": "project",
            "attributes": {
                "slug": self.slug,
                "name": self.name,
                "tag": self.tag,
                "dockerfile": "dockerfile",
                "registry_slug": self.registry,
                "logo": "",
                "readme": ""
            }
        }

    def response(self, *args, **kwargs):
        return JAF(response={"data": self.data})


class TestImage:
    def test_image_attributes(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        image = Image(empty_cnvrg, mock_resp.slug)
        assert image.slug == mock_resp.slug
        assert image.tag == mock_resp.tag
        assert image.name == mock_resp.name
        assert image.registry_slug == mock_resp.registry

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'GET'

    def test_delete_image(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        image = Image(empty_cnvrg, mock_resp.slug)
        image.delete()

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'DELETE'

    def test_image_dockerfile_property(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        image = Image(empty_cnvrg, mock_resp.slug)

        # Should only call the API once (property caching)
        image.dockerfile
        image.dockerfile
        image.dockerfile
        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'GET'

    def test_update_image(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)

        image = Image(empty_cnvrg, mock_resp.slug)
        image.update(logo=ImageLogos.CNVRG)

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[1]['http_method'] == 'PUT'

    def test_update_image_invalid_arguments(self, empty_context, empty_cnvrg):
        image = Image(empty_cnvrg, "slug")

        with pytest.raises(CnvrgError):
            image.update(logo="fake")
