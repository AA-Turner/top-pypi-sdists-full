"""Cases for testing ``create_account`` capability."""

import typing as t

import httpx
from connector.generated import (
    AccountStatus,
    CreateAccountEntitlement,
    CreateAccountResponse,
    CreatedAccount,
    Error,
    ErrorCode,
    ErrorResponse,
)

from connector.oai.capability import CustomRequest
from {name}.dto.user import CreateAccount


from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from connector.generated.models.standard_capability_name import StandardCapabilityName

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    CustomRequest[CreateAccount],
    ResponseBodyMap,
    CreateAccountResponse | ErrorResponse,
]


def case_create_account_201() -> Case:
    """Successful creation request."""
    args = CustomRequest(
        request=CreateAccount(
            email="jw7rT@example.com",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="read_only_user",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="role",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="license",
                ),
            ],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )

    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.CREATED,
                response_body={{}},
            ),
        }},
    }}
    expected_response = CreateAccountResponse(
        response=CreatedAccount(created=True, status=AccountStatus.ACTIVE),
    )
    return StandardCapabilityName.CREATE_ACCOUNT, args, response_body_map, expected_response


def case_create_account_400_too_many_entitlements() -> Case:
    """
    Invalid request when creating an account with entitlements
    that are not necessary or entitlements of different type/count.
    """
    args = CustomRequest(
        request=CreateAccount(
            email="jw7rT@example.com",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),

            ],
        ),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="{name}",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return StandardCapabilityName.CREATE_ACCOUNT, args, response_body_map, expected_response
