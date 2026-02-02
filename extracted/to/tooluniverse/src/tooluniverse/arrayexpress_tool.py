"""
ArrayExpress Database Tool

This tool provides access to the ArrayExpress database for functional genomics
experiments including microarray and RNA-seq data.
"""

import requests
from typing import Any, Dict, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("ArrayExpressRESTTool")
class ArrayExpressRESTTool(BaseTool):
    """
    ArrayExpress REST API tool.
    Generic wrapper for ArrayExpress API endpoints defined in arrayexpress_tools.json.
    """

    def __init__(self, tool_config: Dict):
        super().__init__(tool_config)
        self.base_url = "https://www.ebi.ac.uk/arrayexpress/json/v3"
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "User-Agent": "ToolUniverse/1.0"}
        )
        self.timeout = 30

    def _build_url(self, args: Dict[str, Any]) -> str:
        """Build URL from endpoint template and arguments"""
        endpoint_template = self.tool_config["fields"].get("endpoint", "")
        tool_name = self.tool_config.get("name", "")

        if endpoint_template:
            url = endpoint_template
            for k, v in args.items():
                url = url.replace(f"{{{k}}}", str(v))
            return url

        if tool_name == "arrayexpress_search_experiments":
            return f"{self.base_url}/experiments"

        elif tool_name == "arrayexpress_get_experiment":
            experiment_id = args.get("experiment_id", "")
            if experiment_id:
                return f"{self.base_url}/experiments/{experiment_id}"

        elif tool_name == "arrayexpress_get_experiment_files":
            experiment_id = args.get("experiment_id", "")
            if experiment_id:
                return f"{self.base_url}/experiments/{experiment_id}/files"

        elif tool_name == "arrayexpress_get_experiment_samples":
            experiment_id = args.get("experiment_id", "")
            if experiment_id:
                return f"{self.base_url}/experiments/{experiment_id}/samples"

        return self.base_url

    def _build_params(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Build query parameters for ArrayExpress API"""
        params = {}
        tool_name = self.tool_config.get("name", "")

        if tool_name == "arrayexpress_search_experiments":
            if "keywords" in args:
                params["keywords"] = args["keywords"]
            if "species" in args:
                params["species"] = args["species"]
            if "array" in args:
                params["array"] = args["array"]
            if "limit" in args:
                params["limit"] = args["limit"]
            if "offset" in args:
                params["offset"] = args["offset"]

        return params

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the ArrayExpress API call"""
        try:
            url = self._build_url(arguments)
            params = self._build_params(arguments)

            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            # ArrayExpress may return HTML or other formats
            content_type = response.headers.get("content-type", "")
            if "json" not in content_type.lower():
                # Try to parse as JSON anyway, or return text
                try:
                    data = response.json()
                except Exception:
                    return {
                        "status": "error",
                        "error": f"ArrayExpress API returned non-JSON content: {content_type}",
                        "url": response.url,
                        "note": "ArrayExpress API may have changed or endpoint may not be available",
                    }
            else:
                data = response.json()

            response_data = {
                "status": "success",
                "data": data,
                "url": response.url,
            }

            if isinstance(data, dict):
                if "experiments" in data and isinstance(data["experiments"], list):
                    response_data["count"] = len(data["experiments"])
                elif "experiment" in data:
                    response_data["count"] = 1
            elif isinstance(data, list):
                response_data["count"] = len(data)

            return response_data

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": f"ArrayExpress API error: {str(e)}",
                "url": url if "url" in locals() else None,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "url": url if "url" in locals() else None,
            }
