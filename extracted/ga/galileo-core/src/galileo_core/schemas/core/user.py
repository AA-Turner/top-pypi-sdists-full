from typing import List, Literal, Union

from pydantic import UUID4, BaseModel, Field, field_validator

from galileo_core.schemas.core.auth_method import AuthMethod
from galileo_core.schemas.core.user_role import SystemRole, UserRole

PASS_MIN_LENGTH = 8
INVALID_PASS_MSG = (
    f"Password must be {PASS_MIN_LENGTH} characters or "
    "more and have a mix of uppercase, lowercase, "
    "numbers, and special characters"
)


def valid_pass(password: str) -> bool:
    valid_length = len(password) >= PASS_MIN_LENGTH
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    special = not password.isalnum()
    return valid_length and upper and lower and special


class InviteUsersRequest(BaseModel):
    auth_method: AuthMethod = AuthMethod.email
    emails: List[str] = Field(default_factory=list)
    role: UserRole = UserRole.user
    group_ids: List[UUID4] = []


class User(BaseModel):
    id: UUID4
    email: str
    role: UserRole = UserRole.user


class CreateUserRequest(BaseModel):
    email: str
    auth_method: Literal[AuthMethod.email] = AuthMethod.email
    password: str
    role: UserRole = UserRole.read_only

    @field_validator("password")
    def validate_password(cls, v: str) -> Union[str, None]:
        if not valid_pass(v):
            raise ValueError(INVALID_PASS_MSG)
        return v


class CreateUserResponse(BaseModel):
    id: UUID4
    email: str
    role: Union[UserRole, SystemRole] = UserRole.user


class UpdateUserRoleRequest(BaseModel):
    role: UserRole
