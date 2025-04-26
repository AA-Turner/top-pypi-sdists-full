from connector.generated import (
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    ActivateAccountRequest,
    ActivateAccountResponse,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
)
from connector.oai.capability import CustomRequest
from {name}.dto.user import CreateAccount


async def assign_entitlement(args: AssignEntitlementRequest) -> AssignEntitlementResponse:
    raise NotImplementedError


async def unassign_entitlement(
    args: UnassignEntitlementRequest,
) -> UnassignEntitlementResponse:
    raise NotImplementedError


async def create_account(
    args: CustomRequest[CreateAccount],
) -> CreateAccountResponse:
    raise NotImplementedError


async def delete_account(
    args: DeleteAccountRequest,
) -> DeleteAccountResponse:
    raise NotImplementedError


async def activate_account(
    args: ActivateAccountRequest,
) -> ActivateAccountResponse:
    raise NotImplementedError


async def deactivate_account(
    args: DeactivateAccountRequest,
) -> DeactivateAccountResponse:
    raise NotImplementedError
