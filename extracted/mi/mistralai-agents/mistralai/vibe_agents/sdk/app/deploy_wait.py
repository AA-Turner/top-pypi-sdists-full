from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import datetime
from time import monotonic
from uuid import UUID

import httpx
from pydantic import BaseModel, ConfigDict

from mistralai.vibe_agents.agents_client import AgentDetailResponse, AgentsClient

from .deploy import DeployError, WorkerStartError

# A just-created agent can 404 against a lagging read replica, and the control plane resolves
# deployment status fail-open, so a transient HTTP error means "not visible yet", not "broken".
# Only a clear client error (auth/permission) is fatal.
_FATAL_STATUS_CODES = frozenset({400, 401, 403})


class DeployProgress(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    is_live: bool
    failure: str | None = None
    # Whether the image build is behind us, so a failure from here on comes from the worker itself.
    build_finished: bool = False

    @classmethod
    def from_status(
        cls, status: AgentDetailResponse, *, revision: str | None = None, requested_at: datetime | None = None
    ) -> DeployProgress:
        build_phase = (status.build_phase or "").casefold()
        if build_phase == "failed" and _is_previous_build(status, revision=revision, requested_at=requested_at):
            build_phase = ""
        rollout_status = (status.rollout_status or "").casefold()
        if build_phase == "failed":
            return cls(label="Build failed", is_live=False, failure=status.build_message or "image build failed")
        if rollout_status == "failed":
            return cls(
                label="Rollout failed",
                is_live=False,
                failure=status.message or "worker rollout failed",
                build_finished=True,
            )
        # A redeploy keeps the previous worker polling, so is_active alone would report the old
        # revision as live. Aeon holds rollout_status at in_progress until the new worker reports back.
        if status.is_active and rollout_status != "in_progress":
            return cls(label="Worker active", is_live=True, build_finished=True)
        if build_phase == "running":
            return cls(label="Building image", is_live=False)
        if build_phase == "succeeded":
            return cls(label="Starting worker", is_live=False, build_finished=True)
        # A reconcile that keeps failing holds rollout_status at in_progress with no build phase, so
        # the wait can only end in a timeout. Show the reason it is stuck rather than "Queued".
        if detail := (status.message or "").strip():
            return cls(label=_shorten(detail), is_live=False, build_finished=build_phase == "succeeded")
        return cls(label="Queued", is_live=False)


def _is_previous_build(status: AgentDetailResponse, *, revision: str | None, requested_at: datetime | None) -> bool:
    if revision is not None and status.build_commit_sha is not None and status.build_commit_sha != revision:
        return True
    return requested_at is not None and status.build_started_at is not None and status.build_started_at < requested_at


def _shorten(message: str, limit: int = 90) -> str:
    collapsed = " ".join(message.split())
    return collapsed if len(collapsed) <= limit else f"{collapsed[: limit - 1]}…"


def format_elapsed(seconds: float) -> str:
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes}m{remainder:02d}s" if minutes else f"{remainder}s"


async def wait_for_deploy(
    *,
    agent_id: UUID,
    api_key: str,
    server_url: str,
    timeout_seconds: float,
    poll_interval_seconds: float,
    on_progress: Callable[[DeployProgress, float], None],
    revision: str | None = None,
    requested_at: datetime | None = None,
) -> float:
    async with AgentsClient(base_url=server_url, api_key=api_key) as client:
        return await wait_until_active(
            client=client,
            agent_id=agent_id,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            on_progress=on_progress,
            revision=revision,
            requested_at=requested_at,
        )


async def wait_until_active(
    *,
    client: AgentsClient,
    agent_id: UUID,
    timeout_seconds: float,
    poll_interval_seconds: float,
    on_progress: Callable[[DeployProgress, float], None],
    revision: str | None = None,
    requested_at: datetime | None = None,
) -> float:
    started_at = monotonic()
    # Sticky: status reads can lag or go blank after the build, but a finished build stays finished.
    build_finished = False
    while True:
        progress = await _poll(client, agent_id, revision=revision, requested_at=requested_at)
        elapsed_seconds = monotonic() - started_at
        if progress is not None:
            on_progress(progress, elapsed_seconds)
            build_finished = build_finished or progress.build_finished
            if progress.failure is not None:
                error = WorkerStartError if build_finished else DeployError
                raise error(f"Deploy failed. {progress.label}: {progress.failure}")
            if progress.is_live:
                return elapsed_seconds
        if elapsed_seconds >= timeout_seconds:
            # A worker that keeps crashing can hold the rollout in progress until we give up.
            error = WorkerStartError if build_finished else DeployError
            raise error(
                f"Gave up after {format_elapsed(elapsed_seconds)}. The agent is still deploying and is not ready yet."
            )
        for _ in range(int(poll_interval_seconds)):
            await asyncio.sleep(1)
            if progress is not None:
                on_progress(progress, monotonic() - started_at)
        remainder = poll_interval_seconds % 1
        if remainder:
            await asyncio.sleep(remainder)


async def _poll(
    client: AgentsClient, agent_id: UUID, *, revision: str | None, requested_at: datetime | None
) -> DeployProgress | None:
    try:
        status = await client.get_agent(agent_id)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in _FATAL_STATUS_CODES:
            raise DeployError(f"Failed to read deployment status (HTTP {exc.response.status_code})") from exc
        return None
    except httpx.HTTPError:
        return None
    return DeployProgress.from_status(status, revision=revision, requested_at=requested_at)
