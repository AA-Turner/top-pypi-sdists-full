"""Tests for the LangChain Auth client."""

import pytest
import httpx
import respx

from langchain_auth import (
    Client,
    AuthResult,
    OAuthProvider,
    OAuthTokenStatusResponse,
    DeleteProviderResponse,
    RevokeTokensResponse,
)

MOCK_PROVIDER_RESPONSE = {
    "id": "uuid-123",
    "organization_id": "org-123",
    "provider_id": "google",
    "name": "Google OAuth",
    "client_id": "client-123",
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "uses_pkce": True,
    "code_challenge_method": "S256",
    "provider_type": "oauth2",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}


@pytest.fixture
def client():
    return Client(api_key="test-api-key", api_url="https://test.api.com")


class TestClientConstructor:
    def test_default_api_url(self, monkeypatch):
        monkeypatch.delenv("LANGSMITH_API_URL", raising=False)
        client = Client(api_key="test-key")
        assert client.api_url == "https://api.host.langchain.com"

    def test_custom_api_url_and_key(self):
        client = Client(api_key="key", api_url="https://custom.com")
        assert client.api_url == "https://custom.com"
        assert client.api_key == "key"

    def test_raises_error_when_no_api_key(self, monkeypatch):
        monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
        with pytest.raises(ValueError, match="API key is required"):
            Client(api_key=None)

    def test_reads_langsmith_api_key_env_var(self, monkeypatch):
        monkeypatch.setenv("LANGSMITH_API_KEY", "env-api-key")
        client = Client()
        assert client.api_key == "env-api-key"

    def test_reads_langsmith_api_url_env_var(self, monkeypatch):
        monkeypatch.setenv("LANGSMITH_API_URL", "https://env.example.com/api-host")
        client = Client(api_key="test-key")
        assert client.api_url == "https://env.example.com/api-host"

    def test_api_url_param_takes_precedence_over_env_var(self, monkeypatch):
        monkeypatch.setenv("LANGSMITH_API_URL", "https://env.example.com")
        client = Client(api_key="test-key", api_url="https://param.example.com")
        assert client.api_url == "https://param.example.com"

    def test_strips_trailing_slash(self):
        client = Client(api_key="test-key", api_url="https://example.com/")
        assert client.api_url == "https://example.com"

    def test_strips_multiple_trailing_slashes(self):
        client = Client(api_key="test-key", api_url="https://example.com///")
        assert client.api_url == "https://example.com"

    def test_env_var_trailing_slash_stripped(self, monkeypatch):
        monkeypatch.setenv("LANGSMITH_API_URL", "https://env.example.com/api-host/")
        client = Client(api_key="test-key")
        assert client.api_url == "https://env.example.com/api-host"


class TestAuthenticate:
    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_completed_with_token(self, client):
        respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": "completed",
                    "token": "access-token-123",
                },
            )
        )

        result = await client.authenticate(
            provider="google",
            scopes=["email", "profile"],
            user_id="user-123",
        )

        assert result.status == "completed"
        assert result.token == "access-token-123"

    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_pending_with_auth_url(self, client):
        respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": "pending",
                    "url": "https://accounts.google.com/oauth",
                    "auth_id": "auth-123",
                },
            )
        )

        result = await client.authenticate(
            provider="google",
            scopes=["email"],
            user_id="user-123",
        )

        assert result.status == "pending"
        assert result.url == "https://accounts.google.com/oauth"
        assert result.auth_id == "auth-123"

    @respx.mock
    @pytest.mark.asyncio
    async def test_includes_optional_params(self, client):
        route = respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(200, json={"status": "completed", "token": "token"})
        )

        await client.authenticate(
            provider="google",
            scopes=["email"],
            user_id="user-123",
            ls_user_id="ls-user-456",
            agent_id="agent-789",
        )

        request = route.calls[0].request
        import json

        body = json.loads(request.content)
        assert body["ls_user_id"] == "ls-user-456"
        assert body["agent_id"] == "agent-789"

    @respx.mock
    @pytest.mark.asyncio
    async def test_throws_on_http_error(self, client):
        respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(401, text="Unauthorized")
        )

        with pytest.raises(Exception, match="HTTP 401"):
            await client.authenticate(
                provider="google",
                scopes=["email"],
                user_id="user-123",
            )


