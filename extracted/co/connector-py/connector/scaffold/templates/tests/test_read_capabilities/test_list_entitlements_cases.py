"""Cases for testing ``list_entitlements`` capability."""

import typing as t

import httpx
from connector.generated import (
    ErrorResponse,
    ListEntitlements,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    Page,
    StandardCapabilityName,
)
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    ListEntitlementsRequest,
    ResponseBodyMap,
    ListEntitlementsResponse | ErrorResponse,
]


def case_list_entitlements_200() -> Case:
    """Successful request."""
    args = ListEntitlementsRequest(
        request=ListEntitlements(),
        auth=VALID_AUTH,
        settings=SETTINGS,
        page=Page(
            size=5,
        ),
    )
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListEntitlementsResponse(
        response=[],
    )
    return StandardCapabilityName.LIST_ENTITLEMENTS, args, response_body_map, expected_response
