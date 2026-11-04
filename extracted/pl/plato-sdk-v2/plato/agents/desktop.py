"""World-side lifecycle for an isolated computer-use desktop per agent execution."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from uuid import uuid4

from opentelemetry import trace

from plato._generated.models import SimConfigComputeOverride
from plato.runtimes.config import VMResources
from plato.sims.ubuntu_vm import AsyncClient as DesktopClient
from plato.sims.ubuntu_vm.client import _base_url_from_job_id
from plato.v2 import Env
from plato.v2.async_.environment import Environment
from plato.v2.async_.session import Session

logger = logging.getLogger(__name__)

# Cosmetic only: ownership is tracked by job id on the session, never by alias.
_ALIAS_PREFIX = "agent-desktop-"


@dataclass(frozen=True)
class AgentDesktop:
    job_id: str
    url: str
    env: Environment


async def _wait_for_desktop(url: str, timeout: float) -> None:
    """Probe the actual API the agent harness needs, within a bounded deadline."""
    client = DesktopClient(base_url=url, timeout=15.0)
    try:
        async with asyncio.timeout(timeout):
            await client.wait_for_desktop_ready(timeout=timeout)
    finally:
        await client.close()


async def _remove_created_desktop(creation: asyncio.Task[Environment], session: Session) -> None:
    # Creation is shielded so cancellation cannot lose a successfully allocated
    # job between the backend response and add_env returning its handle.
    try:
        env = await creation
    except Exception:
        return  # Creation failed without returning an environment.
    await session.remove_env(env)
    session.unregister_agent_desktop(env.job_id)
    logger.info("Removed agent desktop %s", env.job_id)


@asynccontextmanager
async def provision_agent_desktop(
    session: Session,
    artifact_id: str,
    *,
    gateway_host: str,
    timeout: int,
    ready_timeout: float = 600,
    resources: VMResources | None = None,
) -> AsyncIterator[AgentDesktop]:
    """Create, attach, and release a desktop, including on failure/cancellation.

    Readiness is separate from creation so the owned job can be removed even
    when its desktop API never becomes healthy. Uses the parent session's mesh;
    never creates or closes a separate session and never removes sibling jobs.
    """
    env_config = Env.artifact(artifact_id, alias=f"{_ALIAS_PREFIX}{uuid4().hex[:12]}")
    if resources is not None:
        env_config.sim_config = SimConfigComputeOverride.model_validate(
            {"cpus": resources.cpus, "memory": resources.memory, "disk": resources.disk}
        )
    creation = asyncio.create_task(
        session.add_env(
            env_config,
            timeout=timeout,
            wait_for_ready=False,
        )
    )

    def _claim(task: asyncio.Task[Environment]) -> None:
        # Record ownership the moment the job exists, so login() and
        # desktop_env never mistake a user's env for this one (or vice versa).
        if not task.cancelled() and task.exception() is None:
            session.register_agent_desktop(task.result().job_id)

    creation.add_done_callback(_claim)
    failed = False
    tracer = trace.get_tracer(__name__)
    try:
        with tracer.start_as_current_span("agent.desktop.provision") as span:
            span.set_attribute("plato.desktop.artifact_id", artifact_id)
            env = await asyncio.shield(creation)
            span.set_attribute("plato.desktop.job_id", env.job_id)
            url = _base_url_from_job_id(env.job_id, gateway_host=gateway_host)
            await _wait_for_desktop(url, min(ready_timeout, timeout))
            await session.connect_network()
            logger.info("Attached agent desktop %s from artifact %s", env.job_id, artifact_id)
        yield AgentDesktop(job_id=env.job_id, url=url, env=env)
    except BaseException:
        failed = True
        raise
    finally:
        cleanup = asyncio.create_task(_remove_created_desktop(creation, session))
        cancelled = False
        try:
            with tracer.start_as_current_span("agent.desktop.cleanup"):
                while not cleanup.done():
                    try:
                        await asyncio.shield(cleanup)
                    except asyncio.CancelledError:
                        cancelled = True
                cleanup.result()
        except Exception:
            if not failed:
                raise
            logger.exception("Failed to remove agent desktop; preserving original execution error")
        if cancelled and not failed:
            raise asyncio.CancelledError
