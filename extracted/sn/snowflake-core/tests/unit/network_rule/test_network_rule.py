from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.network_rule import NetworkRule, NetworkRuleResource

from ...utils import BASE_URL, extra_params, mock_http_response


@pytest.fixture
def network_rules(schema):
    return schema.network_rules


@pytest.fixture
def network_rule(network_rules):
    return network_rules["my_network_rule"]


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
NETWORK_RULE = NetworkRule(
    name="my_network_rule",
    type="HOST_PORT",
    mode="EGRESS",
    value_list=["example.com:443", "api.example.com:443"],
    comment="Test network rule",
)


def test_create_network_rule(fake_root, network_rules):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/network-rules")
    kwargs = extra_params(
        query_params=[],
        body={
            "type": "HOST_PORT",
            "mode": "EGRESS",
            "value_list": ["example.com:443", "api.example.com:443"],
            "comment": "Test network rule",
            "name": "my_network_rule",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        nr_res = network_rules.create(NETWORK_RULE)
        assert isinstance(nr_res, NetworkRuleResource)
        assert nr_res.name == "my_network_rule"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = network_rules.create_async(NETWORK_RULE)
        assert isinstance(op, PollingOperation)
        nr_res = op.result()
        assert nr_res.name == "my_network_rule"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_network_rule(fake_root, network_rules):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/network-rules")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        network_rules.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = network_rules.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, network_rules):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/network-rules?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(network_rules.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            network_rules.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(network_rules):
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(network_rules.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        network_rules.iter_async(limit=10, show_limit=5).result()


def test_fetch_network_rule(fake_root, network_rule):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/network-rules/my_network_rule")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(NETWORK_RULE.to_json())
        network_rule.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(NETWORK_RULE.to_json())
        op = network_rule.fetch_async()
        assert isinstance(op, PollingOperation)
        rule = op.result()
        assert rule.to_dict() == NETWORK_RULE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_network_rule(fake_root, network_rule):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/network-rules/my_network_rule")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        network_rule.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = network_rule.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
