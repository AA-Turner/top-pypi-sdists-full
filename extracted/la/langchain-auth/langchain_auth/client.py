"""LangChain Auth SDK."""

from __future__ import annotations

import os
from typing import List, Optional

import httpx

from .types import (
    AuthResult,
    DeleteProviderResponse,
    OAuthProvider,
    OAuthTokenStatusResponse,
    RevokeTokensResponse,
)

# Optional LangGraph imports
try:
    from langgraph.types import interrupt
    from langgraph.runtime import get_runtime
    from langgraph.config import get_config
except ImportError:
    # Create dummy functions that will fail if called
    def interrupt(data):
        raise ImportError("LangGraph is not installed. Install with: pip install 'langchain-auth[langgraph]'")

    def get_runtime():
        raise ImportError("LangGraph is not installed. Install with: pip install 'langchain-auth[langgraph]'")


def in_langgraph_context() -> bool:
    """Check if we're running inside a LangGraph context."""
    try:
        _runtime = get_runtime()
        return True
    except Exception:
        return False


class Client:
    """LangChain Auth client for OAuth."""

    API_PREFIX = "/v2/auth"
    DEFAULT_API_URL = "https://api.host.langchain.com"

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        resolved_url = api_url or os.environ.get("LANGSMITH_API_URL") or self.DEFAULT_API_URL
        self.api_url = resolved_url.rstrip("/")
        self.api_key = api_key or os.environ.get("LANGSMITH_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via the 'api_key' argument or set the LANGSMITH_API_KEY environment variable."
            )

    def _get_headers(self, include_content_type: bool = False) -> dict:
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        if include_content_type:
            headers["Content-Type"] = "application/json"
        return headers

    def _map_provider_response(self, data: dict) -> OAuthProvider:
        return OAuthProvider(
            id=data["id"],
            organization_id=data["organization_id"],
            provider_id=data["provider_id"],
            name=data["name"],
            client_id=data["client_id"],
            auth_url=data["auth_url"],
            token_url=data["token_url"],
            uses_pkce=data["uses_pkce"],
            code_challenge_method=data.get("code_challenge_method"),
            provider_type=data.get("provider_type"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    async def authenticate(
        self,
        provider: str,
        scopes: List[str],
        user_id: str,
        ls_user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        extra_headers: Optional[dict] = None,
    ) -> AuthResult:
        """Authenticate with OAuth provider and return auth result.
        This method handles the full OAuth flow:
        - If in LangGraph context: throws interrupt for user to complete auth
        - If not in LangGraph context: returns AuthResult immediately with auth URL

        Args:
            provider: OAuth provider name
            scopes: List of required scopes
            user_id: User ID for user-scoped tokens (required)
            ls_user_id: LangSmith user ID (optional)
            agent_id: Specific agent ID for agent-scoped tokens (optional, auto-detected in LangGraph if not provided)
            extra_headers: Additional HTTP headers to include in the authenticate request (optional).
                Merged with the default SDK headers (x-api-key, Content-Type).
                Caller headers take precedence on key collision.

        Returns:
            AuthResult with token (if available) or auth_url (if auth needed)
        """
        in_langgraph = in_langgraph_context()

        # Determine the agent_id for the API call
        api_agent_id = agent_id
        if api_agent_id is None and in_langgraph:
            # Try to get agent_id from LangGraph config
            try:
                config = get_config()
                api_agent_id = config.get("configurable", {}).get("assistant_id")
            except Exception:
                pass

        # Build request matching AuthAuthenticateRequest schema
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {
                "user_id": user_id,
                "provider": provider,
                "scopes": scopes,
            }

            if ls_user_id is not None:
                payload["ls_user_id"] = ls_user_id

            if api_agent_id is not None:
                payload["agent_id"] = api_agent_id

            request_headers = self._get_headers(include_content_type=True)
            if extra_headers:
                request_headers.update(extra_headers)

            response = await client.post(
                f"{self.api_url}{self.API_PREFIX}/authenticate",
                json=payload,
                headers=request_headers,
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        # If token exists, return it
        if data.get("status") == "completed":
            return AuthResult(
                status=data["status"],
                token=data.get("token"),
            )

        # No token found - need OAuth
        auth_url = data.get("url")
        auth_id = data.get("auth_id")

        if in_langgraph:
            interrupt(
                {
                    "message": f"OAuth authentication required for provider '{provider}'.",
                    "auth_url": auth_url,
                    "provider": provider,
                    "scopes": scopes,
                }
            )

            # Only reached on resume - but if we get here, OAuth wasn't completed
            raise ValueError(
                f"OAuth authentication not completed. Please visit {auth_url} and complete authentication before resuming."
            )

        return AuthResult(
            status=data["status"],
            url=auth_url,
            auth_id=auth_id,
        )

    async def wait_for_completion(self, auth_id: str, timeout: int = 300) -> AuthResult:
        """Wait for OAuth authentication to be completed.

        Polls the server until the user completes OAuth flow or timeout is reached.
        Useful after authenticate() returns an auth_url.

        Args:
            auth_id: Auth ID returned from authenticate()
            timeout: Max time to wait for completion in seconds

        Returns:
            AuthResult with token if completed

        Raises:
            TimeoutError: If authentication not completed within timeout
            Exception: If authentication failed
        """
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout + 10) as client:
            response = await client.get(
                f"{self.api_url}{self.API_PREFIX}/wait/{auth_id}?timeout={timeout}", headers=self._get_headers()
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        status = data.get("status")
        if status == "completed":
            return AuthResult(status=status, token=data.get("token"))
        elif status == "timeout":
            raise TimeoutError(f"OAuth authentication timed out after {timeout} seconds")
        elif status == "not_found":
            raise Exception("OAuth authentication request not found or has expired")
        else:
            raise Exception(f"OAuth authentication failed with status: {status}")

    async def create_oauth_provider(
        self,
        provider_id: str,
        name: str,
        client_id: str,
        client_secret: str,
        auth_url: str,
        token_url: str,
        uses_pkce: Optional[bool] = None,
        code_challenge_method: Optional[str] = None,
    ) -> OAuthProvider:
        """Create a new OAuth provider configuration.

        Args:
            provider_id: Unique identifier for the provider (e.g., 'github', 'google')
            name: Human-readable name for the provider
            client_id: OAuth client ID from the provider
            client_secret: OAuth client secret from the provider
            auth_url: Authorization URL for the OAuth flow
            token_url: Token exchange URL for the OAuth flow

        Returns:
            OAuthProvider instance with the created configuration
        """
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {
                "provider_id": provider_id,
                "name": name,
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_url": auth_url,
                "token_url": token_url,
            }

            if uses_pkce is not None:
                payload["uses_pkce"] = uses_pkce

            if code_challenge_method is not None:
                payload["code_challenge_method"] = code_challenge_method

            response = await client.post(
                f"{self.api_url}{self.API_PREFIX}/providers",
                json=payload,
                headers=self._get_headers(include_content_type=True),
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return self._map_provider_response(data)

    async def get_oauth_provider(self, provider_id: str) -> OAuthProvider:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                f"{self.api_url}{self.API_PREFIX}/providers/{provider_id}", headers=self._get_headers()
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return self._map_provider_response(data)

    async def update_oauth_provider(
        self,
        provider_id: str,
        name: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        auth_url: Optional[str] = None,
        token_url: Optional[str] = None,
        uses_pkce: Optional[bool] = None,
        code_challenge_method: Optional[str] = None,
    ) -> OAuthProvider:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {}

            if name is not None:
                payload["name"] = name
            if client_id is not None:
                payload["client_id"] = client_id
            if client_secret is not None:
                payload["client_secret"] = client_secret
            if auth_url is not None:
                payload["auth_url"] = auth_url
            if token_url is not None:
                payload["token_url"] = token_url
            if uses_pkce is not None:
                payload["uses_pkce"] = uses_pkce
            if code_challenge_method is not None:
                payload["code_challenge_method"] = code_challenge_method

            response = await client.patch(
                f"{self.api_url}{self.API_PREFIX}/providers/{provider_id}",
                json=payload,
                headers=self._get_headers(include_content_type=True),
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return self._map_provider_response(data)

    async def delete_oauth_provider(self, provider_id: str) -> DeleteProviderResponse:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(
                f"{self.api_url}{self.API_PREFIX}/providers/{provider_id}", headers=self._get_headers()
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return DeleteProviderResponse(message=data["message"])

    async def list_oauth_providers(self) -> List[OAuthProvider]:
        """List all OAuth provider configurations.

        Returns:
            List of OAuthProvider instances
        """
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"{self.api_url}{self.API_PREFIX}/providers", headers=self._get_headers())

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return [self._map_provider_response(provider) for provider in data]

    async def check_token_exists(self, provider_id: str) -> OAuthTokenStatusResponse:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                f"{self.api_url}{self.API_PREFIX}/tokens/exists?provider_id={provider_id}", headers=self._get_headers()
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return OAuthTokenStatusResponse(has_token=data["has_token"])

    async def revoke_tokens(self, provider_id: str) -> RevokeTokensResponse:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(
                f"{self.api_url}{self.API_PREFIX}/tokens?provider_id={provider_id}", headers=self._get_headers()
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            data = response.json()

        return RevokeTokensResponse(message=data["message"], provider_id=data["provider_id"])

    async def close(self):
        pass
