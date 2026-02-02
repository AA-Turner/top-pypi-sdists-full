import json
from typing import Any, Dict
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from tooluniverse.tool_registry import register_tool


def _http_get(
    url: str,
    headers: Dict[str, str] | None = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        try:
            return json.loads(data.decode("utf-8", errors="ignore"))
        except Exception:
            return {"raw": data.decode("utf-8", errors="ignore")}


@register_tool(
    "GDCCasesTool",
    config={
        "name": "GDC_search_cases",
        "type": "GDCCasesTool",
        "description": "Search NCI GDC cases via /cases",
        "parameter": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "GDC project identifier (e.g., 'TCGA-BRCA')",
                },
                "size": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Number of results (1–100)",
                },
                "offset": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": "Offset for pagination (0-based)",
                },
            },
        },
        "settings": {"base_url": "https://api.gdc.cancer.gov", "timeout": 30},
    },
)
class GDCCasesTool:
    def __init__(self, tool_config=None):
        self.tool_config = tool_config or {}

    def run(self, arguments: Dict[str, Any]):
        base = self.tool_config.get("settings", {}).get(
            "base_url", "https://api.gdc.cancer.gov"
        )
        timeout = int(self.tool_config.get("settings", {}).get("timeout", 30))

        query: Dict[str, Any] = {}
        if arguments.get("project_id"):
            # Build filters JSON for project_id
            filters = {
                "op": "=",
                "content": {
                    "field": "projects.project_id",
                    "value": [arguments["project_id"]],
                },
            }
            query["filters"] = json.dumps(filters)
        if arguments.get("size") is not None:
            query["size"] = int(arguments["size"])
        if arguments.get("offset") is not None:
            query["from"] = int(arguments["offset"])

        url = f"{base}/cases?{urlencode(query)}"
        try:
            data = _http_get(
                url, headers={"Accept": "application/json"}, timeout=timeout
            )
            return {
                "source": "GDC",
                "endpoint": "cases",
                "query": query,
                "data": data,
                "success": True,
            }
        except Exception as e:
            return {
                "error": str(e),
                "source": "GDC",
                "endpoint": "cases",
                "success": False,
            }


@register_tool(
    "GDCFilesTool",
    config={
        "name": "GDC_list_files",
        "type": "GDCFilesTool",
        "description": "List NCI GDC files via /files with optional data_type filter",
        "parameter": {
            "type": "object",
            "properties": {
                "data_type": {
                    "type": "string",
                    "description": "Data type filter (e.g., 'Gene Expression Quantification')",
                },
                "size": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Number of results (1–100)",
                },
                "offset": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": "Offset for pagination (0-based)",
                },
            },
        },
        "settings": {"base_url": "https://api.gdc.cancer.gov", "timeout": 30},
    },
)
class GDCFilesTool:
    def __init__(self, tool_config=None):
        self.tool_config = tool_config or {}

    def run(self, arguments: Dict[str, Any]):
        base = self.tool_config.get("settings", {}).get(
            "base_url", "https://api.gdc.cancer.gov"
        )
        timeout = int(self.tool_config.get("settings", {}).get("timeout", 30))

        query: Dict[str, Any] = {}
        if arguments.get("data_type"):
            filters = {
                "op": "=",
                "content": {
                    "field": "files.data_type",
                    "value": [arguments["data_type"]],
                },
            }
            query["filters"] = json.dumps(filters)
        if arguments.get("size") is not None:
            query["size"] = int(arguments["size"])
        if arguments.get("offset") is not None:
            query["from"] = int(arguments["offset"])

        url = f"{base}/files?{urlencode(query)}"
        try:
            data = _http_get(
                url, headers={"Accept": "application/json"}, timeout=timeout
            )
            return {
                "source": "GDC",
                "endpoint": "files",
                "query": query,
                "data": data,
                "success": True,
            }
        except Exception as e:
            return {
                "error": str(e),
                "source": "GDC",
                "endpoint": "files",
                "success": False,
            }
