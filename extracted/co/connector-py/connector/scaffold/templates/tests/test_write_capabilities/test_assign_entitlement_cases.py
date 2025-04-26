"""Cases for testing ``assign_entitlement`` capability."""

import typing as t

import httpx
from connector.generated import (
    AssignedEntitlement,
    AssignEntitlement,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
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
    AssignEntitlementRequest,
    ResponseBodyMap,
    AssignEntitlementResponse | ErrorResponse,
]


# repeat following cases for all entitlements

def case_assign_entitlement_1_200() -> Case:
    """Succeed with changing entitlement."""
    args = AssignEntitlementRequest(
            request=AssignEntitlement(
                account_integration_specific_id="",
                resource_integration_specific_id="",
                resource_type="",
                entitlement_integration_specific_id="",
                entitlement_type="",
            ),
            auth=VALID_AUTH,
            settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = AssignEntitlementResponse(
        response=AssignedEntitlement(assigned=True),
    )
    return StandardCapabilityName.ASSIGN_ENTITLEMENT, args, response_body_map, expected_response


def case_assign_non_existing_entitlement_1_400() -> Case:
    """Try to assign non-existing entitlement."""
    args = AssignEntitlementRequest(
            request=AssignEntitlement(
                account_integration_specific_id="",
                resource_integration_specific_id="",
                resource_type="",
                entitlement_integration_specific_id="",
                entitlement_type="",
            ),
            auth=VALID_AUTH,
            settings=SETTINGS,
    )

    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                400,
            ),
            status_code=httpx.codes.BAD_REQUEST,
            error_code=ErrorCode.BAD_REQUEST,
            app_id="{name}",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return StandardCapabilityName.ASSIGN_ENTITLEMENT, args, response_body_map, expected_response
