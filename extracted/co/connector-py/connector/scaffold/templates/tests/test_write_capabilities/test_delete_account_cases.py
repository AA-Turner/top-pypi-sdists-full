"""Cases for testing ``delete_account`` capability."""

import typing as t

import httpx
from connector.generated import (
    AccountStatus,
    DeleteAccount,
    DeleteAccountRequest,
    DeleteAccountResponse,
    DeletedAccount,
    Error,
    ErrorCode,
    ErrorResponse,
)
from connector.utils.test import http_error_message

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from connector.generated.models.standard_capability_name import StandardCapabilityName

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    DeleteAccountRequest,
    ResponseBodyMap,
    DeleteAccountResponse | ErrorResponse,
]


def case_delete_account_204() -> Case:
    """Successful deletion request."""
    args = DeleteAccountRequest(
        request=DeleteAccount(
            account_id="1",
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.NO_CONTENT,
                response_body=None,
            ),
        }},
    }}
    expected_response = DeleteAccountResponse(
        response=DeletedAccount(deleted=True, status=AccountStatus.DELETED),
    )
    return StandardCapabilityName.DELETE_ACCOUNT, args, response_body_map, expected_response


def case_delete_account_404() -> Case:
    """User not found request should fail."""
    args = DeleteAccountRequest(
        request=DeleteAccount(
            account_id="non_existent",
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{
                    "error": {{
                        "message": "Not found",
                        "code": 2100,
                    }},
                }},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                httpx.codes.NOT_FOUND,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            app_id="{name}",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:delete_account",
        ),
    )
    return StandardCapabilityName.DELETE_ACCOUNT, args, response_body_map, expected_response
