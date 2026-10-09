"""One client over the provider and the bucket: renders and pods."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable

import httpx

from plato.gpu.pods import (
    OWNER_END,
    PodSession,
    PodStatus,
    PodView,
    create_pod,
    owned_pods,
    pod_status,
    terminate_pod,
)
from plato.gpu.profiles import PodImage, profile_named
from plato.gpu.providers import GpuProvider, provider_for
from plato.gpu.registry import PullCredential, pull_credential
from plato.gpu.render import RenderOutcome, StatusSink, render_blend
from plato.gpu.settings import GpuSettings
from plato.gpu.storage import ObjectStore, S3Store

# A pod's bootstrap installs a desktop, the GPU driver bits and the game
# before its MCP server answers: minutes, not seconds.
POD_READY_TIMEOUT_SECONDS = 20 * 60
POD_READY_POLL_SECONDS = 10


class GpuUnavailable(RuntimeError):
    """These settings allow no such work; the message says what is missing."""


class GpuClient:
    """Renders and pods for one ``owner`` (a world id, a person's handle):
    pods are named and keyed by it, so one owner never sees another's.

    ``provider`` and ``store`` default to what ``settings`` names; tests pass
    fakes."""

    def __init__(
        self,
        settings: GpuSettings,
        *,
        owner: str,
        provider: GpuProvider | None = None,
        store: ObjectStore | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        clock: Callable[[], float] = time.time,
        client_factory: Callable[[], httpx.AsyncClient] | None = None,
        pull_credential: PullCredential = pull_credential,
    ) -> None:
        if not owner or "/" in owner or " " in owner or OWNER_END in owner:
            raise ValueError(f"owner must be a single plain token without {OWNER_END!r} (a world id, a handle)")
        self.settings = settings
        self.owner = owner
        self._provider = provider
        self._store = store
        self._sleep = sleep
        self._clock = clock
        # The HTTP client the bucket is reached with (uploads, polls, downloads).
        self._client_factory = client_factory or (lambda: httpx.AsyncClient(timeout=30))
        # Mints a pod's pull credential for a private image (ECR); tests stub it.
        self._pull_credential = pull_credential

    @property
    def provider(self) -> GpuProvider:
        if self._provider is None:
            self._provider = provider_for(self.settings)
        return self._provider

    @property
    def store(self) -> ObjectStore:
        if self._store is None:
            self._store = S3Store(self.settings)
        return self._store

    # Renders

    async def render(self, blend: bytes, *, frames: str = "all", on_status: StatusSink | None = None) -> RenderOutcome:
        if not self.settings.renders_configured:
            raise GpuUnavailable(
                "GPU renders are not configured: a bucket, a provider key and a render endpoint are needed"
            )

        async def quiet(_: str) -> None:
            return None

        return await render_blend(
            self.provider,
            self.store,
            owner=self.owner,
            blend=blend,
            frames=frames,
            on_status=on_status or quiet,
            sleep=self._sleep,
            clock=self._clock,
            client_factory=self._client_factory,
        )

    # Pods

    def _require_pods(self) -> None:
        if not self.settings.pods_configured:
            raise GpuUnavailable("GPU pods are not configured: a bucket and a provider key are needed")
        if not self.settings.pods_allowed:
            raise GpuUnavailable("GPU pods are not allowed for this owner; an admin grants them")

    async def create_pod(
        self, image: str | PodImage, options: dict[str, str] | None = None, *, env: dict[str, str] | None = None
    ) -> PodSession:
        """Boot a pod: a named preset (``str``) or an image the caller holds
        (an artifact's ``gpu_pod``). ``env`` is the caller's own environment
        for the image's command; a ``PLATO_MCP_TOKEN`` in it is kept."""

        self._require_pods()
        profile_name = image if isinstance(image, str) else None
        pod_image = profile_named(image) if isinstance(image, str) else image
        return await create_pod(
            self.provider,
            self.store,
            owner=self.owner,
            image=pod_image,
            options=options or {},
            idle_minutes=self.settings.pod_idle_minutes,
            profile_name=profile_name,
            env=env,
            pull=await self._pull_credential(pod_image.image, self.settings),
        )

    async def pod_status(self, pod_id: str, *, image: PodImage | None = None) -> PodView:
        """``image`` is what the pod runs, for its ports; None assumes the defaults."""
        self._require_pods()
        ports = image or PodImage(image="-", command=["-"])
        return await pod_status(
            self.provider,
            self.store,
            owner=self.owner,
            pod_id=pod_id,
            mcp_port=ports.mcp_port,
            desktop_port=ports.desktop_port,
            client_factory=self._client_factory,
        )

    async def wait_pod_ready(
        self, pod_id: str, *, image: PodImage | None = None, timeout: float = POD_READY_TIMEOUT_SECONDS
    ) -> PodView:
        """The pod once its MCP server answers; a pod that vanishes or never
        answers in time raises :class:`GpuUnavailable`."""

        deadline = self._clock() + timeout
        while True:
            view = await self.pod_status(pod_id, image=image)
            if view.status == PodStatus.READY:
                return view
            if view.status == PodStatus.GONE:
                raise GpuUnavailable(f"pod {pod_id} ended before it was ready (out of GPUs, or its command failed)")
            if self._clock() > deadline:
                raise GpuUnavailable(f"pod {pod_id} did not answer within {int(timeout)} s")
            await self._sleep(POD_READY_POLL_SECONDS)

    async def terminate_pod(self, pod_id: str, *, image: PodImage | None = None) -> PodView:
        self._require_pods()
        ports = image or PodImage(image="-", command=["-"])
        return await terminate_pod(
            self.provider,
            self.store,
            owner=self.owner,
            pod_id=pod_id,
            mcp_port=ports.mcp_port,
            desktop_port=ports.desktop_port,
        )

    async def pods(self) -> list[PodView]:
        self._require_pods()
        return await owned_pods(self.provider, owner=self.owner)
