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


def _resolve_gene_id(gene_input: str, base_url: str, timeout: int) -> str:
    """Resolve a gene symbol or unversioned Ensembl ID to a versioned GENCODE ID.

    If already a versioned Ensembl ID (contains '.'), returns as-is.
    Otherwise queries GTEx /reference/gene to resolve.
    """
    if "." in gene_input:
        return gene_input
    url = f"{base_url}/reference/gene?geneId={gene_input}&gencodeVersion=v26"
    try:
        data = _http_get(url, headers={"Accept": "application/json"}, timeout=timeout)
        genes = data.get("data", [])
        if isinstance(genes, list) and genes:
            return genes[0].get("gencodeId", gene_input)
    except Exception:
        pass
    return gene_input


@register_tool(
    "GTExExpressionTool",
    config={
        "name": "GTEx_get_expression_summary",
        "type": "GTExExpressionTool",
        "description": "Get GTEx expression summary for a gene via /expression/geneExpression",
        "parameter": {
            "type": "object",
            "properties": {
                "gene_symbol": {
                    "type": "string",
                    "description": "Gene symbol (e.g., TP53, BRCA1). Auto-resolved to GENCODE ID.",
                },
                "ensembl_gene_id": {
                    "type": "string",
                    "description": "Ensembl gene ID, e.g., ENSG00000141510",
                },
            },
            "required": [],
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

        # Resolve gene symbol or unversioned Ensembl ID to versioned GENCODE ID
        gene_input = arguments.get("gene_symbol") or arguments.get(
            "ensembl_gene_id", ""
        )
        gencode_id = _resolve_gene_id(gene_input, base, timeout)

        # Feature-69A-001: /expression/geneExpression with gtex_v10 returns empty.
        # Use /expression/medianGeneExpression with gtex_v8 for reliable results.
        query = {
            "gencodeId": gencode_id,
            "datasetId": "gtex_v8",
        }
        url = f"{base}/expression/medianGeneExpression?{urlencode(query)}"
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
                "endpoint": "expression/medianGeneExpression",
                "query": query,
                "data": wrapped_data,
                "success": True,
            }
        except Exception as e:
            return {
                "error": str(e),
                "source": "GTEx",
                "endpoint": "expression/medianGeneExpression",
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
                "gene_symbol": {
                    "type": "string",
                    "description": "Gene symbol (e.g., TP53, BRCA1). Auto-resolved to GENCODE ID.",
                },
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
            "required": [],
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

        # Resolve gene symbol or unversioned Ensembl ID to versioned GENCODE ID
        gene_input = arguments.get("gene_symbol") or arguments.get(
            "ensembl_gene_id", ""
        )
        gencode_id = _resolve_gene_id(gene_input, base, timeout)

        query: Dict[str, Any] = {
            "gencodeId": gencode_id,
            "datasetId": arguments.get("dataset_id", "gtex_v10"),
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
