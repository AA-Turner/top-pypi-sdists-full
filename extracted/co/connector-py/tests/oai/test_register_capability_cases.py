"""Test cases for ``Integration.info`` function."""

import typing as t

import pytest
from connector.generated import (
    AccountStatus,
    Amount,
    BasicCredential,
    CreateAccountRequest,
    CreateAccountResponse,
    CreatedAccount,
    Expense,
    ExpenseApprovalStatus,
    ExpensePaymentStatus,
    ExpenseType,
    ListAccountsRequest,
    ListAccountsResponse,
    ListExpensesRequest,
    ListExpensesResponse,
    NormalizedExpenseApprovalStatus,
    NormalizedExpensePaymentStatus,
    SpendUser,
    StandardCapabilityName,
    Vendor,
)
from connector.oai.capability import CapabilityCallableProto, CustomRequest, CustomResponse
from connector.oai.integration import (
    DescriptionData,
    Integration,
    InvalidCapabilityNameError,
    ReservedCapabilityNameError,
)

from .shared_types import (
    AccioRequest,
    AccioResponse,
)

Case: t.TypeAlias = tuple[
    str,
    dict[str, CapabilityCallableProto[t.Any]],
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


def case_register_capability_success() -> Case:
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

    return capability_name.value, integration.capabilities


def case_register_list_expenses_success() -> Case:
    integration = new_integration()
    capability_name = StandardCapabilityName.LIST_EXPENSES

    @integration.register_capability(capability_name)
    async def capability(
        args: ListExpensesRequest,
    ) -> ListExpensesResponse:
        return ListExpensesResponse(
            response=[
                Expense(
                    id="2652b217-d686-4277-aad5-37320e9d9912",
                    report_id="bfc896e8-4bca-4aa4-87df-6341b22ed44d",
                    transaction_date="2024-01-01T:00:00+00:00",
                    payment_date="2024-01-03T:00:00+00:00",
                    total_amount=Amount(
                        amount="100.00",
                        currency="USD",
                    ),
                    paid_amount=Amount(
                        amount="100.00",
                        currency="USD",
                    ),
                    seller=Vendor(
                        id="f2d8d6a7-1a1a-4b3d-a092-936a7b32a0b3",
                        name="Adobe",
                        description="A leading software company known for its creativity products",
                    ),
                    description="Creative Cloud for the Marketing team",
                    type=ExpenseType.REIMBURSEMENT,
                    approval_status=ExpenseApprovalStatus(
                        display_value="Approved",
                        normalized_value=NormalizedExpenseApprovalStatus.APPROVED,
                    ),
                    payment_status=ExpensePaymentStatus(
                        display_value="Paid",
                        normalized_value=NormalizedExpensePaymentStatus.PAID,
                    ),
                    submitter=SpendUser(
                        id="6da0e939-9ba9-497c-bf05-a86e95cbbb49",
                        email="harry@hogwarts.edu",
                    ),
                )
            ],
            raw_data=None,
        )

    return capability_name.value, integration.capabilities


def case_register_capability_with_metadata_success() -> Case:
    integration = new_integration()
    capability_name = StandardCapabilityName.CREATE_ACCOUNT

    @integration.register_capability(
        capability_name,
        display_name="Invite User via Email",
        description="Send an email to invite a user to your organization",
    )
    async def capability(
        args: CreateAccountRequest,
    ) -> CreateAccountResponse:
        return CreateAccountResponse(
            response=CreatedAccount(
                status=AccountStatus.ACTIVE,
                created=True,
            ),
            raw_data=None,
        )

    return capability_name.value, integration.capabilities


def case_register_custom_capability_success() -> Case:
    integration = new_integration()
    capability_name = "accio"

    @integration.register_custom_capability(
        capability_name,
        description="A summoning charm.",
    )
    async def custom_capability(
        args: CustomRequest[AccioRequest],
    ) -> CustomResponse[AccioResponse]:
        return CustomResponse[AccioResponse](
            response=AccioResponse(success=True),
        )

    return capability_name, integration.capabilities


def case_register_custom_capability_reserved_name() -> Case:
    """Don't name your custom capability that! It's ours!"""
    integration = new_integration()
    capability_name = "list_accounts"

    with pytest.raises(ReservedCapabilityNameError):

        @integration.register_custom_capability(
            capability_name,
            description="A summoning charm.",
        )
        async def custom_capability(
            args: CustomRequest[AccioRequest],
        ) -> CustomResponse[AccioResponse]:
            return CustomResponse[AccioResponse](
                response=AccioResponse(success=True),
            )

    return capability_name, integration.capabilities


def case_register_custom_capability_numeric_name() -> Case:
    """We should raise an exception if you give us a non-alpha capability name"""
    integration = new_integration()
    capability_name = "name_with_numb3rs"

    with pytest.raises(InvalidCapabilityNameError) as e:

        @integration.register_custom_capability(
            capability_name,
            description="A summoning charm.",
        )
        async def custom_capability(
            args: CustomRequest[AccioRequest],
        ) -> CustomResponse[AccioResponse]:
            return CustomResponse[AccioResponse](
                response=AccioResponse(success=True),
            )

    assert "Capability names must only contain alphabetic characters and underscores" in str(e)

    return capability_name, integration.capabilities


def case_register_custom_capability_camel_case() -> Case:
    """We should raise an error for a custom capability name that isn't snake_cased"""
    integration = new_integration()
    capability_name = "CamelCaseName"

    with pytest.raises(InvalidCapabilityNameError) as e:

        @integration.register_custom_capability(
            capability_name,
            description="A summoning charm.",
        )
        async def custom_capability(
            args: CustomRequest[AccioRequest],
        ) -> CustomResponse[AccioResponse]:
            return CustomResponse[AccioResponse](
                response=AccioResponse(success=True),
            )

    assert "Capability names must use snake casing" in str(e)

    return capability_name, integration.capabilities
