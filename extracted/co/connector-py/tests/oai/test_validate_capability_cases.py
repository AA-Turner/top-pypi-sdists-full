"""Test cases for ``validate_capability`` function."""

import typing as t

import pytest_cases
from connector.generated import (
    AssignedEntitlement,
    AssignEntitlement,
    AssignEntitlementResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    ListResourcesRequest,
    StandardCapabilityName,
    UpdateableAccount,
    UpdateAccountResponse,
)
from connector.oai.capability import (
    CapabilityCallableProto,
    CustomRequest,
)
from pydantic import BaseModel

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    CapabilityCallableProto[t.Any],
]


class CustomListAccountsRequestFromBadBase(ListResourcesRequest):
    """Incorrect base is used for custom request schema."""

    extra: str


class CustomListAccountsResponse(ListAccountsResponse):
    """Subclassing response type is always bad."""

    extra_resp: str


@pytest_cases.case(tags=("valid",))
def case_valid_capability_base_annotation() -> Case:
    def capability(request: ListAccountsRequest) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_custom_response() -> Case:
    """Using subclass of SDK defined response is not correct.

    This would change the output of the method, making it super hard to
    use.
    """

    def capability(request: ListAccountsRequest) -> CustomListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_model() -> Case:
    """Using mismatching request type for capability is invalid.

    Using ListResourcesRequest for list-accounts method is obviously
    invalid.
    """

    def capability(request: ListResourcesRequest) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_base_model() -> Case:
    """Using mismatching base for request type is invalid.

    Using subslass of ListResourcesRequest for list-accounts method is
    obviously invalid.
    """

    def capability(
        request: CustomListAccountsRequestFromBadBase,
    ) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_base() -> Case:
    """Using class unrelated to request type is invalid.

    Using classes unrelated to ``RequestData`` is obviously invalid.
    """

    def capability(request: int) -> ListAccountsResponse:  # type: ignore[type-var]
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_overridden_input_unallowed_for_assign_entitlement() -> CapabilityCallableProto[t.Any]:
    """
    You can't override assign_entitlement's inputs
    """

    class AppSpecificAssignEntitlement(AssignEntitlement):
        size: int

    def assign_entitlement(args: CustomRequest[AppSpecificAssignEntitlement]):
        return AssignEntitlementResponse(
            response=AssignedEntitlement(assigned=True),
            raw_data=None,
        )

    return StandardCapabilityName.ASSIGN_ENTITLEMENT, assign_entitlement  # type: ignore


@pytest_cases.case(tags=("valid",))
def case_overridden_input_allowed_for_update_account() -> Case:
    """
    You're allowed to override update_account's inputs
    """

    class AppSpecificUpdateAccount(UpdateableAccount):
        star_sign: str

    def update_account_for_specific_app(
        args: CustomRequest[AppSpecificUpdateAccount],
    ) -> UpdateAccountResponse:
        return UpdateAccountResponse(
            response=AppSpecificUpdateAccount(id="response_id", star_sign="taurus"),
        )

    return StandardCapabilityName.UPDATE_ACCOUNT, update_account_for_specific_app


@pytest_cases.case(tags=("invalid",))
def case_overridden_input_changes_origin_property_type() -> Case:
    """
    You can't change the type of an existing property, when customizing an input.

    E.g. no `email: int`
    """

    class AppSpecificUpdateAccount(UpdateableAccount):
        # we're changing the type in a way that breaks
        # the relation to the parent class. but this
        # isn't a runtime python failure, just a type
        # checking failure
        id: int  # type: ignore

    def update_account_for_specific_app(
        args: CustomRequest[AppSpecificUpdateAccount],
    ) -> UpdateAccountResponse:
        return UpdateAccountResponse(
            response=UpdateableAccount(id="response_id"),
        )

    return StandardCapabilityName.UPDATE_ACCOUNT, update_account_for_specific_app


@pytest_cases.case(tags=("invalid",))
def case_overridden_input_makes_required_field_optional() -> Case:
    """
    You can't make a previously required input property optional

    E.g. no `id: str | None` when it was `id: str`
    """

    class AppSpecificUpdateAccount(UpdateableAccount):
        id: str | None  # type: ignore

    def update_account_for_specific_app(
        args: CustomRequest[AppSpecificUpdateAccount],
    ) -> UpdateAccountResponse:
        return UpdateAccountResponse(
            response=UpdateableAccount(id="response_id"),
        )

    return StandardCapabilityName.UPDATE_ACCOUNT, update_account_for_specific_app


@pytest_cases.case(tags=("invalid",))
def case_overridden_input_drops_a_field() -> Case:
    """
    You can't remove a previous input property
    """

    class AppSpecificUpdateAccount(BaseModel):
        foo: str

    def update_account_for_specific_app(
        args: CustomRequest[AppSpecificUpdateAccount],
    ) -> UpdateAccountResponse:
        return UpdateAccountResponse(
            response=UpdateableAccount(id="response_id"),
        )

    return StandardCapabilityName.UPDATE_ACCOUNT, update_account_for_specific_app
