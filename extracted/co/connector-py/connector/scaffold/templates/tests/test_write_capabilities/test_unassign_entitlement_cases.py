"""Cases for testing ``unassign_entitlement`` capability."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    UnassignedEntitlement,
    UnassignEntitlement,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
)
from connector.utils.test import http_error_message

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from connector.generated.models.standard_capability_name import StandardCapabilityName

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    UnassignEntitlementRequest,
    ResponseBodyMap,
    UnassignEntitlementResponse | ErrorResponse,
]

# repeat following casess for all entitlements

def case_assign_entitlement_1_404() -> Case:
    """Authorized request for non-existing entitlement should fail."""
    args = UnassignEntitlementRequest(
        request=UnassignEntitlement(
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
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            app_id="{name}",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return StandardCapabilityName.UNASSIGN_ENTITLEMENT, args, response_body_map, expected_response


def case_unassign_entitlement_1_200() -> Case:
    """Successfully unassign entitlement."""
    args = UnassignEntitlementRequest(
        request=UnassignEntitlement(
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
    expected_response = UnassignEntitlementResponse(
        response=UnassignedEntitlement(unassigned=True),
    )
    return StandardCapabilityName.UNASSIGN_ENTITLEMENT, args, response_body_map, expected_response
