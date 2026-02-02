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
    "GTExExpressionTool",
    config={
        "name": "GTEx_get_expression_summary",
        "type": "GTExExpressionTool",
        "description": "Get GTEx expression summary for a gene via /expression/geneExpression",
        "parameter": {
            "type": "object",
            "properties": {
                "ensembl_gene_id": {
                    "type": "string",
                    "description": "Ensembl gene ID, e.g., ENSG00000141510",
                }
            },
            "required": ["ensembl_gene_id"],
        },
        "settings": {"base_url": "https://gtexportal.org/api/v2", "timeout": 30},
    },
)
class GTExExpressionTool:
    def __init__(self, tool_config=None):
        self.tool_config = tool_config or {}

    def run(self, arguments: Dict[str, Any]):
        base = self.tool_config.get("settings", {}).get(
            "base_url", "https://gtexportal.org/api/v2"
        )
        timeout = int(self.tool_config.get("settings", {}).get("timeout", 30))

        query = {"gencodeId": arguments.get("ensembl_gene_id")}
        url = f"{base}/expression/geneExpression?{urlencode(query)}"
        try:
            api_response = _http_get(
                url, headers={"Accept": "application/json"}, timeout=timeout
            )
            # Wrap API response to match schema: data.geneExpression should be array
            # API returns {"data": [...], "paging_info": {...}}
            # Schema expects {"data": {"geneExpression": [...]}}
            if isinstance(api_response, dict) and "data" in api_response:
                wrapped_data = {"geneExpression": api_response.get("data", [])}
            else:
                # Fallback if response format is unexpected
                wrapped_data = {
                    "geneExpression": (
                        api_response if isinstance(api_response, list) else []
                    )
                }

            return {
                "source": "GTEx",
                "endpoint": "expression/geneExpression",
                "query": query,
                "data": wrapped_data,
                "success": True,
            }
        except Exception as e:
            return {
                "error": str(e),
                "source": "GTEx",
                "endpoint": "expression/geneExpression",
                "success": False,
            }


@register_tool(
    "GTExEQTLTool",
    config={
        "name": "GTEx_query_eqtl",
        "type": "GTExEQTLTool",
        "description": "Query GTEx single-tissue eQTL via /association/singleTissueEqtl",
        "parameter": {
            "type": "object",
            "properties": {
                "ensembl_gene_id": {
                    "type": "string",
                    "description": "Ensembl gene ID, e.g., ENSG00000141510",
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "description": "Page number (1-based)",
                },
                "size": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Page size (1–100)",
                },
            },
            "required": ["ensembl_gene_id"],
        },
        "settings": {"base_url": "https://gtexportal.org/api/v2", "timeout": 30},
    },
)
class GTExEQTLTool:
    def __init__(self, tool_config=None):
        self.tool_config = tool_config or {}

    def run(self, arguments: Dict[str, Any]):
        base = self.tool_config.get("settings", {}).get(
            "base_url", "https://gtexportal.org/api/v2"
        )
        timeout = int(self.tool_config.get("settings", {}).get("timeout", 30))

        query: Dict[str, Any] = {
            "gencodeId": arguments.get("ensembl_gene_id"),
        }
        if "page" in arguments:
            query["page"] = int(arguments["page"])
        if "size" in arguments:
            query["pageSize"] = int(arguments["size"])

        url = f"{base}/association/singleTissueEqtl?{urlencode(query)}"
        try:
            api_response = _http_get(
                url, headers={"Accept": "application/json"}, timeout=timeout
            )
            # Wrap API response to match schema: data.singleTissueEqtl should be array
            # API returns {"data": [...], "paging_info": {...}}
            # Schema expects {"data": {"singleTissueEqtl": [...]}}
            if isinstance(api_response, dict) and "data" in api_response:
                wrapped_data = {"singleTissueEqtl": api_response.get("data", [])}
            else:
                # Fallback if response format is unexpected
                wrapped_data = {
                    "singleTissueEqtl": (
                        api_response if isinstance(api_response, list) else []
                    )
                }

            return {
                "source": "GTEx",
                "endpoint": "association/singleTissueEqtl",
                "query": query,
                "data": wrapped_data,
                "success": True,
            }
        except Exception as e:
            return {
                "error": str(e),
                "source": "GTEx",
                "endpoint": "association/singleTissueEqtl",
                "success": False,
            }
