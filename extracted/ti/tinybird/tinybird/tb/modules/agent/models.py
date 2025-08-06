from typing import Optional

from anthropic import AsyncAnthropic
from httpx import AsyncClient, HTTPStatusError
from pydantic_ai.models.anthropic import AnthropicModel, AnthropicModelName
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.retries import AsyncTenacityTransport, wait_retry_after
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential


def create_retrying_client(token: str, workspace_id: str):
    """Create a client with smart retry handling for multiple error types."""

    def should_retry_status(response):
        """Raise exceptions for retryable HTTP status codes."""
        if response.status_code in (400, 429, 502, 503, 504):
            response.raise_for_status()  # This will raise HTTPStatusError

    transport = AsyncTenacityTransport(
        controller=AsyncRetrying(
            # Retry on HTTP errors and connection issues
            retry=retry_if_exception_type((HTTPStatusError, ConnectionError)),
            # Smart waiting: respects Retry-After headers, falls back to exponential backoff
            wait=wait_retry_after(fallback_strategy=wait_exponential(multiplier=1, max=60), max_wait=300),
            # Stop after 5 attempts
            stop=stop_after_attempt(5),
            # Re-raise the last exception if all retries fail
            reraise=True,
        ),
        validate_response=should_retry_status,
    )
    return AsyncClient(transport=transport, params={"token": token, "workspace_id": workspace_id})


def create_model(
    token: str,
    base_url: str,
    workspace_id: str,
    model: AnthropicModelName = "claude-4-sonnet-20250514",
    run_id: Optional[str] = None,
):
    default_headers = {}
    if run_id:
        default_headers["X-Run-Id"] = run_id

    client = AsyncAnthropic(
        base_url=base_url,
        http_client=create_retrying_client(token, workspace_id),
        auth_token=token,
        default_headers=default_headers,
    )
    return AnthropicModel(
        model_name=model,
        provider=AnthropicProvider(anthropic_client=client),
    )


model_costs = {
    "input_cost_per_token": 3e-06,
    "output_cost_per_token": 1.5e-05,
}
