"""Runpod: serverless jobs (``api.runpod.ai/v2``) and pods (``rest.runpod.io/v1``).

The ONE place the Runpod key is used. It is sent as a bearer token and never
returned, logged, or put in an error message.
"""

from __future__ import annotations

from collections.abc import Callable

import httpx
from pydantic import BaseModel

from plato.gpu.providers.base import GpuProviderError, PodInfo, PodSpec, RegistryCredential, RenderJobInput

# Runpod's Cloudflare front refuses some default client User-Agents (1010).
USER_AGENT = "plato-gpu"
# A terminated pod reads as one of these until Runpod forgets it.
_ENDED = ("EXITED", "TERMINATED")


class _Job(BaseModel):
    id: str
    status: str


class _Pod(BaseModel):
    """What ``/pods`` answers; only what the client reads."""

    id: str
    name: str
    desiredStatus: str
    costPerHr: float | None = None
    containerRegistryAuthId: str | None = None
    # "<port>/http" and "<port>/tcp" entries.
    ports: list[str] | None = None


class _Credential(BaseModel):
    """What ``/containerregistryauth`` answers: never the password."""

    id: str
    name: str


class _PodCreate(BaseModel):
    """The fields of ``POST /pods`` this client sets."""

    name: str
    imageName: str
    gpuTypeIds: list[str]
    gpuCount: int = 1
    containerDiskInGb: int
    volumeInGb: int = 0
    ports: list[str]
    env: dict[str, str]
    dockerEntrypoint: list[str]
    containerRegistryAuthId: str | None = None


def _info(pod: _Pod) -> PodInfo:
    return PodInfo(
        id=pod.id,
        name=pod.name,
        status=pod.desiredStatus,
        running=pod.desiredStatus not in _ENDED,
        cost_per_hour=pod.costPerHr,
        pull_credential_id=pod.containerRegistryAuthId,
        ports=[int(entry.split("/", 1)[0]) for entry in pod.ports or [] if entry.endswith("/http")],
    )


class RunpodProvider:
    def __init__(
        self,
        api_key: str,
        *,
        rest_url: str = "https://rest.runpod.io/v1",
        api_url: str = "https://api.runpod.ai/v2",
        render_endpoint_id: str = "",
        registry_auth_id: str = "",
        client_factory: Callable[[], httpx.AsyncClient] = lambda: httpx.AsyncClient(timeout=30.0),
    ) -> None:
        if not api_key:
            raise GpuProviderError("Runpod is not configured: no API key")
        self._headers = {"Authorization": f"Bearer {api_key}", "User-Agent": USER_AGENT}
        self._rest_url = rest_url.rstrip("/")
        self._api_url = api_url.rstrip("/")
        self._render_endpoint_id = render_endpoint_id
        # Lets pods pull private images; the credential itself lives at Runpod.
        self._registry_auth_id = registry_auth_id
        self._client_factory = client_factory

    async def _request(self, method: str, url: str, *, json: object | None = None) -> httpx.Response:
        try:
            async with self._client_factory() as client:
                return await client.request(method, url, json=json, headers=self._headers)
        except httpx.RequestError as error:
            # str(error) names the URL, never the headers.
            raise GpuProviderError(f"Runpod unreachable: {error}") from error

    @staticmethod
    def _refused(response: httpx.Response) -> GpuProviderError:
        return GpuProviderError(f"Runpod returned {response.status_code}: {response.text}")

    async def submit_render(self, job: RenderJobInput) -> str:
        if not self._render_endpoint_id:
            raise GpuProviderError("Runpod is not configured: no render endpoint")
        response = await self._request(
            "POST", f"{self._api_url}/{self._render_endpoint_id}/run", json={"input": job.model_dump()}
        )
        if response.status_code != 200:
            raise self._refused(response)
        return _Job.model_validate(response.json()).id

    async def _store_credential(self, name: str, credential: RegistryCredential) -> str:
        """Stores a pull credential under ``name`` (the pod's, unique at
        Runpod); the pod is created with its id."""
        response = await self._request(
            "POST",
            f"{self._rest_url}/containerregistryauth",
            json={"name": name, "username": credential.username, "password": credential.password},
        )
        if response.status_code // 100 != 2:
            raise self._refused(response)
        return _Credential.model_validate(response.json()).id

    async def _drop_credential(self, credential_id: str, pod_name: str) -> None:
        """Deletes the credential stored under the pod's name; the account's
        standing credential (``registry_auth_id``) is never the pod's own."""
        if credential_id == self._registry_auth_id:
            return
        response = await self._request("GET", f"{self._rest_url}/containerregistryauth/{credential_id}")
        if response.status_code == 404:
            return
        if response.status_code != 200:
            raise self._refused(response)
        if _Credential.model_validate(response.json()).name != pod_name:
            return
        response = await self._request("DELETE", f"{self._rest_url}/containerregistryauth/{credential_id}")
        if response.status_code not in (200, 204, 404):
            raise self._refused(response)

    async def create_pod(self, spec: PodSpec) -> PodInfo:
        credential_id = self._registry_auth_id or None
        if spec.pull is not None:
            credential_id = await self._store_credential(spec.name, spec.pull)
        body = _PodCreate(
            name=spec.name,
            imageName=spec.image,
            gpuTypeIds=spec.gpu_type_ids,
            containerDiskInGb=spec.container_disk_gb,
            ports=spec.ports,
            env=spec.env,
            dockerEntrypoint=spec.entrypoint,
            containerRegistryAuthId=credential_id,
        )
        try:
            response = await self._request("POST", f"{self._rest_url}/pods", json=body.model_dump(exclude_none=True))
            if response.status_code // 100 != 2:
                raise self._refused(response)
        except BaseException:
            # No pod, so nothing will ever delete the credential minted for it.
            if spec.pull is not None and credential_id is not None:
                await self._drop_credential(credential_id, spec.name)
            raise
        return _info(_Pod.model_validate(response.json()))

    async def get_pod(self, pod_id: str) -> PodInfo | None:
        response = await self._request("GET", f"{self._rest_url}/pods/{pod_id}")
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise self._refused(response)
        return _info(_Pod.model_validate(response.json()))

    async def terminate_pod(self, pod_id: str) -> None:
        pod = await self.get_pod(pod_id)
        # The pod first: Runpod refuses to delete a credential a pod still
        # references ("Registry auth is in use by a pod"), so a credential-first
        # order never reached the pod delete and the pod kept billing. The
        # credential's id is read before the delete, while the pod still has it.
        response = await self._request("DELETE", f"{self._rest_url}/pods/{pod_id}")
        if response.status_code not in (200, 204, 404):
            raise self._refused(response)
        if pod is not None and pod.pull_credential_id:
            await self._drop_credential(pod.pull_credential_id, pod.name)

    async def list_pods(self) -> list[PodInfo]:
        response = await self._request("GET", f"{self._rest_url}/pods")
        if response.status_code != 200:
            raise self._refused(response)
        return [_info(_Pod.model_validate(item)) for item in response.json()]

    def pod_http_url(self, pod_id: str, port: int) -> str:
        return f"https://{pod_id}-{port}.proxy.runpod.net"
