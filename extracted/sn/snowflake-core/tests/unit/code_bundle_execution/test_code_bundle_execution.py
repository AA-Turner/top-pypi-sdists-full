from unittest import mock
from unittest.mock import MagicMock

import pytest

from snowflake.core import PollingOperation
from snowflake.core._internal.snowapi_parameters import SnowApiParameter, SnowApiParameters
from snowflake.core.code_bundle_execution import (
    CodeBundleExecutionCollection,
    ExecuteCodeBundleRequest,
    SuccessAcceptedResponse,
    SuccessResponse,
)
from snowflake.core.exceptions import NotFoundError

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


@pytest.fixture
def code_bundle_execution(fake_root):
    return CodeBundleExecutionCollection(fake_root)


@pytest.fixture
def execution(code_bundle_execution):
    return code_bundle_execution["my_execution_id"]


def test_execute_code_bundle(fake_root, code_bundle_execution):
    body = {"from_location": "@my_db.my_schema.my_stage/src", "entrypoint": "main.py"}
    request = ExecuteCodeBundleRequest(from_location="@my_db.my_schema.my_stage/src", entrypoint="main.py")

    # Both execute() and execute_async() default to async_exec=True, so the request carries asyncExec=True.
    args = (fake_root, "POST", BASE_URL + "/code-bundle-executions?asyncExec=True")
    kwargs = extra_params(query_params=[("asyncExec", True)], body=body)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SuccessResponse(status="Execution successful").to_json())
        result = code_bundle_execution.execute(request)
        assert isinstance(result, SuccessResponse)
        assert result.status == "Execution successful"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SuccessResponse(status="Execution successful").to_json())
        op = code_bundle_execution.execute_async(request)
        assert isinstance(op, PollingOperation)
        result = op.result()
        assert isinstance(result, SuccessResponse)
        assert result.status == "Execution successful"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_code_bundle_with_specification_and_execution_name(fake_root, code_bundle_execution):
    # `specification` is an object (dict) that must serialize as a nested JSON object, not a string;
    # `execution_name` is an optional caller-supplied run name.
    specification = {"bundle": {"type": "custom", "compute_type": "warehouse", "language": "python"}}
    body = {
        "from_location": "@my_db.my_schema.my_stage/src",
        "entrypoint": "main.py",
        "specification": specification,
        "execution_name": "my_run",
    }
    request = ExecuteCodeBundleRequest(
        from_location="@my_db.my_schema.my_stage/src",
        entrypoint="main.py",
        specification=specification,
        execution_name="my_run",
    )
    args = (fake_root, "POST", BASE_URL + "/code-bundle-executions?asyncExec=True")
    kwargs = extra_params(query_params=[("asyncExec", True)], body=body)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SuccessResponse(status="Execution successful").to_json())
        code_bundle_execution.execute(request)
    mocked_request.assert_called_once_with(*args, **kwargs)


def _mock_202_response(body: str, location: str = None) -> MagicMock:
    """Build a mock HTTP 202 accepted-response (optionally carrying a Location header)."""
    m = MagicMock()
    m.data = body
    m.status = 202
    m.getheader.side_effect = lambda name: location if name == "Location" else None
    return m


def test_execute_code_bundle_async_exec_returns_202_without_polling(fake_root, code_bundle_execution):
    # With SKIP_ASYNC_EXEC_POLLING enabled (default), a caller-requested async execution (asyncExec=true)
    # that receives a 202 is handed back as-is (SuccessAcceptedResponse with job_id) — the client does not
    # poll the result endpoint to completion.
    request = ExecuteCodeBundleRequest(from_location="@my_db.my_schema.my_stage/src", entrypoint="main.py")
    accepted = SuccessAcceptedResponse(code="392604", message="in progress", job_id="01c-abc")

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = _mock_202_response(accepted.to_json())
        result = code_bundle_execution.execute(request)

    assert isinstance(result, SuccessAcceptedResponse)
    assert result.job_id == "01c-abc"
    # A single POST, no follow-up GET against the result endpoint.
    mocked_request.assert_called_once()


def test_execute_code_bundle_async_exec_polls_when_disabled(fake_root, code_bundle_execution):
    # With SKIP_ASYNC_EXEC_POLLING disabled, the client falls back to polling the 202 result endpoint to
    # completion and returns the final 200 SuccessResponse.
    fake_root.parameters.return_value = SnowApiParameters(
        {SnowApiParameter.MAX_THREADS: "1", SnowApiParameter.SKIP_ASYNC_EXEC_POLLING: "false"}
    )
    request = ExecuteCodeBundleRequest(from_location="@my_db.my_schema.my_stage/src", entrypoint="main.py")

    accepted = _mock_202_response(
        SuccessAcceptedResponse(code="392604", message="in progress", job_id="01c-abc").to_json(),
        location="/api/v2/results/01c-abc",
    )
    completed = mock_http_response(SuccessResponse(status="Execution successful").to_json())

    with (
        mock.patch(API_CLIENT_REQUEST) as mocked_request,
        mock.patch("snowflake.core._generated.api_client.time.sleep"),
    ):
        mocked_request.side_effect = [accepted, completed]
        result = code_bundle_execution.execute(request)

    assert isinstance(result, SuccessResponse)
    assert result.status == "Execution successful"
    # Original POST plus one poll GET against the result endpoint.
    assert mocked_request.call_count == 2


def test_fetch_status(fake_root, execution):
    from snowflake.core.code_bundle_execution._generated.models import CodeBundleExecution

    # The API returns a list; fetch_status returns the first (single) record.
    model = CodeBundleExecution(query_id="my_execution_id", status="SUCCESS")
    list_body = f"[{model.to_json()}]"
    args = (fake_root, "GET", BASE_URL + "/code-bundle-executions/my_execution_id")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(list_body)
        status = execution.fetch_status()
        assert isinstance(status, CodeBundleExecution)
        assert status.query_id == "my_execution_id"
        assert status.status == "SUCCESS"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(list_body)
        op = execution.fetch_status_async()
        assert isinstance(op, PollingOperation)
        status = op.result()
        assert isinstance(status, CodeBundleExecution)
        assert status.query_id == "my_execution_id"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_status_returns_first_when_multiple(fake_root, execution):
    from snowflake.core.code_bundle_execution._generated.models import CodeBundleExecution

    first = CodeBundleExecution(query_id="my_execution_id", status="RUNNING")
    second = CodeBundleExecution(query_id="my_execution_id", status="SUCCESS")
    list_body = f"[{first.to_json()},{second.to_json()}]"

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(list_body)
        status = execution.fetch_status()
        assert status.status == "RUNNING"


def test_fetch_status_not_found_when_empty(fake_root, execution):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response("[]")
        with pytest.raises(NotFoundError):
            execution.fetch_status()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response("[]")
        op = execution.fetch_status_async()
        assert isinstance(op, PollingOperation)
        with pytest.raises(NotFoundError):
            op.result()


def test_cancel(fake_root, execution):
    args = (fake_root, "POST", BASE_URL + "/code-bundle-executions/my_execution_id:cancel")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        execution.cancel()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = execution.cancel_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
