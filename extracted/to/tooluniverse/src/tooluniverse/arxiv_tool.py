import requests
import xml.etree.ElementTree as ET
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("ArXivTool")
class ArXivTool(BaseTool):
    """
    Search arXiv for papers by keyword using the public arXiv API.
    """

    def __init__(
        self,
        tool_config,
        base_url="http://export.arxiv.org/api/query",
    ):
        super().__init__(tool_config)
        self.base_url = base_url

    def run(self, arguments):
        query = arguments.get("query")
        limit = int(arguments.get("limit", 10))
        # sort_by: relevance | lastUpdatedDate | submittedDate
        sort_by = arguments.get("sort_by", "relevance")
        # sort_order: ascending | descending
        sort_order = arguments.get("sort_order", "descending")

        if not query:
            return {"error": "`query` parameter is required."}

        return self._search(query, limit, sort_by, sort_order)

    def _search(self, query, limit, sort_by, sort_order):
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max(1, min(limit, 200)),
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=20)
        except requests.RequestException as e:
            return {
                "error": "Network error calling arXiv API",
                "reason": str(e),
            }

        if response.status_code != 200:
            return {
                "error": f"arXiv API error {response.status_code}",
                "reason": response.reason,
            }

        # Parse Atom XML
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            return {
                "error": "Failed to parse arXiv response",
                "reason": str(e),
            }

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = []
        for entry in root.findall("atom:entry", ns):
            title_text = entry.findtext(
                "atom:title",
                default="",
                namespaces=ns,
            )
            title = (title_text or "").strip()
            summary_text = entry.findtext(
                "atom:summary",
                default="",
                namespaces=ns,
            )
            summary = (summary_text or "").strip()
            link_el = entry.find("atom:link[@type='text/html']", ns)
            if link_el is not None:
                link = link_el.get("href")
            else:
                link = entry.findtext("atom:id", default="", namespaces=ns)
            published = entry.findtext("atom:published", default="", namespaces=ns)
            updated = entry.findtext("atom:updated", default="", namespaces=ns)
            authors = [
                a.findtext("atom:name", default="", namespaces=ns)
                for a in entry.findall("atom:author", ns)
            ]
            primary_category = ""
            cat_el = entry.find("{http://arxiv.org/schemas/atom}primary_category")
            if cat_el is not None:
                primary_category = cat_el.get("term", "")

            entries.append(
                {
                    "title": title,
                    "abstract": summary,
                    "authors": authors,
                    "published": published,
                    "updated": updated,
                    "category": primary_category,
                    "url": link,
                }
            )

        return entries
