"""Cases for testing ``activate_account`` capability."""

import typing as t

import httpx
from connector.generated import (
    AccountStatus,
    ActivateAccount,
    ActivateAccountRequest,
    ActivateAccountResponse,
    ActivatedAccount,
    ErrorResponse,
    ExecutionSummary,
    StandardCapabilityName,
    UpdatedEffect,
)
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    ActivateAccountRequest,
    ResponseBodyMap,
    ActivateAccountResponse | ErrorResponse,
]


def case_activate_account_200() -> Case:
    """Activate Account - Successful case."""
    request = ActivateAccount(
        account_id="1",
    )

    args = ActivateAccountRequest(
        request=request,
        auth=VALID_AUTH,
        settings=SETTINGS,
    )

    response_body_map = {{
        "PUT": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ActivateAccountResponse(
        response=ActivatedAccount(activated=True, status=AccountStatus.ACTIVE),
        # Optional: Include execution_summary for activation operations
        execution_summary=ExecutionSummary(
            effect=UpdatedEffect(),
            request_fingerprint=request.fingerprint(),
            is_idempotent=True,
            description="Successfully activated user account",
        ),
    )
    return StandardCapabilityName.ACTIVATE_ACCOUNT, args, response_body_map, expected_response
