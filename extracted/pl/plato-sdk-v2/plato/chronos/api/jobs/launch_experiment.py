"""Launch Experiment"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LaunchExperimentRequest, LaunchExperimentResponse


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
) -> LaunchExperimentResponse:
    """Launch sessions from an experiment version.

    If the experiment version is linked to a dataset, ``${column_name}``
    placeholders in the world config are substituted with each row's values
    and one session is launched per selected row. When no dataset is linked
    a single session is launched with no substitution.

    The sessions are automatically linked to the experiment version."""

    request_args = _build_request_args(
        version_public_id=version_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LaunchExperimentResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    version_public_id: str,
    body: LaunchExperimentRequest,
    x_api_key: str | None = None,
) -> LaunchExperimentResponse:
    """Launch sessions from an experiment version.

    If the experiment version is linked to a dataset, ``${column_name}``
    placeholders in the world config are substituted with each row's values
    and one session is launched per selected row. When no dataset is linked
    a single session is launched with no substitution.

    The sessions are automatically linked to the experiment version."""

    request_args = _build_request_args(
        version_public_id=version_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LaunchExperimentResponse.model_validate(response.json())
