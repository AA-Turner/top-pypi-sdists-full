from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.code_bundle import (
    AddVersionCodeBundleRequest,
    CodeBundle,
    CodeBundleResource,
    ExecuteCodeBundleRequest,
)

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


@pytest.fixture
def code_bundles(schema):
    return schema.code_bundles


@pytest.fixture
def code_bundle(code_bundles):
    return code_bundles["my_code_bundle"]


def test_create_code_bundle(fake_root, code_bundles):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles")
    kwargs = extra_params(query_params=[], body={"name": "my_code_bundle"})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        bundle_res = code_bundles.create(CodeBundle(name="my_code_bundle"))
        assert isinstance(bundle_res, CodeBundleResource)
        assert bundle_res.name == "my_code_bundle"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = code_bundles.create_async(CodeBundle(name="my_code_bundle"))
        assert isinstance(op, PollingOperation)
        bundle_res = op.result()
        assert bundle_res.name == "my_code_bundle"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_code_bundle(fake_root, code_bundles):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        code_bundles.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = code_bundles.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_code_bundle(fake_root, code_bundle):
    from snowflake.core.code_bundle._generated.models import CodeBundle as CodeBundleModel

    model = CodeBundleModel(name="my_code_bundle")
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles/my_code_bundle")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        code_bundle.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = code_bundle.fetch_async()
        assert isinstance(op, PollingOperation)
        fetched = op.result()
        assert fetched.to_dict() == CodeBundle(name="my_code_bundle").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_code_bundle(fake_root, code_bundle):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles/my_code_bundle")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        code_bundle.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = code_bundle.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_add_version_code_bundle(fake_root, code_bundle):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles/my_code_bundle:add-version",
    )
    kwargs = extra_params(body={"from_location": "@my_db.my_schema.my_stage/src"})
    request = AddVersionCodeBundleRequest(from_location="@my_db.my_schema.my_stage/src")

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        code_bundle.add_version(request)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = code_bundle.add_version_async(request)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_code_bundle(fake_root, code_bundle):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles/my_code_bundle:execute",
    )
    kwargs = extra_params(body={"entrypoint": "main.py", "arguments": ["--flag", "value"]})
    request = ExecuteCodeBundleRequest(entrypoint="main.py", arguments=["--flag", "value"])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        code_bundle.execute(request)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = code_bundle.execute_async(request)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_code_bundle_with_specification_and_execution_name(fake_root, code_bundle):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/code-bundles/my_code_bundle:execute",
    )
    # `specification` is an object (dict) that must serialize as a nested JSON object, not a string;
    # `execution_name` is an optional caller-supplied run name.
    specification = {"bundle": {"type": "custom", "compute_type": "warehouse", "language": "python"}}
    kwargs = extra_params(body={"entrypoint": "main.py", "specification": specification, "execution_name": "my_run"})
    request = ExecuteCodeBundleRequest(entrypoint="main.py", specification=specification, execution_name="my_run")

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        code_bundle.execute(request)
    mocked_request.assert_called_once_with(*args, **kwargs)
