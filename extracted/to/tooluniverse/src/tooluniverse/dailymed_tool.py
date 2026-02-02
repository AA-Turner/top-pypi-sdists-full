# dailymed_tool.py

import requests
from .base_tool import BaseTool
from .tool_registry import register_tool

DAILYMED_BASE = "https://dailymed.nlm.nih.gov/dailymed/services/v2"


@register_tool("SearchSPLTool")
class SearchSPLTool(BaseTool):
    """
    Search SPL list based on multiple filter conditions (drug_name/ndc/rxcui/setid/published_date).
    Returns original DailyMed API JSON (including metadata + data array).
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = f"{DAILYMED_BASE}/spls.json"

    def run(self, arguments):
        # Extract possible filter conditions from arguments
        params = {}
        # Four common filter fields
        if arguments.get("drug_name"):
            params["drug_name"] = arguments["drug_name"]
        if arguments.get("ndc"):
            params["ndc"] = arguments["ndc"]
        if arguments.get("rxcui"):
            params["rxcui"] = arguments["rxcui"]
        if arguments.get("setid"):
            params["setid"] = arguments["setid"]

        # Published date range filter
        if arguments.get("published_date_gte"):
            params["published_date[gte]"] = arguments["published_date_gte"]
        if arguments.get("published_date_eq"):
            params["published_date[eq]"] = arguments["published_date_eq"]

        # Pagination parameters
        params["pagesize"] = arguments.get("pagesize", 100)
        params["page"] = arguments.get("page", 1)

        # Allow query all if no filter conditions and only pagination provided (be careful with return data volume)
        try:
            resp = requests.get(self.endpoint, params=params, timeout=10)
        except Exception as e:
            return {"error": f"Failed to request DailyMed search_spls: {str(e)}"}

        if resp.status_code != 200:
            return {
                "error": f"DailyMed API access failed, HTTP {resp.status_code}",
                "detail": resp.text,
            }

        try:
            result = resp.json()
        except ValueError:
            return {
                "error": "Unable to parse DailyMed returned JSON.",
                "content": resp.text,
            }

        # Return original JSON, including metadata + data
        return result


@register_tool("GetSPLBySetIDTool")
class GetSPLBySetIDTool(BaseTool):
    """
    Get complete SPL label based on SPL Set ID, returns content in XML or JSON format.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        # Different suffixes for XML and JSON
        self.endpoint_template = f"{DAILYMED_BASE}/spls/{{setid}}.{{fmt}}"

    def run(self, arguments):
        setid = arguments.get("setid")
        fmt = arguments.get("format", "xml")

        # DailyMed single SPL API only supports XML format
        if fmt not in ("xml",):
            return {
                "error": "DailyMed single SPL API only supports 'xml' format, JSON is not supported."
            }

        url = self.endpoint_template.format(setid=setid, fmt=fmt)
        try:
            resp = requests.get(url, timeout=10)
        except Exception as e:
            return {"error": f"Failed to request DailyMed get_spl_by_setid: {str(e)}"}

        if resp.status_code == 404:
            return {"error": f"SPL label not found for Set ID={setid}."}
        elif resp.status_code == 415:
            return {
                "error": f"DailyMed API does not support requested format. Set ID={setid} only supports XML format."
            }
        elif resp.status_code != 200:
            return {
                "error": f"DailyMed API access failed, HTTP {resp.status_code}",
                "detail": resp.text,
            }

        # Return XML content
        return {"xml": resp.text}
