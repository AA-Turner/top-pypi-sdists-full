"""Token issuance and verification endpoints.

This file is scaffolded once and never overwritten.
"""

from fastapi import APIRouter

from ..dependencies.db import UserRepo
from ..dependencies.token_service import TokenSvc
from ..models.auth import (
    TokenRequest,
    TokenResponse,
    VerifyRequest,
    VerifyResponse,
)

router = APIRouter(tags=["auth"])



@router.post("/api/token", response_model=TokenResponse)
async def issue_token(
    body: TokenRequest,
    repo: UserRepo,
    token_svc: TokenSvc,
) -> TokenResponse:
    """Validate credentials and issue a JWT access token."""
    user = await repo.verify_credentials(body.username, body.password)
    roles_resp = await repo.get_user_roles(user.id)
    return await token_svc.issue_token(
        user_id=user.id,
        username=user.username,
        roles=roles_resp.roles,
    )


@router.post("/api/verify", response_model=VerifyResponse)
async def verify_token(body: VerifyRequest, token_svc: TokenSvc) -> VerifyResponse:
    """Verify a JWT and return its claims."""
    return await token_svc.verify_token(body.token)
