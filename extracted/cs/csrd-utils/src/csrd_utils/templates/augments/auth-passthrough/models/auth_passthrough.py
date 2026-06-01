"""Auth passthrough request/response models."""

from csrd.models import BaseModel


class SignupRequest(BaseModel):
    """Signup request body."""

    username: str
    password: str


class LoginRequest(BaseModel):
    """Login request body."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response from the auth service."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response from the auth service."""

    id: str
    username: str
