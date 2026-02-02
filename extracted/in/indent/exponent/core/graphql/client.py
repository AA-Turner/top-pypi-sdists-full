from collections.abc import AsyncGenerator
from typing import Any

from gql import Client, GraphQLRequest, gql
from gql.transport.httpx import HTTPXAsyncTransport
from gql.transport.websockets import WebsocketsTransport

from exponent.core.graphql.generated_client import (
    ChatConfig,
    ChatInput,
    Chats,
    CreateCloudChatFromRepository,
    EnableCloudRepository,
    ExponentModels,
    GithubRepositories,
    HaltChatStream,
    IndentGraphQLClient,
    Prompt,
    RebuildCloudRepository,
    RefreshApiKey,
    ReportSandboxInfo,
    RepositoryInput,
    SandboxProvider,
    SetLoginComplete,
    StartChatTurn,
)


class GraphQLClient:
    """Wrapper around the generated GraphQL client with authentication."""

    def __init__(self, api_key: str, base_api_url: str, base_ws_url: str):
        self.graphql_url = f"{base_api_url}/graphql"
        self.websocket_url = f"{base_ws_url}/graphql_ws".replace(
            "https", "wss"
        ).replace("http", "ws")
        self.api_key = api_key
        self._typed_client = IndentGraphQLClient(
            url=self.graphql_url,
            headers={"API-KEY": self.api_key},
        )

    async def get_chats(self) -> Chats:
        """Get chats with proper typing."""
        return await self._typed_client.chats()

    async def get_github_repositories(self) -> GithubRepositories:
        """Get GitHub repositories with proper typing."""
        return await self._typed_client.github_repositories()

    async def halt_chat_stream(self, chat_uuid: str) -> HaltChatStream:
        """Halt a chat stream with proper typing."""
        return await self._typed_client.halt_chat_stream(chat_uuid=chat_uuid)

    async def refresh_api_key(self) -> RefreshApiKey:
        """Refresh API key with proper typing."""
        return await self._typed_client.refresh_api_key()

    async def create_cloud_chat_from_repository(
        self, repository_id: str, provider: SandboxProvider | None = None
    ) -> CreateCloudChatFromRepository:
        """Create a cloud chat from a repository with proper typing."""
        return await self._typed_client.create_cloud_chat_from_repository(
            repository_id=repository_id, provider=provider
        )

    async def enable_cloud_repository(
        self, repositories: list[RepositoryInput]
    ) -> EnableCloudRepository:
        return await self._typed_client.enable_cloud_repository(
            repositories=repositories
        )

    async def rebuild_cloud_repository(
        self, org_name: str, repo_name: str
    ) -> RebuildCloudRepository:
        """Rebuild cloud repository with proper typing."""
        return await self._typed_client.rebuild_cloud_repository(org_name, repo_name)

    async def set_login_complete(self) -> SetLoginComplete:
        """Set login complete with proper typing."""
        return await self._typed_client.set_login_complete()

    async def report_sandbox_info(
        self,
        sandbox_id: str,
        disk_usage_gb: float | None = None,
        indent_log_file: str | None = None,
    ) -> ReportSandboxInfo:
        """Report sandbox info with proper typing."""
        return await self._typed_client.report_sandbox_info(
            sandbox_id=sandbox_id,
            disk_usage_gb=disk_usage_gb,
            indent_log_file=indent_log_file,
        )

    async def start_chat_turn(
        self,
        chat_uuid: str,
        prompt: str,
        parent_uuid: str | None = None,
        exponent_model: ExponentModels = ExponentModels.PREMIUM,
        require_confirmation: bool = False,
        read_only: bool = False,
        depth_limit: int = 20,
    ) -> StartChatTurn:
        """Start a chat turn with proper typing."""
        chat_input = ChatInput(
            prompt=Prompt(message=prompt, attachments=[]),
        )
        # ty doesn't understand Pydantic's Field(alias=...) mechanism, so it expects
        # the alias name (chatUuid) instead of the field name (chat_uuid). Both work at runtime.
        chat_config = ChatConfig(  # ty: ignore[missing-argument]
            chat_uuid=chat_uuid,  # ty: ignore[unknown-argument]
            exponent_model=exponent_model,
            require_confirmation=require_confirmation,
            read_only=read_only,
            depth_limit=depth_limit,
        )
        return await self._typed_client.start_chat_turn(
            chat_input=chat_input,
            chat_config=chat_config,
            parent_uuid=parent_uuid,
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
            query = GraphQLRequest(
                query_str, variable_values=vars, operation_name=op_name
            )
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
