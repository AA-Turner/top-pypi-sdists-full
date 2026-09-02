from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Literal, TypeVar

import httpx
from pydantic import BaseModel
import typer

from runlayer_cli.aiwatch_config_cache import (
    SyncedAIWatchConfig,
    parse_aiwatch_config,
)
from runlayer_cli.catalog_client import CatalogClientMixin
from runlayer_cli.flow_contract import attach_client_flows
from runlayer_cli.flow_delivery import FlowDeliveryQueue
from runlayer_cli.metrics import InstallationAnalyticsEvent
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_api import (
    AssignedSkillContent,
    AssignedSkillsManifest,
    AutoSyncItem,
    DeploymentPublic,
    DeploymentTriggerResponse,
    RegistryCredentials,
    PluginDetail,
    PluginListItem,
    PluginServerRef,
    PluginSkillRef,  # noqa: F401  re-exported for `from runlayer_cli.api import ...`
    ResolvedServerTarget,
    ServerListItem,
    ServerToolItem,
    SkillDetail,
    SkillFileDetail,
    SkillFileMetadata,  # noqa: F401  re-exported for `from runlayer_cli.api import ...`
    SkillScanResponse,
    ValidateYAMLResponse,
)
from runlayer_cli.symbols import FAIL
from runlayer_cli.tls import http_client
from runlayer_cli import telemetry

if TYPE_CHECKING:
    # Kept under TYPE_CHECKING so `aiwatch` (which excludes `mcp` from its
    # PyInstaller bundle) can import this module without pulling in mcp.
    # Annotations stay resolvable thanks to `from __future__ import annotations`.
    from runlayer_cli.models_mcp import LocalCapabilities, PostRequest, PreRequest

USER_AGENT = "Runlayer CLI"
API_KEY_HEADER_NAME = "x-runlayer-api-key"
_SKILL_API_TIMEOUT = 30.0
_PLUGIN_API_TIMEOUT = 30.0
_PLUGIN_READ_RETRIES = 1
_PLUGIN_READ_RETRY_SLEEP_SECONDS = 0.25
_AUDIT_LOG_TIMEOUT = 30.0
_AIWATCH_CONFIG_TIMEOUT = 10.0
# Bounded so a slow/unreachable backend can't stall command exit on the
# best-effort command-perf telemetry flush.
_COMMAND_EVENTS_TIMEOUT = 2.0
T = TypeVar("T", bound=BaseModel)

# Mirror backend SkillListFilter / PluginListFilter separately: their accepted
# values are not identical.
SkillListFilter = Literal["all", "created_by_me", "shared_with_me"]
PluginListFilter = Literal[
    "all",
    "accessible_and_auto_sync",
    "created_by_me",
    "shared_with_me",
]
_ResourceListFilter = SkillListFilter | PluginListFilter


