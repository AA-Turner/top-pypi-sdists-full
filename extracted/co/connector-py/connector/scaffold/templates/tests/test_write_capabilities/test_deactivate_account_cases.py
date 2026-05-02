"""Cases for testing ``deactivate_account`` capability."""

import typing as t

import httpx
from connector.generated import (
    AccountStatus,
    DeactivateAccount,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeactivatedAccount,
    ErrorResponse,
    ExecutionSummary,
    StandardCapabilityName,
    UpdatedEffect,
)
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    DeactivateAccountRequest,
    ResponseBodyMap,
    DeactivateAccountResponse | ErrorResponse,
]


def case_deactivate_account_200() -> Case:
    """Deactivate Account - Successful case."""
    request = DeactivateAccount(
        account_id="1",
    )

    args = DeactivateAccountRequest(
        request=request,
        auth=VALID_AUTH,
        settings=SETTINGS,
    )

    response_body_map = {{
        "PATCH": {{
            "/api/now/table/sys_user/1": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = DeactivateAccountResponse(
        response=DeactivatedAccount(deactivated=True, status=AccountStatus.SUSPENDED),
        raw_data=None,
        # Optional: Include execution_summary for deactivation operations
        execution_summary=ExecutionSummary(
            effect=UpdatedEffect(),
            request_fingerprint=request.fingerprint(),
            is_idempotent=True,
            description="Successfully deactivated user account",
        ),
    )
    return StandardCapabilityName.DEACTIVATE_ACCOUNT, args, response_body_map, expected_response
