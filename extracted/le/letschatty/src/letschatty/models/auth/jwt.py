from pydantic import BaseModel, Field
from typing import Protocol
from enum import StrEnum
import time


def get_expiration_timestamp(hours: int = 24) -> int:
    """
    Generate an expiration timestamp for the token.
    Args:
        hours: Number of hours until the token expires (default: 24)
    Returns:
        int: Unix timestamp in seconds
    """
    return int(time.time() + (hours * 3600))

class TokenPayload(BaseModel):
    company_id: str
    user_id: str
    exp: int = Field(default_factory=get_expiration_timestamp)
    is_mega_admin: bool = Field(default=False)

class AuthType(StrEnum):
    JWT = "jwt"
    API_KEY = "api_key"
    AUTH0 = "auth0"
    LOCAL_TEST = "local_test"

class AuthenticatedG(Protocol):
    token_payload: TokenPayload
    auth_type: AuthType
    request_company_id: str