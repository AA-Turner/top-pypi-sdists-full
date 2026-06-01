import json
from http import HTTPStatus
from unittest.mock import MagicMock

import httpx
import pytest

from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.worker_client.errors import SDKError


def _make_sdk_error(body: str, status_code: int = 400) -> SDKError:
    raw = MagicMock(spec=httpx.Response)
    raw.status_code = status_code
    raw.headers = httpx.Headers({})
    raw.text = body
    return SDKError(message="error", raw_response=raw, body=body)


@pytest.mark.parametrize(
    "body, status_code, kwargs, expected_message, expected_type, expected_status, expected_code",
    [
        pytest.param(
            json.dumps({"message": "bad request", "type": "invalid_request_error"}),
            400,
            {},
            "bad request",
            "invalid_request_error",
            HTTPStatus.BAD_REQUEST,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="valid_json_body",
        ),
        pytest.param(
            json.dumps({"message": "bad request", "type": "invalid_request_error", "code": "workflow_not_found"}),
            400,
            {"code": ErrorCode.TEMPORAL_CONNECTION_ERROR},
            "bad request",
            "invalid_request_error",
            HTTPStatus.BAD_REQUEST,
            "workflow_not_found",
            id="json_body_code_overrides_fallback_code",
        ),
        pytest.param(
            "Internal Server Error",
            500,
            {"message": "fallback message"},
            "fallback message",
            "api_error",
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="plain_text_body_uses_defaults",
        ),
        pytest.param(
            "",
            502,
            {"message": "gateway error"},
            "gateway error",
            "api_error",
            HTTPStatus.BAD_GATEWAY,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="empty_body_uses_defaults",
        ),
        pytest.param(
            "<html><body>502 Bad Gateway</body></html>",
            502,
            {},
            "HTTP request failed",
            "api_error",
            HTTPStatus.BAD_GATEWAY,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="html_body_uses_defaults",
        ),
        pytest.param(
            '{"message": "oops"',
            500,
            {"message": "fallback"},
            "fallback",
            "api_error",
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="truncated_json_uses_defaults",
        ),
        pytest.param(
            json.dumps({"detail": "something went wrong"}),
            422,
            {"message": "default msg"},
            "default msg",
            "api_error",
            HTTPStatus.UNPROCESSABLE_ENTITY,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="json_missing_fields_uses_defaults",
        ),
        pytest.param(
            "not json",
            404,
            {"code": ErrorCode.WORKFLOW_NOT_FOUND},
            "HTTP request failed",
            "api_error",
            HTTPStatus.NOT_FOUND,
            ErrorCode.WORKFLOW_NOT_FOUND,
            id="custom_code_propagated",
        ),
        pytest.param(
            "{}",
            999,
            {},
            "HTTP request failed",
            "api_error",
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="unknown_status_code_falls_back_to_500",
        ),
        pytest.param(
            json.dumps(["not", "a", "dict"]),
            400,
            {"message": "fallback"},
            "fallback",
            "api_error",
            HTTPStatus.BAD_REQUEST,
            ErrorCode.TEMPORAL_CONNECTION_ERROR,
            id="valid_json_non_dict_uses_defaults",
        ),
    ],
)
def test_from_sdk_error(body, status_code, kwargs, expected_message, expected_type, expected_status, expected_code):
    exc = _make_sdk_error(body, status_code=status_code)
    result = WorkflowsException.from_sdk_error(exc, **kwargs)
    assert result.message == expected_message
    assert result.type == expected_type
    assert result.status == expected_status
    assert result.code == expected_code
