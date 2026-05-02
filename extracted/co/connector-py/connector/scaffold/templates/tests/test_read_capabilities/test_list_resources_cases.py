"""Cases for testing ``list_resources`` capability."""

import typing as t

import httpx
from connector.generated import (
    ErrorResponse,
    ListResources,
    ListResourcesRequest,
    ListResourcesResponse,
    StandardCapabilityName,
)
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    ListResourcesRequest,
    ResponseBodyMap,
    ListResourcesResponse | ErrorResponse,
]


def case_list_resources_200() -> Case:
    """Successful request."""
    args = ListResourcesRequest(
        request=ListResources(),
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
    expected_response = ListResourcesResponse(
        response=[],
    )
    return StandardCapabilityName.LIST_RESOURCES, args, response_body_map, expected_response
