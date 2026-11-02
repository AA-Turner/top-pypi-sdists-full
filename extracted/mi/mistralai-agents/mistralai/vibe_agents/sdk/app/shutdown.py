from __future__ import annotations

import httpx
from pydantic import BaseModel, ConfigDict

from mistralai.vibe_agents.agents_client import AgentsClient

from . import config


class ShutdownError(Exception):
    pass


class ShutdownResult(BaseModel):
    """What was shut down, so the caller can describe the consequence accurately.

    ``managed`` separates the two outcomes: a deployed agent loses the deployment the
    control plane built for it, while a self-hosted worker only loses its binding and
    keeps running until its operator stops the process.
    """

    model_config = ConfigDict(frozen=True)

    agent_name: str
    deployment_name: str
    managed: bool


async def shutdown(agent_name: str) -> ShutdownResult:
    """Shut the named agent down with the environment's control plane and API key. Not reversible."""
    try:
        settings = config.load_deploy_settings()
    except config.SettingsError as exc:
        raise ShutdownError(str(exc)) from exc
    return await shutdown_agent(
        agent_name=agent_name, api_key=settings.api_key, server_url=settings.deploy_control_plane_url
    )


async def shutdown_agent(*, agent_name: str, api_key: str, server_url: str) -> ShutdownResult:
    """Resolve the agent by name, then shut it down. Not reversible.

    The name is the handle a human types; the control plane keys shutdown on the agent
    id, which changes with every deploy. Both calls share one client so the lookup and
    the shutdown cannot disagree about which host they reached.
    """
    async with AgentsClient(base_url=server_url, api_key=api_key) as client:
        try:
            agent = await client.get_agent_by_name(agent_name)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == httpx.codes.NOT_FOUND:
                raise ShutdownError(f"No agent named {agent_name} in this workspace.") from exc
            raise ShutdownError(_status_message(exc, agent_name)) from exc
        except httpx.HTTPError as exc:
            raise ShutdownError(f"Failed to look up agent {agent_name}: {exc}") from exc

        if agent.source == "builtin":
            raise ShutdownError(f"Agent {agent_name} is a built-in agent and cannot be shut down.")

        try:
            await client.shutdown_agent(agent.agent_id)
        except httpx.HTTPStatusError as exc:
            # A 404 here means something shut the agent down between the lookup and this
            # call. Report it rather than claim credit for work another caller did.
            if exc.response.status_code == httpx.codes.NOT_FOUND:
                raise ShutdownError(f"Agent {agent_name} was already shut down.") from exc
            raise ShutdownError(_status_message(exc, agent_name)) from exc
        except httpx.HTTPError as exc:
            raise ShutdownError(f"Failed to shut down agent {agent_name}: {exc}") from exc

    return ShutdownResult(
        agent_name=agent.agent_name,
        deployment_name=agent.deployment_name,
        managed=agent.managed,
    )


def _status_message(exc: httpx.HTTPStatusError, agent_name: str) -> str:
    # The control plane owns the reason, so surface its detail instead of restating it here.
    detail = exc.response.text.strip()
    message = f"Failed to shut down agent {agent_name} (HTTP {exc.response.status_code})"
    return f"{message}: {detail}" if detail else message
