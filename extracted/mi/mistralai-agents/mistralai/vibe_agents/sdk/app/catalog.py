"""The agents a workspace has, for `agents list`."""

from __future__ import annotations

import json

import httpx
from pydantic import ValidationError

from mistralai.vibe_agents.agents_client import AgentsClient
from mistralai.vibe_agents.agents_client.api_models import AgentResponse

from . import config

_PAGE_SIZE = 200


class CatalogError(Exception):
    pass


async def list_workspace_agents_from_env() -> list[AgentResponse]:
    """This workspace's agents, served or managed, with the environment's control plane and API key."""
    try:
        settings = config.load_control_plane_settings()
    except config.SettingsError as exc:
        raise CatalogError(str(exc)) from exc
    return await list_workspace_agents(api_key=settings.api_key, server_url=settings.deploy_control_plane_url)


async def list_workspace_agents(
    *, api_key: str, server_url: str, transport: httpx.AsyncBaseTransport | None = None
) -> list[AgentResponse]:
    """Every page of the workspace's own agents, in name order. Built-ins and other kinds are left out."""
    agents: list[AgentResponse] = []
    cursor: str | None = None
    async with AgentsClient(base_url=server_url, api_key=api_key, transport=transport) as client:
        while True:
            try:
                page = await client.list_agents(limit=_PAGE_SIZE, cursor=cursor)
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text.strip()
                message = f"Failed to list agents (HTTP {exc.response.status_code})"
                raise CatalogError(f"{message}: {detail}" if detail else message) from exc
            # A 200 whose body is not JSON raises JSONDecodeError, a ValueError, from response.json().
            except (httpx.HTTPError, ValidationError, json.JSONDecodeError) as exc:
                raise CatalogError(f"Failed to list agents: {exc}") from exc
            # Only the workspace's own agents: built-ins, and any kind a newer control plane adds, are not served
            # or deployed from here.
            agents.extend(agent for agent in page.items if agent.source == "workspace")
            if page.next_cursor is None:
                return agents
            cursor = page.next_cursor
