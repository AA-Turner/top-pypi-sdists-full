# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the gemini platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GeminiSearchInput(TypedDict, total=False):
    """Input for Gemini Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    prompt: Required[str]
    """Question or research prompt for Gemini to answer using web search."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GeminiSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    answer: str = Field(
        description="The web-grounded answer as text. Populated whenever the provider has data for the entity."
    )
    answer_markdown: str = Field(
        alias="answerMarkdown",
        description="The answer in Markdown when the engine returns a Markdown rendering, otherwise the same text as answer. Populated whenever the provider has data for the entity.",
    )
    citations: list[GeminiSearchCitation] = Field(
        description="Sources cited by the answer. Populated whenever the provider has data for the entity."
    )
    prompt: str = Field(description="The prompt answered by Gemini.")


class GeminiSearchCitation(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str = Field(
        description="Source page title when supplied by the search engine."
    )
    url: str = Field(description="Source page URL.")


class GeminiNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GeminiSearchInput],
    ) -> RunResult[GeminiSearchData]:
        """Gemini Search

        Ask Gemini a web-grounded question and receive an answer with source
        citations.

        Price: $0.002 per request.

        Example:
            res = client.gemini.search(prompt="What is AnyAPI at getanyapi.com, and what does it offer?")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "gemini.search", dict(input), options
        )
        return RunResult[GeminiSearchData].model_validate(raw)


class AsyncGeminiNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GeminiSearchInput],
    ) -> RunResult[GeminiSearchData]:
        """Gemini Search

        Ask Gemini a web-grounded question and receive an answer with source
        citations.

        Price: $0.002 per request.

        Example:
            res = client.gemini.search(prompt="What is AnyAPI at getanyapi.com, and what does it offer?")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "gemini.search", dict(input), options
        )
        return RunResult[GeminiSearchData].model_validate(raw)
