"""GitHub OAuth authentication endpoints."""

import os
import secrets
from typing import Optional
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

router = APIRouter(prefix="/auth/github", tags=["auth"])

# GitHub OAuth settings
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "https://emdash-dev.fly.dev/api/auth/github/callback")

# In-memory session store (use Redis in production)
_sessions: dict[str, dict] = {}


class UserInfo(BaseModel):
    """User information from GitHub."""
    id: int
    login: str
    name: Optional[str]
    email: Optional[str]
    avatar_url: str


class AuthStatus(BaseModel):
    """Authentication status."""
    authenticated: bool
    user: Optional[UserInfo] = None


@router.get("/login")
async def github_login():
    """Redirect to GitHub OAuth authorization."""
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")

    state = secrets.token_urlsafe(32)

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "repo read:user user:email",  # repo for clone/push/pull
        "state": state,
    }

    url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"

    response = RedirectResponse(url=url)
    response.set_cookie("oauth_state", state, httponly=True, samesite="lax", max_age=600)
    return response


@router.get("/callback")
async def github_callback(code: str, state: str, request: Request):
    """Handle GitHub OAuth callback."""
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")

    # Verify state
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="No access token in response")

        # Get user info
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")

        user_data = user_response.json()

        # Get user email if not public
        email = user_data.get("email")
        if not email:
            email_response = await client.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((e for e in emails if e.get("primary")), None)
                if primary_email:
                    email = primary_email.get("email")

    # Create session
    session_id = secrets.token_urlsafe(32)
    _sessions[session_id] = {
        "user": {
            "id": user_data["id"],
            "login": user_data["login"],
            "name": user_data.get("name"),
            "email": email,
            "avatar_url": user_data["avatar_url"],
        },
        "access_token": access_token,
    }

    # Redirect to frontend with session cookie
    response = RedirectResponse(url="/")
    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 1 week
    )
    response.delete_cookie("oauth_state")
    return response


@router.get("/me", response_model=AuthStatus)
async def get_current_user(request: Request):
    """Get current authenticated user."""
    session_id = request.cookies.get("session_id")

    if not session_id or session_id not in _sessions:
        return AuthStatus(authenticated=False)

    session = _sessions[session_id]
    return AuthStatus(
        authenticated=True,
        user=UserInfo(**session["user"]),
    )


def get_github_token_from_session(request: Request) -> Optional[str]:
    """Extract the GitHub access token from the session cookie.

    Returns the token if the user is authenticated via GitHub OAuth,
    otherwise None.
    """
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in _sessions:
        return None
    return _sessions[session_id].get("access_token")


@router.post("/logout")
async def logout(request: Request, response: Response):
    """Log out the current user."""
    session_id = request.cookies.get("session_id")

    if session_id and session_id in _sessions:
        del _sessions[session_id]

    response.delete_cookie("session_id")
    return {"success": True}