class RunlayerClient(CatalogClientMixin):
    def __init__(
        self,
        hostname: str,
        secret: str,
        flow_queue: FlowDeliveryQueue | None = None,
    ) -> None:
        self.headers = {
            "User-Agent": USER_AGENT,
            API_KEY_HEADER_NAME: secret,
        }
        self.base_url = hostname
        self._flow_queue = flow_queue

    def _client(self, **kwargs: Any) -> httpx.Client:
        return http_client(headers=self.headers, **kwargs)

    def _handle_deployment_response(self, response: httpx.Response) -> None:
        """
        Handle deployment API response and provide user-friendly error messages.

        Args:
            response: HTTP response from deployment endpoint

        Raises:
            typer.Exit: If deployment feature is not available (404)
            httpx.HTTPStatusError: For other HTTP errors
        """
        if response.status_code == 404:
            try:
                error_data = response.json()
                if "Deployment feature not available" in error_data.get("detail", ""):
                    typer.secho(
                        f"\n{FAIL} Deployment feature is not enabled on this Runlayer instance.",
                        fg=typer.colors.RED,
                        bold=True,
                        err=True,
                    )
                    typer.echo(
                        "Please contact your administrator to enable deployment support.",
                        err=True,
                    )
                    raise typer.Exit(1)
            except (ValueError, KeyError):
                pass

        response.raise_for_status()

    def get_server_details(self, server_id: str) -> ServerDetails:
        with self._client() as client:
            response = client.get(f"{self.base_url}/api/v1/local/{server_id}")
            response.raise_for_status()
            return ServerDetails.model_validate(response.json())

    def resolve_server_target(self, target: str) -> str:
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/local/resolve",
                params={"target": target},
            )
            response.raise_for_status()
            return ResolvedServerTarget.model_validate(response.json()).server_id

    def _get_with_retries(
        self,
        client: httpx.Client,
        url: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        attempts = _PLUGIN_READ_RETRIES + 1
        last_error: httpx.RequestError | None = None
        for attempt in range(attempts):
            try:
                return client.get(url, params=params)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt == attempts - 1:
                    raise
                time.sleep(_PLUGIN_READ_RETRY_SLEEP_SECONDS)
        assert last_error is not None
        raise last_error

    def update_capabilities(
        self,
        server_id: str,
        capabilities: LocalCapabilities,
        *,
        server_version: int | None = None,
    ) -> httpx.Response:
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/local/{server_id}/capabilities",
                json=capabilities.model_dump(mode="json"),
                params=(
                    {"server_version": server_version}
                    if server_version is not None
                    else None
                ),
            )
            response.raise_for_status()
            return response

    def pre(self, server_id: str, request: PreRequest) -> httpx.Response:
        drain = self._flow_queue.drain if self._flow_queue is not None else None
        body = attach_client_flows(request.model_dump(), drain)
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/local/{server_id}/pre",
                json=body,
            )
            return response

    def post(self, server_id: str, request: PostRequest) -> httpx.Response:
        drain = self._flow_queue.drain if self._flow_queue is not None else None
        body = attach_client_flows(request.model_dump(), drain)
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/local/{server_id}/post",
                json=body,
            )
            return response

    def get_deployment(self, deployment_id: str) -> DeploymentPublic:
        """Get a deployment by ID."""
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/deployments/{deployment_id}",
            )
            self._handle_deployment_response(response)
            return DeploymentPublic.model_validate(response.json())

    def create_deployment(self, name: str) -> DeploymentPublic:
        """
        Create a new deployment with just a name.

        The backend always generates and returns a default template YAML.

        Args:
            name: Deployment name

        Returns:
            DeploymentPublic with template_yaml field
        """
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/deployments/",
                json={"name": name},
            )
            self._handle_deployment_response(response)
            return DeploymentPublic.model_validate(response.json())

    def update_deployment(
        self,
        deployment_id: str,
        configuration: dict[str, Any] | None = None,
        yaml_content: str | None = None,
        docker_image: str | None = None,
    ) -> DeploymentPublic:
        """
        Update deployment configuration.

        Args:
            deployment_id: UUID of deployment
            configuration: Legacy configuration dict (deprecated, use yaml_content)
            yaml_content: Raw YAML string to send to backend for validation
            docker_image: Docker image URI (passed separately, not in YAML)

        Returns:
            Updated deployment

        Note: If yaml_content is provided, it takes precedence over configuration.
        """
        payload: dict[str, Any] = {}

        if configuration is not None:
            payload["configuration"] = configuration

        # Send yaml_content and docker_image in request body
        if yaml_content is not None:
            payload["yaml_content"] = yaml_content
        if docker_image is not None:
            payload["docker_image"] = docker_image

        with self._client() as client:
            response = client.put(
                f"{self.base_url}/api/v1/deployments/{deployment_id}",
                json=payload,
            )
            self._handle_deployment_response(response)
            return DeploymentPublic.model_validate(response.json())

    def get_registry_credentials(self) -> RegistryCredentials:
        """Get temporary registry credentials for pushing images."""
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/deployments/registry-credentials",
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/deployments/ecr-credentials",
                )
            self._handle_deployment_response(response)
            return RegistryCredentials.model_validate(response.json())

    def trigger_deployment(self, deployment_id: str) -> DeploymentTriggerResponse:
        """Trigger a deployment."""
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/deployments/{deployment_id}/trigger",
            )
            self._handle_deployment_response(response)
            return DeploymentTriggerResponse.model_validate(response.json())

    def validate_yaml(self, yaml_content: str) -> ValidateYAMLResponse:
        """
        Validate YAML configuration without creating a deployment.

        This calls the backend validation endpoint to check the YAML structure.
        No local validation is performed - this is a pure pass-through to backend.

        Args:
            yaml_content: Raw YAML string to validate

        Returns:
            Validation result with any errors from backend
        """
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/deployments/validate-yaml",
                json={"yaml_content": yaml_content},
            )
            self._handle_deployment_response(response)
            return ValidateYAMLResponse.model_validate(response.json())

    def get_deployment_status(self, deployment_id: str) -> dict[str, Any]:
        """Get deployment status."""
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/deployments/{deployment_id}/status",
            )
            self._handle_deployment_response(response)
            return response.json()

    def get_deployment_logs(self, history_id: str) -> str | None:
        """
        Get deployment logs for a specific history entry.

        Args:
            history_id: UUID of the deployment history entry

        Returns:
            Logs string or None if no logs available
        """
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/deployments/history/{history_id}/logs",
            )
            self._handle_deployment_response(response)
            data = response.json()
            return data.get("logs")

    def get_deployment_history(
        self, deployment_id: str, limit: int = 100
    ) -> dict[str, Any]:
        """
        Get deployment history for a deployment.

        Args:
            deployment_id: UUID of the deployment
            limit: Maximum number of history entries to return

        Returns:
            Dictionary with 'data' (list of history entries) and 'count'
        """
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/deployments/{deployment_id}/history",
                params={"limit": limit},
            )
            self._handle_deployment_response(response)
            return response.json()

    def delete_deployment(self, deployment_id: str) -> None:
        """
        Delete a deployment and trigger infrastructure destruction.

        Args:
            deployment_id: UUID of the deployment to delete

        Raises:
            typer.Exit: If deployment feature is not available or deletion fails
            httpx.HTTPStatusError: For other HTTP errors
        """
        with self._client() as client:
            response = client.delete(
                f"{self.base_url}/api/v1/deployments/{deployment_id}",
            )
            self._handle_deployment_response(response)

    def export_deployment_yaml(self, deployment_id: str) -> str:
        """
        Export deployment configuration as YAML string.

        Args:
            deployment_id: UUID of the deployment to export

        Returns:
            YAML configuration string

        Raises:
            typer.Exit: If deployment feature is not available or export fails
            httpx.HTTPStatusError: For other HTTP errors
            ValueError: If the response is missing or contains empty yaml_content
        """
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/deployments/{deployment_id}/export-yaml",
            )
            self._handle_deployment_response(response)
            data = response.json()
            yaml_content = data.get("yaml_content", "")
            if not yaml_content or not yaml_content.strip():
                raise ValueError(
                    "Server returned empty YAML content. "
                    "This may indicate an API response issue or schema mismatch."
                )
            return yaml_content

    def submit_mcp_watch_scan(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit MCP Watch scan results to the backend.

        Tries /api/v1/ai-watch/scan first, falls back to the legacy
        /api/v1/mcp-watch/scan path if the server hasn't been updated yet.
        Returns {"unsupported": True} only if both paths 404.
        """
        with telemetry.command_span("cli.submit", endpoint="ai-watch/scan"):
            # Propagate W3C trace context so the backend ingest span joins this
            # trace. Best-effort: empty when tracing is disabled.
            trace_headers: dict[str, str] = {}
            telemetry.inject_trace_context(trace_headers)
            with self._client() as client:
                response = client.post(
                    f"{self.base_url}/api/v1/ai-watch/scan",
                    json=payload,
                    headers=trace_headers or None,
                )
                if response.status_code == 404:
                    response = client.post(
                        f"{self.base_url}/api/v1/mcp-watch/scan",
                        json=payload,
                        headers=trace_headers or None,
                    )
                if response.status_code == 404:
                    return {"unsupported": True}
                response.raise_for_status()
                return response.json()

    def submit_aiwatch_checkin(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit an AI Watch feature check-in to the backend."""
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/check-in",
                json=payload,
            )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()

    def get_aiwatch_config(self) -> SyncedAIWatchConfig | None:
        """Fetch backend-authoritative AI Watch settings when supported."""
        with self._client(timeout=_AIWATCH_CONFIG_TIMEOUT) as client:
            response = client.get(f"{self.base_url}/api/v1/ai-watch/config")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return parse_aiwatch_config(response.json())

    def submit_agents(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit discovered AI agents (filesystem-scan phase) to the backend.

        POSTs the redacted agent report to /api/v1/ai-watch/agents. This endpoint
        is ai-watch-only (no legacy mcp-watch path), so a 404 means the backend
        predates agent ingest -> return {"unsupported": True} so the caller can
        bucket it like the other per-category scan submissions.
        """
        with telemetry.command_span("cli.submit", endpoint="ai-watch/agents"):
            # Propagate W3C trace context so the backend ingest span joins this
            # trace. Best-effort: empty when tracing is disabled.
            trace_headers: dict[str, str] = {}
            telemetry.inject_trace_context(trace_headers)
            with self._client(timeout=120) as client:
                response = client.post(
                    f"{self.base_url}/api/v1/ai-watch/agents",
                    json=payload,
                    headers=trace_headers or None,
                )
                if response.status_code == 404:
                    return {"unsupported": True}
                response.raise_for_status()
                return response.json()

    def submit_agent_definitions(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit client-native agent definitions to AI Watch."""
        with telemetry.command_span(
            "cli.submit", endpoint="ai-watch/agent-definitions"
        ):
            trace_headers: dict[str, str] = {}
            telemetry.inject_trace_context(trace_headers)
            with self._client(timeout=120) as client:
                response = client.post(
                    f"{self.base_url}/api/v1/ai-watch/agent-definitions",
                    json=payload,
                    headers=trace_headers or None,
                )
                if response.status_code == 404:
                    return {"unsupported": True}
                response.raise_for_status()
                return response.json()

    def submit_skill_fingerprint(
        self,
        identifier: str,
        artifact_type: str,
        oversized: bool = False,
    ) -> dict[str, Any]:
        """Check if a skill fingerprint is already known by the backend.

        Tries /api/v1/ai-watch/ first, falls back to /api/v1/mcp-watch/.
        """
        body = {
            "identifier": identifier,
            "artifact_type": artifact_type,
            "oversized": oversized,
        }
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/skills/lookup",
                json=body,
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/mcp-watch/skills/lookup",
                    json=body,
                )
            if response.status_code == 404:
                return {"known": False, "unsupported": True}
            response.raise_for_status()
            return response.json()

    def submit_skill_fingerprints(
        self,
        identifiers: list[str],
    ) -> dict[str, Any]:
        """Check a bounded batch of skill fingerprints."""
        body = {"identifiers": identifiers}
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/skills/lookup-batch",
                json=body,
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/mcp-watch/skills/lookup-batch",
                    json=body,
                )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()

    def submit_skill(self, skill_payload: dict[str, Any]) -> dict[str, Any]:
        """Submit a full skill for ingestion and scanning.

        Tries /api/v1/ai-watch/ first, falls back to /api/v1/mcp-watch/.
        """
        with self._client(timeout=120) as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/skills/submit",
                json=skill_payload,
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/mcp-watch/skills/submit",
                    json=skill_payload,
                )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()

    def submit_plugin_fingerprint(
        self,
        identifier: str,
    ) -> dict[str, Any]:
        """Check if a plugin fingerprint is already known."""
        body = {
            "identifier": identifier,
        }
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/plugins/lookup",
                json=body,
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/mcp-watch/plugins/lookup",
                    json=body,
                )
            if response.status_code == 404:
                return {"known": False, "unsupported": True}
            response.raise_for_status()
            return response.json()

    def submit_plugin_fingerprints(
        self,
        identifiers: list[str],
    ) -> dict[str, Any]:
        """Check a bounded batch of plugin fingerprints."""
        body = {"identifiers": identifiers}
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/plugins/lookup-batch",
                json=body,
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/mcp-watch/plugins/lookup-batch",
                    json=body,
                )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()

    def submit_plugin(self, plugin_payload: dict[str, Any]) -> dict[str, Any]:
        """Submit a full plugin for ingestion."""
        with self._client(timeout=120) as client:
            response = client.post(
                f"{self.base_url}/api/v1/ai-watch/plugins/submit",
                json=plugin_payload,
            )
            if response.status_code == 404:
                response = client.post(
                    f"{self.base_url}/api/v1/mcp-watch/plugins/submit",
                    json=plugin_payload,
                )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()

    def list_servers(
        self,
        scope: str = "accessible",
        limit: int = 100,
    ) -> list[ServerListItem]:
        """
        List MCP servers the user has access to.

        Args:
            scope: "accessible" (default), "accessible_and_mine", "all", or "accessible_and_auto_sync"
            limit: Maximum number of servers to return

        Returns:
            List of ServerListItem objects

        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        params: dict[str, str | int] = {"scope": scope, "limit": limit}
        with self._client() as client:
            response = client.get(
                f"{self.base_url}/api/v1/servers",
                params=params,
            )
            response.raise_for_status()
            data = response.json()
            return [ServerListItem.model_validate(s) for s in data.get("data", [])]

    def list_paginated(
        self,
        path: str,
        *,
        model: type[T],
        params: dict[str, Any] | None = None,
    ) -> list[T]:
        items: list[T] = []
        skip = 0
        base_params = dict(params or {})

        with self._client(follow_redirects=True) as client:
            while True:
                request_params = {**base_params, "limit": 100, "skip": skip}
                response = client.get(f"{self.base_url}{path}", params=request_params)
                response.raise_for_status()
                page = [
                    model.model_validate(item)
                    for item in response.json().get("data", [])
                ]
                items.extend(page)
                if len(page) < 100:
                    break
                skip += len(page)
        return items

    def _paginate_resources(
        self,
        path: str,
        model: type[T],
        *,
        filter: _ResourceListFilter,
        namespace: str | None,
        query: str | None,
        timeout: float,
    ) -> list[T]:
        """Paginate filterable skill/plugin records, optionally scoped server-side.

        Shared loop behind :meth:`list_skills` and :meth:`list_plugins_detailed`.
        `filter="all"` + `query` powers catalog browsing; the default
        `created_by_me` matches the namespaced sync/install paths. Pages of 100
        are drained with transient-timeout retries until a short page ends it.
        """
        items: list[T] = []
        skip = 0
        with self._client(timeout=timeout) as client:
            while True:
                params: dict[str, str | int] = {
                    "filter": filter,
                    "limit": 100,
                    "skip": skip,
                }
                if namespace is not None:
                    params["namespace"] = namespace
                if query is not None:
                    params["query"] = query
                response = self._get_with_retries(
                    client, f"{self.base_url}{path}", params=params
                )
                response.raise_for_status()
                page = [
                    model.model_validate(item)
                    for item in response.json().get("data", [])
                ]
                items.extend(page)
                if len(page) < 100:
                    break
                skip += len(page)
        return items

    def list_plugins(self, limit: int = 100) -> list[PluginListItem]:
        """
        List plugins the user has access to.

        Args:
            limit: Maximum number of plugins to return

        Returns:
            List of PluginListItem objects

        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = self._get_with_retries(
                client,
                f"{self.base_url}/api/v1/plugins",
                params={"limit": limit},
            )
            response.raise_for_status()
            data = response.json()
            return [PluginListItem.model_validate(p) for p in data.get("data", [])]

    def list_auto_sync(self, entity_type: str) -> list[AutoSyncItem]:
        """List auto-sync items by entity type."""
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = self._get_with_retries(
                client,
                f"{self.base_url}/api/v1/auto-sync",
                params={"entity_type": entity_type},
            )
            response.raise_for_status()
            data = response.json()
            return [AutoSyncItem.model_validate(p) for p in data.get("data", [])]

    def list_plugins_detailed(
        self,
        namespace: str | None = None,
        *,
        filter: PluginListFilter = "created_by_me",
        query: str | None = None,
    ) -> list["PluginDetail"]:
        """Paginate full PluginDetail records, optionally filtered server-side."""
        return self._paginate_resources(
            "/api/v1/plugins",
            PluginDetail,
            filter=filter,
            namespace=namespace,
            query=query,
            timeout=_PLUGIN_API_TIMEOUT,
        )

    def create_plugin(
        self,
        name: str,
        namespace: str,
        path: str,
        description: str | None,
        is_public: bool,
        use_dynamic_tools: bool,
        servers: list[PluginServerRef],
        skill_ids: list[str],
        identifier: str | None = None,
    ) -> "PluginDetail":
        payload: dict[str, Any] = {
            "name": name,
            "namespace": namespace,
            "path": path,
            "is_public": is_public,
            "use_dynamic_tools": use_dynamic_tools,
            "servers": [server.model_dump() for server in servers],
            "skill_ids": skill_ids,
        }
        if description is not None:
            payload["description"] = description
        if identifier is not None:
            payload["identifier"] = identifier
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = client.post(f"{self.base_url}/api/v1/plugins", json=payload)
            response.raise_for_status()
            return PluginDetail.model_validate(response.json())

    def update_plugin(
        self,
        plugin_id: str,
        name: str,
        namespace: str,
        path: str,
        description: str | None,
        is_public: bool,
        use_dynamic_tools: bool,
        servers: list[PluginServerRef],
        skill_ids: list[str],
        identifier: str | None = None,
    ) -> "PluginDetail":
        payload: dict[str, Any] = {
            "name": name,
            "namespace": namespace,
            "path": path,
            "description": description,
            "is_public": is_public,
            "use_dynamic_tools": use_dynamic_tools,
            "servers": [server.model_dump() for server in servers],
            "skill_ids": skill_ids,
        }
        if identifier is not None:
            payload["identifier"] = identifier
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = client.put(
                f"{self.base_url}/api/v1/plugins/{plugin_id}",
                json=payload,
            )
            response.raise_for_status()
            return PluginDetail.model_validate(response.json())

    def get_plugin(self, plugin_id: str) -> "PluginDetail":
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = client.get(f"{self.base_url}/api/v1/plugins/{plugin_id}")
            response.raise_for_status()
            return PluginDetail.model_validate(response.json())

    def get_plugin_server_tools(self, plugin_id: str, server_id: str) -> list[str]:
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = client.get(
                f"{self.base_url}/api/v1/plugins/{plugin_id}/servers/{server_id}/tools"
            )
            response.raise_for_status()
            data = response.json()
            tool_names = data.get("tool_names", [])
            return [name for name in tool_names if isinstance(name, str)]

    def delete_plugin(self, plugin_id: str) -> None:
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = client.delete(f"{self.base_url}/api/v1/plugins/{plugin_id}")
            response.raise_for_status()

    def list_servers_for_resolution(self) -> list[ServerListItem]:
        all_servers: list[ServerListItem] = []
        skip = 0
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            while True:
                response = self._get_with_retries(
                    client,
                    f"{self.base_url}/api/v1/servers",
                    params={
                        "scope": "accessible",
                        "limit": 100,
                        "skip": skip,
                    },
                )
                response.raise_for_status()
                page = [
                    ServerListItem.model_validate(s)
                    for s in response.json().get("data", [])
                ]
                all_servers.extend(page)
                if len(page) < 100:
                    break
                skip += len(page)
        return all_servers

    def list_server_tools(self, server_id: str) -> list[ServerToolItem]:
        with self._client(timeout=_PLUGIN_API_TIMEOUT) as client:
            response = self._get_with_retries(
                client,
                f"{self.base_url}/api/v1/proxy/{server_id}/tools",
            )
            response.raise_for_status()
            return [ServerToolItem.model_validate(tool) for tool in response.json()]

    def list_skills(
        self,
        namespace: str | None = None,
        *,
        filter: SkillListFilter = "created_by_me",
        query: str | None = None,
    ) -> list["SkillDetail"]:
        """Paginate full SkillDetail records, optionally filtered server-side."""
        return self._paginate_resources(
            "/api/v1/skills",
            SkillDetail,
            filter=filter,
            namespace=namespace,
            query=query,
            timeout=_SKILL_API_TIMEOUT,
        )

    def create_skill(
        self,
        name: str,
        description: str | None = None,
        is_public: bool = False,
        namespace: str | None = None,
        path: str | None = None,
    ) -> "SkillDetail":
        payload: dict[str, Any] = {"name": name, "is_public": is_public}
        if description is not None:
            payload["description"] = description
        if namespace is not None:
            payload["namespace"] = namespace
        if path is not None:
            payload["path"] = path
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.post(f"{self.base_url}/api/v1/skills", json=payload)
            response.raise_for_status()
            return SkillDetail.model_validate(response.json())

    def score_skill(
        self,
        skill_name: str,
        files: list[dict[str, str]],
        scan_id: str | None = None,
    ) -> "SkillScanResponse":
        payload = {
            "skill_name": skill_name,
            "files": files,
        }
        headers = {"x-runlayer-scan-id": scan_id} if scan_id else None
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.post(
                f"{self.base_url}/api/v1/security/score/skill",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return SkillScanResponse.model_validate(response.json())

    def get_skill(self, skill_id: str) -> "SkillDetail":
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.get(f"{self.base_url}/api/v1/skills/{skill_id}")
            response.raise_for_status()
            return SkillDetail.model_validate(response.json())

    def get_assigned_skills(
        self,
        *,
        username: str | None = None,
        device_id: str | None = None,
    ) -> "AssignedSkillsManifest":
        """Skill-sync manifest for this device user (aiwatch org-key auth)."""
        params: dict[str, str] = {}
        if username:
            params["username"] = username
        if device_id:
            params["device_id"] = device_id
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.get(
                f"{self.base_url}/api/v1/ai-watch/skills/assigned", params=params
            )
            response.raise_for_status()
            return AssignedSkillsManifest.model_validate(response.json())

    def get_assigned_skill_content(
        self,
        skill_id: str,
        *,
        username: str | None = None,
        device_id: str | None = None,
    ) -> "AssignedSkillContent":
        """Full file contents for one skill in the resolved user's manifest."""
        params: dict[str, str] = {}
        if username:
            params["username"] = username
        if device_id:
            params["device_id"] = device_id
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.get(
                f"{self.base_url}/api/v1/ai-watch/skills/assigned/{skill_id}/content",
                params=params,
            )
            response.raise_for_status()
            return AssignedSkillContent.model_validate(response.json())

    def update_skill(
        self,
        skill_id: str,
        name: str,
        description: str | None,
        is_public: bool | None = None,
    ) -> "SkillDetail":
        payload: dict[str, Any] = {"name": name, "description": description}
        if is_public is not None:
            payload["is_public"] = is_public
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.put(
                f"{self.base_url}/api/v1/skills/{skill_id}", json=payload
            )
            response.raise_for_status()
            return SkillDetail.model_validate(response.json())

    def create_skill_file(
        self,
        skill_id: str,
        title: str,
        content: str,
        description: str | None = None,
    ) -> "SkillFileDetail":
        payload: dict[str, Any] = {"title": title, "content": content}
        if description is not None:
            payload["description"] = description
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.post(
                f"{self.base_url}/api/v1/skills/{skill_id}/files", json=payload
            )
            response.raise_for_status()
            return SkillFileDetail.model_validate(response.json())

    def get_skill_file(self, skill_id: str, file_id: str) -> "SkillFileDetail":
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.get(
                f"{self.base_url}/api/v1/skills/{skill_id}/files/{file_id}"
            )
            response.raise_for_status()
            return SkillFileDetail.model_validate(response.json())

    def update_skill_file(
        self,
        skill_id: str,
        file_id: str,
        title: str | None = None,
        content: str | None = None,
        description: str | None = None,
    ) -> "SkillFileDetail":
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if content is not None:
            payload["content"] = content
        if description is not None:
            payload["description"] = description
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.put(
                f"{self.base_url}/api/v1/skills/{skill_id}/files/{file_id}",
                json=payload,
            )
            response.raise_for_status()
            return SkillFileDetail.model_validate(response.json())

    def delete_skill(self, skill_id: str) -> None:
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.delete(f"{self.base_url}/api/v1/skills/{skill_id}")
            response.raise_for_status()

    def delete_skill_file(self, skill_id: str, file_id: str) -> None:
        with self._client(timeout=_SKILL_API_TIMEOUT) as client:
            response = client.delete(
                f"{self.base_url}/api/v1/skills/{skill_id}/files/{file_id}"
            )
            response.raise_for_status()

    def get_current_user(self) -> dict[str, Any]:
        with self._client() as client:
            response = client.get(f"{self.base_url}/api/v1/users/me")
            response.raise_for_status()
            return response.json()

    def get_audit_logs(
        self,
        *,
        action_type: str | None = None,
        server_id: str | None = None,
        agent_id: str | None = None,
        actor_id: str | None = None,
        client_name: str | None = None,
        user_id: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str | int] = {"limit": limit}
        if action_type:
            params["action_type"] = action_type
        if server_id:
            params["server_id"] = server_id
        if agent_id:
            params["agent_id"] = agent_id
        if actor_id:
            params["actor_id"] = actor_id
        if client_name:
            params["client_name"] = client_name
        if user_id:
            params["user_id"] = user_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        with self._client(timeout=_AUDIT_LOG_TIMEOUT) as client:
            response = client.get(f"{self.base_url}/api/v1/auditlogs", params=params)
            response.raise_for_status()
            return response.json()

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, Any]:
        with self._client() as client:
            response = client.post(
                f"{self.base_url}/api/v1/metrics/cli-install-events",
                json={"events": events},
            )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()

    def track_command_events(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        """POST per-command performance events to the telemetry relay.

        Best-effort telemetry: bounded timeout so command exit is never blocked
        on a slow backend, and a 404 (backend predates the endpoint) is a no-op
        rather than an error. Mirrors ``track_installation_events``.
        """
        with self._client(timeout=_COMMAND_EVENTS_TIMEOUT) as client:
            response = client.post(
                f"{self.base_url}/api/v1/telemetry/cli-command-events",
                json={"events": events},
            )
            if response.status_code == 404:
                return {"unsupported": True}
            response.raise_for_status()
            return response.json()
