"""Get Public Benchmark Sessions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    simulator_name: str,
    agent_artifact_ids: str | None = None,
    include_replays: bool | None = False,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/session/public/benchmarks/{simulator_name}"

    params: dict[str, Any] = {}
    if agent_artifact_ids is not None:
        params["agentArtifactIds"] = agent_artifact_ids
    if include_replays is not None:
        params["includeReplays"] = include_replays

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    simulator_name: str,
    agent_artifact_ids: str | None = None,
    include_replays: bool | None = False,
) -> Any:
    """Public endpoint to fetch benchmark sessions for a simulator by name.
    - Returns sessions across all orgs (no org/public restriction)
    - Groups results by agent_artifact.data.model
    - Excludes sessions where model is not set"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        agent_artifact_ids=agent_artifact_ids,
        include_replays=include_replays,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
    agent_artifact_ids: str | None = None,
    include_replays: bool | None = False,
) -> Any:
    """Public endpoint to fetch benchmark sessions for a simulator by name.
    - Returns sessions across all orgs (no org/public restriction)
    - Groups results by agent_artifact.data.model
    - Excludes sessions where model is not set"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        agent_artifact_ids=agent_artifact_ids,
        include_replays=include_replays,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
