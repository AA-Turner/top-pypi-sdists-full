"""
Web search tools for ToolUniverse using DDGS (Dux Distributed Global Search).

This module provides web search capabilities using the ddgs library,
which supports multiple search engines including DuckDuckGo, Google, Bing, etc.
"""

import time
from typing import Dict, Any, List
from ddgs import DDGS
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("WebSearchTool")
class WebSearchTool(BaseTool):
    """
    Web search tool using DDGS library.

    This tool performs web searches using the DDGS library which supports
    multiple search engines including Google, Bing, Brave, Yahoo, DuckDuckGo, etc.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        # DDGS instance will be created per request to avoid session issues

    def _search_with_ddgs(
        self,
        query: str,
        max_results: int = 10,
        backend: str = "auto",
        region: str = "us-en",
        safesearch: str = "moderate",
    ) -> List[Dict[str, Any]]:
        """
        Perform a web search using DDGS library and return formatted results.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            backend: Search engine backend (auto, google, bing, brave, etc.)
            region: Search region (e.g., 'us-en', 'cn-zh')
            safesearch: Safe search level ('on', 'moderate', 'off')

        Returns:
            List of search results with title, url, and snippet
        """
        try:
            # Create DDGS instance
            ddgs = DDGS()

            # Perform search using DDGS
            search_results = list(
                ddgs.text(
                    query=query,
                    max_results=max_results,
                    backend=backend,
                    region=region,
                    safesearch=safesearch,
                )
            )

            # Convert DDGS results to our expected format
            results = []
            for i, result in enumerate(search_results):
                results.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                        "rank": i + 1,
                    }
                )

            return results

        except Exception as e:
            return [
                {
                    "title": "Search Error",
                    "url": "",
                    "snippet": f"Failed to perform search: {str(e)}",
                    "rank": 0,
                }
            ]

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute web search using DDGS.

        Args:
            arguments: Dictionary containing:
                - query: Search query string
                - max_results: Maximum number of results (default: 10)
                - search_type: Type of search (default: 'general')
                - backend: Search engine backend (default: 'auto')
                - region: Search region (default: 'us-en')
                - safesearch: Safe search level (default: 'moderate')

        Returns:
            Dictionary containing search results
        """
        try:
            query = arguments.get("query", "").strip()
            max_results = int(arguments.get("max_results", 10))
            search_type = arguments.get("search_type", "general")
            backend = arguments.get("backend", "auto")
            region = arguments.get("region", "us-en")
            safesearch = arguments.get("safesearch", "moderate")

            if not query:
                return {
                    "status": "error",
                    "error": "Query parameter is required",
                    "results": [],
                }

            # Validate max_results
            max_results = max(1, min(max_results, 50))  # Limit between 1-50

            # Modify query based on search type
            if search_type == "api_documentation":
                query = f"{query} API documentation python library"
            elif search_type == "python_packages":
                query = f"{query} python package pypi"
            elif search_type == "github":
                query = f"{query} site:github.com"

            # Perform search using DDGS
            results = self._search_with_ddgs(
                query=query,
                max_results=max_results,
                backend=backend,
                region=region,
                safesearch=safesearch,
            )

            # Add rate limiting to be respectful
            time.sleep(0.5)

            return {
                "status": "success",
                "query": query,
                "search_type": search_type,
                "total_results": len(results),
                "results": results,
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "results": []}


@register_tool("WebAPIDocumentationSearchTool")
class WebAPIDocumentationSearchTool(WebSearchTool):
    """
    Specialized web search tool for API documentation and Python libraries.

    This tool is optimized for finding API documentation, Python packages,
    and technical resources using DDGS with multiple search engines.
    """

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute API documentation focused search.

        Args:
            arguments: Dictionary containing:
                - query: Search query string
                - max_results: Maximum number of results (default: 10)
                - focus: Focus area ('api_docs', 'python_packages', etc.)
                - backend: Search engine backend (default: 'auto')

        Returns:
            Dictionary containing search results
        """
        try:
            query = arguments.get("query", "").strip()
            focus = arguments.get("focus", "api_docs")
            backend = arguments.get("backend", "auto")

            if not query:
                return {
                    "status": "error",
                    "error": "Query parameter is required",
                    "results": [],
                }

            # Modify query based on focus
            if focus == "api_docs":
                enhanced_query = f'"{query}" API documentation official docs'
            elif focus == "python_packages":
                enhanced_query = f'"{query}" python package pypi install pip'
            elif focus == "github_repos":
                enhanced_query = f'"{query}" github repository source code'
            else:
                enhanced_query = f'"{query}" documentation API reference'

            # Use parent class search with enhanced query
            arguments["query"] = enhanced_query
            arguments["search_type"] = "api_documentation"
            arguments["backend"] = backend

            result = super().run(arguments)

            # Add focus-specific metadata
            if result["status"] == "success":
                result["focus"] = focus
                result["enhanced_query"] = enhanced_query

                # Filter results for better relevance
                if focus == "python_packages":
                    result["results"] = [
                        r
                        for r in result["results"]
                        if (
                            "pypi.org" in r.get("url", "")
                            or "python" in r.get("title", "").lower()
                        )
                    ]
                elif focus == "github_repos":
                    result["results"] = [
                        r for r in result["results"] if "github.com" in r.get("url", "")
                    ]

            return result

        except Exception as e:
            return {"status": "error", "error": str(e), "results": []}
