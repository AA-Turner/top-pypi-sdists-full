"""
CIViC (Clinical Interpretation of Variants in Cancer) API tool for ToolUniverse.

CIViC is a community knowledgebase for expert-curated interpretations of variants
in cancer. It provides clinical evidence levels and interpretations.

API Documentation: https://civicdb.org/api
GraphQL Endpoint: https://civicdb.org/api/graphql
"""

import requests
from typing import Dict, Any, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool

# Base URL for CIViC
CIVIC_BASE_URL = "https://civicdb.org/api"
CIVIC_GRAPHQL_URL = f"{CIVIC_BASE_URL}/graphql"


@register_tool("CIViCTool")
class CIViCTool(BaseTool):
    """
    Tool for querying CIViC (Clinical Interpretation of Variants in Cancer).

    CIViC provides:
    - Expert-curated cancer variant interpretations
    - Clinical evidence levels
    - Drug-variant associations
    - Disease-variant associations

    Uses GraphQL API. No authentication required. Free for academic/research use.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        fields = tool_config.get("fields", {})
        self.query_template: str = fields.get("query", "")
        self.operation_name: Optional[str] = fields.get("operation_name")
        self.timeout: int = tool_config.get("timeout", 30)

    def _build_graphql_query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Build GraphQL query from template and arguments."""
        query = self.query_template

        # GraphQL queries use variables, not string replacement
        # Extract variable names from query (e.g., $limit, $gene_id)
        import re

        var_matches = re.findall(r"\$(\w+)", query)

        # Map arguments to GraphQL variables
        # GraphQL variable names match argument names in our config
        variables = {}
        for var_name in var_matches:
            # Check if argument exists (variable name matches argument name)
            if var_name in arguments:
                variables[var_name] = arguments[var_name]

        payload = {"query": query}

        if self.operation_name:
            payload["operationName"] = self.operation_name

        if variables:
            payload["variables"] = variables

        return payload

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the CIViC GraphQL API call."""
        try:
            # Build GraphQL query
            payload = self._build_graphql_query(arguments)

            # Make GraphQL request
            response = requests.post(
                CIVIC_GRAPHQL_URL,
                json=payload,
                timeout=self.timeout,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "ToolUniverse/CIViC",
                },
            )

            response.raise_for_status()
            data = response.json()

            # Check for GraphQL errors
            if "errors" in data:
                return {
                    "error": "GraphQL query errors",
                    "errors": data["errors"],
                    "query": arguments,
                }

            return {
                "data": data.get("data", {}),
                "metadata": {
                    "source": "CIViC (Clinical Interpretation of Variants in Cancer)",
                    "format": "GraphQL",
                    "endpoint": CIVIC_GRAPHQL_URL,
                },
            }

        except requests.RequestException as e:
            return {"error": f"CIViC API request failed: {str(e)}", "query": arguments}
        except ValueError as e:
            return {"error": str(e), "query": arguments}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "query": arguments}
