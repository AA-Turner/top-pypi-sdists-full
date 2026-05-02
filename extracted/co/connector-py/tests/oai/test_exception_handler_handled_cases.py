import json
import typing as t

import httpx
from connector.oai.errors import ConnectorError, HTTPHandler
from connector.oai.integration import DescriptionData, Integration
from connector_sdk_types.errors import ConnectorErrorCode, build_metadata
from connector_sdk_types.generated import (
    BasicCredential,
    Error,
    ErrorCode,
    ErrorResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    StandardCapabilityName,
)

Case = tuple[
    Integration,
    StandardCapabilityName,
    str,
    dict[str, t.Any],
]


def _expected_dict(resp: ErrorResponse, hint: str | None = None) -> dict[str, t.Any]:
    """
    Serialise an expected ErrorResponse to a dict for comparison with dispatch output.

    Automatically populates ``error.error_metadata`` from the resolved error code so
    tests don't need to construct it manually.  Pass ``hint`` when the exception that
    will be raised carries a non-None DEFAULT_HINT (e.g. plain ConnectorError instances).
    """
    if isinstance(resp.error.error_code, ConnectorErrorCode):
        resp.error.error_metadata = build_metadata(resp.error.error_code, hint=hint)
    return resp.model_dump()


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
            error_code=ConnectorErrorCode.UNAUTHORIZED,
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
        _expected_dict(expected_response),
    )


def case_http_status_error_400() -> Case:
    """Test if HTTPStatusError with 400 status can be handled with HTTPHandler."""
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
    requested_url = "https://httpstat.us/400"
    response_status_code = httpx.codes.BAD_REQUEST

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="400 Bad Request",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

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
            message="[400][https://httpstat.us/400] 400 Bad Request",
            error_code=ConnectorErrorCode.BAD_REQUEST,
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
        _expected_dict(expected_response),
    )


def case_http_status_error_403() -> Case:
    """Test if HTTPStatusError with 403 status can be handled with HTTPHandler."""
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
    requested_url = "https://httpstat.us/403"
    response_status_code = httpx.codes.FORBIDDEN

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="403 Forbidden",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

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
            message="[403][https://httpstat.us/403] 403 Forbidden",
            error_code=ConnectorErrorCode.PERMISSION_DENIED,
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
        _expected_dict(expected_response),
    )


def case_http_status_error_404() -> Case:
    """Test if HTTPStatusError with 404 status can be handled with HTTPHandler."""
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
    requested_url = "https://httpstat.us/404"
    response_status_code = httpx.codes.NOT_FOUND

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="404 Not Found",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

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
            message="[404][https://httpstat.us/404] 404 Not Found",
            error_code=ConnectorErrorCode.NOT_FOUND,
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
        _expected_dict(expected_response),
    )


def case_http_status_error_429() -> Case:
    """Test if HTTPStatusError with 429 status can be handled with HTTPHandler."""
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
    requested_url = "https://httpstat.us/429"
    response_status_code = httpx.codes.TOO_MANY_REQUESTS

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="429 Too Many Requests",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

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
            message="[429][https://httpstat.us/429] 429 Too Many Requests",
            error_code=ConnectorErrorCode.RATE_LIMIT,
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
        _expected_dict(expected_response),
    )


def case_http_status_error_502() -> Case:
    """Test if HTTPStatusError with 502 status can be handled with HTTPHandler."""
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
    requested_url = "https://httpstat.us/502"
    response_status_code = httpx.codes.BAD_GATEWAY

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="502 Bad Gateway",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

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
            message="[502][https://httpstat.us/502] 502 Bad Gateway",
            error_code=ConnectorErrorCode.BAD_GATEWAY,
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
        _expected_dict(expected_response),
    )


