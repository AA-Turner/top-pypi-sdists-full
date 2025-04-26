"""Cases for testing ``list_accounts`` capability."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ListAccounts,
    ListAccountsRequest,
    ListAccountsResponse,
    Page,
)
from connector.generated.models.standard_capability_name import StandardCapabilityName
from {name}.pagination import NextPageToken, Pagination
from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH, TEST_MAX_PAGE_SIZE
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    ListAccountsRequest,
    ResponseBodyMap,
    ListAccountsResponse | ErrorResponse,
]


def case_list_accounts_200() -> Case:
    """Successful request."""
    args = ListAccountsRequest(
        request=ListAccounts(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListAccountsResponse(
        response=[],
        page=NextPageToken.from_paginations(
            [Pagination(endpoint="", offset=2)]).to_page(size=TEST_MAX_PAGE_SIZE)
    )
    return StandardCapabilityName.LIST_ACCOUNTS, args, response_body_map, expected_response


def case_list_accounts_200_no_accounts() -> Case:
    """No accounts found."""
    args = ListAccountsRequest(
        request=ListAccounts(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListAccountsResponse(
        response=[],
    )
    return StandardCapabilityName.LIST_ACCOUNTS, args, response_body_map, expected_response
