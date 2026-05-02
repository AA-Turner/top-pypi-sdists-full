"""Cases for testing ``create_account`` capability."""

import typing as t

import httpx
from connector.generated import (
    AccountStatus,
    CreateAccountEntitlement,
    CreateAccountResponse,
    CreatedAccount,
    CreatedEffect,
    Error,
    ErrorCode,
    ErrorResponse,
    ExecutionSummary,
    NoopEffect,
    NoopEffectReason,
    StandardCapabilityName,
)
from connector.oai.capability import CustomRequest
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap
from {name}.dto.user import CreateAccount

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    CustomRequest[CreateAccount],
    ResponseBodyMap,
    CreateAccountResponse | ErrorResponse,
]


def case_create_account_201() -> Case:
    """Successful creation request."""
    request = CreateAccount(
        email="jw7rT@example.com",
        entitlements=[],
    )

    args = CustomRequest(
        request=request,
        auth=VALID_AUTH,
        settings=SETTINGS,
    )

    response_body_map = {{
        "GET": {{
            f"/users?email={{request.email}}": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.CREATED,
                response_body={{"id": "user_123"}},
            ),
        }},
    }}
    expected_response = CreateAccountResponse(
        response=CreatedAccount(
            id="user_123",
            created=True,
            status=AccountStatus.ACTIVE,
        ),
        # Optional: Include execution_summary to track operation metadata
        execution_summary=ExecutionSummary(
            effect=CreatedEffect(),
            request_fingerprint=request.fingerprint(),
            is_idempotent=True,
            description="Successfully created new user account",
        ),
    )
    return StandardCapabilityName.CREATE_ACCOUNT, args, response_body_map, expected_response


def case_create_account_200_already_exists() -> Case:
    """Account already exists - idempotent NOOP."""
    request = CreateAccount(
        email="existing@example.com",
        entitlements=[],
    )

    args = CustomRequest(
        request=request,
        auth=VALID_AUTH,
        settings=SETTINGS,
    )

    response_body_map = {{
        "GET": {{
            "/users?email=existing@example.com": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{"id": "existing_user_123"}},
            ),
        }},
    }}
    expected_response = CreateAccountResponse(
        response=CreatedAccount(
            id="existing_user_123",
            created=True,
            status=AccountStatus.ACTIVE,
        ),
        execution_summary=ExecutionSummary(
            effect=NoopEffect(reason=NoopEffectReason.STATE_ALREADY_MATCHES),
            request_fingerprint=request.fingerprint(),
            is_idempotent=True,
            description="Account already exists for existing@example.com",
        ),
    )
    return StandardCapabilityName.CREATE_ACCOUNT, args, response_body_map, expected_response


def case_create_account_201_with_entitlement_failures() -> Case:
    """Account created successfully with partial entitlement assignment failures."""
    request = CreateAccount(
        email="new@example.com",
        entitlements=[
            CreateAccountEntitlement(
                integration_specific_id="admin_role",
                integration_specific_resource_id="dev-lumos",
                entitlement_type="role",
            ),
            CreateAccountEntitlement(
                integration_specific_id="premium_license",
                integration_specific_resource_id="dev-lumos",
                entitlement_type="license",
            ),
        ],
    )

    args = CustomRequest(
        request=request,
        auth=VALID_AUTH,
        settings=SETTINGS,
    )

    response_body_map = {{
        "GET": {{
            f"/users?email={{request.email}}": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.CREATED,
                response_body={{"id": "user_456"}},
            ),
            "/users/user_456/entitlements/admin_role": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
            "/users/user_456/entitlements/premium_license": MockedResponse(
                status_code=httpx.codes.FORBIDDEN,
                response_body={{"error": "License quota exceeded"}},
            ),
        }},
    }}
    expected_response = CreateAccountResponse(
        response=CreatedAccount(
            id="user_456",
            created=True,
            status=AccountStatus.ACTIVE,
        ),
        execution_summary=ExecutionSummary(
            effect=CreatedEffect(),
            request_fingerprint=request.fingerprint(),
            is_idempotent=True,
            description="Successfully created new user account",
            caught_errors=[
                Error(
                    message="Failed to assign entitlement premium_license: License quota exceeded",
                    error_code=ErrorCode.API_ERROR,
                    app_id="{name}",
                )
            ],
        ),
    )
    return StandardCapabilityName.CREATE_ACCOUNT, args, response_body_map, expected_response
