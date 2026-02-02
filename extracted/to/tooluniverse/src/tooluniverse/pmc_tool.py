#!/usr/bin/env python3
"""
PMC (PubMed Central) Tool for searching full-text biomedical literature.

PMC is the free full-text archive of biomedical and life sciences journal
literature at the U.S. National Institutes of Health's National Library of
Medicine. This tool provides access to millions of full-text articles.
"""

import requests
from typing import Dict, List, Any, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("PMCTool")
class PMCTool(BaseTool):
    """Tool for searching PMC full-text biomedical literature."""

    def __init__(self, tool_config=None):
        super().__init__(tool_config)
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "ToolUniverse/1.0", "Accept": "application/json"}
        )

    def _search(
        self,
        query: str,
        limit: int = 10,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        article_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for papers using PMC API.

        Args:
            query: Search query
            limit: Maximum number of results
            date_from: Start date filter (YYYY/MM/DD)
            date_to: End date filter (YYYY/MM/DD)
            article_type: Article type filter (e.g., 'research-article', 'review')

        Returns
            List of paper dictionaries
        """
        try:
            # Step 1: Search PMC for article IDs
            search_params = {
                "db": "pmc",
                "term": query,
                "retmax": min(limit, 100),  # NCBI API max limit
                "retmode": "json",
                "sort": "relevance",
            }

            # Add date filters if provided
            if date_from or date_to:
                date_filter = []
                if date_from:
                    date_filter.append(
                        f"({date_from}[PDAT]:{date_to or '3000/12/31'}[PDAT])"
                    )
                else:
                    date_filter.append(f"(:{date_to}[PDAT])")
                search_params["term"] += f" AND {' '.join(date_filter)}"

            # Add article type filter if provided
            if article_type:
                search_params["term"] += f" AND {article_type}[PT]"

            # Make search request
            search_response = self.session.get(
                f"{self.base_url}/esearch.fcgi", params=search_params, timeout=30
            )
            search_response.raise_for_status()

            search_data = search_response.json()
            pmc_ids = search_data.get("esearchresult", {}).get("idlist", [])

            if not pmc_ids:
                return []

            # Step 2: Get detailed information for each article
            summary_params = {"db": "pmc", "id": ",".join(pmc_ids), "retmode": "json"}

            summary_response = self.session.get(
                f"{self.base_url}/esummary.fcgi", params=summary_params, timeout=30
            )
            summary_response.raise_for_status()

            summary_data = summary_response.json()
            results = []

            # Parse results
            for pmc_id in pmc_ids:
                article_data = summary_data.get("result", {}).get(pmc_id, {})

                paper = {
                    "title": article_data.get("title", "No title"),
                    "abstract": article_data.get("abstract", "No abstract available"),
                    "authors": self._extract_authors(article_data.get("authors", [])),
                    "year": self._extract_year(article_data.get("pubdate")),
                    "pmc_id": pmc_id,
                    "pmid": article_data.get("pmid"),
                    "doi": article_data.get("elocationid"),
                    "url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/",
                    "venue": article_data.get("source"),
                    "open_access": True,  # PMC only contains open access articles
                    "source": "PMC",
                    "article_type": (
                        article_data.get("pubtype", ["Unknown"])[0]
                        if article_data.get("pubtype")
                        else "Unknown"
                    ),
                    "citations": article_data.get("pmcrefcount", 0),
                }
                results.append(paper)

            return results

        except requests.exceptions.RequestException as e:
            return [{"error": f"PMC API request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"PMC API error: {str(e)}"}]

    def _extract_authors(self, authors: List[Dict]) -> List[str]:
        """Extract author names from PMC API response."""
        if not authors:
            return []

        author_names = []
        for author in authors:
            name = author.get("name", "")
            if name:
                author_names.append(name)

        return author_names

    def _extract_year(self, pubdate: str) -> str:
        """Extract year from publication date."""
        if not pubdate:
            return "Unknown"

        try:
            # PMC API returns dates in various formats
            # Extract year from the beginning of the string
            return pubdate[:4]
        except Exception:
            return "Unknown"

    def run(self, tool_arguments) -> List[Dict[str, Any]]:
        """
        Execute the PMC search.

        Args:
            tool_arguments: Dictionary containing search parameters

        Returns
            List of paper dictionaries
        """
        query = tool_arguments.get("query", "")
        if not query:
            return [{"error": "Query parameter is required"}]

        limit = tool_arguments.get("limit", 10)
        date_from = tool_arguments.get("date_from")
        date_to = tool_arguments.get("date_to")
        article_type = tool_arguments.get("article_type")

        return self._search(
            query=query,
            limit=limit,
            date_from=date_from,
            date_to=date_to,
            article_type=article_type,
        )
