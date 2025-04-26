from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.image_repository import ImageRepository

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.image_repository._generated.api_client.ApiClient.request"


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
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={"name": "my_rep"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        image_repositories.create(ImageRepository(name="my_rep"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = image_repositories.create_async(ImageRepository(name="my_rep"))
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_rep"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_image_repository(fake_root, image_repositories):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories",
    )
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
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep",
    )
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
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep",
    )
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
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/image-repositories/my_rep/images",
    )
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
