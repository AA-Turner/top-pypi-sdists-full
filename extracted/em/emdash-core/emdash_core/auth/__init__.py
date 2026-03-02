"""OAuth authentication for EmDash (GitHub and Google)."""

from .github import (
    GitHubAuth,
    AuthConfig,
    get_github_token,
    is_authenticated,
    get_auth_status,
)

from .google import (
    GoogleAuth,
    get_google_access_token,
    is_google_authenticated,
    get_google_auth_status,
)

__all__ = [
    # GitHub
    "GitHubAuth",
    "AuthConfig",
    "get_github_token",
    "is_authenticated",
    "get_auth_status",
    # Google
    "GoogleAuth",
    "get_google_access_token",
    "is_google_authenticated",
    "get_google_auth_status",
]
