"""OAuth authentication API endpoints (GitHub and Google)."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

# Thread pool for blocking operations
_executor = ThreadPoolExecutor(max_workers=2)


class LoginResponse(BaseModel):
    """Response from login initiation."""
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int


class AuthStatus(BaseModel):
    """Current authentication status."""
    authenticated: bool
    username: Optional[str] = None
    scope: Optional[str] = None


class LoginPollResponse(BaseModel):
    """Response from login polling."""
    status: str  # "pending", "success", "expired", "error"
    username: Optional[str] = None
    error: Optional[str] = None


# Store active device flow states
_device_flows: dict[str, dict] = {}


@router.post("/login", response_model=LoginResponse)
async def start_login():
    """Start GitHub OAuth device flow.

    Returns a user code that the user must enter at github.com/login/device.
    The client should then poll /auth/login/poll until authentication completes.

    Example:
        curl -X POST http://localhost:8765/api/auth/login
    """
    from ..auth.github import GitHubAuth

    loop = asyncio.get_event_loop()

    def _request_device_code():
        auth = GitHubAuth()
        return auth.request_device_code()

    try:
        response = await loop.run_in_executor(_executor, _request_device_code)

        # Store device code for polling
        _device_flows[response.user_code] = {
            "device_code": response.device_code,
            "interval": response.interval,
            "expires_in": response.expires_in,
        }

        return LoginResponse(
            user_code=response.user_code,
            verification_uri=response.verification_uri,
            expires_in=response.expires_in,
            interval=response.interval,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login/poll/{user_code}", response_model=LoginPollResponse)
async def poll_login(user_code: str):
    """Poll for login completion.

    After starting login, the client should poll this endpoint
    every `interval` seconds until status is "success" or "expired".

    Args:
        user_code: The user code returned from /auth/login

    Example:
        curl -X POST http://localhost:8765/api/auth/login/poll/ABCD-1234
    """
    from ..auth.github import GitHubAuth

    if user_code not in _device_flows:
        raise HTTPException(status_code=404, detail="Device flow not found")

    flow = _device_flows[user_code]
    device_code = flow["device_code"]

    loop = asyncio.get_event_loop()

    def _poll_for_token():
        auth = GitHubAuth()
        return auth.poll_for_token(device_code)

    try:
        result = await loop.run_in_executor(_executor, _poll_for_token)

        if result is None:
            # Still pending
            return LoginPollResponse(status="pending")

        if isinstance(result, str):
            # Error message
            if "expired" in result.lower():
                del _device_flows[user_code]
                return LoginPollResponse(status="expired", error=result)
            return LoginPollResponse(status="error", error=result)

        # Success - result is AuthConfig
        del _device_flows[user_code]
        return LoginPollResponse(
            status="success",
            username=result.username,
        )

    except Exception as e:
        return LoginPollResponse(status="error", error=str(e))


@router.post("/logout")
async def logout():
    """Sign out by removing stored credentials.

    Example:
        curl -X POST http://localhost:8765/api/auth/logout
    """
    from ..auth.github import GitHubAuth

    loop = asyncio.get_event_loop()

    def _clear_auth():
        auth = GitHubAuth()
        auth.clear_auth()

    await loop.run_in_executor(_executor, _clear_auth)
    return {"success": True, "message": "Logged out successfully"}


@router.get("/status", response_model=AuthStatus)
async def get_status():
    """Get current GitHub authentication status.

    Example:
        curl http://localhost:8765/api/auth/status
    """
    from ..auth.github import get_auth_status

    loop = asyncio.get_event_loop()

    def _get_status():
        return get_auth_status()

    try:
        status = await loop.run_in_executor(_executor, _get_status)
        return AuthStatus(
            authenticated=status.get("authenticated", False),
            username=status.get("username"),
            scope=status.get("scope"),
        )
    except Exception:
        return AuthStatus(authenticated=False)


# =============================================================================
# Google OAuth Endpoints
# =============================================================================


class GoogleLoginResponse(BaseModel):
    """Response from Google login."""
    success: bool
    auth_url: Optional[str] = None
    message: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    error: Optional[str] = None


class GoogleAuthStatus(BaseModel):
    """Google authentication status."""
    authenticated: bool
    source: Optional[str] = None
    email: Optional[str] = None
    scopes: list[str] = []


@router.post("/google/login", response_model=GoogleLoginResponse)
async def google_login(open_browser: bool = True):
    """Start Google OAuth login flow.

    This opens a browser window for Google OAuth authentication.
    The user authorizes Emdash, and tokens are stored locally.

    Args:
        open_browser: Whether to automatically open the browser (default True)

    Example:
        curl -X POST http://localhost:8765/api/auth/google/login
    """
    from ..auth.google import GoogleAuth

    loop = asyncio.get_event_loop()

    def _google_login():
        auth = GoogleAuth()
        return auth.login(open_browser=open_browser)

    try:
        result = await loop.run_in_executor(_executor, _google_login)
        return GoogleLoginResponse(
            success=result.get("success", False),
            auth_url=result.get("auth_url"),
            message=result.get("message"),
            email=result.get("email"),
            name=result.get("name"),
            error=result.get("error"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/google/logout")
async def google_logout():
    """Sign out from Google by removing stored credentials.

    Example:
        curl -X POST http://localhost:8765/api/auth/google/logout
    """
    from ..auth.google import GoogleAuth

    loop = asyncio.get_event_loop()

    def _google_logout():
        auth = GoogleAuth()
        return auth.logout()

    result = await loop.run_in_executor(_executor, _google_logout)
    return result


@router.get("/google/status", response_model=GoogleAuthStatus)
async def google_status():
    """Get current Google authentication status.

    Example:
        curl http://localhost:8765/api/auth/google/status
    """
    from ..auth.google import get_google_auth_status

    loop = asyncio.get_event_loop()

    def _get_status():
        return get_google_auth_status()

    try:
        status = await loop.run_in_executor(_executor, _get_status)
        return GoogleAuthStatus(
            authenticated=status.get("authenticated", False),
            source=status.get("source"),
            email=status.get("email"),
            scopes=status.get("scopes", []),
        )
    except Exception:
        return GoogleAuthStatus(authenticated=False)
