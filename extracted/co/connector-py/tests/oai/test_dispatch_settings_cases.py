"""Test cases for ``Integration.dispatch`` function.

Those cases should lead to raised error.
"""

import json

from connector.generated import (
    BasicCredential,
    Error,
    ErrorCode,
    ErrorResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    StandardCapabilityName,
)
from connector.oai.integration import DescriptionData, Integration
from pydantic import BaseModel

Case = tuple[
    Integration,
    StandardCapabilityName,
    str,
    BaseModel,
]


class SettingsFixture(BaseModel):
    host: str


def new_integration(
    *,
    settings_model: type[BaseModel] | None,
) -> Integration:
    return Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        handle_errors=True,
        settings_model=settings_model,
        description_data=DescriptionData(
            user_friendly_name="testing thing",
            categories=[],
        ),
    )


def case_valid_settings_are_fine() -> Case:
    """If somebody passes good settings, we should dispatch as normal"""
    integration = new_integration(settings_model=SettingsFixture)

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(response=[])

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"basic": {"username": "foo", "password": "bar"}},
            "request": {},
            "settings": {"host": "https://not-checked"},
        }
    )
    expected_response = ListAccountsResponse(response=[])
    return integration, capability_name, request, expected_response


def case_no_settings_are_fine_for_no_model() -> Case:
    """If somebody passes _no_ settings and there's no model, we should dispatch as normal

    ...until Settings are required"""
    integration = new_integration(settings_model=None)

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(response=[])

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"basic": {"username": "foo", "password": "bar"}},
            "request": {},
        }
    )
    expected_response = ListAccountsResponse(response=[])
    return integration, capability_name, request, expected_response


def case_invalid_settings_are_error() -> Case:
    """If the caller passes an invalid settings object, dispatching should return an error."""
    integration = new_integration(settings_model=SettingsFixture)

    @integration.register_capability(StandardCapabilityName.LIST_ACCOUNTS)
    def list_accounts(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(response=[])

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"basic": {"username": "foo", "password": "bar"}},
            "request": {},
            "settings": {"something": "incorrect"},
        }
    )
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            error_code=ErrorCode.BAD_REQUEST,
            message="Invalid settings passed on request",
            raised_by=None,
            raised_in=None,
            status_code=None,
            app_id="test",
        ),
    )
    return integration, capability_name, request, expected_response
