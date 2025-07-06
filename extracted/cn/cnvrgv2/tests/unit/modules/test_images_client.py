import pytest
from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgError, CnvrgArgumentsError
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.images import ImagesClient, Image, ImageLogos


class MockImage:
    def __init__(self, list=False):
        self.slug = "test-slug"
        self.name = "test-image"
        self.tag = "v1"
        self.registry = "docker-hub"
        self.data = {
            "id": "17",
            "type": "image",
            "attributes": {
                "slug": self.slug,
                "name": self.name,
                "tag": self.tag,
                "registry_slug": self.registry,
                "logo": "",
                "readme": ""
            }
        }
        if list:
            self.data = [self.data]

    def response(self, *args, **kwargs):
        return JAF(response={"data": self.data})


class TestImagesClient:
    def test_create_image_with_valid_arguments(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)
        client = ImagesClient(empty_cnvrg)
        image = client.create(
            name=mock_resp.name,
            tag=mock_resp.tag,
            registry=mock_resp.registry,
            logo=ImageLogos.CNVRG
        )
        assert isinstance(image, Image)
        assert image.slug == mock_resp.slug
        assert image.name == mock_resp.name

    def test_create_image_with_invalid_arguments(self, empty_context, empty_cnvrg):
        name = "test-image"
        tag = "v1"
        registry = "docker-hub"
        client = ImagesClient(empty_cnvrg)
        with pytest.raises(CnvrgError):
            client.create(name=name, tag=1, registry=registry, logo=ImageLogos.CNVRG)
        with pytest.raises(CnvrgError):
            client.create(name=name, tag="bad tag", registry=registry, logo=ImageLogos.CNVRG)
        with pytest.raises(CnvrgError):
            client.create(name=1, tag=tag, registry=registry, logo=ImageLogos.CNVRG)
        with pytest.raises(CnvrgError):
            client.create(name="bad name", tag=tag, registry=registry, logo=ImageLogos.CNVRG)
        with pytest.raises(CnvrgError):
            client.create(name=name, tag=tag, registry=registry, logo="fake")

    def test_list_images(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage(list=True)
        mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)
        client = ImagesClient(empty_cnvrg)
        images = client.list()
        images = [image for image in images]
        assert len(images) == 1
        assert isinstance(images[0], Image)
        assert images[0].slug == mock_resp.slug
        assert images[0].name == mock_resp.name

    def test_get_image(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)
        client = ImagesClient(empty_cnvrg)
        image = client.get(mock_resp.slug)
        assert isinstance(image, Image)
        assert image.slug == mock_resp.slug
        assert image.name == mock_resp.name

    def test_delete_image(self, mocker, empty_context, empty_cnvrg):
        mock_resp = MockImage()
        mocked_call = mocker.patch.object(Proxy, 'call_api', side_effect=mock_resp.response)
        client = ImagesClient(empty_cnvrg)
        client.delete(mock_resp.slug)
        assert mocked_call.call_count == 1

    def test_create_image_with_valid_name(self, mocker, empty_context, empty_cnvrg):
        client = ImagesClient(empty_cnvrg)
        valid_names = ["test", "test-image", "test/image"]
        for name in valid_names:
            mock_data = {
                "id": "17",
                "type": "image",
                "attributes": {
                    "slug": "test-slug",
                    "name": name,
                    "tag": "v1",
                    "registry_slug": "docker-hub",
                    "logo": "",
                    "readme": ""
                }
            }
            mock_response = JAF(response={"data": mock_data})
            mocker.patch.object(Proxy, 'call_api', return_value=mock_response)
            image = client.create(name=name, tag="v1", registry="docker-hub")
            assert image.name == name
            assert image.tag == "v1"

    def test_create_image_with_invalid_name(self, mocker, empty_context, empty_cnvrg):
        invalid_names = ["test\\image", "test!%#", "test*invalid"]
        client = ImagesClient(empty_cnvrg)
        mock_resp = MockImage()
        for name in invalid_names:
            mocker.patch.object(Proxy, 'call_api', side_effect=CnvrgArgumentsError("Bad arguments: Image name is invalid"))
            with pytest.raises(CnvrgArgumentsError, match="Bad arguments: Image name is invalid"):
                client.create(name=name, tag=mock_resp.tag, registry=mock_resp.registry)
