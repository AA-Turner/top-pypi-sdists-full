"""
AGENTICSTAR Platform SDK - Auth Module
AgenticStar Auth API統合機能を提供

Example:
    ```python
    from agenticstar_platform.auth import AgenticStarAuthClient, AgenticStarAuthConfig

    config = AgenticStarAuthConfig(
        base_url="https://auth.example.com",
        api_key="your-api-key",
    )

    async with AgenticStarAuthClient(config) as client:
        # ユーザー一覧取得
        result = await client.get_users(page=1, limit=20)
        if result.success:
            for user in result.users:
                print(f"User: {user.email}")

        # ユーザー詳細取得
        result = await client.get_user("user-id")
        if result.success:
            print(f"User: {result.user.display_name}")

        # MCPトークン取得
        result = await client.get_mcp_tokens("user-id", ["github", "slack"])
        if result.success:
            for provider, token in result.tokens.items():
                print(f"{provider}: expires at {token.expires_at}")
    ```
"""

from .client import AgenticStarAuthClient
from .config import AgenticStarAuthConfig
from .exceptions import (
    AuthAPIError,
    AuthConfigError,
    AuthError,
    AuthNotFoundError,
    AuthRateLimitError,
    AuthUnauthorizedError,
)
from .models import (
    ApiUser,
    DeviceInfo,
    GetMCPTokensResult,
    GetUserResult,
    GetUsersResult,
    LoginHistoryEntry,
    MCPTokenError,
    MCPTokenInfo,
    OAuthProviderName,
    UserPagination,
)

__all__ = [
    # Client
    "AgenticStarAuthClient",
    # Config
    "AgenticStarAuthConfig",
    # Exceptions
    "AuthError",
    "AuthConfigError",
    "AuthAPIError",
    "AuthUnauthorizedError",
    "AuthNotFoundError",
    "AuthRateLimitError",
    # Models - User
    "ApiUser",
    "DeviceInfo",
    "LoginHistoryEntry",
    "UserPagination",
    # Models - MCP OAuth
    "MCPTokenInfo",
    "MCPTokenError",
    "OAuthProviderName",
    # Result Types
    "GetUsersResult",
    "GetUserResult",
    "GetMCPTokensResult",
]
