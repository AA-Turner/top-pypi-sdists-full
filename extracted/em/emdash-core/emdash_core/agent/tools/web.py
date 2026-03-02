"""Web search and fetch tool."""

from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class WebTool(BaseTool):
    """Tool for web search and page fetching."""

    name = "web"
    description = """Search the web or fetch content from a URL.

Use mode 'search' to search the web for information.
Use mode 'fetch' to get content from a specific URL.

Useful for:
- Finding documentation
- Looking up error messages
- Getting latest library information
- Reading external resources"""
    category = ToolCategory.SEARCH

    def execute(
        self,
        mode: str = "search",
        query: Optional[str] = None,
        url: Optional[str] = None,
        max_results: int = 5,
    ) -> ToolResult:
        """Execute web operation.

        Args:
            mode: 'search' or 'fetch'
            query: Search query (for search mode)
            url: URL to fetch (for fetch mode)
            max_results: Max search results

        Returns:
            ToolResult with web content
        """
        if mode == "search":
            if not query:
                return ToolResult.error_result(
                    "Query required for search mode",
                )
            return self._search(query, max_results)
        elif mode == "fetch":
            if not url:
                return ToolResult.error_result(
                    "URL required for fetch mode",
                )
            return self._fetch(url)
        else:
            return ToolResult.error_result(
                f"Unknown mode: {mode}",
                suggestions=["Use mode 'search' or 'fetch'"],
            )

    def _search(self, query: str, max_results: int) -> ToolResult:
        """Perform web search.

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            ToolResult with search results
        """
        try:
            # Try DuckDuckGo search
            from duckduckgo_search import DDGS

            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    })

            return ToolResult.success_result(
                data={
                    "query": query,
                    "results": results,
                    "count": len(results),
                },
            )

        except ImportError:
            return ToolResult.error_result(
                "Web search not available",
                suggestions=["Install duckduckgo-search: pip install duckduckgo-search"],
            )
        except Exception as e:
            log.exception("Web search failed")
            return ToolResult.error_result(f"Search failed: {str(e)}")

    def _fetch(self, url: str) -> ToolResult:
        """Fetch content from URL.

        Args:
            url: URL to fetch

        Returns:
            ToolResult with page content
        """
        try:
            import httpx
            from bs4 import BeautifulSoup

            # Fetch the page
            response = httpx.get(url, timeout=30, follow_redirects=True)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and style elements
            for element in soup(["script", "style", "nav", "header", "footer"]):
                element.decompose()

            # Get text content
            text = soup.get_text(separator="\n", strip=True)

            # Truncate if too long
            if len(text) > 10000:
                text = text[:10000] + "\n\n[Content truncated...]"

            # Get title
            title = ""
            if soup.title:
                title = soup.title.string or ""

            return ToolResult.success_result(
                data={
                    "url": url,
                    "title": title,
                    "content": text,
                    "length": len(text),
                },
            )

        except ImportError:
            return ToolResult.error_result(
                "Web fetch not available",
                suggestions=["Install httpx and beautifulsoup4"],
            )
        except Exception as e:
            log.exception("Web fetch failed")
            return ToolResult.error_result(f"Fetch failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "mode": {
                    "type": "string",
                    "enum": ["search", "fetch"],
                    "description": "Operation mode: 'search' for web search, 'fetch' for URL content",
                },
                "query": {
                    "type": "string",
                    "description": "Search query (required for search mode)",
                },
                "url": {
                    "type": "string",
                    "description": "URL to fetch (required for fetch mode)",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum search results",
                    "default": 5,
                },
            },
            required=["mode"],
        )
