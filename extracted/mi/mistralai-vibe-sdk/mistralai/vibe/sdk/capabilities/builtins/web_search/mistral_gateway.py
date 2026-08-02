"""Mistral-backed web_search gateway."""

import httpx
from mistralai.client import Mistral
from mistralai.client.errors import SDKError
from mistralai.client.models import (
    ConversationResponse,
    MessageOutputEntry,
    TextChunk,
    ToolReferenceChunk,
)

from mistralai.vibe.sdk.capabilities.builtins.web_search.types import (
    WebSearchArgs,
    WebSearchContext,
    WebSearchResult,
    WebSearchSource,
)
from mistralai.vibe.sdk.capabilities.http import build_ssl_context
from mistralai.vibe.sdk.observability.otel.instrumentation import (
    configure_mistral_client_telemetry,
)

DEFAULT_WEB_SEARCH_INSTRUCTIONS = (
    "Always use the web_search tool to answer queries. Never answer from memory alone."
)


class MistralWebSearchGateway:
    async def search(
        self,
        *,
        args: WebSearchArgs,
        context: WebSearchContext,
    ) -> WebSearchResult:
        api_key = context.resolved_api_key

        try:
            async with httpx.AsyncClient(
                follow_redirects=True,
                headers=context.http_headers or None,
                timeout=httpx.Timeout(context.timeout_seconds),
                verify=build_ssl_context(),
            ) as async_http_client:
                client = configure_mistral_client_telemetry(
                    Mistral(
                        api_key=api_key,
                        server_url=context.server_url,
                        async_client=async_http_client,
                    )
                )
                response = await client.beta.conversations.start_async(
                    model=context.model,
                    instructions=DEFAULT_WEB_SEARCH_INSTRUCTIONS,
                    tools=[{"type": "web_search"}],
                    inputs=args.query,
                    store=False,
                )
        except SDKError as exc:
            raise ValueError(f"Mistral API error: {exc}") from exc

        return self._parse_response(response)

    def _parse_response(self, response: ConversationResponse) -> WebSearchResult:
        text_parts: list[str] = []
        sources: dict[str, WebSearchSource] = {}

        for entry in response.outputs:
            if not isinstance(entry, MessageOutputEntry):
                continue
            for chunk in entry.content:
                if isinstance(chunk, TextChunk):
                    text_parts.append(chunk.text)
                    continue
                if isinstance(chunk, ToolReferenceChunk) and chunk.url and chunk.url not in sources:
                    sources[chunk.url] = WebSearchSource(
                        title=chunk.title or chunk.url,
                        url=chunk.url,
                    )

        answer = "".join(text_parts).strip()
        if not answer:
            raise ValueError("No text in agent response.")

        return WebSearchResult(answer=answer, sources=list(sources.values()))
