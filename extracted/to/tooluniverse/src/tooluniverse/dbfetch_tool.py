"""
Dbfetch Database Retrieval Tool

This tool provides access to Dbfetch service for retrieving database entries
from multiple databases (UniProt, PDB, etc.) in various formats.
"""

import requests
from typing import Any, Dict
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("DbfetchRESTTool")
class DbfetchRESTTool(BaseTool):
    """
    Dbfetch REST API tool.
    Generic wrapper for Dbfetch API endpoints defined in dbfetch_tools.json.
    """

    def __init__(self, tool_config: Dict):
        super().__init__(tool_config)
        self.base_url = "https://www.ebi.ac.uk/Tools/dbfetch/dbfetch"
        self.session = requests.Session()
        self.session.headers.update({"Accept": "*/*", "User-Agent": "ToolUniverse/1.0"})
        self.timeout = 30

    def _build_url(self, args: Dict[str, Any]) -> str:
        """Build URL from endpoint template and arguments"""
        endpoint_template = self.tool_config["fields"].get("endpoint", "")
        self.tool_config.get("name", "")

        if endpoint_template:
            url = endpoint_template
            for k, v in args.items():
                url = url.replace(f"{{{k}}}", str(v))
            return url

        # Dbfetch uses query parameters, not path parameters
        return self.base_url

    def _build_params(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Build query parameters for Dbfetch API"""
        params = {}
        tool_name = self.tool_config.get("name", "")

        if tool_name == "dbfetch_fetch_entry":
            if "db" in args:
                params["db"] = args["db"]
            if "id" in args:
                params["id"] = args["id"]
            if "format" in args:
                params["format"] = args["format"]
            else:
                params["format"] = "fasta"

        elif tool_name == "dbfetch_fetch_batch":
            if "db" in args:
                params["db"] = args["db"]
            if "ids" in args:
                # Dbfetch expects comma-separated IDs
                if isinstance(args["ids"], list):
                    params["id"] = ",".join(args["ids"])
                else:
                    params["id"] = args["ids"]
            if "format" in args:
                params["format"] = args["format"]
            else:
                params["format"] = "fasta"

        elif tool_name == "dbfetch_list_databases":
            params["style"] = "raw"

        elif tool_name == "dbfetch_list_formats":
            if "db" in args:
                params["db"] = args["db"]
            params["style"] = "raw"

        return params

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Dbfetch API call"""
        try:
            url = self._build_url(arguments)
            params = self._build_params(arguments)
            tool_name = self.tool_config.get("name", "")

            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            # Dbfetch returns text (FASTA, XML, etc.) not JSON
            content_type = response.headers.get("content-type", "")
            if "json" in content_type:
                data = response.json()
            else:
                # Return text content
                data = response.text

            response_data = {
                "status": "success",
                "data": data,
                "url": response.url,
                "content_type": content_type,
            }

            # For batch operations, count entries
            if tool_name == "dbfetch_fetch_batch" and isinstance(data, str):
                # Count entries in FASTA format
                if params.get("format") == "fasta":
                    response_data["count"] = data.count(">")
                # Count entries in other formats
                elif params.get("format") == "xml":
                    response_data["count"] = data.count("<entry")

            return response_data

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": f"Dbfetch API error: {str(e)}",
                "url": url if "url" in locals() else None,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "url": url if "url" in locals() else None,
            }
