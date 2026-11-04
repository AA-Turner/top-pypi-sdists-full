# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Generated root-resource wiring for ``Composio`` and ``AsyncComposio``.

The two mixins below declare which resources hang off a client and construct
them. Everything else about the clients — options resolution, the transport,
the retry policy, the context-manager protocol — stays hand-written in
``_client.py`` and ``_base_client.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._internal._internal import AsyncInternalResource, InternalResource
from .api_key_revocation import ApiKeyRevocationResource, AsyncApiKeyRevocationResource
from .auth.auth import AsyncAuthResource, AuthResource
from .auth_configs import AsyncAuthConfigsResource, AuthConfigsResource
from .connected_accounts import AsyncConnectedAccountsResource, ConnectedAccountsResource
from .custom import AsyncCustomResource, CustomResource
from .files import AsyncFilesResource, FilesResource
from .keyring import AsyncKeyringResource, KeyringResource
from .link import AsyncLinkResource, LinkResource
from .logs import AsyncLogsResource, LogsResource
from .mcp.mcp import AsyncMcpResource, McpResource
from .org.org import AsyncOrgResource, OrgResource
from .project.project import AsyncProjectResource, ProjectResource
from .session_configs import AsyncSessionConfigsResource, SessionConfigsResource
from .tool_router.tool_router import AsyncToolRouterResource, ToolRouterResource
from .toolkits import AsyncToolkitsResource, ToolkitsResource
from .tools import AsyncToolsResource, ToolsResource
from .trigger_instances.trigger_instances import AsyncTriggerInstancesResource, TriggerInstancesResource
from .triggers_types import AsyncTriggersTypesResource, TriggersTypesResource
from .webhook_endpoints import AsyncWebhookEndpointsResource, WebhookEndpointsResource
from .webhook_subscriptions import AsyncWebhookSubscriptionsResource, WebhookSubscriptionsResource

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, SyncAPIClient


class ClientResources:
    """The root resources of ``Composio``."""

    tool_router: ToolRouterResource
    tools: ToolsResource
    files: FilesResource
    connected_accounts: ConnectedAccountsResource
    link: LinkResource
    toolkits: ToolkitsResource
    auth_configs: AuthConfigsResource
    triggers_types: TriggersTypesResource
    trigger_instances: TriggerInstancesResource
    mcp: McpResource
    logs: LogsResource
    project: ProjectResource
    webhook_subscriptions: WebhookSubscriptionsResource
    webhook_endpoints: WebhookEndpointsResource
    org: OrgResource
    auth: AuthResource
    api_key_revocation: ApiKeyRevocationResource
    _internal: InternalResource
    custom: CustomResource
    keyring: KeyringResource
    session_configs: SessionConfigsResource

    def _install_resources(self, client: SyncAPIClient) -> None:
        self.tool_router = ToolRouterResource(client)
        self.tools = ToolsResource(client)
        self.files = FilesResource(client)
        self.connected_accounts = ConnectedAccountsResource(client)
        self.link = LinkResource(client)
        self.toolkits = ToolkitsResource(client)
        self.auth_configs = AuthConfigsResource(client)
        self.triggers_types = TriggersTypesResource(client)
        self.trigger_instances = TriggerInstancesResource(client)
        self.mcp = McpResource(client)
        self.logs = LogsResource(client)
        self.project = ProjectResource(client)
        self.webhook_subscriptions = WebhookSubscriptionsResource(client)
        self.webhook_endpoints = WebhookEndpointsResource(client)
        self.org = OrgResource(client)
        self.auth = AuthResource(client)
        self.api_key_revocation = ApiKeyRevocationResource(client)
        self._internal = InternalResource(client)
        self.custom = CustomResource(client)
        self.keyring = KeyringResource(client)
        self.session_configs = SessionConfigsResource(client)


class AsyncClientResources:
    """The root resources of ``AsyncComposio``."""

    tool_router: AsyncToolRouterResource
    tools: AsyncToolsResource
    files: AsyncFilesResource
    connected_accounts: AsyncConnectedAccountsResource
    link: AsyncLinkResource
    toolkits: AsyncToolkitsResource
    auth_configs: AsyncAuthConfigsResource
    triggers_types: AsyncTriggersTypesResource
    trigger_instances: AsyncTriggerInstancesResource
    mcp: AsyncMcpResource
    logs: AsyncLogsResource
    project: AsyncProjectResource
    webhook_subscriptions: AsyncWebhookSubscriptionsResource
    webhook_endpoints: AsyncWebhookEndpointsResource
    org: AsyncOrgResource
    auth: AsyncAuthResource
    api_key_revocation: AsyncApiKeyRevocationResource
    _internal: AsyncInternalResource
    custom: AsyncCustomResource
    keyring: AsyncKeyringResource
    session_configs: AsyncSessionConfigsResource

    def _install_resources(self, client: AsyncAPIClient) -> None:
        self.tool_router = AsyncToolRouterResource(client)
        self.tools = AsyncToolsResource(client)
        self.files = AsyncFilesResource(client)
        self.connected_accounts = AsyncConnectedAccountsResource(client)
        self.link = AsyncLinkResource(client)
        self.toolkits = AsyncToolkitsResource(client)
        self.auth_configs = AsyncAuthConfigsResource(client)
        self.triggers_types = AsyncTriggersTypesResource(client)
        self.trigger_instances = AsyncTriggerInstancesResource(client)
        self.mcp = AsyncMcpResource(client)
        self.logs = AsyncLogsResource(client)
        self.project = AsyncProjectResource(client)
        self.webhook_subscriptions = AsyncWebhookSubscriptionsResource(client)
        self.webhook_endpoints = AsyncWebhookEndpointsResource(client)
        self.org = AsyncOrgResource(client)
        self.auth = AsyncAuthResource(client)
        self.api_key_revocation = AsyncApiKeyRevocationResource(client)
        self._internal = AsyncInternalResource(client)
        self.custom = AsyncCustomResource(client)
        self.keyring = AsyncKeyringResource(client)
        self.session_configs = AsyncSessionConfigsResource(client)
