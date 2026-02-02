"""
STRING Database REST API Tool

This tool provides access to protein-protein interaction data from the STRING
database. STRING is a database of known and predicted protein-protein
interactions.
"""

import requests
from typing import Dict, Any, List
from .base_tool import BaseTool
from .tool_registry import register_tool

STRING_BASE_URL = "https://string-db.org/api"


@register_tool("STRINGRESTTool")
class STRINGRESTTool(BaseTool):
    """
    STRING Database REST API tool.
    Generic wrapper for STRING API endpoints defined in ppi_tools.json.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        fields = tool_config.get("fields", {})
        parameter = tool_config.get("parameter", {})

        self.endpoint_template: str = fields.get("endpoint", "/tsv/network")
        self.required: List[str] = parameter.get("required", [])
        self.output_format: str = fields.get("return_format", "TSV")

    def _build_url(self, arguments: Dict[str, Any]) -> str | Dict[str, Any]:
        """Build URL for STRING API request."""
        url_path = self.endpoint_template
        return STRING_BASE_URL + url_path

    def _build_params(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Build parameters for STRING API request."""
        params = {}

        # Map protein IDs to STRING format
        if "protein_ids" in arguments:
            protein_ids = arguments["protein_ids"]
            if isinstance(protein_ids, list):
                params["identifiers"] = "\r".join(protein_ids)
            else:
                params["identifiers"] = str(protein_ids)

        # Add other parameters
        if "species" in arguments:
            params["species"] = arguments["species"]
        if "confidence_score" in arguments:
            params["required_score"] = int(arguments["confidence_score"] * 1000)
        if "limit" in arguments:
            params["limit"] = arguments["limit"]
        if "network_type" in arguments:
            params["network_type"] = arguments["network_type"]

        return params

    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a GET request and handle common errors."""
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            if self.output_format == "TSV":
                return self._parse_tsv_response(response.text)
            else:
                return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def _parse_tsv_response(self, text: str) -> Dict[str, Any]:
        """Parse TSV response from STRING API."""
        lines = text.strip().split("\n")
        if len(lines) < 2:
            return {"data": [], "error": "No data returned"}

        # Parse header
        header = lines[0].split("\t")

        # Parse data rows
        data = []
        for line in lines[1:]:
            if line.strip():
                values = line.split("\t")
                row = {}
                for i, value in enumerate(values):
                    if i < len(header):
                        row[header[i]] = value
                data.append(row)

        return {"data": data, "header": header}

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