class TestWaitForCompletion:
    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_completed(self, client):
        respx.get("https://test.api.com/v2/auth/wait/auth-123?timeout=300").mock(
            return_value=httpx.Response(200, json={"status": "completed"})
        )

        result = await client.wait_for_completion("auth-123")

        assert result.status == "completed"

    @respx.mock
    @pytest.mark.asyncio
    async def test_uses_custom_timeout(self, client):
        route = respx.get("https://test.api.com/v2/auth/wait/auth-123?timeout=60").mock(
            return_value=httpx.Response(200, json={"status": "completed"})
        )

        await client.wait_for_completion("auth-123", timeout=60)

        assert route.called

    @respx.mock
    @pytest.mark.asyncio
    async def test_throws_on_timeout_status(self, client):
        respx.get("https://test.api.com/v2/auth/wait/auth-123?timeout=60").mock(
            return_value=httpx.Response(200, json={"status": "timeout"})
        )

        with pytest.raises(TimeoutError, match="timed out after 60 seconds"):
            await client.wait_for_completion("auth-123", timeout=60)

    @respx.mock
    @pytest.mark.asyncio
    async def test_throws_on_not_found_status(self, client):
        respx.get("https://test.api.com/v2/auth/wait/auth-123?timeout=300").mock(
            return_value=httpx.Response(200, json={"status": "not_found"})
        )

        with pytest.raises(Exception, match="not found or has expired"):
            await client.wait_for_completion("auth-123")

    @respx.mock
    @pytest.mark.asyncio
    async def test_throws_on_unknown_status(self, client):
        respx.get("https://test.api.com/v2/auth/wait/auth-123?timeout=300").mock(
            return_value=httpx.Response(200, json={"status": "pending"})
        )

        with pytest.raises(Exception, match="failed with status: pending"):
            await client.wait_for_completion("auth-123")


class TestCreateOAuthProvider:
    @respx.mock
    @pytest.mark.asyncio
    async def test_creates_provider(self, client):
        respx.post("https://test.api.com/v2/auth/providers").mock(
            return_value=httpx.Response(200, json=MOCK_PROVIDER_RESPONSE)
        )

        result = await client.create_oauth_provider(
            provider_id="google",
            name="Google OAuth",
            client_id="client-123",
            client_secret="secret-123",
            auth_url="https://accounts.google.com/o/oauth2/auth",
            token_url="https://oauth2.googleapis.com/token",
        )

        assert isinstance(result, OAuthProvider)
        assert result.provider_id == "google"
        assert result.name == "Google OAuth"

    @respx.mock
    @pytest.mark.asyncio
    async def test_includes_pkce_fields(self, client):
        route = respx.post("https://test.api.com/v2/auth/providers").mock(
            return_value=httpx.Response(200, json=MOCK_PROVIDER_RESPONSE)
        )

        await client.create_oauth_provider(
            provider_id="google",
            name="Google OAuth",
            client_id="client-123",
            client_secret="secret-123",
            auth_url="https://accounts.google.com/o/oauth2/auth",
            token_url="https://oauth2.googleapis.com/token",
            uses_pkce=True,
            code_challenge_method="S256",
        )

        import json

        body = json.loads(route.calls[0].request.content)
        assert body["uses_pkce"] is True
        assert body["code_challenge_method"] == "S256"


class TestGetOAuthProvider:
    @respx.mock
    @pytest.mark.asyncio
    async def test_gets_provider(self, client):
        respx.get("https://test.api.com/v2/auth/providers/google").mock(
            return_value=httpx.Response(200, json=MOCK_PROVIDER_RESPONSE)
        )

        result = await client.get_oauth_provider("google")

        assert isinstance(result, OAuthProvider)
        assert result.provider_id == "google"


class TestUpdateOAuthProvider:
    @respx.mock
    @pytest.mark.asyncio
    async def test_updates_provider(self, client):
        updated_response = {**MOCK_PROVIDER_RESPONSE, "name": "Updated Name"}
        respx.patch("https://test.api.com/v2/auth/providers/google").mock(
            return_value=httpx.Response(200, json=updated_response)
        )

        result = await client.update_oauth_provider("google", name="Updated Name")

        assert result.name == "Updated Name"

    @respx.mock
    @pytest.mark.asyncio
    async def test_updates_all_fields(self, client):
        route = respx.patch("https://test.api.com/v2/auth/providers/google").mock(
            return_value=httpx.Response(200, json=MOCK_PROVIDER_RESPONSE)
        )

        await client.update_oauth_provider(
            "google",
            name="New Name",
            client_id="new-client",
            client_secret="new-secret",
            auth_url="https://new-auth.com",
            token_url="https://new-token.com",
            uses_pkce=False,
            code_challenge_method="plain",
        )

        import json

        body = json.loads(route.calls[0].request.content)
        assert body["name"] == "New Name"
        assert body["client_id"] == "new-client"
        assert body["client_secret"] == "new-secret"
        assert body["auth_url"] == "https://new-auth.com"
        assert body["token_url"] == "https://new-token.com"
        assert body["uses_pkce"] is False
        assert body["code_challenge_method"] == "plain"


