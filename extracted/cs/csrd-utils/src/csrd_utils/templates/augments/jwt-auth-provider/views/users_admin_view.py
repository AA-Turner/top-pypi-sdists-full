"""Admin-guarded user management endpoints.

All endpoints require ADMIN authority. Uses the same ``tags=["users"]``
so Swagger groups them together with the public signup endpoint.

This file is scaffolded once and never overwritten.
"""

from fastapi import APIRouter

from ..dependencies.auth import AdminGuard
from ..dependencies.db import UserRepo
from ..models.users import RoleRequest, UserResponse, UserRolesResponse

router = APIRouter(tags=["users"])


@router.get("/api/users", response_model=list[UserResponse])
async def list_users(repo: UserRepo, _admin: AdminGuard) -> list[UserResponse]:
    """List all users. Requires ADMIN authority."""
    return await repo.list_users()


@router.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, repo: UserRepo, _admin: AdminGuard) -> UserResponse:
    """Get user info by ID. Requires ADMIN authority."""
    return await repo.get_user(user_id)


@router.get("/api/users/{user_id}/roles", response_model=UserRolesResponse)
async def get_user_roles(user_id: str, repo: UserRepo, _admin: AdminGuard) -> UserRolesResponse:
    """List a user's authorities/roles. Requires ADMIN authority."""
    return await repo.get_user_roles(user_id)


@router.post("/api/users/{user_id}/roles", status_code=201, response_model=UserRolesResponse)
async def add_user_role(
    user_id: str, body: RoleRequest, repo: UserRepo, _admin: AdminGuard
) -> UserRolesResponse:
    """Assign a role/authority to a user. Requires ADMIN authority."""
    return await repo.add_role(user_id, body.role)
