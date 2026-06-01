"""Public user endpoints: signup.

This file is scaffolded once and never overwritten.
"""

from fastapi import APIRouter

from ..dependencies.db import UserRepo
from ..models.users import SignupRequest, UserResponse

router = APIRouter(tags=["users"])


@router.post("/api/signup", status_code=201, response_model=UserResponse)
async def signup(body: SignupRequest, repo: UserRepo) -> UserResponse:
    """Create a new user account.

    The first user registered is automatically granted the ADMIN role.
    """
    return await repo.create_user(body.username, body.password)
