"""Cases for testing ``find_entitlement_associations`` capability."""

import typing as t

import httpx
from connector.generated import (
    ErrorResponse,
    FindEntitlementAssociations,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    StandardCapabilityName,
)
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    FindEntitlementAssociationsRequest,
    ResponseBodyMap,
    FindEntitlementAssociationsResponse | ErrorResponse,
]


def case_find_entitlement_associations_1_200() -> Case:
    """Succeed with finding entitlement associations."""
    args = FindEntitlementAssociationsRequest(
        request=FindEntitlementAssociations(),
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
    expected_response = FindEntitlementAssociationsResponse(
        response=[],
    )
    return StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS, args, response_body_map, expected_response


def case_find_entitlement_associations_1_empty_200() -> Case:
    """Succeed with getting empty entitlement associations."""
    args = FindEntitlementAssociationsRequest(
        request=FindEntitlementAssociations(),
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
    expected_response = FindEntitlementAssociationsResponse(
        response=[],
    )
    return StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS, args, response_body_map, expected_response
