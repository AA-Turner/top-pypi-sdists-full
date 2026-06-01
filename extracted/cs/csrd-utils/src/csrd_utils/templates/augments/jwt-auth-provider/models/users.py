"""User management models."""

from csrd.models import BaseModel


class SignupRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    """Basic user info returned after signup or lookup."""

    id: str
    username: str


class UserRolesResponse(BaseModel):
    """User with their assigned roles/authorities."""

    user_id: str
    roles: list[str]


class RoleRequest(BaseModel):
    role: str
