from __future__ import annotations

import abc
import logging
from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from dataclasses import dataclass
from types import TracebackType
from typing import Any

import aiohttp
from aiohttp import ClientResponseError
from yarl import URL

from .entities import (
    AddNodePoolRequest,
    CloudProviderOptions,
    CloudProviderType,
    Cluster,
    NodePool,
    NotificationType,
    PatchClusterRequest,
    PatchNodePoolResourcesRequest,
    PatchNodePoolSizeRequest,
    PutNodePoolRequest,
    ResourcePreset,
)
from .factories import EntityFactory, PayloadFactory

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _Endpoints:
    clusters: str = "clusters"
    cloud_providers: str = "cloud_providers"

    def cloud_provider_options(self, type: CloudProviderType) -> str:
        return f"{self.cloud_providers}/{type.value}"

    def cluster(self, cluster_name: str) -> str:
        return f"{self.clusters}/{cluster_name}"

    def node_pools(self, cluster_name: str) -> str:
        return f"{self.cluster(cluster_name)}/cloud_provider/node_pools"

    def node_pool(self, cluster_name: str, node_pool_name: str) -> str:
        return f"{self.node_pools(cluster_name)}/{node_pool_name}"

    def storages(self, cluster_name: str) -> str:
        return f"{self.cluster(cluster_name)}/cloud_provider/storages"

    def storage(self, cluster_name: str, storage_name: str) -> str:
        return f"{self.storages(cluster_name)}/{storage_name}"

    def notifications(self, cluster_name: str) -> str:
        return f"{self.cluster(cluster_name)}/notifications"

    def resource_presets(self, cluster_name: str) -> str:
        return f"{self.cluster(cluster_name)}/orchestrator/resource_presets"

    def resource_preset(self, cluster_name: str, preset_name: str) -> str:
        return f"{self.resource_presets(cluster_name)}/{preset_name}"


