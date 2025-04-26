"""Test cases for ``get_capability_annotations`` function."""

import typing as t

import pytest_cases
from connector.generated import (
    AssignedEntitlement,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    UpdateableAccount,
    UpdateAccountResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.oai.capability import (
    CapabilityCallableProto,
    CustomRequest,
    Request,
    Response,
)

Case: t.TypeAlias = tuple[
    CapabilityCallableProto[t.Any],
    tuple[type[Request], type[Response]],
]


@pytest_cases.case(tags=("correct",))
def case_correct_capability() -> Case:
    def capability(
        args: ValidateCredentialsRequest,
    ) -> ValidateCredentialsResponse:
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    expected_annotations = (
        ValidateCredentialsRequest,
        ValidateCredentialsResponse,
    )
    return capability, expected_annotations


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_argument_annotation() -> CapabilityCallableProto[t.Any]:
    def capability(args) -> ValidateCredentialsResponse:
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_return_annotation() -> CapabilityCallableProto[t.Any]:
    def capability(args: ValidateCredentialsRequest):
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_annotations() -> CapabilityCallableProto[t.Any]:
    def capability(args):
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("wrong_annotation",))
def case_overridden_input_unallowed_for_assign_entitlement() -> CapabilityCallableProto[t.Any]:
    """
    You can't override assign_entitlement's inputs
    """

    def assign_entitlement(args: CustomRequest[AssignEntitlementRequest]):
        return AssignEntitlementResponse(
            response=AssignedEntitlement(assigned=True),
            raw_data=None,
        )

    return assign_entitlement  # type: ignore[return-value]


@pytest_cases.case(tags=("correct",))
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

    expected_annotations = (
        CustomRequest[AppSpecificUpdateAccount],
        UpdateAccountResponse,
    )
    return update_account_for_specific_app, expected_annotations
