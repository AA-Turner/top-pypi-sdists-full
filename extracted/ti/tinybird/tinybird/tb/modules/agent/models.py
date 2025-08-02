from typing import Optional

from anthropic import AsyncAnthropic
from httpx import AsyncClient
from pydantic_ai.models.anthropic import AnthropicModel, AnthropicModelName
from pydantic_ai.providers.anthropic import AnthropicProvider


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
        http_client=AsyncClient(params={"token": token, "workspace_id": workspace_id}),
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
