"""Delete Testcase Set"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    set_id: int,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/testcases/sets/{set_id}"

    return {
        "method": "DELETE",
        "url": url,
    }


def sync(
    client: httpx.Client,
    set_id: int,
) -> Any:
    """Delete Testcase Set"""

    request_args = _build_request_args(
        set_id=set_id,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    set_id: int,
) -> Any:
    """Delete Testcase Set"""

    request_args = _build_request_args(
        set_id=set_id,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
