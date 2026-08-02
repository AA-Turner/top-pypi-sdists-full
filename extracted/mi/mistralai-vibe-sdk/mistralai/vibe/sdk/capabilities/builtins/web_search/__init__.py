"""Canonical web_search builtin."""

from mistralai.vibe.sdk.capabilities.builtins.web_search.tool import (
    web_search,
)
from mistralai.vibe.sdk.capabilities.builtins.web_search.types import (
    WebSearchArgs,
    WebSearchContext,
    WebSearchGateway,
    WebSearchResult,
    WebSearchSource,
)

__all__ = [
    "WebSearchArgs",
    "WebSearchContext",
    "WebSearchGateway",
    "WebSearchResult",
    "WebSearchSource",
    "web_search",
]