class ConfigClientBase:
    def __init__(self) -> None:
        self._endpoints = _Endpoints()
        self._entity_factory = EntityFactory()
        self._payload_factory = PayloadFactory()

    @abc.abstractmethod
    def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> AbstractAsyncContextManager[aiohttp.ClientResponse]:
        pass

    def _create_headers(self, *, token: str | None = None) -> dict[str, str]:
        result = {}
        if token:
            result["Authorization"] = f"Bearer {token}"
        return result

    async def list_cloud_provider_options(
        self, *, token: str | None = None
    ) -> list[CloudProviderOptions]:
        path = self._endpoints.cloud_providers
        async with self._request(
            "GET", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            result: list[CloudProviderOptions] = []
            for k, v in resp_payload.items():
                result.append(
                    self._entity_factory.create_cloud_provider_options(
                        CloudProviderType(k), v
                    )
                )
            return result

    async def get_cloud_provider_options(
        self, type: CloudProviderType, *, token: str | None = None
    ) -> CloudProviderOptions:
        path = self._endpoints.cloud_provider_options(type)
        async with self._request(
            "GET", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cloud_provider_options(
                type, resp_payload
            )

    async def list_clusters(self, *, token: str | None = None) -> Sequence[Cluster]:
        async with self._request(
            "GET", self._endpoints.clusters, headers=self._create_headers(token=token)
        ) as response:
            payload = await response.json()
            return [self._entity_factory.create_cluster(p) for p in payload]

    async def get_cluster(self, name: str, *, token: str | None = None) -> Cluster:
        async with self._request(
            "GET",
            self._endpoints.cluster(name),
            headers=self._create_headers(token=token),
        ) as response:
            payload = await response.json()
            return self._entity_factory.create_cluster(payload)

    async def create_blank_cluster(
        self,
        name: str,
        service_token: str,
        *,
        ignore_existing: bool = False,
        token: str | None = None,
    ) -> Cluster:
        payload = {"name": name, "token": service_token}
        try:
            async with self._request(
                "POST",
                self._endpoints.clusters,
                headers=self._create_headers(token=token),
                json=payload,
            ) as resp:
                resp_payload = await resp.json()
                return self._entity_factory.create_cluster(resp_payload)
        except ClientResponseError as e:
            is_existing = e.status == 400 and "already exists" in e.message
            if not ignore_existing or is_existing:
                raise
        return await self.get_cluster(name)

    async def patch_cluster(
        self, name: str, request: PatchClusterRequest, *, token: str | None = None
    ) -> Cluster:
        path = self._endpoints.cluster(name)
        payload = self._payload_factory.create_patch_cluster_request(request)
        async with self._request(
            "PATCH", path, headers=self._create_headers(token=token), json=payload
        ) as resp:
            resp_payload = await resp.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def delete_cluster(self, name: str, *, token: str | None = None) -> None:
        async with self._request(
            "DELETE",
            self._endpoints.cluster(name),
            headers=self._create_headers(token=token),
        ):
            pass

    async def add_storage(
        self,
        cluster_name: str,
        storage_name: str,
        size: int | None = None,
        *,
        start_deployment: bool = True,
        ignore_existing: bool = False,
        token: str | None = None,
    ) -> Cluster:
        try:
            path = self._endpoints.storages(cluster_name)
            payload: dict[str, Any] = {"name": storage_name}
            if size is not None:
                payload["size"] = size
            async with self._request(
                "POST",
                path,
                params={"start_deployment": str(start_deployment).lower()},
                headers=self._create_headers(token=token),
                json=payload,
            ) as response:
                resp_payload = await response.json()
                return self._entity_factory.create_cluster(resp_payload)
        except ClientResponseError as e:
            if not ignore_existing or e.status != 409:
                raise
        return await self.get_cluster(cluster_name)

    async def patch_storage(
        self,
        cluster_name: str,
        storage_name: str | None,
        ready: bool | None = None,
        *,
        ignore_not_found: bool = False,
        token: str | None = None,
    ) -> Cluster:
        try:
            if storage_name:
                path = self._endpoints.storage(cluster_name, storage_name)
            else:
                path = self._endpoints.storage(cluster_name, "default/entry")
            payload: dict[str, Any] = {}
            if ready is not None:
                payload["ready"] = ready
            async with self._request(
                "PATCH", path, headers=self._create_headers(token=token), json=payload
            ) as response:
                resp_payload = await response.json()
                return self._entity_factory.create_cluster(resp_payload)
        except ClientResponseError as e:
            if not ignore_not_found or e.status != 404:
                raise
        return await self.get_cluster(cluster_name)

    async def remove_storage(
        self,
        cluster_name: str,
        storage_name: str,
        *,
        start_deployment: bool = True,
        ignore_not_found: bool = False,
        token: str | None = None,
    ) -> Cluster:
        try:
            path = self._endpoints.storage(cluster_name, storage_name)
            async with self._request(
                "DELETE",
                path,
                params={"start_deployment": str(start_deployment).lower()},
                headers=self._create_headers(token=token),
            ) as response:
                resp_payload = await response.json()
                return self._entity_factory.create_cluster(resp_payload)
        except ClientResponseError as e:
            if not ignore_not_found or e.status != 404:
                raise
        return await self.get_cluster(cluster_name)

    async def get_node_pool(
        self, cluster_name: str, node_pool_name: str, *, token: str | None = None
    ) -> NodePool:
        path = self._endpoints.node_pool(cluster_name, node_pool_name)
        async with self._request(
            "GET", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_node_pool(resp_payload)

    async def list_node_pools(
        self, cluster_name: str, *, token: str | None = None
    ) -> list[NodePool]:
        path = self._endpoints.node_pools(cluster_name)
        async with self._request(
            "GET", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            return [self._entity_factory.create_node_pool(n) for n in resp_payload]

    async def add_node_pool(
        self,
        cluster_name: str,
        node_pool: AddNodePoolRequest,
        *,
        start_deployment: bool = True,
        token: str | None = None,
    ) -> Cluster:
        """Add new node pool to the existing cluster.
        Cloud provider should be already set up.

        Make sure you use one of the available node pool templates by providing
        its machine type, if the cluster is deployed in public cloud
        (AWS / GCP / Azure / VCD).

        Args:
            cluster_name (str): Name of the cluster within the platform.
            node_pool (NodePool): Node pool instance.
                For templates, you could use template.to_node_pool() method
            start_deployment (bool, optional): Start applying changes. Defaults to True.

        Returns:
            Cluster: Cluster instance with applied changes
        """
        path = self._endpoints.node_pools(cluster_name)
        payload = self._payload_factory.create_add_node_pool_request(node_pool)
        async with self._request(
            "POST",
            path,
            params={"start_deployment": str(start_deployment).lower()},
            headers=self._create_headers(token=token),
            json=payload,
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def put_node_pool(
        self,
        cluster_name: str,
        node_pool: PutNodePoolRequest,
        *,
        start_deployment: bool = True,
        token: str | None = None,
    ) -> Cluster:
        path = self._endpoints.node_pool(cluster_name, node_pool.name)
        payload = self._payload_factory.create_add_node_pool_request(node_pool)
        async with self._request(
            "PUT",
            path,
            params={"start_deployment": str(start_deployment).lower()},
            headers=self._create_headers(token=token),
            json=payload,
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def patch_node_pool(
        self,
        cluster_name: str,
        node_pool_name: str,
        request: PatchNodePoolSizeRequest | PatchNodePoolResourcesRequest,
        *,
        start_deployment: bool = True,
        token: str | None = None,
    ) -> Cluster:
        path = self._endpoints.node_pool(cluster_name, node_pool_name)
        payload = self._payload_factory.create_patch_node_pool_request(request)
        async with self._request(
            "PATCH",
            path,
            params={"start_deployment": str(start_deployment).lower()},
            headers=self._create_headers(token=token),
            json=payload,
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def delete_node_pool(
        self,
        cluster_name: str,
        node_pool_name: str,
        *,
        start_deployment: bool = True,
        token: str | None = None,
    ) -> Cluster:
        path = self._endpoints.node_pool(cluster_name, node_pool_name)
        async with self._request(
            "DELETE",
            path,
            params={"start_deployment": str(start_deployment).lower()},
            headers=self._create_headers(token=token),
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def notify(
        self,
        cluster_name: str,
        notification_type: NotificationType,
        message: str | None = None,
        *,
        token: str | None = None,
    ) -> None:
        path = self._endpoints.notifications(cluster_name)
        payload = {"notification_type": notification_type.value}
        if message:
            payload["message"] = message
        async with self._request(
            "POST", path, headers=self._create_headers(token=token), json=payload
        ):
            pass

    async def list_resource_presets(
        self, cluster_name: str, *, token: str | None = None
    ) -> list[ResourcePreset]:
        path = self._endpoints.resource_presets(cluster_name)
        async with self._request(
            "GET", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            return [
                self._entity_factory.create_resource_preset(p) for p in resp_payload
            ]

    async def get_resource_preset(
        self, cluster_name: str, preset_name: str, *, token: str | None = None
    ) -> ResourcePreset:
        path = self._endpoints.resource_preset(cluster_name, preset_name)
        async with self._request(
            "GET", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_resource_preset(resp_payload)

    async def add_resource_preset(
        self, cluster_name: str, preset: ResourcePreset, *, token: str | None = None
    ) -> Cluster:
        path = self._endpoints.resource_presets(cluster_name)
        payload = self._payload_factory.create_resource_preset(preset)
        async with self._request(
            "POST", path, headers=self._create_headers(token=token), json=payload
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def put_resource_preset(
        self, cluster_name: str, preset: ResourcePreset, *, token: str | None = None
    ) -> Cluster:
        path = self._endpoints.resource_preset(cluster_name, preset.name)
        payload = self._payload_factory.create_resource_preset(preset)
        async with self._request(
            "PUT", path, headers=self._create_headers(token=token), json=payload
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)

    async def delete_resource_preset(
        self, cluster_name: str, preset_name: str, *, token: str | None = None
    ) -> Cluster:
        path = self._endpoints.resource_preset(cluster_name, preset_name)
        async with self._request(
            "DELETE", path, headers=self._create_headers(token=token)
        ) as response:
            resp_payload = await response.json()
            return self._entity_factory.create_cluster(resp_payload)


class ConfigClient(ConfigClientBase):
    def __init__(
        self,
        url: URL,
        token: str | None = None,
        timeout: aiohttp.ClientTimeout = aiohttp.client.DEFAULT_TIMEOUT,
        trace_configs: Sequence[aiohttp.TraceConfig] = (),
    ):
        super().__init__()

        self._base_url = url / "api/v1"
        self._token = token
        self._timeout = timeout
        self._trace_configs = trace_configs
        self._client: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> ConfigClient:
        self._client = await self._create_http_client()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        assert self._client
        await self._client.close()

    async def _create_http_client(self) -> aiohttp.ClientSession:
        client = aiohttp.ClientSession(
            headers=self._create_default_headers(),
            timeout=self._timeout,
            trace_configs=list(self._trace_configs),
        )
        return await client.__aenter__()

    def _create_default_headers(self) -> dict[str, str]:
        result = {}
        if self._token:
            result["Authorization"] = f"Bearer {self._token}"
        return result

    @asynccontextmanager
    async def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> AsyncIterator[aiohttp.ClientResponse]:
        assert self._client
        assert self._base_url
        url = self._base_url / path
        if params:
            url = url.with_query(params)

        async with self._client.request(
            method, url, json=json, headers=headers
        ) as response:
            response.raise_for_status()
            yield response
