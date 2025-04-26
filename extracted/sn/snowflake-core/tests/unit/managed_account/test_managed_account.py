from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.managed_account import ManagedAccount, ManagedAccountCollection

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.managed_account._generated.api_client.ApiClient.request"
MANAGED_ACCOUNT = ManagedAccount(name="my_acc", admin_name="admin", admin_password="test")


@pytest.fixture
def managed_accounts(fake_root):
    return ManagedAccountCollection(fake_root)


@pytest.fixture
def managed_account(managed_accounts):
    return managed_accounts["my_acc"]


def test_create_managed_account(fake_root, managed_accounts):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/managed-accounts",
    )
    kwargs = extra_params(
        body={
            "name": "my_acc",
            "admin_name": "admin",
            "admin_password": "test",
            "account_type": "READER",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        managed_accounts.create(MANAGED_ACCOUNT)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = managed_accounts.create_async(MANAGED_ACCOUNT)
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_acc"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_managed_account(fake_root, managed_accounts):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/managed-accounts",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        managed_accounts.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = managed_accounts.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_managed_account(fake_root, managed_account):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/managed-accounts/my_acc",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        managed_account.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = managed_account.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
