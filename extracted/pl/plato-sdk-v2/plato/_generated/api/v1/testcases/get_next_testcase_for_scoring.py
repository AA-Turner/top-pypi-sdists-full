"""Get Next Testcase For Scoring"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    scoring_type: str,
    exclude_test_case_id: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/testcases/next-for-scoring"

    params: dict[str, Any] = {}
    if scoring_type is not None:
        params["scoring_type"] = scoring_type
    if exclude_test_case_id is not None:
        params["exclude_test_case_id"] = exclude_test_case_id

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    scoring_type: str,
    exclude_test_case_id: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get the next test case that needs scoring for the current annotator.
    Returns test cases in NEEDS_SCORING stage with the specified scoring_type.
    Excludes test cases where the user has already scored or created sessions.
    Optionally excludes a specific test case (e.g., the current one).

    Ordering: Prioritizes test cases with higher average scores per session (closer to completion).
    Selection: Random from batch of 50 eligible test cases."""

    request_args = _build_request_args(
        scoring_type=scoring_type,
        exclude_test_case_id=exclude_test_case_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    scoring_type: str,
    exclude_test_case_id: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get the next test case that needs scoring for the current annotator.
    Returns test cases in NEEDS_SCORING stage with the specified scoring_type.
    Excludes test cases where the user has already scored or created sessions.
    Optionally excludes a specific test case (e.g., the current one).

    Ordering: Prioritizes test cases with higher average scores per session (closer to completion).
    Selection: Random from batch of 50 eligible test cases."""

    request_args = _build_request_args(
        scoring_type=scoring_type,
        exclude_test_case_id=exclude_test_case_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
