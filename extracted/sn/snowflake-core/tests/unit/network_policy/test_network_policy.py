from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.network_policy import NetworkPolicy, NetworkPolicyCollection

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.network_policy._generated.api_client.ApiClient.request"


@pytest.fixture
def network_policies(fake_root):
    return NetworkPolicyCollection(fake_root)


@pytest.fixture
def network_policy(network_policies):
    return network_policies["my_policy"]


def test_create_network_policy(fake_root, network_policies):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/network-policies?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={"name": "my_policy"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        network_policies.create(NetworkPolicy(name="my_policy"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = network_policies.create_async(NetworkPolicy(name="my_policy"))
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_policy"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_network_policy(fake_root, network_policies):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/network-policies",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        network_policies.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = network_policies.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_network_policy(fake_root, network_policy):
    from snowflake.core.network_policy._generated.models import NetworkPolicy as NetworkPolicyModel

    model = NetworkPolicyModel(name="my_policy")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/network-policies/my_policy",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        network_policy.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = network_policy.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == NetworkPolicy(name="my_policy").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)



def test_drop_network_policy(fake_root, network_policy):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/network-policies/my_policy",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        network_policy.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = network_policy.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
