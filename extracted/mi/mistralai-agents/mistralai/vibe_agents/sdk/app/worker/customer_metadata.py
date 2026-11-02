"""Read current ZDR headers from Albe before a Workflow model completion."""

from datetime import timedelta
from http import HTTPStatus

import httpx
from pydantic import BaseModel, StrictBool

import mistralai.workflows as workflows
from mistralai.vibe_agents.sdk.app import config


@workflows.activity(retry_policy_max_attempts=3, start_to_close_timeout=timedelta(seconds=10))
async def fetch_customer_no_log_headers(customer_id: str) -> dict[str, str]:
    settings = config.get_app_settings()
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(
            f"{settings.albe_api_url.rstrip('/')}/internal/customer-metadata/{customer_id}",
            headers={"x-internal-service": settings.albe_internal_service_name},
        )
    if response.status_code == HTTPStatus.NOT_FOUND:
        return {}
    response.raise_for_status()
    metadata = _CustomerMetadata.model_validate(response.json())
    return {"x-internal-org-is-no-log": str(metadata.no_log).lower()} if metadata.no_log is not None else {}


class _CustomerMetadata(BaseModel):
    # Albe's CustomerMetadata.from_db_entry forwards its nullable Boolean no_log column.
    no_log: StrictBool | None = None
