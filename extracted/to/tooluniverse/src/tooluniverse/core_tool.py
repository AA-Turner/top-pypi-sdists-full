#!/usr/bin/env python3
"""
CORE API Tool for searching open access academic papers.

CORE is the world's largest collection of open access research papers.
This tool provides access to over 200 million open access papers from
repositories and journals worldwide.
"""

import requests
from typing import Dict, List, Any, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("CoreTool")
class CoreTool(BaseTool):
    """Tool for searching CORE open access academic papers."""

    def __init__(self, tool_config=None):
        super().__init__(tool_config)
        self.base_url = "https://api.core.ac.uk/v3"
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "ToolUniverse/1.0", "Accept": "application/json"}
        )

    def _search(
        self,
        query: str,
        limit: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        language: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for papers using CORE API.

        Args:
            query: Search query
            limit: Maximum number of results
            year_from: Start year filter
            year_to: End year filter
            language: Language filter (e.g., 'en', 'es', 'fr')

        Returns
            List of paper dictionaries
        """
        try:
            # Build search parameters
            params = {
                "q": query,
                "limit": min(limit, 100),  # CORE API max limit is 100
                "page": 1,
            }

            # Add year filters if provided
            if year_from or year_to:
                year_filter = []
                if year_from:
                    year_filter.append(f"year:>={year_from}")
                if year_to:
                    year_filter.append(f"year:<={year_to}")
                params["q"] += f" {' '.join(year_filter)}"

            # Add language filter if provided
            if language:
                params["q"] += f" language:{language}"

            # Make API request
            response = self.session.get(
                f"{self.base_url}/search/works", params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            results = []

            # Parse results
            for item in data.get("results", []):
                paper = {
                    "title": item.get("title", "No title"),
                    "abstract": item.get("abstract", "No abstract available"),
                    "authors": self._extract_authors(item.get("authors", [])),
                    "year": self._extract_year(item.get("publishedDate")),
                    "doi": item.get("doi"),
                    "url": (
                        item.get("downloadUrl") or item.get("links", [{}])[0].get("url")
                    ),
                    "venue": item.get("publisher"),
                    "language": item.get("language", {}).get("code", "Unknown"),
                    "open_access": True,  # CORE only contains open access papers
                    "source": "CORE",
                    "citations": item.get("citationCount", 0),
                    "downloads": item.get("downloadCount", 0),
                }
                results.append(paper)

            return results

        except requests.exceptions.RequestException as e:
            return [{"error": f"CORE API request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"CORE API error: {str(e)}"}]

    def _extract_authors(self, authors: List[Dict]) -> List[str]:
        """Extract author names from CORE API response."""
        if not authors:
            return []

        author_names = []
        for author in authors:
            name = author.get("name", "")
            if name:
                author_names.append(name)

        return author_names

    def _extract_year(self, published_date: str) -> str:
        """Extract year from published date."""
        if not published_date:
            return "Unknown"

        try:
            # CORE API returns dates in ISO format
            return published_date[:4]
        except Exception:
            return "Unknown"

    def run(self, tool_arguments) -> List[Dict[str, Any]]:
        """
        Execute the CORE search.

        Args:
            tool_arguments: Dictionary containing search parameters

        Returns
            List of paper dictionaries
        """
        query = tool_arguments.get("query", "")
        if not query:
            return [{"error": "Query parameter is required"}]

        limit = tool_arguments.get("limit", 10)
        year_from = tool_arguments.get("year_from")
        year_to = tool_arguments.get("year_to")
        language = tool_arguments.get("language")

        return self._search(
            query=query,
            limit=limit,
            year_from=year_from,
            year_to=year_to,
            language=language,
        )
