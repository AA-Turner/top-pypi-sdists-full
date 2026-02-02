import requests
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("MedRxivTool")
class MedRxivTool(BaseTool):
    """
    Search medRxiv preprints using medRxiv's API (same interface as bioRxiv).

    Arguments:
        query (str): Search term
        max_results (int): Max results to return (default 10, max 200)
    """

    def __init__(
        self,
        tool_config,
        base_url="https://api.medrxiv.org/details",
    ):
        super().__init__(tool_config)
        self.base_url = base_url

    def run(self, arguments=None):
        arguments = arguments or {}
        query = arguments.get("query")
        max_results = int(arguments.get("max_results", 10))
        if not query:
            return {"error": "`query` parameter is required."}
        return self._search(query, max_results)

    def _search(self, query, max_results):
        # Use date range search for recent preprints
        # Format: /medrxiv/{start_date}/{end_date}/{cursor}/json
        from datetime import datetime, timedelta

        # Search last 365 days to get more comprehensive results
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        url = (
            f"{self.base_url}/medrxiv/"
            f"{start_date.strftime('%Y-%m-%d')}/"
            f"{end_date.strftime('%Y-%m-%d')}/0/json"
        )

        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            return {
                "error": "Network/API error calling medRxiv",
                "reason": str(e),
            }
        except ValueError:
            return {"error": "Failed to decode medRxiv response as JSON"}

        results = []
        # The API returns a dictionary with a 'collection' key
        collection = data.get("collection", [])
        if not isinstance(collection, list):
            return {"error": "Unexpected API response format"}

        for item in collection:
            title = item.get("title")
            authors = item.get("authors", "")
            if isinstance(authors, str):
                authors = [a.strip() for a in authors.split(";") if a.strip()]
            elif isinstance(authors, list):
                authors = [str(a).strip() for a in authors if str(a).strip()]
            else:
                authors = []

            year = None
            date = item.get("date")
            if date and len(date) >= 4 and date[:4].isdigit():
                year = int(date[:4])

            doi = item.get("doi")
            url = f"https://www.medrxiv.org/content/{doi}" if doi else None

            # Filter by query if provided - search in both title and abstract
            if query:
                title_match = query.lower() in (title or "").lower()
                abstract_match = (
                    query.lower() in (item.get("abstract", "") or "").lower()
                )
                if not (title_match or abstract_match):
                    continue

            results.append(
                {
                    "title": title or "Title not available",
                    "authors": (
                        authors if authors else "Author information not available"
                    ),
                    "year": year,
                    "doi": doi or "DOI not available",
                    "url": url or "URL not available",
                    "abstract": item.get("abstract", "Abstract not available"),
                    "source": "medRxiv",
                    "data_quality": {
                        "has_abstract": bool(
                            item.get("abstract")
                            and item.get("abstract") != "Abstract not available"
                        ),
                        "has_authors": bool(authors),
                        "has_year": bool(year),
                        "has_doi": bool(doi),
                        "has_url": bool(url),
                    },
                }
            )

        return results[:max_results]
