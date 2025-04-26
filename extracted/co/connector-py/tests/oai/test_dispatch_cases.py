"""Test cases for ``Integration.dispatch`` function."""

import json
import typing as t

from connector.generated import (
    AuthModel,
    BasicCredential,
    CredentialConfig,
    Error,
    ErrorCode,
    ErrorResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    StandardCapabilityName,
)
from connector.oai.capability import CustomRequest, CustomResponse, get_basic_auth
from connector.oai.integration import DescriptionData, Integration

from .shared_types import (
    AccioRequest,
    AccioResponse,
)

Case = tuple[
    Integration,
    str,
    str,
    t.Any,
]


def new_integration() -> Integration:
    return Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="testing thing",
            categories=[],
        ),
    )


def new_integration_with_credentials() -> Integration:
    credentials = [
        CredentialConfig(
            id="test",
            description="Test credential",
            type=AuthModel.BASIC,
        ),
        CredentialConfig(
            id="test2",
            description="Test credential 2",
            type=AuthModel.TOKEN,
            optional=True,
        ),
    ]

    return Integration(
        app_id="test",
        version="0.1.0",
        credentials=credentials,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="testing thing",
            categories=[],
        ),
    )


def case_dispatch_not_implemented_handled() -> Case:
    integration = new_integration()
    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    # don't have to care about actual request data, integration should reject the call before it touches it
    request = "{}"
    expected_response = ErrorResponse(
        error=Error(
            message="Capability 'list_accounts' is not implemented.",
            error_code=ErrorCode.NOT_IMPLEMENTED,
            app_id="test",
        ),
        is_error=True,
    )
    return integration, capability_name, request, expected_response


def case_dispatch_async_success() -> Case:
    """Calling working async method should return positive response."""
    integration = new_integration()

    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def capability(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(
            response=[],
            raw_data=None,
        )

    request = json.dumps(
        {
            "request": {},
            "auth": {
                "basic": {
                    "username": "test",
                    "password": "test",
                }
            },
        }
    )

    expected_response = ListAccountsResponse(
        response=[],
        raw_data=None,
        page=None,
    )

    return integration, capability_name, request, expected_response


def case_dispatch_async_error_handled() -> Case:
    """Unhandled error in async capability should get translated into an error response."""
    integration = new_integration()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"basic": {"username": "user", "password": "pass"}},
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="",
            raised_by="CustomException",
            raised_in="tests.oai.test_dispatch_cases:list_accounts",
            error_code=ErrorCode.UNEXPECTED_ERROR,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_sync_not_handled_error() -> Case:
    """Unhandled error in sync capability should get translated into an error response."""
    integration = new_integration()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"basic": {"username": "user", "password": "pass"}},
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="",
            raised_by="CustomException",
            raised_in="tests.oai.test_dispatch_cases:list_accounts",
            error_code=ErrorCode.UNEXPECTED_ERROR,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_incorrect_auth_model() -> Case:
    """If a client calls us with the wrong style auth object, return an error."""
    integration = new_integration()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException  # shouldn't get hit

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"oauth": {"access_token": "hi"}},
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Missing 'basic' auth in request",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_malformed_auth() -> Case:
    """If a client calls us with the wrong shape of an auth object, return an error."""
    integration = new_integration()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            # This is an old style, get outta here!
            "auth": {"basic": {"access_token": "foobar"}},
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Malformed auth in request",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_missing_auth_or_credentials() -> Case:
    """If a client calls us without auth or credentials, return an error."""
    integration = new_integration()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        print("ARGS: ", args)
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            # No "auth" here
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Missing auth/credentials in request",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_duplicate_credentials() -> Case:
    """If a client calls us with auth+credentials, return an error."""
    integration = new_integration()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {
                "basic": {
                    "username": "test",
                    "password": "test",
                }
            },
            "credentials": {
                "basic": {
                    "username": "test",
                    "password": "test",
                }
            },
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Cannot pass credentials and auth in the same request, if you've meant to make this connector multi-auth compatible, please remove the auth field.",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_credentials() -> Case:
    """If a client calls us with auth+credentials, return an error."""
    integration = new_integration_with_credentials()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "credentials": [
                {
                    "id": "test",
                    "basic": {
                        "username": "test",
                        "password": "test",
                    },
                }
            ],
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="",
            raised_by="CustomException",
            raised_in="tests.oai.test_dispatch_cases:list_accounts",
            error_code=ErrorCode.UNEXPECTED_ERROR,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_credentials_id_mismatch() -> Case:
    """If a client calls us with auth+credentials, return an error."""
    integration = new_integration_with_credentials()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "credentials": [
                {
                    "id": "wrong_id",
                    "basic": {
                        "username": "test",
                        "password": "test",
                    },
                }
            ],
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Credential with id 'wrong_id' not expected",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_credentials_missing_type() -> Case:
    """If a client calls us with auth+credentials, return an error."""
    integration = new_integration_with_credentials()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "credentials": [
                {
                    "id": "test",
                    "oauth": {
                        "access_token": "test",
                    },
                }
            ],
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Missing 'basic' credential in request",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_credentials_missing_id() -> Case:
    """If a client calls us with auth+credentials, return an error."""
    integration = new_integration_with_credentials()

    class CustomException(Exception):
        pass

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    async def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        raise CustomException

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "credentials": [
                {
                    # No id here
                    "oauth": {
                        "access_token": "test",
                    },
                }
            ],
            "request": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Missing ID in credential at index 0",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response


def case_dispatch_custom_capability_success() -> Case:
    integration = new_integration()

    @integration.register_custom_capability("accio", description="A summoning charm.")
    async def custom_capability(args: CustomRequest[AccioRequest]) -> CustomResponse[AccioResponse]:
        # Keep this here to verify we can pull of demarshalled auths
        get_basic_auth(args)
        return CustomResponse(
            response=AccioResponse(success=True),
        )

    capability_name = "accio"
    request = json.dumps(
        {
            "request": {
                "object_name": "Firebolt",
            },
            "settings": {},
            "auth": {
                "basic": {
                    "username": "test",
                    "password": "test",
                }
            },
        }
    )
    expected_response = CustomResponse(response=AccioResponse(success=True))

    return integration, capability_name, request, expected_response


def case_dispatch_custom_capability_missing_auth() -> Case:
    integration = new_integration()

    @integration.register_custom_capability("accio", description="A summoning charm.")
    async def custom_capability(args: CustomRequest[AccioRequest]) -> CustomResponse[AccioResponse]:
        return CustomResponse(
            response=AccioResponse(success=True),
        )

    capability_name = "accio"
    request = json.dumps(
        {
            "request": {
                "object_name": "Firebolt",
            },
            "auth": {},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Missing 'basic' auth in request",
            error_code=ErrorCode.BAD_REQUEST,
            app_id="test",
        ),
    )

    return integration, capability_name, request, expected_response
