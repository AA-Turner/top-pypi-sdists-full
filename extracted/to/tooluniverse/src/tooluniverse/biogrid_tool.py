"""
BioGRID Database REST API Tool

This tool provides access to protein and genetic interaction data from the BioGRID database.
BioGRID is a comprehensive database of physical and genetic interactions.
"""

import requests
from typing import Dict, Any, List
from .base_tool import BaseTool
from .tool_registry import register_tool

BIOGRID_BASE_URL = "https://webservice.thebiogrid.org"


@register_tool("BioGRIDRESTTool")
class BioGRIDRESTTool(BaseTool):
    """
    BioGRID Database REST API tool.
    Generic wrapper for BioGRID API endpoints defined in ppi_tools.json.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        fields = tool_config.get("fields", {})
        parameter = tool_config.get("parameter", {})

        self.endpoint_template: str = fields.get("endpoint", "/interactions/")
        self.required: List[str] = parameter.get("required", [])
        self.output_format: str = fields.get("return_format", "JSON")

    def _build_url(self, arguments: Dict[str, Any]) -> str | Dict[str, Any]:
        """Build URL for BioGRID API request."""
        url_path = self.endpoint_template
        return BIOGRID_BASE_URL + url_path

    def _build_params(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Build parameters for BioGRID API request."""
        params = {"format": "json", "interSpeciesExcluded": "false"}

        # Check for API key
        api_key = arguments.get("api_key") or arguments.get("accesskey")
        if not api_key:
            # Try to get from environment variable
            import os

            api_key = os.getenv("BIOGRID_API_KEY")

        if not api_key:
            raise ValueError(
                "BioGRID API key is required. Please provide 'api_key' parameter "
                "or set BIOGRID_API_KEY environment variable. "
                "Register at: https://webservice.thebiogrid.org/"
            )

        params["accesskey"] = api_key

        # Map gene names to BioGRID format
        if "gene_names" in arguments:
            gene_names = arguments["gene_names"]
            if isinstance(gene_names, list):
                params["geneList"] = "|".join(gene_names)
            else:
                params["geneList"] = str(gene_names)

        # Add other parameters
        if "organism" in arguments:
            # Convert organism name to taxonomy ID
            organism = arguments["organism"]
            if organism.lower() == "homo sapiens":
                params["organism"] = 9606
            elif organism.lower() == "mus musculus":
                params["organism"] = 10090
            else:
                params["organism"] = organism

        if "interaction_type" in arguments:
            interaction_type = arguments["interaction_type"]
            if interaction_type == "physical":
                params["evidenceList"] = "physical"
            elif interaction_type == "genetic":
                params["evidenceList"] = "genetic"
            # "both" means no evidence filter

        if "limit" in arguments:
            params["max"] = arguments["limit"]

        return params

    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a GET request and handle common errors."""
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            if self.output_format == "JSON":
                return response.json()
            else:
                return {"data": response.text}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments."""
        # Validate required parameters
        for param in self.required:
            if param not in arguments:
                return {"error": f"Missing required parameter: {param}"}

        url = self._build_url(arguments)
        if isinstance(url, dict) and "error" in url:
            return url

        params = self._build_params(arguments)
        return self._make_request(url, params)
