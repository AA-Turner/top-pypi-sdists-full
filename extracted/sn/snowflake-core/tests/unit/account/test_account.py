from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.account import Account, AccountCollection

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.account._generated.api_client.ApiClient.request"
ACCOUNT = Account("my_account", "STANDARD", "admin", "admin@localhost")


@pytest.fixture()
def accounts(fake_root):
    return AccountCollection(fake_root)


@pytest.fixture()
def account(accounts):
    return accounts["my_account"]


def test_create_async(fake_root, accounts):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/accounts",
    )
    kwargs = extra_params(
        body={
            "name": "my_account",
            "edition": "STANDARD",
            "admin_name": "admin",
            "email": "admin@localhost",
            "must_change_password": False,
            "polaris": False,
            "dropped_on": None,
            "scheduled_deletion_time": None,
            "restored_on": None,
            "organization_URL_expiration_on": None,
            "moved_on": None,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        account_res = accounts.create(ACCOUNT)
        assert account_res.name == "my_account"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = accounts.create_async(ACCOUNT)
        assert isinstance(op, PollingOperation)
        account_res = op.result()
        assert account_res.name == "my_account"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_async(fake_root, accounts):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/accounts",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = accounts.iter()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = accounts.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_async(fake_root, account):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/accounts/my_account?gracePeriodInDays=7",
    )
    kwargs = extra_params(query_params=[("gracePeriodInDays", 7)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        account.drop(7)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = account.drop_async(7)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_async(fake_root, account):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/accounts/my_account:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        account.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = account.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
