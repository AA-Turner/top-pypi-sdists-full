"""Cases for testing ``list_resources`` capability."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ListResources,
    ListResourcesRequest,
    ListResourcesResponse,
)
from connector.utils.test import http_error_message

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from connector.generated.models.standard_capability_name import StandardCapabilityName

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
