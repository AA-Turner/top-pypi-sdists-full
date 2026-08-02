"""Builtin web_search tool for the Vibe SDK."""

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.builtins.web_search.types import (
    WebSearchArgs,
    WebSearchContext,
    WebSearchResult,
)


@tool(
    name="web_search",
    description="Search the web for current information.",
    input_schema=WebSearchArgs,
    ctx_schema=WebSearchContext,
    ctx={
        "api_key_env_var": "MISTRAL_API_KEY",
        "provider": "mistral",
        "model": "mistral-vibe-cli-with-tools",
        "timeout_seconds": 120,
        "server_url": "https://api.mistral.ai",
    },
)
async def web_search(ctx: WebSearchContext, args: WebSearchArgs) -> WebSearchResult:
    if ctx.provider == "mistral":
        from mistralai.vibe.sdk.capabilities.builtins.web_search.mistral_gateway import (
            MistralWebSearchGateway,
        )

        return await MistralWebSearchGateway().search(args=args, context=ctx)
    raise ValueError(f"Unsupported web_search provider: {ctx.provider}")
