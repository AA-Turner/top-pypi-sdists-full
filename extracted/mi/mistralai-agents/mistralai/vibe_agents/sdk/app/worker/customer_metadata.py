"""Read a customer's current completion headers from Albe before a Workflow model completion."""

from datetime import timedelta
from http import HTTPStatus
from typing import Final, get_args

import httpx
import structlog
from pydantic import BaseModel, StrictBool

import mistralai.workflows as workflows
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.app import config
from mistralai.vibe_agents.sdk.app.worker import runtime_metrics

logger = structlog.get_logger(__name__)

_ORG_TIERS: Final = frozenset(get_args(wire.OrgTier))


@workflows.activity(retry_policy_max_attempts=3, start_to_close_timeout=timedelta(seconds=10))
async def fetch_customer_completion_headers(customer_id: str) -> dict[str, str]:
    """The customer's ZDR setting and completion gateway band.

    A band the gateway cannot parse is left out, so the request keeps the lowest band it was built
    with: the gateway reads a missing or unknown tier as outranking every banded caller. Each attempt
    records one resolution outcome, so a retried failure counts once per attempt.
    """
    settings = config.get_app_settings()
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(
                f"{settings.albe_api_url.rstrip('/')}/internal/customer-metadata/{customer_id}",
                headers={"x-internal-service": settings.albe_internal_service_name},
            )
        if response.status_code == HTTPStatus.NOT_FOUND:
            runtime_metrics.record_completion_org_tier("missing")
            return {}
        response.raise_for_status()
        metadata = _CustomerMetadata.model_validate(response.json())
    except Exception:
        runtime_metrics.record_completion_org_tier("error")
        raise
    headers: dict[str, str] = {}
    if metadata.no_log is not None:
        headers["x-internal-org-is-no-log"] = str(metadata.no_log).lower()
    if metadata.tier is None:
        runtime_metrics.record_completion_org_tier("missing")
        return headers
    if metadata.tier in _ORG_TIERS:
        headers["x-internal-org-tier"] = metadata.tier
        runtime_metrics.record_completion_org_tier("resolved", metadata.tier)
        return headers
    runtime_metrics.record_completion_org_tier("unknown")
    # OrgTier lags a band Albe added: its customers are scheduled as free.
    logger.warning("customer_org_tier_unknown", customer_id=customer_id, tier=metadata.tier)
    return headers


class _CustomerMetadata(BaseModel):
    # Albe's CustomerMetadata.from_db_entry forwards its nullable Boolean no_log column.
    no_log: StrictBool | None = None
    # Albe's APIKeyTier, which OrgTier restates.
    tier: str | None = None
