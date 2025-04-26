from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.external_volume import ExternalVolume, ExternalVolumeCollection

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.external_volume._generated.api_client.ApiClient.request"


@pytest.fixture
def external_volumes(fake_root):
    return ExternalVolumeCollection(fake_root)


@pytest.fixture
def external_volume(external_volumes):
    return external_volumes["my_volume"]


def test_create_external_volume(fake_root, external_volumes):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/external-volumes?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_volume",
            "storage_locations": [],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        external_volumes.create(ExternalVolume(name="my_volume", storage_locations=[]))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = external_volumes.create_async(ExternalVolume(name="my_volume", storage_locations=[]))
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_volume"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_external_volume(fake_root, external_volumes):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/external-volumes",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        external_volumes.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = external_volumes.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_external_volume(fake_root, external_volume):
    from snowflake.core.external_volume._generated.models import ExternalVolume as ExternalVolumeModel

    model = ExternalVolumeModel(name="my_volume", storage_locations=[])
    args = (
        fake_root,
        "GET",
        BASE_URL + "/external-volumes/my_volume",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        external_volume.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = external_volume.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == ExternalVolume(name="my_volume", storage_locations=[]).to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_external_volume(fake_root, external_volume):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/external-volumes/my_volume",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        external_volume.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = external_volume.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_external_volume(fake_root, external_volume):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/external-volumes/my_volume:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        external_volume.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = external_volume.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
