"""A whole GPU machine for one live session, from an image.

A pod is named ``plato-pod-<owner>--<id>-<slug>``: that name is the ownership
check, since nothing here keeps pod state. The ``--`` ends the owner, which
may not contain it (:class:`plato.gpu.GpuClient` refuses one that does), so
``alice`` can never match ``alice-team``'s pods. The image's start command runs
under the SDK's wrapper (``profiles/wrapper.sh``, shipped in the pod's
environment as ``POD_BOOTSTRAP``), which waits for the command's MCP server,
records the X display, PUTs the recording to a presigned URL on the bucket
(``<owner>/pods/<id>/recording.mp4``) every 5 minutes and when the pod ends,
and ends the pod itself after ``idle_minutes`` without an MCP call, in case
its owner never does.
"""

from __future__ import annotations

import base64
import json
import re
import secrets
import uuid
from collections.abc import Callable
from enum import Enum

import httpx
from pydantic import BaseModel, Field

from plato.gpu.profiles import PodImage, wrapper_script
from plato.gpu.providers.base import GpuProvider, PodSpec, RegistryCredential
from plato.gpu.storage import ObjectStore

NAME_PREFIX = "plato-pod"
# Assets are read at boot; the recording is written when the session ends,
# however long it ran.
ASSET_URL_TTL_SECONDS = 2 * 3600
RECORDING_URL_TTL_SECONDS = 24 * 3600
_SLUG = re.compile(r"[^a-z0-9]+")


class PodStatus(str, Enum):
    STARTING = "starting"
    READY = "ready"
    GONE = "gone"


class PodView(BaseModel):
    """One pod, as status and terminate report it."""

    id: str
    slug: str = Field(description="The profile name or the image's name, from the pod's own name")
    status: PodStatus
    mcp_url: str = Field(description="The pod's MCP endpoint, behind the mcp token")
    desktop_url: str = Field(description="noVNC for people watching, behind the VNC password")
    recording_url: str | None = Field(
        default=None, description="Presigned GET for the session recording, once uploaded"
    )
    cost_per_hour: float | None = None


class PodSession(PodView):
    """A pod just created: the view plus its secrets, returned once. The MCP
    token is the caller's when it brought one (an artifact's account), else
    minted here."""

    mcp_token: str
    admin_token: str
    vnc_password: str


class NotYourPod(PermissionError):
    """The pod belongs to another owner."""


OWNER_END = "--"


def _owner_prefix(owner: str) -> str:
    return f"{NAME_PREFIX}-{owner}{OWNER_END}"


def _parse_name(owner: str, name: str) -> tuple[str, str]:
    """(short id, slug) of a pod of this owner."""
    short_id, _, slug = name.removeprefix(_owner_prefix(owner)).partition("-")
    return short_id, slug


def slug_of(image: PodImage, profile_name: str | None) -> str:
    """What the pod's name says it runs: the profile, else the image's last
    path segment without its tag."""
    raw = profile_name or image.image.rsplit("/", 1)[-1].split(":", 1)[0]
    return _SLUG.sub("-", raw.lower()).strip("-")[:40] or "image"


def recording_key(owner: str, short_id: str) -> str:
    return f"{owner}/pods/{short_id}/recording.mp4"


def _urls(provider: GpuProvider, pod_id: str, mcp_port: int, desktop_port: int) -> tuple[str, str]:
    return (
        provider.pod_http_url(pod_id, mcp_port) + "/mcp",
        provider.pod_http_url(pod_id, desktop_port) + "/vnc.html?autoconnect=true&resize=scale",
    )


async def create_pod(
    provider: GpuProvider,
    store: ObjectStore,
    *,
    owner: str,
    image: PodImage,
    options: dict[str, str],
    idle_minutes: int,
    profile_name: str | None = None,
    env: dict[str, str] | None = None,
    pull: RegistryCredential | None = None,
) -> PodSession:
    """Boot ``image`` under the wrapper. ``options`` must be ones the image
    takes; ``env`` is the caller's own (a ``PLATO_MCP_TOKEN`` there is used
    instead of minting one, so an artifact's account keeps working); ``pull``
    is a credential minted for this pod's private image."""

    image.allowed(options)
    short_id = uuid.uuid4().hex[:8]
    given = dict(env or {})
    mcp_token = given.get("PLATO_MCP_TOKEN") or secrets.token_urlsafe(24)
    admin_token = given.get("PLATO_MCP_ADMIN_TOKEN") or secrets.token_urlsafe(24)
    # VNC reads only the first 8 characters of a password.
    vnc_password = secrets.token_urlsafe(6)[:8]
    pod_env = {
        **image.env,
        **options,
        **given,
        "POD_BOOTSTRAP": base64.b64encode(wrapper_script()).decode(),
        "POD_COMMAND": json.dumps(image.command),
        "POD_MCP_PORT": str(image.mcp_port),
        "PLATO_MCP_TOKEN": mcp_token,
        "PLATO_MCP_ADMIN_TOKEN": admin_token,
        "VNC_PASSWORD": vnc_password,
        "IDLE_TERMINATE_MINUTES": str(idle_minutes),
        "RECORDING_URL": store.presign_put(
            recording_key(owner, short_id), RECORDING_URL_TTL_SECONDS, content_type="video/mp4"
        ),
        # A compute-only base image needs the driver's GL libraries for a desktop.
        "NVIDIA_DRIVER_CAPABILITIES": "all",
    }
    for name, key in image.assets.items():
        pod_env[name] = store.presign_get(key, ASSET_URL_TTL_SECONDS)
    slug = slug_of(image, profile_name)
    pod = await provider.create_pod(
        PodSpec(
            name=f"{_owner_prefix(owner)}{short_id}-{slug}",
            image=image.image,
            gpu_type_ids=list(image.gpu_type_ids),
            container_disk_gb=image.container_disk_gb,
            ports=[f"{image.mcp_port}/http", f"{image.desktop_port}/http"],
            env=pod_env,
            entrypoint=[
                "bash",
                "-c",
                'echo "$POD_BOOTSTRAP" | base64 -d > /tmp/wrapper.sh && exec bash /tmp/wrapper.sh',
            ],
            pull=pull,
        )
    )
    mcp_url, desktop_url = _urls(provider, pod.id, image.mcp_port, image.desktop_port)
    return PodSession(
        id=pod.id,
        slug=slug,
        status=PodStatus.STARTING,
        mcp_url=mcp_url,
        desktop_url=desktop_url,
        cost_per_hour=pod.cost_per_hour,
        mcp_token=mcp_token,
        admin_token=admin_token,
        vnc_password=vnc_password,
    )


