"""What a GPU provider must do, and the shapes that cross that line.

A provider rents the machines; it never sees the bucket's credentials, only
the presigned URLs the client puts into a job's input or a pod's environment.
"""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel


class GpuProviderError(RuntimeError):
    """The provider could not be reached or refused. Carries the status and
    the provider's own message, never the request, which holds the key."""


class RenderJobInput(BaseModel):
    """The render worker's job input (``sims/gpu-box-runpod/serverless/render_worker.py``
    ``RenderInput``): presigned URLs for one object each, and the frames."""

    blend_url: str
    output_url: str
    # The worker PUTs started.json here as it begins, and its RenderResult
    # to result_url however the render ends.
    started_url: str
    result_url: str
    # Blender's -f syntax, or "all" for the range saved in the file.
    frames: str
    # Unix time after which a worker that only now picks the job up refuses
    # it: its grants and the caller's wait are sized to this.
    start_by: float
    # Ignored by the worker; names the job in the provider's own records.
    gpu_job_id: str


class RegistryCredential(BaseModel):
    """A pull credential for one pod's private image, minted right before
    the pod boots (``plato.gpu.registry``). The provider stores it under the
    pod's name, pulls with it, and deletes it with the pod."""

    username: str
    password: str


class PodSpec(BaseModel):
    """A whole machine to boot: image, GPU, and the environment that carries
    its bootstrap and grants."""

    name: str
    image: str
    gpu_type_ids: list[str]
    container_disk_gb: int
    # "<port>/http" entries the provider proxies.
    ports: list[str]
    env: dict[str, str]
    entrypoint: list[str]
    # None: a public image, or the provider's own stored credential.
    pull: RegistryCredential | None = None


class PodInfo(BaseModel):
    """What the provider says about one pod."""

    id: str
    name: str
    # The provider's own lifecycle word; ``running`` is True while it bills.
    status: str
    running: bool
    cost_per_hour: float | None = None
    # The stored credential the pod pulled with, if any.
    pull_credential_id: str | None = None
    # The HTTP ports the provider proxies, in the order the pod was created
    # with (the client puts MCP first, the desktop second).
    ports: list[int] = []


class GpuProvider(Protocol):
    """The provider's four verbs. Everything else is the client's."""

    async def submit_render(self, job: RenderJobInput) -> str:
        """Queue a render; returns the provider's job id."""
        ...

    async def create_pod(self, spec: PodSpec) -> PodInfo:
        """Boots the pod; a ``spec.pull`` is stored under the pod's name first."""
        ...

    async def get_pod(self, pod_id: str) -> PodInfo | None:
        """The pod, or None once the provider no longer knows it."""
        ...

    async def terminate_pod(self, pod_id: str) -> None:
        """Ends the pod and the pull credential stored under its name;
        billing stops. Gone already is fine."""
        ...

    async def list_pods(self) -> list[PodInfo]: ...

    def pod_http_url(self, pod_id: str, port: int) -> str:
        """Where the provider proxies the pod's HTTP port."""
        ...