class TestDeleteOAuthProvider:
    @respx.mock
    @pytest.mark.asyncio
    async def test_deletes_provider(self, client):
        respx.delete("https://test.api.com/v2/auth/providers/google").mock(
            return_value=httpx.Response(200, json={"message": "Provider deleted"})
        )

        result = await client.delete_oauth_provider("google")

        assert isinstance(result, DeleteProviderResponse)
        assert result.message == "Provider deleted"


class TestListOAuthProviders:
    @respx.mock
    @pytest.mark.asyncio
    async def test_lists_providers(self, client):
        respx.get("https://test.api.com/v2/auth/providers").mock(
            return_value=httpx.Response(200, json=[MOCK_PROVIDER_RESPONSE])
        )

        result = await client.list_oauth_providers()

        assert len(result) == 1
        assert isinstance(result[0], OAuthProvider)
        assert result[0].provider_id == "google"

    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_empty_list(self, client):
        respx.get("https://test.api.com/v2/auth/providers").mock(return_value=httpx.Response(200, json=[]))

        result = await client.list_oauth_providers()

        assert len(result) == 0


class TestCheckTokenExists:
    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_true_when_exists(self, client):
        respx.get("https://test.api.com/v2/auth/tokens/exists?provider_id=google").mock(
            return_value=httpx.Response(200, json={"has_token": True})
        )

        result = await client.check_token_exists("google")

        assert isinstance(result, OAuthTokenStatusResponse)
        assert result.has_token is True

    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_false_when_not_exists(self, client):
        respx.get("https://test.api.com/v2/auth/tokens/exists?provider_id=google").mock(
            return_value=httpx.Response(200, json={"has_token": False})
        )

        result = await client.check_token_exists("google")

        assert result.has_token is False


class TestRevokeTokens:
    @respx.mock
    @pytest.mark.asyncio
    async def test_revokes_tokens(self, client):
        respx.delete("https://test.api.com/v2/auth/tokens?provider_id=google").mock(
            return_value=httpx.Response(
                200,
                json={
                    "message": "Tokens revoked",
                    "provider_id": "google",
                },
            )
        )

        result = await client.revoke_tokens("google")

        assert isinstance(result, RevokeTokensResponse)
        assert result.message == "Tokens revoked"
        assert result.provider_id == "google"


class TestHeaders:
    @respx.mock
    @pytest.mark.asyncio
    async def test_includes_api_key_header(self, client):
        route = respx.get("https://test.api.com/v2/auth/tokens/exists?provider_id=google").mock(
            return_value=httpx.Response(200, json={"has_token": True})
        )

        await client.check_token_exists("google")

        request = route.calls[0].request
        assert request.headers.get("x-api-key") == "test-api-key"

    @respx.mock
    @pytest.mark.asyncio
    async def test_includes_content_type_for_post(self, client):
        route = respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(200, json={"status": "completed", "token": "token"})
        )

        await client.authenticate(provider="google", scopes=["email"], user_id="user-123")

        request = route.calls[0].request
        assert request.headers.get("content-type") == "application/json"

    @respx.mock
    @pytest.mark.asyncio
    async def test_extra_headers_are_included(self, client):
        route = respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(200, json={"status": "completed", "token": "token"})
        )

        await client.authenticate(
            provider="google",
            scopes=["email"],
            user_id="user-123",
            extra_headers={"x-service-key": "svc-123"},
        )

        request = route.calls[0].request
        assert request.headers.get("x-service-key") == "svc-123"
        assert request.headers.get("x-api-key") == "test-api-key"
        assert request.headers.get("content-type") == "application/json"

    @respx.mock
    @pytest.mark.asyncio
    async def test_extra_headers_override_defaults(self, client):
        route = respx.post("https://test.api.com/v2/auth/authenticate").mock(
            return_value=httpx.Response(200, json={"status": "completed", "token": "token"})
        )

        await client.authenticate(
            provider="google",
            scopes=["email"],
            user_id="user-123",
            extra_headers={"x-api-key": "overridden"},
        )

        request = route.calls[0].request
        assert request.headers.get("x-api-key") == "overridden"
