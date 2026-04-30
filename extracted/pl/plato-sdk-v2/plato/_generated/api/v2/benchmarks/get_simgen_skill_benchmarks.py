"""Get Simgen Skill Benchmarks"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/benchmarks/simgen-skills"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Aggregate pass/fail data for simgen-generated simulators, grouped by skill.

    Identifies skill-gym sims primarily via ``config.is_skill_gym == true``,
    falling back to the legacy ``[skill: ...]`` description convention for
    older sims. Excludes sims whose ``config.status`` is out-of-service."""

    request_args = _build_request_args(
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Aggregate pass/fail data for simgen-generated simulators, grouped by skill.

    Identifies skill-gym sims primarily via ``config.is_skill_gym == true``,
    falling back to the legacy ``[skill: ...]`` description convention for
    older sims. Excludes sims whose ``config.status`` is out-of-service."""

    request_args = _build_request_args(
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
