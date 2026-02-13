from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.image_repository import ImageRepository, ImageRepositoryResource
from snowflake.core.image_repository._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


@pytest.fixture
def image_repositories(schema):
    return schema.image_repositories


@pytest.fixture
def image_repository(image_repositories):
    return image_repositories["my_rep"]


def test_create_image_repository(fake_root, image_repositories):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories?createMode=errorIfExists",
    )
    kwargs = extra_params(query_params=[("createMode", "errorIfExists")], body={"name": "my_rep"})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        ir_res = image_repositories.create(ImageRepository(name="my_rep"))
        assert isinstance(ir_res, ImageRepositoryResource)
        assert ir_res.name == "my_rep"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = image_repositories.create_async(ImageRepository(name="my_rep"))
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_rep"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_image_repository(fake_root, image_repositories):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        image_repositories.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = image_repositories.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_image_repository(fake_root, image_repository):
    from snowflake.core.image_repository._generated.models import ImageRepository as ImageRepositoryModel

    model = ImageRepositoryModel(name="my_rep")
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        image_repository.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = image_repository.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == ImageRepository(name="my_rep").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_image_repository(fake_root, image_repository):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        image_repository.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = image_repository.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_list_images_in_repository(fake_root, image_repository):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep/images")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        images = image_repository.list_images_in_repository()
        assert list(images) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = image_repository.list_images_in_repository_async()
        assert isinstance(op, PollingOperation)
        images = op.result()
        assert list(images) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, image_repository, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep:set-tags")
    tags = {tag: TagValue(value="value")}
    kwargs = extra_params(
        body=[
            TagAssignment(
                tag_value=v.value, tag_name=k.name, tag_schema=k.schema.name, tag_database=k.database.name
            ).to_dict()
            for k, v in tags.items()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        image_repository.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = image_repository.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, image_repository, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep:unset-tags")
    tag_resources = {tag}
    kwargs = extra_params(
        body=[
            TagReference(
                tag_name=tag_res.name, tag_schema=tag_res.schema.name, tag_database=tag_res.database.name
            ).to_dict()
            for tag_res in tag_resources
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        image_repository.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = image_repository.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, image_repository):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert image_repository.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = image_repository.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
