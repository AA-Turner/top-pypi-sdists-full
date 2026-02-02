import requests
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("FatcatScholarTool")
class FatcatScholarTool(BaseTool):
    """
    Search Internet Archive Scholar via Fatcat releases search.

    Parameters (arguments):
        query (str): Query string
        max_results (int): Max results (default 10, max 100)
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://api.fatcat.wiki/v0/release/search"

    def run(self, arguments=None):
        arguments = arguments or {}
        query = arguments.get("query")
        max_results = int(arguments.get("max_results", 10))

        if not query:
            return {"error": "`query` parameter is required."}

        params = {
            "q": query,
            "size": max(1, min(max_results, 100)),
        }
        try:
            resp = requests.get(self.base_url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            return {
                "error": "Network/API error calling Fatcat",
                "reason": str(e),
            }
        except ValueError:
            return {"error": "Failed to decode Fatcat response as JSON"}

        results = []
        for r in data.get("hits", {}).get("hits", []):
            src = r.get("_source", {})
            title = src.get("title")
            year = src.get("release_year")
            doi = src.get("doi")
            authors = src.get("contrib_names", [])
            url = None
            if src.get("wikidata_qid"):
                url = f"https://fatcat.wiki/release/{src.get('ident') or ''}"
            results.append(
                {
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "doi": doi,
                    "url": url,
                    "source": "Fatcat/IA Scholar",
                }
            )

        return results
