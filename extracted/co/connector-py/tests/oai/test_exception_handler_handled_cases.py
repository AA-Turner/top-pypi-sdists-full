import json
import typing as t

import httpx
from connector.generated import (
    BasicCredential,
    Error,
    ErrorCode,
    ErrorResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    StandardCapabilityName,
)
from connector.oai.errors import HTTPHandler
from connector.oai.integration import DescriptionData, Integration

Case = tuple[
    Integration,
    StandardCapabilityName,
    str,
    dict[str, t.Any],
]


def case_http_status_error() -> Case:
    """Test if HTTPStatusError can be handled with HTTPHandler.

    We register capability that is mocked to raise ``HTTPStatusError``.
    Since the integration has ``HTTPHandler`` registered for handling
    such error, we should end up with ``ErrorResponse`` that contains
    the details about HTTP error.
    """
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[
            (httpx.HTTPStatusError, HTTPHandler, None),
        ],
        description_data=DescriptionData(user_friendly_name="hi, testing", categories=[]),
    )
    # will be mocked with actual response just to avoid making request
    requested_url = "https://httpstat.us/401"
    response_status_code = httpx.codes.UNAUTHORIZED

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="401 Unauthorized",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

        # this should never happen
        return ListAccountsResponse(
            response=[],
            raw_data=None,
        )

    request_data = json.dumps(
        {
            "auth": {"basic": {"username": "user", "password": "pass"}},
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="[401][https://httpstat.us/401] 401 Unauthorized",
            error_code=ErrorCode.UNAUTHORIZED,
            app_id=app_id,
            status_code=response_status_code,
            raised_by="HTTPStatusError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        expected_response.model_dump(),
    )
