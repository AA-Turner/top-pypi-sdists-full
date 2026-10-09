"""Render one ``.blend`` on a serverless GPU worker.

The flow:

1. The scene goes to the bucket under ``<owner>/renders/<job>/scene.blend``
   through a presigned PUT (the client is not a file server either way).
2. The job goes to the provider with a GET for the scene, PUTs for a started
   marker, the frames tar and a result JSON, and a start deadline: the
   endpoint is shared, so a job can wait in its queue behind others, and a
   worker that picks it up too late refuses it instead of rendering.
3. The client polls the bucket: the started marker says a worker has the job
   (until then it is queued), the result JSON says how it ended.

Nothing keeps job state: a job is its prefix in the bucket, and the bucket's
lifecycle rule expires it. Every grant is one object, one verb, hours at most.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import httpx
from pydantic import BaseModel, Field

from plato.gpu.providers.base import GpuProvider, RenderJobInput
from plato.gpu.storage import ObjectStore

# The scene is uploaded right after signing.
UPLOAD_URL_TTL_SECONDS = 15 * 60
# A worker must pick a job up within this of submission, or refuse it.
START_DEADLINE_SECONDS = 60 * 60
# The render's grants must outlive the start deadline plus a render (the
# endpoint's execution cap is 30 min), and the caller polls that long.
RENDER_URL_TTL_SECONDS = 2 * 3600
RESULT_POLL_SECONDS = 5.0
# Once a worker starts a render, the endpoint caps it at 30 min; past this
# the worker is gone and will never write its result.
RESULT_WAIT_SECONDS = 35 * 60
# A worker refuses a job it picks up after its start_by, writing that as the
# result; past this margin no worker took the job at all.
START_MARGIN_SECONDS = 5 * 60
# Scenes with packed textures run to hundreds of MB.
TRANSFER_TIMEOUT_SECONDS = 300
# The caller holds a scene, and then a frames tar, in memory while it moves
# them; past this a transfer is refused, not attempted.
MAX_TRANSFER_BYTES = 2 * 1024**3

StatusSink = Callable[[str], Awaitable[None]]


class RenderFailed(RuntimeError):
    """The render did not produce frames; the message says why."""


class RenderResult(BaseModel):
    """What the worker writes to ``result_url`` when a render ends, whether
    or not Blender succeeded."""

    exit_code: int = Field(description="Blender's exit code; -1 when it never ran")
    render_seconds: float
    frames: list[str]
    log_tail: str
    error: str | None = Field(default=None, description="Why the worker failed, if it did")


@dataclass(frozen=True)
class RenderOutcome:
    """A finished render: the frames tar as the worker wrote it (flat regular
    files), the worker's result, and a one-line summary."""

    archive: bytes
    result: RenderResult
    provider_job_id: str

    @property
    def summary(self) -> str:
        return f"render {self.result.render_seconds:.0f}s, {len(self.result.frames)} frames"


async def render_blend(
    provider: GpuProvider,
    store: ObjectStore,
    *,
    owner: str,
    blend: bytes,
    frames: str,
    on_status: StatusSink,
    client_factory: Callable[[], httpx.AsyncClient] = lambda: httpx.AsyncClient(timeout=30),
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    clock: Callable[[], float] = time.time,
) -> RenderOutcome:
    """Upload, submit, wait, fetch. ``frames`` is Blender's ``-f`` syntax
    or ``all`` for the range saved in the file; ``on_status`` hears each
    step. Raises :class:`RenderFailed`."""

    if len(blend) > MAX_TRANSFER_BYTES:
        raise RenderFailed(f"the scene exceeds {MAX_TRANSFER_BYTES // 1024**2} MiB")
    job_id = uuid.uuid4().hex
    prefix = f"{owner}/renders/{job_id}"
    scene_key = f"{prefix}/scene.blend"
    frames_key = f"{prefix}/frames.tar"
    started_key = f"{prefix}/started.json"
    result_key = f"{prefix}/result.json"
    async with client_factory() as client:
        await on_status("uploading")
        upload = await client.put(
            store.presign_put(scene_key, UPLOAD_URL_TTL_SECONDS), content=blend, timeout=TRANSFER_TIMEOUT_SECONDS
        )
        upload.raise_for_status()
        start_by = clock() + START_DEADLINE_SECONDS
        provider_job_id = await provider.submit_render(
            RenderJobInput(
                blend_url=store.presign_get(scene_key, RENDER_URL_TTL_SECONDS),
                output_url=store.presign_put(frames_key, RENDER_URL_TTL_SECONDS, content_type="application/x-tar"),
                started_url=store.presign_put(started_key, RENDER_URL_TTL_SECONDS, content_type="application/json"),
                result_url=store.presign_put(result_key, RENDER_URL_TTL_SECONDS, content_type="application/json"),
                frames=frames,
                start_by=start_by,
                gpu_job_id=job_id,
            )
        )
        await on_status(f"queued for a GPU (job {provider_job_id})")
        started_url = store.presign_get(started_key, RENDER_URL_TTL_SECONDS)
        result_url = store.presign_get(result_key, RENDER_URL_TTL_SECONDS)
        deadline = start_by + START_MARGIN_SECONDS
        started = False
        while True:
            body = await _fetch(client, result_url)
            if body is not None:
                result = RenderResult.model_validate_json(body)
                break
            if not started and await _fetch(client, started_url) is not None:
                started = True
                await on_status(f"rendering on the GPU (job {provider_job_id})")
                deadline = clock() + RESULT_WAIT_SECONDS
            if clock() > deadline:
                raise RenderFailed(
                    "the render never finished; the GPU worker is gone"
                    if started
                    else "no GPU worker started the render before its deadline; try again"
                )
            await sleep(RESULT_POLL_SECONDS)
        if result.error:
            raise RenderFailed(result.error)
        if result.exit_code != 0:
            raise RenderFailed(f"Blender exited {result.exit_code}:\n{result.log_tail}")
        archive = await _download(client, store.presign_get(frames_key, RENDER_URL_TTL_SECONDS))
    return RenderOutcome(archive=archive, result=result, provider_job_id=provider_job_id)


async def _fetch(client: httpx.AsyncClient, url: str) -> bytes | None:
    """The object at ``url``, or None while it does not exist (404: the
    signer may list the bucket). Anything else, an expired link's 403
    included, raises."""
    response = await client.get(url)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.content


async def _download(client: httpx.AsyncClient, url: str) -> bytes:
    """The body of ``url``, refused past MAX_TRANSFER_BYTES rather than read
    into memory whatever its size."""
    chunks: list[bytes] = []
    size = 0
    async with client.stream("GET", url, timeout=TRANSFER_TIMEOUT_SECONDS) as response:
        response.raise_for_status()
        async for chunk in response.aiter_bytes():
            size += len(chunk)
            if size > MAX_TRANSFER_BYTES:
                raise RenderFailed(f"the rendered frames exceed {MAX_TRANSFER_BYTES // 1024**2} MiB")
            chunks.append(chunk)
    return b"".join(chunks)