def case_http_status_error_500() -> Case:
    """Test if HTTPStatusError with 500 status can be handled with HTTPHandler."""
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
    requested_url = "https://httpstat.us/500"
    response_status_code = httpx.codes.INTERNAL_SERVER_ERROR

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                text="500 Internal Server Error",
                status_code=response_status_code,
            )

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            _response_text = client.get(requested_url).raise_for_status().text

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
            message="[500][https://httpstat.us/500] 500 Internal Server Error",
            error_code=ConnectorErrorCode.BAD_GATEWAY,
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
        _expected_dict(expected_response),
    )


def case_connect_error() -> Case:
    """Test if httpx.ConnectError will be handled with DefaultHandler."""
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
    requested_url = "https://example.com"
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("name or service not known")

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            client.get(requested_url).raise_for_status()

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
            message="Failed to connect to the API. Please verify the URL or try at a later time due to a potential temporary network issue.",
            error_code=ConnectorErrorCode.CONNECTION_TIMEOUT,
            app_id=app_id,
            status_code=None,
            raised_by="ConnectError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response),
    )


def case_illegal_header_error() -> Case:
    """Test if 'Illegal header' errors are handled with DefaultHandler."""
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
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise Exception("Illegal header value: contains newline")

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
            message="Illegal header constructed for API request. Please check the app configuration and try again.",
            error_code=ConnectorErrorCode.BAD_REQUEST,
            app_id=app_id,
            status_code=None,
            raised_by="Exception",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response),
    )


def case_connection_error_message() -> Case:
    """Test if connection errors with specific messages are handled with DefaultHandler."""
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
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise Exception("nodename nor servname provided, or not known")

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
            message="Failed to connect to the API. Please verify the URL or try at a later time due to a potential temporary network issue.",
            error_code=ConnectorErrorCode.CONNECTION_TIMEOUT,
            app_id=app_id,
            status_code=None,
            raised_by="Exception",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response),
    )


def case_json_decode_error() -> Case:
    """Test if json.JSONDecodeError will be handled with DefaultHandler."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="hi, testing", categories=[]),
    )
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise json.JSONDecodeError("Expecting value", "invalid json", 0)

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
            message="Failed to parse JSON response: Expecting value: line 1 column 1 (char 0)",
            error_code=ConnectorErrorCode.INVALID_RESPONSE,
            app_id=app_id,
            status_code=None,
            raised_by="JSONDecodeError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response),
    )


def _make_http_status_case(
    status_code: int, status_text: str, expected_code: ConnectorErrorCode
) -> Case:
    """Helper to reduce boilerplate for HTTPHandler status-code cases."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[(httpx.HTTPStatusError, HTTPHandler, None)],
        description_data=DescriptionData(user_friendly_name="hi, testing", categories=[]),
    )
    requested_url = f"https://httpstat.us/{status_code}"
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        def request_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(text=status_text, status_code=status_code)

        with httpx.Client(transport=httpx.MockTransport(request_handler)) as client:
            client.get(requested_url).raise_for_status()
        return ListAccountsResponse(response=[], raw_data=None)

    request_data = json.dumps(
        {"auth": {"basic": {"username": "user", "password": "pass"}}, "request": {}}
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=f"[{status_code}][{requested_url}] {status_text}",
            error_code=expected_code,
            app_id=app_id,
            status_code=status_code,
            raised_by="HTTPStatusError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response),
    )


def case_http_status_error_413() -> Case:
    """413 Content Too Large → BAD_REQUEST."""
    return _make_http_status_case(413, "413 Content Too Large", ConnectorErrorCode.BAD_REQUEST)


def case_http_status_error_415() -> Case:
    """415 Unsupported Media Type → BAD_REQUEST."""
    return _make_http_status_case(415, "415 Unsupported Media Type", ConnectorErrorCode.BAD_REQUEST)


def case_http_status_error_422() -> Case:
    """422 Unprocessable Entity → BAD_REQUEST."""
    return _make_http_status_case(422, "422 Unprocessable Entity", ConnectorErrorCode.BAD_REQUEST)


