import requests
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("OpenAIRETool")
class OpenAIRETool(BaseTool):
    """
    Search OpenAIRE Explore for research products (publications by default).

    Parameters (arguments):
        query (str): Query string
        max_results (int): Max number of results (default 10, max 100)
        type (str): product type filter: publications | datasets | software
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://api.openaire.eu/search/publications"

    def run(self, arguments=None):
        arguments = arguments or {}
        query = arguments.get("query")
        max_results = int(arguments.get("max_results", 10))
        prod_type = arguments.get("type", "publications")

        if not query:
            return {"error": "`query` parameter is required."}

        endpoint = self._endpoint_for_type(prod_type)
        if endpoint is None:
            return {
                "error": ("Unsupported type. Use publications/datasets/software."),
            }

        params = {
            "format": "json",
            "size": max(1, min(max_results, 100)),
            "query": query,
        }
        try:
            resp = requests.get(endpoint, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            return {
                "error": "Network/API error calling OpenAIRE",
                "reason": str(e),
            }
        except ValueError:
            return {"error": "Failed to decode OpenAIRE response as JSON"}

        return self._normalize(data, prod_type)

    def _endpoint_for_type(self, prod_type):
        if prod_type == "publications":
            return "https://api.openaire.eu/search/publications"
        if prod_type == "datasets":
            return "https://api.openaire.eu/search/datasets"
        if prod_type == "software":
            return "https://api.openaire.eu/search/software"
        return None

    def _normalize(self, data, prod_type):
        results = []
        # OpenAIRE JSON has a root 'response' with 'results' → 'result' list
        try:
            items = data.get("response", {}).get("results", {}).get("result", [])
        except Exception:
            items = []

        for it in items:
            # header may contain identifiers, not used presently
            _ = it.get("header", {}) if isinstance(it.get("header"), dict) else {}
            metadata = (
                it.get("metadata", {}) if isinstance(it.get("metadata"), dict) else {}
            )
            title = None
            authors = []
            year = None
            doi = None
            url = None

            # Titles can be nested in 'oaf:result' structure
            result_obj = metadata.get("oaf:result", {})
            if isinstance(result_obj, dict):
                t = result_obj.get("title")
                if isinstance(t, list) and t:
                    title = t[0].get("$")
                elif isinstance(t, dict):
                    title = t.get("$")

                # Authors
                creators = result_obj.get("creator", [])
                if isinstance(creators, list):
                    for c in creators:
                        name = c.get("$")
                        if name:
                            authors.append(name)

                # Year
                date_obj = result_obj.get("dateofacceptance") or result_obj.get("date")
                if isinstance(date_obj, dict):
                    year = date_obj.get("year") or date_obj.get("$")

                # DOI and URL
                pid = result_obj.get("pid", [])
                if isinstance(pid, list):
                    for p in pid:
                        if p.get("@classid") == "doi":
                            doi = p.get("$")
                bestaccessright = result_obj.get("bestaccessright", {})
                if isinstance(bestaccessright, dict):
                    url_value = bestaccessright.get("$")
                    if url_value:
                        url = url_value

            results.append(
                {
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "doi": doi,
                    "url": url,
                    "type": prod_type,
                    "source": "OpenAIRE",
                }
            )

        return results
