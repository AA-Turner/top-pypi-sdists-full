"""FastAPI dependency injection helpers for matrx-connect."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import Header, HTTPException, Request, status

from matrx_connect.context.app_context import (
    AppContext,
    TenantAppContext,
    clear_app_context,
    require_tenant_context,
    set_app_context,
)
from matrx_connect.org_hold import ORGANIZATION_MISMATCH, OrganizationRequired


async def context_dep(request: Request) -> AppContext:
    """FastAPI dependency — extracts AppContext set by AuthMiddleware.

    Usage::

        @router.post("/example")
        async def example(ctx: AppContext = Depends(context_dep)):
            ...
    """
    ctx: AppContext | None = getattr(request.state, "context", None)
    if ctx is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AuthMiddleware did not set request context.",
        )
    return ctx


async def require_organization_context(
    request: Request,
    x_organization_id: Annotated[str, Header(alias="X-Organization-Id")],
) -> AsyncGenerator[TenantAppContext]:
    """Admit only a request whose required header matches its resolved context.

    The middleware remains responsible for authentication and organization
    authorization. This dependency is the route-level fail-closed backstop: it
    rejects malformed, unresolved, or disagreeing context before feature code
    runs. Admin callers use the same target-organization contract and retain
    their existing ``is_admin`` / ``admin_level`` identity on the returned
    context.
    """
    # Do not depend on context_dep here. FastAPI caches dependency results, so
    # that subdependency would leave a later handler Depends(context_dep) with
    # the pre-admission AppContext instead of the admitted object.
    ctx: AppContext | None = getattr(request.state, "context", None)
    if ctx is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AuthMiddleware did not set request context.",
        )
    try:
        claimed_organization_id = str(UUID(x_organization_id.strip()))
    except (AttributeError, ValueError):
        # NOT a hold: the caller DID name something, it just is not an
        # organization id. A picker does not answer a malformed value.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "organization_context_invalid",
                "message": "X-Organization-Id must be a valid organization UUID",
            },
        ) from None

    if ctx.organization_admission != "verified" or not ctx.organization_id:
        # THE ONE HOLD. This route needs an organization and this request
        # carries none the middleware would admit — so the person CHOOSES one
        # from their memberships. It never falls back to a default or a
        # personal organization; that substitution is exactly what the
        # 2026-09-19 ruling outlaws.
        raise OrganizationRequired(
            what=(
                "This request's organization was not admitted by authentication. "
                "Name an organization you are a member of in X-Organization-Id."
            ),
            set_on="request",
            user_id=str(getattr(ctx, "user_id", "") or "").strip() or None,
            extra={"organization_admission": ctx.organization_admission},
        )

    try:
        resolved_organization_id = str(UUID(str(ctx.organization_id).strip()))
    except (AttributeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "organization_context_invalid_internal",
                "message": "Authentication middleware produced an invalid organization context",
            },
        ) from None

    if claimed_organization_id != resolved_organization_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": ORGANIZATION_MISMATCH,
                "message": "X-Organization-Id does not match the admitted organization context",
            },
        )

    try:
        admitted = require_tenant_context(ctx)
    except ValueError:
        # Same truth as above, reached one step later: no admitted tenant.
        raise OrganizationRequired(
            what=(
                "This request's organization was not admitted by authentication. "
                "Name an organization you are a member of in X-Organization-Id."
            ),
            set_on="request",
            user_id=str(getattr(ctx, "user_id", "") or "").strip() or None,
            extra={"organization_admission": ctx.organization_admission},
        ) from None

    request.state.context = admitted
    token = set_app_context(admitted)
    try:
        yield admitted
    finally:
        request.state.context = ctx
        clear_app_context(token)


#: The one refusal an account-only route gives a guest token (guests-use-everything D1).
ACCOUNT_REQUIRED = "account_required"
ACCOUNT_REQUIRED_MESSAGE = "Create a free account to use this."


async def require_authenticated(request: Request) -> None:
    """Admit only a person WITH AN ACCOUNT. Use as a router dep on account-only mounts.

    Account-only means the work makes no sense without a persistent identity
    (credential vault, paying, organization membership, HR, sending identities,
    admin). A guest token — a verified JWT with ``is_anonymous: true`` — is
    refused with ``401 account_required`` so the client can offer sign-up;
    every other route admits guests (``require_guest_or_above``).
    """
    _require_verified_identity(request)
    ctx: AppContext = request.state.context
    if getattr(ctx, "is_anonymous", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": ACCOUNT_REQUIRED, "message": ACCOUNT_REQUIRED_MESSAGE},
        )


def _require_verified_identity(request: Request) -> None:
    """Reject any request that isn't authenticated (guest tokens included as authenticated)."""
    ctx: AppContext | None = getattr(request.state, "context", None)
    if ctx is None or not ctx.is_authenticated:
        refused = (getattr(ctx, "metadata", None) or {}).get("credential_refused") if ctx else None
        if refused:
            # A key of ours that stopped working says WHY (revoked / expired), never "sign in".
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "api_key_refused", "message": refused, "user_message": refused},
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "token_required",
                "message": "Valid authentication token required",
            },
        )


async def authenticated_resource_bootstrap(request: Request) -> str | None:
    """Return the literal resource-organization claim after authentication.

    This is intentionally not a tenant admission and does not alter either
    request state or the ambient context.  A later host handler authorizes the
    named row and passes this value as its *new operation* claim.

    A fingerprint GUEST is a real anonymous ``auth.users`` identity and is
    admitted here like a signed-in person: the handler's canonical row check
    (``iam.has_access_for``) decides what that identity may read, exactly as it
    does for everyone else. Only a request with no identity at all is refused.
    """
    ctx: AppContext | None = getattr(request.state, "context", None)
    is_guest = (
        ctx is not None
        and getattr(ctx, "auth_type", None) == "fingerprint"
        and bool(str(getattr(ctx, "user_id", "") or "").strip())
    )
    if not is_guest:
        # A guest TOKEN (is_anonymous) is authenticated and admitted here too:
        # the handler's row check decides what it may read.
        _require_verified_identity(request)
    values = request.headers.getlist("x-organization-id")
    if not values:
        return None
    if len(values) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "resource_organization_claim_invalid",
                "message": "X-Organization-Id must appear at most once for a resource operation",
            },
        )
    try:
        value = values[0].strip()
        if not value:
            raise ValueError
        return str(UUID(value))
    except (AttributeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "resource_organization_claim_invalid",
                "message": "X-Organization-Id must be a valid organization UUID",
            },
        ) from None


async def require_admin(request: Request) -> None:
    """Reject anything that isn't an authenticated admin (401 or 403)."""
    ctx: AppContext | None = getattr(request.state, "context", None)
    if ctx is None or not ctx.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "token_required",
                "message": "Valid authentication token required",
            },
        )
    if not ctx.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "admin_required",
                "message": "Admin access required",
            },
        )
