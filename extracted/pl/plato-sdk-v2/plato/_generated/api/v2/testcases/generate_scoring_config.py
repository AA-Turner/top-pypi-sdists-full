"""Generate Scoring Config"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import GenerateScoringConfigRequest, GenerateScoringConfigResponse


def _build_request_args(
    test_case_id: int,
    body: GenerateScoringConfigRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/testcases/{test_case_id}/generate_scoring_config"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    test_case_id: int,
    body: GenerateScoringConfigRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> GenerateScoringConfigResponse:
    """Generate V2 multi-sim scoring config for a test case.

    Collects scored sessions, generates per-simulator mutation configs via LLM,
    and stores the result in test_case.v2_scoring_config.

    Optionally accepts:
    - session_ids: specific sessions to use (otherwise uses all scored sessions)
    - ignore_configs: per-simulator table/column ignore overrides
      (otherwise derived from SimulatorModel.config + TestCase.mutation_ignore_config)"""

    request_args = _build_request_args(
        test_case_id=test_case_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return GenerateScoringConfigResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    test_case_id: int,
    body: GenerateScoringConfigRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> GenerateScoringConfigResponse:
    """Generate V2 multi-sim scoring config for a test case.

    Collects scored sessions, generates per-simulator mutation configs via LLM,
    and stores the result in test_case.v2_scoring_config.

    Optionally accepts:
    - session_ids: specific sessions to use (otherwise uses all scored sessions)
    - ignore_configs: per-simulator table/column ignore overrides
      (otherwise derived from SimulatorModel.config + TestCase.mutation_ignore_config)"""

    request_args = _build_request_args(
        test_case_id=test_case_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return GenerateScoringConfigResponse.model_validate(response.json())