ClientFactory = Callable[[], httpx.AsyncClient]


def _default_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=10.0)


async def _ready(mcp_url: str, client_factory: ClientFactory = _default_client) -> bool:
    """Whether the command's server is up: its unauthenticated ``/health``.
    The proxy answers 5xx until the wrapper is through."""
    try:
        async with client_factory() as client:
            response = await client.get(mcp_url.removesuffix("/mcp") + "/health", headers={"User-Agent": "plato-gpu"})
    except httpx.RequestError:
        return False
    return response.status_code == 200


def _gone(
    provider: GpuProvider, pod_id: str, mcp_port: int, desktop_port: int, recording_url: str | None = None
) -> PodView:
    mcp_url, desktop_url = _urls(provider, pod_id, mcp_port, desktop_port)
    return PodView(
        id=pod_id,
        slug="",
        status=PodStatus.GONE,
        mcp_url=mcp_url,
        desktop_url=desktop_url,
        recording_url=recording_url,
        cost_per_hour=None,
    )


async def pod_status(
    provider: GpuProvider,
    store: ObjectStore,
    *,
    owner: str,
    pod_id: str,
    mcp_port: int = 8765,
    desktop_port: int = 6080,
    client_factory: ClientFactory = _default_client,
) -> PodView:
    """The pod's state: ``starting`` until its MCP server answers, ``ready``
    after, ``gone`` once ended. Another owner's pod raises."""

    pod = await provider.get_pod(pod_id)
    if pod is None or not pod.running:
        return _gone(provider, pod_id, mcp_port, desktop_port)
    if not pod.name.startswith(_owner_prefix(owner)):
        raise NotYourPod(f"pod {pod_id} is not {owner}'s")
    short_id, slug = _parse_name(owner, pod.name)
    mcp_url, desktop_url = _urls(provider, pod_id, mcp_port, desktop_port)
    return PodView(
        id=pod_id,
        slug=slug,
        status=PodStatus.READY if await _ready(mcp_url, client_factory) else PodStatus.STARTING,
        mcp_url=mcp_url,
        desktop_url=desktop_url,
        recording_url=store.presign_get(recording_key(owner, short_id), RECORDING_URL_TTL_SECONDS),
        cost_per_hour=pod.cost_per_hour,
    )


async def terminate_pod(
    provider: GpuProvider,
    store: ObjectStore,
    *,
    owner: str,
    pod_id: str,
    mcp_port: int = 8765,
    desktop_port: int = 6080,
) -> PodView:
    """Ends the pod and billing. The recording it uploads on the way out is
    at ``recording_url`` once the upload lands."""

    pod = await provider.get_pod(pod_id)
    if pod is None:
        return _gone(provider, pod_id, mcp_port, desktop_port)
    if not pod.name.startswith(_owner_prefix(owner)):
        raise NotYourPod(f"pod {pod_id} is not {owner}'s")
    short_id, _ = _parse_name(owner, pod.name)
    await provider.terminate_pod(pod_id)
    recording = store.presign_get(recording_key(owner, short_id), RECORDING_URL_TTL_SECONDS)
    return _gone(provider, pod_id, mcp_port, desktop_port, recording)


async def owned_pods(provider: GpuProvider, *, owner: str) -> list[PodView]:
    """Every running pod of this owner: what a reaper or a person lists.
    URLs use the ports the provider reports for the pod (MCP first, desktop
    second, as created), the defaults when it reports none."""

    views: list[PodView] = []
    for pod in await provider.list_pods():
        if not pod.running or not pod.name.startswith(_owner_prefix(owner)):
            continue
        _, slug = _parse_name(owner, pod.name)
        mcp_port, desktop_port = (pod.ports[0], pod.ports[1]) if len(pod.ports) >= 2 else (8765, 6080)
        mcp_url, desktop_url = _urls(provider, pod.id, mcp_port, desktop_port)
        views.append(
            PodView(
                id=pod.id,
                slug=slug,
                status=PodStatus.STARTING,
                mcp_url=mcp_url,
                desktop_url=desktop_url,
                cost_per_hour=pod.cost_per_hour,
            )
        )
    return views
