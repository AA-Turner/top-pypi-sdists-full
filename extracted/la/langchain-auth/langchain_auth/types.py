"""Types for LangChain Auth SDK."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AuthStatus(str, Enum):
    """Valid authentication status values."""

    COMPLETED = "completed"
    PENDING = "pending"


class AuthWaitStatus(str, Enum):
    """Valid auth wait status values."""

    COMPLETED = "completed"
    PENDING = "pending"
    TIMEOUT = "timeout"
    NOT_FOUND = "not_found"


@dataclass
class OAuthProvider:
    """OAuth provider configuration."""

    id: str
    organization_id: str
    provider_id: str
    name: str
    client_id: str
    auth_url: str
    token_url: str
    uses_pkce: bool
    code_challenge_method: Optional[str]
    provider_type: Optional[str]
    created_at: str
    updated_at: str

    def __str__(self):
        return f"OAuthProvider(provider_id='{self.provider_id}', name='{self.name}')"

    def __repr__(self):
        return self.__str__()


@dataclass
class AuthResult:
    """Result from authentication attempt."""

    status: str
    token: Optional[str] = None
    url: Optional[str] = None
    auth_id: Optional[str] = None

    def __str__(self):
        if self.token:
            return f"AuthResult(status='{self.status}', token='***')"
        elif self.url:
            return f"AuthResult(status='{self.status}', url='{self.url}')"
        else:
            return f"AuthResult(status='{self.status}')"

    def __repr__(self):
        return self.__str__()


@dataclass
class OAuthTokenStatusResponse:
    has_token: bool


@dataclass
class DeleteProviderResponse:
    message: str


@dataclass
class RevokeTokensResponse:
    message: str
    provider_id: str
