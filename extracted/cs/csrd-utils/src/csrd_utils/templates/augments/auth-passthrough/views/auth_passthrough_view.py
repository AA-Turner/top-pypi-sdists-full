"""Auth passthrough endpoints — unguarded signup and login.

Proxies signup and login requests to the cluster auth service.
No authentication required on these endpoints.

Paths match the auth service exactly (no rewriting) so the mental
model is 1:1: gateway path == inner service path.

This file is scaffolded once and never overwritten.
"""

from fastapi import APIRouter

from ..dependencies.auth_passthrough import AuthDelegateDep
from ..models.auth_passthrough import LoginRequest, SignupRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api", tags=["Auth"])


@router.post("/signup", status_code=201, response_model=UserResponse)
async def signup(body: SignupRequest, delegate: AuthDelegateDep) -> UserResponse:
    """Create a new user account via the auth service."""
    return await delegate.signup(body.username, body.password)


@router.post("/token", response_model=TokenResponse)
async def login(body: LoginRequest, delegate: AuthDelegateDep) -> TokenResponse:
    """Authenticate and obtain a JWT token via the auth service."""
    return await delegate.login(body.username, body.password)
