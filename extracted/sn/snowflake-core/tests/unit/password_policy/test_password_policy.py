from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.password_policy import PasswordPolicy, PasswordPolicyResource

from ...utils import BASE_URL, extra_params, mock_http_response


@pytest.fixture
def password_policies(schema):
    return schema.password_policies


@pytest.fixture
def password_policy(password_policies):
    return password_policies["my_password_policy"]


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
PASSWORD_POLICY = PasswordPolicy(
    name="my_password_policy",
    password_min_length=8,
    password_max_length=256,
    password_min_upper_case_chars=1,
    password_min_lower_case_chars=1,
    password_min_numeric_chars=1,
    password_min_special_chars=1,
    password_min_age_days=1,
    password_max_age_days=90,
    password_max_retries=5,
    password_lockout_time_mins=15,
    password_history=24,
    comment="Test password policy",
)


def test_create_password_policy(fake_root, password_policies):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/password-policies")
    kwargs = extra_params(
        query_params=[],
        body={
            "name": "my_password_policy",
            "password_min_length": 8,
            "password_max_length": 256,
            "password_min_upper_case_chars": 1,
            "password_min_lower_case_chars": 1,
            "password_min_numeric_chars": 1,
            "password_min_special_chars": 1,
            "password_min_age_days": 1,
            "password_max_age_days": 90,
            "password_max_retries": 5,
            "password_lockout_time_mins": 15,
            "password_history": 24,
            "comment": "Test password policy",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        pp_res = password_policies.create(PASSWORD_POLICY)
        assert isinstance(pp_res, PasswordPolicyResource)
        assert pp_res.name == "my_password_policy"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = password_policies.create_async(PASSWORD_POLICY)
        assert isinstance(op, PollingOperation)
        pp_res = op.result()
        assert pp_res.name == "my_password_policy"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_password_policy(fake_root, password_policies):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/password-policies")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        password_policies.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = password_policies.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, password_policies):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/password-policies?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(password_policies.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            password_policies.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(password_policies):
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(password_policies.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        password_policies.iter_async(limit=10, show_limit=5).result()


def test_fetch_password_policy(fake_root, password_policy):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/password-policies/my_password_policy")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(PASSWORD_POLICY.to_json())
        password_policy.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(PASSWORD_POLICY.to_json())
        op = password_policy.fetch_async()
        assert isinstance(op, PollingOperation)
        policy = op.result()
        assert policy.to_dict() == PASSWORD_POLICY.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_password_policy(fake_root, password_policy):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/password-policies/my_password_policy")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        password_policy.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = password_policy.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_password_policy(fake_root, password_policy, password_policies):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/password-policies/my_password_policy:rename?targetName=new_password_policy",
    )
    kwargs = extra_params(query_params=[("targetName", "new_password_policy")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        password_policy.rename("new_password_policy")
        assert password_policy.name == "new_password_policy"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        pp_res = password_policies["another_password_policy"]
        op = pp_res.rename_async("new_password_policy")
        assert isinstance(op, PollingOperation)
        op.result()
        assert pp_res.name == "new_password_policy"
    args2 = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/password-policies/another_password_policy:rename?targetName=new_password_policy",
    )
    mocked_request.assert_called_once_with(*args2, **kwargs)


def test_rename_password_policy_with_options(fake_root, password_policy):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/password-policies/my_password_policy:rename?ifExists=True&targetDatabase=other_db&targetSchema=other_schema&targetName=new_password_policy",
    )
    kwargs = extra_params(
        query_params=[
            ("ifExists", True),
            ("targetDatabase", "other_db"),
            ("targetSchema", "other_schema"),
            ("targetName", "new_password_policy"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        password_policy.rename(
            "new_password_policy", target_database="other_db", target_schema="other_schema", if_exists=True
        )
        assert password_policy.name == "new_password_policy"
    mocked_request.assert_called_once_with(*args, **kwargs)