def case_http_status_error_405() -> Case:
    """405 Method Not Allowed → UNSUPPORTED_OPERATION."""
    return _make_http_status_case(
        405, "405 Method Not Allowed", ConnectorErrorCode.UNSUPPORTED_OPERATION
    )


def case_http_status_error_406() -> Case:
    """406 Not Acceptable → UNSUPPORTED_OPERATION."""
    return _make_http_status_case(
        406, "406 Not Acceptable", ConnectorErrorCode.UNSUPPORTED_OPERATION
    )


def case_http_status_error_501() -> Case:
    """501 Not Implemented → UNSUPPORTED_OPERATION."""
    return _make_http_status_case(
        501, "501 Not Implemented", ConnectorErrorCode.UNSUPPORTED_OPERATION
    )


def case_http_status_error_408() -> Case:
    """408 Request Timeout → REQUEST_TIMEOUT."""
    return _make_http_status_case(408, "408 Request Timeout", ConnectorErrorCode.REQUEST_TIMEOUT)


def case_http_status_error_409() -> Case:
    """409 Conflict → CONFLICT."""
    return _make_http_status_case(409, "409 Conflict", ConnectorErrorCode.CONFLICT)


def case_http_status_error_503() -> Case:
    """503 Service Unavailable → SERVICE_ERROR."""
    return _make_http_status_case(503, "503 Service Unavailable", ConnectorErrorCode.SERVICE_ERROR)


def case_http_status_error_504() -> Case:
    """504 Gateway Timeout → BAD_GATEWAY."""
    return _make_http_status_case(504, "504 Gateway Timeout", ConnectorErrorCode.BAD_GATEWAY)


def case_connector_error_with_deprecated_api_error() -> Case:
    """ConnectorError with deprecated ErrorCode.API_ERROR → redirected to INVALID_RESPONSE."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="hi, testing", categories=[]),
    )
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise ConnectorError(message="api error occurred", error_code=ErrorCode.API_ERROR)

    request_data = json.dumps(
        {"auth": {"basic": {"username": "user", "password": "pass"}}, "request": {}}
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="api error occurred",
            error_code=ConnectorErrorCode.INVALID_RESPONSE,
            app_id=app_id,
            status_code=None,
            raised_by="ConnectorError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response, hint=ConnectorError.DEFAULT_HINT),
    )


def case_connector_error_with_deprecated_unauthenticated() -> Case:
    """ConnectorError with deprecated ErrorCode.UNAUTHENTICATED → redirected to UNAUTHORIZED."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="hi, testing", categories=[]),
    )
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise ConnectorError(message="legacy unauthenticated", error_code=ErrorCode.UNAUTHENTICATED)

    request_data = json.dumps(
        {"auth": {"basic": {"username": "user", "password": "pass"}}, "request": {}}
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="legacy unauthenticated",
            error_code=ConnectorErrorCode.UNAUTHORIZED,
            app_id=app_id,
            status_code=None,
            raised_by="ConnectorError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response, hint=ConnectorError.DEFAULT_HINT),
    )


def case_connector_error_with_sdk_error_code() -> Case:
    """ConnectorError with ConnectorErrorCode passes through unchanged."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="hi, testing", categories=[]),
    )
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise ConnectorError(
            message="rate limited",
            error_code=ConnectorErrorCode.RATE_LIMIT,
            app_error_code="app.429",
        )

    request_data = json.dumps(
        {"auth": {"basic": {"username": "user", "password": "pass"}}, "request": {}}
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="rate limited",
            error_code=ConnectorErrorCode.RATE_LIMIT,
            app_id=app_id,
            app_error_code="app.429",
            status_code=None,
            raised_by="ConnectorError",
            raised_in=f"{__name__}:{capability_name.value}",
        ),
    )
    return (
        integration,
        StandardCapabilityName.LIST_ACCOUNTS,
        request_data,
        _expected_dict(expected_response, hint=ConnectorError.DEFAULT_HINT),
    )
