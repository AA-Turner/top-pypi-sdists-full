from connector.generated import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    CreateAccountResponse,
    CreatedAccount,
    CreatedEffect,
    AccountStatus,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DowngradeLicenseRequest,
    DowngradeLicenseResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    Error,
    ErrorCode,
    ExecutionSummary,
    NoopEffect,
    NoopEffectReason,
    ReleaseResourcesRequest,
    ReleaseResourcesResponse,
    TransferDataRequest,
    TransferDataResponse,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
)
from connector.integration import CustomRequest

from {name}.client import {pascal}Client
from {name}.dto.user import CreateAccount


async def assign_entitlement(args: AssignEntitlementRequest) -> AssignEntitlementResponse:
    raise NotImplementedError  # pragma: no cover


async def unassign_entitlement(
    args: UnassignEntitlementRequest,
) -> UnassignEntitlementResponse:
    raise NotImplementedError  # pragma: no cover


async def create_account(
    args: CustomRequest[CreateAccount],
) -> CreateAccountResponse:
    # TODO: Implement account creation logic
    async with {pascal}Client(args) as client:
        caught_errors = []
        try:
            # Try to create account first
            new_user = await client.create_user(args.request)

            # Assign required entitlements (failures are non-fatal)
            for entitlement in args.request.entitlements:
                try:
                    await client.assign_entitlement(new_user.id, entitlement)
                except Exception as e:
                    caught_errors.append(Error(
                        message=f"Failed to assign entitlement {{entitlement.integration_specific_id}}: {{str(e)}}",
                        error_code=ErrorCode.API_ERROR,
                        app_id="{name}",
                    ))

            return CreateAccountResponse(
                response=CreatedAccount(
                    id=new_user.id,
                    status=AccountStatus.ACTIVE,
                    created=True,
                ),
                execution_summary=ExecutionSummary(
                    effect=CreatedEffect(),
                    request_fingerprint=args.request.fingerprint(),
                    is_idempotent=True,
                    description="Successfully created new user account",
                    caught_errors=caught_errors if caught_errors else None,
                ),
            )

        except Exception as e:
            # Handle "already exists" error - fetch and return existing account
            if "already exists" in str(e).lower():
                existing_user = await client.find_user_by_email(args.request.email)

                return CreateAccountResponse(
                    response=CreatedAccount(
                        id=existing_user.id,
                        status=AccountStatus.ACTIVE,
                        created=True,
                    ),
                    execution_summary=ExecutionSummary(
                        effect=NoopEffect(reason=NoopEffectReason.STATE_ALREADY_MATCHES),
                        request_fingerprint=args.request.fingerprint(),
                        is_idempotent=True,
                        description=f"Account already exists for {{args.request.email}}",
                    ),
                )

            raise


async def delete_account(
    args: DeleteAccountRequest,
) -> DeleteAccountResponse:
    raise NotImplementedError  # pragma: no cover


async def activate_account(
    args: ActivateAccountRequest,
) -> ActivateAccountResponse:
    raise NotImplementedError  # pragma: no cover


async def deactivate_account(
    args: DeactivateAccountRequest,
) -> DeactivateAccountResponse:
    raise NotImplementedError  # pragma: no cover

async def transfer_data(
    args: TransferDataRequest,
) -> TransferDataResponse:
    raise NotImplementedError  # pragma: no cover

async def downgrade_license(
    args: DowngradeLicenseRequest,
) -> DowngradeLicenseResponse:
    raise NotImplementedError  # pragma: no cover

async def release_resources(
    args: ReleaseResourcesRequest,
) -> ReleaseResourcesResponse:
    raise NotImplementedError  # pragma: no cover
