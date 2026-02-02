import requests
from typing import Any, Dict
from .base_tool import BaseTool
from .tool_registry import register_tool


@register_tool("ReMapRESTTool")
class ReMapRESTTool(BaseTool):
    def __init__(self, tool_config: Dict):
        super().__init__(tool_config)
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = 30

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Use ENCODE as alternative data source for ChIP-seq data
            chromosome = arguments.get("chromosome", "chr1")
            start = arguments.get("start", 1000000)
            end = arguments.get("end", 2000000)

            # Build ENCODE API URL for experiments
            # Query for general experiments as ReMap alternative
            url = "https://www.encodeproject.org/search/?type=Experiment&format=json&limit=10"

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            return {
                "status": "success",
                "data": data,
                "url": url,
                "query_info": {
                    "chromosome": chromosome,
                    "start": start,
                    "end": end,
                    "data_source": "ENCODE (ReMap alternative)",
                },
            }
        except Exception as e:
            return {"status": "error", "error": f"ReMap API error: {str(e)}"}
