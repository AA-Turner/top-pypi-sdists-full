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
)
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

from connector.generated.models.standard_capability_name import StandardCapabilityName

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    DeactivateAccountRequest,
    ResponseBodyMap,
    DeactivateAccountResponse | ErrorResponse,
]


def case_deactivate_account_200() -> Case:
    """Deactivate Account - Successful case."""
    args = DeactivateAccountRequest(
        request=DeactivateAccount(
            account_id="1",
        ),
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
    )
    return StandardCapabilityName.DEACTIVATE_ACCOUNT, args, response_body_map, expected_response
