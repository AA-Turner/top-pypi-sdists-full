import requests
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("SemanticScholarTool")
class SemanticScholarTool(BaseTool):
    """
    Tool to search for papers on Semantic Scholar including abstracts.
    """

    def __init__(
        self,
        tool_config,
        base_url="https://api.semanticscholar.org/graph/v1/paper/search",
    ):
        super().__init__(tool_config)
        self.base_url = base_url

    def run(self, arguments):
        query = arguments.get("query")
        limit = arguments.get("limit", 5)
        api_key = arguments.get("api_key")
        if not query:
            return {"error": "`query` parameter is required."}
        return self._search(query, limit, api_key)

    def _search(self, query, limit, api_key):
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,abstract,year,venue,url",
        }
        headers = {"x-api-key": api_key} if api_key else {}
        response = requests.get(
            self.base_url, params=params, headers=headers, timeout=20
        )
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "2"))
            import time

            print(
                f"Semantic Scholar API rate limited, waiting {retry_after} seconds..."
            )
            time.sleep(retry_after)
            response = requests.get(
                self.base_url, params=params, headers=headers, timeout=20
            )
        if response.status_code != 200:
            return {
                "error": f"Semantic Scholar API error {response.status_code}",
                "reason": response.reason,
                "suggestion": "API requests too frequent, please try again later or use an API key",
            }
        results = response.json().get("data", [])
        papers = []
        for p in results:
            # Extract basic information
            title = p.get("title")
            abstract = p.get("abstract")
            journal = p.get("venue")
            year = p.get("year")
            url = p.get("url")

            # Handle missing abstract
            if not abstract:
                abstract = "Abstract not available"

            # Handle missing journal information
            if not journal:
                journal = "Journal information not available"

            papers.append(
                {
                    "title": title or "Title not available",
                    "abstract": abstract,
                    "journal": journal,
                    "year": year,
                    "url": url or "URL not available",
                    "data_quality": {
                        "has_abstract": bool(
                            abstract and abstract != "Abstract not available"
                        ),
                        "has_journal": bool(
                            journal and journal != "Journal information not available"
                        ),
                        "has_year": bool(year),
                        "has_url": bool(url and url != "URL not available"),
                    },
                }
            )
        return papers
