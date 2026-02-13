from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.compute_pool import ComputePool, ComputePoolCollection, ComputePoolResource
from snowflake.core.compute_pool._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
COMPUTE_POOL = ComputePool(name="my_compute_pool", min_nodes=1, max_nodes=1, instance_family="")


@pytest.fixture()
def compute_pools(fake_root):
    return ComputePoolCollection(fake_root)


@pytest.fixture()
def compute_pool(compute_pools):
    return compute_pools["my_compute_pool"]


def test_create_async(fake_root, compute_pools):
    args = (fake_root, "POST", BASE_URL + "/compute-pools?createMode=errorIfExists&initiallySuspended=False")
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("initiallySuspended", False)],
        body={"name": "my_compute_pool", "min_nodes": 1, "max_nodes": 1, "instance_family": ""},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        compute_pool_res = compute_pools.create(COMPUTE_POOL)
        assert isinstance(compute_pool_res, ComputePoolResource)
        assert compute_pool_res.name == "my_compute_pool"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pools.create_async(COMPUTE_POOL)
        assert isinstance(op, PollingOperation)
        compute_pool_res = op.result()
        assert compute_pool_res.name == "my_compute_pool"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_async(fake_root, compute_pools):
    args = (fake_root, "GET", BASE_URL + "/compute-pools")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = compute_pools.iter()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = compute_pools.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_async(fake_root, compute_pool):
    args = (fake_root, "PUT", BASE_URL + "/compute-pools/my_compute_pool")
    kwargs = extra_params(body={"name": "my_compute_pool", "min_nodes": 1, "max_nodes": 1, "instance_family": ""})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        compute_pool.create_or_alter(COMPUTE_POOL)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.create_or_alter_async(COMPUTE_POOL)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_async(fake_root, compute_pool):
    from snowflake.core.compute_pool._generated.models import ComputePool as ComputePoolModel

    model = ComputePoolModel(name="my_compute_pool", min_nodes=1, max_nodes=1, instance_family="")
    args = (fake_root, "GET", BASE_URL + "/compute-pools/my_compute_pool")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        my_compute_pool = compute_pool.fetch()
        assert my_compute_pool.to_dict() == COMPUTE_POOL.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = compute_pool.fetch_async()
        assert isinstance(op, PollingOperation)
        my_compute_pool = op.result()
        assert my_compute_pool.to_dict() == COMPUTE_POOL.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_suspend_async(fake_root, compute_pool):
    args = (fake_root, "POST", BASE_URL + "/compute-pools/my_compute_pool:suspend")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        compute_pool.suspend()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.suspend_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_resume_async(fake_root, compute_pool):
    args = (fake_root, "POST", BASE_URL + "/compute-pools/my_compute_pool:resume")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        compute_pool.resume()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.resume_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_stop_all_services_async(fake_root, compute_pool):
    args = (fake_root, "POST", BASE_URL + "/compute-pools/my_compute_pool:stop-all-services")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        compute_pool.stop_all_services()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.stop_all_services_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_async(fake_root, compute_pool):
    args = (fake_root, "DELETE", BASE_URL + "/compute-pools/my_compute_pool")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        compute_pool.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, compute_pool, tag):
    args = (fake_root, "POST", BASE_URL + "/compute-pools/my_compute_pool:set-tags")
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
        compute_pool.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, compute_pool, tag):
    args = (fake_root, "POST", BASE_URL + "/compute-pools/my_compute_pool:unset-tags")
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
        compute_pool.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = compute_pool.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, compute_pool):
    args = (fake_root, "GET", BASE_URL + "/compute-pools/my_compute_pool:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert compute_pool.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = compute_pool.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
