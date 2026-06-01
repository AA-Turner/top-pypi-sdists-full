"""Auth service delegate for signup and login.

Proxies requests to the auth service's API endpoints.
This file is scaffolded once and never overwritten.
"""

from fastapi import HTTPException
from httpx import Response

from csrd.delegate import BaseDelegate

from ..models.auth_passthrough import TokenResponse, UserResponse


def _forward_error(response: Response) -> Response:
    """Re-raise upstream error responses with their original detail."""
    try:
        body = response.json()
        detail = body.get("detail", body) if isinstance(body, dict) else body
    except Exception:
        detail = response.text or f"Auth service returned {response.status_code}"
    raise HTTPException(status_code=response.status_code, detail=detail)


class AuthDelegate(BaseDelegate):
    """Delegate for the cluster auth service."""

    _error_handlers = {
        status: _forward_error for status in (400, 401, 403, 404, 409, 422)
    }

    def __init__(self, base_url: str) -> None:
        super().__init__(base_url)

    async def signup(self, username: str, password: str) -> UserResponse:
        """Create a new user account via the auth service."""
        return await self.post(
            "/api/signup",
            json={"username": username, "password": password},
            response_model=UserResponse,
            response_handlers=self._error_handlers,
        )

    async def login(self, username: str, password: str) -> TokenResponse:
        """Authenticate and obtain a JWT token via the auth service."""
        return await self.post(
            "/api/token",
            json={"username": username, "password": password},
            response_model=TokenResponse,
            response_handlers=self._error_handlers,
        )


__all__ = ("AuthDelegate",)
