import uuid
from collections.abc import AsyncGenerator
from typing import Any

from gql import Client, GraphQLRequest, gql
from gql.transport.httpx import HTTPXAsyncTransport
from gql.transport.websockets import WebsocketsTransport

from exponent.core.graphql.generated_client import (
    ChatConfigInput,
    ChatInput,
    ChatMode,
    ChatResourceConfigInput,
    Chats,
    CreateCloudChatFromRepository,
    CurrentUser,
    GithubRepositories,
    HaltChatStream,
    IndentGraphQLClient,
    PromptInput,
    RefreshApiKey,
    RepositoryResourceConfigInput,
    SetLoginComplete,
    StartChatTurn,
)


class GraphQLClient:
    """Wrapper around the generated GraphQL client with authentication."""

    def __init__(self, api_key: str, base_api_url: str, base_ws_url: str):
        self.graphql_url = f"{base_api_url}/graphql"
        self.websocket_url = f"{base_ws_url}/graphql_ws".replace("https", "wss").replace("http", "ws")
        self.api_key = api_key
        self._typed_client = IndentGraphQLClient(
            url=self.graphql_url,
            headers={"API-KEY": self.api_key},
        )

    async def get_chats(self, user_uuids: list[uuid.UUID] | None = None) -> Chats:
        return await self._typed_client.chats(user_uuids=user_uuids)

    async def get_current_user(self) -> CurrentUser:
        return await self._typed_client.current_user()

    async def get_github_repositories(self) -> GithubRepositories:
        """Get GitHub repositories with proper typing."""
        return await self._typed_client.github_repositories()

    async def halt_chat_stream(self, chat_uuid: str) -> HaltChatStream:
        return await self._typed_client.halt_chat_stream(chat_uuid=uuid.UUID(chat_uuid))

    async def refresh_api_key(self) -> RefreshApiKey:
        """Refresh API key with proper typing."""
        return await self._typed_client.refresh_api_key()

    async def create_cloud_chat_from_repository(self, repository_uuid: str) -> CreateCloudChatFromRepository:
        return await self._typed_client.create_cloud_chat_from_repository(
            resource_config=ChatResourceConfigInput(
                mode=ChatMode.CLOUD,
                primary_repository=RepositoryResourceConfigInput(  # ty: ignore[missing-argument]
                    repository_uuid=uuid.UUID(repository_uuid),  # ty: ignore[unknown-argument]
                ),
            ),
        )

    async def set_login_complete(self) -> SetLoginComplete:
        """Set login complete with proper typing."""
        return await self._typed_client.set_login_complete()

    async def start_chat_turn(
        self,
        chat_uuid: str,
        prompt: str,
        require_confirmation: bool = False,
        depth_limit: int = 20,
    ) -> StartChatTurn:
        chat_input = ChatInput(
            prompt_input=PromptInput(message=prompt, attachments=[]),
        )
        # ty doesn't understand Pydantic's Field(alias=...) mechanism, so it expects
        # the alias name (chatUuid) instead of the field name (chat_uuid). Both work at runtime.
        chat_config = ChatConfigInput(  # ty: ignore[missing-argument]
            chat_uuid=chat_uuid,  # ty: ignore[unknown-argument]
            require_confirmation=require_confirmation,
            depth_limit=depth_limit,
        )
        return await self._typed_client.start_chat_turn(
            chat_input=chat_input,
            chat_config=chat_config,
        )

    def get_transport(self, timeout: float | None = None) -> HTTPXAsyncTransport:
        return HTTPXAsyncTransport(
            url=self.graphql_url,
            headers={"API-KEY": self.api_key},
            timeout=timeout,
        )

    def get_ws_transport(self) -> WebsocketsTransport:
        return WebsocketsTransport(
            url=self.websocket_url,
            init_payload={"apiKey": self.api_key},
        )

    async def execute(
        self,
        query_str: str,
        vars: dict[str, Any] | None = None,
        op_name: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Execute a GraphQL query (legacy method for backward compatibility)."""
        async with Client(
            transport=self.get_transport(timeout),
            fetch_schema_from_transport=False,
            execute_timeout=timeout,
        ) as session:
            query = GraphQLRequest(query_str, variable_values=vars, operation_name=op_name)
            result = await session.execute(query)
            return result

    async def subscribe(
        self,
        subscription_str: str,
        vars: dict[str, Any] | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        async with Client(
            transport=self.get_ws_transport(),
        ) as session:
            subscription = gql(subscription_str)
            async for result in session.subscribe(subscription, vars):
                yield result
