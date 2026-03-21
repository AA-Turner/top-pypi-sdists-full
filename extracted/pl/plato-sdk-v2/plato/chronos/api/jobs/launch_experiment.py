"""Launch Experiment"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LaunchExperimentRequest, LaunchJobResponse


def _build_request_args(
    version_public_id: str,
    body: LaunchExperimentRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/jobs/launch-experiment/{version_public_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    version_public_id: str,
    body: LaunchExperimentRequest,
    x_api_key: str | None = None,
) -> LaunchJobResponse:
    """Launch a session from an experiment version.

    This endpoint pulls the full config (including world.runtime) from the
    experiment version's config_json in the database, ensuring no fields are
    dropped. The session is automatically linked to the experiment version."""

    request_args = _build_request_args(
        version_public_id=version_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LaunchJobResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    version_public_id: str,
    body: LaunchExperimentRequest,
    x_api_key: str | None = None,
) -> LaunchJobResponse:
    """Launch a session from an experiment version.

    This endpoint pulls the full config (including world.runtime) from the
    experiment version's config_json in the database, ensuring no fields are
    dropped. The session is automatically linked to the experiment version."""

    request_args = _build_request_args(
        version_public_id=version_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LaunchJobResponse.model_validate(response.json())
